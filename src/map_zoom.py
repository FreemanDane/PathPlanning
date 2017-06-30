from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

max_zoom = 10

class thuMap(QGraphicsPixmapItem, QObject):
    def __init__(self):
        super(thuMap, self).__init__()
        self.setPixmap(QPixmap("../data/map.png"))
        self.show()
        self.setTransformationMode(Qt.SmoothTransformation)
        self.size_x = 685.0
        self.size_y = 831.0
        self.zoom = [0, 0]              #第一个代表鼠标滚动之前（过去状态），第二个代表鼠标滚动之后（当前状态）
        self.mouse = QPointF(0, 0)      #发生事件时鼠标在屏幕上的位置（相对窗口左上角）
        self.mouse_true = QPointF(0, 0) #发生点击事件时鼠标在图片上的位置（相对图片左上角）
        self.top_left = QPointF(0, 0)   #图片左上角坐标
        self.is_zoom = 0                #缩放事件标记
        self.is_press = 0               #鼠标按下事件标记
        self.before_drag = QPointF(0, 0)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
    def boundingRect(self):
        return QRectF(self.top_left.x(), self.top_left.y(), self.size_x * pow(1.2, 0.5 * self.zoom[1]), self.size_y * pow(1.2, 0.5 * self.zoom[1]))
    def paint(self, painter, option, widget):
        if self.is_zoom == 1:
            zoom_change = self.zoom[1] - self.zoom[0]

            #计算左上角x
            if zoom_change >= 0:
                x = self.top_left.x() - (pow(1.2, -0.5 * self.zoom[0]) - pow(1.2, -0.5 * self.zoom[1])) * self.mouse.x()
            else:
                x = ((pow(1.2, 0.5 * self.zoom[1]) - 1) * pow(1.2, 0.5 * self.zoom[0])) / ((pow(1.2, 0.5 * self.zoom[0]) - 1) * pow(1.2, 0.5 * self.zoom[1])) * self.top_left.x()

            #计算左上角y
            if zoom_change >= 0:
                y = self.top_left.y() - (pow(1.2, -0.5 * self.zoom[0]) - pow(1.2, -0.5 * self.zoom[1])) * self.mouse.y()
            else:
                y = ((pow(1.2, 0.5 * self.zoom[1]) - 1) * pow(1.2, 0.5 * self.zoom[0])) / ((pow(1.2, 0.5 * self.zoom[0]) - 1) * pow(1.2, 0.5 * self.zoom[1])) * self.top_left.y()

            self.top_left = QPointF(x, y)
            self.is_zoom = 0

        elif self.is_press == 1:
            #计算左上角x
            x = pow(1.2, -0.5 * self.zoom[1]) * self.mouse.x() - self.before_drag.x()
            if x > 0:
                x = 0
            elif x < pow(1.2, -0.5 * self.zoom[1]) * self.size_x - self.size_x:
                x = pow(1.2, -0.5 * self.zoom[1]) * self.size_x - self.size_x

            #计算左上角y
            y = pow(1.2, -0.5 * self.zoom[1]) * self.mouse.y() - self.before_drag.y()
            if y > 0:
                y = 0
            elif y < pow(1.2, -0.5 * self.zoom[1]) * self.size_y - self.size_y:
                y = pow(1.2, -0.5 * self.zoom[1]) * self.size_y - self.size_y

            self.top_left = QPointF(x, y)
        pixmap = self.pixmap()
        target = QRectF(self.top_left.x(), self.top_left.y(), self.size_x, self.size_y)
        source = QRectF(0, 0, self.size_x, self.size_y)
        painter.drawPixmap(target, pixmap, source)
        self.is_zoom = 0
    #鼠标滚轮事件
    def wheelEvent(self, event):
        self.is_zoom = 1
        factor = 1.0

        x = event.pos().x() * pow(1.2, 0.5 * self.zoom[1])
        y = event.pos().y() * pow(1.2, 0.5 * self.zoom[1])
        self.zoom[0] = self.zoom[1]
        self.mouse = QPointF(x, y)
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
        super(thuMap, self).wheelEvent(event)
    #鼠标拖拽事件
    def mousePressEvent(self, event):
        self.is_press = 1
        x = event.pos().x() * pow(1.2, 0.5 * self.zoom[1])
        y = event.pos().y() * pow(1.2, 0.5 * self.zoom[1])
        self.mouse = QPointF(x, y)
        self.before_drag = self.convertScreenToImage(self.mouse)
        super(thuMap, self).mousePressEvent(event)
    def mouseReleaseEvent(self, event):
        self.is_press = 0
        super(thuMap, self).mouseReleaseEvent(event)
    def mouseMoveEvent(self, event):
        if self.is_press == 1:
            x = event.pos().x() * pow(1.2, 0.5 * self.zoom[1])
            y = event.pos().y() * pow(1.2, 0.5 * self.zoom[1])
            self.mouse = QPointF(x, y)
        self.update()
        super(thuMap, self).mouseMoveEvent(event)
    #坐标变换函数
    def convertScreenToImage(self, point):
        image_x = point.x() / pow(1.2, 0.5 * self.zoom[1]) - self.top_left.x()
        image_y = point.y() / pow(1.2, 0.5 * self.zoom[1]) - self.top_left.y()
        return QPointF(image_x, image_y)
    #放大函数
    def zoomIn(self):
        x = self.size_x / 2
        y = self.size_y / 2
        self.mouse = QPointF(x, y)
        self.is_zoom = 1
        self.zoom[0] = self.zoom[1]
        if self.zoom[1] < max_zoom:
            self.zoom[1] = self.zoom[1] + 1
            factor = pow(1.2, 0.5)
            self.setTransform(QTransform.fromScale(factor, factor), True)
            self.update()
    #缩小函数
    def zoomOut(self):
        self.is_zoom = 1
        self.zoom[0] = self.zoom[1]
        if self.zoom[1] > 0:
            self.zoom[1] = self.zoom[1] - 1
            factor = pow(1.2, -0.5)
            self.setTransform(QTransform.fromScale(factor, factor), True)
            self.update()

