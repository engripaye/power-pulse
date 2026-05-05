from datetime import datetime

from pydantic import BaseModel, Field

from app.models.report import PowerStatus


class OfficialUpdateCreate(BaseModel):
    location_id: int
    status: PowerStatus
    estimated_restore_time: datetime | None = None
    message: str | None = Field(default=None, max_length=255)


class OfficialUpdateRead(BaseModel):
    id: int
    location_id: int
    status: PowerStatus
    estimated_restore_time: datetime | None = None
    message: str | None = None
    updated_by: int
    updated_at: datetime

    model_config = {"from_attributes": True}

