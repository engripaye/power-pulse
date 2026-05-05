from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.report import PowerReport
from app.models.user import User
from app.schemas.report import ReportCreate, ReportRead
from app.services.report_service import submit_report

router = APIRouter()


@router.post("", response_model=ReportRead, status_code=status.HTTP_201_CREATED)
def report_power_status(
        payload: ReportCreate,
        db: Annotated[Session, Depends(get_db)],
        current_user: Annotated[User, Depends(get_current_user)],
) -> PowerReport:
    return submit_report(db, current_user, payload)

