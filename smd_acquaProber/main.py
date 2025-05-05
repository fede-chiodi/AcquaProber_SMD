import sys
import time
from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QWidget,
    QVBoxLayout, QLabel, QHBoxLayout
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
import pyqtgraph as pg

from sensors.ph_sensor import read_ph
from sensors.turbidity_sensor import read_turbidity
from sensors.temperature_sensor import read_temperature
from sensors.conductivity_sensor import read_conductivity

class SensorWindow(QWidget):
    def __init__(self, sensor_name, read_function, unit):
        super().__init__()
        self.setWindowTitle(f"{sensor_name} - Monitoraggio")
        self.resize(800, 600)

        self.read_function = read_function
        self.unit = unit
        self.data = []
        self.timestamps = []

        layout = QVBoxLayout()
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot = self.plot_widget.plot(pen='b')
        layout.addWidget(self.plot_widget)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def update_data(self):
        value = self.read_function()
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.data.append(value)
        self.timestamps.append(timestamp)

        if len(self.data) > 100:
            self.data = self.data[-100:]
            self.timestamps = self.timestamps[-100:]

        self.plot.setData(list(range(len(self.data))), self.data)
        self.plot_widget.setTitle(f"{self.windowTitle()}")
        self.plot_widget.setLabel('left', f'Valore ({self.unit})')
        self.plot_widget.setLabel('bottom', 'Tempo')
        self.label.setText(f"Ultimo valore: {value} {self.unit}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Monitoraggio Acquario")
        self.showFullScreen()

        central_widget = QWidget()
        layout = QHBoxLayout()

        sensors = [
            ("pH", read_ph, "ph.png", "pH"),
            ("Torbidità", read_turbidity, "turbid.png", "NTU"),
            ("Temperatura", read_temperature, "temperature.png", "°C"),
            ("Conducibilità", read_conductivity, "conductivity.png", "µS/cm"),
        ]

        for name, func, icon, unit in sensors:
            button = QPushButton()
            button.setIcon(QIcon(f"icons/{icon}"))
            button.setIconSize(QtCore.QSize(100, 100))
            button.setFixedSize(120, 120)
            button.setToolTip(name)
            button.clicked.connect(lambda _, n=name, f=func, u=unit: self.open_sensor_window(n, f, u))
            layout.addWidget(button)

        exit_button = QPushButton("Esci")
        exit_button.setFixedSize(120, 40)
        exit_button.clicked.connect(QApplication.quit)
        layout.addWidget(exit_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_sensor_window(self, name, func, unit):
        self.sensor_window = SensorWindow(name, func, unit)
        self.sensor_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
