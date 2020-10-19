import pytest

from faker import Faker

from worker.shortest_path import generate_distance_matrix

fake = Faker()


def test_distance_matrix_generation():
    """Check the generation of a proper distance matrix"""

    # prepare
    locations = [
        [10, 10],
        [10, 12],
        [100, 500],
        [22, 30]
    ]

    # act
    locations_distances_result = generate_distance_matrix(locations)

    # assert
    enumerated_locations = dict(enumerate(locations))
    assert locations_distances_result.index_coordinates_map == enumerated_locations

    expected_distance_matrix = {
        0: {
            0: 0, 1: 2.0, 2: 498.19674828324605, 3: 23.3238075793812
        },
        1: {
            0: 2.0, 1: 0, 2: 496.22978548249193, 3: 21.633307652783937
        },
        2: {
            0: 498.19674828324605,
            1: 496.22978548249193,
            2: 0,
            3: 476.42837866777
        },
        3: {
            0: 23.3238075793812,
            1: 21.633307652783937,
            2: 476.42837866777,
            3: 0
        }
    }
    assert locations_distances_result.distance_matrix == expected_distance_matrix
