from __future__ import annotations

import sqlite3
import tempfile
import unittest
from pathlib import Path

from src import run_checks


class RunChecksTest(unittest.TestCase):
    def test_synthetic_fixture_returns_expected_findings(self) -> None:
        with sqlite3.connect(":memory:") as connection:
            connection.row_factory = sqlite3.Row
            run_checks.initialize_database(connection)
            findings = run_checks.run_checks(connection, run_checks.PROJECT_ROOT / "checks")

        identifiers = {(finding.finding_id, finding.entity_id) for finding in findings}
        self.assertEqual(len(findings), 8)
        self.assertIn(("ACTIVE_USER_WITHOUT_ORDERS", "2"), identifiers)
        self.assertIn(("ACTIVE_USER_WITHOUT_ORDERS", "4"), identifiers)
        self.assertIn(("DUPLICATE_EMAIL", "ana@example.test"), identifiers)
        self.assertIn(("INVALID_ORDER_VALUE", "102"), identifiers)
        self.assertIn(("INVALID_ORDER_VALUE", "103"), identifiers)
        self.assertIn(("PAID_ORDER_WITHOUT_PAYMENT_DATE", "103"), identifiers)
        self.assertIn(("ORDER_WITH_UNKNOWN_USER", "104"), identifiers)
        self.assertIn(("OUT_OF_STOCK_PRODUCT_FOR_SALE", "202"), identifiers)

    def test_csv_and_html_reports_are_written(self) -> None:
        finding = run_checks.Finding(
            finding_id="EXAMPLE",
            severity="low",
            entity_type="example",
            entity_id="1",
            rule="Example rule",
            details="Example details",
            check_file="example.sql",
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            reports_directory = Path(temporary_directory)
            run_checks.write_csv([finding], reports_directory / "quality-report.csv")
            run_checks.write_html([finding], reports_directory / "quality-report.html")
            self.assertIn("EXAMPLE", (reports_directory / "quality-report.csv").read_text(encoding="utf-8"))
            self.assertIn("Example rule", (reports_directory / "quality-report.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
