from pydantic import BaseModel

class RideRequest(BaseModel):
    rider_id: int

class RideResponse(BaseModel):
    id: int
    rider_id: int
    driver_id: int
    status: str
    fare: float

    class Config:
        orm_mode = True
