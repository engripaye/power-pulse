from datetime import datetime

from pydantic import BaseModel

from app.models.report import PowerStatus


class ReportCreate(BaseModel):
    location_id: int
    status: PowerStatus


class ReportRead(BaseModel):
    id: int
    user_id: int
    location_id: int
    status: PowerStatus
    timestamp: datetime

    model_config = {"from_attributes": True}


class AreaStatus(BaseModel):
    location_id: int
    community_status: PowerStatus | None
    official_status: PowerStatus | None
    estimated_restore_time: datetime | None = None
    outage_reports_last_hour: int
    restored_reports_last_hour: int
    last_reported_at: datetime | None = None

