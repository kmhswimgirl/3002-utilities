import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle
from typing import Iterable, Tuple, Optional

from final_demo.search import Node, OccupancyGrid

Coord = Tuple[int, int]

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

map_80 = OccupancyGrid(10, 10, [
    1,0,0,1,0,1,1,1,1,1,
    1,1,1,1,1,1,0,1,1,1,
    1,1,1,1,1,1,1,0,1,1,
    1,0,1,1,0,1,1,1,1,0,
    1,1,1,0,0,1,0,1,0,1,
    1,0,1,1,1,1,1,1,1,1,
    1,0,0,1,1,1,1,1,1,1,
    0,0,1,1,1,0,0,1,1,1,
    1,1,1,0,0,1,0,1,1,1,
    0,1,1,1,1,0,1,0,1,1
])

map_90 = OccupancyGrid(10, 10, [
    1,1,1,1,1,0,1,1,1,1,
    0,1,0,1,1,0,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,0,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,0,1,0,1,
    1,1,1,1,1,1,1,1,1,1,
    0,1,1,1,1,1,1,1,1,1,
    1,1,1,1,1,1,0,1,0,1,
    1,1,1,1,1,1,1,1,1,1
])


def show_grid(values: Iterable[int], width: int = 10, height: int = 10, figsize: Tuple[int,int]=(6,6)):
    arr = np.asarray(values, dtype=int)
    if arr.size != width * height:
        raise ValueError(f"expected {width*height} values, got {arr.size}")
    grid = arr.reshape((height, width))

    cmap = ListedColormap(["white", "black"])  # 0->white, 1->black
    fig, ax = plt.subplots(figsize=figsize)
    ax.imshow(grid, cmap=cmap, origin="upper", interpolation="nearest", vmin=0, vmax=1)

    ax.set_xticks(np.arange(width))
    ax.set_yticks(np.arange(height))
    ax.set_xticklabels(np.arange(width))
    ax.set_yticklabels(np.arange(height))

    ax.set_xticks(np.arange(-0.5, width, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, height, 1), minor=True)
    ax.grid(which="minor", color="gray", linewidth=0.5)
    ax.set_xlim(-0.5, width - 0.5)
    ax.set_ylim(-0.5, height - 0.5)
    ax.set_aspect("equal")
    return fig, ax


def resolve_to_index(val, width: int, height: int) -> Optional[int]:
    if isinstance(val, int):
        return val
    if isinstance(val, (tuple, list)) and len(val) == 2:
        r, c = int(val[0]), int(val[1])
        if 0 <= r < height and 0 <= c < width:
            return r * width + c
        if 0 <= r < width and 0 <= c < height:
            return c * width + r
    return None


if __name__ == "__main__":
    start = (3, 5)  # grid coords (row, col)
    nearest = Node.nearest_walkable_cell(map_90, start)
    print("raw nearest return:", nearest, type(nearest))

    vals = map_90.data
    fig, ax = show_grid(vals, map_90.width, map_90.height, figsize=(6, 6))

    # annotate grid with flat indices for debugging
    for r in range(map_90.height):
        for c in range(map_90.width):
            idx = r * map_90.width + c
            ax.text(c, r, str(idx), ha="center", va="center", color="red", fontsize=6, zorder=6)

    idx = resolve_to_index(nearest, map_90.width, map_90.height)
    if idx is None:
        print("could not resolve nearest:", nearest)
    else:
        print("resolved index:", idx)
        r = idx // map_90.width
        c = idx % map_90.width
        rect = Rectangle((c - 0.5, r - 0.5), 1.0, 1.0,
                         facecolor='blue', edgecolor='black', alpha=0.6, zorder=7)
        ax.add_patch(rect)

    plt.show()