from fastapi import FastAPI
from app.database import engine
from app.models import driver, rider

app = FastAPI(title="Ride Matching System")

# Auto-create tables
driver.Base.metadata.create_all(bind=engine)
rider.Base.metadata.create_all(bind=engine)

@app.get("/")
def health_check():
    return {"status": "Ride Matching System is running"}
