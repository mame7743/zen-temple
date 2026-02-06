"""Component validator for zen-temple."""

from pathlib import Path
from typing import List
import re
from pydantic import BaseModel, Field


class ValidationResult(BaseModel):
    """Result of component validation."""
    
    is_valid: bool
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    component_name: str
    
    def add_error(self, message: str) -> None:
        """Add an error message."""
        self.errors.append(message)
        self.is_valid = False
    
    def add_warning(self, message: str) -> None:
        """Add a warning message."""
        self.warnings.append(message)


class ComponentValidator:
    """
    Validates zen-temple component structure and adherence to design philosophy.
    
    Validates:
    - No inline JavaScript in HTML (use Alpine.js x-data instead)
    - Proper use of HTMX attributes
    - Alpine.js reactive patterns
    - Template structure
    """
    
    def __init__(self):
        """Initialize the validator."""
        self.rules = [
            self._check_inline_scripts,
            self._check_htmx_usage,
            self._check_alpine_usage,
            self._check_template_structure,
        ]
    
    def validate_component(self, component_path: Path) -> ValidationResult:
        """
        Validate a component file.
        
        Args:
            component_path: Path to the component HTML file
            
        Returns:
            ValidationResult with errors and warnings
        """
        result = ValidationResult(
            is_valid=True,
            component_name=component_path.stem
        )
        
        if not component_path.exists():
            result.add_error(f"Component file not found: {component_path}")
            return result
        
        content = component_path.read_text()
        
        # Run all validation rules
        for rule in self.rules:
            rule(content, result)
        
        return result
    
    def validate_string(self, content: str, component_name: str = "inline") -> ValidationResult:
        """
        Validate component content from a string.
        
        Args:
            content: HTML content to validate
            component_name: Name for the component (for error messages)
            
        Returns:
            ValidationResult with errors and warnings
        """
        result = ValidationResult(
            is_valid=True,
            component_name=component_name
        )
        
        for rule in self.rules:
            rule(content, result)
        
        return result
    
    def _check_inline_scripts(self, content: str, result: ValidationResult) -> None:
        """Check for inline scripts (which violate zen-temple philosophy)."""
        # Look for <script> tags that aren't CDN includes
        # Use a more robust regex that handles whitespace in closing tags
        script_pattern = r'<script(?![^>]*src=)[^>]*>[\s\S]*?</script[\s]*>'
        matches = re.finditer(script_pattern, content, re.IGNORECASE)
        
        for match in matches:
            script_content = match.group(0)
            # Allow Alpine.js inline initialization or HTMX extensions
            if 'x-data' not in script_content and 'htmx' not in script_content.lower():
                result.add_error(
                    "Inline script detected. Move logic to Alpine.js x-data functions."
                )
        
        # Check for inline event handlers
        inline_handlers = [
            r'onclick\s*=',
            r'onload\s*=',
            r'onchange\s*=',
            r'onsubmit\s*=',
        ]
        for pattern in inline_handlers:
            if re.search(pattern, content, re.IGNORECASE):
                result.add_error(
                    f"Inline event handler detected ({pattern}). Use Alpine.js @click, @change, etc."
                )
    
    def _check_htmx_usage(self, content: str, result: ValidationResult) -> None:
        """Check for proper HTMX usage."""
        # Look for HTMX attributes
        htmx_attrs = [
            'hx-get', 'hx-post', 'hx-put', 'hx-delete', 'hx-patch',
            'hx-trigger', 'hx-target', 'hx-swap', 'hx-select'
        ]
        
        has_htmx = any(attr in content for attr in htmx_attrs)
        
        if has_htmx:
            # Check that responses are expected to be JSON/HTML fragments, not full pages
            if 'hx-swap' in content:
                # Warn if potentially replacing full document
                if re.search(r'hx-swap\s*=\s*["\']outerHTML["\']', content):
                    result.add_warning(
                        "Using hx-swap='outerHTML' on full document. "
                        "Ensure server returns HTML fragments, not full pages."
                    )
    
    def _check_alpine_usage(self, content: str, result: ValidationResult) -> None:
        """Check for proper Alpine.js usage."""
        # Check for x-data (state management)
        if 'x-data' in content:
            # Ensure x-data is used properly
            x_data_pattern = r'x-data\s*=\s*["\']([^"\']*)["\']'
            matches = re.finditer(x_data_pattern, content)
            
            for match in matches:
                data_content = match.group(1)
                # Check if it looks like a function call or object
                if data_content and not ('{' in data_content or '(' in data_content):
                    result.add_warning(
                        f"x-data='{data_content}' should be a function call or object literal"
                    )
        
        # Check for Alpine directives
        alpine_directives = ['x-show', 'x-if', 'x-for', 'x-model', 'x-text', 'x-html']
        has_alpine = any(directive in content for directive in alpine_directives)
        
        if not has_alpine and 'x-data' not in content:
            result.add_warning(
                "No Alpine.js directives found. Consider using Alpine.js for reactive behavior."
            )
    
    def _check_template_structure(self, content: str, result: ValidationResult) -> None:
        """Check basic template structure."""
        # Check for Jinja2 blocks or includes
        if '{% block' in content or '{% extends' in content or '{% include' in content:
            # This is good - using Jinja2 template inheritance
            pass
        else:
            # Standalone component - should have some structure
            if '<html' in content.lower() and '</html>' in content.lower():
                result.add_warning(
                    "Component contains full HTML document. "
                    "Consider breaking into reusable component fragments."
                )
