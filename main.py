# -*- coding: utf-8 -*-
"""
@file main.py
@author Y. Kasuga
@date 2021/1/29
@brief Entry point of TimeKeeper.
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.mywindow import MyWindow


def main() -> None:
    """
    @fn main
    @brief Entry point of the program.
    @return None
    """
    app = QApplication(sys.argv)
    timeKeeper = MyWindow()
    # timeKeeper.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
