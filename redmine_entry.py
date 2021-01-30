# -*- coding: utf-8 -*-
"""
@file redmine_entry.py
@author Y. Kasuga
@date 2021/1/30
"""

from redminelib import Redmine


class RedmineEntry(object):
    """
    @class RedmineEntry
    @brief Time entry for redmine.
    """
    def __init__(self, url, username, password) -> None:
        """
        @fn __init__
        @brief Constructor of RedmineEntry class.
        """
        self.redmine = Redmine(url, username=username, password=password)

    def submitTimeEntry(self, date, ticket_number, logged_time, activity, comment) -> bool:
        """
        @fn submitTimeEntry
        @brief Submit time entry to the redmine ticket.
        @return Succeeded or not.
        """
        time_entry = self.redmine.time_entry.new()
        time_entry.issue_id = ticket_number
        time_entry.spent_on = date
        # time_entry.hours = 3   # TODO
        time_entry.hours = logged_time
        time_entry.activity_id = activity
        time_entry.comments = comment
        # time_entry.save()

        # TODO : Debug
        print(
            "submit: ",
            ticket_number,
            date,
            logged_time,
            activity,
            comment
        )

        return True
