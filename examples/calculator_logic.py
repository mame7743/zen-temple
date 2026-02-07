"""
Example: Calculator Logic with Pure/Bridge Architecture

This demonstrates the "Logic is Pure, Bridge is Minimal" design principle
for a calculator component.

1. Pure Logic Layer: CalculatorLogic class is vanilla Python (no dependencies)
2. Minimal Bridge: Jinja macro connects logic to template
3. Zero Legacy: Clean separation between logic and presentation
"""

from typing import Any

from zen_temple import PureLogic


class CalculatorLogic(PureLogic):
    """
    Pure business logic for a calculator component.

    This class has NO dependencies on web frameworks, templates, or UI.
    It's pure Python that can be tested, reused, and understood independently.
    """

    # Constants
    DECIMAL_PRECISION = 8  # Number of decimal places for display

    def __init__(self):
        """Initialize calculator logic."""
        self._display = "0"
        self._current_value = 0.0
        self._previous_value = 0.0
        self._operation = None
        self._new_number = True
        self._history = []

    @property
    def display(self) -> str:
        """Get current display value."""
        return self._display

    def input_digit(self, digit: str) -> str:
        """
        Input a digit (0-9) into the calculator.

        Args:
            digit: Single digit character ('0'-'9')

        Returns:
            New display value
        """
        if not digit.isdigit():
            raise ValueError(f"Invalid digit: {digit}")

        if self._new_number:
            self._display = digit
            self._new_number = False
        else:
            # Avoid multiple leading zeros
            if self._display == "0":
                self._display = digit
            else:
                self._display += digit

        return self._display

    def input_decimal(self) -> str:
        """
        Input a decimal point.

        Returns:
            New display value
        """
        if self._new_number:
            self._display = "0."
            self._new_number = False
        elif "." not in self._display:
            self._display += "."

        return self._display

    def input_operation(self, operation: str) -> str:
        """
        Input an operation (+, -, *, /).

        Args:
            operation: Operation character ('+', '-', '*', '/')

        Returns:
            New display value
        """
        if operation not in ["+", "-", "*", "/"]:
            raise ValueError(f"Invalid operation: {operation}")

        # If there's a pending operation, calculate it first
        if self._operation and not self._new_number:
            self.calculate()

        self._previous_value = float(self._display)
        self._operation = operation
        self._new_number = True

        return self._display

    def calculate(self) -> str:
        """
        Calculate the result of pending operation.

        Returns:
            Result display value
        """
        if not self._operation:
            return self._display

        self._current_value = float(self._display)

        try:
            if self._operation == "+":
                result = self._previous_value + self._current_value
            elif self._operation == "-":
                result = self._previous_value - self._current_value
            elif self._operation == "*":
                result = self._previous_value * self._current_value
            elif self._operation == "/":
                if self._current_value == 0:
                    self._display = "Error"
                    self._operation = None
                    self._new_number = True
                    return self._display
                result = self._previous_value / self._current_value
            else:
                return self._display

            # Format result
            if result == int(result):
                self._display = str(int(result))
            else:
                self._display = str(round(result, self.DECIMAL_PRECISION))

            # Add to history
            operation_str = f"{self._previous_value} {self._operation} {self._current_value} = {result}"
            self._history.append(operation_str)

            # Reset state
            self._operation = None
            self._new_number = True

        except Exception as e:
            self._display = "Error"
            self._operation = None
            self._new_number = True

        return self._display

    def clear(self) -> str:
        """
        Clear calculator (reset to initial state).

        Returns:
            Reset display value
        """
        self._display = "0"
        self._current_value = 0.0
        self._previous_value = 0.0
        self._operation = None
        self._new_number = True
        return self._display

    def clear_entry(self) -> str:
        """
        Clear current entry only.

        Returns:
            Cleared display value
        """
        self._display = "0"
        self._new_number = True
        return self._display

    def get_history(self) -> list:
        """
        Get calculation history.

        Returns:
            List of calculation strings
        """
        return self._history.copy()

    def clear_history(self) -> None:
        """Clear calculation history."""
        self._history = []

    def to_context(self) -> dict[str, Any]:
        """
        Convert logic state to template context.

        This is the minimal bridge to templates.
        Returns only what the template needs to render.
        """
        return {
            "display": self._display,
            "has_operation": self._operation is not None,
            "operation": self._operation or "",
            "history_count": len(self._history),
        }


def demo():
    """Demonstrate the calculator logic."""
    from pathlib import Path

    from zen_temple import TemplateManager

    # Create pure logic instance (no template dependencies)
    calc = CalculatorLogic()

    # Test logic independently (pure Python)
    print("Testing pure calculator logic:")
    print(f"Initial display: {calc.display}")

    # Test: 5 + 3 = 8
    calc.input_digit("5")
    print(f"After inputting 5: {calc.display}")

    calc.input_operation("+")
    print(f"After + operation: {calc.display}")

    calc.input_digit("3")
    print(f"After inputting 3: {calc.display}")

    result = calc.calculate()
    print(f"After calculate: {result}")

    # Test: 10 * 2 = 20
    calc.clear()
    calc.input_digit("1")
    calc.input_digit("0")
    print(f"After inputting 10: {calc.display}")

    calc.input_operation("*")
    calc.input_digit("2")
    result = calc.calculate()
    print(f"10 * 2 = {result}")

    # Test: Division
    calc.clear()
    calc.input_digit("8")
    calc.input_operation("/")
    calc.input_digit("2")
    result = calc.calculate()
    print(f"8 / 2 = {result}")

    # Test: Division by zero
    calc.clear()
    calc.input_digit("5")
    calc.input_operation("/")
    calc.input_digit("0")
    result = calc.calculate()
    print(f"5 / 0 = {result}")

    # Show history
    print(f"\nCalculation history:")
    for entry in calc.get_history():
        print(f"  {entry}")

    # Show context for template
    print("\nTemplate context:")
    context = calc.to_context()
    print(f"  {context}")


if __name__ == "__main__":
    demo()
