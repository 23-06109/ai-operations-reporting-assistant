import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calculate deterministic management KPIs from the cleaned dataset."""
    total = len(df)
    completed = int(df["Status"].eq("Completed").sum())
    open_mask = df["Status"].ne("Completed")
    overdue_mask = open_mask & df["Days_Overdue"].gt(0)
    stale_mask = open_mask & df["Update_Age_Days"].gt(7)
    high_priority_overdue = overdue_mask & df["Priority"].eq("High")

    completed_variance = pd.to_numeric(
        df.loc[df["Status"].eq("Completed"), "Schedule_Variance_Days"],
        errors="coerce",
    )

    return {
        "total_activities": total,
        "completed_activities": completed,
        "completion_rate_pct": round((completed / total) * 100, 1) if total else 0.0,
        "overdue_open_activities": int(overdue_mask.sum()),
        "high_priority_overdue": int(high_priority_overdue.sum()),
        "average_progress_pct": round(float(df["Progress_Pct"].mean()), 1) if total else 0.0,
        "stale_open_updates": int(stale_mask.sum()),
        "average_completed_variance_days": round(float(completed_variance.mean()), 1)
        if completed_variance.notna().any()
        else 0.0,
    }
