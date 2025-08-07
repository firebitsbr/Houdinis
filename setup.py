"""
Houdinis - Advanced Quantum Cryptography Exploitation Framework        console_scripts=[
            "houdini=quantum_exploit:main",
        ],     console_scripts=[
            "houdini=quantum_exploit:main",
        ], comprehensive penetration testing framework for assessing quantum vulnerabilities
in cryptographic implementations. This tool simulates quantum attacks and provides
detailed security assessments for red team operations.

Features:
- Quantum vulnerability scanning
- Shor's algorithm simulation for RSA/ECC attacks
- Grover's algorithm for symmetric key search
- Post-quantum cryptography readiness assessment
- Comprehensive penetration testing reports

Author: Mauro Risonho de Paula Assumpção aka firebitsbr
License: MIT
Version: 1.0.0
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="houdini",
    version="1.0.0",
    author="Mauro Risonho de Paula Assumpção aka firebitsbr",
    author_email="mauro.risonho@gmail.com",
    description="Advanced Quantum Cryptography Exploitation Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/firebitsbr/houdinisframework",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "houdini=quantum_exploit:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="quantum computing, cryptography, penetration testing, red team, security assessment",
)
