"""Tests for the calculator logic example."""

import pytest

from examples.calculator_logic import CalculatorLogic


def test_calculator_init():
    """Test calculator initialization."""
    calc = CalculatorLogic()
    assert calc.display == "0"
    assert calc.to_context()["display"] == "0"
    assert not calc.to_context()["has_operation"]


def test_input_single_digit():
    """Test inputting a single digit."""
    calc = CalculatorLogic()
    result = calc.input_digit("5")
    assert result == "5"
    assert calc.display == "5"


def test_input_multiple_digits():
    """Test inputting multiple digits."""
    calc = CalculatorLogic()
    calc.input_digit("1")
    calc.input_digit("2")
    calc.input_digit("3")
    assert calc.display == "123"


def test_input_leading_zero_replaced():
    """Test that leading zero is replaced."""
    calc = CalculatorLogic()
    calc.input_digit("0")
    calc.input_digit("5")
    assert calc.display == "5"


def test_input_decimal():
    """Test inputting decimal point."""
    calc = CalculatorLogic()
    calc.input_digit("5")
    calc.input_decimal()
    calc.input_digit("5")
    assert calc.display == "5.5"


def test_input_decimal_leading():
    """Test inputting decimal point as first character."""
    calc = CalculatorLogic()
    calc.input_decimal()
    calc.input_digit("5")
    assert calc.display == "0.5"


def test_input_decimal_no_duplicate():
    """Test that decimal point can only be added once."""
    calc = CalculatorLogic()
    calc.input_digit("5")
    calc.input_decimal()
    calc.input_decimal()  # Should be ignored
    calc.input_digit("5")
    assert calc.display == "5.5"


def test_invalid_digit():
    """Test that invalid digit raises error."""
    calc = CalculatorLogic()
    with pytest.raises(ValueError):
        calc.input_digit("a")


def test_addition():
    """Test addition operation."""
    calc = CalculatorLogic()
    calc.input_digit("5")
    calc.input_operation("+")
    calc.input_digit("3")
    result = calc.calculate()
    assert result == "8"


def test_subtraction():
    """Test subtraction operation."""
    calc = CalculatorLogic()
    calc.input_digit("9")
    calc.input_operation("-")
    calc.input_digit("4")
    result = calc.calculate()
    assert result == "5"


def test_multiplication():
    """Test multiplication operation."""
    calc = CalculatorLogic()
    calc.input_digit("6")
    calc.input_operation("*")
    calc.input_digit("7")
    result = calc.calculate()
    assert result == "42"


def test_division():
    """Test division operation."""
    calc = CalculatorLogic()
    calc.input_digit("8")
    calc.input_operation("/")
    calc.input_digit("2")
    result = calc.calculate()
    assert result == "4"


def test_division_by_zero():
    """Test division by zero returns error."""
    calc = CalculatorLogic()
    calc.input_digit("5")
    calc.input_operation("/")
    calc.input_digit("0")
    result = calc.calculate()
    assert result == "Error"


def test_invalid_operation():
    """Test that invalid operation raises error."""
    calc = CalculatorLogic()
    with pytest.raises(ValueError):
        calc.input_operation("%")


def test_chained_operations():
    """Test chained operations (e.g., 2 + 3 + 4)."""
    calc = CalculatorLogic()
    calc.input_digit("2")
    calc.input_operation("+")
    calc.input_digit("3")
    calc.input_operation("+")  # Should calculate 2+3 first
    assert calc.display == "5"
    calc.input_digit("4")
    calc.calculate()
    assert calc.display == "9"


def test_decimal_result():
    """Test result with decimal places."""
    calc = CalculatorLogic()
    calc.input_digit("7")
    calc.input_operation("/")
    calc.input_digit("2")
    result = calc.calculate()
    assert result == "3.5"


def test_clear():
    """Test clear resets calculator."""
    calc = CalculatorLogic()
    calc.input_digit("5")
    calc.input_operation("+")
    calc.input_digit("3")
    calc.clear()
    assert calc.display == "0"
    assert not calc.to_context()["has_operation"]


def test_clear_entry():
    """Test clear entry clears current display."""
    calc = CalculatorLogic()
    calc.input_digit("5")
    calc.input_operation("+")
    calc.input_digit("3")
    calc.clear_entry()
    assert calc.display == "0"


def test_history():
    """Test calculation history."""
    calc = CalculatorLogic()

    # First calculation
    calc.input_digit("2")
    calc.input_operation("+")
    calc.input_digit("3")
    calc.calculate()

    # Second calculation
    calc.input_digit("5")
    calc.input_operation("*")
    calc.input_digit("2")
    calc.calculate()

    history = calc.get_history()
    assert len(history) == 2
    assert "2.0 + 3.0 = 5.0" in history[0]
    assert "5.0 * 2.0 = 10.0" in history[1]


def test_clear_history():
    """Test clearing history."""
    calc = CalculatorLogic()
    calc.input_digit("5")
    calc.input_operation("+")
    calc.input_digit("3")
    calc.calculate()

    calc.clear_history()
    assert len(calc.get_history()) == 0
    assert calc.to_context()["history_count"] == 0


def test_to_context():
    """Test to_context returns correct data."""
    calc = CalculatorLogic()
    calc.input_digit("5")
    calc.input_operation("+")

    context = calc.to_context()
    assert context["display"] == "5"
    assert context["has_operation"] is True
    assert context["operation"] == "+"
    assert context["history_count"] == 0


def test_logic_is_pure():
    """Test that calculator logic is pure (no framework dependencies)."""
    calc = CalculatorLogic()

    # Should work without any framework context
    calc.input_digit("5")
    calc.input_operation("+")
    calc.input_digit("3")
    calc.calculate()

    # Should produce clean context
    context = calc.to_context()
    assert isinstance(context, dict)
    assert "display" in context

    # Logic should be JSON-serializable
    import json

    json_str = json.dumps(context)
    assert "display" in json_str


def test_negative_numbers():
    """Test operations with negative results."""
    calc = CalculatorLogic()
    calc.input_digit("3")
    calc.input_operation("-")
    calc.input_digit("5")
    result = calc.calculate()
    assert result == "-2"


def test_zero_result():
    """Test operations resulting in zero."""
    calc = CalculatorLogic()
    calc.input_digit("5")
    calc.input_operation("-")
    calc.input_digit("5")
    result = calc.calculate()
    assert result == "0"


def test_large_numbers():
    """Test operations with large numbers."""
    calc = CalculatorLogic()
    calc.input_digit("9")
    calc.input_digit("9")
    calc.input_digit("9")
    calc.input_operation("*")
    calc.input_digit("9")
    calc.input_digit("9")
    calc.input_digit("9")
    result = calc.calculate()
    assert result == "998001"


def test_multiple_decimal_places():
    """Test result with multiple decimal places."""
    calc = CalculatorLogic()
    calc.input_digit("1")
    calc.input_operation("/")
    calc.input_digit("3")
    result = calc.calculate()
    # Should round to 8 decimal places
    assert "0.33333333" in result
