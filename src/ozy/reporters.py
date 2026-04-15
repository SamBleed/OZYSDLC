"""Reporter implementations for OzySDLC."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel

from ozy.scanners import ScanResult


class ScanReport(BaseModel):
    """Unified report structure for scan results."""

    timestamp: str
    target: str
    scanners: list[ScanResult]
    risk_score: str


class Reporter(ABC):
    """Base class for output reporters."""

    @abstractmethod
    def render(
        self,
        results: list[ScanResult],
        risk: tuple[str, str],
        target: Path,
    ) -> None:
        """Render scan results in the appropriate format."""
        pass


class ConsoleReporter(Reporter):
    """Reporter that outputs to console using Rich."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def render(
        self,
        results: list[ScanResult],
        risk: tuple[str, str],
        target: Path,
    ) -> None:
        from rich.console import Console
        from rich.panel import Panel

        console = Console()

        # Header
        console.print("\n[bold cyan]🚨 OZYSDLC REPORT[/bold cyan]")
        console.print(f"[dim]Scanning: {target}[/dim]\n")

        # Results in aligned format
        for result in results:
            if result.error:
                status = "⚠️ "
                count = "Error"
                console.print(f"  {status} [bold]{result.scanner:14}[/bold] {count}")
            elif result.found > 0 or result.severity_counts:
                status = "❌ " if result.found > 0 else "✅ "
                counts = result.severity_counts or {}
                # Always show severity breakdown
                critical = counts.get("CRITICAL", 0)
                high = counts.get("HIGH", 0)
                medium = counts.get("MEDIUM", 0)
                count = f"🔴{critical} 🟠{high} 🟡{medium}"
                console.print(f"  {status} [bold]{result.scanner:14}[/bold] {count}")
            else:
                status = "✅ "
                count = "0"
                console.print(f"  {status} [bold]{result.scanner:14}[/bold] {count}")

        # Show detailed results if verbose
        if self.verbose:
            for result in results:
                if result.issues:
                    console.print(f"\n[bold]{result.scanner.upper()} ISSUES:[/bold]")
                    for issue in result.issues[:10]:
                        severity = issue.get("severity", "UNKNOWN")
                        severity_emoji = (
                            "🔴"
                            if severity.upper() in ("CRITICAL", "HIGH")
                            else "🟡"
                        )
                        title = issue.get("title", issue.get("id", "Unknown"))
                        console.print(f"  {severity_emoji} {title}")

        # Print risk score
        risk_level, risk_emoji = risk
        risk_color = {
            "LOW": "green",
            "MEDIUM": "yellow",
            "HIGH": "red",
        }.get(risk_level, "white")

        console.print()
        console.print(
            Panel(
                f"[bold]Risk Score: {risk_emoji} {risk_level}[/bold]",
                border_style=risk_color,
                expand=False,
            )
        )


class JsonReporter(Reporter):
    """Reporter that outputs JSON for CI/CD integration."""

    def __init__(self, output_file: Path | None = None):
        self.output_file = output_file

    def render(
        self,
        results: list[ScanResult],
        risk: tuple[str, str],
        target: Path,
    ) -> None:
        import json

        # Build report structure
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "target": str(target),
            "scanners": [
                {
                    "name": r.scanner,
                    "found": r.found,
                    "error": r.error,
                    "issues": r.issues,
                    "severity_counts": r.severity_counts or {},
                }
                for r in results
            ],
            "risk_score": risk[0],
        }

        json_output = json.dumps(report, indent=2)

        if self.output_file:
            self.output_file.write_text(json_output)
        else:
            print(json_output)
