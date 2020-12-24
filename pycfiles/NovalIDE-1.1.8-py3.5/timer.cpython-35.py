# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/util/timer.py
# Compiled at: 2019-09-09 02:52:13
# Size of source mod 2**32: 701 bytes
import sched, time, threading

class PyTimer(threading.Thread):
    __doc__ = 'description of class'

    def __init__(self, call_func, *args):
        threading.Thread.__init__(self)
        self._call_func = call_func
        self.schedule = sched.scheduler(time.time, time.sleep)
        self._args = args

    def run(self):
        self.schedule.run()

    def Start(self, interval):
        self.schd = self.schedule.enter(interval, 0, self.WarpCallFunc, ())
        self.start()

    def Stop(self):
        if self.schd in self.schedule.queue:
            self.schedule.cancel(self.schd)

    def WarpCallFunc(self):
        print('callback func')
        self._call_func()