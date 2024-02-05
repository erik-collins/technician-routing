from haversine import haversine, Unit
from numpy.random import choice
from pandas import read_csv, concat
from time import time
from typing import List, Union

from ..config import RoutingConfig
from ..distance import calculate_distance_matrix

from .vehicle_routing import VehicleRouting
# from .vehicle_route_solver import VehicleRouteSolver 

__all__ = ['VehicleRoutingEngine',]
    

class VehicleRoutingEngine:

    def __init__(self, config: RoutingConfig): #, number_of_routes: int):
        self.config = config
        # self.number_of_routes = number_of_routes
        #self.route_drivers = None
        self.data_loaded = False

        self._constant_time_on_location = config.time_on_location
        self.route_capacity = config.route_capacity
        self.driver_speed = config.travel_speed
    
    def load_data(self, tech_path: str = None, client_path: str = None):

        self.df_techs = read_csv(tech_path or self.config.technician_availability_filepath)
        self.df_clients = read_csv(client_path or self.config.client_addresses_filepath)

        df_addresses = concat([
            self.df_techs.loc[:, ('address', 'latitude', 'longitude')],
            self.df_clients.loc[:, ('address', 'latitude', 'longitude')]
        ])

        df_addresses.loc[:, 'coordinates'] = list(map(tuple,df_addresses.loc[:, ('latitude', 'longitude')].values))
        self.coordinates_by_address = df_addresses.set_index('address').loc[:, 'coordinates'].to_dict()

        self.tech_addresses = {i: a for i, a in enumerate(self.df_techs.loc[:, 'address'].values)}
        
        self.set_addresses(self.df_clients.loc[:, 'address'].values)

        # if self.route_drivers is None:
        #     route_percents = self.df_techs.loc[:, '% of Routes']
        #     self.set_route_drivers(
        #         choice(
        #             route_percents.index.values,
        #             self.number_of_routes,
        #             p=route_percents.values
        #         )
        #     )

        self.set_time_on_location(self._constant_time_on_location)


        self.data_loaded = True
        print('Data Loaded')

        return self

    # def set_route_drivers(self, drivers: Union[int, List[int]]):
    #     self.route_drivers = drivers
    #     self.number_of_routes = len(self.route_drivers)
    #     print('Set', self.number_of_routes,'drivers',self.route_drivers)
        
    #     return self

    def set_addresses(self, addresses: List[str]):
        self.addresses = addresses
        self.coordinates = list(map(self.coordinates_by_address.__getitem__, self.addresses))
        print('Set',len(self.addresses),'addresses')

        n_addresses = len(self.coordinates)
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
            if len(time_minutes) != len(self.coordinates):
                raise Exception('Must be of same length as number of addresses/coordinates')
            self.time_on_location = time_minutes            
            self._constant_time_on_location = None
            print('Using individual time on location', self.time_on_location)
        else:
            self.time_on_location = [time_minutes,] * len(self.coordinates)
            self._constant_time_on_location = time_minutes
            print('Using uniform minutes on location of', time_minutes)
        return self

    def calculate_travel_duration(self, coordinates_a, coordinates_b):
        miles = haversine(coordinates_a, coordinates_b, unit=Unit.MILES)
        miles_per_minute = self.driver_speed / 60 
        minutes = miles / miles_per_minute
        return int(minutes) # Google Routing requires integer times

    def run(self, route_drivers: Union[int, List[int]]):
        if not self.data_loaded:
            self.load_data()
        
        if (len(self.coordinates) != len(self.time_on_location)):
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
        tech_coordinates = [self.coordinates_by_address[self.tech_addresses[index]] for index in techs]

        # print(techs)
        # print(tech_coordinates)

        coordinates = tech_coordinates + [z for z in self.coordinates]
        # print(coordinates)
        s = time()
        durations = calculate_distance_matrix(
            coordinates, 
            self.calculate_travel_duration
        )
        ts = time() - s
        print('Calculated', len(durations), 'node durations in', ts)

        print('Running routing for', len(durations),'addresses and', len(route_drivers),'drivers')

        time_on_location = [0,] * len(techs) + self.time_on_location
        # print(time_on_location)
    
        self.routing = VehicleRouting(
            durations,
            time_on_location,
            self.route_capacity,
            route_drivers
        )

        # self.solver = VehicleRouteSolver(self.routing)
        return self.routing.get_routes()
        