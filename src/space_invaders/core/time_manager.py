"""Time: static frame-timing class, mirroring Unity's Time."""

import pygame


class Time:
    """Static class providing frame timing, mirroring Unity's Time class.

    Usage:
        Time.delta_time      # scaled seconds since last frame
        Time.elapsed_time    # total seconds since game start
        Time.time_scale      # multiplier (1.0 = normal, 0.0 = paused)
    """

    delta_time: float = 0.0
    unscaled_delta_time: float = 0.0
    elapsed_time: float = 0.0
    time_scale: float = 1.0
    _clock: pygame.time.Clock | None = None

    @classmethod
    def tick(cls, fps: int) -> None:
        """Called by GameEngine each frame to update delta_time.

        Args:
            fps: Target frames per second passed to the pygame clock.
        """
        if cls._clock is None:
            cls._clock = pygame.time.Clock()
        raw = cls._clock.tick(fps) / 1000.0
        # Cap huge deltas (window drag, debugger pause) so physics stays sane.
        cls.unscaled_delta_time = min(raw, 0.1)
        cls.delta_time = cls.unscaled_delta_time * cls.time_scale
        cls.elapsed_time += cls.unscaled_delta_time
