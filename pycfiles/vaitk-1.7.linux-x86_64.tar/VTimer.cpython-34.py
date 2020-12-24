# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vaitk/core/VTimer.py
# Compiled at: 2015-05-02 14:14:14
# Size of source mod 2**32: 2063 bytes
from .VCoreApplication import VCoreApplication
from .VObject import VObject
from .VSignal import VSignal
from . import VTimerEvent
import time, threading

class _TimerThread(threading.Thread):

    def __init__(self, timeout, single_shot, callback):
        super(_TimerThread, self).__init__()
        self.daemon = True
        self._timeout = timeout
        self._single_shot = single_shot
        self._callback = callback
        self.stop = threading.Event()

    def run(self):
        while 1:
            time.sleep(self._timeout / 1000.0)
            if self.stop.is_set():
                break
            self._callback()
            if self._single_shot:
                break


class VTimer(VObject):

    def __init__(self):
        super().__init__()
        self._interval = None
        self._single_shot = False
        self.timeout = VSignal(self)
        self._thread = None
        VCoreApplication.vApp.addTimer(self)

    def start(self):
        if self._thread is not None:
            return
        if self._interval is None:
            return
        self._thread = _TimerThread(self._interval, self._single_shot, self._timeout)
        self._thread.start()

    def _timeout(self):
        VCoreApplication.vApp.postEvent(self, VTimerEvent.VTimerEvent())

    def setSingleShot(self, single_shot):
        self._single_shot = single_shot

    def setInterval(self, interval):
        self._interval = interval

    def stop(self):
        if self._thread:
            self._thread.stop.set()
        self._thread = None

    def isRunning(self):
        return self._thread is not None

    def timerEvent(self, event):
        if isinstance(event, VTimerEvent.VTimerEvent):
            self.timeout.emit()

    @staticmethod
    def singleShot(timeout, callback):
        timer = VTimer()
        timer.setInterval(timeout)
        timer.setSingleShot(True)
        timer.timeout.connect(callback)
        timer.start()