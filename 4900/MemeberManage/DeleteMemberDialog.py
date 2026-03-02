from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QListWidgetItem,
    QMessageBox
)
from PySide6.QtCore import Qt


class DeleteMemberDialog(QDialog):
    def __init__(self, tableMember):
        super().__init__()
        self.setWindowTitle("Delete Member")
        self.resize(400, 300)

        self.tableMember = tableMember
        self.members = None    
        self.tasks = None      
        self.selected_index = None

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Select Member to Delete:"))

        self.memberList = QListWidget()
        self.memberList.itemSelectionChanged.connect(self.select_member)
        layout.addWidget(self.memberList)

        btnLayout = QHBoxLayout()
        self.btnDelete = QPushButton("Delete")
        self.btnCancel = QPushButton("Cancel")

        self.btnDelete.clicked.connect(self.delete_member)
        self.btnCancel.clicked.connect(self.reject)

        btnLayout.addWidget(self.btnDelete)
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

    #  click a member to select
    def select_member(self):
        selected_items = self.memberList.selectedItems()
        if not selected_items:
            self.selected_index = None
            return

        self.selected_index = selected_items[0].data(Qt.UserRole)

    #  delete the selected member 
    def delete_member(self):
        if self.selected_index is None:
            return

        member_name = self.members[self.selected_index]["name"]

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete '{member_name}'?"
        )

        if confirm != QMessageBox.Yes:
            return

        #  from members list
        del self.members[self.selected_index]

        # from tasks' assigned_member
        if self.tasks is not None:
            for task in self.tasks:
                assigned = task.get("assigned_member", "")
                if assigned:
                    member_list = [m.strip() for m in assigned.split(",")]
                    if member_name in member_list:
                        member_list.remove(member_name)
                        task["assigned_member"] = ", ".join(member_list)

        self.accept()