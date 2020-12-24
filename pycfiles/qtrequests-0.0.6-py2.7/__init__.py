# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/__init__.py
# Compiled at: 2014-06-16 16:01:45
import server
from PySide import QtGui
s = server.Server()

def setup():
    s.start()
    if QtGui.qApp is None:
        QtGui.QApplication([])
    return


def teardown():
    QtGui.qApp.quit()
    s.stop()