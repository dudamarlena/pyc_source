# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/_forms/pnl_read_only_ui.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 1461 bytes
from pyqode.qt import QtCore, QtGui, QtWidgets

class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName('Form')
        Form.resize(964, 67)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.lblDescription = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblDescription.sizePolicy().hasHeightForWidth())
        self.lblDescription.setSizePolicy(sizePolicy)
        self.lblDescription.setWordWrap(True)
        self.lblDescription.setObjectName('lblDescription')
        self.horizontalLayout_2.addWidget(self.lblDescription)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_('Form'))
        self.lblDescription.setText(_("<html><head/><body><p>The file you opened is read-only.</p><p>Use &quot;save as&quot; or change the file's permission to edit the document...</p></body></html>"))