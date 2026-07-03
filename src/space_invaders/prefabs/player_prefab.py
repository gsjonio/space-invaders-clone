"""Factory for the Player GameObject."""

import pygame

from space_invaders.components.box_collider_2d import BoxCollider2D
from space_invaders.components.sprite_renderer import SpriteRenderer
from space_invaders.core.game_object import GameObject
from space_invaders.core.scene import Scene
from space_invaders.scripts.player_controller import PlayerController
from space_invaders.settings import LAYER_ENTITY, PLAYER_Y, SCREEN_WIDTH, TAG_PLAYER


def create_player(scene: Scene) -> GameObject:
    """Factory function for the Player GameObject.

    Attaches: Transform, SpriteRenderer, BoxCollider2D, PlayerController.

    Returns:
        The configured GameObject (not yet added to the scene).
    """
    go = GameObject("Player", tag=TAG_PLAYER, layer=LAYER_ENTITY)
    go.transform.position = pygame.Vector2(SCREEN_WIDTH / 2, PLAYER_Y)
    go.add_component(SpriteRenderer(layer_order=LAYER_ENTITY))
    go.add_component(BoxCollider2D(pygame.Vector2(26, 16)))
    go.add_component(PlayerController())
    return go
