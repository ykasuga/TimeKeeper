# -*- coding: utf-8 -*-
"""
@file json.py
@author Y. Kasuga
@date 2021/5/31
"""

import os
import json


class JsonFile(object):
    """IO class of json file
    """
    def __init__(self) -> None:
        """Constructor of JsonFile class
        """
        self.file = None
        super().__init__()

    def __del__(self) -> None:
        """Destructor of JsonFile class
        """
        if self.file:
            self.file.close()

    def open(self, path_file: str, mode: str) -> bool:
        """Open a new file

        Args:
            path_file (str): Path to the file
            mode (str): Open mode: "r" or "w"

        Returns:
            bool: True for success, False for failure
        """
        mode_read = "r"
        mode_write = "w"

        # Already opened a file
        if self.file:
            return False

        # Read mode but file doesn't exits
        if mode == mode_read and not os.path.exists(path_file):
            return False

        # Write mode but file already exists
        # if mode == mode_write and os.path.exists(path_file):
        #     return False

        self.file = open(path_file, mode)
        return True

    def read(self) -> str:
        """Read json file

        Returns:
            str: Content in the file
        """
        if not self.file:
            return None

        content = json.load(self.file)
        return content

    def write(self, content: str) -> bool:
        """Write string to json file

        Args:
            content (str): Content to write to the file

        Returns:
            bool: True for success, False for failure
        """
        if not self.file:
            return False

        json_str = json.dumps(content, indent=4)
        self.file.writelines(json_str)

        # Close the file
        self.file.close()

        return True
