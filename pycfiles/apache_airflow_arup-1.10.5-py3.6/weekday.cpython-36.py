# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/utils/weekday.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1639 bytes
import enum

@enum.unique
class WeekDay(enum.IntEnum):
    __doc__ = '\n    Python Enum containing Days of the Week\n    '
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