# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/util/sleeper.py
# Compiled at: 2018-04-20 03:19:42
import threading

class Sleeper(object):
    """
    Provides a 'sleep' method that sleeps for a number of seconds *unless*
    the notify method is called (from a different thread).
    """

    def __init__(self):
        self.condition = threading.Condition()

    def sleep(self, seconds):
        self.condition.acquire()
        self.condition.wait(seconds)
        self.condition.release()

    def wake(self):
        self.condition.acquire()
        self.condition.notify()
        self.condition.release()