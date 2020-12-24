# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/external/qt/compat.py
# Compiled at: 2019-08-19 15:09:29
"""
This module provides utilities to smooth differences between different
Qt APIs
"""
from taurus.external.qt.Qt import QFileDialog
getSaveFileName = getattr(QFileDialog, 'getSaveFileNameAndFilter', QFileDialog.getSaveFileName)
getOpenFileName = getattr(QFileDialog, 'getOpenFileNameAndFilter', QFileDialog.getOpenFileName)
getOpenFileNames = getattr(QFileDialog, 'getOpenFileNamesAndFilter', QFileDialog.getOpenFileNames)
from taurus.external.qt import PYQT5, PYQT4
if PYQT5 or PYQT4:
    PY_OBJECT = 'PyQt_PyObject'
else:
    PY_OBJECT = 'PyObject'
del QFileDialog
del PYQT5
del PYQT4