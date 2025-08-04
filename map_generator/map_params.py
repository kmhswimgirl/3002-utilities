from PySide6.QtWidgets import QWidget
from PySide6 import QtWidgets

class MapParams(QWidget): # parameters that get exported to the yaml file
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(150,150)

        panel_layout = QtWidgets.QVBoxLayout()
        label_widget = QWidget()
        resolution = self.label_plus_text_box("Resolution:", "m per grid square")
        origin = self.label_plus_text_box("Grid Origin:", "[x, y, yaw]")

        panel_layout.addLayout(resolution)
        panel_layout.addLayout(origin)

        panel_layout.addWidget(label_widget)
        self.setLayout(panel_layout)

    def label_plus_text_box(self, label:str, placeholder:str):
        layout = QtWidgets.QHBoxLayout()
        file_name_txt = QtWidgets.QLabel(f"{label}")
        file_name = QtWidgets.QLineEdit()
        file_name.setPlaceholderText(f'{placeholder}')
        layout.addWidget(file_name_txt)
        layout.addWidget(file_name)
        return layout