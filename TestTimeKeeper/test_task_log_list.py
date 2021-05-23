# -*- coding: utf-8 -*-
"""
@file test_task_log_list.py
@author Y. Kasuga
@date 2021/5/23
"""

from datetime import datetime
from task_log_list import TaskLog

import unittest


class TestTaskLog(unittest.TestCase):
    """Test case for TaskLog class
    """
    def setUp(self) -> None:
        self.tasklog1 = TaskLog(1, datetime(2021, 5, 23, 9, 0, 0), 1, "comment1")
        self.tasklog2 = TaskLog(2, datetime(2021, 5, 23, 10, 0, 0), 2, "comment2")

        return super().setUp()

    def test___lt__(self):
        # self.assertTrue(self.tasklog1 < self.tasklog2)
        self.assertTrue(self.tasklog1 > self.tasklog2)


if __name__ == "__main__":
    unittest.main()
