from PySide6 import QtCore, QtWidgets
from components import MapSpecs, Grid # my components
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROS OccupancyGrid Creator")
        self.setGeometry(100, 100, 800, 600)

        # declare objects for sub grids/widgets
        grid = Grid()

        # central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        # layout
        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)

        # components
        label = QtWidgets.QLabel("Map Generator Application")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addWidget(label)
        layout.addWidget(grid)

        button = QtWidgets.QPushButton("Generate Map")
        layout.addWidget(button)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())