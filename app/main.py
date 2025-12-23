from fastapi import FastAPI
from app.database import engine
from app.models import driver, rider
from app.routes import driver as driver_routes
from app.routes import ride as ride_routes
from app.routes import rider as rider_routes

app = FastAPI(title="Ride Matching System")

driver.Base.metadata.create_all(bind=engine)
rider.Base.metadata.create_all(bind=engine)

app.include_router(driver_routes.router)
app.include_router(rider_routes.router)
app.include_router(ride_routes.router)



@app.get("/")
def health_check():
    return {"status": "Ride Matching System is running"}
