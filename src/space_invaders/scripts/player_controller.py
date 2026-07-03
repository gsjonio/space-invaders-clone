"""PlayerController: movement, shooting, and hit handling."""

from __future__ import annotations

import pygame

from space_invaders.components.box_collider_2d import BoxCollider2D
from space_invaders.components.sprite_renderer import SpriteRenderer
from space_invaders.core.input_manager import Input
from space_invaders.core.mono_behaviour import MonoBehaviour
from space_invaders.scripts.audio_manager import AudioManager
from space_invaders.scripts.game_manager import GameManager
from space_invaders.settings import (
    BULLET_SPEED_PLAYER,
    COLOR_CYAN,
    PLAYER_MARGIN_X,
    PLAYER_SHOOT_COOLDOWN,
    PLAYER_SPEED,
    PLAYER_SPRITE_CELL,
    SCREEN_WIDTH,
    TAG_BULLET_E,
    TAG_BULLET_P,
)
from space_invaders.utils.sprite_utils import build_sprite

PLAYER_SPRITE = [
    "0000001000000",
    "0000011100000",
    "0000011100000",
    "0111111111110",
    "1111111111111",
    "1111111111111",
    "1111111111111",
    "1111111111111",
]


class PlayerController(MonoBehaviour):
    """Handles horizontal movement, shooting with cooldown, and enemy-bullet hits."""

    def awake(self) -> None:
        self._surface = build_sprite(PLAYER_SPRITE, COLOR_CYAN, PLAYER_SPRITE_CELL)
        self._cooldown = 0.0

    def start(self) -> None:
        renderer = self.game_object.get_component(SpriteRenderer)
        renderer.surface = self._surface
        collider = self.game_object.get_component(BoxCollider2D)
        collider.size = pygame.Vector2(self._surface.get_size())

    def update(self, delta_time: float) -> None:
        transform = self.game_object.transform
        direction = 0.0
        if Input.get_key(pygame.K_LEFT):
            direction -= 1.0
        if Input.get_key(pygame.K_RIGHT):
            direction += 1.0
        transform.translate(pygame.Vector2(direction * PLAYER_SPEED * delta_time, 0))
        transform.position.x = max(
            PLAYER_MARGIN_X, min(SCREEN_WIDTH - PLAYER_MARGIN_X, transform.position.x)
        )

        self._cooldown -= delta_time
        if (
            Input.get_key_down(pygame.K_SPACE)
            and delta_time > 0.0  # ignore input while paused
            and self._cooldown <= 0.0
            and self.game_object.scene.find_object_with_tag(TAG_BULLET_P) is None
        ):
            self._shoot()

    def _shoot(self) -> None:
        from space_invaders.prefabs.bullet_prefab import create_bullet

        scene = self.game_object.scene
        position = self.game_object.transform.position + pygame.Vector2(0, -16)
        scene.instantiate(
            create_bullet(position, -1, BULLET_SPEED_PLAYER, TAG_BULLET_P, scene)
        )
        self._cooldown = PLAYER_SHOOT_COOLDOWN
        if AudioManager.instance:
            AudioManager.instance.play("shoot")

    def on_trigger_enter_2d(self, other: BoxCollider2D) -> None:
        if other.tag == TAG_BULLET_E and GameManager.instance:
            GameManager.instance.player_hit()
