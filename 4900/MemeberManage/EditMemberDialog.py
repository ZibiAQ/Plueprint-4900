from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel,
    QListWidget, QListWidgetItem
)
from PySide6.QtCore import Qt


class EditMemberDialog(QDialog):
    def __init__(self, tableMember):
        super().__init__()
        self.setWindowTitle("Edit Member")
        self.resize(450, 400)

        self.tableMember = tableMember
        self.members = None
        self.selected_index = None

        layout = QVBoxLayout()

        # member selection
        layout.addWidget(QLabel("Select Member:"))
        self.memberList = QListWidget()
        self.memberList.itemSelectionChanged.connect(self.load_member_data)
        layout.addWidget(self.memberList)

        # edit area
        layout.addWidget(QLabel("Name:"))
        self.nameEdit = QLineEdit()
        layout.addWidget(self.nameEdit)

        layout.addWidget(QLabel("ID:"))
        self.idEdit = QLineEdit()
        layout.addWidget(self.idEdit)

        layout.addWidget(QLabel("Department:"))
        self.departmentEdit = QLineEdit()
        layout.addWidget(self.departmentEdit)

        layout.addWidget(QLabel("Role:"))
        self.roleEdit = QLineEdit()
        layout.addWidget(self.roleEdit)

        # buttons
        btnLayout = QHBoxLayout()
        self.btnSave = QPushButton("Save")
        self.btnCancel = QPushButton("Cancel")

        self.btnSave.clicked.connect(self.save_member)
        self.btnCancel.clicked.connect(self.reject)

        btnLayout.addWidget(self.btnSave)
        btnLayout.addWidget(self.btnCancel)
        layout.addLayout(btnLayout)

        self.setLayout(layout)

    #  load members from tableMember to dialog list
    def refresh_member_list(self):
        self.memberList.clear()
        if self.members is None:
            return

        for index, member in enumerate(self.members):
            item = QListWidgetItem(member["name"])
            item.setData(Qt.UserRole, index)
            self.memberList.addItem(item)

   
    def load_member_data(self):
        selected_items = self.memberList.selectedItems()
        if not selected_items:
            self.selected_index = None
            return

        self.selected_index = selected_items[0].data(Qt.UserRole)
        member = self.members[self.selected_index]

        self.nameEdit.setText(member.get("name", ""))
        self.idEdit.setText(member.get("id", ""))
        self.departmentEdit.setText(member.get("department", ""))
        self.roleEdit.setText(member.get("role", ""))

   
    def save_member(self):
        if self.selected_index is None:
            return

        self.members[self.selected_index]["name"] = self.nameEdit.text().strip()
        self.members[self.selected_index]["id"] = self.idEdit.text().strip()
        self.members[self.selected_index]["department"] = self.departmentEdit.text().strip()
        self.members[self.selected_index]["role"] = self.roleEdit.text().strip()

        self.accept()