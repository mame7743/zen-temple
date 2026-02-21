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
    assert any("インラインスクリプト" in err for err in result.errors)


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
    assert any("インラインイベントハンドラー" in err for err in result.errors)


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
    assert any("見つかりません" in err for err in result.errors)


def test_validate_class_based_xdata() -> None:
    """Test that class-based x-data passes without warnings."""
    validator = ComponentValidator()

    content = """{%- macro counter(initial_count=0) -%}
<div x-data="new CounterState({{ initial_count }})">
    <span x-text="count"></span>
</div>
<script>
class CounterState {
    constructor(n) { this.count = n; }
}
</script>
{%- endmacro -%}"""
    result = validator.validate_string(content, "counter")

    assert result.is_valid
    assert len(result.errors) == 0
    # Class-based x-data should not trigger the inline object warning
    assert not any("インラインオブジェクト" in w for w in result.warnings)


def test_validate_inline_xdata_warns() -> None:
    """Test that inline x-data object triggers a ZEN philosophy warning."""
    validator = ComponentValidator()

    content = '<div x-data="{ count: 0 }"><span x-text="count"></span></div>'
    result = validator.validate_string(content, "bad_inline")

    # Should still be valid (warning, not error)
    assert result.is_valid
    # But should warn about inline object
    assert any("インラインオブジェクト" in w for w in result.warnings)


def test_validate_macro_wrapper_missing_warns() -> None:
    """Test that a component without a macro wrapper triggers a warning."""
    validator = ComponentValidator()

    content = '<div x-data="new FooState()"><span x-text="msg"></span></div>'
    result = validator.validate_string(content, "no_macro")

    assert result.is_valid
    assert any("macro" in w.lower() for w in result.warnings)


def test_validate_macro_wrapper_present() -> None:
    """Test that a component with a macro wrapper does not trigger the macro warning."""
    validator = ComponentValidator()

    content = """{%- macro my_component() -%}
<div x-data="new MyComponentState()">
    <span x-text="msg"></span>
</div>
<script>
class MyComponentState { constructor() { this.msg = 'hi'; } }
</script>
{%- endmacro -%}"""
    result = validator.validate_string(content, "my_component")

    assert result.is_valid
    assert not any("macro" in w.lower() for w in result.warnings)


def test_validate_server_state_mutation_warns() -> None:
    """Test that push/splice/pop on this.xxx triggers a ZEN philosophy warning."""
    validator = ComponentValidator()

    content = """{%- macro bad_component() -%}
<div x-data="new BadState()">
    <button @click="addItem()">Add</button>
</div>
<script>
class BadState {
    constructor() { this.items = []; }
    addItem() {
        this.items.push({ id: Date.now(), name: 'new item' });
    }
}
</script>
{%- endmacro -%}"""
    result = validator.validate_string(content, "bad_component")

    assert result.is_valid
    assert any("push" in w or "splice" in w or "pop" in w for w in result.warnings)


def test_validate_sfc_pattern_compliant() -> None:
    """Test that a fully ZEN-compliant SFC component passes with no errors or ZEN warnings."""
    validator = ComponentValidator()

    content = """{%- macro todo() -%}
<div x-data="new TodoState()" x-init="init()">
    <ul>
        <template x-for="item in items" :key="item.id">
            <li x-text="item.text"></li>
        </template>
    </ul>
</div>
<script>
class TodoState {
    constructor() {
        this.items = [];
    }
    async init() {
        const response = await fetch('/api/todos');
        const data = await response.json();
        this.items = data.items;
    }
}
</script>
{%- endmacro -%}"""
    result = validator.validate_string(content, "todo")

    assert result.is_valid
    assert len(result.errors) == 0
    # Should have no ZEN-philosophy warnings
    assert not any("インラインオブジェクト" in w for w in result.warnings)
    assert not any("push" in w for w in result.warnings)
    assert not any("macro" in w.lower() for w in result.warnings)
