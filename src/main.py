from src.draw import *
from src.MapPin import *
from src.GetCurrentLocation import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("THU MAP")
        self.setFixedSize(680, 830)
        self.setWindowIcon(QIcon("../data/icons/icon.ico"))
        self.setMouseTracking(True)

        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralWidget)

        self.map = MapDisplay("../data/map.osm", self.centralWidget)
        self.map.setGeometry(QRect(0, 0, 680, 830))
        self.map.show()
        self.map.zoom_signal.connect(self.setZoomBarValue)
        self.map.press_signal.connect(self.pinAdd)

        #缩放按钮和指示条
        self.plus_button = QPushButton(self.centralWidget)
        self.plus_button.setGeometry(QRect(620, 600, 32, 32))
        self.plus_button.setStyleSheet(\
            "QPushButton{border: 0px;background-image:url(../data/icons/add/Add_Normal.png);}"\
            "QPushButton:hover{border: 0px;background-image:url(../data/icons/add/Add_Hover.png);}" \
            "QPushButton:pressed{border: 0px;background-image:url(../data/icons/add/Add_Pressed.png);}")
        self.plus_button.clicked.connect(self.zoomIn)

        self.minus_button = QPushButton(self.centralWidget)
        self.minus_button.setGeometry(QRect(620, 750, 32, 32))
        self.minus_button.setStyleSheet(\
            "QPushButton{border: 0px;background-image:url(../data/icons/minus/Minus_Normal.png);}" \
            "QPushButton:hover{border: 0px;background-image:url(../data/icons/minus/Minus_Hover.png);}" \
            "QPushButton:pressed{border: 0px;background-image:url(../data/icons/minus/Minus_Pressed.png);}")
        self.minus_button.clicked.connect(self.zoomOut)

        self.zoom_bar = QSlider(self.centralWidget)
        self.zoom_bar.setOrientation(Qt.Vertical)
        self.zoom_bar.setGeometry(620, 641, 32, 100)
        self.zoom_bar.setRange(0, 10)
        self.zoom_bar.valueChanged.connect(self.applyZoomBarValue)

        #地图上指示起点和终点的大头针
        self.start_pin = MapPin(self.centralWidget)
        self.start_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Red.png"))
        self.start_pin.setGeometry(QRect(0, 0, 24, 24))
        self.start_pin.color = "Red"
        self.start_pin.hide()
        self.start_pin.change_cursor.connect(self.changeCursorPin)
        self.start_pin.change_cursor.connect(self.changePinStatus)

        self.end_pin = MapPin(self.centralWidget)
        self.end_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Green.png"))
        self.end_pin.setGeometry(QRect(0, 0, 24, 24))
        self.end_pin.color = "Green"
        self.end_pin.hide()
        self.end_pin.change_cursor.connect(self.changeCursorPin)
        self.end_pin.change_cursor.connect(self.changePinStatus)

        #Pin标志位
        self.isPin = "None"

        #带有复杂功能的搜索框
        #使用Layout进行布局
        self.bg = QLabel(self.centralWidget)
        self.bg.setPixmap(QPixmap("../data/icons/Background.png"))
        self.bg.setGeometry(QRect(0, 0, 450, 150))

        self.search_frame = QWidget(self.centralWidget)
        self.search_frame.setGeometry(QRect(0, 0, 450, 150))

        self.v_layout = QVBoxLayout(self.search_frame)
        self.h_layout = QHBoxLayout(self.search_frame)
        self.v_layout.addLayout(self.h_layout)
        self.h_layout_shortcuts = QHBoxLayout(self.search_frame)
        self.v_layout.addLayout(self.h_layout_shortcuts)
        self.v_layout.setStretchFactor(self.h_layout, 2)
        self.v_layout.setStretchFactor(self.h_layout_shortcuts, 1)

        #上方输入栏
        self.swap = QPushButton(self.search_frame)
        self.swap.setFixedSize(48, 48)
        self.swap.setStyleSheet( \
            "QPushButton{border: 0px;background-image:url(../data/icons/swap/Swap_Normal.png);}" \
            "QPushButton:hover{border: 0px;background-image:url(../data/icons/swap/Swap_Hover.png);}" \
            "QPushButton:pressed{border: 0px;background-image:url(../data/icons/swap/Swap_Pressed.png);}")
        self.swap.clicked.connect(self.swapStartAndEnd)
        self.h_layout.addWidget(self.swap)
        self.v_layout_input = QVBoxLayout(self.search_frame)
        self.h_layout.addLayout(self.v_layout_input)
        self.search = QPushButton(self.search_frame)
        self.search.setFixedSize(90, 42)
        self.search.setStyleSheet( \
            "QPushButton{border: 0px;background-image:url(../data/icons/search/Search_Normal.png);}" \
            "QPushButton:hover{border: 0px;background-image:url(../data/icons/search/Search_Hover.png);}" \
            "QPushButton:pressed{border: 0px;background-image:url(../data/icons/search/Search_Pressed.png);}")
        self.h_layout.addWidget(self.search)
        self.h_layout.setStretchFactor(self.swap, 1)
        self.h_layout.setStretchFactor(self.v_layout_input, 6)
        self.h_layout.setStretchFactor(self.search, 2)

        self.h_layout_start = QHBoxLayout(self.search_frame)
        self.v_layout_input.addLayout(self.h_layout_start)
        self.h_layout_end = QHBoxLayout(self.search_frame)
        self.v_layout_input.addLayout(self.h_layout_end)

        #字体及颜色预设
        self.font = QFont("Microsoft YaHei", 14, 75)
        self.font_small = QFont("Microsoft YaHei", 12, 75)
        self.palette = QPalette()
        self.palette.setColor(QPalette.WindowText, Qt.white)
        self.palette.setColor(QPalette.ButtonText, Qt.white)

        self.start_tag = QLabel(self.search_frame)
        self.start_tag.setText("出发地：")
        self.start_tag.setFont(self.font)
        self.start_tag.setPalette(self.palette)
        self.h_layout_start.addWidget(self.start_tag)
        self.start_input = QLineEdit(self.search_frame)
        self.start_input.setFont(self.font_small)
        self.h_layout_start.addWidget(self.start_input)
        self.start_input_pin = MapPin(self.search_frame)
        self.start_input_pin.isInInput = True
        self.start_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Red.png"))
        self.start_input_pin.color = "Red"
        self.start_input_pin.change_cursor.connect(self.changeCursorPin)
        self.start_input_pin.change_cursor.connect(self.changePinStatus)
        self.h_layout_start.addWidget(self.start_input_pin)

        self.end_tag = QLabel(self.search_frame)
        self.end_tag.setText("目的地：")
        self.end_tag.setFont(self.font)
        self.end_tag.setPalette(self.palette)
        self.h_layout_end.addWidget(self.end_tag)
        self.end_input = QLineEdit(self.search_frame)
        self.end_input.setFont(self.font_small)
        self.h_layout_end.addWidget(self.end_input)
        self.end_input_pin = MapPin(self.search_frame)
        self.end_input_pin.isInInput = True
        self.end_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Green.png"))
        self.end_input_pin.color = "Green"
        self.end_input_pin.change_cursor.connect(self.changeCursorPin)
        self.end_input_pin.change_cursor.connect(self.changePinStatus)
        self.h_layout_end.addWidget(self.end_input_pin)

        #下方快捷按钮栏
        self.shortcuts = []
        self.shortcuts_captions = ["我的位置", "我要吃饭", "我要自习", "我要回寝"]
        for i in range(0, len(self.shortcuts_captions)):
            button = QPushButton(self.search_frame)
            button.setText(self.shortcuts_captions[i])
            button.setFont(self.font)
            button.setPalette(self.palette)
            button.setFlat(True)
            self.shortcuts.append(button)
            self.h_layout_shortcuts.addWidget(button)
        self.shortcuts[0].clicked.connect(self.addCurrentLocation)


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
            self.setCursor(cursor)
        elif color == "Green":
            cursor = QCursor(QPixmap("../data/icons/pin/Pin_Green.png"))
            self.setCursor(cursor)
        else :
            self.setCursor(Qt.ArrowCursor)

    def changePinStatus(self, color):
        if color == "Red":
            self.isPin = "Red"
        elif color == "Green":
            self.isPin = "Green"
        elif color == "RedBlank":
            self.isPin = "None"
            self.start_input_pin.isDisplay = True
            self.start_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Red.png"))
            self.start_input.clear()
        elif color == "GreenBlank":
            self.isPin = "None"
            self.end_input_pin.isDisplay = True
            self.end_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Green.png"))
            self.end_input.clear()

    def pinAdd(self, x, y):
        if self.isPin == "Red":
            self.start_pin.setGeometry(QRect(x - 12, y - 12, 24, 24))
            self.start_pin.isDisplay = True
            self.start_pin.show()
            self.setCursor(Qt.ArrowCursor)
            self.isPin = "None"
            mouse_coordinate = self.map.convertScreenToCoordinates(x, y)
            self.start_input.setText(
                "("+ str(round(mouse_coordinate[1], 3))+ "N,"+ str(round(mouse_coordinate[0], 3)) + "E)")
        elif self.isPin == "Green":
            self.end_pin.setGeometry(QRect(x - 12, y - 12, 24, 24))
            self.end_pin.isDisplay = True
            self.end_pin.show()
            self.setCursor(Qt.ArrowCursor)
            self.isPin = "None"
            mouse_coordinate = self.map.convertScreenToCoordinates(x, y)
            self.end_input.setText(
                "(" + str(round(mouse_coordinate[1], 3)) + "N," + str(round(mouse_coordinate[0], 3)) + "E)")

    def swapStartAndEnd(self):
        text = self.start_input.text()
        self.start_input.setText(self.end_input.text())
        self.end_input.setText(text)
        if self.start_pin.isDisplay == True:
            self.start_pin.isDisplay == False
            self.start_pin.hide()
            self.changeCursorPin("RedBlank")
            self.isPin = "None"
            self.start_input_pin.isDisplay = True
            self.start_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Red.png"))
        if self.end_pin.isDisplay == True:
            self.end_pin.isDisplay == False
            self.end_pin.hide()
            self.changeCursorPin("GreenBlank")
            self.isPin = "None"
            self.end_input_pin.isDisplay = True
            self.end_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Green.png"))

    def addCurrentLocation(self):
        curLocation = getLocation()
        self.start_input.setText(
            "(" + str(round(curLocation[1], 3)) + "N," + str(round(curLocation[0], 3)) + "E)")
        self.start_input_pin.isDisplay = True
        self.start_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Red.png"))
        self.start_pin.isDisplay = False
        self.start_pin.hide()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D and event.modifiers() == Qt.ControlModifier:
            if self.search_frame.isHidden() == True:
                self.search_frame.show()
                self.bg.show()
            else:
                self.search_frame.hide()
                self.bg.hide()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())