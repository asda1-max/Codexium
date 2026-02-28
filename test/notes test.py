from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import sqlite3
import os

class encrypt_notes():
    def __init__(self,database_name, mek,notes):
        self.database_name = database_name
        self.mek_key = mek
        self.notes_data = notes.encode()
        self.connnect_database()

    def connnect_database(self):
        self.connection = sqlite3.connect(self.database_name)
        self.current = self.connection.cursor()

    def create_database(self):
        self.current.execute("create table notes_data(notes_id, notes_title, notes_data, nonce, notes_owner)")

    def register_data(self):
        self.connect_database()
        self.current.execute("insert into user values (?, ?, ?)", (self.username, self.login_password_verifier, self.encrypted_mek_key))
        self.connection.commit()