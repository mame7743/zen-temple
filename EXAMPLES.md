# Examples

This directory contains example projects and code snippets demonstrating zen-temple usage.

## Architecture Overview

zen-temple uses a specific architectural pattern:

1. **Jinja Macros** - Components are defined as macros, not plain HTML
2. **JavaScript Classes** - State is managed in ES6 classes
3. **Explicit Data Flow** - HTMX fetches JSON, Alpine.js renders via class methods
4. **Computed Properties** - Use JavaScript getters for reactive computed values

## Quick Start Example

The simplest zen-temple component as a Jinja macro:

```html
<!-- components/greeting.html -->
{%- macro greeting(name='World') -%}
<div x-data="new GreetingState('{{ name }}')">
    <input x-model="name" placeholder="Enter your name" />
    <p>Hello, <span x-text="name"></span>!</p>
</div>

<script>
class GreetingState {
    constructor(name) {
        this.name = name;
    }
}
</script>
{%- endmacro -%}
```

Usage:
```html
{% from "components/greeting.html" import greeting %}
{{ greeting(name='Alice') }}
```

## Counter Component

A classic example showing class-based reactive state:

```html
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
    
    // Computed property using getter
    get double() {
        return this.count * 2;
    }
}
</script>
{%- endmacro -%}
```

## Todo List with CRUD Operations

Demonstrates class-based state management and computed properties:

```html
{%- macro todo() -%}
<div x-data="new TodoState()">
    <!-- Add todo form -->
    <input 
        x-model="newTodo" 
        @keyup.enter="addTodo()" 
        placeholder="Add a todo..."
    />
    <button @click="addTodo()">Add</button>
    
    <!-- Todo list -->
    <ul>
        <template x-for="todo in todos" :key="todo.id">
            <li>
                <input 
                    type="checkbox" 
                    :checked="todo.completed" 
                    @change="toggleTodo(todo.id)"
                />
                <span :class="{ 'line-through': todo.completed }" x-text="todo.text"></span>
                <button @click="removeTodo(todo.id)">Delete</button>
            </li>
        </template>
    </ul>
    
    <!-- Stats using computed properties -->
    <p>Total: <span x-text="totalCount"></span></p>
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
```

## HTMX Data Loading with Explicit Flow

Server communication with explicit data synchronization:

```html
{%- macro data_list() -%}
<div 
    x-data="new DataState()"
    @htmx:after-request="sync($event.detail.xhr.response)"
>
    <button 
        hx-get="/api/users"
        hx-trigger="click"
        hx-swap="none"
    >
        Load Users
    </button>
    
    <div x-show="loading">Loading...</div>
    
    <ul x-show="!loading">
        <template x-for="user in users" :key="user.id">
            <li x-text="user.name"></li>
        </template>
    </ul>
    
    <p>Total users: <span x-text="userCount"></span></p>
</div>

<script>
class DataState {
    constructor() {
        this.users = [];
        this.loading = false;
    }
    
    // Explicit sync method called by HTMX
    sync(jsonData) {
        try {
            const data = JSON.parse(jsonData);
            this.users = data.users || data || [];
            this.loading = false;
        } catch (e) {
            console.error('Failed to sync:', e);
            this.loading = false;
        }
    }
    
    get userCount() {
        return this.users.length;
    }
}
</script>
{%- endmacro -%}
```

Server endpoint (Flask):
```python
@app.route('/api/users')
def get_users():
    return jsonify({
        'users': [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'},
            {'id': 3, 'name': 'Charlie'}
        ]
    })
```

## Form with Validation

Class-based form state with validation:

