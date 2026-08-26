from datetime import date

from src.analysis import (
    flag_attention_needed,
    latest_status_report,
    open_risks_by_project,
    overdue_milestones,
    portfolio_dashboard,
    risk_severity_score,
)
from src.data_sources import (
    MILESTONES,
    PROJECTS,
    RISK_LOG,
    STATUS_REPORTS,
    Milestone,
    RiskLogEntry,
    StatusReport,
)


def test_overdue_milestones_catches_known_overdue_row():
    result = overdue_milestones(MILESTONES, as_of=date(2026, 6, 20))
    ids = [m.milestone_id for m in result]
    assert "M10" in ids  # P04's final QA sign-off, due 2026-05-31, not completed


def test_overdue_milestones_excludes_completed():
    milestones = [
        Milestone("X1", "P99", "done on time", date(2026, 1, 1), date(2026, 1, 1)),
    ]
    assert overdue_milestones(milestones, as_of=date(2026, 6, 1)) == []


def test_overdue_milestones_excludes_future_due_dates():
    milestones = [
        Milestone("X2", "P99", "not due yet", date(2026, 12, 1), None),
    ]
    assert overdue_milestones(milestones, as_of=date(2026, 6, 1)) == []


def test_overdue_milestones_completed_late_is_not_overdue():
    # Completed, even if completed after the due date, should not count
    # as currently overdue -- it's done.
    milestones = [
        Milestone("X3", "P99", "late but done", date(2026, 1, 1), date(2026, 2, 1)),
    ]
    assert overdue_milestones(milestones, as_of=date(2026, 6, 1)) == []


def test_risk_severity_score_high_high_is_nine():
    risk = RiskLogEntry("Z1", "P99", "desc", "high", "high", "open", "owner")
    assert risk_severity_score(risk) == 9


def test_risk_severity_score_low_low_is_one():
    risk = RiskLogEntry("Z2", "P99", "desc", "low", "low", "open", "owner")
    assert risk_severity_score(risk) == 1


def test_open_risks_by_project_excludes_mitigated_and_closed():
    risks = [
        RiskLogEntry("Z3", "P99", "open one", "high", "high", "open", "owner"),
        RiskLogEntry("Z4", "P99", "mitigated one", "high", "high", "mitigated", "owner"),
        RiskLogEntry("Z5", "P99", "closed one", "high", "high", "closed", "owner"),
    ]
    result = open_risks_by_project(risks, "P99")
    assert [r.risk_id for r in result] == ["Z3"]


def test_open_risks_by_project_sorted_highest_severity_first():
    risks = [
        RiskLogEntry("Z6", "P99", "low sev", "low", "low", "open", "owner"),
        RiskLogEntry("Z7", "P99", "high sev", "high", "high", "open", "owner"),
        RiskLogEntry("Z8", "P99", "medium sev", "medium", "medium", "open", "owner"),
    ]
    result = open_risks_by_project(risks, "P99")
    assert [r.risk_id for r in result] == ["Z7", "Z8", "Z6"]


def test_open_risks_by_project_filters_to_correct_project():
    risks = [
        RiskLogEntry("Z9", "P01", "belongs to P01", "high", "high", "open", "owner"),
        RiskLogEntry("Z10", "P02", "belongs to P02", "high", "high", "open", "owner"),
    ]
    result = open_risks_by_project(risks, "P01")
    assert [r.risk_id for r in result] == ["Z9"]


def test_latest_status_report_returns_most_recent():
    reports = [
        StatusReport("SA", "P99", date(2026, 1, 1), "old", 10.0),
        StatusReport("SB", "P99", date(2026, 5, 1), "newest", 50.0),
        StatusReport("SC", "P99", date(2026, 3, 1), "middle", 30.0),
    ]
    result = latest_status_report(reports, "P99")
    assert result.report_id == "SB"


def test_latest_status_report_returns_none_when_no_reports_exist():
    assert latest_status_report(STATUS_REPORTS, "P_NONEXISTENT") is None


def test_portfolio_dashboard_has_one_row_per_project():
    dashboard = portfolio_dashboard(PROJECTS, MILESTONES, RISK_LOG, STATUS_REPORTS, date(2026, 6, 20))
    assert len(dashboard) == len(PROJECTS)
    assert {row["project_id"] for row in dashboard} == {p.project_id for p in PROJECTS}


def test_portfolio_dashboard_p04_shows_overdue_and_delayed():
    dashboard = portfolio_dashboard(PROJECTS, MILESTONES, RISK_LOG, STATUS_REPORTS, date(2026, 6, 20))
    p04 = next(row for row in dashboard if row["project_id"] == "P04")
    assert p04["overdue_milestone_count"] == 1
    assert p04["status"] == "delayed"


def test_portfolio_dashboard_p05_completed_has_no_open_risks():
    dashboard = portfolio_dashboard(PROJECTS, MILESTONES, RISK_LOG, STATUS_REPORTS, date(2026, 6, 20))
    p05 = next(row for row in dashboard if row["project_id"] == "P05")
    assert p05["open_risk_count"] == 0
    assert p05["percent_complete"] == 100.0


def test_flag_attention_needed_includes_at_risk_and_delayed():
    dashboard = portfolio_dashboard(PROJECTS, MILESTONES, RISK_LOG, STATUS_REPORTS, date(2026, 6, 20))
    flagged_ids = {row["project_id"] for row in flag_attention_needed(dashboard)}
    assert "P02" in flagged_ids  # at_risk
    assert "P04" in flagged_ids  # delayed + overdue milestone


def test_flag_attention_needed_excludes_healthy_completed_project():
    dashboard = portfolio_dashboard(PROJECTS, MILESTONES, RISK_LOG, STATUS_REPORTS, date(2026, 6, 20))
    flagged_ids = {row["project_id"] for row in flag_attention_needed(dashboard)}
    assert "P05" not in flagged_ids
