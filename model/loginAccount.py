import sqlite3
def check_data(username,password,database_name):
        connection = sqlite3.connect(database_name)
        current = connection.cursor()
        salt_query= current.execute("SELECT login_salt from user_data where username = ?", (username,))
        salt = salt_query.fetchone()
        pw_verifier_query = current.execute("SELECT pw_verifier from user_data where username = ?", (username,))
        pw_verifier = pw_verifier_query.fetchone()
        print(pw_verifier,salt)
        connection.close()

check_data("suprielek",123,"./model/userData.db")