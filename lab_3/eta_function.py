import math
from math import pi
from typing import Tuple, List

'''
function name: eta
parameters: Path, linear_speed, angular_speed

distance = rate/time
distance/rate = time

++++ maybe split into sub methods? ++++

total distance:
    linear:
        find euclidean distance from point to point + add to the sum
            - have to iterate backwards to avoid errors

    angular:
        take the three next points and find the angle they make, might also have to iterate backwards
        point 1 = point -2

total time:
    linear:
    angular:
'''

path_1 = [(0,0), (1,1), (1,2), (3,3), (5,3)]

def euclidean_distance(p1: List[Tuple], p2: List[Tuple]):
    distance = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
    return distance

def law_of_cosines(a, b, c):
    n = a**2 + c**2 - b**2
    d = 2*a*c
    angle = math.acos(n/d)
    return angle # THIS IS RADIANS!!!!

## ---------- Main Calcs ---------- ##
def total_linear_travel(path: List[Tuple]):
    total_dist = 0
    for i in range(len(path) - 2, -1, -1):
        dist = euclidean_distance(path[i], path[i + 1])
        total_dist += dist
    return total_dist

def total_angular_rotation(path: List[Tuple], initial_heading:float):
    total_rotation = 0
    debug = []
    # initial angle calc
    # init_angle = law_of_cosines()
    for i in range(len(path) -3,-1,-1):
        p1, p2, p3 = path[i], path[i+1], path[i+2]
        a = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
        b = math.sqrt((p3[0] - p1[0])**2 + (p3[1] - p1[1])**2)
        c = math.sqrt((p2[0] - p3[0])**2 + (p2[1] - p3[1])**2)

        angle = law_of_cosines(a,b,c)
        s_angle = math.pi - angle

        debug.append(s_angle)
        total_rotation += s_angle

    # total_in_deg = math.degrees(total_rotation)
    print(debug)
    return total_rotation

def eta (path: List[Tuple]):
    linear_speed = 0.5 # m/s
    linear_distance = total_linear_travel(path) # recall this is in grid squares... however they are 1m x 1m squares :)
    linear_time = linear_distance/linear_speed # in seconds

    ang_speed = 0.2 # rad/s
    total_rotation = total_angular_rotation(path, 0)
    ang_time = total_rotation/ang_speed

    time = linear_time + ang_time

    return int(time)

## ---------- Testing ---------- ##

# testing linear distance
test = total_linear_travel(path_1)
print(f'total linear dist: {test} m')

# testing total rotation 
test2 = total_angular_rotation(path_1, 0.0)
print(f'total rotation = {test2} rad')

# testing total time
test3 = eta(path_1)
print(f'total time (eta): {test3} s')