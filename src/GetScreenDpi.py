from PyQt5.QtWidgets import *
import platform

app = QApplication([])
screen = app.desktop()

def get_dpi_rate():
    if platform.system() == "Windows":
        return 96 / screen.logicalDpiX()
    else:
        return 1