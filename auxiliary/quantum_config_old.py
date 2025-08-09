"""
# Houdinis Framework - Quantum Backend Configuration Module for Houdinis
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# License: MIT

"""

import sys
from typing import Dict, Any

sys.path.append('..')
from core.modules import BaseModule

try:
    from quantum.backend import quantum_backend, setup_ibmq_token
    QUANTUM_BACKEND_AVAILABLE = True
except ImportError:
    QUANTUM_BACKEND_AVAILABLE = False


class QuantumConfigModule(BaseModule):
    """
    Module for configuring quantum backends in Houdinis.
    """
    
    def __init__(self):
        super().__init__()
        
        self.info = {
            'name': 'Quantum Backend Configuration',
            'description': 'Configure and test quantum computing backends',
            'author': 'Mauro Risonho de Paula Assumpção aka firebitsbr',
            'version': '1.0',
            'category': 'auxiliary'
        }
        
        self.options.update({
            'ACTION': {
                'description': 'Action to perform (setup, list, test, status)',
                'required': True,
                'default': 'status'
            },
            'BACKEND': {
                'description': 'Backend to test/configure',
                'required': False,
                'default': 'aer_simulator'
            },
            'IBM_TOKEN': {
                'description': 'IBM Quantum API token for setup',
                'required': False,
                'default': ''
            }
        })
    
    def run(self) -> Dict[str, Any]:
        """Execute quantum backend configuration."""
        action = self.options['ACTION']['default'].lower()
        
        if action == 'setup':
            return self._setup_ibmq()
        elif action == 'list':
            return self._list_backends()
        elif action == 'test':
            return self._test_backend()
        elif action == 'status':
            return self._show_status()
        else:
            return {
                'success': False,
                'error': f'Unknown action: {action}. Use: setup, list, test, status'
            }
    
    def _setup_ibmq(self) -> Dict[str, Any]:
        """Setup IBM Quantum connection."""
        if not QUANTUM_BACKEND_AVAILABLE:
            return {
                'success': False,
                'error': 'Quantum backend module not available'
            }
        
        print("=== IBM Quantum Setup ===")
        print()
        print("To use IBM Quantum backends, you need a free account at:")
        print("[LINK] https://quantum-computing.ibm.com/")
        print()
        print("Setup steps:")
        print("1. Create a free IBM Quantum account")
        print("2. Go to your account settings")
        print("3. Copy your API token")
        print("4. Set IBM_TOKEN option or enter when prompted")
        print()
        
        token = self.options['IBM_TOKEN']['default'].strip()
        
        if not token:
            try:
                # Use secure input handling
                import getpass
                token = getpass.getpass("Enter your IBM Quantum API token (input hidden): ").strip()
                
                # Validate token format
                if token and len(token) < 10:
                    print("\n[!] Warning: Token appears too short. Please verify.")
                    return {'success': False, 'error': 'Invalid token format'}
                    
                # Sanitize token input
                import re
                if token and not re.match(r'^[A-Za-z0-9_-]+$', token):
                    print("\n[!] Error: Token contains invalid characters.")
                    return {'success': False, 'error': 'Invalid token characters'}
                    
            except KeyboardInterrupt:
                print("\n[*] Setup cancelled")
                return {'success': False, 'error': 'Setup cancelled'}
            except Exception as e:
                print(f"\n[!] Error during token input: {e}")
                return {'success': False, 'error': 'Token input failed'}
        
        if token:
            result = quantum_backend.initialize_ibmq(token)
            if result['success']:
                print(f"\n Successfully connected to IBM Quantum!")
                print(f" Available backends: {len(result['backends'])}")
                
                # List available backends
                print("\nAvailable IBM Quantum backends:")
                backends = quantum_backend.list_backends(include_simulators=False)
                for name, info in backends.items():
                    status = "[OK]" if info['operational'] else "[CRITICAL]"
                    print(f"  {status} {name} ({info['qubits']} qubits, {info['pending_jobs']} pending)")
                
                return {
                    'success': True,
                    'backends': result['backends'],
                    'message': 'IBM Quantum configured successfully'
                }
            else:
                print(f"\n Connection failed: {result['error']}")
                return result
        else:
            print("\n No token provided. IBM Quantum setup skipped.")
            return {'success': False, 'error': 'No token provided'}
    
    def _list_backends(self) -> Dict[str, Any]:
        """List all available backends."""
        print("=== Available Quantum Backends ===")
        print()
        
        if not QUANTUM_BACKEND_AVAILABLE:
            print(" Quantum backend module not available")
            return {'success': False, 'error': 'Backend module not available'}
        
        # List local simulators
        print("  Local Simulators:")
        print("   aer_simulator (32 qubits)")
        print("   statevector_simulator (20 qubits)")
        print()
        
        # List IBM Q backends if available
        backends = quantum_backend.list_backends()
        ibmq_backends = {k: v for k, v in backends.items() if v.get('type') == 'ibm_quantum'}
        
        if ibmq_backends:
            print("  IBM Quantum Backends:")
            for name, info in ibmq_backends.items():
                status = "[OK]" if info.get('operational', False) else "[CRITICAL]"
                pending = info.get('pending_jobs', 0)
                qubits = info.get('qubits', 0)
                print(f"  {status} {name} ({qubits} qubits, {pending} pending jobs)")
        else:
            print("  IBM Quantum Backends:")
            print("    Not connected. Run 'set ACTION setup' to configure.")
        
        print()
        print("Usage: Set QUANTUM_BACKEND option in exploits to use these backends")
        
        return {
            'success': True,
            'local_backends': 2,
            'ibmq_backends': len(ibmq_backends)
        }
    
    def _test_backend(self) -> Dict[str, Any]:
        """Test a specific backend."""
        backend_name = self.options['BACKEND']['default']
        
        print(f"=== Testing Backend: {backend_name} ===")
        print()
        
        if not QUANTUM_BACKEND_AVAILABLE:
            return {'success': False, 'error': 'Backend module not available'}
        
        # Select backend
        result = quantum_backend.select_backend(backend_name)
        if not result['success']:
            print(f" Backend selection failed: {result['error']}")
            return result
        
        print(f" Backend selected: {backend_name}")
        print(f" Type: {result['type']}")
        print(f"[NUMERIC] Qubits: {result.get('qubits', 'Unknown')}")
        
        # Get backend info
        info = quantum_backend.get_backend_info()
        if info['success']:
            print(f" Description: {info.get('description', 'N/A')}")
            if 'operational' in info:
                status = "[OK] Operational" if info['operational'] else "[CRITICAL] Offline"
                print(f"[LOADING] Status: {status}")
        
        # Test with simple circuit
        try:
            from quantum.simulator import QuantumCircuitBuilder
            
            print("\n Testing with simple quantum circuit...")
            circuit = QuantumCircuitBuilder(2)
            circuit.h(0).cx(0, 1).measure(0, 0).measure(1, 1)
            
            job_result = quantum_backend.execute_circuit(circuit, shots=100, job_name="test_circuit")
            
            if job_result['success']:
                if job_result['status'] == 'completed':
                    print(" Test circuit executed successfully")
                    if 'counts' in job_result:
                        print(f"[STATS] Results: {job_result['counts']}")
                else:
                    print(f"[UPLOAD] Test circuit submitted: {job_result['job_id']}")
                    print(f"[LOADING] Status: {job_result['status']}")
            else:
                print(f" Test circuit failed: {job_result['error']}")
                
        except Exception as e:
            print(f" Circuit test failed: {str(e)}")
        
        return {'success': True, 'backend': backend_name, 'tested': True}
    
    def _show_status(self) -> Dict[str, Any]:
        """Show quantum backend status."""
        print("=== Quantum Backend Status ===")
        print()
        
        if not QUANTUM_BACKEND_AVAILABLE:
            print(" Quantum backend module not available")
            print("   Install with: pip install qiskit")
            return {'success': False, 'error': 'Backend not available'}
        
        # Check IBM Q connection
        if quantum_backend.provider:
            print("  IBM Quantum:  Connected")
            print(f" Available backends: {len(quantum_backend.available_backends)}")
            
            if quantum_backend.current_backend:
                info = quantum_backend.get_backend_info()
                name = info.get('name', 'Unknown')
                qubits = info.get('qubits', 'Unknown')
                print(f"[TARGET] Current backend: {name} ({qubits} qubits)")
            else:
                print("[TARGET] Current backend: None selected")
        else:
            print("  IBM Quantum:  Not connected")
            print("   Run 'set ACTION setup' to configure")
        
        print()
        print("  Local simulators:  Available")
        print("    -  aer_simulator")
        print("    -  statevector_simulator")
        
        # Job history
        if quantum_backend.job_history:
            print(f"\n[SCROLL] Recent jobs: {len(quantum_backend.job_history)}")
            for job in quantum_backend.job_history[-3:]:  # Show last 3
                print(f"    -  {job['job_id']} on {job['backend']} ({job['submitted']})")
        
        return {
            'success': True,
            'ibmq_connected': bool(quantum_backend.provider),
            'current_backend': quantum_backend.current_backend.name() if quantum_backend.current_backend else None,
            'job_count': len(quantum_backend.job_history)
        }


def create_module():
    """Factory function to create the module."""
    return QuantumConfigModule()
