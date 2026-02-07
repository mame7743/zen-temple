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

## Calculator Component (電卓)

A full-featured calculator demonstrating the complete zen-temple architecture with Pure Logic Layer, Minimal Bridge, and Zero Legacy principles:

### Features

- ✅ Basic arithmetic operations (+, −, ×, ÷)
- ✅ Decimal number support
- ✅ Calculation history tracking
- ✅ Error handling (division by zero)
- ✅ Chained operations
- ✅ Clear (C) and Clear Entry (CE) functions
- ✅ Pure Python logic for backend testing
- ✅ Zero build step - just edit and reload

### Pure Logic Layer (Python)

The calculator logic is implemented as pure Python with no framework dependencies:

```python
# examples/calculator_logic.py
from zen_temple import PureLogic

class CalculatorLogic(PureLogic):
    """Pure business logic for calculator - no framework dependencies."""
    
    def __init__(self):
        self._display = "0"
        self._current_value = 0.0
        self._previous_value = 0.0
        self._operation = None
        self._new_number = True
        self._history = []
    
    def input_digit(self, digit: str) -> str:
        """Input a digit (0-9)."""
        if self._new_number:
            self._display = digit
            self._new_number = False
        else:
            if self._display == "0":
                self._display = digit
            else:
                self._display += digit
        return self._display
    
    def input_operation(self, operation: str) -> str:
        """Input an operation (+, -, *, /)."""
        if self._operation and not self._new_number:
            self.calculate()
        self._previous_value = float(self._display)
        self._operation = operation
        self._new_number = True
        return self._display
    
    def calculate(self) -> str:
        """Calculate the result of pending operation."""
        if not self._operation:
            return self._display
        
        self._current_value = float(self._display)
        
        if self._operation == "+":
            result = self._previous_value + self._current_value
        elif self._operation == "-":
            result = self._previous_value - self._current_value
        elif self._operation == "*":
            result = self._previous_value * self._current_value
        elif self._operation == "/":
            if self._current_value == 0:
                self._display = "Error"
                self._operation = None
                self._new_number = True
                return self._display
            result = self._previous_value / self._current_value
        
        # Format and store result
        self._display = str(int(result)) if result == int(result) else str(round(result, 8))
        self._history.append(f"{self._previous_value} {self._operation} {self._current_value} = {result}")
        self._operation = None
        self._new_number = True
        
        return self._display
    
    def to_context(self) -> dict:
        """Minimal bridge to templates."""
        return {
            "display": self._display,
            "has_operation": self._operation is not None,
            "operation": self._operation or "",
            "history_count": len(self._history),
        }
```

### Frontend Component (Jinja Macro + Alpine.js)

The calculator UI is defined as a reusable Jinja macro with Alpine.js state management:

```html
<!-- examples/templates/components/calculator.html -->
{%- macro calculator() -%}
<div x-data="new CalculatorState()" class="bg-white rounded-xl shadow-lg p-6">
    <h3 class="text-2xl font-bold mb-4">電卓 (Calculator)</h3>
    
    <!-- Display -->
    <div class="bg-gray-100 rounded-lg p-4 mb-4">
        <div x-text="display" class="text-right text-3xl font-mono"></div>
        <div x-show="operation" x-text="'操作: ' + operation" class="text-sm text-gray-500"></div>
    </div>
    
    <!-- Calculator Buttons (simplified for example) -->
    <div class="grid grid-cols-4 gap-2">
        <button @click="inputDigit('7')" class="btn">7</button>
        <button @click="inputDigit('8')" class="btn">8</button>
        <button @click="inputDigit('9')" class="btn">9</button>
        <button @click="inputOperation('/')" class="btn-op">÷</button>
        <!-- More buttons... -->
        <button @click="calculate()" class="btn-equals">=</button>
    </div>
    
    <!-- History -->
    <div class="mt-4" x-show="history.length > 0">
        <h4 class="text-sm font-semibold">履歴 (History)</h4>
        <template x-for="item in history" :key="item">
            <div x-text="item" class="text-xs text-gray-600"></div>
        </template>
    </div>
</div>

<script>
/**
 * CalculatorState - Encapsulated calculator component logic
 * Follows zen-temple principles: class-based state, encapsulated methods
 */
class CalculatorState {
    constructor() {
        this.display = '0';
        this.currentValue = 0;
        this.previousValue = 0;
        this.operation = '';
        this.newNumber = true;
        this.history = [];
    }
    
    inputDigit(digit) {
        if (this.newNumber) {
            this.display = digit;
            this.newNumber = false;
        } else {
            this.display = this.display === '0' ? digit : this.display + digit;
        }
    }
    
    inputOperation(op) {
        if (this.operation && !this.newNumber) {
            this.calculate();
        }
        this.previousValue = parseFloat(this.display);
        this.operation = op;
        this.newNumber = true;
    }
    
    calculate() {
        if (!this.operation) return;
        
        this.currentValue = parseFloat(this.display);
        let result;
        
        switch (this.operation) {
            case '+': result = this.previousValue + this.currentValue; break;
            case '-': result = this.previousValue - this.currentValue; break;
            case '*': result = this.previousValue * this.currentValue; break;
            case '/': 
                if (this.currentValue === 0) {
                    this.display = 'Error';
                    this.operation = '';
                    this.newNumber = true;
                    return;
                }
                result = this.previousValue / this.currentValue;
                break;
        }
        
        this.display = result === Math.floor(result) ? result.toString() : result.toFixed(8).replace(/\.?0+$/, '');
        this.history.push(`${this.previousValue} ${this.operation} ${this.currentValue} = ${result}`);
        this.operation = '';
        this.newNumber = true;
    }
    
    clear() {
        this.display = '0';
        this.currentValue = 0;
        this.previousValue = 0;
        this.operation = '';
        this.newNumber = true;
    }
}
</script>
{%- endmacro -%}
```

### Usage

```html
{% extends "layouts/base.html" %}
{% from "components/calculator.html" import calculator %}

{% block content %}
    <h1>Calculator Example</h1>
    {{ calculator() }}
{% endblock %}
```

### Running the Example

```bash
# Run the demo script
python examples/calculator_demo.py

# Or use with Flask
python examples/app.py  # See calculator_demo.py for Flask setup
```

### Architecture Highlights

1. **Pure Logic Layer**: `CalculatorLogic` class has no framework dependencies - pure Python that can be tested independently
2. **Minimal Bridge**: The `to_context()` method provides only what the template needs
3. **Zero Legacy**: Clean separation allows logic to be reused in CLI tools, APIs, or other contexts
4. **Class-based State**: `CalculatorState` class encapsulates all frontend logic
5. **No Build Step**: Edit templates or logic and reload - no compilation required

### Testing

The calculator includes comprehensive tests for the pure logic layer:

```bash
pytest tests/test_calculator_logic.py -v
```

This demonstrates how zen-temple's architecture enables easy testing of business logic without UI dependencies.

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
