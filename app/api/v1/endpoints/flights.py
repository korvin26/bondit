from typing import List
from fastapi import APIRouter, HTTPException
import logging

from app.core.flight_processing import FlightDataProcessor
from app.models.flight import FlightData

router = APIRouter()
flights_processor = FlightDataProcessor()
logging.debug("App started")

@router.get("/flight/{flight_id}")
async def get_flight(flight_id: str):
    logging.debug(f"Getting flight {flight_id}")
    flight = flights_processor.get_fligth(flight_id)
    if flight:
        return {
            "flight ID": flight.flight_id,
            "Arrival": flight.arrival.strftime("%H:%M"),
            "Departure": flight.departure.strftime("%H:%M"),
            "success": flight.success,
        }
    raise HTTPException(status_code=404, detail="Flight not found")


@router.post("/update_flights/")
async def update_flights(new_flights: List[FlightData]):
    logging.debug("Updating flights")
    flights_processor.process_flight_data(new_flights)
    return {"message": "Flights updated successfully"}
