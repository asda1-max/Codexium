import view.loginPAGE
import view.registerPAGE
import view.dashboardPAGE

from PySide6 import QtCore as QTC
from PySide6 import QtWidgets as QTW
from PySide6 import QtGui as QTUI

class page_switcher(QTW.QWidget):
    def __init__(self):
        super().__init__()
        self.stackWidget = QTW.QStackedWidget()
        self.stackWidget.addWidget(view.loginPAGE.loginGUI())
        self.stackWidget.addWidget(view.registerPAGE.regisGUI())
        self.stackWidget.addWidget(view.dashboardPAGE.dashboard())
        self.layouts = QTW.QVBoxLayout(self)
        self.layouts.addWidget(self.stackWidget)
    
    

