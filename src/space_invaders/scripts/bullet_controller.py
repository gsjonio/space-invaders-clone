"""BulletController: vertical movement and self-destruction."""

from __future__ import annotations

import pygame

from space_invaders.components.box_collider_2d import BoxCollider2D
from space_invaders.core.mono_behaviour import MonoBehaviour
from space_invaders.settings import SCREEN_HEIGHT


class BulletController(MonoBehaviour):
    """Moves a bullet vertically; destroys it off-screen or on any trigger hit.

    Barriers are not part of the trigger matrix — BarrierController polls
    bullets itself so shots can fly through already-eroded holes.
    """

    def __init__(self, direction: int, speed: float) -> None:
        """Args:
        direction: +1 moves down (enemy), -1 moves up (player).
        speed: Pixels per second.
        """
        self.direction = direction
        self.speed = speed

    def update(self, delta_time: float) -> None:
        transform = self.game_object.transform
        transform.translate(pygame.Vector2(0, self.direction * self.speed * delta_time))
        if transform.position.y < -20 or transform.position.y > SCREEN_HEIGHT + 20:
            self.game_object.destroy()

    def on_trigger_enter_2d(self, other: BoxCollider2D) -> None:
        # The other side (invader, player, UFO) handles its own damage.
        self.game_object.destroy()
