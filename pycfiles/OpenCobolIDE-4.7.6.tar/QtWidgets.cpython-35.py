# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.qt/pyqode/qt/QtWidgets.py
# Compiled at: 2016-12-29 05:31:25
# Size of source mod 2**32: 1784 bytes
"""
Provides widget classes and functions.

.. warning:: All PyQt4/PySide gui classes are exposed but when you use
    PyQt5, those classes are not available. Therefore, you should treat/use
    this package as if it was ``PyQt5.QtWidgets`` module.
"""
import os
from pyqode.qt import QT_API
from pyqode.qt import PYQT5_API
from pyqode.qt import PYQT4_API
from pyqode.qt import PYSIDE_API
if os.environ[QT_API] in PYQT5_API:
    from PyQt5.QtWidgets import *
else:
    if os.environ[QT_API] in PYQT4_API:
        from PyQt4.QtGui import *
        from PyQt4.QtGui import QFileDialog as OldFileDialog

        class QFileDialog(OldFileDialog):

            @staticmethod
            def getOpenFileName(parent=None, caption='', directory='', filter='', selectedFilter='', options=OldFileDialog.Options()):
                return OldFileDialog.getOpenFileNameAndFilter(parent, caption, directory, filter, selectedFilter, options)

            @staticmethod
            def getOpenFileNames(parent=None, caption='', directory='', filter='', selectedFilter='', options=OldFileDialog.Options()):
                return OldFileDialog.getOpenFileNamesAndFilter(parent, caption, directory, filter, selectedFilter, options)

            @staticmethod
            def getSaveFileName(parent=None, caption='', directory='', filter='', selectedFilter='', options=OldFileDialog.Options()):
                return OldFileDialog.getSaveFileNameAndFilter(parent, caption, directory, filter, selectedFilter, options)


    elif os.environ[QT_API] in PYSIDE_API:
        from PySide.QtGui import *