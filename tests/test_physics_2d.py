"""Tests for Physics2D collision queries."""

import pygame
import pytest

from space_invaders.components.box_collider_2d import BoxCollider2D
from space_invaders.core.game_object import GameObject
from space_invaders.core.physics_2d import Physics2D


@pytest.fixture(autouse=True)
def clean_physics():
    Physics2D.clear()
    yield
    Physics2D.clear()


def make_box(x: float, y: float, size: float = 10, tag: str = "Untagged") -> BoxCollider2D:
    go = GameObject("Box", tag=tag)
    go.transform.position = pygame.Vector2(x, y)
    return go.add_component(BoxCollider2D(pygame.Vector2(size, size)))


def test_collider_registers_on_awake_and_unregisters_on_destroy() -> None:
    collider = make_box(0, 0)
    assert collider in Physics2D._colliders
    collider.game_object.destroy()
    assert collider not in Physics2D._colliders


def test_overlap_box_finds_overlapping_colliders() -> None:
    inside = make_box(50, 50)
    outside = make_box(500, 500)
    hits = Physics2D.overlap_box(pygame.Rect(40, 40, 20, 20))
    assert inside in hits
    assert outside not in hits


def test_overlap_box_tag_filter() -> None:
    make_box(50, 50, tag="A")
    b = make_box(52, 52, tag="B")
    hits = Physics2D.overlap_box(pygame.Rect(40, 40, 20, 20), tag_filter="B")
    assert hits == [b]


def test_overlap_box_skips_disabled_and_inactive() -> None:
    disabled = make_box(50, 50)
    disabled.enabled = False
    inactive = make_box(52, 52)
    inactive.game_object.active = False
    assert Physics2D.overlap_box(pygame.Rect(40, 40, 20, 20)) == []


def test_collider_rect_uses_position_and_offset() -> None:
    collider = make_box(100, 100, size=20)
    collider.offset = pygame.Vector2(5, -5)
    rect = collider.rect
    assert rect.center == (105, 95)
    assert rect.size == (20, 20)
