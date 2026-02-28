import sys
import view.page_switcher
import control.graphicController as gCON
import PySide6.QtWidgets as QTW
from PySide6.QtGui import QFont, QFontDatabase


if __name__ == "__main__":
    app = QTW.QApplication(sys.argv)

    # ── global font ──────────────────────────────────────────
    font = QFont("Segoe UI", 10)
    font.setHintingPreference(QFont.PreferNoHinting)
    app.setFont(font)

    # ── stylesheet ───────────────────────────────────────────
    app.setStyleSheet(gCON.loadStyleSheet())

    # ── main window ──────────────────────────────────────────
    widget = view.page_switcher.page_switcher()
    widget.setWindowTitle("Codexium — Encrypted Notes")
    widget.setFixedSize(1650, 800)
    widget.show()

    sys.exit(app.exec())