"""Factory for a destructible barrier."""

import pygame

from space_invaders.components.box_collider_2d import BoxCollider2D
from space_invaders.components.sprite_renderer import SpriteRenderer
from space_invaders.core.game_object import GameObject
from space_invaders.core.scene import Scene
from space_invaders.scripts.barrier_controller import BarrierController
from space_invaders.settings import (
    BARRIER_CELL,
    BARRIER_COLS,
    BARRIER_ROWS,
    LAYER_BARRIER,
    TAG_BARRIER,
)


def create_barrier(position: pygame.Vector2, scene: Scene) -> GameObject:
    """Factory for a destructible barrier.

    Args:
        position: Barrier center position.
        scene: Target scene (dependency-injected; not used until instantiate).

    Returns:
        The configured GameObject (not yet added to the scene).
    """
    go = GameObject("Barrier", tag=TAG_BARRIER, layer=LAYER_BARRIER)
    go.transform.position = pygame.Vector2(position)
    go.add_component(SpriteRenderer(layer_order=LAYER_BARRIER))
    go.add_component(
        BoxCollider2D(
            pygame.Vector2(BARRIER_COLS * BARRIER_CELL, BARRIER_ROWS * BARRIER_CELL)
        )
    )
    go.add_component(BarrierController())
    return go
