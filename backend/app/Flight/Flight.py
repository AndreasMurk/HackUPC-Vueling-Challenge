import requests
import os
import json


class Flight:
    def __init__(self, flight_number, departure=None, arrival=None, gate=None, scheduled=None, estimated=None):
        self.flight_number = flight_number
        self.departure = departure
        self.arrival = arrival
        self.gate = gate
        self.scheduled = scheduled
        self.estimated = estimated
        self.flight_api_url = "http://api.aviationstack.com/v1/flights"
        #self.flight_api_key = os.env.get('FLIGHT_API_KEY')
        self.flight_api_key = os.environ.get('FLIGHT_API_KEY')

    def get_flight_info(self):
        params = {
            "access_key": self.flight_api_key,
            "flight_iata": self.flight_number
        }
        response = requests.get(self.flight_api_url, params=params)
        data = response.json()
        data = data['data']
        # if data['pagination']['total'] == 0:
        #     return None
        # else:
        if data is None:
            print("no information available")
        print(data[0])
        self.departure = data[0]['departure']['airport']
        self.arrival = data[0]['arrival']['airport']
        self.gate = data[0]['departure']['gate']
        self.scheduled = data[0]['departure']['scheduled']
        self.estimated = data[0]['departure']['estimated']

    def get_gate(self):
        return self.gate

    def get_departure(self):
        return self.departure
    
    def get_arrival(self):
        return self.arrival
    
    def get_scheduled(self):
        return self.scheduled
    
    def get_estimated(self):
        return self.estimated
    
    def get_flight_number(self):
        return self.flight_number
    
