# -*- coding: utf-8 -*-
"""
@file main.py
@author Y. Kasuga
@date 2021/5/29
@brief Definition of MyWindow class
"""

from PyQt5.QtWidgets import QMainWindow, QAction, QWidget, qApp
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox, QDialog

from src.task_list_widget import TaskListWidget
from src.time_keeper_option import TimeKeeperOption, OptionStruct


class MyWindow(QMainWindow):
    """
    @class MyWindow
    @brief Main window
    """
    def __init__(self) -> None:
        """
        @fn __init__
        @brief Constructor of MyWindow class.
        """
        super().__init__()
        self.title = "TimeKeeper"
        self.width = 700
        self.height = 400
        self.timeKeeper = TimeKeeperWidget()
        self.initUI()

        self.optionWidget = TimeKeeperOption()
        self.optionStruct = self.optionWidget.getOptionStruct()
        self.timeKeeper.setOptionStruct(self.optionStruct)

    def initUI(self) -> None:
        """
        @fn initUI
        @brief Initialize window, shorcuts, menubar and actions.
        """
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        self.show()

        optionAction = QAction("&Option", self)
        optionAction.setShortcut("Ctrl+O")
        optionAction.setStatusTip("Open Option Dialog")
        optionAction.triggered.connect(lambda: self.openOptionDialog())
        
        exitAction = QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip("Close Window")
        exitAction.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(optionAction)
        fileMenu.addAction(exitAction)

        self.setCentralWidget(self.timeKeeper)

    def openOptionDialog(self) -> None:
        """
        @fn openOptionDialog
        @brief Opens option dialog.
        """
        optionDialog = QDialog()
        optionDialog.setWindowTitle("Option")
        # optionDialog.setWindowModality(Qt.ApplicationModal)

        self.optionWidget.closed.connect(lambda: optionDialog.done(0))

        layout = QVBoxLayout()
        layout.addWidget(self.optionWidget)
        optionDialog.setLayout(layout)
        optionDialog.exec_()

        self.optionStruct = self.optionWidget.getOptionStruct()
        self.timeKeeper.setOptionStruct(self.optionStruct)


class TimeKeeperWidget(QWidget):
    """
    @class TimeKeeper
    @brief Main UI to manage time spent on tasks.
    """
    def __init__(self) -> None:
        """
        @fn __ini__
        @brief Constructor of TimeKeeper class.
        """
        super().__init__()
        self.layout = QVBoxLayout()

        button = QPushButton("Add New Task")
        button.clicked.connect(lambda: self.addNewTaskSet())

        button_remove = QPushButton("Remove Last Task")
        button_remove.clicked.connect(lambda: self.removeTaskSet())

        button_submit = QPushButton("Submit")
        button_submit.setShortcut("Ctrl+S")
        button_submit.clicked.connect(lambda: self._submitTaskList())

        self.task_list = TaskListWidget()
        self.optionStruct = OptionStruct()
        
        self.layout.addWidget(button)
        self.layout.addWidget(button_submit)
        self.layout.addWidget(self.task_list)
        self.layout.addWidget(button_remove)
        self.setLayout(self.layout)

    def addNewTaskSet(self) -> None:
        """
        @fn addNewTaskSet
        @brief Add new task line to the window.
        """
        self.task_list.addNewTask()

    def removeTaskSet(self) -> None:
        """
        @fn removeTaskSet
        @brief Remove task line from the window.
        """
        self.task_list.removeTask()

    def setOptionStruct(self, optionStruct) -> None:
        """
        @fn setOptionStruct
        @brief Assign option parameters.
        """
        self.optionStruct = optionStruct

    def _submitTaskList(self) -> None:
        """
        @fn _submitTaskList
        @brief Submit tasks to the tickets at the end of the day.
        """
        if not self.task_list.submit(self.optionStruct):
            return

        dialog = QMessageBox()
        dialog.setGeometry(500, 500, 200, 150)
        dialog.setText("Submit today's your whole task sets.\nGood job!")
        dialog.exec_()

