from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTableWidget, QTableWidgetItem,
    QPushButton
)
from PySide6.QtCore import Qt


class DeleteTaskDialog(QDialog):
    def __init__(self, tasks):
        super().__init__()
        self.setWindowTitle("Delete Task")
        self.resize(500, 400)

        self.tasks = tasks
        self.selected_index = None

        layout = QVBoxLayout()


        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search task...")
        self.searchBar.textChanged.connect(self.filter_tasks)
        layout.addWidget(self.searchBar)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Task Name", "Detail"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)


        buttonLayout = QHBoxLayout()

        self.btnDelete = QPushButton("Delete")
        self.btnCancel = QPushButton("Cancel")

        self.btnDelete.clicked.connect(self.delete_selected)
        self.btnCancel.clicked.connect(self.reject)

        buttonLayout.addWidget(self.btnDelete)
        buttonLayout.addWidget(self.btnCancel)

        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.load_tasks()

    # load tasks to dialog table
    def load_tasks(self):
        self.table.setRowCount(0)

        for index, task in enumerate(self.tasks):
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)

            itemTitle = QTableWidgetItem(task["title"])
            itemDetail = QTableWidgetItem(task["detail"])

          
            itemTitle.setData(Qt.UserRole, index)

            self.table.setItem(rowPosition, 0, itemTitle)
            self.table.setItem(rowPosition, 1, itemDetail)


    #  Delete
    def delete_selected(self):
        selectedRow = self.table.currentRow()

        if selectedRow < 0:
            return

        self.selected_index = self.table.item(selectedRow, 0).data(Qt.UserRole)

        
        self.accept()


    # return the index of the task to delete
    def get_selected_index(self):
        return self.selected_index

    
    # search filter
    def filter_tasks(self):
        keyword = self.searchBar.text().lower()

        for row in range(self.table.rowCount()):
            taskName = self.table.item(row, 0).text().lower()

            if keyword in taskName:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)