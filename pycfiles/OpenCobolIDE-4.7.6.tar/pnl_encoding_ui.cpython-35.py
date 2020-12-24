# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/_forms/pnl_encoding_ui.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 3481 bytes
from pyqode.qt import QtCore, QtGui, QtWidgets

class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName('Form')
        Form.resize(964, 169)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')
        self.lblDescription = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDescription.sizePolicy().hasHeightForWidth())
        self.lblDescription.setSizePolicy(sizePolicy)
        self.lblDescription.setWordWrap(True)
        self.lblDescription.setObjectName('lblDescription')
        self.verticalLayout.addWidget(self.lblDescription)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName('label')
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxEncodings = EncodingsComboBox(Form)
        self.comboBoxEncodings.setMinimumSize(QtCore.QSize(250, 0))
        self.comboBoxEncodings.setEditable(False)
        self.comboBoxEncodings.setObjectName('comboBoxEncodings')
        self.horizontalLayout.addWidget(self.comboBoxEncodings)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.pushButtonRetry = QtWidgets.QPushButton(Form)
        self.pushButtonRetry.setObjectName('pushButtonRetry')
        self.horizontalLayout_2.addWidget(self.pushButtonRetry)
        self.pushButtonEdit = QtWidgets.QPushButton(Form)
        self.pushButtonEdit.setObjectName('pushButtonEdit')
        self.horizontalLayout_2.addWidget(self.pushButtonEdit)
        self.pushButtonCancel = QtWidgets.QPushButton(Form)
        self.pushButtonCancel.setObjectName('pushButtonCancel')
        self.horizontalLayout_2.addWidget(self.pushButtonCancel)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_('Form'))
        self.lblDescription.setText(_('<html><head/><body><p><span style=" font-weight:600;">%s</span></p><p><span style=" font-size:9pt;">The file you opened has some invalid characters. If you continue editing this file you could corrupt this document. You can also choose another character encoding and try again.</span></p></body></html>'))
        self.label.setText(_('Character Encoding:'))
        self.pushButtonRetry.setText(_('Retry'))
        self.pushButtonEdit.setText(_('Edit Anyway'))
        self.pushButtonCancel.setText(_('Cancel'))


from pyqode.core.widgets.encodings import EncodingsComboBox