# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/ui/create_asset_dialog_UI_pyqt4.py
# Compiled at: 2012-06-08 16:48:07
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_create_asset(object):

    def setupUi(self, create_asset):
        create_asset.setObjectName(_fromUtf8('create_asset'))
        create_asset.setWindowModality(QtCore.Qt.ApplicationModal)
        create_asset.resize(326, 115)
        self.verticalLayout = QtGui.QVBoxLayout(create_asset)
        self.verticalLayout.setObjectName(_fromUtf8('verticalLayout'))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8('gridLayout'))
        self.label_2 = QtGui.QLabel(create_asset)
        self.label_2.setObjectName(_fromUtf8('label_2'))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtGui.QLabel(create_asset)
        self.label.setObjectName(_fromUtf8('label'))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.asset_name_lineEdit = QtGui.QLineEdit(create_asset)
        self.asset_name_lineEdit.setObjectName(_fromUtf8('asset_name_lineEdit'))
        self.gridLayout.addWidget(self.asset_name_lineEdit, 0, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8('horizontalLayout'))
        self.asset_types_comboBox = QtGui.QComboBox(create_asset)
        self.asset_types_comboBox.setEditable(True)
        self.asset_types_comboBox.setObjectName(_fromUtf8('asset_types_comboBox'))
        self.horizontalLayout.addWidget(self.asset_types_comboBox)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(create_asset)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8('buttonBox'))
        self.verticalLayout.addWidget(self.buttonBox)
        self.retranslateUi(create_asset)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8('rejected()')), create_asset.reject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8('accepted()')), create_asset.accept)
        QtCore.QMetaObject.connectSlotsByName(create_asset)

    def retranslateUi(self, create_asset):
        create_asset.setWindowTitle(QtGui.QApplication.translate('create_asset', 'Create Asset', None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate('create_asset', 'Asset Type', None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate('create_asset', 'Asset Name', None, QtGui.QApplication.UnicodeUTF8))
        return