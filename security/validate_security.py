#!/usr/bin/env python3
"""
Houdinis Framework - Security Validation Script
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

Comprehensive security validation and testing script for the Houdinis framework.
"""

import os
import sys
import subprocess
import stat
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from security.security_config import SecurityConfig
from security.secure_file_ops import SecureFileOperations


class SecurityValidator:
    """Security validation and testing for Houdinis framework"""
    
    def __init__(self):
        self.results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0,
            'details': []
        }
        self.project_root = project_root
    
    def log_result(self, test_name: str, status: str, message: str):
        """Log test result"""
        self.results['details'].append({
            'test': test_name,
            'status': status,
            'message': message
        })
        
        if status == 'PASS':
            self.results['passed'] += 1
            print(f"✓ {test_name}: {message}")
        elif status == 'FAIL':
            self.results['failed'] += 1
            print(f"✗ {test_name}: {message}")
        elif status == 'WARN':
            self.results['warnings'] += 1
            print(f"⚠ {test_name}: {message}")
    
    def test_file_permissions(self):
        """Test file permissions for security"""
        print("\n=== Testing File Permissions ===")
        
        # Check sensitive files have secure permissions
        sensitive_files = [
            'security/security_config.py',
            'security/secure_file_ops.py',
            'config.ini'
        ]
        
        for file_path in sensitive_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                file_stat = full_path.stat()
                file_mode = stat.filemode(file_stat.st_mode)
                
                # Check if file is world-readable or world-writable
                if file_stat.st_mode & (stat.S_IROTH | stat.S_IWOTH):
                    self.log_result(
                        f"File Permissions: {file_path}",
                        "WARN",
                        f"File may be too permissive: {file_mode}"
                    )
                else:
                    self.log_result(
                        f"File Permissions: {file_path}",
                        "PASS",
                        f"Secure permissions: {file_mode}"
                    )
            else:
                self.log_result(
                    f"File Permissions: {file_path}",
                    "WARN",
                    "File not found"
                )
    
    def test_input_validation(self):
        """Test input validation functions"""
        print("\n=== Testing Input Validation ===")
        
        # Test hostname validation
        valid_hosts = ['example.com', '192.168.1.1', 'localhost']
        invalid_hosts = ['../etc/passwd', 'host;rm -rf /', '']
        
        for host in valid_hosts:
            if SecurityConfig.validate_hostname(host):
                self.log_result(
                    f"Hostname Validation: {host}",
                    "PASS",
                    "Valid hostname accepted"
                )
            else:
                self.log_result(
                    f"Hostname Validation: {host}",
                    "FAIL",
                    "Valid hostname rejected"
                )
        
        for host in invalid_hosts:
            if not SecurityConfig.validate_hostname(host):
                self.log_result(
                    f"Hostname Validation: {host}",
                    "PASS",
                    "Invalid hostname rejected"
                )
            else:
                self.log_result(
                    f"Hostname Validation: {host}",
                    "FAIL",
                    "Invalid hostname accepted"
                )
        
        # Test port validation
        valid_ports = [22, 80, 443, 8080]
        invalid_ports = [0, -1, 70000, 'abc']
        
        for port in valid_ports:
            if SecurityConfig.validate_port(port):
                self.log_result(
                    f"Port Validation: {port}",
                    "PASS",
                    "Valid port accepted"
                )
            else:
                self.log_result(
                    f"Port Validation: {port}",
                    "FAIL",
                    "Valid port rejected"
                )
        
        for port in invalid_ports:
            if not SecurityConfig.validate_port(port):
                self.log_result(
                    f"Port Validation: {port}",
                    "PASS",
                    "Invalid port rejected"
                )
            else:
                self.log_result(
                    f"Port Validation: {port}",
                    "FAIL",
                    "Invalid port accepted"
                )
    
    def test_command_validation(self):
        """Test command validation"""
        print("\n=== Testing Command Validation ===")
        
        safe_commands = [
            'show modules',
            'use exploit/rsa_shor',
            'set target 192.168.1.1',
            'help'
        ]
        
        dangerous_commands = [
            'rm -rf /',
            'cat /etc/passwd',
            '; ls -la',
            '$(whoami)',
            '`id`',
            'exec("import os")'
        ]
        
        for cmd in safe_commands:
            if SecurityConfig.validate_command(cmd):
                self.log_result(
                    f"Command Validation: {cmd}",
                    "PASS",
                    "Safe command accepted"
                )
            else:
                self.log_result(
                    f"Command Validation: {cmd}",
                    "FAIL",
                    "Safe command rejected"
                )
        
        for cmd in dangerous_commands:
            if not SecurityConfig.validate_command(cmd):
                self.log_result(
                    f"Command Validation: {cmd}",
                    "PASS",
                    "Dangerous command rejected"
                )
            else:
                self.log_result(
                    f"Command Validation: {cmd}",
                    "FAIL",
                    "Dangerous command accepted"
                )
    
    def test_secure_file_operations(self):
        """Test secure file operations"""
        print("\n=== Testing Secure File Operations ===")
        
        secure_files = SecureFileOperations(str(self.project_root))
        
        # Test path validation
        valid_paths = ['test.txt', 'logs/test.log', 'config/test.ini']
        invalid_paths = ['../etc/passwd', '/etc/shadow', '../../test.txt']
        
        for path in valid_paths:
            if secure_files.validate_path(path, allow_create=True):
                self.log_result(
                    f"Path Validation: {path}",
                    "PASS",
                    "Valid path accepted"
                )
            else:
                self.log_result(
                    f"Path Validation: {path}",
                    "FAIL",
                    "Valid path rejected"
                )
        
        for path in invalid_paths:
            if not secure_files.validate_path(path, allow_create=True):
                self.log_result(
                    f"Path Validation: {path}",
                    "PASS",
                    "Invalid path rejected"
                )
            else:
                self.log_result(
                    f"Path Validation: {path}",
                    "FAIL",
                    "Invalid path accepted"
                )
        
        # Test secure file write/read
        test_content = "Test security content"
        temp_file = secure_files.create_temp_file(suffix=".txt")
        
        if temp_file:
            if secure_files.secure_write_file(temp_file, test_content):
                self.log_result(
                    "Secure File Write",
                    "PASS",
                    "File written successfully"
                )
                
                # Test read
                read_content = secure_files.secure_read_file(temp_file)
                if read_content == test_content:
                    self.log_result(
                        "Secure File Read",
                        "PASS",
                        "File read successfully"
                    )
                else:
                    self.log_result(
                        "Secure File Read",
                        "FAIL",
                        "File content mismatch"
                    )
                
                # Test file permissions
                file_stat = os.stat(temp_file)
                if file_stat.st_mode & 0o077 == 0:  # Only owner can access
                    self.log_result(
                        "File Permissions",
                        "PASS",
                        "Secure permissions set"
                    )
                else:
                    self.log_result(
                        "File Permissions",
                        "FAIL",
                        "Insecure permissions"
                    )
                
                # Cleanup
                secure_files.secure_delete_file(temp_file)
            else:
                self.log_result(
                    "Secure File Write",
                    "FAIL",
                    "Failed to write file"
                )
        
        secure_files.cleanup_temp_files()
    
    def test_quantum_vulnerability_assessment(self):
        """Test quantum vulnerability assessment"""
        print("\n=== Testing Quantum Vulnerability Assessment ===")
        
        vulnerable_algorithms = ['RSA', 'DSA', 'ECDSA', 'AES-128']
        safe_algorithms = ['AES-256', 'ChaCha20-Poly1305']
        
        for algo in vulnerable_algorithms:
            assessment = SecurityConfig.assess_quantum_vulnerability(algo)
            if assessment['vulnerable']:
                self.log_result(
                    f"Quantum Assessment: {algo}",
                    "PASS",
                    f"Correctly identified as vulnerable ({assessment['risk_level']})"
                )
            else:
                self.log_result(
                    f"Quantum Assessment: {algo}",
                    "FAIL",
                    "Failed to identify vulnerability"
                )
        
        for algo in safe_algorithms:
            assessment = SecurityConfig.assess_quantum_vulnerability(algo)
            if not assessment['vulnerable']:
                self.log_result(
                    f"Quantum Assessment: {algo}",
                    "PASS",
                    "Correctly identified as secure"
                )
            else:
                self.log_result(
                    f"Quantum Assessment: {algo}",
                    "WARN",
                    "May be incorrectly flagged as vulnerable"
                )
    
    def test_dependency_security(self):
        """Test for known vulnerable dependencies"""
        print("\n=== Testing Dependency Security ===")
        
        try:
            # Check if safety is available
            result = subprocess.run(['pip', 'show', 'safety'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                # Run safety check
                safety_result = subprocess.run(['safety', 'check'], 
                                             capture_output=True, text=True)
                
                if safety_result.returncode == 0:
                    self.log_result(
                        "Dependency Security",
                        "PASS",
                        "No known vulnerabilities found"
                    )
                else:
                    self.log_result(
                        "Dependency Security",
                        "WARN",
                        "Potential vulnerabilities found"
                    )
            else:
                self.log_result(
                    "Dependency Security",
                    "WARN",
                    "Safety package not installed - run 'pip install safety'"
                )
        
        except Exception as e:
            self.log_result(
                "Dependency Security",
                "WARN",
                f"Could not check dependencies: {e}"
            )
    
    def scan_for_hardcoded_secrets(self):
        """Scan for potential hardcoded secrets"""
        print("\n=== Scanning for Hardcoded Secrets ===")
        
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']{3,}["\']', 'Hardcoded password'),
            (r'token\s*=\s*["\'][^"\']{10,}["\']', 'Hardcoded token'),
            (r'api_key\s*=\s*["\'][^"\']{10,}["\']', 'Hardcoded API key'),
            (r'secret\s*=\s*["\'][^"\']{10,}["\']', 'Hardcoded secret'),
        ]
        
        python_files = list(self.project_root.rglob('*.py'))
        secrets_found = 0
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                for pattern, description in secret_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Skip test files and examples
                        if 'test' not in str(file_path).lower() and 'example' not in str(file_path).lower():
                            secrets_found += 1
                            self.log_result(
                                f"Secret Scan: {file_path}",
                                "WARN",
                                f"Potential {description} found"
                            )
            
            except Exception:
                continue
        
        if secrets_found == 0:
            self.log_result(
                "Hardcoded Secrets",
                "PASS",
                "No hardcoded secrets detected"
            )
    
    def run_all_tests(self):
        """Run all security validation tests"""
        print("🔒 Houdinis Framework Security Validation")
        print("=" * 50)
        
        self.test_file_permissions()
        self.test_input_validation()
        self.test_command_validation()
        self.test_secure_file_operations()
        self.test_quantum_vulnerability_assessment()
        self.test_dependency_security()
        self.scan_for_hardcoded_secrets()
        
        # Print summary
        print("\n" + "=" * 50)
        print("🔒 Security Validation Summary")
        print("=" * 50)
        print(f"✓ Tests Passed: {self.results['passed']}")
        print(f"✗ Tests Failed: {self.results['failed']}")
        print(f"⚠ Warnings: {self.results['warnings']}")
        
        if self.results['failed'] > 0:
            print("\n❌ SECURITY ISSUES DETECTED - Review failed tests")
            return False
        elif self.results['warnings'] > 0:
            print("\n⚠️  WARNINGS DETECTED - Review and address warnings")
            return True
        else:
            print("\n✅ ALL SECURITY TESTS PASSED")
            return True


if __name__ == "__main__":
    validator = SecurityValidator()
    success = validator.run_all_tests()
    sys.exit(0 if success else 1)
