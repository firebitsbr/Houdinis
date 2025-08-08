#!/usr/bin/env python3
"""
Code Quality Improvement Script for Houdinis Framework
Applies automated fixes for common code quality issues.
"""

import os
import re
import sys
from pathlib import Path

def fix_whitespace_issues():
    """Fix blank lines containing whitespace and trailing whitespace"""
    python_files = list(Path('.').glob('**/*.py'))

    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Fix blank lines containing whitespace
            content = re.sub(r'^[ \t]+$', '', content, flags=re.MULTILINE)

            # Fix trailing whitespace
            content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Fixed whitespace issues in {file_path}")

        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")

def fix_import_issues():
    """Fix common import issues"""
    python_files = list(Path('.').glob('**/*.py'))

    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Remove unused imports (basic detection)
            import_lines = []
            other_lines = []
            content_lines = []

            in_imports = True
            for line in lines:
                if line.strip().startswith(('import ', 'from ')) and in_imports:
                    import_lines.append(line)
                elif line.strip() == '' and in_imports:
                    import_lines.append(line)
                else:
                    in_imports = False
                    other_lines.append(line)

            # Simple check for unused imports
            content = ''.join(other_lines)
            used_imports = []

            for import_line in import_lines:
                if import_line.strip() == '':
                    used_imports.append(import_line)
                    continue

                # Extract imported names
                if import_line.strip().startswith('import '):
                    modules = import_line.strip()[7:].split(',')
                    for module in modules:
                        module_name = module.strip().split(' as ')[0].split('.')[0]
                        if module_name in content or module_name in ['os', 'sys', 'typing']:
                            used_imports.append(import_line)
                            break
                elif import_line.strip().startswith('from '):
                    if ' import ' in import_line:
                        from_part = import_line.split(' import ')[0].strip()
                        import_part = import_line.split(' import ')[1].strip()

                        # Check if any imported name is used
# TODO: Consider breaking this long line (length: 107)
                        imported_names = [name.strip().split(' as ')[0] for name in import_part.split(',')]
# TODO: Consider breaking this long line (length: 124)
                        if any(name in content or name in ['Optional', 'List', 'Dict', 'Union'] for name in imported_names):
                            used_imports.append(import_line)
                else:
                    used_imports.append(import_line)

            # Write back if changes were made
            new_content = ''.join(used_imports + other_lines)
            if new_content != ''.join(lines):
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✓ Cleaned imports in {file_path}")

        except Exception as e:
            print(f"❌ Error processing imports in {file_path}: {e}")

def fix_line_length():
    """Add line length warnings where lines are too long"""
    python_files = list(Path('.').glob('**/*.py'))

    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            modified = False
            new_lines = []

            for i, line in enumerate(lines):
                if len(line.rstrip()) > 100:
                    # Don't modify, just add a comment if it's a URL or long string
                    if any(x in line for x in ['http://', 'https://', '"""', "'''"]):
                        new_lines.append(line)
                    else:
                        # Add a comment suggesting line break
                        if not line.strip().startswith('#'):
# TODO: Consider breaking this long line (length: 122)
                            new_lines.append(f"# TODO: Consider breaking this long line (length: {len(line.rstrip())})\n")
                            modified = True
                        new_lines.append(line)
                else:
                    new_lines.append(line)

            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"✓ Added line length warnings in {file_path}")

        except Exception as e:
            print(f"❌ Error processing line lengths in {file_path}: {e}")

def fix_exception_handling():
    """Improve exception handling patterns"""
    python_files = list(Path('.').glob('**/*.py'))

    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Replace bare except with more specific exceptions
            content = re.sub(
                r'except:\s*\n(\s+)pass',
                r'except Exception as e:\n\1# TODO: Handle specific exception types\n\1pass',
                content
            )

            # Add logging to try/except/pass patterns
            content = re.sub(
                r'except Exception:\s*\n(\s+)pass',
                r'except Exception as e:\n\1# TODO: Consider logging this exception\n\1pass',
                content
            )

            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Improved exception handling in {file_path}")

        except Exception as e:
            print(f"❌ Error processing exception handling in {file_path}: {e}")

