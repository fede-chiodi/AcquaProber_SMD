import sys
from datetime import datetime
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget,
    QVBoxLayout, QLabel, QHBoxLayout
)
import pyqtgraph as pg

from sensors.ph_sensor import read_ph
from sensors.turbidity_sensor import read_turbidity
from sensors.temperature_sensor import read_temperature
from sensors.conductivity_sensor import read_conductivity
from sensors.feeder_servo import open_valve, close_valve, is_valve_open, cleanup


class SensorWindow(QWidget):
    def __init__(self, sensor_name, read_function, unit):
        super().__init__()
        self.setWindowTitle(f"{sensor_name} - Monitoraggio")
        self.resize(900, 600)

        self.read_function = read_function
        self.unit = unit
        self.data = []
        self.timestamps = []

        layout = QVBoxLayout()
        self.setStyleSheet("background-color: #121212; color: white;")

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#121212')
        self.plot_widget.showGrid(x=True, y=True)
        self.plot = self.plot_widget.plot(pen=pg.mkPen('cyan', width=2))
        self.plot_widget.setLabel('left', f'Valore ({self.unit})', color='white')
        self.plot_widget.setLabel('bottom', 'Tempo', color='white')
        layout.addWidget(self.plot_widget)

        self.label = QLabel()
        self.label.setFont(QFont("Arial", 16))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(2000)

    def update_data(self):
        value = self.read_function()
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.data.append(value)
        self.timestamps.append(timestamp)

        if len(self.data) > 100:
            self.data = self.data[-100:]
            self.timestamps = self.timestamps[-100:]

        self.plot.setData(list(range(len(self.data))), self.data)
        self.plot_widget.setTitle(f"<span style='color:white;'>{self.windowTitle()}</span>")
        self.label.setText(f"Ultimo valore: <b>{value:.2f} {self.unit}</b>")

from sensors.feeder_servo import open_valve, close_valve, is_valve_open

class FeederWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Controllo Feeder")
        self.resize(400, 300)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel()
        self.status_label.setFont(QFont("Arial", 16))
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.control_button = QPushButton("Apri Valvola")
        self.control_button.setFont(QFont("Arial", 14))
        self.control_button.setFixedSize(200, 50)
        self.control_button.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #005F99;
            }
        """)
        self.control_button.clicked.connect(self.toggle_valve)
        layout.addWidget(self.control_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.update_status()

    def update_status(self):
        if is_valve_open():
            self.status_label.setText("Stato: <b style='color: lime;'>Aperta</b>")
            self.control_button.setText("Chiudi Valvola")
        else:
            self.status_label.setText("Stato: <b style='color: red;'>Chiusa</b>")
            self.control_button.setText("Apri Valvola")

    def toggle_valve(self):
        if is_valve_open():
            close_valve()
        else:
            open_valve()
        self.update_status()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitoraggio Acquario")
        self.resize(1024, 768)
        self.setStyleSheet("background-color: #1e1e1e;")

        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        sensors = [
            ("pH", read_ph, "ph.png", "pH"),
            ("Torbidità", read_turbidity, "turbid.png", "NTU"),
            ("Temperatura", read_temperature, "temperature.png", "°C"),
            ("Conducibilità", read_conductivity, "conductivity.png", "µS/cm"),
        ]

        for name, func, icon, unit in sensors:
            button = QPushButton()
            button.setIcon(QIcon(f"icons/{icon}"))
            button.setIconSize(QSize(100, 100))
            button.setFixedSize(130, 130)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2e2e2e;
                    border-radius: 15px;
                    border: 2px solid #444;
                }
                QPushButton:hover {
                    background-color: #444;
                    border: 2px solid cyan;
                }
            """)
            button.setToolTip(name)
            button.clicked.connect(lambda _, n=name, f=func, u=unit: self.open_sensor_window(n, f, u))
            button_layout.addWidget(button)

        layout.addLayout(button_layout)

        feeder_button = QPushButton()
        feeder_button.setIcon(QIcon("icons/feeder.jpg"))
        feeder_button.setIconSize(QSize(100, 100))
        feeder_button.setFixedSize(130, 130)
        feeder_button.setStyleSheet("""
            QPushButton {
                background-color: #2e2e2e;
                border-radius: 15px;
                border: 2px solid #444;
            }
            QPushButton:hover {
                background-color: #444;
                border: 2px solid cyan;
            }
        """)
        feeder_button.setToolTip("Feeder")
        feeder_button.clicked.connect(self.open_feeder_window)
        button_layout.addWidget(feeder_button)


        exit_button = QPushButton("Esci")
        exit_button.setFixedSize(150, 50)
        exit_button.setFont(QFont("Arial", 14))
        exit_button.setStyleSheet("""
            QPushButton {
                background-color: #ff4c4c;
                color: white;
                border-radius: 10px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #ff0000;
            }
        """)
        exit_button.clicked.connect(QApplication.quit)
        layout.addWidget(exit_button, alignment=Qt.AlignCenter)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_sensor_window(self, name, func, unit):
        self.sensor_window = SensorWindow(name, func, unit)
        self.sensor_window.show()
    
    def open_feeder_window(self):
        self.feeder_window = FeederWindow()
        self.feeder_window.show()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    finally:
        cleanup()
