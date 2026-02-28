from model.notesManager import NotesManager


class NotesController:
    """
    Controller layer for encrypted notes operations.
    Wraps NotesManager and provides a clean API for the view layer.
    """

    def __init__(self, mek_key: bytes, user_uuid: str, database_path: str = "data/userData.db"):
        self.manager = NotesManager(mek_key, user_uuid, database_path)

    def create_note(self, title: str, content: str = "") -> str:
        """Create a new encrypted note, returning its ID."""
        return self.manager.add_note(title, content)

    def list_notes(self) -> list[tuple[str, str]]:
        """Return all (note_id, decrypted_title) for the user."""
        return self.manager.get_all_notes()

    def open_note(self, note_id: str) -> tuple[str, str] | None:
        """Return (title, content) for a given note, or None."""
        return self.manager.get_note(note_id)

    def save_note(self, note_id: str, title: str, content: str) -> bool:
        """Re-encrypt and persist changes to a note."""
        return self.manager.update_note(note_id, title, content)

    def remove_note(self, note_id: str) -> bool:
        """Delete a note permanently."""
        return self.manager.delete_note(note_id)

    def search(self, query: str) -> list[tuple[str, str]]:
        """Search decrypted note titles for a query string."""
        return self.manager.search_notes(query)
