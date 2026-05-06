from typing import Annotated, Type

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import require_company_admin
from app.db.session import get_db
from app.models.location import Location
from app.models.user import User
from app.repositories.location_repository import create_location, list_locations
from app.middleware.schemas import LocationCreate, LocationRead

router = APIRouter()


@router.get("", response_model=list[LocationRead])
def get_locations(db: Annotated[Session, Depends(get_db)]) -> list[Type[Location]]:
    return list_locations(db)


@router.post("", response_model=LocationRead, status_code=status.HTTP_201_CREATED)
def add_location(
        payload: LocationCreate,
        db: Annotated[Session, Depends(get_db)],
        _admin: Annotated[User, Depends(require_company_admin)],
) -> Location:
    return create_location(db, Location(**payload.model_dump()))

