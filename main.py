from pathlib import Path

from src.ai_narrative import generate_management_briefing
from src.data_cleaning import load_and_clean_data
from src.exception_detection import classify_exceptions
from src.kpi_analysis import calculate_kpis
from src.report_generator import save_outputs


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "operations_data.csv"
OUTPUT_DIR = PROJECT_ROOT / "output"


def main() -> None:
    df = load_and_clean_data(DATA_PATH, snapshot_date="2026-09-01")
    kpis = calculate_kpis(df)
    analyzed_df = classify_exceptions(df)
    save_outputs(analyzed_df, kpis, OUTPUT_DIR)
    _, narrative_mode = generate_management_briefing(analyzed_df, kpis, OUTPUT_DIR)

    print("AI-Powered Operations Reporting Assistant - Deterministic Analytics")
    print("-" * 70)
    for name, value in kpis.items():
        print(f"{name}: {value}")

    critical = int(analyzed_df["Exception_Level"].eq("Critical").sum())
    warning = int(analyzed_df["Exception_Level"].eq("Warning").sum())
    print(f"critical_exceptions: {critical}")
    print(f"warning_exceptions: {warning}")
    print(f"management_briefing: {narrative_mode}")
    print(f"Outputs saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
