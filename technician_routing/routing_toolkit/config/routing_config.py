__all__ = ['RoutingConfig',]


class RoutingConfig:
    def __init__(
            self,
            technician_availability_filepath: str,
            client_addresses_filepath: str,
            travel_speed: int,
            time_on_location: int,
            route_capacity: int
    ):
        """
        
        Default configuration information for the routing engine

        Parameters:
        - technician_availability_filepath
          -- path to where technician information lives
        - client_addresses_filepath
          -- path to where all client information lives
        - travel_speed
          -- average speed that the drivers of the route will travel at, in MPH
        - time_on_location
          -- time that a technician spends at each location, in minutes
        - route_capacity
          -- time that a technician is working a route, in minutes.  
          -- Ex:  360 means a 6 hour work day
        
        """


        self.technician_availability_filepath = technician_availability_filepath
        self.client_addresses_filepath = client_addresses_filepath
        self.travel_speed = travel_speed
        self.time_on_location = time_on_location
        self.route_capacity = route_capacity
