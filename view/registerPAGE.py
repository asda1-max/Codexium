import sys
import control.registerControl as regisControl
from PySide6 import QtCore as QTC
from PySide6 import QtWidgets as QTW
from PySide6 import QtGui as QTUI

class regisGUI(QTW.QWidget):
    def __init__(self):
        super().__init__()

        self.title = QTW.QLabel(text="REGISTER NOW !", alignment=QTC.Qt.AlignHCenter)
        self.title.setFixedSize(800,60)
        self.title.setProperty("role", "title")

        self.label_username = QTW.QLabel(text="Username : ")

        self.usernameBox = QTW.QLineEdit(placeholderText="Username")
        self.usernameBox.setFixedSize(700,40)

        self.label_password = QTW.QLabel(text="Password : ")

        self.passwordBox = QTW.QLineEdit(placeholderText="Password")
        self.passwordBox.setEchoMode(QTW.QLineEdit.Password)
        self.passwordBox.setFixedSize(700,40)

        self.button_regis = QTW.QPushButton(text="Register Now!")
        self.button_regis.setFixedSize(300,40)
        self.button_regis.clicked.connect(self.registerAccount)

        self.button_reset = QTW.QPushButton(text="Reset")
        self.button_reset.clicked.connect(self.clear_box)
        self.button_reset.setFixedSize(300,40)
        self.button_reset.setProperty("role","reset")

        self.login_label = QTW.QLabel(text="Already have an account?")
        self.login_button = QTW.QPushButton(text="Login")
        self.login_button.clicked.connect(self.change_page)
        self.login_button.setFixedSize(120,25)
        self.login_button.setProperty("role", "smaller")

        self.Vlayout: QTW.QVBoxLayout = QTW.QVBoxLayout(self)
        self.Vlayout.setContentsMargins(12,50,12,8)
        self.Vlayout.setSpacing(10)
        
        self.Vlayout.addSpacing(100)
        self.Vlayout.addWidget(self.title, alignment = QTC.Qt.AlignHCenter)
        
        self.Vlayout.addSpacing(30)
        self.Hlayout_username : QTW.QHBoxLayout = QTW.QHBoxLayout()
        self.Hlayout_username.setContentsMargins(40,8,40,8)
        self.Hlayout_username.setSpacing(20)
        self.Hlayout_username.addWidget(self.label_username, alignment= QTC.Qt.AlignLeft)
        self.Hlayout_username.addWidget(self.usernameBox, alignment= QTC.Qt.AlignHCenter)
        self.Hlayout_username.setAlignment(QTC.Qt.AlignCenter)
        self.Vlayout.addLayout(self.Hlayout_username)

        self.Hlayout_password : QTW.QHBoxLayout = QTW.QHBoxLayout()
        self.Hlayout_password.setContentsMargins(40,8,40,8)
        self.Hlayout_password.setSpacing(20)
        self.Hlayout_password.addWidget(self.label_password, alignment= QTC.Qt.AlignLeft)
        self.Hlayout_password.addWidget(self.passwordBox, alignment= QTC.Qt.AlignHCenter)
        self.Hlayout_password.setAlignment(QTC.Qt.AlignCenter)
        self.Vlayout.addLayout(self.Hlayout_password)
        
        self.Vlayout.addSpacing(20)
        self.Hlayout_button : QTW.QHBoxLayout = QTW.QHBoxLayout()
        self.Hlayout_button.addWidget(self.button_regis,alignment= QTC.Qt.AlignHCenter)
        self.Hlayout_button.addWidget(self.button_reset,alignment= QTC.Qt.AlignHCenter)
        self.Hlayout_button.setAlignment(QTC.Qt.AlignHCenter)
        self.Vlayout.addLayout(self.Hlayout_button)

        self.Vlayout.addSpacing(120)
        self.Hlayout_login : QTW.QHBoxLayout =QTW.QHBoxLayout()
        self.Hlayout_login.addWidget(self.login_label, alignment= QTC.Qt.AlignCenter)
        self.Hlayout_login.addWidget(self.login_button, alignment= QTC.Qt.AlignCenter)
        self.Hlayout_login.setAlignment(QTC.Qt.AlignCenter)
        self.Vlayout.addLayout(self.Hlayout_login)
        self.Vlayout.setAlignment(QTC.Qt.AlignTop)
    
    def clear_box(self):
        self.passwordBox.setText("")
        self.usernameBox.setText("")

    def change_page(self):
        self.parentWidget().setCurrentIndex(0)
        
    def registerAccount(self):
        regisControl.registerThis(self.usernameBox.text(), self.passwordBox.text())
        self.clear_box()