# Quick Start Guide

Get started with zen-temple in 5 minutes!

## Installation

```bash
pip install zen-temple
```

Or with uv (recommended):

```bash
uv pip install zen-temple
```

## Create Your First Project

```bash
zen-temple new my-app
cd my-app
```

This creates:
```
my-app/
├── templates/
│   ├── layouts/
│   │   └── base.html          # Base layout
│   ├── components/
│   │   ├── counter.html       # Example components
│   │   ├── todo.html
│   │   └── data_fetch.html
│   └── index.html             # Main page
├── static/
│   ├── css/
│   └── js/
└── zen-temple.yaml            # Configuration
```

## View Your Components

Open `templates/index.html` in your browser to see the example components.

Or, create a project with a development server:

```bash
zen-temple new my-app --with-server
cd my-app
pip install -r requirements.txt
python app/main.py
```

Then visit http://localhost:5000

## Create a Component

```bash
zen-temple component greeting
```

This creates `templates/components/greeting.html`:

```html
<div 
    x-data="{
        message: 'Hello from greeting!'
    }"
    class="bg-white rounded-lg shadow-md p-6"
>
    <h3 class="text-xl font-semibold mb-4">greeting</h3>
    <p x-text="message"></p>
</div>
```

## Use a Component

In any template:

```html
{% extends "layouts/base.html" %}

{% block content %}
    {% include "components/greeting.html" %}
{% endblock %}
```

## Component Types

Generate different component types:

```bash
# Basic component (default)
zen-temple component my-widget

# Form component
zen-temple component user-form --type form

# List component
zen-temple component user-list --type list

# Card component
zen-temple component info-card --type card
```

## Add Interactivity with Alpine.js

```html
<div x-data="{ count: 0 }">
    <button @click="count++">Increment</button>
    <span x-text="count"></span>
</div>
```

## Add Server Communication with HTMX

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

## Validate Your Components

```bash
zen-temple validate templates/components/my-component.html
```

This checks:
- No inline JavaScript
- No inline event handlers
- Proper HTMX usage
- Proper Alpine.js usage

## List All Components

```bash
zen-temple list-components
```

## Learn the Philosophy

```bash
zen-temple philosophy
```

## Next Steps

1. **Read the examples**: Check out [EXAMPLES.md](EXAMPLES.md)
2. **Explore the docs**: See [README.md](README.md)
3. **Try the API**: Use the Python API in your code

```python
from zen_temple import TemplateManager

manager = TemplateManager()
html = manager.render_component("greeting")
print(html)
```

4. **Join the community**: Star the repo, report issues, contribute!

## Common Patterns

### State Management

```html
<div x-data="{ 
    items: [],
    newItem: '',
    add() {
        this.items.push(this.newItem);
        this.newItem = '';
    }
}">
    <input x-model="newItem" @keyup.enter="add()">
    <button @click="add()">Add</button>
    <ul>
        <template x-for="item in items">
            <li x-text="item"></li>
        </template>
    </ul>
</div>
```

### Form Handling

```html
<form 
    hx-post="/api/submit"
    hx-target="#message"
    hx-swap="innerHTML"
>
    <input name="email" type="email" required>
    <button type="submit">Submit</button>
</form>
<div id="message"></div>
```

### Conditional Rendering

```html
<div x-data="{ show: false }">
    <button @click="show = !show">Toggle</button>
    <div x-show="show">Now you see me!</div>
</div>
```

### Dynamic Classes

```html
<div x-data="{ active: false }">
    <button 
        @click="active = !active"
        :class="{ 'bg-blue-500': active, 'bg-gray-500': !active }"
    >
        Toggle
    </button>
</div>
```

## Tips

1. **Keep it simple**: Don't over-complicate. zen-temple is about simplicity.
2. **No build step**: Edit and refresh. No webpack, no bundlers.
3. **Use CDN**: All dependencies come from CDN. No npm install.
4. **Alpine for state**: Keep all logic in Alpine.js x-data.
5. **HTMX for API**: Let HTMX handle server communication.
6. **Validate early**: Run `zen-temple validate` to catch issues.

## Troubleshooting

### Component not found
- Check template directory in zen-temple.yaml
- Ensure component file exists
- Use `.html` extension

### Validation errors
- Remove inline scripts
- Use Alpine.js directives (@click, x-show, etc.)
- Don't use onclick, onload, etc.

### Server not starting
- Install dependencies: `pip install -r requirements.txt`
- Check port availability (default: 5000)
- Ensure Flask is installed

## Resources

- [Full Documentation](README.md)
- [Examples](EXAMPLES.md)
- [Contributing Guide](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)
- [HTMX Docs](https://htmx.org/)
- [Alpine.js Docs](https://alpinejs.dev/)

## Support

- 🐛 [Report Issues](https://github.com/mame7743/zen-temple/issues)
- 💬 [Discussions](https://github.com/mame7743/zen-temple/discussions)
- ⭐ [Star on GitHub](https://github.com/mame7743/zen-temple)

Happy building! 🎨
