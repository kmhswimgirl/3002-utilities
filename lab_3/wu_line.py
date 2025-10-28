import math
from typing import Tuple

'''
Wu's line algorithm (not correct, missing an edge case --> Q2)

'''
class lines:
   def line_of_sight_w( p1:Tuple, p2:Tuple): # wu's line algorithm
      cells = []
      x0, y0 = p1[0], p1[1]
      x1, y1 = p2[0], p2[1]

      if abs(y1 - y0) < abs(x1 - x0): # vertical + horizontal line handling
         if x1 < x0: # if line is in Q4 (negative y coords)
            x0, x1 = x1, x0
            y0, y1 = y1, y0
         dx = x1 - x0
         dy = y1 - y0
         m = dy / dx if dx != 0 else 1
         for i in range(1, int(dx)):
            x = x0 + i
            y = y0 + i * m
            if y1 >=0: y_shift = int(y + 1)
            else: y_shift = int(y -1)
            coord_a = (int(x), int(y))
            coord_b = (int(x), y_shift)
            cells.append(coord_a)
            cells.append(coord_b)
         cells.append(p1)
         cells.append(p2)
      elif x1 < 0 and y1 < 0:
         if x1 < x0: # if line is in Q4 (negative y coords)
            x0, x1 = x1, x0
            y0, y1 = y1, y0
         dx = x1 - x0
         dy = y1 - y0
         m = dy / dx if dx != 0 else 1
         for i in range(1, int(dx)):
            x = x0 + i
            y = y0 + i * m
            if y1 >=0: y_shift = int(y + 1)
            else: y_shift = int(y - 1)
            coord_a = (int(x), int(y))
            coord_b = (int(x), y_shift)
            cells.append(coord_a)
            cells.append(coord_b)
         cells.append(p1)
         cells.append(p2)
      else:
         if y0 > y1: # if line is in Q2 or Q3 (negative x coords)
            x0, x1 = x1, x0
            y0, y1 = y1, y0

         dx = x1 - x0
         dy = y1 - y0
         m = dx / dy if dy !=0 else 1
         for i in range(1, int(dy)):
            x = x0 + i * m
            y = y0 + i
            if x1 >=0: x_shift = int(x - 1)
            else: x_shift = int(x + 1)
            coord_a = (int(x), int(y))
            coord_b = (x_shift, int(y))
            cells.append(coord_a)
            cells.append(coord_b)
         cells.append(p1)
         cells.append(p2)
      return cells
   


# gc = lines.line_of_sight((1,1), (5,10))
# print(gc)