import os
import uuid
import base64
import string
import random
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
        self.generate_salt()
        self.create_login_password_verifier()
        self.create_mek_key_user_password()
        self.encrypt_mek_key()

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
        nonce = os.urandom(12)

        self.encrypted_mek_key = chacha.encrypt(nonce, data, aad)
    
    def generate_recovery_key(self, length_of_key):
        allowedWords = string.ascii_lowercase + string.digits + string.ascii_uppercase
        self.recovery_code = ''.join(random.choices(allowedWords, k=length_of_key))
            
        
        

test = Register(username="Azeroth",password= "Primavera")
print("encrypted mek key = ", test.encrypted_mek_key)
print("user pw verifier = ", test.login_password_verifier)

