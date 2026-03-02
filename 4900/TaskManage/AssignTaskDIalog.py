from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QTableWidgetItem
)
from PySide6.QtCore import Qt

class AssignTaskDialog(QDialog):
    def __init__(self, tableTask, tableMember):
        super().__init__()
        self.setWindowTitle("Assign Task")
        self.resize(500, 400)

        self.tableTask = tableTask
        self.tableMember = tableMember
        self.tasks = None         
        self.selected_task_index = None

        layout = QVBoxLayout()

        # task selection
        layout.addWidget(QLabel("Select Task:"))
        self.taskSearch = QLineEdit()
        self.taskSearch.setPlaceholderText("Search tasks...")
        self.taskSearch.textChanged.connect(self.filter_tasks)
        layout.addWidget(self.taskSearch)

        self.taskList = QListWidget()
        self.taskList.setSelectionMode(QListWidget.SingleSelection)
        self.taskList.itemSelectionChanged.connect(self.load_assigned_members)
        layout.addWidget(self.taskList)

        # member selection
        layout.addWidget(QLabel("Select Members:"))
        self.memberSearch = QLineEdit()
        self.memberSearch.setPlaceholderText("Search members...")
        self.memberSearch.textChanged.connect(self.filter_members)
        layout.addWidget(self.memberSearch)

        self.memberList = QListWidget()
        self.memberList.setSelectionMode(QListWidget.MultiSelection)  # 多选
        layout.addWidget(self.memberList)

        # buttons
        btnLayout = QHBoxLayout()
        self.btnAssign = QPushButton("Assign")
        self.btnCancel = QPushButton("Cancel")
        self.btnAssign.clicked.connect(self.assign_task_to_selected)
        self.btnCancel.clicked.connect(self.reject)
        btnLayout.addWidget(self.btnAssign)
        btnLayout.addWidget(self.btnCancel)
        layout.addLayout(btnLayout)

        self.setLayout(layout)

        self.refresh_task_list()
        self.refresh_member_list()

   
    def refresh_task_list(self):
        self.taskList.clear()
        if self.tasks is None:
            return
        for index, task in enumerate(self.tasks):
            item = QListWidgetItem(task["title"])
            item.setData(Qt.UserRole, index)
            self.taskList.addItem(item)

    
    def refresh_member_list(self):
        self.memberList.clear()
        for row in range(self.tableMember.rowCount()):
            member_name = self.tableMember.item(row, 0).text()
            self.memberList.addItem(QListWidgetItem(member_name))

    # search tasks
    def filter_tasks(self):
        keyword = self.taskSearch.text().lower()
        for i in range(self.taskList.count()):
            item = self.taskList.item(i)
            item.setHidden(keyword not in item.text().lower())

    # search members
    def filter_members(self):
        keyword = self.memberSearch.text().lower()
        for i in range(self.memberList.count()):
            item = self.memberList.item(i)
            item.setHidden(keyword not in item.text().lower())

    # click a task to load its assigned members
    def load_assigned_members(self):
        selected_items = self.taskList.selectedItems()
        if not selected_items or self.tasks is None:
            self.selected_task_index = None
            return

        self.selected_task_index = selected_items[0].data(Qt.UserRole)
        assigned_str = self.tasks[self.selected_task_index].get("assigned_member", "")
        assigned_members = [m.strip() for m in assigned_str.split(",") if m.strip()]

       
        for i in range(self.memberList.count()):
            item = self.memberList.item(i)
            item.setSelected(item.text() in assigned_members)

    # click Assign to save the assigned members to the selected task
    def assign_task_to_selected(self):
        if self.selected_task_index is None:
            return

        
        selected_members = [
            self.memberList.item(i).text()
            for i in range(self.memberList.count())
            if self.memberList.item(i).isSelected()
        ]
        assigned_str = ", ".join(selected_members)

        
        self.tasks[self.selected_task_index]["assigned_member"] = assigned_str

        
        self.tableTask.setItem(
            self.selected_task_index, 2, QTableWidgetItem(assigned_str)
        )

        self.accept()