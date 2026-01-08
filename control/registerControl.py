import model.registerAccount as regis
import os

def registerThis(username,password):
    dataPath = "data/userData.db"
    if os.path.exists(dataPath):
        regisAccount = regis.Register(username, password)
        regisAccount.generate_salt()
        regisAccount.create_login_password_verifier()
        regisAccount.create_mek_key_user_password()
        regisAccount.encrypt_mek_key()
        regisAccount.connect_database(dataPath)
        regisAccount.register_data()
        regisAccount.close_database()
    else:
        regis.create_database(dataPath)
        registerThis(username,password)
    


