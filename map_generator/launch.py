from PySide6 import QtCore, QtWidgets
from grid import Grid # my components
from side_panels import MapSpecs
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # central widget (main window)
        self.setWindowTitle("ROS OccupancyGrid & 2D Map Creator")
        self.setGeometry(100, 100, 800, 600)
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)

        # top level layout  --> vertical, contains text box, 
        layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(layout)

        # sub layout 1 --> horizontal, contains grid & control panel 
        lay_1 = QtWidgets.QHBoxLayout()

        # declare objects for sub widgets
        grid = Grid()
        yaml_panel = MapSpecs()

        # name map text box, to get file name for use later, 
        # use the callback: "file_name.text()"
        file_name = QtWidgets.QLineEdit()
        file_name.setPlaceholderText('enter map name here')
        layout.addWidget(file_name)

        button = QtWidgets.QPushButton("Generate Map")

        # things added to sub layout 1
        lay_1.addWidget(yaml_panel)
        lay_1.addWidget(grid)
        lay_1.addWidget(button)

        # add the sub layout to the main layout
        layout.addLayout(lay_1)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())