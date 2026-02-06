"""Tests for TemplateManager."""

import pytest
from pathlib import Path
from zen_temple.template_manager import TemplateManager
from zen_temple.logic_layer import PureLogic
from typing import Dict, Any


class TestLogic(PureLogic):
    """Test logic class for template manager tests."""
    
    def __init__(self, value: int = 0):
        self.value = value
    
    def to_context(self) -> Dict[str, Any]:
        return {"test_value": self.value}


def test_template_manager_init(tmp_path: Path) -> None:
    """Test TemplateManager initialization."""
    manager = TemplateManager(template_dirs=[tmp_path])
    assert manager.template_dirs == [tmp_path]


def test_render_string(tmp_path: Path) -> None:
    """Test rendering a template from string."""
    manager = TemplateManager(template_dirs=[tmp_path])
    
    template_str = "<h1>{{ title }}</h1>"
    result = manager.render_string(template_str, {"title": "Test"})
    
    assert result == "<h1>Test</h1>"


def test_render_component(tmp_path: Path) -> None:
    """Test rendering a component template."""
    # Create a test component
    component_file = tmp_path / "test.html"
    component_file.write_text("<div>{{ content }}</div>")
    
    manager = TemplateManager(template_dirs=[tmp_path])
    result = manager.render_component("test", content="Hello")
    
    assert result == "<div>Hello</div>"


def test_render_component_with_logic(tmp_path: Path) -> None:
    """Test rendering a component with pure logic (Zero-Legacy Architecture)."""
    # Create a test component that uses logic context
    component_file = tmp_path / "test_logic.html"
    component_file.write_text("<div>Value: {{ test_value }}</div>")
    
    # Create pure logic instance
    logic = TestLogic(value=42)
    
    # Render with logic (bridge is automatic)
    manager = TemplateManager(template_dirs=[tmp_path])
    result = manager.render_component("test_logic", logic=logic)
    
    assert result == "<div>Value: 42</div>"


def test_render_component_logic_with_extra_context(tmp_path: Path) -> None:
    """Test rendering with logic and extra context."""
    component_file = tmp_path / "test.html"
    component_file.write_text("<div>{{ test_value }} - {{ extra }}</div>")
    
    logic = TestLogic(value=10)
    
    manager = TemplateManager(template_dirs=[tmp_path])
    result = manager.render_component("test", logic=logic, extra="data")
    
    assert "10" in result
    assert "data" in result


def test_list_components(tmp_path: Path) -> None:
    """Test listing available components."""
    # Create some test components
    (tmp_path / "comp1.html").write_text("<div>1</div>")
    (tmp_path / "comp2.html").write_text("<div>2</div>")
    
    manager = TemplateManager(template_dirs=[tmp_path])
    components = manager.list_components()
    
    assert "comp1" in components
    assert "comp2" in components
    assert len(components) == 2


def test_component_exists(tmp_path: Path) -> None:
    """Test checking if component exists."""
    (tmp_path / "existing.html").write_text("<div>exists</div>")
    
    manager = TemplateManager(template_dirs=[tmp_path])
    
    assert manager.component_exists("existing")
    assert not manager.component_exists("non_existing")


def test_json_encode_filter(tmp_path: Path) -> None:
    """Test JSON encoding filter for Alpine.js."""
    manager = TemplateManager(template_dirs=[tmp_path])
    
    template_str = "<div x-data='{{ data | json_encode }}'></div>"
    result = manager.render_string(template_str, {"data": {"key": "value"}})
    
    assert '{"key": "value"}' in result


def test_logic_bridge_integration(tmp_path: Path) -> None:
    """Test that LogicBridge is integrated into TemplateManager."""
    manager = TemplateManager(template_dirs=[tmp_path])
    
    # Manager should have a logic bridge
    assert manager.logic_bridge is not None
    
    # Create logic and test bridge functionality
    logic = TestLogic(value=99)
    context = manager.logic_bridge.prepare_context(logic)
    
    assert context == {"test_value": 99}

