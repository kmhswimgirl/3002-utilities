import sys
from PySide6 import QtWidgets
from grid import Grid 
from map_params import MapParams # side panel that determines the yaml file

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # central widget (main window)
        self.setWindowTitle("ROS OccupancyGrid & 2D Map Creator")
        self.setGeometry(100, 100, 1000, 600)
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)

        # top level layout  --> vertical, top item is file text box, 
        layout = QtWidgets.QVBoxLayout()
        main_widget.setLayout(layout)

        # add the sub layout to the main layout
        layout.addLayout(self.top_bar_layout())
        layout.addLayout(self.main_layout())

    # =============== Sub Layouts ===================
    def top_bar_layout(self):
        """top bar with file name input and button"""
        layout = QtWidgets.QHBoxLayout()
        file_name_txt = QtWidgets.QLabel("File Name:")
        file_name = QtWidgets.QLineEdit()
        file_name.setPlaceholderText('enter map name here')
        button = QtWidgets.QPushButton("Generate Map")
        layout.addWidget(file_name_txt)
        layout.addWidget(file_name)
        layout.addWidget(button)
        return layout

    def main_layout(self):
        """main horizontal layout with sidebar and grid"""
        layout = QtWidgets.QHBoxLayout()
        yaml_panel = MapParams()
        grid = Grid()
        layout.addWidget(yaml_panel)
        layout.addWidget(grid)
        return layout

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
