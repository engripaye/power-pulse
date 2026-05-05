from typing import Annotated, List, Type

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_company_admin
from app.db.session import get_db
from app.models.complaint import Complaint
from app.models.user import User
from app.repositories.complaint_repository import list_complaints
from app.schemas.complaint import ComplaintCreate, ComplaintRead, ComplaintRespond
from app.services.complaint_service import respond_to_complaint, submit_complaint

router = APIRouter()


@router.post("", response_model=ComplaintRead, status_code=status.HTTP_201_CREATED)
def create_complaint(
        payload: ComplaintCreate,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
) -> Complaint:
    return submit_complaint(db, current_user, payload)


@router.get("", response_model=list[ComplaintRead])
def get_complaints(
        db: Annotated[Session, Depends(get_db)],
        _admin: Annotated[User, Depends(require_company_admin)],
        location_id: int | None = Query(default=None),
) -> list[Type[Complaint]]:
    return list_complaints(db, location_id=location_id)


@router.patch("/{complaint_id}", response_model=ComplaintRead)
def respond(
        complaint_id: int,
        payload: ComplaintRespond,
        db: Annotated[Session, Depends(get_db)],
        _admin: Annotated[User, Depends(require_company_admin)],
) -> Complaint:
    return respond_to_complaint(db, complaint_id, payload)

