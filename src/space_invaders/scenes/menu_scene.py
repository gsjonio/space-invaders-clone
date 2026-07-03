"""Title screen scene."""

import pygame

from space_invaders.components.sprite_renderer import SpriteRenderer
from space_invaders.core.game_object import GameObject
from space_invaders.core.input_manager import Input
from space_invaders.core.mono_behaviour import MonoBehaviour
from space_invaders.core.scene import Scene
from space_invaders.core.scene_manager import SceneManager
from space_invaders.scripts.invader_controller import INVADER_SPRITES
from space_invaders.scripts.ufo_controller import UFO_SPRITE
from space_invaders.settings import (
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_WHITE,
    LAYER_UI,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UI_FONT_SIZE,
    UI_TITLE_FONT_SIZE,
)
from space_invaders.utils.sprite_utils import build_sprite, create_text_object


class MenuController(MonoBehaviour):
    """Blinks the prompt text and starts the game on ENTER."""

    def __init__(self, blink_renderer: SpriteRenderer) -> None:
        self._blink_renderer = blink_renderer
        self._blink_timer = 0.0

    def update(self, delta_time: float) -> None:
        self._blink_timer += delta_time
        if self._blink_timer >= 0.5:
            self._blink_timer = 0.0
            self._blink_renderer.visible = not self._blink_renderer.visible
        if Input.get_key_down(pygame.K_RETURN):
            from space_invaders.scenes.game_scene import GameScene

            SceneManager.load_scene(GameScene())
        if Input.get_key_down(pygame.K_ESCAPE):
            Input.request_quit()


class MenuScene(Scene):
    """Title screen: logo, score table with invader sprites, blinking prompt."""

    def on_load(self) -> None:
        center_x = SCREEN_WIDTH / 2
        self.instantiate(
            create_text_object(
                "Title",
                "SPACE INVADERS",
                UI_TITLE_FONT_SIZE,
                COLOR_GREEN,
                pygame.Vector2(center_x, 120),
            )
        )

        table = [
            (build_sprite(UFO_SPRITE, COLOR_RED), "= ? MYSTERY"),
            (build_sprite(INVADER_SPRITES[2][0], COLOR_WHITE), "= 30 PTS"),
            (build_sprite(INVADER_SPRITES[1][0], COLOR_WHITE), "= 20 PTS"),
            (build_sprite(INVADER_SPRITES[0][0], COLOR_WHITE), "= 10 PTS"),
        ]
        for i, (sprite, label) in enumerate(table):
            y = 220 + i * 50
            icon = GameObject("TableIcon")
            icon.transform.position = pygame.Vector2(center_x - 80, y)
            icon.add_component(SpriteRenderer(sprite, layer_order=LAYER_UI))
            self.instantiate(icon)
            self.instantiate(
                create_text_object(
                    "TableLabel",
                    label,
                    UI_FONT_SIZE,
                    COLOR_WHITE,
                    pygame.Vector2(center_x + 40, y),
                )
            )

        controls = [
            "MOVE: ARROW KEYS    SHOOT: SPACE",
            "PAUSE: P    MENU/QUIT: ESC",
        ]
        for i, line in enumerate(controls):
            self.instantiate(
                create_text_object(
                    "Controls",
                    line,
                    UI_FONT_SIZE,
                    COLOR_CYAN,
                    pygame.Vector2(center_x, 420 + i * 26),
                )
            )

        prompt = self.instantiate(
            create_text_object(
                "Prompt",
                "PRESS ENTER TO PLAY",
                UI_FONT_SIZE,
                COLOR_WHITE,
                pygame.Vector2(center_x, SCREEN_HEIGHT - 120),
            )
        )
        controller_go = GameObject("MenuController")
        controller_go.add_component(
            MenuController(prompt.get_component(SpriteRenderer))
        )
        self.instantiate(controller_go)
