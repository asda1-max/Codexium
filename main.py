import sys
import view.loginPAGE
import control.graphicController as gCON
import PySide6.QtWidgets as QTW


if __name__ == "__main__":
    app = QTW.QApplication(sys.argv)
    app.setStyleSheet(gCON.loadStyleSheet())
    widget = view.loginPAGE.loginGUI()
    widget.setFixedSize(800,600)
    widget.show()

    sys.exit(app.exec())        