import math
from typing import List
from collections import namedtuple, defaultdict

LocationsDistancesResult = namedtuple('LocationsDistancesResult', ['index_coordinates_map', 'distance_matrix'])


def generate_distance_matrix(locations: List) -> LocationsDistancesResult:
    """
    Translates a vector of location into a inter-location distances matrix.

    :param locations:

    The format of the vector
    [
        (x1, y1),
        (x2, y2),
        ...
    ]

    :return: A matrix depicting the distances between all locations and the coordinates to indexes association.

    """

    index_coordinates_map = {}
    distance_matrix = defaultdict(dict)

    # determine the distance matrix
    for i in range(len(locations)):
        # distance to itself is obviously zero
        distance_matrix[i][i] = 0

        # map index to location
        index_coordinates_map[i] = locations[i]

        # obtain p
        p = locations[i]
        px = p[0]
        py = p[1]

        for j in range(i+1, len(locations)):
            # obtain q
            q = locations[j]
            qx = q[0]
            qy = q[1]

            # calculate distance between p and q
            euclidean_distance = math.hypot((px - qx), (py - qy))

            distance_matrix[i][j] = euclidean_distance
            distance_matrix[j][i] = euclidean_distance

    return LocationsDistancesResult(
        index_coordinates_map=index_coordinates_map,
        distance_matrix=distance_matrix
    )
