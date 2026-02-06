"""
Example: Counter Logic with Pure/Bridge Architecture

This demonstrates the "Logic is Pure, Bridge is Minimal" design principle.

1. Pure Logic Layer: CounterLogic class is vanilla Python (no dependencies)
2. Minimal Bridge: Jinja macro connects logic to template
3. Zero Legacy: Clean separation between logic and presentation
"""

from typing import Any

from zen_temple import PureLogic


class CounterLogic(PureLogic):
    """
    Pure business logic for a counter component.

    This class has NO dependencies on web frameworks, templates, or UI.
    It's pure Python that can be tested, reused, and understood independently.
    """

    def __init__(self, initial_value: int = 0, step: int = 1):
        """
        Initialize counter logic.

        Args:
            initial_value: Starting value for the counter
            step: Amount to increment/decrement by
        """
        self._value = initial_value
        self._step = step
        self._history = [initial_value]

    @property
    def value(self) -> int:
        """Get current counter value."""
        return self._value

    def increment(self) -> int:
        """
        Increment the counter.

        Returns:
            New counter value
        """
        self._value += self._step
        self._history.append(self._value)
        return self._value

    def decrement(self) -> int:
        """
        Decrement the counter.

        Returns:
            New counter value
        """
        self._value -= self._step
        self._history.append(self._value)
        return self._value

    def reset(self) -> int:
        """
        Reset counter to initial value.

        Returns:
            Reset value
        """
        self._value = self._history[0]
        self._history.append(self._value)
        return self._value

    def can_decrement(self) -> bool:
        """Check if counter can be decremented (e.g., not below 0)."""
        return self._value - self._step >= 0

    def get_history(self) -> list:
        """Get counter history."""
        return self._history.copy()

    def to_context(self) -> dict[str, Any]:
        """
        Convert logic state to template context.

        This is the minimal bridge to templates.
        Returns only what the template needs to render.
        """
        return {
            "count": self._value,
            "step": self._step,
            "can_decrement": self.can_decrement(),
            "history_count": len(self._history),
        }


def demo():
    """Demonstrate the counter logic."""
    from pathlib import Path

    from zen_temple import TemplateManager

    # Create pure logic instance (no template dependencies)
    counter = CounterLogic(initial_value=0, step=1)

    # Test logic independently (pure Python)
    print("Testing pure logic:")
    print(f"Initial value: {counter.value}")

    counter.increment()
    print(f"After increment: {counter.value}")

    counter.increment()
    counter.increment()
    print(f"After 2 more increments: {counter.value}")

    counter.decrement()
    print(f"After decrement: {counter.value}")

    print(f"Can decrement? {counter.can_decrement()}")
    print(f"History: {counter.get_history()}")

    # Now connect to template via minimal bridge
    print("\nConnecting to template via LogicBridge:")

    TemplateManager(template_dirs=[Path(__file__).parent / "templates"])

    # Render using the logic instance (bridge is automatic)
    # The template manager uses LogicBridge internally
    context = counter.to_context()
    print(f"Template context: {context}")

    # In a real application, you would:
    # html = template_manager.render_component("counter", logic=counter)


if __name__ == "__main__":
    demo()
