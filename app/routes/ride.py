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

 
    nearest_driver.is_available = False

    ride = Ride(
        rider_id=rider.id,
        driver_id=nearest_driver.id,
        status=RideStatus.REQUESTED,
        fare=calculate_fare(db)

    )

    db.add(ride)
    db.commit()
    db.refresh(ride)

    return ride

@router.post("/{ride_id}/accept", response_model=RideResponse)
def accept_ride(ride_id: int, db: Session = Depends(get_db)):
    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")

    if ride.status != RideStatus.REQUESTED:
        raise HTTPException(status_code=400, detail="Ride cannot be accepted")

    ride.status = RideStatus.ACCEPTED
    db.commit()
    db.refresh(ride)
    return ride

@router.post("/{ride_id}/complete", response_model=RideResponse)
def complete_ride(ride_id: int, db: Session = Depends(get_db)):
    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")

    if ride.status != RideStatus.ACCEPTED:
        raise HTTPException(status_code=400, detail="Ride cannot be completed")

    driver = db.query(Driver).filter(Driver.id == ride.driver_id).first()

    ride.status = RideStatus.COMPLETED
    driver.is_available = True

    db.commit()
    db.refresh(ride)
    return ride

@router.post("/{ride_id}/cancel", response_model=RideResponse)
def cancel_ride(ride_id: int, db: Session = Depends(get_db)):
    ride = db.query(Ride).filter(Ride.id == ride_id).first()
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")

    if ride.status == RideStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Completed ride cannot be cancelled")

    driver = db.query(Driver).filter(Driver.id == ride.driver_id).first()

    ride.status = RideStatus.CANCELLED
    driver.is_available = True

    db.commit()
    db.refresh(ride)
    return ride

def calculate_fare(db):
    base_fare = 100.0

    active_rides = db.query(Ride).filter(
        Ride.status.in_([RideStatus.REQUESTED, RideStatus.ACCEPTED])
    ).count()

    available_drivers = db.query(Driver).filter(
        Driver.is_available == True
    ).count()

    if available_drivers == 0:
        return base_fare * 1.5

    if active_rides > available_drivers:
        return base_fare * 1.5

    return base_fare
