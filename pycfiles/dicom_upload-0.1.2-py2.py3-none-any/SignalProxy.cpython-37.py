# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/SignalProxy.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 3844 bytes
from .Qt import QtCore
from .ptime import time
from . import ThreadsafeTimer
import weakref
__all__ = [
 'SignalProxy']

class SignalProxy(QtCore.QObject):
    """SignalProxy"""
    sigDelayed = QtCore.Signal(object)

    def __init__(self, signal, delay=0.3, rateLimit=0, slot=None):
        """Initialization arguments:
        signal - a bound Signal or pyqtSignal instance
        delay - Time (in seconds) to wait for signals to stop before emitting (default 0.3s)
        slot - Optional function to connect sigDelayed to.
        rateLimit - (signals/sec) if greater than 0, this allows signals to stream out at a 
                    steady rate while they are being received.
        """
        QtCore.QObject.__init__(self)
        signal.connect(self.signalReceived)
        self.signal = signal
        self.delay = delay
        self.rateLimit = rateLimit
        self.args = None
        self.timer = ThreadsafeTimer.ThreadsafeTimer()
        self.timer.timeout.connect(self.flush)
        self.block = False
        self.slot = weakref.ref(slot)
        self.lastFlushTime = None
        if slot is not None:
            self.sigDelayed.connect(slot)

    def setDelay(self, delay):
        self.delay = delay

    def signalReceived(self, *args):
        """Received signal. Cancel previous timer and store args to be forwarded later."""
        if self.block:
            return
        self.args = args
        if self.rateLimit == 0:
            self.timer.stop()
            self.timer.start(self.delay * 1000 + 1)
        else:
            now = time()
            if self.lastFlushTime is None:
                leakTime = 0
            else:
                lastFlush = self.lastFlushTime
                leakTime = max(0, lastFlush + 1.0 / self.rateLimit - now)
            self.timer.stop()
            self.timer.start(min(leakTime, self.delay) * 1000 + 1)

    def flush(self):
        """If there is a signal queued up, send it now."""
        if self.args is None or self.block:
            return False
        self.sigDelayed.emit(self.args)
        self.args = None
        self.timer.stop()
        self.lastFlushTime = time()
        return True

    def disconnect(self):
        self.block = True
        try:
            self.signal.disconnect(self.signalReceived)
        except:
            pass

        try:
            self.sigDelayed.disconnect(self.slot())
        except:
            pass


if __name__ == '__main__':
    from .Qt import QtGui
    app = QtGui.QApplication([])
    win = QtGui.QMainWindow()
    spin = QtGui.QSpinBox()
    win.setCentralWidget(spin)
    win.show()

    def fn(*args):
        print('Raw signal:', args)


    def fn2(*args):
        print('Delayed signal:', args)


    spin.valueChanged.connect(fn)
    proxy = SignalProxy((spin.valueChanged), delay=0.5, slot=fn2)