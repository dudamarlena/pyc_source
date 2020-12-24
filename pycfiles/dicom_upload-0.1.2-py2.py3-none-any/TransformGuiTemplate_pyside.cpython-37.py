# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/canvas/TransformGuiTemplate_pyside.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 2829 bytes
from PySide import QtCore, QtGui

class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName('Form')
        Form.resize(224, 117)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName('verticalLayout')
        self.translateLabel = QtGui.QLabel(Form)
        self.translateLabel.setObjectName('translateLabel')
        self.verticalLayout.addWidget(self.translateLabel)
        self.rotateLabel = QtGui.QLabel(Form)
        self.rotateLabel.setObjectName('rotateLabel')
        self.verticalLayout.addWidget(self.rotateLabel)
        self.scaleLabel = QtGui.QLabel(Form)
        self.scaleLabel.setObjectName('scaleLabel')
        self.verticalLayout.addWidget(self.scaleLabel)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.mirrorImageBtn = QtGui.QPushButton(Form)
        self.mirrorImageBtn.setToolTip('')
        self.mirrorImageBtn.setObjectName('mirrorImageBtn')
        self.horizontalLayout.addWidget(self.mirrorImageBtn)
        self.reflectImageBtn = QtGui.QPushButton(Form)
        self.reflectImageBtn.setObjectName('reflectImageBtn')
        self.horizontalLayout.addWidget(self.reflectImageBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate('Form', 'Form', None, QtGui.QApplication.UnicodeUTF8))
        self.translateLabel.setText(QtGui.QApplication.translate('Form', 'Translate:', None, QtGui.QApplication.UnicodeUTF8))
        self.rotateLabel.setText(QtGui.QApplication.translate('Form', 'Rotate:', None, QtGui.QApplication.UnicodeUTF8))
        self.scaleLabel.setText(QtGui.QApplication.translate('Form', 'Scale:', None, QtGui.QApplication.UnicodeUTF8))
        self.mirrorImageBtn.setText(QtGui.QApplication.translate('Form', 'Mirror', None, QtGui.QApplication.UnicodeUTF8))
        self.reflectImageBtn.setText(QtGui.QApplication.translate('Form', 'Reflect', None, QtGui.QApplication.UnicodeUTF8))