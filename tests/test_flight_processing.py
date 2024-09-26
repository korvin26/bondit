import pytest
from app.core.flight_processing import FlightDataProcessor


@pytest.fixture(autouse=True)
def run_around_tests():
    FlightDataProcessor().reset()
    yield

def test_process_flight_data():
    flight_data = [
        {"flight ID": "A12", "Arrival": "09:00", "Departure": "13:00", "success": ""},
        {"flight ID": "A14", "Arrival": "12:00", "Departure": "19:00", "success": ""},
        {"flight ID": "B15", "Arrival": "10:00", "Departure": "13:00", "success": ""},
    ]
    flight_processor = FlightDataProcessor()
    flight_processor.process_flight_data(flight_data)
    assert flight_processor.flight_list.head.flight_id == "A12"
    assert flight_processor.flight_dict["A12"].success == "success"


def test_process_flight_data_update_flight():
    flight_data = [
        {"flight ID": "A12", "Arrival": "09:00", "Departure": "13:00", "success": ""},
        {"flight ID": "B15", "Arrival": "10:00", "Departure": "13:00", "success": ""},
        {"flight ID": "A12", "Arrival": "12:00", "Departure": "19:00", "success": ""},
    ]

    flight_processor = FlightDataProcessor()
    flight_processor.process_flight_data(flight_data)
    assert flight_processor.flight_list.head.flight_id == "B15"
    assert flight_processor.flight_dict["A12"].success == "success"


def test_process_flight_data_concurrent_update():
    flight_data = [
        {"flight ID": "A12", "Arrival": "09:00", "Departure": "13:00", "success": ""},
        {"flight ID": "A14", "Arrival": "12:00", "Departure": "19:00", "success": ""},
        {"flight ID": "B15", "Arrival": "10:00", "Departure": "13:00", "success": ""},
    ]
    flight_data_2 = [
        {"flight ID": "A22", "Arrival": "09:40", "Departure": "19:00", "success": ""},
        {"flight ID": "A17", "Arrival": "12:50", "Departure": "19:00", "success": ""},
        {"flight ID": "B18", "Arrival": "10:30", "Departure": "18:00", "success": ""},
    ]
    flight_processor = FlightDataProcessor()
    flight_processor.process_flight_data(flight_data)
    flight_processor.process_flight_data(flight_data_2)
    assert flight_processor.success_count == 6


def test_process_flight_data_fail():
    flight_data = [
        {"flight ID": "A12", "Arrival": "09:00", "Departure": "11:00", "success": ""},
        {"flight ID": "A14", "Arrival": "12:00", "Departure": "19:00", "success": ""},
        {"flight ID": "B15", "Arrival": "10:00", "Departure": "12:59", "success": ""},
    ]

    flight_processor = FlightDataProcessor()
    flight_processor.process_flight_data(flight_data)
    assert flight_processor.flight_dict["A12"].success == "fail"
    assert flight_processor.flight_dict["A14"].success == "success"
    assert flight_processor.flight_dict["B15"].success == "fail"


def test_process_flight_data_fail_over_20():
    flight_data = [
        {"flight ID": "A12", "Arrival": "09:00", "Departure": "13:00", "success": ""},
        {"flight ID": "A14", "Arrival": "12:00", "Departure": "19:00", "success": ""},
        {"flight ID": "B15", "Arrival": "10:00", "Departure": "13:00", "success": ""},
        {"flight ID": "C124", "Arrival": "14:00", "Departure": "16:00", "success": ""},
        {"flight ID": "C23", "Arrival": "08:00", "Departure": "17:00", "success": ""},
        {"flight ID": "B12", "Arrival": "13:01", "Departure": "16:00", "success": ""},
        {"flight ID": "G56", "Arrival": "09:30", "Departure": "14:00", "success": ""},
        {"flight ID": "B35", "Arrival": "16:01", "Departure": "20:00", "success": ""},
        {"flight ID": "A21", "Arrival": "08:00", "Departure": "13:00", "success": ""},
        {"flight ID": "A19", "Arrival": "17:00", "Departure": "19:00", "success": ""},
        {"flight ID": "B55", "Arrival": "11:00", "Departure": "13:00", "success": ""},
        {"flight ID": "C128", "Arrival": "12:00", "Departure": "16:00", "success": ""},
        {"flight ID": "C26", "Arrival": "08:00", "Departure": "17:00", "success": ""},
        {"flight ID": "B52", "Arrival": "12:01", "Departure": "16:00", "success": ""},
        {"flight ID": "G86", "Arrival": "07:30", "Departure": "14:00", "success": ""},
        {"flight ID": "B65", "Arrival": "17:01", "Departure": "20:00", "success": ""},
        {"flight ID": "B05", "Arrival": "10:00", "Departure": "14:00", "success": ""},
        {"flight ID": "C1223", "Arrival": "12:55", "Departure": "16:00", "success": ""},
        {"flight ID": "C235", "Arrival": "08:00", "Departure": "22:00", "success": ""},
        {"flight ID": "B46", "Arrival": "14:01", "Departure": "16:00", "success": ""},
        {"flight ID": "G88", "Arrival": "09:30", "Departure": "14:00", "success": ""},
        {"flight ID": "B39", "Arrival": "16:01", "Departure": "20:00", "success": ""},
        {"flight ID": "G88", "Arrival": "11:30", "Departure": "14:05", "success": ""},
        {"flight ID": "B39", "Arrival": "16:01", "Departure": "20:00", "success": ""},
    ]

    flight_processor = FlightDataProcessor()
    flight_processor.process_flight_data(flight_data)
    flights = flight_processor.flight_list.to_list()
    assert len([x for x in flights if x["success"] == "fail"]) == 7
    assert len([x for x in flights if x["success"] == "success"]) == 15


def test_two_instances():
    flight_data = [
        {"flight ID": "A12", "Arrival": "09:00", "Departure": "13:00", "success": ""},
        {"flight ID": "A14", "Arrival": "12:00", "Departure": "19:00", "success": ""},
        {"flight ID": "B15", "Arrival": "10:00", "Departure": "13:00", "success": ""},
    ]
    flight_processor = FlightDataProcessor()
    flight_processor_2 = FlightDataProcessor()
    flight_processor.process_flight_data(flight_data)
    assert flight_processor.flight_list.head.flight_id == "A12"
    assert flight_processor_2.flight_list.head.flight_id == "A12"
    assert flight_processor.flight_dict["A12"].success == "success"
    assert flight_processor_2.flight_dict["A12"].success == "success"
