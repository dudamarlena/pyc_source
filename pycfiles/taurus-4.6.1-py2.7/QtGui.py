# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/external/qt/QtGui.py
# Compiled at: 2019-08-19 15:09:29
"""
Provides QtGui classes and functions.
.. warning:: Contrary to qtpy.QtGui, this module exposes the namespace
    available in ``PyQt4.QtGui``.
    See: http://pyqt.sourceforge.net/Docs/PyQt5/pyqt4_differences.html#qtgui-module
"""
import warnings
from . import PYQT5, PYQT4, PYSIDE, PYSIDE2, PythonQtError
if PYQT5:
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtPrintSupport import *
elif PYSIDE2:
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtPrintSupport import *
elif PYQT4:
    from PyQt4.QtGui import *
elif PYSIDE:
    from PySide.QtGui import *
else:
    raise PythonQtError('No Qt bindings could be found')