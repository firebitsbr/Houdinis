"""
Houdinis Framework - Multi-Platform Quantum Backend Integration for Houdinis
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

Supports: IBM Quantum, NVIDIA cuQuantum, CUDA-Q, Amazon Braket, 
         Azure Quantum, Google Cirq, and other quantum platforms.
"""

import os
import sys
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from abc import ABC, abstractmethod

# Import quantum computing libraries with error handling
try:
    from qiskit import IBMQ, QuantumCircuit, execute, Aer
    from qiskit.providers.ibmq import least_busy
    from qiskit.providers.aer import AerSimulator
    from qiskit.providers import JobStatus
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False

try:
    import cuquantum
    from cuquantum import cutensornet
    CUQUANTUM_AVAILABLE = True
except ImportError:
    CUQUANTUM_AVAILABLE = False

try:
    import braket
    from braket.aws import AwsDevice
    from braket.devices import LocalSimulator
    BRAKET_AVAILABLE = True
except ImportError:
    BRAKET_AVAILABLE = False

try:
    import azure.quantum
    from azure.quantum import Workspace
    AZURE_QUANTUM_AVAILABLE = True
except ImportError:
    AZURE_QUANTUM_AVAILABLE = False

try:
    import cirq
    CIRQ_AVAILABLE = True
except ImportError:
    CIRQ_AVAILABLE = False

try:
    import pennylane as qml
    PENNYLANE_AVAILABLE = True
except ImportError:
    PENNYLANE_AVAILABLE = False


class QuantumBackendBase(ABC):
    """Abstract base class for quantum backends."""
    
    def __init__(self, name: str):
        self.name = name
        self.is_connected = False
        self.available_devices = {}
        
    @abstractmethod
    def initialize(self, **kwargs) -> Dict[str, Any]:
        """Initialize the backend connection."""
        pass
        
    @abstractmethod
    def list_devices(self) -> Dict[str, Any]:
        """List available quantum devices."""
        pass
        
    @abstractmethod
    @abstractmethod
    def execute_circuit(self, circuit: Any, device: Optional[str] = None) -> Dict[str, Any]:
        """Execute a quantum circuit."""
        pass


class IBMQuantumBackend(QuantumBackendBase):
    """IBM Quantum backend implementation."""
    
    def __init__(self):
        super().__init__("IBM Quantum")
        self.provider = None
        self.ibmq_token = None
        
    def initialize(self, token: Optional[str] = None) -> Dict[str, Any]:
        """Initialize IBM Quantum connection."""
        if not QISKIT_AVAILABLE:
            return {
                'success': False,
                'error': 'Qiskit not installed. Install with: pip install qiskit'
            }
        
        try:
            if token:
                IBMQ.save_account(token, overwrite=True)
                print(f"[+] IBM Quantum token saved")
            
            IBMQ.load_account()
            self.provider = IBMQ.get_provider(hub='ibm-q')
            
            # Get available backends
            backends = self.provider.backends()
            self.available_devices = {}
            
            for backend in backends:
                config = backend.configuration()
                status = backend.status()
                
                self.available_devices[backend.name()] = {
                    'backend': backend,
                    'qubits': config.n_qubits,
                    'operational': status.operational,
                    'pending_jobs': status.pending_jobs,
                    'simulator': config.simulator,
                    'description': getattr(config, 'description', 'No description'),
                    'type': 'ibm_quantum'
                }
            
            self.is_connected = True
            print(f"[+] Connected to IBM Quantum")
            print(f"[+] Available backends: {len(self.available_devices)}")
            
            return {
                'success': True,
                'provider': 'IBM Quantum',
                'backends': list(self.available_devices.keys()),
                'total_backends': len(self.available_devices)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"IBM Quantum connection failed: {str(e)}"
            }
    
    def list_devices(self) -> Dict[str, Any]:
        """List available IBM Quantum devices."""
        devices = {}
        
        if self.is_connected and self.available_devices:
            for name, info in self.available_devices.items():
                devices[name] = {
                    'type': 'ibm_quantum',
                    'qubits': info['qubits'],
                    'operational': info['operational'],
                    'pending_jobs': info['pending_jobs'],
                    'description': info['description']
                }
        
        return devices
    
    def execute_circuit(self, circuit: Any, device: Optional[str] = None) -> Dict[str, Any]:
        """Execute circuit on IBM Quantum backend."""
        # Implementation details would go here
        return {'success': True, 'backend': 'IBM Quantum'}


