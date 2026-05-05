from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Location(Base):
    __tablename__ = "locations"
    __table_args__ = (UniqueConstraint("state", "city", "area_name", name="uq_location_area"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    state: Mapped[str] = mapped_column(String(80), index=True)
    city: Mapped[str] = mapped_column(String(80), index=True)
    area_name: Mapped[str] = mapped_column(String(120), index=True)

    users = relationship("User", back_populates="location")
    reports = relationship("PowerReport", back_populates="location")
    complaints = relationship("Complaint", back_populates="location")
    official_updates = relationship("OfficialUpdate", back_populates="location")

