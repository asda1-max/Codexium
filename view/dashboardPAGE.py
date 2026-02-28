from PySide6 import QtCore as QTC
from PySide6 import QtWidgets as QTW
from PySide6 import QtGui as QTUI
from control.notesControl import NotesController


class dialogue(QTW.QDialog):
    """Polished dialog to ask for a note title."""

    def __init__(self, window_title: str = "New Note", default_text: str = "NEW NOTE"):
        super().__init__()
        self.setWindowTitle(window_title)
        self.setFixedSize(420, 160)
        self.text = ""

        layout = QTW.QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.lineEdit = QTW.QLineEdit(default_text)
        self.lineEdit.setFixedHeight(40)
        self.lineEdit.selectAll()
        layout.addWidget(self.lineEdit)

        btn_row = QTW.QHBoxLayout()
        btn_row.setSpacing(10)
        btn_row.addStretch()

        self.btn_cancel = QTW.QPushButton("Cancel")
        self.btn_cancel.setProperty("role", "secondary")
        self.btn_cancel.setFixedSize(100, 36)
        self.btn_cancel.setCursor(QTC.Qt.PointingHandCursor)
        self.btn_cancel.clicked.connect(self.reject)
        btn_row.addWidget(self.btn_cancel)

        self.btn_ok = QTW.QPushButton("Confirm")
        self.btn_ok.setFixedSize(100, 36)
        self.btn_ok.setCursor(QTC.Qt.PointingHandCursor)
        self.btn_ok.clicked.connect(self._accept)
        btn_row.addWidget(self.btn_ok)

        layout.addLayout(btn_row)

    def _accept(self):
        self.text = self.lineEdit.text()
        self.accept()

    def returnvar(self) -> str:
        return self.text


