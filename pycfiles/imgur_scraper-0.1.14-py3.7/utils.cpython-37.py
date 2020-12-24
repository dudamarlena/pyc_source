# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/imgur_scraper/utils.py
# Compiled at: 2019-09-15 21:08:27
# Size of source mod 2**32: 1030 bytes
from datetime import datetime
date_format = '%Y-%m-%d'

class Convert:
    __doc__ = 'Subtracts the given time from the current UTC time\n    and returns the number of days.\n\n    :param:start_date, where date is a string\n    :param:end_date, where date is a string\n    '

    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date

    def _user_given_time(self):
        return (
         datetime.strptime(self.start_date, date_format),
         datetime.strptime(self.end_date, date_format))

    def to_days_ago(self):
        start_time, end_time = self._user_given_time()
        time_now = datetime.utcnow()
        if time_now < start_time or time_now < end_time:
            raise ValueError('Invalid Date')
        start_time = (datetime.utcnow() - start_time).days
        end_time = (datetime.utcnow() - end_time).days
        if start_time < end_time:
            raise ValueError('Invalid Date Range')
        return (
         start_time, end_time)