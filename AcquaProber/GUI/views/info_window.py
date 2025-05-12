from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap
import os

class InfoWindow(QWidget):
    def __init__(self, name):
        super().__init__()
        self.setWindowTitle("INFORMAZIONI ACQUARIO")
        self.resize(1024, 768)
        
        self.fish_list = {
            "Pesce Rosso": 5,
            "Carpa koi": 3,
            "Pesce Combattente": 2
        }

        main_layout = QVBoxLayout()
        self.setStyleSheet("background-color: #010512; color: white;")

        title = QLabel()
        title.setText("ACQUAPROBER INFO")
        title.setFont(QFont("Arial", 25, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("margin: 0; margin-bottom: 20px;")

        main_layout.addWidget(title)

        logo_label = QLabel()
        logo_path = os.path.join("GUI/images", "acquaprober_logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
            logo_label.setAlignment(Qt.AlignCenter)
            logo_label.setStyleSheet("margin: 15px;")
            main_layout.addWidget(logo_label)
        
        fish_layout = QVBoxLayout()
        fish_frame = QFrame()
        fish_frame.setStyleSheet("""
            QFrame {
                border: 3px solid #007ACC;
                border-radius: 10px;
            }
        """)
        for key, value in self.fish_list.items():
            fish_label = QLabel()
            fish_label.setText(f"{key} -- {value}")
            fish_label.setStyleSheet("color: white;  border: none;")
            fish_label.setFont(QFont("Arial", 15, QFont.Bold))
            fish_label.setAlignment(Qt.AlignCenter)

            fish_layout.addWidget(fish_label)
        
        fish_frame.setLayout(fish_layout)
        main_layout.addWidget(fish_frame)

        self.setLayout(main_layout)

