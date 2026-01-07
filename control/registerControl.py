import model.registerAccount as regis

def registerThis(username,password):
    regisAccount = regis.Register(username, password)
    regisAccount.generate_salt()
    regisAccount.create_login_password_verifier()
    regisAccount.create_mek_key_user_password()
    regisAccount.encrypt_mek_key()
    regisAccount.create_database()
    regisAccount.register_data()
    regisAccount.view_data()
    regisAccount.close_database()

