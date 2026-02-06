"""Tests for ComponentValidator."""

from pathlib import Path

from zen_temple.validator import ComponentValidator


def test_validator_init() -> None:
    """Test ComponentValidator initialization."""
    validator = ComponentValidator()
    assert validator is not None
    assert len(validator.rules) > 0


def test_validate_good_component(tmp_path: Path) -> None:
    """Test validating a good component."""
    component = tmp_path / "good.html"
    component.write_text("""
    <div x-data="{ count: 0 }">
        <button @click="count++">Increment</button>
        <span x-text="count"></span>
    </div>
    """)

    validator = ComponentValidator()
    result = validator.validate_component(component)

    assert result.is_valid
    assert len(result.errors) == 0


def test_validate_inline_script(tmp_path: Path) -> None:
    """Test detecting inline scripts."""
    component = tmp_path / "bad.html"
    component.write_text("""
    <div>
        <script>
            function bad() {
                console.log('inline script');
            }
        </script>
    </div>
    """)

    validator = ComponentValidator()
    result = validator.validate_component(component)

    assert not result.is_valid
    assert len(result.errors) > 0
    assert any("inline script" in err.lower() for err in result.errors)


def test_validate_inline_event_handler(tmp_path: Path) -> None:
    """Test detecting inline event handlers."""
    component = tmp_path / "bad.html"
    component.write_text("""
    <button onclick="doSomething()">Click</button>
    """)

    validator = ComponentValidator()
    result = validator.validate_component(component)

    assert not result.is_valid
    assert len(result.errors) > 0
    assert any("inline event handler" in err.lower() for err in result.errors)


def test_validate_htmx_usage(tmp_path: Path) -> None:
    """Test HTMX usage validation."""
    component = tmp_path / "htmx.html"
    component.write_text("""
    <button hx-get="/api/data" hx-target="#result">Load</button>
    <div id="result"></div>
    """)

    validator = ComponentValidator()
    result = validator.validate_component(component)

    # Should pass - proper HTMX usage
    assert result.is_valid


def test_validate_alpine_usage(tmp_path: Path) -> None:
    """Test Alpine.js usage validation."""
    component = tmp_path / "alpine.html"
    component.write_text("""
    <div x-data="{ open: false }">
        <button @click="open = !open">Toggle</button>
        <div x-show="open">Content</div>
    </div>
    """)

    validator = ComponentValidator()
    result = validator.validate_component(component)

    assert result.is_valid


def test_validate_string() -> None:
    """Test validating component from string."""
    validator = ComponentValidator()

    good_content = '<div x-data="{ count: 0 }"><span x-text="count"></span></div>'
    result = validator.validate_string(good_content, "test")

    assert result.is_valid
    assert result.component_name == "test"


def test_validate_nonexistent_file(tmp_path: Path) -> None:
    """Test validating a non-existent file."""
    validator = ComponentValidator()
    result = validator.validate_component(tmp_path / "nonexistent.html")

    assert not result.is_valid
    assert len(result.errors) > 0
    assert any("not found" in err.lower() for err in result.errors)
