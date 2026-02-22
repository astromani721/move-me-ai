.PHONY: help install install-dev lint fix format typecheck test check

help:
	@echo "Targets:"
	@echo "  install      Install runtime dependencies"
	@echo "  install-dev  Install runtime + dev dependencies"
	@echo "  lint         Run Ruff lint checks"
	@echo "  fix          Auto-fix Ruff lint issues where possible"
	@echo "  format       Run Ruff formatter"
	@echo "  typecheck    Run mypy on src/"
	@echo "  test         Run pytest"
	@echo "  check        Run lint + typecheck + test"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

lint:
	ruff check .

fix:
	ruff check --fix .

format:
	ruff format .

typecheck:
	mypy src

test:
	pytest

check: lint typecheck test
