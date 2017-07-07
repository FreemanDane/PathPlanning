from src.draw import *
from src.MapPin import *
#from GetCurrentLocation import *
from src.FindBestWay import *
from src.Dialog import *
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

        self.loading = QLabel(self.centralWidget)
        self.loading.setPixmap(QPixmap("../data/icons/Loading.png"))
        self.loading.setGeometry(QRect(0, 0, 680, 830))
        self.loading.show()

        self.temp_timer = QTimer()
        self.temp_timer.singleShot(100, self.setupUI)

    def setupUI(self):
        self.loading.hide()

        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralWidget)

        #地图信息设置
        self.map = MapDisplay("../data/map.osm", self.centralWidget)
        self.map.setGeometry(QRect(0, 0, 680, 830))
        self.map.show()
        self.map.zoom_signal.connect(self.setZoomBarValue)
        self.map.zoom_signal.connect(self.setPinChange)
        self.map.press_signal.connect(self.pinAdd)
        self.map.move_signal.connect(self.setPinChange)

        # 地图上指示起点和终点的大头针
        self.start_pin_pos = QPointF(0, 0)
        self.start_pin = MapPin(self.centralWidget)
        self.start_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Red.png"))
        self.start_pin.setGeometry(QRect(0, 0, 24, 24))
        self.start_pin.color = "Red"
        self.start_pin.hide()
        self.start_pin.isDisplay = False
        self.start_pin.change_cursor.connect(self.changeCursorPin)
        self.start_pin.change_cursor.connect(self.changePinStatus)

        self.end_pin_pos = QPointF(0, 0)
        self.end_pin = MapPin(self.centralWidget)
        self.end_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Green.png"))
        self.end_pin.setGeometry(QRect(0, 0, 24, 24))
        self.end_pin.color = "Green"
        self.end_pin.hide()
        self.end_pin.isDisplay = False
        self.end_pin.change_cursor.connect(self.changeCursorPin)
        self.end_pin.change_cursor.connect(self.changePinStatus)

        # Pin标志位
        self.isPin = "None"

        # 带有复杂功能的搜索框
        # 使用Layout进行布局
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

        # 上方输入栏
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
        self.search.setFixedSize(45, 41)
        self.search.setStyleSheet( \
            "QPushButton{border: 0px;background-image:url(../data/icons/walk/Walk_Normal.png);}" \
            "QPushButton:hover{border: 0px;background-image:url(../data/icons/walk/Walk_Hover.png);}" \
            "QPushButton:pressed{border: 0px;background-image:url(../data/icons/walk/Walk_Pressed.png);}")
        self.h_layout.addWidget(self.search)
        self.search.clicked.connect(self.drawBestWay)
        self.search_bike = QPushButton(self.search_frame)
        self.search_bike.setFixedSize(45, 41)
        self.search_bike.setStyleSheet( \
            "QPushButton{border: 0px;background-image:url(../data/icons/bike/Bike_Normal.png);}" \
            "QPushButton:hover{border: 0px;background-image:url(../data/icons/bike/Bike_Hover.png);}" \
            "QPushButton:pressed{border: 0px;background-image:url(../data/icons/bike/Bike_Pressed.png);}")
        self.h_layout.addWidget(self.search_bike)
        self.search_bike.clicked.connect(self.drawBestRideWay)
        self.h_layout.setStretchFactor(self.swap, 1)
        self.h_layout.setStretchFactor(self.v_layout_input, 6)
        self.h_layout.setStretchFactor(self.search, 1)
        self.h_layout.setStretchFactor(self.search_bike, 1)

        self.h_layout_start = QHBoxLayout(self.search_frame)
        self.v_layout_input.addLayout(self.h_layout_start)
        self.h_layout_end = QHBoxLayout(self.search_frame)
        self.v_layout_input.addLayout(self.h_layout_end)

        # 字体及颜色预设
        self.font = QFont("Microsoft YaHei", 14, 75)
        self.font_small = QFont("Microsoft YaHei", 10, 75)
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

        # 下方快捷按钮栏
        self.shortcuts = []
        self.shortcuts_captions = ["我的位置", "我要吃饭", "我要运动", "我要自习", "我要约会"]
        self.signal_mapper = QSignalMapper()
        for i in range(0, len(self.shortcuts_captions)):
            button = QPushButton(self.search_frame)
            button.setText(self.shortcuts_captions[i])
            button.setFont(self.font)
            button.setPalette(self.palette)
            button.setFlat(True)
            self.shortcuts.append(button)
            self.h_layout_shortcuts.addWidget(button)
            button.clicked.connect(self.signal_mapper.map)
            self.signal_mapper.setMapping(button, i)
        #self.shortcuts[0].clicked.connect(self.addCurrentLocation)
        self.signal_mapper.mapped[int].connect(self.needRequest)

        # 缩放按钮和指示条
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setOffset(-5, 5)
        self.shadow_effect.setColor(Qt.gray)
        self.shadow_effect.setBlurRadius(8)

        self.plus_button = QPushButton(self.centralWidget)
        self.plus_button.setGeometry(QRect(620, 600, 32, 32))
        self.plus_button.setStyleSheet( \
            "QPushButton{border: 0px;background-image:url(../data/icons/add/Add_Normal.png);}" \
            "QPushButton:hover{border: 0px;background-image:url(../data/icons/add/Add_Hover.png);}" \
            "QPushButton:pressed{border: 0px;background-image:url(../data/icons/add/Add_Pressed.png);}")
        self.plus_button.clicked.connect(self.zoomIn)

        self.minus_button = QPushButton(self.centralWidget)
        self.minus_button.setGeometry(QRect(620, 750, 32, 32))
        self.minus_button.setStyleSheet( \
            "QPushButton{border: 0px;background-image:url(../data/icons/minus/Minus_Normal.png);}" \
            "QPushButton:hover{border: 0px;background-image:url(../data/icons/minus/Minus_Hover.png);}" \
            "QPushButton:pressed{border: 0px;background-image:url(../data/icons/minus/Minus_Pressed.png);}")
        self.minus_button.clicked.connect(self.zoomOut)

        self.zoom_bar = QSlider(self.centralWidget)
        self.zoom_bar.setOrientation(Qt.Vertical)
        self.zoom_bar.setGeometry(620, 641, 32, 100)
        self.zoom_bar.setRange(0, 50)
        self.zoom_bar.setGraphicsEffect(self.shadow_effect)
        self.zoom_bar.valueChanged.connect(self.applyZoomBarValue)

        # 寻找最优路径
        self.painter = QPainter()
        self.timer = QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.adjustToBestWay)
        self.zoom_tag = "None"

        '''
        以下是正则匹配的调用方式：
        name_list = Regular_match_name(self.map.map, "东门")
        print(name_list)'''
        self.update()

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

    def setPinChange(self):
        if self.start_pin.isDisplay == True:
            screen_pos = self.map.convertCoordinatesToScreen(self.start_pin_pos.x(), self.start_pin_pos.y())
            self.start_pin.setGeometry(screen_pos[0] - 12, screen_pos[1] - 24, 24, 24)
        if self.end_pin.isDisplay == True:
            screen_pos = self.map.convertCoordinatesToScreen(self.end_pin_pos.x(), self.end_pin_pos.y())
            self.end_pin.setGeometry(screen_pos[0] - 12, screen_pos[1] - 24, 24, 24)

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
        self.map.show_path = False
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
        self.map.update()

    def pinAdd(self, x, y):
        if self.isPin == "Red":
            self.start_pin.setGeometry(QRect(x - 12, y - 12, 24, 24))
            self.start_pin.isDisplay = True
            self.start_pin.show()
            self.setCursor(Qt.ArrowCursor)
            self.isPin = "None"
            mouse_coordinate = self.map.convertScreenToCoordinates(x, y + 12)
            self.start_pin_pos = QPointF(mouse_coordinate[0], mouse_coordinate[1])
            self.start_input.setText(
                "("+ str(round(mouse_coordinate[1], 5))+ "N,"+ str(round(mouse_coordinate[0], 5)) + "E)")
        elif self.isPin == "Green":
            self.end_pin.setGeometry(QRect(x - 12, y - 12, 24, 24))
            self.end_pin.isDisplay = True
            self.end_pin.show()
            self.setCursor(Qt.ArrowCursor)
            self.isPin = "None"
            mouse_coordinate = self.map.convertScreenToCoordinates(x, y + 12)
            self.end_pin_pos = QPointF(mouse_coordinate[0], mouse_coordinate[1])
            self.end_input.setText(
                "(" + str(round(mouse_coordinate[1], 5)) + "N," + str(round(mouse_coordinate[0], 5)) + "E)")

    def swapStartAndEnd(self):
        text = self.start_input.text()
        self.start_input.setText(self.end_input.text())
        self.end_input.setText(text)
        if self.start_pin.isDisplay == True:
            self.start_pin.isDisplay = False
            self.start_pin.hide()
            self.changeCursorPin("RedBlank")
            self.isPin = "None"
            self.start_input_pin.isDisplay = True
            self.start_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Red.png"))
        if self.end_pin.isDisplay == True:
            self.end_pin.isDisplay = False
            self.end_pin.hide()
            self.changeCursorPin("GreenBlank")
            self.isPin = "None"
            self.end_input_pin.isDisplay = True
            self.end_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Green.png"))
        self.map.show_path = False
        self.update()

    def drawBestWay(self):
        if self.start_input.text() == "":
            warning = QMessageBox.warning(self, "警告", "没有输入出发地！", QMessageBox.Yes)
            return
        if self.end_input.text() == "":
            warning = QMessageBox.warning(self, "警告", "没有输入目的地！", QMessageBox.Yes)
            return

        import re
        coordinate_pattern = re.compile(r'\([1-9]([0-9])*?\.([0-9])+?N,[1-9]([0-9])*?\.([0-9])+?E\)')
        start_coordinate = [-1, -1]
        end_coordinate = [-1, -1]

        #出发地坐标
        if coordinate_pattern.match(self.start_input.text()) != None:
            result = self.start_input.text().split(',')
            lat = float(result[0][1:-1])
            lon = float(result[1][:-2])
            start_coordinate[0] = lon
            start_coordinate[1] = lat
        else:
            if len(self.start_input.text()) <= 5 or self.start_input.text()[-5:] != "(已选中)":
                name_list = Regular_match_name(self.map.map, self.start_input.text())
                if len(name_list) <= 0:
                    warning = QMessageBox.warning(self, "警告", "没有找到出发地！", QMessageBox.Yes)
                    return
                elif len(name_list) >= 2:
                    start_dialog = SelectDialog(name_list, self)
                    start_dialog.setWindowTitle("您想选择哪一个出发地")
                    start_dialog.show()
                    start_dialog.result_signal[str].connect(self.startInputComplete)
                    return
                else:
                    name = name_list[0]
            else:
                name = self.start_input.text()[0:-5]
            node = find_the_name_of_points(self.map.map, name)
            if node.id == -2:
                start_coordinate[0] = node.lon
                start_coordinate[1] = node.lat
                warning = QMessageBox.warning(self, "警告", "没有找到出发地！", QMessageBox.Yes)
                return
            start_coordinate[0] = node.lon
            start_coordinate[1] = node.lat

        #目的地坐标
        if coordinate_pattern.match(self.end_input.text()) != None:
            result = self.end_input.text().split(',')
            lat = float(result[0][1:-1])
            lon = float(result[1][:-2])
            end_coordinate[0] = lon
            end_coordinate[1] = lat
        else:
            if len(self.end_input.text()) <= 5 or self.end_input.text()[-5:] != "(已选中)":
                name_list = Regular_match_name(self.map.map, self.end_input.text())
                if len(name_list) <= 0:
                    warning = QMessageBox.warning(self, "警告", "没有找到目的地！", QMessageBox.Yes)
                    return
                elif len(name_list) >= 2:
                    end_dialog = SelectDialog(name_list, self)
                    end_dialog.setWindowTitle("您想选择哪一个目的地")
                    end_dialog.show()
                    end_dialog.result_signal[str].connect(self.endInputComplete)
                    return
                else:
                    name = name_list[0]
            else:
                name = self.end_input.text()[0:-5]
            node = find_the_name_of_points(self.map.map, name)
            if node.id == -2:
                end_coordinate[0] = node.lon
                end_coordinate[1] = node.lat
                warning = QMessageBox.warning(self, "警告", "没有找到目的地！", QMessageBox.Yes)
                return
            end_coordinate[0] = node.lon
            end_coordinate[1] = node.lat

        if start_coordinate[0] != -1 and end_coordinate[0] != -1:
            if self.start_input_pin.isDisplay == True:
                self.start_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Blank.png"))
                self.start_input_pin.isDisplay = False
            if self.start_pin.isDisplay == False:
                self.start_pin.isDisplay = True
            self.start_pin_pos = QPointF(start_coordinate[0], start_coordinate[1])
            pos = self.map.convertCoordinatesToScreen(self.start_pin_pos.x(), self.start_pin_pos.y())
            self.start_pin.setGeometry(pos[0] - 12, pos[1] - 24, 24, 24)
            self.start_pin.show()

            if self.end_input_pin.isDisplay == True:
                self.end_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Blank.png"))
                self.end_input_pin.isDisplay = False
            if self.end_pin.isDisplay == False:
                self.end_pin.isDisplay = True
            self.end_pin_pos = QPointF(end_coordinate[0], end_coordinate[1])
            pos = self.map.convertCoordinatesToScreen(self.end_pin_pos.x(), self.end_pin_pos.y())
            self.end_pin.setGeometry(pos[0] - 12, pos[1] - 24, 24, 24)
            self.end_pin.show()

            self.setPinChange()
            self.road_list, self.min_distance = search_by_node(self.map.map, start_coordinate[1], start_coordinate[0], end_coordinate[1], end_coordinate[0])
            if self.min_distance == -1:
                warning = QMessageBox.warning(self, "警告", "没有合适的道路！", QMessageBox.Yes)
                return
            else:
                self.map.getPath(self.road_list, self.min_distance)
                self.map.show_path = True
                self.timer.start()
                self.update()

    def adjustToBestWay(self):
        start_pos = self.map.convertCoordinatesToScreen(self.start_pin_pos.x(), self.start_pin_pos.y())
        end_pos = self.map.convertCoordinatesToScreen(self.end_pin_pos.x(), self.end_pin_pos.y())
        center_x = (start_pos[0] + end_pos[0]) / 2
        center_y = (start_pos[1] + end_pos[1]) / 2

        import math

        delta_x = abs(start_pos[0] - end_pos[0])
        delta_y = abs(start_pos[1] - end_pos[1])
        delta = pow((delta_x * delta_x + delta_y * delta_y), 0.5)
        if delta_x == 0:
            angle = math.pi / 2
        else:
            angle = math.atan(delta_y / delta_x)

        if angle <= math.atan(830 / 680):
            limit = 680 / cos(angle)
        else:
            limit = 830 / sin(angle)

        if self.zoom_tag == "None":
            if delta < limit / 2:
                self.zoom_tag = "In"
            elif delta > limit * 3 / 4:
                self.zoom_tag = "Out"
            else:
                self.timer.stop()
                self.map.Move(340 - center_x, 415 - center_y)
        elif self.zoom_tag == "In":
            if delta > limit * 2 / 3 or self.map.zoom[1] == self.map.max_zoom:
                self.timer.stop()
                self.zoom_tag = "None"
            self.map.zoomIn(center_x, center_y)
            self.map.Move(340 - center_x, 415 - center_y)

        elif self.zoom_tag == "Out":
            if delta < limit * 2 / 3 or self.map.zoom[1] == 0:
                self.timer.stop()
                self.zoom_tag = "None"
            self.map.zoomOut(center_x, center_y)
            self.map.Move(340 - center_x, 415 - center_y)

    def needRequest(self, need):
        if self.start_input.text() == "":
            warning = QMessageBox.warning(self, "警告", "没有输入出发地！", QMessageBox.Yes)
            return

        if need == 0:
            return

        import re
        coordinate_pattern = re.compile(r'\([1-9]([0-9])*?\.([0-9])+?N,[1-9]([0-9])*?\.([0-9])+?E\)')
        start_coordinate = [-1, -1]
        end_coordinate = [-1, -1]
        if coordinate_pattern.match(self.start_input.text()) != None:
            result = self.start_input.text().split(',')
            lat = float(result[0][1:-1])
            lon = float(result[1][:-2])
            start_coordinate[0] = lon
            start_coordinate[1] = lat
        else:
            node = find_the_name_of_points(self.map.map, self.start_input.text())
            if node.id == -2:
                start_coordinate[0] = node.lon
                start_coordinate[1] = node.lat
                warning = QMessageBox.warning(self, "警告", "没有找到出发地！", QMessageBox.Yes)
                return
            else:
                start_coordinate[0] = node.lon
                start_coordinate[1] = node.lat
        if start_coordinate[0] != -1:
            if self.start_input_pin.isDisplay == True:
                self.start_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Blank.png"))
                self.start_input_pin.isDisplay = False
            if self.start_pin.isDisplay == False:
                self.start_pin.isDisplay = True
            self.start_pin_pos = QPointF(start_coordinate[0], start_coordinate[1])
            pos = self.map.convertCoordinatesToScreen(self.start_pin_pos.x(), self.start_pin_pos.y())
            self.start_pin.setGeometry(pos[0] - 12, pos[1] - 24, 24, 24)
            self.start_pin.show()

            self.road_list, self.min_distance, self.place_name = search_by_need(self.map.map, start_coordinate[1], start_coordinate[0], need)
            str = ["", "食堂", "运动场地", "自习室", "约会场所"]
            if self.min_distance == -1 and self.place_name == "":
                warning = QMessageBox.warning(self, "警告", "没有找到合适的" + str[need] +"!", QMessageBox.Yes)
                return
            else:
                self.end_input.setText(self.place_name)
                node = find_the_name_of_points(self.map.map, self.place_name)
                end_coordinate[0] = node.lon
                end_coordinate[1] = node.lat

                if self.end_input_pin.isDisplay == True:
                    self.end_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Blank.png"))
                    self.end_input_pin.isDisplay = False
                if self.end_pin.isDisplay == False:
                    self.end_pin.isDisplay = True
                self.end_pin_pos = QPointF(end_coordinate[0], end_coordinate[1])
                pos = self.map.convertCoordinatesToScreen(self.end_pin_pos.x(), self.end_pin_pos.y())
                self.end_pin.setGeometry(pos[0] - 12, pos[1] - 24, 24, 24)
                self.end_pin.show()

                self.setPinChange()

                self.map.getPath(self.road_list, self.min_distance)
                self.map.show_path = True
                self.timer.start()
                self.update()

    def drawBestRideWay(self):
        if self.start_input.text() == "":
            warning = QMessageBox.warning(self, "警告", "没有输入出发地！", QMessageBox.Yes)
            return
        if self.end_input.text() == "":
            warning = QMessageBox.warning(self, "警告", "没有输入目的地！", QMessageBox.Yes)
            return

        import re
        coordinate_pattern = re.compile(r'\([1-9]([0-9])*?\.([0-9])+?N,[1-9]([0-9])*?\.([0-9])+?E\)')
        start_coordinate = [-1, -1]
        end_coordinate = [-1, -1]

        # 出发地坐标
        if coordinate_pattern.match(self.start_input.text()) != None:
            result = self.start_input.text().split(',')
            lat = float(result[0][1:-1])
            lon = float(result[1][:-2])
            start_coordinate[0] = lon
            start_coordinate[1] = lat
        else:
            if len(self.start_input.text()) <= 5 or self.start_input.text()[-5:] != "(已选中)":
                name_list = Regular_match_name(self.map.map, self.start_input.text())
                if len(name_list) <= 0:
                    warning = QMessageBox.warning(self, "警告", "没有找到出发地！", QMessageBox.Yes)
                    return
                elif len(name_list) >= 2:
                    start_dialog = SelectDialog(name_list, self)
                    start_dialog.setWindowTitle("您想选择哪一个出发地")
                    start_dialog.show()
                    start_dialog.result_signal[str].connect(self.startInputComplete)
                    return
                else:
                    name = name_list[0]
            else:
                name = self.start_input.text()[0:-5]
            node = find_the_name_of_points(self.map.map, name)
            if node.id == -2:
                start_coordinate[0] = node.lon
                start_coordinate[1] = node.lat
                warning = QMessageBox.warning(self, "警告", "没有找到出发地！", QMessageBox.Yes)
                return
            start_coordinate[0] = node.lon
            start_coordinate[1] = node.lat

        # 目的地坐标
        if coordinate_pattern.match(self.end_input.text()) != None:
            result = self.end_input.text().split(',')
            lat = float(result[0][1:-1])
            lon = float(result[1][:-2])
            end_coordinate[0] = lon
            end_coordinate[1] = lat
        else:
            if len(self.end_input.text()) <= 5 or self.end_input.text()[-5:] != "(已选中)":
                name_list = Regular_match_name(self.map.map, self.end_input.text())
                if len(name_list) <= 0:
                    warning = QMessageBox.warning(self, "警告", "没有找到目的地！", QMessageBox.Yes)
                    return
                elif len(name_list) >= 2:
                    end_dialog = SelectDialog(name_list, self)
                    end_dialog.setWindowTitle("您想选择哪一个目的地")
                    end_dialog.show()
                    end_dialog.result_signal[str].connect(self.endInputComplete)
                    return
                else:
                    name = name_list[0]
            else:
                name = self.end_input.text()[0:-5]
            node = find_the_name_of_points(self.map.map, name)
            if node.id == -2:
                end_coordinate[0] = node.lon
                end_coordinate[1] = node.lat
                warning = QMessageBox.warning(self, "警告", "没有找到目的地！", QMessageBox.Yes)
                return
            end_coordinate[0] = node.lon
            end_coordinate[1] = node.lat

        if start_coordinate[0] != -1 and end_coordinate[0] != -1:
            if self.start_input_pin.isDisplay == True:
                self.start_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Blank.png"))
                self.start_input_pin.isDisplay = False
            if self.start_pin.isDisplay == False:
                self.start_pin.isDisplay = True
            self.start_pin_pos = QPointF(start_coordinate[0], start_coordinate[1])
            pos = self.map.convertCoordinatesToScreen(self.start_pin_pos.x(), self.start_pin_pos.y())
            self.start_pin.setGeometry(pos[0] - 12, pos[1] - 24, 24, 24)
            self.start_pin.show()

            if self.end_input_pin.isDisplay == True:
                self.end_input_pin.setPixmap(QPixmap("../data/icons/pin/Pin_Blank.png"))
                self.end_input_pin.isDisplay = False
            if self.end_pin.isDisplay == False:
                self.end_pin.isDisplay = True
            self.end_pin_pos = QPointF(end_coordinate[0], end_coordinate[1])
            pos = self.map.convertCoordinatesToScreen(self.end_pin_pos.x(), self.end_pin_pos.y())
            self.end_pin.setGeometry(pos[0] - 12, pos[1] - 24, 24, 24)
            self.end_pin.show()

            self.setPinChange()
            self.road_list, self.min_distance = search_by_node_best_riding_way(self.map.map, start_coordinate[1], start_coordinate[0], end_coordinate[1], end_coordinate[0])
            if self.min_distance == -1:
                warning = QMessageBox.warning(self, "警告", "没有合适的道路！", QMessageBox.Yes)
                return
            else:
                self.map.getPath(self.road_list, self.min_distance)
                self.map.show_path = True
                self.timer.start()
                self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D and event.modifiers() == Qt.ControlModifier:
            if self.search_frame.isHidden() == True:
                self.search_frame.show()
                self.bg.show()
            else:
                self.search_frame.hide()
                self.bg.hide()
        elif event.key() == Qt.Key_Return:
            self.drawBestWay()

    def startInputComplete(self, str):
        self.start_input.setText(str + "(已选中)")

    def endInputComplete(self, str):
        self.end_input.setText(str + "(已选中)")




if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())