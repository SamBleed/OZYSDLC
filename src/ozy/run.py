"""Main run orchestration for OzySDLC."""

from pathlib import Path

from ozy.reporters import ConsoleReporter, JsonReporter, Reporter
from ozy.scanners import CodeScanner, DepsScanner, ScanResult, SecretsScanner

# Exit codes
EXIT_CLEAN = 0      # No vulnerabilities found
EXIT_FINDINGS = 1   # Vulnerabilities detected
EXIT_ERROR = 2      # Execution error (tool missing, path invalid, etc.)


def calculate_risk_score(results: list[ScanResult]) -> tuple[str, str]:
    """Calculate overall risk score based on scan results."""
    total_issues = sum(r.found for r in results)
    has_secrets = any(r.scanner == "secrets" and r.found > 0 for r in results)
    
    # Check for critical/high from both issues and severity_counts
    has_critical = False
    for r in results:
        # Check severity_counts if available
        if r.severity_counts:
            if r.severity_counts.get("CRITICAL", 0) > 0 or r.severity_counts.get("HIGH", 0) > 0:
                has_critical = True
                break
        # Fallback to checking issues
        elif r.issues:
            if any(i.get("severity", "").upper() in ("CRITICAL", "HIGH") for i in r.issues):
                has_critical = True
                break

    if has_secrets or (has_critical and total_issues > 10):
        return "HIGH", "🔴"
    elif total_issues > 5:
        return "MEDIUM", "🟡"
    else:
        return "LOW", "🟢"


def run(
    path: str = ".",
    scan_secrets: bool = True,
    scan_deps: bool = True,
    scan_code: bool = True,
    verbose: bool = False,
    json_output: bool = False,
    output_file: Path | None = None,
) -> int:
    """Run security scans on the project.
    
    Returns:
        EXIT_CLEAN (0) if no vulnerabilities found
        EXIT_FINDINGS (1) if vulnerabilities detected
        EXIT_ERROR (2) if execution error
    """

    target_path = Path(path).resolve()
    if not target_path.exists():
        from rich.console import Console

        console = Console()
        console.print(f"[red]Error: Path '{path}' does not exist[/red]")
        return EXIT_ERROR

    # Create reporter based on flags
    if json_output or output_file:
        reporter: Reporter = JsonReporter(output_file)
    else:
        reporter = ConsoleReporter(verbose)

    # Run scanners
    scanners = []

    if scan_secrets:
        scanners.append(SecretsScanner())
    if scan_deps:
        scanners.append(DepsScanner())
    if scan_code:
        scanners.append(CodeScanner())

    if not scanners:
        from rich.console import Console

        console = Console()
        console.print("[yellow]No scanners enabled[/yellow]")
        return EXIT_ERROR

    results: list[ScanResult] = []
    has_errors = False

    for scanner in scanners:
        result = scanner.scan(target_path)
        results.append(result)
        # Check if scanner had a REAL error (not just tool missing)
        # Tool missing is a warning, not an error
        if result.error and "not found" not in result.error.lower():
            has_errors = True

    # Calculate risk score
    risk = calculate_risk_score(results)

    # Render output
    reporter.render(results, risk, target_path)

    # Return exit code based on results
    if has_errors:
        return EXIT_ERROR
    elif risk[0] in ("MEDIUM", "HIGH"):
        return EXIT_FINDINGS
    elif any(r.found > 0 for r in results):
        # Any vulnerabilities detected = EXIT_FINDINGS
        return EXIT_FINDINGS
    else:
        return EXIT_CLEAN
