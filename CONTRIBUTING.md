# Contributing to ShadowLib

Thank you for your interest in contributing to ShadowLib! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/shadowlib.git`
3. Create a new branch: `git checkout -b feat/your-feature-name`
4. Make your changes following our coding standards
5. Commit using conventional commits (see below)
6. Push and create a pull request

## 📝 Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/) for automated versioning and changelog generation.

### Commit Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature (triggers minor version bump)
- **fix**: A bug fix (triggers patch version bump)
- **docs**: Documentation only changes
- **style**: Code style changes (formatting, semicolons, etc)
- **refactor**: Code refactoring without feature changes
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **build**: Build system or dependency changes
- **ci**: CI/CD configuration changes
- **chore**: Other changes that don't modify src or test files
- **revert**: Reverts a previous commit

### Breaking Changes

Add `BREAKING CHANGE:` in the footer or `!` after type to trigger a major version bump:

```bash
feat!: redesign inventory API

BREAKING CHANGE: getItems() now returns Item objects instead of IDs
```

### Examples

```bash
# Feature (minor version bump: 0.1.0 -> 0.2.0)
feat(inventory): add getItemsByName method

# Bug fix (patch version bump: 0.1.0 -> 0.1.1)
fix(bank): resolve deposit all items issue

# Documentation (patch version bump)
docs(readme): add installation instructions

# Breaking change (major version bump: 0.1.0 -> 1.0.0)
feat(client)!: redesign connection API

BREAKING CHANGE: connect() is now async and requires await

# With scope
fix(navigation): correct pathfinding edge cases

# Multiple lines
feat(interfaces): add grand exchange module

Implements buy/sell orders, price checking, and item search
functionality for the Grand Exchange interface.

Closes #123
```

## 🎨 Code Style

### Naming Conventions

- **Functions/Methods**: `camelCase` (e.g., `getItems()`, `scanNearby()`)
- **Classes**: `PascalCase` (e.g., `Inventory`, `BankInterface`)
- **Constants**: `UPPER_CASE` (e.g., `MAX_INVENTORY_SIZE`)
- **Private functions**: `_camelCase` or `_snake_case` (e.g., `_getIo()`)

### Pre-commit Hooks

We use pre-commit hooks to ensure code quality:

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run manually
pre-commit run --all-files
```

The hooks will automatically:
- Lint code with ruff
- Format code with ruff-format
- Check naming conventions
- Validate YAML/TOML files
- Fix trailing whitespace

## 🏗️ Project Structure

```
shadowlib/
├── tabs/           # Side panel tabs (inventory, equipment, etc.)
├── interfaces/     # Overlay windows (bank, GE, shop, etc.)
├── world/          # 3D world entities (NPCs, objects, players)
├── navigation/     # Movement and pathfinding
├── interactions/   # Menu and clicking systems
├── utilities/      # Helper functions
├── types/          # Type definitions and models
└── _internal/      # Internal implementation details
```

## 📋 Pull Request Process

1. **Update documentation** if you've changed APIs
2. **Add tests** for new functionality
3. **Follow naming conventions** (enforced by pre-commit)
4. **Use conventional commits** (validated by commitlint)
5. **Keep PRs focused** - one feature/fix per PR
6. **Update CHANGELOG.md** is automatic (semantic-release handles it)

### PR Title Format

PR titles should also follow conventional commits:

```
feat: add support for quest tracking
fix: resolve memory leak in event listener
docs: improve bank interface examples
```

## ✅ Testing

```bash
# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=shadowlib --cov-report=html

# Test specific file
pytest tests/test_inventory.py -v
```

## 🔍 Code Review Checklist

Before submitting, ensure:

- [ ] Code follows naming conventions (camelCase for functions)
- [ ] All tests pass
- [ ] Pre-commit hooks pass
- [ ] Commit messages follow conventional commits
- [ ] Documentation is updated
- [ ] No breaking changes (or clearly marked with `!`)
- [ ] Type hints are included
- [ ] Docstrings use Google style

## 🐛 Reporting Bugs

Use GitHub Issues and include:

1. **Description**: Clear description of the bug
2. **Reproduction**: Steps to reproduce
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **Environment**: Python version, OS, shadowlib version

## 💡 Feature Requests

Open an issue with:

1. **Use case**: Why is this needed?
2. **Proposed solution**: How should it work?
3. **Alternatives**: Other approaches considered
4. **API design**: Suggested function signatures

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Your contributions help make ShadowLib better for everyone!
