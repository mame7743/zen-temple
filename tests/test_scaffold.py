"""Tests for ScaffoldGenerator."""

from pathlib import Path

from zen_temple.scaffold import ScaffoldGenerator


def test_scaffold_init(tmp_path: Path) -> None:
    """Test ScaffoldGenerator initialization."""
    generator = ScaffoldGenerator(project_root=tmp_path)
    assert generator.project_root == tmp_path


def test_generate_project(tmp_path: Path) -> None:
    """Test generating a complete project."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    generator.generate_project(
        project_name="test_project", include_examples=True, include_server=False
    )

    project_path = tmp_path / "test_project"

    # Check that directories were created
    assert (project_path / "templates").exists()
    assert (project_path / "templates/components").exists()
    assert (project_path / "templates/layouts").exists()
    assert (project_path / "static").exists()

    # Check that files were created
    assert (project_path / "zen-temple.yaml").exists()
    assert (project_path / "templates/layouts/base.html").exists()
    assert (project_path / "README.md").exists()

    # Check example components
    assert (project_path / "templates/components/counter.html").exists()
    assert (project_path / "templates/components/todo.html").exists()
    assert (project_path / "templates/index.html").exists()


def test_generate_project_with_server(tmp_path: Path) -> None:
    """Test generating a project with server files."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    generator.generate_project(
        project_name="server_project", include_examples=False, include_server=True
    )

    project_path = tmp_path / "server_project"

    # Check server files
    assert (project_path / "app").exists()
    assert (project_path / "app/main.py").exists()
    assert (project_path / ".env").exists()
    assert (project_path / "requirements.txt").exists()


def test_generate_project_no_examples(tmp_path: Path) -> None:
    """Test generating a project without examples."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    generator.generate_project(
        project_name="minimal_project", include_examples=False, include_server=False
    )

    project_path = tmp_path / "minimal_project"

    # Should have basic structure
    assert (project_path / "templates").exists()
    assert (project_path / "zen-temple.yaml").exists()

    # Should not have example components
    assert not (project_path / "templates/components/counter.html").exists()


def test_generate_component(tmp_path: Path) -> None:
    """Test generating a component."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    output_dir = tmp_path / "components"
    component_path = generator.generate_component(
        component_name="test_component", component_type="basic", output_dir=output_dir
    )

    assert component_path.exists()
    assert component_path.name == "test_component.html"

    content = component_path.read_text()
    assert "test_component" in content
    assert "x-data" in content


def test_generate_different_component_types(tmp_path: Path) -> None:
    """Test generating different component types."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    output_dir = tmp_path / "components"

    component_types = ["basic", "form", "list", "card"]

    for comp_type in component_types:
        component_path = generator.generate_component(
            component_name=f"{comp_type}_component", component_type=comp_type, output_dir=output_dir
        )

        assert component_path.exists()
        content = component_path.read_text()
        assert f"{comp_type}_component" in content


def test_create_base_layout(tmp_path: Path) -> None:
    """Test creating base layout."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    layout_path = generator._create_base_layout(tmp_path)

    assert layout_path.exists()
    content = layout_path.read_text()

    # Check for required CDN imports in generated template
    # Note: These are literal strings in our template, not user input
    assert "htmx.org" in content
    assert "alpinejs" in content
    assert "tailwindcss.com" in content

    # Check for Jinja2 blocks
    assert "{% block" in content


def test_create_config_file(tmp_path: Path) -> None:
    """Test creating configuration file."""
    generator = ScaffoldGenerator(project_root=tmp_path)

    config_path = generator._create_config_file(tmp_path, "test_project")

    assert config_path.exists()
    assert config_path.name == "zen-temple.yaml"

    content = config_path.read_text()
    assert "test_project" in content
    assert "htmx" in content
    assert "alpine" in content
