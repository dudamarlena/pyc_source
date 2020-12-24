# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml3dcnnfromscratch.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 44450 bytes
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
from cognitivegeo.src.ml.cnnclassifier3d import cnnclassifier3d as ml_cnn3d
from cognitivegeo.src.gui.viewmllearnmat import viewmllearnmat as gui_viewmllearnmat
from cognitivegeo.src.gui.configmltraindata import configmltraindata as gui_configmltraindata
from cognitivegeo.src.vis.messager import messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml3dcnnfromscratch(object):
    survinfo = {}
    seisdata = {}
    pointsetdata = {}
    rootpath = ''
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    iconpath = os.path.dirname(__file__)
    dialog = None
    featurelist = list()
    traindataconfig = {}
    traindataconfig['TrainPointSet'] = []
    traindataconfig['BalanceTarget_Enabled'] = True
    traindataconfig['BalanceTarget_Checked'] = False
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False

    def setupGUI(self, TrainMl3DCnnFromScratch):
        TrainMl3DCnnFromScratch.setObjectName('TrainMl3DCnnFromScratch')
        TrainMl3DCnnFromScratch.setFixedSize(810, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl3DCnnFromScratch.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl3DCnnFromScratch)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lbloldsize = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 130, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 130, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 130, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lblolddepth = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblolddepth.setObjectName('lblolddepth')
        self.lblolddepth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtolddepth = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtolddepth.setObjectName('ldtolddepth')
        self.ldtolddepth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 130, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 130, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 130, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewdepth = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblnewdepth.setObjectName('lblnewdepth')
        self.lblnewdepth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewdepth = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtnewdepth.setObjectName('ldtnewdepth')
        self.ldtnewdepth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl3DCnnFromScratch)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 50, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 50, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl3DCnnFromScratch)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 90, 180, 160))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 50, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 50, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(TrainMl3DCnnFromScratch)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 90, 180, 160))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 260, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 260, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 260, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 300, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 300, 40, 30))
        self.lblmaskdepth = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblmaskdepth.setObjectName('lblmaskdepth')
        self.lblmaskdepth.setGeometry(QtCore.QRect(500, 340, 50, 30))
        self.ldtmaskdepth = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtmaskdepth.setObjectName('ldtmaskdepth')
        self.ldtmaskdepth.setGeometry(QtCore.QRect(550, 340, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 260, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 260, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 260, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 300, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 300, 40, 30))
        self.lblpooldepth = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblpooldepth.setObjectName('lblpooldepth')
        self.lblpooldepth.setGeometry(QtCore.QRect(700, 340, 50, 30))
        self.ldtpooldepth = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtpooldepth.setObjectName('ldtpooldepth')
        self.ldtpooldepth.setGeometry(QtCore.QRect(750, 340, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl3DCnnFromScratch)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 310, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 350, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.lblfcdropout = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblfcdropout.setObjectName('lblfcdropout')
        self.lblfcdropout.setGeometry(QtCore.QRect(210, 390, 130, 30))
        self.ldtfcdropout = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtfcdropout.setObjectName('ldtfcdropout')
        self.ldtfcdropout.setGeometry(QtCore.QRect(350, 390, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl3DCnnFromScratch)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 100, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl3DCnnFromScratch)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(110, 440, 210, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl3DCnnFromScratch)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 440, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl3DCnnFromScratch)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl3DCnnFromScratch)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl3DCnnFromScratch.geometry().center().x()
        _center_y = TrainMl3DCnnFromScratch.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl3DCnnFromScratch)
        QtCore.QMetaObject.connectSlotsByName(TrainMl3DCnnFromScratch)

    def retranslateGUI(self, TrainMl3DCnnFromScratch):
        self.dialog = TrainMl3DCnnFromScratch
        _translate = QtCore.QCoreApplication.translate
        TrainMl3DCnnFromScratch.setWindowTitle(_translate('TrainMl3DCnnFromScratch', 'Train 3D-CNN from scratch'))
        self.lblfeature.setText(_translate('TrainMl3DCnnFromScratch', 'Select features:'))
        self.lbltarget.setText(_translate('TrainMl3DCnnFromScratch', 'Select target:'))
        self.lbloldsize.setText(_translate('TrainMl3DCnnFromScratch', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl3DCnnFromScratch', 'height=\ntime/depth'))
        self.ldtoldheight.setText(_translate('TrainMl3DCnnFromScratch', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl3DCnnFromScratch', 'width=\ncrossline'))
        self.ldtoldwidth.setText(_translate('TrainMl3DCnnFromScratch', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblolddepth.setText(_translate('TrainMl3DCnnFromScratch', 'depth=\ninline'))
        self.ldtolddepth.setText(_translate('TrainMl3DCnnFromScratch', ''))
        self.ldtolddepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl3DCnnFromScratch', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl3DCnnFromScratch', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl3DCnnFromScratch', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl3DCnnFromScratch', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl3DCnnFromScratch', '32'))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewdepth.setText(_translate('TrainMl3DCnnFromScratch', 'depth='))
        self.ldtnewdepth.setText(_translate('TrainMl3DCnnFromScratch', '32'))
        self.ldtnewdepth.setAlignment(QtCore.Qt.AlignCenter)
        if self.checkSurvInfo():
            self.featurelist.clear()
            self.lwgfeature.clear()
            self.cbbtarget.clear()
            _firstfeature = None
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    self.featurelist.append(i)
                    item = QtWidgets.QListWidgetItem(self.lwgfeature)
                    item.setText(_translate('TrainMl3DCnnFromScratch', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl3DCnnFromScratch', 'Specify CNN architecture:'))
        self.lblnconvblock.setText(_translate('TrainMl2DCnn', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl2DCnn', '3'))
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.twgnconvblock.setRowCount(3)
        for _idx in range(int(self.ldtnconvblock.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(_idx + 1))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgnconvblock.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(2))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgnconvblock.setItem(_idx, 1, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(int(np.power(2, _idx) * 32)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgnconvblock.setItem(_idx, 2, item)

        self.lblnfclayer.setText(_translate('TrainMl2DCnn', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('TrainMl2DCnn', '2'))
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.twgnfclayer.setRowCount(2)
        for _idx in range(int(self.ldtnfclayer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl2DCnn', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgnfclayer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgnfclayer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl3DCnnFromScratch', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl3DCnnFromScratch', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl3DCnnFromScratch', '2'))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('TrainMl3DCnnFromScratch', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl3DCnnFromScratch', '2'))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskdepth.setText(_translate('TrainMl3DCnnFromScratch', 'depth='))
        self.ldtmaskdepth.setText(_translate('TrainMl3DCnnFromScratch', '2'))
        self.ldtmaskdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('TrainMl3DCnnFromScratch', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl3DCnnFromScratch', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl3DCnnFromScratch', '2'))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl3DCnnFromScratch', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl3DCnnFromScratch', '2'))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpooldepth.setText(_translate('TrainMl3DCnnFromScratch', 'depth='))
        self.ldtpooldepth.setText(_translate('TrainMl3DCnnFromScratch', '2'))
        self.ldtpooldepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfcdropout.setText(_translate('TrainMl3DCnnFromScratch', 'MLP dropout rate:'))
        self.lblfcdropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtfcdropout.setText(_translate('TrainMl3DCnnFromScratch', '0.5'))
        self.ldtfcdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.btnconfigtraindata.setText(_translate('TrainMl3DCnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lblpara.setText(_translate('TrainMl3DCnnFromScratch', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl3DCnnFromScratch', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl3DCnnFromScratch', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl3DCnnFromScratch', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl3DCnnFromScratch', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl3DCnnFromScratch', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl3DCnnFromScratch', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl3DCnnFromScratch', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl3DCnnFromScratch', ''))
        self.btnsave.setText(_translate('TrainMl3DCnnFromScratch', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl3DCnnFromScratch', 'Train 3D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl3DCnnFromScratch)

    def changeLdtNconvblock(self):
        if len(self.ldtnconvblock.text()) > 0:
            _nlayer = int(self.ldtnconvblock.text())
            self.twgnconvblock.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblock.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(2))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgnconvblock.setItem(_idx, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(int(np.power(2, _idx) * 32)))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgnconvblock.setItem(_idx, 2, item)

        else:
            self.twgnconvblock.setRowCount(0)

    def changeLdtNfclayer(self):
        if len(self.ldtnfclayer.text()) > 0:
            _nlayer = int(self.ldtnfclayer.text())
            self.twgnfclayer.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnfclayer.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(1024))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgnfclayer.setItem(_idx, 1, item)

        else:
            self.twgnfclayer.setRowCount(0)

    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Save CNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtsave.setText(_file[0])

    def clickBtnConfigTrainData(self):
        _configtraindata = QtWidgets.QDialog()
        _gui = gui_configmltraindata()
        _gui.mltraindataconfig = self.traindataconfig
        _gui.pointsetlist = sorted(self.pointsetdata.keys())
        _gui.setupGUI(_configtraindata)
        _configtraindata.exec()
        self.traindataconfig = _gui.mltraindataconfig
        _configtraindata.show()

    def clickBtnTrainMl3DCnnFromScratch(self):
        self.refreshMsgBox()
        if len(self.lwgfeature.selectedItems()) < 1:
            vis_msg.print('ERROR in TrainMl3DCnnFromScratch: No feature selected for training', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'No feature selected for training')
            return
        _video_height_old = basic_data.str2int(self.ldtoldheight.text())
        _video_width_old = basic_data.str2int(self.ldtoldwidth.text())
        _video_depth_old = basic_data.str2int(self.ldtolddepth.text())
        _video_height_new = basic_data.str2int(self.ldtnewheight.text())
        _video_width_new = basic_data.str2int(self.ldtnewwidth.text())
        _video_depth_new = basic_data.str2int(self.ldtnewdepth.text())
        if _video_height_old is False or _video_width_old is False or _video_depth_old is False or _video_height_new is False or _video_width_new is False or _video_depth_new is False:
            vis_msg.print('ERROR in TrainMl3DCnnFromScratch: Non-integer feature size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Non-integer feature size')
            return
        if _video_height_old < 2 or _video_width_old < 2 or _video_depth_old < 2 or _video_height_new < 2 or _video_width_new < 2 or _video_depth_new < 2:
            vis_msg.print('ERROR in TrainMl3DCnnFromScratch: Features are not 3D', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Features are not 3D')
            return
        _video_height_old = 2 * int(_video_height_old / 2) + 1
        _video_width_old = 2 * int(_video_width_old / 2) + 1
        _video_depth_old = 2 * int(_video_depth_old / 2) + 1
        if _video_height_old <= 1 or _video_width_old <= 1 or _video_depth_old <= 1:
            vis_msg.print('ERROR in TrainMl3DCnnFromScratch: wrong original video size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Wrong original video size')
            return
        _features = self.lwgfeature.selectedItems()
        _features = [f.text() for f in _features]
        _target = self.featurelist[self.cbbtarget.currentIndex()]
        _nconvblock = basic_data.str2int(self.ldtnconvblock.text())
        _nconvlayer = [basic_data.str2int(self.twgnconvblock.item(i, 1).text()) for i in range(_nconvblock)]
        _nconvfeature = [basic_data.str2int(self.twgnconvblock.item(i, 2).text()) for i in range(_nconvblock)]
        _nfclayer = basic_data.str2int(self.ldtnfclayer.text())
        _nfcneuron = [basic_data.str2int(self.twgnfclayer.item(i, 1).text()) for i in range(_nfclayer)]
        _patch_height = basic_data.str2int(self.ldtmaskheight.text())
        _patch_width = basic_data.str2int(self.ldtmaskwidth.text())
        _patch_depth = basic_data.str2int(self.ldtmaskdepth.text())
        _pool_height = basic_data.str2int(self.ldtpoolheight.text())
        _pool_width = basic_data.str2int(self.ldtpoolwidth.text())
        _pool_depth = basic_data.str2int(self.ldtpooldepth.text())
        _nepoch = basic_data.str2int(self.ldtnepoch.text())
        _batchsize = basic_data.str2int(self.ldtbatchsize.text())
        _learning_rate = basic_data.str2float(self.ldtlearnrate.text())
        _dropout_prob_fclayer = basic_data.str2float(self.ldtfcdropout.text())
        if _nconvblock is False or _nconvblock <= 0:
            vis_msg.print('ERROR in TrainMl3DCnnFromScratch: Non-positive convolutional block number', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Non-positive convolutional block number')
            return
        for _i in _nconvlayer:
            if _i is False or _i < 1:
                vis_msg.print('ERROR in TrainMl3DCnnFromScratch: Non-positive convolutional layer number', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Non-positive convolutional layer number')
                return

        for _i in _nconvfeature:
            if _i is False or _i < 1:
                vis_msg.print('ERROR in TrainMl3DCnnFromScratch: Non-positive convolutional feature number', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Non-positive convolutional feature number')
                return

        if _nfclayer is False or _nfclayer <= 0:
            vis_msg.print('ERROR in TrainMl3DCnnFromScratch: Non-positive MLP layer number', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Non-positive MLP layer number')
            return
        for _i in _nfcneuron:
            if _i is False or _i < 1:
                vis_msg.print('ERROR in TrainMl3DCnnFromScratch: Non-positive MLP neuron number', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Non-positive MLP neuron number')
                return

        if _patch_height is False or _patch_width is False or _patch_depth is False or _patch_height < 1 or _patch_width < 1 or _patch_depth < 1:
            vis_msg.print('ERROR in TrainMl3DCnnFromScratch: Non-positive convolutional patch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Non-positive convolutional patch size')
            return
        if _pool_height is False or _pool_width is False or _pool_depth is False or _pool_height < 1 or _pool_width < 1 or _pool_depth < 1:
            vis_msg.print('ERROR in TrainMl3DCnnFromScratch: Non-positive pooling size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Non-positive pooling size')
            return
        if _nepoch is False or _nepoch <= 0:
            vis_msg.print('ERROR in TrainMl3DCnnFromScratch: Non-positive epoch number', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Non-positive epoch number')
            return
        if _batchsize is False or _batchsize <= 0:
            vis_msg.print('ERROR in TrainMl3DCnnFromScratch: Non-positive batch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Non-positive batch size')
            return
        if _learning_rate is False or _learning_rate <= 0:
            vis_msg.print('ERROR in TrainMl3DCnnFromScratch: Non-positive learning rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Non-positive learning rate')
            return
        if _dropout_prob_fclayer is False or _dropout_prob_fclayer <= 0:
            vis_msg.print('ERROR in TrainMl3DCnnFromScratch: Negative dropout rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'Negative dropout rate')
            return
        if len(self.ldtsave.text()) < 1:
            vis_msg.print('EROR in TrainMl3DCnnFromScratch: No name specified for CNN network', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'No name specified for CNN network')
            return
        _savepath = os.path.dirname(self.ldtsave.text())
        _savename = os.path.splitext(os.path.basename(self.ldtsave.text()))[0]
        _wdinl = int(_video_depth_old / 2)
        _wdxl = int(_video_width_old / 2)
        _wdz = int(_video_height_old / 2)
        _seisinfo = self.survinfo
        print('TrainMl3DCnnFromScratchFromScratch: Step 1 - Get training samples:')
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
            vis_msg.print('ERROR in TrainMl3DCnnFromScratch: No training sample found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 3D-CNN', 'No training sample found')
            return
        print('TrainMl3DCnnFromScratch: Step 2 - Retrieve and interpolate videos: (%d, %d, %d) --> (%d, %d, %d)' % (
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
                    vis_msg.print('ERROR in TrainMl3DCnnFromScratch: No training sample found', type='error')
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

            print('TrainMl3DCnnFromScratch: A total of %d valid training samples' % basic_mdt.maxDictConstantRow(_traindict))
            print('TrainMl3DCnnFromScratch: Step 3 - Balance labels')
            if self.traindataconfig['BalanceTarget_Checked']:
                _traindict = ml_aug.balanceLabelbyExtension(_traindict, _target)
                print('TrainMl2DCnnFromScratch: A total of %d training samples after balance' % np.shape(_traindict[_target])[0])
            else:
                print('TrainMl2DCnnFromScratch: No balance applied')
        print('TrainMl3DCnnFromScratch: Step 4 - Start training')
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Train 3D-CNN')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _cnnlog = ml_cnn3d.create3DCNNClassifier(_traindict, videoheight=_video_height_new,
          videowidth=_video_width_new,
          videodepth=_video_depth_new,
          features=_features,
          target=_target,
          nepoch=_nepoch,
          batchsize=_batchsize,
          nconvblock=_nconvblock,
          nconvlayer=_nconvlayer,
          nconvfeature=_nconvfeature,
          nfclayer=_nfclayer,
          nfcneuron=_nfcneuron,
          patchheight=_patch_height,
          patchwidth=_patch_width,
          patchdepth=_patch_depth,
          poolheight=_pool_height,
          poolwidth=_pool_width,
          pooldepth=_pool_depth,
          learningrate=_learning_rate,
          dropoutprobfclayer=_dropout_prob_fclayer,
          save2disk=True,
          savepath=_savepath,
          savename=_savename,
          qpgsdlg=_pgsdlg)
        QtWidgets.QMessageBox.information(self.msgbox, 'Train 3D-CNN', 'CNN trained successfully')
        reply = QtWidgets.QMessageBox.question(self.msgbox, 'Train 3D-CNN', 'View learning matrix?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
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
    TrainMl3DCnnFromScratch = QtWidgets.QWidget()
    gui = trainml3dcnnfromscratch()
    gui.setupGUI(TrainMl3DCnnFromScratch)
    TrainMl3DCnnFromScratch.show()
    sys.exit(app.exec_())