from src import DataAnalysis
from src.CrossList import node, lat_min, lat_max, lon_max, lon_min
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont, QColor, QPolygon, QIcon
from PyQt5.QtCore import QPoint,QRect, Qt, pyqtSignal, QPointF
import sys

class MapDisplay(QWidget):
    zoom_signal = pyqtSignal()
    press_signal = pyqtSignal(int, int)
    move_signal = pyqtSignal()
    def __init__(self, filename, parent = None):
        super(MapDisplay, self).__init__(parent)
        print('Loading Data...')
        self.map = DataAnalysis.map(filename)
        #self.map.cross_list.cartesian_coordinate()
        print('Total {} nodes, {} ways.'.format(len(self.map.cross_list.nodes), len(self.map.ways)))
        self.size_x = 680
        self.size_y = 830

        self.zoom = [0, 0]  # 第一个代表鼠标滚动之前（过去状态），第二个代表鼠标滚动之后（当前状态）
        self.max_zoom = 50
        self.zoom_ratio = 1.1
        self.mouse = QPoint(0, 0)  # 发生事件时鼠标在屏幕上的位置（相对窗口左上角）
        self.top_left = node('5', lat_min, lon_min)  # 图片左上角坐标
        self.top_left.cartesian_coordinate(self.map.cross_list.origin)
        self.is_zoom = 0  # 缩放事件标记
        self.is_press = 0  # 鼠标按下事件标记
        self.before_drag = QPoint(0, 0)

        self.initUI()
    def initUI(self):
        self.setWindowTitle("At Tsinghua")
        self.setFixedWidth(self.size_x)
        self.setFixedHeight(self.size_y)
        self.painter = QPainter()
        self.show()

    def map_render(self):
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
                polygon.append(QPoint(new_pt.x * self.size_x / max_x, self.size_y - new_pt.y * self.size_y / max_y))
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
                polygon.append(QPoint(new_pt.x * self.size_x / max_x, self.size_y - new_pt.y * self.size_y / max_y))
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
                polygon.append(QPoint(new_pt.x * self.size_x / max_x, self.size_y - new_pt.y * self.size_y / max_y))
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
                polygon.append(QPoint(new_pt.x * self.size_x / max_x, self.size_y - new_pt.y * self.size_y / max_y))
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
                polygon.append(QPoint(new_pt.x * self.size_x / max_x, self.size_y - new_pt.y * self.size_y / max_y))
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
                polygon.append(QPoint(new_pt.x * self.size_x / max_x, self.size_y - new_pt.y * self.size_y / max_y))
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
                self.painter.drawLine(start.x * self.size_x / max_x, self.size_y - start.y * self.size_y / max_y,
                                      end.x * self.size_x / max_x, self.size_y - end.y * self.size_y /max_y)
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
                self.painter.drawLine(start.x * self.size_x / max_x, self.size_y - start.y * self.size_y / max_y,
                                      end.x * self.size_x / max_x, self.size_y - end.y * self.size_y / max_y)

    def paintEvent(self, e):
        self.painter.begin(self)
        rect = QRect(0,0,1000,1000)
        self.painter.fillRect(rect, QColor(244, 241, 219))
        self.map_render()
        self.mark()
        self.painter.end()

    # 鼠标滚轮事件
    def wheelEvent(self, event):
        factor = 1.0
        x = event.pos().x()
        y = event.pos().y()
        self.zoom[0] = self.zoom[1]
        d = event.angleDelta().y()
        if (self.zoom[1] + d / 120.0) >= 0 and (self.zoom[1] + d / 120.0) <= self.max_zoom:
            factor = pow(self.zoom_ratio, d / 240.0)
            self.zoom[1] = self.zoom[1] + d / 120.0
        elif (self.zoom[1] + d / 120.0) > self.max_zoom:
            factor = pow(self.zoom_ratio, (self.max_zoom - self.zoom[1]) / 2)
            self.zoom[1] = self.max_zoom
        else:
            factor = pow(self.zoom_ratio, -self.zoom[1] / 2)
            self.zoom[1] = 0

        mouse_lon = x / self.size_x * (self.map.cross_list.farthest_node.lon - self.map.cross_list.origin.lon) + self.map.cross_list.origin.lon
        mouse_lat = self.map.cross_list.farthest_node.lat - y / self.size_y * (self.map.cross_list.farthest_node.lat - self.map.cross_list.origin.lat)
        new_origin_lon = mouse_lon - (lon_max - lon_min) / (self.size_x / x * pow(self.zoom_ratio, 0.5 * self.zoom[1]))
        if new_origin_lon <= lon_min:
            new_origin_lon = lon_min
        elif new_origin_lon > lon_max - (lon_max - lon_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1]):
            new_origin_lon = lon_max - (lon_max - lon_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1])
        new_origin_lat = mouse_lat - (lat_max - lat_min) / (self.size_y / (self.size_y - y) * pow(self.zoom_ratio, 0.5 * self.zoom[1]))
        if new_origin_lat <= lat_min:
            new_origin_lat = lat_min
        elif new_origin_lat > lat_max - (lat_max - lat_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1]):
            new_origin_lat = lat_max - (lat_max - lat_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1])
        self.map.cross_list.origin.lon = new_origin_lon
        self.map.cross_list.origin.lat = new_origin_lat
        new_farthest_lon = new_origin_lon + (lon_max - lon_min) / pow(self.zoom_ratio, 0.5 * self.zoom[1])
        new_farthest_lat = new_origin_lat + (lat_max - lat_min) / pow(self.zoom_ratio, 0.5 * self.zoom[1])
        self.map.cross_list.farthest_node.lon = new_farthest_lon
        self.map.cross_list.farthest_node.lat = new_farthest_lat
        self.map.cross_list.farthest_node.cartesian_coordinate(self.map.cross_list.origin)
        self.map.cross_list.cartesian_coordinate()
        self.update()
        self.zoom_signal.emit()

    # 鼠标拖拽事件
    def mousePressEvent(self, event):
        self.is_press = 1
        x = event.pos().x()
        y = event.pos().y()
        self.before_drag = QPoint(x, y)
        self.max_lon_fixed = self.map.cross_list.farthest_node.lon
        self.min_lon_fixed = self.map.cross_list.origin.lon
        self.max_lat_fixed = self.map.cross_list.farthest_node.lat
        self.min_lat_fixed = self.map.cross_list.origin.lat
        self.press_signal.emit(int(x), int(y))

    def mouseReleaseEvent(self, event):
        self.is_press = 0

    def mouseMoveEvent(self, event):
        if self.is_press == 1:
            x = event.pos().x()
            y = event.pos().y()
            self.mouse = QPoint(x, y)

            new_origin_lon = (self.before_drag.x() - self.mouse.x()) * (self.max_lon_fixed - self.min_lon_fixed) / self.size_x + self.min_lon_fixed
            if new_origin_lon <= lon_min:
                new_origin_lon = lon_min
            elif new_origin_lon > lon_max - (lon_max - lon_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1]):
                new_origin_lon = lon_max - (lon_max - lon_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1])
            new_origin_lat = (self.mouse.y() - self.before_drag.y()) * (self.max_lat_fixed - self.min_lat_fixed) / self.size_y + self.min_lat_fixed
            if new_origin_lat <= lat_min:
                new_origin_lat = lat_min
            elif new_origin_lat > lat_max - (lat_max - lat_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1]):
                new_origin_lat = lat_max - (lat_max - lat_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1])
            self.map.cross_list.origin.lon = new_origin_lon
            self.map.cross_list.origin.lat = new_origin_lat
            new_farthest_lon = new_origin_lon + (lon_max - lon_min) / pow(self.zoom_ratio, 0.5 * self.zoom[1])
            new_farthest_lat = new_origin_lat + (lat_max - lat_min) / pow(self.zoom_ratio, 0.5 * self.zoom[1])
            self.map.cross_list.farthest_node.lon = new_farthest_lon
            self.map.cross_list.farthest_node.lat = new_farthest_lat
            self.map.cross_list.farthest_node.cartesian_coordinate(self.map.cross_list.origin)
            self.map.cross_list.cartesian_coordinate()
            self.update()
            self.move_signal.emit()
    # 坐标变换函数
    def convertScreenToCoordinates(self, x, y):
        mouse_lon = x / self.size_x * (self.map.cross_list.farthest_node.lon - self.map.cross_list.origin.lon) + self.map.cross_list.origin.lon
        mouse_lat = self.map.cross_list.farthest_node.lat - y / self.size_y * (self.map.cross_list.farthest_node.lat - self.map.cross_list.origin.lat)
        return [mouse_lon, mouse_lat]
    def convertCoordinatesToScreen(self, lon, lat):
        x = (lon - self.map.cross_list.origin.lon) / (self.map.cross_list.farthest_node.lon - self.map.cross_list.origin.lon) * self.size_x
        y = (self.map.cross_list.farthest_node.lat - lat) / (self.map.cross_list.farthest_node.lat - self.map.cross_list.origin.lat) * self.size_y
        return [x, y]

    # 放大函数
    def zoomIn(self, x = -1.0, y = -1.0):
        if x < 0 or y < 0:
            x = self.size_x / 2
            y = self.size_y / 2
        self.mouse = QPoint(x, y)
        self.is_zoom = 1
        self.zoom[0] = self.zoom[1]
        if self.zoom[1] < self.max_zoom:
            self.zoom[1] = self.zoom[1] + 1
            factor = pow(self.zoom_ratio, 0.5)

            mouse_lon = x / self.size_x * (
            self.map.cross_list.farthest_node.lon - self.map.cross_list.origin.lon) + self.map.cross_list.origin.lon
            mouse_lat = self.map.cross_list.farthest_node.lat - y / self.size_y * (
            self.map.cross_list.farthest_node.lat - self.map.cross_list.origin.lat)
            new_origin_lon = mouse_lon - (lon_max - lon_min) / (self.size_x / x * pow(self.zoom_ratio, 0.5 * self.zoom[1]))
            if new_origin_lon <= lon_min:
                new_origin_lon = lon_min
            elif new_origin_lon > lon_max - (lon_max - lon_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1]):
                new_origin_lon = lon_max - (lon_max - lon_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1])
            new_origin_lat = mouse_lat - (lat_max - lat_min) / (
            self.size_y / (self.size_y - y) * pow(self.zoom_ratio, 0.5 * self.zoom[1]))
            if new_origin_lat <= lat_min:
                new_origin_lat = lat_min
            elif new_origin_lat > lat_max - (lat_max - lat_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1]):
                new_origin_lat = lat_max - (lat_max - lat_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1])
            self.map.cross_list.origin.lon = new_origin_lon
            self.map.cross_list.origin.lat = new_origin_lat
            new_farthest_lon = new_origin_lon + (lon_max - lon_min) / pow(self.zoom_ratio, 0.5 * self.zoom[1])
            new_farthest_lat = new_origin_lat + (lat_max - lat_min) / pow(self.zoom_ratio, 0.5 * self.zoom[1])
            self.map.cross_list.farthest_node.lon = new_farthest_lon
            self.map.cross_list.farthest_node.lat = new_farthest_lat
            self.map.cross_list.farthest_node.cartesian_coordinate(self.map.cross_list.origin)
            self.map.cross_list.cartesian_coordinate()
            self.update()
            self.zoom_signal.emit()
    # 缩小函数
    def zoomOut(self):
        self.is_zoom = 1
        self.zoom[0] = self.zoom[1]
        if self.zoom[1] > 0:
            self.zoom[1] = self.zoom[1] - 1
            factor = pow(self.zoom_ratio, -0.5)

            x = self.size_x / 2
            y = self.size_y / 2
            mouse_lon = x / self.size_x * (
            self.map.cross_list.farthest_node.lon - self.map.cross_list.origin.lon) + self.map.cross_list.origin.lon
            mouse_lat = self.map.cross_list.farthest_node.lat - y / self.size_y * (
            self.map.cross_list.farthest_node.lat - self.map.cross_list.origin.lat)
            new_origin_lon = mouse_lon - (lon_max - lon_min) / (self.size_x / x * pow(self.zoom_ratio, 0.5 * self.zoom[1]))
            if new_origin_lon <= lon_min:
                new_origin_lon = lon_min
            elif new_origin_lon > lon_max - (lon_max - lon_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1]):
                new_origin_lon = lon_max - (lon_max - lon_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1])
            new_origin_lat = mouse_lat - (lat_max - lat_min) / (
            self.size_y / (self.size_y - y) * pow(self.zoom_ratio, 0.5 * self.zoom[1]))
            if new_origin_lat <= lat_min:
                new_origin_lat = lat_min
            elif new_origin_lat > lat_max - (lat_max - lat_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1]):
                new_origin_lat = lat_max - (lat_max - lat_min) * pow(self.zoom_ratio, -0.5 * self.zoom[1])
            self.map.cross_list.origin.lon = new_origin_lon
            self.map.cross_list.origin.lat = new_origin_lat
            new_farthest_lon = new_origin_lon + (lon_max - lon_min) / pow(self.zoom_ratio, 0.5 * self.zoom[1])
            new_farthest_lat = new_origin_lat + (lat_max - lat_min) / pow(self.zoom_ratio, 0.5 * self.zoom[1])
            self.map.cross_list.farthest_node.lon = new_farthest_lon
            self.map.cross_list.farthest_node.lat = new_farthest_lat
            self.map.cross_list.farthest_node.cartesian_coordinate(self.map.cross_list.origin)
            self.map.cross_list.cartesian_coordinate()
            self.update()
            self.zoom_signal.emit()
    # 显示区域左上角在原图中坐标
    def displayTopLeft(self):
        x = -self.top_left.x
        y = -self.top_left.y
        return QPoint(x, y)

    # 显示区域右下角在原图中坐标
    def displayBottomRight(self):
        x = self.size_x / pow(self.zoom_ratio, 0.5 * self.zoom[1]) - self.top_left.x
        y = self.size_y / pow(self.zoom_ratio, 0.5 * self.zoom[1]) - self.top_left.y
        return QPoint(x, y)

    # 缩放比例
    def zoomRatio(self):
        return pow(self.zoom_ratio, 0.5 * self.zoom[1])

    def mark(self):
        for wy in self.map.ways:
            try:
                name = wy.attr['name']
                try:
                    x = wy.attr['highway']
                    continue
                except KeyError:
                    pass
                rect = self.map.way_rect(wy)
                #l = rect[2] * pow(self.zoom_ratio, 0.5 * self.zoom[1] + 1) / (len(name))
                l = 10
                if name == "篮球场":
                    rect = (rect[0], rect[1],rect[2] / 2, rect[3])
                if l > rect[2] * pow(self.zoom_ratio, 0.5 * self.zoom[1] + 1) / (len(name)) or rect[3] * pow(self.zoom_ratio, 0.5 * self.zoom[1] + 1) < l:
                    continue

                height = self.map.cross_list.farthest_node.y
                weight = self.map.cross_list.farthest_node.x
                self.painter.setFont(QFont('Microsoft Yahei', l, 75))

                self.painter.setPen(QColor(150, 150, 150))
                self.painter.drawText(
                    rect[0] / weight * self.size_x - 1, \
                    self.size_y - (rect[1] + rect[3]) / height * self.size_y + 1, \
                    rect[2] / weight * self.size_x, \
                    rect[3] / height * self.size_y, \
                    Qt.AlignCenter, \
                    name)

                self.painter.setPen(QColor(0, 0, 0))
                self.painter.drawText(
                    rect[0] / weight * self.size_x, \
                    self.size_y - (rect[1] + rect[3]) / height * self.size_y, \
                    rect[2] / weight * self.size_x, \
                    rect[3] / height * self.size_y, \
                    Qt.AlignCenter, \
                    name)
            except KeyError:
                continue