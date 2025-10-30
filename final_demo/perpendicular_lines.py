from typing import Tuple
import math

# perpendicular lines method of finding a valid walkable nav goal
class DriveGoal:

    def perpendicular_lines(end_point:Tuple, centroid: Tuple, c_space:int):
        # points
        x2, y2 = end_point
        x1, y1 = centroid

        dx21 = x1 - x2
        dy21 = y1 - y2

        d12 = math.sqrt( dx21**2 + dy21**2 )
        d13 = c_space * math.sqrt(2)

        psi = d13/d12

        dy13 = int(-psi * dx21)
        dx13 = int(psi * dy21)

        x3 = x1 + dx13
        y3 = y1 + dy13

        x4 = x1 - dx13
        y4 = y1 - dy13

        coords = [(x3,y3), (x4, y4)]
        return coords