# Contributing to zen-temple

Thank you for considering contributing to zen-temple! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate in all interactions with the zen-temple community.

## Getting Started

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/mame7743/zen-temple.git
cd zen-temple
```

2. Install dependencies:
```bash
# Using pip
pip install -e ".[dev]"

# Or using uv (recommended)
uv pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

### Project Structure

```
zen-temple/
├── src/zen_temple/          # Main package code
│   ├── __init__.py          # Package initialization
│   ├── cli.py               # CLI commands
│   ├── template_manager.py  # Template rendering
│   ├── validator.py         # Component validation
│   └── scaffold.py          # Project scaffolding
├── tests/                   # Test suite
│   ├── test_cli.py
│   ├── test_template_manager.py
│   ├── test_validator.py
│   └── test_scaffold.py
├── pyproject.toml           # Project metadata and dependencies
└── README.md                # Documentation
```

## How to Contribute

### Reporting Bugs

- Use the GitHub Issues tracker
- Include a clear description of the problem
- Provide steps to reproduce
- Include your environment details (OS, Python version, etc.)
- Add relevant error messages and stack traces

### Suggesting Features

- Open a GitHub Issue with the "enhancement" label
- Describe the feature and its use case
- Explain how it aligns with zen-temple's philosophy
- Provide examples if possible

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add or update tests as needed
5. Ensure all tests pass (`pytest`)
6. Run linting (`ruff check src/`)
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to your branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Guidelines

### Code Style

We use Ruff for linting and formatting:

```bash
# Check code
ruff check src/

# Format code
ruff format src/
```

### Testing

- Write tests for all new features
- Maintain or improve code coverage
- Run tests before submitting PR:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=zen_temple --cov-report=html

# Run specific test file
pytest tests/test_cli.py
```

### Type Hints

- Use type hints for all function signatures
- Run mypy for type checking:

```bash
mypy src/zen_temple
```

### Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions and classes
- Update EXAMPLES.md for new component patterns
- Include examples in your code

### Commit Messages

Follow these guidelines:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Keep first line under 72 characters
- Reference issues and PRs when relevant

Good examples:
```
Add support for custom Alpine.js stores
Fix validation error for nested components
Update documentation for new CLI command
```

## zen-temple Philosophy

When contributing, keep these principles in mind:

1. **No Build Step** - Features should not require compilation or bundling
2. **No Hidden Magic** - Code should be transparent and predictable
3. **Template-Centered** - Templates are the source of truth
4. **Zero Dependencies** (runtime) - Use CDN for frontend dependencies
5. **Backend Developer Friendly** - Simple, straightforward APIs

## Areas for Contribution

### High Priority
- Additional component examples
- Documentation improvements
- Tutorial content
- Bug fixes
- Performance improvements

### Medium Priority
- Additional CLI commands
- Enhanced validation rules
- Support for more component types
- IDE extensions/plugins

### Low Priority
- Advanced features (as long as they align with philosophy)
- Integrations with other frameworks
- Performance optimizations

## Questions?

- Open a GitHub Discussion for general questions
- Use GitHub Issues for bug reports and feature requests
- Check existing issues and discussions first

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to zen-temple! 🎉
