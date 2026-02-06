"""Scaffold generator for zen-temple projects."""

from pathlib import Path
from typing import Dict, Optional
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
    ) -> Dict[str, Path]:
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
    
    def _create_example_components(self, project_path: Path) -> Dict[str, Path]:
        """Create example components demonstrating zen-temple philosophy."""
        components = {}
        
        # Counter component (Alpine.js reactive example with class-based state)
        counter_content = '''<!-- Counter Component - Demonstrates Alpine.js class-based state management -->
{%- macro counter(initial_count=0) -%}
<div 
    x-data="new CounterState({{ initial_count }})"
    class="bg-white rounded-lg shadow-md p-6 max-w-md"
>
    <h3 class="text-xl font-semibold mb-4">Counter</h3>
    
    <div class="flex items-center justify-between mb-4">
        <button 
            @click="decrement()"
            class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
        >
            -
        </button>
        
        <span class="text-3xl font-bold" x-text="count"></span>
        
        <button 
            @click="increment()"
            class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded"
        >
            +
        </button>
    </div>
    
    <button 
        @click="reset()"
        class="w-full bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded"
    >
        Reset
    </button>
    
    <div class="mt-4 text-sm text-gray-600">
        <p>Double: <span x-text="double"></span></p>
    </div>
</div>

<script>
// CounterState - Encapsulated component state and logic
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
    
    reset() {
        this.count = 0;
    }
    
    // Computed property using getter
    get double() {
        return this.count * 2;
    }
}
</script>
{%- endmacro -%}
'''
        counter_path = project_path / "templates/components/counter.html"
        counter_path.write_text(counter_content)
        components['templates/components/counter.html'] = counter_path
        
        # Todo list component (HTMX + Alpine.js example with class-based state)
        todo_content = '''<!-- Todo List Component - Demonstrates class-based state management -->
{%- macro todo() -%}
<div 
    x-data="new TodoState()"
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
            class="flex-1 px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
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
    
    <div class="mt-4 text-sm text-gray-600">
        <p>Total: <span x-text="totalCount"></span> | Completed: <span x-text="completedCount"></span></p>
    </div>
</div>

<script>
// TodoState - Encapsulated todo list state and logic
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
    
    // Computed properties using getters
    get totalCount() {
        return this.todos.length;
    }
    
    get completedCount() {
        return this.todos.filter(t => t.completed).length;
    }
}
</script>
{%- endmacro -%}
'''
        todo_path = project_path / "templates/components/todo.html"
        todo_path.write_text(todo_content)
        components['templates/components/todo.html'] = todo_path
        
        # Data fetch component (HTMX example with explicit data flow)
        fetch_content = '''<!-- Data Fetch Component - Demonstrates HTMX with explicit data flow -->
{%- macro data_fetch() -%}
<div 
    x-data="new DataFetchState()"
    @htmx:after-request="sync($event.detail.xhr.response)"
    class="bg-white rounded-lg shadow-md p-6 max-w-2xl"
>
    <h3 class="text-xl font-semibold mb-4">Data Fetcher</h3>
    
    <button 
        hx-get="/api/data"
        hx-trigger="click"
        hx-swap="none"
        class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded mb-4"
    >
        Load Data
    </button>
    
    <div x-show="loading" class="text-center py-4">
        <span class="text-gray-500">Loading...</span>
    </div>
    
    <div 
        x-show="!loading && items.length > 0"
        class="space-y-2"
    >
        <template x-for="item in items" :key="item.id">
            <div class="p-3 bg-gray-50 rounded border">
                <strong x-text="item.title"></strong>: <span x-text="item.description"></span>
            </div>
        </template>
    </div>
    
    <div 
        x-show="!loading && items.length === 0"
        class="p-4 bg-gray-50 rounded min-h-[100px] text-center text-gray-400"
    >
        Click the button to load data from the server.
    </div>
    
    <div class="mt-4 text-sm text-gray-600">
        <p>Items loaded: <span x-text="itemCount"></span></p>
    </div>
</div>

<script>
// DataFetchState - Encapsulated data fetching state and logic
class DataFetchState {
    constructor() {
        this.items = [];
        this.loading = false;
    }
    
    // Explicit data sync method called by HTMX
    sync(jsonData) {
        try {
            const data = typeof jsonData === 'string' ? JSON.parse(jsonData) : jsonData;
            this.items = data.items || data || [];
            this.loading = false;
        } catch (e) {
            console.error('Failed to sync data:', e);
            this.loading = false;
        }
    }
    
    // Computed property using getter
    get itemCount() {
        return this.items.length;
    }
}
</script>
{%- endmacro -%}
'''
        fetch_path = project_path / "templates/components/data_fetch.html"
        fetch_path.write_text(fetch_content)
        components['templates/components/data_fetch.html'] = fetch_path
        
        # Example index page with macro imports
        index_content = '''{% extends "layouts/base.html" %}
{% from "components/counter.html" import counter %}
{% from "components/todo.html" import todo %}
{% from "components/data_fetch.html" import data_fetch %}

{% block title %}zen-temple Examples{% endblock %}

{% block content %}
<div class="space-y-8">
    <header class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-800 mb-2">zen-temple</h1>
        <p class="text-lg text-gray-600">Zero-build, zero-magic frontend components</p>
        <p class="text-sm text-gray-500 mt-2">Using Jinja Macros + Alpine.js Classes + HTMX</p>
    </header>
    
    <section class="space-y-6">
        <h2 class="text-2xl font-semibold text-gray-700">Example Components</h2>
        
        <div class="grid md:grid-cols-2 gap-6">
            <div>
                {{ counter(initial_count=0) }}
            </div>
            
            <div>
                {{ data_fetch() }}
            </div>
        </div>
        
        <div>
            {{ todo() }}
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
    
    def _create_server_files(self, project_path: Path, project_name: str) -> Dict[str, Path]:
        """Create basic Flask server files."""
        files = {}
        
        # Main app file - use f-string for cleaner formatting
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
    Example API endpoint that returns JSON for Alpine.js to consume.
    
    Following zen-temple philosophy:
    - Server returns JSON data
    - HTMX fetches the data
    - Alpine.js handles reactive rendering via class methods
    """
    # In production, this would fetch real data
    data = {{
        'items': [
            {{'id': 1, 'title': 'Item 1', 'description': 'Data loaded from server'}},
            {{'id': 2, 'title': 'Item 2', 'description': 'HTMX handles the communication'}},
            {{'id': 3, 'title': 'Item 3', 'description': 'Alpine.js renders the data'}},
        ]
    }}
    
    return jsonify(data)


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
        # Convert component name to different cases - done before templates
        name_snake = component_name.replace('-', '_')
        name_pascal = ''.join(word.capitalize() for word in component_name.replace('_', '-').split('-'))
        
        templates = {
            'basic': f'''<!-- {component_name} Component -->
{{%- macro {name_snake}(message='Hello from {component_name}!') -%}}
<div 
    x-data="new {name_pascal}State('{{{{{{ message }}}}}}')"
    class="bg-white rounded-lg shadow-md p-6"
