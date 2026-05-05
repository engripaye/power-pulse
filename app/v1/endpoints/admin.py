from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_company_admin
from app.db.session import get_db
from app.models.power_status import OfficialUpdate
from app.models.user import User
from app.repositories.complaint_repository import list_complaints
from app.schemas.complaint import ComplaintRead
from app.schemas.power_status import OfficialUpdateCreate, OfficialUpdateRead
from app.schemas.report import AreaStatus
from app.services.report_service import get_area_status
from app.services.status_service import post_official_update

router = APIRouter()


@router.post("/updates", response_model=OfficialUpdateRead, status_code=status.HTTP_201_CREATED)
def create_official_update(
        payload: OfficialUpdateCreate,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(require_company_admin)],
) -> OfficialUpdate:
    return post_official_update(db, current_user, payload)


@router.get("/dashboard", response_model=AreaStatus)
def dashboard(
        location_id: int,
        db: Annotated[Session, Depends(get_db)],
        _admin: Annotated[User, Depends(require_company_admin)],
) -> AreaStatus:
    return get_area_status(db, location_id)


@router.get("/complaints", response_model=list[ComplaintRead])
def admin_complaints(
        db: Annotated[Session, Depends(get_db)],
        _admin: Annotated[User, Depends(require_company_admin)],
        location_id: int | None = Query(default=None),
) -> list:
    return list_complaints(db, location_id=location_id)

