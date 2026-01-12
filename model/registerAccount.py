import os
import uuid
import base64
import string
import random
import sqlite3
from argon2 import PasswordHasher
from argon2 import hash_password_raw
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

class Register():
    """
    Regis a new user data
    """
    def __init__(self, username, password):
        """
        Docstring for __init__
        
        :param self: self
        :param username: User's username
        :param password: User's Password
        """
        self.username = username
        self.password = password
        self.userid = uuid.uuid4()
        self.mek = uuid.uuid4().bytes
        

    def generate_salt(self):
        """
        Generating completely random salt
        """
        self.salt_login = base64.urlsafe_b64encode(uuid.uuid4().bytes)
        self.salt_MEK = base64.urlsafe_b64encode(uuid.uuid4().bytes)


    def create_login_password_verifier(self):
        """
        Generating pw_verifier
        """
        self.login_password_verifier = PasswordHasher().hash(password=self.password, salt=self.salt_login)

    def create_mek_key_user_password(self):
        """
        Generating raw mek key
        """
        self.mek_key_by_user_password = hash_password_raw(
            password= self.password.encode(),
            salt=self.salt_MEK,
            time_cost=3,
            memory_cost= 77777,
            hash_len=32,
        )
    
    def encrypt_mek_key(self):
        """
        encrypting mek key
        """
        data = self.mek
        aad = self.userid.bytes
        key = self.mek_key_by_user_password
        chacha = ChaCha20Poly1305(key)
        self.nonce = os.urandom(12)

        self.encrypted_mek_key = chacha.encrypt(self.nonce, data, aad)
    
    def generate_recovery_key(self, length_of_key):
        """
        Docstring for generate_recovery_key
        
        :param self: Description
        :param length_of_key: Description
        """
        allowedWords = string.ascii_lowercase + string.digits + string.ascii_uppercase
        self.recovery_code = ''.join(random.choices(allowedWords, k=length_of_key))
    
    def connect_database(self, database_name):
        self.connection = sqlite3.connect(database_name)
        self.current = self.connection.cursor()
    
    def register_data(self):
        self.current.execute("insert into user_data values (?, ?, ?, ?, ?, ?, ?)", (str(self.userid), self.username, self.salt_login, self.login_password_verifier, self.salt_MEK, self.nonce, self.encrypted_mek_key))
        self.connection.commit()
    
    def close_database(self):
        self.connection.close()

            
def create_database(database_name):
        connection = sqlite3.connect(database_name)
        current = connection.cursor()
        current.execute("create table user_data(" \
        "uuid, " \
        "username, " \
        "login_salt, " \
        "pw_verifier, " \
        "mek_salt,"\
        "nonce," \
        "encrypted_mek_key" \
        ")"
        )
        connection.close()

def view_data(username,database_name):
        connection = sqlite3.connect(database_name)
        current = connection.cursor()
        res = current.execute("SELECT username from user_data where username = ?", (username,))
        result = res.fetchall()
        connection.close()
        return result

