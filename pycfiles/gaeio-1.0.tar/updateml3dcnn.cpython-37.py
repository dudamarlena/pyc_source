# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\updateml3dcnn.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 43228 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.pointset.analysis as point_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.video as basic_video
import cognitivegeo.src.ml.augmentation as ml_aug
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.cnnclassifier3d as ml_cnn3d
import cognitivegeo.src.gui.viewml3dcnn as gui_viewml3dcnn
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
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

    def clickBtnUpdateMl3DCnn--- This code section failed: ---

 L. 548         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 550         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 551        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in UpdateMl3DCnn: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 552        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 553        44  LOAD_STR                 'Update 3D-CNN'

 L. 554        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 555        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 557        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              check3DCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 558        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in UpdateMl3DCnn: No pre-CNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 559        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 560       100  LOAD_STR                 'Update 3D-CNN'

 L. 561       102  LOAD_STR                 'No pre-CNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 562       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 564       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 565       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 566       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in UpdateMl3DCnn: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    

 L. 567       152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 568       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 569       170  LOAD_STR                 'Update 3D-CNN'

 L. 570       172  LOAD_STR                 "Feature '"
              174  LOAD_FAST                'f'
              176  BINARY_ADD       
              178  LOAD_STR                 "' not found in seismic data"
              180  BINARY_ADD       
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L. 571       186  LOAD_CONST               None
              188  RETURN_VALUE     
              190  JUMP_BACK           124  'to 124'
              192  POP_BLOCK        
            194_0  COME_FROM_LOOP      112  '112'

 L. 572       194  LOAD_FAST                'self'
              196  LOAD_ATTR                modelinfo
              198  LOAD_STR                 'target'
              200  BINARY_SUBSCR    
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                seisdata
              206  LOAD_METHOD              keys
              208  CALL_METHOD_0         0  '0 positional arguments'
              210  COMPARE_OP               not-in
          212_214  POP_JUMP_IF_FALSE   276  'to 276'

 L. 573       216  LOAD_GLOBAL              vis_msg
              218  LOAD_ATTR                print
              220  LOAD_STR                 "ERROR in UpdateMl3DCnn: Target '%s' not found in seismic data"
              222  LOAD_FAST                'self'
              224  LOAD_ATTR                modelinfo
              226  LOAD_STR                 'target'
              228  BINARY_SUBSCR    
              230  BINARY_MODULO    

 L. 574       232  LOAD_STR                 'error'
              234  LOAD_CONST               ('type',)
              236  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              238  POP_TOP          

 L. 575       240  LOAD_GLOBAL              QtWidgets
              242  LOAD_ATTR                QMessageBox
              244  LOAD_METHOD              critical
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                msgbox

 L. 576       250  LOAD_STR                 'Update 3D-CNN'

 L. 577       252  LOAD_STR                 "Target label '"
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                modelinfo
              258  LOAD_STR                 'target'
              260  BINARY_SUBSCR    
              262  BINARY_ADD       
              264  LOAD_STR                 ' not found in seismic data'
              266  BINARY_ADD       
              268  CALL_METHOD_3         3  '3 positional arguments'
              270  POP_TOP          

 L. 578       272  LOAD_CONST               None
              274  RETURN_VALUE     
            276_0  COME_FROM           212  '212'

 L. 580       276  LOAD_GLOBAL              basic_data
              278  LOAD_METHOD              str2int
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                ldtoldheight
              284  LOAD_METHOD              text
              286  CALL_METHOD_0         0  '0 positional arguments'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  STORE_FAST               '_video_height_old'

 L. 581       292  LOAD_GLOBAL              basic_data
              294  LOAD_METHOD              str2int
              296  LOAD_FAST                'self'
              298  LOAD_ATTR                ldtoldwidth
              300  LOAD_METHOD              text
              302  CALL_METHOD_0         0  '0 positional arguments'
              304  CALL_METHOD_1         1  '1 positional argument'
              306  STORE_FAST               '_video_width_old'

 L. 582       308  LOAD_GLOBAL              basic_data
              310  LOAD_METHOD              str2int
              312  LOAD_FAST                'self'
              314  LOAD_ATTR                ldtolddepth
              316  LOAD_METHOD              text
              318  CALL_METHOD_0         0  '0 positional arguments'
              320  CALL_METHOD_1         1  '1 positional argument'
              322  STORE_FAST               '_video_depth_old'

 L. 583       324  LOAD_GLOBAL              basic_data
              326  LOAD_METHOD              str2int
              328  LOAD_FAST                'self'
              330  LOAD_ATTR                ldtnewheight
              332  LOAD_METHOD              text
              334  CALL_METHOD_0         0  '0 positional arguments'
              336  CALL_METHOD_1         1  '1 positional argument'
              338  STORE_FAST               '_video_height_new'

 L. 584       340  LOAD_GLOBAL              basic_data
              342  LOAD_METHOD              str2int
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                ldtnewwidth
              348  LOAD_METHOD              text
              350  CALL_METHOD_0         0  '0 positional arguments'
              352  CALL_METHOD_1         1  '1 positional argument'
              354  STORE_FAST               '_video_width_new'

 L. 585       356  LOAD_GLOBAL              basic_data
              358  LOAD_METHOD              str2int
              360  LOAD_FAST                'self'
              362  LOAD_ATTR                ldtnewdepth
              364  LOAD_METHOD              text
              366  CALL_METHOD_0         0  '0 positional arguments'
              368  CALL_METHOD_1         1  '1 positional argument'
              370  STORE_FAST               '_video_depth_new'

 L. 586       372  LOAD_FAST                '_video_height_old'
              374  LOAD_CONST               False
              376  COMPARE_OP               is
          378_380  POP_JUMP_IF_TRUE    432  'to 432'
              382  LOAD_FAST                '_video_width_old'
              384  LOAD_CONST               False
              386  COMPARE_OP               is
          388_390  POP_JUMP_IF_TRUE    432  'to 432'
              392  LOAD_FAST                '_video_depth_old'
              394  LOAD_CONST               False
              396  COMPARE_OP               is
          398_400  POP_JUMP_IF_TRUE    432  'to 432'

 L. 587       402  LOAD_FAST                '_video_height_new'
              404  LOAD_CONST               False
              406  COMPARE_OP               is
          408_410  POP_JUMP_IF_TRUE    432  'to 432'
              412  LOAD_FAST                '_video_width_new'
              414  LOAD_CONST               False
              416  COMPARE_OP               is
          418_420  POP_JUMP_IF_TRUE    432  'to 432'
              422  LOAD_FAST                '_video_depth_new'
              424  LOAD_CONST               False
              426  COMPARE_OP               is
          428_430  POP_JUMP_IF_FALSE   468  'to 468'
            432_0  COME_FROM           418  '418'
            432_1  COME_FROM           408  '408'
            432_2  COME_FROM           398  '398'
            432_3  COME_FROM           388  '388'
            432_4  COME_FROM           378  '378'

 L. 588       432  LOAD_GLOBAL              vis_msg
              434  LOAD_ATTR                print
              436  LOAD_STR                 'ERROR in UpdateMl3DCnn: Non-integer feature size'
              438  LOAD_STR                 'error'
              440  LOAD_CONST               ('type',)
              442  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              444  POP_TOP          

 L. 589       446  LOAD_GLOBAL              QtWidgets
              448  LOAD_ATTR                QMessageBox
              450  LOAD_METHOD              critical
              452  LOAD_FAST                'self'
              454  LOAD_ATTR                msgbox

 L. 590       456  LOAD_STR                 'Update 3D-CNN'

 L. 591       458  LOAD_STR                 'Non-integer feature size'
              460  CALL_METHOD_3         3  '3 positional arguments'
              462  POP_TOP          

 L. 592       464  LOAD_CONST               None
              466  RETURN_VALUE     
            468_0  COME_FROM           428  '428'

 L. 593       468  LOAD_FAST                '_video_height_old'
              470  LOAD_CONST               2
              472  COMPARE_OP               <
          474_476  POP_JUMP_IF_TRUE    528  'to 528'
              478  LOAD_FAST                '_video_width_old'
              480  LOAD_CONST               2
              482  COMPARE_OP               <
          484_486  POP_JUMP_IF_TRUE    528  'to 528'
              488  LOAD_FAST                '_video_depth_old'
              490  LOAD_CONST               2
              492  COMPARE_OP               <
          494_496  POP_JUMP_IF_TRUE    528  'to 528'

 L. 594       498  LOAD_FAST                '_video_height_new'
              500  LOAD_CONST               2
              502  COMPARE_OP               <
          504_506  POP_JUMP_IF_TRUE    528  'to 528'
              508  LOAD_FAST                '_video_width_new'
              510  LOAD_CONST               2
              512  COMPARE_OP               <
          514_516  POP_JUMP_IF_TRUE    528  'to 528'
              518  LOAD_FAST                '_video_depth_new'
              520  LOAD_CONST               2
              522  COMPARE_OP               <
          524_526  POP_JUMP_IF_FALSE   564  'to 564'
            528_0  COME_FROM           514  '514'
            528_1  COME_FROM           504  '504'
            528_2  COME_FROM           494  '494'
            528_3  COME_FROM           484  '484'
            528_4  COME_FROM           474  '474'

 L. 595       528  LOAD_GLOBAL              vis_msg
              530  LOAD_ATTR                print
              532  LOAD_STR                 'ERROR in UpdateMl3DCnn: Features are not 3D'
              534  LOAD_STR                 'error'
              536  LOAD_CONST               ('type',)
              538  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              540  POP_TOP          

 L. 596       542  LOAD_GLOBAL              QtWidgets
              544  LOAD_ATTR                QMessageBox
              546  LOAD_METHOD              critical
              548  LOAD_FAST                'self'
              550  LOAD_ATTR                msgbox

 L. 597       552  LOAD_STR                 'Update 3D-CNN'

 L. 598       554  LOAD_STR                 'Features are not 3D'
              556  CALL_METHOD_3         3  '3 positional arguments'
              558  POP_TOP          

 L. 599       560  LOAD_CONST               None
              562  RETURN_VALUE     
            564_0  COME_FROM           524  '524'

 L. 601       564  LOAD_CONST               2
              566  LOAD_GLOBAL              int
              568  LOAD_FAST                '_video_height_old'
              570  LOAD_CONST               2
              572  BINARY_TRUE_DIVIDE
              574  CALL_FUNCTION_1       1  '1 positional argument'
              576  BINARY_MULTIPLY  
              578  LOAD_CONST               1
              580  BINARY_ADD       
              582  STORE_FAST               '_video_height_old'

 L. 602       584  LOAD_CONST               2
              586  LOAD_GLOBAL              int
              588  LOAD_FAST                '_video_width_old'
              590  LOAD_CONST               2
              592  BINARY_TRUE_DIVIDE
              594  CALL_FUNCTION_1       1  '1 positional argument'
              596  BINARY_MULTIPLY  
              598  LOAD_CONST               1
              600  BINARY_ADD       
              602  STORE_FAST               '_video_width_old'

 L. 603       604  LOAD_CONST               2
              606  LOAD_GLOBAL              int
              608  LOAD_FAST                '_video_depth_old'
              610  LOAD_CONST               2
              612  BINARY_TRUE_DIVIDE
              614  CALL_FUNCTION_1       1  '1 positional argument'
              616  BINARY_MULTIPLY  
              618  LOAD_CONST               1
              620  BINARY_ADD       
              622  STORE_FAST               '_video_depth_old'

 L. 605       624  LOAD_FAST                'self'
              626  LOAD_ATTR                modelinfo
              628  LOAD_STR                 'feature_list'
              630  BINARY_SUBSCR    
              632  STORE_FAST               '_features'

 L. 606       634  LOAD_FAST                'self'
              636  LOAD_ATTR                modelinfo
              638  LOAD_STR                 'target'
              640  BINARY_SUBSCR    
              642  STORE_FAST               '_target'

 L. 608       644  LOAD_GLOBAL              basic_data
              646  LOAD_METHOD              str2int
              648  LOAD_FAST                'self'
              650  LOAD_ATTR                ldtnepoch
              652  LOAD_METHOD              text
              654  CALL_METHOD_0         0  '0 positional arguments'
              656  CALL_METHOD_1         1  '1 positional argument'
              658  STORE_FAST               '_nepoch'

 L. 609       660  LOAD_GLOBAL              basic_data
              662  LOAD_METHOD              str2int
              664  LOAD_FAST                'self'
              666  LOAD_ATTR                ldtbatchsize
              668  LOAD_METHOD              text
              670  CALL_METHOD_0         0  '0 positional arguments'
              672  CALL_METHOD_1         1  '1 positional argument'
              674  STORE_FAST               '_batchsize'

 L. 610       676  LOAD_GLOBAL              basic_data
              678  LOAD_METHOD              str2float
              680  LOAD_FAST                'self'
              682  LOAD_ATTR                ldtlearnrate
              684  LOAD_METHOD              text
              686  CALL_METHOD_0         0  '0 positional arguments'
              688  CALL_METHOD_1         1  '1 positional argument'
              690  STORE_FAST               '_learning_rate'

 L. 611       692  LOAD_GLOBAL              basic_data
              694  LOAD_METHOD              str2float
              696  LOAD_FAST                'self'
              698  LOAD_ATTR                ldtfcdropout
              700  LOAD_METHOD              text
              702  CALL_METHOD_0         0  '0 positional arguments'
              704  CALL_METHOD_1         1  '1 positional argument'
              706  STORE_FAST               '_dropout_prob_fclayer'

 L. 612       708  LOAD_FAST                '_nepoch'
              710  LOAD_CONST               False
              712  COMPARE_OP               is
          714_716  POP_JUMP_IF_TRUE    728  'to 728'
              718  LOAD_FAST                '_nepoch'
              720  LOAD_CONST               0
              722  COMPARE_OP               <=
          724_726  POP_JUMP_IF_FALSE   764  'to 764'
            728_0  COME_FROM           714  '714'

 L. 613       728  LOAD_GLOBAL              vis_msg
              730  LOAD_ATTR                print
              732  LOAD_STR                 'ERROR in UpdateMl3DCnn: Non-positive epoch number'
              734  LOAD_STR                 'error'
              736  LOAD_CONST               ('type',)
              738  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              740  POP_TOP          

 L. 614       742  LOAD_GLOBAL              QtWidgets
              744  LOAD_ATTR                QMessageBox
              746  LOAD_METHOD              critical
              748  LOAD_FAST                'self'
              750  LOAD_ATTR                msgbox

 L. 615       752  LOAD_STR                 'Update 3D-CNN'

 L. 616       754  LOAD_STR                 'Non-positive epoch number'
              756  CALL_METHOD_3         3  '3 positional arguments'
              758  POP_TOP          

 L. 617       760  LOAD_CONST               None
              762  RETURN_VALUE     
            764_0  COME_FROM           724  '724'

 L. 618       764  LOAD_FAST                '_batchsize'
              766  LOAD_CONST               False
              768  COMPARE_OP               is
          770_772  POP_JUMP_IF_TRUE    784  'to 784'
              774  LOAD_FAST                '_batchsize'
              776  LOAD_CONST               0
              778  COMPARE_OP               <=
          780_782  POP_JUMP_IF_FALSE   820  'to 820'
            784_0  COME_FROM           770  '770'

 L. 619       784  LOAD_GLOBAL              vis_msg
              786  LOAD_ATTR                print
              788  LOAD_STR                 'ERROR in UpdateMl3DCnn: Non-positive batch size'
              790  LOAD_STR                 'error'
              792  LOAD_CONST               ('type',)
              794  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              796  POP_TOP          

 L. 620       798  LOAD_GLOBAL              QtWidgets
              800  LOAD_ATTR                QMessageBox
              802  LOAD_METHOD              critical
              804  LOAD_FAST                'self'
              806  LOAD_ATTR                msgbox

 L. 621       808  LOAD_STR                 'Update 3D-CNN'

 L. 622       810  LOAD_STR                 'Non-positive batch size'
              812  CALL_METHOD_3         3  '3 positional arguments'
              814  POP_TOP          

 L. 623       816  LOAD_CONST               None
              818  RETURN_VALUE     
            820_0  COME_FROM           780  '780'

 L. 624       820  LOAD_FAST                '_learning_rate'
              822  LOAD_CONST               False
              824  COMPARE_OP               is
          826_828  POP_JUMP_IF_TRUE    840  'to 840'
              830  LOAD_FAST                '_learning_rate'
              832  LOAD_CONST               0
              834  COMPARE_OP               <=
          836_838  POP_JUMP_IF_FALSE   876  'to 876'
            840_0  COME_FROM           826  '826'

 L. 625       840  LOAD_GLOBAL              vis_msg
              842  LOAD_ATTR                print
              844  LOAD_STR                 'ERROR in UpdateMl3DCnn: Non-positive learning rate'
              846  LOAD_STR                 'error'
              848  LOAD_CONST               ('type',)
              850  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              852  POP_TOP          

 L. 626       854  LOAD_GLOBAL              QtWidgets
              856  LOAD_ATTR                QMessageBox
              858  LOAD_METHOD              critical
              860  LOAD_FAST                'self'
              862  LOAD_ATTR                msgbox

 L. 627       864  LOAD_STR                 'Update 3D-CNN'

 L. 628       866  LOAD_STR                 'Non-positive learning rate'
              868  CALL_METHOD_3         3  '3 positional arguments'
              870  POP_TOP          

 L. 629       872  LOAD_CONST               None
              874  RETURN_VALUE     
            876_0  COME_FROM           836  '836'

 L. 630       876  LOAD_FAST                '_dropout_prob_fclayer'
              878  LOAD_CONST               False
              880  COMPARE_OP               is
          882_884  POP_JUMP_IF_TRUE    896  'to 896'
              886  LOAD_FAST                '_dropout_prob_fclayer'
              888  LOAD_CONST               0
              890  COMPARE_OP               <=
          892_894  POP_JUMP_IF_FALSE   932  'to 932'
            896_0  COME_FROM           882  '882'

 L. 631       896  LOAD_GLOBAL              vis_msg
              898  LOAD_ATTR                print
              900  LOAD_STR                 'ERROR in UpdateMl3DCnn: Negative dropout rate'
              902  LOAD_STR                 'error'
              904  LOAD_CONST               ('type',)
              906  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              908  POP_TOP          

 L. 632       910  LOAD_GLOBAL              QtWidgets
              912  LOAD_ATTR                QMessageBox
              914  LOAD_METHOD              critical
              916  LOAD_FAST                'self'
              918  LOAD_ATTR                msgbox

 L. 633       920  LOAD_STR                 'Update 3D-CNN'

 L. 634       922  LOAD_STR                 'Negative dropout rate'
              924  CALL_METHOD_3         3  '3 positional arguments'
              926  POP_TOP          

 L. 635       928  LOAD_CONST               None
              930  RETURN_VALUE     
            932_0  COME_FROM           892  '892'

 L. 637       932  LOAD_GLOBAL              len
              934  LOAD_FAST                'self'
              936  LOAD_ATTR                ldtsave
              938  LOAD_METHOD              text
              940  CALL_METHOD_0         0  '0 positional arguments'
              942  CALL_FUNCTION_1       1  '1 positional argument'
              944  LOAD_CONST               1
              946  COMPARE_OP               <
          948_950  POP_JUMP_IF_FALSE   988  'to 988'

 L. 638       952  LOAD_GLOBAL              vis_msg
              954  LOAD_ATTR                print
              956  LOAD_STR                 'ERROR in UpdateMl3DCnn: No name specified for new-CNN'
              958  LOAD_STR                 'error'
              960  LOAD_CONST               ('type',)
              962  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              964  POP_TOP          

 L. 639       966  LOAD_GLOBAL              QtWidgets
              968  LOAD_ATTR                QMessageBox
              970  LOAD_METHOD              critical
              972  LOAD_FAST                'self'
              974  LOAD_ATTR                msgbox

 L. 640       976  LOAD_STR                 'Train 3D-CNN'

 L. 641       978  LOAD_STR                 'No name specified for new-CNN'
              980  CALL_METHOD_3         3  '3 positional arguments'
              982  POP_TOP          

 L. 642       984  LOAD_CONST               None
              986  RETURN_VALUE     
            988_0  COME_FROM           948  '948'

 L. 643       988  LOAD_GLOBAL              os
              990  LOAD_ATTR                path
              992  LOAD_METHOD              dirname
              994  LOAD_FAST                'self'
              996  LOAD_ATTR                ldtsave
              998  LOAD_METHOD              text
             1000  CALL_METHOD_0         0  '0 positional arguments'
             1002  CALL_METHOD_1         1  '1 positional argument'
             1004  STORE_FAST               '_savepath'

 L. 644      1006  LOAD_GLOBAL              os
             1008  LOAD_ATTR                path
             1010  LOAD_METHOD              splitext
             1012  LOAD_GLOBAL              os
             1014  LOAD_ATTR                path
             1016  LOAD_METHOD              basename
             1018  LOAD_FAST                'self'
             1020  LOAD_ATTR                ldtsave
             1022  LOAD_METHOD              text
             1024  CALL_METHOD_0         0  '0 positional arguments'
             1026  CALL_METHOD_1         1  '1 positional argument'
             1028  CALL_METHOD_1         1  '1 positional argument'
             1030  LOAD_CONST               0
             1032  BINARY_SUBSCR    
             1034  STORE_FAST               '_savename'

 L. 646      1036  LOAD_GLOBAL              int
             1038  LOAD_FAST                '_video_depth_old'
             1040  LOAD_CONST               2
             1042  BINARY_TRUE_DIVIDE
             1044  CALL_FUNCTION_1       1  '1 positional argument'
             1046  STORE_FAST               '_wdinl'

 L. 647      1048  LOAD_GLOBAL              int
             1050  LOAD_FAST                '_video_width_old'
             1052  LOAD_CONST               2
             1054  BINARY_TRUE_DIVIDE
             1056  CALL_FUNCTION_1       1  '1 positional argument'
             1058  STORE_FAST               '_wdxl'

 L. 648      1060  LOAD_GLOBAL              int
             1062  LOAD_FAST                '_video_height_old'
             1064  LOAD_CONST               2
             1066  BINARY_TRUE_DIVIDE
             1068  CALL_FUNCTION_1       1  '1 positional argument'
             1070  STORE_FAST               '_wdz'

 L. 650      1072  LOAD_FAST                'self'
             1074  LOAD_ATTR                survinfo
             1076  STORE_FAST               '_seisinfo'

 L. 652      1078  LOAD_GLOBAL              print
             1080  LOAD_STR                 'TrainMl3DCnnFromScratch: Step 1 - Get training samples:'
             1082  CALL_FUNCTION_1       1  '1 positional argument'
             1084  POP_TOP          

 L. 653      1086  LOAD_FAST                'self'
             1088  LOAD_ATTR                traindataconfig
             1090  LOAD_STR                 'TrainPointSet'
             1092  BINARY_SUBSCR    
             1094  STORE_FAST               '_trainpoint'

 L. 654      1096  LOAD_GLOBAL              np
             1098  LOAD_METHOD              zeros
             1100  LOAD_CONST               0
             1102  LOAD_CONST               3
             1104  BUILD_LIST_2          2 
             1106  CALL_METHOD_1         1  '1 positional argument'
             1108  STORE_FAST               '_traindata'

 L. 655      1110  SETUP_LOOP         1186  'to 1186'
             1112  LOAD_FAST                '_trainpoint'
             1114  GET_ITER         
           1116_0  COME_FROM          1134  '1134'
             1116  FOR_ITER           1184  'to 1184'
             1118  STORE_FAST               '_p'

 L. 656      1120  LOAD_GLOBAL              point_ays
             1122  LOAD_METHOD              checkPoint
             1124  LOAD_FAST                'self'
             1126  LOAD_ATTR                pointsetdata
             1128  LOAD_FAST                '_p'
             1130  BINARY_SUBSCR    
             1132  CALL_METHOD_1         1  '1 positional argument'
         1134_1136  POP_JUMP_IF_FALSE  1116  'to 1116'

 L. 657      1138  LOAD_GLOBAL              basic_mdt
             1140  LOAD_METHOD              exportMatDict
             1142  LOAD_FAST                'self'
             1144  LOAD_ATTR                pointsetdata
             1146  LOAD_FAST                '_p'
             1148  BINARY_SUBSCR    
             1150  LOAD_STR                 'Inline'
             1152  LOAD_STR                 'Crossline'
             1154  LOAD_STR                 'Z'
             1156  BUILD_LIST_3          3 
             1158  CALL_METHOD_2         2  '2 positional arguments'
             1160  STORE_FAST               '_pt'

 L. 658      1162  LOAD_GLOBAL              np
             1164  LOAD_ATTR                concatenate
             1166  LOAD_FAST                '_traindata'
             1168  LOAD_FAST                '_pt'
             1170  BUILD_TUPLE_2         2 
             1172  LOAD_CONST               0
             1174  LOAD_CONST               ('axis',)
             1176  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1178  STORE_FAST               '_traindata'
         1180_1182  JUMP_BACK          1116  'to 1116'
             1184  POP_BLOCK        
           1186_0  COME_FROM_LOOP     1110  '1110'

 L. 659      1186  LOAD_GLOBAL              seis_ays
             1188  LOAD_ATTR                removeOutofSurveySample
             1190  LOAD_FAST                '_traindata'

 L. 660      1192  LOAD_FAST                '_seisinfo'
             1194  LOAD_STR                 'ILStart'
             1196  BINARY_SUBSCR    
             1198  LOAD_FAST                '_wdinl'
             1200  LOAD_FAST                '_seisinfo'
             1202  LOAD_STR                 'ILStep'
             1204  BINARY_SUBSCR    
             1206  BINARY_MULTIPLY  
             1208  BINARY_ADD       

 L. 661      1210  LOAD_FAST                '_seisinfo'
             1212  LOAD_STR                 'ILEnd'
             1214  BINARY_SUBSCR    
             1216  LOAD_FAST                '_wdinl'
             1218  LOAD_FAST                '_seisinfo'
             1220  LOAD_STR                 'ILStep'
             1222  BINARY_SUBSCR    
             1224  BINARY_MULTIPLY  
             1226  BINARY_SUBTRACT  

 L. 662      1228  LOAD_FAST                '_seisinfo'
             1230  LOAD_STR                 'XLStart'
             1232  BINARY_SUBSCR    
             1234  LOAD_FAST                '_wdxl'
             1236  LOAD_FAST                '_seisinfo'
             1238  LOAD_STR                 'XLStep'
             1240  BINARY_SUBSCR    
             1242  BINARY_MULTIPLY  
             1244  BINARY_ADD       

 L. 663      1246  LOAD_FAST                '_seisinfo'
             1248  LOAD_STR                 'XLEnd'
             1250  BINARY_SUBSCR    
             1252  LOAD_FAST                '_wdxl'
             1254  LOAD_FAST                '_seisinfo'
             1256  LOAD_STR                 'XLStep'
             1258  BINARY_SUBSCR    
             1260  BINARY_MULTIPLY  
             1262  BINARY_SUBTRACT  

 L. 664      1264  LOAD_FAST                '_seisinfo'
             1266  LOAD_STR                 'ZStart'
             1268  BINARY_SUBSCR    
             1270  LOAD_FAST                '_wdz'
             1272  LOAD_FAST                '_seisinfo'
             1274  LOAD_STR                 'ZStep'
             1276  BINARY_SUBSCR    
             1278  BINARY_MULTIPLY  
             1280  BINARY_ADD       

 L. 665      1282  LOAD_FAST                '_seisinfo'
             1284  LOAD_STR                 'ZEnd'
             1286  BINARY_SUBSCR    
             1288  LOAD_FAST                '_wdz'
             1290  LOAD_FAST                '_seisinfo'
             1292  LOAD_STR                 'ZStep'
             1294  BINARY_SUBSCR    
             1296  BINARY_MULTIPLY  
             1298  BINARY_SUBTRACT  
             1300  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1302  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1304  STORE_FAST               '_traindata'

 L. 668      1306  LOAD_GLOBAL              np
             1308  LOAD_METHOD              shape
             1310  LOAD_FAST                '_traindata'
             1312  CALL_METHOD_1         1  '1 positional argument'
             1314  LOAD_CONST               0
             1316  BINARY_SUBSCR    
             1318  LOAD_CONST               0
             1320  COMPARE_OP               <=
         1322_1324  POP_JUMP_IF_FALSE  1362  'to 1362'

 L. 669      1326  LOAD_GLOBAL              vis_msg
             1328  LOAD_ATTR                print
             1330  LOAD_STR                 'ERROR in UpdateMl3DCnn: No training sample found'
             1332  LOAD_STR                 'error'
             1334  LOAD_CONST               ('type',)
             1336  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1338  POP_TOP          

 L. 670      1340  LOAD_GLOBAL              QtWidgets
             1342  LOAD_ATTR                QMessageBox
             1344  LOAD_METHOD              critical
             1346  LOAD_FAST                'self'
             1348  LOAD_ATTR                msgbox

 L. 671      1350  LOAD_STR                 'Train 3D-CNN'

 L. 672      1352  LOAD_STR                 'No training sample found'
             1354  CALL_METHOD_3         3  '3 positional arguments'
             1356  POP_TOP          

 L. 673      1358  LOAD_CONST               None
             1360  RETURN_VALUE     
           1362_0  COME_FROM          1322  '1322'

 L. 676      1362  LOAD_GLOBAL              print
             1364  LOAD_STR                 'TrainMl3DCnn: Step 2 - Retrieve and interpolate videos: (%d, %d, %d) --> (%d, %d, %d)'

 L. 677      1366  LOAD_FAST                '_video_height_old'
             1368  LOAD_FAST                '_video_width_old'
             1370  LOAD_FAST                '_video_depth_old'

 L. 678      1372  LOAD_FAST                '_video_height_new'
             1374  LOAD_FAST                '_video_width_new'
             1376  LOAD_FAST                '_video_depth_new'
             1378  BUILD_TUPLE_6         6 
             1380  BINARY_MODULO    
             1382  CALL_FUNCTION_1       1  '1 positional argument'
             1384  POP_TOP          

 L. 679      1386  BUILD_MAP_0           0 
             1388  STORE_FAST               '_traindict'

 L. 680      1390  SETUP_LOOP         1462  'to 1462'
             1392  LOAD_FAST                '_features'
             1394  GET_ITER         
             1396  FOR_ITER           1460  'to 1460'
             1398  STORE_FAST               'f'

 L. 681      1400  LOAD_FAST                'self'
             1402  LOAD_ATTR                seisdata
             1404  LOAD_FAST                'f'
             1406  BINARY_SUBSCR    
             1408  STORE_FAST               '_seisdata'

 L. 682      1410  LOAD_GLOBAL              seis_ays
             1412  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1414  LOAD_FAST                '_seisdata'
             1416  LOAD_FAST                '_traindata'
             1418  LOAD_FAST                'self'
             1420  LOAD_ATTR                survinfo

 L. 683      1422  LOAD_FAST                '_wdinl'
             1424  LOAD_FAST                '_wdxl'
             1426  LOAD_FAST                '_wdz'

 L. 684      1428  LOAD_CONST               False
             1430  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1432  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1434  LOAD_CONST               None
             1436  LOAD_CONST               None
             1438  BUILD_SLICE_2         2 
             1440  LOAD_CONST               3
             1442  LOAD_CONST               None
             1444  BUILD_SLICE_2         2 
             1446  BUILD_TUPLE_2         2 
             1448  BINARY_SUBSCR    
             1450  LOAD_FAST                '_traindict'
             1452  LOAD_FAST                'f'
             1454  STORE_SUBSCR     
         1456_1458  JUMP_BACK          1396  'to 1396'
             1460  POP_BLOCK        
           1462_0  COME_FROM_LOOP     1390  '1390'

 L. 685      1462  LOAD_FAST                '_target'
             1464  LOAD_FAST                '_features'
             1466  COMPARE_OP               not-in
         1468_1470  POP_JUMP_IF_FALSE  1522  'to 1522'

 L. 686      1472  LOAD_FAST                'self'
             1474  LOAD_ATTR                seisdata
             1476  LOAD_FAST                '_target'
             1478  BINARY_SUBSCR    
             1480  STORE_FAST               '_seisdata'

 L. 687      1482  LOAD_GLOBAL              seis_ays
             1484  LOAD_ATTR                retrieveSeisSampleFrom3DMat
             1486  LOAD_FAST                '_seisdata'
             1488  LOAD_FAST                '_traindata'
             1490  LOAD_FAST                'self'
             1492  LOAD_ATTR                survinfo

 L. 688      1494  LOAD_CONST               False
             1496  LOAD_CONST               ('seisinfo', 'verbose')
             1498  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1500  LOAD_CONST               None
             1502  LOAD_CONST               None
             1504  BUILD_SLICE_2         2 
             1506  LOAD_CONST               3
             1508  LOAD_CONST               None
             1510  BUILD_SLICE_2         2 
             1512  BUILD_TUPLE_2         2 
             1514  BINARY_SUBSCR    
             1516  LOAD_FAST                '_traindict'
             1518  LOAD_FAST                '_target'
             1520  STORE_SUBSCR     
           1522_0  COME_FROM          1468  '1468'

 L. 690      1522  LOAD_FAST                'self'
             1524  LOAD_ATTR                traindataconfig
             1526  LOAD_STR                 'RemoveInvariantFeature_Checked'
             1528  BINARY_SUBSCR    
         1530_1532  POP_JUMP_IF_FALSE  1608  'to 1608'

 L. 691      1534  SETUP_LOOP         1608  'to 1608'
             1536  LOAD_FAST                '_features'
             1538  GET_ITER         
           1540_0  COME_FROM          1568  '1568'
             1540  FOR_ITER           1606  'to 1606'
             1542  STORE_FAST               'f'

 L. 692      1544  LOAD_GLOBAL              ml_aug
             1546  LOAD_METHOD              removeInvariantFeature
             1548  LOAD_FAST                '_traindict'
             1550  LOAD_FAST                'f'
             1552  CALL_METHOD_2         2  '2 positional arguments'
             1554  STORE_FAST               '_traindict'

 L. 693      1556  LOAD_GLOBAL              basic_mdt
             1558  LOAD_METHOD              maxDictConstantRow
             1560  LOAD_FAST                '_traindict'
             1562  CALL_METHOD_1         1  '1 positional argument'
             1564  LOAD_CONST               0
             1566  COMPARE_OP               <=
         1568_1570  POP_JUMP_IF_FALSE  1540  'to 1540'

 L. 694      1572  LOAD_GLOBAL              print
             1574  LOAD_STR                 'TrainMl3DCnn: No training sample found'
             1576  CALL_FUNCTION_1       1  '1 positional argument'
             1578  POP_TOP          

 L. 695      1580  LOAD_GLOBAL              QtWidgets
             1582  LOAD_ATTR                QMessageBox
             1584  LOAD_METHOD              critical
             1586  LOAD_FAST                'self'
             1588  LOAD_ATTR                msgbox

 L. 696      1590  LOAD_STR                 'Train 3D-CNN'

 L. 697      1592  LOAD_STR                 'No training sample found'
             1594  CALL_METHOD_3         3  '3 positional arguments'
             1596  POP_TOP          

 L. 698      1598  LOAD_CONST               None
             1600  RETURN_VALUE     
         1602_1604  JUMP_BACK          1540  'to 1540'
             1606  POP_BLOCK        
           1608_0  COME_FROM_LOOP     1534  '1534'
           1608_1  COME_FROM          1530  '1530'

 L. 700      1608  LOAD_GLOBAL              np
             1610  LOAD_METHOD              round
             1612  LOAD_FAST                '_traindict'
             1614  LOAD_FAST                '_target'
             1616  BINARY_SUBSCR    
             1618  CALL_METHOD_1         1  '1 positional argument'
             1620  LOAD_METHOD              astype
             1622  LOAD_GLOBAL              int
             1624  CALL_METHOD_1         1  '1 positional argument'
             1626  LOAD_FAST                '_traindict'
             1628  LOAD_FAST                '_target'
             1630  STORE_SUBSCR     

 L. 702      1632  LOAD_FAST                '_video_height_new'
             1634  LOAD_FAST                '_video_height_old'
             1636  COMPARE_OP               !=
         1638_1640  POP_JUMP_IF_TRUE   1662  'to 1662'

 L. 703      1642  LOAD_FAST                '_video_width_new'
             1644  LOAD_FAST                '_video_width_old'
             1646  COMPARE_OP               !=
         1648_1650  POP_JUMP_IF_TRUE   1662  'to 1662'

 L. 704      1652  LOAD_FAST                '_video_depth_new'
             1654  LOAD_FAST                '_video_depth_old'
             1656  COMPARE_OP               !=
         1658_1660  POP_JUMP_IF_FALSE  1710  'to 1710'
           1662_0  COME_FROM          1648  '1648'
           1662_1  COME_FROM          1638  '1638'

 L. 705      1662  SETUP_LOOP         1710  'to 1710'
             1664  LOAD_FAST                '_features'
             1666  GET_ITER         
             1668  FOR_ITER           1708  'to 1708'
             1670  STORE_FAST               'f'

 L. 706      1672  LOAD_GLOBAL              basic_video
             1674  LOAD_ATTR                changeVideoSize
             1676  LOAD_FAST                '_traindict'
             1678  LOAD_FAST                'f'
             1680  BINARY_SUBSCR    

 L. 707      1682  LOAD_FAST                '_video_height_old'

 L. 708      1684  LOAD_FAST                '_video_width_old'

 L. 709      1686  LOAD_FAST                '_video_depth_old'

 L. 710      1688  LOAD_FAST                '_video_height_new'

 L. 711      1690  LOAD_FAST                '_video_width_new'

 L. 712      1692  LOAD_FAST                '_video_depth_new'
             1694  LOAD_CONST               ('video_height', 'video_width', 'video_depth', 'video_height_new', 'video_width_new', 'video_depth_new')
             1696  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1698  LOAD_FAST                '_traindict'
             1700  LOAD_FAST                'f'
             1702  STORE_SUBSCR     
         1704_1706  JUMP_BACK          1668  'to 1668'
             1708  POP_BLOCK        
           1710_0  COME_FROM_LOOP     1662  '1662'
           1710_1  COME_FROM          1658  '1658'

 L. 714      1710  LOAD_GLOBAL              print
             1712  LOAD_STR                 'TrainMl3DCnn: A total of %d valid training samples'

 L. 715      1714  LOAD_GLOBAL              basic_mdt
             1716  LOAD_METHOD              maxDictConstantRow
             1718  LOAD_FAST                '_traindict'
             1720  CALL_METHOD_1         1  '1 positional argument'
             1722  BINARY_MODULO    
             1724  CALL_FUNCTION_1       1  '1 positional argument'
             1726  POP_TOP          

 L. 717      1728  LOAD_GLOBAL              print
             1730  LOAD_STR                 'TrainMl3DCnn: Step 3 - Balance labels'
             1732  CALL_FUNCTION_1       1  '1 positional argument'
             1734  POP_TOP          

 L. 718      1736  LOAD_FAST                'self'
             1738  LOAD_ATTR                traindataconfig
             1740  LOAD_STR                 'BalanceTarget_Checked'
             1742  BINARY_SUBSCR    
         1744_1746  POP_JUMP_IF_FALSE  1788  'to 1788'

 L. 719      1748  LOAD_GLOBAL              ml_aug
             1750  LOAD_METHOD              balanceLabelbyExtension
             1752  LOAD_FAST                '_traindict'
             1754  LOAD_FAST                '_target'
             1756  CALL_METHOD_2         2  '2 positional arguments'
             1758  STORE_FAST               '_traindict'

 L. 720      1760  LOAD_GLOBAL              print

 L. 721      1762  LOAD_STR                 'TrainMl2DCnnFromScratch: A total of %d training samples after balance'

 L. 722      1764  LOAD_GLOBAL              np
             1766  LOAD_METHOD              shape
             1768  LOAD_FAST                '_traindict'
             1770  LOAD_FAST                '_target'
             1772  BINARY_SUBSCR    
             1774  CALL_METHOD_1         1  '1 positional argument'
             1776  LOAD_CONST               0
             1778  BINARY_SUBSCR    
             1780  BINARY_MODULO    
             1782  CALL_FUNCTION_1       1  '1 positional argument'
             1784  POP_TOP          
             1786  JUMP_FORWARD       1796  'to 1796'
           1788_0  COME_FROM          1744  '1744'

 L. 724      1788  LOAD_GLOBAL              print
             1790  LOAD_STR                 'TrainMl2DCnnFromScratch: No balance applied'
             1792  CALL_FUNCTION_1       1  '1 positional argument'
             1794  POP_TOP          
           1796_0  COME_FROM          1786  '1786'

 L. 726      1796  LOAD_GLOBAL              print
             1798  LOAD_STR                 'TrainMl3DCnn: Step 3 - Start training'
             1800  CALL_FUNCTION_1       1  '1 positional argument'
             1802  POP_TOP          

 L. 728      1804  LOAD_GLOBAL              QtWidgets
             1806  LOAD_METHOD              QProgressDialog
             1808  CALL_METHOD_0         0  '0 positional arguments'
             1810  STORE_FAST               '_pgsdlg'

 L. 729      1812  LOAD_GLOBAL              QtGui
             1814  LOAD_METHOD              QIcon
             1816  CALL_METHOD_0         0  '0 positional arguments'
             1818  STORE_FAST               'icon'

 L. 730      1820  LOAD_FAST                'icon'
             1822  LOAD_METHOD              addPixmap
             1824  LOAD_GLOBAL              QtGui
             1826  LOAD_METHOD              QPixmap
             1828  LOAD_GLOBAL              os
             1830  LOAD_ATTR                path
             1832  LOAD_METHOD              join
             1834  LOAD_FAST                'self'
             1836  LOAD_ATTR                iconpath
             1838  LOAD_STR                 'icons/update.png'
             1840  CALL_METHOD_2         2  '2 positional arguments'
             1842  CALL_METHOD_1         1  '1 positional argument'

 L. 731      1844  LOAD_GLOBAL              QtGui
             1846  LOAD_ATTR                QIcon
             1848  LOAD_ATTR                Normal
             1850  LOAD_GLOBAL              QtGui
             1852  LOAD_ATTR                QIcon
             1854  LOAD_ATTR                Off
             1856  CALL_METHOD_3         3  '3 positional arguments'
             1858  POP_TOP          

 L. 732      1860  LOAD_FAST                '_pgsdlg'
             1862  LOAD_METHOD              setWindowIcon
             1864  LOAD_FAST                'icon'
             1866  CALL_METHOD_1         1  '1 positional argument'
             1868  POP_TOP          

 L. 733      1870  LOAD_FAST                '_pgsdlg'
             1872  LOAD_METHOD              setWindowTitle
             1874  LOAD_STR                 'Update 3D-CNN'
             1876  CALL_METHOD_1         1  '1 positional argument'
             1878  POP_TOP          

 L. 734      1880  LOAD_FAST                '_pgsdlg'
             1882  LOAD_METHOD              setCancelButton
             1884  LOAD_CONST               None
             1886  CALL_METHOD_1         1  '1 positional argument'
             1888  POP_TOP          

 L. 735      1890  LOAD_FAST                '_pgsdlg'
             1892  LOAD_METHOD              setWindowFlags
             1894  LOAD_GLOBAL              QtCore
             1896  LOAD_ATTR                Qt
             1898  LOAD_ATTR                WindowStaysOnTopHint
             1900  CALL_METHOD_1         1  '1 positional argument'
             1902  POP_TOP          

 L. 736      1904  LOAD_FAST                '_pgsdlg'
             1906  LOAD_METHOD              forceShow
             1908  CALL_METHOD_0         0  '0 positional arguments'
             1910  POP_TOP          

 L. 737      1912  LOAD_FAST                '_pgsdlg'
             1914  LOAD_METHOD              setFixedWidth
             1916  LOAD_CONST               400
             1918  CALL_METHOD_1         1  '1 positional argument'
             1920  POP_TOP          

 L. 738      1922  LOAD_GLOBAL              ml_cnn3d
             1924  LOAD_ATTR                update3DCNNClassifier
             1926  LOAD_FAST                '_traindict'

 L. 739      1928  LOAD_FAST                '_nepoch'
             1930  LOAD_FAST                '_batchsize'

 L. 740      1932  LOAD_FAST                '_learning_rate'

 L. 741      1934  LOAD_FAST                '_dropout_prob_fclayer'

 L. 742      1936  LOAD_FAST                'self'
             1938  LOAD_ATTR                modelpath
             1940  LOAD_FAST                'self'
             1942  LOAD_ATTR                modelname

 L. 743      1944  LOAD_CONST               True

 L. 744      1946  LOAD_FAST                '_savepath'
             1948  LOAD_FAST                '_savename'

 L. 745      1950  LOAD_FAST                '_pgsdlg'
             1952  LOAD_CONST               ('nepoch', 'batchsize', 'learningrate', 'dropoutprobfclayer', 'cnn3dpath', 'cnn3dname', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             1954  CALL_FUNCTION_KW_11    11  '11 total positional and keyword args'
             1956  STORE_FAST               '_cnnlog'

 L. 748      1958  LOAD_GLOBAL              QtWidgets
             1960  LOAD_ATTR                QMessageBox
             1962  LOAD_METHOD              information
             1964  LOAD_FAST                'self'
             1966  LOAD_ATTR                msgbox

 L. 749      1968  LOAD_STR                 'Update 3D-CNN'

 L. 750      1970  LOAD_STR                 'CNN updated successfully'
             1972  CALL_METHOD_3         3  '3 positional arguments'
             1974  POP_TOP          

 L. 752      1976  LOAD_GLOBAL              QtWidgets
             1978  LOAD_ATTR                QMessageBox
             1980  LOAD_METHOD              question
             1982  LOAD_FAST                'self'
             1984  LOAD_ATTR                msgbox
             1986  LOAD_STR                 'Update 3D-CNN'
             1988  LOAD_STR                 'View learning matrix?'

 L. 753      1990  LOAD_GLOBAL              QtWidgets
             1992  LOAD_ATTR                QMessageBox
             1994  LOAD_ATTR                Yes
             1996  LOAD_GLOBAL              QtWidgets
             1998  LOAD_ATTR                QMessageBox
             2000  LOAD_ATTR                No
             2002  BINARY_OR        

 L. 754      2004  LOAD_GLOBAL              QtWidgets
             2006  LOAD_ATTR                QMessageBox
             2008  LOAD_ATTR                Yes
             2010  CALL_METHOD_5         5  '5 positional arguments'
             2012  STORE_FAST               'reply'

 L. 756      2014  LOAD_FAST                'reply'
             2016  LOAD_GLOBAL              QtWidgets
             2018  LOAD_ATTR                QMessageBox
             2020  LOAD_ATTR                Yes
             2022  COMPARE_OP               ==
         2024_2026  POP_JUMP_IF_FALSE  2094  'to 2094'

 L. 757      2028  LOAD_GLOBAL              QtWidgets
             2030  LOAD_METHOD              QDialog
             2032  CALL_METHOD_0         0  '0 positional arguments'
             2034  STORE_FAST               '_viewmllearnmat'

 L. 758      2036  LOAD_GLOBAL              gui_viewmllearnmat
             2038  CALL_FUNCTION_0       0  '0 positional arguments'
             2040  STORE_FAST               '_gui'

 L. 759      2042  LOAD_FAST                '_cnnlog'
             2044  LOAD_STR                 'learning_curve'
             2046  BINARY_SUBSCR    
             2048  LOAD_FAST                '_gui'
             2050  STORE_ATTR               learnmat

 L. 760      2052  LOAD_FAST                'self'
             2054  LOAD_ATTR                linestyle
             2056  LOAD_FAST                '_gui'
             2058  STORE_ATTR               linestyle

 L. 761      2060  LOAD_FAST                'self'
             2062  LOAD_ATTR                fontstyle
             2064  LOAD_FAST                '_gui'
             2066  STORE_ATTR               fontstyle

 L. 762      2068  LOAD_FAST                '_gui'
             2070  LOAD_METHOD              setupGUI
             2072  LOAD_FAST                '_viewmllearnmat'
             2074  CALL_METHOD_1         1  '1 positional argument'
             2076  POP_TOP          

 L. 763      2078  LOAD_FAST                '_viewmllearnmat'
             2080  LOAD_METHOD              exec
             2082  CALL_METHOD_0         0  '0 positional arguments'
             2084  POP_TOP          

 L. 764      2086  LOAD_FAST                '_viewmllearnmat'
             2088  LOAD_METHOD              show
             2090  CALL_METHOD_0         0  '0 positional arguments'
             2092  POP_TOP          
           2094_0  COME_FROM          2024  '2024'

Parse error at or near `POP_TOP' instruction at offset 2092

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))

    def checkSurvInfo(self):
        self.refreshMsgBox()
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            return False
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