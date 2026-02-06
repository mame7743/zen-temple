# zen-temple Architecture

## Overview

zen-temple implements a specific architectural pattern that combines Jinja2 macros, Alpine.js class-based state management, and HTMX for explicit data flow. This document describes the core architectural principles and patterns.

## Core Principles

### 1. Jinja Macro Encapsulation

**Principle**: All UI components MUST be defined as Jinja macros, not plain HTML files.

**Why**: Macros provide:
- Parameterized components with explicit interfaces
- Clear component boundaries
- Single-file components (SFC) pattern similar to Svelte
- Encapsulation of HTML + JavaScript together

**Example**:
```html
<!-- templates/components/counter.html -->
{%- macro counter(initial_count=0) -%}
<div x-data="new CounterState({{ initial_count }})">
    <button @click="increment()">+</button>
    <span x-text="count"></span>
</div>

<script>
class CounterState {
    constructor(initialCount = 0) {
        this.count = initialCount;
    }
    
    increment() {
        this.count++;
    }
}
</script>
{%- endmacro -%}
```

**Usage**:
```html
{% from "components/counter.html" import counter %}
{{ counter(initial_count=5) }}
```

### 2. Zero-Magic Class Definition

**Principle**: Alpine.js x-data MUST always instantiate a JavaScript class with `new`.

**Forbidden Patterns**:
- ❌ `x-data="{ count: 0 }"` - Inline object literals
- ❌ `Alpine.store('counter', ...)` - Global stores
- ❌ `Alpine.data('counter', ...)` - Global component registration

**Required Pattern**:
- ✅ `x-data="new CounterState(0)"` - Explicit class instantiation

**Why**:
- Explicit and imperative code (no hidden magic)
- Clear state ownership
- Better debugging and traceability
- IDE support and type checking
- Loose coupling between components

**Example**:
```html
<div x-data="new TodoState()">
    <!-- Component HTML -->
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
}
</script>
```

### 3. HTMX for Explicit Data Flow

**Principle**: HTMX handles data transport (JSON fetching) and triggers. Data is explicitly passed to Alpine.js class methods.

**Pattern**:
1. HTMX fetches JSON from server
2. `@htmx:after-request` event fires
3. Event handler calls explicit sync method on Alpine class
4. Alpine reactively renders the UI

**Forbidden Pattern**:
- ❌ `hx-swap="innerHTML"` - Direct DOM replacement

**Required Pattern**:
- ✅ `hx-swap="none"` + explicit sync method

**Example**:
```html
<div 
    x-data="new DataState()"
    @htmx:after-request="sync($event.detail.xhr.response)"
>
    <button 
        hx-get="/api/data"
        hx-trigger="click"
        hx-swap="none"
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
    
    // Explicit sync method called by HTMX
    sync(jsonData) {
        try {
            const data = typeof jsonData === 'string' ? JSON.parse(jsonData) : jsonData;
            this.items = data.items || data || [];
        } catch (e) {
            console.error('Failed to sync:', e);
        }
    }
}
</script>
```

**Server Side** (Flask example):
```python
@app.route('/api/data')
def get_data():
    # Return JSON, not HTML
    return jsonify({
        'items': [
            {'id': 1, 'name': 'Item 1'},
            {'id': 2, 'name': 'Item 2'}
        ]
    })
```

### 4. Loose Coupling with Computed Properties

**Principle**: Components are independent. Use JavaScript class getters for computed properties to ensure reactivity.

**Pattern**:
```javascript
class TodoState {
    constructor() {
        this.todos = [];
    }
    
    // Computed property using getter
    get totalCount() {
        return this.todos.length;
    }
    
    get completedCount() {
        return this.todos.filter(t => t.completed).length;
    }
}
```

**Usage in Template**:
```html
<p>Total: <span x-text="totalCount"></span></p>
<p>Completed: <span x-text="completedCount"></span></p>
```

