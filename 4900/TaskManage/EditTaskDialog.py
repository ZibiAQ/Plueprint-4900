from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTableWidget, QTableWidgetItem,
    QPushButton, QFormLayout, QTextEdit, QAbstractItemView
)
from PySide6.QtCore import Qt


class EditTaskDialog(QDialog):
    def __init__(self, tasks):
        super().__init__()
        self.setWindowTitle("Edit Task")
        self.resize(500, 450)

    
        self.tasks = tasks
        self.selected_index = None

        mainLayout = QVBoxLayout()

        # search
        self.searchEdit = QLineEdit()
        self.searchEdit.setPlaceholderText("Search tasks...")
        self.searchEdit.textChanged.connect(self.filter_tasks)
        mainLayout.addWidget(self.searchEdit)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Task Name", "Detail", "Status"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.itemSelectionChanged.connect(self.load_task_info)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        mainLayout.addWidget(self.table)

        # edit area
        formLayout = QFormLayout()
        self.editTaskName = QLineEdit()
        self.editDetail = QTextEdit()
        self.editStatus = QLineEdit()
        formLayout.addRow("Task Name:", self.editTaskName)
        formLayout.addRow("Detail:", self.editDetail)
        formLayout.addRow("Status:", self.editStatus)
        mainLayout.addLayout(formLayout)

        # buttons
        btnLayout = QHBoxLayout()
        self.btnSave = QPushButton("Save")
        self.btnCancel = QPushButton("Cancel")
        self.btnSave.clicked.connect(self.save_task)
        self.btnCancel.clicked.connect(self.reject)
        btnLayout.addWidget(self.btnSave)
        btnLayout.addWidget(self.btnCancel)
        mainLayout.addLayout(btnLayout)

        self.setLayout(mainLayout)

  
        self.load_tasks()


    # load tasks to dialog table
    def load_tasks(self):
        self.table.setRowCount(0)

        for index, task in enumerate(self.tasks):
            rowPos = self.table.rowCount()
            self.table.insertRow(rowPos)

            itemTitle = QTableWidgetItem(task["title"])
            itemDetail = QTableWidgetItem(task["detail"])
            itemStatus = QTableWidgetItem(task.get("status", ""))

            itemTitle.setData(Qt.UserRole, index)

            self.table.setItem(rowPos, 0, itemTitle)
            self.table.setItem(rowPos, 1, itemDetail)
            self.table.setItem(rowPos, 2, itemStatus)


    # search filter
    def filter_tasks(self):
        keyword = self.searchEdit.text().lower()
        for row in range(self.table.rowCount()):
            taskName = self.table.item(row, 0).text().lower()
            self.table.setRowHidden(row, keyword not in taskName)


    
    def load_task_info(self):
        selected = self.table.selectedItems()
        if not selected:
            self.editTaskName.clear()
            self.editDetail.clear()
            self.selected_index = None
            return

        row = selected[0].row()
        self.selected_index = self.table.item(row, 0).data(Qt.UserRole)

        task = self.tasks[self.selected_index]
        self.editTaskName.setText(task["title"])
        self.editDetail.setText(task["detail"])
        self.editStatus.setText(task.get("status", ""))

    # save the edited task info back to tasks list
    def save_task(self):
        if self.selected_index is None:
            return

        newName = self.editTaskName.text().strip()
        newDetail = self.editDetail.toPlainText()
        newStatus = self.editStatus.text().strip()

        if not newName:
            return

        self.tasks[self.selected_index]["title"] = newName
        self.tasks[self.selected_index]["detail"] = newDetail
        self.tasks[self.selected_index]["status"] = newStatus

        self.accept()

    # get the index of the edited task
    def get_edited_index(self):
        return self.selected_index