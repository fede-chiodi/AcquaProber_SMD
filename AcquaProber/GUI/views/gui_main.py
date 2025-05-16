from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QGridLayout, QDialog, QFrame
from PyQt5.QtGui import QPixmap, QFont, QIcon, QCursor
from PyQt5.QtCore import Qt, QTimer
from GUI.views.sensor_window_ipc import SensorWindow
from GUI.views.info_window import InfoWindow
from GUI.views.plotter_window import PlotterWindow
from GUI.views.feeder_window import FeederWindow
import os

class MainWindow(QMainWindow):
    def __init__(self, shared_dict):
        super().__init__()
        self.setWindowTitle("ACQUAPROBER DASHOBARD")
        self.setStyleSheet("background-color: #010512; color: white;")
        self.resize(1024, 768)
        self.shared_dict = shared_dict

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        
        sensor_frame = QFrame()
        sensor_frame.setStyleSheet("""
            QFrame {
                border: 2px solid #007ACC;
                border-radius: 10px;
                padding: 1px;
                background-color: #010512; 
            }
        """)
        sensor_frame.setMaximumHeight(100)

        sensor_layout = QGridLayout()
        sensors_type = [
            ("pH", "pH"),
            ("Turbidity", "NTU"),
            ("Temperature", "°C"),
            ("TDS", "ppm")
        ]
        self.value_labels = {}

        for i, (name, unit) in enumerate(sensors_type):
            label_title = QLabel(name)
            label_title.setFont(QFont("Arial", 12, QFont.Bold))
            label_title.setStyleSheet("color: white; border: none;")
            label_title.setAlignment(Qt.AlignCenter)
            label_title.setCursor(QCursor(Qt.PointingHandCursor))
            label_title.mousePressEvent = lambda _, n=name, u=unit: self.open_sensor_window(n, u, self.shared_dict)

            label_value = QLabel("--")
            label_value.setFont(QFont("Arial", 18, QFont.Bold))
            label_value.setStyleSheet("color: cyan; border: none;")
            label_value.setAlignment(Qt.AlignCenter)
            

            sensor_layout.addWidget(label_title, 0, i)
            sensor_layout.addWidget(label_value, 1, i)
            self.value_labels[name] = label_value;

        sensor_frame.setLayout(sensor_layout)
        main_layout.addWidget(sensor_frame)

        logo_label = QLabel()
        logo_path = os.path.join("GUI/images", "acquaprober_logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            main_layout.addWidget(logo_label)

        buttons_layout = QHBoxLayout()
        for label in ["Sonda", "Info", "Feeder"]:
            btn = QPushButton(label)
            btn.setFixedSize(200, 70)
            btn.setStyleSheet("""
                QPushButton {
                    background-color #1E1E1E;
                    color: white;
                    border: 2px solid #007ACC;
                    border-radius: 10px;
                    padding: 8px;
                    font-size: 20px;
                    font-weight: bold;
                    margin-top: 10px;
                }

                QPushButton:hover {
                    background-color: #007ACC;
                    color: black;
                }
            """)
            btn.clicked.connect(lambda _, l=label: self.open_placeholder_window(l, self.shared_dict))
            buttons_layout.addWidget(btn)

        main_layout.addLayout(buttons_layout)
        central_widget.setLayout(main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_values)
        self.timer.start(2000)

    def update_values(self):
        for name in self.value_labels:
            if name in self.shared_dict:
                value = self.shared_dict[name]
                self.value_labels[name].setText(f"{value:.1f}")

    def open_sensor_window(self, name, unit, shared_dict):
        self.sensor_window = SensorWindow(name, unit, shared_dict)
        self.sensor_window.show()

    def open_placeholder_window(self, btn_name, shared_dict):
        if btn_name == "Info":
            self.info_window = InfoWindow(btn_name)
            self.info_window.show()
        elif btn_name == "Sonda":
            self.plotter_window = PlotterWindow(shared_dict)
            self.plotter_window.show()
        elif btn_name == "Feeder":
            self.feeder_window = FeederWindow()
            self.feeder_window.show()
