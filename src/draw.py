from src import DataAnalysis
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont, QColor, QPolygon
from PyQt5.QtCore import QPoint
import sys

class MapDisplay(QWidget):
    def __init__(self, filename, parent = None):
        super(MapDisplay, self).__init__()
        print('Loading Data...')
        self.map = DataAnalysis.map(filename)
        self.map.cross_list.cartesian_coordinate()
        print('Total {} nodes, {} ways.'.format(len(self.map.cross_list.nodes), len(self.map.ways)))
        self.initUI()

    def initUI(self):
        self.setWindowTitle("At Tsinghua")
        self.setFixedWidth(680)
        self.setFixedHeight(830)
        self.painter = QPainter()
        self.show()

    def map_render(self):
        print("render map")
        max_x = self.map.cross_list.farthest_node.x
        max_y = self.map.cross_list.farthest_node.y
        for wy in self.map.ways:
            attrs = wy.attr
            try:
                x = attrs['surface']
                if not x:
                    continue
            except KeyError:
                continue
            brush = QBrush()
            if x == 'paving_stones' or x == 'paved' or x == 'concrete:plates' or x == 'asphalt':
                brush.setColor(QColor(157, 145, 170))
            elif x == 'earth':
                brush.setColor((QColor(231, 179, 22)))
            polygon = QPolygon()
            length = len(wy.point) - 1
            for i in range(length):
                new_pt = self.map.cross_list.get_node(wy.point[i]['ref'])
                polygon.append(QPoint(new_pt.x * 680 / max_x, new_pt.y * 830 / max_y))
            self.painter.setBrush(brush)
            self.painter.drawPolygon(polygon)
        for wy in self.map.ways:
            attrs = wy.attr
            try:
                x = attrs['landuse']
                if not x:
                    continue
            except KeyError:
                continue
            brush = QBrush()
            if x == 'grass' or x == 'meadow':
                brush.setColor(QColor(55, 232, 30))
            elif x == 'forest':
                brush.setColor(QColor(75, 189, 72))
            elif x == 'commercial' or x == 'retail' or x == 'construction' or x == 'park' or x == 'residential':
                brush.setColor((QColor(134, 139, 122)))
            polygon = QPolygon()
            length = len(wy.point) - 1
            for i in range(length):
                new_pt = self.map.cross_list.get_node(wy.point[i]['ref'])
                polygon.append(QPoint(new_pt.x * 680 / max_x, new_pt.y * 830 / max_y))
            self.painter.setBrush(brush)
            self.painter.drawPolygon(polygon)
        for wy in self.map.ways:
            attrs = wy.attr
            try:
                x = attrs['building']
                if not x:
                    continue
            except KeyError:
                continue
            brush = QBrush()
            brush.setColor(QColor(65, 62, 200))
            polygon = QPolygon()
            length = len(wy.point) - 1
            for i in range(length):
                new_pt = self.map.cross_list.get_node(wy.point[i]['ref'])
                polygon.append(QPoint(new_pt.x * 680 / max_x, new_pt.y * 830 / max_y))
            self.painter.setBrush(brush)
            self.painter.drawPolygon(polygon)

        for wy in self.map.ways:
            attrs = wy.attr
            try:
                x = attrs['highway']
                if not x:
                    continue
            except KeyError:
                continue
            pen = QPen()
            pen.setColor(QColor(68, 193, 181))
            pen.setWidth(2)
            self.painter.setPen(pen)
            points = []
            length = len(wy.point) - 1
            for i in range(length):
                start = self.map.cross_list.get_node(wy.point[i]['ref'])
                end = self.map.cross_list.get_node(wy.point[i + 1]['ref'])
                self.painter.drawLine(start.x * 680 / max_x, start.y * 830 / max_y,
                                      end.x * 680 / max_x, end.y * 830 / max_y)

    def paintEvent(self, e):
        print('paint')
        brush = QBrush()
        brush.setColor(QColor(227, 174, 222))
        self.painter.setBackground(brush)
        self.painter.begin(self)
        #self.painter.setBrush(brush)
        self.map_render()
        self.painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    map_display = MapDisplay(filename='../data/map.osm')
    sys.exit(app.exec_())
