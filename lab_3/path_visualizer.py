from typing import Iterable, Sequence, Tuple, Optional
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
from line_of_sight import lines

Coord = Tuple[float, float]
Cell = Tuple[int, int]

class PathVisualizer:
    """Minimal grid visualizer with world-centered integer cell centers and no seams."""

    def __init__(self, grid_width: int = 25, grid_height: int = 25, cell_size: float = 1.0):
        self.w = int(grid_width)
        self.h = int(grid_height)
        self.cell_size = float(cell_size)

        # grid array: 0 = empty, 1 = filled
        self.grid = np.zeros((self.h, self.w), dtype=np.int8)

        # world origin centered on the grid: world x=0 maps to array index w//2
        self._x_offset = self.w // 2
        self._y_offset = self.h // 2
        self._world_x_labels = (np.arange(self.w) - self._x_offset).astype(int)
        self._world_y_labels = (np.arange(self.h) - self._y_offset).astype(int)

        # colormap: index 0 -> background, 1 -> filled
        self.cmap = ListedColormap(["white", "#ff6666"])

        # plotting objects
        self._fig, self._ax = plt.subplots()
        self._mesh = None
        self._line = None

        # build initial mesh
        self._create_mesh()
        self._setup_axes()

    def _create_mesh(self):
        # compute world-centered cell centers and edges
        x_centers = (np.arange(self.w) - self._x_offset) * self.cell_size
        y_centers = (np.arange(self.h) - self._y_offset) * self.cell_size
        left = x_centers[0] - 0.5 * self.cell_size
        bottom = y_centers[0] - 0.5 * self.cell_size
        x_edges = left + np.arange(self.w + 1) * self.cell_size
        y_edges = bottom + np.arange(self.h + 1) * self.cell_size

        # remove existing mesh if present
        if getattr(self, "_mesh", None) is not None:
            try:
                self._mesh.remove()
            except Exception:
                pass

        # pcolormesh avoids hairline seams between cells
        # pass 1D edge arrays and let Matplotlib choose shading mode
        self._mesh = self._ax.pcolormesh(
            x_edges, y_edges, self.grid, cmap=self.cmap, shading="auto", vmin=0, vmax=1
        )

        # fix axis limits to the edges
        self._ax.set_xlim(x_edges[0], x_edges[-1])
        self._ax.set_ylim(y_edges[0], y_edges[-1])
        self._ax.set_aspect("equal")

    def _setup_axes(self):
        # major ticks at integer world-centered cell centers
        x_centers = (np.arange(self.w) - self._x_offset) * self.cell_size
        y_centers = (np.arange(self.h) - self._y_offset) * self.cell_size
        left = x_centers[0] - 0.5 * self.cell_size
        minor_x = left + np.arange(self.w + 1) * self.cell_size
        minor_y = (np.arange(self.h) - self._y_offset) * self.cell_size
        self._ax.set_xticks(x_centers)
        self._ax.set_yticks(minor_y)
        self._ax.set_xticklabels(self._world_x_labels)
        self._ax.set_yticklabels(self._world_y_labels)
        self._ax.set_xticks(minor_x, minor=True)
        self._ax.set_yticks(minor_x, minor=True)
        self._ax.grid(which="minor", color="lightgray", linewidth=0.8)

        # move spines so axes cross at world (0,0)
        try:
            self._ax.spines["left"].set_position(("data", 0))
            self._ax.spines["bottom"].set_position(("data", 0))
        except Exception:
            self._ax.spines["left"].set_position("zero")
            self._ax.spines["bottom"].set_position("zero")
        self._ax.spines["right"].set_color("none")
        self._ax.spines["top"].set_color("none")
        self._ax.xaxis.set_ticks_position("bottom")
        self._ax.yaxis.set_ticks_position("left")

    # coordinate helpers -------------------------------------------------
    def world_to_index(self, x: int, y: int) -> Tuple[int, int]:
        return int(x + self._x_offset), int(y + self._y_offset)

    def index_to_world(self, ix: int, iy: int) -> Tuple[int, int]:
        return int(ix - self._x_offset), int(iy - self._y_offset)

    # grid mutation -----------------------------------------------------
    def set_cells(self, cells: Iterable[Cell], value: int = 1):
        for x, y in cells:
            ix, iy = self.world_to_index(x, y)
            if 0 <= ix < self.w and 0 <= iy < self.h:
                self.grid[iy, ix] = 1 if value else 0
        self._update_image()

    def clear_cells(self):
        self.grid.fill(0)
        self._update_image()

    def toggle_cell(self, x: int, y: int):
        ix, iy = self.world_to_index(x, y)
        if 0 <= ix < self.w and 0 <= iy < self.h:
            self.grid[iy, ix] = 0 if self.grid[iy, ix] else 1
            self._update_image()

    # drawing -----------------------------------------------------------
    def plot_path(self, points: Sequence[Coord], color: str = "blue", linewidth: float = 2.0):
        pts = np.asarray(points, dtype=float)
        if pts.ndim != 2 or pts.shape[1] != 2:
            raise ValueError("points must be a sequence of (x,y) pairs")
        if self._line is None:
            self._line, = self._ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=linewidth, zorder=3)
            self._ax.scatter(pts[0, 0], pts[0, 1], color="green", zorder=4, label="start")
            self._ax.scatter(pts[-1, 0], pts[-1, 1], color="black", zorder=4, label="end")
            self._ax.legend(loc="upper right")
        else:
            self._line.set_data(pts[:, 0], pts[:, 1])
        self._ax.relim()
        self._ax.autoscale_view()

    def _update_image(self):
        # recreate mesh to update colors (simple and robust)
        self._create_mesh()
        self._fig.canvas.draw_idle()

    def show(self, block: bool = True):
        self._ax.set_title("Path + Grid Cell Visualizer")
        plt.show(block=block)

if __name__ == "__main__":
    vis = PathVisualizer(grid_width=25, grid_height=25, cell_size=1.0)
    start = (0, 0)
    end = [(7, 5), (-7, 5), (7, -5), (-7, -5)]

    # color cells along the line-of-sight (world coords)
    cells_1 = lines.line_of_sight_w(start, end[1])
    vis.set_cells(cells_1)

    c2 = lines.line_of_sight_w(start, end[0])
    vis.set_cells(c2)
    c3 = lines.line_of_sight_w(start, end[2])
    vis.set_cells(c3)
    c4 = lines.line_of_sight_w(start, end[3])
    vis.set_cells(c4)

    vis.plot_path([start, end[3]], color="blue", linewidth=2.5)

    vis.show()