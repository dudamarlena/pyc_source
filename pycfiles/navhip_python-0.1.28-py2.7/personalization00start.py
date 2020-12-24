# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/navhip/ui/personalization00start.py
# Compiled at: 2020-02-12 12:19:44
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8('Dialog'))
        Dialog.resize(400, 231)
        self.TitleLabel = QtGui.QLabel(Dialog)
        self.TitleLabel.setGeometry(QtCore.QRect(120, 20, 231, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setObjectName(_fromUtf8('TitleLabel'))
        self.IntroLabel = QtGui.QLabel(Dialog)
        self.IntroLabel.setGeometry(QtCore.QRect(20, 60, 351, 61))
        self.IntroLabel.setWordWrap(True)
        self.IntroLabel.setObjectName(_fromUtf8('IntroLabel'))
        self.NextButton = QtGui.QPushButton(Dialog)
        self.NextButton.setGeometry(QtCore.QRect(310, 200, 75, 25))
        self.NextButton.setObjectName(_fromUtf8('NextButton'))
        self.arningLabel = QtGui.QLabel(Dialog)
        self.arningLabel.setGeometry(QtCore.QRect(20, 120, 351, 81))
        self.arningLabel.setWordWrap(True)
        self.arningLabel.setObjectName(_fromUtf8('arningLabel'))
        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setGeometry(QtCore.QRect(20, 200, 75, 25))
        self.CancelButton.setObjectName(_fromUtf8('CancelButton'))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate('Dialog', 'BTChip setup', None, QtGui.QApplication.UnicodeUTF8))
        self.TitleLabel.setText(QtGui.QApplication.translate('Dialog', 'BTChip setup', None, QtGui.QApplication.UnicodeUTF8))
        self.IntroLabel.setText(QtGui.QApplication.translate('Dialog', "Your BTChip dongle is not set up - you'll be able to create a new wallet, or restore an existing one, and choose your security profile.", None, QtGui.QApplication.UnicodeUTF8))
        self.NextButton.setText(QtGui.QApplication.translate('Dialog', 'Next', None, QtGui.QApplication.UnicodeUTF8))
        self.arningLabel.setText(QtGui.QApplication.translate('Dialog', 'Sensitive information including your dongle PIN will be exchanged during this setup phase - it is recommended to execute it on a secure computer, disconnected from any network, especially if you restore a wallet backup.', None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate('Dialog', 'Cancel', None, QtGui.QApplication.UnicodeUTF8))
        return