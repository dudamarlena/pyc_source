# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/common/StopWatch.py
# Compiled at: 2017-04-23 10:30:41
"""
Class for starting and stopping named timers.

This class is based on a similar java class in cyberaide, and java cog kit.

"""
import time

class StopWatch(object):
    """
    A class to measure times between events.
    """
    timer_start = {}
    timer_end = {}

    @classmethod
    def keys(cls):
        """returns the names of the timers"""
        return list(cls.timer_end.keys())

    @classmethod
    def start(cls, name):
        """
        starts a timer with the given name.

        :param name: the name of the timer
        :type name: string
        """
        cls.timer_start[name] = time.time()

    @classmethod
    def stop(cls, name):
        """
        stops the timer with a given name.

        :param name: the name of the timer
        :type name: string
        """
        cls.timer_end[name] = time.time()

    @classmethod
    def get(cls, name):
        """
        returns the time of the timer.

        :param name: the name of the timer
        :type name: string
        :rtype: the elapsed time
        """
        time_elapsed = cls.timer_end[name] - cls.timer_start[name]
        return time_elapsed

    @classmethod
    def clear(cls):
        """
        clear start and end timer_start
        """
        cls.timer_start.clear()
        cls.timer_end.clear()