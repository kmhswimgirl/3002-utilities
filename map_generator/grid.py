import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor, QMouseEvent, QKeyEvent, QKeySequence
from dataclasses import dataclass

@dataclass
class GridCell:
    x: int
    y: int
    occ: int = -1 # 100 is occupied, 0 is free, -1 is unknown


class Grid(QWidget):
    def __init__(self, grid_size=20, parent=None):
        super().__init__(parent)
        self.grid_size = grid_size
        self.setFixedSize(600, 600)  # square widget, only impacts size of widget itself
        self.setStyleSheet("background-color: white; border: 2px solid black;")

        # occupancy grid data
        self.grid_data = None
        self.resolution = 0.05  # meters per grid square
        self.origin = [0.0, 0.0, 0.0]  # [x, y, yaw] in world coordinates
        self.occupied_thresh = 0.65
        self.free_thresh = 0.196
        self.negate = 0 
        self.show_grid_lines = True

        # init grid with GC objects
        self.grid_data = []
        for row in range(grid_size):
            for col in range(grid_size):
                self.grid_data.append(GridCell(col, row))  # x=col, y=row

        self.mouse_xy = None  

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # get widget dimensions
        width = self.width()
        height = self.height()

        if self.show_grid_lines:
            # draw grid lines
            self.draw_grid_lines(painter, width, height)

    def draw_grid_lines(self, painter, width, height):
        """draw grid lines"""
        # set pen for grid lines
        pen = QPen(Qt.GlobalColor.gray, 1, Qt.PenStyle.SolidLine)
        painter.setPen(pen)

        # default grid
        cell_width = width / self.grid_size
        cell_height = height / self.grid_size

        # vertical lines
        for i in range(self.grid_size + 1):
            x = int(i * cell_width)
            painter.drawLine(x, 0, x, height)

        # horizontal lines
        for i in range(self.grid_size + 1):
            y = int(i * cell_height)
            painter.drawLine(0, y, width, y)

    def toggle_grid_lines(self):
        """toggle grid lines on/off"""
        self.show_grid_lines = not self.show_grid_lines
        self.update()

    @staticmethod
    def pixel_to_grid(coords):
        x, y = coords[0], coords[1]
        widget_pixels = Grid().width()
        pix_per_cell = widget_pixels / Grid().grid_size
        x_grid = int(x / pix_per_cell)
        y_grid = int(y / pix_per_cell)
        return GridCell(x_grid, y_grid)
    
    @staticmethod
    def in_bounds(mouse_xy: tuple[int, int]):
        grid_height = Grid().height()
        grid_width = Grid().width()
        x, y = mouse_xy
        if 0 <= x < grid_width and 0 <= y < grid_height:
            return True
        else:
            return False

    def _get_grid_cell_from_event(self, event: QMouseEvent) -> GridCell:
        """mouse event --> grid coords"""
        pos = event.position() if hasattr(event, "position") else event.pos()
        coords_px = (int(pos.x()), int(pos.y()))
        return Grid.pixel_to_grid(coords_px)

    def mousePressEvent(self, event: QMouseEvent): 
        grid_cell = self._get_grid_cell_from_event(event)
        if not Grid.in_bounds:
            print(f"out of bounds: ({grid_cell.x}, {grid_cell.y})")
        print(f"Mouse pressed at: ({grid_cell.x}, {grid_cell.y})")

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = event.position() if hasattr(event, "position") else event.pos()
        coords_px = (int(pos.x()), int(pos.y()))
        if event.buttons() & Qt.MouseButton.LeftButton and Grid.in_bounds(coords_px):
            grid_cell = self._get_grid_cell_from_event(event)
            print(f"Mouse dragged @: ({grid_cell.x}, {grid_cell.y})")