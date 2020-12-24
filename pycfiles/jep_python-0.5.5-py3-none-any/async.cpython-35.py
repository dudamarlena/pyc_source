# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\Work\jep\src\jep-python\build\lib\jep_py\async.py
# Compiled at: 2015-04-11 18:32:26
# Size of source mod 2**32: 1183 bytes
"""Asynchronous reader from file like object, used to read subprocess output without blocking.

This feature is not part of the Python 3.3 standard library. It was requested in PEP 3145 (Asynchronous I/O For subprocess.Popen) but
was deferred and is now available integrated into the standard library's asyncio module (Python 3.4+).

This implementation inspired by http://stefaanlippens.net/python-asynchronous-subprocess-pipe-reading.
"""
import queue, threading

class AsynchronousFileReader(threading.Thread):
    __doc__ = 'Helper class to implement asynchronous reading of a file in a separate thread.\n\n    Pushes read lines on a queue to be consumed in another thread.\n    '

    def __init__(self, file_, queue_=None):
        super().__init__()
        self.file_ = file_
        self.queue_ = queue_ or queue.Queue()

    def run(self):
        """The body of the tread: read lines and put them on the queue."""
        for line in iter(self.file_.readline, ''):
            self.queue_.put(line)

    def eof(self):
        """Check whether there is no more content to expect."""
        return not self.is_alive() and self.queue_.empty()