"""GameManager: singleton script managing game state."""

from __future__ import annotations

from typing import ClassVar

import pygame

from space_invaders.core.input_manager import Input
from space_invaders.core.mono_behaviour import MonoBehaviour
from space_invaders.core.scene_manager import SceneManager
from space_invaders.core.time_manager import Time
from space_invaders.scripts.audio_manager import AudioManager
from space_invaders.settings import (
    PLAYER_RESPAWN_GUARD,
    PLAYER_Y,
    SCREEN_WIDTH,
    TAG_PLAYER,
)


class GameManager(MonoBehaviour):
    """Singleton script managing game state: score, hi-score, lives, wave.

    Mirrors the Unity pattern of a persistent GameManager singleton.
    hi_score is a class attribute so it survives scene reloads within a run.

    Attributes:
        instance: Singleton reference, set in awake().
        score: Current score.
        lives: Remaining lives.
        wave: Current wave number (1-based).
    """

    instance: ClassVar["GameManager | None"] = None
    hi_score: ClassVar[int] = 0  # ponytail: session-only; persist to a file if wanted

    def __init__(self, wave: int = 1, score: int = 0, lives: int = 3) -> None:
        self.wave = wave
        self.score = score
        self.lives = lives
        self._invulnerable = 0.0
        self._finished = False

    def awake(self) -> None:
        GameManager.instance = self

    def on_destroy(self) -> None:
        if GameManager.instance is self:
            GameManager.instance = None

    def update(self, delta_time: float) -> None:
        if self._invulnerable > 0.0:
            self._invulnerable -= delta_time
        if Input.get_key_down(pygame.K_p):
            Time.time_scale = 0.0 if Time.time_scale > 0.0 else 1.0
        if Input.get_key_down(pygame.K_ESCAPE):
            from space_invaders.scenes.menu_scene import MenuScene

            SceneManager.load_scene(MenuScene())

    def player_hit(self) -> None:
        """Decreases lives, then respawns the player or ends the game."""
        if self._finished or self._invulnerable > 0.0:
            return
        self.lives -= 1
        if AudioManager.instance:
            AudioManager.instance.play("explosion_player")
        if self.lives <= 0:
            self.game_over()
            return
        self._invulnerable = PLAYER_RESPAWN_GUARD
        player = self.game_object.scene.find_object_with_tag(TAG_PLAYER)
        if player is not None:
            player.transform.position = pygame.Vector2(SCREEN_WIDTH / 2, PLAYER_Y)

    def enemy_killed(self, points: int) -> None:
        """Adds points to score and updates the hi-score."""
        self.score += points
        GameManager.hi_score = max(GameManager.hi_score, self.score)

    def wave_cleared(self) -> None:
        """Loads the next, faster wave, carrying score and lives over."""
        if self._finished:
            return
        self._finished = True
        from space_invaders.scenes.game_scene import GameScene

        SceneManager.load_scene(
            GameScene(wave=self.wave + 1, score=self.score, lives=self.lives)
        )

    def game_over(self) -> None:
        """Transitions to the GameOverScene."""
        if self._finished:
            return
        self._finished = True
        from space_invaders.scenes.game_over_scene import GameOverScene

        SceneManager.load_scene(GameOverScene(score=self.score))
