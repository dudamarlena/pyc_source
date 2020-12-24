# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brent/anaconda/envs/fba/lib/python2.7/site-packages/celery_geolocator/helpers/decorators.py
# Compiled at: 2014-09-11 18:35:22
import datetime
from time import sleep
__author__ = 'brent'

class MaxCallsExceededException(Exception):
    pass


class rate_limit(object):
    """
    This is a single threaded solution and does not rate limit across threads or processes.
    """

    def __init__(self, one_per_timedelta=None, max_limit=None, refresh_after_timedelta=None):
        self.one_per_timedelta = one_per_timedelta
        self.number_of_calls = 0
        self.max_limit = None
        self.refresh_after_timedelta = refresh_after_timedelta
        self.first_call_in_cycle = None
        return

    def __call__(self, function_to_decorate):

        def rate_limited_function(*args, **kwargs):
            if not self.first_call_in_cycle:
                self.first_call_in_cycle = datetime.datetime.now()
            if self.max_limit and self.number_of_calls + 1 > self.max_limit:
                if self.refresh_after_timedelta:
                    time_left = datetime.datetime.now() + self.one_per_timedelta - self.first_call_in_cycle
                    sleep(time_left.total_seconds())
                    self.number_of_calls = 0
                    self.first_call_in_cycle = datetime.datetime.now()
                else:
                    raise MaxCallsExceededException()
            return_value = function_to_decorate(*args, **kwargs)
            self.number_of_calls += 1
            if self.one_per_timedelta:
                sleep(self.one_per_timedelta.total_seconds())
            return return_value

        return rate_limited_function