from datetime import datetime

from app.models.flight import FlightData


class FlightNode:
    def __init__(self, flight_data: FlightData):
        self.flight_id = flight_data.flight_ID
        self.arrival = datetime.strptime(flight_data.Arrival, "%H:%M")
        self.departure = datetime.strptime(flight_data.Departure, "%H:%M")
        self.success = flight_data.success
        self.duration = (self.departure - self.arrival).total_seconds() / 60
        self.next = None


class FlightList:
    def __init__(self):
        self.head = None

    def insert_sorted(self, flight: FlightNode) -> None:
        if not self.head or self.head.arrival > flight.arrival:
            flight.next = self.head
            self.head = flight
        else:
            current = self.head
            while current.next and current.next.arrival <= flight.arrival:
                current = current.next
            flight.next = current.next
            current.next = flight

    def remove_node_by_id(self, flight_id: str) -> None:
        if self.head.flight_id == flight_id:
            self.head = self.head.next
            return
        current = self.head
        while current.next:
            if current.next.flight_id == flight_id:
                current.next = current.next.next
                return
            current = current.next

    def to_list(self) -> list[dict]:
        flights = []
        current = self.head
        while current:
            flights.append(
                {
                    "flight ID": current.flight_id,
                    "Arrival": current.arrival.strftime("%H:%M"),
                    "Departure": current.departure.strftime("%H:%M"),
                    "success": current.success,
                }
            )
            current = current.next
        return flights


class FlightDataProcessor:
    _instance = None

    # Decided to use in-memory storage instead of csv file, more convenient
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FlightDataProcessor, cls).__new__(
                cls, *args, **kwargs
            )
        return cls._instance

    def reset(self):
        self.flight_list = FlightList()
        self.flight_dict = {}
        self.success_count = 0

    def __init__(self):
        if not hasattr(self, "initialized"):  # Prevent reinitialization in singleton
            self.flight_list = FlightList()  # Linked list to keep flights sorted
            self.flight_dict = {}  # Dictionary for fast access by flight ID
            self.success_count = 0  # Counter for the number of successful flights
            self.initialized = True

    def get_fligth(self, flight_id: str):
        return self.flight_dict.get(flight_id)

    def remove_flight(self, flight: str):
        flight = self.get_fligth(flight.flight_id)
        self.flight_list.remove_node_by_id(flight.flight_id)
        del self.flight_dict[flight.flight_id]
        self.success_count = (
            self.success_count - 1
            if flight.success == "success"
            else self.success_count
        )

    def add_flight(self, flight: FlightNode):
        if self.success_count < 20 and flight.duration >= 180:
            flight.success = "success"
        else:
            flight.success = "fail"

        self.success_count = (
            self.success_count + 1
            if flight.success == "success"
            else self.success_count
        )
        self.flight_list.insert_sorted(flight)
        self.flight_dict[flight.flight_id] = flight

    def process_flight_data(self, flight_data_list: list[FlightData]):
        for flight_data in flight_data_list:
            flight_node = FlightNode(flight_data)
            if flight_node.flight_id in self.flight_dict:
                self.remove_flight(flight_node)
                self.add_flight(flight_node)
            else:
                self.add_flight(flight_node)

        return self.flight_list, self.flight_dict
