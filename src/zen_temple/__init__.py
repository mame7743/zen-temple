"""
zen-temple: A zero-build, zero-magic frontend component system

This library provides tools for building web UIs using HTMX, Alpine.js, Jinja2, and
Tailwind CSS, following the zen-temple philosophy:
- No build step required
- No hidden abstractions
- Template-centered design
- Logic in Alpine.js x-data functions only
- Server returns JSON only
- HTMX for communication and events only

Architecture:
- Logic is Pure: Business logic in vanilla Python classes (logic_layer)
- Bridge is Minimal: Jinja macros connect logic to templates (LogicBridge)
"""

__version__ = "0.1.0"

from zen_temple.logic_layer import (
    ComponentLogic,
    ComponentState,
    LogicBridge,
    PureLogic,
    create_macro_helpers,
)
from zen_temple.scaffold import ScaffoldGenerator
from zen_temple.template_manager import TemplateManager
from zen_temple.validator import ComponentValidator

__all__ = [
    "TemplateManager",
    "ComponentValidator",
    "ScaffoldGenerator",
    "PureLogic",
    "ComponentState",
    "LogicBridge",
    "ComponentLogic",
    "create_macro_helpers",
]
