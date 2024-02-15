from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver.routing_parameters_pb2 import RoutingSearchParameters
from ortools.constraint_solver.routing_enums_pb2 import FirstSolutionStrategy, LocalSearchMetaheuristic
from typing import Optional

__all__ = ['create_search_parameters',]


def create_search_parameters(
            use_greedy_local_search: bool = True,
            search_time_seconds: int = 120) -> RoutingSearchParameters:
        
        ## Setting heuristic strategies
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()

        search_parameters.first_solution_strategy = (FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        if use_greedy_local_search:
            ## Local heuristic strategy
            search_parameters.local_search_metaheuristic = (LocalSearchMetaheuristic.GREEDY_DESCENT)

        ## Time to search
        search_parameters.time_limit.seconds = search_time_seconds
        search_parameters.use_full_propagation = True
        search_parameters.log_search = True

        return search_parameters
