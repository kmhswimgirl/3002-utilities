import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor, QMouseEvent
from PySide6 import QtWidgets

class Grid(QWidget):
    def __init__(self, grid_size=10, parent=None):
        super().__init__(parent)
        self.grid_size = grid_size
        self.setFixedSize(600, 600)  # square widget, only impacts size of wigit itself
        self.setStyleSheet("background-color: white; border: 2px solid black;")

        # occupancy grid data
        self.grid_data = None
        self.resolution = 0.05  # meters per grid square
        self.origin = [0.0, 0.0, 0.0]  # [x, y, yaw] in world coordinates
        self.occupied_thresh = 0.65
        self.free_thresh = 0.196
        self.negate = 0 
        self.show_grid_lines = True

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
        """Draw grid lines"""
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

    def pixel_to_grid(self, coords):
        x, y = coords[0], coords[1]

        widget_pixels = 600
        pix_per_cell = widget_pixels / self.grid_size
        x_grid = int(x / pix_per_cell)
        y_grid = int(y / pix_per_cell)

        return (x_grid, y_grid)

    def mousePressEvent(self, event: QMouseEvent): 
        pos = event.position() if hasattr(event, "position") else event.pos()
        grid_coords = (int(pos.x()), int(pos.y()))
        grid_xy = self.pixel_to_grid(grid_coords)
        # print(f"Mouse pressed at: {grid_xy}")