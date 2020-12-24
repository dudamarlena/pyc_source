# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/navhip/ui/personalizationseedbackup02.py
# Compiled at: 2020-02-12 12:19:44
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8('Dialog'))
        Dialog.resize(400, 300)
        self.TitleLabel = QtGui.QLabel(Dialog)
        self.TitleLabel.setGeometry(QtCore.QRect(30, 20, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setObjectName(_fromUtf8('TitleLabel'))
        self.IntroLabel = QtGui.QLabel(Dialog)
        self.IntroLabel.setGeometry(QtCore.QRect(20, 70, 351, 31))
        self.IntroLabel.setWordWrap(True)
        self.IntroLabel.setObjectName(_fromUtf8('IntroLabel'))
        self.NextButton = QtGui.QPushButton(Dialog)
        self.NextButton.setGeometry(QtCore.QRect(320, 270, 75, 25))
        self.NextButton.setObjectName(_fromUtf8('NextButton'))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate('Dialog', 'BTChip setup', None, QtGui.QApplication.UnicodeUTF8))
        self.TitleLabel.setText(QtGui.QApplication.translate('Dialog', 'BTChip setup  - seed backup', None, QtGui.QApplication.UnicodeUTF8))
        self.IntroLabel.setText(QtGui.QApplication.translate('Dialog', 'Please disconnect the dongle then press Next', None, QtGui.QApplication.UnicodeUTF8))
        self.NextButton.setText(QtGui.QApplication.translate('Dialog', 'Next', None, QtGui.QApplication.UnicodeUTF8))
        return