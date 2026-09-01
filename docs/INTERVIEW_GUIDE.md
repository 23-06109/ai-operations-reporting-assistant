# Interview and Demo Guide

## 60-Second Project Explanation

> I built an operations reporting assistant that takes a synthetic activity
> tracker, validates the data, calculates management KPIs, detects overdue and
> stale work, and classifies exceptions as Critical or Warning. It then produces
> structured outputs and a management-ready Excel report with a summary,
> concentration analysis, full audit data, and a prioritized action register.
> I kept all calculations deterministic and tested. The AI layer is optional and
> only converts verified evidence into a concise briefing; it does not calculate
> or invent business facts.

## Five-Minute Demonstration

1. Open the **Summary** sheet and explain the headline KPIs.
2. Open **Visual Analysis** and identify exception concentration and missing
   issue classification.
3. Open **Exceptions** and filter Critical, High-priority, or departmental work.
4. Open **Activity Data** and trace one classification back to its formulas.
5. Show `management_briefing.md` and explain the grounded AI/fallback design.
6. Run the automated tests to demonstrate reliability.

## Architecture Explanation

```text
main.py coordinates the workflow
    → data_cleaning.py validates and derives analytical fields
    → kpi_analysis.py calculates management metrics
    → exception_detection.py applies transparent business rules
    → report_generator.py exports deterministic files
    → ai_narrative.py creates grounded evidence and narrative
```

## Strong Design Decisions to Discuss

### Why not let AI calculate the KPIs?

Operational metrics must be reproducible and auditable. Python calculates the
facts; the model only helps communicate them.

### Why use a fixed reporting date?

It keeps portfolio results reproducible. In a client implementation, the date
could be supplied as a runtime parameter or scheduled-report date.

### Why separate Critical and Warning rules?

Managers need a consistent priority order. Critical rules take precedence so an
urgent activity cannot be downgraded by a later warning rule.

### How did you test the solution?

Automated tests verify the approved KPI values, classification totals, overdue
behavior, exception reasons, narrative evidence, and grounding instructions.

### What would you improve next?

- Make reporting date and thresholds configurable.
- Preserve multiple exception reasons when several rules apply.
- Generate the Excel workbook directly during every pipeline run.
- Add scheduled delivery through email, Teams, SharePoint, or another client tool.
- Add historical snapshots for trends without changing the verified KPI logic.

## Client-Facing Positioning

> I can adapt this workflow to an existing Excel or CSV tracker, define the KPI
> and escalation rules with the client, automate the recurring report, and add a
> grounded management summary while keeping calculations transparent.
