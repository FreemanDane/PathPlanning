from src.DataAnalysis import *
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont, QColor, QPolygon

class MapDisplay(QDialog):
    def __init__(self, filename, parent, title):
        super(MapDisplay, self).__init__(flags=0)
        self.map = map(filename)
        self.setWindowTitle("At Tsinghua")
        self.setFixedWidth(680)
        self.setFixedHeight(830)
        self.painter = QPainter(self)
        brush = QBrush()
        brush.setColor(QColor(227,174,222))
        self.painter.setBackground(brush)
    def map_render(self):
        for wy in self.map.ways:
            attrs = wy.attr
            try:
                x = attrs['surface']
                brush = QBrush()
                if x == 'paving_stones' or x == 'paved' or x == 'concrete:plates' or x == 'asphalt':
                    brush.setColor(QColor(157,145,170))
                elif x == 'earth':
                    brush.setColor((QColor(231,179,22)))
                points = []
                length = len(wy.point) - 1
                for i in range(length):
                    points.append(wy.point[i])
                self.painter.setBrush(brush)
                self.painter.drawPolygon(QPolygon(points),4)
            except:
                continue

