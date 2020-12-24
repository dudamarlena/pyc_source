# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/ui/singletonQApplication.py
# Compiled at: 2012-01-25 12:13:51
import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
from PyQt4 import QtGui

class QApplication(QtGui.QApplication):
    """a singleton QApplication class
    """

    def __new__(cls, *args):
        if cls.instance() is None:
            return QtGui.QApplication(*args)
        else:
            return cls.instance()