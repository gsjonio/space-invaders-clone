"""BoxCollider2D component: axis-aligned bounding box collider."""

import pygame

from space_invaders.core.mono_behaviour import MonoBehaviour
from space_invaders.core.physics_2d import Physics2D


class BoxCollider2D(MonoBehaviour):
    """Axis-aligned bounding box collider. Mirrors Unity's BoxCollider2D.

    Registers itself with Physics2D on awake and unregisters on destroy.

    Attributes:
        size: Collider dimensions in pixels.
        offset: Offset from transform.position (the sprite center).
        is_trigger: If True, fires on_trigger_enter_2d instead of collision.
        enabled: Disabled colliders are ignored by all physics queries.
    """

    def __init__(
        self,
        size: pygame.Vector2,
        offset: pygame.Vector2 | None = None,
        is_trigger: bool = True,
    ) -> None:
        self.size = pygame.Vector2(size)
        self.offset = pygame.Vector2(offset) if offset is not None else pygame.Vector2()
        self.is_trigger = is_trigger
        self.enabled = True

    def awake(self) -> None:
        Physics2D.register_collider(self)

    def on_destroy(self) -> None:
        Physics2D.unregister_collider(self)

    @property
    def rect(self) -> pygame.Rect:
        """Current world-space rect derived from transform.position + offset."""
        center = self.game_object.transform.position + self.offset
        rect = pygame.Rect(0, 0, int(self.size.x), int(self.size.y))
        rect.center = (int(center.x), int(center.y))
        return rect

    @property
    def tag(self) -> str:
        """Shortcut to game_object.tag."""
        return self.game_object.tag
