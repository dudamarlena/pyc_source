# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\startGuiSAXSqt.py
# Compiled at: 2017-08-30 10:07:00
"""
execute this file for opening guiSAXS qt (the graphic user interface for pySAXS)
"""
from PyQt5 import QtGui, QtCore, QtWidgets
import os, sys, pySAXS
app = QtWidgets.QApplication(sys.argv)
from pySAXS.guisaxs.qt.mainGuisaxs import showSplash
splash = showSplash()
app.processEvents()
from pySAXS.guisaxs.qt import mainGuisaxs
myapp = mainGuisaxs.mainGuisaxs(splashScreen=splash)
myapp.show()
splash.destroy()
sys.exit(app.exec_())