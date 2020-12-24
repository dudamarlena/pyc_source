# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Joseph\Anaconda3-new\Lib\site-packages\pyformulas\_formulas\settimeout.py
# Compiled at: 2018-03-19 17:54:01
# Size of source mod 2**32: 929 bytes


class settimeout:

    def __init__(self, callback, delay, repeat=False, args=(), kwargs={}):
        import pyformulas
        self._thread = pyformulas.thread
        self.callback = callback
        self.delay = delay
        self.repeat = repeat
        self.args = args
        self.kwargs = kwargs
        self.running = True
        self._thread(self._timer)

    def _timer(self):
        import time
        start_time = time.time()
        while 1:
            delta_time = (time.time() - start_time) % self.delay
            time.sleep(self.delay - delta_time)
            self._thread(self.callback, self.args, self.kwargs)
            if not (self.running and self.repeat):
                break

    def stop(self):
        self.running = False

    def start(self):
        if self.running:
            return
        self.running = True
        self._thread(self._timer)