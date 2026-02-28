import os
import model.registerAccount as regis
from PySide6.QtWidgets import QMessageBox


def check_eligibility(username: str, password: str) -> bool:
    """Validate registration input."""
    if len(username) < 6:
        QMessageBox.warning(None, "Username Too Short", "Username must be at least 6 characters.")
        return False
    if len(password) < 8:
        QMessageBox.warning(None, "Password Too Short", "Password must be at least 8 characters.")
        return False
    return True


def registerThis(username: str, password: str) -> bool:
    """
    Register a new account.  Returns True on success.
    """
    dataPath = "data/userData.db"

    if not check_eligibility(username, password):
        return False

    # Create database file + table if it doesn't exist yet
    if not os.path.exists(dataPath):
        os.makedirs(os.path.dirname(dataPath), exist_ok=True)
        regis.create_database(dataPath)

    # Check for duplicate username
    if regis.view_data(username, dataPath) != []:
        QMessageBox.critical(None, "Username Taken", "An account with this username already exists.")
        return False

    try:
        account = regis.Register(username, password)
        account.connect_database(dataPath)
        account.generate_salt()
        account.create_login_password_verifier()
        account.create_mek_key_user_password()
        account.encrypt_mek_key()
        account.register_data()
        account.close_database()
        QMessageBox.information(None, "Success", "Account successfully created!")
        return True
    except Exception as e:
        QMessageBox.critical(None, "Registration Error", f"An error occurred:\n{e}")
        return False
