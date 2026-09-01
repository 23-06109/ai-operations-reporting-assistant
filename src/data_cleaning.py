from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = [
    "Activity_ID",
    "Department",
    "Responsible_Team",
    "Activity_Type",
    "Planned_Start",
    "Planned_Finish",
    "Actual_Finish",
    "Status",
    "Priority",
    "Progress_Pct",
    "Issue_Type",
    "Last_Update_Date",
    "Owner",
]

DATE_COLUMNS = [
    "Planned_Start",
    "Planned_Finish",
    "Actual_Finish",
    "Last_Update_Date",
]


def load_and_clean_data(csv_path: str | Path, snapshot_date: str = "2026-09-01") -> pd.DataFrame:
    """Load the synthetic operations dataset, validate it, and create analytical fields."""
    df = pd.read_csv(csv_path)

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if df["Activity_ID"].duplicated().any():
        duplicates = df.loc[df["Activity_ID"].duplicated(), "Activity_ID"].tolist()
        raise ValueError(f"Duplicate Activity_ID values found: {duplicates[:10]}")

    for column in DATE_COLUMNS:
        df[column] = pd.to_datetime(df[column], errors="coerce")

    text_columns = [
        "Department",
        "Responsible_Team",
        "Activity_Type",
        "Status",
        "Priority",
        "Issue_Type",
        "Owner",
    ]
    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    df["Progress_Pct"] = pd.to_numeric(df["Progress_Pct"], errors="coerce")
    invalid_progress = df["Progress_Pct"].isna() | ~df["Progress_Pct"].between(0, 100)
    if invalid_progress.any():
        raise ValueError("Progress_Pct contains missing values or values outside 0–100.")

    snapshot = pd.Timestamp(snapshot_date)

    df["Days_Overdue"] = 0
    overdue_mask = (
        df["Status"].ne("Completed")
        & df["Planned_Finish"].notna()
        & df["Planned_Finish"].lt(snapshot)
    )
    df.loc[overdue_mask, "Days_Overdue"] = (
        snapshot - df.loc[overdue_mask, "Planned_Finish"]
    ).dt.days

    df["Update_Age_Days"] = (snapshot - df["Last_Update_Date"]).dt.days

    df["Schedule_Variance_Days"] = pd.NA
    completed_mask = (
        df["Status"].eq("Completed")
        & df["Actual_Finish"].notna()
        & df["Planned_Finish"].notna()
    )
    df.loc[completed_mask, "Schedule_Variance_Days"] = (
        df.loc[completed_mask, "Actual_Finish"]
        - df.loc[completed_mask, "Planned_Finish"]
    ).dt.days

    return df
