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
    """
    Convert a 1D index to (row, col) coordinates for a grid of given width.
    Args:
        index (int): The 1D index in the map array.
        width (int): The width of the grid.
    Returns:
        tuple[int, int]: (row, col) coordinates.
    """
    row = index // width
    col = index % width
    return (row, col)


def neighbors_8(index: int, width: int, height: int) -> list[int]:
    """
    Get the 8-connected neighbors of a cell in a 1D grid map.
    Args:
        index (int): The 1D index in the map array.
        width (int): The width of the grid.
        height (int): The height of the grid.
    Returns:
        list[int]: List of 1D indices of valid 8-connected neighbors.
    """
    row, col = index_to_grid(index, width)
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = row + dr, col + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append(nr * width + nc)
    return neighbors

# ============= Frontier Generation Code ===============
def get_frontier_cells(map:Map):
    frontier_cells = set()
    for index, cell in enumerate(map.data):
        if cell == 0:
            next_to_cells = neighbors_8(index, map.width, map.height)
            for item in next_to_cells:
                if map.data[item] == -1:
                    frontier_cells.add(index)
                    break
    return frontier_cells

m = Map()
print(get_frontier_cells(m))