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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
