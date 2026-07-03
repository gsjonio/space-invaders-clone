"""UfoController: bonus UFO spawner and mover."""

from __future__ import annotations

import random

import pygame

from space_invaders.components.box_collider_2d import BoxCollider2D
from space_invaders.components.sprite_renderer import SpriteRenderer
from space_invaders.core.mono_behaviour import MonoBehaviour
from space_invaders.scripts.audio_manager import AudioManager
from space_invaders.scripts.game_manager import GameManager
from space_invaders.settings import (
    COLOR_RED,
    SCREEN_WIDTH,
    TAG_BULLET_P,
    UFO_POINTS,
    UFO_SPAWN_INTERVAL,
    UFO_SPEED,
    UFO_Y,
)
from space_invaders.utils.sprite_utils import build_sprite

UFO_SPRITE = [
    "0000011111100000",
    "0001111111111000",
    "0011111111111100",
    "0110110110110110",
    "1111111111111111",
    "0011100110011100",
    "0001000000001000",
]


class UfoController(MonoBehaviour):
    """Single persistent GameObject: idles offscreen, crosses the top every
    UFO_SPAWN_INTERVAL seconds, awards a random UFO_POINTS value when shot."""

    def awake(self) -> None:
        self._surface = build_sprite(UFO_SPRITE, COLOR_RED)
        self._timer = UFO_SPAWN_INTERVAL
        self._flying = False
        self._direction = 1

    def start(self) -> None:
        self._renderer = self.game_object.get_component(SpriteRenderer)
        self._renderer.surface = self._surface
        self._renderer.visible = False
        self._collider = self.game_object.get_component(BoxCollider2D)
        self._collider.size = pygame.Vector2(self._surface.get_size())
        self._collider.enabled = False
        self.game_object.transform.position = pygame.Vector2(-100, UFO_Y)

    def update(self, delta_time: float) -> None:
        if delta_time <= 0.0:
            return
        if not self._flying:
            self._timer -= delta_time
            if self._timer <= 0.0:
                self._spawn()
            return
        transform = self.game_object.transform
        transform.translate(
            pygame.Vector2(self._direction * UFO_SPEED * delta_time, 0)
        )
        if transform.position.x < -60 or transform.position.x > SCREEN_WIDTH + 60:
            self._despawn()

    def _spawn(self) -> None:
        self._direction = random.choice([-1, 1])
        start_x = -50 if self._direction > 0 else SCREEN_WIDTH + 50
        self.game_object.transform.position = pygame.Vector2(start_x, UFO_Y)
        self._flying = True
        self._renderer.visible = True
        self._collider.enabled = True
        if AudioManager.instance:
            AudioManager.instance.play_loop("ufo_loop")

    def _despawn(self) -> None:
        self._flying = False
        self._timer = UFO_SPAWN_INTERVAL
        self._renderer.visible = False
        self._collider.enabled = False
        self.game_object.transform.position = pygame.Vector2(-100, UFO_Y)
        if AudioManager.instance:
            AudioManager.instance.stop("ufo_loop")

    def on_trigger_enter_2d(self, other: BoxCollider2D) -> None:
        if other.tag != TAG_BULLET_P or not self._flying:
            return
        if GameManager.instance:
            GameManager.instance.enemy_killed(random.choice(UFO_POINTS))
        if AudioManager.instance:
            AudioManager.instance.play("explosion_invader")
        self._despawn()
