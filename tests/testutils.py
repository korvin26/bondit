from app.models.flight import FlightData


def convert_to_flight_data_model(flight_data: list[dict]):
    return [FlightData(**data) for data in flight_data]

def convert_to_flight_data_model_single(flight_data: dict):
    return FlightData(**flight_data)