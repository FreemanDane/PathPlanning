import DataAnalysis
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton
from PyQt5.QtGui import QPainter, QPen, QBrush, QFont, QColor, QPolygon, QIcon
from PyQt5.QtCore import QPoint,QRect, Qt
import sys

class MapDisplay(QWidget):
    def __init__(self, filename, parent = None):
        super(MapDisplay, self).__init__(parent)
        print('Loading Data...')
        self.map = DataAnalysis.map(filename)
        self.map.cross_list.cartesian_coordinate()
        print('Total {} nodes, {} ways.'.format(len(self.map.cross_list.nodes), len(self.map.ways)))
        self.size_x = 680
        self.size_y = 830

        self.zoom = [0, 0]  # 第一个代表鼠标滚动之前（过去状态），第二个代表鼠标滚动之后（当前状态）
        self.max_zoom = 10
        self.mouse = QPoint(0, 0)  # 发生事件时鼠标在屏幕上的位置（相对窗口左上角）
        self.mouse_true = QPoint(0, 0)  # 发生点击事件时鼠标在图片上的位置（相对图片左上角）
        self.top_left = QPoint(0, 0)  # 图片左上角坐标
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
        print("render map")
        max_x = self.map.cross_list.farthest_node.x
        max_y = self.map.cross_list.farthest_node.y
        top_left_point = self.displayTopLeft()
        bottom_right_point = self.displayBottomRight()
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
                display_x = ((new_pt.x / max_x) * self.size_x - top_left_point.x()) / (
                    bottom_right_point.x() - top_left_point.x()) * self.size_x
                display_y = (self.size_y - (new_pt.y / max_y) * self.size_y - top_left_point.y()) / (
                    bottom_right_point.y() - top_left_point.y()) * self.size_y
                polygon.append(QPoint(display_x, display_y))
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
                display_x = ((new_pt.x / max_x) * self.size_x - top_left_point.x()) / (
                    bottom_right_point.x() - top_left_point.x()) * self.size_x
                display_y = (self.size_y - (new_pt.y / max_y) * self.size_y - top_left_point.y()) / (
                    bottom_right_point.y() - top_left_point.y()) * self.size_y
                polygon.append(QPoint(display_x, display_y))
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
                display_x = ((new_pt.x / max_x) * self.size_x - top_left_point.x()) / (
                    bottom_right_point.x() - top_left_point.x()) * self.size_x
                display_y = (self.size_y - (new_pt.y / max_y) * self.size_y - top_left_point.y()) / (
                    bottom_right_point.y() - top_left_point.y()) * self.size_y
                polygon.append(QPoint(display_x, display_y))
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
                display_x = ((new_pt.x / max_x) * self.size_x - top_left_point.x()) / (
                    bottom_right_point.x() - top_left_point.x()) * self.size_x
                display_y = (self.size_y - (new_pt.y / max_y) * self.size_y - top_left_point.y()) / (
                    bottom_right_point.y() - top_left_point.y()) * self.size_y
                polygon.append(QPoint(display_x, display_y))
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
                display_x = ((new_pt.x / max_x) * self.size_x - top_left_point.x()) / (
                    bottom_right_point.x() - top_left_point.x()) * self.size_x
                display_y = (self.size_y - (new_pt.y / max_y) * self.size_y - top_left_point.y()) / (
                    bottom_right_point.y() - top_left_point.y()) * self.size_y
                polygon.append(QPoint(display_x, display_y))
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
                display_x = ((new_pt.x / max_x) * self.size_x - top_left_point.x()) / (
                    bottom_right_point.x() - top_left_point.x()) * self.size_x
                display_y = (self.size_y - (new_pt.y / max_y) * self.size_y - top_left_point.y()) / (
                    bottom_right_point.y() - top_left_point.y()) * self.size_y
                polygon.append(QPoint(display_x, display_y))
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
                start_display_x = ((start.x / max_x) * self.size_x - top_left_point.x()) / (
                    bottom_right_point.x() - top_left_point.x()) * self.size_x
                start_display_y = (self.size_y - (start.y / max_y) * self.size_y - top_left_point.y()) / (
                    bottom_right_point.y() - top_left_point.y()) * self.size_y
                end_display_x = ((end.x / max_x) * self.size_x - top_left_point.x()) / (
                    bottom_right_point.x() - top_left_point.x()) * self.size_x
                end_display_y = (self.size_y - (end.y / max_y) * self.size_y - top_left_point.y()) / (
                    bottom_right_point.y() - top_left_point.y()) * self.size_y
                self.painter.drawLine(start_display_x, start_display_y, end_display_x, end_display_y)
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
                start_display_x = ((start.x / max_x) * self.size_x - top_left_point.x()) / (
                    bottom_right_point.x() - top_left_point.x()) * self.size_x
                start_display_y = (self.size_y - (start.y / max_y) * self.size_y - top_left_point.y()) / (
                    bottom_right_point.y() - top_left_point.y()) * self.size_y
                end_display_x = ((end.x / max_x) * self.size_x - top_left_point.x()) / (
                    bottom_right_point.x() - top_left_point.x()) * self.size_x
                end_display_y = (self.size_y - (end.y / max_y) * self.size_y - top_left_point.y()) / (
                    bottom_right_point.y() - top_left_point.y()) * self.size_y
                self.painter.drawLine(start_display_x, start_display_y, end_display_x, end_display_y)

    def paintEvent(self, e):
        print('paint')
        self.painter.begin(self)
        rect = QRect(0,0,1000,1000)
        self.painter.fillRect(rect, QColor(244, 241, 219))
        self.map_render()
        self.painter.end()

    # 鼠标滚轮事件
    def wheelEvent(self, event):
        factor = 1.0
        x = event.pos().x()
        y = event.pos().y()
        self.zoom[0] = self.zoom[1]
        self.mouse = QPoint(x, y)
        d = event.angleDelta().y()
        if (self.zoom[1] + d / 120.0) >= 0 and (self.zoom[1] + d / 120.0) <= self.max_zoom:
            factor = pow(1.2, d / 240.0)
            self.zoom[1] = self.zoom[1] + d / 120.0
        elif (self.zoom[1] + d / 120.0) > self.max_zoom:
            factor = pow(1.2, (self.max_zoom - self.zoom[1]) / 2)
            self.zoom[1] = self.max_zoom
        else:
            factor = pow(1.2, -self.zoom[1] / 2)
            self.zoom[1] = 0

        zoom_change = self.zoom[1] - self.zoom[0]

        # 计算左上角x
        if zoom_change >= 0:
            x = self.top_left.x() - (pow(1.2, -0.5 * self.zoom[0]) - pow(1.2, -0.5 * self.zoom[1])) * self.mouse.x()
        else:
            x = ((pow(1.2, 0.5 * self.zoom[1]) - 1) * pow(1.2, 0.5 * self.zoom[0])) / (
            (pow(1.2, 0.5 * self.zoom[0]) - 1) * pow(1.2, 0.5 * self.zoom[1])) * self.top_left.x()

        # 计算左上角y
        if zoom_change >= 0:
            y = self.top_left.y() - (pow(1.2, -0.5 * self.zoom[0]) - pow(1.2, -0.5 * self.zoom[1])) * self.mouse.y()
        else:
            y = ((pow(1.2, 0.5 * self.zoom[1]) - 1) * pow(1.2, 0.5 * self.zoom[0])) / (
            (pow(1.2, 0.5 * self.zoom[0]) - 1) * pow(1.2, 0.5 * self.zoom[1])) * self.top_left.y()

        self.top_left = QPoint(x, y)
        self.update()

    # 鼠标拖拽事件
    def mousePressEvent(self, event):
        self.is_press = 1
        x = event.pos().x()
        y = event.pos().y()
        self.mouse = QPoint(x, y)
        self.before_drag = self.convertScreenToImage(self.mouse)

    def mouseReleaseEvent(self, event):
        self.is_press = 0

    def mouseMoveEvent(self, event):
        if self.is_press == 1:
            x = event.pos().x()
            y = event.pos().y()
            self.mouse = QPoint(x, y)

            # 计算左上角x
            x = pow(1.2, -0.5 * self.zoom[1]) * self.mouse.x() - self.before_drag.x()
            if x > 0:
                x = 0
            elif x < pow(1.2, -0.5 * self.zoom[1]) * self.size_x - self.size_x:
                x = pow(1.2, -0.5 * self.zoom[1]) * self.size_x - self.size_x

            # 计算左上角y
            y = pow(1.2, -0.5 * self.zoom[1]) * self.mouse.y() - self.before_drag.y()
            if y > 0:
                y = 0
            elif y < pow(1.2, -0.5 * self.zoom[1]) * self.size_y - self.size_y:
                y = pow(1.2, -0.5 * self.zoom[1]) * self.size_y - self.size_y

            self.top_left = QPoint(x, y)
        self.update()

    # 坐标变换函数
    def convertScreenToImage(self, point):
        image_x = point.x() / pow(1.2, 0.5 * self.zoom[1]) - self.top_left.x()
        image_y = point.y() / pow(1.2, 0.5 * self.zoom[1]) - self.top_left.y()
        return QPoint(image_x, image_y)

    # 放大函数
    def zoomIn(self):
        x = self.size_x / 2
        y = self.size_y / 2
        self.mouse = QPoint(x, y)
        self.is_zoom = 1
        self.zoom[0] = self.zoom[1]
        if self.zoom[1] < self.max_zoom:
            self.zoom[1] = self.zoom[1] + 1
            factor = pow(1.2, 0.5)

            x = self.top_left.x() - (pow(1.2, -0.5 * self.zoom[0]) - pow(1.2, -0.5 * self.zoom[1])) * self.mouse.x()
            y = self.top_left.y() - (pow(1.2, -0.5 * self.zoom[0]) - pow(1.2, -0.5 * self.zoom[1])) * self.mouse.y()
            self.top_left = QPoint(x, y)
            self.update()

    # 缩小函数
    def zoomOut(self):
        self.is_zoom = 1
        self.zoom[0] = self.zoom[1]
        if self.zoom[1] > 0:
            self.zoom[1] = self.zoom[1] - 1
            factor = pow(1.2, -0.5)

            x = ((pow(1.2, 0.5 * self.zoom[1]) - 1) * pow(1.2, 0.5 * self.zoom[0])) / (
                (pow(1.2, 0.5 * self.zoom[0]) - 1) * pow(1.2, 0.5 * self.zoom[1])) * self.top_left.x()
            y = ((pow(1.2, 0.5 * self.zoom[1]) - 1) * pow(1.2, 0.5 * self.zoom[0])) / (
                (pow(1.2, 0.5 * self.zoom[0]) - 1) * pow(1.2, 0.5 * self.zoom[1])) * self.top_left.y()
            self.top_left = QPoint(x, y)
            self.update()

    # 显示区域左上角在原图中坐标
    def displayTopLeft(self):
        x = -self.top_left.x()
        y = -self.top_left.y()
        return QPoint(x, y)

    # 显示区域右下角在原图中坐标
    def displayBottomRight(self):
        x = self.size_x / pow(1.2, 0.5 * self.zoom[1]) - self.top_left.x()
        y = self.size_y / pow(1.2, 0.5 * self.zoom[1]) - self.top_left.y()
        return QPoint(x, y)

    # 缩放比例
    def zoomRatio(self):
        return pow(1.2, 0.5 * self.zoom[1])

