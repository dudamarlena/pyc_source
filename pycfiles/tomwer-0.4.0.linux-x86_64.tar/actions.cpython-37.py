# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/datawatcher/actions.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 2575 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '18/02/2018'
import tomwer.gui as tomwericons
from silx.gui import qt

class _HistoryAction(qt.QAction):
    __doc__ = '\n    Action displaying the history of finished scans\n    '

    def __init__(self, parent):
        icon = tomwericons.getQIcon('history')
        qt.QAction.__init__(self, icon, 'history', parent)
        self.setCheckable(True)


class _ConfigurationAction(qt.QAction):
    __doc__ = '\n    Action to show the configuration dialog\n    '

    def __init__(self, parent):
        icon = tomwericons.getQIcon('parameters')
        qt.QAction.__init__(self, icon, 'configuration', parent)
        self.setCheckable(True)


class _ObservationAction(qt.QAction):
    __doc__ = '\n    Action to show the observation dialog\n    '

    def __init__(self, parent):
        icon = tomwericons.getQIcon('loop')
        qt.QAction.__init__(self, icon, 'observations', parent)
        self.setCheckable(True)


class _ControlAction(qt.QAction):
    __doc__ = '\n    Action to control the datawatcher (see status and select folder)\n    '

    def __init__(self, parent):
        icon = tomwericons.getQIcon('health')
        qt.QAction.__init__(self, icon, 'control', parent)
        self.setCheckable(True)