# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\index\main.py
# Compiled at: 2013-09-27 04:13:25
from __future__ import division, absolute_import, print_function, unicode_literals
import sys, logging
from PySide import QtCore, QtGui
from .mainframe import MainFrame
app = QtGui.QApplication(sys.argv)

def main(files=None, method=None):
    frame = MainFrame(files, method)
    frame.show()
    res = app.exec_()
    return res