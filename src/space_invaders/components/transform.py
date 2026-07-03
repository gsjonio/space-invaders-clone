"""Transform component: position, rotation, scale."""

import pygame

from space_invaders.core.mono_behaviour import MonoBehaviour


class Transform(MonoBehaviour):
    """Holds position, rotation, and scale.

    Every GameObject has exactly one Transform, attached automatically at
    construction. Mirrors Unity's Transform component.

    Attributes:
        position: World position in pixels (sprite center).
        rotation: Degrees, clockwise. (Not applied by SpriteRenderer —
            nothing in this game rotates.)
        scale: (1.0, 1.0) = no scale.
    """

    def __init__(self) -> None:
        self.position = pygame.Vector2(0.0, 0.0)
        self.rotation = 0.0
        self.scale = pygame.Vector2(1.0, 1.0)

    def translate(self, delta: pygame.Vector2) -> None:
        """Moves the object by delta in world space."""
        self.position += delta
