# Ride Matching System (Uber-like Backend)

## Overview
This project is a backend service that simulates the core functionality of a ride-hailing platform like Uber. It focuses on efficient rider–driver matching, ride lifecycle management, and dynamic pricing based on demand and supply.

## Features
- Driver and rider registration
- Nearest-driver matching using geospatial distance (Haversine formula)
- Ride lifecycle management (Request → Accept → Complete / Cancel)
- Driver availability locking to prevent double allocation
- Dynamic surge pricing based on demand–supply imbalance
- RESTful APIs with Swagger documentation

## Tech Stack
- Backend: Python, FastAPI
- Database: MySQL
- ORM: SQLAlchemy
- API Documentation: Swagger (OpenAPI)

## Architecture
The system follows a layered architecture:
- API Layer (FastAPI routes)
- Service Layer (matching logic, pricing logic, state transitions)
- Persistence Layer (MySQL via SQLAlchemy)

This separation ensures scalability and clean code organization.

## Matching Logic
- Fetch all available drivers
- Compute distance between rider and drivers using Haversine formula
- Assign the nearest available driver
- Lock the driver to prevent concurrent assignments

## Ride Lifecycle
The ride is modeled as a finite state machine:
- REQUESTED → ACCEPTED → COMPLETED
- REQUESTED / ACCEPTED → CANCELLED

Invalid state transitions are blocked to ensure consistency.

## Surge Pricing
A simple demand–supply based surge model is implemented:
- If active rides exceed available drivers, fare increases dynamically
- This simulates real-world peak demand scenarios

## Future Improvements
- Redis for real-time driver location caching
- Authentication and authorization
- ETA prediction
- Microservices-based scaling

## How to Run
```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
