# zen-temple

<p align="center">
  <img src="https://github.com/user-attachments/assets/3b3466ec-9a18-4cd6-8d42-1327de6764a9" alt="zen-temple logo" width="600">
</p>

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**zen-temple** is a zero-build, zero-magic frontend component system for backend developers. Built on Jinja2, HTMX, and Alpine.js — fully transparent, fully controllable.

## 🎯 Philosophy

zen-temple follows the **Zero Template** philosophy:

- **No build step required** - Edit templates and see changes immediately
- **No hidden abstractions** - What you write is what runs
- **Template-centered design** - Templates are the source of truth
- **Jinja Macros for components** - Encapsulate HTML + JavaScript together
- **Class-based state** - Use `new ComponentState()`, never inline objects
- **Explicit data flow** - HTMX fetches JSON, passes to Alpine methods
- **Computed properties via getters** - Use JavaScript `get` accessors
- **Loose coupling** - Components are independent and self-contained

### 🏛️ Zero-Legacy Architecture

**NEW:** zen-temple implements the **"Logic is Pure, Bridge is Minimal"** design principle:

- **Pure Logic Layer**: Business logic in vanilla Python classes (no framework dependencies)
- **Minimal Bridge**: Jinja macros connect logic to templates
- **Zero Legacy**: Clean separation ensures easy testing, reusability, and migration

```python
from zen_temple import PureLogic, TemplateManager

# 1. Pure Logic (vanilla Python)
class CounterLogic(PureLogic):
    def __init__(self, initial_value=0):
        self._value = initial_value
    
    def increment(self):
        self._value += 1
    
    def to_context(self):
        return {"count": self._value}

# 2. Minimal Bridge (automatic via TemplateManager)
counter = CounterLogic(initial_value=0)
manager = TemplateManager()
html = manager.render_component("counter", logic=counter)
```

See [ZERO_LEGACY_ARCHITECTURE.md](ZERO_LEGACY_ARCHITECTURE.md) for details.

Inspired by Svelte's reactive design philosophy, but without the build step.

## 🚀 Quick Start

### Installation

```bash
# Using uv (recommended)
uv pip install zen-temple

# Or using pip
pip install zen-temple
```

### Create Your First Project

```bash
# Create a new project with examples
zen-temple new my-app

# Create with a Flask development server
zen-temple new my-app --with-server

# Create without examples
zen-temple new my-app --no-examples
```

### Project Structure

```
my-app/
├── templates/
│   ├── layouts/
│   │   └── base.html          # Base layout with CDN imports
│   ├── components/
│   │   ├── counter.html       # Example: Alpine.js reactivity
│   │   ├── todo.html          # Example: State management
│   │   └── data_fetch.html    # Example: HTMX communication
│   └── index.html             # Main page
├── static/
│   ├── css/                   # Custom styles (optional)
│   └── js/                    # Custom Alpine.js stores (optional)
├── app/                       # Flask server (if --with-server)
│   └── main.py
└── zen-temple.yaml            # Project configuration
```

## 📚 Core Concepts

### Components as Jinja Macros

Components are defined as Jinja macros with encapsulated JavaScript classes:

```html
<!-- templates/components/counter.html -->
{%- macro counter(initial_count=0) -%}
<div 
    x-data="new CounterState({{ initial_count }})"
    class="bg-white rounded-lg shadow p-6"
>
    <h3 class="text-xl font-semibold mb-4">Counter</h3>
    <button @click="increment()">+</button>
    <span x-text="count"></span>
    <button @click="decrement()">-</button>
</div>

<script>
// CounterState - Encapsulated component logic
class CounterState {
    constructor(initialCount = 0) {
        this.count = initialCount;
    }
    
    increment() {
        this.count++;
    }
    
    decrement() {
        this.count--;
    }
    
    // Computed property using getter
    get double() {
        return this.count * 2;
    }
}
</script>
{%- endmacro -%}
```

Use components by importing and calling the macro:

```html
{% extends "layouts/base.html" %}
{% from "components/counter.html" import counter %}

{% block content %}
    {{ counter(initial_count=5) }}
{% endblock %}
```

### Class-Based State Management

All state must be managed through JavaScript classes instantiated with `new`:

- ✅ **Do**: `x-data="new ComponentState()"`
- ❌ **Don't**: `x-data="{ count: 0 }"` (inline objects)
- ❌ **Don't**: `Alpine.store()` or `Alpine.data()` (global state)

