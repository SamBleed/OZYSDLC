# OzySDLC

> Secure SDLC Pipeline - Scan your code for security vulnerabilities in seconds.

OzySDLC is a CLI tool that runs security scans on your project:
- **Secrets** - Detect API keys, tokens, passwords in your code
- **Dependencies** - Find vulnerable packages in your dependencies  
- **Code** - Static analysis for common security issues

## Quick Start

```bash
# Install
pip install ozy-sdlc

# Run scan
ozy run .
```

## Installation

### From PyPI (recommended)
```bash
pip install ozy-sdlc
```

### From source
```bash
git clone https://github.com/ozysdlc/ozysdlc.git
cd ozysdlc
pip install -e .
```

## Usage

```bash
# Scan current directory
ozy run .

# Scan specific path
ozy run /path/to/project

# Output JSON for CI/CD
ozy run . --json

# Save to file
ozy run . --output results.json

# Skip specific scanners
ozy run . --no-secrets --no-code
```

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | No vulnerabilities found (clean) |
| `1` | Vulnerabilities detected |
| `2` | Execution error (tool missing, invalid path, etc.) |

## Requirements

Install these tools for full functionality:

- [gitleaks](https://github.com/zricethezav/gitleaks) - Secrets detection
- [trivy](https://aquasecurity.github.io/trivy/) - Dependency scanning
- [semgrep](https://semgrep.dev/) - Static code analysis

> Note: OzySDLC works even if tools are missing (shows warnings)

## Options

```
--no-secrets     Skip secrets scanning
--no-deps       Skip dependency scanning
--no-code       Skip code analysis
-v, --verbose   Show detailed output
--json          Output JSON to stdout
--output FILE   Write output to file
```

## License

MIT
