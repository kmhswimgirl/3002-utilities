# made for the lab 3 extra credit "optimize path"

""" 
============== Psuedocode && Notes ================
workflow:
    input: path from A* function (type Path)
    output: optimized path to send to driver.py (type Path)

helper methods:
    is_colinear():
        Desc: takes in three points and returns true if colinear and false if not
        Input: pt1:tuple, pt2:tuple, pt3:tuple
        Returns: is_colinear:bool

        sub methods:
        calc_slope(pt_a:tuple, pt_b:tuple) --> sub method
            Takes in two points and returns the slope.
            Equation: slope = (x2 - x1) / (y2 - y1)

        slope_ab = calc_slope(pt1, pt2)
        slope_bc = calc_slope(pt2, pt3)

        Logic: 
            if slope_ab == slope_bc
                return True
            else:
                return False
===================================================
"""

def is_colinear(pt_1:tuple, pt_2:tuple, pt_3:tuple):
    """
    Returns true if the three points are colinear, false if they are not.
    """
    # slope calculator helper method
    def calc_slope(pt_a:tuple, pt_b:tuple):

        # assign (x,y) to input tuples
        x1, y1 = pt_a[0], pt_a[1]
        x2, y2 = pt_b[0], pt_b[1]

        # calculate slope
        if (y2 - y1) == 0:
            slope = (y2 - y1) / (x2 - x1)
        elif (x1 == x2 ) and (y1 == y2):
            print("two identical points")
            slope = None
        else:
            slope = (x2 - x1) / (y2 - y1)
        return slope

    # slope calculations
    slope_1_2 = calc_slope(pt_1, pt_2)
    slope_2_3 = calc_slope(pt_2, pt_3)

    # logic handling
    if slope_1_2 == slope_2_3: return True
    else: return False

def optimize_path(path: list[tuple]):
    """
    Takes in a path and returns an optimized one that eliminates colinear points.
    """
    for i in range(len(path) - 3, -1, -1): # have to move backwards to avoid IndexError
        # define the current, next and next + 1 point
        current_pose = path[i]
        next = path[i + 1]
        next_plus = path[i + 2]

        # check if the points are colinear
        check_line = is_colinear(current_pose, next, next_plus)
        if check_line:
            del path[i + 1] # remove point that is in the middle of the line segment
    return path

def line_of_sight(path: list[tuple]):
    for pose in path:



# example path
path:list[tuple] = [(0,1), (0,2), (0,3), (1,4), (2,4), (3,4)] # output should be [(0,1), (0,3), (1,4), (3,4)]

# test for is_colinear
a = path[4]
b = path[5]
c = path[0]

print(is_colinear (a,b,c))

# test for optimize_path
print(optimize_path(path))