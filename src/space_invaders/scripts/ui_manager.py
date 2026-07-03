"""UIManager: HUD with score, hi-score, lives, and wave number."""

from __future__ import annotations

import pygame

from space_invaders.components.sprite_renderer import SpriteRenderer
from space_invaders.core.mono_behaviour import MonoBehaviour
from space_invaders.core.time_manager import Time
from space_invaders.scripts.game_manager import GameManager
from space_invaders.scripts.player_controller import PLAYER_SPRITE
from space_invaders.settings import (
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_WHITE,
    COLOR_YELLOW,
    LAYER_UI,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UI_FONT_SIZE,
    UI_MARGIN,
)
from space_invaders.utils.sprite_utils import build_sprite, render_text


class UIManager(MonoBehaviour):
    """Redraws the HUD surface only when the displayed values change."""

    def awake(self) -> None:
        self._surface = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        self._life_icon = build_sprite(PLAYER_SPRITE, COLOR_CYAN, 1)
        self._cache: tuple | None = None

    def start(self) -> None:
        renderer = self.game_object.get_component(SpriteRenderer)
        renderer.surface = self._surface
        renderer.layer_order = LAYER_UI
        self.game_object.transform.position = pygame.Vector2(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
        )

    def update(self, delta_time: float) -> None:
        manager = GameManager.instance
        if manager is None:
            return
        state = (
            manager.score,
            GameManager.hi_score,
            manager.lives,
            manager.wave,
            Time.time_scale == 0.0,
        )
        if state != self._cache:
            self._cache = state
            self._redraw(*state)

    def _redraw(
        self, score: int, hi_score: int, lives: int, wave: int, paused: bool
    ) -> None:
        surface = self._surface
        surface.fill((0, 0, 0, 0))
        surface.blit(
            render_text(f"SCORE {score:05d}", UI_FONT_SIZE, COLOR_WHITE),
            (UI_MARGIN, UI_MARGIN),
        )
        hi_text = render_text(f"HI-SCORE {hi_score:05d}", UI_FONT_SIZE, COLOR_YELLOW)
        surface.blit(
            hi_text, ((SCREEN_WIDTH - hi_text.get_width()) / 2, UI_MARGIN)
        )
        wave_text = render_text(f"WAVE {wave}", UI_FONT_SIZE, COLOR_WHITE)
        surface.blit(
            wave_text, (SCREEN_WIDTH - wave_text.get_width() - UI_MARGIN, UI_MARGIN)
        )
        # Floor line + lives as small ship icons, classic style.
        pygame.draw.line(
            surface,
            COLOR_GREEN,
            (0, SCREEN_HEIGHT - 24),
            (SCREEN_WIDTH, SCREEN_HEIGHT - 24),
        )
        surface.blit(
            render_text(str(lives), UI_FONT_SIZE, COLOR_WHITE),
            (UI_MARGIN, SCREEN_HEIGHT - 21),
        )
        for i in range(max(0, lives - 1)):
            surface.blit(
                self._life_icon, (UI_MARGIN + 25 + i * 20, SCREEN_HEIGHT - 17)
            )
        if paused:
            pause_text = render_text("PAUSED", UI_FONT_SIZE * 2, COLOR_YELLOW)
            surface.blit(
                pause_text,
                (
                    (SCREEN_WIDTH - pause_text.get_width()) / 2,
                    (SCREEN_HEIGHT - pause_text.get_height()) / 2,
                ),
            )
