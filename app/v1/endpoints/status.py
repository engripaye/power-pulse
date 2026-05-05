from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.report import AreaStatus
from app.services.report_service import get_area_status

router = APIRouter()


@router.get("/{location_id}", response_model=AreaStatus)
def area_status(location_id: int, db: Annotated[Session, Depends(get_db)]) -> AreaStatus:
    return get_area_status(db, location_id)

