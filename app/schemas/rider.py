from pydantic import BaseModel

class RiderCreate(BaseModel):
    name: str
    latitude: float
    longitude: float

class RiderResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True
