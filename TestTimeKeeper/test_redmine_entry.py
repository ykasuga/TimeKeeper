# -*- coding: utf-8 -*-
"""
@file test_redmine_entry.py
@author Y. Kasuga
@date 2021/5/23
"""

import datetime
from redmine_entry import RedmineEntry, timedelta_to_hour

import unittest
from datetime import timedelta


class TestTimedeltaToHour(unittest.TestCase):
    """Test class for timedelta_to_hour
    """

    def test_timedelta_to_hour(self):
        timedelta = datetime.timedelta(seconds=900)
        expected = 0.25
        actual = timedelta_to_hour(timedelta)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
