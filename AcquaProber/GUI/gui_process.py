import sys
from PyQt5.QtWidgets import QApplication
from .views.gui_main import MainWindow

def run_gui(shared_dict):
    app = QApplication(sys.argv)
    window = MainWindow(shared_dict)
    window.show()
    sys.exit(app.exec_())
