PluePrint
*********



A lightweight desktop Project Management System built with PySide6.
This application allows users to manage tasks and team members with a clean business-style interface.

* Features
* Member Management
Add new members

Edit member details (Name, ID, Department, Role)

Delete members

Automatic cleanup of assigned tasks when a member is deleted

* Task Management
Add tasks

Edit task title and details

Delete tasks

Assign one or multiple members to tasks

Task status management:

Not Started

In Progress

Completed

* Assignment System
Multi-select members for task assignment

Assigned members are displayed in the main task table

Data automatically updates and persists

* Data Persistence
Data stored locally using JSON

All changes saved through save_data()

Reloaded automatically on startup

## Local multi-user

This app supports multiple users on the same computer (local only):

- On the login screen, click **Register** to create a new user.
- On the login screen, click **Forgot Password** to reset a user's password by username.
- Each user has an independent local data file under `data_users/<username>/data.json`.
- Logging in will automatically load that user's data.

## Datasets (named data sets)

Each user can manage multiple named datasets locally (e.g. `ProjectA`, `ProjectB`).

- Use `Datasets` menu to **New / Rename / Delete / Switch**
- The current dataset name is shown in the window title

## Logout / switch user

In the main window menu, go to `Account` → `Logout / Switch User...` to return to the login screen and login as another user.

## Data import/export

You can import/export all members and tasks with one click:

- **Export**: In the main window menu, go to `Data` → `Export...` and choose a `.json` file path.
- **Export Tasks Only**: `Data` → `Export Tasks Only...` to export only the task table.
- **Import**: In the main window menu, go to `Data` → `Import...` and select a `.json` file.
  - Import will **replace** the current `data.json`
  - Before replacing, the app will automatically create/overwrite `data.backup.json` (last backup only)
- **Import Tasks Only**: `Data` → `Import Tasks Only...` to replace only tasks (members are kept). A backup is still created.



PySide6 (Qt for Python)

JSON (local storage)

## Build a Windows EXE (share to others)

On your machine (Windows), run:

- `powershell -ExecutionPolicy Bypass -File .\build_exe.ps1`

Then send `dist\PluePrint.exe` to others. They can double-click to run (no Python needed).
