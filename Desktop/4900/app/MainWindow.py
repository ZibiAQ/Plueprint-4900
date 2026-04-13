import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel , QInputDialog , QTableWidgetItem, QAbstractItemView, QTableWidget, QLineEdit
from PySide6.QtCore import Qt, QEvent, QTimer
import MemeberManage.SearchMemberDialog as SearchMemberDialog
from TaskManage.EditTaskDialog import EditTaskDialog
from ui.Ui_mainWindow import Ui_MainWindow
from MemeberManage.DeleteMemberDialog import DeleteMemberDialog
from MemeberManage.EditMemberDialog import EditMemberDialog
from MemeberManage.SearchMemberDialog import SearchMemberDialog
from MemeberManage.AddMemeberDialog import AddMemberDialog
from TaskManage.NewTaskDialog import NewTaskDialog
from TaskManage.DeleteTaskDialog import DeleteTaskDialog
from TaskManage.AssignTaskDIalog import AssignTaskDialog
from TaskManage.SearchTaskDialog import SearchTaskDialog
from .FloatingPill import FloatingPill
import json
import os






class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.members = []
        self.tasks = []
        

        # menu -> stacked pages
        self.actionMember.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.actionTask.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.actionTracker.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        
        self.actionHomePage.triggered.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.tableMember.verticalHeader().setVisible(False)

      

        # member page buttons
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

        # task page buttons
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
        self.setup_home_page()
        self.refresh_home_page()

        self.floatingPill = FloatingPill(self)

    def changeEvent(self, event):
        if event.type() == QEvent.Type.WindowStateChange:
            if self.windowState() & Qt.WindowState.WindowMinimized:
                QTimer.singleShot(0, self.minimize_to_floating)
        super().changeEvent(event)

    def minimize_to_floating(self):
        self.setWindowState(Qt.WindowState.WindowNoState)
        self.hide()
        self.floatingPill.place_default()
        self.floatingPill.show()

    def restore_from_floating(self):
        self.floatingPill.hide()
        self.showNormal()
        self.show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event):
        self.floatingPill.close()
        QApplication.quit()
        event.accept()

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
            self.refresh_home_page()

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
            self.refresh_home_page()


    def edit_member(self):
        dialog = EditMemberDialog(self.tableMember)
        dialog.members = self.members
        dialog.refresh_member_list()

        if dialog.exec():
            self.save_data()
            self.refresh_member_table()
            self.refresh_home_page()

    def search_member(self):
     dialog = SearchMemberDialog(self.tableMember)
     dialog.exec()





    def new_task(self):

        dialog = NewTaskDialog()

        if dialog.exec():
            taskName, detail, status = dialog.getData()

            if not taskName:
                return

        
            new_task = {
                "title": taskName,
                "detail": detail,
                "assigned_members": [],
                "status": status or "Not Started"
            }

            self.tasks.append(new_task)

          
            self.save_data()

            
            self.refresh_task_table()
            self.refresh_home_page()


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
                self.refresh_home_page()

    def edit_task(self):
        dialog = EditTaskDialog(self.tasks)

        if dialog.exec():
            self.save_data()
            self.refresh_task_table()
            self.refresh_home_page()


    def assign_task(self):
        dialog = AssignTaskDialog(self.tableTask, self.tableMember)
        dialog.tasks = self.tasks      
        dialog.refresh_task_list()     
        dialog.refresh_member_list()    
        if dialog.exec():
            self.save_data()
            self.refresh_task_table()
            self.refresh_home_page()
           
    def search_task(self):
     dialog = SearchTaskDialog(self.tableTask)
     dialog.exec()

    def setup_home_page(self):
        # dashboard buttons
        self.btnGoMember.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.btnGoTask.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btnQuickNewTask.clicked.connect(self.btnNewTask.click)
        self.btnQuickAddMember.clicked.connect(self.btnAddMember.click)

        self.tableRecentTasks.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableRecentTasks.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableRecentTasks.verticalHeader().setVisible(False)
        self.tableRecentTasks.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tableRecentTasks.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def refresh_home_page(self):
        total_members = len(self.members)
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for t in self.tasks if t.get("status") == "Completed")
        in_progress_tasks = sum(1 for t in self.tasks if t.get("status") == "In Progress")
        not_started_tasks = sum(1 for t in self.tasks if t.get("status") == "Not Started")

        self.labelTotalMembers.setText(str(total_members))
        self.labelTotalTasks.setText(str(total_tasks))
        self.labelCompletedTasks.setText(str(completed_tasks))

        if total_tasks == 0:
            self.progressTasks.setValue(0)
        else:
            self.progressTasks.setValue(int(completed_tasks * 100 / total_tasks))

        self.labelProgressText.setText(
            "Not Started: %s   In Progress: %s   Completed: %s (Total: %s)"
            % (not_started_tasks, in_progress_tasks, completed_tasks, total_tasks)
        )

        # in progress tasks only, last 5
        doing = [t for t in self.tasks if t.get("status") == "In Progress"]
        recent = doing[-5:]
        self.tableRecentTasks.setColumnCount(3)
        self.tableRecentTasks.setHorizontalHeaderLabels(["Title", "Assigned To", "Status"])
        self.tableRecentTasks.setRowCount(len(recent))

        for row, task in enumerate(recent):
            self.tableRecentTasks.setItem(row, 0, QTableWidgetItem(task.get("title", "")))
            self.tableRecentTasks.setItem(row, 1, QTableWidgetItem(task.get("assigned_member", "")))
            self.tableRecentTasks.setItem(row, 2, QTableWidgetItem(task.get("status", "")))

        self.tableRecentTasks.resizeColumnsToContents()
    

    




    


    
     

     




        

if __name__ == "__main__":
    from PySide6.QtWidgets import QDialog
    from .login import LoginWindow

    app = QApplication(sys.argv)
    dlg = LoginWindow()
    if dlg.exec() == QDialog.Accepted:
        win = MainWindow()
        win.show()
        sys.exit(app.exec())