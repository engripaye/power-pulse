from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.power_status import OfficialUpdate
from app.models.user import User
from app.repositories.location_repository import get_location
from app.repositories.status_repository import create_official_update
from app.middleware.schemas import OfficialUpdateCreate


def post_official_update(
        db: Session,
        current_user: User,
        payload: OfficialUpdateCreate,
) -> OfficialUpdate:
    if get_location(db, payload.location_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")

    update = OfficialUpdate(
        location_id=payload.location_id,
        status=payload.status.value,
        estimated_restore_time=payload.estimated_restore_time,
        message=payload.message,
        updated_by=current_user.id,
    )
    return create_official_update(db, update)

