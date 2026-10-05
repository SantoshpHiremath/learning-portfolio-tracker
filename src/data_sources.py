"""
Synthetic data for a fictional digital/immersive learning portfolio --
several concurrent pilot projects (an AR onboarding module, a VR safety
training simulation, an AI-tutoring chatbot pilot, and so on), each with
milestones, a risk log, and periodic status reports. Modeled on the
kind of portfolio a Digital & Immersive Learning team would track.
All project names, dates, and content are invented.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Project:
    project_id: str
    name: str
    sponsor_team: str
    start_date: date
    target_end_date: date
    status: str  # "on_track", "at_risk", "delayed", "completed"


@dataclass(frozen=True)
class Milestone:
    milestone_id: str
    project_id: str
    name: str
    due_date: date
    completed_date: date | None  # None if not yet completed


@dataclass(frozen=True)
class RiskLogEntry:
    risk_id: str
    project_id: str
    description: str
    likelihood: str  # "low", "medium", "high"
    impact: str  # "low", "medium", "high"
    status: str  # "open", "mitigated", "closed"
    owner: str


@dataclass(frozen=True)
class StatusReport:
    report_id: str
    project_id: str
    report_date: date
    summary: str
    percent_complete: float  # 0.0-100.0


PROJECTS: list[Project] = [
    Project("P01", "AR Onboarding Module — Pilot", "Field Service Training", date(2026, 3, 1), date(2026, 9, 30), "on_track"),
    Project("P02", "VR Safety Training Simulation", "EHS Learning", date(2026, 2, 15), date(2026, 8, 15), "at_risk"),
    Project("P03", "AI Tutoring Chatbot — Co-Creation Pilot", "Learning Academy Digital", date(2026, 5, 1), date(2026, 11, 30), "on_track"),
    Project("P04", "Immersive Product Training Library", "Product Learning Solutions", date(2026, 1, 10), date(2026, 6, 30), "delayed"),
    Project("P05", "Micro-Learning Content Refresh", "Learning Academy Digital", date(2026, 4, 1), date(2026, 7, 15), "completed"),
]

MILESTONES: list[Milestone] = [
    Milestone("M01", "P01", "Storyboard & content approval", date(2026, 4, 15), date(2026, 4, 12)),
    Milestone("M02", "P01", "AR prototype build", date(2026, 6, 30), None),
    Milestone("M03", "P01", "Pilot user testing", date(2026, 8, 31), None),
    Milestone("M04", "P02", "VR scenario scripting", date(2026, 3, 31), date(2026, 4, 20)),
    Milestone("M05", "P02", "Hardware procurement", date(2026, 5, 1), None),
    Milestone("M06", "P02", "Pilot rollout to 2 sites", date(2026, 7, 15), None),
    Milestone("M07", "P03", "Stakeholder co-creation workshop", date(2026, 6, 1), date(2026, 6, 3)),
    Milestone("M08", "P03", "Chatbot MVP", date(2026, 9, 15), None),
    Milestone("M09", "P04", "Content migration", date(2026, 3, 15), date(2026, 4, 30)),
    # Deliberately overdue and still not completed -- exercises the
    # "overdue milestone" detection in analysis.py.
    Milestone("M10", "P04", "Final QA sign-off", date(2026, 5, 31), None),
    Milestone("M11", "P05", "Content refresh rollout", date(2026, 7, 10), date(2026, 7, 9)),
]

RISK_LOG: list[RiskLogEntry] = [
    RiskLogEntry("R01", "P02", "VR headset procurement delayed by vendor lead time", "high", "high", "open", "S. Hiremath"),
    RiskLogEntry("R02", "P02", "Two pilot sites have limited WiFi bandwidth for streaming content", "medium", "medium", "open", "S. Hiremath"),
    RiskLogEntry("R03", "P04", "Legacy content format incompatible with new player, requires manual conversion", "high", "medium", "mitigated", "S. Hiremath"),
    RiskLogEntry("R04", "P01", "AR prototype dependent on a third-party SDK update timeline", "medium", "low", "open", "S. Hiremath"),
    RiskLogEntry("R05", "P03", "Chatbot pilot requires legal review of training-data sourcing", "low", "high", "open", "S. Hiremath"),
    # Closed risk -- exercises filtering to open-only risk views.
    RiskLogEntry("R06", "P05", "Content refresh timeline overlapped with a public holiday week", "low", "low", "closed", "S. Hiremath"),
]

STATUS_REPORTS: list[StatusReport] = [
    StatusReport("SR01", "P01", date(2026, 6, 1), "Storyboard approved on schedule. AR prototype build underway.", 35.0),
    StatusReport("SR02", "P02", date(2026, 6, 1), "Scripting complete but hardware procurement is delayed; flagged as at-risk.", 40.0),
    StatusReport("SR03", "P03", date(2026, 6, 15), "Co-creation workshop completed with strong stakeholder engagement.", 25.0),
    StatusReport("SR04", "P04", date(2026, 5, 1), "Content migration behind schedule due to format-conversion effort.", 60.0),
    StatusReport("SR05", "P05", date(2026, 7, 10), "Rollout completed on schedule, no open issues.", 100.0),
]
