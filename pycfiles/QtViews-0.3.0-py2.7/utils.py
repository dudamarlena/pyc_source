# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qtviews/utils.py
# Compiled at: 2012-12-03 11:41:28
from PySide import QtCore, QtGui
_test_app = None

def qtapp():
    """
    A QApplication creator for test cases.  QApplication is a single-ton and 
    this provides a safe construction wrapper.
    
    >>> app=qtapp()
    >>> # put test code here
    """
    global _test_app
    _test_app = QtGui.QApplication.instance()
    if _test_app is None:
        _test_app = QtGui.QApplication([])
    return _test_app