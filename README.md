# OzySDLC

**Secure SDLC Pipeline — Scan your code for security vulnerabilities in seconds.**

OzySDLC is a CLI tool that runs automated security scans on your project:

* 🔐 **Secrets** — Detect API keys, tokens, passwords in your code
* 📦 **Dependencies** — Find vulnerable packages in your dependencies
* 🧪 **Code** — Static analysis for common security issues

> Fast, simple and practical DevSecOps scanning from your terminal.

---

## 🚀 Quick Start

```bash
pip install ozy-sdlc
ozy run .
```

---

## 📦 Installation

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

---

## ⚙️ Usage

```bash
# Scan current directory
ozy run .

# Scan specific path
ozy run /path/to/project

# Output JSON for CI/CD
ozy run . --json

# Save to file
ozy run . --output results.json

# Skip specific scanners (--no-code recommended for large projects)
ozy run . --no-secrets --no-deps --no-code
```

---

## ⚠️ Note on Semgrep

Semgrep can be slow on large projects (>30s). For faster scans, use:

```bash
ozy run . --no-code
```

---

## 📊 Example Output

```text
🚨 OZYSDLC REPORT

Secrets        ❌ 2
Dependencies   ⚠️ 5
Code Issues    ⚠️ 3

Risk Score: HIGH 🔴
```

---

## 🚦 Exit Codes

| Code | Meaning                                            |
| ---- | -------------------------------------------------- |
| 0    | No vulnerabilities found (clean)                   |
| 1    | Vulnerabilities detected                           |
| 2    | Execution error (tool missing, invalid path, etc.) |

---

## 🧰 Requirements

For full functionality, install:

* **gitleaks** — Secrets detection
* **trivy** — Dependency scanning
* **semgrep** — Static code analysis

> OzySDLC still runs if tools are missing (warnings will be shown)

---

## ⚙️ Options

```
--no-secrets     Skip secrets scanning
--no-deps        Skip dependency scanning
--no-code        Skip code analysis
-v, --verbose    Show detailed output
--json           Output JSON to stdout
--output FILE    Write output to file
```

---

## 🎯 Philosophy

> Verify every stage. Trust nothing by default.

---

## 📄 License

MIT
