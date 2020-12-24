# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/boduch/interface/event/eventthread.py
# Compiled at: 2009-08-14 17:29:28
__doc__ = 'This module defines the interface for the event thread class.'
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