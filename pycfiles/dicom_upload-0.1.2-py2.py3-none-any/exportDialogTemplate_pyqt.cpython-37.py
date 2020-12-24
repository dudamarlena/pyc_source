# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/GraphicsScene/exportDialogTemplate_pyqt.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 3351 bytes
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)


except AttributeError:

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8('Form'))
        Form.resize(241, 367)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8('gridLayout'))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8('label'))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.itemTree = QtGui.QTreeWidget(Form)
        self.itemTree.setObjectName(_fromUtf8('itemTree'))
        self.itemTree.headerItem().setText(0, _fromUtf8('1'))
        self.itemTree.header().setVisible(False)
        self.gridLayout.addWidget(self.itemTree, 1, 0, 1, 3)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8('label_2'))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 3)
        self.formatList = QtGui.QListWidget(Form)
        self.formatList.setObjectName(_fromUtf8('formatList'))
        self.gridLayout.addWidget(self.formatList, 3, 0, 1, 3)
        self.exportBtn = QtGui.QPushButton(Form)
        self.exportBtn.setObjectName(_fromUtf8('exportBtn'))
        self.gridLayout.addWidget(self.exportBtn, 6, 1, 1, 1)
        self.closeBtn = QtGui.QPushButton(Form)
        self.closeBtn.setObjectName(_fromUtf8('closeBtn'))
        self.gridLayout.addWidget(self.closeBtn, 6, 2, 1, 1)
        self.paramTree = ParameterTree(Form)
        self.paramTree.setObjectName(_fromUtf8('paramTree'))
        self.paramTree.headerItem().setText(0, _fromUtf8('1'))
        self.paramTree.header().setVisible(False)
        self.gridLayout.addWidget(self.paramTree, 5, 0, 1, 3)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8('label_3'))
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 3)
        self.copyBtn = QtGui.QPushButton(Form)
        self.copyBtn.setObjectName(_fromUtf8('copyBtn'))
        self.gridLayout.addWidget(self.copyBtn, 6, 0, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate('Form', 'Export', None))
        self.label.setText(_translate('Form', 'Item to export:', None))
        self.label_2.setText(_translate('Form', 'Export format', None))
        self.exportBtn.setText(_translate('Form', 'Export', None))
        self.closeBtn.setText(_translate('Form', 'Close', None))
        self.label_3.setText(_translate('Form', 'Export options', None))
        self.copyBtn.setText(_translate('Form', 'Copy', None))


from ..parametertree import ParameterTree