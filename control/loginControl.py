from model import loginAccount
import tkinter.messagebox as msgbox

def login(username ,password):
    login = loginAccount.login(username,password, "./data/userData.db")
    login.check_data()

    loginOutput, data = login.returnVar()
    if loginOutput != 0:
        msgbox.showinfo("Info", "Benar login")
        print("data : " ,data)
        return True, data
    else:
        msgbox.showerror("Info", "Salah login")
        return False, None
