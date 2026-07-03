"""AudioManager: singleton script that plays procedurally generated sounds."""

from __future__ import annotations

import array
import random
from pathlib import Path
from typing import ClassVar

import pygame

from space_invaders.core.mono_behaviour import MonoBehaviour

_SOUNDS_DIR = Path(__file__).resolve().parents[3] / "assets" / "sounds"

_MARCH_FREQS = [110.0, 104.0, 98.0, 92.0]


class AudioManager(MonoBehaviour):
    """Singleton providing all sound effects.

    Loads .wav files from assets/sounds/ when present; otherwise every sound
    is synthesized as 16-bit PCM square waves / noise built with the stdlib
    ``array`` module and fed to ``pygame.mixer.Sound(buffer=...)``.

    Usage:
        AudioManager.instance.play("shoot")
    """

    instance: ClassVar["AudioManager | None"] = None

    def awake(self) -> None:
        AudioManager.instance = self
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._init = pygame.mixer.get_init()
        if self._init is None:
            return  # no audio device — all play() calls become no-ops
        self._build_sounds()

    def on_destroy(self) -> None:
        if AudioManager.instance is self:
            self.stop("ufo_loop")
            AudioManager.instance = None

    def play(self, sound_name: str) -> None:
        """Plays a sound once (no-op if audio is unavailable)."""
        sound = self._sounds.get(sound_name)
        if sound is not None:
            sound.play()

    def play_loop(self, sound_name: str) -> None:
        """Plays a sound on infinite loop until stop() is called."""
        sound = self._sounds.get(sound_name)
        if sound is not None:
            sound.play(loops=-1)

    def stop(self, sound_name: str) -> None:
        """Stops all playing instances of a sound."""
        sound = self._sounds.get(sound_name)
        if sound is not None:
            sound.stop()

    # ------------------------------------------------------------------ #

    def _build_sounds(self) -> None:
        specs: dict[str, pygame.mixer.Sound] = {
            "shoot": self._sweep(1400.0, 400.0, 0.12, steps=8),
            "explosion_invader": self._noise(0.12, 0.35),
            "explosion_player": self._noise(0.5, 0.5),
            "barrier_hit": self._noise(0.05, 0.2),
            "ufo_loop": self._warble(950.0, 720.0, 0.05, cycles=6),
        }
        for i, freq in enumerate(_MARCH_FREQS, start=1):
            specs[f"march_{i}"] = self._tone(freq, 0.09, 0.4)
        for name, synthesized in specs.items():
            wav = _SOUNDS_DIR / f"{name}.wav"
            if wav.exists():
                self._sounds[name] = pygame.mixer.Sound(str(wav))
            else:
                self._sounds[name] = synthesized
        self._sounds["ufo_loop"].set_volume(0.25)

    def _samples_to_sound(self, samples: array.array) -> pygame.mixer.Sound:
        """Converts mono int16 samples to a Sound matching the mixer format."""
        _, _, channels = self._init
        if channels == 2:
            stereo = array.array("h")
            for s in samples:
                stereo.append(s)
                stereo.append(s)
            samples = stereo
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def _tone(self, freq: float, duration: float, volume: float) -> pygame.mixer.Sound:
        """Square wave tone."""
        rate = self._init[0]
        amp = int(32767 * volume)
        period = rate / freq
        n = int(rate * duration)
        samples = array.array(
            "h", (amp if (i / period) % 1.0 < 0.5 else -amp for i in range(n))
        )
        return self._samples_to_sound(samples)

    def _noise(self, duration: float, volume: float) -> pygame.mixer.Sound:
        """White noise burst (explosions, barrier chips)."""
        rate = self._init[0]
        amp = int(32767 * volume)
        n = int(rate * duration)
        samples = array.array("h", (random.randint(-amp, amp) for _ in range(n)))
        return self._samples_to_sound(samples)

    def _segments(self, freqs: list[float], seg_dur: float, volume: float) -> array.array:
        rate = self._init[0]
        amp = int(32767 * volume)
        samples = array.array("h")
        for freq in freqs:
            period = rate / freq
            n = int(rate * seg_dur)
            samples.extend(
                amp if (i / period) % 1.0 < 0.5 else -amp for i in range(n)
            )
        return samples

    def _sweep(
        self, start: float, end: float, duration: float, steps: int
    ) -> pygame.mixer.Sound:
        """Descending frequency sweep (player shot)."""
        freqs = [start + (end - start) * i / (steps - 1) for i in range(steps)]
        return self._samples_to_sound(self._segments(freqs, duration / steps, 0.3))

    def _warble(
        self, high: float, low: float, seg_dur: float, cycles: int
    ) -> pygame.mixer.Sound:
        """Alternating two-tone warble (UFO loop)."""
        freqs = [high if i % 2 == 0 else low for i in range(cycles)]
        return self._samples_to_sound(self._segments(freqs, seg_dur, 0.3))
