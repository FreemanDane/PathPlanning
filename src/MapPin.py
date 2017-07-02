from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class MapPin(QLabel):
    change_cursor = pyqtSignal(str)
    def __init__(self, parent = None):
        super(MapPin, self).__init__(parent)
        self.isInInput = False
        self.isDisplay = True
        self.color = "Blank"

    def mousePressEvent(self, event):
        if self.isDisplay == True:
            self.isDisplay = False
            if self.isInInput == True:
                self.setPixmap(QPixmap("../data/icons/pin/Pin_Blank.png"))
                self.change_cursor.emit(self.color)
            else:
                self.hide()