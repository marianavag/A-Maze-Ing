MAIN=a-maze-ing.py

install:
	python3 -m pip install flake8 mypy

run:
	python $(MAIN) config.txt

debug:
	python -m pdb $(MAIN) config.txt

clean:
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +
	find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete

lint:
	flake8
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8
	mypy . --strict

.PHONY: install run debug clean lint lint-strict