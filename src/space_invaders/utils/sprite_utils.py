"""Shared helpers for procedural pixel-grid sprites and text surfaces."""

from pathlib import Path

import pygame

from space_invaders.settings import LAYER_UI, SPRITE_CELL

_ASSETS_DIR = Path(__file__).resolve().parents[3] / "assets"
_font_cache: dict[int, pygame.font.Font] = {}


def build_sprite(
    grid: list[str], color: tuple[int, int, int], cell: int = SPRITE_CELL
) -> pygame.Surface:
    """Builds a transparent surface from a pixel grid.

    Args:
        grid: Rows of '0'/'1' characters; '1' cells are filled with color.
        color: Fill color for solid cells.
        cell: Pixel size of each grid cell.

    Returns:
        A new SRCALPHA surface of size (cols*cell, rows*cell).
    """
    rows = len(grid)
    cols = len(grid[0])
    surface = pygame.Surface((cols * cell, rows * cell), pygame.SRCALPHA)
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch == "1":
                surface.fill(color, (x * cell, y * cell, cell, cell))
    return surface


def get_font(size: int) -> pygame.font.Font:
    """Returns a cached font: first .ttf found in assets/fonts, else monospace SysFont."""
    if size not in _font_cache:
        font: pygame.font.Font | None = None
        try:
            ttf_files = sorted((_ASSETS_DIR / "fonts").glob("*.ttf"))
            if ttf_files:
                font = pygame.font.Font(str(ttf_files[0]), size)
        except OSError:
            font = None
        if font is None:
            font = pygame.font.SysFont("monospace", size, bold=True)
        _font_cache[size] = font
    return _font_cache[size]


def render_text(
    text: str, size: int, color: tuple[int, int, int]
) -> pygame.Surface:
    """Renders text to a surface using the shared font."""
    return get_font(size).render(text, True, color)


def create_text_object(
    name: str,
    text: str,
    size: int,
    color: tuple[int, int, int],
    position: pygame.Vector2,
    layer_order: int = LAYER_UI,
) -> "GameObject":
    """Builds a GameObject with a text SpriteRenderer (not yet instantiated)."""
    from space_invaders.components.sprite_renderer import SpriteRenderer
    from space_invaders.core.game_object import GameObject

    go = GameObject(name)
    go.transform.position = pygame.Vector2(position)
    go.add_component(SpriteRenderer(render_text(text, size, color), layer_order))
    return go
