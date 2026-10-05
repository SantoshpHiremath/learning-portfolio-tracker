# Learning Portfolio Tracker

A tested Python project that tracks a portfolio of digital and immersive learning projects: milestones, a risk log, status reports, and a combined portfolio dashboard that flags which projects need management attention. It supports planning, scheduling, and reporting, maintains project plans, status reports, risk logs, and dashboards, and flags what needs attention.

## What it does

- **`src/data_sources.py`**: the projects, milestones, risk log, and status reports, including one deliberately overdue, uncompleted milestone and a mix of open, mitigated, and closed risks, so the analysis logic has real conditions to detect.
- **`src/analysis.py`**: overdue-milestone detection, risk severity scoring (likelihood × impact) and open-risk filtering/sorting, latest-status-report lookup, a combined per-project portfolio dashboard row, and attention-flagging logic (overdue milestone, high-severity open risk, or an already at-risk/delayed status).
- **`src/report.py`**: renders the portfolio dashboard, risk log, and status reports as a 3-sheet `.xlsx` workbook via openpyxl, with header styling and attention-flagged rows highlighted. The output is an actual Excel file a stakeholder can open directly, not a printed table.
- **`run_pipeline.py`**: runs the full flow end to end and prints a console report (see sample output below, copied from an actual run).

## Data

The project, milestone, risk, and status-report data is synthetic. `src/data_sources.py` contains 5 fictional digital and immersive learning projects (an AR onboarding module, a VR safety training simulation, an AI tutoring chatbot pilot, an immersive product training library, and a micro-learning content refresh). The tracker covers the data handling and reporting logic of portfolio management (milestone and risk computation and the dashboard view); the pipeline is built so real project data can replace the fictional set.

The risk-severity scoring (likelihood × impact, 1-9) is a simple, transparent model chosen for clarity.

## Results

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

P04 is flagged for its overdue "Final QA sign-off" milestone despite having zero open risks (its one risk was already mitigated), which shows the dashboard combines multiple signals rather than just echoing project status back.

## Tests

25 automated tests (`tests/`), all passing. The milestone/risk/status data model is simple and was written test-first alongside the analysis functions.

## Project structure

```
src/
  data_sources.py
  analysis.py
  report.py
tests/
  test_data_sources.py
  test_analysis.py
  test_report.py
run_pipeline.py
Learning_Portfolio_Dashboard.xlsx   generated workbook
```

## Running it

```bash
python3 -m pytest -v      # 25 tests, all passing
python3 run_pipeline.py   # runs the full pipeline end to end, writes Learning_Portfolio_Dashboard.xlsx
```

## Notes

The tracker focuses on portfolio data logic and reporting. Coordination work such as stakeholder negotiation and workshops happens outside the tool; the workbook is the artifact those conversations can use.

## Possible extensions

- Load projects and milestones from a real source (Excel, a project-management tool export).
- Add a PowerPoint status-report export alongside the Excel workbook.
- Trend the dashboard across several reporting dates.
