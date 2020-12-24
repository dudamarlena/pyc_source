# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/progress.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 1856 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '07/08/2019'
from silx.gui import qt
from est.core.process.progress import Progress

class QProgress(Progress, qt.QObject):
    sigProgress = qt.Signal(int)

    def __init__(self, name):
        assert name is not None
        qt.QObject.__init__(self)
        Progress.__init__(self, name)

    def startProcess(self):
        self.sigProgress.emit(0)

    def setAdvancement(self, value):
        self.sigProgress.emit(value)

    def endProcess(self):
        self.sigProgress.emit(100)