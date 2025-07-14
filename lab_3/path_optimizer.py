# made for the lab 3 extra credit "optimize path"

"""
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

ways to "optimize the path":

    three in a row:
        Name: is_colinear()
        Take in the path and check if there are 3 co-linear points. 
        This means that the middle point (path index + 1) can be eliminated from the path.
    
    vectors
"""

path:list[tuple] = [(0,1), (0,2), (0,3), (1,4), (2,4), (3,4)] # output should be [(0,1), (0,3), (1,4), (3,4)]

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

a = path[4]
b = path[5]
c = path[0]

answer = is_colinear (a,b,c)
print(answer)