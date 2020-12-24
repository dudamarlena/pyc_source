# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml15ddcnnfromscratch.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 43726 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.seismic.analysis import analysis as seis_ays
from cognitivegeo.src.pointset.analysis import analysis as point_ays
from cognitivegeo.src.basic.data import data as basic_data
from cognitivegeo.src.basic.matdict import matdict as basic_mdt
from cognitivegeo.src.basic.curve import curve as basic_curve
from cognitivegeo.src.basic.image import image as basic_image
from cognitivegeo.src.ml.augmentation import augmentation as ml_aug
from cognitivegeo.src.ml.dcnnsegmentor15d import dcnnsegmentor15d as ml_dcnn15d
from cognitivegeo.src.gui.viewmllearnmat import viewmllearnmat as gui_viewmllearnmat
from cognitivegeo.src.gui.configmltraindata import configmltraindata as gui_configmltraindata
from cognitivegeo.src.vis.messager import messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml15ddcnnfromscratch(object):
    survinfo = {}
    seisdata = {}
    pointsetdata = {}
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    rootpath = ''
    iconpath = os.path.dirname(__file__)
    dialog = None
    featurelist = list()
    traindataconfig = {}
    traindataconfig['TrainPointSet'] = []
    traindataconfig['RotateFeature_Enabled'] = True
    traindataconfig['RotateFeature_Checked'] = False
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False

    def setupGUI(self, TrainMl15DDcnnFromScratch):
        TrainMl15DDcnnFromScratch.setObjectName('TrainMl15DDcnnFromScratch')
        TrainMl15DDcnnFromScratch.setFixedSize(810, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl15DDcnnFromScratch.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl15DDcnnFromScratch)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl15DDcnnFromScratch)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl15DDcnnFromScratch)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 50, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 50, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl15DDcnnFromScratch)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 90, 180, 200))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 50, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 50, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(TrainMl15DDcnnFromScratch)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 90, 180, 200))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 300, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 300, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 300, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 340, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 340, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 300, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 300, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 300, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 340, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 340, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl15DDcnnFromScratch)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 310, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 350, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.lbldropout = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 390, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 390, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl15DDcnnFromScratch)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl15DDcnnFromScratch)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 440, 180, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl15DDcnnFromScratch)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 440, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl15DDcnnFromScratch)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl15DDcnnFromScratch)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl15DDcnnFromScratch.geometry().center().x()
        _center_y = TrainMl15DDcnnFromScratch.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl15DDcnnFromScratch)
        QtCore.QMetaObject.connectSlotsByName(TrainMl15DDcnnFromScratch)

    def retranslateGUI(self, TrainMl15DDcnnFromScratch):
        self.dialog = TrainMl15DDcnnFromScratch
        _translate = QtCore.QCoreApplication.translate
        TrainMl15DDcnnFromScratch.setWindowTitle(_translate('TrainMl15DDcnnFromScratch', 'Train 1.5D-DCNN from scratch'))
        self.lblfeature.setText(_translate('TrainMl15DDcnnFromScratch', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl15DDcnnFromScratch', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl15DDcnnFromScratch', 'Select target:'))
        self.btnconfigtraindata.setText(_translate('TrainMl15DDcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('TrainMl15DDcnnFromScratch', 'Original\nimage\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl15DDcnnFromScratch', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl15DDcnnFromScratch', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl15DDcnnFromScratch', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl15DDcnnFromScratch', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl15DDcnnFromScratch', 'Interpolated\nimage\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl15DDcnnFromScratch', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl15DDcnnFromScratch', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl15DDcnnFromScratch', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl15DDcnnFromScratch', '32'))
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
                    item.setText(_translate('TrainMl15DDcnnFromScratch', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl15DDcnnFromScratch', 'Specify DCNN architecture:'))
        self.lblnconvblock.setText(_translate('TrainMl15DDcnnFromScratch', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl15DDcnnFromScratch', '3'))
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setColumnCount(3)
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

        self.lbln1x1layer.setText(_translate('TrainMl15DDcnnFromScratch', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('TrainMl15DDcnnFromScratch', '2'))
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.twgn1x1layer.setRowCount(2)
        for _idx in range(int(self.ldtn1x1layer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl15DDcnnFromScratch', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgn1x1layer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgn1x1layer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl15DDcnnFromScratch', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl15DDcnnFromScratch', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl15DDcnnFromScratch', '3'))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('TrainMl15DDcnnFromScratch', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl15DDcnnFromScratch', '3'))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('TrainMl15DDcnnFromScratch', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl15DDcnnFromScratch', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl15DDcnnFromScratch', '2'))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl15DDcnnFromScratch', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl15DDcnnFromScratch', '2'))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('TrainMl15DDcnnFromScratch', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl15DDcnnFromScratch', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl15DDcnnFromScratch', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl15DDcnnFromScratch', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl15DDcnnFromScratch', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl15DDcnnFromScratch', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl15DDcnnFromScratch', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('TrainMl15DDcnnFromScratch', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('TrainMl15DDcnnFromScratch', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl15DDcnnFromScratch', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl15DDcnnFromScratch', ''))
        self.btnsave.setText(_translate('TrainMl15DDcnnFromScratch', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl15DDcnnFromScratch', 'Train 1.5D-DCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl15DDcnnFromScratch)

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

    def changeLdtN1x1layer(self):
        if len(self.ldtn1x1layer.text()) > 0:
            _nlayer = int(self.ldtn1x1layer.text())
            self.twgn1x1layer.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgn1x1layer.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(1024))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgn1x1layer.setItem(_idx, 1, item)

        else:
            self.twgn1x1layer.setRowCount(0)

    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Save DCNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
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

    def clickBtnTrainMl15DDcnnFromScratch(self):
        self.refreshMsgBox()
        if len(self.lwgfeature.selectedItems()) < 1:
            vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: No feature selected for training', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'No feature selected for training')
            return
        _image_height = basic_data.str2int(self.ldtoldheight.text())
        _image_width = basic_data.str2int(self.ldtoldwidth.text())
        _image_height_new = basic_data.str2int(self.ldtnewheight.text())
        _image_width_new = basic_data.str2int(self.ldtnewwidth.text())
        if _image_height is False or _image_width is False or _image_height_new is False or _image_width_new is False:
            vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Non-integer feature size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Non-integer feature size')
            return
        if _image_height < 2 or _image_width < 2 or _image_height_new < 2 or _image_width_new < 2:
            vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Features are not 2D', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Features are not 2D')
            return
        _image_height = 2 * int(_image_height / 2) + 1
        _image_width = 2 * int(_image_width / 2) + 1
        _features = self.lwgfeature.selectedItems()
        _features = [f.text() for f in _features]
        _target = self.featurelist[self.cbbtarget.currentIndex()]
        if _target in _features:
            vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Target also used as features', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Target also used as features')
            return
        _nconvblock = basic_data.str2int(self.ldtnconvblock.text())
        _nconvlayer = [basic_data.str2int(self.twgnconvblock.item(i, 1).text()) for i in range(_nconvblock)]
        _nconvfeature = [basic_data.str2int(self.twgnconvblock.item(i, 2).text()) for i in range(_nconvblock)]
        _n1x1layer = basic_data.str2int(self.ldtn1x1layer.text())
        _n1x1feature = [basic_data.str2int(self.twgn1x1layer.item(i, 1).text()) for i in range(_n1x1layer)]
        _patch_height = basic_data.str2int(self.ldtmaskheight.text())
        _patch_width = basic_data.str2int(self.ldtmaskwidth.text())
        _pool_height = basic_data.str2int(self.ldtpoolheight.text())
        _pool_width = basic_data.str2int(self.ldtpoolwidth.text())
        _nepoch = basic_data.str2int(self.ldtnepoch.text())
        _batchsize = basic_data.str2int(self.ldtbatchsize.text())
        _learning_rate = basic_data.str2float(self.ldtlearnrate.text())
        _dropout_prob = basic_data.str2float(self.ldtdropout.text())
        if _nconvblock is False or _nconvblock <= 0:
            vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Non-positive convolutional block number', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Non-positive convolutional block number')
            return
        for _i in _nconvlayer:
            if _i is False or _i < 1:
                vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Non-positive convolutional layer number', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Non-positive convolutional layer number')
                return

        for _i in _nconvfeature:
            if _i is False or _i < 1:
                vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Non-positive convolutional feature number', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Non-positive convolutional feature number')
                return

        if _n1x1layer is False or _n1x1layer <= 0:
            vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Non-positive 1x1 convolutional layer number', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Non-positive 1x1 convolutional layer number')
            return
        for _i in _n1x1feature:
            if _i is False or _i < 1:
                vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Non-positive 1x1 convolutional feature number', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Non-positive 1x1 convolutional feature number')
                return

        if _patch_height is False or _patch_width is False or _patch_height < 1 or _patch_width < 1:
            vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Non-positive convolutional patch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Non-positive convolutional patch size')
            return
        if _pool_height is False or _pool_width is False or _pool_height < 1 or _pool_width < 1:
            vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Non-positive pooling size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Non-positive pooling size')
            return
        if _nepoch is False or _nepoch <= 0:
            vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Non-positive epoch number', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Non-positive epoch number')
            return
        if _batchsize is False or _batchsize <= 0:
            vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Non-positive batch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Non-positive batch size')
            return
        if _learning_rate is False or _learning_rate <= 0:
            vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Non-positive learning rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Non-positive learning rate')
            return
        if _dropout_prob is False or _dropout_prob <= 0:
            vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: Negative dropout rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'Negative dropout rate')
            return
        if len(self.ldtsave.text()) < 1:
            vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: No name specified for DCNN network', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'No name specified for DCNN network')
            return
        _savepath = os.path.dirname(self.ldtsave.text())
        _savename = os.path.splitext(os.path.basename(self.ldtsave.text()))[0]
        _wdinl = 0
        _wdxl = 0
        _wdz = 0
        _wdinltarget = 0
        _wdxltarget = 0
        _wdztarget = 0
        if self.cbbornt.currentIndex() == 0:
            _wdxl = int(_image_width / 2)
            _wdz = int(_image_height / 2)
            _wdztarget = int(_image_height / 2)
        if self.cbbornt.currentIndex() == 1:
            _wdinl = int(_image_width / 2)
            _wdz = int(_image_height / 2)
            _wdztarget = int(_image_height / 2)
        if self.cbbornt.currentIndex() == 2:
            _wdinl = int(_image_width / 2)
            _wdxl = int(_image_height / 2)
            _wdxltarget = int(_image_height / 2)
        _seisinfo = self.survinfo
        print('TrainMl15DDcnnFromScratch: Step 1 - Get training samples:')
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
            vis_msg.print('ERROR in TrainMl2DDCnnFromScratch: No training sample found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'No training sample found')
            return
        print('TrainMl15DDcnnFromScratch: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)' % (
         _image_height, _image_width, _image_height_new, _image_width_new))
        _traindict = {}
        for f in _features:
            _seisdata = self.seisdata[f]
            _traindict[f] = seis_ays.retrieveSeisWindowFrom3DMat(_seisdata, _traindata, seisinfo=(self.survinfo), wdinl=_wdinl,
              wdxl=_wdxl,
              wdz=_wdz,
              verbose=False)[:, 3:]

        if _target not in _features:
            _seisdata = self.seisdata[_target]
            _traindict[_target] = seis_ays.retrieveSeisWindowFrom3DMat(_seisdata, _traindata, seisinfo=(self.survinfo), wdinl=_wdinltarget,
              wdxl=_wdxltarget,
              wdz=_wdztarget,
              verbose=False)[:, 3:]
        if self.traindataconfig['RemoveInvariantFeature_Checked']:
            for f in _features:
                _traindict = ml_aug.removeInvariantFeature(_traindict, f)
                if basic_mdt.maxDictConstantRow(_traindict) <= 0:
                    vis_msg.print('ERROR in TrainMl15DDcnnFromScratch: No training sample found', type='error')
                    QtWidgets.QMessageBox.critical(self.msgbox, 'Train 1.5D-DCNN', 'No training sample found')
                    return

        if _image_height_new != _image_height or _image_width_new != _image_width:
            for f in _features:
                _traindict[f] = basic_image.changeImageSize((_traindict[f]), image_height=_image_height,
                  image_width=_image_width,
                  image_height_new=_image_height_new,
                  image_width_new=_image_width_new)

        if _image_height_new != _image_height:
            if _target not in _features:
                _traindict[_target] = basic_curve.changeCurveSize((_traindict[_target]), length=_image_height,
                  length_new=_image_height_new,
                  kind='linear')
        if self.traindataconfig['RotateFeature_Checked'] is True:
            for f in _features:
                _traindict[f] = ml_aug.rotateImage4Way(_traindict[f], _image_height_new, _image_width_new)

            if _target not in _features:
                _traindict[_target] = ml_aug.rotateImage4Way(_traindict[_target], _image_height_new, 1)
        _traindict[_target] = np.round(_traindict[_target]).astype(int)
        print('TrainMl15DDcnnFromScratch: A total of %d valid training samples' % basic_mdt.maxDictConstantRow(_traindict))
        print('TrainMl15DDcnnFromScratch: Step 3 - Start training')
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Train 1.5D-DCNN')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _dcnnlog = ml_dcnn15d.create15DDCNNSegmentor(_traindict, imageheight=_image_height_new,
          imagewidth=_image_width_new,
          features=_features,
          target=_target,
          nepoch=_nepoch,
          batchsize=_batchsize,
          nconvblock=_nconvblock,
          nconvfeature=_nconvfeature,
          nconvlayer=_nconvlayer,
          n1x1layer=_n1x1layer,
          n1x1feature=_n1x1feature,
          patchheight=_patch_height,
          patchwidth=_patch_width,
          poolheight=_pool_height,
          poolwidth=_pool_width,
          learningrate=_learning_rate,
          dropoutprob=_dropout_prob,
          save2disk=True,
          savepath=_savepath,
          savename=_savename,
          qpgsdlg=_pgsdlg)
        QtWidgets.QMessageBox.information(self.msgbox, 'Train 1.5D DCNN', 'DCNN trained successfully')
        reply = QtWidgets.QMessageBox.question(self.msgbox, 'Train 1.5D DCNN', 'View learning matrix?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            _viewmllearnmat = QtWidgets.QDialog()
            _gui = gui_viewmllearnmat()
            _gui.linestyle = self.linestyle
            _gui.fontstyle = self.fontstyle
            _gui.learnmat = _dcnnlog['learning_curve']
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
    TrainMl15DDcnnFromScratch = QtWidgets.QWidget()
    gui = trainml15ddcnnfromscratch()
    gui.setupGUI(TrainMl15DDcnnFromScratch)
    TrainMl15DDcnnFromScratch.show()
    sys.exit(app.exec_())