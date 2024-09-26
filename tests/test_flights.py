import json
from unittest import mock
from fastapi.testclient import TestClient
from app.main import app
from app.core.flight_processing import FlightNode

client = TestClient(app)

def test_get_flight():
    with mock.patch('app.core.flight_processing.FlightDataProcessor.get_fligth') as mock_get_flight:
        new_flight_data = {'flight ID': 'A12', 'Arrival': '15:00', 'Departure': '18:30', 'success': ''}
        flight_node = FlightNode(new_flight_data)
        mock_get_flight.return_value = flight_node
        response = client.get("/api/v1/flight/A12")
        assert response.status_code == 200
        flight = response.json()
        assert flight['flight ID'] == 'A12'


def test_update_flights():
    new_flight_data = [{'flight ID': 'X123', 'Arrival': '15:00', 'Departure': '18:30', 'success': ''}]
    headers={"content-type": "application/json"}
    response = client.post("/api/v1/update_flights/", json=new_flight_data, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Flights updated successfully"}
