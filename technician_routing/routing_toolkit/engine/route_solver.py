from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver.routing_parameters_pb2 import RoutingSearchParameters
from typing import Optional

from .optimizer_utils import create_search_parameters

__all__ = ['RouteSolver',]


class RouteSolver:
    def __init__(
            self, 
            distances,
            demands, 
            capacity: int, 
            starts, 
            ends = None,
            search_parameters: Optional[RoutingSearchParameters] = None,
            solve_immediately = False):
        """
            distances:
                matrix of edge costs (distances between each node)
                N x N for N addresses
                
            demands:
                array of node costs (time spent at address)
                1 x N for N addresses

            capacity:
                max time per route
                
            starts:
                array of start indices, length of number of vehicles

            ends:
                array of end indices, length of number of vehicles
                Optional, None -> ends = starts

            search_parameters:
                Optional optimization parameters

            solve_immediately:
                Solve route immediately on construction
                
        """
        
        self.distances = distances
        self.demands = demands
        self.capacity = capacity

        if hasattr(starts, 'tolist'):
            starts = starts.tolist()

        if hasattr(ends, 'tolist'):
            ends = ends.tolist()

        self.n_destinations = len(self.distances)
        self.n_vehicles = len(starts)
        self.starts = starts
        self.ends = ends or starts
            
        ## Create the routing index manager, manages index <-> Node relationships
        self.index_manager = pywrapcp.RoutingIndexManager(
            self.n_destinations,
            self.n_vehicles,
            self.starts,
            self.ends
        )

        ## Create Routing Model
        self.model = pywrapcp.RoutingModel(self.index_manager)

        ## Define transit callback function
        #transit_callback_index = self.model.RegisterTransitCallback(self.distance_callback)
        combined_callback_index = self.model.RegisterTransitCallback(self.combined_callback)
            
        # Define cost of each arc
        self.model.SetArcCostEvaluatorOfAllVehicles(combined_callback_index)
        
        ## Define demand callback function
        # demand_callback_index = self.model.RegisterUnaryTransitCallback(self.demand_callback)
        
        # Any constraint associated with vehicles can take same arguments
        # self.model.AddDimensionWithVehicleCapacity(
        #     demand_callback_index,
        #     0,  # null capacity slack
        #     self.capacities,  # vehicle maximum capacities (list for each vehicle)
        #     True,  # start cumul to zero
        #     'Capacity'
        # )
        self.model.AddDimension(
            combined_callback_index,
            0,
            self.capacity,
            True,
            'Combined'
        )
    
        self.search_parameters = search_parameters or create_search_parameters()
        self.solved = False
        if solve_immediately:
            self.solve()
        else:
            self.solved_objective_value = None
            self.solution = None

    
    def combined_callback(self, from_index, to_index):
        from_node = self.index_manager.IndexToNode(from_index)
        to_node = self.index_manager.IndexToNode(to_index)
        distance = int(self.distances[from_node, to_node])
        time_at = int(self.demands[to_node])
        # print(from_index, to_index, distance)
        return distance + time_at


    # Same valid for any callback related to arcs/edges
    # Note:  This must return an integer
    def distance_callback(self, from_index, to_index):
        from_node = self.index_manager.IndexToNode(from_index)
        to_node = self.index_manager.IndexToNode(to_index)
        distance = int(self.distances[from_node, to_node])
        return distance


    # Same valid for any callback related to nodes
    # Note:  This must return an integer
    def demand_callback(self, from_index):
        from_node = self.index_manager.IndexToNode(from_index)
        demand = int(self.demands[from_node])
        return demand
    

    def solve(self, re_solve: bool = False, search_parameters: Optional[RoutingSearchParameters] = None):
        if not re_solve and self.solved:
            return self.solution

        self.solution = self.model.SolveWithParameters(search_parameters or self.search_parameters)
        if self.solution is None:
            raise Exception('Failed to solve problem, likely too few routes/vehicles')
    
        self.solved_objective_value = self.solution.ObjectiveValue()
        print('Solved objective value', self.solved_objective_value)
        self.solved = True
        return self.solution


    def get_routes(self):
        solution = self.solve(re_solve =False)
        routes = []

        for tour_number, vehicle_id in enumerate(range(len(self.starts))):
            index = self.model.Start(vehicle_id)
            starting_node = self.index_manager.IndexToNode(index)
            route = [starting_node,]
            
            while not self.model.IsEnd(index):
                next_var = self.model.NextVar(index)
                previous_index = index
                index = solution.Value(next_var)
                    
                route.append(self.index_manager.IndexToNode(index))

            if len(route) == 2 and route[0] == route[-1]:
                print(f'Skipped unused route {tour_number} starting at {vehicle_id}')
                continue # Empty / Unused Route

            routes.append(route)

        return routes
