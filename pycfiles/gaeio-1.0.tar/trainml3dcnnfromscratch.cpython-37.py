# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml3dcnnfromscratch.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 44450 bytes
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
import cognitivegeo.src.ml.cnnclassifier3d as ml_cnn3d
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
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

    def clickBtnTrainMl3DCnnFromScratch--- This code section failed: ---

 L. 461         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 463         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 464        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 465        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 466        50  LOAD_STR                 'Train 3D-CNN'

 L. 467        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 468        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 470        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_video_height_old'

 L. 471        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_video_width_old'

 L. 472        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtolddepth
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_video_depth_old'

 L. 473       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewheight
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_video_height_new'

 L. 474       126  LOAD_GLOBAL              basic_data
              128  LOAD_METHOD              str2int
              130  LOAD_DEREF               'self'
              132  LOAD_ATTR                ldtnewwidth
              134  LOAD_METHOD              text
              136  CALL_METHOD_0         0  '0 positional arguments'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  STORE_FAST               '_video_width_new'

 L. 475       142  LOAD_GLOBAL              basic_data
              144  LOAD_METHOD              str2int
              146  LOAD_DEREF               'self'
              148  LOAD_ATTR                ldtnewdepth
              150  LOAD_METHOD              text
              152  CALL_METHOD_0         0  '0 positional arguments'
              154  CALL_METHOD_1         1  '1 positional argument'
              156  STORE_FAST               '_video_depth_new'

 L. 476       158  LOAD_FAST                '_video_height_old'
              160  LOAD_CONST               False
              162  COMPARE_OP               is
              164  POP_JUMP_IF_TRUE    206  'to 206'
              166  LOAD_FAST                '_video_width_old'
              168  LOAD_CONST               False
              170  COMPARE_OP               is
              172  POP_JUMP_IF_TRUE    206  'to 206'
              174  LOAD_FAST                '_video_depth_old'
              176  LOAD_CONST               False
              178  COMPARE_OP               is
              180  POP_JUMP_IF_TRUE    206  'to 206'

 L. 477       182  LOAD_FAST                '_video_height_new'
              184  LOAD_CONST               False
              186  COMPARE_OP               is
              188  POP_JUMP_IF_TRUE    206  'to 206'
              190  LOAD_FAST                '_video_width_new'
              192  LOAD_CONST               False
              194  COMPARE_OP               is
              196  POP_JUMP_IF_TRUE    206  'to 206'
              198  LOAD_FAST                '_video_depth_new'
              200  LOAD_CONST               False
              202  COMPARE_OP               is
              204  POP_JUMP_IF_FALSE   242  'to 242'
            206_0  COME_FROM           196  '196'
            206_1  COME_FROM           188  '188'
            206_2  COME_FROM           180  '180'
            206_3  COME_FROM           172  '172'
            206_4  COME_FROM           164  '164'

 L. 478       206  LOAD_GLOBAL              vis_msg
              208  LOAD_ATTR                print
              210  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: Non-integer feature size'
              212  LOAD_STR                 'error'
              214  LOAD_CONST               ('type',)
              216  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              218  POP_TOP          

 L. 479       220  LOAD_GLOBAL              QtWidgets
              222  LOAD_ATTR                QMessageBox
              224  LOAD_METHOD              critical
              226  LOAD_DEREF               'self'
              228  LOAD_ATTR                msgbox

 L. 480       230  LOAD_STR                 'Train 3D-CNN'

 L. 481       232  LOAD_STR                 'Non-integer feature size'
              234  CALL_METHOD_3         3  '3 positional arguments'
              236  POP_TOP          

 L. 482       238  LOAD_CONST               None
              240  RETURN_VALUE     
            242_0  COME_FROM           204  '204'

 L. 483       242  LOAD_FAST                '_video_height_old'
              244  LOAD_CONST               2
              246  COMPARE_OP               <
          248_250  POP_JUMP_IF_TRUE    302  'to 302'
              252  LOAD_FAST                '_video_width_old'
              254  LOAD_CONST               2
              256  COMPARE_OP               <
          258_260  POP_JUMP_IF_TRUE    302  'to 302'
              262  LOAD_FAST                '_video_depth_old'
              264  LOAD_CONST               2
              266  COMPARE_OP               <
          268_270  POP_JUMP_IF_TRUE    302  'to 302'

 L. 484       272  LOAD_FAST                '_video_height_new'
              274  LOAD_CONST               2
              276  COMPARE_OP               <
          278_280  POP_JUMP_IF_TRUE    302  'to 302'
              282  LOAD_FAST                '_video_width_new'
              284  LOAD_CONST               2
              286  COMPARE_OP               <
          288_290  POP_JUMP_IF_TRUE    302  'to 302'
              292  LOAD_FAST                '_video_depth_new'
              294  LOAD_CONST               2
              296  COMPARE_OP               <
          298_300  POP_JUMP_IF_FALSE   338  'to 338'
            302_0  COME_FROM           288  '288'
            302_1  COME_FROM           278  '278'
            302_2  COME_FROM           268  '268'
            302_3  COME_FROM           258  '258'
            302_4  COME_FROM           248  '248'

 L. 485       302  LOAD_GLOBAL              vis_msg
              304  LOAD_ATTR                print
              306  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: Features are not 3D'
              308  LOAD_STR                 'error'
              310  LOAD_CONST               ('type',)
              312  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              314  POP_TOP          

 L. 486       316  LOAD_GLOBAL              QtWidgets
              318  LOAD_ATTR                QMessageBox
              320  LOAD_METHOD              critical
              322  LOAD_DEREF               'self'
              324  LOAD_ATTR                msgbox

 L. 487       326  LOAD_STR                 'Train 3D-CNN'

 L. 488       328  LOAD_STR                 'Features are not 3D'
              330  CALL_METHOD_3         3  '3 positional arguments'
              332  POP_TOP          

 L. 489       334  LOAD_CONST               None
              336  RETURN_VALUE     
            338_0  COME_FROM           298  '298'

 L. 491       338  LOAD_CONST               2
              340  LOAD_GLOBAL              int
              342  LOAD_FAST                '_video_height_old'
              344  LOAD_CONST               2
              346  BINARY_TRUE_DIVIDE
              348  CALL_FUNCTION_1       1  '1 positional argument'
              350  BINARY_MULTIPLY  
              352  LOAD_CONST               1
              354  BINARY_ADD       
              356  STORE_FAST               '_video_height_old'

 L. 492       358  LOAD_CONST               2
              360  LOAD_GLOBAL              int
              362  LOAD_FAST                '_video_width_old'
              364  LOAD_CONST               2
              366  BINARY_TRUE_DIVIDE
              368  CALL_FUNCTION_1       1  '1 positional argument'
              370  BINARY_MULTIPLY  
              372  LOAD_CONST               1
              374  BINARY_ADD       
              376  STORE_FAST               '_video_width_old'

 L. 493       378  LOAD_CONST               2
              380  LOAD_GLOBAL              int
              382  LOAD_FAST                '_video_depth_old'
              384  LOAD_CONST               2
              386  BINARY_TRUE_DIVIDE
              388  CALL_FUNCTION_1       1  '1 positional argument'
              390  BINARY_MULTIPLY  
              392  LOAD_CONST               1
              394  BINARY_ADD       
              396  STORE_FAST               '_video_depth_old'

 L. 494       398  LOAD_FAST                '_video_height_old'
              400  LOAD_CONST               1
              402  COMPARE_OP               <=
          404_406  POP_JUMP_IF_TRUE    428  'to 428'
              408  LOAD_FAST                '_video_width_old'
              410  LOAD_CONST               1
              412  COMPARE_OP               <=
          414_416  POP_JUMP_IF_TRUE    428  'to 428'
              418  LOAD_FAST                '_video_depth_old'
              420  LOAD_CONST               1
              422  COMPARE_OP               <=
          424_426  POP_JUMP_IF_FALSE   464  'to 464'
            428_0  COME_FROM           414  '414'
            428_1  COME_FROM           404  '404'

 L. 495       428  LOAD_GLOBAL              vis_msg
              430  LOAD_ATTR                print
              432  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: wrong original video size'
              434  LOAD_STR                 'error'
              436  LOAD_CONST               ('type',)
              438  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              440  POP_TOP          

 L. 496       442  LOAD_GLOBAL              QtWidgets
              444  LOAD_ATTR                QMessageBox
              446  LOAD_METHOD              critical
              448  LOAD_DEREF               'self'
              450  LOAD_ATTR                msgbox

 L. 497       452  LOAD_STR                 'Train 3D-CNN'

 L. 498       454  LOAD_STR                 'Wrong original video size'
              456  CALL_METHOD_3         3  '3 positional arguments'
              458  POP_TOP          

 L. 499       460  LOAD_CONST               None
              462  RETURN_VALUE     
            464_0  COME_FROM           424  '424'

 L. 501       464  LOAD_DEREF               'self'
              466  LOAD_ATTR                lwgfeature
              468  LOAD_METHOD              selectedItems
              470  CALL_METHOD_0         0  '0 positional arguments'
              472  STORE_FAST               '_features'

 L. 502       474  LOAD_LISTCOMP            '<code_object <listcomp>>'
              476  LOAD_STR                 'trainml3dcnnfromscratch.clickBtnTrainMl3DCnnFromScratch.<locals>.<listcomp>'
              478  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              480  LOAD_FAST                '_features'
              482  GET_ITER         
              484  CALL_FUNCTION_1       1  '1 positional argument'
              486  STORE_FAST               '_features'

 L. 503       488  LOAD_DEREF               'self'
              490  LOAD_ATTR                featurelist
              492  LOAD_DEREF               'self'
              494  LOAD_ATTR                cbbtarget
              496  LOAD_METHOD              currentIndex
              498  CALL_METHOD_0         0  '0 positional arguments'
              500  BINARY_SUBSCR    
              502  STORE_FAST               '_target'

 L. 505       504  LOAD_GLOBAL              basic_data
              506  LOAD_METHOD              str2int
              508  LOAD_DEREF               'self'
              510  LOAD_ATTR                ldtnconvblock
              512  LOAD_METHOD              text
              514  CALL_METHOD_0         0  '0 positional arguments'
              516  CALL_METHOD_1         1  '1 positional argument'
              518  STORE_FAST               '_nconvblock'

 L. 506       520  LOAD_CLOSURE             'self'
              522  BUILD_TUPLE_1         1 
              524  LOAD_LISTCOMP            '<code_object <listcomp>>'
              526  LOAD_STR                 'trainml3dcnnfromscratch.clickBtnTrainMl3DCnnFromScratch.<locals>.<listcomp>'
              528  MAKE_FUNCTION_8          'closure'
              530  LOAD_GLOBAL              range
              532  LOAD_FAST                '_nconvblock'
              534  CALL_FUNCTION_1       1  '1 positional argument'
              536  GET_ITER         
              538  CALL_FUNCTION_1       1  '1 positional argument'
              540  STORE_FAST               '_nconvlayer'

 L. 507       542  LOAD_CLOSURE             'self'
              544  BUILD_TUPLE_1         1 
              546  LOAD_LISTCOMP            '<code_object <listcomp>>'
              548  LOAD_STR                 'trainml3dcnnfromscratch.clickBtnTrainMl3DCnnFromScratch.<locals>.<listcomp>'
              550  MAKE_FUNCTION_8          'closure'
              552  LOAD_GLOBAL              range
              554  LOAD_FAST                '_nconvblock'
              556  CALL_FUNCTION_1       1  '1 positional argument'
              558  GET_ITER         
              560  CALL_FUNCTION_1       1  '1 positional argument'
              562  STORE_FAST               '_nconvfeature'

 L. 508       564  LOAD_GLOBAL              basic_data
              566  LOAD_METHOD              str2int
              568  LOAD_DEREF               'self'
              570  LOAD_ATTR                ldtnfclayer
              572  LOAD_METHOD              text
              574  CALL_METHOD_0         0  '0 positional arguments'
              576  CALL_METHOD_1         1  '1 positional argument'
              578  STORE_FAST               '_nfclayer'

 L. 509       580  LOAD_CLOSURE             'self'
              582  BUILD_TUPLE_1         1 
              584  LOAD_LISTCOMP            '<code_object <listcomp>>'
              586  LOAD_STR                 'trainml3dcnnfromscratch.clickBtnTrainMl3DCnnFromScratch.<locals>.<listcomp>'
              588  MAKE_FUNCTION_8          'closure'
              590  LOAD_GLOBAL              range
              592  LOAD_FAST                '_nfclayer'
              594  CALL_FUNCTION_1       1  '1 positional argument'
              596  GET_ITER         
              598  CALL_FUNCTION_1       1  '1 positional argument'
              600  STORE_FAST               '_nfcneuron'

 L. 510       602  LOAD_GLOBAL              basic_data
              604  LOAD_METHOD              str2int
              606  LOAD_DEREF               'self'
              608  LOAD_ATTR                ldtmaskheight
              610  LOAD_METHOD              text
              612  CALL_METHOD_0         0  '0 positional arguments'
              614  CALL_METHOD_1         1  '1 positional argument'
              616  STORE_FAST               '_patch_height'

 L. 511       618  LOAD_GLOBAL              basic_data
              620  LOAD_METHOD              str2int
              622  LOAD_DEREF               'self'
              624  LOAD_ATTR                ldtmaskwidth
              626  LOAD_METHOD              text
              628  CALL_METHOD_0         0  '0 positional arguments'
              630  CALL_METHOD_1         1  '1 positional argument'
              632  STORE_FAST               '_patch_width'

 L. 512       634  LOAD_GLOBAL              basic_data
              636  LOAD_METHOD              str2int
              638  LOAD_DEREF               'self'
              640  LOAD_ATTR                ldtmaskdepth
              642  LOAD_METHOD              text
              644  CALL_METHOD_0         0  '0 positional arguments'
              646  CALL_METHOD_1         1  '1 positional argument'
              648  STORE_FAST               '_patch_depth'

 L. 513       650  LOAD_GLOBAL              basic_data
              652  LOAD_METHOD              str2int
              654  LOAD_DEREF               'self'
              656  LOAD_ATTR                ldtpoolheight
              658  LOAD_METHOD              text
              660  CALL_METHOD_0         0  '0 positional arguments'
              662  CALL_METHOD_1         1  '1 positional argument'
              664  STORE_FAST               '_pool_height'

 L. 514       666  LOAD_GLOBAL              basic_data
              668  LOAD_METHOD              str2int
              670  LOAD_DEREF               'self'
              672  LOAD_ATTR                ldtpoolwidth
              674  LOAD_METHOD              text
              676  CALL_METHOD_0         0  '0 positional arguments'
              678  CALL_METHOD_1         1  '1 positional argument'
              680  STORE_FAST               '_pool_width'

 L. 515       682  LOAD_GLOBAL              basic_data
              684  LOAD_METHOD              str2int
              686  LOAD_DEREF               'self'
              688  LOAD_ATTR                ldtpooldepth
              690  LOAD_METHOD              text
              692  CALL_METHOD_0         0  '0 positional arguments'
              694  CALL_METHOD_1         1  '1 positional argument'
              696  STORE_FAST               '_pool_depth'

 L. 516       698  LOAD_GLOBAL              basic_data
              700  LOAD_METHOD              str2int
              702  LOAD_DEREF               'self'
              704  LOAD_ATTR                ldtnepoch
              706  LOAD_METHOD              text
              708  CALL_METHOD_0         0  '0 positional arguments'
              710  CALL_METHOD_1         1  '1 positional argument'
              712  STORE_FAST               '_nepoch'

 L. 517       714  LOAD_GLOBAL              basic_data
              716  LOAD_METHOD              str2int
              718  LOAD_DEREF               'self'
              720  LOAD_ATTR                ldtbatchsize
              722  LOAD_METHOD              text
              724  CALL_METHOD_0         0  '0 positional arguments'
              726  CALL_METHOD_1         1  '1 positional argument'
              728  STORE_FAST               '_batchsize'

 L. 518       730  LOAD_GLOBAL              basic_data
              732  LOAD_METHOD              str2float
              734  LOAD_DEREF               'self'
              736  LOAD_ATTR                ldtlearnrate
              738  LOAD_METHOD              text
              740  CALL_METHOD_0         0  '0 positional arguments'
              742  CALL_METHOD_1         1  '1 positional argument'
              744  STORE_FAST               '_learning_rate'

 L. 519       746  LOAD_GLOBAL              basic_data
              748  LOAD_METHOD              str2float
              750  LOAD_DEREF               'self'
              752  LOAD_ATTR                ldtfcdropout
              754  LOAD_METHOD              text
              756  CALL_METHOD_0         0  '0 positional arguments'
              758  CALL_METHOD_1         1  '1 positional argument'
              760  STORE_FAST               '_dropout_prob_fclayer'

 L. 520       762  LOAD_FAST                '_nconvblock'
              764  LOAD_CONST               False
              766  COMPARE_OP               is
          768_770  POP_JUMP_IF_TRUE    782  'to 782'
              772  LOAD_FAST                '_nconvblock'
              774  LOAD_CONST               0
              776  COMPARE_OP               <=
          778_780  POP_JUMP_IF_FALSE   818  'to 818'
            782_0  COME_FROM           768  '768'

 L. 521       782  LOAD_GLOBAL              vis_msg
              784  LOAD_ATTR                print
              786  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: Non-positive convolutional block number'
              788  LOAD_STR                 'error'
              790  LOAD_CONST               ('type',)
              792  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              794  POP_TOP          

 L. 522       796  LOAD_GLOBAL              QtWidgets
              798  LOAD_ATTR                QMessageBox
              800  LOAD_METHOD              critical
              802  LOAD_DEREF               'self'
              804  LOAD_ATTR                msgbox

 L. 523       806  LOAD_STR                 'Train 3D-CNN'

 L. 524       808  LOAD_STR                 'Non-positive convolutional block number'
              810  CALL_METHOD_3         3  '3 positional arguments'
              812  POP_TOP          

 L. 525       814  LOAD_CONST               None
              816  RETURN_VALUE     
            818_0  COME_FROM           778  '778'

 L. 526       818  SETUP_LOOP          890  'to 890'
              820  LOAD_FAST                '_nconvlayer'
              822  GET_ITER         
            824_0  COME_FROM           844  '844'
              824  FOR_ITER            888  'to 888'
              826  STORE_FAST               '_i'

 L. 527       828  LOAD_FAST                '_i'
              830  LOAD_CONST               False
              832  COMPARE_OP               is
          834_836  POP_JUMP_IF_TRUE    848  'to 848'
              838  LOAD_FAST                '_i'
              840  LOAD_CONST               1
              842  COMPARE_OP               <
          844_846  POP_JUMP_IF_FALSE   824  'to 824'
            848_0  COME_FROM           834  '834'

 L. 528       848  LOAD_GLOBAL              vis_msg
              850  LOAD_ATTR                print
              852  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: Non-positive convolutional layer number'

 L. 529       854  LOAD_STR                 'error'
              856  LOAD_CONST               ('type',)
              858  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              860  POP_TOP          

 L. 530       862  LOAD_GLOBAL              QtWidgets
              864  LOAD_ATTR                QMessageBox
              866  LOAD_METHOD              critical
              868  LOAD_DEREF               'self'
              870  LOAD_ATTR                msgbox

 L. 531       872  LOAD_STR                 'Train 3D-CNN'

 L. 532       874  LOAD_STR                 'Non-positive convolutional layer number'
              876  CALL_METHOD_3         3  '3 positional arguments'
              878  POP_TOP          

 L. 533       880  LOAD_CONST               None
              882  RETURN_VALUE     
          884_886  JUMP_BACK           824  'to 824'
              888  POP_BLOCK        
            890_0  COME_FROM_LOOP      818  '818'

 L. 534       890  SETUP_LOOP          962  'to 962'
              892  LOAD_FAST                '_nconvfeature'
              894  GET_ITER         
            896_0  COME_FROM           916  '916'
              896  FOR_ITER            960  'to 960'
              898  STORE_FAST               '_i'

 L. 535       900  LOAD_FAST                '_i'
              902  LOAD_CONST               False
              904  COMPARE_OP               is
          906_908  POP_JUMP_IF_TRUE    920  'to 920'
              910  LOAD_FAST                '_i'
              912  LOAD_CONST               1
              914  COMPARE_OP               <
          916_918  POP_JUMP_IF_FALSE   896  'to 896'
            920_0  COME_FROM           906  '906'

 L. 536       920  LOAD_GLOBAL              vis_msg
              922  LOAD_ATTR                print
              924  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: Non-positive convolutional feature number'

 L. 537       926  LOAD_STR                 'error'
              928  LOAD_CONST               ('type',)
              930  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              932  POP_TOP          

 L. 538       934  LOAD_GLOBAL              QtWidgets
              936  LOAD_ATTR                QMessageBox
              938  LOAD_METHOD              critical
              940  LOAD_DEREF               'self'
              942  LOAD_ATTR                msgbox

 L. 539       944  LOAD_STR                 'Train 3D-CNN'

 L. 540       946  LOAD_STR                 'Non-positive convolutional feature number'
              948  CALL_METHOD_3         3  '3 positional arguments'
              950  POP_TOP          

 L. 541       952  LOAD_CONST               None
              954  RETURN_VALUE     
          956_958  JUMP_BACK           896  'to 896'
              960  POP_BLOCK        
            962_0  COME_FROM_LOOP      890  '890'

 L. 542       962  LOAD_FAST                '_nfclayer'
              964  LOAD_CONST               False
              966  COMPARE_OP               is
          968_970  POP_JUMP_IF_TRUE    982  'to 982'
              972  LOAD_FAST                '_nfclayer'
              974  LOAD_CONST               0
              976  COMPARE_OP               <=
          978_980  POP_JUMP_IF_FALSE  1018  'to 1018'
            982_0  COME_FROM           968  '968'

 L. 543       982  LOAD_GLOBAL              vis_msg
              984  LOAD_ATTR                print
              986  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: Non-positive MLP layer number'
              988  LOAD_STR                 'error'
              990  LOAD_CONST               ('type',)
              992  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              994  POP_TOP          

 L. 544       996  LOAD_GLOBAL              QtWidgets
              998  LOAD_ATTR                QMessageBox
             1000  LOAD_METHOD              critical
             1002  LOAD_DEREF               'self'
             1004  LOAD_ATTR                msgbox

 L. 545      1006  LOAD_STR                 'Train 3D-CNN'

 L. 546      1008  LOAD_STR                 'Non-positive MLP layer number'
             1010  CALL_METHOD_3         3  '3 positional arguments'
             1012  POP_TOP          

 L. 547      1014  LOAD_CONST               None
             1016  RETURN_VALUE     
           1018_0  COME_FROM           978  '978'

 L. 548      1018  SETUP_LOOP         1090  'to 1090'
             1020  LOAD_FAST                '_nfcneuron'
             1022  GET_ITER         
           1024_0  COME_FROM          1044  '1044'
             1024  FOR_ITER           1088  'to 1088'
             1026  STORE_FAST               '_i'

 L. 549      1028  LOAD_FAST                '_i'
             1030  LOAD_CONST               False
             1032  COMPARE_OP               is
         1034_1036  POP_JUMP_IF_TRUE   1048  'to 1048'
             1038  LOAD_FAST                '_i'
             1040  LOAD_CONST               1
             1042  COMPARE_OP               <
         1044_1046  POP_JUMP_IF_FALSE  1024  'to 1024'
           1048_0  COME_FROM          1034  '1034'

 L. 550      1048  LOAD_GLOBAL              vis_msg
             1050  LOAD_ATTR                print
             1052  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: Non-positive MLP neuron number'
             1054  LOAD_STR                 'error'
             1056  LOAD_CONST               ('type',)
             1058  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1060  POP_TOP          

 L. 551      1062  LOAD_GLOBAL              QtWidgets
             1064  LOAD_ATTR                QMessageBox
             1066  LOAD_METHOD              critical
             1068  LOAD_DEREF               'self'
             1070  LOAD_ATTR                msgbox

 L. 552      1072  LOAD_STR                 'Train 3D-CNN'

 L. 553      1074  LOAD_STR                 'Non-positive MLP neuron number'
             1076  CALL_METHOD_3         3  '3 positional arguments'
             1078  POP_TOP          

 L. 554      1080  LOAD_CONST               None
             1082  RETURN_VALUE     
         1084_1086  JUMP_BACK          1024  'to 1024'
             1088  POP_BLOCK        
           1090_0  COME_FROM_LOOP     1018  '1018'

 L. 555      1090  LOAD_FAST                '_patch_height'
             1092  LOAD_CONST               False
             1094  COMPARE_OP               is
         1096_1098  POP_JUMP_IF_TRUE   1150  'to 1150'
             1100  LOAD_FAST                '_patch_width'
             1102  LOAD_CONST               False
             1104  COMPARE_OP               is
         1106_1108  POP_JUMP_IF_TRUE   1150  'to 1150'
             1110  LOAD_FAST                '_patch_depth'
             1112  LOAD_CONST               False
             1114  COMPARE_OP               is
         1116_1118  POP_JUMP_IF_TRUE   1150  'to 1150'

 L. 556      1120  LOAD_FAST                '_patch_height'
             1122  LOAD_CONST               1
             1124  COMPARE_OP               <
         1126_1128  POP_JUMP_IF_TRUE   1150  'to 1150'
             1130  LOAD_FAST                '_patch_width'
             1132  LOAD_CONST               1
             1134  COMPARE_OP               <
         1136_1138  POP_JUMP_IF_TRUE   1150  'to 1150'
             1140  LOAD_FAST                '_patch_depth'
             1142  LOAD_CONST               1
             1144  COMPARE_OP               <
         1146_1148  POP_JUMP_IF_FALSE  1186  'to 1186'
           1150_0  COME_FROM          1136  '1136'
           1150_1  COME_FROM          1126  '1126'
           1150_2  COME_FROM          1116  '1116'
           1150_3  COME_FROM          1106  '1106'
           1150_4  COME_FROM          1096  '1096'

 L. 557      1150  LOAD_GLOBAL              vis_msg
             1152  LOAD_ATTR                print
             1154  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: Non-positive convolutional patch size'
             1156  LOAD_STR                 'error'
             1158  LOAD_CONST               ('type',)
             1160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1162  POP_TOP          

 L. 558      1164  LOAD_GLOBAL              QtWidgets
             1166  LOAD_ATTR                QMessageBox
             1168  LOAD_METHOD              critical
             1170  LOAD_DEREF               'self'
             1172  LOAD_ATTR                msgbox

 L. 559      1174  LOAD_STR                 'Train 3D-CNN'

 L. 560      1176  LOAD_STR                 'Non-positive convolutional patch size'
             1178  CALL_METHOD_3         3  '3 positional arguments'
             1180  POP_TOP          

 L. 561      1182  LOAD_CONST               None
             1184  RETURN_VALUE     
           1186_0  COME_FROM          1146  '1146'

 L. 562      1186  LOAD_FAST                '_pool_height'
             1188  LOAD_CONST               False
             1190  COMPARE_OP               is
         1192_1194  POP_JUMP_IF_TRUE   1246  'to 1246'
             1196  LOAD_FAST                '_pool_width'
             1198  LOAD_CONST               False
             1200  COMPARE_OP               is
         1202_1204  POP_JUMP_IF_TRUE   1246  'to 1246'
             1206  LOAD_FAST                '_pool_depth'
             1208  LOAD_CONST               False
             1210  COMPARE_OP               is
         1212_1214  POP_JUMP_IF_TRUE   1246  'to 1246'

 L. 563      1216  LOAD_FAST                '_pool_height'
             1218  LOAD_CONST               1
             1220  COMPARE_OP               <
         1222_1224  POP_JUMP_IF_TRUE   1246  'to 1246'
             1226  LOAD_FAST                '_pool_width'
             1228  LOAD_CONST               1
             1230  COMPARE_OP               <
         1232_1234  POP_JUMP_IF_TRUE   1246  'to 1246'
             1236  LOAD_FAST                '_pool_depth'
             1238  LOAD_CONST               1
             1240  COMPARE_OP               <
         1242_1244  POP_JUMP_IF_FALSE  1282  'to 1282'
           1246_0  COME_FROM          1232  '1232'
           1246_1  COME_FROM          1222  '1222'
           1246_2  COME_FROM          1212  '1212'
           1246_3  COME_FROM          1202  '1202'
           1246_4  COME_FROM          1192  '1192'

 L. 564      1246  LOAD_GLOBAL              vis_msg
             1248  LOAD_ATTR                print
             1250  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: Non-positive pooling size'
             1252  LOAD_STR                 'error'
             1254  LOAD_CONST               ('type',)
             1256  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1258  POP_TOP          

 L. 565      1260  LOAD_GLOBAL              QtWidgets
             1262  LOAD_ATTR                QMessageBox
             1264  LOAD_METHOD              critical
             1266  LOAD_DEREF               'self'
             1268  LOAD_ATTR                msgbox

 L. 566      1270  LOAD_STR                 'Train 3D-CNN'

 L. 567      1272  LOAD_STR                 'Non-positive pooling size'
             1274  CALL_METHOD_3         3  '3 positional arguments'
             1276  POP_TOP          

 L. 568      1278  LOAD_CONST               None
             1280  RETURN_VALUE     
           1282_0  COME_FROM          1242  '1242'

 L. 569      1282  LOAD_FAST                '_nepoch'
             1284  LOAD_CONST               False
             1286  COMPARE_OP               is
         1288_1290  POP_JUMP_IF_TRUE   1302  'to 1302'
             1292  LOAD_FAST                '_nepoch'
             1294  LOAD_CONST               0
             1296  COMPARE_OP               <=
         1298_1300  POP_JUMP_IF_FALSE  1338  'to 1338'
           1302_0  COME_FROM          1288  '1288'

 L. 570      1302  LOAD_GLOBAL              vis_msg
             1304  LOAD_ATTR                print
             1306  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: Non-positive epoch number'
             1308  LOAD_STR                 'error'
             1310  LOAD_CONST               ('type',)
             1312  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1314  POP_TOP          

 L. 571      1316  LOAD_GLOBAL              QtWidgets
             1318  LOAD_ATTR                QMessageBox
             1320  LOAD_METHOD              critical
             1322  LOAD_DEREF               'self'
             1324  LOAD_ATTR                msgbox

 L. 572      1326  LOAD_STR                 'Train 3D-CNN'

 L. 573      1328  LOAD_STR                 'Non-positive epoch number'
             1330  CALL_METHOD_3         3  '3 positional arguments'
             1332  POP_TOP          

 L. 574      1334  LOAD_CONST               None
             1336  RETURN_VALUE     
           1338_0  COME_FROM          1298  '1298'

 L. 575      1338  LOAD_FAST                '_batchsize'
             1340  LOAD_CONST               False
             1342  COMPARE_OP               is
         1344_1346  POP_JUMP_IF_TRUE   1358  'to 1358'
             1348  LOAD_FAST                '_batchsize'
             1350  LOAD_CONST               0
             1352  COMPARE_OP               <=
         1354_1356  POP_JUMP_IF_FALSE  1394  'to 1394'
           1358_0  COME_FROM          1344  '1344'

 L. 576      1358  LOAD_GLOBAL              vis_msg
             1360  LOAD_ATTR                print
             1362  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: Non-positive batch size'
             1364  LOAD_STR                 'error'
             1366  LOAD_CONST               ('type',)
             1368  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1370  POP_TOP          

 L. 577      1372  LOAD_GLOBAL              QtWidgets
             1374  LOAD_ATTR                QMessageBox
             1376  LOAD_METHOD              critical
             1378  LOAD_DEREF               'self'
             1380  LOAD_ATTR                msgbox

 L. 578      1382  LOAD_STR                 'Train 3D-CNN'

 L. 579      1384  LOAD_STR                 'Non-positive batch size'
             1386  CALL_METHOD_3         3  '3 positional arguments'
             1388  POP_TOP          

 L. 580      1390  LOAD_CONST               None
             1392  RETURN_VALUE     
           1394_0  COME_FROM          1354  '1354'

 L. 581      1394  LOAD_FAST                '_learning_rate'
             1396  LOAD_CONST               False
             1398  COMPARE_OP               is
         1400_1402  POP_JUMP_IF_TRUE   1414  'to 1414'
             1404  LOAD_FAST                '_learning_rate'
             1406  LOAD_CONST               0
             1408  COMPARE_OP               <=
         1410_1412  POP_JUMP_IF_FALSE  1450  'to 1450'
           1414_0  COME_FROM          1400  '1400'

 L. 582      1414  LOAD_GLOBAL              vis_msg
             1416  LOAD_ATTR                print
             1418  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: Non-positive learning rate'
             1420  LOAD_STR                 'error'
             1422  LOAD_CONST               ('type',)
             1424  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1426  POP_TOP          

 L. 583      1428  LOAD_GLOBAL              QtWidgets
             1430  LOAD_ATTR                QMessageBox
             1432  LOAD_METHOD              critical
             1434  LOAD_DEREF               'self'
             1436  LOAD_ATTR                msgbox

 L. 584      1438  LOAD_STR                 'Train 3D-CNN'

 L. 585      1440  LOAD_STR                 'Non-positive learning rate'
             1442  CALL_METHOD_3         3  '3 positional arguments'
             1444  POP_TOP          

 L. 586      1446  LOAD_CONST               None
             1448  RETURN_VALUE     
           1450_0  COME_FROM          1410  '1410'

 L. 587      1450  LOAD_FAST                '_dropout_prob_fclayer'
             1452  LOAD_CONST               False
             1454  COMPARE_OP               is
         1456_1458  POP_JUMP_IF_TRUE   1470  'to 1470'
             1460  LOAD_FAST                '_dropout_prob_fclayer'
             1462  LOAD_CONST               0
             1464  COMPARE_OP               <=
         1466_1468  POP_JUMP_IF_FALSE  1506  'to 1506'
           1470_0  COME_FROM          1456  '1456'

 L. 588      1470  LOAD_GLOBAL              vis_msg
             1472  LOAD_ATTR                print
             1474  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: Negative dropout rate'
             1476  LOAD_STR                 'error'
             1478  LOAD_CONST               ('type',)
             1480  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1482  POP_TOP          

 L. 589      1484  LOAD_GLOBAL              QtWidgets
             1486  LOAD_ATTR                QMessageBox
             1488  LOAD_METHOD              critical
             1490  LOAD_DEREF               'self'
             1492  LOAD_ATTR                msgbox

 L. 590      1494  LOAD_STR                 'Train 3D-CNN'

 L. 591      1496  LOAD_STR                 'Negative dropout rate'
             1498  CALL_METHOD_3         3  '3 positional arguments'
             1500  POP_TOP          

 L. 592      1502  LOAD_CONST               None
             1504  RETURN_VALUE     
           1506_0  COME_FROM          1466  '1466'

 L. 594      1506  LOAD_GLOBAL              len
             1508  LOAD_DEREF               'self'
             1510  LOAD_ATTR                ldtsave
             1512  LOAD_METHOD              text
             1514  CALL_METHOD_0         0  '0 positional arguments'
             1516  CALL_FUNCTION_1       1  '1 positional argument'
             1518  LOAD_CONST               1
             1520  COMPARE_OP               <
         1522_1524  POP_JUMP_IF_FALSE  1562  'to 1562'

 L. 595      1526  LOAD_GLOBAL              vis_msg
             1528  LOAD_ATTR                print
             1530  LOAD_STR                 'EROR in TrainMl3DCnnFromScratch: No name specified for CNN network'
             1532  LOAD_STR                 'error'
             1534  LOAD_CONST               ('type',)
             1536  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1538  POP_TOP          

 L. 596      1540  LOAD_GLOBAL              QtWidgets
             1542  LOAD_ATTR                QMessageBox
             1544  LOAD_METHOD              critical
             1546  LOAD_DEREF               'self'
             1548  LOAD_ATTR                msgbox

 L. 597      1550  LOAD_STR                 'Train 3D-CNN'

 L. 598      1552  LOAD_STR                 'No name specified for CNN network'
             1554  CALL_METHOD_3         3  '3 positional arguments'
             1556  POP_TOP          

 L. 599      1558  LOAD_CONST               None
             1560  RETURN_VALUE     
           1562_0  COME_FROM          1522  '1522'

 L. 600      1562  LOAD_GLOBAL              os
             1564  LOAD_ATTR                path
             1566  LOAD_METHOD              dirname
             1568  LOAD_DEREF               'self'
             1570  LOAD_ATTR                ldtsave
             1572  LOAD_METHOD              text
             1574  CALL_METHOD_0         0  '0 positional arguments'
             1576  CALL_METHOD_1         1  '1 positional argument'
             1578  STORE_FAST               '_savepath'

 L. 601      1580  LOAD_GLOBAL              os
             1582  LOAD_ATTR                path
             1584  LOAD_METHOD              splitext
             1586  LOAD_GLOBAL              os
             1588  LOAD_ATTR                path
             1590  LOAD_METHOD              basename
             1592  LOAD_DEREF               'self'
             1594  LOAD_ATTR                ldtsave
             1596  LOAD_METHOD              text
             1598  CALL_METHOD_0         0  '0 positional arguments'
             1600  CALL_METHOD_1         1  '1 positional argument'
             1602  CALL_METHOD_1         1  '1 positional argument'
             1604  LOAD_CONST               0
             1606  BINARY_SUBSCR    
             1608  STORE_FAST               '_savename'

 L. 603      1610  LOAD_GLOBAL              int
             1612  LOAD_FAST                '_video_depth_old'
             1614  LOAD_CONST               2
             1616  BINARY_TRUE_DIVIDE
             1618  CALL_FUNCTION_1       1  '1 positional argument'
             1620  STORE_FAST               '_wdinl'

 L. 604      1622  LOAD_GLOBAL              int
             1624  LOAD_FAST                '_video_width_old'
             1626  LOAD_CONST               2
             1628  BINARY_TRUE_DIVIDE
             1630  CALL_FUNCTION_1       1  '1 positional argument'
             1632  STORE_FAST               '_wdxl'

 L. 605      1634  LOAD_GLOBAL              int
             1636  LOAD_FAST                '_video_height_old'
             1638  LOAD_CONST               2
             1640  BINARY_TRUE_DIVIDE
             1642  CALL_FUNCTION_1       1  '1 positional argument'
             1644  STORE_FAST               '_wdz'

 L. 607      1646  LOAD_DEREF               'self'
             1648  LOAD_ATTR                survinfo
             1650  STORE_FAST               '_seisinfo'

 L. 609      1652  LOAD_GLOBAL              print
             1654  LOAD_STR                 'TrainMl3DCnnFromScratchFromScratch: Step 1 - Get training samples:'
             1656  CALL_FUNCTION_1       1  '1 positional argument'
             1658  POP_TOP          

 L. 610      1660  LOAD_DEREF               'self'
             1662  LOAD_ATTR                traindataconfig
             1664  LOAD_STR                 'TrainPointSet'
             1666  BINARY_SUBSCR    
             1668  STORE_FAST               '_trainpoint'

 L. 611      1670  LOAD_GLOBAL              np
             1672  LOAD_METHOD              zeros
             1674  LOAD_CONST               0
             1676  LOAD_CONST               3
             1678  BUILD_LIST_2          2 
             1680  CALL_METHOD_1         1  '1 positional argument'
             1682  STORE_FAST               '_traindata'

 L. 612      1684  SETUP_LOOP         1760  'to 1760'
             1686  LOAD_FAST                '_trainpoint'
             1688  GET_ITER         
           1690_0  COME_FROM          1708  '1708'
             1690  FOR_ITER           1758  'to 1758'
             1692  STORE_FAST               '_p'

 L. 613      1694  LOAD_GLOBAL              point_ays
             1696  LOAD_METHOD              checkPoint
             1698  LOAD_DEREF               'self'
             1700  LOAD_ATTR                pointsetdata
             1702  LOAD_FAST                '_p'
             1704  BINARY_SUBSCR    
             1706  CALL_METHOD_1         1  '1 positional argument'
         1708_1710  POP_JUMP_IF_FALSE  1690  'to 1690'

 L. 614      1712  LOAD_GLOBAL              basic_mdt
             1714  LOAD_METHOD              exportMatDict
             1716  LOAD_DEREF               'self'
             1718  LOAD_ATTR                pointsetdata
             1720  LOAD_FAST                '_p'
             1722  BINARY_SUBSCR    
             1724  LOAD_STR                 'Inline'
             1726  LOAD_STR                 'Crossline'
             1728  LOAD_STR                 'Z'
             1730  BUILD_LIST_3          3 
             1732  CALL_METHOD_2         2  '2 positional arguments'
             1734  STORE_FAST               '_pt'

 L. 615      1736  LOAD_GLOBAL              np
             1738  LOAD_ATTR                concatenate
             1740  LOAD_FAST                '_traindata'
             1742  LOAD_FAST                '_pt'
             1744  BUILD_TUPLE_2         2 
             1746  LOAD_CONST               0
             1748  LOAD_CONST               ('axis',)
             1750  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1752  STORE_FAST               '_traindata'
         1754_1756  JUMP_BACK          1690  'to 1690'
             1758  POP_BLOCK        
           1760_0  COME_FROM_LOOP     1684  '1684'

 L. 616      1760  LOAD_GLOBAL              seis_ays
             1762  LOAD_ATTR                removeOutofSurveySample
             1764  LOAD_FAST                '_traindata'

 L. 617      1766  LOAD_FAST                '_seisinfo'
             1768  LOAD_STR                 'ILStart'
             1770  BINARY_SUBSCR    
             1772  LOAD_FAST                '_wdinl'
             1774  LOAD_FAST                '_seisinfo'
             1776  LOAD_STR                 'ILStep'
             1778  BINARY_SUBSCR    
             1780  BINARY_MULTIPLY  
             1782  BINARY_ADD       

 L. 618      1784  LOAD_FAST                '_seisinfo'
             1786  LOAD_STR                 'ILEnd'
             1788  BINARY_SUBSCR    
             1790  LOAD_FAST                '_wdinl'
             1792  LOAD_FAST                '_seisinfo'
             1794  LOAD_STR                 'ILStep'
             1796  BINARY_SUBSCR    
             1798  BINARY_MULTIPLY  
             1800  BINARY_SUBTRACT  

 L. 619      1802  LOAD_FAST                '_seisinfo'
             1804  LOAD_STR                 'XLStart'
             1806  BINARY_SUBSCR    
             1808  LOAD_FAST                '_wdxl'
             1810  LOAD_FAST                '_seisinfo'
             1812  LOAD_STR                 'XLStep'
             1814  BINARY_SUBSCR    
             1816  BINARY_MULTIPLY  
             1818  BINARY_ADD       

 L. 620      1820  LOAD_FAST                '_seisinfo'
             1822  LOAD_STR                 'XLEnd'
             1824  BINARY_SUBSCR    
             1826  LOAD_FAST                '_wdxl'
             1828  LOAD_FAST                '_seisinfo'
             1830  LOAD_STR                 'XLStep'
             1832  BINARY_SUBSCR    
             1834  BINARY_MULTIPLY  
             1836  BINARY_SUBTRACT  

 L. 621      1838  LOAD_FAST                '_seisinfo'
             1840  LOAD_STR                 'ZStart'
             1842  BINARY_SUBSCR    
             1844  LOAD_FAST                '_wdz'
             1846  LOAD_FAST                '_seisinfo'
             1848  LOAD_STR                 'ZStep'
             1850  BINARY_SUBSCR    
             1852  BINARY_MULTIPLY  
             1854  BINARY_ADD       

 L. 622      1856  LOAD_FAST                '_seisinfo'
             1858  LOAD_STR                 'ZEnd'
             1860  BINARY_SUBSCR    
             1862  LOAD_FAST                '_wdz'
             1864  LOAD_FAST                '_seisinfo'
             1866  LOAD_STR                 'ZStep'
             1868  BINARY_SUBSCR    
             1870  BINARY_MULTIPLY  
             1872  BINARY_SUBTRACT  
             1874  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1876  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1878  STORE_FAST               '_traindata'

 L. 625      1880  LOAD_GLOBAL              np
             1882  LOAD_METHOD              shape
             1884  LOAD_FAST                '_traindata'
             1886  CALL_METHOD_1         1  '1 positional argument'
             1888  LOAD_CONST               0
             1890  BINARY_SUBSCR    
             1892  LOAD_CONST               0
             1894  COMPARE_OP               <=
         1896_1898  POP_JUMP_IF_FALSE  1936  'to 1936'

 L. 626      1900  LOAD_GLOBAL              vis_msg
             1902  LOAD_ATTR                print
             1904  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: No training sample found'
             1906  LOAD_STR                 'error'
             1908  LOAD_CONST               ('type',)
             1910  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1912  POP_TOP          

 L. 627      1914  LOAD_GLOBAL              QtWidgets
             1916  LOAD_ATTR                QMessageBox
             1918  LOAD_METHOD              critical
             1920  LOAD_DEREF               'self'
             1922  LOAD_ATTR                msgbox

 L. 628      1924  LOAD_STR                 'Train 3D-CNN'

 L. 629      1926  LOAD_STR                 'No training sample found'
             1928  CALL_METHOD_3         3  '3 positional arguments'
             1930  POP_TOP          

 L. 630      1932  LOAD_CONST               None
             1934  RETURN_VALUE     
           1936_0  COME_FROM          1896  '1896'

 L. 633      1936  LOAD_GLOBAL              print
             1938  LOAD_STR                 'TrainMl3DCnnFromScratch: Step 2 - Retrieve and interpolate videos: (%d, %d, %d) --> (%d, %d, %d)'

 L. 634      1940  LOAD_FAST                '_video_height_old'
             1942  LOAD_FAST                '_video_width_old'
             1944  LOAD_FAST                '_video_depth_old'

 L. 635      1946  LOAD_FAST                '_video_height_new'
             1948  LOAD_FAST                '_video_width_new'
             1950  LOAD_FAST                '_video_depth_new'
             1952  BUILD_TUPLE_6         6 
             1954  BINARY_MODULO    
             1956  CALL_FUNCTION_1       1  '1 positional argument'
             1958  POP_TOP          

 L. 636      1960  BUILD_MAP_0           0 
             1962  STORE_FAST               '_traindict'

 L. 637      1964  SETUP_LOOP         2036  'to 2036'
             1966  LOAD_FAST                '_features'
             1968  GET_ITER         
             1970  FOR_ITER           2034  'to 2034'
             1972  STORE_FAST               'f'

 L. 638      1974  LOAD_DEREF               'self'
             1976  LOAD_ATTR                seisdata
             1978  LOAD_FAST                'f'
             1980  BINARY_SUBSCR    
             1982  STORE_FAST               '_seisdata'

 L. 639      1984  LOAD_GLOBAL              seis_ays
             1986  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1988  LOAD_FAST                '_seisdata'
             1990  LOAD_FAST                '_traindata'
             1992  LOAD_DEREF               'self'
             1994  LOAD_ATTR                survinfo

 L. 640      1996  LOAD_FAST                '_wdinl'
             1998  LOAD_FAST                '_wdxl'
             2000  LOAD_FAST                '_wdz'

 L. 641      2002  LOAD_CONST               False
             2004  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2006  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2008  LOAD_CONST               None
             2010  LOAD_CONST               None
             2012  BUILD_SLICE_2         2 
             2014  LOAD_CONST               3
             2016  LOAD_CONST               None
             2018  BUILD_SLICE_2         2 
             2020  BUILD_TUPLE_2         2 
             2022  BINARY_SUBSCR    
             2024  LOAD_FAST                '_traindict'
             2026  LOAD_FAST                'f'
             2028  STORE_SUBSCR     
         2030_2032  JUMP_BACK          1970  'to 1970'
             2034  POP_BLOCK        
           2036_0  COME_FROM_LOOP     1964  '1964'

 L. 642      2036  LOAD_FAST                '_target'
             2038  LOAD_FAST                '_features'
             2040  COMPARE_OP               not-in
         2042_2044  POP_JUMP_IF_FALSE  2096  'to 2096'

 L. 643      2046  LOAD_DEREF               'self'
             2048  LOAD_ATTR                seisdata
             2050  LOAD_FAST                '_target'
             2052  BINARY_SUBSCR    
             2054  STORE_FAST               '_seisdata'

 L. 644      2056  LOAD_GLOBAL              seis_ays
             2058  LOAD_ATTR                retrieveSeisSampleFrom3DMat
             2060  LOAD_FAST                '_seisdata'
             2062  LOAD_FAST                '_traindata'
             2064  LOAD_DEREF               'self'
             2066  LOAD_ATTR                survinfo

 L. 645      2068  LOAD_CONST               False
             2070  LOAD_CONST               ('seisinfo', 'verbose')
             2072  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2074  LOAD_CONST               None
             2076  LOAD_CONST               None
             2078  BUILD_SLICE_2         2 
             2080  LOAD_CONST               3
             2082  LOAD_CONST               None
             2084  BUILD_SLICE_2         2 
             2086  BUILD_TUPLE_2         2 
             2088  BINARY_SUBSCR    
             2090  LOAD_FAST                '_traindict'
             2092  LOAD_FAST                '_target'
             2094  STORE_SUBSCR     
           2096_0  COME_FROM          2042  '2042'

 L. 647      2096  LOAD_DEREF               'self'
             2098  LOAD_ATTR                traindataconfig
             2100  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2102  BINARY_SUBSCR    
         2104_2106  POP_JUMP_IF_FALSE  2188  'to 2188'

 L. 648      2108  SETUP_LOOP         2188  'to 2188'
             2110  LOAD_FAST                '_features'
             2112  GET_ITER         
           2114_0  COME_FROM          2142  '2142'
             2114  FOR_ITER           2186  'to 2186'
             2116  STORE_FAST               'f'

 L. 649      2118  LOAD_GLOBAL              ml_aug
             2120  LOAD_METHOD              removeInvariantFeature
             2122  LOAD_FAST                '_traindict'
             2124  LOAD_FAST                'f'
             2126  CALL_METHOD_2         2  '2 positional arguments'
             2128  STORE_FAST               '_traindict'

 L. 650      2130  LOAD_GLOBAL              basic_mdt
             2132  LOAD_METHOD              maxDictConstantRow
             2134  LOAD_FAST                '_traindict'
             2136  CALL_METHOD_1         1  '1 positional argument'
             2138  LOAD_CONST               0
             2140  COMPARE_OP               <=
         2142_2144  POP_JUMP_IF_FALSE  2114  'to 2114'

 L. 651      2146  LOAD_GLOBAL              vis_msg
             2148  LOAD_ATTR                print
             2150  LOAD_STR                 'ERROR in TrainMl3DCnnFromScratch: No training sample found'
             2152  LOAD_STR                 'error'
             2154  LOAD_CONST               ('type',)
             2156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2158  POP_TOP          

 L. 652      2160  LOAD_GLOBAL              QtWidgets
             2162  LOAD_ATTR                QMessageBox
             2164  LOAD_METHOD              critical
             2166  LOAD_DEREF               'self'
             2168  LOAD_ATTR                msgbox

 L. 653      2170  LOAD_STR                 'Train 3D-CNN'

 L. 654      2172  LOAD_STR                 'No training sample found'
             2174  CALL_METHOD_3         3  '3 positional arguments'
             2176  POP_TOP          

 L. 655      2178  LOAD_CONST               None
             2180  RETURN_VALUE     
         2182_2184  JUMP_BACK          2114  'to 2114'
             2186  POP_BLOCK        
           2188_0  COME_FROM_LOOP     2108  '2108'
           2188_1  COME_FROM          2104  '2104'

 L. 657      2188  LOAD_GLOBAL              np
             2190  LOAD_METHOD              round
             2192  LOAD_FAST                '_traindict'
             2194  LOAD_FAST                '_target'
             2196  BINARY_SUBSCR    
             2198  CALL_METHOD_1         1  '1 positional argument'
             2200  LOAD_METHOD              astype
             2202  LOAD_GLOBAL              int
             2204  CALL_METHOD_1         1  '1 positional argument'
             2206  LOAD_FAST                '_traindict'
             2208  LOAD_FAST                '_target'
             2210  STORE_SUBSCR     

 L. 659      2212  LOAD_FAST                '_video_height_new'
             2214  LOAD_FAST                '_video_height_old'
             2216  COMPARE_OP               !=
         2218_2220  POP_JUMP_IF_TRUE   2242  'to 2242'

 L. 660      2222  LOAD_FAST                '_video_width_new'
             2224  LOAD_FAST                '_video_width_old'
             2226  COMPARE_OP               !=
         2228_2230  POP_JUMP_IF_TRUE   2242  'to 2242'

 L. 661      2232  LOAD_FAST                '_video_depth_new'
             2234  LOAD_FAST                '_video_depth_old'
             2236  COMPARE_OP               !=
         2238_2240  POP_JUMP_IF_FALSE  2290  'to 2290'
           2242_0  COME_FROM          2228  '2228'
           2242_1  COME_FROM          2218  '2218'

 L. 662      2242  SETUP_LOOP         2290  'to 2290'
             2244  LOAD_FAST                '_features'
             2246  GET_ITER         
             2248  FOR_ITER           2288  'to 2288'
             2250  STORE_FAST               'f'

 L. 663      2252  LOAD_GLOBAL              basic_video
             2254  LOAD_ATTR                changeVideoSize
             2256  LOAD_FAST                '_traindict'
             2258  LOAD_FAST                'f'
             2260  BINARY_SUBSCR    

 L. 664      2262  LOAD_FAST                '_video_height_old'

 L. 665      2264  LOAD_FAST                '_video_width_old'

 L. 666      2266  LOAD_FAST                '_video_depth_old'

 L. 667      2268  LOAD_FAST                '_video_height_new'

 L. 668      2270  LOAD_FAST                '_video_width_new'

 L. 669      2272  LOAD_FAST                '_video_depth_new'
             2274  LOAD_CONST               ('video_height', 'video_width', 'video_depth', 'video_height_new', 'video_width_new', 'video_depth_new')
             2276  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2278  LOAD_FAST                '_traindict'
             2280  LOAD_FAST                'f'
             2282  STORE_SUBSCR     
         2284_2286  JUMP_BACK          2248  'to 2248'
             2288  POP_BLOCK        
           2290_0  COME_FROM_LOOP     2242  '2242'
           2290_1  COME_FROM          2238  '2238'

 L. 671      2290  LOAD_GLOBAL              print
             2292  LOAD_STR                 'TrainMl3DCnnFromScratch: A total of %d valid training samples'

 L. 672      2294  LOAD_GLOBAL              basic_mdt
             2296  LOAD_METHOD              maxDictConstantRow
             2298  LOAD_FAST                '_traindict'
             2300  CALL_METHOD_1         1  '1 positional argument'
             2302  BINARY_MODULO    
             2304  CALL_FUNCTION_1       1  '1 positional argument'
             2306  POP_TOP          

 L. 674      2308  LOAD_GLOBAL              print
             2310  LOAD_STR                 'TrainMl3DCnnFromScratch: Step 3 - Balance labels'
             2312  CALL_FUNCTION_1       1  '1 positional argument'
             2314  POP_TOP          

 L. 675      2316  LOAD_DEREF               'self'
             2318  LOAD_ATTR                traindataconfig
             2320  LOAD_STR                 'BalanceTarget_Checked'
             2322  BINARY_SUBSCR    
         2324_2326  POP_JUMP_IF_FALSE  2368  'to 2368'

 L. 676      2328  LOAD_GLOBAL              ml_aug
             2330  LOAD_METHOD              balanceLabelbyExtension
             2332  LOAD_FAST                '_traindict'
             2334  LOAD_FAST                '_target'
             2336  CALL_METHOD_2         2  '2 positional arguments'
             2338  STORE_FAST               '_traindict'

 L. 677      2340  LOAD_GLOBAL              print

 L. 678      2342  LOAD_STR                 'TrainMl2DCnnFromScratch: A total of %d training samples after balance'

 L. 679      2344  LOAD_GLOBAL              np
             2346  LOAD_METHOD              shape
             2348  LOAD_FAST                '_traindict'
             2350  LOAD_FAST                '_target'
             2352  BINARY_SUBSCR    
             2354  CALL_METHOD_1         1  '1 positional argument'
             2356  LOAD_CONST               0
             2358  BINARY_SUBSCR    
             2360  BINARY_MODULO    
             2362  CALL_FUNCTION_1       1  '1 positional argument'
             2364  POP_TOP          
             2366  JUMP_FORWARD       2376  'to 2376'
           2368_0  COME_FROM          2324  '2324'

 L. 681      2368  LOAD_GLOBAL              print
             2370  LOAD_STR                 'TrainMl2DCnnFromScratch: No balance applied'
             2372  CALL_FUNCTION_1       1  '1 positional argument'
             2374  POP_TOP          
           2376_0  COME_FROM          2366  '2366'

 L. 683      2376  LOAD_GLOBAL              print
             2378  LOAD_STR                 'TrainMl3DCnnFromScratch: Step 4 - Start training'
             2380  CALL_FUNCTION_1       1  '1 positional argument'
             2382  POP_TOP          

 L. 685      2384  LOAD_GLOBAL              QtWidgets
             2386  LOAD_METHOD              QProgressDialog
             2388  CALL_METHOD_0         0  '0 positional arguments'
             2390  STORE_FAST               '_pgsdlg'

 L. 686      2392  LOAD_GLOBAL              QtGui
             2394  LOAD_METHOD              QIcon
             2396  CALL_METHOD_0         0  '0 positional arguments'
             2398  STORE_FAST               'icon'

 L. 687      2400  LOAD_FAST                'icon'
             2402  LOAD_METHOD              addPixmap
             2404  LOAD_GLOBAL              QtGui
             2406  LOAD_METHOD              QPixmap
             2408  LOAD_GLOBAL              os
             2410  LOAD_ATTR                path
             2412  LOAD_METHOD              join
             2414  LOAD_DEREF               'self'
             2416  LOAD_ATTR                iconpath
             2418  LOAD_STR                 'icons/new.png'
             2420  CALL_METHOD_2         2  '2 positional arguments'
             2422  CALL_METHOD_1         1  '1 positional argument'

 L. 688      2424  LOAD_GLOBAL              QtGui
             2426  LOAD_ATTR                QIcon
             2428  LOAD_ATTR                Normal
             2430  LOAD_GLOBAL              QtGui
             2432  LOAD_ATTR                QIcon
             2434  LOAD_ATTR                Off
             2436  CALL_METHOD_3         3  '3 positional arguments'
             2438  POP_TOP          

 L. 689      2440  LOAD_FAST                '_pgsdlg'
             2442  LOAD_METHOD              setWindowIcon
             2444  LOAD_FAST                'icon'
             2446  CALL_METHOD_1         1  '1 positional argument'
             2448  POP_TOP          

 L. 690      2450  LOAD_FAST                '_pgsdlg'
             2452  LOAD_METHOD              setWindowTitle
             2454  LOAD_STR                 'Train 3D-CNN'
             2456  CALL_METHOD_1         1  '1 positional argument'
             2458  POP_TOP          

 L. 691      2460  LOAD_FAST                '_pgsdlg'
             2462  LOAD_METHOD              setCancelButton
             2464  LOAD_CONST               None
             2466  CALL_METHOD_1         1  '1 positional argument'
             2468  POP_TOP          

 L. 692      2470  LOAD_FAST                '_pgsdlg'
             2472  LOAD_METHOD              setWindowFlags
             2474  LOAD_GLOBAL              QtCore
             2476  LOAD_ATTR                Qt
             2478  LOAD_ATTR                WindowStaysOnTopHint
             2480  CALL_METHOD_1         1  '1 positional argument'
             2482  POP_TOP          

 L. 693      2484  LOAD_FAST                '_pgsdlg'
             2486  LOAD_METHOD              forceShow
             2488  CALL_METHOD_0         0  '0 positional arguments'
             2490  POP_TOP          

 L. 694      2492  LOAD_FAST                '_pgsdlg'
             2494  LOAD_METHOD              setFixedWidth
             2496  LOAD_CONST               400
             2498  CALL_METHOD_1         1  '1 positional argument'
             2500  POP_TOP          

 L. 695      2502  LOAD_GLOBAL              ml_cnn3d
             2504  LOAD_ATTR                create3DCNNClassifier
             2506  LOAD_FAST                '_traindict'

 L. 696      2508  LOAD_FAST                '_video_height_new'

 L. 697      2510  LOAD_FAST                '_video_width_new'

 L. 698      2512  LOAD_FAST                '_video_depth_new'

 L. 699      2514  LOAD_FAST                '_features'
             2516  LOAD_FAST                '_target'

 L. 700      2518  LOAD_FAST                '_nepoch'
             2520  LOAD_FAST                '_batchsize'

 L. 701      2522  LOAD_FAST                '_nconvblock'

 L. 702      2524  LOAD_FAST                '_nconvlayer'
             2526  LOAD_FAST                '_nconvfeature'

 L. 703      2528  LOAD_FAST                '_nfclayer'
             2530  LOAD_FAST                '_nfcneuron'

 L. 704      2532  LOAD_FAST                '_patch_height'
             2534  LOAD_FAST                '_patch_width'

 L. 705      2536  LOAD_FAST                '_patch_depth'

 L. 706      2538  LOAD_FAST                '_pool_height'
             2540  LOAD_FAST                '_pool_width'

 L. 707      2542  LOAD_FAST                '_pool_depth'

 L. 708      2544  LOAD_FAST                '_learning_rate'

 L. 709      2546  LOAD_FAST                '_dropout_prob_fclayer'

 L. 710      2548  LOAD_CONST               True

 L. 711      2550  LOAD_FAST                '_savepath'
             2552  LOAD_FAST                '_savename'

 L. 712      2554  LOAD_FAST                '_pgsdlg'
             2556  LOAD_CONST               ('videoheight', 'videowidth', 'videodepth', 'features', 'target', 'nepoch', 'batchsize', 'nconvblock', 'nconvlayer', 'nconvfeature', 'nfclayer', 'nfcneuron', 'patchheight', 'patchwidth', 'patchdepth', 'poolheight', 'poolwidth', 'pooldepth', 'learningrate', 'dropoutprobfclayer', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2558  CALL_FUNCTION_KW_25    25  '25 total positional and keyword args'
             2560  STORE_FAST               '_cnnlog'

 L. 715      2562  LOAD_GLOBAL              QtWidgets
             2564  LOAD_ATTR                QMessageBox
             2566  LOAD_METHOD              information
             2568  LOAD_DEREF               'self'
             2570  LOAD_ATTR                msgbox

 L. 716      2572  LOAD_STR                 'Train 3D-CNN'

 L. 717      2574  LOAD_STR                 'CNN trained successfully'
             2576  CALL_METHOD_3         3  '3 positional arguments'
             2578  POP_TOP          

 L. 719      2580  LOAD_GLOBAL              QtWidgets
             2582  LOAD_ATTR                QMessageBox
             2584  LOAD_METHOD              question
             2586  LOAD_DEREF               'self'
             2588  LOAD_ATTR                msgbox
             2590  LOAD_STR                 'Train 3D-CNN'
             2592  LOAD_STR                 'View learning matrix?'

 L. 720      2594  LOAD_GLOBAL              QtWidgets
             2596  LOAD_ATTR                QMessageBox
             2598  LOAD_ATTR                Yes
             2600  LOAD_GLOBAL              QtWidgets
             2602  LOAD_ATTR                QMessageBox
             2604  LOAD_ATTR                No
             2606  BINARY_OR        

 L. 721      2608  LOAD_GLOBAL              QtWidgets
             2610  LOAD_ATTR                QMessageBox
             2612  LOAD_ATTR                Yes
             2614  CALL_METHOD_5         5  '5 positional arguments'
             2616  STORE_FAST               'reply'

 L. 723      2618  LOAD_FAST                'reply'
             2620  LOAD_GLOBAL              QtWidgets
             2622  LOAD_ATTR                QMessageBox
             2624  LOAD_ATTR                Yes
             2626  COMPARE_OP               ==
         2628_2630  POP_JUMP_IF_FALSE  2698  'to 2698'

 L. 724      2632  LOAD_GLOBAL              QtWidgets
             2634  LOAD_METHOD              QDialog
             2636  CALL_METHOD_0         0  '0 positional arguments'
             2638  STORE_FAST               '_viewmllearnmat'

 L. 725      2640  LOAD_GLOBAL              gui_viewmllearnmat
             2642  CALL_FUNCTION_0       0  '0 positional arguments'
             2644  STORE_FAST               '_gui'

 L. 726      2646  LOAD_FAST                '_cnnlog'
             2648  LOAD_STR                 'learning_curve'
             2650  BINARY_SUBSCR    
             2652  LOAD_FAST                '_gui'
             2654  STORE_ATTR               learnmat

 L. 727      2656  LOAD_DEREF               'self'
             2658  LOAD_ATTR                linestyle
             2660  LOAD_FAST                '_gui'
             2662  STORE_ATTR               linestyle

 L. 728      2664  LOAD_DEREF               'self'
             2666  LOAD_ATTR                fontstyle
             2668  LOAD_FAST                '_gui'
             2670  STORE_ATTR               fontstyle

 L. 729      2672  LOAD_FAST                '_gui'
             2674  LOAD_METHOD              setupGUI
             2676  LOAD_FAST                '_viewmllearnmat'
             2678  CALL_METHOD_1         1  '1 positional argument'
             2680  POP_TOP          

 L. 730      2682  LOAD_FAST                '_viewmllearnmat'
             2684  LOAD_METHOD              exec
             2686  CALL_METHOD_0         0  '0 positional arguments'
             2688  POP_TOP          

 L. 731      2690  LOAD_FAST                '_viewmllearnmat'
             2692  LOAD_METHOD              show
             2694  CALL_METHOD_0         0  '0 positional arguments'
             2696  POP_TOP          
           2698_0  COME_FROM          2628  '2628'

Parse error at or near `POP_TOP' instruction at offset 2696

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
    TrainMl3DCnnFromScratch = QtWidgets.QWidget()
    gui = trainml3dcnnfromscratch()
    gui.setupGUI(TrainMl3DCnnFromScratch)
    TrainMl3DCnnFromScratch.show()
    sys.exit(app.exec_())