"""Scaffold generator for zen-temple projects."""

from pathlib import Path
from typing import Optional

import yaml


class ScaffoldGenerator:
    """
    Generates project scaffolding for zen-temple applications.

    Creates:
    - Project structure
    - Configuration files
    - Example components
    - Base templates
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the scaffold generator.

        Args:
            project_root: Root directory for the project (defaults to cwd)
        """
        self.project_root = project_root or Path.cwd()

    def generate_project(
        self,
        project_name: str,
        include_examples: bool = True,
        include_server: bool = False
    ) -> dict[str, Path]:
        """
        Generate a complete project structure.

        Args:
            project_name: Name of the project
            include_examples: Whether to include example components
            include_server: Whether to include a basic Flask server

        Returns:
            Dictionary mapping structure names to created paths
        """
        project_path = self.project_root / project_name
        created_paths = {}

        # Create directory structure
        directories = [
            project_path / "templates",
            project_path / "templates/components",
            project_path / "templates/layouts",
            project_path / "static",
            project_path / "static/css",
            project_path / "static/js",
        ]

        if include_server:
            directories.extend([
                project_path / "app",
                project_path / "app/routes",
            ])

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            created_paths[str(directory.relative_to(project_path))] = directory

        # Generate configuration file
        config_file = self._create_config_file(project_path, project_name)
        created_paths['zen-temple.yaml'] = config_file

        # Generate base layout
        base_layout = self._create_base_layout(project_path)
        created_paths['templates/layouts/base.html'] = base_layout

        # Generate example components if requested
        if include_examples:
            example_paths = self._create_example_components(project_path)
            created_paths.update(example_paths)

        # Generate server files if requested
        if include_server:
            server_paths = self._create_server_files(project_path, project_name)
            created_paths.update(server_paths)

        # Create README
        readme = self._create_readme(project_path, project_name, include_server)
        created_paths['README.md'] = readme

        return created_paths

    def generate_component(
        self,
        component_name: str,
        component_type: str = "basic",
        output_dir: Optional[Path] = None
    ) -> Path:
        """
        Generate a component template.

        Args:
            component_name: Name of the component
            component_type: Type of component (basic, form, list, card)
            output_dir: Directory to create component in

        Returns:
            Path to created component file
        """
        if output_dir is None:
            output_dir = self.project_root / "templates/components"

        output_dir.mkdir(parents=True, exist_ok=True)
        component_path = output_dir / f"{component_name}.html"

        template_content = self._get_component_template(component_name, component_type)
        component_path.write_text(template_content)

        return component_path

    def _create_config_file(self, project_path: Path, project_name: str) -> Path:
        """Create zen-temple configuration file."""
        config = {
            'project': {
                'name': project_name,
                'version': '0.1.0',
            },
            'templates': {
                'directories': ['templates', 'templates/components', 'templates/layouts'],
            },
            'cdn': {
                'htmx': 'https://unpkg.com/htmx.org@1.9.10',
                'alpine': 'https://unpkg.com/alpinejs@3.13.5/dist/cdn.min.js',
                'tailwind': 'https://cdn.tailwindcss.com',
            },
            'zen_temple': {
                'philosophy': [
                    'No build step required',
                    'No hidden abstractions',
                    'Template-centered design',
                    'Logic in Alpine.js x-data only',
                    'Server returns JSON only',
                    'HTMX for communication and events only',
                ]
            }
        }

        config_path = project_path / "zen-temple.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

        return config_path

    def _create_base_layout(self, project_path: Path) -> Path:
        """Create base HTML layout with HTMX, Alpine.js, and Tailwind."""
        layout_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}zen-temple App{% endblock %}</title>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>

    <!-- Alpine.js -->
    <script defer src="https://unpkg.com/alpinejs@3.13.5/dist/cdn.min.js"></script>

    {% block extra_head %}{% endblock %}
</head>
<body class="bg-gray-50 min-h-screen">
    <!-- Main container -->
    <div class="container mx-auto px-4 py-8">
        {% block content %}
        <!-- Page content goes here -->
        {% endblock %}
    </div>

    {% block extra_body %}{% endblock %}
