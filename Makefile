MAIN=a-maze-ing.py

install:
	pip install -r config.txt
	pip install flake8
	pip install mypy

run:
	python $(MAIN)

debug:
	python -m pdb $(MAIN)

clean:
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +
	find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete

lint:
	flake8
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8
	mypy . --strict
