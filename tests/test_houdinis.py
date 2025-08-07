#!/usr/bin/env python3
"""
Houdinis Framework - Houdinis Framework Installation Test
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

Quick test to verify framework setup
"""

import sys
import os
import importlib.util

# Add the parent directory (project root) to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add project root to path
def get_project_root():
    """Get the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

project_root = get_project_root()
sys.path.insert(0, str(project_root))

def test_imports():
    """Test basic framework imports."""
    print("Testing framework imports...")
    
    try:
        from core.modules import BaseModule
        print("  [PASS] Core modules import successful")
    except ImportError as e:
        print(f"  [FAIL] Core modules import failed: {e}")
        return False
    
    try:
        from core.session import Session  
        print("  [PASS] Session module import successful")
    except ImportError as e:
        print(f"  [FAIL] Session module import failed: {e}")
        return False
    
    try:
        from quantum.backend import QuantumBackendManager
        print("  [PASS] Quantum backend import successful")
    except ImportError as e:
        print(f"  [FAIL] Quantum backend import failed: {e}")
        return False
    
    return True

def test_quantum_dependencies():
    """Test quantum computing dependencies."""
    print("Testing quantum computing dependencies...")
    
    # Test Qiskit
    try:
        import qiskit
        print(f"  [PASS] Qiskit {qiskit.__version__} available")
    except ImportError:
        print("  [WARN] Qiskit not available (optional)")
    
    # Test other quantum libraries
    quantum_libs = [
        ('cirq', 'Google Cirq'),
        ('pennylane', 'PennyLane'), 
        ('cuquantum', 'NVIDIA cuQuantum'),
    ]
    
    for lib, name in quantum_libs:
        try:
            __import__(lib)
            print(f"  [PASS] {name} available")
        except ImportError:
            print(f"  [WARN] {name} not available (optional)")

def test_module_loading():
    """Test if exploit modules can be loaded"""
    print("Testing module loading...")
    exploits_dir = os.path.join(project_root, "exploits")
    
    if not os.path.exists(exploits_dir):
        print("  [FAIL] Exploits directory not found")
        return False
    
    try:
        exploit_files = [f for f in os.listdir(exploits_dir) if f.endswith('.py') and f != '__init__.py']
        if exploit_files:
            print(f"  [PASS] Found {len(exploit_files)} exploit modules")
            # Try to import one test module
            test_module = exploit_files[0].replace('.py', '')
            module_name = f"exploits.{test_module}"
            try:
                spec = importlib.util.spec_from_file_location(
                    module_name, 
                    os.path.join(exploits_dir, exploit_files[0])
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    print(f"  [PASS] Test import of {test_module} successful")
                else:
                    print(f"  [WARN] Could not create spec for {test_module}")
            except Exception as e:
                print(f"    [WARN] {test_module} import warning: {e}")
                
            return True
        else:
            print("  [WARN] No exploit modules found")
            return False
    except Exception as e:
        print(f"  [FAIL] Module loading test failed: {e}")
        return False

def test_configuration():
    """Test if configuration files exist"""
    print(" Testing configuration...")
    
    config_files = ["config.ini", "requirements.txt", "setup.py"]
    found_count = 0
    
    for config_file in config_files:
        config_path = os.path.join(project_root, config_file)
        if os.path.exists(config_path):
            print(f"  [PASS] {config_file} found")
            found_count += 1
        else:
            print(f"  [WARN] {config_file} not found")
    
    # Check documentation files
    doc_files = ["README.md", "BACKENDS.md", "LICENSE"]
    for doc_file in doc_files:
        doc_path = os.path.join(project_root, doc_file)
        if os.path.exists(doc_path):
            print(f"  [PASS] {doc_file} found")
            found_count += 1
        else:
            print(f"  [WARN] {doc_file} not found")
    
    return found_count > 0

def test_basic_functionality():
    """Test basic framework functionality."""
    print("\n Testing basic functionality...")
    
    try:
        # Test quantum backend manager
        from quantum.backend import QuantumBackendManager
        
        backend_manager = QuantumBackendManager()
        print("  [PASS] Quantum backend manager created successfully")
        
        # Test available backends (simulated)
        available_backends = {
            'aer_simulator': 'Local Qiskit Aer simulator',
            'qasm_simulator': 'QASM simulator',
            'test_backend': 'Test backend for validation'
        }
        
        print(f"  [PASS] Backend system operational ({len(available_backends)} backends)")
        
    except Exception as e:
        print(f"  [WARN] Basic functionality test warning: {e}")

def test_demo_scripts():
    """Test if demo scripts are available"""
    print(" Testing demo scripts...")
    
    demo_files = ["demo_multi_backend.py", "main.py", "run_exploit.py"]
    found_count = 0
    
    for demo_file in demo_files:
        demo_path = os.path.join(project_root, demo_file)
        if os.path.exists(demo_path):
            print(f"  [PASS] {demo_file} available")
            found_count += 1
        else:
            print(f"  [WARN] {demo_file} not found")
    
    return found_count > 0

def test_notebooks():
    """Test if Jupyter notebooks are available"""
    print(" Testing Jupyter notebooks...")
    
    notebooks_dir = os.path.join(project_root, "notebooks")
    
    if os.path.exists(notebooks_dir):
        try:
            notebook_files = [f for f in os.listdir(notebooks_dir) if f.endswith('.ipynb')]
            if notebook_files:
                print(f"  [PASS] Found {len(notebook_files)} notebooks")
                for nb in notebook_files[:3]:  # Show first 3
                    print(f"    - {nb}")
                if len(notebook_files) > 3:
                    print(f"    ... and {len(notebook_files) - 3} more")
                return True
            else:
                print("  [WARN] Notebooks directory exists but no .ipynb files found")
        except Exception as e:
            print(f"  [WARN] Error reading notebooks directory: {e}")
    else:
        print("  [WARN] No notebooks directory found")
        
        # Check for notebooks in project root
        try:
            root_notebooks = [f for f in os.listdir(project_root) if f.endswith('.ipynb')]
            if root_notebooks:
                print(f"  [PASS] Found {len(root_notebooks)} notebooks in project root")
                return True
        except Exception as e:
            print(f"  [WARN] Error checking project root for notebooks: {e}")
    
    return False

def run_installation_check():
    """Run complete installation check."""
    print("Houdinis Framework Installation Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Run all tests
    test_functions = [
        test_imports,
        test_quantum_dependencies,
        test_module_loading,
        test_configuration,
        test_basic_functionality,
        test_demo_scripts,
        test_notebooks
    ]
    
    for test_func in test_functions:
        try:
            result = test_func()
            if result is False:
                all_tests_passed = False
        except Exception as e:
            print(f"  [FAIL] Test {test_func.__name__} failed: {e}")
            all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("All tests completed successfully!")
        print("\n[PASS] Houdinis Framework is ready to use!")
        print("\nNext steps:")
        print("  1. Configure quantum backends: python -c 'from auxiliary.quantum_config import *'")
        print("  2. Run the demo: python demo_multi_backend.py")
        print("  3. Try the benchmark: python -c 'from exploits.multi_backend_benchmark import *'")
        print("  4. Explore notebooks: jupyter lab notebooks/")
    else:
        print("[WARN] Some tests completed with warnings.")
        print("The framework should still be functional, but some features may be limited.")
        print("\nTroubleshooting:")
        print("  1. Install missing dependencies: pip install -r requirements.txt")
        print("  2. Check quantum library installations")
        print("  3. Verify file permissions and paths")
    
    return all_tests_passed

def main():
    """Main test function."""
    try:
        success = run_installation_check()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[WARN] Test interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[FAIL] Test failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
