from datetime import datetime

from pydantic import BaseModel, Field

from app.models.complaint import ComplaintStatus


class ComplaintCreate(BaseModel):
    location_id: int
    message: str = Field(min_length=5, max_length=2000)


class ComplaintRespond(BaseModel):
    status: ComplaintStatus
    response: str = Field(min_length=2, max_length=2000)


class ComplaintRead(BaseModel):
    id: int
    user_id: int
    location_id: int
    message: str
    status: ComplaintStatus
    response: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}

