from src.draw import *
from src.MapPin import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("THU MAP")
        self.setFixedSize(680, 830)
        self.setWindowIcon(QIcon("../data/icons/icon.ico"))

        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralWidget)

        self.map = MapDisplay("../data/map.osm", self.centralWidget)
        self.map.setGeometry(QRect(0, 0, 680, 830))
        self.map.show()
        self.map.zoom_signal.connect(self.setZoomBarValue)

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

        self.zoom_bar = QSlider(self.centralWidget)
        self.zoom_bar.setOrientation(Qt.Vertical)
        self.zoom_bar.setGeometry(620, 641, 32, 100)
        self.zoom_bar.setRange(0, 10)
        self.zoom_bar.valueChanged.connect(self.applyZoomBarValue)
        self.zoom_bar.show()

        #地图上指示起点和终点的大头针
        self.start_pin = MapPin(self.centralWidget)
        self.start_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Red.png"))
        self.start_pin.setGeometry(QRect(0, 0, 24, 24))
        self.start_pin.color = "Red"
        self.start_pin.hide()

        self.end_pin = MapPin(self.centralWidget)
        self.end_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Green.png"))
        self.end_pin.setGeometry(QRect(0, 0, 24, 24))
        self.start_pin.color = "Green"
        self.end_pin.hide()

        #带有复杂功能的搜索框
        #使用Layout进行布局
        self.bg = QLabel(self.centralWidget)
        self.bg.setPixmap(QPixmap("../data/icons/Background.png"))
        self.bg.setGeometry(QRect(0, 0, 450, 100))

        self.h_layout_frame = QWidget(self.centralWidget)
        self.h_layout_frame.setGeometry(QRect(0, 0, 450, 100))

        self.h_layout = QHBoxLayout(self.h_layout_frame)
        self.swap = QPushButton(self.h_layout_frame)
        self.swap.setFixedSize(48, 48)
        self.swap.setStyleSheet( \
            "QPushButton{border: 0px;background-image:url(../data/icons/swap/Swap_Normal.png);}" \
            "QPushButton:hover{border: 0px;background-image:url(../data/icons/swap/Swap_Hover.png);}" \
            "QPushButton:pressed{border: 0px;background-image:url(../data/icons/swap/Swap_Pressed.png);}")
        self.h_layout.addWidget(self.swap)
        self.v_layout = QVBoxLayout(self.h_layout_frame)
        self.h_layout.addLayout(self.v_layout)
        self.search = QPushButton(self.h_layout_frame)
        self.search.setFixedSize(90, 42)
        self.search.setStyleSheet( \
            "QPushButton{border: 0px;background-image:url(../data/icons/search/Search_Normal.png);}" \
            "QPushButton:hover{border: 0px;background-image:url(../data/icons/search/Search_Hover.png);}" \
            "QPushButton:pressed{border: 0px;background-image:url(../data/icons/search/Search_Pressed.png);}")
        self.h_layout.addWidget(self.search)
        self.h_layout.setStretchFactor(self.swap, 1)
        self.h_layout.setStretchFactor(self.v_layout, 6)
        self.h_layout.setStretchFactor(self.search, 2)

        self.h_layout_start = QHBoxLayout(self.h_layout_frame)
        self.v_layout.addLayout(self.h_layout_start)
        self.h_layout_end = QHBoxLayout(self.h_layout_frame)
        self.v_layout.addLayout(self.h_layout_end)

        self.font = QFont("Microsoft YaHei", 14, 75)
        self.palette = QPalette()
        self.palette.setColor(QPalette.WindowText, Qt.white)

        self.start_tag = QLabel(self.h_layout_frame)
        self.start_tag.setText("出发地：")
        self.start_tag.setFont(self.font)
        self.start_tag.setPalette(self.palette)
        self.h_layout_start.addWidget(self.start_tag)
        self.start_input = QLineEdit(self.h_layout_frame)
        self.h_layout_start.addWidget(self.start_input)
        self.start_input_pin = MapPin(self.h_layout_frame)
        self.start_input_pin.isInInput = True
        self.start_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Red.png"))
        self.start_input_pin.color = "Red"
        self.start_input_pin.change_cursor.connect(self.changeCursorPin)
        self.h_layout_start.addWidget(self.start_input_pin)

        self.end_tag = QLabel(self.h_layout_frame)
        self.end_tag.setText("目的地：")
        self.end_tag.setFont(self.font)
        self.end_tag.setPalette(self.palette)
        self.h_layout_end.addWidget(self.end_tag)
        self.end_input = QLineEdit(self.h_layout_frame)
        self.h_layout_end.addWidget(self.end_input)
        self.end_input_pin = MapPin(self.h_layout_frame)
        self.end_input_pin.isInInput = True
        self.end_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Green.png"))
        self.end_input_pin.color = "Green"
        self.end_input_pin.change_cursor.connect(self.changeCursorPin)
        self.h_layout_end.addWidget(self.end_input_pin)

    def zoomIn(self):
        self.map.zoomIn()

    def zoomOut(self):
        self.map.zoomOut()

    def setZoomBarValue(self):
        self.zoom_bar.setValue(self.map.zoom[1])

    def applyZoomBarValue(self):
        if self.zoom_bar.value() > self.map.zoom[1]:
            for i in range(int(self.map.zoom[1]), self.zoom_bar.value()):
                self.map.zoomIn()
        elif self.zoom_bar.value() < self.map.zoom[1]:
            for i in range(self.zoom_bar.value(), int(self.map.zoom[1])):
                self.map.zoomOut()

    def changeCursorPin(self, color):
        if color == "Red":
            cursor = QCursor(QPixmap("../data/icons/pin/Pin_Red.png"))
            MainWindow.setCursor(cursor)
        elif color == "Green":
            cursor = QCursor(QPixmap("../data/icons/pin/Pin_Green.png"))
            MainWindow.setCursor(cursor)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D and event.modifiers() == Qt.ControlModifier:
            if self.h_layout_frame.isHidden() == True:
                self.h_layout_frame.show()
                self.bg.show()
            else:
                self.h_layout_frame.hide()
                self.bg.hide()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())