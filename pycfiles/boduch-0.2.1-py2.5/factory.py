# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/boduch/event/factory.py
# Compiled at: 2009-08-14 17:29:30
from Queue import Empty
from zope.interface import implements
from boduch.type import Type
from boduch.interface import IEventThread

def build_thread_base_class(threaded=False, processed=False):
    if threaded:
        from threading import Thread
        return Thread
    elif processed:
        from multiprocessing import Process
        return Process


def build_thread_class(threaded=False, processed=False):
    Thread = build_thread_base_class(threaded=threaded, processed=processed)

    class EventThread(Type, Thread):
        """This class extends the core thread class to start a new thread of
        control."""
        implements(IEventThread)

        def __init__(self, queue):
            """Constructor.  Initialize the thread class as well as the event
            queue."""
            Type.__init__(self)
            Thread.__init__(self, name=self.uuid)
            self.queue = queue

        def run(self):
            """Execute each event handler in a new thread."""
            while True:
                try:
                    handle = self.queue.get_nowait()
                    handle.run()
                except Empty:
                    break

    return EventThread


__all__ = [
 'build_thread_base_class', 'build_thread_class']