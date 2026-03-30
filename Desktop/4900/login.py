import sys
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox, QLineEdit
from Ui_login import Ui_Form


class LoginWindow(QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Login")
        self.lineEdit_2.setEchoMode(QLineEdit.Password)
        self.pushButton.clicked.connect(self.loginFuc)

    def loginFuc(self):
        u = self.lineEdit.text()
        p = self.lineEdit_2.text()
        if u == "admin" and p == "123456":
            self.accept()
        else:
            QMessageBox.warning(self, "Login", "Wrong username or password.")


if __name__ == "__main__":
    from MainWindow import MainWindow

    app = QApplication(sys.argv)
    dlg = LoginWindow()
    if dlg.exec() == QDialog.Accepted:
        win = MainWindow()
        win.show()
        sys.exit(app.exec())
