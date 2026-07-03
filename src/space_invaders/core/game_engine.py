"""GameEngine: bootstraps pygame and owns the main loop."""

import pygame

from space_invaders.core.input_manager import Input
from space_invaders.core.physics_2d import Physics2D
from space_invaders.core.scene_manager import SceneManager
from space_invaders.core.time_manager import Time
from space_invaders.settings import COLOR_BLACK


class GameEngine:
    """Bootstraps pygame, owns the main loop. Mirrors Unity's runtime lifecycle.

    Loop order (mirrors Unity's execution order):
        1. Handle pending SceneManager transitions
        2. Process OS events -> Input.update()
        3. Time.tick()
        4. Physics2D.check_all_overlaps()
        5. scene.update(Time.delta_time)
        6. screen.fill + scene.render + display.flip
        7. scene._flush_destroyed()
    """

    def __init__(self, width: int, height: int, fps: int, title: str) -> None:
        self._fps = fps
        self._screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

    def run(self) -> None:
        """Runs the main loop until the window is closed or quit is requested."""
        while True:
            scene = SceneManager.apply_pending()
            if scene is None:
                return
            Input.update(pygame.event.get())
            if Input.get_quit():
                return
            Time.tick(self._fps)
            Physics2D.check_all_overlaps()
            scene.update(Time.delta_time)
            self._screen.fill(COLOR_BLACK)
            scene.render(self._screen)
            pygame.display.flip()
            scene._flush_destroyed()
