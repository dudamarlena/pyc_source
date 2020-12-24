# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\dlgClipQRange.py
# Compiled at: 2017-08-30 06:00:58
from PyQt5 import QtGui, QtCore, QtWidgets, uic
import pySAXS

class dlgClipQRange(QtWidgets.QDialog):

    def __init__(self, label='', qmin=0.0, qmax=1.0):
        QtWidgets.QDialog.__init__(self)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'dlgClipQRange.ui', self)
        self.labelDataName.setText(label)
        self.qmin.setText(str(qmin))
        self.qmin.setValidator(QtGui.QDoubleValidator())
        self.qmax.setText(str(qmax))
        self.qmax.setValidator(QtGui.QDoubleValidator())

    def getValues(self):
        return (
         float(self.qmin.text()), float(self.qmax.text()))