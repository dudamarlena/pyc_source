# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/ThreadsafeTimer.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 1551 bytes
from .Qt import QtCore, QtGui

class ThreadsafeTimer(QtCore.QObject):
    __doc__ = '\n    Thread-safe replacement for QTimer.\n    '
    timeout = QtCore.Signal()
    sigTimerStopRequested = QtCore.Signal()
    sigTimerStartRequested = QtCore.Signal(object)

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerFinished)
        self.timer.moveToThread(QtCore.QCoreApplication.instance().thread())
        self.moveToThread(QtCore.QCoreApplication.instance().thread())
        self.sigTimerStopRequested.connect(self.stop, QtCore.Qt.QueuedConnection)
        self.sigTimerStartRequested.connect(self.start, QtCore.Qt.QueuedConnection)

    def start(self, timeout):
        isGuiThread = QtCore.QThread.currentThread() == QtCore.QCoreApplication.instance().thread()
        if isGuiThread:
            self.timer.start(timeout)
        else:
            self.sigTimerStartRequested.emit(timeout)

    def stop(self):
        isGuiThread = QtCore.QThread.currentThread() == QtCore.QCoreApplication.instance().thread()
        if isGuiThread:
            self.timer.stop()
        else:
            self.sigTimerStopRequested.emit()

    def timerFinished(self):
        self.timeout.emit()