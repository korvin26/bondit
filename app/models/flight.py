# app/models/flight.py

from pydantic import BaseModel, field_validator, ConfigDict, ValidationInfo
from datetime import datetime

class FlightData(BaseModel):
    flight_ID: str
    Arrival: str
    Departure: str
    success: str

    model_config = ConfigDict(populate_by_name=True, fields={'flight_ID': {'alias': 'flight ID'}})

    @field_validator('flight_ID')
    def validate_flight_id(cls, value):
        if not value or not value.isalnum():
            raise ValueError("Flight ID must be a non-empty alphanumeric string")
        return value

    @field_validator('Arrival', 'Departure')
    def validate_time_format(cls, value):
        try:
            datetime.strptime(value, '%H:%M')
        except ValueError:
            raise ValueError(f"Time '{value}' is not in the correct format 'HH:MM'")
        return value

    @field_validator('Departure')
    def validate_departure_after_arrival(cls, value, info: ValidationInfo):
        # Access the 'Arrival' field using info.data
        arrival_time_str = info.data.get('Arrival')
        if arrival_time_str:
            arrival_time = datetime.strptime(arrival_time_str, '%H:%M')
            departure_time = datetime.strptime(value, '%H:%M')
            if departure_time <= arrival_time:
                raise ValueError("Departure time must be after the arrival time")
        return value
