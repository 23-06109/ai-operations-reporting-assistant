from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd


DEFAULT_MODEL = "gpt-5.6-luna"


def build_narrative_evidence(df: pd.DataFrame, kpis: dict) -> dict:
    """Build a compact, verified evidence package for narrative generation."""
    exception_mask = df["Exception_Level"].isin(["Critical", "Warning"])
    exceptions = df.loc[exception_mask]

    department_counts = (
        exceptions.groupby("Department", dropna=False)
        .size()
        .sort_values(ascending=False)
        .astype(int)
        .to_dict()
    )
    normalized_issues = exceptions["Issue_Type"].fillna("Not Specified")
    issue_counts = (
        normalized_issues.groupby(normalized_issues)
        .size()
        .sort_values(ascending=False)
        .astype(int)
        .to_dict()
    )

    return {
        "reporting_snapshot": "2026-09-01",
        "kpis": kpis,
        "exception_counts": {
            "critical": int(df["Exception_Level"].eq("Critical").sum()),
            "warning": int(df["Exception_Level"].eq("Warning").sum()),
            "normal": int(df["Exception_Level"].eq("Normal").sum()),
        },
        "exceptions_by_department": department_counts,
        "exceptions_by_issue_type": issue_counts,
        "data_context": "Fully synthetic portfolio dataset; no employer or client data.",
    }


def build_grounded_prompt(evidence: dict) -> str:
    """Create a prompt that restricts the narrative to verified evidence."""
    return f"""Write a concise weekly operations management briefing using only the
verified evidence below.

Required structure:
1. Executive Summary — two sentences.
2. Priority Risks — three bullets.
3. Recommended Actions — three numbered actions.

Rules:
- Do not calculate new metrics.
- Do not invent causes, forecasts, owners, deadlines, or business context.
- Preserve every number exactly as supplied.
- Clearly describe missing issue classification as a data-quality gap, not a root cause.
- Keep the complete briefing below 220 words.

VERIFIED EVIDENCE
{json.dumps(evidence, indent=2, default=str)}
"""


def build_deterministic_briefing(evidence: dict) -> str:
    """Provide a useful briefing when no API key is configured."""
    kpis = evidence["kpis"]
    levels = evidence["exception_counts"]
    departments = evidence["exceptions_by_department"]
    issues = evidence["exceptions_by_issue_type"]
    top_department, top_department_count = next(iter(departments.items()))
    missing_issue_count = int(issues.get("Not Specified", 0))

    return f"""# Weekly Operations Management Briefing

_Deterministic fallback generated from verified analytics. Configure an OpenAI
API key to replace this version with an AI-assisted narrative._

## Executive Summary

The reporting snapshot contains {kpis['total_activities']} activities with a {kpis['completion_rate_pct']}% completion rate and {kpis['average_progress_pct']}% average progress. Management attention is required for {levels['critical']} Critical and {levels['warning']} Warning activities.

## Priority Risks

- {kpis['overdue_open_activities']} open activities are overdue, including {kpis['high_priority_overdue']} high-priority overdue items.
- {kpis['stale_open_updates']} open activities have updates older than seven days.
- {top_department} has the highest exception volume at {top_department_count}; {missing_issue_count} exception records have no specific issue classification.

## Recommended Actions

1. Review and assign follow-up actions for all Critical exceptions.
2. Prioritize high-priority overdue work and refresh stale activity updates.
3. Complete missing issue classifications to improve root-cause visibility.
"""


def generate_management_briefing(
    df: pd.DataFrame,
    kpis: dict,
    output_dir: str | Path,
    use_ai: bool | None = None,
) -> tuple[str, str]:
    """Save evidence and generate either an AI-assisted or fallback briefing."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    evidence = build_narrative_evidence(df, kpis)

    with (output_dir / "narrative_evidence.json").open("w", encoding="utf-8") as file:
        json.dump(evidence, file, indent=2, default=str)

    should_use_ai = bool(os.getenv("OPENAI_API_KEY")) if use_ai is None else use_ai
    mode = "deterministic_fallback"

    if should_use_ai:
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY is required when use_ai=True.")
        from openai import OpenAI

        client = OpenAI()
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", DEFAULT_MODEL),
            instructions=(
                "You are an operations reporting assistant. Use only supplied "
                "verified evidence and never invent or recalculate facts."
            ),
            input=build_grounded_prompt(evidence),
            max_output_tokens=600,
        )
        briefing = response.output_text.strip()
        mode = "ai_assisted"
    else:
        briefing = build_deterministic_briefing(evidence).strip()

    briefing_path = output_dir / "management_briefing.md"
    briefing_path.write_text(briefing + "\n", encoding="utf-8")
    return briefing, mode
