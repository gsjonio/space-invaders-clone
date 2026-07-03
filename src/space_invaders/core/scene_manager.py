"""SceneManager singleton, mirroring Unity's SceneManager."""

from __future__ import annotations

from space_invaders.core.physics_2d import Physics2D
from space_invaders.core.scene import Scene
from space_invaders.core.time_manager import Time


class SceneManager:
    """Singleton that manages scene transitions. Equivalent to Unity's SceneManager.

    Transitions never happen mid-frame: ``load_scene`` queues the scene and the
    GameEngine applies it at a safe point via ``apply_pending()``.

    Usage:
        SceneManager.load_scene(GameScene())
        SceneManager.reload_scene()
    """

    _current_scene: Scene | None = None
    _next_scene: Scene | None = None

    @classmethod
    def load_scene(cls, scene: Scene) -> None:
        """Queues a scene to become current at the start of the next frame."""
        cls._next_scene = scene

    @classmethod
    def reload_scene(cls) -> None:
        """Queues a fresh instance of the current scene's class."""
        if cls._current_scene is not None:
            cls._next_scene = type(cls._current_scene)()

    @classmethod
    def get_current_scene(cls) -> Scene | None:
        """Returns the active scene, or None before the first load."""
        return cls._current_scene

    @classmethod
    def apply_pending(cls) -> Scene | None:
        """Performs a queued transition, if any. Called by GameEngine.

        Returns:
            The (possibly new) current scene.
        """
        if cls._next_scene is not None:
            if cls._current_scene is not None:
                cls._current_scene.on_unload()
                cls._current_scene.clear()
            Physics2D.clear()
            Time.time_scale = 1.0
            cls._current_scene = cls._next_scene
            cls._next_scene = None
            cls._current_scene.on_load()
        return cls._current_scene
