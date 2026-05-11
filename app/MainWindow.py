import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QInputDialog,
    QTableWidgetItem,
    QAbstractItemView,
    QTableWidget,
    QLineEdit,
    QFileDialog,
    QMessageBox,
)
from PySide6.QtGui import QAction
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
import shutil
from datetime import datetime
from .dataset_store import (
    create_dataset,
    delete_dataset,
    ensure_user_datasets,
    get_current_dataset_id,
    list_datasets,
    rename_dataset,
    set_current_dataset,
    dataset_data_file,
    dataset_name,
)
from PySide6.QtWidgets import QDialog
from .user_store import reset_password
from .DatasetSwitchDialog import DatasetSwitchDialog






class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, username: str = "admin"):
        super().__init__()
        self.setupUi(self)

        self.members = []
        self.tasks = []

        self.username = username
        ensure_user_datasets(self.username)
        self.dataset_id = get_current_dataset_id(self.username)
        self.dataset_display_name = dataset_name(self.username, self.dataset_id)
        self.data_file = dataset_data_file(self.username, self.dataset_id)
        self._update_window_title()
        

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
        self._setup_data_menu()
        self._setup_datasets_menu()
        self._setup_account_menu()

    def _update_window_title(self):
        self.setWindowTitle(f"PluePrint - {self.username} [{self.dataset_display_name}]")

    def _setup_datasets_menu(self):
        self.menuDatasets = self.menuBar().addMenu("Datasets")

        self.actionSwitchDataset = QAction("Switch...", self)
        self.actionNewDataset = QAction("New...", self)
        self.actionRenameDataset = QAction("Rename...", self)
        self.actionDeleteDataset = QAction("Delete...", self)

        self.actionSwitchDataset.triggered.connect(self.switch_dataset)
        self.actionNewDataset.triggered.connect(self.new_dataset)
        self.actionRenameDataset.triggered.connect(self.rename_current_dataset)
        self.actionDeleteDataset.triggered.connect(self.delete_current_dataset)

        self.menuDatasets.addAction(self.actionSwitchDataset)
        self.menuDatasets.addSeparator()
        self.menuDatasets.addAction(self.actionNewDataset)
        self.menuDatasets.addAction(self.actionRenameDataset)
        self.menuDatasets.addAction(self.actionDeleteDataset)

    def _reload_from_current_dataset(self):
        self.members = []
        self.tasks = []
        self.load_data()
        self.refresh_member_table()
        self.refresh_task_table()
        self.refresh_home_page()

    def switch_dataset(self):
        datasets = list_datasets(self.username)
        names = [d.name for d in datasets]
        current_name = self.dataset_display_name if self.dataset_display_name in names else (names[0] if names else "")

        dlg = DatasetSwitchDialog(names, current_name=current_name)
        if dlg.exec() != QDialog.Accepted:
            return

        choice = dlg.selected_name()
        if not choice:
            return

        selected = next((d for d in datasets if d.name == choice), None)
        if selected is None:
            return
        try:
            set_current_dataset(self.username, selected.dataset_id)
        except Exception as e:
            QMessageBox.warning(self, "Datasets", str(e))
            return
        self.dataset_id = selected.dataset_id
        self.dataset_display_name = selected.name
        self.data_file = dataset_data_file(self.username, self.dataset_id)
        self._update_window_title()
        self._reload_from_current_dataset()

    def new_dataset(self):
        name, ok = QInputDialog.getText(self, "New Dataset", "Dataset name:")
        if not ok:
            return
        try:
            rec = create_dataset(self.username, name)
        except Exception as e:
            QMessageBox.warning(self, "Datasets", str(e))
            return
        self.dataset_id = rec.dataset_id
        self.dataset_display_name = rec.name
        self.data_file = dataset_data_file(self.username, self.dataset_id)
        self._update_window_title()
        self._reload_from_current_dataset()

    def rename_current_dataset(self):
        new_name, ok = QInputDialog.getText(self, "Rename Dataset", "New name:", text=self.dataset_display_name)
        if not ok:
            return
        try:
            rename_dataset(self.username, self.dataset_id, new_name)
        except Exception as e:
            QMessageBox.warning(self, "Datasets", str(e))
            return
        self.dataset_display_name = new_name.strip()
        self._update_window_title()

    def delete_current_dataset(self):
        confirm = QMessageBox.question(
            self,
            "Delete Dataset",
            f"Delete dataset '{self.dataset_display_name}'?\n\nThis will remove its local data file.",
        )
        if confirm != QMessageBox.Yes:
            return
        try:
            delete_dataset(self.username, self.dataset_id)
            self.dataset_id = get_current_dataset_id(self.username)
            self.dataset_display_name = dataset_name(self.username, self.dataset_id)
            self.data_file = dataset_data_file(self.username, self.dataset_id)
        except Exception as e:
            QMessageBox.warning(self, "Datasets", str(e))
            return
        self._update_window_title()
        self._reload_from_current_dataset()

    def _setup_account_menu(self):
        self.menuAccount = self.menuBar().addMenu("Account")

        self.actionLogout = QAction("Logout / Switch User...", self)
        self.actionResetPassword = QAction("Reset Password...", self)

        self.actionLogout.triggered.connect(self.logout_switch_user)
        self.actionResetPassword.triggered.connect(self.reset_password_flow)

        self.menuAccount.addAction(self.actionLogout)
        self.menuAccount.addAction(self.actionResetPassword)

    def logout_switch_user(self):
        from .login import LoginWindow

        dlg = LoginWindow()
        if dlg.exec() != QDialog.Accepted:
            return

        next_user = dlg.username or "admin"
        win = MainWindow(username=next_user)
        win.show()
        self.close()

    def reset_password_flow(self):
        username, ok = QInputDialog.getText(self, "Reset Password", "Username:")
        if not ok:
            return
        password, ok = QInputDialog.getText(self, "Reset Password", "New password:", QLineEdit.Password)
        if not ok:
            return
        confirm, ok = QInputDialog.getText(self, "Reset Password", "Confirm new password:", QLineEdit.Password)
        if not ok:
            return
        if password != confirm:
            QMessageBox.warning(self, "Reset Password", "Passwords do not match.")
            return
        try:
            reset_password(username, password)
        except Exception as e:
            QMessageBox.warning(self, "Reset Password", str(e))
            return
        QMessageBox.information(self, "Reset Password", "Password updated.")

    def _setup_data_menu(self):
        self.menuData = self.menuBar().addMenu("Data")

        self.actionExportData = QAction("Export...", self)
        self.actionExportTasks = QAction("Export Tasks Only...", self)
        self.actionImportData = QAction("Import...", self)
        self.actionImportTasks = QAction("Import Tasks Only...", self)

        self.actionExportData.triggered.connect(self.export_data)
        self.actionExportTasks.triggered.connect(self.export_tasks_only)
        self.actionImportData.triggered.connect(self.import_data)
        self.actionImportTasks.triggered.connect(self.import_tasks_only)

        self.menuData.addAction(self.actionExportData)
        self.menuData.addAction(self.actionExportTasks)
        self.menuData.addSeparator()
        self.menuData.addAction(self.actionImportData)
        self.menuData.addAction(self.actionImportTasks)

    def _make_export_payload(self):
        return {
            "schema_version": 1,
            "exported_at": datetime.now().isoformat(timespec="seconds"),
            "kind": "full",
            "members": self.members,
            "tasks": self.tasks,
        }

    def _make_export_tasks_payload(self):
        return {
            "schema_version": 1,
            "exported_at": datetime.now().isoformat(timespec="seconds"),
            "kind": "tasks_only",
            "tasks": self.tasks,
        }

    def _validate_import_payload(self, payload, mode: str):
        if not isinstance(payload, dict):
            raise ValueError("Import file must be a JSON object.")

        if mode == "full":
            if "members" not in payload or "tasks" not in payload:
                raise ValueError("Import JSON must contain 'members' and 'tasks'.")
            members = payload.get("members")
            tasks = payload.get("tasks")
            if not isinstance(members, list) or not isinstance(tasks, list):
                raise ValueError("'members' and 'tasks' must be lists.")
            return members, tasks

        if mode == "tasks_only":
            # allow importing from either a full export or a tasks-only export
            tasks = payload.get("tasks")
            if tasks is None:
                raise ValueError("Import JSON must contain 'tasks'.")
            if not isinstance(tasks, list):
                raise ValueError("'tasks' must be a list.")
            return None, tasks

        raise ValueError(f"Unknown import mode: {mode}")

    def _backup_data_file(self):
        if not os.path.exists(self.data_file):
            return
        # keep only one "last backup" file
        backup_path = os.path.splitext(self.data_file)[0] + ".backup.json"
        shutil.copy2(self.data_file, backup_path)

    def export_data(self):
        suggested = f"plueprint-export-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Data",
            suggested,
            "JSON Files (*.json);;All Files (*)",
        )
        if not file_path:
            return

        payload = self._make_export_payload()
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Export", "Export completed.")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))

    def export_tasks_only(self):
        suggested = f"plueprint-tasks-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Tasks",
            suggested,
            "JSON Files (*.json);;All Files (*)",
        )
        if not file_path:
            return

        payload = self._make_export_tasks_payload()
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Export", "Export completed.")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))

    def import_data(self):
        self._import_data_common(mode="full")

    def import_tasks_only(self):
        self._import_data_common(mode="tasks_only")

    def _import_data_common(self, mode: str):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Data" if mode == "full" else "Import Tasks",
            "",
            "JSON Files (*.json);;All Files (*)",
        )
        if not file_path:
            return

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
            members, tasks = self._validate_import_payload(payload, mode=mode)
        except Exception as e:
            QMessageBox.critical(self, "Import Failed", f"Invalid import file.\n\n{e}")
            return

        confirm_text = (
            "Import will replace current data.\n\nContinue?"
            if mode == "full"
            else "Import will replace current TASKS only.\nMembers will be kept.\n\nContinue?"
        )
        confirm = QMessageBox.question(
            self,
            "Confirm Import",
            confirm_text,
        )
        if confirm != QMessageBox.Yes:
            return

        # backup existing data.json if present
        try:
            self._backup_data_file()
        except Exception as e:
            QMessageBox.critical(self, "Import Failed", f"Backup failed.\n\n{e}")
            return

        if mode == "full":
            self.members = members or []
            self.tasks = tasks or []
        else:
            self.tasks = tasks or []

        try:
            self.save_data()
            if mode == "full":
                self.refresh_member_table()
            self.refresh_task_table()
            self.refresh_home_page()
            QMessageBox.information(self, "Import", "Import completed.")
        except Exception as e:
            QMessageBox.critical(self, "Import Failed", str(e))

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
        # Don't force-quit the entire app here.
        # This allows "Logout / Switch User..." to close the current window
        # while keeping the application running with a new window.
        event.accept()

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
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

        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)



    




        

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