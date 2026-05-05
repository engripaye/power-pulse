from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.user import User
from app.repositories.complaint_repository import create_complaint, get_complaint
from app.repositories.location_repository import get_location
from app.schemas.complaint import ComplaintCreate, ComplaintRespond


def submit_complaint(db: Session, current_user: User, payload: ComplaintCreate) -> Complaint:
    if get_location(db, payload.location_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    complaint = Complaint(
        user_id=current_user.id,
        location_id=payload.location_id,
        message=payload.message,
    )
    return create_complaint(db, complaint)


def respond_to_complaint(db: Session, complaint_id: int, payload: ComplaintRespond) -> Complaint:
    complaint = get_complaint(db, complaint_id)
    if complaint is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")

    complaint.status = payload.status.value
    complaint.response = payload.response
    db.commit()
    db.refresh(complaint)
    return complaint

