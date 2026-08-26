"""
Runs the full learning-portfolio-tracker pipeline end to end: loads the
synthetic project/milestone/risk/status data, computes the portfolio
dashboard, flags projects needing attention, and writes a real .xlsx
workbook. Prints a real console report.
"""

from datetime import date

from src.analysis import flag_attention_needed, portfolio_dashboard
from src.data_sources import MILESTONES, PROJECTS, RISK_LOG, STATUS_REPORTS
from src.report import save_workbook

AS_OF = date(2026, 6, 20)


def main():
    print(f"Loaded {len(PROJECTS)} projects, {len(MILESTONES)} milestones, "
          f"{len(RISK_LOG)} risk log entries, {len(STATUS_REPORTS)} status reports.\n")

    dashboard = portfolio_dashboard(PROJECTS, MILESTONES, RISK_LOG, STATUS_REPORTS, AS_OF)
    print(f"Portfolio dashboard (as of {AS_OF.isoformat()}):")
    for row in dashboard:
        print(f"  {row['project_id']} {row['name']:42s} status={row['status']:10s} "
              f"%complete={str(row['percent_complete']):6s} overdue={row['overdue_milestone_count']} "
              f"open_risks={row['open_risk_count']} highest_risk_score={row['highest_open_risk_score']}")

    attention = flag_attention_needed(dashboard)
    print(f"\nProjects flagged for management attention ({len(attention)}):")
    for row in attention:
        print(f"  {row['project_id']} {row['name']}")

    save_workbook("Learning_Portfolio_Dashboard.xlsx", AS_OF)
    print("\nWrote Learning_Portfolio_Dashboard.xlsx (Portfolio Dashboard, Risk Log, Status Reports sheets).")


if __name__ == "__main__":
    main()
