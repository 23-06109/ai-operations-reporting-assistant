from pathlib import Path
import json
import pandas as pd


def save_outputs(df: pd.DataFrame, kpis: dict, output_dir: str | Path) -> None:
    """Save deterministic KPI and exception outputs for management review."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with (output_dir / "kpi_summary.json").open("w", encoding="utf-8") as file:
        json.dump(kpis, file, indent=2)

    exception_columns = [
        "Activity_ID",
        "Department",
        "Responsible_Team",
        "Activity_Type",
        "Status",
        "Priority",
        "Progress_Pct",
        "Planned_Finish",
        "Days_Overdue",
        "Last_Update_Date",
        "Update_Age_Days",
        "Issue_Type",
        "Owner",
        "Exception_Level",
        "Exception_Reason",
    ]

    exceptions = df.loc[
        df["Exception_Level"].isin(["Critical", "Warning"]),
        exception_columns,
    ].sort_values(
        by=["Exception_Level", "Days_Overdue", "Priority"],
        ascending=[True, False, True],
    )

    exceptions.to_csv(output_dir / "management_exceptions.csv", index=False)
