---
description: "Project standards for Python monorepo with Poetry - includes code style, project structure, and dependency management guidelines"
alwaysApply: true
---

# Project Standards

## Documentation
- NEVER proactively create README.md files or other documentation unless explicitly requested by the user
- Only create documentation when the user specifically asks for it

## Code Style
- Follow PEP 8 for Python code
- Use type hints for all function signatures
- Prefer explicit over implicit

## Project Structure
- This is a Python monorepo with Poetry
- common_lib contains shared code (schemas, config, utilities)
- Applications live in applications/ directory
- Environment files (.env) at repository root are for shared configuration
- Applications can declare their own .env files for app-specific configuration
- Never commit .env files with secrets

## Dependencies
- Use Poetry for dependency management
- When adding dependencies, use `poetry add` commands
- Shared dependencies go in common_lib
- App-specific dependencies in respective app directories

