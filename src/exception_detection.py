import pandas as pd


def classify_exceptions(df: pd.DataFrame) -> pd.DataFrame:
    """Classify records into Critical, Warning, or Normal management attention levels."""
    result = df.copy()
    result["Exception_Level"] = "Normal"
    result["Exception_Reason"] = ""

    critical_on_hold = result["Status"].eq("On Hold")
    critical_high_overdue = (
        result["Priority"].eq("High")
        & result["Days_Overdue"].gt(7)
        & result["Status"].ne("Completed")
    )
    critical_mask = critical_on_hold | critical_high_overdue

    result.loc[critical_on_hold, "Exception_Reason"] = "Activity is on hold"
    result.loc[critical_high_overdue, "Exception_Reason"] = "High-priority activity overdue by more than 7 days"
    result.loc[critical_mask, "Exception_Level"] = "Critical"

    warning_overdue = (
        result["Days_Overdue"].between(1, 7)
        & result["Status"].ne("Completed")
    )
    warning_stale = (
        result["Update_Age_Days"].gt(7)
        & result["Status"].ne("Completed")
    )
    warning_mask = (warning_overdue | warning_stale) & ~critical_mask

    result.loc[warning_overdue & ~critical_mask, "Exception_Reason"] = "Open activity overdue by 1–7 days"
    result.loc[warning_stale & ~critical_mask, "Exception_Reason"] = "Open activity has a stale update (>7 days)"
    result.loc[warning_mask, "Exception_Level"] = "Warning"

    return result
