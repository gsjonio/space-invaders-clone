"""InvaderController: sprite frames, animation toggle, and death handling."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from space_invaders.components.box_collider_2d import BoxCollider2D
from space_invaders.components.sprite_renderer import SpriteRenderer
from space_invaders.core.mono_behaviour import MonoBehaviour
from space_invaders.scripts.audio_manager import AudioManager
from space_invaders.scripts.game_manager import GameManager
from space_invaders.settings import COLOR_WHITE, INVADER_POINTS, TAG_BULLET_P
from space_invaders.utils.sprite_utils import build_sprite

if TYPE_CHECKING:
    from space_invaders.scripts.invader_formation import InvaderFormation

# Two animation frames per type. Type 0 = octopus (bottom rows),
# type 1 = crab (middle rows), type 2 = squid (top row).
INVADER_SPRITES: dict[int, tuple[list[str], list[str]]] = {
    0: (
        [
            "000011110000",
            "011111111110",
            "111111111111",
            "111001100111",
            "111111111111",
            "000110011000",
            "001101101100",
            "110000000011",
        ],
        [
            "000011110000",
            "011111111110",
            "111111111111",
            "111001100111",
            "111111111111",
            "001110011100",
            "011001100110",
            "001100001100",
        ],
    ),
    1: (
        [
            "00100000100",
            "00010001000",
            "00111111100",
            "01101110110",
            "11111111111",
            "10111111101",
            "10100000101",
            "00011011000",
        ],
        [
            "00100000100",
            "10010001001",
            "10111111101",
            "11101110111",
            "11111111111",
            "01111111110",
            "00100000100",
            "01000000010",
        ],
    ),
    2: (
        [
            "00011000",
            "00111100",
            "01111110",
            "11011011",
            "11111111",
            "00100100",
            "01011010",
            "10100101",
        ],
        [
            "00011000",
            "00111100",
            "01111110",
            "11011011",
            "11111111",
            "01011010",
            "10000001",
            "01000010",
        ],
    ),
}


class InvaderController(MonoBehaviour):
    """A single invader: two-frame animation, point value, bullet-hit death."""

    def __init__(self, invader_type: int, formation: "InvaderFormation") -> None:
        """Args:
        invader_type: 0 (bottom rows), 1 (middle rows), 2 (top row).
        formation: The owning formation, notified on death.
        """
        self.invader_type = invader_type
        self.formation = formation
        self.points = INVADER_POINTS[invader_type]
        self._frame = 0

    def awake(self) -> None:
        frame_a, frame_b = INVADER_SPRITES[self.invader_type]
        self._frames = (
            build_sprite(frame_a, COLOR_WHITE),
            build_sprite(frame_b, COLOR_WHITE),
        )

    def start(self) -> None:
        self._renderer = self.game_object.get_component(SpriteRenderer)
        self._renderer.surface = self._frames[0]
        collider = self.game_object.get_component(BoxCollider2D)
        collider.size = pygame.Vector2(self._frames[0].get_size())

    def toggle_frame(self) -> None:
        """Advances the two-frame animation. Called by the formation each step."""
        self._frame = 1 - self._frame
        self._renderer.surface = self._frames[self._frame]

    def on_trigger_enter_2d(self, other: BoxCollider2D) -> None:
        if other.tag != TAG_BULLET_P:
            return
        if GameManager.instance:
            GameManager.instance.enemy_killed(self.points)
        if AudioManager.instance:
            AudioManager.instance.play("explosion_invader")
        self.formation.notify_death(self)
        self.game_object.destroy()
