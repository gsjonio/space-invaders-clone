"""SpriteRenderer component: draws a surface at the Transform's position."""

import pygame

from space_invaders.core.mono_behaviour import MonoBehaviour
from space_invaders.settings import COLOR_WHITE


class SpriteRenderer(MonoBehaviour):
    """Renders a pygame.Surface centered on the Transform's position.

    Mirrors Unity's SpriteRenderer.

    Attributes:
        surface: The cached sprite surface (created once, e.g. in awake()).
        color: Informational tint color (surfaces are pre-colored).
        visible: If False, draw() is a no-op.
        layer_order: Higher = drawn on top.
        flip_x: Mirror horizontally at draw time.
        flip_y: Mirror vertically at draw time.
    """

    def __init__(
        self,
        surface: pygame.Surface | None = None,
        layer_order: int = 0,
        color: tuple[int, int, int] = COLOR_WHITE,
    ) -> None:
        self.surface = surface
        self.color = color
        self.visible = True
        self.layer_order = layer_order
        self.flip_x = False
        self.flip_y = False

    def draw(self, screen: pygame.Surface) -> None:
        """Blits the surface centered on transform.position."""
        if not self.visible or self.surface is None:
            return
        surface = self.surface
        if self.flip_x or self.flip_y:
            surface = pygame.transform.flip(surface, self.flip_x, self.flip_y)
        rect = surface.get_rect(center=self.game_object.transform.position)
        screen.blit(surface, rect)
