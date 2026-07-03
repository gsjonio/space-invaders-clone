"""Game over scene."""

import pygame

from space_invaders.core.game_object import GameObject
from space_invaders.core.input_manager import Input
from space_invaders.core.mono_behaviour import MonoBehaviour
from space_invaders.core.scene import Scene
from space_invaders.core.scene_manager import SceneManager
from space_invaders.settings import (
    COLOR_RED,
    COLOR_WHITE,
    COLOR_YELLOW,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UI_FONT_SIZE,
    UI_TITLE_FONT_SIZE,
)
from space_invaders.utils.sprite_utils import create_text_object


class GameOverController(MonoBehaviour):
    """ENTER retries, ESC quits."""

    def update(self, delta_time: float) -> None:
        if Input.get_key_down(pygame.K_RETURN):
            from space_invaders.scenes.game_scene import GameScene

            SceneManager.load_scene(GameScene())
        if Input.get_key_down(pygame.K_ESCAPE):
            Input.request_quit()


class GameOverScene(Scene):
    """Shown on death or invasion: final score plus retry/quit prompts."""

    def __init__(self, score: int = 0, message: str = "GAME OVER") -> None:
        super().__init__()
        self._score = score
        self._message = message

    def on_load(self) -> None:
        center_x = SCREEN_WIDTH / 2
        self.instantiate(
            create_text_object(
                "GameOver",
                self._message,
                UI_TITLE_FONT_SIZE,
                COLOR_RED,
                pygame.Vector2(center_x, SCREEN_HEIGHT / 3),
            )
        )
        self.instantiate(
            create_text_object(
                "FinalScore",
                f"FINAL SCORE {self._score:05d}",
                UI_FONT_SIZE,
                COLOR_YELLOW,
                pygame.Vector2(center_x, SCREEN_HEIGHT / 2),
            )
        )
        self.instantiate(
            create_text_object(
                "Retry",
                "PRESS ENTER TO RETRY  -  PRESS ESC TO QUIT",
                UI_FONT_SIZE,
                COLOR_WHITE,
                pygame.Vector2(center_x, SCREEN_HEIGHT * 2 / 3),
            )
        )
        controller_go = GameObject("GameOverController")
        controller_go.add_component(GameOverController())
        self.instantiate(controller_go)
