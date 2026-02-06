# Examples

This directory contains example projects and code snippets demonstrating zen-temple usage.

## Quick Start Example

The simplest zen-temple component:

```html
<!-- components/greeting.html -->
<div x-data="{ name: 'World' }">
    <input x-model="name" placeholder="Enter your name" />
    <p>Hello, <span x-text="name"></span>!</p>
</div>
```

## Counter Component

A classic example showing Alpine.js reactive state:

```html
<div x-data="{ count: 0 }">
    <button @click="count--">-</button>
    <span x-text="count"></span>
    <button @click="count++">+</button>
</div>
```

## Todo List with CRUD Operations

Demonstrates state management and list rendering:

```html
<div x-data="{
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
}">
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
</div>
```

## HTMX Data Loading

Server communication without JavaScript:

```html
<button 
    hx-get="/api/users"
    hx-target="#user-list"
    hx-swap="innerHTML"
>
    Load Users
</button>
<div id="user-list">Click to load users</div>
```

## Form with Validation

```html
<div x-data="{
    formData: {
        email: '',
        password: ''
    },
    errors: {},
    validate() {
        this.errors = {};
        if (!this.formData.email.includes('@')) {
            this.errors.email = 'Invalid email';
        }
        if (this.formData.password.length < 8) {
            this.errors.password = 'Password too short';
        }
        return Object.keys(this.errors).length === 0;
    },
    submit() {
        if (this.validate()) {
            // Submit form
            console.log('Valid!', this.formData);
        }
    }
}">
    <form @submit.prevent="submit()">
        <div>
            <input x-model="formData.email" type="email" placeholder="Email" />
            <p x-show="errors.email" x-text="errors.email" class="error"></p>
        </div>
        
        <div>
            <input x-model="formData.password" type="password" placeholder="Password" />
            <p x-show="errors.password" x-text="errors.password" class="error"></p>
        </div>
        
        <button type="submit">Sign In</button>
    </form>
</div>
```

## Modal Dialog

```html
<div x-data="{ open: false }">
    <button @click="open = true">Open Modal</button>
    
    <div 
        x-show="open"
        @click.away="open = false"
        class="modal"
    >
        <div class="modal-content">
            <h2>Modal Title</h2>
            <p>Modal content goes here...</p>
            <button @click="open = false">Close</button>
        </div>
    </div>
</div>
```

## Accordion

```html
<div x-data="{ activeItem: null }">
    <div>
        <button @click="activeItem = activeItem === 1 ? null : 1">
            Item 1
        </button>
        <div x-show="activeItem === 1">Content 1</div>
    </div>
    
    <div>
        <button @click="activeItem = activeItem === 2 ? null : 2">
            Item 2
        </button>
        <div x-show="activeItem === 2">Content 2</div>
    </div>
</div>
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

```html
<div x-data="{
    query: '',
    items: ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'],
    get filteredItems() {
        return this.items.filter(item => 
            item.toLowerCase().includes(this.query.toLowerCase())
        );
    }
}">
    <input x-model="query" placeholder="Search..." />
    
    <ul>
        <template x-for="item in filteredItems" :key="item">
            <li x-text="item"></li>
        </template>
    </ul>
</div>
```

## Tabs

```html
<div x-data="{ activeTab: 'tab1' }">
    <div class="tab-buttons">
        <button @click="activeTab = 'tab1'">Tab 1</button>
        <button @click="activeTab = 'tab2'">Tab 2</button>
        <button @click="activeTab = 'tab3'">Tab 3</button>
    </div>
    
    <div x-show="activeTab === 'tab1'">Content 1</div>
    <div x-show="activeTab === 'tab2'">Content 2</div>
    <div x-show="activeTab === 'tab3'">Content 3</div>
</div>
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
