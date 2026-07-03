"""Scene: manages GameObjects, mirroring a Unity Scene."""

from __future__ import annotations

from typing import TypeVar

import pygame

from space_invaders.components.box_collider_2d import BoxCollider2D
from space_invaders.components.sprite_renderer import SpriteRenderer
from space_invaders.core.game_object import GameObject
from space_invaders.core.mono_behaviour import MonoBehaviour
from space_invaders.core.physics_2d import Physics2D

T = TypeVar("T", bound=MonoBehaviour)


class Scene:
    """Manages all GameObjects in the current level. Equivalent to a Unity Scene."""

    def __init__(self) -> None:
        self._game_objects: list[GameObject] = []

    @property
    def game_objects(self) -> list[GameObject]:
        """All objects currently in the scene (including ones marked destroyed)."""
        return self._game_objects

    def on_load(self) -> None:
        """Override in subclasses to build the scene. Called by SceneManager."""

    def on_unload(self) -> None:
        """Override to clean up. Called before loading a new scene."""

    def instantiate(self, game_object: GameObject) -> GameObject:
        """Adds a GameObject to the scene and calls start() on all its components.

        Args:
            game_object: A fully configured GameObject (e.g. from a prefab factory).

        Returns:
            The same GameObject.
        """
        game_object.scene = self
        self._game_objects.append(game_object)
        for component in list(game_object.components):
            component.start()
        return game_object

    def destroy(self, game_object: GameObject) -> None:
        """Marks a GameObject for removal (removed at end of frame)."""
        game_object.destroy()

    def find_object_with_tag(self, tag: str) -> GameObject | None:
        """Returns the first live GameObject with the given tag, or None."""
        for go in self._game_objects:
            if go.tag == tag and not go.destroyed:
                return go
        return None

    def find_objects_with_tag(self, tag: str) -> list[GameObject]:
        """Returns all live GameObjects with the given tag."""
        return [go for go in self._game_objects if go.tag == tag and not go.destroyed]

    def find_object_of_type(self, component_type: type[T]) -> T | None:
        """Finds the first component of given type across all live objects."""
        for go in self._game_objects:
            if go.destroyed:
                continue
            component = go.get_component(component_type)
            if component is not None:
                return component
        return None

    def update(self, delta_time: float) -> None:
        """Calls update() on every active component in scene order."""
        for go in list(self._game_objects):
            if not go.active or go.destroyed:
                continue
            for component in list(go.components):
                if go.destroyed:
                    break
                component.update(delta_time)

    def render(self, surface: pygame.Surface) -> None:
        """Renders all SpriteRenderer components sorted by layer_order."""
        renderers: list[SpriteRenderer] = []
        for go in self._game_objects:
            if go.active and not go.destroyed:
                renderers.extend(go.get_components(SpriteRenderer))
        renderers.sort(key=lambda r: r.layer_order)
        for renderer in renderers:
            renderer.draw(surface)

    def _flush_destroyed(self) -> None:
        """End-of-frame cleanup of destroyed objects (also unregisters colliders)."""
        destroyed = [go for go in self._game_objects if go.destroyed]
        for go in destroyed:
            for collider in go.get_components(BoxCollider2D):
                Physics2D.unregister_collider(collider)
            self._game_objects.remove(go)

    def clear(self) -> None:
        """Destroys and flushes every object. Used on scene unload."""
        for go in list(self._game_objects):
            go.destroy()
        self._flush_destroyed()
