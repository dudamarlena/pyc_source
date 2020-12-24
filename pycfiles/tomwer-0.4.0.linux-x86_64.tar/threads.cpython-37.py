# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/utils/threads.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 3179 bytes
"""
This module is used to manage observations. Initially on files.
Observations are runned on a thread and run each n seconds.
They are manage by thread and signals
"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '09/01/2019'
import threading, time

class LoopThread(threading.Thread):
    __doc__ = '\n    Thread looping on a defined process, as long not receiving the stopEvent.\n    Wait for `_time_between_loops` between two loops\n    '
    startEvent = threading.Event()
    stopEvent = threading.Event()
    quitEvent = threading.Event()

    def __init__(self, time_between_loops):
        threading.Thread.__init__(self)
        self._time_between_loops = time_between_loops
        self._status = None
        self._last_processing = None

    def run(self):
        threading.Thread.run(self)
        while not (self.quitEvent.isSet() or self._status is None):
            if self._status == 'not running':
                if self.startEvent.isSet():
                    self._status = 'running'
                    self.startEvent.clear()
            else:
                if self._status == 'running':
                    if self.stopEvent.isSet() is True:
                        self.stopEvent.clear()
                        self._status = 'not running'
                if self._status == 'running' and self.should_process():
                    self._last_processing = time.time()
                    self.process()
            time.sleep(0.05)

    def process(self):
        raise NotImplementedError('Pure virtual class')

    def should_process(self):
        if self._last_processing is None:
            return True
        _pass_time_since_last_pro = time.time() - self._last_processing
        return _pass_time_since_last_pro > self._time_between_loops

    def _stop(self):
        pass