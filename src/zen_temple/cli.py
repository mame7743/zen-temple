"""Command-line interface for zen-temple."""

import sys
from pathlib import Path
from typing import Optional

import click

from zen_temple import __version__
from zen_temple.scaffold import ScaffoldGenerator
from zen_temple.template_manager import TemplateManager
from zen_temple.validator import ComponentValidator


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    """
    zen-temple: A zero-build, zero-magic frontend component system.

    Build reactive web UIs using HTMX, Alpine.js, Jinja2, and Tailwind CSS.
    """
    pass


@main.command()
@click.argument("project_name")
@click.option(
    "--path",
    type=click.Path(),
    default=".",
    help="Parent directory for the project (default: current directory)",
)
@click.option("--no-examples", is_flag=True, help="Skip creating example components")
@click.option("--with-server", is_flag=True, help="Include a basic Flask development server")
def new(project_name: str, path: str, no_examples: bool, with_server: bool) -> None:
    """
    Create a new zen-temple project.

    This generates a complete project structure with:
    - Base templates and layouts
    - Configuration files
    - Example components (unless --no-examples is specified)
    - Optional Flask server (with --with-server)

    Example:
        zen-temple new my-app
        zen-temple new my-app --with-server
    """
    click.echo(f"Creating new zen-temple project: {project_name}")

    generator = ScaffoldGenerator(project_root=Path(path))

    try:
        created = generator.generate_project(
            project_name=project_name, include_examples=not no_examples, include_server=with_server
        )

        click.echo("\n✓ Project created successfully!")
        click.echo("\nCreated files:")
        for name in sorted(created.keys()):
            click.echo(f"  - {name}")

        click.echo("\nNext steps:")
        click.echo(f"  cd {project_name}")

        if with_server:
            click.echo("  pip install -r requirements.txt")
            click.echo("  python app/main.py")
        else:
            click.echo("  # Edit templates in templates/ directory")
            click.echo("  # View zen-temple.yaml for configuration")

        click.echo("\nHappy building! 🎨")

    except Exception as e:
        click.echo(f"Error creating project: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("component_name")
@click.option(
    "--type",
    "component_type",
    type=click.Choice(["basic", "form", "list", "card"]),
    default="basic",
    help="Type of component to generate",
)
@click.option(
    "--output", type=click.Path(), help="Output directory (default: templates/components)"
)
def component(component_name: str, component_type: str, output: Optional[str]) -> None:
    """
    Generate a new component template.

    Components are self-contained, reusable HTML templates with Alpine.js
    for state management and HTMX for server communication.

    Component types:
        - basic: Simple component with Alpine.js state
        - form: Form component with validation
        - list: List component with data loading
        - card: Card/widget component

    Example:
        zen-temple component my-widget
        zen-temple component user-form --type form
    """
    click.echo(f"Generating {component_type} component: {component_name}")

    generator = ScaffoldGenerator()
    output_dir = Path(output) if output else None

    try:
        component_path = generator.generate_component(
            component_name=component_name, component_type=component_type, output_dir=output_dir
        )

        click.echo(f"✓ Component created: {component_path}")
        click.echo("\nTo use this component:")
        click.echo(f'  {{% include "components/{component_name}.html" %}}')

    except Exception as e:
        click.echo(f"Error creating component: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--project-name", prompt="Project name", help="Name of your project")
@click.option(
    "--template-dir", default="templates", help="Templates directory (default: templates)"
)
def init(project_name: str, template_dir: str) -> None:
    """
    Initialize zen-temple configuration in an existing project.

    This creates a zen-temple.yaml configuration file with sensible defaults.
    Use this if you want to add zen-temple to an existing project.

    Example:
        zen-temple init --project-name my-app
    """
    click.echo(f"Initializing zen-temple configuration for: {project_name}")

    generator = ScaffoldGenerator()
    project_path = Path.cwd()

    try:
        config_file = generator._create_config_file(project_path, project_name)
        click.echo(f"✓ Configuration created: {config_file}")

        # Create template directories if they don't exist
        template_path = project_path / template_dir
        template_path.mkdir(exist_ok=True)
        (template_path / "components").mkdir(exist_ok=True)
        (template_path / "layouts").mkdir(exist_ok=True)

        click.echo(f"✓ Template directories created in {template_dir}/")

    except Exception as e:
        click.echo(f"Error initializing project: {e}", err=True)
        sys.exit(1)


@main.command()
@click.argument("component_path", type=click.Path(exists=True))
def validate(component_path: str) -> None:
    """
    Validate a component template.

    Checks that the component follows zen-temple philosophy:
    - No inline JavaScript (use Alpine.js)
    - Proper HTMX usage
    - Clean template structure

    Example:
        zen-temple validate templates/components/my-component.html
    """
    click.echo(f"Validating component: {component_path}")

    validator = ComponentValidator()
    path = Path(component_path)

    result = validator.validate_component(path)

    if result.is_valid:
        click.echo(click.style("✓ Component is valid!", fg="green"))
    else:
        click.echo(click.style("✗ Component has issues:", fg="red"))

    if result.errors:
        click.echo("\nErrors:")
        for error in result.errors:
            click.echo(click.style(f"  - {error}", fg="red"))

    if result.warnings:
        click.echo("\nWarnings:")
        for warning in result.warnings:
            click.echo(click.style(f"  - {warning}", fg="yellow"))

    if not result.is_valid:
        sys.exit(1)


@main.command()
@click.option(
    "--template-dir",
    default="templates",
    type=click.Path(exists=True),
    help="Templates directory to list from",
)
def list_components(template_dir: str) -> None:
    """
    List all available components in the project.

    Example:
        zen-temple list-components
        zen-temple list-components --template-dir my-templates
    """
    manager = TemplateManager(template_dirs=[Path(template_dir)])
    components = manager.list_components()

    if components:
        click.echo(f"Found {len(components)} component(s):")
        for component in components:
            click.echo(f"  - {component}")
    else:
        click.echo("No components found.")
        click.echo("\nCreate a component with: zen-temple component <name>")


@main.command()
def philosophy() -> None:
    """
    Display the zen-temple design philosophy.

    Understanding these principles will help you build better applications
    with zen-temple.
    """
    philosophy_text = """
╔════════════════════════════════════════════════════════════════╗
║                   zen-temple Philosophy                         ║
║              (Zero Template - Zero Build - Zero Magic)          ║
╚════════════════════════════════════════════════════════════════╝

1. No Build Step Required
   Edit templates and see changes immediately. No webpack, no bundlers,
   no compilation. Just reload the page.

2. No Hidden Abstractions
   What you write is what runs. No magic transformations, no hidden
   complexity. Templates are templates.

3. Template-Centered Design
   Templates are the source of truth. Everything flows from HTML.
   Components are just Jinja2 includes.

4. Logic in Alpine.js
   State management belongs in x-data functions. Keep HTML declarative.
   Use Alpine.js for all client-side reactivity.

5. Server Returns JSON/HTML
   API endpoints return JSON data or HTML fragments. Let the client
   decide how to handle it (Alpine.js or HTMX).

6. HTMX for Communication
   Use HTMX for all server communication and events. No manual fetch()
   calls unless you need fine-grained control.

7. Zero Magic
   Every line of code is visible and editable. No code generation,
   no build artifacts, no hidden files.

Technology Stack:
  • HTMX      - Server communication and dynamic updates
  • Alpine.js - Reactive state and client-side logic
  • Jinja2    - Template rendering and composition
  • Tailwind  - Styling via CDN (no build needed)

Learn more at: https://github.com/mame7743/zen-temple
"""
    click.echo(philosophy_text)


if __name__ == "__main__":
    main()
