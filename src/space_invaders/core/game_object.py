"""GameObject: component container, mirroring Unity's GameObject."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from space_invaders.components.transform import Transform
from space_invaders.core.mono_behaviour import MonoBehaviour

if TYPE_CHECKING:
    from space_invaders.core.scene import Scene

T = TypeVar("T", bound=MonoBehaviour)


class GameObject:
    """Container for components, mirroring Unity's GameObject.

    Every entity in the scene (player, bullet, invader) is a GameObject
    with components attached to it. A Transform is attached automatically
    at construction.

    Attributes:
        name: Human-readable name.
        tag: Unity-style tag string (see settings.TAG_*).
        layer: Numeric layer (see settings.LAYER_*).
        scene: The Scene this object was instantiated into (or None).
        destroyed: True once destroy() has been called.
    """

    def __init__(self, name: str, tag: str = "Untagged", layer: int = 0) -> None:
        self.name = name
        self.tag = tag
        self.layer = layer
        self.scene: "Scene | None" = None
        self.destroyed = False
        self._active = True
        self._components: list[MonoBehaviour] = []
        self._transform = Transform()
        self.add_component(self._transform)

    @property
    def components(self) -> list[MonoBehaviour]:
        """All attached components, in attach order."""
        return self._components

    def add_component(self, component: T) -> T:
        """Attaches a component, sets its .game_object back-ref, calls awake().

        Args:
            component: The MonoBehaviour instance to attach.

        Returns:
            The same component, for chaining.
        """
        component.game_object = self
        self._components.append(component)
        component.awake()
        return component

    def get_component(self, component_type: type[T]) -> T | None:
        """Returns the first component of the given type, or None."""
        for component in self._components:
            if isinstance(component, component_type):
                return component
        return None

    def get_components(self, component_type: type[T]) -> list[T]:
        """Returns all components of the given type."""
        return [c for c in self._components if isinstance(c, component_type)]

    @property
    def transform(self) -> Transform:
        """Shortcut — every GameObject always has a Transform."""
        return self._transform

    @property
    def active(self) -> bool:
        """Whether the object participates in update/render/physics."""
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        if value == self._active:
            return
        self._active = value
        for component in self._components:
            if value:
                component.on_enable()
            else:
                component.on_disable()

    def destroy(self) -> None:
        """Marks for destruction and calls on_destroy() on all components.

        The object is actually removed from the scene at end of frame by
        ``Scene._flush_destroyed()``.
        """
        if self.destroyed:
            return
        self.destroyed = True
        for component in self._components:
            component.on_destroy()
