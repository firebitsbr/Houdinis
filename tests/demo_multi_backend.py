#!/usr/bin/env python3
"""
Houdinis Framework - Houdinis Framework Multi-Backend Demo
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

This demo shows how to use the Houdinis Framework with multiple quantum backends.
It demonstrates:
1. Setting up different quantum backends
2. Running quantum algorithms on multiple platforms
3. Comparing performance across backends
4. Best practices for quantum computing with Houdinis

Usage:
    python demo_multi_backend.py
    
MIT License

Copyright (c) 2025 Mauro Risonho de Paula Assumpção aka firebitsbr
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Houdinis Framework imports
from core.cli import HoudinisConsole
from core.session import Session
from utils.banner import get_banner


def print_section_header(title: str):
    """Print formatted section header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_subsection(title: str):
    """Print formatted subsection header."""
    print(f"\n--- {title} ---")


def demo_basic_usage():
    """Demonstrate basic Houdinis usage."""
    print_section_header("Basic Houdinis Framework Usage")
    
    print("1. Creating a new Houdinis console...")
    console = HoudinisConsole()
    print("   [PASS] Console initialized")
    
    print("2. Available quantum modules:")
    modules = [
        "auxiliary/quantum_config - Multi-platform quantum backend configuration",
        "exploits/rsa_shor - RSA factorization using Shor's algorithm", 
        "exploits/grover_bruteforce - Symmetric key attacks using Grover's",
        "exploits/multi_backend_benchmark - Performance comparison across backends",
        "scanners/quantum_vuln_scanner - Network quantum vulnerability scanner"
    ]
    
    for module in modules:
        print(f"    -  {module}")
    
    print("\n3. Framework capabilities:")
    capabilities = [
        "[PASS] Multi-platform quantum backend support",
        "[PASS] Real quantum hardware integration",
        "[PASS] GPU-accelerated simulation",
        "[PASS] Cryptographic vulnerability assessment",
        "[PASS] Performance benchmarking tools"
    ]
    
    for capability in capabilities:
        print(f"   {capability}")


def demo_quantum_backends():
    """Demonstrate quantum backend configuration."""
    print_section_header("Quantum Backend Configuration")
    
    print("Houdinis supports multiple quantum computing backends:")
    
    backends = {
        "IBM Quantum": {
            "description": "IBM's quantum cloud platform with real quantum hardware",
            "features": ["Real quantum processors", "QASM simulator", "Pulse-level control"],
            "use_cases": ["Research", "Algorithm testing", "Educational purposes"]
        },
        "NVIDIA cuQuantum": {
            "description": "GPU-accelerated quantum circuit simulation",
            "features": ["CUDA acceleration", "State vector simulation", "Tensor network"],
            "use_cases": ["High-performance simulation", "Large circuit simulation"]
        },
        "Amazon Braket": {
            "description": "AWS quantum computing service",
            "features": ["Multiple hardware providers", "Managed simulation", "Hybrid algorithms"],
            "use_cases": ["Cloud-based quantum computing", "Vendor-agnostic development"]
        },
        "Azure Quantum": {
            "description": "Microsoft's quantum cloud platform",
            "features": ["Q# integration", "Multiple hardware partners", "Quantum chemistry"],
            "use_cases": ["Enterprise quantum applications", "Quantum optimization"]
        },
        "Google Cirq": {
            "description": "Google's quantum computing framework",
            "features": ["NISQ algorithms", "Quantum supremacy research", "Optimization"],
            "use_cases": ["Google quantum hardware", "Research algorithms"]
        }
    }
    
    for backend, info in backends.items():
        print_subsection(backend)
        print(f"Description: {info['description']}")
        print("Features:")
        for feature in info['features']:
            print(f"   -  {feature}")
        print("Use cases:")
        for use_case in info['use_cases']:
            print(f"   -  {use_case}")


