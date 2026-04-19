# OzySDLC

[![Status](https://img.shields.io/badge/status-Alpha-yellow)](https://github.com/SamBleed/OZYSDLC)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/ozy-sdlc)](https://pypi.org/project/ozy-sdlc/)

**Secure SDLC Pipeline — Scan your code for security vulnerabilities in seconds.**

> Fast, simple and practical DevSecOps scanning from your terminal.

---

## 📋 Índice
- [¿Qué hace?](#-qué-hace)
- [Inicio rápido](#-inicio-rápido)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estado del proyecto](#-estado-del-proyecto)
- [Contribuir](#-contribuir)
- [Licencia](#-licencia)

---

## 🔐 ¿Qué hace?

OzySDLC runs automated security scans on your project:

* 🔐 **Secrets** — Detect API keys, tokens, passwords
* 📦 **Dependencies** — Find vulnerable packages
* 🧪 **Code** — Static analysis for common security issues 

---

## 🚀 Inicio rápido

```bash
pip install ozy-sdlc
ozy run .
```

---

## 📦 Instalación

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

### Arch Linux

```bash
# Using pipx (recommended)
pipx install ozy-sdlc

# Or with aur (if available)
yay -S python-ozysdlc
```

### Troubleshooting

**Error: "externally-managed-environment"**

```bash
# Use pipx (recommended)
pipx install ozy-sdlc

# Or create a virtual environment
python -m venv venv
source venv/bin/activate
pip install ozy-sdlc
```

---

## ⚙️ Uso

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

Semgrep can be slow on large projects (>30s).

For faster scans:

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

| Code | Meaning                          |
| ---- | -------------------------------- |
| 0    | No vulnerabilities found (clean) |
| 1    | Vulnerabilities detected         |
| 2    | Execution error                  |

---

## 🧰 Requirements

For full functionality:

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

## 📊 Estado del proyecto

Este proyecto está en estado **Alpha**.  Las funcionalidades principales están implementadas, pero pueden haber cambios importantes en futuras versiones. No se recomienda para producción.

---

## 🤝 Contribuir

¡Bienvenido/a a contribuir! Por favor, sigue estos pasos:
1. Haz un *fork* del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`).
3. Haz tus cambios y *commits* (`git commit -am 'Añade nueva funcionalidad'`).
4. Haz *push* a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un *Pull Request*.

---

## 📄 Licencia

MIT