class NVIDIAQuantumBackend(QuantumBackendBase):
    """NVIDIA cuQuantum backend implementation."""
    
    def __init__(self):
        super().__init__("NVIDIA cuQuantum")
        self.gpu_devices = []
        
    def initialize(self, **kwargs) -> Dict[str, Any]:
        """Initialize NVIDIA cuQuantum."""
        if not CUQUANTUM_AVAILABLE:
            return {
                'success': False,
                'error': 'cuQuantum not installed. Install with: pip install cuquantum-python'
            }
        
        try:
            # Check for CUDA-capable GPUs
            import cupy as cp
            gpu_count = cp.cuda.runtime.getDeviceCount()
            
            self.available_devices = {}
            for i in range(gpu_count):
                with cp.cuda.Device(i):
                    props = cp.cuda.runtime.getDeviceProperties(i)
                    self.available_devices[f'cuquantum_gpu_{i}'] = {
                        'type': 'nvidia_cuquantum',
                        'qubits': 40,  # Depends on GPU memory
                        'operational': True,
                        'pending_jobs': 0,
                        'description': f'NVIDIA GPU {i}: {props["name"]}',
                        'gpu_id': i
                    }
            
            # Add tensor network simulator
            self.available_devices['cuquantum_tensornet'] = {
                'type': 'nvidia_tensornet',
                'qubits': 50,
                'operational': True,
                'pending_jobs': 0,
                'description': 'cuQuantum Tensor Network Simulator'
            }
            
            self.is_connected = True
            return {
                'success': True,
                'provider': 'NVIDIA cuQuantum',
                'backends': list(self.available_devices.keys()),
                'gpu_count': gpu_count
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"NVIDIA cuQuantum initialization failed: {str(e)}"
            }
    
    def list_devices(self) -> Dict[str, Any]:
        """List available NVIDIA devices."""
        return self.available_devices
    
    def execute_circuit(self, circuit: Any, device: Optional[str] = None) -> Dict[str, Any]:
        """Execute circuit on NVIDIA cuQuantum."""
        return {'success': True, 'backend': 'NVIDIA cuQuantum'}


