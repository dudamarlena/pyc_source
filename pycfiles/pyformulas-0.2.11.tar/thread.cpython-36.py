# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Joseph\PycharmProjects\pyformulas\_formulas\thread.py
# Compiled at: 2018-05-22 17:48:56
# Size of source mod 2**32: 625 bytes
from threading import Thread

class thread(Thread):

    def __init__(self, function, args=(), kwargs={}, callback=None):
        from threading import Thread
        Thread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.callback = callback
        self.start()

    def run(self):
        self.result = (self.function)(*self.args, **self.kwargs)
        if self.callback is not None:
            if isinstance(self.result, tuple):
                (self.callback)(*self.result)
            else:
                self.callback(self.result)