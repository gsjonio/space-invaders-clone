"""MonoBehaviour lifecycle base class, mirroring Unity's MonoBehaviour."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from space_invaders.components.box_collider_2d import BoxCollider2D
    from space_invaders.core.game_object import GameObject


class MonoBehaviour:
    """Base class for all game scripts, mirroring Unity's MonoBehaviour lifecycle.

    Attributes:
        game_object: Back-reference to the owning GameObject, set by
            ``GameObject.add_component()``.
    """

    game_object: "GameObject"

    def awake(self) -> None:
        """Called once when the component is first created, before Start.

        Use for self-initialization (does not depend on other objects).
        Equivalent to Unity's Awake().
        """

    def start(self) -> None:
        """Called once when the GameObject enters the scene.

        Use for cross-object references. Equivalent to Unity's Start().
        """

    def update(self, delta_time: float) -> None:
        """Called every frame.

        Args:
            delta_time: Scaled seconds since last frame (0 while paused).
        """

    def on_destroy(self) -> None:
        """Called just before the GameObject is removed from the scene."""

    def on_enable(self) -> None:
        """Called when the component or its GameObject is activated."""

    def on_disable(self) -> None:
        """Called when the component or its GameObject is deactivated."""

    def on_collision_enter_2d(self, other: "BoxCollider2D") -> None:
        """Called when this object's collider first overlaps a non-trigger collider."""

    def on_trigger_enter_2d(self, other: "BoxCollider2D") -> None:
        """Called when a trigger overlap begins. Equivalent to OnTriggerEnter2D()."""
