.PHONY: help install install-dev lint fix format typecheck test check search

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
	@echo "  search       Search for housing (ZIP= BED= BATH= RENT= LIMIT=)"

install:
	pip install -e . -r requirements.txt

install-dev:
	pip install -e . -r requirements-dev.txt

lint:
	ruff check .

fix:
	ruff check --fix .

format:
	ruff format .

typecheck:
	mypy --explicit-package-bases src

test:
	pytest

check: lint typecheck test

ZIP  ?= 10583
BED  ?= 3
BATH ?= 1
RENT ?=
LIMIT ?= 5

search:
	PYTHONPATH=src python -m cli --zip $(ZIP) --bedrooms $(BED) --bathrooms $(BATH) --limit $(LIMIT) $(if $(RENT),--max-rent $(RENT),)
