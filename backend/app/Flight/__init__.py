from Flight import Flight
import schedule
import time

def get_flight(flight_code):
    flight = Flight(flight_code)
    flight.get_flight_info()
    return flight

def update_gate(flight):
    flight.get_gate()
    return flight



