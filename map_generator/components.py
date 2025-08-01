import os
import yaml
from PIL import Image
import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor

class Grid(QWidget):
    def __init__(self, grid_size=10, parent=None):
        super().__init__(parent)
        self.grid_size = grid_size
        self.setFixedSize(600, 600)  # Square widget
        self.setStyleSheet("background-color: white; border: 2px solid black;")
        
        # Occupancy grid data
        self.grid_data = None
        self.resolution = 0.05  # meters per pixel
        self.origin = [0.0, 0.0, 0.0]  # [x, y, yaw] in world coordinates
        self.occupied_thresh = 0.65
        self.free_thresh = 0.196
        self.negate = 0 
        self.show_grid_lines = True
    
    def find_pgm_file(self, yaml_file):
        """Find the corresponding PGM file for a YAML file"""
        # First try the same directory with .pgm extension
        pgm_file = yaml_file.replace('.yaml', '.pgm').replace('.yml', '.pgm')
        if os.path.exists(pgm_file):
            return pgm_file
        
        # Try reading the image path from YAML
        try:
            with open(yaml_file, 'r') as f:
                metadata = yaml.safe_load(f)
            image_path = metadata.get('image', '')
            if image_path:
                # Try relative to YAML file directory
                yaml_dir = os.path.dirname(yaml_file)
                full_path = os.path.join(yaml_dir, image_path)
                if os.path.exists(full_path):
                    return full_path
        except:
            pass
        return None

    def load_occupancy_grid(self, pgm_file, yaml_file):
        """Load occupancy grid from PGM and YAML files"""
        try:
            # Load YAML metadata
            with open(yaml_file, 'r') as f:
                metadata = yaml.safe_load(f)

            # Extract parameters from YAML
            self.resolution = metadata.get('resolution', 0.05)
            self.origin = metadata.get('origin', [0.0, 0.0, 0.0])
            self.occupied_thresh = metadata.get('occupied_thresh', 0.65)
            self.free_thresh = metadata.get('free_thresh', 0.196)
            self.negate = metadata.get('negate', 0)

            # Load PGM image
            image = Image.open(pgm_file).convert('L')  # Convert to grayscale
            self.grid_data = np.array(image)

            # Apply negation if specified
            if self.negate:
                self.grid_data = 255 - self.grid_data

            # Update grid size based on image dimensions
            self.grid_size = max(self.grid_data.shape)

            # Trigger repaint
            self.update()

            return True, "Grid loaded successfully"

        except Exception as e:
            return False, f"Error loading grid: {str(e)}"

    def get_cell_type(self, value):
        """Determine cell type based on occupancy value"""
        # Convert to probability (0-1 scale)
        prob = value / 255.0

        # In ROS occupancy grids:
        # - Values closer to 0 (black) = occupied
        # - Values closer to 1 (white) = free
        # - Values around 0.5 (gray) = unknown

        if prob <= self.free_thresh:
            return "occupied"  # Low probability = occupied
        elif prob >= self.occupied_thresh:
            return "free"  # High probability = free
        else:
            return "unknown"  # In between = unknown

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Get widget dimensions
        width = self.width()
        height = self.height()

        if self.grid_data is not None:
            # Draw occupancy grid
            self.draw_occupancy_grid(painter, width, height)

        if self.show_grid_lines:
            # Draw grid lines
            self.draw_grid_lines(painter, width, height)

    def draw_occupancy_grid(self, painter, width, height):
        """Draw the occupancy grid based on loaded data"""
        if self.grid_data is None:
            return

        grid_height, grid_width = self.grid_data.shape

        cell_width = width / grid_width
        cell_height = height / grid_height

        for y in range(grid_height):
            for x in range(grid_width):
                value = self.grid_data[y, x]
                cell_type = self.get_cell_type(value)
                
                # Choose color based on cell type
                if cell_type == "occupied":
                    color = QColor(0, 0, 0)  # Black for occupied
                elif cell_type == "free":
                    color = QColor(255, 255, 255)  # White for free
                else:
                    color = QColor(128, 128, 128)  # Gray for unknown

                # Draw filled rectangle for this cell
                painter.fillRect(
                    int(x * cell_width),
                    int(y * cell_height),
                    int(cell_width) + 1,
                    int(cell_height) + 1,
                    color
                )

    def draw_grid_lines(self, painter, width, height):
        """Draw grid lines"""
        # Set pen for grid lines
        pen = QPen(Qt.GlobalColor.gray, 1, Qt.PenStyle.SolidLine)
        painter.setPen(pen)

        if self.grid_data is not None:
            grid_height, grid_width = self.grid_data.shape
            cell_width = width / grid_width
            cell_height = height / grid_height

            # Draw vertical lines
            for i in range(grid_width + 1):
                x = int(i * cell_width)
                painter.drawLine(x, 0, x, height)

            # Draw horizontal lines
            for i in range(grid_height + 1):
                y = int(i * cell_height)
                painter.drawLine(0, y, width, y)
        else:
            # Draw simple grid if no data loaded
            cell_width = width / self.grid_size
            cell_height = height / self.grid_size

            # Draw vertical lines
            for i in range(self.grid_size + 1):
                x = int(i * cell_width)
                painter.drawLine(x, 0, x, height)

            # Draw horizontal lines
            for i in range(self.grid_size + 1):
                y = int(i * cell_height)
                painter.drawLine(0, y, width, y)

    def toggle_grid_lines(self):
        """Toggle grid lines on/off"""
        self.show_grid_lines = not self.show_grid_lines
        self.update()

    def get_grid_info(self):
        """Get information about the current grid"""
        if self.grid_data is not None:
            # Count cells based on probability thresholds
            prob_data = self.grid_data / 255.0
            occupied = np.sum(prob_data <= self.free_thresh)
            free = np.sum(prob_data >= self.occupied_thresh)
            unknown = self.grid_data.size - occupied - free
            
            return {
                'resolution': self.resolution,
                'origin': self.origin,
                'size': self.grid_data.shape,
                'occupied_cells': occupied,
                'free_cells': free,
                'unknown_cells': unknown,
                'occupied_thresh': self.occupied_thresh,
                'free_thresh': self.free_thresh,
                'negate': self.negate
            }
        else:
            return {
                'resolution': self.resolution,
                'origin': self.origin,
                'size': (self.grid_size, self.grid_size),
                'occupied_cells': 0,
                'free_cells': 0,
                'unknown_cells': 0,
                'occupied_thresh': self.occupied_thresh,
                'free_thresh': self.free_thresh,
                'negate': self.negate
            }

    def get_formatted_grid_info(self):
        """Return formatted info about the grid."""
        info = [
            f"Grid size: {self.grid_size}",
            f"Resolution: {getattr(self, 'resolution', 'N/A')}",
            f"Origin: {getattr(self, 'origin', 'N/A')}",
            f"Occupied threshold: {getattr(self, 'occupied_thresh', 'N/A')}",
            f"Free threshold: {getattr(self, 'free_thresh', 'N/A')}",
            f"Negate: {getattr(self, 'negate', 'N/A')}",
        ]
        return info

class MapSpecs:
    def __init__(self):
        pass