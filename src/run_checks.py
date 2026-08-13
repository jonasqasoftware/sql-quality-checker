#!/usr/bin/env python3
"""Run deterministic SQL data-quality checks against a synthetic SQLite store."""

from __future__ import annotations

import argparse
import csv
import html
import sqlite3
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUIRED_COLUMNS = {
    "finding_id",
    "severity",
    "entity_type",
    "entity_id",
    "rule",
    "details",
}


@dataclass(frozen=True)
class Finding:
    finding_id: str
    severity: str
    entity_type: str
    entity_id: str
    rule: str
    details: str
    check_file: str


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run SQL business-rule checks and generate CSV and HTML reports."
    )
    parser.add_argument(
        "--database",
        default=":memory:",
        help="SQLite database path. The synthetic schema and seed are loaded on each run.",
    )
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=PROJECT_ROOT / "reports",
        help="Directory for quality-report.csv and quality-report.html.",
    )
    parser.add_argument(
        "--fail-on-findings",
        action="store_true",
        help="Exit with code 1 when at least one inconsistency is found.",
    )
    return parser.parse_args()


def load_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def initialize_database(connection: sqlite3.Connection) -> None:
    connection.executescript(load_sql(PROJECT_ROOT / "database" / "schema.sql"))
    connection.executescript(load_sql(PROJECT_ROOT / "database" / "seed.sql"))


def run_checks(connection: sqlite3.Connection, checks_directory: Path) -> list[Finding]:
    findings: list[Finding] = []
    for check_path in sorted(checks_directory.glob("*.sql")):
        cursor = connection.execute(load_sql(check_path))
        columns = {description[0] for description in cursor.description or []}
        missing_columns = REQUIRED_COLUMNS - columns
        if missing_columns:
            names = ", ".join(sorted(missing_columns))
            raise ValueError(f"{check_path.name} is missing required column(s): {names}")
        for row in cursor.fetchall():
            record = dict(row)
            findings.append(
                Finding(
                    finding_id=str(record["finding_id"]),
                    severity=str(record["severity"]),
                    entity_type=str(record["entity_type"]),
                    entity_id=str(record["entity_id"]),
                    rule=str(record["rule"]),
                    details=str(record["details"]),
                    check_file=check_path.name,
                )
            )
    return sorted(findings, key=lambda item: (severity_rank(item.severity), item.finding_id, item.entity_id))


def severity_rank(severity: str) -> int:
    return {"critical": 0, "high": 1, "medium": 2, "low": 3}.get(severity.lower(), 4)


def write_csv(findings: Iterable[Finding], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    field_names = list(Finding.__dataclass_fields__)
    with output_path.open("w", encoding="utf-8", newline="") as report:
        writer = csv.DictWriter(report, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(asdict(finding) for finding in findings)


def write_html(findings: list[Finding], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary = Counter(finding.severity.lower() for finding in findings)
    rows = "\n".join(
        "<tr>"
        f"<td>{html.escape(finding.finding_id)}</td>"
        f"<td><span class=\"severity {html.escape(finding.severity.lower())}\">{html.escape(finding.severity)}</span></td>"
        f"<td>{html.escape(finding.entity_type)}</td>"
        f"<td>{html.escape(finding.entity_id)}</td>"
        f"<td>{html.escape(finding.rule)}</td>"
        f"<td>{html.escape(finding.details)}</td>"
        f"<td>{html.escape(finding.check_file)}</td>"
        "</tr>"
        for finding in findings
    ) or "<tr><td colspan=\"7\">No inconsistencies found.</td></tr>"
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    output_path.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>SQL Quality Checker report</title>
  <style>
    body {{ font-family: system-ui, sans-serif; color: #24292f; margin: 2rem; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #d0d7de; padding: .5rem; text-align: left; vertical-align: top; }}
    th {{ background: #f6f8fa; }}
    .severity {{ border-radius: 999px; color: white; font-weight: 600; padding: .15rem .5rem; }}
    .critical {{ background: #82071e; }} .high {{ background: #cf222e; }}
    .medium {{ background: #9a6700; }} .low {{ background: #1a7f37; }}
  </style>
</head>
<body>
  <h1>SQL Quality Checker report</h1>
  <p>Generated from synthetic laboratory data at {generated_at}. This report identifies declared rule violations; it is not production evidence.</p>
  <p><strong>{len(findings)}</strong> finding(s): critical={summary['critical']}, high={summary['high']}, medium={summary['medium']}, low={summary['low']}.</p>
  <table>
    <thead><tr><th>Finding</th><th>Severity</th><th>Entity</th><th>ID</th><th>Rule</th><th>Details</th><th>Check</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</body>
</html>
""",
        encoding="utf-8",
    )


def main() -> int:
    arguments = parse_arguments()
    database_path = arguments.database
    if database_path != ":memory:":
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        initialize_database(connection)
        findings = run_checks(connection, PROJECT_ROOT / "checks")

    write_csv(findings, arguments.reports_dir / "quality-report.csv")
    write_html(findings, arguments.reports_dir / "quality-report.html")
    counts = Counter(finding.severity.lower() for finding in findings)
    print(
        f"SQL Quality Checker: {len(findings)} finding(s) "
        f"(critical={counts['critical']}, high={counts['high']}, medium={counts['medium']}, low={counts['low']})."
    )
    print(f"Reports: {arguments.reports_dir.resolve()}")
    return 1 if findings and arguments.fail_on_findings else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, sqlite3.Error, ValueError) as error:
        print(f"sql-quality-checker: {error}", file=sys.stderr)
        raise SystemExit(2) from error
