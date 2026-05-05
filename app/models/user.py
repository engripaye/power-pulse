from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.constants import USER_ROLE
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(40), default=USER_ROLE)
    location_id: Mapped[int | None] = mapped_column(ForeignKey("locations.id"))

    location = relationship("Location", back_populates="users")
    reports = relationship("PowerReport", back_populates="user")
    complaints = relationship("Complaint", back_populates="user")

