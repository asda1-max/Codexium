from model import loginAccount
import tkinter.messagebox as msgbox

def login(username ,password):
    if loginAccount.check_data(username,password, "./data/userData.db") == True:
        msgbox.showinfo("Info", "Benar login")
    else:
        msgbox.showerror("Info", "Benar login")
