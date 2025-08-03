from PySide6.QtWidgets import QWidget
from PySide6 import QtWidgets

class MapParams(QWidget): # parameters that get exported to the yaml file
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(150,150)

        b1 = QtWidgets.QPushButton("Button 1")
        b2 = QtWidgets.QPushButton("Button 2")
        b3 = QtWidgets.QPushButton("Button 3")

        panel_layout = QtWidgets.QVBoxLayout()
        panel_layout.addWidget(b1)
        panel_layout.addWidget(b2)
        panel_layout.addWidget(b3)
        self.setLayout(panel_layout)