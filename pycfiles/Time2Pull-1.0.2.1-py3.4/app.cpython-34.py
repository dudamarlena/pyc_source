# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/time2pull/app.py
# Compiled at: 2014-06-16 16:02:59
# Size of source mod 2**32: 294 bytes
import sys
from PyQt5 import QtWidgets
from time2pull.window import MainWindow
from time2pull.settings import Settings

def main():
    global app
    global win
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    if not Settings().hide_on_startup:
        win.show()
    app.exec_()