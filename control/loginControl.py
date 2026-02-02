from model import loginAccount
import tkinter.messagebox as msgbox

def login(username ,password):
    loginOutput = loginAccount.check_data(username,password, "./data/userData.db")
    if loginOutput != 0:
        msgbox.showinfo("Info", "Benar login")
        print(loginOutput)
        return True
    else:
        msgbox.showerror("Info", "Salah login")
