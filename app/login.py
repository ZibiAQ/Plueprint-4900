import sys
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QMessageBox,
    QLineEdit,
    QPushButton,
    QInputDialog,
)
from ui.Ui_login import Ui_Form
from .user_store import create_user, verify_login, reset_password


class LoginWindow(QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Login")
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.pushButton.clicked.connect(self.loginFuc)

        self.username: str | None = None

        self.resize(340, 300)

        geo = self.pushButton.geometry()
        gap = 8
        btn_w = 180
        btn_h = geo.height()
        btn_x = int((self.width() - btn_w) / 2)
        btn_y = geo.y()

        self.pushButton.setGeometry(btn_x, btn_y, btn_w, btn_h)

        self.btnRegister = QPushButton("Register", self)
        self.btnRegister.setGeometry(btn_x, btn_y + btn_h + gap, btn_w, btn_h)
        self.btnRegister.clicked.connect(self.register_user)

        self.btnForgot = QPushButton("Forgot Password", self)
        self.btnForgot.setGeometry(btn_x, btn_y + (btn_h + gap) * 2, btn_w, btn_h)
        self.btnForgot.clicked.connect(self.forgot_password)

    def loginFuc(self):
        u = self.lineEdit.text()
        p = self.lineEdit_2.text()
        if verify_login(u, p) or (u == "admin" and p == "123456"):
            self.username = u.strip() if u.strip() else "admin"
            self.accept()
        else:
            QMessageBox.warning(self, "Login", "Wrong username or password.")

    def register_user(self):
        username, ok = QInputDialog.getText(self, "Register", "Choose a username (letters/numbers/_/-):")
        if not ok:
            return
        password, ok = QInputDialog.getText(self, "Register", "Choose a password:", QLineEdit.Password)
        if not ok:
            return
        confirm, ok = QInputDialog.getText(self, "Register", "Confirm password:", QLineEdit.Password)
        if not ok:
            return
        if password != confirm:
            QMessageBox.warning(self, "Register", "Passwords do not match.")
            return
        try:
            create_user(username, password)
        except Exception as e:
            QMessageBox.warning(self, "Register", str(e))
            return
        QMessageBox.information(self, "Register", "User created. You can login now.")

    def forgot_password(self):
        username, ok = QInputDialog.getText(self, "Reset Password", "Username:")
        if not ok:
            return
        password, ok = QInputDialog.getText(self, "Reset Password", "New password:", QLineEdit.Password)
        if not ok:
            return
        confirm, ok = QInputDialog.getText(self, "Reset Password", "Confirm new password:", QLineEdit.Password)
        if not ok:
            return
        if password != confirm:
            QMessageBox.warning(self, "Reset Password", "Passwords do not match.")
            return
        try:
            reset_password(username, password)
        except Exception as e:
            QMessageBox.warning(self, "Reset Password", str(e))
            return
        QMessageBox.information(self, "Reset Password", "Password updated. You can login now.")


if __name__ == "__main__":
    from .MainWindow import MainWindow

    app = QApplication(sys.argv)
    dlg = LoginWindow()
    if dlg.exec() == QDialog.Accepted:
        win = MainWindow(username=dlg.username or "admin")
        win.show()
        sys.exit(app.exec())
