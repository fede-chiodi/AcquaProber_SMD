import sys
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap
import os
from GUI.views.timer_window import TimerPopup
import json

class FeederWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FEEDER")
        self.setStyleSheet("background-color: #010512; color: white;")
        self.resize(1024, 768)

        main_layout = QVBoxLayout()

        title_label = QLabel("FEEDER")
        title_label.setFont(QFont("Arial", 30, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("margin-left: 40px; margin-bottom: 30px;")
        main_layout.addWidget(title_label)

        body_layout = QHBoxLayout()

        # TIMER SECTION
        body_layout.addSpacing(50)
        timer_layout = QVBoxLayout()
        timer_label = QLabel("Timer")
        timer_label.setFont(QFont("Arial", 14, QFont.Bold))
        timer_label.setAlignment(Qt.AlignCenter)
        timer_layout.addWidget(timer_label)
        self.time_label = QLabel("--h --m --s")
        self.time_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.time_label.setAlignment(Qt.AlignCenter)
        timer_layout.addWidget(self.time_label)
        timer_layout.addSpacing(30)
        change_button = QPushButton("CAMBIA")
        change_button.setFont(QFont("Arial", 14, QFont.Bold))
        change_button.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                color: white;
                font-weight: bold;
                padding: 10px;
                border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #3a3aff, stop:1 #9f00ff);
            }
            QPushButton:hover {
                border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #3a3aff, stop:1 #9f00ff);
            }
        """)
        change_button.setFixedSize(200, 50)
        change_button.clicked.connect(self.change_timer_window)
        timer_layout.addWidget(change_button)

        body_layout.addLayout(timer_layout)
        body_layout.addSpacing(100)

        # NUTRITION INFORMATION SECTION
        nutrition_info = QVBoxLayout()
        last_nutrition_label = QLabel("Ultima Nutrizione")
        last_nutrition_label.setFont(QFont("Arial", 14, QFont.Bold))
        last_nutrition_label.setAlignment(Qt.AlignCenter)
        nutrition_info.addWidget(last_nutrition_label)
        self.last_nutrition_time_label = QLabel("--h --m --s")
        self.last_nutrition_time_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.last_nutrition_time_label.setAlignment(Qt.AlignCenter)
        nutrition_info.addWidget(self.last_nutrition_time_label)
        next_nutrition_label = QLabel("Prossima Nutrizione")
        next_nutrition_label.setFont(QFont("Arial", 14, QFont.Bold))
        next_nutrition_label.setAlignment(Qt.AlignCenter)
        nutrition_info.addWidget(next_nutrition_label)
        self.next_nutrition_time_label = QLabel("--h --m --s")
        self.next_nutrition_time_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.next_nutrition_time_label.setAlignment(Qt.AlignCenter)
        nutrition_info.addWidget(self.next_nutrition_time_label)

        body_layout.addLayout(nutrition_info)

        # FEED LEVEL
        feed_layout = QVBoxLayout()

        feed_level_label = QLabel("LIVELLO MANGIME")
        feed_level_label.setFont(QFont("Arial", 14, QFont.Bold))
        feed_level_label.setAlignment(Qt.AlignCenter)
        feed_layout.addWidget(feed_level_label)
        self.feed_level_value_label = QLabel("--")
        self.feed_level_value_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.feed_level_value_label.setAlignment(Qt.AlignCenter)
        feed_layout.addWidget(self.feed_level_value_label)

        body_layout.addLayout(feed_layout)

        main_layout.addLayout(body_layout)

        logo_label = QLabel()
        logo_path = os.path.join("GUI/images", "acquaprober_logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            logo_label.setStyleSheet("margin: 15px; margin-left: 70px;")
            main_layout.addWidget(logo_label)

        close_window_button = QPushButton("CHIUDI")
        close_window_button.setFont(QFont("Arial", 14, QFont.Bold))
        close_window_button.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                color: white;
                font-weight: bold;
                padding: 10px;
                border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #3a3aff, stop:1 #9f00ff);
            }
            QPushButton:hover {
                border: 2px solid qlineargradient(x1:0, y1:0, x2:1, y2:1,
                              stop:0 #3a3aff, stop:1 #9f00ff);
            }
        """)
        close_window_button.clicked.connect(self.close)
        main_layout.addWidget(close_window_button)

        self.setLayout(main_layout)

        self.refresh_labels_from_file()
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_labels_from_file)
        self.timer.start(100)

    def change_timer_window(self):
        self.timer_popup = TimerPopup(self)
        self.timer_popup.set_confirm_callback(self.update_timer_label)
        self.timer_popup.show()

    def update_timer_label(self, time_tuple):
        if time_tuple is None:
            return  
        hours, minutes, seconds = time_tuple
        self.update_data(hours, minutes, seconds)
        self.refresh_labels_from_file()



    def update_data(self, hours, minutes, seconds):
        total_sec_tim = hours * 3600 + minutes * 60 + seconds
        file_path = "data/settings.json"

        data = {}
        with open(file_path, "r") as file:
            data = json.load(file)

        data["feeder_time"] = total_sec_tim

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def refresh_labels_from_file(self):
        file_path = "data/settings.json"
        try:
            with open(file_path, "r") as file:
                data = json.load(file)

            self.last_nutrition_time_label.setText(data.get("last_feed", "--:--"))
            self.next_nutrition_time_label.setText(data.get("next_feed", "--:--"))
            self.feed_level_value_label.setText(data.get("feed_level", "--:--"))
            if data.get("food_level", 0) > 10:
                self.feed_level_value_label.setText("BUONO")
                self.feed_level_value_label.setStyleSheet("color: green;")
            elif 5 < data.get("food_level", 0)  <= 10:
                self.feed_level_value_label.setText("MEDIO")
                self.feed_level_value_label.setStyleSheet("color: yellow;")
            elif data.get("food_level", 0) <= 5:
                self.feed_level_value_label.setText("MALE")
                self.feed_level_value_label.setStyleSheet("color: red;")

            feeder_time = data.get("feeder_time", 0)
            h = feeder_time // 3600
            m = (feeder_time % 3600) // 60
            s = feeder_time % 60
            self.time_label.setText(f"{h:02d}h {m:02d}m {s:02d}s")

        except FileNotFoundError:
            print("File impostazioni non trovato.")
        except Exception as e:
            print("Errore nella lettura del file:", e)
