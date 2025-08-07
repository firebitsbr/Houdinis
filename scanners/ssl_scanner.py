"""
Houdinis Framework - SSL/TLS Scanner for Houdinis
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

Scans for SSL/TLS configurations vulnerable to quantum attacks.
"""

import socket
import ssl
import sys
import threading
from typing import Dict, Any, List, Tuple
from datetime import datetime

sys.path.append('..')
from core.modules import ScannerModule


class SslScannerModule(ScannerModule):
    """
    SSL/TLS vulnerability scanner for quantum cryptography attacks.
    
    Identifies weak cryptographic algorithms that could be vulnerable
    to quantum computing attacks using Shor's and Grover's algorithms.
    """
    
    def __init__(self):
        super().__init__()
        
        self.info = {
            'name': 'SSL/TLS Quantum Vulnerability Scanner',
            'description': 'Scans SSL/TLS configurations for quantum-vulnerable cryptography',
            'author': 'Mauro Risonho de Paula Assumpção aka firebitsbr',
            'version': '1.0',
            'category': 'scanner'
        }
        
        # Add scanner-specific options
        self.options.update({
            'THREADS': {
                'description': 'Number of threads for scanning',
                'required': False,
                'default': '5'
            },
            'VERBOSE': {
                'description': 'Enable verbose output',
                'required': False,
                'default': 'false'
            }
        })
        
        # Initialize additional attributes
        self.threads = "5"
        self.verbose = "false"
        
        # Quantum-vulnerable algorithms
        self.vulnerable_ciphers = {
            'RSA': 'Vulnerable to Shor\'s algorithm',
            'DH': 'Vulnerable to Shor\'s algorithm', 
            'ECDH': 'Vulnerable to Shor\'s algorithm',
            'ECDSA': 'Vulnerable to Shor\'s algorithm',
            'DSA': 'Vulnerable to Shor\'s algorithm'
        }
        
        self.weak_symmetric = {
            'DES': 'Vulnerable to Grover\'s algorithm (effective 28-bit security)',
            '3DES': 'Vulnerable to Grover\'s algorithm (effective 56-bit security)',
            'AES-128': 'Reduced to 64-bit security against quantum attacks',
            'RC4': 'Already broken classically and quantum-vulnerable'
        }
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the SSL/TLS quantum vulnerability scan.
        
        Returns:
            Dict containing scan results
        """
        if not self.check_requirements():
            return {
                'success': False,
                'error': 'Required options not set'
            }
        
        try:
            print(f"[*] Starting SSL/TLS quantum vulnerability scan on {self.target}:{self.port}")
            
            # Parse port as integer
            port_int = int(self.port)
            
            # Perform scan
            scan_results = self._scan_target(self.target, port_int)
            
            # Analyze results for quantum vulnerabilities
            vulnerabilities = self._analyze_quantum_vulnerabilities(scan_results)
            
            # Generate report
            report = self._generate_report(scan_results, vulnerabilities)
            
            print(report)
            
            return {
                'success': True,
                'scan_results': scan_results,
                'vulnerabilities': vulnerabilities,
                'report': report
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _scan_target(self, host: str, port: int) -> Dict[str, Any]:
        """
        Scan target for SSL/TLS configuration.
        
        Args:
            host: Target hostname/IP
            port: Target port
            
        Returns:
            Scan results dictionary
        """
        results = {
            'host': host,
            'port': port,
            'ssl_enabled': False,
            'certificate': None,
            'cipher_suites': [],
            'protocols': [],
            'errors': []
        }
        
        try:
            # Test SSL/TLS connection
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((host, port), timeout=int(self.timeout)) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    results['ssl_enabled'] = True
                    
                    # Get certificate information
                    cert = ssock.getpeercert()
                    if cert:
                        results['certificate'] = {
                            'subject': dict(x[0] for x in cert.get('subject', [])),
                            'issuer': dict(x[0] for x in cert.get('issuer', [])),
                            'version': cert.get('version'),
                            'serialNumber': cert.get('serialNumber'),
                            'notBefore': cert.get('notBefore'),
                            'notAfter': cert.get('notAfter'),
                            'subjectAltName': cert.get('subjectAltName', [])
                        }
                    
                    # Get cipher and protocol information
                    cipher = ssock.cipher()
                    if cipher:
                        results['cipher_suites'].append({
                            'name': cipher[0],
                            'protocol': cipher[1],
                            'bits': cipher[2]
                        })
                    
                    results['protocols'].append(ssock.version())
        
        except socket.timeout:
            results['errors'].append('Connection timeout')
        except socket.gaierror:
            results['errors'].append('DNS resolution failed')
        except ConnectionRefusedError:
            results['errors'].append('Connection refused')
        except ssl.SSLError as e:
            results['errors'].append(f'SSL Error: {str(e)}')
        except Exception as e:
            results['errors'].append(f'Unexpected error: {str(e)}')
        
        # Test multiple SSL/TLS protocols
        if results['ssl_enabled']:
            self._test_protocols(host, port, results)
        
        return results
    
    def _test_protocols(self, host: str, port: int, results: Dict[str, Any]):
        """
        Test different SSL/TLS protocol versions.
        
        Args:
            host: Target hostname/IP
            port: Target port
            results: Results dictionary to update
        """
        protocols_to_test = [
            ('SSLv2', ssl.PROTOCOL_SSLv23),
            ('SSLv3', ssl.PROTOCOL_SSLv23),
            ('TLSv1.0', ssl.PROTOCOL_TLSv1),
            ('TLSv1.1', ssl.PROTOCOL_TLSv1_1),
            ('TLSv1.2', ssl.PROTOCOL_TLSv1_2),
        ]
        
        # Add TLSv1.3 if available
        if hasattr(ssl, 'PROTOCOL_TLSv1_3'):
            protocols_to_test.append(('TLSv1.3', ssl.PROTOCOL_TLSv1_3))
        
        supported_protocols = []
        
        for proto_name, proto_const in protocols_to_test:
            try:
                context = ssl.SSLContext(proto_const)
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                with socket.create_connection((host, port), timeout=5) as sock:
                    with context.wrap_socket(sock) as ssock:
                        supported_protocols.append(proto_name)
                        
                        if self.verbose.lower() == 'true':
                            print(f"[+] {proto_name} supported")
                        
            except Exception:
                if self.verbose.lower() == 'true':
                    print(f"[-] {proto_name} not supported")
                continue
        
        results['supported_protocols'] = supported_protocols
    
    def _analyze_quantum_vulnerabilities(self, scan_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze scan results for quantum vulnerabilities.
        
        Args:
            scan_results: Results from SSL/TLS scan
            
        Returns:
            List of identified vulnerabilities
        """
        vulnerabilities = []
        
        if not scan_results.get('ssl_enabled'):
            return vulnerabilities
        
        # Check for quantum-vulnerable cipher suites
        for cipher in scan_results.get('cipher_suites', []):
            cipher_name = cipher.get('name', '')
            
            for vuln_cipher, description in self.vulnerable_ciphers.items():
                if vuln_cipher in cipher_name.upper():
                    vulnerabilities.append({
                        'type': 'quantum_vulnerable_cipher',
                        'severity': 'HIGH',
                        'cipher': cipher_name,
                        'description': description,
                        'recommendation': 'Migrate to post-quantum cryptography'
                    })
        
        # Check for weak symmetric encryption
        for cipher in scan_results.get('cipher_suites', []):
            cipher_name = cipher.get('name', '')
            
            for weak_sym, description in self.weak_symmetric.items():
                if weak_sym in cipher_name.upper():
                    vulnerabilities.append({
                        'type': 'quantum_weak_symmetric',
                        'severity': 'MEDIUM',
                        'cipher': cipher_name,
                        'description': description,
                        'recommendation': 'Use AES-256 or post-quantum symmetric algorithms'
                    })
        
        # Check for weak protocols
        weak_protocols = ['SSLv2', 'SSLv3', 'TLSv1.0', 'TLSv1.1']
        for protocol in scan_results.get('supported_protocols', []):
            if protocol in weak_protocols:
                vulnerabilities.append({
                    'type': 'weak_protocol',
                    'severity': 'HIGH',
                    'protocol': protocol,
                    'description': f'{protocol} is deprecated and vulnerable',
                    'recommendation': 'Disable weak protocols, use TLS 1.2+ only'
                })
        
        # Check certificate key algorithms
        cert = scan_results.get('certificate')
        if cert:
            # Note: We'd need to extract the public key algorithm from the certificate
            # This is simplified for demonstration
            vulnerabilities.append({
                'type': 'certificate_analysis',
                'severity': 'INFO',
                'description': 'Certificate uses classical cryptography',
                'recommendation': 'Plan migration to post-quantum certificates'
            })
        
        return vulnerabilities
    
    def _generate_report(self, scan_results: Dict[str, Any], vulnerabilities: List[Dict[str, Any]]) -> str:
        """
        Generate human-readable scan report.
        
        Args:
            scan_results: Scan results
            vulnerabilities: Identified vulnerabilities
            
        Returns:
            Formatted report string
        """
        report = []
        report.append("=" * 60)
        report.append("SSL/TLS QUANTUM VULNERABILITY SCAN REPORT")
        report.append("=" * 60)
        report.append(f"Target: {scan_results['host']}:{scan_results['port']}")
        report.append(f"Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        if not scan_results.get('ssl_enabled'):
            report.append("[-] SSL/TLS not enabled on target")
            if scan_results.get('errors'):
                report.append("Errors:")
                for error in scan_results['errors']:
                    report.append(f"  - {error}")
            return "\n".join(report)
        
        report.append("[+] SSL/TLS is enabled")
        report.append("")
        
        # Protocol information
        protocols = scan_results.get('supported_protocols', [])
        if protocols:
            report.append("Supported Protocols:")
            for proto in protocols:
                report.append(f"  - {proto}")
            report.append("")
        
        # Cipher suites
        ciphers = scan_results.get('cipher_suites', [])
        if ciphers:
            report.append("Cipher Suites:")
            for cipher in ciphers:
                report.append(f"  - {cipher['name']} ({cipher['protocol']}, {cipher['bits']} bits)")
            report.append("")
        
        # Vulnerabilities
        if vulnerabilities:
            report.append("QUANTUM VULNERABILITIES FOUND:")
            report.append("-" * 40)
            
            high_vulns = [v for v in vulnerabilities if v['severity'] == 'HIGH']
            medium_vulns = [v for v in vulnerabilities if v['severity'] == 'MEDIUM']
            info_vulns = [v for v in vulnerabilities if v['severity'] == 'INFO']
            
            if high_vulns:
                report.append("HIGH SEVERITY:")
                for vuln in high_vulns:
                    report.append(f"  [!] {vuln.get('cipher', vuln.get('protocol', 'Unknown'))}")
                    report.append(f"      {vuln['description']}")
                    report.append(f"      Recommendation: {vuln['recommendation']}")
                    report.append("")
            
            if medium_vulns:
                report.append("MEDIUM SEVERITY:")
                for vuln in medium_vulns:
                    report.append(f"  [*] {vuln.get('cipher', vuln.get('protocol', 'Unknown'))}")
                    report.append(f"      {vuln['description']}")
                    report.append(f"      Recommendation: {vuln['recommendation']}")
                    report.append("")
            
            if info_vulns:
                report.append("INFORMATIONAL:")
                for vuln in info_vulns:
                    report.append(f"  [i] {vuln['description']}")
                    report.append(f"      Recommendation: {vuln['recommendation']}")
                    report.append("")
        else:
            report.append("[+] No quantum vulnerabilities detected")
            report.append("    (Note: This doesn't guarantee quantum resistance)")
        
        report.append("=" * 60)
        
        return "\n".join(report)
