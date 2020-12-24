# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\configmltraindata.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 8503 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys, numpy as np
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class configmltraindata(object):
    mltraindataconfig = {}
    pointsetlist = []
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, ConfigMlTrainData):
        ConfigMlTrainData.setObjectName('ConfigMlTrainData')
        ConfigMlTrainData.setFixedSize(400, 260)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ConfigMlTrainData.setWindowIcon(icon)
        self.lblselect = QtWidgets.QLabel(ConfigMlTrainData)
        self.lblselect.setObjectName('lblselect')
        self.lblselect.setGeometry(QtCore.QRect(10, 10, 190, 30))
        self.lwgpoint = QtWidgets.QListWidget(ConfigMlTrainData)
        self.lwgpoint.setObjectName('lwgpoint')
        self.lwgpoint.setGeometry(QtCore.QRect(30, 40, 150, 150))
        self.lwgpoint.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblaugmentation = QtWidgets.QLabel(ConfigMlTrainData)
        self.lblaugmentation.setObjectName('lblaugmentation')
        self.lblaugmentation.setGeometry(QtCore.QRect(210, 10, 190, 30))
        self.cbxbalancetarget = QtWidgets.QCheckBox(ConfigMlTrainData)
        self.cbxbalancetarget.setObjectName('cbxbalancetarget')
        self.cbxbalancetarget.setGeometry(QtCore.QRect(230, 40, 170, 30))
        self.cbxrotatefeature = QtWidgets.QCheckBox(ConfigMlTrainData)
        self.cbxrotatefeature.setObjectName('cbxrotatefeature')
        self.cbxrotatefeature.setGeometry(QtCore.QRect(230, 80, 170, 30))
        self.cbxremovenan = QtWidgets.QCheckBox(ConfigMlTrainData)
        self.cbxremovenan.setObjectName('cbxremovenan')
        self.cbxremovenan.setGeometry(QtCore.QRect(230, 120, 170, 30))
        self.cbxremovezero = QtWidgets.QCheckBox(ConfigMlTrainData)
        self.cbxremovezero.setObjectName('cbxremovezero')
        self.cbxremovezero.setGeometry(QtCore.QRect(230, 160, 170, 30))
        self.btnapply = QtWidgets.QPushButton(ConfigMlTrainData)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(150, 210, 100, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/ok.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ConfigMlTrainData)
        self.msgbox.setObjectName('msgbox')
        _center_x = ConfigMlTrainData.geometry().center().x()
        _center_y = ConfigMlTrainData.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ConfigMlTrainData)
        QtCore.QMetaObject.connectSlotsByName(ConfigMlTrainData)

    def retranslateGUI(self, ConfigMlTrainData):
        self.dialog = ConfigMlTrainData
        _translate = QtCore.QCoreApplication.translate
        ConfigMlTrainData.setWindowTitle(_translate('ConfigMlTrainData', 'ML Training Data Configuration'))
        self.lblselect.setText(_translate('ConfigMlTrainData', 'List of available points:'))
        self.lblaugmentation.setText(_translate('ConfigMlTrainData', 'Augmentation options:'))
        self.cbxbalancetarget.setText(_translate('ConfigMlTrainData', 'Balance target'))
        self.cbxrotatefeature.setText(_translate('ConfigMlTrainData', 'Rotate feature'))
        self.cbxremovenan.setText(_translate('ConfigMlTrainData', 'Remove invariant feature'))
        self.cbxremovezero.setText(_translate('ConfigMlTrainData', 'Remove zero weight'))
        self.btnapply.setText(_translate('ConfigMlTrainData', 'Apply'))
        self.btnapply.clicked.connect(self.clickBtnApply)
        self.cbxbalancetarget.setEnabled(False)
        self.cbxbalancetarget.setChecked(False)
        self.cbxrotatefeature.setEnabled(False)
        self.cbxrotatefeature.setChecked(False)
        self.cbxremovenan.setEnabled(False)
        self.cbxremovenan.setChecked(False)
        self.cbxremovezero.setEnabled(False)
        self.cbxremovezero.setChecked(False)
        self.lwgpoint.clear()
        for key in self.pointsetlist:
            item = QtWidgets.QListWidgetItem(self.lwgpoint)
            item.setText(_translate('ConfigMlTrainData', key))
            if self.mltraindataconfig is not None and len(self.mltraindataconfig.keys()) >= 1 and 'TrainPointSet' in self.mltraindataconfig.keys():
                if key in self.mltraindataconfig['TrainPointSet']:
                    item.setSelected(True)
            self.lwgpoint.addItem(item)

        if self.mltraindataconfig is not None:
            if len(self.mltraindataconfig.keys()) >= 1:
                if 'BalanceTarget_Enabled' in self.mltraindataconfig.keys():
                    self.cbxbalancetarget.setEnabled(self.mltraindataconfig['BalanceTarget_Enabled'])
                if 'BalanceTarget_Checked' in self.mltraindataconfig.keys():
                    self.cbxbalancetarget.setChecked(self.mltraindataconfig['BalanceTarget_Checked'])
                if 'RotateFeature_Enabled' in self.mltraindataconfig.keys():
                    self.cbxrotatefeature.setEnabled(self.mltraindataconfig['RotateFeature_Enabled'])
                if 'RotateFeature_Checked' in self.mltraindataconfig.keys():
                    self.cbxrotatefeature.setChecked(self.mltraindataconfig['RotateFeature_Checked'])
                if 'RemoveInvariantFeature_Enabled' in self.mltraindataconfig.keys():
                    self.cbxremovenan.setEnabled(self.mltraindataconfig['RemoveInvariantFeature_Enabled'])
                if 'RemoveInvariantFeature_Checked' in self.mltraindataconfig.keys():
                    self.cbxremovenan.setChecked(self.mltraindataconfig['RemoveInvariantFeature_Checked'])
                if 'RemoveZeroWeight_Enabled' in self.mltraindataconfig.keys():
                    self.cbxremovezero.setEnabled(self.mltraindataconfig['RemoveZeroWeight_Enabled'])
                if 'RemoveZeroWeight_Checked' in self.mltraindataconfig.keys():
                    self.cbxremovezero.setChecked(self.mltraindataconfig['RemoveZeroWeight_Checked'])

    def clickBtnApply(self):
        self.refreshMsgBox()
        self.mltraindataconfig['TrainPointSet'] = [_p.text() for _p in self.lwgpoint.selectedItems()]
        self.mltraindataconfig['BalanceTarget_Checked'] = self.cbxbalancetarget.isChecked()
        self.mltraindataconfig['RotateFeature_Checked'] = self.cbxrotatefeature.isChecked()
        self.mltraindataconfig['RemoveInvariantFeature_Checked'] = self.cbxremovenan.isChecked()
        self.mltraindataconfig['RemoveZeroWeight_Checked'] = self.cbxremovezero.isChecked()
        self.dialog.close()

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConfigMlTrainData = QtWidgets.QWidget()
    gui = configmltraindata()
    gui.setupGUI(ConfigMlTrainData)
    ConfigMlTrainData.show()
    sys.exit(app.exec_())