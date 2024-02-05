# from ortools.constraint_solver import pywrapcp
# from ortools.constraint_solver.routing_parameters_pb2 import RoutingSearchParameters
# from typing import Optional

# from .vehicle_routing import VehicleRouting
# from .optimizer_utils import create_search_parameters

# __all__ = ['VehicleRouteSolver',]


# class VehicleRouteSolver:

#     def __init__(
#         self,
#         routing: VehicleRouting,
#         search_parameters: Optional[RoutingSearchParameters] = None,
#         solve_immediately = True):

#         self.routing = routing
#         self.search_parameters = search_parameters or create_search_parameters()

#         self.solved = False
#         if solve_immediately:
#             self.solve()
#         else:
#             self.solved_objective_value = None
#             self.solution = None

#     def solve(self, re_solve: bool = False):
#         if not re_solve and self.solved:
#             return

#         self.solution = self.routing.model.SolveWithParameters(self.search_parameters)
#         if self.solution is None:
#             raise Exception('Failed to solve problem')
    
#         self.solved_objective_value = self.solution.ObjectiveValue()
#         print('Solved objective value', self.solved_objective_value)
#         self.solved = True

#     def get_routes(self):  
#         self.solve(re_solve = False)      
#         routes = self.routing.get_routes(self.solution)
#         return routes

        
