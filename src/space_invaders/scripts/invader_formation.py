"""InvaderFormation: spawns and marches the invader grid."""

from __future__ import annotations

import random

import pygame

from space_invaders.core.mono_behaviour import MonoBehaviour
from space_invaders.scripts.audio_manager import AudioManager
from space_invaders.scripts.game_manager import GameManager
from space_invaders.scripts.invader_controller import InvaderController
from space_invaders.settings import (
    BULLET_SPEED_ENEMY,
    INVADER_BASE_INTERVAL,
    INVADER_COLS,
    INVADER_EDGE_MARGIN,
    INVADER_H_SPACING,
    INVADER_LOSE_Y,
    INVADER_MIN_INTERVAL,
    INVADER_ROWS,
    INVADER_SHOOT_CHANCE,
    INVADER_START_Y,
    INVADER_STEP_DOWN,
    INVADER_STEP_X,
    INVADER_V_SPACING,
    INVADER_WAVE_SPEEDUP,
    SCREEN_WIDTH,
    TAG_BULLET_E,
)

# Row (top to bottom) -> invader_type: squid, crab, crab, octopus, octopus.
_ROW_TYPES = [2, 1, 1, 0, 0]


class InvaderFormation(MonoBehaviour):
    """Grid of invaders: step-march with speed escalation, random shots,
    win/lose detection."""

    def __init__(self, wave: int = 1) -> None:
        """Args:
        wave: Current wave; higher waves march faster from the start.
        """
        self.wave = wave
        self._invaders: list[InvaderController] = []
        self._direction = 1
        self._march_beat = 0
        self._total = INVADER_ROWS * INVADER_COLS
        self._base_interval = max(
            INVADER_MIN_INTERVAL,
            INVADER_BASE_INTERVAL * INVADER_WAVE_SPEEDUP ** (wave - 1),
        )
        self._timer = self._base_interval

    def start(self) -> None:
        from space_invaders.prefabs.invader_prefab import create_invader

        scene = self.game_object.scene
        grid_width = (INVADER_COLS - 1) * INVADER_H_SPACING
        x0 = (SCREEN_WIDTH - grid_width) / 2
        for row in range(INVADER_ROWS):
            for col in range(INVADER_COLS):
                position = pygame.Vector2(
                    x0 + col * INVADER_H_SPACING,
                    INVADER_START_Y + row * INVADER_V_SPACING,
                )
                go = scene.instantiate(
                    create_invader(position, _ROW_TYPES[row], self, scene)
                )
                self._invaders.append(go.get_component(InvaderController))

    def update(self, delta_time: float) -> None:
        if delta_time <= 0.0 or not self._invaders:
            return
        for invader in self._invaders:
            if random.random() < INVADER_SHOOT_CHANCE:
                self._shoot_from(invader)
        self._timer -= delta_time
        if self._timer <= 0.0:
            self._step()
            self._timer = self._interval()

    def notify_death(self, invader: InvaderController) -> None:
        """Removes a dead invader; triggers wave-cleared when none remain."""
        if invader in self._invaders:
            self._invaders.remove(invader)
        if not self._invaders and GameManager.instance:
            GameManager.instance.wave_cleared()

    def _interval(self) -> float:
        alive = len(self._invaders)
        return max(INVADER_MIN_INTERVAL, self._base_interval * alive / self._total)

    def _step(self) -> None:
        xs = [inv.game_object.transform.position.x for inv in self._invaders]
        at_edge = (
            self._direction > 0
            and max(xs) + INVADER_STEP_X > SCREEN_WIDTH - INVADER_EDGE_MARGIN
        ) or (
            self._direction < 0 and min(xs) - INVADER_STEP_X < INVADER_EDGE_MARGIN
        )
        if at_edge:
            delta = pygame.Vector2(0, INVADER_STEP_DOWN)
            self._direction *= -1
        else:
            delta = pygame.Vector2(self._direction * INVADER_STEP_X, 0)
        for invader in self._invaders:
            invader.game_object.transform.translate(delta)
            invader.toggle_frame()
        if AudioManager.instance:
            AudioManager.instance.play(f"march_{self._march_beat + 1}")
        self._march_beat = (self._march_beat + 1) % 4
        if at_edge and GameManager.instance:
            lowest = max(
                inv.game_object.transform.position.y for inv in self._invaders
            )
            if lowest > INVADER_LOSE_Y:
                GameManager.instance.game_over()

    def _shoot_from(self, invader: InvaderController) -> None:
        from space_invaders.prefabs.bullet_prefab import create_bullet

        scene = self.game_object.scene
        position = invader.game_object.transform.position + pygame.Vector2(0, 20)
        scene.instantiate(
            create_bullet(position, 1, BULLET_SPEED_ENEMY, TAG_BULLET_E, scene)
        )
