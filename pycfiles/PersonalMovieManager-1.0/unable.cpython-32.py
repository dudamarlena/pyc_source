# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Personal Movie Manager\pyFiles\unable.py
# Compiled at: 2013-01-09 08:54:55
from PySide import QtCore, QtGui

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName('Dialog')
        Dialog.resize(400, 145)
        self.frame = QtGui.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(20, 10, 351, 131))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName('frame')
        self.buttonBox = QtGui.QDialogButtonBox(self.frame)
        self.buttonBox.setGeometry(QtCore.QRect(90, 90, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName('buttonBox')
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(28, 20, 301, 61))
        font = QtGui.QFont()
        font.setFamily('Lucida Console')
        font.setPointSize(9)
        font.setWeight(50)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setFrameShape(QtGui.QFrame.Box)
        self.label.setFrameShadow(QtGui.QFrame.Sunken)
        self.label.setWordWrap(True)
        self.label.setObjectName('label')
        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('accepted()'), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL('rejected()'), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate('Dialog', 'Unable  to find Film', None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate('Dialog', 'Unable to find film. To try once more mentioning Year or IMDB id press Cancel. Else press OK to open search page in Web Browser', None, QtGui.QApplication.UnicodeUTF8))
        return