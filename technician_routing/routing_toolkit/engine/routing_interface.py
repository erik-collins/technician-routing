from haversine import haversine, Unit
from numpy.random import choice
from ortools.constraint_solver.routing_parameters_pb2 import RoutingSearchParameters
from pandas import read_csv, concat
from time import time
from typing import List, Union, Optional

from ..config import RoutingConfig

from .distance_calculations import calculate_distance_matrix
from .route_solver import RouteSolver

__all__ = ['RoutingInterface',]
    

class RoutingInterface:

    def __init__(self, config: RoutingConfig):
        self.config = config
        self.data_loaded = False

        self._constant_time_on_location = config.time_on_location
        self.route_capacity = config.route_capacity
        self.driver_speed = config.travel_speed

        self.solver = None
        
        self.df_techs = None
        self.df_clients = None
        self.coordinates_by_address = None

        self.tech_address_by_id = None

        self.client_addresses = None
        self.client_coordinates = None
        self.time_on_location = None
                
        self.last_coordinates = None
        self.last_durations = None

        self.search_parameters = None


    
    def load_data(self, tech_path: str = None, client_path: str = None):

        self.df_techs = read_csv(tech_path or self.config.technician_availability_filepath)
        self.df_clients = read_csv(client_path or self.config.client_addresses_filepath)

        df_addresses = concat([
            self.df_techs.loc[:, ('address', 'latitude', 'longitude')],
            self.df_clients.loc[:, ('address', 'latitude', 'longitude')]
        ])

        df_addresses.loc[:, 'coordinates'] = list(map(tuple,df_addresses.loc[:, ('latitude', 'longitude')].values))
        self.coordinates_by_address = df_addresses.set_index('address').loc[:, 'coordinates'].to_dict()

        self.tech_address_by_id = {i: a for i, a in enumerate(self.df_techs.loc[:, 'address'].values)}
        
        self.set_addresses(self.df_clients.loc[:, 'address'].values)
        self.set_time_on_location(self._constant_time_on_location)

        self.data_loaded = True
        print('Data Loaded')

        return self


    def set_addresses(self, addresses: List[str]):
        self.client_addresses = [z for z in addresses]
        self.client_coordinates = [self.coordinates_by_address[a] for a in self.client_addresses]
        print('Set',len(self.client_addresses),'client addresses')

        n_addresses = len(self.client_coordinates)
        if self._constant_time_on_location is not None:
            self.time_on_location = n_addresses * [self._constant_time_on_location]
        elif self.time_on_location is not None and len(self.time_on_location) < n_addresses:
            self.time_on_location = self.time_on_location[:n_addresses]

        return self


    def set_driver_speed(self, speed_mph: int):
        self.driver_speed = speed_mph
        print('Using driver speed of', self.driver_speed,'MPH')
        return self


    def set_time_on_location(self, time_minutes: Union[List[int], int]):
        if hasattr(time_minutes, '__iter__'):
            if len(time_minutes) != len(self.client_coordinates):
                raise Exception('Must be of same length as number of addresses/coordinates')
            self.time_on_location = time_minutes            
            self._constant_time_on_location = None
            print('Using individual time on location', self.time_on_location)
        else:
            self.time_on_location = [time_minutes,] * len(self.client_coordinates)
            self._constant_time_on_location = time_minutes
            print('Using uniform minutes on location of', time_minutes)
        return self


    def set_search_parameters(self, search_parameters: Optional[RoutingSearchParameters] = None):
        self.search_parameters = search_parameters
        return self

    def calculate_travel_duration(self, coordinates_a, coordinates_b):
        miles = haversine(coordinates_a, coordinates_b, unit=Unit.MILES)
        miles_per_minute = self.driver_speed / 60 
        minutes = miles / miles_per_minute
        return int(minutes) # Google Routing requires integer times


    def run(self, route_drivers: Union[int, List[int]]):
        if not self.data_loaded:
            self.load_data()
        
        if (len(self.client_coordinates) != len(self.time_on_location)):
            raise Exception('coordinates and time_on_location must be of the same length')
        
        if hasattr(route_drivers, '__iter__'):
            print(route_drivers)
            route_drivers = [z for z in route_drivers]
        else:
            route_percents = self.df_techs.loc[:, '% of Routes']
            route_drivers = choice(
                route_percents.index.values,
                route_drivers,
                p=route_percents.values
            )

        techs = list(sorted(set(route_drivers)))
        tech_addresses = [self.tech_address_by_id[index] for index in techs]
        tech_coordinates = [self.coordinates_by_address[address] for address in tech_addresses]

        self.last_coordinates = tech_coordinates + self.client_coordinates
        self.last_addresses = tech_addresses + self.client_addresses

        s = time()
        self.last_durations = calculate_distance_matrix(
            self.last_coordinates, 
            self.calculate_travel_duration
        )



        ts = time() - s
        print('Calculated', len(self.last_durations), 'node durations in', ts)

        print('Running routing for', len(self.last_durations),'addresses and', len(route_drivers),'drivers')

        time_on_location = [0,] * len(techs) + self.time_on_location
    
        self.solver = RouteSolver(
            self.last_durations,
            time_on_location,
            self.route_capacity,
            route_drivers,
            search_parameters = self.search_parameters
        )

        return self.solver.get_routes()
        