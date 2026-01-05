import sys
import view.page_switcher
import control.graphicController as gCON
import PySide6.QtWidgets as QTW


if __name__ == "__main__":
    app = QTW.QApplication(sys.argv)
    app.setStyleSheet(gCON.loadStyleSheet())
    widget = view.page_switcher.page_switcher()
    widget.setFixedSize(1200,800)
    widget.show()

    sys.exit(app.exec())        