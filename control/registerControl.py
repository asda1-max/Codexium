import model.registerAccount as regis
import tkinter.messagebox as msgbox

import os

def check_eligibility(username,password):
    if len(username) < 6:
        msgbox.showerror("Username are Too Short !", "Username are Too Short ! ")
        return False
    if len(password) < 8:
        msgbox.showerror("Password are Too Short !", "Password are Too Short !\nMinimum 8 Char ")
        return False
    return True

def registerThis(username,password):
    dataPath = "data/userData.db"
    if check_eligibility(username,password) == True:
        if os.path.exists(dataPath):
            if regis.view_data(username,dataPath) != []:
                msgbox.showerror("Multiple Entries Found !", "Multiple Entries Found\n ")
            else:
                regisAccount = regis.Register(username, password)
                regisAccount.connect_database(dataPath)
                regisAccount.generate_salt()
                regisAccount.create_login_password_verifier()
                regisAccount.create_mek_key_user_password()
                regisAccount.encrypt_mek_key()
                regisAccount.register_data()
                regisAccount.close_database()
                msgbox.showinfo("Success !", "Acount Successfully Created\n ")
        else:
            regis.create_database(dataPath)
            registerThis(username,password)
    


