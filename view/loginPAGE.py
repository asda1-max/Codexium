import sys
from PySide6 import QtCore as QTC
from PySide6 import QtWidgets as QTW
from PySide6 import QtGui as QTUI

class loginGUI(QTW.QWidget):
    def __init__(self):
        super().__init__()

        self.title = QTW.QLabel(text="LOGIN NOW !", alignment=QTC.Qt.AlignHCenter)
        self.title.setFixedSize(800,80)
        self.title.setProperty("role", "title")

        self.usernameBox = QTW.QLineEdit(placeholderText="Username")

        self.usernameBox.setFixedSize(400,40)

        self.layout = QTW.QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.usernameBox)
 