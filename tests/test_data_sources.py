from src.data_sources import MILESTONES, PROJECTS, RISK_LOG, STATUS_REPORTS


def test_projects_have_unique_ids():
    ids = [p.project_id for p in PROJECTS]
    assert len(ids) == len(set(ids))


def test_milestones_reference_known_projects():
    project_ids = {p.project_id for p in PROJECTS}
    for m in MILESTONES:
        assert m.project_id in project_ids


def test_risk_log_references_known_projects():
    project_ids = {p.project_id for p in PROJECTS}
    for r in RISK_LOG:
        assert r.project_id in project_ids


def test_status_reports_reference_known_projects():
    project_ids = {p.project_id for p in PROJECTS}
    for r in STATUS_REPORTS:
        assert r.project_id in project_ids


def test_at_least_one_open_and_one_closed_risk_exist():
    statuses = {r.status for r in RISK_LOG}
    assert "open" in statuses
    assert "closed" in statuses or "mitigated" in statuses