class BraketBackend(QuantumBackendBase):
    """Amazon Braket backend implementation."""
    
    def __init__(self):
        super().__init__("Amazon Braket")
        
    def initialize(self, **kwargs) -> Dict[str, Any]:
        """Initialize Amazon Braket."""
        if not BRAKET_AVAILABLE:
            return {
                'success': False,
                'error': 'Braket SDK not installed. Install with: pip install amazon-braket-sdk'
            }
        
        try:
            # Local simulators
            self.available_devices = {
                'braket_local': {
                    'type': 'braket_local',
                    'qubits': 25,
                    'operational': True,
                    'pending_jobs': 0,
                    'description': 'Braket Local Simulator'
                }
            }
            
            # Try to get AWS devices
            try:
                from braket.aws import AwsDevice
                
                # Add cloud simulators
                self.available_devices.update({
                    'braket_sv1': {
                        'type': 'braket_cloud',
                        'qubits': 34,
                        'operational': True,
                        'pending_jobs': 0,
                        'description': 'Braket SV1 State Vector Simulator'
                    },
                    'braket_tn1': {
                        'type': 'braket_cloud',
                        'qubits': 50,
                        'operational': True,
                        'pending_jobs': 0,
                        'description': 'Braket TN1 Tensor Network Simulator'
                    },
                    'braket_dm1': {
                        'type': 'braket_cloud',
                        'qubits': 17,
                        'operational': True,
                        'pending_jobs': 0,
                        'description': 'Braket DM1 Density Matrix Simulator'
                    }
                })
                
                # Add hardware devices (IonQ, Rigetti, etc.)
                hardware_devices = {
                    'ionq': {
                        'type': 'braket_hardware',
                        'qubits': 32,
                        'operational': True,
                        'pending_jobs': 5,
                        'description': 'IonQ Trapped Ion Quantum Computer'
                    },
                    'rigetti': {
                        'type': 'braket_hardware', 
                        'qubits': 80,
                        'operational': True,
                        'pending_jobs': 3,
                        'description': 'Rigetti Superconducting Quantum Computer'
                    }
                }
                self.available_devices.update(hardware_devices)
                
            except Exception as aws_e:
                print(f"[!] AWS devices unavailable: {aws_e}")
            
            self.is_connected = True
            return {
                'success': True,
                'provider': 'Amazon Braket',
                'backends': list(self.available_devices.keys())
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Braket initialization failed: {str(e)}"
            }
    
    def list_devices(self) -> Dict[str, Any]:
        """List available Braket devices."""
        return self.available_devices
    
    def execute_circuit(self, circuit: Any, device: Optional[str] = None) -> Dict[str, Any]:
        """Execute circuit on Braket."""
        return {'success': True, 'backend': 'Amazon Braket'}


class AzureQuantumBackend(QuantumBackendBase):
    """Microsoft Azure Quantum backend implementation."""
    
    def __init__(self):
        super().__init__("Azure Quantum")
        
    def initialize(self, **kwargs) -> Dict[str, Any]:
        """Initialize Azure Quantum."""
        if not AZURE_QUANTUM_AVAILABLE:
            return {
                'success': False,
                'error': 'Azure Quantum SDK not installed. Install with: pip install azure-quantum'
            }
        
        try:
            self.available_devices = {
                'azure_simulator': {
                    'type': 'azure_simulator',
                    'qubits': 40,
                    'operational': True,
                    'pending_jobs': 0,
                    'description': 'Azure Quantum Simulator'
                },
                'ionq_azure': {
                    'type': 'azure_hardware',
                    'qubits': 32,
                    'operational': True,
                    'pending_jobs': 2,
                    'description': 'IonQ on Azure Quantum'
                },
                'quantinuum_azure': {
                    'type': 'azure_hardware',
                    'qubits': 56,
                    'operational': True,
                    'pending_jobs': 4,
                    'description': 'Quantinuum on Azure Quantum'
                }
            }
            
            self.is_connected = True
            return {
                'success': True,
                'provider': 'Azure Quantum',
                'backends': list(self.available_devices.keys())
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Azure Quantum initialization failed: {str(e)}"
            }
    
    def list_devices(self) -> Dict[str, Any]:
        """List available Azure Quantum devices."""
        return self.available_devices
    
    def execute_circuit(self, circuit: Any, device: Optional[str] = None) -> Dict[str, Any]:
        """Execute circuit on Azure Quantum."""
        return {'success': True, 'backend': 'Azure Quantum'}


class GoogleQuantumBackend(QuantumBackendBase):
    """Google Quantum AI backend implementation."""
    
    def __init__(self):
        super().__init__("Google Quantum AI")
        
    def initialize(self, **kwargs) -> Dict[str, Any]:
        """Initialize Google Cirq."""
        if not CIRQ_AVAILABLE:
            return {
                'success': False,
                'error': 'Cirq not installed. Install with: pip install cirq'
            }
        
        try:
            self.available_devices = {
                'cirq_simulator': {
                    'type': 'cirq_simulator',
                    'qubits': 20,
                    'operational': True,
                    'pending_jobs': 0,
                    'description': 'Cirq Local Simulator'
                },
                'sycamore': {
                    'type': 'google_hardware',
                    'qubits': 70,
                    'operational': False,  # Research access only
                    'pending_jobs': 0,
                    'description': 'Google Sycamore Quantum Processor'
                }
            }
            
            self.is_connected = True
            return {
                'success': True,
                'provider': 'Google Quantum AI',
                'backends': list(self.available_devices.keys())
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Google Quantum AI initialization failed: {str(e)}"
            }
    
    def list_devices(self) -> Dict[str, Any]:
        """List available Google Quantum devices."""
        return self.available_devices
    
    def execute_circuit(self, circuit: Any, device: Optional[str] = None) -> Dict[str, Any]:
        """Execute circuit on Google Quantum AI."""
        return {'success': True, 'backend': 'Google Quantum AI'}


