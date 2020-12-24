# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/canvas/TransformGuiTemplate_pyqt5.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2586 bytes
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName('Form')
        Form.resize(224, 117)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName('verticalLayout')
        self.translateLabel = QtWidgets.QLabel(Form)
        self.translateLabel.setObjectName('translateLabel')
        self.verticalLayout.addWidget(self.translateLabel)
        self.rotateLabel = QtWidgets.QLabel(Form)
        self.rotateLabel.setObjectName('rotateLabel')
        self.verticalLayout.addWidget(self.rotateLabel)
        self.scaleLabel = QtWidgets.QLabel(Form)
        self.scaleLabel.setObjectName('scaleLabel')
        self.verticalLayout.addWidget(self.scaleLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.mirrorImageBtn = QtWidgets.QPushButton(Form)
        self.mirrorImageBtn.setToolTip('')
        self.mirrorImageBtn.setObjectName('mirrorImageBtn')
        self.horizontalLayout.addWidget(self.mirrorImageBtn)
        self.reflectImageBtn = QtWidgets.QPushButton(Form)
        self.reflectImageBtn.setObjectName('reflectImageBtn')
        self.horizontalLayout.addWidget(self.reflectImageBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate('Form', 'Form'))
        self.translateLabel.setText(_translate('Form', 'Translate:'))
        self.rotateLabel.setText(_translate('Form', 'Rotate:'))
        self.scaleLabel.setText(_translate('Form', 'Scale:'))
        self.mirrorImageBtn.setText(_translate('Form', 'Mirror'))
        self.reflectImageBtn.setText(_translate('Form', 'Reflect'))