```html
{%- macro login_form() -%}
<div x-data="new FormState()">
    <form @submit.prevent="submit()" class="space-y-4">
        <div>
            <input 
                x-model="formData.email" 
                type="email" 
                placeholder="Email" 
            />
            <p x-show="errors.email" x-text="errors.email" class="error"></p>
        </div>
        
        <div>
            <input 
                x-model="formData.password" 
                type="password" 
                placeholder="Password" 
            />
            <p x-show="errors.password" x-text="errors.password" class="error"></p>
        </div>
        
        <button type="submit" :disabled="!isValid">Sign In</button>
    </form>
</div>

<script>
class FormState {
    constructor() {
        this.formData = {
            email: '',
            password: ''
        };
        this.errors = {};
    }
    
    validate() {
        this.errors = {};
        
        if (!this.formData.email.includes('@')) {
            this.errors.email = 'Invalid email';
        }
        
        if (this.formData.password.length < 8) {
            this.errors.password = 'Password too short';
        }
        
        return Object.keys(this.errors).length === 0;
    }
    
    submit() {
        if (this.validate()) {
            console.log('Valid!', this.formData);
            // Submit to server
        }
    }
    
    get isValid() {
        return this.formData.email.includes('@') && 
               this.formData.password.length >= 8;
    }
}
</script>
{%- endmacro -%}
```

## Modal Dialog

Encapsulated modal with class state:

```html
{%- macro modal() -%}
<div x-data="new ModalState()">
    <button @click="open()">Open Modal</button>
    
    <div 
        x-show="isOpen"
        @click.away="close()"
        class="modal"
    >
        <div class="modal-content">
            <h2>Modal Title</h2>
            <p>Modal content goes here...</p>
            <button @click="close()">Close</button>
        </div>
    </div>
</div>

<script>
class ModalState {
    constructor() {
        this.isOpen = false;
    }
    
    open() {
        this.isOpen = true;
    }
    
    close() {
        this.isOpen = false;
    }
}
</script>
{%- endmacro -%}
```

## Accordion

Component with active state management:

```html
{%- macro accordion() -%}
<div x-data="new AccordionState()">
    <div>
        <button @click="toggle(1)">
            Item 1
        </button>
        <div x-show="activeItem === 1">Content 1</div>
    </div>
    
    <div>
        <button @click="toggle(2)">
            Item 2
        </button>
        <div x-show="activeItem === 2">Content 2</div>
    </div>
</div>

<script>
class AccordionState {
    constructor() {
        this.activeItem = null;
    }
    
    toggle(item) {
        this.activeItem = this.activeItem === item ? null : item;
    }
}
</script>
{%- endmacro -%}
```

## Data Fetching with Alpine.js

```html
<div x-data="{
    users: [],
    loading: false,
    async loadUsers() {
        this.loading = true;
        try {
            const response = await fetch('/api/users');
            this.users = await response.json();
        } catch (error) {
            console.error('Failed to load users', error);
        } finally {
            this.loading = false;
        }
    }
}" x-init="loadUsers()">
    <div x-show="loading">Loading...</div>
    
    <ul x-show="!loading">
        <template x-for="user in users" :key="user.id">
            <li x-text="user.name"></li>
        </template>
    </ul>
</div>
```

## Live Search

Component with computed filtering:

```html
{%- macro search() -%}
<div x-data="new SearchState()">
    <input x-model="query" placeholder="Search..." />
    
    <ul>
        <template x-for="item in filteredItems" :key="item">
            <li x-text="item"></li>
        </template>
    </ul>
</div>

<script>
class SearchState {
    constructor() {
        this.query = '';
        this.items = ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'];
    }
    
    // Computed property using getter
    get filteredItems() {
        return this.items.filter(item => 
            item.toLowerCase().includes(this.query.toLowerCase())
        );
    }
}
</script>
{%- endmacro -%}
```

## Tabs

Tab navigation with class state:

```html
{%- macro tabs() -%}
<div x-data="new TabState()">
    <div class="tab-buttons">
        <button @click="setActive('tab1')">Tab 1</button>
        <button @click="setActive('tab2')">Tab 2</button>
        <button @click="setActive('tab3')">Tab 3</button>
    </div>
    
    <div x-show="activeTab === 'tab1'">Content 1</div>
    <div x-show="activeTab === 'tab2'">Content 2</div>
    <div x-show="activeTab === 'tab3'">Content 3</div>
</div>

<script>
class TabState {
    constructor() {
        this.activeTab = 'tab1';
    }
    
    setActive(tab) {
        this.activeTab = tab;
    }
}
</script>
{%- endmacro -%}
```

## More Examples

For complete working examples, create a new project:

```bash
zen-temple new my-app
cd my-app
```

The generated project includes:
- Counter component
- Todo list component
- Data fetching with HTMX
- Base layout with CDN imports
- Flask server (with --with-server flag)
