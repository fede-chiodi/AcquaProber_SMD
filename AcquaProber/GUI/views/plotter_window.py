import sys
from PyQt5.QtWidgets import (
            QWidget, QLabel, QSlider, QPushButton, QVBoxLayout, QHBoxLayout
        )
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class PlotterWindow(QWidget):
    def __init__(self, shared_dict):
        super().__init__()
        self.setWindowTitle("SONDA")
        self.setStyleSheet("background-color: #010512; color: white;")
        self.resize(1024, 768)
        self.shared_dict = shared_dict
        self.shared_dict["mode"] = 1
        self.shared_dict["x_pos"] = 0
        self.shared_dict["y_pos"] = 0
        self.init_ui()

    def init_ui(self):
        title = QLabel("Sonda")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        header_layout = QHBoxLayout()
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addSpacing(30)  

        stream = QLabel("STREAM")
        stream.setFont(QFont("Arial", 24, QFont.Bold))
        stream.setAlignment(Qt.AlignCenter)
        stream.setStyleSheet("color: white; background-color: lightgray;")
        stream.setFixedSize(500, 300)

        self.slider_y = QSlider(Qt.Vertical)
        self.slider_y.setRange(0, 100)
        self.slider_y.setValue(0)
        self.slider_y.setFixedSize(60, 300) 
        self.slider_y.setStyleSheet(self.slider_style())
        self.slider_y.valueChanged.connect(self.update_y_pos)

        slider_y_layout = QVBoxLayout()
        slider_y_layout.addWidget(self.slider_y)
        slider_y_layout.setAlignment(Qt.AlignCenter)

        center_layout = QHBoxLayout()
        center_layout.addSpacing(110)
        center_layout.addWidget(stream)
        center_layout.addSpacing(50)
        center_layout.addLayout(slider_y_layout)
        center_layout.setAlignment(Qt.AlignCenter)

        self.slider_x = QSlider(Qt.Horizontal)
        self.slider_x.setRange(0, 100)
        self.slider_x.setValue(0)
        self.slider_x.setFixedWidth(500)
        self.slider_x.setStyleSheet(self.slider_style())
        self.slider_x.valueChanged.connect(self.update_x_pos)

        slider_x_container = QHBoxLayout()
        slider_x_container.addWidget(self.slider_x)
        slider_x_container.setAlignment(Qt.AlignCenter)

        close_window_button = QPushButton("CHIUDI")
        close_window_button.setStyleSheet(
            "color: black; font-size: 16px; font-weight: bold; "
            "margin: 40px; padding: 5px;"
        )
        close_window_button.clicked.connect(self.close)

        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(center_layout)
        main_layout.addLayout(slider_x_container)
        main_layout.addSpacing(10)
        main_layout.addWidget(close_window_button)
        #main_layout.addSpacing(100)

        self.setLayout(main_layout)

    def update_y_pos(self, value):
        self.shared_dict["y_pos"] = value
        print(f"y_pos updated: {value}")

    def update_x_pos(self, value):
        self.shared_dict["x_pos"] = value
        print(f"x_pos updated: {value}")

    def closeEvent(self, event):
        self.shared_dict["mode"] = 0
        print("Window closed. mode set to 0.")
        event.accept()

    def slider_style(self):
        return """
            .QSlider {
                min-height: 80px;
                max-height: 340px;
                min-width: 60px;
                max-width: 550px;
            }
            
            QSlider::groove:vertical {
                background: #1E1E1E;
                border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #3a3aff, stop:1 #9f00ff);
                width: 30px;
                height: 300px; 
                border-radius: 5px;
            }

            QSlider::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #3a3aff, stop:1 #9f00ff);
                height: 40px;
                width: 40px;
                margin: -10px;
                border-radius: 12px;
            }

            QSlider::groove:horizontal {
                background: #1E1E1E;
                border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #3a3aff, stop:1 #9f00ff);
                height: 30px;
                width: 500px;
                border-radius: 5px;
            }

            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #3a3aff, stop:1 #9f00ff);
                width: 40px;
                height: 40px;
                margin: -10px;
                border-radius: 12px;
            }
        """
