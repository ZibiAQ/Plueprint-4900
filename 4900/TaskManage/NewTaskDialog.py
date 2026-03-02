from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QTextEdit,
    QPushButton, QHBoxLayout
)

class NewTaskDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Task")
        self.resize(400, 300)

        layout = QVBoxLayout()

        formLayout = QFormLayout()

        self.editTaskName = QLineEdit()
        self.editDetail = QTextEdit()

        formLayout.addRow("Task Name:", self.editTaskName)
        formLayout.addRow("Detail:", self.editDetail)

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
            self.editTaskName.text(),
            self.editDetail.toPlainText()
        )
