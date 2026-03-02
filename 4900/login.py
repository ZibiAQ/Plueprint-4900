from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QLabel ,QWidget
from Ui_login import Ui_Form

class Mywindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.pushButton.clicked.connect(self.loginFuc)
    

    def loginFuc(self):
        account = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if account == "admin" and password == "123456":
            print("login success")
        else:
            print("login failed")


#further development




if __name__ == "__main__":
    app = QApplication([])
    window = Mywindow()
    window.show()
    app.exec()