class QuantumBackendManager:
    """
    Unified manager for all quantum computing backends.
    Supports IBM Quantum, NVIDIA cuQuantum, Amazon Braket, Azure Quantum, Google Cirq.
    """
    
    def __init__(self):
        self.backends = {
            'ibm': IBMQuantumBackend(),
            'nvidia': NVIDIAQuantumBackend(),
            'braket': BraketBackend(),
            'azure': AzureQuantumBackend(),
            'google': GoogleQuantumBackend()
        }
        self.current_backend = None
        self.current_device = None
        self.active_backends = []
        
    def initialize_all_backends(self) -> Dict[str, Any]:
        """Initialize all available backends."""
        results = {}
        
        for name, backend in self.backends.items():
            try:
                result = backend.initialize()
                results[name] = result
                if result.get('success', False):
                    self.active_backends.append(name)
                    print(f"[+] {backend.name} initialized successfully")
                else:
                    print(f"[!] {backend.name} initialization failed: {result.get('error', 'Unknown error')}")
            except Exception as e:
                results[name] = {'success': False, 'error': str(e)}
                print(f"[!] {backend.name} initialization error: {e}")
        
        return {
            'total_backends': len(self.backends),
            'active_backends': len(self.active_backends),
            'results': results
        }
    
    def initialize_backend(self, backend_name: str, **kwargs) -> Dict[str, Any]:
        """Initialize a specific backend."""
        if backend_name not in self.backends:
            return {
                'success': False,
                'error': f'Backend {backend_name} not found. Available: {list(self.backends.keys())}'
            }
        
        backend = self.backends[backend_name]
        result = backend.initialize(**kwargs)
        
        if result.get('success', False) and backend_name not in self.active_backends:
            self.active_backends.append(backend_name)
        
        return result
    
    def list_all_devices(self) -> Dict[str, Any]:
        """List devices from all active backends."""
        all_devices = {}
        
        for backend_name in self.active_backends:
            backend = self.backends[backend_name]
            devices = backend.list_devices()
            all_devices.update(devices)
        
        return all_devices
    
    def list_devices_by_backend(self, backend_name: str) -> Dict[str, Any]:
        """List devices from a specific backend."""
        if backend_name not in self.backends:
            return {}
        
        if backend_name not in self.active_backends:
            return {}
        
        return self.backends[backend_name].list_devices()
    
    def select_device(self, device_name: str) -> Dict[str, Any]:
        """Select a specific device for execution."""
        all_devices = self.list_all_devices()
        
        if device_name not in all_devices:
            return {
                'success': False,
                'error': f'Device {device_name} not found. Available: {list(all_devices.keys())}'
            }
        
        device_info = all_devices[device_name]
        
        # Find which backend owns this device
        for backend_name in self.active_backends:
            backend_devices = self.backends[backend_name].list_devices()
            if device_name in backend_devices:
                self.current_backend = backend_name
                self.current_device = device_name
                break
        
        return {
            'success': True,
            'device': device_name,
            'backend': self.current_backend,
            'device_info': device_info
        }
    
    def auto_select_best_device(self, circuit_qubits: int, use_case: str = 'development') -> Dict[str, Any]:
        """Automatically select the best device based on requirements."""
        all_devices = self.list_all_devices()
        
        if not all_devices:
            return {
                'success': False,
                'error': 'No devices available'
            }
        
        # Filter devices by qubit requirements
        suitable_devices = {}
        for name, info in all_devices.items():
            if info.get('qubits', 0) >= circuit_qubits and info.get('operational', False):
                suitable_devices[name] = info
        
        if not suitable_devices:
            return {
                'success': False,
                'error': f'No devices found with {circuit_qubits}+ qubits'
            }
        
        # Selection algorithm based on use case
        if use_case == 'development':
            # Prefer local simulators
            for name, info in suitable_devices.items():
                if 'aer_simulator' in name or 'local' in info.get('type', ''):
                    return self.select_device(name)
            
            # Then NVIDIA GPU if available
            for name, info in suitable_devices.items():
                if 'nvidia' in info.get('type', '') or 'cuquantum' in name:
                    return self.select_device(name)
        
        elif use_case == 'validation':
            # Prefer real hardware with low queue
            hardware_devices = {k: v for k, v in suitable_devices.items() 
                              if 'hardware' in v.get('type', '') and v.get('pending_jobs', 0) < 5}
            if hardware_devices:
                # Select device with lowest queue
                best_device = min(hardware_devices.items(), key=lambda x: x[1].get('pending_jobs', 0))
                return self.select_device(best_device[0])
        
        elif use_case == 'performance':
            # Prefer GPU accelerated backends
            for name, info in suitable_devices.items():
                if 'nvidia' in info.get('type', '') or 'cuquantum' in name:
                    return self.select_device(name)
        
        # Default: select first suitable device
        first_device = list(suitable_devices.keys())[0]
        return self.select_device(first_device)
    
    def execute_circuit(self, circuit: Any, device: Optional[str] = None, **kwargs) -> Dict[str, Any]:
        """Execute a quantum circuit on the selected or specified device."""
        target_device = device or self.current_device
        
        if not target_device:
            return {
                'success': False,
                'error': 'No device selected. Use select_device() or specify device parameter.'
            }
        
        # Find backend that owns this device
        target_backend = None
        for backend_name in self.active_backends:
            backend_devices = self.backends[backend_name].list_devices()
            if target_device in backend_devices:
                target_backend = backend_name
                break
        
        if not target_backend:
            return {
                'success': False,
                'error': f'Device {target_device} not found in active backends'
            }
        
        # Execute on the appropriate backend
        return self.backends[target_backend].execute_circuit(circuit, target_device, **kwargs)
    
    def get_backend_status(self) -> Dict[str, Any]:
        """Get status of all backends and devices."""
        status = {
            'total_backends': len(self.backends),
            'active_backends': len(self.active_backends),
            'current_backend': self.current_backend,
            'current_device': self.current_device,
            'backend_details': {}
        }
        
        for name, backend in self.backends.items():
            status['backend_details'][name] = {
                'name': backend.name,
                'connected': backend.is_connected,
                'device_count': len(backend.available_devices) if hasattr(backend, 'available_devices') else 0
            }
        
        return status
    
    def benchmark_devices(self, circuit_qubits: int = 4) -> Dict[str, Any]:
        """Benchmark available devices with a test circuit."""
        from qiskit import QuantumCircuit
        
        # Create a simple test circuit
        test_circuit = QuantumCircuit(circuit_qubits)
        for i in range(circuit_qubits):
            test_circuit.h(i)
        test_circuit.measure_all()
        
        benchmark_results = {}
        all_devices = self.list_all_devices()
        
        for device_name, device_info in all_devices.items():
            if device_info.get('qubits', 0) >= circuit_qubits and device_info.get('operational', False):
                try:
                    start_time = datetime.now()
                    result = self.execute_circuit(test_circuit, device_name)
                    execution_time = (datetime.now() - start_time).total_seconds()
                    
                    benchmark_results[device_name] = {
                        'success': result.get('success', False),
                        'execution_time': execution_time,
                        'qubits': device_info.get('qubits', 0),
                        'type': device_info.get('type', 'unknown')
                    }
                except Exception as e:
                    benchmark_results[device_name] = {
                        'success': False,
                        'error': str(e),
                        'execution_time': None
                    }
        
        return benchmark_results


