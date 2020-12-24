# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/boduch/interface/event/eventthread.py
# Compiled at: 2009-08-14 17:29:28
"""This module defines the interface for the event thread class."""
from zope.interface import Interface, Attribute

class IEventThread(Interface):
    """The event thread class must store a list of handles to execute
    and must define a run method which actually executes the handles."""
    queue = Attribute('The queue containing handles to be executed.')

    def run(self):
        """Run the thread and in turn, execute all the handlers for the
        event."""
        pass


__all__ = [
 'IEventThread']