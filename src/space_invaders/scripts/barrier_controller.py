"""BarrierController: destructible shield with per-cell damage."""

from __future__ import annotations

import random

import pygame

from space_invaders.components.box_collider_2d import BoxCollider2D
from space_invaders.components.sprite_renderer import SpriteRenderer
from space_invaders.core.mono_behaviour import MonoBehaviour
from space_invaders.core.physics_2d import Physics2D
from space_invaders.scripts.audio_manager import AudioManager
from space_invaders.settings import (
    BARRIER_BLAST_RADIUS,
    BARRIER_CELL,
    BARRIER_COLS,
    BARRIER_ROWS,
    COLOR_GREEN,
    TAG_BULLET_E,
    TAG_BULLET_P,
)


def _build_mask() -> list[list[bool]]:
    """Classic bunker shape: sloped top corners and a bottom-center notch."""
    cells = [[True] * BARRIER_COLS for _ in range(BARRIER_ROWS)]
    for row in range(4):
        cut = 4 - row
        for col in range(BARRIER_COLS):
            if col < cut or col >= BARRIER_COLS - cut:
                cells[row][col] = False
    for row in range(BARRIER_ROWS - 4, BARRIER_ROWS):
        half = 3 + (row - (BARRIER_ROWS - 4))
        for col in range(BARRIER_COLS // 2 - half, BARRIER_COLS // 2 + half):
            cells[row][col] = False
    return cells


class BarrierController(MonoBehaviour):
    """Destructible shield: a 2D boolean cell grid redrawn on damage.

    Bullets are detected by polling Physics2D.overlap_box each frame instead
    of trigger events, so shots pass through cells already eroded away.
    """

    def awake(self) -> None:
        self.cells = _build_mask()
        self._surface = pygame.Surface(
            (BARRIER_COLS * BARRIER_CELL, BARRIER_ROWS * BARRIER_CELL),
            pygame.SRCALPHA,
        )
        self._redraw()

    def start(self) -> None:
        renderer = self.game_object.get_component(SpriteRenderer)
        renderer.surface = self._surface
        self._collider = self.game_object.get_component(BoxCollider2D)
        self._collider.size = pygame.Vector2(self._surface.get_size())

    def update(self, delta_time: float) -> None:
        own_rect = self._collider.rect
        for bullet in Physics2D.overlap_box(own_rect):
            if bullet.tag not in (TAG_BULLET_P, TAG_BULLET_E):
                continue
            if bullet.game_object.destroyed:
                continue
            if self._damage(bullet.rect, from_top=bullet.tag == TAG_BULLET_E):
                bullet.game_object.destroy()
                if AudioManager.instance:
                    AudioManager.instance.play("barrier_hit")

    def _damage(self, bullet_rect: pygame.Rect, from_top: bool) -> bool:
        """Erodes cells around the impact point.

        Args:
            bullet_rect: World-space rect of the bullet.
            from_top: True for enemy bullets (impact scanned top-down).

        Returns:
            True if any solid cell was hit (bullet should be destroyed).
        """
        own = self._collider.rect
        col_lo = max(0, (bullet_rect.left - own.left) // BARRIER_CELL)
        col_hi = min(BARRIER_COLS - 1, (bullet_rect.right - own.left) // BARRIER_CELL)
        rows = range(BARRIER_ROWS) if from_top else range(BARRIER_ROWS - 1, -1, -1)
        impact: tuple[int, int] | None = None
        for row in rows:
            for col in range(col_lo, col_hi + 1):
                if self.cells[row][col]:
                    impact = (row, col)
                    break
            if impact:
                break
        if impact is None:
            return False
        impact_row, impact_col = impact
        radius = BARRIER_BLAST_RADIUS
        for row in range(impact_row - radius - 1, impact_row + radius + 2):
            for col in range(impact_col - radius - 1, impact_col + radius + 2):
                if not (0 <= row < BARRIER_ROWS and 0 <= col < BARRIER_COLS):
                    continue
                dist = abs(row - impact_row) + abs(col - impact_col)
                if dist <= radius or (dist == radius + 1 and random.random() < 0.5):
                    self.cells[row][col] = False
        self._redraw()
        return True

    def _redraw(self) -> None:
        self._surface.fill((0, 0, 0, 0))
        for row in range(BARRIER_ROWS):
            for col in range(BARRIER_COLS):
                if self.cells[row][col]:
                    self._surface.fill(
                        COLOR_GREEN,
                        (
                            col * BARRIER_CELL,
                            row * BARRIER_CELL,
                            BARRIER_CELL,
                            BARRIER_CELL,
                        ),
                    )
