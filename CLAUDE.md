# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python project for deploying GDPR compliance-related GenAI agents to AWS. It uses Poetry for dependency management and follows a modular architecture with separate packages for deployment, utilities, and no-code development assets.

## Development Commands

### Testing
```bash
# Run all tests
pytest tests/

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/

# Run tests with coverage
pytest --cov=genai_agent_gdpr_compliance tests/
```

### Dependency Management
```bash
# Install dependencies using Poetry
poetry install

# Add a new dependency
poetry add <package-name>

# Update dependencies
poetry update
```

### Git Workflow
```bash
# Merge dev into main (use the provided script)
./gh-release-to-main.sh
```

## Architecture

### Key Components

1. **AWS Deployment Module** (`genai_agent_gdpr_compliance/deploy/`)
   - `AWS__Setup__GDPR_Compliance`: Manages AWS infrastructure setup including S3 bucket creation and configuration
   - `AWS__Deploy__GDPR_Compliance`: Handles deployment of no-code development files to S3

2. **No-Code Development Assets** (`genai_agent_gdpr_compliance/no-code-dev/`)
   - Contains HTML files and other assets that are deployed to S3
   - Organized by date (year/month/day structure)

3. **Utilities** (`genai_agent_gdpr_compliance/utils/`)
   - Version management utilities

### AWS Integration

The project integrates with AWS services, primarily S3, and requires the following environment variables:
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`
- `AWS_ACCOUNT_ID`
- `AWS_ACCESS_KEY_ID`

S3 bucket naming convention: `{project-name}--{account-id}--{region}`

### CI/CD Pipeline

- **Dev branch**: Runs tests and increments minor version on push
- **Main branch**: Runs tests, increments major version, and publishes to PyPI
- Uses GitHub Actions with custom actions from `owasp-sbot/OSBot-GitHub-Actions`

### Important Conventions

- Uses Type-Safe patterns with `osbot_utils.type_safe.Type_Safe` base class
- Employs caching decorators (`@cache_on_self`) for AWS service clients
- Files use Safe String patterns for path handling (`Safe_Str__File__Path`)