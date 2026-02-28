import sys
import control.registerControl as regisControl
from PySide6 import QtCore as QTC
from PySide6 import QtWidgets as QTW
from PySide6 import QtGui as QTUI


class regisGUI(QTW.QWidget):
    """Modern card-based registration page."""

    def __init__(self):
        super().__init__()

        # ── brand header ─────────────────────────────────────────
        self.brand_icon = QTW.QLabel("✨")
        self.brand_icon.setStyleSheet("font-size: 48px;")
        self.brand_icon.setAlignment(QTC.Qt.AlignHCenter)

        self.brand_label = QTW.QLabel("Codexium")
        self.brand_label.setProperty("role", "brand")
        self.brand_label.setAlignment(QTC.Qt.AlignHCenter)

        self.brand_sub = QTW.QLabel("Create your encrypted vault")
        self.brand_sub.setProperty("role", "brand-sub")
        self.brand_sub.setAlignment(QTC.Qt.AlignHCenter)

        # ── title ────────────────────────────────────────────────
        self.title = QTW.QLabel("Create Account")
        self.title.setProperty("role", "title")
        self.title.setAlignment(QTC.Qt.AlignHCenter)

        self.subtitle = QTW.QLabel("Set up your secure credentials")
        self.subtitle.setProperty("role", "brand-sub")
        self.subtitle.setAlignment(QTC.Qt.AlignHCenter)

        # ── form fields ──────────────────────────────────────────
        self.label_username = QTW.QLabel("USERNAME")
        self.label_username.setProperty("role", "field-label")

        self.usernameBox = QTW.QLineEdit(placeholderText="Min. 6 characters")
        self.usernameBox.setFixedHeight(44)
        self.usernameBox.setMinimumWidth(380)

        self.label_password = QTW.QLabel("PASSWORD")
        self.label_password.setProperty("role", "field-label")

        self.passwordBox = QTW.QLineEdit(placeholderText="Min. 8 characters")
        self.passwordBox.setEchoMode(QTW.QLineEdit.Password)
        self.passwordBox.setFixedHeight(44)
        self.passwordBox.setMinimumWidth(380)

        # ── buttons ──────────────────────────────────────────────
        self.button_regis = QTW.QPushButton("Create Account")
        self.button_regis.setFixedHeight(44)
        self.button_regis.clicked.connect(self.registerAccount)
        self.button_regis.setCursor(QTC.Qt.PointingHandCursor)

        self.button_reveal = QTW.QPushButton("👁  Show")
        self.button_reveal.clicked.connect(self.reveal_password_box)
        self.button_reveal.setFixedSize(90, 44)
        self.button_reveal.setProperty("role", "secondary")
        self.button_reveal.setCursor(QTC.Qt.PointingHandCursor)

        self.button_reset = QTW.QPushButton("Clear")
        self.button_reset.clicked.connect(self.clear_box)
        self.button_reset.setFixedSize(90, 44)
        self.button_reset.setProperty("role", "ghost")
        self.button_reset.setCursor(QTC.Qt.PointingHandCursor)

        # ── login link ───────────────────────────────────────────
        self.login_label = QTW.QLabel("Already have an account?")
        self.login_label.setProperty("role", "brand-sub")

        self.login_button = QTW.QPushButton("Sign in")
        self.login_button.clicked.connect(self.change_page)
        self.login_button.setProperty("role", "smaller")
        self.login_button.setCursor(QTC.Qt.PointingHandCursor)

        # ══════════════════════════════════════════════════════════
        # CARD LAYOUT
        # ══════════════════════════════════════════════════════════

        card = QTW.QWidget()
        card.setProperty("role", "card")
        card.setFixedWidth(480)

        card_layout = QTW.QVBoxLayout(card)
        card_layout.setContentsMargins(48, 40, 48, 40)
        card_layout.setSpacing(6)

        card_layout.addWidget(self.brand_icon)
        card_layout.addWidget(self.brand_label)
        card_layout.addWidget(self.brand_sub)
        card_layout.addSpacing(28)
        card_layout.addWidget(self.title)
        card_layout.addWidget(self.subtitle)
        card_layout.addSpacing(24)

        # username field
        card_layout.addWidget(self.label_username)
        card_layout.addSpacing(4)
        card_layout.addWidget(self.usernameBox)
        card_layout.addSpacing(14)

        # password field + reveal
        card_layout.addWidget(self.label_password)
        card_layout.addSpacing(4)
        pw_row = QTW.QHBoxLayout()
        pw_row.setSpacing(8)
        pw_row.addWidget(self.passwordBox)
        pw_row.addWidget(self.button_reveal)
        card_layout.addLayout(pw_row)
        card_layout.addSpacing(24)

        # action buttons
        btn_row = QTW.QHBoxLayout()
        btn_row.setSpacing(10)
        btn_row.addWidget(self.button_regis, 1)
        btn_row.addWidget(self.button_reset)
        card_layout.addLayout(btn_row)
        card_layout.addSpacing(20)

        # separator
        sep = QTW.QFrame()
        sep.setFrameShape(QTW.QFrame.HLine)
        sep.setProperty("role", "separator")
        card_layout.addWidget(sep)
        card_layout.addSpacing(14)

        # login link
        login_row = QTW.QHBoxLayout()
        login_row.setAlignment(QTC.Qt.AlignCenter)
        login_row.addWidget(self.login_label)
        login_row.addWidget(self.login_button)
        card_layout.addLayout(login_row)

        # ── Center the card in the page ──────────────────────────
        outer = QTW.QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addStretch()
        h_center = QTW.QHBoxLayout()
        h_center.addStretch()
        h_center.addWidget(card)
        h_center.addStretch()
        outer.addLayout(h_center)
        outer.addStretch()

    # ── actions ──────────────────────────────────────────────────

    def clear_box(self):
        self.passwordBox.clear()
        self.usernameBox.clear()

    def change_page(self):
        self.parentWidget().setCurrentIndex(0)

    def registerAccount(self):
        username = self.usernameBox.text().strip()
        password = self.passwordBox.text()
        success = regisControl.registerThis(username, password)
        if success:
            self.clear_box()
            self.parentWidget().setCurrentIndex(0)

    def reveal_password_box(self):
        if self.passwordBox.echoMode() == QTW.QLineEdit.Password:
            self.button_reveal.setText("👁  Hide")
            self.passwordBox.setEchoMode(QTW.QLineEdit.Normal)
        else:
            self.button_reveal.setText("👁  Show")
            self.passwordBox.setEchoMode(QTW.QLineEdit.Password)
