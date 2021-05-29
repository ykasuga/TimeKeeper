# -*- coding: utf-8 -*-
"""
@file task_log_list.py
@author Y. Kasuga
@date 2021/1/30
@brief Definition of TaskLog class and TaskLogList class.
"""

import datetime
from datetime import timedelta

# from redmine_entry import timedelta_to_hour
from src.redmine_entry import timedelta_to_hour


class TaskLog():
    """
    @class TaskLog
    @brief Set of parameters of a task
    """
    def __init__(self, id: int, start_time: datetime,
        ticket_number: int=0, comment: str="EndOfDay") -> None:
        """
        @fn __init__
        @brief Constructor of TaskLog class
        @param id Identification number of the task
        @param start_time When the task began
        @param ticket_number Ticket id to log the task. Default=0.
        @param comment Comment of the ticket. Default="EndOfDay".
        @return None
        """
        self.id = id
        self._start_time = start_time
        self.logged_time = timedelta(0.)
        self._ticket_number = ticket_number
        self.activity_id = 1
        self._comment = comment

    def __lt__(self, other) -> bool:
        return self.ticket_number < other.ticket_number
    # def __le__(self, other) -> bool:
    #     return self.ticket_number <= other.ticket_number
    def __eq__(self, other) -> bool:
        return self.ticket_number == other.ticket_number and self.comment == other.comment
    # def __ne__(self, other) -> bool:
    #     return self.ticket_number != other.ticket_number
    # def __gt__(self, other) -> bool:
    #     return self.ticket_number > other.ticket_number
    # def __ge__(self, other) -> bool:
    #     return self.ticket_number >= other.ticket_number

    #=== Properties ===
    @property
    def start_time(self) -> datetime:
        return self._start_time

    # @start_time.setter

    @property
    def ticket_number(self) -> int:
        return self._ticket_number

    # @ticket_number.setter

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, comment: str) -> None:
        if self._ticket_number:
            self._comment = comment

    #=== Functions ===    
    def show(self, message_callback=print) -> None:
        """
        @fn show
        @brief Show the parameters of the task.
        @param message_callback Specify the way to output.
        @return None
        """
        message_callback("{} : {} {} {} {}".format(self.id,
            self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            self.logged_time, self.ticket_number, self.comment
            ))

    def is_end_of_day(self) -> bool:
        """
        @fn is_end_of_day
        @brief Returns if this task is the end of a day.
        @detail If _ticket_number equals 0, the task is recognized as the end of a day.
        @return Wheather this task is the end of a day.
        """
        return self._ticket_number == 0

    def submit_log(self) -> None:
        """
        @fn submit_log
        @brief Submit task log to the ticket.
        @note TODO not implemented
        """
        pass

    def merge(self, other_task: int) -> bool:
        """
        @fn merge
        @brief Merge with other task.
        @param other_task Instance of TaskLog class of other task.
        @return Succeeded or not.
        """
        if not self == other_task:
            return False

        self.logged_time += other_task.logged_time
        return True


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

    def get_tasks_sorted(self): # TODO : return type
        """
        @fn get_tasks_sorted
        @brief Get list of sorted tasks.
        @return Sorted list of tasks.
        """
        return self.tasks_sorted

    def get_total_time(self) -> float:
        """Get total time in the day
        """
        total_time = 0.

        self.calculate_logged_time()
        self.sort()
        for task in self.tasks_sorted:
            total_time += timedelta_to_hour(task.logged_time)

        return total_time
