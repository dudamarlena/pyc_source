# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/_forms/dlg_unsaved_files_ui.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 1658 bytes
from pyqode.qt import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName('Dialog')
        Dialog.resize(717, 301)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName('verticalLayout')
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName('label')
        self.verticalLayout.addWidget(self.label)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget.setObjectName('listWidget')
        self.verticalLayout.addWidget(self.listWidget)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Discard | QtWidgets.QDialogButtonBox.SaveAll)
        self.buttonBox.setObjectName('buttonBox')
        self.verticalLayout.addWidget(self.buttonBox)
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_('Dialog'))
        self.label.setText(_('The following files have unsaved changes:'))