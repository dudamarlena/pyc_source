# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/BusyCursor.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 596 bytes
from ..Qt import QtGui, QtCore
__all__ = ['BusyCursor']

class BusyCursor(object):
    __doc__ = 'Class for displaying a busy mouse cursor during long operations.\n    Usage::\n\n        with pyqtgraph.BusyCursor():\n            doLongOperation()\n\n    May be nested.\n    '
    active = []

    def __enter__(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        BusyCursor.active.append(self)

    def __exit__(self, *args):
        BusyCursor.active.pop(-1)
        if len(BusyCursor.active) == 0:
            QtGui.QApplication.restoreOverrideCursor()