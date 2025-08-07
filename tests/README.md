# Test Suite - Houdinis Framework

This directory contains all test suites for the Houdinis framework.

## Test Structure

```
tests/
├── __init__.py                # Python module for tests
├── test_houdinis.py          # Primary test suite
└── README.md                 # This file
```

## Executing Tests

### Local Tests (Native)
```bash
# From project root
python3 tests/test_houdinis.py

# Or using pytest (if installed)
pytest tests/
```

### Docker Tests
```bash
# Using quick access script
./docker.sh test

# Or directly
cd docker/
./docker-manager.sh test
./run-docker.sh --test

# Or with Docker Compose
./docker.sh compose-test
```

## Available Test Suites

### `test_houdinis.py` - Primary Suite
Tests framework installation and basic functionality:

- **Module Imports** - Verifies all modules load correctly
- **Dependencies** - Validates required libraries
- **Core Framework** - Tests primary functionalities
- **Exploits** - Verifies exploitation modules
- **Scanners** - Tests scanning modules
- **Quantum Backends** - Validates quantum connectivity

### Detailed Execution
```bash
# Complete test with verbose output
python3 tests/test_houdinis.py

# Expected output:
Houdinis Framework Installation Test
====================================
[PASS] Core modules imported successfully
[PASS] Quantum computing libraries available
[PASS] Network analysis tools ready
[PASS] Cryptography modules loaded
[PASS] Houdinis Framework is ready to use!
```

## Adding New Tests

### Recommended Structure
```python
#!/usr/bin/env python3
"""
Test module for [component name]
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_[component]():
    """Test [component] functionality"""
    try:
        # Test implementation
        assert condition
        print("[PASS] [Component] test passed")
        return True
    except Exception as e:
        print(f"[FAIL] [Component] test failed: {e}")
        return False

if __name__ == "__main__":
    test_[component]()
```

### Naming Conventions
- **Files**: `test_[module_name].py`
- **Functions**: `test_[functionality]()`
- **Classes**: `Test[Component]`

### Test Categories
- **Unit tests** - Unit tests for individual modules
- **Integration tests** - Integration tests between components
- **System tests** - Complete system testing
- **Performance tests** - Performance and benchmark tests

## Test Environment Configuration

### Minimum Dependencies
```bash
# Install basic dependencies
pip install pytest pytest-cov

# For quantum tests (optional)
pip install qiskit qiskit-aer

# For network tests
pip install scapy python-nmap
```

### Environment Variables
```bash
# Define for tests
export HOUDINIS_TEST_MODE=1
export HOUDINIS_LOG_LEVEL=DEBUG

# For real quantum backend tests (opcional)
export IBM_QUANTUM_TOKEN=your_token_here
export AWS_ACCESS_KEY_ID=your_key_here
```

##  Coverage e Relatórios

### Execute with Coverage
```bash
# Install pytest-cov
pip install pytest-cov

# Execute with coverage
pytest tests/ --cov=. --cov-report=html

# View report
open htmlcov/index.html
```

### CI/CD Integration
```yaml
# Example for GitHub Actions
- name: Run Tests
  run: |
    python3 tests/test_houdinis.py
    
- name: Docker Tests
  run: |
    ./docker.sh build
    ./docker.sh test
```

##  Test Debugging

### Detailed Logs
```bash
# Execute with debug
HOUDINIS_LOG_LEVEL=DEBUG python3 tests/test_houdinis.py

# In Docker
./docker.sh shell
cd /opt/houdinis
HOUDINIS_LOG_LEVEL=DEBUG python3 tests/test_houdinis.py
```

### Isolated Tests
```bash
# Test specific module
python3 -c "
import sys
sys.path.append('.')
from tests.test_houdinis import test_core_imports
test_core_imports()
"
```

##  Test Checklist

Before committing, verify:

- [ ]  All tests pass locally
- [ ]  Tests pass in Docker
- [ ]  New tests for added functionality
- [ ]  Coverage maintained or improved
- [ ]  Test documentation updated

##  Troubleshooting

### Common Issues

1. **ImportError**: Module not found
   ```bash
   # Check PYTHONPATH
   export PYTHONPATH=$PWD:$PYTHONPATH
   ```

2. **Network permissions**: Network tests fail
   ```bash
   # Execute with sudo for network tests
   sudo python3 tests/test_houdinis.py
   ```

3. **Quantum backends**: Connectivity failure
   ```bash
   # Test connectivity
   ping quantum-computing.ibm.com
   ```

4. **Docker tests**: Container fails
   ```bash
   # Debug container
   ./docker.sh shell
   ./docker.sh logs
   ```

##  Referências

- **[Pytest Documentation](https://docs.pytest.org/)**
- **[Coverage.py](https://coverage.readthedocs.io/)**
- **[Qiskit Testing](https://qiskit.org/documentation/contributing_to_qiskit.html#test-structure)**
- **[Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)**

---

 **Keep tests updated** - Tests are the framework quality assurance!
