import view.loginPAGE
import view.registerPAGE
import view.dashboardPAGE

from PySide6 import QtCore as QTC
from PySide6 import QtWidgets as QTW
from PySide6 import QtGui as QTUI


class page_switcher(QTW.QWidget):
    """
    Central stacked-widget that manages page navigation and
    passes encrypted user data (MEK, UUID) between pages.
    """

    PAGE_LOGIN = 0
    PAGE_REGISTER = 1
    PAGE_DASHBOARD = 2

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Codexium")

        self.stackWidget = QTW.QStackedWidget()

        # ── pages ────────────────────────────────────────────────
        self.loginPage = view.loginPAGE.loginGUI()
        self.registerPage = view.registerPAGE.regisGUI()
        self.dashboardPage = view.dashboardPAGE.dashboard()

        self.stackWidget.addWidget(self.loginPage)       # index 0
        self.stackWidget.addWidget(self.registerPage)     # index 1
        self.stackWidget.addWidget(self.dashboardPage)    # index 2

        self.layouts = QTW.QVBoxLayout(self)
        self.layouts.setContentsMargins(0, 0, 0, 0)
        self.layouts.addWidget(self.stackWidget)

        # ── signals ──────────────────────────────────────────────
        self.loginPage.login_success.connect(self._on_login_success)
        self.dashboardPage.logout_requested.connect(self._on_logout)

    # ── slots ────────────────────────────────────────────────────

    def _on_login_success(self, mek: bytes, user_uuid: str):
        """Called when login succeeds — hand the MEK to the dashboard."""
        self.dashboardPage.initialize_session(mek, user_uuid)
        self.stackWidget.setCurrentIndex(self.PAGE_DASHBOARD)

    def _on_logout(self):
        """Return to login page and clear sensitive state."""
        self.dashboardPage.clear_session()
        self.loginPage.usernameBox.clear()
        self.loginPage.passwordBox.clear()
        self.stackWidget.setCurrentIndex(self.PAGE_LOGIN)
