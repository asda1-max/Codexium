import sys
import view.page_switcher
from control import loginControl
from PySide6 import QtCore as QTC
from PySide6 import QtWidgets as QTW
from PySide6 import QtGui as QTUI


class loginGUI(QTW.QWidget):
    """Modern card-based login page."""

    # Signal emitted on successful login: (mek_bytes, user_uuid_str)
    login_success = QTC.Signal(bytes, str)

    def __init__(self):
        super().__init__()

        # ── brand header ─────────────────────────────────────────
        self.brand_icon = QTW.QLabel("🔐")
        self.brand_icon.setStyleSheet("font-size: 48px;")
        self.brand_icon.setAlignment(QTC.Qt.AlignHCenter)

        self.brand_label = QTW.QLabel("Codexium")
        self.brand_label.setProperty("role", "brand")
        self.brand_label.setAlignment(QTC.Qt.AlignHCenter)

        self.brand_sub = QTW.QLabel("Your encrypted knowledge vault")
        self.brand_sub.setProperty("role", "brand-sub")
        self.brand_sub.setAlignment(QTC.Qt.AlignHCenter)

        # ── title ────────────────────────────────────────────────
        self.title = QTW.QLabel("Welcome back")
        self.title.setProperty("role", "title")
        self.title.setAlignment(QTC.Qt.AlignHCenter)

        self.subtitle = QTW.QLabel("Sign in to access your notes")
        self.subtitle.setProperty("role", "brand-sub")
        self.subtitle.setAlignment(QTC.Qt.AlignHCenter)

        # ── form fields ──────────────────────────────────────────
        self.label_username = QTW.QLabel("USERNAME")
        self.label_username.setProperty("role", "field-label")

        self.usernameBox = QTW.QLineEdit(placeholderText="Enter your username")
        self.usernameBox.setFixedHeight(44)
        self.usernameBox.setMinimumWidth(380)

        self.label_password = QTW.QLabel("PASSWORD")
        self.label_password.setProperty("role", "field-label")

        self.passwordBox = QTW.QLineEdit(placeholderText="Enter your password")
        self.passwordBox.setEchoMode(QTW.QLineEdit.Password)
        self.passwordBox.setFixedHeight(44)
        self.passwordBox.setMinimumWidth(380)

        # ── buttons ──────────────────────────────────────────────
        self.button_login = QTW.QPushButton("Sign In")
        self.button_login.clicked.connect(self.loginThis)
        self.button_login.setFixedHeight(44)
        self.button_login.setCursor(QTC.Qt.PointingHandCursor)

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

        # ── register link ────────────────────────────────────────
        self.regis_label = QTW.QLabel("Don't have an account?")
        self.regis_label.setProperty("role", "brand-sub")

        self.regis_button = QTW.QPushButton("Create one")
        self.regis_button.clicked.connect(self.change_page)
        self.regis_button.setProperty("role", "smaller")
        self.regis_button.setCursor(QTC.Qt.PointingHandCursor)

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
        btn_row.addWidget(self.button_login, 1)
        btn_row.addWidget(self.button_reset)
        card_layout.addLayout(btn_row)
        card_layout.addSpacing(20)

        # separator
        sep = QTW.QFrame()
        sep.setFrameShape(QTW.QFrame.HLine)
        sep.setProperty("role", "separator")
        card_layout.addWidget(sep)
        card_layout.addSpacing(14)

        # register link
        reg_row = QTW.QHBoxLayout()
        reg_row.setAlignment(QTC.Qt.AlignCenter)
        reg_row.addWidget(self.regis_label)
        reg_row.addWidget(self.regis_button)
        card_layout.addLayout(reg_row)

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

    def change_page(self):
        self.parentWidget().setCurrentIndex(1)

    def clear_box(self):
        self.usernameBox.clear()
        self.passwordBox.clear()

    def reveal_password_box(self):
        if self.passwordBox.echoMode() == QTW.QLineEdit.Password:
            self.button_reveal.setText("👁  Hide")
            self.passwordBox.setEchoMode(QTW.QLineEdit.Normal)
        else:
            self.button_reveal.setText("👁  Show")
            self.passwordBox.setEchoMode(QTW.QLineEdit.Password)

    def loginThis(self):
        username = self.usernameBox.text().strip()
        password = self.passwordBox.text()
        success, data = loginControl.login(username, password)
        if success and data is not None:
            self.login_success.emit(data["mek"], data["uuid"])
