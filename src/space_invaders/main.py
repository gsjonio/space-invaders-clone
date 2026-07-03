"""Entry point: bootstraps the GameEngine and the first Scene."""

import pygame

from space_invaders.core.game_engine import GameEngine
from space_invaders.core.scene_manager import SceneManager
from space_invaders.scenes.menu_scene import MenuScene
from space_invaders.settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE


def main() -> None:
    """Initializes pygame, loads the menu scene, and runs the main loop."""
    # Mono 16-bit at 22050 Hz keeps procedural sound buffers small.
    pygame.mixer.pre_init(22050, -16, 1, 256)
    pygame.init()
    engine = GameEngine(width=SCREEN_WIDTH, height=SCREEN_HEIGHT, fps=FPS, title=TITLE)
    SceneManager.load_scene(MenuScene())
    engine.run()
    pygame.quit()


if __name__ == "__main__":
    main()
