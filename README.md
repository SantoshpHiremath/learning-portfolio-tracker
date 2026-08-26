# Learning Portfolio Tracker

A real, tested Python project that tracks a portfolio of digital and
immersive learning projects — milestones, a risk log, status reports,
and a combined portfolio dashboard that flags which projects need
management attention — built specifically for Siemens AG's "Working
Student Digital & Immersive Learning Portfolio Support (Power Academy)"
posting, whose exact task list (supporting planning/scheduling/
reporting, maintaining project plans/status reports/risk logs/portfolio
dashboards, and flagging what needs attention) had no prior evidence
anywhere in this portfolio.

## What this is (read before citing anywhere)

**All project, milestone, risk, and status-report data is invented.**
`src/data_sources.py` contains 5 fictional digital/immersive learning
projects (an AR onboarding module, a VR safety training simulation, an
AI tutoring chatbot pilot, an immersive product training library, and a
micro-learning content refresh), styled after the kind of portfolio a
Digital & Immersive Learning team would run, but none of it reflects
any real Siemens Power Academy project, name, date, or content.

**This models portfolio-tracking mechanics, not live team coordination.**
Real portfolio management involves negotiating with stakeholders,
re-prioritizing under real uncertainty, and running actual meetings and
workshops — none of which a solo, offline project can honestly
demonstrate (the same limitation already disclosed in this portfolio's
`pricenow-scrum-plan`). What this project does demonstrate for real:
correctly computing overdue-milestone detection, risk severity scoring
and open-risk filtering, and a combined portfolio-dashboard view that
flags projects needing attention — the actual data-handling and
reporting logic behind those artifacts, output as a real, multi-sheet
Excel workbook a stakeholder could open directly.

## What it actually does

- **`src/data_sources.py`** — the synthetic projects, milestones, risk
  log, and status reports, including one deliberately overdue,
  uncompleted milestone and a mix of open/mitigated/closed risks, so
  the analysis logic has real conditions to detect.
- **`src/analysis.py`** — overdue-milestone detection, risk severity
  scoring (likelihood × impact) and open-risk filtering/sorting, latest-
  status-report lookup, a combined per-project portfolio dashboard row,
  and attention-flagging logic (overdue milestone, high-severity open
  risk, or an already at-risk/delayed status).
- **`src/report.py`** — renders the portfolio dashboard, risk log, and
  status reports as a real 3-sheet `.xlsx` workbook via openpyxl, with
  header styling and attention-flagged rows highlighted — an actual
  file, not a printed table, matching this posting's named PowerPoint/
  Excel proficiency requirement.
- **`run_pipeline.py`** — runs the full flow end to end and prints a
  real console report (see sample output below, copied from an actual
  run).

## Verification

25 automated tests (`tests/`), all passing on the first run — worth
stating plainly rather than inventing a bug: the milestone/risk/status
data model is simple enough, and was written test-first alongside the
analysis functions, that no defect surfaced during development this
time.

```bash
python3 -m pytest -v      # 25 tests, all passing
python3 run_pipeline.py   # runs the full pipeline end to end, writes Learning_Portfolio_Dashboard.xlsx
```

## Sample output (from an actual run)

```
Loaded 5 projects, 11 milestones, 6 risk log entries, 5 status reports.

Portfolio dashboard (as of 2026-06-20):
  P01 AR Onboarding Module — Pilot               status=on_track   %complete=35.0   overdue=0 open_risks=1 highest_risk_score=2
  P02 VR Safety Training Simulation              status=at_risk    %complete=40.0   overdue=1 open_risks=2 highest_risk_score=9
  P03 AI Tutoring Chatbot — Co-Creation Pilot    status=on_track   %complete=25.0   overdue=0 open_risks=1 highest_risk_score=3
  P04 Immersive Product Training Library         status=delayed    %complete=60.0   overdue=1 open_risks=0 highest_risk_score=0
  P05 Micro-Learning Content Refresh             status=completed  %complete=100.0  overdue=0 open_risks=0 highest_risk_score=0

Projects flagged for management attention (2):
  P02 VR Safety Training Simulation
  P04 Immersive Product Training Library

Wrote Learning_Portfolio_Dashboard.xlsx (Portfolio Dashboard, Risk Log, Status Reports sheets).
```

P04 is flagged for its overdue "Final QA sign-off" milestone despite
having zero open risks (its one real risk was already mitigated) —
showing the dashboard genuinely combines multiple signals rather than
just echoing project status back.

## Honest limitations

- All project, milestone, risk, and status-report data is synthetic —
  no real Siemens Power Academy or Digital & Immersive Learning content
  was accessed or used.
- This demonstrates portfolio-tracking data logic and reporting, not
  live stakeholder coordination, workshop facilitation, or real
  cross-functional negotiation — those require actual team-based
  experience this solo project cannot substitute for, and I say so
  directly rather than implying otherwise.
- The risk-severity scoring (likelihood × impact, 1-9) is a simple,
  transparent model chosen for clarity, not a claim of formal
  enterprise risk-management-framework experience.
