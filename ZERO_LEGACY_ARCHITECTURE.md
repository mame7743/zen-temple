# Zero-Legacy Architecture: Logic is Pure, Bridge is Minimal

## Design Principle

**Zen-Temple** follows a strict architectural pattern called **"Zero-Legacy Implementation"** where:

1. **Logic is Pure**: All business logic is isolated in vanilla Python classes with zero framework dependencies
2. **Bridge is Minimal**: Jinja macros serve as the minimal bridge between logic and presentation

This architecture ensures:
- **Testability**: Pure logic can be tested independently without templates or frameworks
- **Reusability**: Logic classes can be reused across different presentation layers
- **Maintainability**: Clear separation makes code easier to understand and modify
- **Zero Legacy**: No tight coupling to frameworks means easy migration and updates

## Architecture Layers

### 1. Pure Logic Layer (Vanilla Python)

Business logic lives in pure Python classes that extend `PureLogic`:

```python
from zen_temple import PureLogic
from typing import Dict, Any

class CounterLogic(PureLogic):
    """Pure business logic - no framework dependencies"""
    
    def __init__(self, initial_value: int = 0):
        self._value = initial_value
    
    def increment(self) -> int:
        self._value += 1
        return self._value
    
    def decrement(self) -> int:
        self._value -= 1
        return self._value
    
    def to_context(self) -> Dict[str, Any]:
        """Minimal bridge: export only what templates need"""
        return {"count": self._value}
```

**Key Principles:**
- NO imports from web frameworks (Flask, Django, etc.)
- NO imports from template engines (Jinja2, etc.)
- NO imports from UI libraries
- Pure Python only: standard library and domain-specific libraries

### 2. Minimal Bridge (Jinja Macros)

The `LogicBridge` class connects pure logic to templates:

```python
from zen_temple import TemplateManager

# Logic stays pure
counter = CounterLogic(initial_value=0)

# Bridge connects logic to template
template_manager = TemplateManager()
html = template_manager.render_component("counter", logic=counter)
```

The bridge is "minimal" because:
- Logic exposes only `to_context()` method
- No direct template dependencies in logic
- Bridge handles serialization automatically

### 3. Presentation Layer (Templates + Alpine.js)

Templates receive clean data from logic via the bridge:

```html
<!-- templates/counter.html -->
<!-- Jinja Macro: Minimal Bridge -->
{% macro counter_component(count) %}
<div x-data="{ count: {{ count }} }">
    <button @click="count--">-</button>
    <span x-text="count"></span>
    <button @click="count++">+</button>
</div>
{% endmacro %}

<!-- Use the macro -->
{{ counter_component(count=count) }}
```

## Benefits

### 1. Pure Logic is Testable

```python
# Test without any framework setup
def test_counter():
    counter = CounterLogic(0)
    assert counter.increment() == 1
    assert counter.increment() == 2
    assert counter.decrement() == 1
```

### 2. Logic is Reusable

```python
# Use same logic with different presentations
counter = CounterLogic(0)

# Web template
html = template_manager.render_component("counter", logic=counter)

# API response
json_data = counter.to_context()

# CLI display
print(f"Count: {counter.value}")
```

### 3. Easy Migration

```python
# Logic never changes when switching frameworks
counter = CounterLogic(0)

# Use with Flask
@app.route("/counter")
def counter_view():
    return render_template("counter.html", **counter.to_context())

# Use with FastAPI
@app.get("/counter")
def counter_view():
    return templates.TemplateResponse("counter.html", counter.to_context())
```

## Example: Todo List Logic

```python
from zen_temple import PureLogic
from typing import Dict, Any, List
from dataclasses import dataclass, asdict

@dataclass
class Todo:
    """Pure data structure"""
    id: int
    text: str
    completed: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TodoListLogic(PureLogic):
    """Pure business logic for todo list"""
    
    def __init__(self):
        self._todos: List[Todo] = []
        self._next_id = 1
    
    def add_todo(self, text: str) -> Todo:
        """Add a new todo"""
        todo = Todo(id=self._next_id, text=text)
        self._todos.append(todo)
        self._next_id += 1
        return todo
    
    def toggle_todo(self, todo_id: int) -> bool:
        """Toggle todo completion status"""
        for todo in self._todos:
            if todo.id == todo_id:
                todo.completed = not todo.completed
                return True
        return False
    
    def remove_todo(self, todo_id: int) -> bool:
        """Remove a todo"""
        self._todos = [t for t in self._todos if t.id != todo_id]
        return True
    
    def get_active_count(self) -> int:
        """Count active todos"""
        return sum(1 for t in self._todos if not t.completed)
    
    def to_context(self) -> Dict[str, Any]:
        """Minimal bridge to templates"""
        return {
            "todos": [t.to_dict() for t in self._todos],
            "active_count": self.get_active_count(),
            "total_count": len(self._todos),
        }
```

## Using with Templates

```python
from zen_temple import TemplateManager
from pathlib import Path

# Create logic
todos = TodoListLogic()
todos.add_todo("Learn zen-temple")
todos.add_todo("Build an app")

# Render with bridge
manager = TemplateManager(template_dirs=[Path("templates")])
html = manager.render_component("todo_list", logic=todos)
```

## Jinja Macro Example

```html
<!-- templates/macros/todo.html -->
{% macro todo_list_component(todos, active_count, total_count) %}
<div x-data="{
    todos: {{ todos | json_encode }},
    newTodo: '',
    addTodo() {
        if (this.newTodo.trim()) {
            this.todos.push({
                id: Date.now(),
                text: this.newTodo,
                completed: false
            });
            this.newTodo = '';
        }
    }
}">
    <h3>Todo List ({{ active_count }}/{{ total_count }} active)</h3>
    
    <input x-model="newTodo" @keyup.enter="addTodo()" />
    <button @click="addTodo()">Add</button>
    
    <ul>
        <template x-for="todo in todos" :key="todo.id">
            <li>
                <input type="checkbox" :checked="todo.completed" />
                <span x-text="todo.text"></span>
            </li>
        </template>
    </ul>
</div>
{% endmacro %}

<!-- templates/todo_list.html -->
{% from "macros/todo.html" import todo_list_component %}
{{ todo_list_component(todos=todos, active_count=active_count, total_count=total_count) }}
```

## Guidelines

### DO:
✓ Keep logic in vanilla Python classes  
✓ Test logic independently  
✓ Use `to_context()` as the bridge  
✓ Use Jinja macros for reusable template patterns  
✓ Keep Alpine.js for client-side interactivity  

### DON'T:
✗ Import web frameworks in logic classes  
✗ Mix business logic with template code  
✗ Tightly couple logic to specific frameworks  
✗ Put complex logic in templates  
✗ Create large bridges with many dependencies  

## Summary

The **Zero-Legacy Architecture** ensures your code is:
- **Pure**: Logic is framework-independent
- **Testable**: Easy to test without infrastructure
- **Reusable**: Logic works across different contexts
- **Maintainable**: Clear separation of concerns
- **Future-proof**: Easy to migrate and upgrade

By following **"Logic is Pure, Bridge is Minimal"**, you create code that stands the test of time.
