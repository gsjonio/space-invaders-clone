"""Tests for the Transform component."""

import pygame

from space_invaders.core.game_object import GameObject


def test_transform_defaults() -> None:
    go = GameObject("Test")
    assert go.transform.position == pygame.Vector2(0, 0)
    assert go.transform.rotation == 0.0
    assert go.transform.scale == pygame.Vector2(1.0, 1.0)


def test_translate_moves_position() -> None:
    go = GameObject("Test")
    go.transform.position = pygame.Vector2(10, 20)
    go.transform.translate(pygame.Vector2(5, -3))
    assert go.transform.position == pygame.Vector2(15, 17)


def test_translate_accumulates() -> None:
    go = GameObject("Test")
    for _ in range(4):
        go.transform.translate(pygame.Vector2(1.5, 0))
    assert go.transform.position == pygame.Vector2(6.0, 0)
