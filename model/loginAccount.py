import sqlite3
import os
import uuid
from argon2 import PasswordHasher, hash_password_raw
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
def check_data(username,password,database_name):
        connection = sqlite3.connect(database_name)
        current = connection.cursor()
        try:
                query = current.execute("SELECT pw_verifier from user_data where username = ?", (username,))
                pw_verifier = query.fetchone()[0]
                query = current.execute("SELECT mek_salt from user_data where username = ?", (username,))
                salt_MEK = query.fetchone()[0]
                query = current.execute("SELECT encrypted_mek_key from user_data where username = ?", (username,))
                encrypted_mek = query.fetchone()[0]
                query = current.execute("SELECT uuid from user_data where username = ?", (username,))
                userid = query.fetchone()[0]
                query = current.execute("SELECT nonce from user_data where username = ?", (username,))
                nonce = query.fetchone()[0]
        except:
                return False
        connection.close()
        try:
                PasswordHasher().verify(pw_verifier, password)
                print("Password verified successfully")
        except Exception as e:
                print("Invalid password")
                return False
        
        decrypt_mek(password, salt_MEK, encrypted_mek, userid, nonce)
        
        return True
def decrypt_mek(password, salt_MEK, encrypted_mek,userid, nonce):
        mek_key_by_user_password = hash_password_raw(
            password= password.encode(),
            salt= salt_MEK,
            time_cost=3,
            memory_cost= 77777,
            hash_len=32,
        )

        data = encrypted_mek
        aad = uuid.UUID(userid).bytes
        key = mek_key_by_user_password
        chacha = ChaCha20Poly1305(key)

        decrypt_mek = chacha.decrypt(nonce, data, aad)
        print(decrypt_mek)
