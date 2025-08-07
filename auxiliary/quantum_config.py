"""
# Houdinis Framework - Multi-Platform Quantum Configuration Module for Houdinis
# Author: Mauro Risonho de Paula Assumpção aka firebitsbr
# License: MIT

Supports configuration and management of:
- IBM Quantum Experience
- NVIDIA cuQuantum & CUDA-Q
- Amazon Braket
- Microsoft Azure Quantum
- Google Quantum AI (Cirq)
- Other quantum computing platforms

"""

import os
import sys
from typing import Dict, Any, Optional, List
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from quantum.backend import quantum_backend
    BACKEND_AVAILABLE = True
except ImportError:
    BACKEND_AVAILABLE = False

from core.modules import BaseModule


class QuantumConfigModule(BaseModule):
    """
    Enhanced quantum configuration module supporting multiple backends.
    """
    
    def __init__(self):
        super().__init__()
        self.info = {
            'name': 'quantum_config',
            'description': 'Multi-platform quantum backend configuration',
            'author': 'Mauro Risonho de Paula Assumpção aka firebitsbr',
            'version': '2.0.0',
            'category': 'auxiliary'
        }
        
        self.options = {
            'ACTION': {
                'value': 'list',
                'required': True,
                'description': 'Action to perform',
                'choices': [
                    'setup', 'setup_ibm', 'setup_nvidia', 'setup_cuda_q',
                    'setup_braket', 'setup_azure', 'setup_google',
                    'list', 'list_all', 'list_ibm', 'list_nvidia', 
                    'list_braket', 'list_azure', 'list_google',
                    'test', 'monitor', 'benchmark', 'auto_select',
                    'status', 'initialize_all'
                ]
            },
            'IBM_TOKEN': {
                'value': '',
                'required': False,
                'description': 'IBM Quantum Experience API token'
            },
            'BACKEND': {
                'value': '',
                'required': False,
                'description': 'Specific backend to test/use'
            },
            'CUDA_VISIBLE_DEVICES': {
                'value': '0',
                'required': False,
                'description': 'CUDA GPU devices for NVIDIA backends'
            },
            'CUQUANTUM_BACKEND': {
                'value': 'cuquantum_statevec',
                'required': False,
                'description': 'cuQuantum backend type',
                'choices': ['cuquantum_statevec', 'cuquantum_tensornet']
            },
            'CUDA_Q_BACKEND': {
                'value': 'cuda_q_simulator',
                'required': False,
                'description': 'CUDA-Q backend type',
                'choices': ['cuda_q_simulator', 'cuda_q_mqpu']
            },
            'GPU_COUNT': {
                'value': '1',
                'required': False,
                'description': 'Number of GPUs for multi-GPU backends'
            },
            'AWS_PROFILE': {
                'value': 'default',
                'required': False,
                'description': 'AWS profile for Braket'
            },
            'AWS_REGION': {
                'value': 'us-east-1',
                'required': False,
                'description': 'AWS region for Braket'
            },
            'AZURE_SUBSCRIPTION_ID': {
                'value': '',
                'required': False,
                'description': 'Azure subscription ID'
            },
            'AZURE_RESOURCE_GROUP': {
                'value': 'quantum-rg',
                'required': False,
                'description': 'Azure resource group'
            },
            'AZURE_WORKSPACE': {
                'value': 'houdini-workspace',
                'required': False,
                'description': 'Azure Quantum workspace name'
            },
            'CIRCUIT_QUBITS': {
                'value': '4',
                'required': False,
                'description': 'Number of qubits for test circuit'
            },
            'USE_CASE': {
                'value': 'development',
                'required': False,
                'description': 'Use case for auto-selection',
                'choices': ['development', 'validation', 'performance', 'production']
            },
            'BUDGET': {
                'value': '100',
                'required': False,
                'description': 'Budget in USD for cloud backends'
            },
            'PRIORITY': {
                'value': 'speed',
                'required': False,
                'description': 'Optimization priority',
                'choices': ['speed', 'cost', 'accuracy', 'availability']
            }
        }
    
    def run(self) -> Dict[str, Any]:
        """Execute the quantum configuration action."""
        if not BACKEND_AVAILABLE:
            return {
                'success': False,
                'error': 'Quantum backend not available. Check quantum/backend.py'
            }
        
        action = self.options['ACTION']['value'].lower()
        
        # Setup actions
        if action == 'setup' or action == 'setup_ibm':
            return self._setup_ibm()
        elif action == 'setup_nvidia':
            return self._setup_nvidia()
        elif action == 'setup_cuda_q':
            return self._setup_cuda_q()
        elif action == 'setup_braket':
            return self._setup_braket()
        elif action == 'setup_azure':
            return self._setup_azure()
        elif action == 'setup_google':
            return self._setup_google()
        elif action == 'initialize_all':
            return self._initialize_all_backends()
        
        # List actions
        elif action == 'list' or action == 'list_all':
            return self._list_all_backends()
        elif action == 'list_ibm':
            return self._list_backend('ibm')
        elif action == 'list_nvidia':
            return self._list_backend('nvidia')
        elif action == 'list_braket':
            return self._list_backend('braket')
        elif action == 'list_azure':
            return self._list_backend('azure')
        elif action == 'list_google':
            return self._list_backend('google')
        
        # Other actions
        elif action == 'test':
            return self._test_backend()
        elif action == 'monitor':
            return self._monitor_backends()
        elif action == 'benchmark':
            return self._benchmark_backends()
        elif action == 'auto_select':
            return self._auto_select_backend()
        elif action == 'status':
            return self._get_status()
        
        else:
            return {
                'success': False,
                'error': f'Unknown action: {action}'
            }
    
    def _setup_ibm(self) -> Dict[str, Any]:
        """Setup IBM Quantum backend."""
        token = self.options['IBM_TOKEN']['value']
        
        if not token:
            return {
                'success': False,
                'error': 'IBM_TOKEN required. Get it from https://quantum-computing.ibm.com/'
            }
        
        try:
            result = quantum_backend.initialize_backend('ibm', token=token)
            
            if result['success']:
                self.print_success("IBM Quantum configured successfully!")
                self.print_info(f"Available backends: {result.get('backends', [])}")
            else:
                self.print_error(f"IBM Quantum setup failed: {result.get('error', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"IBM Quantum setup error: {str(e)}"
            }
    
    def _setup_nvidia(self) -> Dict[str, Any]:
        """Setup NVIDIA cuQuantum backend."""
        try:
            # Set CUDA devices
            cuda_devices = self.options['CUDA_VISIBLE_DEVICES']['value']
            os.environ['CUDA_VISIBLE_DEVICES'] = cuda_devices
            
            result = quantum_backend.initialize_backend('nvidia')
            
            if result['success']:
                self.print_success("NVIDIA cuQuantum configured successfully!")
                self.print_info(f"GPU count: {result.get('gpu_count', 0)}")
                self.print_info(f"Available backends: {result.get('backends', [])}")
            else:
                self.print_error(f"NVIDIA setup failed: {result.get('error', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"NVIDIA cuQuantum setup error: {str(e)}"
            }
    
    def _setup_cuda_q(self) -> Dict[str, Any]:
        """Setup CUDA-Q backend."""
        try:
            gpu_count = int(self.options['GPU_COUNT']['value'])
            backend_type = self.options['CUDA_Q_BACKEND']['value']
            
            result = quantum_backend.initialize_backend('nvidia', 
                                                      backend_type=backend_type,
                                                      gpu_count=gpu_count)
            
            if result['success']:
                self.print_success("CUDA-Q configured successfully!")
                self.print_info(f"Backend type: {backend_type}")
                self.print_info(f"GPU count: {gpu_count}")
            else:
                self.print_error(f"CUDA-Q setup failed: {result.get('error', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"CUDA-Q setup error: {str(e)}"
            }
    
    def _setup_braket(self) -> Dict[str, Any]:
        """Setup Amazon Braket backend."""
        try:
            aws_profile = self.options['AWS_PROFILE']['value']
            aws_region = self.options['AWS_REGION']['value']
            
            result = quantum_backend.initialize_backend('braket',
                                                      aws_profile=aws_profile,
                                                      aws_region=aws_region)
            
            if result['success']:
                self.print_success("Amazon Braket configured successfully!")
                self.print_info(f"AWS Profile: {aws_profile}")
                self.print_info(f"AWS Region: {aws_region}")
                self.print_info(f"Available backends: {result.get('backends', [])}")
            else:
                self.print_error(f"Braket setup failed: {result.get('error', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Amazon Braket setup error: {str(e)}"
            }
    
    def _setup_azure(self) -> Dict[str, Any]:
        """Setup Azure Quantum backend."""
        try:
            subscription_id = self.options['AZURE_SUBSCRIPTION_ID']['value']
            resource_group = self.options['AZURE_RESOURCE_GROUP']['value']
            workspace = self.options['AZURE_WORKSPACE']['value']
            
            if not subscription_id:
                return {
                    'success': False,
                    'error': 'AZURE_SUBSCRIPTION_ID required'
                }
            
            result = quantum_backend.initialize_backend('azure',
                                                      subscription_id=subscription_id,
                                                      resource_group=resource_group,
                                                      workspace=workspace)
            
            if result['success']:
                self.print_success("Azure Quantum configured successfully!")
                self.print_info(f"Subscription: {subscription_id}")
                self.print_info(f"Resource Group: {resource_group}")
                self.print_info(f"Workspace: {workspace}")
            else:
                self.print_error(f"Azure setup failed: {result.get('error', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Azure Quantum setup error: {str(e)}"
            }
    
    def _setup_google(self) -> Dict[str, Any]:
        """Setup Google Quantum AI backend."""
        try:
            result = quantum_backend.initialize_backend('google')
            
            if result['success']:
                self.print_success("Google Quantum AI configured successfully!")
                self.print_info(f"Available backends: {result.get('backends', [])}")
            else:
                self.print_error(f"Google setup failed: {result.get('error', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Google Quantum AI setup error: {str(e)}"
            }
    
    def _initialize_all_backends(self) -> Dict[str, Any]:
        """Initialize all available backends."""
        try:
            result = quantum_backend.initialize_all_backends()
            
            self.print_info(f"Total backends: {result['total_backends']}")
            self.print_info(f"Active backends: {result['active_backends']}")
            
            for backend_name, backend_result in result['results'].items():
                if backend_result.get('success', False):
                    self.print_success(f"[PASS] {backend_name}: OK")
                else:
                    self.print_error(f"[FAIL] {backend_name}: {backend_result.get('error', 'Failed')}")
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Backend initialization error: {str(e)}"
            }
    
    def _list_all_backends(self) -> Dict[str, Any]:
        """List all available backends."""
        try:
            devices = quantum_backend.list_all_devices()
            
            if not devices:
                self.print_warning("No quantum devices available. Initialize backends first.")
                return {'success': True, 'devices': {}}
            
            # Group devices by type
            device_types = {}
            for name, info in devices.items():
                device_type = info.get('type', 'unknown')
                if device_type not in device_types:
                    device_types[device_type] = []
                device_types[device_type].append((name, info))
            
            # Display results
            self.print_info(f"Found {len(devices)} quantum devices:")
            self.print_line()
            
            for device_type, device_list in device_types.items():
                self.print_info(f"[{device_type.upper()}]")
                for name, info in device_list:
                    status = "[PASS]" if info.get('operational', False) else "[FAIL]"
                    qubits = info.get('qubits', 0)
                    queue = info.get('pending_jobs', 0)
                    desc = info.get('description', 'No description')
                    
                    self.print_result(f"  {status} {name} ({qubits} qubits, queue: {queue})")
                    self.print_result(f"    {desc}")
                self.print_line()
            
            return {
                'success': True,
                'total_devices': len(devices),
                'devices': devices,
                'device_types': list(device_types.keys())
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error listing backends: {str(e)}"
            }
    
    def _list_backend(self, backend_name: str) -> Dict[str, Any]:
        """List devices for a specific backend."""
        try:
            devices = quantum_backend.list_devices_by_backend(backend_name)
            
            if not devices:
                self.print_warning(f"No devices found for {backend_name} backend.")
                return {'success': True, 'devices': {}}
            
            self.print_info(f"{backend_name.upper()} Backend Devices:")
            self.print_line()
            
            for name, info in devices.items():
                status = "[PASS]" if info.get('operational', False) else "[FAIL]"
                qubits = info.get('qubits', 0)
                queue = info.get('pending_jobs', 0)
                desc = info.get('description', 'No description')
                
                self.print_result(f"{status} {name} ({qubits} qubits, queue: {queue})")
                self.print_result(f"  {desc}")
            
            return {
                'success': True,
                'backend': backend_name,
                'device_count': len(devices),
                'devices': devices
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error listing {backend_name} backend: {str(e)}"
            }
    
    def _test_backend(self) -> Dict[str, Any]:
        """Test a specific backend."""
        backend_name = self.options['BACKEND']['value']
        
        if not backend_name:
            return {
                'success': False,
                'error': 'BACKEND option required for testing'
            }
        
        try:
            circuit_qubits = int(self.options['CIRCUIT_QUBITS']['value'])
            
            # Select the backend
            result = quantum_backend.select_device(backend_name)
            
            if not result['success']:
                return result
            
            self.print_info(f"Testing backend: {backend_name}")
            self.print_info(f"Device info: {result['device_info']}")
            
            # Create and execute test circuit
            from qiskit import QuantumCircuit
            test_circuit = QuantumCircuit(circuit_qubits)
            for i in range(circuit_qubits):
                test_circuit.h(i)
            test_circuit.measure_all()
            
            exec_result = quantum_backend.execute_circuit(test_circuit, backend_name)
            
            if exec_result['success']:
                self.print_success(f"[PASS] Backend {backend_name} test successful!")
            else:
                self.print_error(f"[FAIL] Backend {backend_name} test failed: {exec_result.get('error', 'Unknown error')}")
            
            return exec_result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Backend test error: {str(e)}"
            }
    
    def _monitor_backends(self) -> Dict[str, Any]:
        """Monitor backend status."""
        try:
            status = quantum_backend.get_backend_status()
            
            self.print_info("=== Quantum Backend Status ===")
            self.print_info(f"Total backends: {status['total_backends']}")
            self.print_info(f"Active backends: {status['active_backends']}")
            self.print_info(f"Current backend: {status.get('current_backend', 'None')}")
            self.print_info(f"Current device: {status.get('current_device', 'None')}")
            
            self.print_line()
            self.print_info("Backend Details:")
            
            for name, details in status['backend_details'].items():
                connection_status = "[PASS] Connected" if details['connected'] else "[FAIL] Disconnected"
                device_count = details['device_count']
                
                self.print_result(f"  {details['name']}: {connection_status} ({device_count} devices)")
            
            return {
                'success': True,
                'status': status
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Error monitoring backends: {str(e)}"
            }
    
    def _benchmark_backends(self) -> Dict[str, Any]:
        """Benchmark available backends."""
        try:
            circuit_qubits = int(self.options['CIRCUIT_QUBITS']['value'])
            
            self.print_info(f"Benchmarking backends with {circuit_qubits}-qubit circuit...")
            
            results = quantum_backend.benchmark_devices(circuit_qubits)
            
            if not results:
                self.print_warning("No suitable devices found for benchmarking.")
                return {'success': True, 'results': {}}
            
            # Sort by execution time
            sorted_results = sorted(results.items(), 
                                  key=lambda x: x[1].get('execution_time', float('inf')))
            
            self.print_info("=== Benchmark Results ===")
            self.print_line()
            
            for device_name, result in sorted_results:
                if result.get('success', False):
                    exec_time = result.get('execution_time', 0)
                    device_type = result.get('type', 'unknown')
                    qubits = result.get('qubits', 0)
                    
                    self.print_result(f"[PASS] {device_name}: {exec_time:.3f}s ({device_type}, {qubits} qubits)")
                else:
                    error = result.get('error', 'Unknown error')
                    self.print_error(f"[FAIL] {device_name}: {error}")
            
            return {
                'success': True,
                'benchmark_results': results,
                'fastest_device': sorted_results[0][0] if sorted_results else None
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Benchmark error: {str(e)}"
            }
    
    def _auto_select_backend(self) -> Dict[str, Any]:
        """Automatically select the best backend."""
        try:
            circuit_qubits = int(self.options['CIRCUIT_QUBITS']['value'])
            use_case = self.options['USE_CASE']['value']
            
            result = quantum_backend.auto_select_best_device(circuit_qubits, use_case)
            
            if result['success']:
                self.print_success(f"Auto-selected device: {result['device']}")
                self.print_info(f"Backend: {result['backend']}")
                self.print_info(f"Device info: {result['device_info']}")
            else:
                self.print_error(f"Auto-selection failed: {result.get('error', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Auto-selection error: {str(e)}"
            }
    
    def _get_status(self) -> Dict[str, Any]:
        """Get overall quantum system status."""
        try:
            status = quantum_backend.get_backend_status()
            devices = quantum_backend.list_all_devices()
            
            # Count operational devices
            operational_count = sum(1 for info in devices.values() if info.get('operational', False))
            total_qubits = sum(info.get('qubits', 0) for info in devices.values() if info.get('operational', False))
            
            self.print_info("=== Houdinis Quantum System Status ===")
            self.print_info(f"Active backends: {status['active_backends']}/{status['total_backends']}")
            self.print_info(f"Operational devices: {operational_count}/{len(devices)}")
            self.print_info(f"Total available qubits: {total_qubits}")
            self.print_info(f"Current selection: {status.get('current_device', 'None')}")
            
            return {
                'success': True,
                'active_backends': status['active_backends'],
                'total_backends': status['total_backends'],
                'operational_devices': operational_count,
                'total_devices': len(devices),
                'total_qubits': total_qubits,
                'current_device': status.get('current_device')
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Status error: {str(e)}"
            }


# Module instance for the framework
module = QuantumConfigModule()
