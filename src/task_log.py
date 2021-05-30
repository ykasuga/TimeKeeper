# -*- coding: utf-8 -*-
"""
@file task_log.py
@author Y. Kasuga
@date 2021/5/30
@brief Definition of TaskLog class.
"""

from datetime import datetime, timedelta


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
