from pydantic import BaseModel

class DriverCreate(BaseModel):
    name: str
    latitude: float
    longitude: float

class DriverResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    is_available: bool

    class Config:
        orm_mode = True
