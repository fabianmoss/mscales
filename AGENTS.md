# AGENTS.md - Guidelines for Contributing to mscales

`mscales` is a Python package to generate, visualize, and sonify musical scales. It provides tools for pitch-class set theory analysis, scale generation, and musical visualization.

## Build, Lint, and Test Commands

### Installation

```bash
pip install -e ".[dev]"         # Install with dev dependencies
```

### Running Tests

```bash
pytest                               # Run all tests
pytest mscales/tests/test_examples.py      # Run single file
pytest mscales/tests/test_examples.py::test_generate_scales  # Run single test
pytest -v                            # Verbose output
```

### Linting and Formatting

```bash
ruff check mscales/          # Lint code
ruff format mscales/         # Format code
pre-commit run --all-files   # Run all hooks
```

### Building

```bash
pip install build            # Install build tools
python -m build              # Build package
```

## Code Style Guidelines

### General

- Python 3.11+
- **Ruff** for linting and formatting (line length: 88)

### Naming Conventions

- **Classes**: `PascalCase` (e.g., `PitchClass`, `Scales`, `PitchClassSet`)
- **Functions/variables**: `snake_case` (e.g., `all_scales()`, `n_scales`)
- **Constants**: `SCREAMING_SNAKE_CASE`
- **Private**: Leading underscore (e.g., `_private_method()`)

### Type Hints

Use type hints in function signatures:

```python
def transpose(self, n: int) -> "PitchClassSet":
    return PitchClassSet((self.pcs + n) % self.c)
```

### Import Organization

Order: stdlib → third-party → local (separated by blank lines):

```python
import numpy as np
from itertools import combinations
from collections import Counter

import matplotlib.pyplot as plt
import pretty_midi as pm

from .utils import find_ngrams
from .scales import Scales
```

### Docstrings

Use NumPy-style docstrings:

```python
def function_name(param: int, param2: str = "default") -> return_type:
    """
    Short description.

    Parameters
    ----------
    param : int
        Description.
    param2 : str, optional
        Description, by default "default".

    Returns
    -------
    return_type
        Description.
    """
    return result
```

### Error Handling

- **TypeError** for type mismatches:
  ```python
  raise TypeError(f"Can't add type {type(other)} to pitch class {self.p}.")
  ```
- **ValueError** for invalid values
- **assertions** for internal validation

### Code Formatting

- Use f-strings: `f"PitchClass({self.p})"`
- Use trailing commas for multi-line structures
- Use `from collections.abc import Iterable` for abstract base classes

### Class Structure

Include `__init__`, `__repr__`, `__str__` methods. Implement dunder methods (`__add__`, `__sub__`, `__eq__`, etc.):

```python
class PitchClass:
    def __init__(self, p, c: int = 12):
        self.c = c
        self.p = p % self.c

    def __repr__(self):
        return f"PitchClass({self.p})"

    def __str__(self):
        return str(self.p)

    def __add__(self, other):
        # implementation
        pass
```

### File Organization

```
mscales/
├── __init__.py          # Package exports
├── scales.py            # Scales class
├── basic.py             # Core classes
├── concepts.py          # Musical concepts
├── plots.py            # Visualization
├── sound.py            # Audio/sonification
├── utils.py            # Utilities
└── tests/
    ├── test_examples.py
    └── conftest.py
```

### Pre-commit

Uses `.pre-commit-config.yaml` with Ruff. Run `pre-commit install` to set up git hooks.
