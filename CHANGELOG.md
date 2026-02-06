# Changelog

All notable changes to zen-temple will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-02-06

### Added

#### Core Library
- **TemplateManager**: Jinja2 template management with component rendering
  - Support for multiple template directories
  - JSON encoding filter for Alpine.js integration
  - Component existence checking
  - Template listing
  
- **ComponentValidator**: Validation system for zen-temple components
  - Detection of inline scripts (anti-pattern)
  - Detection of inline event handlers (anti-pattern)
  - HTMX usage validation
  - Alpine.js usage validation
  - Template structure validation
  
- **ScaffoldGenerator**: Project and component scaffolding
  - Full project generation with examples
  - Individual component generation
  - Multiple component types (basic, form, list, card)
  - Flask server integration (optional)
  - Configuration file generation

#### CLI Commands
- `zen-temple new <project>` - Create new zen-temple projects
  - `--path` - Specify parent directory
  - `--no-examples` - Skip example components
  - `--with-server` - Include Flask development server
  
- `zen-temple component <name>` - Generate component templates
  - `--type` - Choose component type (basic, form, list, card)
  - `--output` - Specify output directory
  
- `zen-temple init` - Initialize zen-temple configuration
  - `--project-name` - Set project name
  - `--template-dir` - Set templates directory
  
- `zen-temple validate <file>` - Validate component templates
  - Checks adherence to zen-temple philosophy
  - Reports errors and warnings
  
- `zen-temple list-components` - List available components
  - `--template-dir` - Specify templates directory
  
- `zen-temple philosophy` - Display zen-temple design philosophy

#### Example Components
- **Counter**: Demonstrates Alpine.js reactive state management
- **Todo List**: Shows CRUD operations with Alpine.js
- **Data Fetcher**: Demonstrates HTMX server communication

#### Templates
- Base HTML layout with CDN imports (HTMX, Alpine.js, Tailwind CSS)
- Component template structures
- Flask server templates
- Project README template

#### Documentation
- Comprehensive README with quick start guide
- Examples documentation (EXAMPLES.md)
- Contributing guidelines (CONTRIBUTING.md)
- API documentation in docstrings
- CLI help text and usage examples

#### Testing
- 34 comprehensive tests covering all modules
- 93% code coverage
- Test fixtures and utilities
- CLI testing with Click's test runner

#### Configuration
- Project configuration via zen-temple.yaml
- CDN version management
- Template directory configuration
- Project metadata

### Design Philosophy
- **No Build Step**: Edit templates and see changes immediately
- **No Hidden Abstractions**: What you write is what runs
- **Template-Centered**: Templates are the source of truth
- **Logic in Alpine.js**: State management in x-data functions
- **Server Returns JSON/HTML**: Clean separation of concerns
- **HTMX for Communication**: Declarative API calls

### Technology Stack
- HTMX 1.9.10 - Server communication
- Alpine.js 3.13.5 - Reactive state management
- Jinja2 3.1+ - Template engine
- Tailwind CSS (CDN) - Styling
- Click 8.1+ - CLI framework
- Pydantic 2.0+ - Data validation

### Dependencies
- Runtime: jinja2, click, pydantic, pyyaml
- Development: pytest, pytest-cov, ruff, mypy
- Optional: flask, python-dotenv (for server)

[0.1.0]: https://github.com/mame7743/zen-temple/releases/tag/v0.1.0
