# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.qt/pyqode/qt/QtTest.py
# Compiled at: 2016-12-29 05:31:25
# Size of source mod 2**32: 683 bytes
"""
Provides QtTest and functions

.. warning:: PySide is not supported here, that's why there is not unit tests
    running with PySide.

"""
import os
from pyqode.qt import QT_API
from pyqode.qt import PYQT5_API
from pyqode.qt import PYQT4_API
from pyqode.qt import PYSIDE_API
if os.environ[QT_API] in PYQT5_API:
    from PyQt5.QtTest import QTest
else:
    if os.environ[QT_API] in PYQT4_API:
        from PyQt4.QtTest import QTest as OldQTest

        class QTest(OldQTest):

            @staticmethod
            def qWaitForWindowActive(QWidget):
                OldQTest.qWaitForWindowShown(QWidget)


    elif os.environ[QT_API] in PYSIDE_API:
        raise ImportError('QtTest support is incomplete for PySide')