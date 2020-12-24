# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\updateml3dcnn.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 43228 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.seismic.analysis import analysis as seis_ays
from cognitivegeo.src.pointset.analysis import analysis as point_ays
from cognitivegeo.src.basic.data import data as basic_data
from cognitivegeo.src.basic.matdict import matdict as basic_mdt
from cognitivegeo.src.basic.video import video as basic_video
from cognitivegeo.src.ml.augmentation import augmentation as ml_aug
from cognitivegeo.src.ml.tfmodel import tfmodel as ml_tfm
from cognitivegeo.src.ml.cnnclassifier3d import cnnclassifier3d as ml_cnn3d
from cognitivegeo.src.gui.viewml3dcnn import viewml3dcnn as gui_viewml3dcnn
from cognitivegeo.src.gui.viewmllearnmat import viewmllearnmat as gui_viewmllearnmat
from cognitivegeo.src.gui.configmltraindata import configmltraindata as gui_configmltraindata
from cognitivegeo.src.vis.messager import messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class updateml3dcnn(object):
    survinfo = {}
    seisdata = {}
    pointsetdata = {}
    rootpath = ''
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    iconpath = os.path.dirname(__file__)
    dialog = None
    modelpath = ''
    modelname = ''
    modelinfo = None
    traindataconfig = {}
    traindataconfig['TrainPointSet'] = []
    traindataconfig['BalanceTarget_Enabled'] = True
    traindataconfig['BalanceTarget_Checked'] = False
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False

    def setupGUI(self, UpdateMl3DCnn):
        UpdateMl3DCnn.setObjectName('UpdateMl3DCnn')
        UpdateMl3DCnn.setFixedSize(800, 540)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UpdateMl3DCnn.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(UpdateMl3DCnn)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(UpdateMl3DCnn)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lbloldsize = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 180, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 180, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 180, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 220, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 220, 40, 30))
        self.lblolddepth = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblolddepth.setObjectName('lblolddepth')
        self.lblolddepth.setGeometry(QtCore.QRect(100, 260, 50, 30))
        self.ldtolddepth = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtolddepth.setObjectName('ldtolddepth')
        self.ldtolddepth.setGeometry(QtCore.QRect(150, 260, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 180, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 180, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 180, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 220, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 220, 40, 30))
        self.lblnewdepth = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblnewdepth.setObjectName('lblnewdepth')
        self.lblnewdepth.setGeometry(QtCore.QRect(300, 260, 50, 30))
        self.ldtnewdepth = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtnewdepth.setObjectName('ldtnewdepth')
        self.ldtnewdepth.setGeometry(QtCore.QRect(350, 260, 40, 30))
        self.lbltarget = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(UpdateMl3DCnn)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 310, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(UpdateMl3DCnn)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(UpdateMl3DCnn)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 130))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(UpdateMl3DCnn)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 140, 180, 130))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblmaskdepth = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblmaskdepth.setObjectName('lblmaskdepth')
        self.lblmaskdepth.setGeometry(QtCore.QRect(500, 360, 50, 30))
        self.ldtmaskdepth = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtmaskdepth.setObjectName('ldtmaskdepth')
        self.ldtmaskdepth.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.lblpooldepth = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblpooldepth.setObjectName('lblpooldepth')
        self.lblpooldepth.setGeometry(QtCore.QRect(700, 360, 50, 30))
        self.ldtpooldepth = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtpooldepth.setObjectName('ldtpooldepth')
        self.ldtpooldepth.setGeometry(QtCore.QRect(750, 360, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(UpdateMl3DCnn)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 360, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 360, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 400, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 400, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 400, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 400, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 440, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 440, 40, 30))
        self.lblfcdropout = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblfcdropout.setObjectName('lblfcdropout')
        self.lblfcdropout.setGeometry(QtCore.QRect(210, 440, 130, 30))
        self.ldtfcdropout = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtfcdropout.setObjectName('ldtfcdropout')
        self.ldtfcdropout.setGeometry(QtCore.QRect(350, 440, 40, 30))
        self.lblsave = QtWidgets.QLabel(UpdateMl3DCnn)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 490, 100, 30))
        self.ldtsave = QtWidgets.QLineEdit(UpdateMl3DCnn)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(110, 490, 210, 30))
        self.btnsave = QtWidgets.QPushButton(UpdateMl3DCnn)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 490, 60, 30))
        self.btnapply = QtWidgets.QPushButton(UpdateMl3DCnn)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 490, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(UpdateMl3DCnn)
        self.msgbox.setObjectName('msgbox')
        _center_x = UpdateMl3DCnn.geometry().center().x()
        _center_y = UpdateMl3DCnn.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(UpdateMl3DCnn)
        QtCore.QMetaObject.connectSlotsByName(UpdateMl3DCnn)

    def retranslateGUI(self, UpdateMl3DCnn):
        self.dialog = UpdateMl3DCnn
        _translate = QtCore.QCoreApplication.translate
        UpdateMl3DCnn.setWindowTitle(_translate('UpdateMl3DCnn', 'Update 3D-CNN'))
        self.lblfrom.setText(_translate('UpdateMl3DCnn', 'Select network:'))
        self.ldtfrom.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('UpdateMl3DCnn', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('UpdateMl3DCnn', 'Training features:'))
        self.lbltarget.setText(_translate('UpdateMl3DCnn', 'Training target:'))
        self.lbloldsize.setText(_translate('UpdateMl3DCnn', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('UpdateMl3DCnn', 'height=\ntime/depth'))
        self.ldtoldheight.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('UpdateMl3DCnn', 'width=\ncrossline'))
        self.ldtoldwidth.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblolddepth.setText(_translate('UpdateMl3DCnn', 'depth=\ninline'))
        self.ldtolddepth.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtolddepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('UpdateMl3DCnn', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('UpdateMl3DCnn', 'height='))
        self.ldtnewheight.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtnewheight.setEnabled(False)
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('UpdateMl3DCnn', 'width='))
        self.ldtnewwidth.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtnewwidth.setEnabled(False)
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewdepth.setText(_translate('UpdateMl3DCnn', 'depth='))
        self.ldtnewdepth.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtnewdepth.setEnabled(False)
        self.ldtnewdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('UpdateMl3DCnn', 'Pre-trained CNN architecture:'))
        self.btnviewnetwork.setText(_translate('UpdateMl3DCnn', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('UpdateMl3DCnn', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblnfclayer.setText(_translate('UpdateMl3DCnn', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtnfclayer.setEnabled(False)
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblmasksize.setText(_translate('UpdateMl3DCnn', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('UpdateMl3DCnn', 'height='))
        self.ldtmaskheight.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('UpdateMl3DCnn', 'width='))
        self.ldtmaskwidth.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskdepth.setText(_translate('UpdateMl3DCnn', 'depth='))
        self.ldtmaskdepth.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtmaskdepth.setEnabled(False)
        self.ldtmaskdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('UpdateMl3DCnn', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('UpdateMl3DCnn', 'height='))
        self.ldtpoolheight.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('UpdateMl3DCnn', 'width='))
        self.ldtpoolwidth.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpooldepth.setText(_translate('UpdateMl3DCnn', 'depth='))
        self.ldtpooldepth.setText(_translate('UpdateMl3DCnn', ''))
        self.ldtpooldepth.setEnabled(False)
        self.ldtpooldepth.setAlignment(QtCore.Qt.AlignCenter)
        self.btnconfigtraindata.setText(_translate('UpdateMl3DCnn', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lblpara.setText(_translate('UpdateMl3DCnn', 'Specify update parameters:'))
        self.lblnepoch.setText(_translate('UpdateMl3DCnn', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('UpdateMl3DCnn', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('UpdateMl3DCnn', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('UpdateMl3DCnn', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('UpdateMl3DCnn', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('UpdateMl3DCnn', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfcdropout.setText(_translate('UpdateMl3DCnn', 'MLP dropout rate:'))
        self.lblfcdropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtfcdropout.setText(_translate('UpdateMl3DCnn', '0.5'))
        self.ldtfcdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('UpdateMl3DCnn', 'Save new-CNN to:'))
        self.ldtsave.setText(_translate('UpdateMl3DCnn', ''))
        self.btnsave.setText(_translate('UpdateMl3DCnn', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('UpdateMl3DCnn', 'Update 3D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnUpdateMl3DCnn)

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.check3DCNNModel(self.modelpath, self.modelname) is True:
            self.modelinfo = ml_tfm.getModelInfo(self.modelpath, self.modelname)
            self.lwgfeature.clear()
            _firstfeature = None
            for f in self.modelinfo['feature_list']:
                item = QtWidgets.QListWidgetItem(self.lwgfeature)
                item.setText(f)
                self.lwgfeature.addItem(item)
                if _firstfeature is None:
                    _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            _height = self.modelinfo['video_size'][0]
            _width = self.modelinfo['video_size'][1]
            _depth = self.modelinfo['video_size'][2]
            self.ldtnewheight.setText(str(_height))
            self.ldtnewwidth.setText(str(_width))
            self.ldtnewdepth.setText(str(_depth))
            self.ldtoldheight.setText(str(3))
            self.ldtoldwidth.setText(str(3))
            self.ldtolddepth.setText(str(3))
            self.cbbtarget.clear()
            self.cbbtarget.addItem(self.modelinfo['target'])
            self.btnviewnetwork.setEnabled(True)
            self.ldtnconvblock.setText(str(self.modelinfo['number_conv_block']))
            self.ldtnfclayer.setText(str(self.modelinfo['number_fc_layer']))
            self.ldtmaskheight.setText(str(self.modelinfo['patch_size'][0]))
            self.ldtmaskwidth.setText(str(self.modelinfo['patch_size'][1]))
            self.ldtmaskdepth.setText(str(self.modelinfo['patch_size'][2]))
            self.ldtpoolheight.setText(str(self.modelinfo['pool_size'][0]))
            self.ldtpoolwidth.setText(str(self.modelinfo['pool_size'][1]))
            self.ldtpooldepth.setText(str(self.modelinfo['pool_size'][2]))
        else:
            self.modelpath = ''
            self.modelname = ''
            self.modelinfo = None
            self.lwgfeature.clear()
            self.ldtoldheight.setText('')
            self.ldtnewheight.setText('')
            self.ldtoldwidth.setText('')
            self.ldtnewwidth.setText('')
            self.ldtolddepth.setText('')
            self.ldtnewdepth.setText('')
            self.cbbtarget.clear()
            self.btnviewnetwork.setEnabled(False)
            self.ldtnconvblock.setText('')
            self.ldtnfclayer.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtmaskdepth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')
            self.ldtpooldepth.setText('')

    def clickBtnFrom(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select CNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def clickBtnViewNetwork(self):
        _viewmlcnn = QtWidgets.QDialog()
        _gui = gui_viewml3dcnn()
        _gui.linestyle = self.linestyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewmlcnn)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewmlcnn.exec()
        _viewmlcnn.show()

    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Save CNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtsave.setText(_file[0])

    def changeLdtNconvblock(self):
        if ml_tfm.check3DCNNModel(self.modelpath, self.modelname) is True:
            _nlayer = self.modelinfo['number_conv_block']
            self.twgnconvblock.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblock.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.modelinfo['number_conv_layer'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblock.setItem(_idx, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.modelinfo['number_conv_feature'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblock.setItem(_idx, 2, item)

        else:
            self.twgnconvblock.setRowCount(0)

    def changeLdtNfclayer(self):
        if ml_tfm.check3DCNNModel(self.modelpath, self.modelname) is True:
            _nlayer = self.modelinfo['number_fc_layer']
            self.twgnfclayer.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnfclayer.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.modelinfo['number_fc_neuron'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnfclayer.setItem(_idx, 1, item)

        else:
            self.twgnfclayer.setRowCount(0)

    def clickBtnConfigTrainData(self):
        _configtraindata = QtWidgets.QDialog()
        _gui = gui_configmltraindata()
        _gui.mltraindataconfig = self.traindataconfig
        _gui.pointsetlist = sorted(self.pointsetdata.keys())
        _gui.setupGUI(_configtraindata)
        _configtraindata.exec()
        self.traindataconfig = _gui.mltraindataconfig
        _configtraindata.show()

    def clickBtnUpdateMl3DCnn(self):
        self.refreshMsgBox()
        if self.checkSurvInfo() is False:
            vis_msg.print('ERROR in UpdateMl3DCnn: No seismic survey available', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 3D-CNN', 'No seismic survey available')
            return
        if ml_tfm.check3DCNNModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in UpdateMl3DCnn: No pre-CNN network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 3D-CNN', 'No pre-CNN network found')
            return
        for f in self.modelinfo['feature_list']:
            if self.checkSeisData(f) is False:
                vis_msg.print(("ERROR in UpdateMl3DCnn: Feature '%s' not found in seismic data" % f), type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Update 3D-CNN', "Feature '" + f + "' not found in seismic data")
                return

        if self.modelinfo['target'] not in self.seisdata.keys():
            vis_msg.print(("ERROR in UpdateMl3DCnn: Target '%s' not found in seismic data" % self.modelinfo['target']), type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 3D-CNN', "Target label '" + self.modelinfo['target'] + ' not found in seismic data')
            return
        _video_height_old = basic_data.str2int(self.ldtoldheight.text())
        _video_width_old = basic_data.str2int(self.ldtoldwidth.text())
        _video_depth_old = basic_data.str2int(self.ldtolddepth.text())
        _video_height_new = basic_data.str2int(self.ldtnewheight.text())
        _video_width_new = basic_data.str2int(self.ldtnewwidth.text())
        _video_depth_new = basic_data.str2int(self.ldtnewdepth.text())
        if _video_height_old is False or _video_width_old is False or _video_depth_old is False or _video_height_new is False or _video_width_new is False or _video_depth_new is False:
            vis_msg.print('ERROR in UpdateMl3DCnn: Non-integer feature size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 3D-CNN', 'Non-integer feature size')
            return
        if _video_height_old < 2 or _video_width_old < 2 or _video_depth_old < 2 or _video_height_new < 2 or _video_width_new < 2 or _video_depth_new < 2:
            vis_msg.print('ERROR in UpdateMl3DCnn: Features are not 3D', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 3D-CNN', 'Features are not 3D')
            return
        _video_height_old = 2 * int(_video_height_old / 2) + 1
        _video_width_old = 2 * int(_video_width_old / 2) + 1
        _video_depth_old = 2 * int(_video_depth_old / 2) + 1
        _features = self.modelinfo['feature_list']
        _target = self.modelinfo['target']
        _nepoch = basic_data.str2int(self.ldtnepoch.text())
        _batchsize = basic_data.str2int(self.ldtbatchsize.text())
        _learning_rate = basic_data.str2float(self.ldtlearnrate.text())
        _dropout_prob_fclayer = basic_data.str2float(self.ldtfcdropout.text())
        if _nepoch is False or _nepoch <= 0:
            vis_msg.print('ERROR in UpdateMl3DCnn: Non-positive epoch number', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 3D-CNN', 'Non-positive epoch number')
            return
        if _batchsize is False or _batchsize <= 0:
            vis_msg.print('ERROR in UpdateMl3DCnn: Non-positive batch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 3D-CNN', 'Non-positive batch size')
            return
        if _learning_rate is False or _learning_rate <= 0:
            vis_msg.print('ERROR in UpdateMl3DCnn: Non-positive learning rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 3D-CNN', 'Non-positive learning rate')
            return
        if _dropout_prob_fclayer is False or _dropout_prob_fclayer <= 0:
            vis_msg.print('ERROR in UpdateMl3DCnn: Negative dropout rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 3D-CNN', 'Negative dropout rate')
            return
        if len(self.ldtsave.text()) < 1:
            vis_msg.print('ERROR in UpdateMl3DCnn: No name specified for new-CNN', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'No name specified for new-CNN')
            return
        _savepath = os.path.dirname(self.ldtsave.text())
        _savename = os.path.splitext(os.path.basename(self.ldtsave.text()))[0]
        _wdinl = int(_video_depth_old / 2)
        _wdxl = int(_video_width_old / 2)
        _wdz = int(_video_height_old / 2)
        _seisinfo = self.survinfo
        print('TrainMl3DCnnFromScratch: Step 1 - Get training samples:')
        _trainpoint = self.traindataconfig['TrainPointSet']
        _traindata = np.zeros([0, 3])
        for _p in _trainpoint:
            if point_ays.checkPoint(self.pointsetdata[_p]):
                _pt = basic_mdt.exportMatDict(self.pointsetdata[_p], ['Inline', 'Crossline', 'Z'])
                _traindata = np.concatenate((_traindata, _pt), axis=0)

        _traindata = seis_ays.removeOutofSurveySample(_traindata, inlstart=(_seisinfo['ILStart'] + _wdinl * _seisinfo['ILStep']),
          inlend=(_seisinfo['ILEnd'] - _wdinl * _seisinfo['ILStep']),
          xlstart=(_seisinfo['XLStart'] + _wdxl * _seisinfo['XLStep']),
          xlend=(_seisinfo['XLEnd'] - _wdxl * _seisinfo['XLStep']),
          zstart=(_seisinfo['ZStart'] + _wdz * _seisinfo['ZStep']),
          zend=(_seisinfo['ZEnd'] - _wdz * _seisinfo['ZStep']))
        if np.shape(_traindata)[0] <= 0:
            vis_msg.print('ERROR in UpdateMl3DCnn: No training sample found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'No training sample found')
            return
        print('TrainMl3DCnn: Step 2 - Retrieve and interpolate videos: (%d, %d, %d) --> (%d, %d, %d)' % (
         _video_height_old, _video_width_old, _video_depth_old,
         _video_height_new, _video_width_new, _video_depth_new))
        _traindict = {}
        for f in _features:
            _seisdata = self.seisdata[f]
            _traindict[f] = seis_ays.retrieveSeisWindowFrom3DMat(_seisdata, _traindata, seisinfo=(self.survinfo), wdinl=_wdinl,
              wdxl=_wdxl,
              wdz=_wdz,
              verbose=False)[:, 3:]

        if _target not in _features:
            _seisdata = self.seisdata[_target]
            _traindict[_target] = seis_ays.retrieveSeisSampleFrom3DMat(_seisdata, _traindata, seisinfo=(self.survinfo), verbose=False)[:, 3:]
        if self.traindataconfig['RemoveInvariantFeature_Checked']:
            for f in _features:
                _traindict = ml_aug.removeInvariantFeature(_traindict, f)
                if basic_mdt.maxDictConstantRow(_traindict) <= 0:
                    print('TrainMl3DCnn: No training sample found')
                    QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'No training sample found')
                    return

        else:
            _traindict[_target] = np.round(_traindict[_target]).astype(int)
            if _video_height_new != _video_height_old or _video_width_new != _video_width_old or _video_depth_new != _video_depth_old:
                for f in _features:
                    _traindict[f] = basic_video.changeVideoSize((_traindict[f]), video_height=_video_height_old,
                      video_width=_video_width_old,
                      video_depth=_video_depth_old,
                      video_height_new=_video_height_new,
                      video_width_new=_video_width_new,
                      video_depth_new=_video_depth_new)

            print('TrainMl3DCnn: A total of %d valid training samples' % basic_mdt.maxDictConstantRow(_traindict))
            print('TrainMl3DCnn: Step 3 - Balance labels')
            if self.traindataconfig['BalanceTarget_Checked']:
                _traindict = ml_aug.balanceLabelbyExtension(_traindict, _target)
                print('TrainMl2DCnnFromScratch: A total of %d training samples after balance' % np.shape(_traindict[_target])[0])
            else:
                print('TrainMl2DCnnFromScratch: No balance applied')
        print('TrainMl3DCnn: Step 3 - Start training')
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Update 3D-CNN')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _cnnlog = ml_cnn3d.update3DCNNClassifier(_traindict, nepoch=_nepoch,
          batchsize=_batchsize,
          learningrate=_learning_rate,
          dropoutprobfclayer=_dropout_prob_fclayer,
          cnn3dpath=(self.modelpath),
          cnn3dname=(self.modelname),
          save2disk=True,
          savepath=_savepath,
          savename=_savename,
          qpgsdlg=_pgsdlg)
        QtWidgets.QMessageBox.information(self.msgbox, 'Update 3D-CNN', 'CNN updated successfully')
        reply = QtWidgets.QMessageBox.question(self.msgbox, 'Update 3D-CNN', 'View learning matrix?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            _viewmllearnmat = QtWidgets.QDialog()
            _gui = gui_viewmllearnmat()
            _gui.learnmat = _cnnlog['learning_curve']
            _gui.linestyle = self.linestyle
            _gui.fontstyle = self.fontstyle
            _gui.setupGUI(_viewmllearnmat)
            _viewmllearnmat.exec()
            _viewmllearnmat.show()

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))

    def checkSurvInfo(self):
        self.refreshMsgBox()
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            return False
        else:
            return True

    def checkSeisData(self, f):
        self.refreshMsgBox()
        return seis_ays.isSeis3DMatConsistentWithSeisInfo(self.seisdata[f], self.survinfo)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UpdateMl3DCnn = QtWidgets.QWidget()
    gui = updateml3dcnn()
    gui.setupGUI(UpdateMl3DCnn)
    UpdateMl3DCnn.show()
    sys.exit(app.exec_())