**Why**:
- Automatic reactivity with Alpine.js
- No manual recalculation needed
- Clean separation of concerns
- DRY (Don't Repeat Yourself)

## Component Structure

Every component follows this structure:

```html
<!-- Component comment describing purpose -->
{%- macro component_name(param1='default', param2=0) -%}
<div 
    x-data="new ComponentNameState('{{ param1 }}', {{ param2 }})"
    class="..."
>
    <!-- HTML structure with Alpine directives -->
    <button @click="method()">Action</button>
    <span x-text="property"></span>
</div>

<script>
// ComponentNameState - Component logic and state
class ComponentNameState {
    constructor(param1, param2) {
        // Initialize state
        this.property = param1;
        this.count = param2;
    }
    
    // Methods
    method() {
        // Imperative logic
        this.count++;
    }
    
    // Computed properties
    get computedValue() {
        return this.count * 2;
    }
}
</script>
{%- endmacro -%}
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│                    Browser                          │
│                                                     │
│  ┌────────────────────────────────────────────┐   │
│  │  Jinja Template (Server-Rendered)         │   │
│  │                                            │   │
│  │  {% from "counter.html" import counter %}  │   │
│  │  {{ counter(initial_count=5) }}            │   │
│  └────────────────────────────────────────────┘   │
│                     │                              │
│                     ▼                              │
│  ┌────────────────────────────────────────────┐   │
│  │  Component Macro (Rendered HTML + JS)     │   │
│  │                                            │   │
│  │  <div x-data="new CounterState(5)">       │   │
│  │    <button @click="increment()">+</button>│   │
│  │  </div>                                    │   │
│  │                                            │   │
│  │  <script>                                  │   │
│  │    class CounterState { ... }             │   │
│  │  </script>                                 │   │
│  └────────────────────────────────────────────┘   │
│                     │                              │
│                     ▼                              │
│  ┌────────────────────────────────────────────┐   │
│  │  Alpine.js (Reactive State Management)    │   │
│  │                                            │   │
│  │  - Instantiates CounterState class        │   │
│  │  - Binds to DOM                            │   │
│  │  - Handles reactivity                      │   │
│  │  - Updates UI on state changes             │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
│  ┌────────────────────────────────────────────┐   │
│  │  HTMX (Data Transport)                     │   │
│  │                                            │   │
│  │  1. Fetches JSON from server               │   │
│  │  2. Fires @htmx:after-request event        │   │
│  │  3. Passes data to Alpine method           │   │
│  └────────────────────────────────────────────┘   │
│                     │                              │
└─────────────────────┼──────────────────────────────┘
                      │
                      │ HTTP Request
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│                    Server                           │
│                                                     │
│  ┌────────────────────────────────────────────┐   │
│  │  API Endpoint (Flask/FastAPI/Django)       │   │
│  │                                            │   │
│  │  @app.route('/api/data')                   │   │
│  │  def get_data():                           │   │
│  │      return jsonify({'items': [...]})      │   │
│  └────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Best Practices

### DO ✅

1. **Use Jinja macros for all components**
   ```html
   {%- macro button(text='Click me') -%}
   <button>{{ text }}</button>
   {%- endmacro -%}
   ```

2. **Instantiate classes in x-data**
   ```html
   <div x-data="new ButtonState()">
   ```

3. **Use explicit sync methods for HTMX data**
   ```javascript
   sync(jsonData) {
       this.items = JSON.parse(jsonData).items;
   }
   ```

4. **Use getters for computed properties**
   ```javascript
   get total() {
       return this.items.reduce((sum, i) => sum + i.price, 0);
   }
   ```

5. **Keep components independent**
   - No cross-component dependencies
   - Each component has its own state class
   - Pass data through macro parameters

### DON'T ❌

1. **Use inline x-data objects**
   ```html
   <!-- BAD -->
   <div x-data="{ count: 0 }">
   ```

2. **Use Alpine.store or Alpine.data**
   ```javascript
   // BAD
   Alpine.store('counter', { count: 0 })
   ```

3. **Use hx-swap="innerHTML"**
   ```html
   <!-- BAD -->
   <button hx-get="/api/data" hx-swap="innerHTML">
   ```

4. **Mix concerns between components**
   ```javascript
   // BAD - accessing other component's state
   window.otherComponent.doSomething()
   ```

5. **Return HTML from API endpoints**
   ```python
   # BAD
   return '<div>HTML content</div>'
   
   # GOOD
   return jsonify({'data': 'value'})
   ```

## Component Examples

See [EXAMPLES.md](EXAMPLES.md) for complete working examples of:
- Counter with computed properties
- Todo list with CRUD operations
- Data fetching with HTMX
- Form validation
- Modal dialogs
- Accordions
- Search with filtering
- Tab navigation

## Testing

Components should be tested for:
1. Correct macro structure
2. Class instantiation in x-data
3. HTMX event handlers
4. Computed properties
5. State mutations

See the test suite in `tests/` for examples.

## Migration Guide

If you have existing zen-temple components using the old pattern, migrate them as follows:

### Old Pattern
```html
<div x-data="{ count: 0 }">
    <button @click="count++">+</button>
</div>
```

### New Pattern
```html
{%- macro counter(initial_count=0) -%}
<div x-data="new CounterState({{ initial_count }})">
    <button @click="increment()">+</button>
</div>

<script>
class CounterState {
    constructor(initialCount = 0) {
        this.count = initialCount;
    }
    
    increment() {
        this.count++;
    }
}
</script>
{%- endmacro -%}
```

## References

- [Jinja2 Macros Documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/#macros)
- [Alpine.js Documentation](https://alpinejs.dev/)
- [HTMX Events Reference](https://htmx.org/reference/#events)
- [JavaScript Getters](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/get)
