"""Template Manager for zen-temple components."""

from pathlib import Path
from typing import Any, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from zen_temple.logic_layer import LogicBridge, PureLogic, create_macro_helpers


class TemplateManager:
    """
    Manages Jinja2 templates for zen-temple components.

    Follows zen-temple philosophy:
    - Templates are the source of truth
    - No build step required
    - Clear, transparent rendering
    - Logic is Pure, Bridge is Minimal (via LogicBridge)
    """

    def __init__(
        self, template_dirs: Optional[list[Path]] = None, logic_bridge: Optional[LogicBridge] = None
    ):
        """
        Initialize the template manager.

        Args:
            template_dirs: List of directories to search for templates
            logic_bridge: Optional logic bridge for connecting pure logic to templates
        """
        if template_dirs is None:
            template_dirs = [Path.cwd() / "templates"]

        self.template_dirs = [Path(d) for d in template_dirs]
        self.logic_bridge = logic_bridge or LogicBridge()
        self._setup_environment()

    def _setup_environment(self) -> None:
        """Set up the Jinja2 environment with appropriate settings."""
        loader = FileSystemLoader([str(d) for d in self.template_dirs])
        self.env = Environment(
            loader=loader,
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Add custom filters for zen-temple
        self.env.filters["json_encode"] = self._json_encode_filter

        # Add macro helpers to globals (bridge between logic and templates)
        macro_helpers = create_macro_helpers()
        self.env.globals.update(macro_helpers)

    @staticmethod
    def _json_encode_filter(value: Any) -> str:
        """Filter to safely encode values as JSON for Alpine.js."""
        import json

        from markupsafe import Markup

        return Markup(json.dumps(value))

    def render_component(
        self,
        component_name: str,
        context: Optional[dict[str, Any]] = None,
        logic: Optional[PureLogic] = None,
        **kwargs: Any,
    ) -> str:
        """
        Render a component template.

        Args:
            component_name: Name of the component template
            context: Context dictionary for rendering
            logic: Optional pure logic instance (follows "Logic is Pure" principle)
            **kwargs: Additional context variables

        Returns:
            Rendered HTML string
        """
        if context is None:
            context = {}

        # If logic is provided, prepare context from it (minimal bridge)
        if logic is not None:
            logic_context = self.logic_bridge.prepare_context(logic, extra_context=context)
            context = logic_context

        context.update(kwargs)

        template = self.env.get_template(f"{component_name}.html")
        return template.render(**context)

    def render_string(self, template_string: str, context: Optional[dict[str, Any]] = None) -> str:
        """
        Render a template from a string.

        Args:
            template_string: Template string to render
            context: Context dictionary for rendering

        Returns:
            Rendered HTML string
        """
        if context is None:
            context = {}
        template = self.env.from_string(template_string)
        return template.render(**context)

    def add_template_dir(self, template_dir: Path) -> None:
        """
        Add a new template directory to the search path.

        Args:
            template_dir: Path to template directory
        """
        if template_dir not in self.template_dirs:
            self.template_dirs.append(Path(template_dir))
            self._setup_environment()

    def list_components(self) -> list[str]:
        """
        List all available component templates.

        Returns:
            List of component names (without .html extension)
        """
        components = []
        for template_dir in self.template_dirs:
            if template_dir.exists():
                for file in template_dir.glob("*.html"):
                    component_name = file.stem
                    if component_name not in components:
                        components.append(component_name)
        return sorted(components)

    def component_exists(self, component_name: str) -> bool:
        """
        Check if a component template exists.

        Args:
            component_name: Name of the component

        Returns:
            True if component exists, False otherwise
        """
        try:
            self.env.get_template(f"{component_name}.html")
            return True
        except Exception:
            return False
