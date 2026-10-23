# Contributing to LifeLine Navigator 🚨

We welcome contributions to LifeLine Navigator! This document provides guidelines for contributing to the project.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Pull Requests](#submitting-pull-requests)
- [Reporting Issues](#reporting-issues)

## 🤝 Code of Conduct

This project follows a standard Code of Conduct. Please be respectful and inclusive in all interactions.

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Git
- pip

### Fork and Clone
1. Fork the repository on GitHub
2. Clone your fork locally:
```bash
git clone https://github.com/yourusername/lifeline-navigator.git
cd lifeline-navigator
```

### Setup Development Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If exists

# Install pre-commit hooks
pre-commit install
```

## 💻 Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes
- Follow the [Code Style](#code-style) guidelines
- Write clear, descriptive commit messages
- Add tests for new functionality
- Update documentation as needed

### 3. Test Your Changes
```bash
# Run the application
streamlit run app.py

# Run tests (if implemented)
python -m pytest tests/

# Check code style
black src/
flake8 src/
```

### 4. Commit Your Changes
```bash
git add .
git commit -m "feat: add new emergency alert feature"
```

### 5. Push and Create Pull Request
```bash
git push origin feature/your-feature-name
```
Then create a Pull Request on GitHub.

## 🎨 Code Style

### Python Code
- Follow PEP 8 style guidelines
- Use Black code formatter
- Maximum line length: 88 characters
- Use type hints where appropriate
- Use meaningful variable and function names

### File Structure
- Keep files organized in the specified directory structure
- Use `__init__.py` for Python packages
- Follow the existing naming conventions

### Comments and Docstrings
- Use Google-style docstrings for functions and classes
- Write comments explaining complex logic
- Include examples in docstrings when helpful

Example:
```python
def calculate_route(start: Coordinates, end: Coordinates) -> RouteResponse:
    """
    Calculate the safest route between two points avoiding hazards.
    
    Args:
        start: Starting coordinates
        end: Destination coordinates
        
    Returns:
        RouteResponse containing the calculated route or error message
        
    Example:
        >>> start = Coordinates(latitude=31.634, longitude=74.872)
        >>> end = Coordinates(latitude=31.650, longitude=74.890)
        >>> result = calculate_route(start, end)
        >>> print(f"Distance: {result.total_distance_km} km")
    """
    # Implementation...
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_routing.py
```

### Writing Tests
- Write tests for new features and bug fixes
- Use pytest framework
- FollowArrange-Act-Assert pattern
- Mock external dependencies

Example:
```python
def test_routing_avoids_hazards():
    # Arrange
    start = Coordinates(latitude=31.634, longitude=74.872)
    end = Coordinates(latitude=31.650, longitude=74.890)
    hazard = Hazard(id="test_hazard", type="fire", latitude=31.642, 
                   longitude=74.881, radius_m=500, severity="high",
                   reported_at=datetime.now(), reported_by="test")
    
    # Act
    result = calculate_route(start, end)
    
    # Assert
    assert result.success
    assert result.hazard_zones_crossed == 0
```

## 🔄 Submitting Pull Requests

### PR Checklist
- [ ] Code follows the [Code Style](#code-style) guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated if needed
- [ ] PR title follows conventional commits format
- [ ] PR description explains the changes
- [ ] All CI checks pass

### PR Template
```markdown
## Description
Brief description of the changes made.

## Changes Made
- Feature 1
- Feature 2
- Bug fix 1

## Testing
- [ ] Tested locally
- [ ] Added unit tests
- [ ] Verified UI changes

## Related Issues
Closes #123
Related to #456
```

## 🐛 Reporting Issues

### Bug Reports
When reporting bugs, please include:
1. **Steps to Reproduce**
   ```markdown
   1. Go to '...'
   2. Click on '....'
   3. Scroll down to '....'
   4. See error
   ```

2. **Expected Behavior**
   What should happen

3. **Actual Behavior**
   What actually happened

4. **Screenshots** (if applicable)
   Include screenshots to help explain the issue

5. **Environment**
   - OS: [e.g., Ubuntu 20.04]
   - Python version: [e.g., 3.11.0]
   - Streamlit version: [e.g., 1.37.1]
   - Browser: [e.g., Chrome 120.0]

### Feature Requests
For feature requests:
1. Use a clear and descriptive title
2. Describe the feature in detail
3. Explain the use case
4. Include mockups or examples if possible

## 📚 Documentation

### Updating Documentation
- Update README.md for major changes
- Add/update inline docstrings
- Update API documentation in docs/API.md
- Add deployment guides in docs/DEPLOYMENT.md

### Documentation Style
- Use clear, concise language
- Include examples where helpful
- Keep documentation up to date with code changes

## 🏆 Recognition

Contributors will be recognized in:
- Contributors list in README
- Commit history
- Release notes for significant contributions

## 📞 Support

For questions about contributing:
- Check existing issues and discussions
- Start a discussion for general questions
- Contact maintainers for urgent matters

Thank you for contributing to LifeLine Navigator! 🚨