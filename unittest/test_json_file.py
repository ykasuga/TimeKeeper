# -*- coding: utf-8 -*-
"""
@file test_json_file.py
@author Y. Kasuga
@date 2021/5/31
"""

from src.json_file import JsonFile

import unittest
import os
import json
from datetime import datetime, time

class TestJsonFile(unittest.TestCase):
    """Test case for JsonFile class
    """

    def setUp(self) -> None:
        # Directory of test data
        self.test_dir = "unittest/data"
        return super().setUp()

    def test_open(self):
        """Test open() method
        """
        json = JsonFile()

        # Read mode but file doesn't exist
        self.assertFalse(json.open("file_doesnt_exist.json", "r"))
        # Write mode but file already exists
        # self.assertFalse(json.open(self.test_dir + "/sample.json", "w"))
        # Existing file
        self.assertTrue(json.open(self.test_dir + "/sample.json", "r"))
        # Already opended a file
        self.assertFalse(json.open(self.test_dir + "/sample.json", "r"))

    def test_read_write(self):
        """Test read() and write() method
        """
        path_file = self.test_dir + "/test_file.json"
        test_str = {
            "account" : {
                "username" : "yohei.kasuga",
                "password" : "my_password",
            },
            "data" : {
                "date" : datetime(2021, 6, 1).strftime("%Y-%m-%d"),
                "task_list" : [
                    {
                        "start_time" : time(hour=9, minute=0, second=0).strftime("%H:%M:%S"),
                        "ticket_id" : "001",
                        "activity_id" : "1", 
                        "comment" : "Task 1 comment",
                    },
                    {
                        "starttime" : time(hour=10, minute=0, second=0).strftime("%H:%M:%S"),
                        "ticket_id" : "002",
                        "activity_id" : "2", 
                        "comment" : "Task 2 comment",
                    }
                ],
            },
        }

        if (os.path.exists(path_file)):
            os.remove(path_file)

        #
        # Write test
        #
        jsonFile_write = JsonFile()
        # Write before openning file
        self.assertFalse(jsonFile_write.write(test_str))
        # Open
        self.assertTrue(jsonFile_write.open(path_file, "w"))
        # Write
        self.assertTrue(jsonFile_write.write(test_str))
        # Close the file
        jsonFile_write = None

        #
        # Read test
        #
        jsonFile_read = JsonFile()
        # Open
        jsonFile_read.open(path_file, "r")
        # Read
        read_content = jsonFile_read.read()
        # Assert
        self.assertEqual(test_str, read_content)
        # Close the file
        jsonFile_read = None


if __name__ == "__main__":
    unittest.main()
