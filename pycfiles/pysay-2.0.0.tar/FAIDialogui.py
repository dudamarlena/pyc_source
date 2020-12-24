# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Python27\lib\site-packages\pySAXS\guisaxs\qt\FAIDialogui.py
# Compiled at: 2012-11-20 08:48:43
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_FAIDialog(object):

    def setupUi(self, FAIDialog):
        FAIDialog.setObjectName(_fromUtf8('FAIDialog'))
        FAIDialog.resize(400, 421)
        FAIDialog.setWindowTitle(QtGui.QApplication.translate('FAIDialog', 'Fast Integration dialog box', None, QtGui.QApplication.UnicodeUTF8))
        self.Par = QtGui.QGroupBox(FAIDialog)
        self.Par.setGeometry(QtCore.QRect(10, 10, 381, 61))
        self.Par.setTitle(QtGui.QApplication.translate('FAIDialog', 'Parameters file', None, QtGui.QApplication.UnicodeUTF8))
        self.Par.setObjectName(_fromUtf8('Par'))
        self.paramTxt = QtGui.QLineEdit(self.Par)
        self.paramTxt.setGeometry(QtCore.QRect(20, 20, 251, 20))
        self.paramTxt.setObjectName(_fromUtf8('paramTxt'))
        self.paramFileButton = QtGui.QPushButton(self.Par)
        self.paramFileButton.setGeometry(QtCore.QRect(290, 20, 41, 23))
        self.paramFileButton.setText(QtGui.QApplication.translate('FAIDialog', '...', None, QtGui.QApplication.UnicodeUTF8))
        self.paramFileButton.setObjectName(_fromUtf8('paramFileButton'))
        self.paramViewButton = QtGui.QPushButton(self.Par)
        self.paramViewButton.setEnabled(False)
        self.paramViewButton.setGeometry(QtCore.QRect(334, 20, 41, 23))
        self.paramViewButton.setText(QtGui.QApplication.translate('FAIDialog', 'View', None, QtGui.QApplication.UnicodeUTF8))
        self.paramViewButton.setObjectName(_fromUtf8('paramViewButton'))
        self.groupBox = QtGui.QGroupBox(FAIDialog)
        self.groupBox.setGeometry(QtCore.QRect(10, 80, 381, 221))
        self.groupBox.setTitle(QtGui.QApplication.translate('FAIDialog', 'Data :', None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setObjectName(_fromUtf8('groupBox'))
        self.listWidget = QtGui.QListWidget(self.groupBox)
        self.listWidget.setGeometry(QtCore.QRect(20, 20, 281, 191))
        self.listWidget.setAcceptDrops(True)
        self.listWidget.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.listWidget.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidget.setObjectName(_fromUtf8('listWidget'))
        self.addButton = QtGui.QPushButton(self.groupBox)
        self.addButton.setGeometry(QtCore.QRect(310, 20, 61, 23))
        self.addButton.setText(QtGui.QApplication.translate('FAIDialog', 'Add', None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setObjectName(_fromUtf8('addButton'))
        self.clearButton = QtGui.QPushButton(self.groupBox)
        self.clearButton.setGeometry(QtCore.QRect(310, 80, 61, 23))
        self.clearButton.setText(QtGui.QApplication.translate('FAIDialog', 'Clear list', None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setObjectName(_fromUtf8('clearButton'))
        self.remButton = QtGui.QPushButton(self.groupBox)
        self.remButton.setGeometry(QtCore.QRect(310, 50, 61, 23))
        self.remButton.setText(QtGui.QApplication.translate('FAIDialog', 'remove', None, QtGui.QApplication.UnicodeUTF8))
        self.remButton.setObjectName(_fromUtf8('remButton'))
        self.groupBox_2 = QtGui.QGroupBox(FAIDialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 310, 381, 61))
        self.groupBox_2.setTitle(QtGui.QApplication.translate('FAIDialog', 'Output directory :', None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setObjectName(_fromUtf8('groupBox_2'))
        self.outputDirTxt = QtGui.QLineEdit(self.groupBox_2)
        self.outputDirTxt.setGeometry(QtCore.QRect(20, 20, 301, 20))
        self.outputDirTxt.setObjectName(_fromUtf8('outputDirTxt'))
        self.changeOutputDirButton = QtGui.QPushButton(self.groupBox_2)
        self.changeOutputDirButton.setGeometry(QtCore.QRect(334, 20, 41, 23))
        self.changeOutputDirButton.setText(QtGui.QApplication.translate('FAIDialog', '...', None, QtGui.QApplication.UnicodeUTF8))
        self.changeOutputDirButton.setObjectName(_fromUtf8('changeOutputDirButton'))
        self.progressBar = QtGui.QProgressBar(FAIDialog)
        self.progressBar.setGeometry(QtCore.QRect(140, 380, 241, 23))
        self.progressBar.setProperty('value', 0)
        self.progressBar.setObjectName(_fromUtf8('progressBar'))
        self.RADButton = QtGui.QPushButton(FAIDialog)
        self.RADButton.setGeometry(QtCore.QRect(20, 380, 91, 23))
        self.RADButton.setText(QtGui.QApplication.translate('FAIDialog', 'Radial average', None, QtGui.QApplication.UnicodeUTF8))
        self.RADButton.setObjectName(_fromUtf8('RADButton'))
        self.retranslateUi(FAIDialog)
        QtCore.QObject.connect(self.clearButton, QtCore.SIGNAL(_fromUtf8('clicked()')), self.listWidget.clear)
        QtCore.QObject.connect(self.remButton, QtCore.SIGNAL(_fromUtf8('clicked()')), self.listWidget.clearSelection)
        QtCore.QMetaObject.connectSlotsByName(FAIDialog)
        return

    def retranslateUi(self, FAIDialog):
        pass