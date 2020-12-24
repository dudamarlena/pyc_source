# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml15ddcnnfromscratch.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 43726 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.pointset.analysis as point_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.curve as basic_curve
import cognitivegeo.src.basic.image as basic_image
import cognitivegeo.src.ml.augmentation as ml_aug
import cognitivegeo.src.ml.dcnnsegmentor15d as ml_dcnn15d
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
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

    def clickBtnTrainMl15DDcnnFromScratch--- This code section failed: ---

 L. 445         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 447         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 448        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 449        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 450        50  LOAD_STR                 'Train 1.5D-DCNN'

 L. 451        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 452        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 454        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_image_height'

 L. 455        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_image_width'

 L. 456        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtnewheight
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_image_height_new'

 L. 457       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewwidth
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_image_width_new'

 L. 458       126  LOAD_FAST                '_image_height'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'
              134  LOAD_FAST                '_image_width'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_TRUE    158  'to 158'

 L. 459       142  LOAD_FAST                '_image_height_new'
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

 L. 460       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 461       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 462       182  LOAD_STR                 'Train 1.5D-DCNN'

 L. 463       184  LOAD_STR                 'Non-integer feature size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 464       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 465       194  LOAD_FAST                '_image_height'
              196  LOAD_CONST               2
              198  COMPARE_OP               <
              200  POP_JUMP_IF_TRUE    228  'to 228'
              202  LOAD_FAST                '_image_width'
              204  LOAD_CONST               2
              206  COMPARE_OP               <
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 466       210  LOAD_FAST                '_image_height_new'
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

 L. 467       228  LOAD_GLOBAL              vis_msg
              230  LOAD_ATTR                print
              232  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 468       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 469       252  LOAD_STR                 'Train 1.5D-DCNN'

 L. 470       254  LOAD_STR                 'Features are not 2D'
              256  CALL_METHOD_3         3  '3 positional arguments'
              258  POP_TOP          

 L. 471       260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           224  '224'

 L. 473       264  LOAD_CONST               2
              266  LOAD_GLOBAL              int
              268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               2
              272  BINARY_TRUE_DIVIDE
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  BINARY_MULTIPLY  
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  STORE_FAST               '_image_height'

 L. 474       284  LOAD_CONST               2
              286  LOAD_GLOBAL              int
              288  LOAD_FAST                '_image_width'
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BINARY_MULTIPLY  
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               '_image_width'

 L. 476       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                lwgfeature
              308  LOAD_METHOD              selectedItems
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               '_features'

 L. 477       314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainml15ddcnnfromscratch.clickBtnTrainMl15DDcnnFromScratch.<locals>.<listcomp>'
              318  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              320  LOAD_FAST                '_features'
              322  GET_ITER         
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               '_features'

 L. 478       328  LOAD_DEREF               'self'
              330  LOAD_ATTR                featurelist
              332  LOAD_DEREF               'self'
              334  LOAD_ATTR                cbbtarget
              336  LOAD_METHOD              currentIndex
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  BINARY_SUBSCR    
              342  STORE_FAST               '_target'

 L. 480       344  LOAD_FAST                '_target'
              346  LOAD_FAST                '_features'
              348  COMPARE_OP               in
          350_352  POP_JUMP_IF_FALSE   390  'to 390'

 L. 481       354  LOAD_GLOBAL              vis_msg
              356  LOAD_ATTR                print
              358  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Target also used as features'
              360  LOAD_STR                 'error'
              362  LOAD_CONST               ('type',)
              364  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              366  POP_TOP          

 L. 482       368  LOAD_GLOBAL              QtWidgets
              370  LOAD_ATTR                QMessageBox
              372  LOAD_METHOD              critical
              374  LOAD_DEREF               'self'
              376  LOAD_ATTR                msgbox

 L. 483       378  LOAD_STR                 'Train 1.5D-DCNN'

 L. 484       380  LOAD_STR                 'Target also used as features'
              382  CALL_METHOD_3         3  '3 positional arguments'
              384  POP_TOP          

 L. 485       386  LOAD_CONST               None
              388  RETURN_VALUE     
            390_0  COME_FROM           350  '350'

 L. 487       390  LOAD_GLOBAL              basic_data
              392  LOAD_METHOD              str2int
              394  LOAD_DEREF               'self'
              396  LOAD_ATTR                ldtnconvblock
              398  LOAD_METHOD              text
              400  CALL_METHOD_0         0  '0 positional arguments'
              402  CALL_METHOD_1         1  '1 positional argument'
              404  STORE_FAST               '_nconvblock'

 L. 488       406  LOAD_CLOSURE             'self'
              408  BUILD_TUPLE_1         1 
              410  LOAD_LISTCOMP            '<code_object <listcomp>>'
              412  LOAD_STR                 'trainml15ddcnnfromscratch.clickBtnTrainMl15DDcnnFromScratch.<locals>.<listcomp>'
              414  MAKE_FUNCTION_8          'closure'
              416  LOAD_GLOBAL              range
              418  LOAD_FAST                '_nconvblock'
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  GET_ITER         
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  STORE_FAST               '_nconvlayer'

 L. 489       428  LOAD_CLOSURE             'self'
              430  BUILD_TUPLE_1         1 
              432  LOAD_LISTCOMP            '<code_object <listcomp>>'
              434  LOAD_STR                 'trainml15ddcnnfromscratch.clickBtnTrainMl15DDcnnFromScratch.<locals>.<listcomp>'
              436  MAKE_FUNCTION_8          'closure'
              438  LOAD_GLOBAL              range
              440  LOAD_FAST                '_nconvblock'
              442  CALL_FUNCTION_1       1  '1 positional argument'
              444  GET_ITER         
              446  CALL_FUNCTION_1       1  '1 positional argument'
              448  STORE_FAST               '_nconvfeature'

 L. 490       450  LOAD_GLOBAL              basic_data
              452  LOAD_METHOD              str2int
              454  LOAD_DEREF               'self'
              456  LOAD_ATTR                ldtn1x1layer
              458  LOAD_METHOD              text
              460  CALL_METHOD_0         0  '0 positional arguments'
              462  CALL_METHOD_1         1  '1 positional argument'
              464  STORE_FAST               '_n1x1layer'

 L. 491       466  LOAD_CLOSURE             'self'
              468  BUILD_TUPLE_1         1 
              470  LOAD_LISTCOMP            '<code_object <listcomp>>'
              472  LOAD_STR                 'trainml15ddcnnfromscratch.clickBtnTrainMl15DDcnnFromScratch.<locals>.<listcomp>'
              474  MAKE_FUNCTION_8          'closure'
              476  LOAD_GLOBAL              range
              478  LOAD_FAST                '_n1x1layer'
              480  CALL_FUNCTION_1       1  '1 positional argument'
              482  GET_ITER         
              484  CALL_FUNCTION_1       1  '1 positional argument'
              486  STORE_FAST               '_n1x1feature'

 L. 492       488  LOAD_GLOBAL              basic_data
              490  LOAD_METHOD              str2int
              492  LOAD_DEREF               'self'
              494  LOAD_ATTR                ldtmaskheight
              496  LOAD_METHOD              text
              498  CALL_METHOD_0         0  '0 positional arguments'
              500  CALL_METHOD_1         1  '1 positional argument'
              502  STORE_FAST               '_patch_height'

 L. 493       504  LOAD_GLOBAL              basic_data
              506  LOAD_METHOD              str2int
              508  LOAD_DEREF               'self'
              510  LOAD_ATTR                ldtmaskwidth
              512  LOAD_METHOD              text
              514  CALL_METHOD_0         0  '0 positional arguments'
              516  CALL_METHOD_1         1  '1 positional argument'
              518  STORE_FAST               '_patch_width'

 L. 494       520  LOAD_GLOBAL              basic_data
              522  LOAD_METHOD              str2int
              524  LOAD_DEREF               'self'
              526  LOAD_ATTR                ldtpoolheight
              528  LOAD_METHOD              text
              530  CALL_METHOD_0         0  '0 positional arguments'
              532  CALL_METHOD_1         1  '1 positional argument'
              534  STORE_FAST               '_pool_height'

 L. 495       536  LOAD_GLOBAL              basic_data
              538  LOAD_METHOD              str2int
              540  LOAD_DEREF               'self'
              542  LOAD_ATTR                ldtpoolwidth
              544  LOAD_METHOD              text
              546  CALL_METHOD_0         0  '0 positional arguments'
              548  CALL_METHOD_1         1  '1 positional argument'
              550  STORE_FAST               '_pool_width'

 L. 496       552  LOAD_GLOBAL              basic_data
              554  LOAD_METHOD              str2int
              556  LOAD_DEREF               'self'
              558  LOAD_ATTR                ldtnepoch
              560  LOAD_METHOD              text
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  CALL_METHOD_1         1  '1 positional argument'
              566  STORE_FAST               '_nepoch'

 L. 497       568  LOAD_GLOBAL              basic_data
              570  LOAD_METHOD              str2int
              572  LOAD_DEREF               'self'
              574  LOAD_ATTR                ldtbatchsize
              576  LOAD_METHOD              text
              578  CALL_METHOD_0         0  '0 positional arguments'
              580  CALL_METHOD_1         1  '1 positional argument'
              582  STORE_FAST               '_batchsize'

 L. 498       584  LOAD_GLOBAL              basic_data
              586  LOAD_METHOD              str2float
              588  LOAD_DEREF               'self'
              590  LOAD_ATTR                ldtlearnrate
              592  LOAD_METHOD              text
              594  CALL_METHOD_0         0  '0 positional arguments'
              596  CALL_METHOD_1         1  '1 positional argument'
              598  STORE_FAST               '_learning_rate'

 L. 499       600  LOAD_GLOBAL              basic_data
              602  LOAD_METHOD              str2float
              604  LOAD_DEREF               'self'
              606  LOAD_ATTR                ldtdropout
              608  LOAD_METHOD              text
              610  CALL_METHOD_0         0  '0 positional arguments'
              612  CALL_METHOD_1         1  '1 positional argument'
              614  STORE_FAST               '_dropout_prob'

 L. 500       616  LOAD_FAST                '_nconvblock'
              618  LOAD_CONST               False
              620  COMPARE_OP               is
          622_624  POP_JUMP_IF_TRUE    636  'to 636'
              626  LOAD_FAST                '_nconvblock'
              628  LOAD_CONST               0
              630  COMPARE_OP               <=
          632_634  POP_JUMP_IF_FALSE   672  'to 672'
            636_0  COME_FROM           622  '622'

 L. 501       636  LOAD_GLOBAL              vis_msg
              638  LOAD_ATTR                print
              640  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Non-positive convolutional block number'

 L. 502       642  LOAD_STR                 'error'
              644  LOAD_CONST               ('type',)
              646  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              648  POP_TOP          

 L. 503       650  LOAD_GLOBAL              QtWidgets
              652  LOAD_ATTR                QMessageBox
              654  LOAD_METHOD              critical
              656  LOAD_DEREF               'self'
              658  LOAD_ATTR                msgbox

 L. 504       660  LOAD_STR                 'Train 1.5D-DCNN'

 L. 505       662  LOAD_STR                 'Non-positive convolutional block number'
              664  CALL_METHOD_3         3  '3 positional arguments'
              666  POP_TOP          

 L. 506       668  LOAD_CONST               None
              670  RETURN_VALUE     
            672_0  COME_FROM           632  '632'

 L. 507       672  SETUP_LOOP          744  'to 744'
              674  LOAD_FAST                '_nconvlayer'
              676  GET_ITER         
            678_0  COME_FROM           698  '698'
              678  FOR_ITER            742  'to 742'
              680  STORE_FAST               '_i'

 L. 508       682  LOAD_FAST                '_i'
              684  LOAD_CONST               False
              686  COMPARE_OP               is
          688_690  POP_JUMP_IF_TRUE    702  'to 702'
              692  LOAD_FAST                '_i'
              694  LOAD_CONST               1
              696  COMPARE_OP               <
          698_700  POP_JUMP_IF_FALSE   678  'to 678'
            702_0  COME_FROM           688  '688'

 L. 509       702  LOAD_GLOBAL              vis_msg
              704  LOAD_ATTR                print
              706  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Non-positive convolutional layer number'

 L. 510       708  LOAD_STR                 'error'
              710  LOAD_CONST               ('type',)
              712  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              714  POP_TOP          

 L. 511       716  LOAD_GLOBAL              QtWidgets
              718  LOAD_ATTR                QMessageBox
              720  LOAD_METHOD              critical
              722  LOAD_DEREF               'self'
              724  LOAD_ATTR                msgbox

 L. 512       726  LOAD_STR                 'Train 1.5D-DCNN'

 L. 513       728  LOAD_STR                 'Non-positive convolutional layer number'
              730  CALL_METHOD_3         3  '3 positional arguments'
              732  POP_TOP          

 L. 514       734  LOAD_CONST               None
              736  RETURN_VALUE     
          738_740  JUMP_BACK           678  'to 678'
              742  POP_BLOCK        
            744_0  COME_FROM_LOOP      672  '672'

 L. 515       744  SETUP_LOOP          816  'to 816'
              746  LOAD_FAST                '_nconvfeature'
              748  GET_ITER         
            750_0  COME_FROM           770  '770'
              750  FOR_ITER            814  'to 814'
              752  STORE_FAST               '_i'

 L. 516       754  LOAD_FAST                '_i'
              756  LOAD_CONST               False
              758  COMPARE_OP               is
          760_762  POP_JUMP_IF_TRUE    774  'to 774'
              764  LOAD_FAST                '_i'
              766  LOAD_CONST               1
              768  COMPARE_OP               <
          770_772  POP_JUMP_IF_FALSE   750  'to 750'
            774_0  COME_FROM           760  '760'

 L. 517       774  LOAD_GLOBAL              vis_msg
              776  LOAD_ATTR                print
              778  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Non-positive convolutional feature number'

 L. 518       780  LOAD_STR                 'error'
              782  LOAD_CONST               ('type',)
              784  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              786  POP_TOP          

 L. 519       788  LOAD_GLOBAL              QtWidgets
              790  LOAD_ATTR                QMessageBox
              792  LOAD_METHOD              critical
              794  LOAD_DEREF               'self'
              796  LOAD_ATTR                msgbox

 L. 520       798  LOAD_STR                 'Train 1.5D-DCNN'

 L. 521       800  LOAD_STR                 'Non-positive convolutional feature number'
              802  CALL_METHOD_3         3  '3 positional arguments'
              804  POP_TOP          

 L. 522       806  LOAD_CONST               None
              808  RETURN_VALUE     
          810_812  JUMP_BACK           750  'to 750'
              814  POP_BLOCK        
            816_0  COME_FROM_LOOP      744  '744'

 L. 523       816  LOAD_FAST                '_n1x1layer'
              818  LOAD_CONST               False
              820  COMPARE_OP               is
          822_824  POP_JUMP_IF_TRUE    836  'to 836'
              826  LOAD_FAST                '_n1x1layer'
              828  LOAD_CONST               0
              830  COMPARE_OP               <=
          832_834  POP_JUMP_IF_FALSE   872  'to 872'
            836_0  COME_FROM           822  '822'

 L. 524       836  LOAD_GLOBAL              vis_msg
              838  LOAD_ATTR                print
              840  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Non-positive 1x1 convolutional layer number'

 L. 525       842  LOAD_STR                 'error'
              844  LOAD_CONST               ('type',)
              846  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              848  POP_TOP          

 L. 526       850  LOAD_GLOBAL              QtWidgets
              852  LOAD_ATTR                QMessageBox
              854  LOAD_METHOD              critical
              856  LOAD_DEREF               'self'
              858  LOAD_ATTR                msgbox

 L. 527       860  LOAD_STR                 'Train 1.5D-DCNN'

 L. 528       862  LOAD_STR                 'Non-positive 1x1 convolutional layer number'
              864  CALL_METHOD_3         3  '3 positional arguments'
              866  POP_TOP          

 L. 529       868  LOAD_CONST               None
              870  RETURN_VALUE     
            872_0  COME_FROM           832  '832'

 L. 530       872  SETUP_LOOP          944  'to 944'
              874  LOAD_FAST                '_n1x1feature'
              876  GET_ITER         
            878_0  COME_FROM           898  '898'
              878  FOR_ITER            942  'to 942'
              880  STORE_FAST               '_i'

 L. 531       882  LOAD_FAST                '_i'
              884  LOAD_CONST               False
              886  COMPARE_OP               is
          888_890  POP_JUMP_IF_TRUE    902  'to 902'
              892  LOAD_FAST                '_i'
              894  LOAD_CONST               1
              896  COMPARE_OP               <
          898_900  POP_JUMP_IF_FALSE   878  'to 878'
            902_0  COME_FROM           888  '888'

 L. 532       902  LOAD_GLOBAL              vis_msg
              904  LOAD_ATTR                print
              906  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Non-positive 1x1 convolutional feature number'

 L. 533       908  LOAD_STR                 'error'
              910  LOAD_CONST               ('type',)
              912  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              914  POP_TOP          

 L. 534       916  LOAD_GLOBAL              QtWidgets
              918  LOAD_ATTR                QMessageBox
              920  LOAD_METHOD              critical
              922  LOAD_DEREF               'self'
              924  LOAD_ATTR                msgbox

 L. 535       926  LOAD_STR                 'Train 1.5D-DCNN'

 L. 536       928  LOAD_STR                 'Non-positive 1x1 convolutional feature number'
              930  CALL_METHOD_3         3  '3 positional arguments'
              932  POP_TOP          

 L. 537       934  LOAD_CONST               None
              936  RETURN_VALUE     
          938_940  JUMP_BACK           878  'to 878'
              942  POP_BLOCK        
            944_0  COME_FROM_LOOP      872  '872'

 L. 538       944  LOAD_FAST                '_patch_height'
              946  LOAD_CONST               False
              948  COMPARE_OP               is
          950_952  POP_JUMP_IF_TRUE    984  'to 984'
              954  LOAD_FAST                '_patch_width'
              956  LOAD_CONST               False
              958  COMPARE_OP               is
          960_962  POP_JUMP_IF_TRUE    984  'to 984'

 L. 539       964  LOAD_FAST                '_patch_height'
              966  LOAD_CONST               1
              968  COMPARE_OP               <
          970_972  POP_JUMP_IF_TRUE    984  'to 984'
              974  LOAD_FAST                '_patch_width'
              976  LOAD_CONST               1
              978  COMPARE_OP               <
          980_982  POP_JUMP_IF_FALSE  1020  'to 1020'
            984_0  COME_FROM           970  '970'
            984_1  COME_FROM           960  '960'
            984_2  COME_FROM           950  '950'

 L. 540       984  LOAD_GLOBAL              vis_msg
              986  LOAD_ATTR                print
              988  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Non-positive convolutional patch size'

 L. 541       990  LOAD_STR                 'error'
              992  LOAD_CONST               ('type',)
              994  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              996  POP_TOP          

 L. 542       998  LOAD_GLOBAL              QtWidgets
             1000  LOAD_ATTR                QMessageBox
             1002  LOAD_METHOD              critical
             1004  LOAD_DEREF               'self'
             1006  LOAD_ATTR                msgbox

 L. 543      1008  LOAD_STR                 'Train 1.5D-DCNN'

 L. 544      1010  LOAD_STR                 'Non-positive convolutional patch size'
             1012  CALL_METHOD_3         3  '3 positional arguments'
             1014  POP_TOP          

 L. 545      1016  LOAD_CONST               None
             1018  RETURN_VALUE     
           1020_0  COME_FROM           980  '980'

 L. 546      1020  LOAD_FAST                '_pool_height'
             1022  LOAD_CONST               False
             1024  COMPARE_OP               is
         1026_1028  POP_JUMP_IF_TRUE   1060  'to 1060'
             1030  LOAD_FAST                '_pool_width'
             1032  LOAD_CONST               False
             1034  COMPARE_OP               is
         1036_1038  POP_JUMP_IF_TRUE   1060  'to 1060'

 L. 547      1040  LOAD_FAST                '_pool_height'
             1042  LOAD_CONST               1
             1044  COMPARE_OP               <
         1046_1048  POP_JUMP_IF_TRUE   1060  'to 1060'
             1050  LOAD_FAST                '_pool_width'
             1052  LOAD_CONST               1
             1054  COMPARE_OP               <
         1056_1058  POP_JUMP_IF_FALSE  1096  'to 1096'
           1060_0  COME_FROM          1046  '1046'
           1060_1  COME_FROM          1036  '1036'
           1060_2  COME_FROM          1026  '1026'

 L. 548      1060  LOAD_GLOBAL              vis_msg
             1062  LOAD_ATTR                print
             1064  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Non-positive pooling size'
             1066  LOAD_STR                 'error'
             1068  LOAD_CONST               ('type',)
             1070  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1072  POP_TOP          

 L. 549      1074  LOAD_GLOBAL              QtWidgets
             1076  LOAD_ATTR                QMessageBox
             1078  LOAD_METHOD              critical
             1080  LOAD_DEREF               'self'
             1082  LOAD_ATTR                msgbox

 L. 550      1084  LOAD_STR                 'Train 1.5D-DCNN'

 L. 551      1086  LOAD_STR                 'Non-positive pooling size'
             1088  CALL_METHOD_3         3  '3 positional arguments'
             1090  POP_TOP          

 L. 552      1092  LOAD_CONST               None
             1094  RETURN_VALUE     
           1096_0  COME_FROM          1056  '1056'

 L. 553      1096  LOAD_FAST                '_nepoch'
             1098  LOAD_CONST               False
             1100  COMPARE_OP               is
         1102_1104  POP_JUMP_IF_TRUE   1116  'to 1116'
             1106  LOAD_FAST                '_nepoch'
             1108  LOAD_CONST               0
             1110  COMPARE_OP               <=
         1112_1114  POP_JUMP_IF_FALSE  1152  'to 1152'
           1116_0  COME_FROM          1102  '1102'

 L. 554      1116  LOAD_GLOBAL              vis_msg
             1118  LOAD_ATTR                print
             1120  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Non-positive epoch number'
             1122  LOAD_STR                 'error'
             1124  LOAD_CONST               ('type',)
             1126  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1128  POP_TOP          

 L. 555      1130  LOAD_GLOBAL              QtWidgets
             1132  LOAD_ATTR                QMessageBox
             1134  LOAD_METHOD              critical
             1136  LOAD_DEREF               'self'
             1138  LOAD_ATTR                msgbox

 L. 556      1140  LOAD_STR                 'Train 1.5D-DCNN'

 L. 557      1142  LOAD_STR                 'Non-positive epoch number'
             1144  CALL_METHOD_3         3  '3 positional arguments'
             1146  POP_TOP          

 L. 558      1148  LOAD_CONST               None
             1150  RETURN_VALUE     
           1152_0  COME_FROM          1112  '1112'

 L. 559      1152  LOAD_FAST                '_batchsize'
             1154  LOAD_CONST               False
             1156  COMPARE_OP               is
         1158_1160  POP_JUMP_IF_TRUE   1172  'to 1172'
             1162  LOAD_FAST                '_batchsize'
             1164  LOAD_CONST               0
             1166  COMPARE_OP               <=
         1168_1170  POP_JUMP_IF_FALSE  1208  'to 1208'
           1172_0  COME_FROM          1158  '1158'

 L. 560      1172  LOAD_GLOBAL              vis_msg
             1174  LOAD_ATTR                print
             1176  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Non-positive batch size'
             1178  LOAD_STR                 'error'
             1180  LOAD_CONST               ('type',)
             1182  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1184  POP_TOP          

 L. 561      1186  LOAD_GLOBAL              QtWidgets
             1188  LOAD_ATTR                QMessageBox
             1190  LOAD_METHOD              critical
             1192  LOAD_DEREF               'self'
             1194  LOAD_ATTR                msgbox

 L. 562      1196  LOAD_STR                 'Train 1.5D-DCNN'

 L. 563      1198  LOAD_STR                 'Non-positive batch size'
             1200  CALL_METHOD_3         3  '3 positional arguments'
             1202  POP_TOP          

 L. 564      1204  LOAD_CONST               None
             1206  RETURN_VALUE     
           1208_0  COME_FROM          1168  '1168'

 L. 565      1208  LOAD_FAST                '_learning_rate'
             1210  LOAD_CONST               False
             1212  COMPARE_OP               is
         1214_1216  POP_JUMP_IF_TRUE   1228  'to 1228'
             1218  LOAD_FAST                '_learning_rate'
             1220  LOAD_CONST               0
             1222  COMPARE_OP               <=
         1224_1226  POP_JUMP_IF_FALSE  1264  'to 1264'
           1228_0  COME_FROM          1214  '1214'

 L. 566      1228  LOAD_GLOBAL              vis_msg
             1230  LOAD_ATTR                print
             1232  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Non-positive learning rate'
             1234  LOAD_STR                 'error'
             1236  LOAD_CONST               ('type',)
             1238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1240  POP_TOP          

 L. 567      1242  LOAD_GLOBAL              QtWidgets
             1244  LOAD_ATTR                QMessageBox
             1246  LOAD_METHOD              critical
             1248  LOAD_DEREF               'self'
             1250  LOAD_ATTR                msgbox

 L. 568      1252  LOAD_STR                 'Train 1.5D-DCNN'

 L. 569      1254  LOAD_STR                 'Non-positive learning rate'
             1256  CALL_METHOD_3         3  '3 positional arguments'
             1258  POP_TOP          

 L. 570      1260  LOAD_CONST               None
             1262  RETURN_VALUE     
           1264_0  COME_FROM          1224  '1224'

 L. 571      1264  LOAD_FAST                '_dropout_prob'
             1266  LOAD_CONST               False
             1268  COMPARE_OP               is
         1270_1272  POP_JUMP_IF_TRUE   1284  'to 1284'
             1274  LOAD_FAST                '_dropout_prob'
             1276  LOAD_CONST               0
             1278  COMPARE_OP               <=
         1280_1282  POP_JUMP_IF_FALSE  1320  'to 1320'
           1284_0  COME_FROM          1270  '1270'

 L. 572      1284  LOAD_GLOBAL              vis_msg
             1286  LOAD_ATTR                print
             1288  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: Negative dropout rate'
             1290  LOAD_STR                 'error'
             1292  LOAD_CONST               ('type',)
             1294  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1296  POP_TOP          

 L. 573      1298  LOAD_GLOBAL              QtWidgets
             1300  LOAD_ATTR                QMessageBox
             1302  LOAD_METHOD              critical
             1304  LOAD_DEREF               'self'
             1306  LOAD_ATTR                msgbox

 L. 574      1308  LOAD_STR                 'Train 1.5D-DCNN'

 L. 575      1310  LOAD_STR                 'Negative dropout rate'
             1312  CALL_METHOD_3         3  '3 positional arguments'
             1314  POP_TOP          

 L. 576      1316  LOAD_CONST               None
             1318  RETURN_VALUE     
           1320_0  COME_FROM          1280  '1280'

 L. 578      1320  LOAD_GLOBAL              len
             1322  LOAD_DEREF               'self'
             1324  LOAD_ATTR                ldtsave
             1326  LOAD_METHOD              text
             1328  CALL_METHOD_0         0  '0 positional arguments'
             1330  CALL_FUNCTION_1       1  '1 positional argument'
             1332  LOAD_CONST               1
             1334  COMPARE_OP               <
         1336_1338  POP_JUMP_IF_FALSE  1376  'to 1376'

 L. 579      1340  LOAD_GLOBAL              vis_msg
             1342  LOAD_ATTR                print
             1344  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: No name specified for DCNN network'
             1346  LOAD_STR                 'error'
             1348  LOAD_CONST               ('type',)
             1350  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1352  POP_TOP          

 L. 580      1354  LOAD_GLOBAL              QtWidgets
             1356  LOAD_ATTR                QMessageBox
             1358  LOAD_METHOD              critical
             1360  LOAD_DEREF               'self'
             1362  LOAD_ATTR                msgbox

 L. 581      1364  LOAD_STR                 'Train 1.5D-DCNN'

 L. 582      1366  LOAD_STR                 'No name specified for DCNN network'
             1368  CALL_METHOD_3         3  '3 positional arguments'
             1370  POP_TOP          

 L. 583      1372  LOAD_CONST               None
             1374  RETURN_VALUE     
           1376_0  COME_FROM          1336  '1336'

 L. 584      1376  LOAD_GLOBAL              os
             1378  LOAD_ATTR                path
             1380  LOAD_METHOD              dirname
             1382  LOAD_DEREF               'self'
             1384  LOAD_ATTR                ldtsave
             1386  LOAD_METHOD              text
             1388  CALL_METHOD_0         0  '0 positional arguments'
             1390  CALL_METHOD_1         1  '1 positional argument'
             1392  STORE_FAST               '_savepath'

 L. 585      1394  LOAD_GLOBAL              os
             1396  LOAD_ATTR                path
             1398  LOAD_METHOD              splitext
             1400  LOAD_GLOBAL              os
             1402  LOAD_ATTR                path
             1404  LOAD_METHOD              basename
             1406  LOAD_DEREF               'self'
             1408  LOAD_ATTR                ldtsave
             1410  LOAD_METHOD              text
             1412  CALL_METHOD_0         0  '0 positional arguments'
             1414  CALL_METHOD_1         1  '1 positional argument'
             1416  CALL_METHOD_1         1  '1 positional argument'
             1418  LOAD_CONST               0
             1420  BINARY_SUBSCR    
             1422  STORE_FAST               '_savename'

 L. 587      1424  LOAD_CONST               0
             1426  STORE_FAST               '_wdinl'

 L. 588      1428  LOAD_CONST               0
             1430  STORE_FAST               '_wdxl'

 L. 589      1432  LOAD_CONST               0
             1434  STORE_FAST               '_wdz'

 L. 590      1436  LOAD_CONST               0
             1438  STORE_FAST               '_wdinltarget'

 L. 591      1440  LOAD_CONST               0
             1442  STORE_FAST               '_wdxltarget'

 L. 592      1444  LOAD_CONST               0
             1446  STORE_FAST               '_wdztarget'

 L. 593      1448  LOAD_DEREF               'self'
             1450  LOAD_ATTR                cbbornt
             1452  LOAD_METHOD              currentIndex
             1454  CALL_METHOD_0         0  '0 positional arguments'
             1456  LOAD_CONST               0
             1458  COMPARE_OP               ==
         1460_1462  POP_JUMP_IF_FALSE  1500  'to 1500'

 L. 594      1464  LOAD_GLOBAL              int
             1466  LOAD_FAST                '_image_width'
             1468  LOAD_CONST               2
             1470  BINARY_TRUE_DIVIDE
             1472  CALL_FUNCTION_1       1  '1 positional argument'
             1474  STORE_FAST               '_wdxl'

 L. 595      1476  LOAD_GLOBAL              int
             1478  LOAD_FAST                '_image_height'
             1480  LOAD_CONST               2
             1482  BINARY_TRUE_DIVIDE
             1484  CALL_FUNCTION_1       1  '1 positional argument'
             1486  STORE_FAST               '_wdz'

 L. 596      1488  LOAD_GLOBAL              int
             1490  LOAD_FAST                '_image_height'
             1492  LOAD_CONST               2
             1494  BINARY_TRUE_DIVIDE
             1496  CALL_FUNCTION_1       1  '1 positional argument'
             1498  STORE_FAST               '_wdztarget'
           1500_0  COME_FROM          1460  '1460'

 L. 597      1500  LOAD_DEREF               'self'
             1502  LOAD_ATTR                cbbornt
             1504  LOAD_METHOD              currentIndex
             1506  CALL_METHOD_0         0  '0 positional arguments'
             1508  LOAD_CONST               1
             1510  COMPARE_OP               ==
         1512_1514  POP_JUMP_IF_FALSE  1552  'to 1552'

 L. 598      1516  LOAD_GLOBAL              int
             1518  LOAD_FAST                '_image_width'
             1520  LOAD_CONST               2
             1522  BINARY_TRUE_DIVIDE
             1524  CALL_FUNCTION_1       1  '1 positional argument'
             1526  STORE_FAST               '_wdinl'

 L. 599      1528  LOAD_GLOBAL              int
             1530  LOAD_FAST                '_image_height'
             1532  LOAD_CONST               2
             1534  BINARY_TRUE_DIVIDE
             1536  CALL_FUNCTION_1       1  '1 positional argument'
             1538  STORE_FAST               '_wdz'

 L. 600      1540  LOAD_GLOBAL              int
             1542  LOAD_FAST                '_image_height'
             1544  LOAD_CONST               2
             1546  BINARY_TRUE_DIVIDE
             1548  CALL_FUNCTION_1       1  '1 positional argument'
             1550  STORE_FAST               '_wdztarget'
           1552_0  COME_FROM          1512  '1512'

 L. 601      1552  LOAD_DEREF               'self'
             1554  LOAD_ATTR                cbbornt
             1556  LOAD_METHOD              currentIndex
             1558  CALL_METHOD_0         0  '0 positional arguments'
             1560  LOAD_CONST               2
             1562  COMPARE_OP               ==
         1564_1566  POP_JUMP_IF_FALSE  1604  'to 1604'

 L. 602      1568  LOAD_GLOBAL              int
             1570  LOAD_FAST                '_image_width'
             1572  LOAD_CONST               2
             1574  BINARY_TRUE_DIVIDE
             1576  CALL_FUNCTION_1       1  '1 positional argument'
             1578  STORE_FAST               '_wdinl'

 L. 603      1580  LOAD_GLOBAL              int
             1582  LOAD_FAST                '_image_height'
             1584  LOAD_CONST               2
             1586  BINARY_TRUE_DIVIDE
             1588  CALL_FUNCTION_1       1  '1 positional argument'
             1590  STORE_FAST               '_wdxl'

 L. 604      1592  LOAD_GLOBAL              int
             1594  LOAD_FAST                '_image_height'
             1596  LOAD_CONST               2
             1598  BINARY_TRUE_DIVIDE
             1600  CALL_FUNCTION_1       1  '1 positional argument'
             1602  STORE_FAST               '_wdxltarget'
           1604_0  COME_FROM          1564  '1564'

 L. 606      1604  LOAD_DEREF               'self'
             1606  LOAD_ATTR                survinfo
             1608  STORE_FAST               '_seisinfo'

 L. 608      1610  LOAD_GLOBAL              print
             1612  LOAD_STR                 'TrainMl15DDcnnFromScratch: Step 1 - Get training samples:'
             1614  CALL_FUNCTION_1       1  '1 positional argument'
             1616  POP_TOP          

 L. 609      1618  LOAD_DEREF               'self'
             1620  LOAD_ATTR                traindataconfig
             1622  LOAD_STR                 'TrainPointSet'
             1624  BINARY_SUBSCR    
             1626  STORE_FAST               '_trainpoint'

 L. 610      1628  LOAD_GLOBAL              np
             1630  LOAD_METHOD              zeros
             1632  LOAD_CONST               0
             1634  LOAD_CONST               3
             1636  BUILD_LIST_2          2 
             1638  CALL_METHOD_1         1  '1 positional argument'
             1640  STORE_FAST               '_traindata'

 L. 611      1642  SETUP_LOOP         1718  'to 1718'
             1644  LOAD_FAST                '_trainpoint'
             1646  GET_ITER         
           1648_0  COME_FROM          1666  '1666'
             1648  FOR_ITER           1716  'to 1716'
             1650  STORE_FAST               '_p'

 L. 612      1652  LOAD_GLOBAL              point_ays
             1654  LOAD_METHOD              checkPoint
             1656  LOAD_DEREF               'self'
             1658  LOAD_ATTR                pointsetdata
             1660  LOAD_FAST                '_p'
             1662  BINARY_SUBSCR    
             1664  CALL_METHOD_1         1  '1 positional argument'
         1666_1668  POP_JUMP_IF_FALSE  1648  'to 1648'

 L. 613      1670  LOAD_GLOBAL              basic_mdt
             1672  LOAD_METHOD              exportMatDict
             1674  LOAD_DEREF               'self'
             1676  LOAD_ATTR                pointsetdata
             1678  LOAD_FAST                '_p'
             1680  BINARY_SUBSCR    
             1682  LOAD_STR                 'Inline'
             1684  LOAD_STR                 'Crossline'
             1686  LOAD_STR                 'Z'
             1688  BUILD_LIST_3          3 
             1690  CALL_METHOD_2         2  '2 positional arguments'
             1692  STORE_FAST               '_pt'

 L. 614      1694  LOAD_GLOBAL              np
             1696  LOAD_ATTR                concatenate
             1698  LOAD_FAST                '_traindata'
             1700  LOAD_FAST                '_pt'
             1702  BUILD_TUPLE_2         2 
             1704  LOAD_CONST               0
             1706  LOAD_CONST               ('axis',)
             1708  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1710  STORE_FAST               '_traindata'
         1712_1714  JUMP_BACK          1648  'to 1648'
             1716  POP_BLOCK        
           1718_0  COME_FROM_LOOP     1642  '1642'

 L. 615      1718  LOAD_GLOBAL              seis_ays
             1720  LOAD_ATTR                removeOutofSurveySample
             1722  LOAD_FAST                '_traindata'

 L. 616      1724  LOAD_FAST                '_seisinfo'
             1726  LOAD_STR                 'ILStart'
             1728  BINARY_SUBSCR    
             1730  LOAD_FAST                '_wdinl'
             1732  LOAD_FAST                '_seisinfo'
             1734  LOAD_STR                 'ILStep'
             1736  BINARY_SUBSCR    
             1738  BINARY_MULTIPLY  
             1740  BINARY_ADD       

 L. 617      1742  LOAD_FAST                '_seisinfo'
             1744  LOAD_STR                 'ILEnd'
             1746  BINARY_SUBSCR    
             1748  LOAD_FAST                '_wdinl'
             1750  LOAD_FAST                '_seisinfo'
             1752  LOAD_STR                 'ILStep'
             1754  BINARY_SUBSCR    
             1756  BINARY_MULTIPLY  
             1758  BINARY_SUBTRACT  

 L. 618      1760  LOAD_FAST                '_seisinfo'
             1762  LOAD_STR                 'XLStart'
             1764  BINARY_SUBSCR    
             1766  LOAD_FAST                '_wdxl'
             1768  LOAD_FAST                '_seisinfo'
             1770  LOAD_STR                 'XLStep'
             1772  BINARY_SUBSCR    
             1774  BINARY_MULTIPLY  
             1776  BINARY_ADD       

 L. 619      1778  LOAD_FAST                '_seisinfo'
             1780  LOAD_STR                 'XLEnd'
             1782  BINARY_SUBSCR    
             1784  LOAD_FAST                '_wdxl'
             1786  LOAD_FAST                '_seisinfo'
             1788  LOAD_STR                 'XLStep'
             1790  BINARY_SUBSCR    
             1792  BINARY_MULTIPLY  
             1794  BINARY_SUBTRACT  

 L. 620      1796  LOAD_FAST                '_seisinfo'
             1798  LOAD_STR                 'ZStart'
             1800  BINARY_SUBSCR    
             1802  LOAD_FAST                '_wdz'
             1804  LOAD_FAST                '_seisinfo'
             1806  LOAD_STR                 'ZStep'
             1808  BINARY_SUBSCR    
             1810  BINARY_MULTIPLY  
             1812  BINARY_ADD       

 L. 621      1814  LOAD_FAST                '_seisinfo'
             1816  LOAD_STR                 'ZEnd'
             1818  BINARY_SUBSCR    
             1820  LOAD_FAST                '_wdz'
             1822  LOAD_FAST                '_seisinfo'
             1824  LOAD_STR                 'ZStep'
             1826  BINARY_SUBSCR    
             1828  BINARY_MULTIPLY  
             1830  BINARY_SUBTRACT  
             1832  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1834  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1836  STORE_FAST               '_traindata'

 L. 624      1838  LOAD_GLOBAL              np
             1840  LOAD_METHOD              shape
             1842  LOAD_FAST                '_traindata'
             1844  CALL_METHOD_1         1  '1 positional argument'
             1846  LOAD_CONST               0
             1848  BINARY_SUBSCR    
             1850  LOAD_CONST               0
             1852  COMPARE_OP               <=
         1854_1856  POP_JUMP_IF_FALSE  1894  'to 1894'

 L. 625      1858  LOAD_GLOBAL              vis_msg
             1860  LOAD_ATTR                print
             1862  LOAD_STR                 'ERROR in TrainMl2DDCnnFromScratch: No training sample found'
             1864  LOAD_STR                 'error'
             1866  LOAD_CONST               ('type',)
             1868  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1870  POP_TOP          

 L. 626      1872  LOAD_GLOBAL              QtWidgets
             1874  LOAD_ATTR                QMessageBox
             1876  LOAD_METHOD              critical
             1878  LOAD_DEREF               'self'
             1880  LOAD_ATTR                msgbox

 L. 627      1882  LOAD_STR                 'Train 1.5D-DCNN'

 L. 628      1884  LOAD_STR                 'No training sample found'
             1886  CALL_METHOD_3         3  '3 positional arguments'
             1888  POP_TOP          

 L. 629      1890  LOAD_CONST               None
             1892  RETURN_VALUE     
           1894_0  COME_FROM          1854  '1854'

 L. 632      1894  LOAD_GLOBAL              print
             1896  LOAD_STR                 'TrainMl15DDcnnFromScratch: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 633      1898  LOAD_FAST                '_image_height'
             1900  LOAD_FAST                '_image_width'
             1902  LOAD_FAST                '_image_height_new'
             1904  LOAD_FAST                '_image_width_new'
             1906  BUILD_TUPLE_4         4 
             1908  BINARY_MODULO    
             1910  CALL_FUNCTION_1       1  '1 positional argument'
             1912  POP_TOP          

 L. 634      1914  BUILD_MAP_0           0 
             1916  STORE_FAST               '_traindict'

 L. 635      1918  SETUP_LOOP         1990  'to 1990'
             1920  LOAD_FAST                '_features'
             1922  GET_ITER         
             1924  FOR_ITER           1988  'to 1988'
             1926  STORE_FAST               'f'

 L. 636      1928  LOAD_DEREF               'self'
             1930  LOAD_ATTR                seisdata
             1932  LOAD_FAST                'f'
             1934  BINARY_SUBSCR    
             1936  STORE_FAST               '_seisdata'

 L. 637      1938  LOAD_GLOBAL              seis_ays
             1940  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1942  LOAD_FAST                '_seisdata'
             1944  LOAD_FAST                '_traindata'
             1946  LOAD_DEREF               'self'
             1948  LOAD_ATTR                survinfo

 L. 638      1950  LOAD_FAST                '_wdinl'
             1952  LOAD_FAST                '_wdxl'
             1954  LOAD_FAST                '_wdz'

 L. 639      1956  LOAD_CONST               False
             1958  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1960  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1962  LOAD_CONST               None
             1964  LOAD_CONST               None
             1966  BUILD_SLICE_2         2 
             1968  LOAD_CONST               3
             1970  LOAD_CONST               None
             1972  BUILD_SLICE_2         2 
             1974  BUILD_TUPLE_2         2 
             1976  BINARY_SUBSCR    
             1978  LOAD_FAST                '_traindict'
             1980  LOAD_FAST                'f'
             1982  STORE_SUBSCR     
         1984_1986  JUMP_BACK          1924  'to 1924'
             1988  POP_BLOCK        
           1990_0  COME_FROM_LOOP     1918  '1918'

 L. 640      1990  LOAD_FAST                '_target'
             1992  LOAD_FAST                '_features'
             1994  COMPARE_OP               not-in
         1996_1998  POP_JUMP_IF_FALSE  2056  'to 2056'

 L. 641      2000  LOAD_DEREF               'self'
             2002  LOAD_ATTR                seisdata
             2004  LOAD_FAST                '_target'
             2006  BINARY_SUBSCR    
             2008  STORE_FAST               '_seisdata'

 L. 642      2010  LOAD_GLOBAL              seis_ays
             2012  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2014  LOAD_FAST                '_seisdata'
             2016  LOAD_FAST                '_traindata'
             2018  LOAD_DEREF               'self'
             2020  LOAD_ATTR                survinfo

 L. 643      2022  LOAD_FAST                '_wdinltarget'

 L. 644      2024  LOAD_FAST                '_wdxltarget'

 L. 645      2026  LOAD_FAST                '_wdztarget'

 L. 646      2028  LOAD_CONST               False
             2030  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2032  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2034  LOAD_CONST               None
             2036  LOAD_CONST               None
             2038  BUILD_SLICE_2         2 
             2040  LOAD_CONST               3
             2042  LOAD_CONST               None
             2044  BUILD_SLICE_2         2 
             2046  BUILD_TUPLE_2         2 
             2048  BINARY_SUBSCR    
             2050  LOAD_FAST                '_traindict'
             2052  LOAD_FAST                '_target'
             2054  STORE_SUBSCR     
           2056_0  COME_FROM          1996  '1996'

 L. 648      2056  LOAD_DEREF               'self'
             2058  LOAD_ATTR                traindataconfig
             2060  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2062  BINARY_SUBSCR    
         2064_2066  POP_JUMP_IF_FALSE  2148  'to 2148'

 L. 649      2068  SETUP_LOOP         2148  'to 2148'
             2070  LOAD_FAST                '_features'
             2072  GET_ITER         
           2074_0  COME_FROM          2102  '2102'
             2074  FOR_ITER           2146  'to 2146'
             2076  STORE_FAST               'f'

 L. 650      2078  LOAD_GLOBAL              ml_aug
             2080  LOAD_METHOD              removeInvariantFeature
             2082  LOAD_FAST                '_traindict'
             2084  LOAD_FAST                'f'
             2086  CALL_METHOD_2         2  '2 positional arguments'
             2088  STORE_FAST               '_traindict'

 L. 651      2090  LOAD_GLOBAL              basic_mdt
             2092  LOAD_METHOD              maxDictConstantRow
             2094  LOAD_FAST                '_traindict'
             2096  CALL_METHOD_1         1  '1 positional argument'
             2098  LOAD_CONST               0
             2100  COMPARE_OP               <=
         2102_2104  POP_JUMP_IF_FALSE  2074  'to 2074'

 L. 652      2106  LOAD_GLOBAL              vis_msg
             2108  LOAD_ATTR                print
             2110  LOAD_STR                 'ERROR in TrainMl15DDcnnFromScratch: No training sample found'
             2112  LOAD_STR                 'error'
             2114  LOAD_CONST               ('type',)
             2116  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2118  POP_TOP          

 L. 653      2120  LOAD_GLOBAL              QtWidgets
             2122  LOAD_ATTR                QMessageBox
             2124  LOAD_METHOD              critical
             2126  LOAD_DEREF               'self'
             2128  LOAD_ATTR                msgbox

 L. 654      2130  LOAD_STR                 'Train 1.5D-DCNN'

 L. 655      2132  LOAD_STR                 'No training sample found'
             2134  CALL_METHOD_3         3  '3 positional arguments'
             2136  POP_TOP          

 L. 656      2138  LOAD_CONST               None
             2140  RETURN_VALUE     
         2142_2144  JUMP_BACK          2074  'to 2074'
             2146  POP_BLOCK        
           2148_0  COME_FROM_LOOP     2068  '2068'
           2148_1  COME_FROM          2064  '2064'

 L. 658      2148  LOAD_FAST                '_image_height_new'
             2150  LOAD_FAST                '_image_height'
             2152  COMPARE_OP               !=
         2154_2156  POP_JUMP_IF_TRUE   2168  'to 2168'
             2158  LOAD_FAST                '_image_width_new'
             2160  LOAD_FAST                '_image_width'
             2162  COMPARE_OP               !=
         2164_2166  POP_JUMP_IF_FALSE  2212  'to 2212'
           2168_0  COME_FROM          2154  '2154'

 L. 659      2168  SETUP_LOOP         2212  'to 2212'
             2170  LOAD_FAST                '_features'
             2172  GET_ITER         
             2174  FOR_ITER           2210  'to 2210'
             2176  STORE_FAST               'f'

 L. 660      2178  LOAD_GLOBAL              basic_image
             2180  LOAD_ATTR                changeImageSize
             2182  LOAD_FAST                '_traindict'
             2184  LOAD_FAST                'f'
             2186  BINARY_SUBSCR    

 L. 661      2188  LOAD_FAST                '_image_height'

 L. 662      2190  LOAD_FAST                '_image_width'

 L. 663      2192  LOAD_FAST                '_image_height_new'

 L. 664      2194  LOAD_FAST                '_image_width_new'
             2196  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2198  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2200  LOAD_FAST                '_traindict'
             2202  LOAD_FAST                'f'
             2204  STORE_SUBSCR     
         2206_2208  JUMP_BACK          2174  'to 2174'
             2210  POP_BLOCK        
           2212_0  COME_FROM_LOOP     2168  '2168'
           2212_1  COME_FROM          2164  '2164'

 L. 665      2212  LOAD_FAST                '_image_height_new'
             2214  LOAD_FAST                '_image_height'
             2216  COMPARE_OP               !=
         2218_2220  POP_JUMP_IF_FALSE  2258  'to 2258'
             2222  LOAD_FAST                '_target'
             2224  LOAD_FAST                '_features'
             2226  COMPARE_OP               not-in
         2228_2230  POP_JUMP_IF_FALSE  2258  'to 2258'

 L. 666      2232  LOAD_GLOBAL              basic_curve
             2234  LOAD_ATTR                changeCurveSize
             2236  LOAD_FAST                '_traindict'
             2238  LOAD_FAST                '_target'
             2240  BINARY_SUBSCR    

 L. 667      2242  LOAD_FAST                '_image_height'

 L. 668      2244  LOAD_FAST                '_image_height_new'
             2246  LOAD_STR                 'linear'
             2248  LOAD_CONST               ('length', 'length_new', 'kind')
             2250  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2252  LOAD_FAST                '_traindict'
             2254  LOAD_FAST                '_target'
             2256  STORE_SUBSCR     
           2258_0  COME_FROM          2228  '2228'
           2258_1  COME_FROM          2218  '2218'

 L. 669      2258  LOAD_DEREF               'self'
             2260  LOAD_ATTR                traindataconfig
             2262  LOAD_STR                 'RotateFeature_Checked'
             2264  BINARY_SUBSCR    
             2266  LOAD_CONST               True
             2268  COMPARE_OP               is
         2270_2272  POP_JUMP_IF_FALSE  2344  'to 2344'

 L. 670      2274  SETUP_LOOP         2312  'to 2312'
             2276  LOAD_FAST                '_features'
             2278  GET_ITER         
             2280  FOR_ITER           2310  'to 2310'
             2282  STORE_FAST               'f'

 L. 671      2284  LOAD_GLOBAL              ml_aug
             2286  LOAD_METHOD              rotateImage4Way
             2288  LOAD_FAST                '_traindict'
             2290  LOAD_FAST                'f'
             2292  BINARY_SUBSCR    
             2294  LOAD_FAST                '_image_height_new'
             2296  LOAD_FAST                '_image_width_new'
             2298  CALL_METHOD_3         3  '3 positional arguments'
             2300  LOAD_FAST                '_traindict'
             2302  LOAD_FAST                'f'
             2304  STORE_SUBSCR     
         2306_2308  JUMP_BACK          2280  'to 2280'
             2310  POP_BLOCK        
           2312_0  COME_FROM_LOOP     2274  '2274'

 L. 672      2312  LOAD_FAST                '_target'
             2314  LOAD_FAST                '_features'
             2316  COMPARE_OP               not-in
         2318_2320  POP_JUMP_IF_FALSE  2344  'to 2344'

 L. 673      2322  LOAD_GLOBAL              ml_aug
             2324  LOAD_METHOD              rotateImage4Way
             2326  LOAD_FAST                '_traindict'
             2328  LOAD_FAST                '_target'
             2330  BINARY_SUBSCR    
             2332  LOAD_FAST                '_image_height_new'
             2334  LOAD_CONST               1
             2336  CALL_METHOD_3         3  '3 positional arguments'
             2338  LOAD_FAST                '_traindict'
             2340  LOAD_FAST                '_target'
             2342  STORE_SUBSCR     
           2344_0  COME_FROM          2318  '2318'
           2344_1  COME_FROM          2270  '2270'

 L. 675      2344  LOAD_GLOBAL              np
             2346  LOAD_METHOD              round
             2348  LOAD_FAST                '_traindict'
             2350  LOAD_FAST                '_target'
             2352  BINARY_SUBSCR    
             2354  CALL_METHOD_1         1  '1 positional argument'
             2356  LOAD_METHOD              astype
             2358  LOAD_GLOBAL              int
             2360  CALL_METHOD_1         1  '1 positional argument'
             2362  LOAD_FAST                '_traindict'
             2364  LOAD_FAST                '_target'
             2366  STORE_SUBSCR     

 L. 678      2368  LOAD_GLOBAL              print
             2370  LOAD_STR                 'TrainMl15DDcnnFromScratch: A total of %d valid training samples'
             2372  LOAD_GLOBAL              basic_mdt
             2374  LOAD_METHOD              maxDictConstantRow

 L. 679      2376  LOAD_FAST                '_traindict'
             2378  CALL_METHOD_1         1  '1 positional argument'
             2380  BINARY_MODULO    
             2382  CALL_FUNCTION_1       1  '1 positional argument'
             2384  POP_TOP          

 L. 681      2386  LOAD_GLOBAL              print
             2388  LOAD_STR                 'TrainMl15DDcnnFromScratch: Step 3 - Start training'
             2390  CALL_FUNCTION_1       1  '1 positional argument'
             2392  POP_TOP          

 L. 683      2394  LOAD_GLOBAL              QtWidgets
             2396  LOAD_METHOD              QProgressDialog
             2398  CALL_METHOD_0         0  '0 positional arguments'
             2400  STORE_FAST               '_pgsdlg'

 L. 684      2402  LOAD_GLOBAL              QtGui
             2404  LOAD_METHOD              QIcon
             2406  CALL_METHOD_0         0  '0 positional arguments'
             2408  STORE_FAST               'icon'

 L. 685      2410  LOAD_FAST                'icon'
             2412  LOAD_METHOD              addPixmap
             2414  LOAD_GLOBAL              QtGui
             2416  LOAD_METHOD              QPixmap
             2418  LOAD_GLOBAL              os
             2420  LOAD_ATTR                path
             2422  LOAD_METHOD              join
             2424  LOAD_DEREF               'self'
             2426  LOAD_ATTR                iconpath
             2428  LOAD_STR                 'icons/new.png'
             2430  CALL_METHOD_2         2  '2 positional arguments'
             2432  CALL_METHOD_1         1  '1 positional argument'

 L. 686      2434  LOAD_GLOBAL              QtGui
             2436  LOAD_ATTR                QIcon
             2438  LOAD_ATTR                Normal
             2440  LOAD_GLOBAL              QtGui
             2442  LOAD_ATTR                QIcon
             2444  LOAD_ATTR                Off
             2446  CALL_METHOD_3         3  '3 positional arguments'
             2448  POP_TOP          

 L. 687      2450  LOAD_FAST                '_pgsdlg'
             2452  LOAD_METHOD              setWindowIcon
             2454  LOAD_FAST                'icon'
             2456  CALL_METHOD_1         1  '1 positional argument'
             2458  POP_TOP          

 L. 688      2460  LOAD_FAST                '_pgsdlg'
             2462  LOAD_METHOD              setWindowTitle
             2464  LOAD_STR                 'Train 1.5D-DCNN'
             2466  CALL_METHOD_1         1  '1 positional argument'
             2468  POP_TOP          

 L. 689      2470  LOAD_FAST                '_pgsdlg'
             2472  LOAD_METHOD              setCancelButton
             2474  LOAD_CONST               None
             2476  CALL_METHOD_1         1  '1 positional argument'
             2478  POP_TOP          

 L. 690      2480  LOAD_FAST                '_pgsdlg'
             2482  LOAD_METHOD              setWindowFlags
             2484  LOAD_GLOBAL              QtCore
             2486  LOAD_ATTR                Qt
             2488  LOAD_ATTR                WindowStaysOnTopHint
             2490  CALL_METHOD_1         1  '1 positional argument'
             2492  POP_TOP          

 L. 691      2494  LOAD_FAST                '_pgsdlg'
             2496  LOAD_METHOD              forceShow
             2498  CALL_METHOD_0         0  '0 positional arguments'
             2500  POP_TOP          

 L. 692      2502  LOAD_FAST                '_pgsdlg'
             2504  LOAD_METHOD              setFixedWidth
             2506  LOAD_CONST               400
             2508  CALL_METHOD_1         1  '1 positional argument'
             2510  POP_TOP          

 L. 693      2512  LOAD_GLOBAL              ml_dcnn15d
             2514  LOAD_ATTR                create15DDCNNSegmentor
             2516  LOAD_FAST                '_traindict'

 L. 694      2518  LOAD_FAST                '_image_height_new'
             2520  LOAD_FAST                '_image_width_new'

 L. 695      2522  LOAD_FAST                '_features'
             2524  LOAD_FAST                '_target'

 L. 696      2526  LOAD_FAST                '_nepoch'
             2528  LOAD_FAST                '_batchsize'

 L. 697      2530  LOAD_FAST                '_nconvblock'
             2532  LOAD_FAST                '_nconvfeature'

 L. 698      2534  LOAD_FAST                '_nconvlayer'

 L. 699      2536  LOAD_FAST                '_n1x1layer'
             2538  LOAD_FAST                '_n1x1feature'

 L. 700      2540  LOAD_FAST                '_patch_height'
             2542  LOAD_FAST                '_patch_width'

 L. 701      2544  LOAD_FAST                '_pool_height'
             2546  LOAD_FAST                '_pool_width'

 L. 702      2548  LOAD_FAST                '_learning_rate'

 L. 703      2550  LOAD_FAST                '_dropout_prob'

 L. 704      2552  LOAD_CONST               True

 L. 705      2554  LOAD_FAST                '_savepath'
             2556  LOAD_FAST                '_savename'

 L. 706      2558  LOAD_FAST                '_pgsdlg'
             2560  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'nepoch', 'batchsize', 'nconvblock', 'nconvfeature', 'nconvlayer', 'n1x1layer', 'n1x1feature', 'patchheight', 'patchwidth', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprob', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2562  CALL_FUNCTION_KW_22    22  '22 total positional and keyword args'
             2564  STORE_FAST               '_dcnnlog'

 L. 709      2566  LOAD_GLOBAL              QtWidgets
             2568  LOAD_ATTR                QMessageBox
             2570  LOAD_METHOD              information
             2572  LOAD_DEREF               'self'
             2574  LOAD_ATTR                msgbox

 L. 710      2576  LOAD_STR                 'Train 1.5D DCNN'

 L. 711      2578  LOAD_STR                 'DCNN trained successfully'
             2580  CALL_METHOD_3         3  '3 positional arguments'
             2582  POP_TOP          

 L. 713      2584  LOAD_GLOBAL              QtWidgets
             2586  LOAD_ATTR                QMessageBox
             2588  LOAD_METHOD              question
             2590  LOAD_DEREF               'self'
             2592  LOAD_ATTR                msgbox
             2594  LOAD_STR                 'Train 1.5D DCNN'
             2596  LOAD_STR                 'View learning matrix?'

 L. 714      2598  LOAD_GLOBAL              QtWidgets
             2600  LOAD_ATTR                QMessageBox
             2602  LOAD_ATTR                Yes
             2604  LOAD_GLOBAL              QtWidgets
             2606  LOAD_ATTR                QMessageBox
             2608  LOAD_ATTR                No
             2610  BINARY_OR        

 L. 715      2612  LOAD_GLOBAL              QtWidgets
             2614  LOAD_ATTR                QMessageBox
             2616  LOAD_ATTR                Yes
             2618  CALL_METHOD_5         5  '5 positional arguments'
             2620  STORE_FAST               'reply'

 L. 717      2622  LOAD_FAST                'reply'
             2624  LOAD_GLOBAL              QtWidgets
             2626  LOAD_ATTR                QMessageBox
             2628  LOAD_ATTR                Yes
             2630  COMPARE_OP               ==
         2632_2634  POP_JUMP_IF_FALSE  2702  'to 2702'

 L. 718      2636  LOAD_GLOBAL              QtWidgets
             2638  LOAD_METHOD              QDialog
             2640  CALL_METHOD_0         0  '0 positional arguments'
             2642  STORE_FAST               '_viewmllearnmat'

 L. 719      2644  LOAD_GLOBAL              gui_viewmllearnmat
             2646  CALL_FUNCTION_0       0  '0 positional arguments'
             2648  STORE_FAST               '_gui'

 L. 720      2650  LOAD_DEREF               'self'
             2652  LOAD_ATTR                linestyle
             2654  LOAD_FAST                '_gui'
             2656  STORE_ATTR               linestyle

 L. 721      2658  LOAD_DEREF               'self'
             2660  LOAD_ATTR                fontstyle
             2662  LOAD_FAST                '_gui'
             2664  STORE_ATTR               fontstyle

 L. 722      2666  LOAD_FAST                '_dcnnlog'
             2668  LOAD_STR                 'learning_curve'
             2670  BINARY_SUBSCR    
             2672  LOAD_FAST                '_gui'
             2674  STORE_ATTR               learnmat

 L. 723      2676  LOAD_FAST                '_gui'
             2678  LOAD_METHOD              setupGUI
             2680  LOAD_FAST                '_viewmllearnmat'
             2682  CALL_METHOD_1         1  '1 positional argument'
             2684  POP_TOP          

 L. 724      2686  LOAD_FAST                '_viewmllearnmat'
             2688  LOAD_METHOD              exec
             2690  CALL_METHOD_0         0  '0 positional arguments'
             2692  POP_TOP          

 L. 725      2694  LOAD_FAST                '_viewmllearnmat'
             2696  LOAD_METHOD              show
             2698  CALL_METHOD_0         0  '0 positional arguments'
             2700  POP_TOP          
           2702_0  COME_FROM          2632  '2632'

Parse error at or near `POP_TOP' instruction at offset 2700

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
    TrainMl15DDcnnFromScratch = QtWidgets.QWidget()
    gui = trainml15ddcnnfromscratch()
    gui.setupGUI(TrainMl15DDcnnFromScratch)
    TrainMl15DDcnnFromScratch.show()
    sys.exit(app.exec_())