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
"""

path:list[tuple] = [(0,1), (0,2), (0,3), (1,4), (2,4), (3,4)] # output should be [(0,1), (0,3), (1,4), (3,4)]
