from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class SelectDialog(QDialog):
    result_signal = pyqtSignal(str)
    def __init__(self, string_list, parent = None):
        super(SelectDialog, self).__init__(parent)
        self.setModal(True)

        self.result = ""

        self.list_widget = QListWidget(self)
        self.list_widget.addItems(string_list)
        self.list_widget.itemClicked[QListWidgetItem].connect(self.get_result)

        self.ok_button = QPushButton(self)
        self.ok_button.clicked.connect(self.accept)
        self.ok_button.setText("确认")
        self.ok_button.setEnabled(False)

        self.v_layout = QVBoxLayout(self)
        self.v_layout.addWidget(self.list_widget)
        self.v_layout.addWidget(self.ok_button)

    def get_result(self, list_item):
        self.result = list_item.text()
        self.ok_button.setEnabled(True)

    def accept(self):
        super(SelectDialog, self).accept()
        self.result_signal.emit(self.result)


