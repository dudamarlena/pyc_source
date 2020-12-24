# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/timing.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 7699 bytes
"""
Simple code performance timer that allows for the execution time to be recorded

**Credit:**

- This is a modified version of Paul's and Nicojo's answers on stackoverflow.
- Reference: http://stackoverflow.com/questions/1557571/how-to-get-time-of-a-python-program-execution

**Usage Case:**

>>> # At the beginning of the chunk of code to be timed.
>>> from blowdrycss.timing import Timer
>>> timer = Timer()
>>> timer.report()
Completed @ 2015-12-14 16:56:08.665080
=======================================
It took: 0.17296 seconds
=======================================

"""
from __future__ import absolute_import, print_function, division, unicode_literals
from builtins import str
from time import time
from datetime import timedelta, datetime
import blowdrycss_settings as settings
__author__ = 'chad nelson'
__project__ = 'blowdrycss'

class Timer(object):
    __doc__ = ' A performance Timer that reports the amount of time it took to run a block of code.\n\n    | **Parameters:**\n\n    | **start** (*time*) -- Time that the program started.\n\n    | **end** (*time*) -- Time that the program ended.\n\n\n    :return: None\n\n    **Example**\n\n    >>> from blowdrycss.timing import Timer\n    >>> timer = Timer()\n    >>> timer.report()\n    Completed 2015-12-14 16:56:08.665080\n    =====================================\n    It took: 0.17296 seconds\n    =====================================\n    >>> timer.reset()       # Resets start time to now.\n    >>> timer.report()\n    Completed 2015-12-14 17:05:12.164030\n    =====================================\n    It took: 1.45249 seconds\n    =====================================\n\n    '

    def __init__(self):
        self.start = time()
        self.end = time()

    @staticmethod
    def seconds_to_string(seconds_elapsed=0.0):
        """ Converts the amount of time elapsed to seconds_elapsed, and returns it as a string.

        :type seconds_elapsed: float
        :param seconds_elapsed: A time() value in units of seconds_elapsed.
        :return: (*str*) -- Returns a string version of the total time elapsed in seconds_elapsed.

        """
        return str(timedelta(seconds=seconds_elapsed).total_seconds())

    @property
    def elapsed(self):
        """ Calculates the amount of time elapsed (delta T) by subtracting start ``time()`` from end ``time()``.

        **Math:** elapsed = delta T = end - start

        :return: (*str*) -- Returns delta T in units of seconds as a string.

        """
        seconds_elapsed = self.end - self.start
        return self.seconds_to_string(seconds_elapsed=seconds_elapsed)

    def print_time(self):
        """ Prints temporal metadata to the console. Including the completion timestamp and delta T in seconds.

        :return: None

        """
        completed_at = '\nCompleted ' + str(datetime.now())
        border = '=' * len(completed_at)
        print(str(completed_at))
        print(str(border))
        print('It took: ' + self.elapsed + 'seconds')
        print(str(border))

    def report(self):
        """ Sets ``end`` time and prints the time elapsed (delta T).  Calls ``print_time()``, and prints
        temporal metadata.

        :return: None

        """
        self.end = time()
        self.print_time()


class LimitTimer(object):
    __doc__ = ' Timer governs when to perform a full and comprehensive run of blowdry.parse().\n\n    .. note::   This is independent of file modification watchdog triggers which only scan the file(s) that changed\n        since the last run.\n\n    ** Why is a LimitTimer needed? **\n\n    *Understanding the Truth Table*\n\n    #. The project only contains two files: File 1  and File 2.\n    #. Each file either contains the CSS class selector \'blue\' or not i.e. set().\n    #. File 2 is modified. Either the class ``blue`` is added or removed i.e. set().\n    #. X means don\'t care whether the file contains blue or set().\n    #. Case #3 is the reason why the LimitTimer is required. The css class selector ``blue``\n       was only defined in File 2. Then blue was removed from File 2. Since blue existed in the\n       combined class_set before File 2 was modified, it will remain in the\n       combined class_set after the union with set(). This is undesirable in Case #3 since ``blue`` is not\n       used anymore in either of the two files. The LimitTimer runs periodically to clear these unused selectors.\n\n    +--------+------------------+------------------+--------------------+-----------------+--------------------+\n    | Case # | File 1 class_set | File 2 class_set | Combined class_set | File 2 modified | Combined class_set |\n    +========+==================+==================+====================+=================+====================+\n    |    1   |       blue       |       blue       |        blue        |      set()      |        blue        |\n    +--------+------------------+------------------+--------------------+-----------------+--------------------+\n    |    2   |       blue       |       set()      |        blue        |        X        |        blue        |\n    +--------+------------------+------------------+--------------------+-----------------+--------------------+\n    |    3   |       set()      |       blue       |        blue        |      set()      |        blue        |\n    +--------+------------------+------------------+--------------------+-----------------+--------------------+\n    |    4   |       set()      |       set()      |        set()       |       blue      |        blue        |\n    +--------+------------------+------------------+--------------------+-----------------+--------------------+\n    |    5   |       set()      |       set()      |        set()       |      set()      |        set()       |\n    +--------+------------------+------------------+--------------------+-----------------+--------------------+\n\n    ** Another reason why the LimitTimer is needed. **\n\n    On windows and mac watchdog on_modify event gets triggered twice on save. In order to prevent a duplicate run\n    for the same change or set of changes this class is implemented. It can also depend on the IDE being\n    used since some IDEs auto-save.\n\n    | **Members:**\n\n    | **time_limit** (*str*) -- Number of seconds that must pass before the limit is exceeded. Default is\n      settings.time_limit.\n\n    | **start_time** (*str*) -- Time that the timer started.\n\n    :return: None\n\n    **Example**\n\n    >>> from blowdrycss.timing import LimitTimer\n    >>> limit_timer = LimitTimer()\n    >>> if limit_timer.limit_exceeded:\n    >>>     print("30 minutes elapses.")\n    >>>     limit_timer.reset()\n    '

    def __init__(self):
        self._time_limit = settings.time_limit
        self.start_time = time()

    @property
    def time_limit(self):
        """ Getter returns ``_time_limit``.

        :return: (*int*) -- Returns ``_time_limit``.

        """
        return self._time_limit

    @time_limit.setter
    def time_limit(self, custom_limit):
        """ Set time_limit in units of seconds.

        :type custom_limit: int
        :param custom_limit: Time limit in units of seconds.

        :return: None

        """
        self._time_limit = custom_limit

    @property
    def limit_exceeded(self):
        """ Compares the current time to the start time, and returns True if ``self.time_limit``
        is exceeded and False otherwise.

        :return: (*bool*) -- Returns True if ``self.time_limit`` is exceeded and False otherwise.

        """
        return time() - self.start_time >= self.time_limit

    def reset(self):
        """ Resets ``self.start`` to the current time.

        :return: None

        """
        self.start_time = time()