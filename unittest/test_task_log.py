# -*- coding: utf-8 -*-
"""
@file test_task_log.py
@author Y. Kasuga
@date 2021/5/30
"""

from src.task_log import TaskLog

import unittest
from datetime import datetime
import sys
from io import StringIO


class TestTaskLog(unittest.TestCase):
    """Test case for TaskLog class
    """
    def setUp(self) -> None:
        self._task1_datetime = datetime(2021, 5, 23, 9, 0, 0)
        self.task1 = TaskLog(1, self._task1_datetime, 1, "comment1")
        self.task2 = TaskLog(2, datetime(2021, 5, 23, 10, 0, 0), 2, "comment2")
        self.task3 = TaskLog(3, datetime(2021, 5, 23, 11, 0, 0), 1, "comment1")
        self.task4 = TaskLog(4, datetime(2021, 5, 23, 12, 0, 0), 1, "comment1.2")

        self.task1.logged_time = 1
        self.task2.logged_time = 1
        self.task3.logged_time = 1
        self.task4.logged_time = 1

        self.org_stdout, sys.stdout = sys.stdout, StringIO()

        return super().setUp()

    def tearDown(self) -> None:
        sys.stdout = self.org_stdout

        return super().tearDown()

    def test___lt__(self) -> None:
        """Test __lt__() method
        """
        self.assertTrue(self.task1 < self.task2)
        self.assertFalse(self.task1 < self.task3)

    def test___eq__(self) -> None:
        """Test __eq__() method
        """
        self.assertEqual(self.task1, self.task3)
        self.assertNotEqual(self.task1, self.task2)
        self.assertNotEqual(self.task1, self.task4)

    def test_start_time(self) -> None:
        """Test start_time() method
        """
        actual = self.task1.start_time
        self.assertEqual(self._task1_datetime, actual)

    def test_show(self) -> None:
        """Test sho() method
        """
        self.task1.show()
        actual = f"1 : {self._task1_datetime.strftime('%Y-%m-%d %H:%M:%S')} 1 1 comment1\n"
        self.assertEqual(sys.stdout.getvalue(), actual)

    def test_is_end_of_day(self) -> None:
        """Test is_end_of_day() method
        """
        ticket = TaskLog(0, datetime.today(), 0, "End of day")
        self.assertTrue(ticket.is_end_of_day())
        self.assertFalse(self.task1.is_end_of_day())

    # def test_submit_log(self):
    #     """Test submit_log() method
    #     """
    #     pass

    def test_merge(self) -> None:
        """Test merge() method
        """
        self.assertEqual(1, self.task1.logged_time)
        self.task1.merge(self.task3)
        self.assertEqual(2, self.task1.logged_time)
