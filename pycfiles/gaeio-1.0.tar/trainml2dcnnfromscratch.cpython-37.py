# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml2dcnnfromscratch.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 42814 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.pointset.analysis as point_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.image as basic_image
import cognitivegeo.src.ml.augmentation as ml_aug
import cognitivegeo.src.ml.cnnclassifier as ml_cnn
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml2dcnnfromscratch(object):
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
    traindataconfig['RotateFeature_Enabled'] = True
    traindataconfig['RotateFeature_Checked'] = False
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False

    def setupGUI(self, TrainMl2DCnnFromScratch):
        TrainMl2DCnnFromScratch.setObjectName('TrainMl2DCnnFromScratch')
        TrainMl2DCnnFromScratch.setFixedSize(800, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl2DCnnFromScratch.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl2DCnnFromScratch)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl2DCnnFromScratch)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl2DCnnFromScratch)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 50, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 50, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl2DCnnFromScratch)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 90, 180, 180))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 50, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 50, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(TrainMl2DCnnFromScratch)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 90, 180, 180))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl2DCnnFromScratch)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 310, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 350, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.lblfcdropout = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblfcdropout.setObjectName('lblfcdropout')
        self.lblfcdropout.setGeometry(QtCore.QRect(210, 390, 130, 30))
        self.ldtfcdropout = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtfcdropout.setObjectName('ldtfcdropout')
        self.ldtfcdropout.setGeometry(QtCore.QRect(350, 390, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl2DCnnFromScratch)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 100, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl2DCnnFromScratch)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(110, 440, 210, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl2DCnnFromScratch)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 440, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl2DCnnFromScratch)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl2DCnnFromScratch)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl2DCnnFromScratch.geometry().center().x()
        _center_y = TrainMl2DCnnFromScratch.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl2DCnnFromScratch)
        QtCore.QMetaObject.connectSlotsByName(TrainMl2DCnnFromScratch)

    def retranslateGUI(self, TrainMl2DCnnFromScratch):
        self.dialog = TrainMl2DCnnFromScratch
        _translate = QtCore.QCoreApplication.translate
        TrainMl2DCnnFromScratch.setWindowTitle(_translate('TrainMl2DCnnFromScratch', 'Train 2D-CNN from scratch'))
        self.lblfeature.setText(_translate('TrainMl2DCnnFromScratch', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl2DCnnFromScratch', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl2DCnnFromScratch', 'Select target:'))
        self.lbloldsize.setText(_translate('TrainMl2DCnnFromScratch', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl2DCnnFromScratch', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl2DCnnFromScratch', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl2DCnnFromScratch', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl2DCnnFromScratch', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl2DCnnFromScratch', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl2DCnnFromScratch', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl2DCnnFromScratch', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl2DCnnFromScratch', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl2DCnnFromScratch', '32'))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        if self.checkSurvInfo():
            self.featurelist.clear()
            self.lwgfeature.clear()
            self.cbbtarget.clear()
            _firstfeature = None
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    self.featurelist.append(i)
                    item = QtWidgets.QListWidgetItem(self.lwgfeature)
                    item.setText(_translate('TrainMl2DCnnFromScratch', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl2DCnnFromScratch', 'Specify CNN architecture:'))
        self.lblnconvblock.setText(_translate('TrainMl2DCnnFromScratch', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl2DCnnFromScratch', '3'))
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

        self.lblnfclayer.setText(_translate('TrainMl2DCnnFromScratch', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('TrainMl2DCnnFromScratch', '2'))
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.twgnfclayer.setRowCount(2)
        for _idx in range(int(self.ldtnfclayer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl2DCnnFromScratch', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgnfclayer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgnfclayer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl2DCnnFromScratch', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl2DCnnFromScratch', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl2DCnnFromScratch', '3'))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('TrainMl2DCnnFromScratch', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl2DCnnFromScratch', '3'))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('TrainMl2DCnnFromScratch', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl2DCnnFromScratch', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl2DCnnFromScratch', '2'))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl2DCnnFromScratch', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl2DCnnFromScratch', '2'))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfcdropout.setText(_translate('TrainMl2DCnnFromScratch', 'MLP dropout rate:'))
        self.lblfcdropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtfcdropout.setText(_translate('TrainMl2DCnnFromScratch', '0.5'))
        self.ldtfcdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.btnconfigtraindata.setText(_translate('TrainMl2DCnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lblpara.setText(_translate('TrainMl2DCnnFromScratch', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl2DCnnFromScratch', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl2DCnnFromScratch', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl2DCnnFromScratch', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl2DCnnFromScratch', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl2DCnnFromScratch', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl2DCnnFromScratch', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl2DCnnFromScratch', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl2DCnnFromScratch', ''))
        self.btnsave.setText(_translate('TrainMl2DCnnFromScratch', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl2DCnnFromScratch', 'Train 2D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl2DCnnFromScratch)

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

    def clickBtnTrainMl2DCnnFromScratch--- This code section failed: ---

 L. 439         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 441         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 442        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 443        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 444        50  LOAD_STR                 'Train 2D-CNN'

 L. 445        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 446        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 448        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_image_height_old'

 L. 449        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_image_width_old'

 L. 450        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtnewheight
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_image_height_new'

 L. 451       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewwidth
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_image_width_new'

 L. 452       126  LOAD_FAST                '_image_height_old'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'
              134  LOAD_FAST                '_image_width_old'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_TRUE    158  'to 158'

 L. 453       142  LOAD_FAST                '_image_height_new'
              144  LOAD_CONST               False
              146  COMPARE_OP               is
              148  POP_JUMP_IF_TRUE    158  'to 158'
              150  LOAD_FAST                '_image_width_new'
              152  LOAD_CONST               False
              154  COMPARE_OP               is
              156  POP_JUMP_IF_FALSE   194  'to 194'
            158_0  COME_FROM           148  '148'
            158_1  COME_FROM           140  '140'
            158_2  COME_FROM           132  '132'

 L. 454       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 455       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 456       182  LOAD_STR                 'Train 2D-CNN'

 L. 457       184  LOAD_STR                 'Non-integer feature size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 458       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 459       194  LOAD_FAST                '_image_height_old'
              196  LOAD_CONST               2
              198  COMPARE_OP               <
              200  POP_JUMP_IF_TRUE    228  'to 228'
              202  LOAD_FAST                '_image_width_old'
              204  LOAD_CONST               2
              206  COMPARE_OP               <
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 460       210  LOAD_FAST                '_image_height_new'
              212  LOAD_CONST               2
              214  COMPARE_OP               <
              216  POP_JUMP_IF_TRUE    228  'to 228'
              218  LOAD_FAST                '_image_width_new'
              220  LOAD_CONST               2
              222  COMPARE_OP               <
          224_226  POP_JUMP_IF_FALSE   264  'to 264'
            228_0  COME_FROM           216  '216'
            228_1  COME_FROM           208  '208'
            228_2  COME_FROM           200  '200'

 L. 461       228  LOAD_GLOBAL              vis_msg
              230  LOAD_ATTR                print
              232  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 462       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 463       252  LOAD_STR                 'Train 2D-CNN'

 L. 464       254  LOAD_STR                 'Features are not 2D'
              256  CALL_METHOD_3         3  '3 positional arguments'
              258  POP_TOP          

 L. 465       260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           224  '224'

 L. 467       264  LOAD_CONST               2
              266  LOAD_GLOBAL              int
              268  LOAD_FAST                '_image_height_old'
              270  LOAD_CONST               2
              272  BINARY_TRUE_DIVIDE
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  BINARY_MULTIPLY  
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  STORE_FAST               '_image_height_old'

 L. 468       284  LOAD_CONST               2
              286  LOAD_GLOBAL              int
              288  LOAD_FAST                '_image_width_old'
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BINARY_MULTIPLY  
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               '_image_width_old'

 L. 470       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                lwgfeature
              308  LOAD_METHOD              selectedItems
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               '_features'

 L. 471       314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainml2dcnnfromscratch.clickBtnTrainMl2DCnnFromScratch.<locals>.<listcomp>'
              318  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              320  LOAD_FAST                '_features'
              322  GET_ITER         
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               '_features'

 L. 472       328  LOAD_DEREF               'self'
              330  LOAD_ATTR                featurelist
              332  LOAD_DEREF               'self'
              334  LOAD_ATTR                cbbtarget
              336  LOAD_METHOD              currentIndex
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  BINARY_SUBSCR    
              342  STORE_FAST               '_target'

 L. 474       344  LOAD_FAST                '_target'
              346  LOAD_FAST                '_features'
              348  COMPARE_OP               in
          350_352  POP_JUMP_IF_FALSE   390  'to 390'

 L. 475       354  LOAD_GLOBAL              vis_msg
              356  LOAD_ATTR                print
              358  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Target also used as features'
              360  LOAD_STR                 'error'
              362  LOAD_CONST               ('type',)
              364  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              366  POP_TOP          

 L. 476       368  LOAD_GLOBAL              QtWidgets
              370  LOAD_ATTR                QMessageBox
              372  LOAD_METHOD              critical
              374  LOAD_DEREF               'self'
              376  LOAD_ATTR                msgbox

 L. 477       378  LOAD_STR                 'Train 2D-CNN'

 L. 478       380  LOAD_STR                 'Target also used as features'
              382  CALL_METHOD_3         3  '3 positional arguments'
              384  POP_TOP          

 L. 479       386  LOAD_CONST               None
              388  RETURN_VALUE     
            390_0  COME_FROM           350  '350'

 L. 481       390  LOAD_GLOBAL              basic_data
              392  LOAD_METHOD              str2int
              394  LOAD_DEREF               'self'
              396  LOAD_ATTR                ldtnconvblock
              398  LOAD_METHOD              text
              400  CALL_METHOD_0         0  '0 positional arguments'
              402  CALL_METHOD_1         1  '1 positional argument'
              404  STORE_FAST               '_nconvblock'

 L. 482       406  LOAD_CLOSURE             'self'
              408  BUILD_TUPLE_1         1 
              410  LOAD_LISTCOMP            '<code_object <listcomp>>'
              412  LOAD_STR                 'trainml2dcnnfromscratch.clickBtnTrainMl2DCnnFromScratch.<locals>.<listcomp>'
              414  MAKE_FUNCTION_8          'closure'
              416  LOAD_GLOBAL              range
              418  LOAD_FAST                '_nconvblock'
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  GET_ITER         
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  STORE_FAST               '_nconvlayer'

 L. 483       428  LOAD_CLOSURE             'self'
              430  BUILD_TUPLE_1         1 
              432  LOAD_LISTCOMP            '<code_object <listcomp>>'
              434  LOAD_STR                 'trainml2dcnnfromscratch.clickBtnTrainMl2DCnnFromScratch.<locals>.<listcomp>'
              436  MAKE_FUNCTION_8          'closure'
              438  LOAD_GLOBAL              range
              440  LOAD_FAST                '_nconvblock'
              442  CALL_FUNCTION_1       1  '1 positional argument'
              444  GET_ITER         
              446  CALL_FUNCTION_1       1  '1 positional argument'
              448  STORE_FAST               '_nconvfeature'

 L. 484       450  LOAD_GLOBAL              basic_data
              452  LOAD_METHOD              str2int
              454  LOAD_DEREF               'self'
              456  LOAD_ATTR                ldtnfclayer
              458  LOAD_METHOD              text
              460  CALL_METHOD_0         0  '0 positional arguments'
              462  CALL_METHOD_1         1  '1 positional argument'
              464  STORE_FAST               '_nfclayer'

 L. 485       466  LOAD_CLOSURE             'self'
              468  BUILD_TUPLE_1         1 
              470  LOAD_LISTCOMP            '<code_object <listcomp>>'
              472  LOAD_STR                 'trainml2dcnnfromscratch.clickBtnTrainMl2DCnnFromScratch.<locals>.<listcomp>'
              474  MAKE_FUNCTION_8          'closure'
              476  LOAD_GLOBAL              range
              478  LOAD_FAST                '_nfclayer'
              480  CALL_FUNCTION_1       1  '1 positional argument'
              482  GET_ITER         
              484  CALL_FUNCTION_1       1  '1 positional argument'
              486  STORE_FAST               '_nfcneuron'

 L. 486       488  LOAD_GLOBAL              basic_data
              490  LOAD_METHOD              str2int
              492  LOAD_DEREF               'self'
              494  LOAD_ATTR                ldtmaskheight
              496  LOAD_METHOD              text
              498  CALL_METHOD_0         0  '0 positional arguments'
              500  CALL_METHOD_1         1  '1 positional argument'
              502  STORE_FAST               '_patch_height'

 L. 487       504  LOAD_GLOBAL              basic_data
              506  LOAD_METHOD              str2int
              508  LOAD_DEREF               'self'
              510  LOAD_ATTR                ldtmaskwidth
              512  LOAD_METHOD              text
              514  CALL_METHOD_0         0  '0 positional arguments'
              516  CALL_METHOD_1         1  '1 positional argument'
              518  STORE_FAST               '_patch_width'

 L. 488       520  LOAD_GLOBAL              basic_data
              522  LOAD_METHOD              str2int
              524  LOAD_DEREF               'self'
              526  LOAD_ATTR                ldtpoolheight
              528  LOAD_METHOD              text
              530  CALL_METHOD_0         0  '0 positional arguments'
              532  CALL_METHOD_1         1  '1 positional argument'
              534  STORE_FAST               '_pool_height'

 L. 489       536  LOAD_GLOBAL              basic_data
              538  LOAD_METHOD              str2int
              540  LOAD_DEREF               'self'
              542  LOAD_ATTR                ldtpoolwidth
              544  LOAD_METHOD              text
              546  CALL_METHOD_0         0  '0 positional arguments'
              548  CALL_METHOD_1         1  '1 positional argument'
              550  STORE_FAST               '_pool_width'

 L. 490       552  LOAD_GLOBAL              basic_data
              554  LOAD_METHOD              str2int
              556  LOAD_DEREF               'self'
              558  LOAD_ATTR                ldtnepoch
              560  LOAD_METHOD              text
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  CALL_METHOD_1         1  '1 positional argument'
              566  STORE_FAST               '_nepoch'

 L. 491       568  LOAD_GLOBAL              basic_data
              570  LOAD_METHOD              str2int
              572  LOAD_DEREF               'self'
              574  LOAD_ATTR                ldtbatchsize
              576  LOAD_METHOD              text
              578  CALL_METHOD_0         0  '0 positional arguments'
              580  CALL_METHOD_1         1  '1 positional argument'
              582  STORE_FAST               '_batchsize'

 L. 492       584  LOAD_GLOBAL              float
              586  LOAD_DEREF               'self'
              588  LOAD_ATTR                ldtlearnrate
              590  LOAD_METHOD              text
              592  CALL_METHOD_0         0  '0 positional arguments'
              594  CALL_FUNCTION_1       1  '1 positional argument'
              596  STORE_FAST               '_learning_rate'

 L. 493       598  LOAD_GLOBAL              float
              600  LOAD_DEREF               'self'
              602  LOAD_ATTR                ldtfcdropout
              604  LOAD_METHOD              text
              606  CALL_METHOD_0         0  '0 positional arguments'
              608  CALL_FUNCTION_1       1  '1 positional argument'
              610  STORE_FAST               '_dropout_prob_fclayer'

 L. 494       612  LOAD_FAST                '_nconvblock'
              614  LOAD_CONST               False
              616  COMPARE_OP               is
          618_620  POP_JUMP_IF_TRUE    632  'to 632'
              622  LOAD_FAST                '_nconvblock'
              624  LOAD_CONST               0
              626  COMPARE_OP               <=
          628_630  POP_JUMP_IF_FALSE   668  'to 668'
            632_0  COME_FROM           618  '618'

 L. 495       632  LOAD_GLOBAL              vis_msg
              634  LOAD_ATTR                print
              636  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Non-positive convolutional block number'

 L. 496       638  LOAD_STR                 'error'
              640  LOAD_CONST               ('type',)
              642  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              644  POP_TOP          

 L. 497       646  LOAD_GLOBAL              QtWidgets
              648  LOAD_ATTR                QMessageBox
              650  LOAD_METHOD              critical
              652  LOAD_DEREF               'self'
              654  LOAD_ATTR                msgbox

 L. 498       656  LOAD_STR                 'Train 2D-CNN'

 L. 499       658  LOAD_STR                 'Non-positive convolutional block number'
              660  CALL_METHOD_3         3  '3 positional arguments'
              662  POP_TOP          

 L. 500       664  LOAD_CONST               None
              666  RETURN_VALUE     
            668_0  COME_FROM           628  '628'

 L. 501       668  SETUP_LOOP          740  'to 740'
              670  LOAD_FAST                '_nconvlayer'
              672  GET_ITER         
            674_0  COME_FROM           694  '694'
              674  FOR_ITER            738  'to 738'
              676  STORE_FAST               '_i'

 L. 502       678  LOAD_FAST                '_i'
              680  LOAD_CONST               False
              682  COMPARE_OP               is
          684_686  POP_JUMP_IF_TRUE    698  'to 698'
              688  LOAD_FAST                '_i'
              690  LOAD_CONST               1
              692  COMPARE_OP               <
          694_696  POP_JUMP_IF_FALSE   674  'to 674'
            698_0  COME_FROM           684  '684'

 L. 503       698  LOAD_GLOBAL              vis_msg
              700  LOAD_ATTR                print
              702  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Non-positive convolutional layer number'

 L. 504       704  LOAD_STR                 'error'
              706  LOAD_CONST               ('type',)
              708  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              710  POP_TOP          

 L. 505       712  LOAD_GLOBAL              QtWidgets
              714  LOAD_ATTR                QMessageBox
              716  LOAD_METHOD              critical
              718  LOAD_DEREF               'self'
              720  LOAD_ATTR                msgbox

 L. 506       722  LOAD_STR                 'Train 2D-CNN'

 L. 507       724  LOAD_STR                 'Non-positive convolutional layer number'
              726  CALL_METHOD_3         3  '3 positional arguments'
              728  POP_TOP          

 L. 508       730  LOAD_CONST               None
              732  RETURN_VALUE     
          734_736  JUMP_BACK           674  'to 674'
              738  POP_BLOCK        
            740_0  COME_FROM_LOOP      668  '668'

 L. 509       740  SETUP_LOOP          812  'to 812'
              742  LOAD_FAST                '_nconvfeature'
              744  GET_ITER         
            746_0  COME_FROM           766  '766'
              746  FOR_ITER            810  'to 810'
              748  STORE_FAST               '_i'

 L. 510       750  LOAD_FAST                '_i'
              752  LOAD_CONST               False
              754  COMPARE_OP               is
          756_758  POP_JUMP_IF_TRUE    770  'to 770'
              760  LOAD_FAST                '_i'
              762  LOAD_CONST               1
              764  COMPARE_OP               <
          766_768  POP_JUMP_IF_FALSE   746  'to 746'
            770_0  COME_FROM           756  '756'

 L. 511       770  LOAD_GLOBAL              vis_msg
              772  LOAD_ATTR                print
              774  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Non-positive convolutional feature number'

 L. 512       776  LOAD_STR                 'error'
              778  LOAD_CONST               ('type',)
              780  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              782  POP_TOP          

 L. 513       784  LOAD_GLOBAL              QtWidgets
              786  LOAD_ATTR                QMessageBox
              788  LOAD_METHOD              critical
              790  LOAD_DEREF               'self'
              792  LOAD_ATTR                msgbox

 L. 514       794  LOAD_STR                 'Train 2D-CNN'

 L. 515       796  LOAD_STR                 'Non-positive convolutional feature number'
              798  CALL_METHOD_3         3  '3 positional arguments'
              800  POP_TOP          

 L. 516       802  LOAD_CONST               None
              804  RETURN_VALUE     
          806_808  JUMP_BACK           746  'to 746'
              810  POP_BLOCK        
            812_0  COME_FROM_LOOP      740  '740'

 L. 517       812  LOAD_FAST                '_nfclayer'
              814  LOAD_CONST               False
              816  COMPARE_OP               is
          818_820  POP_JUMP_IF_TRUE    832  'to 832'
              822  LOAD_FAST                '_nfclayer'
              824  LOAD_CONST               0
              826  COMPARE_OP               <=
          828_830  POP_JUMP_IF_FALSE   868  'to 868'
            832_0  COME_FROM           818  '818'

 L. 518       832  LOAD_GLOBAL              vis_msg
              834  LOAD_ATTR                print
              836  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Non-positive MLP layer number'
              838  LOAD_STR                 'error'
              840  LOAD_CONST               ('type',)
              842  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              844  POP_TOP          

 L. 519       846  LOAD_GLOBAL              QtWidgets
              848  LOAD_ATTR                QMessageBox
              850  LOAD_METHOD              critical
              852  LOAD_DEREF               'self'
              854  LOAD_ATTR                msgbox

 L. 520       856  LOAD_STR                 'Train 2D-CNN'

 L. 521       858  LOAD_STR                 'Non-positive MLP layer number'
              860  CALL_METHOD_3         3  '3 positional arguments'
              862  POP_TOP          

 L. 522       864  LOAD_CONST               None
              866  RETURN_VALUE     
            868_0  COME_FROM           828  '828'

 L. 523       868  SETUP_LOOP          940  'to 940'
              870  LOAD_FAST                '_nfcneuron'
              872  GET_ITER         
            874_0  COME_FROM           894  '894'
              874  FOR_ITER            938  'to 938'
              876  STORE_FAST               '_i'

 L. 524       878  LOAD_FAST                '_i'
              880  LOAD_CONST               False
              882  COMPARE_OP               is
          884_886  POP_JUMP_IF_TRUE    898  'to 898'
              888  LOAD_FAST                '_i'
              890  LOAD_CONST               1
              892  COMPARE_OP               <
          894_896  POP_JUMP_IF_FALSE   874  'to 874'
            898_0  COME_FROM           884  '884'

 L. 525       898  LOAD_GLOBAL              vis_msg
              900  LOAD_ATTR                print
              902  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Non-positive MLP neuron number'
              904  LOAD_STR                 'error'
              906  LOAD_CONST               ('type',)
              908  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              910  POP_TOP          

 L. 526       912  LOAD_GLOBAL              QtWidgets
              914  LOAD_ATTR                QMessageBox
              916  LOAD_METHOD              critical
              918  LOAD_DEREF               'self'
              920  LOAD_ATTR                msgbox

 L. 527       922  LOAD_STR                 'Train 2D-CNN'

 L. 528       924  LOAD_STR                 'Non-positive MLP neuron number'
              926  CALL_METHOD_3         3  '3 positional arguments'
              928  POP_TOP          

 L. 529       930  LOAD_CONST               None
              932  RETURN_VALUE     
          934_936  JUMP_BACK           874  'to 874'
              938  POP_BLOCK        
            940_0  COME_FROM_LOOP      868  '868'

 L. 530       940  LOAD_FAST                '_patch_height'
              942  LOAD_CONST               False
              944  COMPARE_OP               is
          946_948  POP_JUMP_IF_TRUE    980  'to 980'
              950  LOAD_FAST                '_patch_width'
              952  LOAD_CONST               False
              954  COMPARE_OP               is
          956_958  POP_JUMP_IF_TRUE    980  'to 980'

 L. 531       960  LOAD_FAST                '_patch_height'
              962  LOAD_CONST               1
              964  COMPARE_OP               <
          966_968  POP_JUMP_IF_TRUE    980  'to 980'
              970  LOAD_FAST                '_patch_width'
              972  LOAD_CONST               1
              974  COMPARE_OP               <
          976_978  POP_JUMP_IF_FALSE  1016  'to 1016'
            980_0  COME_FROM           966  '966'
            980_1  COME_FROM           956  '956'
            980_2  COME_FROM           946  '946'

 L. 532       980  LOAD_GLOBAL              vis_msg
              982  LOAD_ATTR                print
              984  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Non-positive convolutional patch size'

 L. 533       986  LOAD_STR                 'error'
              988  LOAD_CONST               ('type',)
              990  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              992  POP_TOP          

 L. 534       994  LOAD_GLOBAL              QtWidgets
              996  LOAD_ATTR                QMessageBox
              998  LOAD_METHOD              critical
             1000  LOAD_DEREF               'self'
             1002  LOAD_ATTR                msgbox

 L. 535      1004  LOAD_STR                 'Train 2D-CNN'

 L. 536      1006  LOAD_STR                 'Non-positive convolutional patch size'
             1008  CALL_METHOD_3         3  '3 positional arguments'
             1010  POP_TOP          

 L. 537      1012  LOAD_CONST               None
             1014  RETURN_VALUE     
           1016_0  COME_FROM           976  '976'

 L. 538      1016  LOAD_FAST                '_pool_height'
             1018  LOAD_CONST               False
             1020  COMPARE_OP               is
         1022_1024  POP_JUMP_IF_TRUE   1056  'to 1056'
             1026  LOAD_FAST                '_pool_width'
             1028  LOAD_CONST               False
             1030  COMPARE_OP               is
         1032_1034  POP_JUMP_IF_TRUE   1056  'to 1056'

 L. 539      1036  LOAD_FAST                '_pool_height'
             1038  LOAD_CONST               1
             1040  COMPARE_OP               <
         1042_1044  POP_JUMP_IF_TRUE   1056  'to 1056'
             1046  LOAD_FAST                '_pool_width'
             1048  LOAD_CONST               1
             1050  COMPARE_OP               <
         1052_1054  POP_JUMP_IF_FALSE  1092  'to 1092'
           1056_0  COME_FROM          1042  '1042'
           1056_1  COME_FROM          1032  '1032'
           1056_2  COME_FROM          1022  '1022'

 L. 540      1056  LOAD_GLOBAL              vis_msg
             1058  LOAD_ATTR                print
             1060  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Non-positive pooling size'
             1062  LOAD_STR                 'error'
             1064  LOAD_CONST               ('type',)
             1066  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1068  POP_TOP          

 L. 541      1070  LOAD_GLOBAL              QtWidgets
             1072  LOAD_ATTR                QMessageBox
             1074  LOAD_METHOD              critical
             1076  LOAD_DEREF               'self'
             1078  LOAD_ATTR                msgbox

 L. 542      1080  LOAD_STR                 'Train 2D-CNN'

 L. 543      1082  LOAD_STR                 'Non-positive pooling size'
             1084  CALL_METHOD_3         3  '3 positional arguments'
             1086  POP_TOP          

 L. 544      1088  LOAD_CONST               None
             1090  RETURN_VALUE     
           1092_0  COME_FROM          1052  '1052'

 L. 545      1092  LOAD_FAST                '_nepoch'
             1094  LOAD_CONST               False
             1096  COMPARE_OP               is
         1098_1100  POP_JUMP_IF_TRUE   1112  'to 1112'
             1102  LOAD_FAST                '_nepoch'
             1104  LOAD_CONST               0
             1106  COMPARE_OP               <=
         1108_1110  POP_JUMP_IF_FALSE  1148  'to 1148'
           1112_0  COME_FROM          1098  '1098'

 L. 546      1112  LOAD_GLOBAL              vis_msg
             1114  LOAD_ATTR                print
             1116  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Non-positive epoch number'
             1118  LOAD_STR                 'error'
             1120  LOAD_CONST               ('type',)
             1122  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1124  POP_TOP          

 L. 547      1126  LOAD_GLOBAL              QtWidgets
             1128  LOAD_ATTR                QMessageBox
             1130  LOAD_METHOD              critical
             1132  LOAD_DEREF               'self'
             1134  LOAD_ATTR                msgbox

 L. 548      1136  LOAD_STR                 'Train 2D-CNN'

 L. 549      1138  LOAD_STR                 'Non-positive epoch number'
             1140  CALL_METHOD_3         3  '3 positional arguments'
             1142  POP_TOP          

 L. 550      1144  LOAD_CONST               None
             1146  RETURN_VALUE     
           1148_0  COME_FROM          1108  '1108'

 L. 551      1148  LOAD_FAST                '_batchsize'
             1150  LOAD_CONST               False
             1152  COMPARE_OP               is
         1154_1156  POP_JUMP_IF_TRUE   1168  'to 1168'
             1158  LOAD_FAST                '_batchsize'
             1160  LOAD_CONST               0
             1162  COMPARE_OP               <=
         1164_1166  POP_JUMP_IF_FALSE  1204  'to 1204'
           1168_0  COME_FROM          1154  '1154'

 L. 552      1168  LOAD_GLOBAL              vis_msg
             1170  LOAD_ATTR                print
             1172  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Non-positive batch size'
             1174  LOAD_STR                 'error'
             1176  LOAD_CONST               ('type',)
             1178  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1180  POP_TOP          

 L. 553      1182  LOAD_GLOBAL              QtWidgets
             1184  LOAD_ATTR                QMessageBox
             1186  LOAD_METHOD              critical
             1188  LOAD_DEREF               'self'
             1190  LOAD_ATTR                msgbox

 L. 554      1192  LOAD_STR                 'Train 2D-CNN'

 L. 555      1194  LOAD_STR                 'Non-positive batch size'
             1196  CALL_METHOD_3         3  '3 positional arguments'
             1198  POP_TOP          

 L. 556      1200  LOAD_CONST               None
             1202  RETURN_VALUE     
           1204_0  COME_FROM          1164  '1164'

 L. 557      1204  LOAD_FAST                '_learning_rate'
             1206  LOAD_CONST               False
             1208  COMPARE_OP               is
         1210_1212  POP_JUMP_IF_TRUE   1224  'to 1224'
             1214  LOAD_FAST                '_learning_rate'
             1216  LOAD_CONST               0
             1218  COMPARE_OP               <=
         1220_1222  POP_JUMP_IF_FALSE  1260  'to 1260'
           1224_0  COME_FROM          1210  '1210'

 L. 558      1224  LOAD_GLOBAL              vis_msg
             1226  LOAD_ATTR                print
             1228  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Non-positive learning rate'
             1230  LOAD_STR                 'error'
             1232  LOAD_CONST               ('type',)
             1234  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1236  POP_TOP          

 L. 559      1238  LOAD_GLOBAL              QtWidgets
             1240  LOAD_ATTR                QMessageBox
             1242  LOAD_METHOD              critical
             1244  LOAD_DEREF               'self'
             1246  LOAD_ATTR                msgbox

 L. 560      1248  LOAD_STR                 'Train 2D-CNN'

 L. 561      1250  LOAD_STR                 'Non-positive learning rate'
             1252  CALL_METHOD_3         3  '3 positional arguments'
             1254  POP_TOP          

 L. 562      1256  LOAD_CONST               None
             1258  RETURN_VALUE     
           1260_0  COME_FROM          1220  '1220'

 L. 563      1260  LOAD_FAST                '_dropout_prob_fclayer'
             1262  LOAD_CONST               False
             1264  COMPARE_OP               is
         1266_1268  POP_JUMP_IF_TRUE   1280  'to 1280'
             1270  LOAD_FAST                '_dropout_prob_fclayer'
             1272  LOAD_CONST               0
             1274  COMPARE_OP               <=
         1276_1278  POP_JUMP_IF_FALSE  1316  'to 1316'
           1280_0  COME_FROM          1266  '1266'

 L. 564      1280  LOAD_GLOBAL              vis_msg
             1282  LOAD_ATTR                print
             1284  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: Negative dropout rate'
             1286  LOAD_STR                 'error'
             1288  LOAD_CONST               ('type',)
             1290  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1292  POP_TOP          

 L. 565      1294  LOAD_GLOBAL              QtWidgets
             1296  LOAD_ATTR                QMessageBox
             1298  LOAD_METHOD              critical
             1300  LOAD_DEREF               'self'
             1302  LOAD_ATTR                msgbox

 L. 566      1304  LOAD_STR                 'Train 2D-CNN'

 L. 567      1306  LOAD_STR                 'Negative dropout rate'
             1308  CALL_METHOD_3         3  '3 positional arguments'
             1310  POP_TOP          

 L. 568      1312  LOAD_CONST               None
             1314  RETURN_VALUE     
           1316_0  COME_FROM          1276  '1276'

 L. 570      1316  LOAD_GLOBAL              len
             1318  LOAD_DEREF               'self'
             1320  LOAD_ATTR                ldtsave
             1322  LOAD_METHOD              text
             1324  CALL_METHOD_0         0  '0 positional arguments'
             1326  CALL_FUNCTION_1       1  '1 positional argument'
             1328  LOAD_CONST               1
             1330  COMPARE_OP               <
         1332_1334  POP_JUMP_IF_FALSE  1372  'to 1372'

 L. 571      1336  LOAD_GLOBAL              vis_msg
             1338  LOAD_ATTR                print
             1340  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: No name specified for CNN network'
             1342  LOAD_STR                 'error'
             1344  LOAD_CONST               ('type',)
             1346  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1348  POP_TOP          

 L. 572      1350  LOAD_GLOBAL              QtWidgets
             1352  LOAD_ATTR                QMessageBox
             1354  LOAD_METHOD              critical
             1356  LOAD_DEREF               'self'
             1358  LOAD_ATTR                msgbox

 L. 573      1360  LOAD_STR                 'Train 2D-CNN'

 L. 574      1362  LOAD_STR                 'No name specified for CNN network'
             1364  CALL_METHOD_3         3  '3 positional arguments'
             1366  POP_TOP          

 L. 575      1368  LOAD_CONST               None
             1370  RETURN_VALUE     
           1372_0  COME_FROM          1332  '1332'

 L. 576      1372  LOAD_GLOBAL              os
             1374  LOAD_ATTR                path
             1376  LOAD_METHOD              dirname
             1378  LOAD_DEREF               'self'
             1380  LOAD_ATTR                ldtsave
             1382  LOAD_METHOD              text
             1384  CALL_METHOD_0         0  '0 positional arguments'
             1386  CALL_METHOD_1         1  '1 positional argument'
             1388  STORE_FAST               '_savepath'

 L. 577      1390  LOAD_GLOBAL              os
             1392  LOAD_ATTR                path
             1394  LOAD_METHOD              splitext
             1396  LOAD_GLOBAL              os
             1398  LOAD_ATTR                path
             1400  LOAD_METHOD              basename
             1402  LOAD_DEREF               'self'
             1404  LOAD_ATTR                ldtsave
             1406  LOAD_METHOD              text
             1408  CALL_METHOD_0         0  '0 positional arguments'
             1410  CALL_METHOD_1         1  '1 positional argument'
             1412  CALL_METHOD_1         1  '1 positional argument'
             1414  LOAD_CONST               0
             1416  BINARY_SUBSCR    
             1418  STORE_FAST               '_savename'

 L. 579      1420  LOAD_CONST               0
             1422  STORE_FAST               '_wdinl'

 L. 580      1424  LOAD_CONST               0
             1426  STORE_FAST               '_wdxl'

 L. 581      1428  LOAD_CONST               0
             1430  STORE_FAST               '_wdz'

 L. 582      1432  LOAD_DEREF               'self'
             1434  LOAD_ATTR                cbbornt
             1436  LOAD_METHOD              currentIndex
             1438  CALL_METHOD_0         0  '0 positional arguments'
             1440  LOAD_CONST               0
             1442  COMPARE_OP               ==
         1444_1446  POP_JUMP_IF_FALSE  1472  'to 1472'

 L. 583      1448  LOAD_GLOBAL              int
             1450  LOAD_FAST                '_image_width_old'
             1452  LOAD_CONST               2
             1454  BINARY_TRUE_DIVIDE
             1456  CALL_FUNCTION_1       1  '1 positional argument'
             1458  STORE_FAST               '_wdxl'

 L. 584      1460  LOAD_GLOBAL              int
             1462  LOAD_FAST                '_image_height_old'
             1464  LOAD_CONST               2
             1466  BINARY_TRUE_DIVIDE
             1468  CALL_FUNCTION_1       1  '1 positional argument'
             1470  STORE_FAST               '_wdz'
           1472_0  COME_FROM          1444  '1444'

 L. 585      1472  LOAD_DEREF               'self'
             1474  LOAD_ATTR                cbbornt
             1476  LOAD_METHOD              currentIndex
             1478  CALL_METHOD_0         0  '0 positional arguments'
             1480  LOAD_CONST               1
             1482  COMPARE_OP               ==
         1484_1486  POP_JUMP_IF_FALSE  1512  'to 1512'

 L. 586      1488  LOAD_GLOBAL              int
             1490  LOAD_FAST                '_image_width_old'
             1492  LOAD_CONST               2
             1494  BINARY_TRUE_DIVIDE
             1496  CALL_FUNCTION_1       1  '1 positional argument'
             1498  STORE_FAST               '_wdinl'

 L. 587      1500  LOAD_GLOBAL              int
             1502  LOAD_FAST                '_image_height_old'
             1504  LOAD_CONST               2
             1506  BINARY_TRUE_DIVIDE
             1508  CALL_FUNCTION_1       1  '1 positional argument'
             1510  STORE_FAST               '_wdz'
           1512_0  COME_FROM          1484  '1484'

 L. 588      1512  LOAD_DEREF               'self'
             1514  LOAD_ATTR                cbbornt
             1516  LOAD_METHOD              currentIndex
             1518  CALL_METHOD_0         0  '0 positional arguments'
             1520  LOAD_CONST               2
             1522  COMPARE_OP               ==
         1524_1526  POP_JUMP_IF_FALSE  1552  'to 1552'

 L. 589      1528  LOAD_GLOBAL              int
             1530  LOAD_FAST                '_image_width_old'
             1532  LOAD_CONST               2
             1534  BINARY_TRUE_DIVIDE
             1536  CALL_FUNCTION_1       1  '1 positional argument'
             1538  STORE_FAST               '_wdinl'

 L. 590      1540  LOAD_GLOBAL              int
             1542  LOAD_FAST                '_image_height_old'
             1544  LOAD_CONST               2
             1546  BINARY_TRUE_DIVIDE
             1548  CALL_FUNCTION_1       1  '1 positional argument'
             1550  STORE_FAST               '_wdxl'
           1552_0  COME_FROM          1524  '1524'

 L. 592      1552  LOAD_DEREF               'self'
             1554  LOAD_ATTR                survinfo
             1556  STORE_FAST               '_seisinfo'

 L. 594      1558  LOAD_GLOBAL              print
             1560  LOAD_STR                 'TrainMl2DCnnFromScratch: Step 1 - Get training samples:'
             1562  CALL_FUNCTION_1       1  '1 positional argument'
             1564  POP_TOP          

 L. 595      1566  LOAD_DEREF               'self'
             1568  LOAD_ATTR                traindataconfig
             1570  LOAD_STR                 'TrainPointSet'
             1572  BINARY_SUBSCR    
             1574  STORE_FAST               '_trainpoint'

 L. 596      1576  LOAD_GLOBAL              np
             1578  LOAD_METHOD              zeros
             1580  LOAD_CONST               0
             1582  LOAD_CONST               3
             1584  BUILD_LIST_2          2 
             1586  CALL_METHOD_1         1  '1 positional argument'
             1588  STORE_FAST               '_traindata'

 L. 597      1590  SETUP_LOOP         1666  'to 1666'
             1592  LOAD_FAST                '_trainpoint'
             1594  GET_ITER         
           1596_0  COME_FROM          1614  '1614'
             1596  FOR_ITER           1664  'to 1664'
             1598  STORE_FAST               '_p'

 L. 598      1600  LOAD_GLOBAL              point_ays
             1602  LOAD_METHOD              checkPoint
             1604  LOAD_DEREF               'self'
             1606  LOAD_ATTR                pointsetdata
             1608  LOAD_FAST                '_p'
             1610  BINARY_SUBSCR    
             1612  CALL_METHOD_1         1  '1 positional argument'
         1614_1616  POP_JUMP_IF_FALSE  1596  'to 1596'

 L. 599      1618  LOAD_GLOBAL              basic_mdt
             1620  LOAD_METHOD              exportMatDict
             1622  LOAD_DEREF               'self'
             1624  LOAD_ATTR                pointsetdata
             1626  LOAD_FAST                '_p'
             1628  BINARY_SUBSCR    
             1630  LOAD_STR                 'Inline'
             1632  LOAD_STR                 'Crossline'
             1634  LOAD_STR                 'Z'
             1636  BUILD_LIST_3          3 
             1638  CALL_METHOD_2         2  '2 positional arguments'
             1640  STORE_FAST               '_pt'

 L. 600      1642  LOAD_GLOBAL              np
             1644  LOAD_ATTR                concatenate
             1646  LOAD_FAST                '_traindata'
             1648  LOAD_FAST                '_pt'
             1650  BUILD_TUPLE_2         2 
             1652  LOAD_CONST               0
             1654  LOAD_CONST               ('axis',)
             1656  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1658  STORE_FAST               '_traindata'
         1660_1662  JUMP_BACK          1596  'to 1596'
             1664  POP_BLOCK        
           1666_0  COME_FROM_LOOP     1590  '1590'

 L. 601      1666  LOAD_GLOBAL              seis_ays
             1668  LOAD_ATTR                removeOutofSurveySample
             1670  LOAD_FAST                '_traindata'

 L. 602      1672  LOAD_FAST                '_seisinfo'
             1674  LOAD_STR                 'ILStart'
             1676  BINARY_SUBSCR    
             1678  LOAD_FAST                '_wdinl'
             1680  LOAD_FAST                '_seisinfo'
             1682  LOAD_STR                 'ILStep'
             1684  BINARY_SUBSCR    
             1686  BINARY_MULTIPLY  
             1688  BINARY_ADD       

 L. 603      1690  LOAD_FAST                '_seisinfo'
             1692  LOAD_STR                 'ILEnd'
             1694  BINARY_SUBSCR    
             1696  LOAD_FAST                '_wdinl'
             1698  LOAD_FAST                '_seisinfo'
             1700  LOAD_STR                 'ILStep'
             1702  BINARY_SUBSCR    
             1704  BINARY_MULTIPLY  
             1706  BINARY_SUBTRACT  

 L. 604      1708  LOAD_FAST                '_seisinfo'
             1710  LOAD_STR                 'XLStart'
             1712  BINARY_SUBSCR    
             1714  LOAD_FAST                '_wdxl'
             1716  LOAD_FAST                '_seisinfo'
             1718  LOAD_STR                 'XLStep'
             1720  BINARY_SUBSCR    
             1722  BINARY_MULTIPLY  
             1724  BINARY_ADD       

 L. 605      1726  LOAD_FAST                '_seisinfo'
             1728  LOAD_STR                 'XLEnd'
             1730  BINARY_SUBSCR    
             1732  LOAD_FAST                '_wdxl'
             1734  LOAD_FAST                '_seisinfo'
             1736  LOAD_STR                 'XLStep'
             1738  BINARY_SUBSCR    
             1740  BINARY_MULTIPLY  
             1742  BINARY_SUBTRACT  

 L. 606      1744  LOAD_FAST                '_seisinfo'
             1746  LOAD_STR                 'ZStart'
             1748  BINARY_SUBSCR    
             1750  LOAD_FAST                '_wdz'
             1752  LOAD_FAST                '_seisinfo'
             1754  LOAD_STR                 'ZStep'
             1756  BINARY_SUBSCR    
             1758  BINARY_MULTIPLY  
             1760  BINARY_ADD       

 L. 607      1762  LOAD_FAST                '_seisinfo'
             1764  LOAD_STR                 'ZEnd'
             1766  BINARY_SUBSCR    
             1768  LOAD_FAST                '_wdz'
             1770  LOAD_FAST                '_seisinfo'
             1772  LOAD_STR                 'ZStep'
             1774  BINARY_SUBSCR    
             1776  BINARY_MULTIPLY  
             1778  BINARY_SUBTRACT  
             1780  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1782  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1784  STORE_FAST               '_traindata'

 L. 610      1786  LOAD_GLOBAL              np
             1788  LOAD_METHOD              shape
             1790  LOAD_FAST                '_traindata'
             1792  CALL_METHOD_1         1  '1 positional argument'
             1794  LOAD_CONST               0
             1796  BINARY_SUBSCR    
             1798  LOAD_CONST               0
             1800  COMPARE_OP               <=
         1802_1804  POP_JUMP_IF_FALSE  1842  'to 1842'

 L. 611      1806  LOAD_GLOBAL              vis_msg
             1808  LOAD_ATTR                print
             1810  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: No training sample found'
             1812  LOAD_STR                 'error'
             1814  LOAD_CONST               ('type',)
             1816  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1818  POP_TOP          

 L. 612      1820  LOAD_GLOBAL              QtWidgets
             1822  LOAD_ATTR                QMessageBox
             1824  LOAD_METHOD              critical
             1826  LOAD_DEREF               'self'
             1828  LOAD_ATTR                msgbox

 L. 613      1830  LOAD_STR                 'Train 2D-CNN'

 L. 614      1832  LOAD_STR                 'No training sample found'
             1834  CALL_METHOD_3         3  '3 positional arguments'
             1836  POP_TOP          

 L. 615      1838  LOAD_CONST               None
             1840  RETURN_VALUE     
           1842_0  COME_FROM          1802  '1802'

 L. 618      1842  LOAD_GLOBAL              print
             1844  LOAD_STR                 'TrainMl2DCnnFromScratch: Step 2 - Retrieve and interpolate images: (%d, %d) --> (%d, %d)'

 L. 619      1846  LOAD_FAST                '_image_height_old'
             1848  LOAD_FAST                '_image_width_old'
             1850  LOAD_FAST                '_image_height_new'
             1852  LOAD_FAST                '_image_width_new'
             1854  BUILD_TUPLE_4         4 
             1856  BINARY_MODULO    
             1858  CALL_FUNCTION_1       1  '1 positional argument'
             1860  POP_TOP          

 L. 620      1862  BUILD_MAP_0           0 
             1864  STORE_FAST               '_traindict'

 L. 621      1866  SETUP_LOOP         1938  'to 1938'
             1868  LOAD_FAST                '_features'
             1870  GET_ITER         
             1872  FOR_ITER           1936  'to 1936'
             1874  STORE_FAST               'f'

 L. 622      1876  LOAD_DEREF               'self'
             1878  LOAD_ATTR                seisdata
             1880  LOAD_FAST                'f'
             1882  BINARY_SUBSCR    
             1884  STORE_FAST               '_seisdata'

 L. 623      1886  LOAD_GLOBAL              seis_ays
             1888  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1890  LOAD_FAST                '_seisdata'
             1892  LOAD_FAST                '_traindata'
             1894  LOAD_DEREF               'self'
             1896  LOAD_ATTR                survinfo

 L. 624      1898  LOAD_FAST                '_wdinl'
             1900  LOAD_FAST                '_wdxl'
             1902  LOAD_FAST                '_wdz'

 L. 625      1904  LOAD_CONST               False
             1906  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1908  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1910  LOAD_CONST               None
             1912  LOAD_CONST               None
             1914  BUILD_SLICE_2         2 
             1916  LOAD_CONST               3
             1918  LOAD_CONST               None
             1920  BUILD_SLICE_2         2 
             1922  BUILD_TUPLE_2         2 
             1924  BINARY_SUBSCR    
             1926  LOAD_FAST                '_traindict'
             1928  LOAD_FAST                'f'
             1930  STORE_SUBSCR     
         1932_1934  JUMP_BACK          1872  'to 1872'
             1936  POP_BLOCK        
           1938_0  COME_FROM_LOOP     1866  '1866'

 L. 626      1938  LOAD_FAST                '_target'
             1940  LOAD_FAST                '_features'
             1942  COMPARE_OP               not-in
         1944_1946  POP_JUMP_IF_FALSE  1998  'to 1998'

 L. 627      1948  LOAD_DEREF               'self'
             1950  LOAD_ATTR                seisdata
             1952  LOAD_FAST                '_target'
             1954  BINARY_SUBSCR    
             1956  STORE_FAST               '_seisdata'

 L. 628      1958  LOAD_GLOBAL              seis_ays
             1960  LOAD_ATTR                retrieveSeisSampleFrom3DMat
             1962  LOAD_FAST                '_seisdata'
             1964  LOAD_FAST                '_traindata'
             1966  LOAD_DEREF               'self'
             1968  LOAD_ATTR                survinfo

 L. 629      1970  LOAD_CONST               False
             1972  LOAD_CONST               ('seisinfo', 'verbose')
             1974  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1976  LOAD_CONST               None
             1978  LOAD_CONST               None
             1980  BUILD_SLICE_2         2 
             1982  LOAD_CONST               3
             1984  LOAD_CONST               None
             1986  BUILD_SLICE_2         2 
             1988  BUILD_TUPLE_2         2 
             1990  BINARY_SUBSCR    
             1992  LOAD_FAST                '_traindict'
             1994  LOAD_FAST                '_target'
             1996  STORE_SUBSCR     
           1998_0  COME_FROM          1944  '1944'

 L. 631      1998  LOAD_DEREF               'self'
             2000  LOAD_ATTR                traindataconfig
             2002  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2004  BINARY_SUBSCR    
         2006_2008  POP_JUMP_IF_FALSE  2090  'to 2090'

 L. 632      2010  SETUP_LOOP         2090  'to 2090'
             2012  LOAD_FAST                '_features'
             2014  GET_ITER         
           2016_0  COME_FROM          2044  '2044'
             2016  FOR_ITER           2088  'to 2088'
             2018  STORE_FAST               'f'

 L. 633      2020  LOAD_GLOBAL              ml_aug
             2022  LOAD_METHOD              removeInvariantFeature
             2024  LOAD_FAST                '_traindict'
             2026  LOAD_FAST                'f'
             2028  CALL_METHOD_2         2  '2 positional arguments'
             2030  STORE_FAST               '_traindict'

 L. 634      2032  LOAD_GLOBAL              basic_mdt
             2034  LOAD_METHOD              maxDictConstantRow
             2036  LOAD_FAST                '_traindict'
             2038  CALL_METHOD_1         1  '1 positional argument'
             2040  LOAD_CONST               0
             2042  COMPARE_OP               <=
         2044_2046  POP_JUMP_IF_FALSE  2016  'to 2016'

 L. 635      2048  LOAD_GLOBAL              vis_msg
             2050  LOAD_ATTR                print
             2052  LOAD_STR                 'ERROR in TrainMl2DCnnFromScratch: No training sample found'
             2054  LOAD_STR                 'error'
             2056  LOAD_CONST               ('type',)
             2058  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2060  POP_TOP          

 L. 636      2062  LOAD_GLOBAL              QtWidgets
             2064  LOAD_ATTR                QMessageBox
             2066  LOAD_METHOD              critical
             2068  LOAD_DEREF               'self'
             2070  LOAD_ATTR                msgbox

 L. 637      2072  LOAD_STR                 'Train 2D-CNN'

 L. 638      2074  LOAD_STR                 'No training sample found'
             2076  CALL_METHOD_3         3  '3 positional arguments'
             2078  POP_TOP          

 L. 639      2080  LOAD_CONST               None
             2082  RETURN_VALUE     
         2084_2086  JUMP_BACK          2016  'to 2016'
             2088  POP_BLOCK        
           2090_0  COME_FROM_LOOP     2010  '2010'
           2090_1  COME_FROM          2006  '2006'

 L. 641      2090  LOAD_GLOBAL              np
             2092  LOAD_METHOD              round
             2094  LOAD_FAST                '_traindict'
             2096  LOAD_FAST                '_target'
             2098  BINARY_SUBSCR    
             2100  CALL_METHOD_1         1  '1 positional argument'
             2102  LOAD_METHOD              astype
             2104  LOAD_GLOBAL              int
             2106  CALL_METHOD_1         1  '1 positional argument'
             2108  LOAD_FAST                '_traindict'
             2110  LOAD_FAST                '_target'
             2112  STORE_SUBSCR     

 L. 643      2114  LOAD_FAST                '_image_height_new'
             2116  LOAD_FAST                '_image_height_old'
             2118  COMPARE_OP               !=
         2120_2122  POP_JUMP_IF_TRUE   2134  'to 2134'
             2124  LOAD_FAST                '_image_width_new'
             2126  LOAD_FAST                '_image_width_old'
             2128  COMPARE_OP               !=
         2130_2132  POP_JUMP_IF_FALSE  2178  'to 2178'
           2134_0  COME_FROM          2120  '2120'

 L. 644      2134  SETUP_LOOP         2178  'to 2178'
             2136  LOAD_FAST                '_features'
             2138  GET_ITER         
             2140  FOR_ITER           2176  'to 2176'
             2142  STORE_FAST               'f'

 L. 645      2144  LOAD_GLOBAL              basic_image
             2146  LOAD_ATTR                changeImageSize
             2148  LOAD_FAST                '_traindict'
             2150  LOAD_FAST                'f'
             2152  BINARY_SUBSCR    

 L. 646      2154  LOAD_FAST                '_image_height_old'

 L. 647      2156  LOAD_FAST                '_image_width_old'

 L. 648      2158  LOAD_FAST                '_image_height_new'

 L. 649      2160  LOAD_FAST                '_image_width_new'
             2162  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2164  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2166  LOAD_FAST                '_traindict'
             2168  LOAD_FAST                'f'
             2170  STORE_SUBSCR     
         2172_2174  JUMP_BACK          2140  'to 2140'
             2176  POP_BLOCK        
           2178_0  COME_FROM_LOOP     2134  '2134'
           2178_1  COME_FROM          2130  '2130'

 L. 650      2178  LOAD_DEREF               'self'
             2180  LOAD_ATTR                traindataconfig
             2182  LOAD_STR                 'RotateFeature_Checked'
             2184  BINARY_SUBSCR    
             2186  LOAD_CONST               True
             2188  COMPARE_OP               is
         2190_2192  POP_JUMP_IF_FALSE  2322  'to 2322'

 L. 651      2194  SETUP_LOOP         2266  'to 2266'
             2196  LOAD_FAST                '_features'
             2198  GET_ITER         
             2200  FOR_ITER           2264  'to 2264'
             2202  STORE_FAST               'f'

 L. 652      2204  LOAD_FAST                '_image_height_new'
             2206  LOAD_FAST                '_image_width_new'
             2208  COMPARE_OP               ==
         2210_2212  POP_JUMP_IF_FALSE  2238  'to 2238'

 L. 653      2214  LOAD_GLOBAL              ml_aug
             2216  LOAD_METHOD              rotateImage6Way
             2218  LOAD_FAST                '_traindict'
             2220  LOAD_FAST                'f'
             2222  BINARY_SUBSCR    
             2224  LOAD_FAST                '_image_height_new'
             2226  LOAD_FAST                '_image_width_new'
             2228  CALL_METHOD_3         3  '3 positional arguments'
             2230  LOAD_FAST                '_traindict'
             2232  LOAD_FAST                'f'
             2234  STORE_SUBSCR     
             2236  JUMP_BACK          2200  'to 2200'
           2238_0  COME_FROM          2210  '2210'

 L. 655      2238  LOAD_GLOBAL              ml_aug
             2240  LOAD_METHOD              rotateImage4Way
             2242  LOAD_FAST                '_traindict'
             2244  LOAD_FAST                'f'
             2246  BINARY_SUBSCR    
             2248  LOAD_FAST                '_image_height_new'
             2250  LOAD_FAST                '_image_width_new'
             2252  CALL_METHOD_3         3  '3 positional arguments'
             2254  LOAD_FAST                '_traindict'
             2256  LOAD_FAST                'f'
             2258  STORE_SUBSCR     
         2260_2262  JUMP_BACK          2200  'to 2200'
             2264  POP_BLOCK        
           2266_0  COME_FROM_LOOP     2194  '2194'

 L. 657      2266  LOAD_FAST                '_image_height_new'
             2268  LOAD_FAST                '_image_width_new'
             2270  COMPARE_OP               ==
         2272_2274  POP_JUMP_IF_FALSE  2300  'to 2300'

 L. 659      2276  LOAD_GLOBAL              ml_aug
             2278  LOAD_METHOD              rotateImage6Way
             2280  LOAD_FAST                '_traindict'
             2282  LOAD_FAST                '_target'
             2284  BINARY_SUBSCR    
             2286  LOAD_CONST               1
             2288  LOAD_CONST               1
             2290  CALL_METHOD_3         3  '3 positional arguments'
             2292  LOAD_FAST                '_traindict'
             2294  LOAD_FAST                '_target'
             2296  STORE_SUBSCR     
             2298  JUMP_FORWARD       2322  'to 2322'
           2300_0  COME_FROM          2272  '2272'

 L. 662      2300  LOAD_GLOBAL              ml_aug
             2302  LOAD_METHOD              rotateImage4Way
             2304  LOAD_FAST                '_traindict'
             2306  LOAD_FAST                '_target'
             2308  BINARY_SUBSCR    
             2310  LOAD_CONST               1
             2312  LOAD_CONST               1
             2314  CALL_METHOD_3         3  '3 positional arguments'
             2316  LOAD_FAST                '_traindict'
             2318  LOAD_FAST                '_target'
             2320  STORE_SUBSCR     
           2322_0  COME_FROM          2298  '2298'
           2322_1  COME_FROM          2190  '2190'

 L. 664      2322  LOAD_GLOBAL              print
             2324  LOAD_STR                 'TrainMl2DCnnFromScratch: A total of %d valid training samples'
             2326  LOAD_GLOBAL              basic_mdt
             2328  LOAD_METHOD              maxDictConstantRow

 L. 665      2330  LOAD_FAST                '_traindict'
             2332  CALL_METHOD_1         1  '1 positional argument'
             2334  BINARY_MODULO    
             2336  CALL_FUNCTION_1       1  '1 positional argument'
             2338  POP_TOP          

 L. 667      2340  LOAD_GLOBAL              print
             2342  LOAD_STR                 'TrainMl2DCnnFromScratch: Step 3 - Balance labels'
             2344  CALL_FUNCTION_1       1  '1 positional argument'
             2346  POP_TOP          

 L. 668      2348  LOAD_DEREF               'self'
             2350  LOAD_ATTR                traindataconfig
             2352  LOAD_STR                 'BalanceTarget_Checked'
             2354  BINARY_SUBSCR    
         2356_2358  POP_JUMP_IF_FALSE  2400  'to 2400'

 L. 669      2360  LOAD_GLOBAL              ml_aug
             2362  LOAD_METHOD              balanceLabelbyExtension
             2364  LOAD_FAST                '_traindict'
             2366  LOAD_FAST                '_target'
             2368  CALL_METHOD_2         2  '2 positional arguments'
             2370  STORE_FAST               '_traindict'

 L. 670      2372  LOAD_GLOBAL              print
             2374  LOAD_STR                 'TrainMl2DCnnFromScratch: A total of %d training samples after balance'
             2376  LOAD_GLOBAL              np
             2378  LOAD_METHOD              shape
             2380  LOAD_FAST                '_traindict'
             2382  LOAD_FAST                '_target'
             2384  BINARY_SUBSCR    
             2386  CALL_METHOD_1         1  '1 positional argument'
             2388  LOAD_CONST               0
             2390  BINARY_SUBSCR    
             2392  BINARY_MODULO    
             2394  CALL_FUNCTION_1       1  '1 positional argument'
             2396  POP_TOP          
             2398  JUMP_FORWARD       2408  'to 2408'
           2400_0  COME_FROM          2356  '2356'

 L. 672      2400  LOAD_GLOBAL              print
             2402  LOAD_STR                 'TrainMl2DCnnFromScratch: No balance applied'
             2404  CALL_FUNCTION_1       1  '1 positional argument'
             2406  POP_TOP          
           2408_0  COME_FROM          2398  '2398'

 L. 674      2408  LOAD_GLOBAL              print
             2410  LOAD_STR                 'TrainMl2DCnnFromScratch: Step 4 - Start training'
             2412  CALL_FUNCTION_1       1  '1 positional argument'
             2414  POP_TOP          

 L. 676      2416  LOAD_GLOBAL              QtWidgets
             2418  LOAD_METHOD              QProgressDialog
             2420  CALL_METHOD_0         0  '0 positional arguments'
             2422  STORE_FAST               '_pgsdlg'

 L. 677      2424  LOAD_GLOBAL              QtGui
             2426  LOAD_METHOD              QIcon
             2428  CALL_METHOD_0         0  '0 positional arguments'
             2430  STORE_FAST               'icon'

 L. 678      2432  LOAD_FAST                'icon'
             2434  LOAD_METHOD              addPixmap
             2436  LOAD_GLOBAL              QtGui
             2438  LOAD_METHOD              QPixmap
             2440  LOAD_GLOBAL              os
             2442  LOAD_ATTR                path
             2444  LOAD_METHOD              join
             2446  LOAD_DEREF               'self'
             2448  LOAD_ATTR                iconpath
             2450  LOAD_STR                 'icons/new.png'
             2452  CALL_METHOD_2         2  '2 positional arguments'
             2454  CALL_METHOD_1         1  '1 positional argument'

 L. 679      2456  LOAD_GLOBAL              QtGui
             2458  LOAD_ATTR                QIcon
             2460  LOAD_ATTR                Normal
             2462  LOAD_GLOBAL              QtGui
             2464  LOAD_ATTR                QIcon
             2466  LOAD_ATTR                Off
             2468  CALL_METHOD_3         3  '3 positional arguments'
             2470  POP_TOP          

 L. 680      2472  LOAD_FAST                '_pgsdlg'
             2474  LOAD_METHOD              setWindowIcon
             2476  LOAD_FAST                'icon'
             2478  CALL_METHOD_1         1  '1 positional argument'
             2480  POP_TOP          

 L. 681      2482  LOAD_FAST                '_pgsdlg'
             2484  LOAD_METHOD              setWindowTitle
             2486  LOAD_STR                 'Train 2D-CNN'
             2488  CALL_METHOD_1         1  '1 positional argument'
             2490  POP_TOP          

 L. 682      2492  LOAD_FAST                '_pgsdlg'
             2494  LOAD_METHOD              setCancelButton
             2496  LOAD_CONST               None
             2498  CALL_METHOD_1         1  '1 positional argument'
             2500  POP_TOP          

 L. 683      2502  LOAD_FAST                '_pgsdlg'
             2504  LOAD_METHOD              setWindowFlags
             2506  LOAD_GLOBAL              QtCore
             2508  LOAD_ATTR                Qt
             2510  LOAD_ATTR                WindowStaysOnTopHint
             2512  CALL_METHOD_1         1  '1 positional argument'
             2514  POP_TOP          

 L. 684      2516  LOAD_FAST                '_pgsdlg'
             2518  LOAD_METHOD              forceShow
             2520  CALL_METHOD_0         0  '0 positional arguments'
             2522  POP_TOP          

 L. 685      2524  LOAD_FAST                '_pgsdlg'
             2526  LOAD_METHOD              setFixedWidth
             2528  LOAD_CONST               400
             2530  CALL_METHOD_1         1  '1 positional argument'
             2532  POP_TOP          

 L. 686      2534  LOAD_GLOBAL              ml_cnn
             2536  LOAD_ATTR                createCNNClassifier
             2538  LOAD_FAST                '_traindict'

 L. 687      2540  LOAD_FAST                '_image_height_new'
             2542  LOAD_FAST                '_image_width_new'

 L. 688      2544  LOAD_FAST                '_features'
             2546  LOAD_FAST                '_target'

 L. 689      2548  LOAD_FAST                '_nepoch'
             2550  LOAD_FAST                '_batchsize'

 L. 690      2552  LOAD_FAST                '_nconvblock'

 L. 691      2554  LOAD_FAST                '_nconvlayer'
             2556  LOAD_FAST                '_nconvfeature'

 L. 692      2558  LOAD_FAST                '_nfclayer'
             2560  LOAD_FAST                '_nfcneuron'

 L. 693      2562  LOAD_FAST                '_patch_height'
             2564  LOAD_FAST                '_patch_width'

 L. 694      2566  LOAD_FAST                '_pool_height'
             2568  LOAD_FAST                '_pool_width'

 L. 695      2570  LOAD_FAST                '_learning_rate'

 L. 696      2572  LOAD_FAST                '_dropout_prob_fclayer'

 L. 697      2574  LOAD_CONST               True

 L. 698      2576  LOAD_FAST                '_savepath'
             2578  LOAD_FAST                '_savename'

 L. 699      2580  LOAD_FAST                '_pgsdlg'
             2582  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'nepoch', 'batchsize', 'nconvblock', 'nconvlayer', 'nconvfeature', 'nfclayer', 'nfcneuron', 'patchheight', 'patchwidth', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprobfclayer', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2584  CALL_FUNCTION_KW_22    22  '22 total positional and keyword args'
             2586  STORE_FAST               '_cnnlog'

 L. 701      2588  LOAD_GLOBAL              QtWidgets
             2590  LOAD_ATTR                QMessageBox
             2592  LOAD_METHOD              information
             2594  LOAD_DEREF               'self'
             2596  LOAD_ATTR                msgbox

 L. 702      2598  LOAD_STR                 'Train 2D-CNN'

 L. 703      2600  LOAD_STR                 'CNN trained successfully'
             2602  CALL_METHOD_3         3  '3 positional arguments'
             2604  POP_TOP          

 L. 705      2606  LOAD_GLOBAL              QtWidgets
             2608  LOAD_ATTR                QMessageBox
             2610  LOAD_METHOD              question
             2612  LOAD_DEREF               'self'
             2614  LOAD_ATTR                msgbox
             2616  LOAD_STR                 'Train 2D-CNN'
             2618  LOAD_STR                 'View learning matrix?'

 L. 706      2620  LOAD_GLOBAL              QtWidgets
             2622  LOAD_ATTR                QMessageBox
             2624  LOAD_ATTR                Yes
             2626  LOAD_GLOBAL              QtWidgets
             2628  LOAD_ATTR                QMessageBox
             2630  LOAD_ATTR                No
             2632  BINARY_OR        

 L. 707      2634  LOAD_GLOBAL              QtWidgets
             2636  LOAD_ATTR                QMessageBox
             2638  LOAD_ATTR                Yes
             2640  CALL_METHOD_5         5  '5 positional arguments'
             2642  STORE_FAST               'reply'

 L. 709      2644  LOAD_FAST                'reply'
             2646  LOAD_GLOBAL              QtWidgets
             2648  LOAD_ATTR                QMessageBox
             2650  LOAD_ATTR                Yes
             2652  COMPARE_OP               ==
         2654_2656  POP_JUMP_IF_FALSE  2724  'to 2724'

 L. 710      2658  LOAD_GLOBAL              QtWidgets
             2660  LOAD_METHOD              QDialog
             2662  CALL_METHOD_0         0  '0 positional arguments'
             2664  STORE_FAST               '_viewmllearnmat'

 L. 711      2666  LOAD_GLOBAL              gui_viewmllearnmat
             2668  CALL_FUNCTION_0       0  '0 positional arguments'
             2670  STORE_FAST               '_gui'

 L. 712      2672  LOAD_FAST                '_cnnlog'
             2674  LOAD_STR                 'learning_curve'
             2676  BINARY_SUBSCR    
             2678  LOAD_FAST                '_gui'
             2680  STORE_ATTR               learnmat

 L. 713      2682  LOAD_DEREF               'self'
             2684  LOAD_ATTR                linestyle
             2686  LOAD_FAST                '_gui'
             2688  STORE_ATTR               linestyle

 L. 714      2690  LOAD_DEREF               'self'
             2692  LOAD_ATTR                fontstyle
             2694  LOAD_FAST                '_gui'
             2696  STORE_ATTR               fontstyle

 L. 715      2698  LOAD_FAST                '_gui'
             2700  LOAD_METHOD              setupGUI
             2702  LOAD_FAST                '_viewmllearnmat'
             2704  CALL_METHOD_1         1  '1 positional argument'
             2706  POP_TOP          

 L. 716      2708  LOAD_FAST                '_viewmllearnmat'
             2710  LOAD_METHOD              exec
             2712  CALL_METHOD_0         0  '0 positional arguments'
             2714  POP_TOP          

 L. 717      2716  LOAD_FAST                '_viewmllearnmat'
             2718  LOAD_METHOD              show
             2720  CALL_METHOD_0         0  '0 positional arguments'
             2722  POP_TOP          
           2724_0  COME_FROM          2654  '2654'

Parse error at or near `POP_TOP' instruction at offset 2722

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
    TrainMl2DCnnFromScratch = QtWidgets.QWidget()
    gui = trainml2dcnnfromscratch()
    gui.setupGUI(TrainMl2DCnnFromScratch)
    TrainMl2DCnnFromScratch.show()
    sys.exit(app.exec_())