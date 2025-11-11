#!/usr/bin python3

from dataclasses import dataclass, field
from typing import Tuple, List

@dataclass
class OccupancyGrid:
        height: int
        width: int
        data: List[int]

map_1 = OccupancyGrid(10, 10, [
                                1,0,1,1,0,0,1,0,1,0,
                                0,1,0,0,1,1,0,1,0,0,
                                1,1,1,0,0,1,0,0,1,0,
                                0,0,1,0,1,0,1,1,0,1,
                                1,0,0,1,1,0,0,1,0,0,
                                0,1,0,1,0,1,1,0,1,0,
                                1,1,0,0,1,0,1,0,0,1,
                                0,0,1,1,0,1,0,1,1,0,
                                1,0,1,0,1,1,0,0,1,1,
                                0,1,0,1,0,0,1,1,0,0
])


class Node:
    def grid_to_index(mapdata: OccupancyGrid, p: Tuple[int, int]) -> int:
        """
        Returns the index corresponding to the given (x,y) coordinates in the occupancy grid.
        :param p [(int, int)] The cell coordinate.
        :return  [int] The index.
        """
        r, c = p
        return r * mapdata.width + c

    def is_cell_walkable(map: OccupancyGrid, cell: Tuple[int, int]):
        cell_index = Node.grid_to_index(map, cell)
        if map.data[cell_index] == 0 and Node.in_bounds(map, cell): # 0 == free space, 1 is blocked
            return True
        else: 
            return False
        
    def in_bounds(mapdata:OccupancyGrid, cell:Tuple[int, int]) -> bool: # helper for checking if searched cells are in bounds
            if not isinstance(cell, tuple) or len(cell) != 2:
                return False
            r, c = cell
            if not isinstance(r, int) or not isinstance(c, int):
                return False
            # cell is (row, col)
            return 0 <= r < mapdata.height and 0 <= c < mapdata.width
        
    def nearest_walkable_cell(mapdata: OccupancyGrid, grid_cell:Tuple[int, int]):
        # queue
        # take top of queue, return neighbors of 8
            # mark cell as visited
        # for loop through all neighbors and see if any are walkable, 
            # if walkable, that is the goal
            # if not walkable and not visited add to search list
            
        if Node.is_cell_walkable(mapdata, grid_cell): # og cell is walkable case
            return grid_cell
        
        start = grid_cell 
        searched = []
        not_searched = [] 
        not_searched.append(start)

        dir_four = [(1,0), (0,1), (0,-1), (-1, 0)]

        while len(not_searched) > 0:
            current = not_searched.pop(0)
            searched.append(current) # add current cell to searched list

            for (dx, dy) in dir_four:
                nx = dx + current[0]
                ny = dy + current[1]

                if Node.in_bounds(mapdata, (nx, ny)):
                    is_goal = Node.is_cell_walkable(mapdata, (nx, ny))

                    if is_goal == True: # walkable cell found!
                        return (nx,ny)
                    
                    elif is_goal == False: # not walkable cell
                        if (nx, ny) not in searched and (nx, ny) not in not_searched: # has not been current yet
                            not_searched.append((nx, ny))
                            continue