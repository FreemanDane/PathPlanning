# coding=utf-8
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication
from PyQt5.QtGui import QPixmap
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    scene = QGraphicsScene()
    scene.addPixmap(QPixmap("../data/map.png"))
    view = QGraphicsView(scene)
    view.show()
    sys.exit(app.exec_())
