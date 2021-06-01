# -*- coding: utf-8 -*-
"""
@file json.py
@author Y. Kasuga
@date 2021/5/31
"""

import os


class JsonFile(object):
    """IO class of json file
    """
    def __init__(self) -> None:
        """Constructor of JsonFile class
        """
        self.file = None
        super().__init__()

    def open(self, path_file: str, mode: str):
        """Open a new file

        Args:
            path_file (str): Path to the file
            mode (str): Open mode: "r" or "w"

        Returns:
            bool: Succeeded or failed
        """
        mode_read = "r"
        mode_write = "w"

        # Already opened a file
        if self.file:
            return False

        # Read mode but file doesn't exits
        if mode == mode_read and not os.path.exists(path_file):
            return False

        # Write mode but file already exist
        if mode == mode_write and os.path.exists(path_file):
            return False

        self.file = open(path_file, mode)
        return True
