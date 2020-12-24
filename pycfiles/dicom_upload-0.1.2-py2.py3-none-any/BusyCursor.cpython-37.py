# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/BusyCursor.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 596 bytes
from ..Qt import QtGui, QtCore
__all__ = ['BusyCursor']

class BusyCursor(object):
    """BusyCursor"""
    active = []

    def __enter__(self):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        BusyCursor.active.append(self)

    def __exit__(self, *args):
        BusyCursor.active.pop(-1)
        if len(BusyCursor.active) == 0:
            QtGui.QApplication.restoreOverrideCursor()