# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.qt/pyqode/qt/QtCore.py
# Compiled at: 2016-12-29 05:31:25
# Size of source mod 2**32: 1137 bytes
"""
Provides QtCore classes and functions.
"""
import os
from pyqode.qt import QT_API
from pyqode.qt import PYQT5_API
from pyqode.qt import PYQT4_API
from pyqode.qt import PYSIDE_API
if os.environ[QT_API] in PYQT5_API:
    from PyQt5.QtCore import *
    from PyQt5.QtCore import pyqtSignal as Signal
    from PyQt5.QtCore import pyqtSlot as Slot
    from PyQt5.QtCore import pyqtProperty as Property
    from PyQt5.QtCore import QT_VERSION_STR as __version__
else:
    if os.environ[QT_API] in PYQT4_API:
        from PyQt4.QtCore import *
        from PyQt4.QtCore import pyqtSignal as Signal
        from PyQt4.QtCore import pyqtSlot as Slot
        from PyQt4.QtCore import pyqtProperty as Property
        from PyQt4.QtGui import QSortFilterProxyModel
        from PyQt4.QtCore import QT_VERSION_STR as __version__
    elif os.environ[QT_API] in PYSIDE_API:
        from PySide.QtCore import *
        from PySide.QtGui import QSortFilterProxyModel
        import PySide.QtCore
        __version__ = PySide.QtCore.__version__