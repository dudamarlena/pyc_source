# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/utils/buttons.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 2091 bytes
"""
Button of general usage.
"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '03/10/2018'
from silx.gui import qt
from tomwer.gui import icons

class PadlockButton(qt.QPushButton):
    __doc__ = 'Simple button to define a button with PadLock icons'

    def __init__(self, parent):
        qt.QPushButton.__init__(self, parent)
        self._lockIcon = icons.getQIcon('locked')
        self._unlockIcon = icons.getQIcon('unlocked')
        self.setIcon(self._unlockIcon)
        self.setCheckable(True)
        self.isLocked = self.isChecked
        self.toggled.connect(self._updateDisplay)

    def _updateDisplay(self, checked):
        _icon = self._lockIcon if checked else self._unlockIcon
        self.setIcon(_icon)