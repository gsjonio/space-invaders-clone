"""Main gameplay scene."""

import pygame

from space_invaders.components.box_collider_2d import BoxCollider2D
from space_invaders.components.sprite_renderer import SpriteRenderer
from space_invaders.core.game_object import GameObject
from space_invaders.core.scene import Scene
from space_invaders.prefabs.barrier_prefab import create_barrier
from space_invaders.prefabs.player_prefab import create_player
from space_invaders.scripts.audio_manager import AudioManager
from space_invaders.scripts.game_manager import GameManager
from space_invaders.scripts.invader_formation import InvaderFormation
from space_invaders.scripts.ufo_controller import UfoController
from space_invaders.scripts.ui_manager import UIManager
from space_invaders.settings import (
    BARRIER_COUNT,
    BARRIER_Y,
    LAYER_ENTITY,
    PLAYER_LIVES,
    SCREEN_WIDTH,
    TAG_UFO,
)


class GameScene(Scene):
    """Main gameplay scene: managers, player, formation, barriers, UFO, HUD."""

    def __init__(
        self, wave: int = 1, score: int = 0, lives: int = PLAYER_LIVES
    ) -> None:
        super().__init__()
        self._wave = wave
        self._score = score
        self._lives = lives

    def on_load(self) -> None:
        audio_go = GameObject("AudioManager")
        audio_go.add_component(AudioManager())
        self.instantiate(audio_go)

        manager_go = GameObject("GameManager")
        manager_go.add_component(
            GameManager(wave=self._wave, score=self._score, lives=self._lives)
        )
        self.instantiate(manager_go)

        self.instantiate(create_player(self))

        formation_go = GameObject("InvaderFormation")
        formation_go.add_component(InvaderFormation(wave=self._wave))
        self.instantiate(formation_go)

        for i in range(BARRIER_COUNT):
            x = SCREEN_WIDTH * (i + 1) / (BARRIER_COUNT + 1)
            self.instantiate(create_barrier(pygame.Vector2(x, BARRIER_Y), self))

        ufo_go = GameObject("UFO", tag=TAG_UFO, layer=LAYER_ENTITY)
        ufo_go.add_component(SpriteRenderer(layer_order=LAYER_ENTITY))
        ufo_go.add_component(BoxCollider2D(pygame.Vector2(48, 21)))
        ufo_go.add_component(UfoController())
        self.instantiate(ufo_go)

        ui_go = GameObject("UIManager")
        ui_go.add_component(SpriteRenderer())
        ui_go.add_component(UIManager())
        self.instantiate(ui_go)
