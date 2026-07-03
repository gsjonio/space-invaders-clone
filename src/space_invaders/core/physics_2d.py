"""Physics2D: static 2D collision-query class, mirroring Unity's Physics2D."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from space_invaders.settings import (
    TAG_BULLET_E,
    TAG_BULLET_P,
    TAG_ENEMY,
    TAG_PLAYER,
    TAG_UFO,
)

if TYPE_CHECKING:
    from space_invaders.components.box_collider_2d import BoxCollider2D

# Only these pairs generate trigger events (spatial-partitioning hint from the
# spec: bullets vs their valid targets; barriers poll overlap_box themselves).
COLLISION_MATRIX: dict[str, set[str]] = {
    TAG_BULLET_P: {TAG_ENEMY, TAG_UFO},
    TAG_BULLET_E: {TAG_PLAYER},
}


class Physics2D:
    """Static class for 2D collision queries, mirroring Unity's Physics2D."""

    _colliders: list["BoxCollider2D"] = []
    _overlaps: set[tuple[int, int]] = set()

    @classmethod
    def register_collider(cls, collider: "BoxCollider2D") -> None:
        """Adds a collider to the physics world."""
        if collider not in cls._colliders:
            cls._colliders.append(collider)

    @classmethod
    def unregister_collider(cls, collider: "BoxCollider2D") -> None:
        """Removes a collider from the physics world (no-op if absent)."""
        if collider in cls._colliders:
            cls._colliders.remove(collider)

    @classmethod
    def clear(cls) -> None:
        """Removes all colliders and overlap memory (scene unload / tests)."""
        cls._colliders.clear()
        cls._overlaps.clear()

    @classmethod
    def _active_colliders(cls) -> list["BoxCollider2D"]:
        return [
            c
            for c in cls._colliders
            if c.enabled and c.game_object.active and not c.game_object.destroyed
        ]

    @classmethod
    def check_all_overlaps(cls) -> None:
        """Called once per frame. Fires on_trigger_enter_2d on new overlapping pairs."""
        active = cls._active_colliders()
        current: set[tuple[int, int]] = set()
        for a in active:
            targets = COLLISION_MATRIX.get(a.tag)
            if not targets:
                continue
            for b in active:
                if b.tag not in targets:
                    continue
                if not a.rect.colliderect(b.rect):
                    continue
                key = (id(a), id(b))
                current.add(key)
                if key not in cls._overlaps:
                    cls._fire(a, b)
                    cls._fire(b, a)
        cls._overlaps = current

    @staticmethod
    def _fire(receiver: "BoxCollider2D", other: "BoxCollider2D") -> None:
        for component in list(receiver.game_object.components):
            if receiver.is_trigger or other.is_trigger:
                component.on_trigger_enter_2d(other)
            else:
                component.on_collision_enter_2d(other)

    @classmethod
    def overlap_box(
        cls, rect: pygame.Rect, tag_filter: str | None = None
    ) -> list["BoxCollider2D"]:
        """Returns all colliders overlapping the given rect.

        Args:
            rect: World-space query rectangle.
            tag_filter: If given, only colliders whose GameObject has this tag.

        Returns:
            List of overlapping, enabled colliders on active objects.
        """
        return [
            c
            for c in cls._active_colliders()
            if (tag_filter is None or c.tag == tag_filter) and rect.colliderect(c.rect)
        ]
