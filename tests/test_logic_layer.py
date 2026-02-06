"""Tests for the logic layer (Zero-Legacy Architecture)."""

from dataclasses import dataclass
from typing import Any

import pytest

from zen_temple.logic_layer import (
    ComponentLogic,
    ComponentState,
    LogicBridge,
    PureLogic,
    create_macro_helpers,
)


class SimpleLogic(PureLogic):
    """Simple logic class for testing."""

    def __init__(self, value: int = 0):
        self.value = value

    def to_context(self) -> dict[str, Any]:
        return {"value": self.value}


class CounterLogic(PureLogic):
    """Counter logic for testing."""

    def __init__(self, initial_value: int = 0):
        self._value = initial_value

    def increment(self) -> int:
        self._value += 1
        return self._value

    def decrement(self) -> int:
        self._value -= 1
        return self._value

    def to_context(self) -> dict[str, Any]:
        return {"count": self._value}


@dataclass
class TestState(ComponentState):
    """Test state for ComponentState."""

    value: int
    name: str


def test_pure_logic_abstraction():
    """Test that PureLogic is an abstract base class."""
    with pytest.raises(TypeError):
        # Should not be able to instantiate abstract class
        PureLogic()


def test_simple_logic_to_context():
    """Test simple logic to_context conversion."""
    logic = SimpleLogic(value=42)
    context = logic.to_context()

    assert context == {"value": 42}


def test_counter_logic():
    """Test counter logic implementation."""
    counter = CounterLogic(initial_value=0)

    # Test initial state
    assert counter.to_context() == {"count": 0}

    # Test increment
    counter.increment()
    assert counter.to_context() == {"count": 1}

    # Test multiple increments
    counter.increment()
    counter.increment()
    assert counter.to_context() == {"count": 3}

    # Test decrement
    counter.decrement()
    assert counter.to_context() == {"count": 2}


def test_component_state_to_dict():
    """Test ComponentState to_dict method."""
    state = TestState(value=100, name="test")
    state_dict = state.to_dict()

    assert state_dict == {"value": 100, "name": "test"}


def test_logic_bridge_init():
    """Test LogicBridge initialization."""
    bridge = LogicBridge()
    assert bridge is not None
    assert bridge._logic_registry == {}


def test_logic_bridge_register():
    """Test registering logic classes."""
    bridge = LogicBridge()
    bridge.register_logic("counter", CounterLogic)

    assert "counter" in bridge._logic_registry
    assert bridge._logic_registry["counter"] == CounterLogic


def test_logic_bridge_prepare_context():
    """Test preparing context from logic."""
    bridge = LogicBridge()
    logic = CounterLogic(initial_value=5)

    context = bridge.prepare_context(logic)
    assert context == {"count": 5}


def test_logic_bridge_prepare_context_with_extra():
    """Test preparing context with extra context."""
    bridge = LogicBridge()
    logic = SimpleLogic(value=10)

    extra = {"user": "alice", "theme": "dark"}
    context = bridge.prepare_context(logic, extra_context=extra)

    assert context == {"value": 10, "user": "alice", "theme": "dark"}


def test_logic_bridge_create_logic():
    """Test creating logic instances by name."""
    bridge = LogicBridge()
    bridge.register_logic("counter", CounterLogic)

    # Create instance
    logic = bridge.create_logic("counter", initial_value=10)
    assert logic is not None
    assert isinstance(logic, CounterLogic)
    assert logic.to_context() == {"count": 10}


def test_logic_bridge_create_logic_not_found():
    """Test creating logic for non-existent name."""
    bridge = LogicBridge()

    logic = bridge.create_logic("nonexistent")
    assert logic is None


def test_component_logic_init():
    """Test ComponentLogic initialization."""
    logic = ComponentLogic()

    assert logic.component_id is not None
    assert logic.component_id.startswith("component-")


def test_component_logic_custom_id():
    """Test ComponentLogic with custom ID."""
    logic = ComponentLogic(component_id="my-component")

    assert logic.component_id == "my-component"


def test_component_logic_to_context():
    """Test ComponentLogic to_context includes ID."""
    logic = ComponentLogic(component_id="test-123")
    context = logic.to_context()

    assert "component_id" in context
    assert context["component_id"] == "test-123"


def test_create_macro_helpers():
    """Test creating macro helpers."""
    helpers = create_macro_helpers()

    assert "prepare_alpine_data" in helpers
    assert "serialize_state" in helpers

    # Test prepare_alpine_data
    logic = SimpleLogic(value=42)
    data = helpers["prepare_alpine_data"](logic)
    assert data == {"value": 42}

    # Test serialize_state
    state = TestState(value=100, name="test")
    serialized = helpers["serialize_state"](state)
    assert serialized == {"value": 100, "name": "test"}


def test_logic_is_pure():
    """Test that logic classes are pure (no framework dependencies)."""
    # This test verifies the principle "Logic is Pure"
    # CounterLogic should have no dependencies on web frameworks

    counter = CounterLogic(0)

    # Should work without any framework context
    counter.increment()
    counter.increment()
    counter.decrement()

    # Should produce clean context
    context = counter.to_context()
    assert isinstance(context, dict)
    assert "count" in context

    # Logic should be JSON-serializable (no complex objects)
    import json

    json_str = json.dumps(context)
    assert json_str == '{"count": 1}'


def test_bridge_is_minimal():
    """Test that bridge is minimal (only to_context method)."""
    # This test verifies the principle "Bridge is Minimal"

    logic = SimpleLogic(value=99)
    bridge = LogicBridge()

    # Bridge should only need to_context() to work
    context = bridge.prepare_context(logic)

    # No complex translation, just direct context
    assert context == logic.to_context()

    # Bridge should not modify or enhance the context
    assert context == {"value": 99}
