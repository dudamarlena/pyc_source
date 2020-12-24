# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/external/qt/QtWebKit.py
# Compiled at: 2019-08-19 15:09:29
"""This module exposes QtWebKit module"""
from . import PYQT5, PYQT4, PYSIDE, PYSIDE2, PythonQtError
if PYQT5:
    from PyQt5.QtWebKit import *
    from PyQt5.QtWebKitWidgets import *
elif PYSIDE2:
    from PySide2.QtWebKit import *
    from PySide2.QtWebKitWidgets import *
elif PYQT4:
    from PyQt4.QtWebKit import *
elif PYSIDE:
    from PySide.QtWebKit import *
else:
    raise PythonQtError('No Qt bindings could be found')