def demo_algorithm_comparison():
    """Demonstrate algorithm performance comparison."""
    print_section_header("Algorithm Performance Comparison")
    
    print("Simulating quantum algorithm performance across backends...")
    
    algorithms = ["Shor's Algorithm", "Grover's Algorithm", "QFT", "VQE"]
    backends = ["IBM Quantum", "NVIDIA cuQuantum", "Amazon Braket", "Azure Quantum"]
    
    # Simulate performance data
    performance_data = {
        "Shor's Algorithm": {
            "IBM Quantum": {"time": 45.2, "qubits": 8, "success_rate": 0.85},
            "NVIDIA cuQuantum": {"time": 2.1, "qubits": 8, "success_rate": 0.98},
            "Amazon Braket": {"time": 12.7, "qubits": 8, "success_rate": 0.92},
            "Azure Quantum": {"time": 18.3, "qubits": 8, "success_rate": 0.89}
        },
        "Grover's Algorithm": {
            "IBM Quantum": {"time": 32.1, "qubits": 6, "success_rate": 0.82},
            "NVIDIA cuQuantum": {"time": 1.3, "qubits": 6, "success_rate": 0.99},
            "Amazon Braket": {"time": 8.9, "qubits": 6, "success_rate": 0.94},
            "Azure Quantum": {"time": 14.2, "qubits": 6, "success_rate": 0.91}
        },
        "QFT": {
            "IBM Quantum": {"time": 28.5, "qubits": 5, "success_rate": 0.88},
            "NVIDIA cuQuantum": {"time": 0.8, "qubits": 5, "success_rate": 0.99},
            "Amazon Braket": {"time": 6.2, "qubits": 5, "success_rate": 0.96},
            "Azure Quantum": {"time": 9.7, "qubits": 5, "success_rate": 0.93}
        },
        "VQE": {
            "IBM Quantum": {"time": 156.3, "qubits": 4, "success_rate": 0.75},
            "NVIDIA cuQuantum": {"time": 8.2, "qubits": 4, "success_rate": 0.95},
            "Amazon Braket": {"time": 42.1, "qubits": 4, "success_rate": 0.87},
            "Azure Quantum": {"time": 67.4, "qubits": 4, "success_rate": 0.83}
        }
    }
    
    print("\nPerformance Comparison Table:")
    print("-" * 90)
    print(f"{'Algorithm':<20} {'Backend':<18} {'Time (s)':<10} {'Qubits':<8} {'Success Rate':<12}")
    print("-" * 90)
    
    for algorithm in algorithms:
        for i, backend in enumerate(backends):
            data = performance_data[algorithm][backend]
            alg_name = algorithm if i == 0 else ""
            print(f"{alg_name:<20} {backend:<18} {data['time']:<10.1f} {data['qubits']:<8} {data['success_rate']:<12.2%}")
        print("-" * 90)
    
    # Find best backend for each algorithm
    print("\nBest Backend by Algorithm:")
    for algorithm in algorithms:
        best_backend = min(performance_data[algorithm].items(), 
                          key=lambda x: x[1]['time'])
        print(f"  {algorithm}: {best_backend[0]} ({best_backend[1]['time']:.1f}s)")


def demo_security_scenarios():
    """Demonstrate quantum cryptography attack scenarios."""
    print_section_header("Quantum Cryptography Attack Scenarios")
    
    scenarios = {
        "RSA Key Breaking": {
            "algorithm": "Shor's Algorithm",
            "target": "RSA-2048 encryption keys",
            "impact": "Complete RSA cryptosystem compromise",
            "timeline": "10-20 years (fault-tolerant quantum computers)",
            "mitigation": "Migrate to post-quantum cryptography"
        },
        "Symmetric Key Search": {
            "algorithm": "Grover's Algorithm", 
            "target": "AES-128 symmetric keys",
            "impact": "Effective key length reduced to 64 bits",
            "timeline": "15-25 years (large-scale quantum computers)",
            "mitigation": "Use AES-256 or larger key sizes"
        },
        "Elliptic Curve Cryptography": {
            "algorithm": "Modified Shor's Algorithm",
            "target": "ECDSA, ECDH key exchange",
            "impact": "Complete ECC compromise",
            "timeline": "10-20 years",
            "mitigation": "Transition to lattice-based cryptography"
        },
        "Hash Function Analysis": {
            "algorithm": "Quantum collision search",
            "target": "SHA-256, MD5 hash functions",
            "impact": "Faster collision finding",
            "timeline": "20-30 years",
            "mitigation": "Use SHA-3 or quantum-resistant hashes"
        }
    }
    
    for scenario, details in scenarios.items():
        print_subsection(scenario)
        print(f"Algorithm: {details['algorithm']}")
        print(f"Target: {details['target']}")
        print(f"Impact: {details['impact']}")
        print(f"Timeline: {details['timeline']}")
        print(f"Mitigation: {details['mitigation']}")


