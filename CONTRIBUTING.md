# Contributing to PocketCache

We love your input! We want to make contributing to PocketCache as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Development Setup

1. Clone your fork of the repository:
```bash
git clone https://github.com/YOUR_USERNAME/pocket-cache.git
cd pocket-cache
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev,test,docs]"
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

## Code Quality Standards

Before submitting your code, make sure it meets our quality standards:

1. Code Formatting:
```bash
black src tests examples
isort src tests examples
```

2. Type Checking:
```bash
mypy src tests examples
```

3. Style Guide:
```bash
flake8 src tests examples
```

4. Tests:
```bash
pytest
pytest --cov=pocket_cache  # Check coverage
```

## Pull Request Process

1. Update the README.md with details of changes to the interface, if applicable.
2. Update the documentation with any new features or changes.
3. The PR will be merged once you have the sign-off of at least one maintainer.

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](LICENSE) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issue tracker](https://github.com/jasur-py/pocket-cache/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/jasur-py/pocket-cache/issues/new).

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## License

By contributing, you agree that your contributions will be licensed under its MIT License. 