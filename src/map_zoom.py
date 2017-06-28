from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class thu_map(QGraphicsPixmapItem):
    def __init__(self):
        super(thu_map, self).__init__()
        self.setPixmap(QPixmap("../data/map.png"))
        self.size_x = 685
        self.size_y = 831
        self.zoom = [0, 0]           #第一个代表鼠标滚动之前（过去状态），第二个代表鼠标滚动之后（当前状态）
        self.mouse = QPointF(0, 0)
        self.top_left = QPointF(0, 0)
    def boundingRect(self):
        return QRectF(self.top_left.x(), self.top_left.y(), self.size_x * pow(1.2, 0.5 * self.zoom[1]), self.size_y * pow(1.2, 0.5 * self.zoom[1]))
    def paint(self, painter, option, widget):
        zoom_change = self.zoom[1] - self.zoom[0]
        x = pow(1.2, 0.5 * zoom_change) * self.top_left.x() - (pow(1.2, 0.5 * zoom_change) - 1) * self.mouse.x()
        if x < self.size_x * (1 - pow(1.2, 0.5 * self.zoom[1])):
            x = self.size_x * (1 - pow(1.2, 0.5 * self.zoom[1]))
        elif x > 0:
            x = 0
        y = pow(1.2, 0.5 * zoom_change) * self.top_left.y() - (pow(1.2, 0.5 * zoom_change) - 1) * self.mouse.y()
        if y < self.size_y * (1 - pow(1.2, 0.5 * self.zoom[1])):
            y = self.size_y * (1 - pow(1.2, 0.5 * self.zoom[1]))
        elif y > 0:
            y = 0
        self.top_left = QPointF(x, y)
        target = QRectF(x, y, self.size_x * pow(1.2, 0.5 * self.zoom[1]), self.size_y * pow(1.2, 0.5 * self.zoom[1]))
        source = QRectF(0, 0, self.size_x, self.size_y)
        painter.drawPixmap(target, QPixmap("../data/map.png"),source)
    def wheelEvent(self, event):
        factor = 1
        max_zoom = 5
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
        #self.setTransform(QTransform.fromScale(factor, factor), True)
        #self.scale(factor)
        self.update()
        super(thu_map, self).wheelEvent(event)
class MainWindow(QGraphicsView):
    def __init__(self):
        super(MainWindow, self).__init__()
        scene = QGraphicsScene(self)
        self.map = thu_map()
        #self.map = QPixmap("../data/map.png")
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

