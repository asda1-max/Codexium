import os
import uuid
import sqlite3
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


class NotesManager:
    """
    Manages encrypted notes using ChaCha20Poly1305 with the user's MEK key.
    All note titles and content are encrypted at rest.
    """

    def __init__(self, mek_key: bytes, user_uuid: str, database_path: str = "data/userData.db"):
        """
        Initialize the NotesManager.

        :param mek_key: The decrypted Master Encryption Key (16 bytes from uuid4)
        :param user_uuid: The user's UUID string
        :param database_path: Path to the SQLite database
        """
        self.mek_key = mek_key
        self.user_uuid = user_uuid
        self.database_path = database_path
        self._ensure_notes_table()

    # ── database helpers ─────────────────────────────────────────────

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def _ensure_notes_table(self):
        """Create the notes table if it doesn't exist."""
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS notes_data("
            "notes_id TEXT PRIMARY KEY, "
            "notes_title BLOB, "
            "title_nonce BLOB, "
            "notes_data BLOB, "
            "data_nonce BLOB, "
            "notes_owner TEXT"
            ")"
        )
        conn.commit()
        conn.close()

    # ── encryption helpers ───────────────────────────────────────────

    def _derive_key(self) -> bytes:
        """
        Derive a 256-bit key from the 128-bit MEK via duplication.
        ChaCha20Poly1305 requires a 32-byte key.
        """
        if len(self.mek_key) == 32:
            return self.mek_key
        return self.mek_key + self.mek_key  # 16 → 32 bytes

    def _encrypt(self, plaintext: bytes) -> tuple[bytes, bytes]:
        """Encrypt data, returning (ciphertext, nonce)."""
        key = self._derive_key()
        nonce = os.urandom(12)
        aad = uuid.UUID(self.user_uuid).bytes
        chacha = ChaCha20Poly1305(key)
        ciphertext = chacha.encrypt(nonce, plaintext, aad)
        return ciphertext, nonce

    def _decrypt(self, ciphertext: bytes, nonce: bytes) -> bytes:
        """Decrypt data back to plaintext bytes."""
        key = self._derive_key()
        aad = uuid.UUID(self.user_uuid).bytes
        chacha = ChaCha20Poly1305(key)
        return chacha.decrypt(nonce, ciphertext, aad)

    # ── CRUD operations ──────────────────────────────────────────────

    def add_note(self, title: str, content: str = "") -> str:
        """
        Create a new encrypted note.

        :param title: Note title (plaintext)
        :param content: Note content (plaintext)
        :return: The new note's UUID string
        """
        note_id = str(uuid.uuid4())
        enc_title, title_nonce = self._encrypt(title.encode("utf-8"))
        enc_content, data_nonce = self._encrypt(content.encode("utf-8"))

        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO notes_data VALUES (?, ?, ?, ?, ?, ?)",
            (note_id, enc_title, title_nonce, enc_content, data_nonce, self.user_uuid),
        )
        conn.commit()
        conn.close()
        return note_id

    def get_all_notes(self) -> list[tuple[str, str]]:
        """
        Fetch all notes for the current user.

        :return: List of (note_id, decrypted_title)
        """
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT notes_id, notes_title, title_nonce FROM notes_data WHERE notes_owner = ?",
            (self.user_uuid,),
        )
        rows = cur.fetchall()
        conn.close()

        results = []
        for note_id, enc_title, title_nonce in rows:
            try:
                title = self._decrypt(enc_title, title_nonce).decode("utf-8")
            except Exception:
                title = "[Decryption Error]"
            results.append((note_id, title))
        return results

    def get_note(self, note_id: str) -> tuple[str, str] | None:
        """
        Fetch and decrypt a single note.

        :param note_id: The note UUID
        :return: (decrypted_title, decrypted_content) or None
        """
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT notes_title, title_nonce, notes_data, data_nonce "
            "FROM notes_data WHERE notes_id = ? AND notes_owner = ?",
            (note_id, self.user_uuid),
        )
        row = cur.fetchone()
        conn.close()

        if row is None:
            return None

        enc_title, title_nonce, enc_content, data_nonce = row
        try:
            title = self._decrypt(enc_title, title_nonce).decode("utf-8")
            content = self._decrypt(enc_content, data_nonce).decode("utf-8")
        except Exception:
            return None
        return title, content

    def update_note(self, note_id: str, title: str, content: str) -> bool:
        """
        Re-encrypt and update an existing note.

        :param note_id: The note UUID
        :param title: New title (plaintext)
        :param content: New content (plaintext)
        :return: True if a row was updated
        """
        enc_title, title_nonce = self._encrypt(title.encode("utf-8"))
        enc_content, data_nonce = self._encrypt(content.encode("utf-8"))

        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "UPDATE notes_data SET notes_title = ?, title_nonce = ?, "
            "notes_data = ?, data_nonce = ? "
            "WHERE notes_id = ? AND notes_owner = ?",
            (enc_title, title_nonce, enc_content, data_nonce, note_id, self.user_uuid),
        )
        updated = cur.rowcount > 0
        conn.commit()
        conn.close()
        return updated

    def delete_note(self, note_id: str) -> bool:
        """
        Delete a note by ID.

        :param note_id: The note UUID
        :return: True if a row was deleted
        """
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM notes_data WHERE notes_id = ? AND notes_owner = ?",
            (note_id, self.user_uuid),
        )
        deleted = cur.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    def search_notes(self, query: str) -> list[tuple[str, str]]:
        """
        Search through decrypted note titles.

        :param query: Search term (case-insensitive)
        :return: List of (note_id, decrypted_title) that match
        """
        all_notes = self.get_all_notes()
        query_lower = query.lower()
        return [(nid, title) for nid, title in all_notes if query_lower in title.lower()]
