from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class thu_map(QGraphicsPixmapItem):
    def __init__(self):
        super(thu_map, self).__init__()
        self.setPixmap(QPixmap("../data/map.png"))
        self.zoom = 0
    def boundingRect(self):
        return QRectF(0, 0, 685, 831)
    def paint(self, painter, option, widget):
        #self.show()
        rectF = QRectF(0, 0, 685, 831)
        painter.drawPixmap(rectF, QPixmap("../data/map.png"),rectF)
    def wheelEvent(self, event):
        factor = 1
        if (self.zoom + event.delta() / 120.0) >= 0 and (self.zoom + event.delta() / 120.0) <= 5:
            factor = pow(1.2, event.delta() / 240.0)
            self.zoom = self.zoom + event.delta() / 120.0
        elif (self.zoom + event.delta() / 120.0) > 5:
            factor = pow(1.2, (5 - self.zoom) / 2)
            self.zoom = 5
        else:
            factor = pow(1.2, -self.zoom / 2)
            self.zoom = 0
        self.setTransform(QTransform.fromScale(factor, factor), True)
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

