from PySide6 import QtCore as QTC
from PySide6 import QtWidgets as QTW
from PySide6 import QtGui as QTUI
from view import dashboard_ui
from view import dialog_ui

class dialogue(QTW.QDialog):
    def __init__(self):
        super().__init__()
        self.dialogue_ui = dialog_ui.Ui_Dialog()
        self.dialogue_ui.setupUi(self)

        self.dialogue_ui.buttonBox.accepted.connect(self.acc)
        self.dialogue_ui.buttonBox.rejected.connect(self.rejected)
    
    def acc(self):
        self.text = self.dialogue_ui.lineEdit.text() 
        self.accept()

    def rejected(self):
        self.reject()

    def returnvar(self):
        return self.text

class dashboard(QTW.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = dashboard_ui.Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(self.addItem)
        self.ui.listWidget.currentItemChanged.connect(self.previewNode)

    def addItem(self):
        dial = dialogue()
        dial.exec()
        title = dial.returnvar()
        self.ui.listWidget.addItem(title)

    def previewNode(self, current, previous):
        if current:
            self.ui.lineEdit_2.setText(current.text())

