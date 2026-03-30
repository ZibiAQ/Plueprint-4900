import sys
from PySide6.QtWidgets import QApplication, QDialog

from login import LoginWindow
from MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dlg = LoginWindow()
    if dlg.exec() == QDialog.Accepted:
        win = MainWindow()
        win.show()
        sys.exit(app.exec())
