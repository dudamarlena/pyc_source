# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/synctools/axis.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 1978 bytes
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '03/05/2019'
from silx.gui import qt
from tomwer.core.process.reconstruction.axis.params import AxisRP
from tomwer.core.log import TomwerLogger
logger = TomwerLogger(__name__)

class QAxisRP(AxisRP, qt.QObject):
    sigChanged = qt.Signal()
    sigAxisUrlChanged = qt.Signal()

    def __init__(self):
        qt.QObject.__init__(self)
        AxisRP.__init__(self)

    def changed(self):
        self.sigChanged.emit()

    def axis_urls_changed(self):
        self.sigAxisUrlChanged.emit()