class graphicView(QGraphicsView):
    def __init__(self, CentralWidget):
        super(graphicView, self).__init__(CentralWidget)
        scene = QGraphicsScene(self)
        self.map = thuMap()
        scene.addItem(self.map)
        scene.setSceneRect(0, 0, 687, 833)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)


class Ui_MainWindow(object):
    def setupUI(self, MainWindow):
        MainWindow.setWindowTitle("THU MAP")
        MainWindow.setFixedSize(687, 833)
        MainWindow.setWindowIcon(QIcon("../data/icons/icon.ico"))
        MainWindow.setObjectName("MainWindow")

        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralWidget)
        self.graphicsView = graphicView(self.centralWidget)
        self.graphicsView.setGeometry(QRect(0, 0, 689, 835))
        self.graphicsView.show()
        #缩放按钮和指示条
        self.plus_button = QPushButton(self.centralWidget)
        self.plus_button.setGeometry(QRect(620, 600, 32, 32))
        self.plus_button.setStyleSheet(\
            "QPushButton{border: 0px;background-image:url(../data/icons/add/Add_Normal.png);}"\
            "QPushButton:hover{border: 0px;background-image:url(../data/icons/add/Add_Hover.png);}" \
            "QPushButton:pressed{border: 0px;background-image:url(../data/icons/add/Add_Pressed.png);}")
        self.plus_button.show()
        self.plus_button.clicked.connect(self.zoomIn)

        self.minus_button = QPushButton(self.centralWidget)
        self.minus_button.setGeometry(QRect(620, 750, 32, 32))
        self.minus_button.setStyleSheet(\
            "QPushButton{border: 0px;background-image:url(../data/icons/minus/Minus_Normal.png);}" \
            "QPushButton:hover{border: 0px;background-image:url(../data/icons/minus/Minus_Hover.png);}" \
            "QPushButton:pressed{border: 0px;background-image:url(../data/icons/minus/Minus_Pressed.png);}")
        self.minus_button.show()
        self.minus_button.clicked.connect(self.zoomOut)

    def zoomIn(self):
        self.graphicsView.map.zoomIn()
    def zoomOut(self):
        self.graphicsView.map.zoomOut()
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

