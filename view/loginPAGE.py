import sys
from PySide6 import QtCore as QTC
from PySide6 import QtWidgets as QTW
from PySide6 import QtGui as QTUI

class loginGUI(QTW.QWidget):
    def __init__(self):
        super().__init__()

        self.title = QTW.QLabel(text="LOGIN NOW !", alignment=QTC.Qt.AlignHCenter)
        self.title.setFixedSize(800,60)
        self.title.setProperty("role", "title")

        self.label_username = QTW.QLabel(text="Username : ")

        self.usernameBox = QTW.QLineEdit(placeholderText="Username")
        self.usernameBox.setFixedSize(400,40)

        self.label_password = QTW.QLabel(text="Password :")

        self.passwordBox = QTW.QLineEdit(placeholderText="Password")
        self.passwordBox.setFixedSize(400,40)

        self.button = QTW.QPushButton(text="Login")

        self.Vlayout: QTW.QVBoxLayout = QTW.QVBoxLayout(self)
        self.Vlayout.setContentsMargins(12,8,12,8)
        self.Vlayout.setSpacing(4)
        self.Vlayout.addWidget(self.title, alignment = QTC.Qt.AlignHCenter)

        self.Hlayout_username : QTW.QHBoxLayout = QTW.QHBoxLayout()
        self.Hlayout_username.setContentsMargins(12,8,12,8)
        self.Hlayout_username.setSpacing(4)
        self.Hlayout_username.addWidget(self.label_username, alignment= QTC.Qt.AlignHCenter)
        self.Hlayout_username.addWidget(self.usernameBox, alignment= QTC.Qt.AlignHCenter)
        self.Vlayout.addLayout(self.Hlayout_username)

        self.Hlayout_password : QTW.QHBoxLayout = QTW.QHBoxLayout()
        self.Hlayout_password.setContentsMargins(12,8,12,8)
        self.Hlayout_password.setSpacing(4)
        self.Hlayout_password.addWidget(self.label_password, alignment= QTC.Qt.AlignHCenter)
        self.Hlayout_password.addWidget(self.passwordBox, alignment= QTC.Qt.AlignHCenter)
        self.Vlayout.addLayout(self.Hlayout_password)

        self.Vlayout.addWidget(self.button)