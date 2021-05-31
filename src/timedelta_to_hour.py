# -*- coding: utf-8 -*-
"""
@file timedelta_to_hour.py
@author Y. Kasuga
@date 2021/5/30
"""

from datetime import date, datetime, timedelta


def timedelta_to_hour(delta_t: timedelta) -> float:
    """
    @fn timedelta_to_hour
    @brief Convert timedelta to hours in float.
    @param timedelta Timedelta to convert.
    @return Converted hours.
    """
    return round(delta_t / timedelta(hours=1), 2)
