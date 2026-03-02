from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QPushButton
)
from PySide6.QtCore import Qt

class SearchMemberDialog(QDialog):
    def __init__(self, tableMember):
        super().__init__()
        self.setWindowTitle("Search Member")
        self.tableMember = tableMember
        self.resize(500, 400)

        layout = QVBoxLayout()

        # search box
        self.searchBox = QLineEdit()
        self.searchBox.setPlaceholderText("Enter Name to search...")
        self.searchBox.textChanged.connect(self.filter_table)
        layout.addWidget(self.searchBox)

        # search result table
        self.tableSearch = QTableWidget()
        self.tableSearch.setColumnCount(4)
        self.tableSearch.setHorizontalHeaderLabels(["Name", "ID", "Department", "Role"])
        self.tableSearch.verticalHeader().setVisible(False)
        self.tableSearch.setEditTriggers(QTableWidget.NoEditTriggers) 
        self.tableSearch.setSelectionMode(QTableWidget.NoSelection)    
        self.tableSearch.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.tableSearch)

        
        btnClose = QPushButton("Close")
        btnClose.clicked.connect(self.accept)
        layout.addWidget(btnClose)

        self.setLayout(layout)

       
        self.load_all_members()

    def load_all_members(self):
        
        self.tableSearch.setRowCount(0)
        for row in range(self.tableMember.rowCount()):
            self.add_row_to_search(row)

    def add_row_to_search(self, row):
        self.tableSearch.insertRow(self.tableSearch.rowCount())
        for col in range(4):
            item = self.tableMember.item(row, col)
            if item:
                self.tableSearch.setItem(self.tableSearch.rowCount()-1, col, QTableWidgetItem(item.text()))

    def filter_table(self, text):
        
        for row in range(self.tableSearch.rowCount()):
            match = False
            for col in range(self.tableSearch.columnCount()):
                item = self.tableSearch.item(row, col)
                if item and text.lower() in item.text().lower():
                    match = True
                    break
            self.tableSearch.setRowHidden(row, not match)

