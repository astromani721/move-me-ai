.PHONY: help install install-dev lint fix format typecheck test check run ping-model

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
	@echo "  run          Run relocation planner (PROMPT= required)"
	@echo "  ping-model   Send a test prompt to the HuggingFace model"

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

PROMPT ?= Relocating to 10583. Find 3-bedroom rentals, check schools, estimate insurance, and find nearest Indian grocery.

run:
	PYTHONPATH=src python -m cli "$(PROMPT)"

ping-model:
	PYTHONPATH=src python -c "from model import get_model; m = get_model(); print(m([{'role':'user','content':'Say hello in one sentence.'}]))"
