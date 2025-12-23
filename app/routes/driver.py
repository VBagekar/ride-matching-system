from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.driver import Driver
from app.schemas.driver import DriverCreate, DriverResponse

router = APIRouter(prefix="/drivers", tags=["Drivers"])

@router.post("/", response_model=DriverResponse)
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    new_driver = Driver(
        name=driver.name,
        latitude=driver.latitude,
        longitude=driver.longitude,
        is_available=True
    )
    db.add(new_driver)
    db.commit()
    db.refresh(new_driver)
    return new_driver
