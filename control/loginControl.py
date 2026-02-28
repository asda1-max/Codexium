from model import loginAccount
from PySide6.QtWidgets import QMessageBox


def login(username: str, password: str) -> tuple[bool, dict | None]:
    """
    Attempt login.  Returns (success, user_data_dict | None).
    user_data_dict keys: 'mek', 'uuid'
    """
    if not username or not password:
        QMessageBox.warning(None, "Input Error", "Username and password cannot be empty.")
        return False, None

    try:
        acc = loginAccount.login(username, password, "./data/userData.db")
        acc.check_data()
        login_code, mek = acc.returnVar()
    except Exception as e:
        QMessageBox.critical(None, "Login Error", f"An error occurred:\n{e}")
        return False, None

    if login_code != 0 and mek != "NO FETCHED DATA":
        QMessageBox.information(None, "Success", "Login successful!")
        return True, {"mek": mek, "uuid": acc.userid}
    else:
        QMessageBox.critical(None, "Login Failed", "Invalid username or password.")
        return False, None
