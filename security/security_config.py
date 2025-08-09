#!/usr/bin/env python3
"""
Houdinis Framework - Security Configuration Module
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

Centralized security configuration and validation for the Houdinis framework.
"""

import re
import os
import secrets
import hashlib
import ipaddress
from typing import Dict, List, Union, Optional
import logging


class SecurityConfig:
    """Security configuration and validation for Houdinis framework"""
    
    # Security constants
    MAX_INPUT_LENGTH = 1000
    MAX_FILENAME_LENGTH = 255
    MAX_COMMAND_LENGTH = 500
    
    # Allowed characters in various contexts
    SAFE_HOSTNAME_PATTERN = re.compile(r'^[a-zA-Z0-9.-]+$')
    SAFE_FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9._-]+$')
    SAFE_COMMAND_PATTERN = re.compile(r'^[a-zA-Z0-9\s._/-]+$')
    
    # Dangerous command patterns to block
    DANGEROUS_PATTERNS = [
        re.compile(r'[;&|`$()]'),  # Command injection
        re.compile(r'\.\./'),      # Path traversal
        re.compile(r'eval\s*\('),  # Code execution
        re.compile(r'exec\s*\('),  # Code execution
        re.compile(r'import\s+os'), # OS imports
        re.compile(r'subprocess'),  # Subprocess calls
        re.compile(r'shell=True'), # Shell execution
        re.compile(r'\brm\s+'), # File deletion commands
        re.compile(r'\bcat\s+/'), # System file access
        re.compile(r'\bls\s+/'), # Directory listing
        re.compile(r'/etc/'), # System directory access
        re.compile(r'/bin/'), # Binary directory access
        re.compile(r'sudo\s+'), # Privilege escalation
    ]
    
    # Quantum-vulnerable algorithms (for educational purposes)
    QUANTUM_VULNERABLE_ALGORITHMS = {
        'RSA': {'type': 'asymmetric', 'risk': 'HIGH'},
        'DSA': {'type': 'asymmetric', 'risk': 'HIGH'},
        'ECDSA': {'type': 'asymmetric', 'risk': 'HIGH'},
        'DH': {'type': 'key_exchange', 'risk': 'HIGH'},
        'ECDH': {'type': 'key_exchange', 'risk': 'HIGH'},
        'AES-128': {'type': 'symmetric', 'risk': 'MEDIUM'},
        '3DES': {'type': 'symmetric', 'risk': 'HIGH'},
        'MD5': {'type': 'hash', 'risk': 'HIGH'},
        'SHA1': {'type': 'hash', 'risk': 'MEDIUM'},
    }

    @staticmethod
    def validate_hostname(hostname: str) -> bool:
        """Validate hostname format"""
        if not hostname or len(hostname) > 253:
            return False
        
        if not SecurityConfig.SAFE_HOSTNAME_PATTERN.match(hostname):
            return False
        
        # Additional validation for IP addresses
        try:
            ipaddress.ip_address(hostname)
            return True
        except ValueError:
            pass
        
        # Validate hostname parts
        parts = hostname.split('.')
        for part in parts:
            if not part or len(part) > 63:
                return False
            if part.startswith('-') or part.endswith('-'):
                return False
        
        return True

    @staticmethod
    def validate_port(port: Union[int, str]) -> bool:
        """Validate network port number"""
        try:
            port_int = int(port)
            return 1 <= port_int <= 65535
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_filename(filename: str) -> bool:
        """Validate filename for security"""
        if not filename or len(filename) > SecurityConfig.MAX_FILENAME_LENGTH:
            return False
        
        # Check for path traversal
        if '..' in filename or filename.startswith('/'):
            return False
        
        # Check for safe characters
        if not SecurityConfig.SAFE_FILENAME_PATTERN.match(filename):
            return False
        
        return True

    @staticmethod
    def validate_command(command: str) -> bool:
        """Validate command input for safety"""
        if not command or len(command) > SecurityConfig.MAX_COMMAND_LENGTH:
            return False
        
        # Check for dangerous patterns
        for pattern in SecurityConfig.DANGEROUS_PATTERNS:
            if pattern.search(command):
                return False
        
        return True

    @staticmethod
    def sanitize_input(input_str: str, max_length: int = None) -> str:
        """Sanitize user input"""
        if not input_str:
            return ""
        
        # Limit length
        if max_length:
            input_str = input_str[:max_length]
        else:
            input_str = input_str[:SecurityConfig.MAX_INPUT_LENGTH]
        
        # Remove control characters
        input_str = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', input_str)
        
        return input_str.strip()

    @staticmethod
    def validate_token(token: str) -> bool:
        """Validate API token format"""
        if not token or len(token) < 10:
            return False
        
        # Check for reasonable token format
        if not re.match(r'^[A-Za-z0-9_-]+$', token):
            return False
        
        return True

    @staticmethod
    def secure_file_permissions(filepath: str, mode: int = 0o600):
        """Set secure file permissions"""
        try:
            os.chmod(filepath, mode)
            return True
        except (OSError, IOError):
            return False

    @staticmethod
    def generate_secure_filename(base_name: str, extension: str = "") -> str:
        """Generate a secure filename with random component"""
        # Sanitize base name
        safe_base = re.sub(r'[^a-zA-Z0-9_-]', '_', base_name)
        
        # Add random component for uniqueness
        random_part = secrets.token_hex(8)
        
        if extension and not extension.startswith('.'):
            extension = '.' + extension
        
        return f"{safe_base}_{random_part}{extension}"

    @staticmethod
    def hash_sensitive_data(data: str) -> str:
        """Hash sensitive data for logging"""
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    @staticmethod
    def setup_secure_logging(log_file: str = "houdinis_security.log") -> logging.Logger:
        """Setup secure logging configuration"""
        logger = logging.getLogger('houdinis_security')
        logger.setLevel(logging.INFO)
        
        # Create file handler with secure permissions
        handler = logging.FileHandler(log_file)
        SecurityConfig.secure_file_permissions(log_file, 0o600)
        
        # Set format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger

    @staticmethod
    def log_security_event(event_type: str, details: Dict, logger: logging.Logger = None):
        """Log security-related events"""
        if logger is None:
            logger = SecurityConfig.setup_secure_logging()
        
        # Sanitize details for logging
        safe_details = {}
        for key, value in details.items():
            if isinstance(value, str):
                if 'token' in key.lower() or 'password' in key.lower():
                    safe_details[key] = SecurityConfig.hash_sensitive_data(value)
                else:
                    safe_details[key] = SecurityConfig.sanitize_input(value, 100)
            else:
                safe_details[key] = str(value)[:100]
        
        logger.info(f"Security Event: {event_type} - {safe_details}")

    @staticmethod
    def assess_quantum_vulnerability(algorithm: str) -> Dict:
        """Assess quantum vulnerability of cryptographic algorithm"""
        algorithm_upper = algorithm.upper()
        
        if algorithm_upper in SecurityConfig.QUANTUM_VULNERABLE_ALGORITHMS:
            vuln_info = SecurityConfig.QUANTUM_VULNERABLE_ALGORITHMS[algorithm_upper]
            return {
                'vulnerable': True,
                'algorithm': algorithm,
                'type': vuln_info['type'],
                'risk_level': vuln_info['risk'],
                'recommendation': SecurityConfig._get_quantum_safe_alternative(algorithm_upper)
            }
        else:
            return {
                'vulnerable': False,
                'algorithm': algorithm,
                'type': 'unknown',
                'risk_level': 'LOW',
                'recommendation': 'Monitor for quantum developments'
            }

    @staticmethod
    def _get_quantum_safe_alternative(algorithm: str) -> str:
        """Get quantum-safe alternative for vulnerable algorithm"""
        alternatives = {
            'RSA': 'Use post-quantum algorithms like CRYSTALS-Kyber or NTRU',
            'DSA': 'Use post-quantum signatures like CRYSTALS-Dilithium or SPHINCS+',
            'ECDSA': 'Use EdDSA or post-quantum signatures',
            'DH': 'Use post-quantum key exchange like CRYSTALS-Kyber',
            'ECDH': 'Use post-quantum key exchange like CRYSTALS-Kyber',
            'AES-128': 'Use AES-256 for quantum resistance',
            '3DES': 'Use AES-256',
            'MD5': 'Use SHA-3 or BLAKE2',
            'SHA1': 'Use SHA-256 or SHA-3'
        }
        return alternatives.get(algorithm, 'Use quantum-safe alternatives')


# Example usage and testing
if __name__ == "__main__":
    # Test security functions
    print("Testing Security Configuration...")
    
    # Test hostname validation
    print(f"Valid hostname 'example.com': {SecurityConfig.validate_hostname('example.com')}")
    print(f"Invalid hostname '../etc/passwd': {SecurityConfig.validate_hostname('../etc/passwd')}")
    
    # Test port validation
    print(f"Valid port 443: {SecurityConfig.validate_port(443)}")
    print(f"Invalid port 70000: {SecurityConfig.validate_port(70000)}")
    
    # Test command validation
    print(f"Safe command 'show modules': {SecurityConfig.validate_command('show modules')}")
    print(f"Dangerous command 'rm -rf /': {SecurityConfig.validate_command('rm -rf /')}")
    
    # Test quantum vulnerability assessment
    rsa_assessment = SecurityConfig.assess_quantum_vulnerability('RSA')
    print(f"RSA vulnerability: {rsa_assessment}")
    
    print("Security configuration tests completed.")
