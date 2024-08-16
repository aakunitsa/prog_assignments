import numpy as np
from typing import List, Union

class Plane3D:

    def __init__(self, point: np.array, normal_vec: np.array):
        self.point = point
        # Check that normal_vec is normalized to 1
        normal_vec /= np.sqrt(np.sum(normal_vec**2))
        self.normal_vec = normal_vec

    def __call__(self, test_point) -> float:
        '''
        If the result is:
            = 0 - test point belongs to the plane
            > 0 - test point is above the plane in the direction of the normal vector
            < 0 - test point is below the plane in the direction of the normal vector
        '''

        return np.dot(test_point - self.point, self.normal_vec)
