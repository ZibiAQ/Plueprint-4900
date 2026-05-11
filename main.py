import sys
from PySide6.QtWidgets import QApplication, QDialog

from app.login import LoginWindow
from app.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = LoginWindow()
    if dlg.exec() == QDialog.Accepted:
        win = MainWindow(username=dlg.username or "admin")
        win.show()
        sys.exit(app.exec())
