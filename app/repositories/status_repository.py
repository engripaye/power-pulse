from sqlalchemy.orm import Session

from app.models.power_status import OfficialUpdate


def create_official_update(db: Session, update: OfficialUpdate) -> OfficialUpdate:
    db.add(update)
    db.commit()
    db.refresh(update)
    return update


def get_latest_official_update(db: Session, location_id: int) -> OfficialUpdate | None:
    return (
        db.query(OfficialUpdate)
        .filter(OfficialUpdate.location_id == location_id)
        .order_by(OfficialUpdate.updated_at.desc())
        .first()
    )

