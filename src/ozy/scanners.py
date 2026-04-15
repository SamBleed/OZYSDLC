"""Scanner implementations for OzySDLC."""

import json
import shutil
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class ScanResult(BaseModel):
    """Result from a security scanner."""

    scanner: str
    found: int
    issues: list[dict[str, Any]] = []
    error: str | None = None
    severity_counts: dict[str, int] = {}


class Scanner(ABC):
    """Base class for security scanners."""

    name: str
    tool_name: str

    def is_available(self) -> bool:
        """Check if the scanning tool is installed."""
        return shutil.which(self.tool_name) is not None

    @abstractmethod
    def scan(self, path: Path) -> ScanResult:
        """Run the scanner and return results."""
        pass


class SecretsScanner(Scanner):
    """Scanner for secrets using gitleaks."""

    name = "secrets"
    tool_name = "gitleaks"

    def scan(self, path: Path) -> ScanResult:
        if not self.is_available():
            return ScanResult(
                scanner=self.name,
                found=0,
                error="gitleaks not found. Install: https://github.com/zricethezav/gitleaks",
            )

        try:
            result = subprocess.run(
                ["gitleaks", "detect", "-r", "json", "-f", "json", str(path)],
                capture_output=True,
                text=True,
                timeout=300,
            )

            issues = []
            found = 0

            if result.stdout.strip():
                try:
                    data = json.loads(result.stdout)
                    issues = data if isinstance(data, list) else [data]
                    found = len(issues)
                except json.JSONDecodeError:
                    pass

            return ScanResult(scanner=self.name, found=found, issues=issues)

        except subprocess.TimeoutExpired:
            return ScanResult(scanner=self.name, found=0, error="Timeout expired")
        except Exception as e:
            return ScanResult(scanner=self.name, found=0, error=str(e))


class DepsScanner(Scanner):
    """Scanner for dependencies using trivy."""

    name = "dependencies"
    tool_name = "trivy"

    def scan(self, path: Path) -> ScanResult:
        if not self.is_available():
            return ScanResult(
                scanner=self.name,
                found=0,
                error="trivy not found. Install: https://aquasecurity.github.io/trivy/",
            )

        try:
            result = subprocess.run(
                [
                    "trivy",
                    "fs",
                    "--format",
                    "json",
                    "--severity",
                    "MEDIUM,HIGH,CRITICAL",
                    str(path),
                ],
                capture_output=True,
                text=True,
                timeout=300,
            )

            issues = []
            found = 0
            severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0}

            if result.stdout.strip():
                try:
                    data = json.loads(result.stdout)
                    results = data.get("Results", [])
                    for r in results:
                        for vuln in r.get("Vulnerabilities", []):
                            sev = vuln.get("Severity", "UNKNOWN")
                            issues.append({
                                "id": vuln.get("VulnerabilityID"),
                                "severity": sev,
                                "title": vuln.get("Title", ""),
                                "package": vuln.get("PkgName"),
                            })
                            if sev in severity_counts:
                                severity_counts[sev] += 1
                    found = len(issues)
                except json.JSONDecodeError:
                    pass

            return ScanResult(
                scanner=self.name, 
                found=found, 
                issues=issues,
                severity_counts=severity_counts,
            )

        except subprocess.TimeoutExpired:
            return ScanResult(scanner=self.name, found=0, error="Timeout")
        except Exception as e:
            return ScanResult(scanner=self.name, found=0, error=f"Error: {str(e)}")


class CodeScanner(Scanner):
    """Scanner for code issues using semgrep."""

    name = "code"
    tool_name = "semgrep"

    def scan(self, path: Path) -> ScanResult:
        if not self.is_available():
            return ScanResult(
                scanner=self.name,
                found=0,
                error="semgrep not found. Install: https://semgrep.dev/",
            )

        try:
            result = subprocess.run(
                [
                    "semgrep",
                    "--config",
                    "auto",
                    "--json",
                    "--quiet",
                    "--max-memory",
                    "512",
                    str(path),
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )

            issues = []
            found = 0

            if result.stdout.strip():
                try:
                    data = json.loads(result.stdout)
                    results = data.get("results", [])
                    for r in results:
                        issues.append({
                            "id": r.get("check_id"),
                            "severity": r.get("extra", {}).get("severity"),
                            "title": r.get("extra", {}).get("message", ""),
                            "file": r.get("path"),
                        })
                    found = len(issues)
                except json.JSONDecodeError:
                    pass

            return ScanResult(scanner=self.name, found=found, issues=issues)

        except subprocess.TimeoutExpired:
            return ScanResult(scanner=self.name, found=0, error="Timeout expired")
        except Exception as e:
            return ScanResult(scanner=self.name, found=0, error=str(e))