def add_docstrings():
    """Add basic docstrings to functions missing them"""
    python_files = list(Path('.').glob('**/*.py'))

    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            new_lines = []
            i = 0
            modified = False

            while i < len(lines):
                line = lines[i]

                # Check for function definition
                if re.match(r'^\s*def\s+\w+\s*\(', line):
                    new_lines.append(line)
                    i += 1

                    # Check if next non-empty line is a docstring
                    next_line_idx = i
                    while next_line_idx < len(lines) and lines[next_line_idx].strip() == '':
                        new_lines.append(lines[next_line_idx])
                        next_line_idx += 1
                        i += 1

                    if next_line_idx < len(lines) and not lines[next_line_idx].strip().startswith('"""'):
                        # Add basic docstring
                        indent = ' ' * (len(line) - len(line.lstrip()))
                        func_name = re.search(r'def\s+(\w+)', line).group(1)
                        new_lines.append(f'{indent}    """TODO: Add description for {func_name}"""\n')
                        modified = True
                else:
                    new_lines.append(line)
                    i += 1

            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"✓ Added docstring placeholders in {file_path}")

        except Exception as e:
            print(f"❌ Error adding docstrings to {file_path}: {e}")

def create_code_quality_config():
    """Create code quality configuration files"""

    # Create pyproject.toml for black
    pyproject_toml = """[tool.black]
line-length = 100
target-version = ['py39']
include = '\\.pyi?$'
extend-exclude = '''
/(
  # directories
  \\.eggs
  | \\.git
  | \\.mypy_cache
  | \\.pytest_cache
  | \\.venv
  | build
  | dist
  | __pycache__
)/
'''

[tool.isort]
profile = "black"
line_length = 100
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

[tool.pylint.messages_control]
disable = [
    "C0114",  # missing-module-docstring
    "C0115",  # missing-class-docstring
    "C0116",  # missing-function-docstring
]

[tool.pylint.format]
max-line-length = 100
"""

    with open('pyproject.toml', 'w') as f:
        f.write(pyproject_toml)
    print("✓ Created pyproject.toml")

    # Create .flake8 config
    flake8_config = """[flake8]
max-line-length = 100
extend-ignore =
    E203,  # whitespace before ':'
    E501,  # line too long (handled by black)
    W503,  # line break before binary operator
exclude =
    .git,
    __pycache__,
    .pytest_cache,
    .mypy_cache,
    build,
    dist,
    *.egg-info
per-file-ignores =
    __init__.py:F401
"""

    with open('.flake8', 'w') as f:
        f.write(flake8_config)
    print("✓ Created .flake8")

def create_makefile():
    """Create Makefile for common development tasks"""
    makefile_content = """# Houdinis Framework Development Makefile

.PHONY: help install test lint format security clean

help:  ## Show this help message
	@echo "Available commands:"
# TODO: Consider breaking this long line (length: 143)
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \\033[36m%-15s\\033[0m %s\\n", $$1, $$2}'

install:  ## Install dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:  ## Run tests
	python -m pytest tests/ -v

lint:  ## Run linting tools
	flake8 .
	pylint core/ exploits/ quantum/ utils/

format:  ## Format code
	black .
	isort .

security:  ## Run security scans
	bandit -r . -f json -o bandit-report.json
	safety check

quality:  ## Run all quality checks
	make lint
	make security

fix:  ## Apply automated fixes
	python fix_security_issues.py
	python fix_code_quality.py

clean:  ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -f bandit-report.json safety-report.json
	rm -rf .pytest_cache .mypy_cache

setup-dev:  ## Setup development environment
	pip install black flake8 isort pylint bandit safety pytest
	pre-commit install

docs:  ## Generate documentation
	@echo "Documentation available in:"
	@echo "  - README.md"
	@echo "  - CODE_REVIEW_REPORT.md"
	@echo "  - SECURITY_IMPROVEMENTS.md"
"""

    with open('Makefile', 'w') as f:
        f.write(makefile_content)
    print("✓ Created Makefile")

def main():
    """Run all code quality improvements"""
    print("📈 Applying Code Quality Improvements for Houdinis Framework")
    print("=" * 60)

    try:
        print("\n1. Fixing whitespace issues...")
        fix_whitespace_issues()

        print("\n2. Cleaning up imports...")
        fix_import_issues()

        print("\n3. Adding line length warnings...")
        fix_line_length()

        print("\n4. Improving exception handling...")
        fix_exception_handling()

        print("\n5. Adding docstring placeholders...")
        add_docstrings()

        print("\n6. Creating configuration files...")
        create_code_quality_config()

        print("\n7. Creating development Makefile...")
        create_makefile()

        print("\n✅ Code quality improvements applied successfully!")
        print("\n📋 Next steps:")
        print("1. Run 'make setup-dev' to install development tools")
        print("2. Run 'make format' to apply black formatting")
        print("3. Run 'make lint' to check for remaining issues")
        print("4. Run 'make quality' for comprehensive quality check")
        print("5. Review TODO comments added to the code")

    except Exception as e:
        print(f"\n❌ Error applying code quality improvements: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()