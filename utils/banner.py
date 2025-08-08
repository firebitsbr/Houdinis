"""
Houdinis Framework - Corporate banner utility for Houdinis framework.
Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT

Displays professional ASCII art and version information.
"""

import random
from datetime import datetime


def get_banner() -> str:
    """
    Get the Houdinis framework banner.

    Returns:
        ASCII art banner string
    """
    banners = [
        r"""
HOUDINIS FRAMEWORK
==================

Quantum Cryptography Penetration Testing Platform
Enterprise Security Assessment Solution

Version: 2.0.0
Build: Professional
""",
        r"""
+================================================================+
|                     HOUDINIS FRAMEWORK                        |
|                                                                |
|         Quantum Cryptography Security Assessment              |
|              Professional Testing Platform                    |
+================================================================+
""",
        r"""
HOUDINIS
--------
Advanced Quantum Cryptography Analysis Platform
Professional Security Testing Framework

Enterprise Edition v2.0.0
Corporate Security Solutions
""",
        r"""
HOUDINIS ENTERPRISE FRAMEWORK
=============================

Advanced Quantum Cryptography Analysis Platform
Professional Security Testing and Assessment

Build: Corporate Edition
Support: Enterprise Level
"""
    ]

    return random.choice(banners)


def get_version_info() -> str:
    """
    Get version and build information.

    Returns:
        Version information string
    """
    version_info = """
+================================================================+
| Houdinis Framework v2.0.0                                     |
| Advanced Quantum Cryptography Penetration Testing            |
|                                                                |
| Algorithms: Shor's, Grover's, Post-Quantum Analysis          |
| Platforms:  SSL/TLS, SSH, Custom Crypto Implementations      |
| Purpose:    Authorized Security Testing Only                  |
+================================================================+
"""
    return version_info


def get_disclaimer() -> str:
    """
    Get legal disclaimer.

    Returns:
        Disclaimer text
    """
    disclaimer = """
LEGAL DISCLAIMER

This tool is designed for authorized penetration testing and security
research purposes only. Users are responsible for complying with all
applicable local, state, national, and international laws.

The authors assume no liability and are not responsible for any misuse
or damage caused by this program. Use at your own risk.

By using this tool, you agree to use it only on systems you own or
have explicit written permission to test.

═══════════════════════════════════════════════════════════════════
"""
    return disclaimer


def get_startup_info() -> str:
    """
    Get startup information including tips.

    Returns:
        Startup information string
    """
    tips = [
        "Tip: Use 'show modules' to see all available quantum exploit modules",
        "Tip: Start with 'use scanner/quantum_vuln_scanner' for vulnerability assessment",
        "Tip: Try 'use exploit/rsa_shor' to demonstrate quantum RSA factorization",
        "Tip: Use 'help' command to see all available console commands",
        "Tip: Set 'VERBOSE true' for detailed output in scanner modules",
        "Tip: Check 'show sessions' to manage active exploit sessions"
    ]

    info = f"""
Active modules:
  - Scanners: SSL/TLS quantum vulnerability detection
  - Exploits:  Shor's algorithm RSA factorization
  - Payloads: Post-quantum migration guidance

{random.choice(tips)}

Ready for quantum cryptography security assessment.
"""
    return info


def print_banner(show_disclaimer: bool = True):
    """
    Print the complete banner with version info.

    Args:
        show_disclaimer: Whether to show legal disclaimer
    """
    print(get_banner())
    print(get_version_info())

    if show_disclaimer:
        print(get_disclaimer())

    print(get_startup_info())


def get_module_banner(module_name: str, module_info: dict) -> str:
    """
    Get banner for a specific module.

    Args:
        module_name: Name of the module
        module_info: Module information dictionary

    Returns:
        Module-specific banner
    """
    banner = f"""
+================================================================+
| Module: {module_name:<51} |
| {module_info.get('description', 'No description'):<61} |
|                                                                |
| Author:  {module_info.get('author', 'Unknown'):<51} |
| Version: {module_info.get('version', '1.0'):<51} |
+================================================================+
"""
    return banner


def get_quantum_facts() -> str:
    """
    Get random quantum computing facts for educational purposes.

    Returns:
        Random quantum fact
    """
    facts = [
# TODO: Consider breaking this long line (length: 106)
        "Shor's algorithm can factor large integers exponentially faster than known classical algorithms",
        "Grover's algorithm provides quadratic speedup for unstructured search problems",
        "NIST is standardizing post-quantum cryptographic algorithms like CRYSTALS-Kyber",
        "Quantum computers with 4096 logical qubits could break 2048-bit RSA",
        "AES-256 provides 128 bits of security against quantum attacks (Grover's)",
        "Post-quantum cryptography is based on problems like lattices and hash functions",
        "IBM's quantum computers currently have over 1000 physical qubits",
        "Quantum error correction requires hundreds of physical qubits per logical qubit",
        "The NSA recommends planning migration to post-quantum cryptography now"
    ]

    return f"Quantum Fact: {random.choice(facts)}"


if __name__ == "__main__":
    # Test banner functions
    print_banner()
    print("\n" + "="*70)
    print(get_quantum_facts())
