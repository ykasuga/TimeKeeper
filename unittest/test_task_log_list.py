# -*- coding: utf-8 -*-
"""
@file test_task_log_list.py
@author Y. Kasuga
@date 2021/5/23
"""

from src.task_log_list import TaskLog, TaskLogList

import unittest
from datetime import datetime
import sys
from io import StringIO

from src.redmine_entry import timedelta_to_hour


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


class TestTaskLogList(unittest.TestCase):
    """Test case for TaskLogList class
    """

    def setUp(self) -> None:
        self.new_task1 = TaskLog(1, datetime(2021, 1, 1, 11, 34, 56), 101, "New task1")
        self.new_task2 = TaskLog(2, datetime(2021, 1, 1, 12, 34, 56), 102, "New task2")
        self.new_task3 = TaskLog(3, datetime(2021, 1, 1, 13, 34, 56), 103, "New task3")
        self.close_time = datetime(2021, 1, 1, 17, 30)
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_append_new(self) -> None:
        """Test append_new() method
        """
        taskList = TaskLogList()

        # Append new task
        self.assertTrue(taskList.append_new(
            self.new_task1.start_time, self.new_task1.ticket_number, self.new_task1.comment
        ))
        self.assertTrue(taskList.append_new(
            self.new_task2.start_time, self.new_task2.ticket_number, self.new_task2.comment
        ))

        self.assertEqual(self.new_task1, taskList.tasks[0])
        self.assertEqual(self.new_task2, taskList.tasks[1])
        # Num of tasks
        self.assertEqual(2, len(taskList.tasks))

        # Close the day
        taskList.close_day(self.close_time)
        # Cannot append new task to closed day
        self.assertFalse(taskList.append_new(
            self.new_task3.start_time, self.new_task3.ticket_number, self.new_task3.comment
        ))

    def test_insert_new(self) -> None:
        """Test insert_new() method
        """
        taskList = TaskLogList()

        # Insert new task
        self.assertTrue(taskList.append_new(
            self.new_task1.start_time, self.new_task1.ticket_number, self.new_task1.comment
        ))
        self.assertTrue(taskList.append_new(
            self.new_task2.start_time, self.new_task2.ticket_number, self.new_task2.comment
        ))

        self.assertEqual(self.new_task1, taskList.tasks[0])
        self.assertEqual(self.new_task2, taskList.tasks[1])
        # Num of tasks
        self.assertEqual(2, len(taskList.tasks))

        # Close the day
        taskList.close_day(self.close_time)
        # Cannot append new task to closed day
        self.assertFalse(taskList.append_new(
            self.new_task3.start_time, self.new_task3.ticket_number, self.new_task3.comment
        ))

    def test_remove_task(self) -> None:
        """Test remove_task() method
        """
        taskList = TaskLogList()

        # Append new task
        self.assertTrue(taskList.append_new(
            self.new_task1.start_time, self.new_task1.ticket_number, self.new_task1.comment
        ))
        self.assertTrue(taskList.append_new(
            self.new_task2.start_time, self.new_task2.ticket_number, self.new_task2.comment
        ))

        # Num of tasks
        self.assertEqual(2, len(taskList.tasks))

        # Cannot remove task out of range
        self.assertFalse(taskList.remove_task(2))
        # Remove task
        self.assertTrue(taskList.remove_task(1))
        self.assertEqual(1, len(taskList.tasks))

    def test_get_str_tasks_sorted(self) -> None:
        """Test get_str_tasks_sorted() method
        """
        taskList = TaskLogList()

        # Append new task
        self.assertTrue(taskList.append_new(
            self.new_task1.start_time, self.new_task1.ticket_number, self.new_task1.comment
        ))
        self.assertTrue(taskList.append_new(
            self.new_task2.start_time, self.new_task2.ticket_number, self.new_task2.comment
        ))

        # Expected string
        expected: str = ""
        # task1
        expected += "{:10} {:>10} {:>10} {}\n".format(
            self.new_task1.ticket_number,
            timedelta_to_hour(self.new_task1.logged_time),
            self.new_task1.activity_id,
            self.new_task1.comment)
        # task2
        expected += "{:10} {:>10} {:>10} {}\n".format(
            self.new_task2.ticket_number,
            timedelta_to_hour(self.new_task2.logged_time),
            self.new_task2.activity_id,
            self.new_task2.comment)
        # Total time
        expected += "Total time: 1.0"

        self.assertEqual(expected, taskList.get_str_tasks_sorted())

    def test_get_total_time(self) -> None:
        """Test get_total_time() method
        """
        taskList = TaskLogList()

        # Append new task
        self.assertTrue(taskList.append_new(
            self.new_task1.start_time, self.new_task1.ticket_number, self.new_task1.comment
        ))
        self.assertTrue(taskList.append_new(
            self.new_task2.start_time, self.new_task2.ticket_number, self.new_task2.comment
        ))

        self.assertEqual(1., taskList.get_total_time())


if __name__ == "__main__":
    unittest.main()