class dashboard(QTW.QWidget):
    """
    Modern 3-column dashboard: sidebar  |  editor  |  toolbar
    Built entirely with layouts — no absolute positioning.
    """

    logout_requested = QTC.Signal()

    def __init__(self):
        super().__init__()

        self.notes_ctrl: NotesController | None = None
        self.current_note_id: str | None = None
        self._note_ids: list[str] = []

        self._build_ui()
        self._connect_signals()
        self._set_editor_enabled(False)

    # ══════════════════════════════════════════════════════════════
    # BUILD UI
    # ══════════════════════════════════════════════════════════════

    def _build_ui(self):
        root = QTW.QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── LEFT: sidebar ────────────────────────────────────────
        sidebar = QTW.QWidget()
        sidebar.setProperty("role", "sidebar")
        sidebar.setFixedWidth(280)
        sb_layout = QTW.QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(16, 16, 16, 16)
        sb_layout.setSpacing(10)

        # sidebar header
        sb_header = QTW.QHBoxLayout()
        sb_title = QTW.QLabel("📒  Notes")
        sb_title.setStyleSheet("font-size: 16px; font-weight: 700; color: #ffffff;")
        sb_header.addWidget(sb_title)
        sb_header.addStretch()
        sb_layout.addLayout(sb_header)

        # search
        self.search_input = QTW.QLineEdit()
        self.search_input.setPlaceholderText("🔍  Search notes…")
        self.search_input.setProperty("role", "search")
        self.search_input.setFixedHeight(36)
        sb_layout.addWidget(self.search_input)

        # add note button
        self.btn_add = QTW.QPushButton("＋  New Note")
        self.btn_add.setProperty("role", "sidebar-action")
        self.btn_add.setFixedHeight(38)
        self.btn_add.setCursor(QTC.Qt.PointingHandCursor)
        sb_layout.addWidget(self.btn_add)

        # section label
        lbl_all = QTW.QLabel("ALL NOTES")
        lbl_all.setProperty("role", "section-header")
        sb_layout.addSpacing(4)
        sb_layout.addWidget(lbl_all)

        # notes list
        self.listWidget = QTW.QListWidget()
        sb_layout.addWidget(self.listWidget, 1)

        # version
        ver = QTW.QLabel("Codexium v1.0")
        ver.setProperty("role", "version")
        ver.setAlignment(QTC.Qt.AlignCenter)
        sb_layout.addWidget(ver)

        root.addWidget(sidebar)

        # ── MIDDLE: editor area ──────────────────────────────────
        editor_wrapper = QTW.QWidget()
        ed_layout = QTW.QVBoxLayout(editor_wrapper)
        ed_layout.setContentsMargins(24, 20, 24, 20)
        ed_layout.setSpacing(12)

        # note title editor
        self.title_input = QTW.QLineEdit()
        self.title_input.setProperty("role", "title-editor")
        self.title_input.setPlaceholderText("Note title")
        self.title_input.setReadOnly(True)
        self.title_input.setFixedHeight(48)
        ed_layout.addWidget(self.title_input)

        # note content
        self.textEdit = QTW.QTextEdit()
        self.textEdit.setPlaceholderText("Select a note or create a new one to start writing…")
        ed_layout.addWidget(self.textEdit, 1)

        # bottom status bar (subtle)
        self.status_label = QTW.QLabel("No note selected")
        self.status_label.setProperty("role", "version")
        ed_layout.addWidget(self.status_label)

        root.addWidget(editor_wrapper, 1)

        # ── RIGHT: toolbar ───────────────────────────────────────
        toolbar = QTW.QWidget()
        toolbar.setProperty("role", "toolbar")
        toolbar.setFixedWidth(190)
        tb_layout = QTW.QVBoxLayout(toolbar)
        tb_layout.setContentsMargins(16, 20, 16, 20)
        tb_layout.setSpacing(10)

        tb_title = QTW.QLabel("ACTIONS")
        tb_title.setProperty("role", "section-header")
        tb_layout.addWidget(tb_title)
        tb_layout.addSpacing(4)

        self.btn_save = QTW.QPushButton("💾  Save Note")
        self.btn_save.setProperty("role", "save")
        self.btn_save.setFixedHeight(42)
        self.btn_save.setCursor(QTC.Qt.PointingHandCursor)
        tb_layout.addWidget(self.btn_save)

        self.btn_rename = QTW.QPushButton("✏️  Rename")
        self.btn_rename.setProperty("role", "toolbar-btn")
        self.btn_rename.setFixedHeight(42)
        self.btn_rename.setCursor(QTC.Qt.PointingHandCursor)
        tb_layout.addWidget(self.btn_rename)

        self.btn_delete = QTW.QPushButton("🗑  Delete")
        self.btn_delete.setProperty("role", "toolbar-danger")
        self.btn_delete.setFixedHeight(42)
        self.btn_delete.setCursor(QTC.Qt.PointingHandCursor)
        tb_layout.addWidget(self.btn_delete)

        tb_layout.addStretch()

        sep = QTW.QFrame()
        sep.setFrameShape(QTW.QFrame.HLine)
        sep.setProperty("role", "separator")
        tb_layout.addWidget(sep)
        tb_layout.addSpacing(6)

        self.btn_account = QTW.QPushButton("⚙  Settings")
        self.btn_account.setProperty("role", "toolbar-btn")
        self.btn_account.setFixedHeight(42)
        self.btn_account.setCursor(QTC.Qt.PointingHandCursor)
        tb_layout.addWidget(self.btn_account)

        self.btn_logout = QTW.QPushButton("🚪  Logout")
        self.btn_logout.setProperty("role", "toolbar-danger")
        self.btn_logout.setFixedHeight(42)
        self.btn_logout.setCursor(QTC.Qt.PointingHandCursor)
        tb_layout.addWidget(self.btn_logout)

        root.addWidget(toolbar)

    # ══════════════════════════════════════════════════════════════
    # SIGNALS
    # ══════════════════════════════════════════════════════════════

    def _connect_signals(self):
        self.btn_add.clicked.connect(self.addItem)
        self.btn_save.clicked.connect(self.saveNote)
        self.btn_rename.clicked.connect(self.renameNote)
        self.btn_delete.clicked.connect(self.deleteNote)
        self.btn_account.clicked.connect(self._on_account_settings)
        self.btn_logout.clicked.connect(self._on_logout)
        self.listWidget.currentRowChanged.connect(self._on_note_selected)
        self.search_input.textChanged.connect(self._on_search)

    # ══════════════════════════════════════════════════════════════
    # SESSION
    # ══════════════════════════════════════════════════════════════

    def initialize_session(self, mek_key: bytes, user_uuid: str):
        self.notes_ctrl = NotesController(mek_key, user_uuid)
        self._refresh_note_list()

    def clear_session(self):
        self.notes_ctrl = None
        self.current_note_id = None
        self._note_ids.clear()
        self.listWidget.clear()
        self.search_input.clear()
        self.title_input.clear()
        self.textEdit.clear()
        self.status_label.setText("No note selected")
        self._set_editor_enabled(False)

    # ══════════════════════════════════════════════════════════════
    # LIST HELPERS
    # ══════════════════════════════════════════════════════════════

    def _refresh_note_list(self, search_query: str = ""):
        if self.notes_ctrl is None:
            return

        self.listWidget.blockSignals(True)
        self.listWidget.clear()
        self._note_ids.clear()

        notes = (
            self.notes_ctrl.search(search_query)
            if search_query
            else self.notes_ctrl.list_notes()
        )

        for note_id, title in notes:
            self._note_ids.append(note_id)
            self.listWidget.addItem(title)

        self.listWidget.blockSignals(False)

        if self.current_note_id in self._note_ids:
            idx = self._note_ids.index(self.current_note_id)
            self.listWidget.setCurrentRow(idx)
        else:
            self.current_note_id = None
            self.title_input.clear()
            self.textEdit.clear()
            self.status_label.setText("No note selected")
            self._set_editor_enabled(False)

    def _set_editor_enabled(self, enabled: bool):
        self.textEdit.setReadOnly(not enabled)
        self.title_input.setReadOnly(not enabled)
        self.btn_save.setEnabled(enabled)
        self.btn_delete.setEnabled(enabled)
        self.btn_rename.setEnabled(enabled)

    # ══════════════════════════════════════════════════════════════
    # SLOTS
    # ══════════════════════════════════════════════════════════════

    def _on_note_selected(self, row: int):
        if row < 0 or row >= len(self._note_ids) or self.notes_ctrl is None:
            return

        note_id = self._note_ids[row]
        result = self.notes_ctrl.open_note(note_id)
        if result is None:
            QTW.QMessageBox.warning(self, "Error", "Could not decrypt this note.")
            return

        title, content = result
        self.current_note_id = note_id
        self.title_input.setText(title)
        self.textEdit.setPlainText(content)
        self.status_label.setText(f"Editing  ·  {len(content)} chars  ·  Encrypted ✓")
        self._set_editor_enabled(True)

    def _on_search(self, text: str):
        self._refresh_note_list(text.strip())

    # ── CRUD ─────────────────────────────────────────────────────

    def addItem(self):
        if self.notes_ctrl is None:
            return

        dial = dialogue("New Note", "Untitled Note")
        if dial.exec() != QTW.QDialog.Accepted:
            return

        title = dial.returnvar().strip()
        if not title:
            return

        note_id = self.notes_ctrl.create_note(title, "")
        self._refresh_note_list(self.search_input.text().strip())

        if note_id in self._note_ids:
            self.listWidget.setCurrentRow(self._note_ids.index(note_id))

    def saveNote(self):
        if self.notes_ctrl is None or self.current_note_id is None:
            return

        title = self.title_input.text().strip()
        content = self.textEdit.toPlainText()

        if not title:
            QTW.QMessageBox.warning(self, "Empty Title", "Note title cannot be empty.")
            return

        ok = self.notes_ctrl.save_note(self.current_note_id, title, content)
        if ok:
            self.status_label.setText(f"Saved ✓  ·  {len(content)} chars  ·  Encrypted")
            self._refresh_note_list(self.search_input.text().strip())
        else:
            QTW.QMessageBox.critical(self, "Error", "Failed to save the note.")

    def deleteNote(self):
        if self.notes_ctrl is None or self.current_note_id is None:
            return

        reply = QTW.QMessageBox.question(
            self, "Delete Note",
            "Are you sure you want to permanently delete this note?\nThis cannot be undone.",
            QTW.QMessageBox.Yes | QTW.QMessageBox.No, QTW.QMessageBox.No,
        )
        if reply != QTW.QMessageBox.Yes:
            return

        self.notes_ctrl.remove_note(self.current_note_id)
        self.current_note_id = None
        self.title_input.clear()
        self.textEdit.clear()
        self.status_label.setText("Note deleted")
        self._set_editor_enabled(False)
        self._refresh_note_list(self.search_input.text().strip())

    def renameNote(self):
        if self.notes_ctrl is None or self.current_note_id is None:
            QTW.QMessageBox.information(self, "No Note", "Select a note first.")
            return

        dial = dialogue("Rename Note", self.title_input.text())
        if dial.exec() != QTW.QDialog.Accepted:
            return

        new_title = dial.returnvar().strip()
        if not new_title:
            return

        content = self.textEdit.toPlainText()
        self.notes_ctrl.save_note(self.current_note_id, new_title, content)
        self.title_input.setText(new_title)
        self._refresh_note_list(self.search_input.text().strip())

    # ── misc ─────────────────────────────────────────────────────

    def _on_account_settings(self):
        QTW.QMessageBox.information(self, "Account", "Account settings coming soon.")

    def _on_logout(self):
        reply = QTW.QMessageBox.question(
            self, "Logout", "Are you sure you want to logout?",
            QTW.QMessageBox.Yes | QTW.QMessageBox.No, QTW.QMessageBox.No,
        )
        if reply == QTW.QMessageBox.Yes:
            self.logout_requested.emit()
