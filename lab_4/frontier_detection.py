# lab 4 detecting frontiers from the occupancy grid
# 1D representation of the map (10x10 grid)

class Map:
    def __init__(self):
        self.data = [
             -1,   0,  -1,  -1,  -1,  -1,  -1,   0,  -1,  -1,
             -1,   0,  -1,  -1,   0,  -1,   0,   0,  -1,  -1,
             -1,   0,  -1,  -1,   0,  -1,   0,   0,  -1,  -1,
             -1,   0,  -1,  -1,   0,   0,   0,   0,  -1,  -1,
              0,   0,  -1,  -1,   0,   0,   0,   0,  -1,  -1,
            100,   0,   0,   0,   0,   0,   0,   0,   0,  -1,
            100,   0,   0,   0,   0,   0,   0,   0,   0,  -1,
            100,   0,   0,   0,   0,   0,   0, 100,   0, 100,
            100,   0,   0, 100, 100,   0,   0, 100,   0, 100,
            100, 100, 100, 100, 100, 100, 100, 100, 100, 100
        ]

        self.height = 10
        self.width = 10

# map utilities
def index_to_grid(index: int, width: int) -> tuple[int, int]:
   
    row = index // width
    col = index % width
    return (row, col)

def get_neighbors(cell, grid_shape):
    x, y = cell
    neighbors = []
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1),(1,1)]:  # 4-connected
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_shape[0] and 0 <= ny < grid_shape[1]:
            neighbors.append((nx, ny))
    return neighbors

# ============= Frontier Generation Code ===============
def get_frontier_cells(map:Map):
    frontier_cells = set()
    for index, cell in enumerate(map.data):
        if cell == 0:
            next_to_cells = get_neighbors(index, map.width, map.height)
            for item in next_to_cells:
                if map.data[item] == -1:
                    frontier_cells.add(index)
                    break
    return frontier_cells

def get_frontiers(map:Map, frontier_cells):
    # its a DFS, already have filtered out which cells are frontier cells... 
    pass

