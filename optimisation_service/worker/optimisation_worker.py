import logging
from collections import namedtuple
from typing import Callable, Union, Dict

from celery import Celery

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import shortest_path

VehicleResult = namedtuple('VehicleResult', ['total_distance', 'route'])

logger = logging.getLogger(__name__)

app = Celery('optimisation_service')
app.config_from_object('celeryconfig')

logger.info("---- OPTIMISATION SERVICE ----")


def get_distance_callback(manager, distance_matrix) -> Callable:
    """Returns the distance between the two nodes."""

    def distance_callback(from_index, to_index) -> Union[float, int]:
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    return distance_callback


def get_vehicles_routes(manager, routing, solution, num_vehicles) -> Dict[int, VehicleResult]:
    """Construct a dictionary mapping vehicles as indexes to their counterpart data"""

    vehicles_routes = {}

    for vehicle_id in range(num_vehicles):
        route_distance = 0
        route_nodes = []

        # obtain first node
        index = routing.Start(vehicle_id)
        location_index = manager.IndexToNode(index)
        route_nodes.append((location_index, 0,))

        while not routing.IsEnd(index):
            # get next index
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            location_index = manager.IndexToNode(index)

            # obtain the distance
            distance_between_nodes = routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            route_distance += distance_between_nodes

            # record the node
            route_nodes.append((location_index, distance_between_nodes,))

        vehicles_routes[vehicle_id] = VehicleResult(total_distance=route_distance, route=route_nodes)
        return vehicles_routes


@app.task(name='optimisation.calculate_shortest_path')
def calculate_shortest_path(locations, num_vehicles, depot=0):
    locations_distances_result = shortest_path.generate_distance_matrix(locations)

    # create routing index manager
    manager = pywrapcp.RoutingIndexManager(len(locations_distances_result.distance_matrix), num_vehicles, depot)

    # create the routing model
    routing = pywrapcp.RoutingModel(manager)

    transit_callback_index = routing.RegisterTransitCallback(
        get_distance_callback(manager, locations_distances_result.distance_matrix)
    )

    # define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # solve the problem
    solution = routing.SolveWithParameters(search_parameters)

    if not solution:
        return {}

    # generate the results
    vehicles_routes = get_vehicles_routes(manager, routing, solution, num_vehicles)

    routes = [
        {
            'vehicle_index': vehicle_id,
            'total_distance': vehicle_route.total_distance,
            'route': vehicle_route.route,
        }
        for vehicle_id, vehicle_route in vehicles_routes.items()
    ]

    # return the result

    """
    Format of the response:
    
    {
        'indexed_locations': [
            [<location index>, <location coordinates tuple>],
            ...
        ],
        
        'starting_location': <location index of the starting point / depot>,
        
        'routes': [
            {
                'vehicle_index': <vehicle index>,
                'total_distance': <total distance of the route>,
                'route': [
                    [<location index>, <distance from last location>],
                    ...
                ]
            },
            ...   
        ]
    }
    
    """

    return {
        'indexed_locations': list(locations_distances_result.index_coordinates_map.items()),
        'starting_location': depot,
        'routes': routes
    }
