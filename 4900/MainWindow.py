import sys
from tkinter import dialog
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel , QInputDialog , QTableWidgetItem, QAbstractItemView, QTableWidget, QLineEdit
from PySide6.QtCore import Qt
import MemeberManage.SearchMemberDialog as SearchMemberDialog
from TaskManage.EditTaskDialog import EditTaskDialog
from Ui_mainWindow import Ui_MainWindow
from MemeberManage.DeleteMemberDialog import DeleteMemberDialog
from MemeberManage.EditMemberDialog import EditMemberDialog
from MemeberManage.SearchMemberDialog import SearchMemberDialog
from MemeberManage.AddMemeberDialog import AddMemberDialog
from TaskManage.NewTaskDialog import NewTaskDialog
from TaskManage.DeleteTaskDialog import DeleteTaskDialog
from TaskManage.AssignTaskDIalog import AssignTaskDialog
from TaskManage.SearchTaskDialog import SearchTaskDialog
import json
import os






class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.members = []
        self.tasks = []
        

        # 菜单,页面切换
        self.actionMember.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.actionTask.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.actionTracker.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.tableMember.verticalHeader().setVisible(False)

      

    # member管理页面按钮
        self.btnAddMember.clicked.connect(self.add_member)
        self.btnDeleteMember.clicked.connect(self.delete_member)
        self.btnEditMember.clicked.connect(self.edit_member)
        self.btnSearch.clicked.connect(self.search_member)
        
        self.tableMember.setColumnCount(4)
        self.tableMember.setHorizontalHeaderLabels(["Name", "ID", "Dept", "Role"])

   
        self.tableMember.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableMember.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableMember.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableMember.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.btnNewTask.clicked.connect(self.new_task)
        self.btnAssignTask.clicked.connect(self.assign_task)
        self.btnDeleteTask.clicked.connect(self.delete_task)
        self.btnEditTask.clicked.connect(self.edit_task)
        self.btnSearch_2.clicked.connect(self.search_task)

        self.tableTask.setColumnCount(4)
        self.tableTask.setHorizontalHeaderLabels(["Task Name", "Detail", "Assigned To", "Status"])

        self.tableTask.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableTask.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableTask.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableTask.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.load_data()
        self.refresh_member_table()
        self.refresh_task_table()

        
      
    


    def load_data(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as f:
                data = json.load(f)
                self.members = data.get("members", [])
                self.tasks = data.get("tasks", [])
        else:
            self.members = []
            self.tasks = []

    def save_data(self):
        data = {
            "members": self.members,
            "tasks": self.tasks
        }

        with open("data.json", "w") as f:
            json.dump(data, f, indent=4)



    




        

    def add_member(self):
        dialog = AddMemberDialog()

        if dialog.exec():
            name, id_, dept, role = dialog.getData()

            if not name or not id_ or not dept or not role:
                return

          
            new_member = {
                "name": name,
                "id": id_,
                "department": dept,
                "role": role
            }

            self.members.append(new_member)

            
            self.save_data()

           
            self.refresh_member_table()

    def refresh_member_table(self):
        self.tableMember.setRowCount(len(self.members))

        for row, member in enumerate(self.members):
            self.tableMember.setItem(row, 0, QTableWidgetItem(member["name"]))
            self.tableMember.setItem(row, 1, QTableWidgetItem(member["id"]))
            self.tableMember.setItem(row, 2, QTableWidgetItem(member["department"]))
            self.tableMember.setItem(row, 3, QTableWidgetItem(member["role"]))

        


    def delete_member(self):
        dialog = DeleteMemberDialog(self.tableMember)
        dialog.members = self.members
        dialog.tasks = self.tasks
        dialog.refresh_member_list()

        if dialog.exec():
            self.save_data()
            self.refresh_member_table()
            self.refresh_task_table()   


    def edit_member(self):
        dialog = EditMemberDialog(self.tableMember)
        dialog.members = self.members
        dialog.refresh_member_list()

        if dialog.exec():
            self.save_data()
            self.refresh_member_table()

    def search_member(self):
     dialog = SearchMemberDialog(self.tableMember)
     dialog.exec()





    def new_task(self):

        dialog = NewTaskDialog()

        if dialog.exec():
            taskName, detail = dialog.getData()

            if not taskName:
                return

        
            new_task = {
                "title": taskName,
                "detail": detail,
                "assigned_members": []
            }

            self.tasks.append(new_task)

          
            self.save_data()

            
            self.refresh_task_table()


    def refresh_task_table(self):
        self.tableTask.setRowCount(len(self.tasks))

        for row, task in enumerate(self.tasks):
            self.tableTask.setItem(row, 0, QTableWidgetItem(task["title"]))
            self.tableTask.setItem(row, 1, QTableWidgetItem(task["detail"]))
            self.tableTask.setItem(row, 2, QTableWidgetItem(task.get("assigned_member", "")))
            self.tableTask.setItem(row, 3, QTableWidgetItem(task.get("status", "")))
            

    def delete_task(self):
        dialog = DeleteTaskDialog(self.tasks)
        print(type(self.tasks))

        if dialog.exec():
            index_to_delete = dialog.get_selected_index()

            if index_to_delete is not None:
                del self.tasks[index_to_delete]

                self.save_data()
                self.refresh_task_table()

    def edit_task(self):
        dialog = EditTaskDialog(self.tasks)

        if dialog.exec():
            self.save_data()
            self.refresh_task_table()


    def assign_task(self):
        dialog = AssignTaskDialog(self.tableTask, self.tableMember)
        dialog.tasks = self.tasks      
        dialog.refresh_task_list()     
        dialog.refresh_member_list()    
        if dialog.exec():
            self.save_data()
            self.refresh_task_table()
           
    def search_task(self):
     dialog = SearchTaskDialog(self.tableTask)
     dialog.exec()
    

    




    


    
     

     




        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())