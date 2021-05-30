# -*- coding: utf-8 -*-
"""
@file timedelta_to_hour.py
@author Y. Kasuga
@date 2021/5/30
"""

from datetime import timedelta


def timedelta_to_hour(timedelta: timedelta) -> float:
    """
    @fn timedelta_to_hour
    @brief Convert timedelta to hours in float.
    @param timedelta Timedelta to convert.
    @return Converted hours.
    """
    seconds_per_hour = 3600
    return round(timedelta.total_seconds() / seconds_per_hour, 2)
