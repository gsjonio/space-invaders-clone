"""Tests for GameObject component container and lifecycle."""

from space_invaders.components.transform import Transform
from space_invaders.core.game_object import GameObject
from space_invaders.core.mono_behaviour import MonoBehaviour


class Probe(MonoBehaviour):
    """Records lifecycle calls."""

    def __init__(self) -> None:
        self.calls: list[str] = []

    def awake(self) -> None:
        self.calls.append("awake")

    def start(self) -> None:
        self.calls.append("start")

    def on_enable(self) -> None:
        self.calls.append("on_enable")

    def on_disable(self) -> None:
        self.calls.append("on_disable")

    def on_destroy(self) -> None:
        self.calls.append("on_destroy")


def test_game_object_has_transform_by_default() -> None:
    go = GameObject("Empty")
    assert isinstance(go.transform, Transform)
    assert go.get_component(Transform) is go.transform


def test_add_component_sets_back_ref_and_calls_awake() -> None:
    go = GameObject("Test")
    probe = go.add_component(Probe())
    assert probe.game_object is go
    assert probe.calls == ["awake"]


def test_get_component_returns_first_of_type_or_none() -> None:
    go = GameObject("Test")
    first = go.add_component(Probe())
    second = go.add_component(Probe())
    assert go.get_component(Probe) is first
    assert go.get_components(Probe) == [first, second]

    class Unattached(MonoBehaviour):
        pass

    assert go.get_component(Unattached) is None


def test_active_toggle_fires_enable_disable() -> None:
    go = GameObject("Test")
    probe = go.add_component(Probe())
    go.active = False
    assert probe.calls[-1] == "on_disable"
    go.active = True
    assert probe.calls[-1] == "on_enable"
    # Setting the same value again must not re-fire.
    go.active = True
    assert probe.calls.count("on_enable") == 1


def test_destroy_marks_and_calls_on_destroy_once() -> None:
    go = GameObject("Test")
    probe = go.add_component(Probe())
    go.destroy()
    go.destroy()
    assert go.destroyed
    assert probe.calls.count("on_destroy") == 1