</body>
</html>
'''
        layout_path = project_path / "templates/layouts/base.html"
        layout_path.parent.mkdir(parents=True, exist_ok=True)
        layout_path.write_text(layout_content)
        return layout_path

    def _create_example_components(self, project_path: Path) -> dict[str, Path]:
        """Create example components demonstrating zen-temple philosophy."""
        components = {}

        # Counter component (Alpine.js reactive example)
        counter_content = '''<!-- Counter Component - Demonstrates Alpine.js state management -->
<div
    x-data="{ count: 0 }"
    class="bg-white rounded-lg shadow-md p-6 max-w-md"
>
    <h3 class="text-xl font-semibold mb-4">Counter</h3>

    <div class="flex items-center justify-between mb-4">
        <button
            @click="count--"
            class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
            -
        </button>

        <span class="text-3xl font-bold" x-text="count"></span>

        <button
            @click="count++"
            class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
        >
            +
        </button>
    </div>

    <button
        @click="count = 0"
        class="w-full bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded"
    >
        Reset
    </button>
</div>
'''
        counter_path = project_path / "templates/components/counter.html"
        counter_path.write_text(counter_content)
        components['templates/components/counter.html'] = counter_path

        # Todo list component (HTMX + Alpine.js example)
        todo_content = '''<!-- Todo List Component - Demonstrates HTMX + Alpine.js integration -->
<div
    x-data="{
        todos: [],
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
        },
        toggleTodo(id) {
            const todo = this.todos.find(t => t.id === id);
            if (todo) todo.completed = !todo.completed;
        },
        removeTodo(id) {
            this.todos = this.todos.filter(t => t.id !== id);
        }
    }"
    class="bg-white rounded-lg shadow-md p-6 max-w-2xl"
>
    <h3 class="text-xl font-semibold mb-4">Todo List</h3>

    <!-- Add todo form -->
    <div class="flex gap-2 mb-4">
        <input
            type="text"
            x-model="newTodo"
            @keyup.enter="addTodo()"
            placeholder="Add a new todo..."
            class="flex-1 px-4 py-2 border border-gray-300 rounded focus:outline-none
                   focus:ring-2 focus:ring-blue-500"
        />
        <button
            @click="addTodo()"
            class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded"
        >
            Add
        </button>
    </div>

    <!-- Todo list -->
    <ul class="space-y-2">
        <template x-for="todo in todos" :key="todo.id">
            <li class="flex items-center gap-2 p-3 bg-gray-50 rounded">
                <input
                    type="checkbox"
                    :checked="todo.completed"
                    @change="toggleTodo(todo.id)"
                    class="w-5 h-5 text-blue-500"
                />
                <span
                    x-text="todo.text"
                    :class="{ 'line-through text-gray-400': todo.completed }"
                    class="flex-1"
                ></span>
                <button
                    @click="removeTodo(todo.id)"
                    class="text-red-500 hover:text-red-700"
                >
                    Delete
                </button>
            </li>
        </template>
    </ul>

    <div x-show="todos.length === 0" class="text-center text-gray-400 py-8">
        No todos yet. Add one above!
    </div>
</div>
'''
        todo_path = project_path / "templates/components/todo.html"
        todo_path.write_text(todo_content)
        components['templates/components/todo.html'] = todo_path

        # Data fetch component (HTMX example)
        fetch_content = '''<!-- Data Fetch Component - Demonstrates HTMX for API communication -->
<div class="bg-white rounded-lg shadow-md p-6 max-w-2xl">
    <h3 class="text-xl font-semibold mb-4">Data Fetcher</h3>

    <button
        hx-get="/api/data"
        hx-trigger="click"
        hx-target="#data-container"
        hx-swap="innerHTML"
        class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded mb-4"
    >
        Load Data
    </button>

    <div
        id="data-container"
        class="p-4 bg-gray-50 rounded min-h-[100px]"
    >
        Click the button to load data from the server.
    </div>
</div>

<!-- Example response template (server would return this) -->
{% raw %}
<!--
<div class="space-y-2">
    <div class="p-3 bg-white rounded border">
        <strong>Item 1:</strong> Data loaded from server
    </div>
    <div class="p-3 bg-white rounded border">
        <strong>Item 2:</strong> HTMX handles the communication
    </div>
    <div class="p-3 bg-white rounded border">
        <strong>Item 3:</strong> Server returns HTML fragments
    </div>
