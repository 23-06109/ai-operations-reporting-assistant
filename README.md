# AI-Powered Operations Reporting Assistant

Python and Excel portfolio project by **Jimmy Manalon** demonstrating a reliable
operations-reporting workflow: validate source data, calculate KPIs, detect
management exceptions, produce an action-focused Excel report, and optionally
generate a grounded AI briefing.

![Management summary](screenshots/management-summary.png)

## Business Problem

Operations teams often spend hours consolidating trackers, checking overdue
work, finding stale updates, prioritizing risks, and drafting recurring
management summaries. This project converts that manual process into a
repeatable reporting pipeline built around a fully synthetic dataset.

## Solution

```text
Synthetic CSV
    → validation and cleaning
    → deterministic KPI calculations
    → Critical / Warning exception rules
    → management outputs and Excel report
    → optional grounded AI narrative
```

Python—not an AI model—calculates every KPI and exception. The optional model
receives only the verified evidence package and is instructed not to calculate
new metrics or invent causes, forecasts, owners, or deadlines.

## Verified Results

| KPI | Result |
|---|---:|
| Total activities | 300 |
| Completed activities | 175 |
| Completion rate | 58.3% |
| Average progress | 79.1% |
| Overdue open activities | 77 |
| High-priority overdue | 17 |
| Stale open updates | 69 |
| Critical exceptions | 34 |
| Warning exceptions | 48 |

The visual analysis also identifies **Construction** as the department with the
largest exception volume (23) and finds 23 exception records without a specific
issue classification—a data-quality and root-cause tracking gap.

![Exception concentration analysis](screenshots/exception-analysis.png)

## Excel Deliverable

The included [`operations_management_report.xlsx`](output/operations_management_report.xlsx)
contains four audience-focused sheets:

- **Summary:** management KPI cards and exception overview
- **Visual Analysis:** exception concentration by department and issue type
- **Activity Data:** all records with auditable formula-driven calculations
- **Exceptions:** prioritized Critical and Warning action register

## Project Structure

```text
ai-operations-reporting-assistant/
├── data/
│   └── operations_data.csv
├── docs/
│   ├── CASE_STUDY.md
│   └── INTERVIEW_GUIDE.md
├── output/
│   ├── management_briefing.md
│   └── operations_management_report.xlsx
├── screenshots/
├── src/
│   ├── ai_narrative.py
│   ├── data_cleaning.py
│   ├── exception_detection.py
│   ├── kpi_analysis.py
│   └── report_generator.py
├── tests/
│   └── test_phase1.py
├── .env.example
├── main.py
├── requirements.txt
└── README.md
```

## Run Locally

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

The default run requires no API key. It produces a deterministic management
briefing alongside the KPI and exception outputs.

## Enable the Optional AI Briefing

Configure the environment variables shown in `.env.example`:

```text
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-5.6-luna
```

Never place a real API key in the repository. When a key is present, the
pipeline uses the OpenAI Responses API; otherwise it safely uses the grounded
deterministic fallback.

## Run the Tests

```bash
python -m unittest discover -s tests -v
```

The six automated checks protect KPI totals, exception counts, overdue logic,
reason completeness, narrative evidence, and prompt grounding.

## Portfolio Value

This project demonstrates:

- Operations and KPI reporting knowledge
- Python and pandas data processing
- Transparent business-rule automation
- Excel management-report design
- Automated testing and data-quality controls
- Grounded AI integration with a safe fallback
- Translation of analysis into management action

See the [case study](docs/CASE_STUDY.md) for the business narrative and the
[interview guide](docs/INTERVIEW_GUIDE.md) for a concise demonstration script.

## Data Privacy

All records are synthetic and were created specifically for portfolio
demonstration. No confidential employer, client, or project data is included.
