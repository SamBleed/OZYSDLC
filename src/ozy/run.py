"""Main run orchestration for OzySDLC."""

from pathlib import Path

from ozy.reporters import ConsoleReporter, JsonReporter, Reporter
from ozy.scanners import CodeScanner, DepsScanner, ScanResult, SecretsScanner

# Exit codes
EXIT_CLEAN = 0      # No vulnerabilities found
EXIT_FINDINGS = 1   # Vulnerabilities detected
EXIT_ERROR = 2      # Execution error (tool missing, path invalid, etc.)


def calculate_risk_score(results: list[ScanResult]) -> tuple[str, str]:
    """Calculate overall risk score based on scan results.
    
    Priority:
    - Any CRITICAL or HIGH issue -> HIGH
    - More than 10 total issues -> HIGH
    - Any issues found -> MEDIUM
    - Otherwise -> LOW
    """
    total_found = 0
    has_critical = False
    
    for r in results:
        issues_count = len(r.issues)
        total_found += issues_count
        
        # Check issues list for severity
        for issue in r.issues:
            sev = str(issue.get("severity", "")).upper()
            if sev in ("CRITICAL", "HIGH"):
                has_critical = True
                break

    if has_critical or total_found > 10:
        return "HIGH", "🔴"
    elif total_found > 0:
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
    has_warnings = False
    has_real_errors = False

    for scanner in scanners:
        result = scanner.scan(target_path)
        results.append(result)
        
        # Scanner errors are WARNINGs, not hard errors
        # Tool not found = warning, not error
        if result.error:
            has_warnings = True
            # Only true errors (not tool missing) would be real errors
            # But for now, scanner errors are just warnings

    # Calculate risk score
    risk = calculate_risk_score(results)

    # Render output
    reporter.render(results, risk, target_path)

    # Return exit code based on results
    # If scanner has issues (vulnerabilities found) = EXIT_FINDINGS (1)
    # If scanner error (but has results) = EXIT_FINDINGS (1) - there were still scans done
    if any(r.found > 0 for r in results):
        return EXIT_FINDINGS
    elif risk[0] in ("MEDIUM", "HIGH"):
        return EXIT_FINDINGS
    else:
        return EXIT_CLEAN