</div>
-->
{% endraw %}
'''
        fetch_path = project_path / "templates/components/data_fetch.html"
        fetch_path.write_text(fetch_content)
        components['templates/components/data_fetch.html'] = fetch_path

        # Example index page
        index_content = '''{% extends "layouts/base.html" %}

{% block title %}zen-temple Examples{% endblock %}

{% block content %}
<div class="space-y-8">
    <header class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">zen-temple</h1>
        <p class="text-lg text-gray-600">Zero-build, zero-magic frontend components</p>
    </header>

    <section class="space-y-6">
        <h2 class="text-2xl font-semibold text-gray-700">Example Components</h2>

        <div class="grid md:grid-cols-2 gap-6">
            <div>
                {% include "components/counter.html" %}
            </div>

            <div>
                {% include "components/data_fetch.html" %}
            </div>
        </div>

        <div>
            {% include "components/todo.html" %}
        </div>
    </section>

    <footer class="text-center text-gray-500 mt-12 pt-8 border-t">
        <p>Built with HTMX, Alpine.js, Jinja2, and Tailwind CSS</p>
        <p class="text-sm mt-2">No build step • No hidden magic • Template-centered</p>
    </footer>
</div>
{% endblock %}
'''
        index_path = project_path / "templates/index.html"
        index_path.write_text(index_content)
        components['templates/index.html'] = index_path

        return components

    def _create_server_files(self, project_path: Path, project_name: str) -> dict[str, Path]:
        """Create basic Flask server files."""
        files = {}

        # Main app file
        app_content = f'''"""
Main application entry point for {project_name}.
"""

from flask import Flask, render_template, jsonify
from pathlib import Path

app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/api/data')
def get_data():
    """
    Example API endpoint that returns HTML fragments for HTMX.

    Following zen-temple philosophy:
    - Server returns HTML fragments (not JSON for UI updates)
    - HTMX handles the communication
    - No JavaScript needed for this interaction
    """
    # In production, this would fetch real data
    items = [
        {{'id': 1, 'title': 'Item 1', 'description': 'Data loaded from server'}},
        {{'id': 2, 'title': 'Item 2', 'description': 'HTMX handles the communication'}},
        {{'id': 3, 'title': 'Item 3', 'description': 'Server returns HTML fragments'}},
    ]

    # Return HTML fragment directly
    html = '<div class="space-y-2">'
    for item in items:
        html += '<div class="p-3 bg-white rounded border">'
        html += '<strong>' + item['title'] + ':</strong> ' + item['description']
        html += '</div>'
    html += '</div>'

    return html


