# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Personal Movie Manager\pyFiles\about.py
# Compiled at: 2013-01-16 11:30:26
from PySide import QtCore, QtGui

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName('Dialog')
        Dialog.resize(400, 147)
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(9, 9, 381, 131))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName('frame')
        self.label_11 = QtGui.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(15, 11, 351, 41))
        font = QtGui.QFont()
        font.setFamily('Rod')
        font.setPointSize(17)
        font.setWeight(75)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName('label_11')
        self.label_12 = QtGui.QLabel(self.frame)
        self.label_12.setGeometry(QtCore.QRect(20, 51, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName('label_12')
        self.pushButton = QtGui.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(210, 90, 75, 23))
        self.pushButton.setObjectName('pushButton')
        self.help = QtGui.QPushButton(self.frame)
        self.help.setGeometry(QtCore.QRect(100, 90, 75, 23))
        self.help.setObjectName('help')
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL('clicked()'), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate('Dialog', 'About', None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate('Dialog', 'Personal Movie Manager', None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate('Dialog', '© Avirup Kundu', None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate('Dialog', 'Cut!', None, QtGui.QApplication.UnicodeUTF8))
        self.help.setText(QtGui.QApplication.translate('Dialog', 'Help Me!', None, QtGui.QApplication.UnicodeUTF8))
        return