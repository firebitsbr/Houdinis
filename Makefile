# Houdinis Framework Development Makefile

.PHONY: help install test lint format security clean

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

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
