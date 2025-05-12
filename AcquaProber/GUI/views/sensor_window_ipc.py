from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import pyqtgraph as pg
import json
import os

class SensorWindow(QWidget):
    def __init__(self, sensor_name, unit, shared_dict):
        super().__init__()
        self.setWindowTitle(f"{sensor_name} - Monitoring")
        self.resize(1024, 768)
        self.sensor_name = sensor_name
        self.unit = unit
        self.datas = []
        self.shared_dict = shared_dict

        layout = QVBoxLayout()
        self.setStyleSheet("background-color: #010512; color: white;")

        title = QLabel(sensor_name)
        title.setFont(QFont("Arial", 28, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        info_layout = QHBoxLayout()

        self.current_value = QLabel("Valore attuale\n--")
        self.current_value.setFont(QFont("Arial", 18, QFont.Bold))
        self.current_value.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.current_value)

        self.state_label = QLabel("Stato\n--")
        self.state_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.state_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.state_label)

        self.avg_value_label = QLabel("Media dei valori\n--")
        self.avg_value_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.avg_value_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(self.avg_value_label)

        layout.addLayout(info_layout)

        self.advice_label = QLabel("Consigli riferiti allo stato")
        self.advice_label.setFont(QFont("Arial", 12))
        self.advice_label.setStyleSheet("color: orange;")
        # self.advice_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.advice_label)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#1E1E1E')
        self.plot_widget.showGrid(x=True, y=True)
        self.plot = self.plot_widget.plot(pen=pg.mkPen('cyan', width=2))
        layout.addWidget(self.plot_widget)

        close_window_button = QPushButton("CHIUDI")
        close_window_button.setStyleSheet("color: black; font-size: 16px; font-weight: bold; margin: 40px; padding: 5px;")
        close_window_button.clicked.connect(self.close)
        layout.addWidget(close_window_button)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(2000)

    def update_plot(self):
        value = self.shared_dict.get(self.sensor_name)
        avg = None
        if value is not None:
            self.datas.append(value)
            if len(self.datas) > 100:
                self.data = self.datas[-100:]

            self.plot.setData(self.datas)

        with open("data/sensors_datas.json", "r") as file:
            file_log = json.load(file)

        values = [entry[self.sensor_name] for entry in file_log if self.sensor_name in entry]
        if values:
            avg = sum(values) / len(values)
        
        if value is not None and avg is not None:
            self.current_value.setText(f"Valore attuale\n{value:.2f} {self.unit}")
            self.avg_value_label.setText(f"Media dei valori\n{avg:.2f} {self.unit}")
            self.update_state(value)

    def update_state(self, readed_value):
        state = "--"
        color = "white"
        advice = ""

        if self.sensor_name.lower() == "temperature":
            if readed_value < 20:
                state, color, advice = "Freddo", "blue", "Assicurarsi che l'acquario non sia freddo"
            elif 20 <= readed_value <= 26:
                state, color, advice = "Buono", "green", ""
            elif readed_value > 26:
                state, color, advice = "Caldo", "red", "Assciurarsi che l'acquario si trovi in un posto al fresco"
        
        elif self.sensor_name.lower() == "ph":
            if readed_value < 7:
                state, color, advice = "Acida", "red", "Utilizzare correttori di pH"
            elif readed_value == 7:
                state, color, advice = "Neutrale", "green", ""
            elif readed_value > 7:
                state, color, advice = "Basica", "blue", "Necessario abassare il pH (aggiungendo un acido)"

        elif self.sensor_name.lower() == "turbidity":
            if readed_value <= 1:
                state, color, advice =  "Cristallina", "#A7D8FF", ""
            elif 1 < readed_value <= 5:
                state, color, advice = "Leggermente Torbida", "#B3E0FF", "leggera filtrazione"
            elif 5 < readed_value <= 10:
                state, color, advice = "Moderatamente Torbida", "#80BFFF", "filtrazione avanzata con trattamenti chimici"
            elif 10 < readed_value <= 100:
                state, color, advice = "Torbida", "#A6D8A0", "filtrazione intensiva con uso di coagulanti"
            elif 100 < readed_value <= 1000:
                state, color, advice = "Molto Torbida", "#FFD700", "trattamento intensivo con disinfezione"
            elif readed_value > 1000:
                state, color, advice = "Estremamente Torbida", "#8B4513", "filtrazione avanzata immediata con controllo di emergenza"
        
        elif self.sensor_name.lower() == "conductivity":
            if readed_value <= 250:
                state, color, advice = "Bassa", "#A7D8FF", "Possibile integrazione di minerali"
            elif 250 < readed_value <= 500:
                state, color, advice = "Moderata", "#A6E1A1", "Monitoraggio continuo"
            elif 500 < readed_value <= 1000:
                state, color, advice = "Alta", "#FFD700", "Filtrazione e osmosi inverse e controllo della qualità"
            elif 1000 < readed_value <= 3000:
                state, color, advice = "Molto Alte", "#FFA500", "Desalinizzazione e trattamento"
            elif readed_value > 3000:
                state, color, advice = "Estremamente Alta", "#8B0000", "Desalinizzazione avanzata e monitoraggio costante"

        
        self.state_label.setTextFormat(Qt.RichText)
        self.state_label.setText(f"Stato<br><span style=\"color:{color};\">{state}</span>")
        self.advice_label.setText(advice)
