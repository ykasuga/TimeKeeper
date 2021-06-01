# -*- coding: utf-8 -*-
"""
@file test_json_file.py
@author Y. Kasuga
@date 2021/5/31
"""

from src.json_file import JsonFile

import unittest

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


if __name__ == "__main__":
    unittest.main()
