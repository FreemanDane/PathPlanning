from src import DataAnalysis
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont, QColor, QPolygon
from PyQt5.QtCore import QPoint,QRect, Qt
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
        self.painter.setPen(Qt.NoPen)
        for wy in self.map.ways:
            attrs = wy.attr
            try:
                x = attrs['amenity']
            except KeyError:
                continue
            if x == 'parking':
                self.painter.setBrush(QColor(254, 194, 146))
            polygon = QPolygon()
            length = len(wy.point) - 1
            for i in range(length):
                new_pt = self.map.cross_list.get_node(wy.point[i]['ref'])
                polygon.append(QPoint(new_pt.x * 680 / max_x, 830 - new_pt.y * 830 / max_y))
            self.painter.drawPolygon(polygon)
        for wy in self.map.ways:
            attrs = wy.attr
            try:
                x = attrs['surface']
                if not x:
                    continue
            except KeyError:
                continue
            if x == 'paving_stones' or x == 'paved' or x == 'concrete:plates' or x == 'asphalt' or x == 'cobblestone':
                self.painter.setBrush(QColor(220, 220, 220))
            elif x == 'earth' or x == 'sand':
                self.painter.setBrush((QColor(231, 179, 22)))
            elif x == 'grass':
                self.painter.setBrush(QColor(55, 232, 30))
            else:
                print('{} is not showed in surface'.format(x))
            polygon = QPolygon()
            length = len(wy.point) - 1
            for i in range(length):
                new_pt = self.map.cross_list.get_node(wy.point[i]['ref'])
                polygon.append(QPoint(new_pt.x * 680 / max_x, 830 - new_pt.y * 830 / max_y))
            self.painter.drawPolygon(polygon)
        for wy in self.map.ways:
            attrs = wy.attr
            try:
                x = attrs['leisure']
            except KeyError:
                continue
            if x == 'swimming_pool':
                self.painter.setBrush(QColor(150, 182, 218))
            elif x == 'park' or x == 'playground':
                self.painter.setBrush(QColor(150, 218, 179))
            polygon = QPolygon()
            length = len(wy.point) - 1
            for i in range(length):
                new_pt = self.map.cross_list.get_node(wy.point[i]['ref'])
                polygon.append(QPoint(new_pt.x * 680 / max_x, 830 - new_pt.y * 830 / max_y))
            self.painter.drawPolygon(polygon)
        for wy in self.map.ways:
            attrs = wy.attr
            try:
                x = attrs['natural']
            except KeyError:
                continue
            if x == 'water':
                self.painter.setBrush(QColor(146,160,209))
            elif x == 'grassland':
                self.painter.setBrush(QColor(55, 232, 30))
            elif x == 'wood':
                self.painter.setBrush(QColor(75, 189, 72))
            else:
                print('{} is not showed in natural'.format(x))
            polygon = QPolygon()
            length = len(wy.point) - 1
            for i in range(length):
                new_pt = self.map.cross_list.get_node(wy.point[i]['ref'])
                polygon.append(QPoint(new_pt.x * 680 / max_x, 830 - new_pt.y * 830 / max_y))
            self.painter.drawPolygon(polygon)
        for wy in self.map.ways:
            attrs = wy.attr
            try:
                x = attrs['landuse']
                if not x:
                    continue
            except KeyError:
                continue
            if x == 'grass' or x == 'meadow':
                self.painter.setBrush(QColor(55, 232, 30))
            elif x == 'forest':
                self.painter.setBrush(QColor(75, 189, 72))
            elif x == 'commercial' or x == 'retail' or x == 'construction' or x == 'park' or x == 'residential':
                self.painter.setBrush((QColor(220, 220, 220)))
            else:
                print('{} is not showed in landuse'.format(x))
            polygon = QPolygon()
            length = len(wy.point) - 1
            for i in range(length):
                new_pt = self.map.cross_list.get_node(wy.point[i]['ref'])
                polygon.append(QPoint(new_pt.x * 680 / max_x, 830 - new_pt.y * 830 / max_y))
            self.painter.drawPolygon(polygon)
        for wy in self.map.ways:
            attrs = wy.attr
            try:
                x = attrs['building']
                if not x:
                    continue
            except KeyError:
                continue
            self.painter.setBrush(QColor(213, 191, 223))
            polygon = QPolygon()
            length = len(wy.point) - 1
            for i in range(length):
                new_pt = self.map.cross_list.get_node(wy.point[i]['ref'])
                polygon.append(QPoint(new_pt.x * 680 / max_x, 830 - new_pt.y * 830 / max_y))
            self.painter.drawPolygon(polygon)
        for wy in self.map.ways:
            attrs = wy.attr
            try:
                x = attrs['waterway']
            except KeyError:
                continue
            pen = QPen()
            pen.setColor(QColor(146, 160, 209))
            pen.setWidth(2)
            self.painter.setPen(pen)
            points = []
            length = len(wy.point) - 1
            for i in range(length):
                start = self.map.cross_list.get_node(wy.point[i]['ref'])
                end = self.map.cross_list.get_node(wy.point[i + 1]['ref'])
                self.painter.drawLine(start.x * 680 / max_x, 830 - start.y * 830 / max_y,
                                      end.x * 680 / max_x, 830 - end.y * 830 / max_y)
        for wy in self.map.ways:
            attrs = wy.attr
            try:
                x = attrs['highway']
                if not x:
                    continue
            except KeyError:
                continue
            pen = QPen()
            pen.setColor(QColor(202, 200, 153))
            pen.setWidth(2)
            self.painter.setPen(pen)
            points = []
            length = len(wy.point) - 1
            for i in range(length):
                start = self.map.cross_list.get_node(wy.point[i]['ref'])
                end = self.map.cross_list.get_node(wy.point[i + 1]['ref'])
                self.painter.drawLine(start.x * 680 / max_x, 830 - start.y * 830 / max_y,
                                      end.x * 680 / max_x, 830 - end.y * 830 / max_y)

    def paintEvent(self, e):
        print('paint')
        self.painter.begin(self)
        rect = QRect(0,0,1000,1000)
        self.painter.fillRect(rect, QColor(244, 241, 219))
        self.map_render()
        self.painter.end()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    map_display = MapDisplay(filename='../data/map.osm')
    sys.exit(app.exec_())
