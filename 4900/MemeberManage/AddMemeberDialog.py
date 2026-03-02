from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QHBoxLayout
)

class AddMemberDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Member")
        self.resize(400, 250)

        layout = QVBoxLayout()

        formLayout = QFormLayout()

        self.editName = QLineEdit()
        self.editID = QLineEdit()
        self.editDept = QLineEdit()
        self.editRole = QLineEdit()

        formLayout.addRow("Name:", self.editName)
        formLayout.addRow("ID:", self.editID)
        formLayout.addRow("Department:", self.editDept)
        formLayout.addRow("Role:", self.editRole)

        layout.addLayout(formLayout)

        # buttons
        buttonLayout = QHBoxLayout()
        self.btnOK = QPushButton("OK")
        self.btnCancel = QPushButton("Cancel")

        self.btnOK.clicked.connect(self.accept)
        self.btnCancel.clicked.connect(self.reject)

        buttonLayout.addWidget(self.btnOK)
        buttonLayout.addWidget(self.btnCancel)

        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def getData(self):
        return (
            self.editName.text(),
            self.editID.text(),
            self.editDept.text(),
            self.editRole.text()
        )