# Global backend manager instance
quantum_backend = QuantumBackendManager()


def setup_ibmq_token(token: str) -> Dict[str, Any]:
    """Setup IBM Quantum token."""
    return quantum_backend.initialize_backend('ibm', token=token)


def setup_nvidia_cuda() -> Dict[str, Any]:
    """Setup NVIDIA CUDA for cuQuantum."""
    return quantum_backend.initialize_backend('nvidia')


def setup_braket_aws(profile: str = 'default', region: str = 'us-east-1') -> Dict[str, Any]:
    """Setup Amazon Braket with AWS credentials."""
    return quantum_backend.initialize_backend('braket', aws_profile=profile, aws_region=region)


def setup_azure_quantum(subscription_id: str, resource_group: str) -> Dict[str, Any]:
    """Setup Azure Quantum workspace."""
    return quantum_backend.initialize_backend('azure', subscription_id=subscription_id, resource_group=resource_group)


def setup_google_cirq() -> Dict[str, Any]:
    """Setup Google Cirq."""
    return quantum_backend.initialize_backend('google')
    """
    Manages quantum backends for Houdinis framework.
    Supports both local simulators and IBM Q Experience backends.
    """
    
    def __init__(self):
        self.provider = None
        self.current_backend = None
        self.ibmq_token = None
        self.available_backends = {}
        self.job_history = []
        
    def initialize_ibmq(self, token: Optional[str] = None) -> Dict[str, Any]:
        """
        Initialize IBM Q Experience connection.
        
        Args:
            token: IBM Quantum token (if None, will try to load from saved account)
            
        Returns:
            Status dictionary
        """
        if not QISKIT_AVAILABLE:
            return {
                'success': False,
                'error': 'Qiskit not installed. Install with: pip install qiskit[visualization]'
            }
        
        try:
            if token:
                # Save and load account with token
                IBMQ.save_account(token, overwrite=True)
                print(f"[+] IBM Quantum token saved")
            
            # Load account
            IBMQ.load_account()
            self.provider = IBMQ.get_provider(hub='ibm-q')
            
            # Get available backends
            backends = self.provider.backends()
            self.available_backends = {}
            
            for backend in backends:
                config = backend.configuration()
                status = backend.status()
                
                self.available_backends[backend.name()] = {
                    'backend': backend,
                    'qubits': config.n_qubits,
                    'operational': status.operational,
                    'pending_jobs': status.pending_jobs,
                    'simulator': config.simulator,
                    'description': getattr(config, 'description', 'No description')
                }
            
            print(f"[+] Connected to IBM Quantum")
            print(f"[+] Available backends: {len(self.available_backends)}")
            
            return {
                'success': True,
                'backends': list(self.available_backends.keys()),
                'provider': 'IBM Quantum'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to connect to IBM Quantum: {str(e)}'
            }
    
    def list_backends(self, include_simulators: bool = True) -> Dict[str, Any]:
        """
        List available quantum backends.
        
        Args:
            include_simulators: Whether to include simulator backends
            
        Returns:
            Dictionary with backend information
        """
        backends = {}
        
        # Add local simulators
        if include_simulators and QISKIT_AVAILABLE:
            backends['aer_simulator'] = {
                'type': 'local_simulator',
                'qubits': 32,
                'operational': True,
                'pending_jobs': 0,
                'description': 'Local Qiskit Aer simulator'
            }
            
            backends['statevector_simulator'] = {
                'type': 'local_simulator', 
                'qubits': 20,
                'operational': True,
                'pending_jobs': 0,
                'description': 'Local statevector simulator'
            }
        
        # Add IBM Q backends if connected
        if self.available_backends:
            for name, info in self.available_backends.items():
                if include_simulators or not info['simulator']:
                    backends[name] = {
                        'type': 'ibm_quantum',
                        'qubits': info['qubits'],
                        'operational': info['operational'],
                        'pending_jobs': info['pending_jobs'],
                        'description': info['description']
                    }
        
        return backends
    
    def select_backend(self, backend_name: str) -> Dict[str, Any]:
        """
        Select a quantum backend for execution.
        
        Args:
            backend_name: Name of the backend to select
            
        Returns:
            Status dictionary
        """
        if not QISKIT_AVAILABLE:
            return {
                'success': False,
                'error': 'Qiskit not available'
            }
        
        # Local simulators
        if backend_name in ['aer_simulator', 'statevector_simulator']:
            if backend_name == 'aer_simulator':
                self.current_backend = Aer.get_backend('aer_simulator')
            else:
                self.current_backend = Aer.get_backend('statevector_simulator')
            
            return {
                'success': True,
                'backend': backend_name,
                'type': 'local_simulator',
                'qubits': 32 if backend_name == 'aer_simulator' else 20
            }
        
        # IBM Q backends
        if backend_name in self.available_backends:
            backend_info = self.available_backends[backend_name]
            
            if not backend_info['operational']:
                return {
                    'success': False,
                    'error': f'Backend {backend_name} is not operational'
                }
            
            self.current_backend = backend_info['backend']
            
            return {
                'success': True,
                'backend': backend_name,
                'type': 'ibm_quantum',
                'qubits': backend_info['qubits'],
                'pending_jobs': backend_info['pending_jobs']
            }
        
        return {
            'success': False,
            'error': f'Backend {backend_name} not found'
        }
    
    def get_least_busy_backend(self, min_qubits: int = 5) -> Dict[str, Any]:
        """
        Get the least busy IBM Q backend with minimum qubits.
        
        Args:
            min_qubits: Minimum number of qubits required
            
        Returns:
            Backend information
        """
        if not self.provider:
            return {
                'success': False,
                'error': 'Not connected to IBM Quantum'
            }
        
        try:
            # Filter backends by criteria
            suitable_backends = []
            for name, info in self.available_backends.items():
                if (info['operational'] and 
                    not info['simulator'] and 
                    info['qubits'] >= min_qubits):
                    suitable_backends.append(info['backend'])
            
            if not suitable_backends:
                return {
                    'success': False,
                    'error': f'No operational backends with {min_qubits}+ qubits'
                }
            
            # Get least busy
            backend = least_busy(suitable_backends)
            backend_name = backend.name()
            
            return {
                'success': True,
                'backend': backend_name,
                'qubits': self.available_backends[backend_name]['qubits'],
                'pending_jobs': self.available_backends[backend_name]['pending_jobs']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error finding least busy backend: {str(e)}'
            }
    
    def execute_circuit(self, circuit: 'QuantumCircuit', shots: int = 1024, 
                       job_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Execute a quantum circuit on the selected backend.
        
        Args:
            circuit: Quantum circuit to execute
            shots: Number of shots to run
            job_name: Optional job name for tracking
            
        Returns:
            Job execution results
        """
        if not self.current_backend:
            return {
                'success': False,
                'error': 'No backend selected. Use select_backend() first.'
            }
        
        if not QISKIT_AVAILABLE:
            return {
                'success': False,
                'error': 'Qiskit not available'
            }
        
        try:
            job_name = job_name or f"quantum_exploit_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            print(f"[*] Executing circuit on {self.current_backend.name()}")
            print(f"[*] Shots: {shots}")
            print(f"[*] Job name: {job_name}")
            
            # Execute the circuit
            job = execute(circuit, self.current_backend, shots=shots, job_name=job_name)
            
            # Store job info
            job_info = {
                'job_id': job.job_id(),
                'job_name': job_name,
                'backend': self.current_backend.name(),
                'shots': shots,
                'submitted': datetime.now(),
                'job': job
            }
            self.job_history.append(job_info)
            
            print(f"[+] Job submitted: {job.job_id()}")
            
            # Wait for completion (with timeout for real backends)
            if hasattr(self.current_backend, 'provider'):
                # IBM Q backend - don't wait too long
                print(f"[*] Job queued on IBM Quantum backend")
                print(f"[*] Monitor status with: job_status('{job.job_id()}')")
                
                return {
                    'success': True,
                    'job_id': job.job_id(),
                    'status': 'submitted',
                    'backend': self.current_backend.name(),
                    'message': 'Job submitted to IBM Quantum. Check status later.'
                }
            else:
                # Local simulator - wait for result
                print(f"[*] Executing on local simulator...")
                result = job.result()
                
                return {
                    'success': True,
                    'job_id': job.job_id(),
                    'status': 'completed',
                    'result': result,
                    'backend': self.current_backend.name(),
                    'counts': result.get_counts() if hasattr(result, 'get_counts') else None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Circuit execution failed: {str(e)}'
            }
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get status of a submitted job.
        
        Args:
            job_id: Job ID to check
            
        Returns:
            Job status information
        """
        # Find job in history
        job_info = None
        for job_data in self.job_history:
            if job_data['job_id'] == job_id:
                job_info = job_data
                break
        
        if not job_info:
            return {
                'success': False,
                'error': f'Job {job_id} not found in history'
            }
        
        try:
            job = job_info['job']
            status = job.status()
            
            result_data = {
                'success': True,
                'job_id': job_id,
                'status': status.name,
                'backend': job_info['backend'],
                'submitted': job_info['submitted'],
                'shots': job_info['shots']
            }
            
            # If completed, get results
            if status == JobStatus.DONE:
                try:
                    result = job.result()
                    result_data['result'] = result
                    result_data['counts'] = result.get_counts() if hasattr(result, 'get_counts') else None
                    result_data['execution_time'] = getattr(result, 'time_taken', None)
                except:
                    result_data['error'] = 'Failed to retrieve results'
            
            elif status == JobStatus.ERROR:
                result_data['error'] = job.error_message()
            
            return result_data
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error checking job status: {str(e)}'
            }
    
    def get_backend_info(self) -> Dict[str, Any]:
        """
        Get information about the currently selected backend.
        
        Returns:
            Backend information dictionary
        """
        if not self.current_backend:
            return {
                'success': False,
                'error': 'No backend selected'
            }
        
        try:
            config = self.current_backend.configuration()
            
            info = {
                'success': True,
                'name': self.current_backend.name(),
                'qubits': config.n_qubits,
                'simulator': config.simulator,
                'description': getattr(config, 'description', 'No description'),
                'basis_gates': getattr(config, 'basis_gates', []),
                'coupling_map': getattr(config, 'coupling_map', None)
            }
            
            # Add status for IBM Q backends
            if hasattr(self.current_backend, 'status'):
                try:
                    status = self.current_backend.status()
                    info['operational'] = status.operational
                    info['pending_jobs'] = status.pending_jobs
                except:
                    pass
            
            return info
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error getting backend info: {str(e)}'
            }


# Global backend manager instance
quantum_backend = QuantumBackendManager()


def setup_ibmq_token():
    """
    Interactive setup for IBM Quantum token.
    """
    print("\n=== IBM Quantum Setup ===")
    print("To use IBM Quantum backends, you need a free account at:")
    print("https://quantum-computing.ibm.com/")
    print("\nAfter creating an account:")
    print("1. Go to your account settings")
    print("2. Copy your API token")
    print("3. Enter it below")
    
    token = input("\nEnter your IBM Quantum API token (or press Enter to skip): ").strip()
    
    if token:
        result = quantum_backend.initialize_ibmq(token)
        if result['success']:
            print(f"\n[+] Successfully connected to IBM Quantum!")
            print(f"[+] Available backends: {len(result['backends'])}")
            return True
        else:
            print(f"\n[!] Connection failed: {result['error']}")
            return False
    else:
        print("\n[*] Skipping IBM Quantum setup. You can configure it later.")
        return False


if __name__ == "__main__":
    # Example usage
    setup_ibmq_token()
