from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.report import PowerReport, PowerStatus
from app.models.user import User
from app.repositories.location_repository import get_location
from app.repositories.report_repository import create_report, get_latest_report, get_reports_since
from app.repositories.status_repository import get_latest_official_update
from app.middleware.schemas.report import AreaStatus, ReportCreate


def submit_report(db: Session, current_user: User, payload: ReportCreate) -> PowerReport:
    if get_location(db, payload.location_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    report = PowerReport(
        user_id=current_user.id,
        location_id=payload.location_id,
        status=payload.status.value,
    )
    return create_report(db, report)


def get_area_status(db: Session, location_id: int) -> AreaStatus:
    if get_location(db, location_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    since = datetime.now(timezone.utc) - timedelta(hours=1)
    reports = get_reports_since(db, location_id, since)
    outage_count = sum(1 for report in reports if report.status == PowerStatus.OUTAGE.value)
    restored_count = sum(1 for report in reports if report.status == PowerStatus.RESTORED.value)
    latest_report = get_latest_report(db, location_id)
    official_update = get_latest_official_update(db, location_id)

    community_status = None
    if outage_count or restored_count:
        community_status = (
            PowerStatus.OUTAGE if outage_count >= restored_count else PowerStatus.RESTORED
        )

    return AreaStatus(
        location_id=location_id,
        community_status=community_status,
        official_status=PowerStatus(official_update.status) if official_update else None,
        estimated_restore_time=official_update.estimated_restore_time if official_update else None,
        outage_reports_last_hour=outage_count,
        restored_reports_last_hour=restored_count,
        last_reported_at=latest_report.timestamp if latest_report else None,
    )

