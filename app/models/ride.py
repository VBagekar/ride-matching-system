from sqlalchemy import Column, Integer, Float, Enum, ForeignKey
from app.database import Base
import enum

class RideStatus(enum.Enum):
    REQUESTED = "REQUESTED"
    ACCEPTED = "ACCEPTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    rider_id = Column(Integer, ForeignKey("riders.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    status = Column(Enum(RideStatus), default=RideStatus.REQUESTED)
    fare = Column(Float)
