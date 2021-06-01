# -*- coding: utf-8 -*-
"""
@file task_list_widget.py
@author Y. Kasuga
@date 2021/5/30
@brief Definition of TaskListWidget class
"""

import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QTableWidget, QComboBox, QLineEdit, QCompleter, QDateTimeEdit
from PyQt5.QtWidgets import QMessageBox

from src.task_log_list import TaskLogList
from src.time_keeper_option import OptionStruct
from src.redmine_entry import RedmineEntry


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
        initial_row = 1

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
        dateTimeEdit = QDateTimeEdit()
        dateTimeEdit.setDisplayFormat("h:m")
        dateTimeEdit.setFrame(False)
        dateTimeEdit.setDateTime(datetime.datetime.today())
        dateTimeEdit.dateTimeChanged.connect(self._calculateDuration)
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
        self.task_table.setRowCount(self.task_table.rowCount() + num)
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
        self._gather_tasks()

        # Close the day
        self.task_log_list.close_day(datetime.datetime.today())
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

    def _calculateDuration(self) -> None:
        """
        @fn _calculateDuration()
        @brief Calculate duration of each tasks.
        """
        for n in range(self.task_table.rowCount()-1):
            item = QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsEditable)
            starttime = datetime.datetime.strptime(
                self.task_table.cellWidget(n, 0).text(), "%H:%M"
            )
            endtime = datetime.datetime.strptime(
                self.task_table.cellWidget(n+1, 0).text(), "%H:%M"
            )
            duration = endtime - starttime
            item.setText(":".join(str(duration).split(":")[:2]))
            self.task_table.setItem(n, 1, item)

    def _setSample(self) -> None:
        """
        @fn _setSample()
        @brief Set examples of task list for debugging.
        """
        for n in range(self.task_table.rowCount()):
            today = datetime.datetime.combine(datetime.date.today(), datetime.time(9+n, 0, 0))

            widget = self.task_table.cellWidget(n, 0)
            # widget.setDateTime(datetime.datetime(2021, 2, 1, 9+n, 0, 0))
            widget.setDateTime(today)

            widget2 = self.task_table.cellWidget(n, 2)
            widget2.setCurrentIndex(n % 3 + 1)

            item = QTableWidgetItem()
            # item.setText(str(n) + "th job")
            item.setText("th job")
            self.task_table.setItem(n, 4, item)

    def _gather_tasks(self) -> None:
        """
        @fn _gather_tasks
        @brief Gather all task parameters from task_table and contain into task_log_list.
        @note If comment is empty, put dummy comment.
        """
        num_tasks = self.task_table.rowCount()
        self.task_log_list.clear()

        for n in range(num_tasks):
            starttime = self.task_table.cellWidget(n, 0).dateTime().toPyDateTime()
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