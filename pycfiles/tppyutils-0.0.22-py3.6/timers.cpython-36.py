# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpPyUtils/timers.py
# Compiled at: 2020-01-16 14:56:47
# Size of source mod 2**32: 1717 bytes
"""
Module that contains different types of timers
"""
from __future__ import print_function, division, absolute_import
import sys, time

class StopWatch(object):
    __doc__ = '\n    Class that can be used to check how long a command takes to run\n    '
    running = 0

    def __init__(self):
        self.time = None
        self.feedback = True

    def __del__(self):
        self.end()

    def start(self, description='', feedback=True):
        self.feedback = feedback
        if feedback:
            tabs = '\t' * self.running
            sys.utils_log.debug('{}started timer: {}'.format(tabs, description))
        self.time = time.time()
        if feedback:
            self.__class__.running += 1

    def end(self):
        if not self.time:
            return
        else:
            seconds = time.time() - self.time
            self.time = None
            seconds = round(seconds, 2)
            minutes = None
            if seconds > 60:
                minutes, seconds = divmod(seconds, 60)
                seconds = round(seconds, 2)
                minutes = int(minutes)
            if self.feedback:
                tabs = '\t' * self.running
                if minutes is None:
                    sys.utils_log.debug('{}end timer: {} seconds'.format(tabs, seconds))
                else:
                    if minutes > 1:
                        sys.utils_log.debug('{} end timer: {}  minutes, {} seconds'.format(tabs, minutes, seconds))
                    else:
                        if minutes == 1:
                            sys.utils_log.debug('{} end timer: {} minute, {} seconds'.format(tabs, minutes, seconds))
                self.__class__.running -= 1
            return (minutes, seconds)

    def stop(self):
        return self.end()