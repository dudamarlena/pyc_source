# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/navhip/ui/personalization03config.py
# Compiled at: 2020-02-12 12:19:44
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8('Dialog'))
        Dialog.resize(400, 243)
        self.TitleLabel = QtGui.QLabel(Dialog)
        self.TitleLabel.setGeometry(QtCore.QRect(30, 10, 361, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setObjectName(_fromUtf8('TitleLabel'))
        self.IntroLabel = QtGui.QLabel(Dialog)
        self.IntroLabel.setGeometry(QtCore.QRect(20, 50, 351, 61))
        self.IntroLabel.setWordWrap(True)
        self.IntroLabel.setObjectName(_fromUtf8('IntroLabel'))
        self.qwertyButton = QtGui.QRadioButton(Dialog)
        self.qwertyButton.setGeometry(QtCore.QRect(50, 110, 94, 21))
        self.qwertyButton.setChecked(True)
        self.qwertyButton.setObjectName(_fromUtf8('qwertyButton'))
        self.keyboardGroup = QtGui.QButtonGroup(Dialog)
        self.keyboardGroup.setObjectName(_fromUtf8('keyboardGroup'))
        self.keyboardGroup.addButton(self.qwertyButton)
        self.qwertzButton = QtGui.QRadioButton(Dialog)
        self.qwertzButton.setGeometry(QtCore.QRect(50, 140, 94, 21))
        self.qwertzButton.setObjectName(_fromUtf8('qwertzButton'))
        self.keyboardGroup.addButton(self.qwertzButton)
        self.azertyButton = QtGui.QRadioButton(Dialog)
        self.azertyButton.setGeometry(QtCore.QRect(50, 170, 94, 21))
        self.azertyButton.setObjectName(_fromUtf8('azertyButton'))
        self.keyboardGroup.addButton(self.azertyButton)
        self.CancelButton = QtGui.QPushButton(Dialog)
        self.CancelButton.setGeometry(QtCore.QRect(10, 210, 75, 25))
        self.CancelButton.setObjectName(_fromUtf8('CancelButton'))
        self.NextButton = QtGui.QPushButton(Dialog)
        self.NextButton.setGeometry(QtCore.QRect(320, 210, 75, 25))
        self.NextButton.setObjectName(_fromUtf8('NextButton'))
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate('Dialog', 'BTChip setup', None, QtGui.QApplication.UnicodeUTF8))
        self.TitleLabel.setText(QtGui.QApplication.translate('Dialog', 'BTChip setup - config (3/3)', None, QtGui.QApplication.UnicodeUTF8))
        self.IntroLabel.setText(QtGui.QApplication.translate('Dialog', 'Please select your keyboard type to type the second factor confirmation', None, QtGui.QApplication.UnicodeUTF8))
        self.qwertyButton.setText(QtGui.QApplication.translate('Dialog', 'QWERTY', None, QtGui.QApplication.UnicodeUTF8))
        self.qwertzButton.setText(QtGui.QApplication.translate('Dialog', 'QWERTZ', None, QtGui.QApplication.UnicodeUTF8))
        self.azertyButton.setText(QtGui.QApplication.translate('Dialog', 'AZERTY', None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setText(QtGui.QApplication.translate('Dialog', 'Cancel', None, QtGui.QApplication.UnicodeUTF8))
        self.NextButton.setText(QtGui.QApplication.translate('Dialog', 'Next', None, QtGui.QApplication.UnicodeUTF8))
        return