"""Factory for player and enemy bullets."""

import pygame

from space_invaders.components.box_collider_2d import BoxCollider2D
from space_invaders.components.sprite_renderer import SpriteRenderer
from space_invaders.core.game_object import GameObject
from space_invaders.core.scene import Scene
from space_invaders.scripts.bullet_controller import BulletController
from space_invaders.settings import (
    BULLET_HEIGHT,
    BULLET_WIDTH,
    COLOR_WHITE,
    COLOR_YELLOW,
    LAYER_BULLET,
    TAG_BULLET_P,
)


def create_bullet(
    position: pygame.Vector2,
    direction: int,
    speed: float,
    tag: str,
    scene: Scene,
) -> GameObject:
    """Factory for player or enemy bullets.

    Args:
        position: Spawn position (bullet center).
        direction: -1 up (player), +1 down (enemy).
        speed: Pixels per second.
        tag: TAG_BULLET_P or TAG_BULLET_E.
        scene: Target scene (dependency-injected; not used until instantiate).

    Returns:
        The configured GameObject (not yet added to the scene).
    """
    go = GameObject("Bullet", tag=tag, layer=LAYER_BULLET)
    go.transform.position = pygame.Vector2(position)
    color = COLOR_WHITE if tag == TAG_BULLET_P else COLOR_YELLOW
    surface = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
    surface.fill(color)
    go.add_component(SpriteRenderer(surface, layer_order=LAYER_BULLET))
    go.add_component(BoxCollider2D(pygame.Vector2(BULLET_WIDTH, BULLET_HEIGHT)))
    go.add_component(BulletController(direction, speed))
    return go
