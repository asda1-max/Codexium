from argon2 import PasswordHasher
from argon2 import hash_password_raw
import random
import base64
import uuid

import os

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305




userID = uuid.uuid4().bytes
mek = uuid.uuid4().bytes
usernameuser = "Azeroth"
passworduser = "Primavera"
saltUser = base64.urlsafe_b64encode(uuid.uuid4().bytes)
saltMekKey = base64.urlsafe_b64encode(uuid.uuid4().bytes)
print(saltUser)

hashedUserKey = PasswordHasher().hash(password=passworduser, salt=saltUser)
hashedMekKey = hash_password_raw(
    password= passworduser.encode(),
    salt=saltMekKey,
    time_cost=3,
    memory_cost= 77777,
    hash_len=32,
)


data = mek
aad = userID
key = hashedMekKey
chacha = ChaCha20Poly1305(key)
nonce = os.urandom(12)

ct = chacha.encrypt(nonce, data, aad)
chacha.decrypt(nonce, ct, aad)

print("Encrypted : ",ct, "\ndecrypted : " , chacha.decrypt(nonce, ct, aad))
