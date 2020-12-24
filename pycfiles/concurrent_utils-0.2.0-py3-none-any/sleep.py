# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/common/threads/sleep.py
# Compiled at: 2011-09-28 13:50:09
import threading

class Sleep:
    """A counterpart of the C{time.sleep()} function. This implementation
        allows some thread to wake up the sleeping thread. 
        """

    def __init__(self):
        self.__cond = threading.Condition()

    def sleep(self, seconds):
        self.__cond.acquire()
        self.__cond.wait(seconds)
        self.__cond.release()

    def wake_up(self):
        self.__cond.acquire()
        self.__cond.notifyAll()
        self.__cond.release()