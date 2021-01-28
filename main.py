import sys
import datetime

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QLayout, QMainWindow, QAction, QTableWidgetItem, QWidget, qApp
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton, QTableWidget, QComboBox, QLineEdit, QCompleter, QDateTimeEdit
from PyQt5.QtWidgets import QMessageBox, QDialog

from task_log_list import TaskLogList
from time_keeper_option import TimeKeeperOption, OptionStruct
from redmine_entry import RedmineEntry


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "TimeKeeper"
        self.width = 700
        self.height = 400
        self.timeKeeper = TimeKeeper()
        self.initUI()

        self.optionWidget = TimeKeeperOption()
        self.optionStruct = self.optionWidget.getOptionStruct()
        self.timeKeeper.setOptionStruct(self.optionStruct)

    def initUI(self):
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

    def openOptionDialog(self):
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


class TimeKeeper(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        button = QPushButton("Add New Task")
        button.clicked.connect(lambda: self.addNewTaskSet())

        button_remove = QPushButton("Remove Last Task")
        button_remove.clicked.connect(lambda: self.removeTaskSet())

        button_submit = QPushButton("Submit")
        button_submit.setShortcut("Ctrl+S")
        button_submit.clicked.connect(lambda: self._submitTaskList())

        self.task_list = TaskList()
        self.optionStruct = OptionStruct()
        
        self.layout.addWidget(button)
        self.layout.addWidget(button_submit)
        self.layout.addWidget(self.task_list)
        self.layout.addWidget(button_remove)
        self.setLayout(self.layout)

    def addNewTaskSet(self):
        self.task_list.addNewTask()

    def removeTaskSet(self):
        self.task_list.removeTask()

    def setOptionStruct(self, optionStruct):
        self.optionStruct = optionStruct

    def _submitTaskList(self):
        self.task_list.submit(self.optionStruct)

        dialog = QMessageBox()
        dialog.setGeometry(500, 500, 200, 150)
        dialog.setText("Submit today's your whole task sets.\nGood job!")
        dialog.exec_()


class TaskList(QWidget):
    def __init__(self):
        super().__init__()

        self.task_log_list = TaskLogList()

        initial_row = 2
        labels = ["Start Time", "Duration", "Ticket", "Activity", "Comment"]
        self.task_table = QTableWidget(initial_row, len(labels), self)
        self.task_table.setHorizontalHeaderLabels(labels)

        # self.tickets = ["Lunch", "#001 hoge", "#002 moge", "#003 hage"]
        self.tickets = ["Lunch", "001", "002", "003"]

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

    def _setTaskRow(self, row=0):
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
        comboBox.addItems(self.tickets)
        comboBox.setFrame(False)
        self.task_table.setCellWidget(row, 2, comboBox)

    def addNewTask(self, num=1):
        self.task_table.setRowCount(self.task_table.rowCount() + num)
        self._setTaskRow(self.task_table.rowCount() - 1)
        self._calculateDuration()

    def removeTask(self, num=1):
        self.task_table.setRowCount(self.task_table.rowCount() - num)
        self._calculateDuration()

    def submit(self, optionStruct):
        num_tasks = self.task_table.rowCount()
        self.task_log_list.clear()

        for n in range(num_tasks):
            starttime = self.task_table.cellWidget(n, 0).dateTime().toPyDateTime()
            # TODO : check if ticket number is valid
            ticket_str = self.task_table.cellWidget(n, 2).currentText()
            try:
                ticket = int(ticket_str)
            except ValueError:
                print(ticket_str)
                ticket = -1
                # continue
            comment = self.task_table.item(n, 4).text()

            self.task_log_list.append_new(starttime, ticket, comment)

        # Close the day
        self.task_log_list.close_day(datetime.datetime.today())

        # Submit tasks to redmine
        redmine = RedmineEntry("http://redmine03/", 
            username=optionStruct.username, password=optionStruct.password)
        tasks_sorted = self.task_log_list.get_tasks_sorted()
        for task in tasks_sorted:
            redmine.submitTimeEntry(
                optionStruct.today,
                task.ticket_number,
                task.logged_time,
                task.activity_id,
                task.comment
            )

        # # Debug
        # self.task_log_list.show_tasks()
        # self.task_log_list.show_tasks_sorted()

    def _calculateDuration(self):
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
            item.setText(str(duration))
            self.task_table.setItem(n, 1, item)

    def _setSample(self):
        for _ in range(3):
            self.addNewTask()
        
        for n in range(self.task_table.rowCount()):
            widget = self.task_table.cellWidget(n, 0)
            widget.setDateTime(datetime.datetime(2020, 11, 17, 9+n, 0, 0))

            widget2 = self.task_table.cellWidget(n, 2)
            widget2.setCurrentIndex(n % 3 + 1)

            item = QTableWidgetItem()
            # item.setText(str(n) + "th job")
            item.setText("th job")
            self.task_table.setItem(n, 4, item)


def main():
    app = QApplication(sys.argv)
    timeKeeper = MyWindow()
    # timeKeeper.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