### HTMX with Explicit Data Flow

HTMX fetches JSON data, which is then explicitly passed to Alpine.js methods:

```html
<div 
    x-data="new DataState()"
    @htmx:after-request="sync($event.detail.xhr.response)"
>
    <button 
        hx-get="/api/data"
        hx-swap="none"
        class="bg-blue-500 text-white px-4 py-2 rounded"
    >
        Load Data
    </button>
    <ul>
        <template x-for="item in items" :key="item.id">
            <li x-text="item.name"></li>
        </template>
    </ul>
</div>

<script>
class DataState {
    constructor() {
        this.items = [];
    }
    
    // Explicit data sync method called by HTMX
    sync(jsonData) {
        const data = JSON.parse(jsonData);
        this.items = data.items || [];
    }
}
</script>
```

Server returns JSON (not HTML):

```python
@app.route('/api/data')
def get_data():
    return jsonify({'items': [...]})
```

### Computed Properties

Use JavaScript getters for computed values:

```javascript
class TodoState {
    constructor() {
        this.todos = [];
    }
    
    // Computed property - automatically reactive in Alpine
    get completedCount() {
        return this.todos.filter(t => t.completed).length;
    }
}
```

Access in template: `<span x-text="completedCount"></span>`

## 🛠️ CLI Commands

### Create a New Project

```bash
zen-temple new <project-name> [OPTIONS]

Options:
  --path TEXT          Parent directory (default: current directory)
  --no-examples        Skip example components
  --with-server        Include Flask development server
```

### Generate Components

```bash
zen-temple component <component-name> [OPTIONS]

Options:
  --type [basic|form|list|card]  Component type (default: basic)
  --output TEXT                  Output directory
```

**Component types:**
- `basic` - Simple component with Alpine.js state
- `form` - Form component with validation
- `list` - List component with data loading
- `card` - Card/widget component

### Initialize Configuration

```bash
zen-temple init [OPTIONS]

Options:
  --project-name TEXT   Name of your project (prompted if not provided)
  --template-dir TEXT   Templates directory (default: templates)
```

### Validate Components

```bash
zen-temple validate <component-path>
```

Checks for:
- Inline JavaScript (should use Alpine.js instead)
- Inline event handlers (should use Alpine.js directives)
- Proper HTMX usage
- Template structure

### List Components

```bash
zen-temple list-components [OPTIONS]

Options:
  --template-dir TEXT  Templates directory (default: templates)
```

### Show Philosophy

```bash
zen-temple philosophy
```

Displays the zen-temple design philosophy and principles.

## 🧪 Python API

### Template Manager

```python
from zen_temple import TemplateManager
from pathlib import Path

# Initialize with template directories
manager = TemplateManager(template_dirs=[Path("templates")])

# Render a component
html = manager.render_component("counter", count=0)

# Render from string
html = manager.render_string("<div>{{ message }}</div>", {"message": "Hello"})

# List available components
components = manager.list_components()

# Check if component exists
if manager.component_exists("my-component"):
    html = manager.render_component("my-component")
```

### Pure Logic Layer (Zero-Legacy Architecture)

```python
from zen_temple import PureLogic, TemplateManager
from typing import Dict, Any

# Define pure business logic (no framework dependencies)
class TodoListLogic(PureLogic):
    def __init__(self):
        self._todos = []
    
    def add_todo(self, text: str):
        self._todos.append({"id": len(self._todos), "text": text, "done": False})
    
    def to_context(self) -> Dict[str, Any]:
        """Minimal bridge to templates"""
        return {"todos": self._todos}

# Use logic with templates
todos = TodoListLogic()
todos.add_todo("Learn zen-temple")
todos.add_todo("Build an app")

manager = TemplateManager()
html = manager.render_component("todo_list", logic=todos)
```

### Component Validator

```python
from zen_temple import ComponentValidator
from pathlib import Path

validator = ComponentValidator()

# Validate a component file
result = validator.validate_component(Path("templates/components/my-component.html"))

if result.is_valid:
    print("✓ Component is valid")
else:
    for error in result.errors:
        print(f"✗ {error}")
    for warning in result.warnings:
        print(f"⚠ {warning}")

# Validate component content
result = validator.validate_string("<div x-data='{ count: 0 }'></div>", "inline")
```

### Scaffold Generator

