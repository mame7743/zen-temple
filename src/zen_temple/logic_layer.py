"""
Pure Logic Layer for zen-temple components.

This module implements the "Logic is Pure, Bridge is Minimal" design principle.
All business logic should be in vanilla Python classes, with Jinja macros serving
as the minimal bridge to templates.

Design Principles:
1. Vanilla Class Isolation: Logic is pure Python, no framework dependencies
2. Minimal Bridge: Jinja macros connect logic to templates
3. Zero Legacy: Clean separation between logic and presentation
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict


class PureLogic(ABC):
    """
    Base class for pure business logic.
    
    All business logic should extend this class and remain framework-independent.
    Logic classes should contain only pure Python code with no dependencies on
    web frameworks, template engines, or UI libraries.
    
    Example:
        class CounterLogic(PureLogic):
            def __init__(self, initial_value: int = 0):
                self.value = initial_value
            
            def increment(self) -> int:
                self.value += 1
                return self.value
            
            def decrement(self) -> int:
                self.value -= 1
                return self.value
            
            def to_context(self) -> Dict[str, Any]:
                return {"count": self.value}
    """
    
    @abstractmethod
    def to_context(self) -> Dict[str, Any]:
        """
        Convert logic state to template context.
        
        Returns:
            Dictionary of variables to pass to template
        """
        pass


@dataclass
class ComponentState:
    """
    Immutable state container for components.
    
    Use dataclass for type safety and automatic serialization.
    All state should be JSON-serializable for Alpine.js compatibility.
    
    Example:
        @dataclass
        class TodoState(ComponentState):
            todos: List[Dict[str, Any]]
            new_todo: str = ""
    """
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary."""
        return asdict(self)


class LogicBridge:
    """
    Minimal bridge between pure logic and templates.
    
    This class provides utilities to connect vanilla Python logic classes
    with Jinja2 templates using macros as the interface layer.
    
    Example:
        bridge = LogicBridge()
        counter_logic = CounterLogic(initial_value=0)
        context = bridge.prepare_context(counter_logic)
        # Use context in template rendering
    """
    
    def __init__(self):
        """Initialize the logic bridge."""
        self._logic_registry: Dict[str, type] = {}
    
    def register_logic(self, name: str, logic_class: type) -> None:
        """
        Register a logic class.
        
        Args:
            name: Name to register the logic class under
            logic_class: The logic class to register
        """
        self._logic_registry[name] = logic_class
    
    def prepare_context(
        self,
        logic: PureLogic,
        extra_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Prepare template context from logic instance.
        
        Args:
            logic: Pure logic instance
            extra_context: Additional context variables
            
        Returns:
            Complete context dictionary for template rendering
        """
        context = logic.to_context()
        
        if extra_context:
            context.update(extra_context)
        
        return context
    
    def create_logic(self, name: str, **kwargs: Any) -> Optional[PureLogic]:
        """
        Create a logic instance by name.
        
        Args:
            name: Registered name of the logic class
            **kwargs: Arguments to pass to logic constructor
            
        Returns:
            Logic instance or None if not found
        """
        logic_class = self._logic_registry.get(name)
        if logic_class is None:
            return None
        
        return logic_class(**kwargs)


class ComponentLogic(PureLogic):
    """
    Base class for component business logic.
    
    Provides common functionality for component-level logic.
    Components should extend this class for reusable logic patterns.
    """
    
    def __init__(self, component_id: Optional[str] = None):
        """
        Initialize component logic.
        
        Args:
            component_id: Optional unique identifier for the component
        """
        self.component_id = component_id or self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate a unique component ID."""
        import uuid
        return f"component-{uuid.uuid4().hex[:8]}"
    
    def to_context(self) -> Dict[str, Any]:
        """
        Default context includes component ID.
        
        Override this method to add more context.
        """
        return {
            "component_id": self.component_id
        }


def create_macro_helpers() -> Dict[str, Any]:
    """
    Create helper functions for use in Jinja macros.
    
    These helpers serve as the minimal bridge between Python logic
    and template macros.
    
    Returns:
        Dictionary of helper functions for Jinja environment
    """
    def prepare_alpine_data(logic: PureLogic) -> Dict[str, Any]:
        """Prepare logic context for Alpine.js x-data."""
        return logic.to_context()
    
    def serialize_state(state: ComponentState) -> Dict[str, Any]:
        """Serialize component state for templates."""
        return state.to_dict()
    
    return {
        "prepare_alpine_data": prepare_alpine_data,
        "serialize_state": serialize_state,
    }
