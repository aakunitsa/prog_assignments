import numpy as np
from geom import Plane3D

observer = np.zeros(3)
screen = np.array([[1, 0, 0],
                   [0, 1, 0],
                   [0, 0, 1]], dtype=float)
#screen = np.array([[1, 0, 0],
#                   [0, 1, 0],
#                   [3, 2, 0]], dtype=float)
#test_point = np.array([-1, -1, -1], dtype=float)
test_point = np.array([10, 10, 10], dtype=float)

# Check if the screen is a valid triangle
gram_matrix = np.dot(screen, screen.T)
if np.abs(np.linalg.det(gram_matrix)) < 1e-12:
    raise Exception('Screen is not a valid triangle')

# Determine the boundary of the screen 
# shadow as an intersection of the 
# three half-spaces defined below

# First half-space (left)
vec_left_1 = screen[0] - observer
vec_left_2 = screen[2] - observer
left_plane = Plane3D(point = observer, normal_vec = np.cross(vec_left_1, vec_left_2))
assert left_plane(screen[1]) < 0

# Seconf half-space (right)
vec_right_1 = screen[0] - observer
vec_right_2 = screen[1] - observer
right_plane = Plane3D(point = observer, normal_vec = np.cross(vec_right_2, vec_right_1))
assert right_plane(screen[2]) < 0

# Third half-space (bottom)
vec_bottom_1 = screen[1] - observer
vec_bottom_2 = screen[2] - observer
bottom_plane = Plane3D(point = observer, normal_vec = np.cross(vec_bottom_2, vec_bottom_1))
assert bottom_plane(screen[0]) < 0

# Outer half-space (defined by the screen)
vec_outer_1 = screen[0] - screen[1]
vec_outer_2 = screen[0] - screen[2]
outer_plane = Plane3D(point = screen[0], normal_vec = np.cross(vec_outer_1, vec_outer_2))
if outer_plane(observer) >= 0:
    outer_plane = Plane3D(point = screen[0], normal_vec = -outer_plane.normal_vec)

assert outer_plane(observer) < 0

orientation = (left_plane(test_point) <= 0) & (bottom_plane(test_point) <= 0) & (right_plane(test_point) <= 0) & (outer_plane(test_point) >=0)

if orientation:
    print('Test point is invisible')
else:
    print('Test point is visible')

