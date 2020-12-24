# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/clock.py
# Compiled at: 2017-02-16 09:50:19
# Size of source mod 2**32: 576 bytes
from PyQt5 import QtWidgets, QtCore
__all__ = ['DigitalClock']

class DigitalClock(QtWidgets.QLCDNumber):

    def __init__(self, parent=None):
        super(DigitalClock, self).__init__(parent)
        self.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)

    def showTime(self):
        time = QtCore.QTime.currentTime()
        text = time.toString('hh:mm')
        if time.second() % 2 == 0:
            text = text[:2] + ' ' + text[3:]
        self.display(text)