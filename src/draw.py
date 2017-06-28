from src.DataAnalysis import *
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont, QColor

a = QDialog()
class MapDisplay(QDialog):
    def __init__(self, filename, parent, title):
        super()
        self.map = map(filename)


