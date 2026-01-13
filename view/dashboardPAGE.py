from PySide6 import QtCore as QTC
from PySide6 import QtWidgets as QTW
from PySide6 import QtGui as QTUI
from view import dashboard_ui

class dashboard(QTW.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = dashboard_ui.Ui_Form()
        self.ui.setupUi(self)