```python
from zen_temple import ScaffoldGenerator
from pathlib import Path

generator = ScaffoldGenerator(project_root=Path.cwd())

# Generate a complete project
created_paths = generator.generate_project(
    project_name="my-app",
    include_examples=True,
    include_server=False
)

# Generate a single component
component_path = generator.generate_component(
    component_name="my-widget",
    component_type="basic",
    output_dir=Path("templates/components")
)
```

## 📦 Technology Stack

- **[HTMX](https://htmx.org/)** - AJAX, WebSockets, and Server-Sent Events
- **[Alpine.js](https://alpinejs.dev/)** - Reactive and declarative JavaScript
- **[Jinja2](https://jinja.palletsprojects.com/)** - Template engine
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS (via CDN)

All dependencies are loaded from CDN - no build step required!

## 🎓 Examples

### Counter Component with Macro

A reactive counter using Jinja macro and class-based state:

```html
<!-- templates/components/counter.html -->
{%- macro counter(initial_count=0) -%}
<div x-data="new CounterState({{ initial_count }})">
    <button @click="decrement()">-</button>
    <span x-text="count"></span>
    <button @click="increment()">+</button>
    <p>Double: <span x-text="double"></span></p>
</div>

<script>
class CounterState {
    constructor(initialCount = 0) {
        this.count = initialCount;
    }
    
    increment() { this.count++; }
    decrement() { this.count--; }
    
    get double() { return this.count * 2; }
}
</script>
{%- endmacro -%}
```

Usage:
```html
{% from "components/counter.html" import counter %}
{{ counter(initial_count=5) }}
```

### Todo List with Class State

A todo list with class-based state management:

```html
{%- macro todo() -%}
<div x-data="new TodoState()">
    <input x-model="newTodo" @keyup.enter="addTodo()" />
    <button @click="addTodo()">Add</button>
    
    <ul>
        <template x-for="todo in todos" :key="todo.id">
            <li>
                <input type="checkbox" :checked="todo.completed" @change="toggleTodo(todo.id)" />
                <span :class="{ 'line-through': todo.completed }" x-text="todo.text"></span>
                <button @click="removeTodo(todo.id)">Delete</button>
            </li>
        </template>
    </ul>
    
    <p>Completed: <span x-text="completedCount"></span></p>
</div>

<script>
class TodoState {
    constructor() {
        this.todos = [];
        this.newTodo = '';
    }
    
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
    
    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) todo.completed = !todo.completed;
    }
    
    removeTodo(id) {
        this.todos = this.todos.filter(t => t.id !== id);
    }
    
    get completedCount() {
        return this.todos.filter(t => t.completed).length;
    }
}
</script>
{%- endmacro -%}
```

### HTMX Data Fetching with Explicit Flow

Fetch JSON data and sync to Alpine class:

```html
{%- macro data_fetch() -%}
<div 
    x-data="new DataState()"
    @htmx:after-request="sync($event.detail.xhr.response)"
>
    <button hx-get="/api/data" hx-swap="none">
        Load Data
    </button>
    
    <ul>
        <template x-for="item in items" :key="item.id">
            <li x-text="item.name"></li>
        </template>
    </ul>
</div>

<script>
class DataState {
    constructor() {
        this.items = [];
    }
    
    sync(jsonData) {
        const data = JSON.parse(jsonData);
        this.items = data.items || [];
    }
}
</script>
{%- endmacro -%}
```

Server endpoint:
```python
@app.route('/api/data')
def get_data():
    return jsonify({'items': [{'id': 1, 'name': 'Item 1'}]})
```
```

## 🧑‍💻 Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/mame7743/zen-temple.git
cd zen-temple

# Install with uv (recommended)
uv pip install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Running with Coverage

```bash
pytest --cov=zen_temple --cov-report=html
```

### Linting and Formatting

```bash
# Run ruff
ruff check src/

# Format code
ruff format src/
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [Svelte](https://svelte.dev/)'s reactive design philosophy
- Built on the shoulders of [HTMX](https://htmx.org/), [Alpine.js](https://alpinejs.dev/), and [Jinja2](https://jinja.palletsprojects.com/)
- Special thanks to the Python web development community

## 📞 Support

- 🐛 Report bugs on [GitHub Issues](https://github.com/mame7743/zen-temple/issues)
- 💬 Ask questions on [GitHub Discussions](https://github.com/mame7743/zen-temple/discussions)

---

**zen-temple**: Zero Template, Zero Build, Zero Magic ✨
