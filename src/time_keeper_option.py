# -*- coding: utf-8 -*-
"""
@file time_keeper_option.py
@author Y. Kasuga
@date 2021/1/29
@brief Option of TimeKeeper.
"""

from PyQt5.QtCore import QFile, pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QDateTimeEdit, QFileDialog
from PyQt5.QtCore import QDateTime


class OptionStruct(object):
    """
    @class OptionStruct
    @brief Option parameters.
    """
    def __init__(self) -> None:
        """
        @fn __init__()
        @brief Constructor of OptionStruct class.
        """
        self.redmine_server: str = ""
        self.username: str = ""
        self.password: str = ""
        self.today = QDateTime()
        self.save_file: str = ""


class TimeKeeperOption(QWidget):
    """
    @class TimeKeeperOption
    @brief Option parameters for TimeKeeper.
    @note
    TODO :
        userfolder
        username
        password
        today's date
        ticket list
    """
    closed = pyqtSignal()

    def __init__(self) -> None:
        """
        @fn __init__()
        @brief Constructor on TimeKeeperOption class.
        """
        super().__init__()

        self._redmine_server = ""
        self.userfolder = ""
        self.option_file = "TimeKeeperOption.txt"
        self._save_file = ""

        self.layout_options = QFormLayout(self)
        self._initUI()
        self.setLayout(self.layout_options)

        self._loadOption()

    def _initUI(self) -> None:
        """
        @fn _initUI()
        @brief Initialize UI of option dialog.
        """
        # # Userfolder
        # self.button_userfolder = QPushButton("Select")
        # self.button_userfolder.clicked.connect(lambda: self._selectUserfolder())
        # self.edit_userfolder = QLineEdit(self)
        # self.layout_options.addRow(self.button_userfolder, self.edit_userfolder)

        # Redmine server
        self.label_redmine_server = QLabel("Redmine server")
        self.edit_redmine_server = QLineEdit(self)
        self.layout_options.addRow(self.label_redmine_server, self.edit_redmine_server)

        # Username
        self.label_username = QLabel("Username")
        self.edit_username = QLineEdit(self)
        self.layout_options.addRow(self.label_username, self.edit_username)

        # Password
        self.label_password = QLabel("Password")
        self.edit_password = QLineEdit(self)
        self.edit_password.setEchoMode(QLineEdit.Password)
        self.layout_options.addRow(self.label_password, self.edit_password)

        # Today
        self.label_today = QLabel("Date")
        self.edit_today = QDateTimeEdit(self)
        self.edit_today.setDisplayFormat("yyyy.MM.dd")
        date = QDateTime()
        self.edit_today.setDateTime(date.currentDateTime())
        self.layout_options.addRow(self.label_today, self.edit_today)

        # Save file
        self.button_save_file = QPushButton("Select save file")
        self.edit_save_file = QLineEdit(self)
        self.layout_options.addRow(self.button_save_file, self.edit_save_file)
        self.button_save_file.clicked.connect(lambda: self._selectSaveFile())

        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self._closeEvent)
        self.layout_options.addWidget(self.close_button)

    def getOptionStruct(self) -> OptionStruct:
        """
        @fn getOptionStruct()
        @breif Getter.
        @return optionStruct A structure of option parameters.
        """
        optionStruct = OptionStruct()

        optionStruct.redmine_server = self.edit_redmine_server.text()
        optionStruct.username = self.edit_username.text()
        optionStruct.password = self.edit_password.text()
        optionStruct.today = self.edit_today.dateTime()
        optionStruct.save_file = self.edit_save_file.text()

        return optionStruct

    def _closeEvent(self) -> None:
        """
        @fn _closeEvent
        @brief Save option parameters and close dialog.
        """
        self._saveOption()
        self.closed.emit()

    def _selectUserfolder(self) -> None:
        """
        @fn _selectUserfolder
        @brief Let user to select userfolder.
        """
        fileDialog = QFileDialog()
        self.userfolder = fileDialog.getExistingDirectory()
        # self.edit_userfolder.setText(self.userfolder)

    def _selectSaveFile(self) -> None:
        """Select save file path
        """
        save_file_dialog = QFileDialog()
        self._save_file = save_file_dialog.getSaveFileName()[0]
        self.edit_save_file.setText(self._save_file)

    def _loadOption(self) -> None:
        """
        @fn _loadOption
        @brief Load option parameters from the savefile.
        """
        lines = []
        username = ""
        password = ""

        try:
            with open(self.option_file, "r") as f:
                lines = [s.strip() for s in f.readlines()]
                self._redmine_server = lines[0]
                self.userfolder = lines[1]
                username = lines[2]
                password = lines[3]
                self._save_file = lines[4]
        except FileNotFoundError:
            print("No option file found.")
        except IndexError:
            pass
        
        # self.edit_userfolder.setText(self.userfolder)
        self.edit_redmine_server.setText(self._redmine_server)
        self.edit_username.setText(username)
        self.edit_password.setText(password)
        self.edit_save_file.setText(self._save_file)

    def _saveOption(self) -> None:
        """
        @fn _saveOption
        @brief Save option parameters from the savefile.
        """
        with open(self.option_file, "w") as f:
            f.write(self.edit_redmine_server.text() + "\n")
            f.write(self.userfolder + "\n")
            f.write(self.edit_username.text() + "\n")
            f.write(self.edit_password.text() + "\n")
            f.write(self._save_file + "\n")

    def _setSaveFile(self) -> None:
        """Set _save_file variable
        """
        self._save_file = self.edit_save_file.text()
