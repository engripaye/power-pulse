from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.location import Location

SEED_LOCATIONS = [
    {"state": "Lagos", "city": "Ikeja", "area_name": "Allen Avenue"},
    {"state": "Lagos", "city": "Yaba", "area_name": "Sabo"},
    {"state": "Abuja", "city": "Garki", "area_name": "Area 10"},
]


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for location in SEED_LOCATIONS:
            exists = (
                db.query(Location)
                .filter(
                    Location.state == location["state"],
                    Location.city == location["city"],
                    Location.area_name == location["area_name"],
                    )
                .first()
            )
            if not exists:
                db.add(Location(**location))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    print("PowerPulse database initialized.")

