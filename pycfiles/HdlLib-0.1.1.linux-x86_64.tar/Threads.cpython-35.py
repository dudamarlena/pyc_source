# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/HdlLib/Utilities/Threads.py
# Compiled at: 2017-07-08 08:29:58
# Size of source mod 2**32: 1248 bytes
import threading, logging

def LaunchAsThread(Name='Thread_Unknown', function=None, arglist=[]):
    """Launch the function in a thread and return the thread identificator"""
    thread = threading.Thread(None, function, Name, args=arglist, kwargs={})
    thread.start()
    logging.debug("Thread '{0}' Launched !!!".format(Name))
    return thread


def Wait(Thread):
    if Thread:
        Thread.join()
        logging.debug('*** Thread <{0}> joined ***'.format(Thread.name))


class ThreadFunction(threading.Thread):

    def __init__(self, Function, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.Function = Function
        self.Returned = None
        threading.Thread.__init__(self)

    def run(self):
        self.Returned = self.Function(*self.args, **self.kwargs)