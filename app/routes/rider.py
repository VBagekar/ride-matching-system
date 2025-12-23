from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.rider import Rider
from app.schemas.rider import RiderCreate, RiderResponse

router = APIRouter(prefix="/riders", tags=["Riders"])

@router.post("/", response_model=RiderResponse)
def create_rider(rider: RiderCreate, db: Session = Depends(get_db)):
    new_rider = Rider(
        name=rider.name,
        latitude=rider.latitude,
        longitude=rider.longitude
    )
    db.add(new_rider)
    db.commit()
    db.refresh(new_rider)
    return new_rider