>
    <h3 class="text-xl font-semibold mb-4">{component_name}</h3>
    <p x-text="message"></p>
</div>

<script>
// {name_pascal}State - Component state and logic
class {name_pascal}State {{
    constructor(message) {{
        this.message = message;
    }}
}}
</script>
{{%- endmacro -%}}
''',
            'form': f'''<!-- {component_name} Form Component -->
{{%- macro {name_snake}() -%}}
<div 
    x-data="new {name_pascal}State()"
    class="bg-white rounded-lg shadow-md p-6"
>
    <h3 class="text-xl font-semibold mb-4">{component_name}</h3>
    
    <form @submit.prevent="submit()" class="space-y-4">
        <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
                Field Name
            </label>
            <input 
                type="text"
                x-model="formData.field"
                class="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
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

<script>
// {name_pascal}State - Form state and logic
class {name_pascal}State {{
    constructor() {{
        this.formData = {{
            field: ''
        }};
    }}
    
    submit() {{
        // Handle form submission
        console.log('Form submitted:', this.formData);
    }}
}}
</script>
{{%- endmacro -%}}
''',
            'list': f'''<!-- {component_name} List Component -->
{{%- macro {name_snake}() -%}}
<div 
    x-data="new {name_pascal}State()"
    x-init="loadItems()"
    @htmx:after-request="sync($event.detail.xhr.response)"
    class="bg-white rounded-lg shadow-md p-6"
>
    <h3 class="text-xl font-semibold mb-4">{component_name}</h3>
    
    <button
        hx-get="/api/{name_snake}"
        hx-trigger="click"
        hx-swap="none"
        class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded mb-4"
    >
        Load Items
    </button>
    
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
    
    <div class="mt-4 text-sm text-gray-600">
        <p>Total items: <span x-text="itemCount"></span></p>
    </div>
</div>

<script>
// {name_pascal}State - List state and logic
class {name_pascal}State {{
    constructor() {{
        this.items = [];
    }}
    
    loadItems() {{
        // Can also load items via fetch if needed
        fetch('/api/{name_snake}')
            .then(r => r.json())
            .then(data => this.sync(JSON.stringify(data)));
    }}
    
    // Explicit data sync method called by HTMX
    sync(jsonData) {{
        try {{
            const data = typeof jsonData === 'string' ? JSON.parse(jsonData) : jsonData;
            this.items = data.items || data || [];
        }} catch (e) {{
            console.error('Failed to sync data:', e);
        }}
    }}
    
    // Computed property using getter
    get itemCount() {{
        return this.items.length;
    }}
}}
</script>
{{%- endmacro -%}}
''',
            'card': f'''<!-- {component_name} Card Component -->
{{%- macro {name_snake}(title='{component_name}', description='Card description goes here.') -%}}
<div 
    x-data="new {name_pascal}State('{{{{{{ title }}}}}}', '{{{{{{ description }}}}}}')"
    class="bg-white rounded-lg shadow-md overflow-hidden"
>
    <div class="p-6">
        <h3 class="text-xl font-semibold mb-2" x-text="title"></h3>
        <p class="text-gray-600 mb-4" x-text="description"></p>
        
        <button 
            @click="handleAction()"
            class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
        >
            Action
        </button>
    </div>
</div>

<script>
// {name_pascal}State - Card state and logic
class {name_pascal}State {{
    constructor(title, description) {{
        this.title = title;
        this.description = description;
    }}
    
    handleAction() {{
        // Handle button action
        console.log('Action clicked');
    }}
}}
</script>
{{%- endmacro -%}}
'''
        }
        
        return templates.get(component_type, templates['basic'])
