import requests
import os


class Flight:
    def __init__(self, flight_number, departure=None, arrival=None, gate=None, delayed=0, timeDelayed=None):
        self.flight_number = flight_number
        self.departure = departure
        self.arrival = arrival
        self.gate = gate
        self.delayed = delayed
        self.timeDelayed = timeDelayed
        self.flight_api_url = "https://api.aviationstack.com/v1/flights"
        self.flight_api_key = os.env.get('FLIGHT_API_KEY')
        self.data = None

    def get_flight_info(self):
        params = {
            "access_key": self.flight_api_key,
            "flight_iata": self.flight_number
        }
        response = requests.get(self.flight_api_url, params=params)
        data = response.json()
        if data['pagination']['total'] == 0:
            return None
        else:
            self.data = data

    def get_gate(self):
        params = {
            "access_key": self.flight_api_key,
            "flight_iata": self.flight_number
        }
        response = requests.get(self.flight_api_url, params=params)
        data = response.json()
        if data['pagination']['total'] == 0:
            return None
        else:
            self.gate = data['departure']['gate']
