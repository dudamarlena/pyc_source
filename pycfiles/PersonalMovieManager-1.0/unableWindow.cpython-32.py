# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Personal Movie Manager\pyFiles\unableWindow.py
# Compiled at: 2013-01-17 07:57:03
from PySide import QtCore, QtGui
from .unable import Ui_Dialog as unable_Ui_Dialog
from .nomovie import Ui_Dialog as nomovie_Ui_Dialog
from .noentryselected import Ui_Dialog as noentryselected_Ui_Dialog
from .nointernet import Ui_Dialog as nointernet_Ui_Dialog
import mainWindow, sys

class unable(QtGui.QDialog, mainWindow.Ui_MainWindow):

    def __init__(self, parent=None):
        super(unable, self).__init__(parent)
        self.ui = unable_Ui_Dialog()
        self.ui.setupUi(self)


class noMovie(QtGui.QDialog, mainWindow.Ui_MainWindow):

    def __init__(self, parent=None):
        super(noMovie, self).__init__(parent)
        self.ui = nomovie_Ui_Dialog()
        self.ui.setupUi(self)


class noEntrySelected(QtGui.QDialog, mainWindow.Ui_MainWindow):

    def __init__(self, parent=None):
        super(noEntrySelected, self).__init__(parent)
        self.ui = noentryselected_Ui_Dialog()
        self.ui.setupUi(self)


class noInternet(QtGui.QDialog, mainWindow.Ui_MainWindow):

    def __init__(self, parent=None):
        super(noInternet, self).__init__(parent)
        self.ui = nointernet_Ui_Dialog()
        self.ui.setupUi(self)