from pydantic import BaseModel, EmailStr, Field

from app.core.constants import USER_ROLE


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    location_id: int | None = None
    role: str = USER_ROLE


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    location_id: int | None = None

    model_config = {"from_attributes": True}

