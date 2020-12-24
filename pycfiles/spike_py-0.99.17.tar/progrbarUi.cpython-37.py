# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mad/Documents/spike/spike/util/progrbarUi.py
# Compiled at: 2017-08-31 16:40:33
# Size of source mod 2**32: 2038 bytes
from __future__ import print_function
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8('MainWindow'))
        MainWindow.resize(365, 90)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8('centralwidget'))
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(90, 20, 181, 31))
        self.progressBar.setProperty(_fromUtf8('value'), 24)
        self.progressBar.setObjectName(_fromUtf8('progressBar'))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(290, 20, 62, 16))
        self.label.setObjectName(_fromUtf8('label'))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 365, 22))
        self.menubar.setObjectName(_fromUtf8('menubar'))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8('statusbar'))
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate('MainWindow', 'MainWindow', None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate('MainWindow', 'TextLabel', None, QtGui.QApplication.UnicodeUTF8))