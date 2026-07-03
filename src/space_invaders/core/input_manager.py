"""Input: static keyboard-polling class, mirroring Unity's Input."""

import pygame


class Input:
    """Static class for polling keyboard input, mirroring Unity's Input class.

    Usage:
        Input.get_key(pygame.K_LEFT)       # held
        Input.get_key_down(pygame.K_SPACE) # pressed this frame
        Input.get_key_up(pygame.K_SPACE)   # released this frame
    """

    _held: set[int] = set()
    _down: set[int] = set()
    _up: set[int] = set()
    _quit: bool = False

    @classmethod
    def update(cls, events: list[pygame.event.Event]) -> None:
        """Called by GameEngine every frame before scene.update().

        Args:
            events: The pygame events polled this frame.
        """
        cls._down.clear()
        cls._up.clear()
        for event in events:
            if event.type == pygame.QUIT:
                cls._quit = True
            elif event.type == pygame.KEYDOWN:
                cls._held.add(event.key)
                cls._down.add(event.key)
            elif event.type == pygame.KEYUP:
                cls._held.discard(event.key)
                cls._up.add(event.key)

    @classmethod
    def get_key(cls, key: int) -> bool:
        """True while the key is held."""
        return key in cls._held

    @classmethod
    def get_key_down(cls, key: int) -> bool:
        """True only on the frame the key was pressed."""
        return key in cls._down

    @classmethod
    def get_key_up(cls, key: int) -> bool:
        """True only on the frame the key was released."""
        return key in cls._up

    @classmethod
    def get_quit(cls) -> bool:
        """True once the window close button or request_quit() fired."""
        return cls._quit

    @classmethod
    def request_quit(cls) -> None:
        """Programmatically request application shutdown."""
        cls._quit = True