@app.route('/api/json-example')
def get_json_example():
    """
    Example of returning JSON for Alpine.js to consume.

    Use this pattern when you need Alpine.js to handle the data
    rather than replacing HTML directly.
    """
    return jsonify({{
        'status': 'success',
        'data': [
            {{'id': 1, 'name': 'Example 1'}},
            {{'id': 2, 'name': 'Example 2'}},
        ]
    }})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''

        app_path = project_path / "app/main.py"
        app_path.write_text(app_content)
        files['app/main.py'] = app_path

        # .env file
        env_content = '''# Flask configuration
FLASK_APP=app/main.py
FLASK_ENV=development
FLASK_DEBUG=1
'''
        env_path = project_path / ".env"
        env_path.write_text(env_content)
        files['.env'] = env_path

        # requirements file
        requirements_content = '''flask>=3.0.0
python-dotenv>=1.0.0
jinja2>=3.1.0
'''
        req_path = project_path / "requirements.txt"
        req_path.write_text(requirements_content)
        files['requirements.txt'] = req_path

        return files

    def _create_readme(self, project_path: Path, project_name: str, include_server: bool) -> Path:
        """Create project README."""
        server_section = ""
        if include_server:
            server_section = """
## Running the Development Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python app/main.py
```

Then open http://localhost:5000 in your browser.
"""

        readme_content = f'''# {project_name}

A zen-temple project - zero-build, zero-magic frontend components.

## Philosophy

This project follows the zen-temple philosophy:

- **No build step required**: Edit templates and see changes immediately
- **No hidden abstractions**: What you see is what you get
- **Template-centered design**: Templates are the source of truth
- **Logic in Alpine.js**: State management in x-data functions
- **Server returns JSON/HTML**: Clean separation of concerns
- **HTMX for communication**: Simple, declarative API calls

## Project Structure

```
{project_name}/
├── templates/
│   ├── layouts/
│   │   └── base.html          # Base layout with CDN imports
│   ├── components/
│   │   ├── counter.html       # Example: Alpine.js reactivity
│   │   ├── todo.html          # Example: State management
│   │   └── data_fetch.html    # Example: HTMX communication
│   └── index.html             # Main page
├── static/
│   ├── css/                   # Custom styles (if needed)
│   └── js/                    # Custom Alpine.js stores (if needed)
{"├── app/" if include_server else ""}
{"│   └── main.py               # Flask application" if include_server else ""}
└── zen-temple.yaml            # Project configuration
```
{server_section}
## Technology Stack

- **HTMX**: For AJAX, WebSockets, and Server-Sent Events
- **Alpine.js**: For reactive and declarative JavaScript
- **Jinja2**: For template rendering
- **Tailwind CSS**: For styling (via CDN)

## Creating Components

Components are simple HTML files with Alpine.js for interactivity:

```html
<div x-data="{{ count: 0 }}">
    <button @click="count++">Increment</button>
    <span x-text="count"></span>
</div>
```

## HTMX Integration

Use HTMX for server communication:

```html
<button
    hx-get="/api/data"
    hx-target="#result"
    hx-swap="innerHTML"
>
    Load Data
</button>
<div id="result"></div>
```

## Learn More

- [HTMX Documentation](https://htmx.org/)
- [Alpine.js Documentation](https://alpinejs.dev/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
'''
        readme_path = project_path / "README.md"
        readme_path.write_text(readme_content)
        return readme_path

    def _get_component_template(self, component_name: str, component_type: str) -> str:
        """Get template content for a component type."""
        templates = {
            'basic': '''<!-- {name} Component -->
<div
    x-data="{{
        // Component state goes here
        message: 'Hello from {name}!'
    }}"
    class="bg-white rounded-lg shadow-md p-6"
>
    <h3 class="text-xl font-semibold mb-4">{name}</h3>
    <p x-text="message"></p>
</div>
''',
            'form': '''<!-- {name} Form Component -->
<div
    x-data="{{
        formData: {{
            // Form fields
        }},
        submit() {{
            // Handle form submission
            console.log('Form submitted:', this.formData);
        }}
    }}"
    class="bg-white rounded-lg shadow-md p-6"
>
    <h3 class="text-xl font-semibold mb-4">{name}</h3>

    <form @submit.prevent="submit()" class="space-y-4">
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
                Field Name
            </label>
            <input
                type="text"
                x-model="formData.field"
                class="w-full px-4 py-2 border border-gray-300 rounded
                       focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
        </div>

        <button
            type="submit"
            class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded"
        >
            Submit
        </button>
    </form>
</div>
''',
            'list': '''<!-- {name} List Component -->
<div
    x-data="{{
        items: [],
        loadItems() {{
            // Load items from API
            fetch('/api/{name}')
                .then(r => r.json())
                .then(data => this.items = data);
        }}
    }}"
    x-init="loadItems()"
    class="bg-white rounded-lg shadow-md p-6"
>
    <h3 class="text-xl font-semibold mb-4">{name}</h3>

    <ul class="space-y-2">
        <template x-for="item in items" :key="item.id">
            <li class="p-3 bg-gray-50 rounded">
                <span x-text="item.name"></span>
            </li>
        </template>
    </ul>

    <div x-show="items.length === 0" class="text-center text-gray-400 py-8">
        No items found.
    </div>
</div>
''',
            'card': '''<!-- {name} Card Component -->
<div class="bg-white rounded-lg shadow-md overflow-hidden">
    <div class="p-6">
        <h3 class="text-xl font-semibold mb-2">{name}</h3>
        <p class="text-gray-600 mb-4">
            Card description goes here.
        </p>

        <button class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
            Action
        </button>
    </div>
</div>
'''
        }

        template = templates.get(component_type, templates['basic'])
        return template.format(name=component_name)
