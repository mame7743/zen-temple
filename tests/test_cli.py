"""Tests for CLI commands."""

import pytest
from click.testing import CliRunner
from pathlib import Path
from zen_temple.cli import main


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI runner."""
    return CliRunner()


def test_cli_help(runner: CliRunner) -> None:
    """Test CLI help command."""
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert 'zen-temple' in result.output


def test_cli_version(runner: CliRunner) -> None:
    """Test CLI version command."""
    result = runner.invoke(main, ['--version'])
    assert result.exit_code == 0


def test_new_project(runner: CliRunner, tmp_path: Path) -> None:
    """Test creating a new project."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(main, ['new', 'test_project'])
        assert result.exit_code == 0
        assert 'Project created successfully' in result.output
        
        # Check that project was created
        assert Path('test_project').exists()
        assert Path('test_project/zen-temple.yaml').exists()


def test_new_project_with_server(runner: CliRunner, tmp_path: Path) -> None:
    """Test creating a new project with server."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(main, ['new', 'server_project', '--with-server'])
        assert result.exit_code == 0
        
        # Check server files
        assert Path('server_project/app/main.py').exists()
        assert Path('server_project/requirements.txt').exists()


def test_new_project_no_examples(runner: CliRunner, tmp_path: Path) -> None:
    """Test creating a project without examples."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(main, ['new', 'minimal_project', '--no-examples'])
        assert result.exit_code == 0
        
        # Should not have example components
        assert not Path('minimal_project/templates/components/counter.html').exists()


def test_component_command(runner: CliRunner, tmp_path: Path) -> None:
    """Test component generation command."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Create templates directory
        Path('templates/components').mkdir(parents=True)
        
        result = runner.invoke(main, ['component', 'my_widget'])
        assert result.exit_code == 0
        assert 'Component created' in result.output
        
        # Check component was created
        assert Path('templates/components/my_widget.html').exists()


def test_component_with_type(runner: CliRunner, tmp_path: Path) -> None:
    """Test component generation with specific type."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        Path('templates/components').mkdir(parents=True)
        
        result = runner.invoke(main, ['component', 'user_form', '--type', 'form'])
        assert result.exit_code == 0
        
        component_path = Path('templates/components/user_form.html')
        assert component_path.exists()
        
        content = component_path.read_text()
        assert 'form' in content.lower()


def test_init_command(runner: CliRunner, tmp_path: Path) -> None:
    """Test init command."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        result = runner.invoke(main, ['init', '--project-name', 'my_project'])
        assert result.exit_code == 0
        assert 'Configuration created' in result.output
        
        # Check config was created
        assert Path('zen-temple.yaml').exists()


def test_validate_command(runner: CliRunner, tmp_path: Path) -> None:
    """Test validate command."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Create a valid component
        component_path = Path('test.html')
        component_path.write_text('<div x-data="{ count: 0 }"></div>')
        
        result = runner.invoke(main, ['validate', 'test.html'])
        assert result.exit_code == 0
        assert 'valid' in result.output.lower()


def test_validate_invalid_component(runner: CliRunner, tmp_path: Path) -> None:
    """Test validating an invalid component."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Create an invalid component with inline script
        component_path = Path('bad.html')
        component_path.write_text('<script>alert("bad");</script>')
        
        result = runner.invoke(main, ['validate', 'bad.html'])
        assert result.exit_code == 1
        assert 'issues' in result.output.lower()


def test_list_components(runner: CliRunner, tmp_path: Path) -> None:
    """Test list-components command."""
    with runner.isolated_filesystem(temp_dir=tmp_path):
        # Create some components
        Path('templates').mkdir()
        Path('templates/comp1.html').write_text('<div></div>')
        Path('templates/comp2.html').write_text('<div></div>')
        
        result = runner.invoke(main, ['list-components'])
        assert result.exit_code == 0
        assert 'comp1' in result.output
        assert 'comp2' in result.output


def test_philosophy_command(runner: CliRunner) -> None:
    """Test philosophy command."""
    result = runner.invoke(main, ['philosophy'])
    assert result.exit_code == 0
    assert 'zen-temple' in result.output
    assert 'Philosophy' in result.output
    assert 'HTMX' in result.output
    assert 'Alpine.js' in result.output
