# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\winpython\python-2.7.10.amd64\lib\site-packages\pySAXS\guisaxs\qt\dlgTextViewui.py
# Compiled at: 2016-02-29 04:24:26
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_dlgTextView(object):

    def setupUi(self, dlgTextView):
        dlgTextView.setObjectName(_fromUtf8('dlgTextView'))
        dlgTextView.setWindowModality(QtCore.Qt.ApplicationModal)
        dlgTextView.resize(400, 382)
        self.verticalLayout = QtGui.QVBoxLayout(dlgTextView)
        self.verticalLayout.setObjectName(_fromUtf8('verticalLayout'))
        self.textBrowser = QtGui.QTextBrowser(dlgTextView)
        self.textBrowser.setObjectName(_fromUtf8('textBrowser'))
        self.verticalLayout.addWidget(self.textBrowser)
        self.buttonBox = QtGui.QDialogButtonBox(dlgTextView)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8('buttonBox'))
        self.verticalLayout.addWidget(self.buttonBox)
        self.retranslateUi(dlgTextView)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8('accepted()')), dlgTextView.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8('rejected()')), dlgTextView.reject)
        QtCore.QMetaObject.connectSlotsByName(dlgTextView)

    def retranslateUi(self, dlgTextView):
        dlgTextView.setWindowTitle(QtGui.QApplication.translate('dlgTextView', 'Dialog', None, QtGui.QApplication.UnicodeUTF8))
        return