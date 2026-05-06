from pydantic import BaseModel, Field


class LocationCreate(BaseModel):
    state: str = Field(min_length=2, max_length=80)
    city: str = Field(min_length=2, max_length=80)
    area_name: str = Field(min_length=2, max_length=120)


class LocationRead(BaseModel):
    id: int
    state: str
    city: str
    area_name: str

    model_config = {"from_attributes": True}

