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

        # File doesn't exist
        self.assertFalse(json.open("file_doesnt_exist.json", "r"))
        # Existing file
        self.assertTrue(json.open(self.test_dir + "/sample.json", "r"))

    def test_write(self):
        """Test write() method
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
                        "comments" : "Task 1 comment",
                    },
                    {
                        "starttime" : time(hour=10, minute=0, second=0).strftime("%H:%M:%S"),
                        "ticket_id" : "002",
                        "activity_id" : "2", 
                        "comments" : "Task 2 comment",
                    }
                ],
            },
        }
        jsonFile = JsonFile()

        if (os.path.exists(path_file)):
            os.remove(path_file)

        # Open
        self.assertTrue(jsonFile.open(path_file, "w"))
        # Write
        self.assertTrue(jsonFile.write(test_str))
        # Close the file
        jsonFile = None

        # Read file and check content
        with open(path_file) as file:
            read_str = json.load(file)
        self.assertEqual(test_str, read_str)


if __name__ == "__main__":
    unittest.main()
