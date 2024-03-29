# -*- coding: utf-8 -*-
"""
@file redmine_entry.py
@author Y. Kasuga
@date 2021/1/30
"""

from datetime import datetime, timedelta
from redminelib import Redmine

from src.timedelta_to_hour import timedelta_to_hour


class RedmineEntry(object):
    """
    @class RedmineEntry
    @brief Time entry for redmine.
    """
    def __init__(self, url: str, username: str, password: str) -> None:
        """
        @fn __init__
        @brief Constructor of RedmineEntry class.
        @param url URL of the Redmine's root page.
        @param username User's ID to login.
        @param password Password to login.
        """
        self.redmine = Redmine(url=url, username=username, password=password, requests={'verify': False})


    def submitTimeEntry(self, date: datetime, ticket_number: int,
        logged_time: timedelta, activity: str, comment: str) -> bool:
        """
        @fn submitTimeEntry
        @brief Submit time entry to the redmine ticket.
        @param date Logged date.
        @param ticket_number Issue ID.
        @param logged_time Duration of the task.
        @param activity Activity type.
        @param comment Comment.
        @return Succeeded or not.
        """
        time_entry = self.redmine.time_entry.new()

        try:
            time_entry.issue_id = ticket_number
            time_entry.hours = timedelta_to_hour(logged_time)
            # time_entry.activity_id = activity
            time_entry.comments = comment
            # time_entry.activity = "開発要件001:調査・設計"
        
            time_entry.save()
        except Exception as e:
            print(f"Error on RedmineEntry: {e}")
            return

        # TODO : Debug
        print(
            "submit: ",
            ticket_number,
            date,
            time_entry.hours,
            activity,
            comment
        )

        return True
