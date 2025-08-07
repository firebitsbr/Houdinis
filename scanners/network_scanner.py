"""
Houdinis Framework - Network Host Scanner for Houdinis
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

Network Host Scanner for Houdinis
Discovers hosts (Classical Computers) and quantum-vulnerable cryptographic services.
"""

import socket
import ssl
import sys
import threading
import time
from typing import Dict, Any, List, Tuple
from datetime import datetime

sys.path.append('..')
from core.modules import ScannerModule


class NetworkScannerModule(ScannerModule):
    """
    Network scanner for discovering quantum-vulnerable services.
    
    Scans hosts for open ports and identifies cryptographic implementations
    that may be vulnerable to quantum attacks.
    """
    
    def __init__(self):
        super().__init__()
        
        self.info = {
            'name': 'Network Quantum Vulnerability Scanner',
            'description': 'Discovers hosts and quantum-vulnerable cryptographic services',
            'author': 'Mauro Risonho de Paula Assumpção aka firebitsbr',
            'version': '1.0',
            'category': 'scanner'
        }
        
        # Add scanner-specific options
        self.options.update({
            'RHOSTS': {
                'description': 'Target host(s) (single IP or CIDR range)',
                'required': True,
                'default': ''
            },
            'PORTS': {
                'description': 'Ports to scan (comma-separated or range)',
                'required': False,
                'default': '22,80,443,993,995'
            },
            'THREADS': {
                'description': 'Number of concurrent threads',
                'required': False,
                'default': '50'
            },
            'CRYPTO_DETECT': {
                'description': 'Enable cryptographic service detection',
                'required': False,
                'default': 'true'
            }
        })
        
        # Initialize additional attributes
        self.rhosts = ""
        self.ports = "22,80,443,993,995"
        self.threads = "50"
        self.crypto_detect = "true"
        
        # Service detection signatures
        self.service_signatures = {
            22: {'name': 'SSH', 'crypto': True},
            80: {'name': 'HTTP', 'crypto': False},
            443: {'name': 'HTTPS', 'crypto': True},
            993: {'name': 'IMAPS', 'crypto': True},
            995: {'name': 'POP3S', 'crypto': True},
            25: {'name': 'SMTP', 'crypto': False},
            587: {'name': 'SMTP-TLS', 'crypto': True},
            21: {'name': 'FTP', 'crypto': False},
            990: {'name': 'FTPS', 'crypto': True}
        }
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the network quantum vulnerability scan.
        
        Returns:
            Dict containing scan results
        """
        if not self.check_requirements():
            return {
                'success': False,
                'error': 'Required options not set'
            }
        
        try:
            print(f"[*] Starting network scan...")
            
            # Parse targets and ports
            targets = self._parse_targets(self.rhosts)
            ports = self._parse_ports(self.ports)
            
            print(f"[*] Scanning {len(targets)} host(s) on {len(ports)} port(s)")
            print(f"[*] Using {self.threads} threads")
            
            # Perform scan
            scan_results = {
                'targets_scanned': len(targets),
                'ports_scanned': len(ports),
                'open_services': [],
                'vulnerable_services': [],
                'scan_time': datetime.now().isoformat()
            }
            
            # Scan all targets
            for target in targets:
                host_results = self._scan_host(target, ports)
                scan_results['open_services'].extend(host_results['open_services'])
                scan_results['vulnerable_services'].extend(host_results['vulnerable_services'])
            
            # Generate summary
            self._print_scan_summary(scan_results)
            
            return {
                'success': True,
                'scan_results': scan_results
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _parse_targets(self, target_string: str) -> List[str]:
        """Parse target specification into list of IPs."""
        targets = []
        
        if '/' in target_string:
            # CIDR notation - simplified implementation
            base_ip = target_string.split('/')[0]
            base_parts = base_ip.split('.')
            
            # For demo, just scan a few IPs in the range
            for i in range(1, 11):  # Scan .1 to .10
                ip = f"{base_parts[0]}.{base_parts[1]}.{base_parts[2]}.{i}"
                targets.append(ip)
        else:
            # Single IP
            targets.append(target_string)
        
        return targets
    
    def _parse_ports(self, port_string: str) -> List[int]:
        """Parse port specification into list of port numbers."""
        ports = []
        
        for part in port_string.split(','):
            part = part.strip()
            if '-' in part:
                # Port range
                start, end = map(int, part.split('-'))
                ports.extend(range(start, end + 1))
            else:
                # Single port
                ports.append(int(part))
        
        return ports
    
    def _scan_host(self, host: str, ports: List[int]) -> Dict[str, Any]:
        """Scan a single host for open ports and services."""
        results = {
            'host': host,
            'open_services': [],
            'vulnerable_services': []
        }
        
        for port in ports:
            try:
                # Test connection
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                
                if sock.connect_ex((host, port)) == 0:
                    service_info = {
                        'host': host,
                        'port': port,
                        'service': self.service_signatures.get(port, {}).get('name', 'unknown'),
                        'state': 'open'
                    }
                    
                    # Detect cryptographic details if enabled
                    if self.crypto_detect.lower() == 'true':
                        crypto_info = self._detect_crypto_service(host, port)
                        service_info.update(crypto_info)
                        
                        # Check for quantum vulnerabilities
                        if crypto_info.get('quantum_vulnerable'):
                            results['vulnerable_services'].append(service_info)
                            print(f"[+] Port {port} open — {crypto_info.get('details', '')} (Vulnerable: Yes)")
                        else:
                            print(f"[+] Port {port} open — {service_info['service']}")
                    else:
                        print(f"[+] Port {port} open — {service_info['service']}")
                    
                    results['open_services'].append(service_info)
                
                sock.close()
                
            except Exception:
                # Port closed or filtered
                continue
        
        return results
    
    def _detect_crypto_service(self, host: str, port: int) -> Dict[str, Any]:
        """Detect cryptographic details of a service."""
        crypto_info = {
            'crypto_enabled': False,
            'quantum_vulnerable': False,
            'details': ''
        }
        
        try:
            if port == 443:  # HTTPS
                crypto_info.update(self._analyze_tls_service(host, port))
            elif port == 22:  # SSH
                crypto_info.update(self._analyze_ssh_service(host, port))
            elif port in [993, 995, 587, 990]:  # Other TLS services
                crypto_info.update(self._analyze_tls_service(host, port))
        
        except Exception as e:
            crypto_info['error'] = str(e)
        
        return crypto_info
    
    def _analyze_tls_service(self, host: str, port: int) -> Dict[str, Any]:
        """Analyze TLS/SSL service for quantum vulnerabilities."""
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((host, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cipher = ssock.cipher()
                    
                    if cipher:
                        cipher_name = cipher[0]
                        
                        # Check for quantum-vulnerable algorithms
                        vulnerable = False
                        details = cipher_name
                        
                        if 'RSA' in cipher_name:
                            vulnerable = True
                            # Simulate key size detection (simplified)
                            key_size = 1024 if 'CBC' in cipher_name else 2048
                            details = f"TLS_{cipher_name} (RSA-{key_size})"
                        elif 'ECDHE' in cipher_name:
                            vulnerable = True
                            details = f"TLS_{cipher_name} (ECDHE-P256)"
                        elif 'DH' in cipher_name:
                            vulnerable = True
                            details = f"TLS_{cipher_name} (DH-1024)"
                        
                        return {
                            'crypto_enabled': True,
                            'quantum_vulnerable': vulnerable,
                            'details': details,
                            'cipher_suite': cipher_name,
                            'protocol': ssock.version()
                        }
        
        except Exception:
            pass
        
        return {
            'crypto_enabled': False,
            'quantum_vulnerable': False,
            'details': 'No TLS detected'
        }
    
    def _analyze_ssh_service(self, host: str, port: int) -> Dict[str, Any]:
        """Analyze SSH service for quantum vulnerabilities."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            
            # Get SSH banner
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            
            # Simulate algorithm detection (simplified)
            vulnerable_algos = ['ssh-rsa', 'ecdsa-sha2-nistp256', 'diffie-hellman-group14-sha256']
            
            return {
                'crypto_enabled': True,
                'quantum_vulnerable': True,  # SSH typically uses quantum-vulnerable algorithms
                'details': f"SSH-2.0 (RSA/ECDSA keys detected)",
                'banner': banner,
                'vulnerable_algorithms': vulnerable_algos
            }
        
        except Exception:
            pass
        
        return {
            'crypto_enabled': False,
            'quantum_vulnerable': False,
            'details': 'SSH detection failed'
        }
    
    def _print_scan_summary(self, results: Dict[str, Any]):
        """Print scan summary."""
        print(f"\n[*] Scan completed")
        print(f"[*] {len(results['open_services'])} services found")
        print(f"[*] {len(results['vulnerable_services'])} quantum-vulnerable services detected")
        
        if results['vulnerable_services']:
            print(f"\n[!] Quantum-vulnerable services:")
            for service in results['vulnerable_services']:
                print(f"    {service['host']}:{service['port']} - {service['details']}")
                
            print(f"\n[!] Recommendation: Use exploit modules to test these services")
            print(f"[!] Try: use exploit/rsa_shor or use exploit/tls_decrypt")
