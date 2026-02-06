"""Pytest configuration and shared fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def sample_template_dir(tmp_path: Path) -> Path:
    """Create a temporary directory with sample templates."""
    templates_dir = tmp_path / "templates"
    templates_dir.mkdir()
    
    # Create a sample component
    component = templates_dir / "sample.html"
    component.write_text("""
    <div x-data="{ message: 'Hello' }">
        <span x-text="message"></span>
    </div>
    """)
    
    return templates_dir
