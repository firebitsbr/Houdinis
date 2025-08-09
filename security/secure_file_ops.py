#!/usr/bin/env python3
"""
Houdinis Framework - Secure File Operations Module
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

Secure file operations with proper validation and error handling.
"""

import os
import stat
import tempfile
import hashlib
import shutil
from typing import Dict, List, Optional, Union
from pathlib import Path
from security.security_config import SecurityConfig


class SecureFileOperations:
    """Secure file operations for Houdinis framework"""
    
    # Allowed file extensions for different operations
    ALLOWED_EXTENSIONS = {
        'config': ['.ini', '.conf', '.cfg', '.yaml', '.yml', '.json'],
        'log': ['.log', '.txt'],
        'data': ['.db', '.sqlite', '.sqlite3'],
        'key': ['.pem', '.key', '.crt', '.pub'],
        'script': ['.py', '.sh', '.rc']
    }
    
    MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB limit
    
    def __init__(self, base_path: Optional[str] = None):
        """Initialize secure file operations"""
        if base_path:
            self.base_path = Path(base_path).resolve()
        else:
            self.base_path = Path.cwd()
        
        # Ensure base path exists
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        self.temp_dir = None
        self.logger = SecurityConfig.setup_secure_logging("file_operations.log")
    
    def validate_path(self, file_path: Union[str, Path], allow_create: bool = False) -> bool:
        """Validate file path for security"""
        try:
            path = Path(file_path).resolve()
            
            # Check for path traversal
            if not str(path).startswith(str(self.base_path)):
                self.logger.warning(f"Path traversal attempt: {file_path}")
                return False
            
            # Check filename
            if not SecurityConfig.validate_filename(path.name):
                self.logger.warning(f"Invalid filename: {path.name}")
                return False
            
            # Check if file exists (if required)
            if not allow_create and not path.exists():
                return False
            
            return True
        except Exception as e:
            self.logger.error(f"Path validation error: {e}")
            return False
    
    def secure_read_file(self, file_path: Union[str, Path], max_size: int = None) -> Optional[str]:
        """Securely read file content"""
        if not self.validate_path(file_path):
            return None
        
        try:
            path = Path(file_path).resolve()
            
            # Check file size
            file_size = path.stat().st_size
            max_allowed = max_size or self.MAX_FILE_SIZE
            
            if file_size > max_allowed:
                self.logger.warning(f"File too large: {path} ({file_size} bytes)")
                return None
            
            # Read with proper encoding
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(max_allowed)
            
            SecurityConfig.log_security_event(
                "file_read",
                {"path": str(path), "size": file_size},
                self.logger
            )
            
            return content
            
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            return None
    
    def secure_write_file(self, file_path: Union[str, Path], content: str, mode: int = 0o600) -> bool:
        """Securely write file content"""
        try:
            path = Path(file_path).resolve()
            
            # For temp files, skip base path validation
            if not str(path).startswith('/tmp/'):
                if not self.validate_path(file_path, allow_create=True):
                    return False
            
            # Check content size
            if len(content.encode('utf-8')) > self.MAX_FILE_SIZE:
                self.logger.warning(f"Content too large for file: {path}")
                return False
            
            # Create directory if needed
            path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            
            # Write to temporary file first
            with tempfile.NamedTemporaryFile(
                mode='w', 
                encoding='utf-8', 
                dir=path.parent, 
                delete=False
            ) as tmp_file:
                tmp_file.write(content)
                tmp_path = tmp_file.name
            
            # Set secure permissions
            os.chmod(tmp_path, mode)
            
            # Atomic move
            shutil.move(tmp_path, path)
            
            SecurityConfig.log_security_event(
                "file_write",
                {"path": str(path), "size": len(content)},
                self.logger
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error writing file {file_path}: {e}")
            return False
    
    def secure_delete_file(self, file_path: Union[str, Path]) -> bool:
        """Securely delete file"""
        if not self.validate_path(file_path):
            return False
        
        try:
            path = Path(file_path).resolve()
            
            if not path.exists():
                return True
            
            # Secure deletion (overwrite with random data)
            if path.is_file():
                file_size = path.stat().st_size
                
                # Overwrite with random data multiple times
                with open(path, 'r+b') as f:
                    for _ in range(3):
                        f.seek(0)
                        f.write(os.urandom(file_size))
                        f.flush()
                        os.fsync(f.fileno())
            
            # Remove file
            path.unlink()
            
            SecurityConfig.log_security_event(
                "file_delete",
                {"path": str(path)},
                self.logger
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error deleting file {file_path}: {e}")
            return False
    
    def create_temp_file(self, suffix: str = "", prefix: str = "houdini_") -> Optional[str]:
        """Create secure temporary file"""
        try:
            if not self.temp_dir:
                self.temp_dir = tempfile.mkdtemp(prefix="houdini_secure_")
                os.chmod(self.temp_dir, 0o700)
            
            tmp_file = tempfile.NamedTemporaryFile(
                suffix=suffix,
                prefix=prefix,
                dir=self.temp_dir,
                delete=False
            )
            tmp_file.close()
            
            # Set secure permissions
            os.chmod(tmp_file.name, 0o600)
            
            return tmp_file.name
            
        except Exception as e:
            self.logger.error(f"Error creating temp file: {e}")
            return None
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        try:
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                self.temp_dir = None
                
        except Exception as e:
            self.logger.error(f"Error cleaning temp files: {e}")
    
    def calculate_file_hash(self, file_path: Union[str, Path], algorithm: str = "sha256") -> Optional[str]:
        """Calculate secure hash of file"""
        if not self.validate_path(file_path):
            return None
        
        try:
            path = Path(file_path).resolve()
            
            # Get hash algorithm
            if algorithm.lower() == "sha256":
                hasher = hashlib.sha256()
            elif algorithm.lower() == "sha512":
                hasher = hashlib.sha512()
            else:
                self.logger.warning(f"Unsupported hash algorithm: {algorithm}")
                return None
            
            # Read file in chunks
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    hasher.update(chunk)
            
            return hasher.hexdigest()
            
        except Exception as e:
            self.logger.error(f"Error calculating hash for {file_path}: {e}")
            return None
    
    def validate_file_extension(self, file_path: Union[str, Path], file_type: str) -> bool:
        """Validate file extension against allowed types"""
        try:
            path = Path(file_path)
            extension = path.suffix.lower()
            
            allowed = self.ALLOWED_EXTENSIONS.get(file_type, [])
            return extension in allowed
            
        except Exception:
            return False
    
    def get_safe_filename(self, original_name: str, file_type: str = None) -> str:
        """Generate safe filename from original"""
        # Remove dangerous characters
        safe_name = SecurityConfig.sanitize_input(original_name, 200)
        
        # Ensure valid extension if type specified
        if file_type and not self.validate_file_extension(safe_name, file_type):
            if file_type in self.ALLOWED_EXTENSIONS:
                safe_name += self.ALLOWED_EXTENSIONS[file_type][0]
        
        return SecurityConfig.generate_secure_filename(safe_name)
    
    def __del__(self):
        """Cleanup on destruction"""
        self.cleanup_temp_files()


# Example usage
if __name__ == "__main__":
    # Test secure file operations
    secure_files = SecureFileOperations()
    
    # Test file validation
    print(f"Valid path test: {secure_files.validate_path('test.txt', allow_create=True)}")
    print(f"Invalid path test: {secure_files.validate_path('../../../etc/passwd')}")
    
    # Test safe filename generation
    safe_name = secure_files.get_safe_filename("my file with spaces.txt", "config")
    print(f"Safe filename: {safe_name}")
    
    print("Secure file operations tests completed.")
