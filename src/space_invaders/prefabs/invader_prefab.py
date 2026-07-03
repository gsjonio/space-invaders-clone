"""Factory for a single invader."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from space_invaders.components.box_collider_2d import BoxCollider2D
from space_invaders.components.sprite_renderer import SpriteRenderer
from space_invaders.core.game_object import GameObject
from space_invaders.core.scene import Scene
from space_invaders.scripts.invader_controller import InvaderController
from space_invaders.settings import LAYER_ENTITY, TAG_ENEMY

if TYPE_CHECKING:
    from space_invaders.scripts.invader_formation import InvaderFormation


def create_invader(
    position: pygame.Vector2,
    invader_type: int,
    formation: "InvaderFormation",
    scene: Scene,
) -> GameObject:
    """Factory for a single invader.

    Args:
        position: Grid slot position.
        invader_type: 0/1/2 (see InvaderController).
        formation: Owning formation, notified on death.
        scene: Target scene (dependency-injected; not used until instantiate).

    Returns:
        The configured GameObject (not yet added to the scene).
    """
    go = GameObject("Invader", tag=TAG_ENEMY, layer=LAYER_ENTITY)
    go.transform.position = pygame.Vector2(position)
    go.add_component(SpriteRenderer(layer_order=LAYER_ENTITY))
    go.add_component(BoxCollider2D(pygame.Vector2(24, 24)))
    go.add_component(InvaderController(invader_type, formation))
    return go
