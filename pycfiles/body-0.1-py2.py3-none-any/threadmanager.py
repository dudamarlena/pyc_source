# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/boduch/interface/event/threadmanager.py
# Compiled at: 2009-08-14 17:29:28
from zope.interface import Interface, Attribute

class IThreadManager(Interface):
    threaded = Attribute('True if the thread manager is running in threaded\n    mode.')
    max_threads = Attribute('Maximum number of threads that can run.')

    def get_threaded(cls):
        """Return true if the thread manager is running in threaded mode."""
        pass

    def start_event_thread(cls, queue):
        """Start a new thread of control to run the first handle found in 
        the specified queue."""
        pass


__all__ = [
 'IThreadManager']