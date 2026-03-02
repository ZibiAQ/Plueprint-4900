# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStackedWidget, QStatusBar, QTableWidget, QTableWidgetItem,
    QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet(u"")
        self.actionTask_Management = QAction(MainWindow)
        self.actionTask_Management.setObjectName(u"actionTask_Management")
        self.actionRemove_members = QAction(MainWindow)
        self.actionRemove_members.setObjectName(u"actionRemove_members")
        self.actionRemove_members.setEnabled(True)
        self.actionMember_list = QAction(MainWindow)
        self.actionMember_list.setObjectName(u"actionMember_list")
        self.actionMember_list.setEnabled(True)
        self.actionCreate_a_new_task = QAction(MainWindow)
        self.actionCreate_a_new_task.setObjectName(u"actionCreate_a_new_task")
        self.actionCreate_a_new_task.setEnabled(True)
        self.actionAssign_a_task = QAction(MainWindow)
        self.actionAssign_a_task.setObjectName(u"actionAssign_a_task")
        self.actionAssign_a_task.setEnabled(True)
        self.actionTask_list = QAction(MainWindow)
        self.actionTask_list.setObjectName(u"actionTask_list")
        self.actionTask_list.setEnabled(True)
        self.actionCreate_a_new_project = QAction(MainWindow)
        self.actionCreate_a_new_project.setObjectName(u"actionCreate_a_new_project")
        self.actionOpen_a_project = QAction(MainWindow)
        self.actionOpen_a_project.setObjectName(u"actionOpen_a_project")
        self.actionProject_settings = QAction(MainWindow)
        self.actionProject_settings.setObjectName(u"actionProject_settings")
        self.actionAdd_members = QAction(MainWindow)
        self.actionAdd_members.setObjectName(u"actionAdd_members")
        self.actionAdd_members.setEnabled(True)
        self.actionHomePage = QAction(MainWindow)
        self.actionHomePage.setObjectName(u"actionHomePage")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(30, 80, 721, 361))
        self.pageMember = QWidget()
        self.pageMember.setObjectName(u"pageMember")
        self.btnAddMember = QPushButton(self.pageMember)
        self.btnAddMember.setObjectName(u"btnAddMember")
        self.btnAddMember.setGeometry(QRect(20, 30, 151, 26))
        self.btnDeleteMember = QPushButton(self.pageMember)
        self.btnDeleteMember.setObjectName(u"btnDeleteMember")
        self.btnDeleteMember.setGeometry(QRect(20, 70, 151, 26))
        self.btnEditMember = QPushButton(self.pageMember)
        self.btnEditMember.setObjectName(u"btnEditMember")
        self.btnEditMember.setGeometry(QRect(20, 110, 151, 26))
        self.tableMember = QTableWidget(self.pageMember)
        self.tableMember.setObjectName(u"tableMember")
        self.tableMember.setGeometry(QRect(180, 30, 511, 261))
        self.btnSearch = QPushButton(self.pageMember)
        self.btnSearch.setObjectName(u"btnSearch")
        self.btnSearch.setGeometry(QRect(180, 0, 81, 26))
        self.stackedWidget.addWidget(self.pageMember)
        self.pageTask = QWidget()
        self.pageTask.setObjectName(u"pageTask")
        self.btnNewTask = QPushButton(self.pageTask)
        self.btnNewTask.setObjectName(u"btnNewTask")
        self.btnNewTask.setGeometry(QRect(20, 30, 141, 26))
        self.btnDeleteTask = QPushButton(self.pageTask)
        self.btnDeleteTask.setObjectName(u"btnDeleteTask")
        self.btnDeleteTask.setGeometry(QRect(20, 70, 141, 26))
        self.btnAssignTask = QPushButton(self.pageTask)
        self.btnAssignTask.setObjectName(u"btnAssignTask")
        self.btnAssignTask.setGeometry(QRect(20, 110, 141, 26))
        self.tableTask = QTableWidget(self.pageTask)
        self.tableTask.setObjectName(u"tableTask")
        self.tableTask.setGeometry(QRect(170, 30, 511, 261))
        self.btnSearch_2 = QPushButton(self.pageTask)
        self.btnSearch_2.setObjectName(u"btnSearch_2")
        self.btnSearch_2.setGeometry(QRect(170, 0, 81, 26))
        self.btnEditTask = QPushButton(self.pageTask)
        self.btnEditTask.setObjectName(u"btnEditTask")
        self.btnEditTask.setGeometry(QRect(20, 150, 141, 26))
        self.stackedWidget.addWidget(self.pageTask)
        self.pageProject = QWidget()
        self.pageProject.setObjectName(u"pageProject")
        self.stackedWidget.addWidget(self.pageProject)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 0, 81, 81))
        self.label.setPixmap(QPixmap(u":/images/75size.png"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.actionMember = QMenu(self.menubar)
        self.actionMember.setObjectName(u"actionMember")
        self.actionTask = QMenu(self.menubar)
        self.actionTask.setObjectName(u"actionTask")
        self.actionTracker = QMenu(self.menubar)
        self.actionTracker.setObjectName(u"actionTracker")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.actionMember.menuAction())
        self.menubar.addAction(self.actionTask.menuAction())
        self.menubar.addAction(self.actionTracker.menuAction())
        self.actionMember.addAction(self.actionAdd_members)
        self.actionTask.addAction(self.actionCreate_a_new_task)
        self.actionTracker.addAction(self.actionHomePage)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Company/Team Management System", None))
        self.actionTask_Management.setText(QCoreApplication.translate("MainWindow", u"Add members", None))
        self.actionRemove_members.setText(QCoreApplication.translate("MainWindow", u"Remove members", None))
        self.actionMember_list.setText(QCoreApplication.translate("MainWindow", u"Member list", None))
        self.actionCreate_a_new_task.setText(QCoreApplication.translate("MainWindow", u"HomePage", None))
        self.actionAssign_a_task.setText(QCoreApplication.translate("MainWindow", u"Assign a task", None))
        self.actionTask_list.setText(QCoreApplication.translate("MainWindow", u"Task list", None))
        self.actionCreate_a_new_project.setText(QCoreApplication.translate("MainWindow", u"Create a new project", None))
        self.actionOpen_a_project.setText(QCoreApplication.translate("MainWindow", u"Open a project", None))
        self.actionProject_settings.setText(QCoreApplication.translate("MainWindow", u"Project settings", None))
        self.actionAdd_members.setText(QCoreApplication.translate("MainWindow", u"HomePage", None))
        self.actionHomePage.setText(QCoreApplication.translate("MainWindow", u"HomePage", None))
        self.btnAddMember.setText(QCoreApplication.translate("MainWindow", u"Add Member", None))
        self.btnDeleteMember.setText(QCoreApplication.translate("MainWindow", u"Delete Member", None))
        self.btnEditMember.setText(QCoreApplication.translate("MainWindow", u"Edit Member", None))
        self.btnSearch.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.btnNewTask.setText(QCoreApplication.translate("MainWindow", u"New Task", None))
        self.btnDeleteTask.setText(QCoreApplication.translate("MainWindow", u"Delete Task", None))
        self.btnAssignTask.setText(QCoreApplication.translate("MainWindow", u"Assign Task", None))
        self.btnSearch_2.setText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.btnEditTask.setText(QCoreApplication.translate("MainWindow", u"Edit Task", None))
        self.label.setText("")
        self.actionMember.setTitle(QCoreApplication.translate("MainWindow", u"Member Management", None))
        self.actionTask.setTitle(QCoreApplication.translate("MainWindow", u"Task Management", None))
        self.actionTracker.setTitle(QCoreApplication.translate("MainWindow", u"Tracker", None))
    # retranslateUi

