# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/_forms/popup_open_files_ui.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 2788 bytes
from pyqode.qt import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName('Dialog')
        Dialog.resize(640, 320)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName('gridLayout')
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName('groupBox')
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName('gridLayout_2')
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setObjectName('checkBox')
        self.gridLayout_2.addWidget(self.checkBox, 0, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked | QtWidgets.QAbstractItemView.EditKeyPressed)
        self.tableWidget.setProperty('showDropIndicator', False)
        self.tableWidget.setDragDropOverwriteMode(False)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setCornerButtonEnabled(False)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName('tableWidget')
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(250)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.gridLayout_2.addWidget(self.tableWidget, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_('Dialog'))
        self.groupBox.setTitle(_('Open files'))
        self.checkBox.setText(_('Sort alphabetically'))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_('Filename'))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_('Path'))