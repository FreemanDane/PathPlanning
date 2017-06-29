from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class thu_map(QGraphicsPixmapItem, QObject):
    def __init__(self):
        super(thu_map, self).__init__()
        self.setPixmap(QPixmap("../data/map.png"))
        self.show()
        self.setTransformationMode(Qt.SmoothTransformation)
        self.size_x = 685.0
        self.size_y = 831.0
        self.zoom = [0, 0]           #第一个代表鼠标滚动之前（过去状态），第二个代表鼠标滚动之后（当前状态）
        self.mouse = QPointF(0, 0)
        self.top_left = QPointF(0, 0)
        self.flag = 0
    def boundingRect(self):
        return QRectF(self.top_left.x(), self.top_left.y(), self.size_x * pow(1.2, 0.5 * self.zoom[1]), self.size_y * pow(1.2, 0.5 * self.zoom[1]))
    def paint(self, painter, option, widget):
        zoom_change = self.zoom[1] - self.zoom[0]
        #计算x
        if zoom_change >= 0:
            x = self.top_left.x() - (1 - pow(1.2, -0.5 * zoom_change)) * self.mouse.x()
        else:
            x = (pow(1.2, 0.5 * self.zoom[1]) - 1) / (pow(1.2, 0.5 * self.zoom[0]) - 1) * self.top_left.x()

        #计算y
        if zoom_change >= 0:
            y = self.top_left.y() - (1 - pow(1.2, -0.5 * zoom_change)) * self.mouse.y()
        else:
            y = (pow(1.2, 0.5 * self.zoom[1]) - 1) / (pow(1.2, 0.5 * self.zoom[0]) - 1) * self.top_left.y()

        self.top_left = QPointF(x, y)
        #target = QRectF(x, y, (self.size_x * pow(1.2, 0.5 * self.zoom[1])), (self.size_y * pow(1.2, 0.5 * self.zoom[1])))
        if self.flag == 0:
            self.setTransform(QTransform.fromScale(1.2, 1.2), True)
            self.flag = 1
        pixmap = self.pixmap()
        target = QRectF(-200, -200, self.size_x, self.size_y)
        source = QRectF(0, 0, self.size_x, self.size_y)
        painter.drawPixmap(target, pixmap, source)
    def wheelEvent(self, event):
        factor = 1.0
        max_zoom = 10
        self.mouse = event.pos()
        self.zoom[0] = self.zoom[1]
        if (self.zoom[1] + event.delta() / 120.0) >= 0 and (self.zoom[1] + event.delta() / 120.0) <= max_zoom:
            factor = pow(1.2, event.delta() / 240.0)
            self.zoom[1] = self.zoom[1] + event.delta() / 120.0
        elif (self.zoom[1] + event.delta() / 120.0) > max_zoom:
            factor = pow(1.2, (max_zoom - self.zoom[1]) / 2)
            self.zoom[1] = max_zoom
        else:
            factor = pow(1.2, -self.zoom[1] / 2)
            self.zoom[1] = 0
        self.setTransform(QTransform.fromScale(factor, factor), True)
        self.update()
        super(thu_map, self).wheelEvent(event)
class MainWindow(QGraphicsView):
    def __init__(self):
        super(MainWindow, self).__init__()
        scene = QGraphicsScene(self)
        self.map = thu_map()
        scene.addItem(self.map)
        scene.setSceneRect(0, 0, 685, 831)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setWindowTitle("THU MAP")
        self.setFixedSize(687, 833)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())

