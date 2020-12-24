# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/FakeWebware/TaskKit/Task.py
# Compiled at: 2006-10-22 17:01:00
from MiscUtils import AbstractError

class Task:
    __module__ = __name__

    def __init__(self):
        """ Subclasses should invoke super for this method. """
        pass

    def run(self):
        """
                Override this method for you own tasks. Long running tasks can periodically 
                use the proceed() method to check if a task should stop. 
                """
        raise AbstractError, self.__class__

    def proceed(self):
        """
                Should this task continue running?
                Should be called periodically by long tasks to check if the system wants them to exit.
                Returns 1 if its OK to continue, 0 if its time to quit
                """
        return self._handle._isRunning

    def handle(self):
        """
                A task is scheduled by wrapping a handler around it. It knows
                everything about the scheduling (periodicity and the like).
                Under normal circumstances you should not need the handler,
                but if you want to write period modifying run() methods, 
                it is useful to have access to the handler. Use it with care.
                """
        return self._handle

    def name(self):
        """
                Returns the unique name under which the task was scheduled.
                """
        return self._name

    def _run(self, handle):
        """
                This is the actual run method for the Task thread. It is a private method which
                should not be overriden.
                """
        self._name = handle.name()
        self._handle = handle
        self.run()
        handle.notifyCompletion()