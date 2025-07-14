"""
vars:
    path
    path.next = path[i+1]
    path.two_ahead = path[i+2]

helper methods:
    is_colinear():
        takes in a

ways to "optimize the path":

    three in a row:
        Take in the path and check if there are 3 co-linear points. 
        This means that the middle point can be eliminated.
"""

path:list[tuple] = [(0,1)]