from datetime import datetime

from sqlalchemy.orm import Session
from typing_extensions import Type

from app.models.report import PowerReport


def create_report(db: Session, report: PowerReport) -> PowerReport:
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


def get_reports_since(db: Session, location_id: int, since: datetime) -> list[Type[PowerReport]]:
    return (
        db.query(PowerReport)
        .filter(PowerReport.location_id == location_id, PowerReport.timestamp >= since)
        .order_by(PowerReport.timestamp.desc())
        .all()
    )


def get_latest_report(db: Session, location_id: int) -> PowerReport | None:
    return (
        db.query(PowerReport)
        .filter(PowerReport.location_id == location_id)
        .order_by(PowerReport.timestamp.desc())
        .first()
    )

