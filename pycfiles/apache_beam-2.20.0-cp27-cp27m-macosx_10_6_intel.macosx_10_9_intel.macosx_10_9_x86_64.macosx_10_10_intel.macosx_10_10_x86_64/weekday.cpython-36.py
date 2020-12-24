# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/utils/weekday.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1639 bytes
import enum

@enum.unique
class WeekDay(enum.IntEnum):
    """WeekDay"""
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    @classmethod
    def get_weekday_number(cls, week_day_str):
        """
        Return the ISO Week Day Number for a Week Day

        :param week_day_str: Full Name of the Week Day. Example: "Sunday"
        :type week_day_str: str
        :return: ISO Week Day Number corresponding to the provided Weekday
        """
        sanitized_week_day_str = week_day_str.upper()
        if sanitized_week_day_str not in cls.__members__:
            raise AttributeError('Invalid Week Day passed: "{}"'.format(week_day_str))
        return cls[sanitized_week_day_str]