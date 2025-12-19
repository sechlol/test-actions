.PHONY: lint

# Run all lints and checks: ruff format and isort
lint:
	@echo "Running ruff format..."
	ruff format .
	@echo "Sorting imports with isort..."
	isort .
	@echo "✓ Linting complete!"

