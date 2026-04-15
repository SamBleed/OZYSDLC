"""CLI entry point for OzySDLC."""

import sys
from pathlib import Path

import click

from ozy import __version__
from ozy.run import EXIT_CLEAN, EXIT_ERROR, EXIT_FINDINGS, run


def check_installation():
    """Check if OzySDLC is properly installed."""
    try:
        import ozy
        return True
    except ImportError:
        return False


@click.group()
@click.version_option(version=__version__)
def main():
    """OzySDLC - Secure SDLC Pipeline"""
    pass


@main.command("run")
@click.argument("path", default=".")
@click.option("--no-secrets", is_flag=True, help="Skip secrets scanning")
@click.option("--no-deps", is_flag=True, help="Skip dependency scanning")
@click.option("--no-code", "skip_code", is_flag=True, help="Skip code analysis (semgrep can be slow on large projects)")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
@click.option("--json", "json_output", is_flag=True, help="Output JSON to stdout")
@click.option("--output", "output_file", type=click.Path(path_type=Path), help="Write output to file")
def run_cmd(path, no_secrets, no_deps, skip_code, verbose, json_output, output_file):
    """Run security scans on the project"""
    exit_code = run(
        path=path,
        scan_secrets=not no_secrets,
        scan_deps=not no_deps,
        scan_code=not skip_code,
        verbose=verbose,
        json_output=json_output,
        output_file=output_file,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
