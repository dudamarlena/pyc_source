# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/flowchart/FlowchartCtrlTemplate_pyqt5.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2908 bytes
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName('Form')
        Form.resize(217, 499)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName('gridLayout')
        self.loadBtn = QtWidgets.QPushButton(Form)
        self.loadBtn.setObjectName('loadBtn')
        self.gridLayout.addWidget(self.loadBtn, 1, 0, 1, 1)
        self.saveBtn = FeedbackButton(Form)
        self.saveBtn.setObjectName('saveBtn')
        self.gridLayout.addWidget(self.saveBtn, 1, 1, 1, 2)
        self.saveAsBtn = FeedbackButton(Form)
        self.saveAsBtn.setObjectName('saveAsBtn')
        self.gridLayout.addWidget(self.saveAsBtn, 1, 3, 1, 1)
        self.reloadBtn = FeedbackButton(Form)
        self.reloadBtn.setCheckable(False)
        self.reloadBtn.setFlat(False)
        self.reloadBtn.setObjectName('reloadBtn')
        self.gridLayout.addWidget(self.reloadBtn, 4, 0, 1, 2)
        self.showChartBtn = QtWidgets.QPushButton(Form)
        self.showChartBtn.setCheckable(True)
        self.showChartBtn.setObjectName('showChartBtn')
        self.gridLayout.addWidget(self.showChartBtn, 4, 2, 1, 2)
        self.ctrlList = TreeWidget(Form)
        self.ctrlList.setObjectName('ctrlList')
        self.ctrlList.headerItem().setText(0, '1')
        self.ctrlList.header().setVisible(False)
        self.ctrlList.header().setStretchLastSection(False)
        self.gridLayout.addWidget(self.ctrlList, 3, 0, 1, 4)
        self.fileNameLabel = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fileNameLabel.setFont(font)
        self.fileNameLabel.setText('')
        self.fileNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fileNameLabel.setObjectName('fileNameLabel')
        self.gridLayout.addWidget(self.fileNameLabel, 0, 1, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'Form'))
        self.loadBtn.setText(_translate('Form', 'Load..'))
        self.saveBtn.setText(_translate('Form', 'Save'))
        self.saveAsBtn.setText(_translate('Form', 'As..'))
        self.reloadBtn.setText(_translate('Form', 'Reload Libs'))
        self.showChartBtn.setText(_translate('Form', 'Flowchart'))


import widgets.FeedbackButton as FeedbackButton
import widgets.TreeWidget as TreeWidget