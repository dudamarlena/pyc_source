# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/GraphicsScene/exportDialogTemplate_pyqt5.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2846 bytes
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName('Form')
        Form.resize(241, 367)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName('gridLayout')
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName('label')
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.itemTree = QtWidgets.QTreeWidget(Form)
        self.itemTree.setObjectName('itemTree')
        self.itemTree.headerItem().setText(0, '1')
        self.itemTree.header().setVisible(False)
        self.gridLayout.addWidget(self.itemTree, 1, 0, 1, 3)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName('label_2')
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 3)
        self.formatList = QtWidgets.QListWidget(Form)
        self.formatList.setObjectName('formatList')
        self.gridLayout.addWidget(self.formatList, 3, 0, 1, 3)
        self.exportBtn = QtWidgets.QPushButton(Form)
        self.exportBtn.setObjectName('exportBtn')
        self.gridLayout.addWidget(self.exportBtn, 6, 1, 1, 1)
        self.closeBtn = QtWidgets.QPushButton(Form)
        self.closeBtn.setObjectName('closeBtn')
        self.gridLayout.addWidget(self.closeBtn, 6, 2, 1, 1)
        self.paramTree = ParameterTree(Form)
        self.paramTree.setObjectName('paramTree')
        self.paramTree.headerItem().setText(0, '1')
        self.paramTree.header().setVisible(False)
        self.gridLayout.addWidget(self.paramTree, 5, 0, 1, 3)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName('label_3')
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 3)
        self.copyBtn = QtWidgets.QPushButton(Form)
        self.copyBtn.setObjectName('copyBtn')
        self.gridLayout.addWidget(self.copyBtn, 6, 0, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'Export'))
        self.label.setText(_translate('Form', 'Item to export:'))
        self.label_2.setText(_translate('Form', 'Export format'))
        self.exportBtn.setText(_translate('Form', 'Export'))
        self.closeBtn.setText(_translate('Form', 'Close'))
        self.label_3.setText(_translate('Form', 'Export options'))
        self.copyBtn.setText(_translate('Form', 'Copy'))


from ..parametertree import ParameterTree