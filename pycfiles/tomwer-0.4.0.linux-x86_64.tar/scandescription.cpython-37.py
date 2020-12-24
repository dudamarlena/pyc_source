# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/utils/scandescription.py
# Compiled at: 2020-02-10 09:12:42
# Size of source mod 2**32: 2493 bytes
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '04/02/2020'
from silx.gui import qt
import os

class ScanNameLabel(qt.QWidget):
    __doc__ = 'Scan to display the scan name'

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent=parent)
        self.setLayout(qt.QHBoxLayout())
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        label = qt.QLabel('scan: ', self)
        label.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self.layout().addWidget(label)
        self._scanNameLabel = qt.QLabel('', self)
        self._scanNameLabel.setAlignment(qt.Qt.AlignLeft)
        self._scanNameLabel.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self.layout().addWidget(self._scanNameLabel)
        self.clear()

    def setScan(self, scan):
        if scan is None:
            self.clear()
        else:
            self._scanNameLabel.setText(os.path.basename(scan.path))
            self._scanNameLabel.setToolTip(scan.path)

    def clear(self):
        self._scanNameLabel.setText('-')
        self._scanNameLabel.setToolTip('')