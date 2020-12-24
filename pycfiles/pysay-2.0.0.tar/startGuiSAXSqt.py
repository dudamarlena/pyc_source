# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\startGuiSAXSqt.py
# Compiled at: 2017-08-30 10:07:00
__doc__ = '\nexecute this file for opening guiSAXS qt (the graphic user interface for pySAXS)\n'
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