import unittest
from pathlib import Path

from src.data_cleaning import load_and_clean_data
from src.exception_detection import classify_exceptions
from src.kpi_analysis import calculate_kpis
from src.ai_narrative import (
    build_deterministic_briefing,
    build_grounded_prompt,
    build_narrative_evidence,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "operations_data.csv"
SNAPSHOT_DATE = "2026-09-01"


class Phase1PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cleaned = load_and_clean_data(DATA_PATH, snapshot_date=SNAPSHOT_DATE)
        cls.kpis = calculate_kpis(cls.cleaned)
        cls.analyzed = classify_exceptions(cls.cleaned)

    def test_expected_dataset_and_kpis(self) -> None:
        expected = {
            "total_activities": 300,
            "completed_activities": 175,
            "completion_rate_pct": 58.3,
            "overdue_open_activities": 77,
            "high_priority_overdue": 17,
            "average_progress_pct": 79.1,
            "stale_open_updates": 69,
            "average_completed_variance_days": 4.2,
        }
        self.assertEqual(self.kpis, expected)

    def test_expected_exception_counts(self) -> None:
        counts = self.analyzed["Exception_Level"].value_counts().to_dict()
        self.assertEqual(counts.get("Critical"), 34)
        self.assertEqual(counts.get("Warning"), 48)
        self.assertEqual(counts.get("Normal"), 218)

    def test_completed_activities_are_not_overdue(self) -> None:
        completed = self.cleaned["Status"].eq("Completed")
        self.assertTrue(self.cleaned.loc[completed, "Days_Overdue"].eq(0).all())

    def test_every_exception_has_a_reason(self) -> None:
        exceptions = self.analyzed["Exception_Level"].isin(["Critical", "Warning"])
        self.assertTrue(self.analyzed.loc[exceptions, "Exception_Reason"].ne("").all())

    def test_narrative_evidence_matches_verified_results(self) -> None:
        evidence = build_narrative_evidence(self.analyzed, self.kpis)
        self.assertEqual(evidence["exception_counts"]["critical"], 34)
        self.assertEqual(evidence["exception_counts"]["warning"], 48)
        self.assertEqual(evidence["exceptions_by_department"]["Construction"], 23)
        self.assertEqual(evidence["exceptions_by_issue_type"]["Not Specified"], 23)

    def test_prompt_and_fallback_are_grounded(self) -> None:
        evidence = build_narrative_evidence(self.analyzed, self.kpis)
        prompt = build_grounded_prompt(evidence)
        briefing = build_deterministic_briefing(evidence)
        self.assertIn("Do not calculate new metrics", prompt)
        self.assertIn("34 Critical", briefing)
        self.assertIn("48 Warning", briefing)


if __name__ == "__main__":
    unittest.main()
