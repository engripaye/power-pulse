from typing import List, Type

from sqlalchemy.orm import Session

from app.models.complaint import Complaint


def create_complaint(db: Session, complaint: Complaint) -> Complaint:
    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint


def list_complaints(db: Session, location_id: int | None = None) -> list[Type[Complaint]]:
    query = db.query(Complaint)
    if location_id is not None:
        query = query.filter(Complaint.location_id == location_id)
    return query.order_by(Complaint.created_at.desc()).all()


def get_complaint(db: Session, complaint_id: int) -> Complaint | None:
    return db.get(Complaint, complaint_id)

