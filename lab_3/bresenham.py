from typing import Tuple, List
'''
Bresenham's line algorithm
---
Cases:
    1. 0 < m <= 1
    2. -1 <= m < 0
    3. m = 0
    4. m = undefined
    5. m > 1
    6. m < -1
Each case has two sub cases: dx > dy and dy > dx
'''
class line:
    def bresenham(p1: Tuple[int,int], p2: Tuple[int,int]) -> List[Tuple[int,int]]:
        x0, y0 = p1[0], p1[1]
        x1, y1 = p2[0], p2[1]

        cells: List[Tuple[int,int]] = []

        dx = abs(x1 - x0)
        sx = 1 if x0 < x1 else -1
        dy = -abs(y1 - y0)
        sy = 1 if y0 < y1 else -1
        err = dx + dy  # err = dx - abs(dy)

        while True:
            cells.append((x0, y0))
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
        return cells


# print(bresenham((0,0),(3,1)))  
# print(bresenham((3,1),(0,0)))   
# print(bresenham((-2,-2),(2,1))) 
# print(bresenham((0,0), (0,1)))