def demo_best_practices():
    """Demonstrate best practices for quantum computing with Houdinis."""
    print_section_header("Best Practices for Quantum Computing with Houdinis")
    
    practices = {
        "Backend Selection": [
            "Use simulators for algorithm development and testing",
            "Reserve real quantum hardware for final validation",
            "Choose GPU-accelerated backends for large simulations",
            "Consider cloud costs when using commercial platforms"
        ],
        "Algorithm Design": [
            "Start with small qubit counts and scale gradually",
            "Use variational algorithms for NISQ devices",
            "Implement error mitigation techniques",
            "Design circuits with hardware constraints in mind"
        ],
        "Security Testing": [
            "Test cryptographic implementations against quantum attacks",
            "Evaluate key sizes for post-quantum security",
            "Benchmark attack algorithms on current systems",
            "Plan migration timelines for quantum-resistant cryptography"
        ],
        "Performance Optimization": [
            "Profile circuits before running on expensive hardware",
            "Use circuit optimization and transpilation",
            "Implement noise-aware algorithms for NISQ devices",
            "Cache simulation results for repeated experiments"
        ]
    }
    
    for category, tips in practices.items():
        print_subsection(category)
        for tip in tips:
            print(f"   -  {tip}")


def demo_code_examples():
    """Show code examples for using Houdinis."""
    print_section_header("Code Examples")
    
    print_subsection("Basic Quantum Circuit with Houdinis")
    print("""
# Load Houdinis modules
from core.session import Session
from quantum.backend import quantum_backend

# Create session and configure quantum backend
session = Session()
quantum_backend.setup_backend('ibm_quantum', {
    'token': 'your_ibm_token_here',
    'hub': 'ibm-q',
    'group': 'open',
    'project': 'main'
})

# Load and configure RSA Shor exploit
session.load_module('exploits/rsa_shor')
shor_module = session.get_module('rsa_shor')
shor_module.set_option('TARGET_NUMBER', '15')
shor_module.set_option('BACKEND', 'ibmq_qasm_simulator')

# Run the exploit
result = shor_module.run()
print(f"Factorization result: {result}")
""")
    
    print_subsection("Multi-Backend Benchmark")
    print("""
# Load benchmark module
session.load_module('exploits/multi_backend_benchmark')
benchmark = session.get_module('multi_backend_benchmark')

# Configure benchmark parameters
benchmark.set_option('ALGORITHM', 'grover')
benchmark.set_option('QUBITS', '6')
benchmark.set_option('BACKENDS', 'all')
benchmark.set_option('RUNS', '5')

# Run benchmark across all backends
results = benchmark.run()

# Analyze results
fastest = results['analysis']['fastest_backend']
print(f"Fastest backend: {fastest}")
""")
    
    print_subsection("Network Quantum Vulnerability Scan")
    print("""
# Load quantum network scanner
session.load_module('scanners/quantum_vuln_scanner')
scanner = session.get_module('quantum_vuln_scanner')

# Configure scan parameters
scanner.set_option('TARGET', '192.168.1.0/24')
scanner.set_option('CHECK_TLS', 'true')
scanner.set_option('CHECK_SSH', 'true')
scanner.set_option('QUANTUM_TIMELINE', '15')  # years

# Run vulnerability scan
vuln_results = scanner.run()

# Generate report
print(f"Quantum-vulnerable hosts: {vuln_results['vulnerable_count']}")
""")


def main():
    """Main demo function."""
    print(get_banner())
    print("\nWelcome to the Houdinis Framework Multi-Backend Demo!")
    print("This demonstration showcases the quantum computing capabilities")
    print("of the Houdinis Framework across multiple backends.")
    
    # Auto-continue for demonstration
    print("Starting demonstration automatically...\n")
    
    try:
        # Run all demo sections
        demo_basic_usage()
        time.sleep(1)
        
        demo_quantum_backends()
        time.sleep(1)
        
        demo_algorithm_comparison()
        time.sleep(1)
        
        demo_security_scenarios()
        time.sleep(1)
        
        demo_best_practices()
        time.sleep(1)
        
        demo_code_examples()
        
        print_section_header("Demo Complete")
        print(" Thank you for exploring the Houdinis Framework!")
        print("\nNext steps:")
        print("  1. Install quantum computing dependencies: pip install -r requirements.txt")
        print("  2. Configure your preferred quantum backend")
        print("  3. Start with the multi_backend_benchmark module")
        print("  4. Explore the various quantum cryptography exploits")
        print("  5. Check out the notebooks/ directory for detailed examples")
        
        print("\n Resources:")
        print("  - Documentation: README.md")
        print("  - Backend guide: BACKENDS.md")
        print("  - Example notebooks: notebooks/")
        print("  - Project repository: https://github.com/firebitsbr/houdinisframework")
        
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Demo interrupted by user.")
    except Exception as e:
        print(f"\n[ERROR] Demo error: {e}")


if __name__ == "__main__":
    main()
