# -*- coding: utf-8 -*-
"""
@file test_task_log_list.py
@author Y. Kasuga
@date 2021/5/23
"""

import datetime
from src.task_log_list import TaskLogList

import unittest
from PyQt5.QtCore import QTime

from src.redmine_entry import timedelta_to_hour
from src.task_log import TaskLog


class TestTaskLogList(unittest.TestCase):
    """Test case for TaskLogList class
    """

    def setUp(self) -> None:
        self.new_task1 = TaskLog(1, QTime(11, 34, 56), 101, "New task1")
        self.new_task2 = TaskLog(2, QTime(12, 34, 56), 102, "New task2")
        self.new_task3 = TaskLog(3, QTime(13, 34, 56), 103, "New task3")
        self.close_time = QTime(17, 30, 0)
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

    def test_close_day(self) -> None:
        """Test close_day() method
        """
        taskList = TaskLogList()
        self.assertTrue(taskList.close_day(self.close_time))

        # Added ticket with id=0
        self.assertEqual(0, taskList.tasks[0].ticket_number)

        # Cannot close the day which is already closed
        self.assertFalse(taskList.close_day(self.close_time))

    def test_is_day_closed(self) -> None:
        """Test is_day_closed() method
        when it is not closed
        """
        taskList = TaskLogList()
        self.assertTrue(taskList.append_new(
            self.new_task1.start_time, self.new_task1.ticket_number, self.new_task1.comment
        ))
        self.assertFalse(taskList.is_day_closed())

    def test_is_day_closed_no_tasks(self) -> None:
        """Test is_day_closed() method
        when it has no tasks
        """
        taskList = TaskLogList()
        self.assertFalse(taskList.is_day_closed())

    def test_is_day_closed_already_closed(self) -> None:
        """Test is_day_closed() method
        when it is already closed
        """
        taskList = TaskLogList()
        # Add ticket with id=0, which means the end of the day
        self.assertTrue(taskList.append_new(
            self.new_task1.start_time, 0, self.new_task1.comment
        ))
        self.assertTrue(taskList.is_day_closed())

    # def test_show_tasks(self) -> None:

    # def test_show_tasks_sorted(self) -> None:

    def test_calculate_logged_time(self) -> None:
        """Test calculate_logged time() method
        """
        taskList = TaskLogList()
        self.assertTrue(taskList.append_new(
            self.new_task1.start_time, self.new_task1.ticket_number, self.new_task1.comment
        ))
        self.assertTrue(taskList.append_new(
            self.new_task2.start_time, self.new_task2.ticket_number, self.new_task2.comment
        ))
        self.assertTrue(taskList.append_new(
            self.new_task3.start_time, self.new_task3.ticket_number, self.new_task3.comment
        ))

        # Close tha day
        self.assertTrue(taskList.append_new(
            self.close_time, 0, ""
        ))

        # Calculate logged time
        taskList.calculate_logged_time()

        # Assert
        self.assertEqual(datetime.timedelta(hours=1), taskList.tasks[0].logged_time)
        self.assertEqual(datetime.timedelta(hours=1), taskList.tasks[1].logged_time)
        self.assertEqual(datetime.timedelta(hours=3, minutes=55, seconds=4), taskList.tasks[2].logged_time)
        self.assertEqual(datetime.timedelta(0), taskList.tasks[3].logged_time)

    def test_sort(self) -> None:
        """Test sort() method
        """
        new_task1 = TaskLog(1, QTime(11, 34, 56), 101, "New task1")
        new_task2 = TaskLog(2, QTime(12, 34, 56), 102, "New task2")
        new_task3 = TaskLog(3, QTime(13, 34, 56), 103, "New task3")
        new_task4 = TaskLog(4, QTime(14, 34, 56), 101, "New task1")

        taskList = TaskLogList()
        self.assertTrue(taskList.append_new(
            new_task1.start_time, new_task1.ticket_number, new_task1.comment
        ))
        self.assertTrue(taskList.append_new(
            new_task2.start_time, new_task2.ticket_number, new_task2.comment
        ))
        self.assertTrue(taskList.append_new(
            new_task3.start_time, new_task3.ticket_number, new_task3.comment
        ))
        self.assertTrue(taskList.append_new(
            new_task4.start_time, new_task4.ticket_number, new_task4.comment
        ))

        # Close tha day
        self.assertTrue(taskList.append_new(
            self.close_time, 0, ""
        ))

        # Sort
        taskList.sort()

        # Number of sorted tasks
        self.assertEqual(3, len(taskList.tasks_sorted))
        # Start time
        self.assertEqual(new_task1.start_time, taskList.tasks_sorted[0].start_time)
        self.assertEqual(new_task2.start_time, taskList.tasks_sorted[1].start_time)
        self.assertEqual(new_task3.start_time, taskList.tasks_sorted[2].start_time)
        # ticket_number
        self.assertEqual(new_task1.ticket_number, taskList.tasks_sorted[0].ticket_number)
        self.assertEqual(new_task2.ticket_number, taskList.tasks_sorted[1].ticket_number)
        self.assertEqual(new_task3.ticket_number, taskList.tasks_sorted[2].ticket_number)

    # def test_clear(self) -> None:

    # def test_get_tasks_sorted(self) -> None:

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

    # def test_get_task_dict(self) -> None:

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

    # def test_set_tasks(self) -> None:


if __name__ == "__main__":
    unittest.main()
