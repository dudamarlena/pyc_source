# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/flowchart/FlowchartTemplate_pyqt5.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2404 bytes
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName('Form')
        Form.resize(529, 329)
        self.selInfoWidget = QtWidgets.QWidget(Form)
        self.selInfoWidget.setGeometry(QtCore.QRect(260, 10, 264, 222))
        self.selInfoWidget.setObjectName('selInfoWidget')
        self.gridLayout = QtWidgets.QGridLayout(self.selInfoWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName('gridLayout')
        self.selDescLabel = QtWidgets.QLabel(self.selInfoWidget)
        self.selDescLabel.setText('')
        self.selDescLabel.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.selDescLabel.setWordWrap(True)
        self.selDescLabel.setObjectName('selDescLabel')
        self.gridLayout.addWidget(self.selDescLabel, 0, 0, 1, 1)
        self.selNameLabel = QtWidgets.QLabel(self.selInfoWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.selNameLabel.setFont(font)
        self.selNameLabel.setText('')
        self.selNameLabel.setObjectName('selNameLabel')
        self.gridLayout.addWidget(self.selNameLabel, 0, 1, 1, 1)
        self.selectedTree = DataTreeWidget(self.selInfoWidget)
        self.selectedTree.setObjectName('selectedTree')
        self.selectedTree.headerItem().setText(0, '1')
        self.gridLayout.addWidget(self.selectedTree, 1, 0, 1, 2)
        self.hoverText = QtWidgets.QTextEdit(Form)
        self.hoverText.setGeometry(QtCore.QRect(0, 240, 521, 81))
        self.hoverText.setObjectName('hoverText')
        self.view = FlowchartGraphicsView(Form)
        self.view.setGeometry(QtCore.QRect(0, 0, 256, 192))
        self.view.setObjectName('view')
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'Form'))


import widgets.DataTreeWidget as DataTreeWidget
import flowchart.FlowchartGraphicsView as FlowchartGraphicsView