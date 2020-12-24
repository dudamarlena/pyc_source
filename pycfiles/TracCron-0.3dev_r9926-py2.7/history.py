# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/traccron/history.py
# Compiled at: 2011-09-06 05:59:06
"""
Created on 28 oct. 2010

@author: thierry
"""
from trac.core import Component, implements
from traccron.api import IHistoryTaskExecutionStore

class MemoryHistoryStore(Component, IHistoryTaskExecutionStore):
    implements(IHistoryTaskExecutionStore)
    history = []

    def addExecution(self, task, start, end, success):
        """
        Add a new execution of a task into this history
        """
        self.history.append((task, start, end, success))

    def getExecution(self, task=None, fromTime=None, toTime=None, sucess=None):
        """
        Return a iterator on all execution stored. Each element is a tuple
        of (task, start time, end time, success status)
        """
        for h in self.history:
            yield h

    def clear(self):
        self.history[:] = []