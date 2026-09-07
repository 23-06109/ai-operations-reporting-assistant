# Portfolio Case Study

## AI-Powered Operations Reporting Assistant

**Created by:** Jimmy Manalon  
**Positioning:** Reporting Automation → Operations Analytics → AI Automation

## Goal

Build a credible portfolio solution that reduces the manual work involved in
validating operational trackers, calculating KPIs, identifying exceptions, and
preparing a management briefing.

## Business Scenario

An operations team maintains a tracker containing planned and actual dates,
status, priority, progress, issue type, last update, team, and owner. Management
needs a repeatable weekly report that answers:

- What is the current delivery position?
- Which open activities are overdue or stale?
- Which records require immediate attention?
- Where are exceptions concentrated?
- What actions should management prioritize?

## Approach

1. Validate the expected columns, activity identifiers, dates, and progress.
2. Derive overdue days, update age, and completed schedule variance.
3. Calculate management KPIs with deterministic Python logic.
4. Classify activities using transparent Critical and Warning rules.
5. Export structured KPI, exception, and narrative-evidence files.
6. Include a separate saved Excel management workbook; the current entry point
   does not rebuild this file.
7. Add an optional AI narrative prompted with calculated evidence and review
   the generated text against the source figures.

## Exception Rules

**Critical**

- Activity is On Hold; or
- High-priority open activity is overdue by more than seven days.

**Warning**

- Open activity is overdue by one to seven days; or
- Open activity has not been updated for more than seven days.

Critical classifications take precedence over warnings. Every exception includes
a human-readable reason.

## Results

The pipeline analyzed 300 synthetic activities and produced:

- 175 completed activities and a 58.3% completion rate
- 77 overdue open activities
- 17 high-priority overdue activities
- 69 stale open updates
- 34 Critical and 48 Warning exceptions

The visual analysis found the highest exception volume in Construction (23).
It also found 23 exception records without a specific issue classification,
highlighting a data-quality gap that limits root-cause analysis.

## Management Recommendation

Prioritize the Critical exception register, assign follow-up actions for
high-priority overdue activities, refresh stale updates, and improve issue-type
completion so recurring operational causes can be analyzed reliably.

## Design Decisions

- Calculations remain deterministic and testable.
- AI is used for communication, not arithmetic.
- The fixed reporting snapshot makes results reproducible.
- Synthetic data protects employer and client confidentiality.
- Separate management, analyst, and action views support different users.

## Potential Client Adaptation

The same workflow can be adapted for project controls, procurement tracking,
document control, service operations, maintenance backlogs, sales operations,
and recurring client reporting. Client-specific thresholds, categories, and
templates would need to be adapted and tested for each implementation. The
current portfolio uses fixed rules and does not provide a configuration interface.
