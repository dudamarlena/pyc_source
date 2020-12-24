# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/flowchart/FlowchartTemplate_pyqt.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2849 bytes
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
        Form.resize(529, 329)
        self.selInfoWidget = QtGui.QWidget(Form)
        self.selInfoWidget.setGeometry(QtCore.QRect(260, 10, 264, 222))
        self.selInfoWidget.setObjectName(_fromUtf8('selInfoWidget'))
        self.gridLayout = QtGui.QGridLayout(self.selInfoWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8('gridLayout'))
        self.selDescLabel = QtGui.QLabel(self.selInfoWidget)
        self.selDescLabel.setText(_fromUtf8(''))
        self.selDescLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.selDescLabel.setWordWrap(True)
        self.selDescLabel.setObjectName(_fromUtf8('selDescLabel'))
        self.gridLayout.addWidget(self.selDescLabel, 0, 0, 1, 1)
        self.selNameLabel = QtGui.QLabel(self.selInfoWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.selNameLabel.setFont(font)
        self.selNameLabel.setText(_fromUtf8(''))
        self.selNameLabel.setObjectName(_fromUtf8('selNameLabel'))
        self.gridLayout.addWidget(self.selNameLabel, 0, 1, 1, 1)
        self.selectedTree = DataTreeWidget(self.selInfoWidget)
        self.selectedTree.setObjectName(_fromUtf8('selectedTree'))
        self.selectedTree.headerItem().setText(0, _fromUtf8('1'))
        self.gridLayout.addWidget(self.selectedTree, 1, 0, 1, 2)
        self.hoverText = QtGui.QTextEdit(Form)
        self.hoverText.setGeometry(QtCore.QRect(0, 240, 521, 81))
        self.hoverText.setObjectName(_fromUtf8('hoverText'))
        self.view = FlowchartGraphicsView(Form)
        self.view.setGeometry(QtCore.QRect(0, 0, 256, 192))
        self.view.setObjectName(_fromUtf8('view'))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate('Form', 'Form', None))


import flowchart.FlowchartGraphicsView as FlowchartGraphicsView
import widgets.DataTreeWidget as DataTreeWidget