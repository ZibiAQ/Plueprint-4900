from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)


class NewTaskDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Task")
        self.resize(400, 320)

        layout = QVBoxLayout()

        formLayout = QFormLayout()

        self.editTaskName = QLineEdit()
        self.editDetail = QTextEdit()
        self.editStatus = QComboBox()
        self.editStatus.addItems(["Not Started", "In Progress", "Completed"])

        formLayout.addRow("Task Name:", self.editTaskName)
        formLayout.addRow("Detail:", self.editDetail)
        formLayout.addRow("Status:", self.editStatus)

        layout.addLayout(formLayout)

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
            self.editDetail.toPlainText(),
            self.editStatus.currentText(),
        )

