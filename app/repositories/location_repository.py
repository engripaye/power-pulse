from typing import List, Type

from sqlalchemy.orm import Session

from app.models.location import Location


def get_location(db: Session, location_id: int) -> Location | None:
    return db.get(Location, location_id)


def list_locations(db: Session) -> list[Type[Location]]:
    return db.query(Location).order_by(Location.state, Location.city, Location.area_name).all()


def create_location(db: Session, location: Location) -> Location:
    db.add(location)
    db.commit()
    db.refresh(location)
    return location

