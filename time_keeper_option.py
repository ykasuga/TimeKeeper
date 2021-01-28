# -*- coding: utf-8 -*-
"""
@file time_keeper_option.py
@author Y. Kasuga
@date 2021/1/29
@brief Option of TimeKeeper.
"""

import os

from PyQt5.QtCore import pyqtSignal
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
        self.username = ""
        self.password = ""
        self.today = QDateTime()


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
        self.userfolder = ""
        self.savefile = "C:\\Users\\y-kas\\Desktop\\TimeKeeperOption.txt"

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

        optionStruct.username = self.edit_username.text()
        optionStruct.password = self.edit_password.text()
        optionStruct.today = self.edit_today.text()

        return optionStruct

    def _closeEvent(self):
        self._saveOption()
        self.closed.emit()

    def _selectUserfolder(self):
        fileDialog = QFileDialog()
        self.userfolder = fileDialog.getExistingDirectory()
        # self.edit_userfolder.setText(self.userfolder)

    def _loadOption(self):
        lines = []
        username = ""
        password = ""

        with open(self.savefile, "r") as f:
            lines = [s.strip() for s in f.readlines()]
            self.userfolder = lines[0]
            username = lines[1]
            password = lines[2]
        
        # self.edit_userfolder.setText(self.userfolder)
        self.edit_username.setText(username)
        self.edit_password.setText(password)

    def _saveOption(self):
        with open(self.savefile, "w") as f:
            f.write(self.userfolder + "\n")
            f.write(self.edit_username.text() + "\n")
            f.write(self.edit_password.text() + "\n")
