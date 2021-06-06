# -*- coding: utf-8 -*-
"""
@file task_log_list.py
@author Y. Kasuga
@date 2021/1/30
@brief Definition of TaskLogList class.
"""

from datetime import datetime
from typing import List

from src.task_log import TaskLog
from src.redmine_entry import timedelta_to_hour


class TaskLogList():
    def __init__(self) -> None:
        """
        @fn __init__
        @brief Constructor of TaskLogList class.
        """
        self.tasks = []
        self.tasks_sorted = []

    def append_new(self, start_time: datetime, ticket_number: int, comment: str) -> bool:
        """
        @fn append_new
        @brief Append new task log to the list.
        @detail To append new task, the day should be open 
                and star time of the new task should be latter than the last task.
        @param start_time Star time of the new task.
        @param ticket_number Ticket number of the new task.
        @param comment Comment for the new task.
        @return Succeeded or not.
        """
        if self.is_day_closed():
            print("The day is already closed")
            return False

        if self.tasks and self.tasks[-1].start_time > start_time:
            print("Please specify valid start_time: {} > {}".format(
                self.tasks[-1].start_time.strftime("%Y-%m-%d %H:%M:%S"),
                start_time.strftime("%Y-%m-%d %H:%M:%S")
            ))
            return False

        self.tasks.append(TaskLog(len(self.tasks), start_time, ticket_number, comment))
        return True

    def insert_new(self, start_time: datetime, ticket_number: int, comment: str) -> bool:
        """
        @fn insert_new
        @brief Insert new task before existing tasks.
        @param start_time Star time of the new task.
        @param ticket_number Ticket number of the new task.
        @param comment Comment for the new task.
        @return Succeeded or not.
        """
        if self.is_day_closed():
            print("The day is already closed")
            return False

        self.tasks.append(TaskLog(len(self.tasks), start_time, ticket_number, comment))
        self.tasks = sorted(self.tasks, key=lambda task: task.start_time)
        return True

    def remove_task(self, task_id: int=-1) -> bool:
        """
        @fn remove_task
        @brief Remove an existing task.
        @param task_id The id of the task to remove.
        @return Suceeded or not
        """
        if self.is_day_closed():
            print("The day is already closed")
            return False

        if task_id == -1:
            self.tasks.pop(-1)
        elif task_id < len(self.tasks):
            del self.tasks[task_id]
        else:
            print("task_id out of range")
            return False
        
        return True

    def close_day(self, time: datetime) -> bool:
        """
        @fn close_day
        @brief Close the day.
        @detail If the day is already closed, return False.
        @param time The time to end the day.
        @return Succeeded or not.
        """
        if not self.is_day_closed():
            self.tasks.append(TaskLog(len(self.tasks), time))
            self.calculate_logged_time()
            self.sort()
            return True
        else:
            return False

    def is_day_closed(self) -> bool:
        """
        @fn is_day_closed
        @breif Check if the day is closed.
        @return If the day is closed.
        """
        if not len(self.tasks):
            return False

        for task in self.tasks:
            if task.is_end_of_day():
                return True

        return False

    def show_tasks(self) -> None:
        """
        @fn show_tasks
        @brief Prints the list of tasks in order of start time.
        """
        for task in self.tasks:
            task.show()
        print("")
    
    def show_tasks_sorted(self) -> None:
        """
        @fn show_tasks_sorted
        @brief Prints the list of tasks in order of ticket id.
        """
        for tasks_sorted in self.tasks_sorted:
            tasks_sorted.show()
        print(f"Total time: {self.get_total_time()}")
        print("")
    
    def calculate_logged_time(self) -> None:
        """
        @fn calculate_logged_time
        @brief Calculate logged time of every task.
        """
        for n in range(len(self.tasks) - 1):
            self.tasks[n].logged_time = self.tasks[n+1].start_time - self.tasks[n].start_time

    def sort(self) -> None:
        """
        @fn sort
        @brief Sort tasks in order of ticket id.
        """
        self.tasks_sorted = sorted(self.tasks)
        
        n = 0
        while n < len(self.tasks_sorted) - 1:
            n = n + 1

            while n < len(self.tasks_sorted) - 1:
                if self.tasks_sorted[n] == self.tasks_sorted[n+1]:
                    self.tasks_sorted[n].merge(self.tasks_sorted[n+1])
                    del self.tasks_sorted[n+1]
                else:
                    break

        n = -1
        while n < len(self.tasks_sorted) - 1:
            n = n + 1
            if self.tasks_sorted[n].ticket_number <= 0:
                    del self.tasks_sorted[n]
                    n -= 1
    
    def clear(self) -> None:
        """
        @fn clear
        @brief Clear all tasks.
        """
        self.tasks.clear()
        self.tasks_sorted.clear()

    def get_tasks_sorted(self) -> List[TaskLog]:
        """
        @fn get_tasks_sorted
        @brief Get list of sorted tasks.
        @return Sorted list of tasks.
        """
        return self.tasks_sorted

    def get_str_tasks_sorted(self) -> str:
        """Get list of tasks_sorted in formatted string

        Returns:
            str: List of tasks_sorted in formatted string
        """
        self.sort()
        
        str_tasks_sorted: str = ""
        for task in self.tasks_sorted:
            str_tasks_sorted += "{:10} {:>10} {:>10} {}\n".format(
                task.ticket_number,
                timedelta_to_hour(task.logged_time),
                task.activity_id,
                task.comment)
        str_tasks_sorted += f"Total time: {self.get_total_time()}"

        return str_tasks_sorted

    def get_task_dict(self) -> dict:
        """Get task list

        Returns:
            dict: Task list as a dictionary
        """
        key_date = "date"
        key_task = "task_list"
        task_dict = {
            key_date: datetime.today().strftime("%Y-%m-%d"),
            key_task: []
        }

        key_star_time = "start_time"
        key_ticket_id = "ticket_id"
        key_activity_id = "activity_id"
        key_comment = "comment"

        for task in self.tasks:
            task_dict[key_task].append(
                {
                    key_star_time: task.start_time.strftime("%H:%M:%S"),
                    key_ticket_id: task.ticket_number,
                    key_activity_id: task.activity_id,
                    key_comment: task.comment
                },
            )

        return task_dict

    def get_total_time(self, ndigits: int=2) -> float:
        """Get total time in the day
        """
        total_time = 0.

        self.calculate_logged_time()
        self.sort()
        for task in self.tasks_sorted:
            total_time += timedelta_to_hour(task.logged_time)

        return round(total_time, ndigits)
