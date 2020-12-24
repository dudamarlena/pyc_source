# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Personal Movie Manager\pyFiles\aboutWindow.py
# Compiled at: 2013-01-17 08:27:47
from PySide import QtCore, QtGui
from .about import Ui_Dialog
import mainWindow, sys, os

class about(QtGui.QDialog, mainWindow.Ui_MainWindow):

    def __init__(self, parent=None):
        super(about, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.connect(self.ui.help, QtCore.SIGNAL('clicked()'), self.help)

    def help(self):
        try:
            os.startfile('README.txt')
        except WindowsError:
            pass