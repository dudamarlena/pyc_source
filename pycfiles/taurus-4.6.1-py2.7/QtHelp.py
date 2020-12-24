# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/external/qt/QtHelp.py
# Compiled at: 2019-08-19 15:09:29
"""QtHelp Wrapper."""
from . import PYQT5
from . import PYQT4
from . import PYSIDE
from . import PYSIDE2
if PYQT5:
    from PyQt5.QtHelp import *
elif PYSIDE2:
    from PySide2.QtHelp import *
elif PYQT4:
    from PyQt4.QtHelp import *
elif PYSIDE:
    from PySide.QtHelp import *
del PYQT4
del PYQT5
del PYSIDE
del PYSIDE2