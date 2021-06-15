# -*- coding: utf-8 -*-
"""
@file task_list_widget.py
@author Y. Kasuga
@date 2021/5/30
@brief Definition of TaskListWidget class
"""

from datetime import time, timedelta
from typing import List
from PyQt5 import QtCore
from PyQt5.QtCore import QTime
from PyQt5.QtWidgets import QTableWidgetItem, QTimeEdit, QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QTableWidget, QComboBox, QLineEdit, QCompleter, QDateTimeEdit
from PyQt5.QtWidgets import QMessageBox

from src.task_log_list import TaskLogList
from src.time_keeper_option import OptionStruct
from src.redmine_entry import RedmineEntry
from src.json_file import JsonFile


class TaskListWidget(QWidget):
    """
    @class TaskList
    @brief Data set to contain the list of tasks and times spent.
    """
    def __init__(self) -> None:
        """
        @fn __init__
        @brief Constructor of TaskList class.
        """
        super().__init__()

        self.task_log_list = TaskLogList()

        # TODO Number of initail task lists
        initial_row = 2

        # Set horizontal header labels
        labels = ["Start Time", "Duration", "Ticket", "Activity", "Comment"]
        self.task_table = QTableWidget(initial_row, len(labels), self)
        self.task_table.setHorizontalHeaderLabels(labels)

        # Set last column to stretch
        self.task_table.horizontalHeader().setStretchLastSection(True)

        # TODO Examples of tickets
        self.tickets = {"Lunch": "-1", "#001 hoge": "001", "#002 moge": "002", "#003 hage": "003"}

        for n in range(initial_row):
            self._setTaskRow(n)

        edit = QLineEdit()
        candidates = ["#001", "#002", "#003", "#101", "#102", "#201"]
        comp = QCompleter(candidates, edit)
        comp.setCompletionMode(QCompleter.PopupCompletion)
        edit.setCompleter(comp)
        self.task_table.setCellWidget(0, 3, edit)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.task_table)
        self.setLayout(self.layout)

        # Debug
        self._setSample()

    def _setTaskRow(self, row:int=0) -> None:
        """
        @fn _setTaskRow
        @brief Generate a new task line in UI.
        """
        # Start Time
        dateTimeEdit = QTimeEdit()
        dateTimeEdit.setDisplayFormat("h:m")
        dateTimeEdit.setFrame(False)
        dateTimeEdit.setTime(QTime.currentTime())
        dateTimeEdit.dateTimeChanged.connect(lambda: self._calculateDuration())
        self.task_table.setCellWidget(row, 0, dateTimeEdit)

        # Ticket
        comboBox = QComboBox()
        comboBox.setEditable(True)
        comboBox.addItems(self.tickets.values())
        comboBox.setFrame(False)
        self.task_table.setCellWidget(row, 2, comboBox)

    def addNewTask(self, num:int=1) -> None:
        """
        @fn addNewTask()
        @brief Add new task line.
        """
        for _ in range(num):
            self.task_table.setRowCount(self.task_table.rowCount() + 1)
            self._setTaskRow(self.task_table.rowCount() - 1)
            self._calculateDuration()

    def removeTask(self, num:int=1) -> None:
        """
        @fn removeTask()
        @brief Remove task line.
        """
        self.task_table.setRowCount(self.task_table.rowCount() - num)
        self._calculateDuration()

    def submit(self, optionStruct:OptionStruct) -> None:
        """
        @fn submit()
        @brief Submit logged time to the tickets.
        @param optionStruct Specify username, password and today's date.
        """
        # TODO need file path
        # self.save()

        # Close the day
        self.task_log_list.close_day(QTime.currentTime())
        tasks_sorted = self.task_log_list.get_tasks_sorted()

        # Confirmation dialog
        diag_confirm = QMessageBox()
        text = "Today's tasks:\n"
        text += self.task_log_list.get_str_tasks_sorted()
        diag_confirm.setText(text)
        diag_confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        if diag_confirm.exec_() == QMessageBox.No:
            return False

        # Submit tasks to redmine
        redmine = RedmineEntry("http://redmine03/", 
            username=optionStruct.username, password=optionStruct.password)
        for task in tasks_sorted:
            redmine.submitTimeEntry(
                optionStruct.today,
                task.ticket_number,
                task.logged_time,
                task.activity_id,
                task.comment
            )

        # Debug
        print("end")

        return True

    def save(self, path_file) -> None:
        """Save tasks
        """
        self._gather_tasks()
        self.task_log_list.sort()

        jsonFile = JsonFile()
        jsonFile.open(path_file, "w")
        task_dict = self.task_log_list.get_task_dict()
        jsonFile.write(task_dict)

        del jsonFile

    def load(self, pathFile: str) -> None:
        """Load tasks

        Args:
            pathFile (str): Path to the file to load
        """
        # TODO Debug
        print(f"Load: {pathFile}")

        jsonFile = JsonFile()
        jsonFile.open(pathFile, "r")
        task_list: dict = jsonFile.read()
        del jsonFile

        self._setTasks(task_list)
        pass

    def _calculateDuration(self) -> None:
        """
        @fn _calculateDuration()
        @brief Calculate duration of each tasks.
        """
        for n in range(self.task_table.rowCount()-1):
            item = QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEditable)

            starttime = self.task_table.cellWidget(n, 0).time()
            endtime = self.task_table.cellWidget(n+1, 0).time()

            duration = timedelta(seconds=starttime.secsTo(endtime))
            item.setText(":".join(str(duration).split(":")[:2]))
            self.task_table.setItem(n, 1, item)

    def _setSample(self) -> None:
        """
        @fn _setSample()
        @brief Set examples of task list for debugging.
        """
        for n in range(self.task_table.rowCount()):
            widget = self.task_table.cellWidget(n, 0)
            widget.setTime(time(9+n, 0, 0))

            widget2 = self.task_table.cellWidget(n, 2)
            widget2.setCurrentIndex(n % 3 + 1)

            item = QTableWidgetItem()
            item.setText(str(n+1) + "th job")
            self.task_table.setItem(n, 4, item)

    def _setTasks(self, task_list: dict) -> None:
        """Set task log list to GUI

        Args:
            task_list (dict): Task list to set
        """
        # Set TaskLogList
        self.task_log_list.set_tasks(task_list)

        # Set GUI
        self.removeTask(self.task_table.rowCount())
        self.addNewTask(len(task_list["task_list"]))

        # Set value to the cells
        for n, task in enumerate(task_list["task_list"]):
            start_time = self.task_table.cellWidget(n, 0)
            start_time.setTime(QTime.fromString(task["start_time"], "HH:mm:ss"))

            ticket_widget = self.task_table.cellWidget(n, 2)
            ticket_widget.setCurrentText(str(task["ticket_id"]))

            activity_id = QTableWidgetItem()
            activity_id.setText(str(task["activity_id"]))
            self.task_table.setItem(n, 3, activity_id)

            comment_widget = QTableWidgetItem()
            comment_widget.setText(task["comment"])
            self.task_table.setItem(n, 4, comment_widget)

    def _gather_tasks(self) -> None:
        """
        @fn _gather_tasks
        @brief Gather all task parameters from task_table and contain into task_log_list.
        @note If comment is empty, put dummy comment.
        """
        num_tasks = self.task_table.rowCount()
        self.task_log_list.clear()

        for n in range(num_tasks):
            # starttime = self.task_table.cellWidget(n, 0).dateTime().toPyDateTime()
            starttime = self.task_table.cellWidget(n, 0).time()
            # TODO : check if ticket number is valid
            ticket_str = self.task_table.cellWidget(n, 2).currentText()
            try:
                ticket = int(ticket_str)
            except ValueError:
                print(f"Invalid ticket number: {ticket_str}")
                ticket = -1

            # If comment is empty, put dummy
            if not self.task_table.item(n, 4):
                comment = "Comment is empty"
            else:
                comment = self.task_table.item(n, 4).text()

            self.task_log_list.append_new(starttime, ticket, comment)
