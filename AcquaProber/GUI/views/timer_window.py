from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSpinBox, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TimerPopup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(parent.size())
        self.setStyleSheet("background-color: #010512")

        self.popup = QWidget(self)
        self.popup.setFixedSize(600, 400)
        self.popup.move((self.width() - 600) // 2, (self.height() - 400) // 2)
        self.popup.setStyleSheet("""
            QWidget {
                background-color: #010512;
                color: white;
                border: 3px solid #00bfff;
                border-radius: 10px;
            }
        """)

        layout = QVBoxLayout(self.popup)
        layout.setSpacing(20)

        title_label = QLabel("Imposta nuovo timer")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("border: none;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        time_layout = QHBoxLayout()
        time_layout.setSpacing(20)

        self.hour_spin = self._create_spinbox()
        time_layout.addLayout(self._wrap_spinbox("Ore", self.hour_spin))

        self.minute_spin = self._create_spinbox()
        time_layout.addLayout(self._wrap_spinbox("Minuti", self.minute_spin))

        self.second_spin = self._create_spinbox()
        time_layout.addLayout(self._wrap_spinbox("Secondi", self.second_spin))

        layout.addLayout(time_layout)

        warning_label = QLabel("*Attenzione, le modifiche avranno effetto a partire dalla prossima nutrizione")
        warning_label.setStyleSheet("color: red; border: none;")
        warning_label.setFont(QFont("Arial", 10))
        warning_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(warning_label)

        buttons = QHBoxLayout()

        confirm_button = QPushButton("Imposta")
        confirm_button.setFont(QFont("Arial", 14, QFont.Bold))
        confirm_button.setFixedSize(500, 100)
        confirm_button.clicked.connect(self.confirm)
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #1E1E1E;
                color: white;
                border: 2px solid #00bfff;
                border-radius: 5px;
                padding: 10px 20px;
                margin: 30px;
            }
            QPushButton:hover {
                background-color: #00bfff;
                color: black;
            }
        """)

        buttons.addWidget(confirm_button)
        layout.addLayout(buttons)

        self.confirm_callback = None

    def _create_spinbox(self):
        spinbox = QSpinBox()
        spinbox.setRange(0, 59)
        spinbox.setFont(QFont("Arial", 30))
        spinbox.setAlignment(Qt.AlignCenter)
        spinbox.setFixedSize(100, 50)
        spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #1E1E1E;
                color: white;
                padding: 5px;
                border: none;
                font-size: 30px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #1E1E1E;
                border-radius: 20px;
            }
        """)
        return spinbox

    def _wrap_spinbox(self, label_text, spinbox):
        layout = QVBoxLayout()
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        label.setStyleSheet("border: none;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        layout.addWidget(spinbox)
        return layout

    def confirm(self):
        time_tuple = self.get_time()
        if not time_tuple:
            return 
        if self.confirm_callback:
            self.confirm_callback(time_tuple)
        self.close()

    def get_time(self):
        if self.hour_spin.value() == 0 and self.minute_spin.value() < 5:
            message_box_error = QMessageBox()
            message_box_error.setIcon(QMessageBox.Critical)
            message_box_error.setText("ERRORE")
            message_box_error.setFixedSize(400, 600)
            message_box_error.setStyleSheet("color: red; font-size: 15px; font-weight: bold;")
            message_box_error.setInformativeText("INSERISCI UN TEMPO DI APERTURA\nMINIMO 5 MINUTI")
            message_box_error.setWindowTitle("Errore")
            message_box_error.exec_()
            return None
        else:
            return (
                self.hour_spin.value(),
                self.minute_spin.value(),
                self.second_spin.value()
            )

    def set_confirm_callback(self, callback):
        self.confirm_callback = callback
