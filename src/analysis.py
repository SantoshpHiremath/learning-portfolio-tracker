"""
Portfolio-level analysis: overdue milestones, open-risk summaries by
severity, and a per-project rollup combining status, milestone
progress, and open risk count -- the "portfolio dashboard" view the
posting names directly.
"""

from __future__ import annotations

from datetime import date

from src.data_sources import Milestone, Project, RiskLogEntry, StatusReport

_LIKELIHOOD_IMPACT_SCORE = {"low": 1, "medium": 2, "high": 3}


def overdue_milestones(milestones: list[Milestone], as_of: date) -> list[Milestone]:
    """Milestones whose due date has passed and which have not been
    completed. Explicit as_of parameter (not date.today()) so this is
    deterministic and testable."""
    return [
        m for m in milestones
        if m.completed_date is None and m.due_date < as_of
    ]


def risk_severity_score(risk: RiskLogEntry) -> int:
    """Simple likelihood x impact score (1-9), used to rank risks by
    severity for the portfolio dashboard's risk summary."""
    return _LIKELIHOOD_IMPACT_SCORE[risk.likelihood] * _LIKELIHOOD_IMPACT_SCORE[risk.impact]


def open_risks_by_project(risks: list[RiskLogEntry], project_id: str) -> list[RiskLogEntry]:
    """Open (not mitigated or closed) risks for a given project, sorted
    highest-severity first."""
    open_for_project = [
        r for r in risks if r.project_id == project_id and r.status == "open"
    ]
    return sorted(open_for_project, key=risk_severity_score, reverse=True)


def latest_status_report(reports: list[StatusReport], project_id: str) -> StatusReport | None:
    """Most recent status report for a project, or None if there isn't
    one yet."""
    project_reports = [r for r in reports if r.project_id == project_id]
    if not project_reports:
        return None
    return max(project_reports, key=lambda r: r.report_date)


def portfolio_dashboard(
    projects: list[Project],
    milestones: list[Milestone],
    risks: list[RiskLogEntry],
    reports: list[StatusReport],
    as_of: date,
) -> list[dict]:
    """One row per project: status, latest reported percent-complete,
    count of overdue milestones, count of open risks, and highest open-
    risk severity score -- the combined view a portfolio dashboard
    needs to flag which projects need attention at a glance."""
    rows = []
    for project in projects:
        project_milestones = [m for m in milestones if m.project_id == project.project_id]
        overdue = overdue_milestones(project_milestones, as_of)
        open_risks = open_risks_by_project(risks, project.project_id)
        latest_report = latest_status_report(reports, project.project_id)
        rows.append({
            "project_id": project.project_id,
            "name": project.name,
            "status": project.status,
            "percent_complete": latest_report.percent_complete if latest_report else None,
            "overdue_milestone_count": len(overdue),
            "open_risk_count": len(open_risks),
            "highest_open_risk_score": risk_severity_score(open_risks[0]) if open_risks else 0,
        })
    return rows


def flag_attention_needed(dashboard_rows: list[dict]) -> list[dict]:
    """Projects worth flagging for management attention: any overdue
    milestone, OR a high-severity open risk (score >= 6), OR a status
    already marked at_risk/delayed. This mirrors the kind of triage
    logic a portfolio owner applies when deciding what to raise in a
    status meeting."""
    return [
        row for row in dashboard_rows
        if row["overdue_milestone_count"] > 0
        or row["highest_open_risk_score"] >= 6
        or row["status"] in ("at_risk", "delayed")
    ]
