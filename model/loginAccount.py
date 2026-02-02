import sqlite3
import uuid
from argon2 import PasswordHasher, hash_password_raw
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

#check data user apakah sudah sama dengan yang di database 
#contoh : check_data("username1", "password1","database_name1") 
#return : bool True / False
def check_data(username,password,database_name):
        connection = sqlite3.connect(database_name)
        current = connection.cursor()

        try:
                query = current.execute("SELECT pw_verifier from user_data where username = ?", (username,))
                pw_verifier = query.fetchone()[0]
        except Exception as e:
                print("error with id : 404", e)
                return 0       
        try:
                PasswordHasher().verify(pw_verifier, password)
                print("Password verified successfully")
        except Exception as e:
                print("Invalid password")
                return 0
        
        output_info, data = fetch_info(connection, current, username, password)
        connection.close()

        if output_info == 1:
                print("Info Fetched Successfully")
                return data
        else :
                print("error with id : ", output_info)
                return 0
        
#fetch info, fetch data yang dibutuhkan untuk mendeskripsikan MEK key
#return : int(debug) / byte(data) | NONE jika data invalid
def fetch_info(connection, cur, username, password):
        current = cur
        try:
                query = current.execute("SELECT mek_salt from user_data where username = ?", (username,))
                salt_MEK = query.fetchone()[0]
                query = current.execute("SELECT encrypted_mek_key from user_data where username = ?", (username,))
                encrypted_mek = query.fetchone()[0]
                query = current.execute("SELECT uuid from user_data where username = ?", (username,))
                userid = query.fetchone()[0]
                query = current.execute("SELECT nonce from user_data where username = ?", (username,))
                nonce = query.fetchone()[0]

        except Exception as e:
                print("error : ", e)
                return 404, None
        
        output = decrypt_mek(password, salt_MEK, encrypted_mek, userid, nonce)
        return 1, output

#decrypt mek key
#return : byte(data)
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
        return decrypt_mek
