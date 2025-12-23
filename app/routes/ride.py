from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.driver import Driver
from app.models.rider import Rider
from app.models.ride import Ride, RideStatus
from app.schemas.ride import RideRequest, RideResponse
from app.utils.distance import haversine

router = APIRouter(prefix="/rides", tags=["Rides"])

@router.post("/request", response_model=RideResponse)
def request_ride(ride_request: RideRequest, db: Session = Depends(get_db)):
    rider = db.query(Rider).filter(Rider.id == ride_request.rider_id).first()
    if not rider:
        raise HTTPException(status_code=404, detail="Rider not found")

    available_drivers = db.query(Driver).filter(Driver.is_available == True).all()
    if not available_drivers:
        raise HTTPException(status_code=400, detail="No drivers available")

    nearest_driver = None
    min_distance = float("inf")

    for driver in available_drivers:
        distance = haversine(
            rider.latitude, rider.longitude,
            driver.latitude, driver.longitude
        )
        if distance < min_distance:
            min_distance = distance
            nearest_driver = driver

    # Lock driver
    nearest_driver.is_available = False

    ride = Ride(
        rider_id=rider.id,
        driver_id=nearest_driver.id,
        status=RideStatus.REQUESTED,
        fare=100.0  # base fare for now
    )

    db.add(ride)
    db.commit()
    db.refresh(ride)

    return ride
