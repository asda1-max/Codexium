import sqlite3
import uuid
from argon2 import PasswordHasher, hash_password_raw
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

class login():
        #class initialization
        def __init__(self,username,password,database_name):
                """_summary_

                Args:
                    username (_type_): _description_
                    password (_type_): _description_
                    database_name (_type_): _description_
                """
                self.username = username
                self.password = password
                self.database_name = database_name
                self.return_con = 9
                self.data = None

        #check data user apakah sudah sama dengan yang di database 
        #contoh : check_data("username1", "password1","database_name1") 
        #return : int 
        def check_data(self):
                
                connection = sqlite3.connect(self.database_name)
                self.current = connection.cursor()

                try:
                        query = self.current.execute("SELECT pw_verifier from user_data where username = ?", (self.username,))
                        self.pw_verifier = query.fetchone()[0]
                except Exception as e:
                        print("error with id : 404", e)
                        self.return_con = 404    
                        self.returnVar()   
                try:
                        PasswordHasher().verify(self.pw_verifier, self.password)
                        print("Password verified successfully")
                except Exception as e:
                        print("Invalid password")
                        self.return_con = 0
                        self.returnVar()

                connection.close()
                self.fetch_info()

                
        #fetch info, fetch data yang dibutuhkan untuk mendeskripsikan MEK key
        #return : int(debug) / byte(data) | NONE jika data invalid
        def fetch_info(self):
                connection = sqlite3.connect(self.database_name)
                self.current = connection.cursor()
                print("fetch info")
                try:
                        query = self.current.execute("SELECT mek_salt from user_data where username = ?", (self.username,))
                        self.salt_MEK = query.fetchone()[0]
                        query = self.current.execute("SELECT encrypted_mek_key from user_data where username = ?", (self.username,))
                        self.encrypted_mek = query.fetchone()[0]
                        query = self.current.execute("SELECT uuid from user_data where username = ?", (self.username,))
                        self.userid = query.fetchone()[0]
                        query = self.current.execute("SELECT nonce from user_data where username = ?", (self.username,))
                        self.nonce = query.fetchone()[0]

                except Exception as e:
                        print("error : ", e)
                        self.return_con = 404
                        self.returnVar()

                connection.close()         
                self.return_con = 1
                self.decrypt_mek()

        #decrypt mek key
        #return : byte(data)
        def decrypt_mek(self):
                print("decrypt")
                mek_key_by_user_password = hash_password_raw(
                password= self.password.encode(),
                salt= self.salt_MEK,
                time_cost=3,
                memory_cost= 77777,
                hash_len=32,
                )

                data = self.encrypted_mek
                aad = uuid.UUID(self.userid).bytes
                key = mek_key_by_user_password
                chacha = ChaCha20Poly1305(key)

                decrypt_mek = chacha.decrypt(self.nonce, data, aad)
                print("decrypted data : ", decrypt_mek)
                self.data = decrypt_mek
                self.return_con = 1

        def returnVar(self):
                print("returnvar")
                if self.data == None :
                        self.data = "NO FETCHED DATA"
                print(self.return_con, self.data)
                return self.return_con, self.data
