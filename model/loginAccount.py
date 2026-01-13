import sqlite3
from argon2 import PasswordHasher
def check_data(username,password,database_name):
        connection = sqlite3.connect(database_name)
        current = connection.cursor()
        pw_verifier_query = current.execute("SELECT pw_verifier from user_data where username = ?", (username,))
        pw_verifier = pw_verifier_query.fetchone()[0]
        try:
                PasswordHasher().verify(pw_verifier, password)
                print("Password verified successfully")
                return True
        except Exception as e:
                print("Invalid password")
                return False
        connection.close()

check_data("rakhatokan","kontoru69","./data/userData.db")