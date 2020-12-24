# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml15dwdcnnfromscratch.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 47147 bytes
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
import cognitivegeo.src.ml.wdcnnsegmentor15d as ml_wdcnn15d
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml15dwdcnnfromscratch(object):
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
    traindataconfig['RemoveZeroWeight_Enabled'] = True
    traindataconfig['RemoveZeroWeight_Checked'] = False

    def setupGUI(self, TrainMl15DWdcnnFromScratch):
        TrainMl15DWdcnnFromScratch.setObjectName('TrainMl15DWdcnnFromScratch')
        TrainMl15DWdcnnFromScratch.setFixedSize(810, 540)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl15DWdcnnFromScratch.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl15DWdcnnFromScratch)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl15DWdcnnFromScratch)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl15DWdcnnFromScratch)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblweight = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblweight.setObjectName('lblweight')
        self.lblweight.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.cbbweight = QtWidgets.QComboBox(TrainMl15DWdcnnFromScratch)
        self.cbbweight.setObjectName('cbbweight')
        self.cbbweight.setGeometry(QtCore.QRect(110, 310, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 50, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 50, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl15DWdcnnFromScratch)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 90, 180, 200))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 50, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 50, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(TrainMl15DWdcnnFromScratch)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 90, 180, 200))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 300, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 300, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 300, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 340, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 340, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 300, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 300, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 300, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 340, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 340, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl15DWdcnnFromScratch)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 360, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 360, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 400, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 400, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 400, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 400, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 440, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 440, 40, 30))
        self.lbldropout = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 440, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 440, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl15DWdcnnFromScratch)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 490, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl15DWdcnnFromScratch)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 490, 180, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl15DWdcnnFromScratch)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 490, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl15DWdcnnFromScratch)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 490, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl15DWdcnnFromScratch)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl15DWdcnnFromScratch.geometry().center().x()
        _center_y = TrainMl15DWdcnnFromScratch.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl15DWdcnnFromScratch)
        QtCore.QMetaObject.connectSlotsByName(TrainMl15DWdcnnFromScratch)

    def retranslateGUI(self, TrainMl15DWdcnnFromScratch):
        self.dialog = TrainMl15DWdcnnFromScratch
        _translate = QtCore.QCoreApplication.translate
        TrainMl15DWdcnnFromScratch.setWindowTitle(_translate('TrainMl15DWdcnnFromScratch', 'Train 1.5D-WDCNN from scratch'))
        self.lblfeature.setText(_translate('TrainMl15DWdcnnFromScratch', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl15DWdcnnFromScratch', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl15DWdcnnFromScratch', 'Select target:'))
        self.lblweight.setText(_translate('TrainMl15DWdcnnFromScratch', 'Select weight:'))
        self.btnconfigtraindata.setText(_translate('TrainMl15DWdcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('TrainMl15DWdcnnFromScratch', 'Original\nimage\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl15DWdcnnFromScratch', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl15DWdcnnFromScratch', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl15DWdcnnFromScratch', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl15DWdcnnFromScratch', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl15DWdcnnFromScratch', 'Interpolated\nimage\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl15DWdcnnFromScratch', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl15DWdcnnFromScratch', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl15DWdcnnFromScratch', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl15DWdcnnFromScratch', '32'))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        if self.checkSurvInfo():
            self.featurelist.clear()
            self.lwgfeature.clear()
            self.cbbtarget.clear()
            self.cbbweight.clear()
            _firstfeature = None
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    self.featurelist.append(i)
                    item = QtWidgets.QListWidgetItem(self.lwgfeature)
                    item.setText(_translate('TrainMl15DWdcnnFromScratch', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
            self.cbbweight.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl15DWdcnnFromScratch', 'Specify WDCNN architecture:'))
        self.lblnconvblock.setText(_translate('TrainMl15DWdcnnFromScratch', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl15DWdcnnFromScratch', '3'))
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

        self.lbln1x1layer.setText(_translate('TrainMl15DWdcnnFromScratch', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('TrainMl15DWdcnnFromScratch', '2'))
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.twgn1x1layer.setRowCount(2)
        for _idx in range(int(self.ldtn1x1layer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl15DWdcnnFromScratch', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgn1x1layer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgn1x1layer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl15DWdcnnFromScratch', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl15DWdcnnFromScratch', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl15DWdcnnFromScratch', '3'))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('TrainMl15DWdcnnFromScratch', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl15DWdcnnFromScratch', '3'))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('TrainMl15DWdcnnFromScratch', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl15DWdcnnFromScratch', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl15DWdcnnFromScratch', '2'))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl15DWdcnnFromScratch', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl15DWdcnnFromScratch', '2'))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('TrainMl15DWdcnnFromScratch', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl15DWdcnnFromScratch', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl15DWdcnnFromScratch', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl15DWdcnnFromScratch', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl15DWdcnnFromScratch', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl15DWdcnnFromScratch', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl15DWdcnnFromScratch', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('TrainMl15DWdcnnFromScratch', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('TrainMl15DWdcnnFromScratch', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl15DWdcnnFromScratch', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl15DWdcnnFromScratch', ''))
        self.btnsave.setText(_translate('TrainMl15DWdcnnFromScratch', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl15DWdcnnFromScratch', 'Train 1.5D-WDCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl15DWdcnnFromScratch)

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

    def clickBtnTrainMl15DWdcnnFromScratch--- This code section failed: ---

 L. 456         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 458         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 459        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 460        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 461        50  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 462        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 463        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 465        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_image_height'

 L. 466        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_image_width'

 L. 467        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtnewheight
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_image_height_new'

 L. 468       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewwidth
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_image_width_new'

 L. 469       126  LOAD_FAST                '_image_height'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'
              134  LOAD_FAST                '_image_width'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_TRUE    158  'to 158'

 L. 470       142  LOAD_FAST                '_image_height_new'
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

 L. 471       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 472       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 473       182  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 474       184  LOAD_STR                 'Non-integer feature size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 475       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 476       194  LOAD_FAST                '_image_height'
              196  LOAD_CONST               2
              198  COMPARE_OP               <
              200  POP_JUMP_IF_TRUE    228  'to 228'
              202  LOAD_FAST                '_image_width'
              204  LOAD_CONST               2
              206  COMPARE_OP               <
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 477       210  LOAD_FAST                '_image_height_new'
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

 L. 478       228  LOAD_GLOBAL              vis_msg
              230  LOAD_ATTR                print
              232  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 479       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 480       252  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 481       254  LOAD_STR                 'Features are not 2D'
              256  CALL_METHOD_3         3  '3 positional arguments'
              258  POP_TOP          

 L. 482       260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           224  '224'

 L. 484       264  LOAD_CONST               2
              266  LOAD_GLOBAL              int
              268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               2
              272  BINARY_TRUE_DIVIDE
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  BINARY_MULTIPLY  
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  STORE_FAST               '_image_height'

 L. 485       284  LOAD_CONST               2
              286  LOAD_GLOBAL              int
              288  LOAD_FAST                '_image_width'
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BINARY_MULTIPLY  
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               '_image_width'

 L. 487       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                lwgfeature
              308  LOAD_METHOD              selectedItems
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               '_features'

 L. 488       314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainml15dwdcnnfromscratch.clickBtnTrainMl15DWdcnnFromScratch.<locals>.<listcomp>'
              318  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              320  LOAD_FAST                '_features'
              322  GET_ITER         
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               '_features'

 L. 489       328  LOAD_DEREF               'self'
              330  LOAD_ATTR                featurelist
              332  LOAD_DEREF               'self'
              334  LOAD_ATTR                cbbtarget
              336  LOAD_METHOD              currentIndex
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  BINARY_SUBSCR    
              342  STORE_FAST               '_target'

 L. 490       344  LOAD_DEREF               'self'
              346  LOAD_ATTR                featurelist
              348  LOAD_DEREF               'self'
              350  LOAD_ATTR                cbbweight
              352  LOAD_METHOD              currentIndex
              354  CALL_METHOD_0         0  '0 positional arguments'
              356  BINARY_SUBSCR    
              358  STORE_FAST               '_weight'

 L. 492       360  LOAD_FAST                '_target'
              362  LOAD_FAST                '_features'
              364  COMPARE_OP               in
          366_368  POP_JUMP_IF_FALSE   406  'to 406'

 L. 493       370  LOAD_GLOBAL              vis_msg
              372  LOAD_ATTR                print
              374  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Target also used as features'
              376  LOAD_STR                 'error'
              378  LOAD_CONST               ('type',)
              380  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              382  POP_TOP          

 L. 494       384  LOAD_GLOBAL              QtWidgets
              386  LOAD_ATTR                QMessageBox
              388  LOAD_METHOD              critical
              390  LOAD_DEREF               'self'
              392  LOAD_ATTR                msgbox

 L. 495       394  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 496       396  LOAD_STR                 'Target also used as features'
              398  CALL_METHOD_3         3  '3 positional arguments'
              400  POP_TOP          

 L. 497       402  LOAD_CONST               None
              404  RETURN_VALUE     
            406_0  COME_FROM           366  '366'

 L. 498       406  LOAD_FAST                '_weight'
              408  LOAD_FAST                '_features'
              410  COMPARE_OP               in
          412_414  POP_JUMP_IF_FALSE   452  'to 452'

 L. 499       416  LOAD_GLOBAL              vis_msg
              418  LOAD_ATTR                print
              420  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Weight also used as features'
              422  LOAD_STR                 'error'
              424  LOAD_CONST               ('type',)
              426  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              428  POP_TOP          

 L. 500       430  LOAD_GLOBAL              QtWidgets
              432  LOAD_ATTR                QMessageBox
              434  LOAD_METHOD              critical
              436  LOAD_DEREF               'self'
              438  LOAD_ATTR                msgbox

 L. 501       440  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 502       442  LOAD_STR                 'Weight also used as features'
              444  CALL_METHOD_3         3  '3 positional arguments'
              446  POP_TOP          

 L. 503       448  LOAD_CONST               None
              450  RETURN_VALUE     
            452_0  COME_FROM           412  '412'

 L. 505       452  LOAD_GLOBAL              basic_data
              454  LOAD_METHOD              str2int
              456  LOAD_DEREF               'self'
              458  LOAD_ATTR                ldtnconvblock
              460  LOAD_METHOD              text
              462  CALL_METHOD_0         0  '0 positional arguments'
              464  CALL_METHOD_1         1  '1 positional argument'
              466  STORE_FAST               '_nconvblock'

 L. 506       468  LOAD_CLOSURE             'self'
              470  BUILD_TUPLE_1         1 
              472  LOAD_LISTCOMP            '<code_object <listcomp>>'
              474  LOAD_STR                 'trainml15dwdcnnfromscratch.clickBtnTrainMl15DWdcnnFromScratch.<locals>.<listcomp>'
              476  MAKE_FUNCTION_8          'closure'
              478  LOAD_GLOBAL              range
              480  LOAD_FAST                '_nconvblock'
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  GET_ITER         
              486  CALL_FUNCTION_1       1  '1 positional argument'
              488  STORE_FAST               '_nconvlayer'

 L. 507       490  LOAD_CLOSURE             'self'
              492  BUILD_TUPLE_1         1 
              494  LOAD_LISTCOMP            '<code_object <listcomp>>'
              496  LOAD_STR                 'trainml15dwdcnnfromscratch.clickBtnTrainMl15DWdcnnFromScratch.<locals>.<listcomp>'
              498  MAKE_FUNCTION_8          'closure'
              500  LOAD_GLOBAL              range
              502  LOAD_FAST                '_nconvblock'
              504  CALL_FUNCTION_1       1  '1 positional argument'
              506  GET_ITER         
              508  CALL_FUNCTION_1       1  '1 positional argument'
              510  STORE_FAST               '_nconvfeature'

 L. 508       512  LOAD_GLOBAL              basic_data
              514  LOAD_METHOD              str2int
              516  LOAD_DEREF               'self'
              518  LOAD_ATTR                ldtn1x1layer
              520  LOAD_METHOD              text
              522  CALL_METHOD_0         0  '0 positional arguments'
              524  CALL_METHOD_1         1  '1 positional argument'
              526  STORE_FAST               '_n1x1layer'

 L. 509       528  LOAD_CLOSURE             'self'
              530  BUILD_TUPLE_1         1 
              532  LOAD_LISTCOMP            '<code_object <listcomp>>'
              534  LOAD_STR                 'trainml15dwdcnnfromscratch.clickBtnTrainMl15DWdcnnFromScratch.<locals>.<listcomp>'
              536  MAKE_FUNCTION_8          'closure'
              538  LOAD_GLOBAL              range
              540  LOAD_FAST                '_n1x1layer'
              542  CALL_FUNCTION_1       1  '1 positional argument'
              544  GET_ITER         
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  STORE_FAST               '_n1x1feature'

 L. 510       550  LOAD_GLOBAL              basic_data
              552  LOAD_METHOD              str2int
              554  LOAD_DEREF               'self'
              556  LOAD_ATTR                ldtmaskheight
              558  LOAD_METHOD              text
              560  CALL_METHOD_0         0  '0 positional arguments'
              562  CALL_METHOD_1         1  '1 positional argument'
              564  STORE_FAST               '_patch_height'

 L. 511       566  LOAD_GLOBAL              basic_data
              568  LOAD_METHOD              str2int
              570  LOAD_DEREF               'self'
              572  LOAD_ATTR                ldtmaskwidth
              574  LOAD_METHOD              text
              576  CALL_METHOD_0         0  '0 positional arguments'
              578  CALL_METHOD_1         1  '1 positional argument'
              580  STORE_FAST               '_patch_width'

 L. 512       582  LOAD_GLOBAL              basic_data
              584  LOAD_METHOD              str2int
              586  LOAD_DEREF               'self'
              588  LOAD_ATTR                ldtpoolheight
              590  LOAD_METHOD              text
              592  CALL_METHOD_0         0  '0 positional arguments'
              594  CALL_METHOD_1         1  '1 positional argument'
              596  STORE_FAST               '_pool_height'

 L. 513       598  LOAD_GLOBAL              basic_data
              600  LOAD_METHOD              str2int
              602  LOAD_DEREF               'self'
              604  LOAD_ATTR                ldtpoolwidth
              606  LOAD_METHOD              text
              608  CALL_METHOD_0         0  '0 positional arguments'
              610  CALL_METHOD_1         1  '1 positional argument'
              612  STORE_FAST               '_pool_width'

 L. 514       614  LOAD_GLOBAL              basic_data
              616  LOAD_METHOD              str2int
              618  LOAD_DEREF               'self'
              620  LOAD_ATTR                ldtnepoch
              622  LOAD_METHOD              text
              624  CALL_METHOD_0         0  '0 positional arguments'
              626  CALL_METHOD_1         1  '1 positional argument'
              628  STORE_FAST               '_nepoch'

 L. 515       630  LOAD_GLOBAL              basic_data
              632  LOAD_METHOD              str2int
              634  LOAD_DEREF               'self'
              636  LOAD_ATTR                ldtbatchsize
              638  LOAD_METHOD              text
              640  CALL_METHOD_0         0  '0 positional arguments'
              642  CALL_METHOD_1         1  '1 positional argument'
              644  STORE_FAST               '_batchsize'

 L. 516       646  LOAD_GLOBAL              basic_data
              648  LOAD_METHOD              str2float
              650  LOAD_DEREF               'self'
              652  LOAD_ATTR                ldtlearnrate
              654  LOAD_METHOD              text
              656  CALL_METHOD_0         0  '0 positional arguments'
              658  CALL_METHOD_1         1  '1 positional argument'
              660  STORE_FAST               '_learning_rate'

 L. 517       662  LOAD_GLOBAL              basic_data
              664  LOAD_METHOD              str2float
              666  LOAD_DEREF               'self'
              668  LOAD_ATTR                ldtdropout
              670  LOAD_METHOD              text
              672  CALL_METHOD_0         0  '0 positional arguments'
              674  CALL_METHOD_1         1  '1 positional argument'
              676  STORE_FAST               '_dropout_prob'

 L. 518       678  LOAD_FAST                '_nconvblock'
              680  LOAD_CONST               False
              682  COMPARE_OP               is
          684_686  POP_JUMP_IF_TRUE    698  'to 698'
              688  LOAD_FAST                '_nconvblock'
              690  LOAD_CONST               0
              692  COMPARE_OP               <=
          694_696  POP_JUMP_IF_FALSE   734  'to 734'
            698_0  COME_FROM           684  '684'

 L. 519       698  LOAD_GLOBAL              vis_msg
              700  LOAD_ATTR                print
              702  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Non-positive convolutional block number'

 L. 520       704  LOAD_STR                 'error'
              706  LOAD_CONST               ('type',)
              708  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              710  POP_TOP          

 L. 521       712  LOAD_GLOBAL              QtWidgets
              714  LOAD_ATTR                QMessageBox
              716  LOAD_METHOD              critical
              718  LOAD_DEREF               'self'
              720  LOAD_ATTR                msgbox

 L. 522       722  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 523       724  LOAD_STR                 'Non-positive convolutional block number'
              726  CALL_METHOD_3         3  '3 positional arguments'
              728  POP_TOP          

 L. 524       730  LOAD_CONST               None
              732  RETURN_VALUE     
            734_0  COME_FROM           694  '694'

 L. 525       734  SETUP_LOOP          806  'to 806'
              736  LOAD_FAST                '_nconvlayer'
              738  GET_ITER         
            740_0  COME_FROM           760  '760'
              740  FOR_ITER            804  'to 804'
              742  STORE_FAST               '_i'

 L. 526       744  LOAD_FAST                '_i'
              746  LOAD_CONST               False
              748  COMPARE_OP               is
          750_752  POP_JUMP_IF_TRUE    764  'to 764'
              754  LOAD_FAST                '_i'
              756  LOAD_CONST               1
              758  COMPARE_OP               <
          760_762  POP_JUMP_IF_FALSE   740  'to 740'
            764_0  COME_FROM           750  '750'

 L. 527       764  LOAD_GLOBAL              vis_msg
              766  LOAD_ATTR                print
              768  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Non-positive convolutional layer number'

 L. 528       770  LOAD_STR                 'error'
              772  LOAD_CONST               ('type',)
              774  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              776  POP_TOP          

 L. 529       778  LOAD_GLOBAL              QtWidgets
              780  LOAD_ATTR                QMessageBox
              782  LOAD_METHOD              critical
              784  LOAD_DEREF               'self'
              786  LOAD_ATTR                msgbox

 L. 530       788  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 531       790  LOAD_STR                 'Non-positive convolutional layer number'
              792  CALL_METHOD_3         3  '3 positional arguments'
              794  POP_TOP          

 L. 532       796  LOAD_CONST               None
              798  RETURN_VALUE     
          800_802  JUMP_BACK           740  'to 740'
              804  POP_BLOCK        
            806_0  COME_FROM_LOOP      734  '734'

 L. 533       806  SETUP_LOOP          878  'to 878'
              808  LOAD_FAST                '_nconvfeature'
              810  GET_ITER         
            812_0  COME_FROM           832  '832'
              812  FOR_ITER            876  'to 876'
              814  STORE_FAST               '_i'

 L. 534       816  LOAD_FAST                '_i'
              818  LOAD_CONST               False
              820  COMPARE_OP               is
          822_824  POP_JUMP_IF_TRUE    836  'to 836'
              826  LOAD_FAST                '_i'
              828  LOAD_CONST               1
              830  COMPARE_OP               <
          832_834  POP_JUMP_IF_FALSE   812  'to 812'
            836_0  COME_FROM           822  '822'

 L. 535       836  LOAD_GLOBAL              vis_msg
              838  LOAD_ATTR                print
              840  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Non-positive convolutional feature number'

 L. 536       842  LOAD_STR                 'error'
              844  LOAD_CONST               ('type',)
              846  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              848  POP_TOP          

 L. 537       850  LOAD_GLOBAL              QtWidgets
              852  LOAD_ATTR                QMessageBox
              854  LOAD_METHOD              critical
              856  LOAD_DEREF               'self'
              858  LOAD_ATTR                msgbox

 L. 538       860  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 539       862  LOAD_STR                 'Non-positive convolutional feature number'
              864  CALL_METHOD_3         3  '3 positional arguments'
              866  POP_TOP          

 L. 540       868  LOAD_CONST               None
              870  RETURN_VALUE     
          872_874  JUMP_BACK           812  'to 812'
              876  POP_BLOCK        
            878_0  COME_FROM_LOOP      806  '806'

 L. 541       878  LOAD_FAST                '_n1x1layer'
              880  LOAD_CONST               False
              882  COMPARE_OP               is
          884_886  POP_JUMP_IF_TRUE    898  'to 898'
              888  LOAD_FAST                '_n1x1layer'
              890  LOAD_CONST               0
              892  COMPARE_OP               <=
          894_896  POP_JUMP_IF_FALSE   934  'to 934'
            898_0  COME_FROM           884  '884'

 L. 542       898  LOAD_GLOBAL              vis_msg
              900  LOAD_ATTR                print
              902  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Non-positive 1x1 convolutional layer number'

 L. 543       904  LOAD_STR                 'error'
              906  LOAD_CONST               ('type',)
              908  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              910  POP_TOP          

 L. 544       912  LOAD_GLOBAL              QtWidgets
              914  LOAD_ATTR                QMessageBox
              916  LOAD_METHOD              critical
              918  LOAD_DEREF               'self'
              920  LOAD_ATTR                msgbox

 L. 545       922  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 546       924  LOAD_STR                 'Non-positive 1x1 convolutional layer number'
              926  CALL_METHOD_3         3  '3 positional arguments'
              928  POP_TOP          

 L. 547       930  LOAD_CONST               None
              932  RETURN_VALUE     
            934_0  COME_FROM           894  '894'

 L. 548       934  SETUP_LOOP         1006  'to 1006'
              936  LOAD_FAST                '_n1x1feature'
              938  GET_ITER         
            940_0  COME_FROM           960  '960'
              940  FOR_ITER           1004  'to 1004'
              942  STORE_FAST               '_i'

 L. 549       944  LOAD_FAST                '_i'
              946  LOAD_CONST               False
              948  COMPARE_OP               is
          950_952  POP_JUMP_IF_TRUE    964  'to 964'
              954  LOAD_FAST                '_i'
              956  LOAD_CONST               1
              958  COMPARE_OP               <
          960_962  POP_JUMP_IF_FALSE   940  'to 940'
            964_0  COME_FROM           950  '950'

 L. 550       964  LOAD_GLOBAL              vis_msg
              966  LOAD_ATTR                print
              968  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Non-positive 1x1 convolutional feature number'

 L. 551       970  LOAD_STR                 'error'
              972  LOAD_CONST               ('type',)
              974  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              976  POP_TOP          

 L. 552       978  LOAD_GLOBAL              QtWidgets
              980  LOAD_ATTR                QMessageBox
              982  LOAD_METHOD              critical
              984  LOAD_DEREF               'self'
              986  LOAD_ATTR                msgbox

 L. 553       988  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 554       990  LOAD_STR                 'Non-positive 1x1 convolutional feature number'
              992  CALL_METHOD_3         3  '3 positional arguments'
              994  POP_TOP          

 L. 555       996  LOAD_CONST               None
              998  RETURN_VALUE     
         1000_1002  JUMP_BACK           940  'to 940'
             1004  POP_BLOCK        
           1006_0  COME_FROM_LOOP      934  '934'

 L. 556      1006  LOAD_FAST                '_patch_height'
             1008  LOAD_CONST               False
             1010  COMPARE_OP               is
         1012_1014  POP_JUMP_IF_TRUE   1046  'to 1046'
             1016  LOAD_FAST                '_patch_width'
             1018  LOAD_CONST               False
             1020  COMPARE_OP               is
         1022_1024  POP_JUMP_IF_TRUE   1046  'to 1046'

 L. 557      1026  LOAD_FAST                '_patch_height'
             1028  LOAD_CONST               1
             1030  COMPARE_OP               <
         1032_1034  POP_JUMP_IF_TRUE   1046  'to 1046'
             1036  LOAD_FAST                '_patch_width'
             1038  LOAD_CONST               1
             1040  COMPARE_OP               <
         1042_1044  POP_JUMP_IF_FALSE  1082  'to 1082'
           1046_0  COME_FROM          1032  '1032'
           1046_1  COME_FROM          1022  '1022'
           1046_2  COME_FROM          1012  '1012'

 L. 558      1046  LOAD_GLOBAL              vis_msg
             1048  LOAD_ATTR                print
             1050  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Non-positive convolutional patch size'

 L. 559      1052  LOAD_STR                 'error'
             1054  LOAD_CONST               ('type',)
             1056  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1058  POP_TOP          

 L. 560      1060  LOAD_GLOBAL              QtWidgets
             1062  LOAD_ATTR                QMessageBox
             1064  LOAD_METHOD              critical
             1066  LOAD_DEREF               'self'
             1068  LOAD_ATTR                msgbox

 L. 561      1070  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 562      1072  LOAD_STR                 'Non-positive convolutional patch size'
             1074  CALL_METHOD_3         3  '3 positional arguments'
             1076  POP_TOP          

 L. 563      1078  LOAD_CONST               None
             1080  RETURN_VALUE     
           1082_0  COME_FROM          1042  '1042'

 L. 564      1082  LOAD_FAST                '_pool_height'
             1084  LOAD_CONST               False
             1086  COMPARE_OP               is
         1088_1090  POP_JUMP_IF_TRUE   1122  'to 1122'
             1092  LOAD_FAST                '_pool_width'
             1094  LOAD_CONST               False
             1096  COMPARE_OP               is
         1098_1100  POP_JUMP_IF_TRUE   1122  'to 1122'

 L. 565      1102  LOAD_FAST                '_pool_height'
             1104  LOAD_CONST               1
             1106  COMPARE_OP               <
         1108_1110  POP_JUMP_IF_TRUE   1122  'to 1122'
             1112  LOAD_FAST                '_pool_width'
             1114  LOAD_CONST               1
             1116  COMPARE_OP               <
         1118_1120  POP_JUMP_IF_FALSE  1158  'to 1158'
           1122_0  COME_FROM          1108  '1108'
           1122_1  COME_FROM          1098  '1098'
           1122_2  COME_FROM          1088  '1088'

 L. 566      1122  LOAD_GLOBAL              vis_msg
             1124  LOAD_ATTR                print
             1126  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Non-positive pooling size'
             1128  LOAD_STR                 'error'
             1130  LOAD_CONST               ('type',)
             1132  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1134  POP_TOP          

 L. 567      1136  LOAD_GLOBAL              QtWidgets
             1138  LOAD_ATTR                QMessageBox
             1140  LOAD_METHOD              critical
             1142  LOAD_DEREF               'self'
             1144  LOAD_ATTR                msgbox

 L. 568      1146  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 569      1148  LOAD_STR                 'Non-positive pooling size'
             1150  CALL_METHOD_3         3  '3 positional arguments'
             1152  POP_TOP          

 L. 570      1154  LOAD_CONST               None
             1156  RETURN_VALUE     
           1158_0  COME_FROM          1118  '1118'

 L. 571      1158  LOAD_FAST                '_nepoch'
             1160  LOAD_CONST               False
             1162  COMPARE_OP               is
         1164_1166  POP_JUMP_IF_TRUE   1178  'to 1178'
             1168  LOAD_FAST                '_nepoch'
             1170  LOAD_CONST               0
             1172  COMPARE_OP               <=
         1174_1176  POP_JUMP_IF_FALSE  1214  'to 1214'
           1178_0  COME_FROM          1164  '1164'

 L. 572      1178  LOAD_GLOBAL              vis_msg
             1180  LOAD_ATTR                print
             1182  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Non-positive epoch number'
             1184  LOAD_STR                 'error'
             1186  LOAD_CONST               ('type',)
             1188  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1190  POP_TOP          

 L. 573      1192  LOAD_GLOBAL              QtWidgets
             1194  LOAD_ATTR                QMessageBox
             1196  LOAD_METHOD              critical
             1198  LOAD_DEREF               'self'
             1200  LOAD_ATTR                msgbox

 L. 574      1202  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 575      1204  LOAD_STR                 'Non-positive epoch number'
             1206  CALL_METHOD_3         3  '3 positional arguments'
             1208  POP_TOP          

 L. 576      1210  LOAD_CONST               None
             1212  RETURN_VALUE     
           1214_0  COME_FROM          1174  '1174'

 L. 577      1214  LOAD_FAST                '_batchsize'
             1216  LOAD_CONST               False
             1218  COMPARE_OP               is
         1220_1222  POP_JUMP_IF_TRUE   1234  'to 1234'
             1224  LOAD_FAST                '_batchsize'
             1226  LOAD_CONST               0
             1228  COMPARE_OP               <=
         1230_1232  POP_JUMP_IF_FALSE  1270  'to 1270'
           1234_0  COME_FROM          1220  '1220'

 L. 578      1234  LOAD_GLOBAL              vis_msg
             1236  LOAD_ATTR                print
             1238  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Non-positive batch size'
             1240  LOAD_STR                 'error'
             1242  LOAD_CONST               ('type',)
             1244  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1246  POP_TOP          

 L. 579      1248  LOAD_GLOBAL              QtWidgets
             1250  LOAD_ATTR                QMessageBox
             1252  LOAD_METHOD              critical
             1254  LOAD_DEREF               'self'
             1256  LOAD_ATTR                msgbox

 L. 580      1258  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 581      1260  LOAD_STR                 'Non-positive batch size'
             1262  CALL_METHOD_3         3  '3 positional arguments'
             1264  POP_TOP          

 L. 582      1266  LOAD_CONST               None
             1268  RETURN_VALUE     
           1270_0  COME_FROM          1230  '1230'

 L. 583      1270  LOAD_FAST                '_learning_rate'
             1272  LOAD_CONST               False
             1274  COMPARE_OP               is
         1276_1278  POP_JUMP_IF_TRUE   1290  'to 1290'
             1280  LOAD_FAST                '_learning_rate'
             1282  LOAD_CONST               0
             1284  COMPARE_OP               <=
         1286_1288  POP_JUMP_IF_FALSE  1326  'to 1326'
           1290_0  COME_FROM          1276  '1276'

 L. 584      1290  LOAD_GLOBAL              vis_msg
             1292  LOAD_ATTR                print
             1294  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Non-positive learning rate'
             1296  LOAD_STR                 'error'
             1298  LOAD_CONST               ('type',)
             1300  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1302  POP_TOP          

 L. 585      1304  LOAD_GLOBAL              QtWidgets
             1306  LOAD_ATTR                QMessageBox
             1308  LOAD_METHOD              critical
             1310  LOAD_DEREF               'self'
             1312  LOAD_ATTR                msgbox

 L. 586      1314  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 587      1316  LOAD_STR                 'Non-positive learning rate'
             1318  CALL_METHOD_3         3  '3 positional arguments'
             1320  POP_TOP          

 L. 588      1322  LOAD_CONST               None
             1324  RETURN_VALUE     
           1326_0  COME_FROM          1286  '1286'

 L. 589      1326  LOAD_FAST                '_dropout_prob'
             1328  LOAD_CONST               False
             1330  COMPARE_OP               is
         1332_1334  POP_JUMP_IF_TRUE   1346  'to 1346'
             1336  LOAD_FAST                '_dropout_prob'
             1338  LOAD_CONST               0
             1340  COMPARE_OP               <=
         1342_1344  POP_JUMP_IF_FALSE  1382  'to 1382'
           1346_0  COME_FROM          1332  '1332'

 L. 590      1346  LOAD_GLOBAL              vis_msg
             1348  LOAD_ATTR                print
             1350  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: Negative dropout rate'
             1352  LOAD_STR                 'error'
             1354  LOAD_CONST               ('type',)
             1356  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1358  POP_TOP          

 L. 591      1360  LOAD_GLOBAL              QtWidgets
             1362  LOAD_ATTR                QMessageBox
             1364  LOAD_METHOD              critical
             1366  LOAD_DEREF               'self'
             1368  LOAD_ATTR                msgbox

 L. 592      1370  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 593      1372  LOAD_STR                 'Negative dropout rate'
             1374  CALL_METHOD_3         3  '3 positional arguments'
             1376  POP_TOP          

 L. 594      1378  LOAD_CONST               None
             1380  RETURN_VALUE     
           1382_0  COME_FROM          1342  '1342'

 L. 596      1382  LOAD_GLOBAL              len
             1384  LOAD_DEREF               'self'
             1386  LOAD_ATTR                ldtsave
             1388  LOAD_METHOD              text
             1390  CALL_METHOD_0         0  '0 positional arguments'
             1392  CALL_FUNCTION_1       1  '1 positional argument'
             1394  LOAD_CONST               1
             1396  COMPARE_OP               <
         1398_1400  POP_JUMP_IF_FALSE  1438  'to 1438'

 L. 597      1402  LOAD_GLOBAL              vis_msg
             1404  LOAD_ATTR                print
             1406  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: No name specified for WDCNN network'

 L. 598      1408  LOAD_STR                 'error'
             1410  LOAD_CONST               ('type',)
             1412  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1414  POP_TOP          

 L. 599      1416  LOAD_GLOBAL              QtWidgets
             1418  LOAD_ATTR                QMessageBox
             1420  LOAD_METHOD              critical
             1422  LOAD_DEREF               'self'
             1424  LOAD_ATTR                msgbox

 L. 600      1426  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 601      1428  LOAD_STR                 'No name specified for WDCNN network'
             1430  CALL_METHOD_3         3  '3 positional arguments'
             1432  POP_TOP          

 L. 602      1434  LOAD_CONST               None
             1436  RETURN_VALUE     
           1438_0  COME_FROM          1398  '1398'

 L. 603      1438  LOAD_GLOBAL              os
             1440  LOAD_ATTR                path
             1442  LOAD_METHOD              dirname
             1444  LOAD_DEREF               'self'
             1446  LOAD_ATTR                ldtsave
             1448  LOAD_METHOD              text
             1450  CALL_METHOD_0         0  '0 positional arguments'
             1452  CALL_METHOD_1         1  '1 positional argument'
             1454  STORE_FAST               '_savepath'

 L. 604      1456  LOAD_GLOBAL              os
             1458  LOAD_ATTR                path
             1460  LOAD_METHOD              splitext
             1462  LOAD_GLOBAL              os
             1464  LOAD_ATTR                path
             1466  LOAD_METHOD              basename
             1468  LOAD_DEREF               'self'
             1470  LOAD_ATTR                ldtsave
             1472  LOAD_METHOD              text
             1474  CALL_METHOD_0         0  '0 positional arguments'
             1476  CALL_METHOD_1         1  '1 positional argument'
             1478  CALL_METHOD_1         1  '1 positional argument'
             1480  LOAD_CONST               0
             1482  BINARY_SUBSCR    
             1484  STORE_FAST               '_savename'

 L. 606      1486  LOAD_CONST               0
             1488  STORE_FAST               '_wdinl'

 L. 607      1490  LOAD_CONST               0
             1492  STORE_FAST               '_wdxl'

 L. 608      1494  LOAD_CONST               0
             1496  STORE_FAST               '_wdz'

 L. 609      1498  LOAD_CONST               0
             1500  STORE_FAST               '_wdinltarget'

 L. 610      1502  LOAD_CONST               0
             1504  STORE_FAST               '_wdxltarget'

 L. 611      1506  LOAD_CONST               0
             1508  STORE_FAST               '_wdztarget'

 L. 612      1510  LOAD_DEREF               'self'
             1512  LOAD_ATTR                cbbornt
             1514  LOAD_METHOD              currentIndex
             1516  CALL_METHOD_0         0  '0 positional arguments'
             1518  LOAD_CONST               0
             1520  COMPARE_OP               ==
         1522_1524  POP_JUMP_IF_FALSE  1562  'to 1562'

 L. 613      1526  LOAD_GLOBAL              int
             1528  LOAD_FAST                '_image_width'
             1530  LOAD_CONST               2
             1532  BINARY_TRUE_DIVIDE
             1534  CALL_FUNCTION_1       1  '1 positional argument'
             1536  STORE_FAST               '_wdxl'

 L. 614      1538  LOAD_GLOBAL              int
             1540  LOAD_FAST                '_image_height'
             1542  LOAD_CONST               2
             1544  BINARY_TRUE_DIVIDE
             1546  CALL_FUNCTION_1       1  '1 positional argument'
             1548  STORE_FAST               '_wdz'

 L. 615      1550  LOAD_GLOBAL              int
             1552  LOAD_FAST                '_image_height'
             1554  LOAD_CONST               2
             1556  BINARY_TRUE_DIVIDE
             1558  CALL_FUNCTION_1       1  '1 positional argument'
             1560  STORE_FAST               '_wdztarget'
           1562_0  COME_FROM          1522  '1522'

 L. 616      1562  LOAD_DEREF               'self'
             1564  LOAD_ATTR                cbbornt
             1566  LOAD_METHOD              currentIndex
             1568  CALL_METHOD_0         0  '0 positional arguments'
             1570  LOAD_CONST               1
             1572  COMPARE_OP               ==
         1574_1576  POP_JUMP_IF_FALSE  1614  'to 1614'

 L. 617      1578  LOAD_GLOBAL              int
             1580  LOAD_FAST                '_image_width'
             1582  LOAD_CONST               2
             1584  BINARY_TRUE_DIVIDE
             1586  CALL_FUNCTION_1       1  '1 positional argument'
             1588  STORE_FAST               '_wdinl'

 L. 618      1590  LOAD_GLOBAL              int
             1592  LOAD_FAST                '_image_height'
             1594  LOAD_CONST               2
             1596  BINARY_TRUE_DIVIDE
             1598  CALL_FUNCTION_1       1  '1 positional argument'
             1600  STORE_FAST               '_wdz'

 L. 619      1602  LOAD_GLOBAL              int
             1604  LOAD_FAST                '_image_height'
             1606  LOAD_CONST               2
             1608  BINARY_TRUE_DIVIDE
             1610  CALL_FUNCTION_1       1  '1 positional argument'
             1612  STORE_FAST               '_wdztarget'
           1614_0  COME_FROM          1574  '1574'

 L. 620      1614  LOAD_DEREF               'self'
             1616  LOAD_ATTR                cbbornt
             1618  LOAD_METHOD              currentIndex
             1620  CALL_METHOD_0         0  '0 positional arguments'
             1622  LOAD_CONST               2
             1624  COMPARE_OP               ==
         1626_1628  POP_JUMP_IF_FALSE  1666  'to 1666'

 L. 621      1630  LOAD_GLOBAL              int
             1632  LOAD_FAST                '_image_width'
             1634  LOAD_CONST               2
             1636  BINARY_TRUE_DIVIDE
             1638  CALL_FUNCTION_1       1  '1 positional argument'
             1640  STORE_FAST               '_wdinl'

 L. 622      1642  LOAD_GLOBAL              int
             1644  LOAD_FAST                '_image_height'
             1646  LOAD_CONST               2
             1648  BINARY_TRUE_DIVIDE
             1650  CALL_FUNCTION_1       1  '1 positional argument'
             1652  STORE_FAST               '_wdxl'

 L. 623      1654  LOAD_GLOBAL              int
             1656  LOAD_FAST                '_image_height'
             1658  LOAD_CONST               2
             1660  BINARY_TRUE_DIVIDE
             1662  CALL_FUNCTION_1       1  '1 positional argument'
             1664  STORE_FAST               '_wdxltarget'
           1666_0  COME_FROM          1626  '1626'

 L. 625      1666  LOAD_DEREF               'self'
             1668  LOAD_ATTR                survinfo
             1670  STORE_FAST               '_seisinfo'

 L. 627      1672  LOAD_GLOBAL              print
             1674  LOAD_STR                 'TrainMl15DWdcnnFromScratch: Step 1 - Get training samples:'
             1676  CALL_FUNCTION_1       1  '1 positional argument'
             1678  POP_TOP          

 L. 628      1680  LOAD_DEREF               'self'
             1682  LOAD_ATTR                traindataconfig
             1684  LOAD_STR                 'TrainPointSet'
             1686  BINARY_SUBSCR    
             1688  STORE_FAST               '_trainpoint'

 L. 629      1690  LOAD_GLOBAL              np
             1692  LOAD_METHOD              zeros
             1694  LOAD_CONST               0
             1696  LOAD_CONST               3
             1698  BUILD_LIST_2          2 
             1700  CALL_METHOD_1         1  '1 positional argument'
             1702  STORE_FAST               '_traindata'

 L. 630      1704  SETUP_LOOP         1780  'to 1780'
             1706  LOAD_FAST                '_trainpoint'
             1708  GET_ITER         
           1710_0  COME_FROM          1728  '1728'
             1710  FOR_ITER           1778  'to 1778'
             1712  STORE_FAST               '_p'

 L. 631      1714  LOAD_GLOBAL              point_ays
             1716  LOAD_METHOD              checkPoint
             1718  LOAD_DEREF               'self'
             1720  LOAD_ATTR                pointsetdata
             1722  LOAD_FAST                '_p'
             1724  BINARY_SUBSCR    
             1726  CALL_METHOD_1         1  '1 positional argument'
         1728_1730  POP_JUMP_IF_FALSE  1710  'to 1710'

 L. 632      1732  LOAD_GLOBAL              basic_mdt
             1734  LOAD_METHOD              exportMatDict
             1736  LOAD_DEREF               'self'
             1738  LOAD_ATTR                pointsetdata
             1740  LOAD_FAST                '_p'
             1742  BINARY_SUBSCR    
             1744  LOAD_STR                 'Inline'
             1746  LOAD_STR                 'Crossline'
             1748  LOAD_STR                 'Z'
             1750  BUILD_LIST_3          3 
             1752  CALL_METHOD_2         2  '2 positional arguments'
             1754  STORE_FAST               '_pt'

 L. 633      1756  LOAD_GLOBAL              np
             1758  LOAD_ATTR                concatenate
             1760  LOAD_FAST                '_traindata'
             1762  LOAD_FAST                '_pt'
             1764  BUILD_TUPLE_2         2 
             1766  LOAD_CONST               0
             1768  LOAD_CONST               ('axis',)
             1770  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1772  STORE_FAST               '_traindata'
         1774_1776  JUMP_BACK          1710  'to 1710'
             1778  POP_BLOCK        
           1780_0  COME_FROM_LOOP     1704  '1704'

 L. 634      1780  LOAD_GLOBAL              seis_ays
             1782  LOAD_ATTR                removeOutofSurveySample
             1784  LOAD_FAST                '_traindata'

 L. 635      1786  LOAD_FAST                '_seisinfo'
             1788  LOAD_STR                 'ILStart'
             1790  BINARY_SUBSCR    
             1792  LOAD_FAST                '_wdinl'
             1794  LOAD_FAST                '_seisinfo'
             1796  LOAD_STR                 'ILStep'
             1798  BINARY_SUBSCR    
             1800  BINARY_MULTIPLY  
             1802  BINARY_ADD       

 L. 636      1804  LOAD_FAST                '_seisinfo'
             1806  LOAD_STR                 'ILEnd'
             1808  BINARY_SUBSCR    
             1810  LOAD_FAST                '_wdinl'
             1812  LOAD_FAST                '_seisinfo'
             1814  LOAD_STR                 'ILStep'
             1816  BINARY_SUBSCR    
             1818  BINARY_MULTIPLY  
             1820  BINARY_SUBTRACT  

 L. 637      1822  LOAD_FAST                '_seisinfo'
             1824  LOAD_STR                 'XLStart'
             1826  BINARY_SUBSCR    
             1828  LOAD_FAST                '_wdxl'
             1830  LOAD_FAST                '_seisinfo'
             1832  LOAD_STR                 'XLStep'
             1834  BINARY_SUBSCR    
             1836  BINARY_MULTIPLY  
             1838  BINARY_ADD       

 L. 638      1840  LOAD_FAST                '_seisinfo'
             1842  LOAD_STR                 'XLEnd'
             1844  BINARY_SUBSCR    
             1846  LOAD_FAST                '_wdxl'
             1848  LOAD_FAST                '_seisinfo'
             1850  LOAD_STR                 'XLStep'
             1852  BINARY_SUBSCR    
             1854  BINARY_MULTIPLY  
             1856  BINARY_SUBTRACT  

 L. 639      1858  LOAD_FAST                '_seisinfo'
             1860  LOAD_STR                 'ZStart'
             1862  BINARY_SUBSCR    
             1864  LOAD_FAST                '_wdz'
             1866  LOAD_FAST                '_seisinfo'
             1868  LOAD_STR                 'ZStep'
             1870  BINARY_SUBSCR    
             1872  BINARY_MULTIPLY  
             1874  BINARY_ADD       

 L. 640      1876  LOAD_FAST                '_seisinfo'
             1878  LOAD_STR                 'ZEnd'
             1880  BINARY_SUBSCR    
             1882  LOAD_FAST                '_wdz'
             1884  LOAD_FAST                '_seisinfo'
             1886  LOAD_STR                 'ZStep'
             1888  BINARY_SUBSCR    
             1890  BINARY_MULTIPLY  
             1892  BINARY_SUBTRACT  
             1894  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1896  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1898  STORE_FAST               '_traindata'

 L. 643      1900  LOAD_GLOBAL              np
             1902  LOAD_METHOD              shape
             1904  LOAD_FAST                '_traindata'
             1906  CALL_METHOD_1         1  '1 positional argument'
             1908  LOAD_CONST               0
             1910  BINARY_SUBSCR    
             1912  LOAD_CONST               0
             1914  COMPARE_OP               <=
         1916_1918  POP_JUMP_IF_FALSE  1956  'to 1956'

 L. 644      1920  LOAD_GLOBAL              vis_msg
             1922  LOAD_ATTR                print
             1924  LOAD_STR                 'ERROR in TrainMl2DDCnnFromScratch: No training sample found'
             1926  LOAD_STR                 'error'
             1928  LOAD_CONST               ('type',)
             1930  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1932  POP_TOP          

 L. 645      1934  LOAD_GLOBAL              QtWidgets
             1936  LOAD_ATTR                QMessageBox
             1938  LOAD_METHOD              critical
             1940  LOAD_DEREF               'self'
             1942  LOAD_ATTR                msgbox

 L. 646      1944  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 647      1946  LOAD_STR                 'No training sample found'
             1948  CALL_METHOD_3         3  '3 positional arguments'
             1950  POP_TOP          

 L. 648      1952  LOAD_CONST               None
             1954  RETURN_VALUE     
           1956_0  COME_FROM          1916  '1916'

 L. 651      1956  LOAD_GLOBAL              print
             1958  LOAD_STR                 'TrainMl15DWdcnnFromScratch: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 652      1960  LOAD_FAST                '_image_height'
             1962  LOAD_FAST                '_image_width'
             1964  LOAD_FAST                '_image_height_new'
             1966  LOAD_FAST                '_image_width_new'
             1968  BUILD_TUPLE_4         4 
             1970  BINARY_MODULO    
             1972  CALL_FUNCTION_1       1  '1 positional argument'
             1974  POP_TOP          

 L. 653      1976  BUILD_MAP_0           0 
             1978  STORE_FAST               '_traindict'

 L. 654      1980  SETUP_LOOP         2052  'to 2052'
             1982  LOAD_FAST                '_features'
             1984  GET_ITER         
             1986  FOR_ITER           2050  'to 2050'
             1988  STORE_FAST               'f'

 L. 655      1990  LOAD_DEREF               'self'
             1992  LOAD_ATTR                seisdata
             1994  LOAD_FAST                'f'
             1996  BINARY_SUBSCR    
             1998  STORE_FAST               '_seisdata'

 L. 656      2000  LOAD_GLOBAL              seis_ays
             2002  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2004  LOAD_FAST                '_seisdata'
             2006  LOAD_FAST                '_traindata'
             2008  LOAD_DEREF               'self'
             2010  LOAD_ATTR                survinfo

 L. 657      2012  LOAD_FAST                '_wdinl'
             2014  LOAD_FAST                '_wdxl'
             2016  LOAD_FAST                '_wdz'

 L. 658      2018  LOAD_CONST               False
             2020  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2022  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2024  LOAD_CONST               None
             2026  LOAD_CONST               None
             2028  BUILD_SLICE_2         2 
             2030  LOAD_CONST               3
             2032  LOAD_CONST               None
             2034  BUILD_SLICE_2         2 
             2036  BUILD_TUPLE_2         2 
             2038  BINARY_SUBSCR    
             2040  LOAD_FAST                '_traindict'
             2042  LOAD_FAST                'f'
             2044  STORE_SUBSCR     
         2046_2048  JUMP_BACK          1986  'to 1986'
             2050  POP_BLOCK        
           2052_0  COME_FROM_LOOP     1980  '1980'

 L. 659      2052  LOAD_FAST                '_target'
             2054  LOAD_FAST                '_features'
             2056  COMPARE_OP               not-in
         2058_2060  POP_JUMP_IF_FALSE  2118  'to 2118'

 L. 660      2062  LOAD_DEREF               'self'
             2064  LOAD_ATTR                seisdata
             2066  LOAD_FAST                '_target'
             2068  BINARY_SUBSCR    
             2070  STORE_FAST               '_seisdata'

 L. 661      2072  LOAD_GLOBAL              seis_ays
             2074  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2076  LOAD_FAST                '_seisdata'
             2078  LOAD_FAST                '_traindata'
             2080  LOAD_DEREF               'self'
             2082  LOAD_ATTR                survinfo

 L. 662      2084  LOAD_FAST                '_wdinltarget'

 L. 663      2086  LOAD_FAST                '_wdxltarget'

 L. 664      2088  LOAD_FAST                '_wdztarget'

 L. 665      2090  LOAD_CONST               False
             2092  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2094  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2096  LOAD_CONST               None
             2098  LOAD_CONST               None
             2100  BUILD_SLICE_2         2 
             2102  LOAD_CONST               3
             2104  LOAD_CONST               None
             2106  BUILD_SLICE_2         2 
             2108  BUILD_TUPLE_2         2 
             2110  BINARY_SUBSCR    
             2112  LOAD_FAST                '_traindict'
             2114  LOAD_FAST                '_target'
             2116  STORE_SUBSCR     
           2118_0  COME_FROM          2058  '2058'

 L. 666      2118  LOAD_FAST                '_weight'
             2120  LOAD_FAST                '_features'
             2122  COMPARE_OP               not-in
         2124_2126  POP_JUMP_IF_FALSE  2194  'to 2194'
             2128  LOAD_FAST                '_weight'
             2130  LOAD_FAST                '_target'
             2132  COMPARE_OP               !=
         2134_2136  POP_JUMP_IF_FALSE  2194  'to 2194'

 L. 667      2138  LOAD_DEREF               'self'
             2140  LOAD_ATTR                seisdata
             2142  LOAD_FAST                '_weight'
             2144  BINARY_SUBSCR    
             2146  STORE_FAST               '_seisdata'

 L. 668      2148  LOAD_GLOBAL              seis_ays
             2150  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2152  LOAD_FAST                '_seisdata'
             2154  LOAD_FAST                '_traindata'
             2156  LOAD_DEREF               'self'
             2158  LOAD_ATTR                survinfo

 L. 669      2160  LOAD_FAST                '_wdinltarget'

 L. 670      2162  LOAD_FAST                '_wdxltarget'

 L. 671      2164  LOAD_FAST                '_wdztarget'

 L. 672      2166  LOAD_CONST               False
             2168  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2170  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2172  LOAD_CONST               None
             2174  LOAD_CONST               None
             2176  BUILD_SLICE_2         2 
             2178  LOAD_CONST               3
             2180  LOAD_CONST               None
             2182  BUILD_SLICE_2         2 
             2184  BUILD_TUPLE_2         2 
             2186  BINARY_SUBSCR    
             2188  LOAD_FAST                '_traindict'
             2190  LOAD_FAST                '_weight'
             2192  STORE_SUBSCR     
           2194_0  COME_FROM          2134  '2134'
           2194_1  COME_FROM          2124  '2124'

 L. 674      2194  LOAD_DEREF               'self'
             2196  LOAD_ATTR                traindataconfig
             2198  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2200  BINARY_SUBSCR    
         2202_2204  POP_JUMP_IF_FALSE  2286  'to 2286'

 L. 675      2206  SETUP_LOOP         2286  'to 2286'
             2208  LOAD_FAST                '_features'
             2210  GET_ITER         
           2212_0  COME_FROM          2240  '2240'
             2212  FOR_ITER           2284  'to 2284'
             2214  STORE_FAST               'f'

 L. 676      2216  LOAD_GLOBAL              ml_aug
             2218  LOAD_METHOD              removeInvariantFeature
             2220  LOAD_FAST                '_traindict'
             2222  LOAD_FAST                'f'
             2224  CALL_METHOD_2         2  '2 positional arguments'
             2226  STORE_FAST               '_traindict'

 L. 677      2228  LOAD_GLOBAL              basic_mdt
             2230  LOAD_METHOD              maxDictConstantRow
             2232  LOAD_FAST                '_traindict'
             2234  CALL_METHOD_1         1  '1 positional argument'
             2236  LOAD_CONST               0
             2238  COMPARE_OP               <=
         2240_2242  POP_JUMP_IF_FALSE  2212  'to 2212'

 L. 678      2244  LOAD_GLOBAL              vis_msg
             2246  LOAD_ATTR                print
             2248  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: No training sample found'
             2250  LOAD_STR                 'error'
             2252  LOAD_CONST               ('type',)
             2254  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2256  POP_TOP          

 L. 679      2258  LOAD_GLOBAL              QtWidgets
             2260  LOAD_ATTR                QMessageBox
             2262  LOAD_METHOD              critical
             2264  LOAD_DEREF               'self'
             2266  LOAD_ATTR                msgbox

 L. 680      2268  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 681      2270  LOAD_STR                 'No training sample found'
             2272  CALL_METHOD_3         3  '3 positional arguments'
             2274  POP_TOP          

 L. 682      2276  LOAD_CONST               None
             2278  RETURN_VALUE     
         2280_2282  JUMP_BACK          2212  'to 2212'
             2284  POP_BLOCK        
           2286_0  COME_FROM_LOOP     2206  '2206'
           2286_1  COME_FROM          2202  '2202'

 L. 683      2286  LOAD_DEREF               'self'
             2288  LOAD_ATTR                traindataconfig
             2290  LOAD_STR                 'RemoveZeroWeight_Checked'
             2292  BINARY_SUBSCR    
         2294_2296  POP_JUMP_IF_FALSE  2362  'to 2362'

 L. 684      2298  LOAD_GLOBAL              ml_aug
             2300  LOAD_METHOD              removeZeroWeight
             2302  LOAD_FAST                '_traindict'
             2304  LOAD_FAST                '_weight'
             2306  CALL_METHOD_2         2  '2 positional arguments'
             2308  STORE_FAST               '_traindict'

 L. 685      2310  LOAD_GLOBAL              basic_mdt
             2312  LOAD_METHOD              maxDictConstantRow
             2314  LOAD_FAST                '_traindict'
             2316  CALL_METHOD_1         1  '1 positional argument'
             2318  LOAD_CONST               0
             2320  COMPARE_OP               <=
         2322_2324  POP_JUMP_IF_FALSE  2362  'to 2362'

 L. 686      2326  LOAD_GLOBAL              vis_msg
             2328  LOAD_ATTR                print
             2330  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromScratch: No training sample found'
             2332  LOAD_STR                 'error'
             2334  LOAD_CONST               ('type',)
             2336  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2338  POP_TOP          

 L. 687      2340  LOAD_GLOBAL              QtWidgets
             2342  LOAD_ATTR                QMessageBox
             2344  LOAD_METHOD              critical
             2346  LOAD_DEREF               'self'
             2348  LOAD_ATTR                msgbox

 L. 688      2350  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 689      2352  LOAD_STR                 'No training sample found'
             2354  CALL_METHOD_3         3  '3 positional arguments'
             2356  POP_TOP          

 L. 690      2358  LOAD_CONST               None
             2360  RETURN_VALUE     
           2362_0  COME_FROM          2322  '2322'
           2362_1  COME_FROM          2294  '2294'

 L. 692      2362  LOAD_GLOBAL              np
             2364  LOAD_METHOD              shape
             2366  LOAD_FAST                '_traindict'
             2368  LOAD_FAST                '_target'
             2370  BINARY_SUBSCR    
             2372  CALL_METHOD_1         1  '1 positional argument'
             2374  LOAD_CONST               0
             2376  BINARY_SUBSCR    
             2378  LOAD_CONST               0
             2380  COMPARE_OP               <=
         2382_2384  POP_JUMP_IF_FALSE  2422  'to 2422'

 L. 693      2386  LOAD_GLOBAL              vis_msg
             2388  LOAD_ATTR                print
             2390  LOAD_STR                 'ERROR in TrainMl2DDCnnFromScratch: No training sample found'
             2392  LOAD_STR                 'error'
             2394  LOAD_CONST               ('type',)
             2396  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2398  POP_TOP          

 L. 694      2400  LOAD_GLOBAL              QtWidgets
             2402  LOAD_ATTR                QMessageBox
             2404  LOAD_METHOD              critical
             2406  LOAD_DEREF               'self'
             2408  LOAD_ATTR                msgbox

 L. 695      2410  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 696      2412  LOAD_STR                 'No training sample found'
             2414  CALL_METHOD_3         3  '3 positional arguments'
             2416  POP_TOP          

 L. 697      2418  LOAD_CONST               None
             2420  RETURN_VALUE     
           2422_0  COME_FROM          2382  '2382'

 L. 699      2422  LOAD_FAST                '_image_height_new'
             2424  LOAD_FAST                '_image_height'
             2426  COMPARE_OP               !=
         2428_2430  POP_JUMP_IF_TRUE   2442  'to 2442'
             2432  LOAD_FAST                '_image_width_new'
             2434  LOAD_FAST                '_image_width'
             2436  COMPARE_OP               !=
         2438_2440  POP_JUMP_IF_FALSE  2486  'to 2486'
           2442_0  COME_FROM          2428  '2428'

 L. 700      2442  SETUP_LOOP         2486  'to 2486'
             2444  LOAD_FAST                '_features'
             2446  GET_ITER         
             2448  FOR_ITER           2484  'to 2484'
             2450  STORE_FAST               'f'

 L. 701      2452  LOAD_GLOBAL              basic_image
             2454  LOAD_ATTR                changeImageSize
             2456  LOAD_FAST                '_traindict'
             2458  LOAD_FAST                'f'
             2460  BINARY_SUBSCR    

 L. 702      2462  LOAD_FAST                '_image_height'

 L. 703      2464  LOAD_FAST                '_image_width'

 L. 704      2466  LOAD_FAST                '_image_height_new'

 L. 705      2468  LOAD_FAST                '_image_width_new'
             2470  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2472  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2474  LOAD_FAST                '_traindict'
             2476  LOAD_FAST                'f'
             2478  STORE_SUBSCR     
         2480_2482  JUMP_BACK          2448  'to 2448'
             2484  POP_BLOCK        
           2486_0  COME_FROM_LOOP     2442  '2442'
           2486_1  COME_FROM          2438  '2438'

 L. 706      2486  LOAD_FAST                '_image_height_new'
             2488  LOAD_FAST                '_image_height'
             2490  COMPARE_OP               !=
         2492_2494  POP_JUMP_IF_FALSE  2532  'to 2532'
             2496  LOAD_FAST                '_target'
             2498  LOAD_FAST                '_features'
             2500  COMPARE_OP               not-in
         2502_2504  POP_JUMP_IF_FALSE  2532  'to 2532'

 L. 707      2506  LOAD_GLOBAL              basic_curve
             2508  LOAD_ATTR                changeCurveSize
             2510  LOAD_FAST                '_traindict'
             2512  LOAD_FAST                '_target'
             2514  BINARY_SUBSCR    

 L. 708      2516  LOAD_FAST                '_image_height'

 L. 709      2518  LOAD_FAST                '_image_height_new'
             2520  LOAD_STR                 'linear'
             2522  LOAD_CONST               ('length', 'length_new', 'kind')
             2524  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2526  LOAD_FAST                '_traindict'
             2528  LOAD_FAST                '_target'
             2530  STORE_SUBSCR     
           2532_0  COME_FROM          2502  '2502'
           2532_1  COME_FROM          2492  '2492'

 L. 710      2532  LOAD_FAST                '_image_height_new'
             2534  LOAD_FAST                '_image_height'
             2536  COMPARE_OP               !=
         2538_2540  POP_JUMP_IF_FALSE  2588  'to 2588'
             2542  LOAD_FAST                '_weight'
             2544  LOAD_FAST                '_features'
             2546  COMPARE_OP               not-in
         2548_2550  POP_JUMP_IF_FALSE  2588  'to 2588'
             2552  LOAD_FAST                '_weight'
             2554  LOAD_FAST                '_target'
             2556  COMPARE_OP               !=
         2558_2560  POP_JUMP_IF_FALSE  2588  'to 2588'

 L. 711      2562  LOAD_GLOBAL              basic_curve
             2564  LOAD_ATTR                changeCurveSize
             2566  LOAD_FAST                '_traindict'
             2568  LOAD_FAST                '_weight'
             2570  BINARY_SUBSCR    

 L. 712      2572  LOAD_FAST                '_image_height'

 L. 713      2574  LOAD_FAST                '_image_height_new'
             2576  LOAD_STR                 'linear'
             2578  LOAD_CONST               ('length', 'length_new', 'kind')
             2580  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2582  LOAD_FAST                '_traindict'
             2584  LOAD_FAST                '_weight'
             2586  STORE_SUBSCR     
           2588_0  COME_FROM          2558  '2558'
           2588_1  COME_FROM          2548  '2548'
           2588_2  COME_FROM          2538  '2538'

 L. 714      2588  LOAD_DEREF               'self'
             2590  LOAD_ATTR                traindataconfig
             2592  LOAD_STR                 'RotateFeature_Checked'
             2594  BINARY_SUBSCR    
             2596  LOAD_CONST               True
             2598  COMPARE_OP               is
         2600_2602  POP_JUMP_IF_FALSE  2716  'to 2716'

 L. 715      2604  SETUP_LOOP         2642  'to 2642'
             2606  LOAD_FAST                '_features'
             2608  GET_ITER         
             2610  FOR_ITER           2640  'to 2640'
             2612  STORE_FAST               'f'

 L. 716      2614  LOAD_GLOBAL              ml_aug
             2616  LOAD_METHOD              rotateImage4Way
             2618  LOAD_FAST                '_traindict'
             2620  LOAD_FAST                'f'
             2622  BINARY_SUBSCR    
             2624  LOAD_FAST                '_image_height_new'
             2626  LOAD_FAST                '_image_width_new'
             2628  CALL_METHOD_3         3  '3 positional arguments'
             2630  LOAD_FAST                '_traindict'
             2632  LOAD_FAST                'f'
             2634  STORE_SUBSCR     
         2636_2638  JUMP_BACK          2610  'to 2610'
             2640  POP_BLOCK        
           2642_0  COME_FROM_LOOP     2604  '2604'

 L. 717      2642  LOAD_FAST                '_target'
             2644  LOAD_FAST                '_features'
             2646  COMPARE_OP               not-in
         2648_2650  POP_JUMP_IF_FALSE  2674  'to 2674'

 L. 718      2652  LOAD_GLOBAL              ml_aug
             2654  LOAD_METHOD              rotateImage4Way
             2656  LOAD_FAST                '_traindict'
             2658  LOAD_FAST                '_target'
             2660  BINARY_SUBSCR    
             2662  LOAD_FAST                '_image_height_new'
             2664  LOAD_CONST               1
             2666  CALL_METHOD_3         3  '3 positional arguments'
             2668  LOAD_FAST                '_traindict'
             2670  LOAD_FAST                '_target'
             2672  STORE_SUBSCR     
           2674_0  COME_FROM          2648  '2648'

 L. 719      2674  LOAD_FAST                '_weight'
             2676  LOAD_FAST                '_features'
             2678  COMPARE_OP               not-in
         2680_2682  POP_JUMP_IF_FALSE  2716  'to 2716'
             2684  LOAD_FAST                '_weight'
             2686  LOAD_FAST                '_target'
             2688  COMPARE_OP               !=
         2690_2692  POP_JUMP_IF_FALSE  2716  'to 2716'

 L. 720      2694  LOAD_GLOBAL              ml_aug
             2696  LOAD_METHOD              rotateImage4Way
             2698  LOAD_FAST                '_traindict'
             2700  LOAD_FAST                '_weight'
             2702  BINARY_SUBSCR    
             2704  LOAD_FAST                '_image_height_new'
             2706  LOAD_CONST               1
             2708  CALL_METHOD_3         3  '3 positional arguments'
             2710  LOAD_FAST                '_traindict'
             2712  LOAD_FAST                '_weight'
             2714  STORE_SUBSCR     
           2716_0  COME_FROM          2690  '2690'
           2716_1  COME_FROM          2680  '2680'
           2716_2  COME_FROM          2600  '2600'

 L. 722      2716  LOAD_GLOBAL              np
             2718  LOAD_METHOD              round
             2720  LOAD_FAST                '_traindict'
             2722  LOAD_FAST                '_target'
             2724  BINARY_SUBSCR    
             2726  CALL_METHOD_1         1  '1 positional argument'
             2728  LOAD_METHOD              astype
             2730  LOAD_GLOBAL              int
             2732  CALL_METHOD_1         1  '1 positional argument'
             2734  LOAD_FAST                '_traindict'
             2736  LOAD_FAST                '_target'
             2738  STORE_SUBSCR     

 L. 725      2740  LOAD_GLOBAL              print
             2742  LOAD_STR                 'TrainMl15DWdcnnFromScratch: A total of %d valid training samples'
             2744  LOAD_GLOBAL              basic_mdt
             2746  LOAD_METHOD              maxDictConstantRow

 L. 726      2748  LOAD_FAST                '_traindict'
             2750  CALL_METHOD_1         1  '1 positional argument'
             2752  BINARY_MODULO    
             2754  CALL_FUNCTION_1       1  '1 positional argument'
             2756  POP_TOP          

 L. 728      2758  LOAD_GLOBAL              print
             2760  LOAD_STR                 'TrainMl15DWdcnnFromScratch: Step 3 - Start training'
             2762  CALL_FUNCTION_1       1  '1 positional argument'
             2764  POP_TOP          

 L. 730      2766  LOAD_GLOBAL              QtWidgets
             2768  LOAD_METHOD              QProgressDialog
             2770  CALL_METHOD_0         0  '0 positional arguments'
             2772  STORE_FAST               '_pgsdlg'

 L. 731      2774  LOAD_GLOBAL              QtGui
             2776  LOAD_METHOD              QIcon
             2778  CALL_METHOD_0         0  '0 positional arguments'
             2780  STORE_FAST               'icon'

 L. 732      2782  LOAD_FAST                'icon'
             2784  LOAD_METHOD              addPixmap
             2786  LOAD_GLOBAL              QtGui
             2788  LOAD_METHOD              QPixmap
             2790  LOAD_GLOBAL              os
             2792  LOAD_ATTR                path
             2794  LOAD_METHOD              join
             2796  LOAD_DEREF               'self'
             2798  LOAD_ATTR                iconpath
             2800  LOAD_STR                 'icons/new.png'
             2802  CALL_METHOD_2         2  '2 positional arguments'
             2804  CALL_METHOD_1         1  '1 positional argument'

 L. 733      2806  LOAD_GLOBAL              QtGui
             2808  LOAD_ATTR                QIcon
             2810  LOAD_ATTR                Normal
             2812  LOAD_GLOBAL              QtGui
             2814  LOAD_ATTR                QIcon
             2816  LOAD_ATTR                Off
             2818  CALL_METHOD_3         3  '3 positional arguments'
             2820  POP_TOP          

 L. 734      2822  LOAD_FAST                '_pgsdlg'
             2824  LOAD_METHOD              setWindowIcon
             2826  LOAD_FAST                'icon'
             2828  CALL_METHOD_1         1  '1 positional argument'
             2830  POP_TOP          

 L. 735      2832  LOAD_FAST                '_pgsdlg'
             2834  LOAD_METHOD              setWindowTitle
             2836  LOAD_STR                 'Train 1.5D-WDCNN'
             2838  CALL_METHOD_1         1  '1 positional argument'
             2840  POP_TOP          

 L. 736      2842  LOAD_FAST                '_pgsdlg'
             2844  LOAD_METHOD              setCancelButton
             2846  LOAD_CONST               None
             2848  CALL_METHOD_1         1  '1 positional argument'
             2850  POP_TOP          

 L. 737      2852  LOAD_FAST                '_pgsdlg'
             2854  LOAD_METHOD              setWindowFlags
             2856  LOAD_GLOBAL              QtCore
             2858  LOAD_ATTR                Qt
             2860  LOAD_ATTR                WindowStaysOnTopHint
             2862  CALL_METHOD_1         1  '1 positional argument'
             2864  POP_TOP          

 L. 738      2866  LOAD_FAST                '_pgsdlg'
             2868  LOAD_METHOD              forceShow
             2870  CALL_METHOD_0         0  '0 positional arguments'
             2872  POP_TOP          

 L. 739      2874  LOAD_FAST                '_pgsdlg'
             2876  LOAD_METHOD              setFixedWidth
             2878  LOAD_CONST               400
             2880  CALL_METHOD_1         1  '1 positional argument'
             2882  POP_TOP          

 L. 740      2884  LOAD_GLOBAL              ml_wdcnn15d
             2886  LOAD_ATTR                create15DWDCNNSegmentor
             2888  LOAD_FAST                '_traindict'

 L. 741      2890  LOAD_FAST                '_image_height_new'
             2892  LOAD_FAST                '_image_width_new'

 L. 742      2894  LOAD_FAST                '_features'
             2896  LOAD_FAST                '_target'
             2898  LOAD_FAST                '_weight'

 L. 743      2900  LOAD_FAST                '_nepoch'
             2902  LOAD_FAST                '_batchsize'

 L. 744      2904  LOAD_FAST                '_nconvblock'
             2906  LOAD_FAST                '_nconvfeature'

 L. 745      2908  LOAD_FAST                '_nconvlayer'

 L. 746      2910  LOAD_FAST                '_n1x1layer'
             2912  LOAD_FAST                '_n1x1feature'

 L. 747      2914  LOAD_FAST                '_patch_height'
             2916  LOAD_FAST                '_patch_width'

 L. 748      2918  LOAD_FAST                '_pool_height'
             2920  LOAD_FAST                '_pool_width'

 L. 749      2922  LOAD_FAST                '_learning_rate'

 L. 750      2924  LOAD_FAST                '_dropout_prob'

 L. 751      2926  LOAD_CONST               True

 L. 752      2928  LOAD_FAST                '_savepath'
             2930  LOAD_FAST                '_savename'

 L. 753      2932  LOAD_FAST                '_pgsdlg'
             2934  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'weight', 'nepoch', 'batchsize', 'nconvblock', 'nconvfeature', 'nconvlayer', 'n1x1layer', 'n1x1feature', 'patchheight', 'patchwidth', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprob', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2936  CALL_FUNCTION_KW_23    23  '23 total positional and keyword args'
             2938  STORE_FAST               '_dcnnlog'

 L. 756      2940  LOAD_GLOBAL              QtWidgets
             2942  LOAD_ATTR                QMessageBox
             2944  LOAD_METHOD              information
             2946  LOAD_DEREF               'self'
             2948  LOAD_ATTR                msgbox

 L. 757      2950  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 758      2952  LOAD_STR                 'WDCNN trained successfully'
             2954  CALL_METHOD_3         3  '3 positional arguments'
             2956  POP_TOP          

 L. 760      2958  LOAD_GLOBAL              QtWidgets
             2960  LOAD_ATTR                QMessageBox
             2962  LOAD_METHOD              question
             2964  LOAD_DEREF               'self'
             2966  LOAD_ATTR                msgbox
             2968  LOAD_STR                 'Train 1.5D-WDCNN'
             2970  LOAD_STR                 'View learning matrix?'

 L. 761      2972  LOAD_GLOBAL              QtWidgets
             2974  LOAD_ATTR                QMessageBox
             2976  LOAD_ATTR                Yes
             2978  LOAD_GLOBAL              QtWidgets
             2980  LOAD_ATTR                QMessageBox
             2982  LOAD_ATTR                No
             2984  BINARY_OR        

 L. 762      2986  LOAD_GLOBAL              QtWidgets
             2988  LOAD_ATTR                QMessageBox
             2990  LOAD_ATTR                Yes
             2992  CALL_METHOD_5         5  '5 positional arguments'
             2994  STORE_FAST               'reply'

 L. 764      2996  LOAD_FAST                'reply'
             2998  LOAD_GLOBAL              QtWidgets
             3000  LOAD_ATTR                QMessageBox
             3002  LOAD_ATTR                Yes
             3004  COMPARE_OP               ==
         3006_3008  POP_JUMP_IF_FALSE  3076  'to 3076'

 L. 765      3010  LOAD_GLOBAL              QtWidgets
             3012  LOAD_METHOD              QDialog
             3014  CALL_METHOD_0         0  '0 positional arguments'
             3016  STORE_FAST               '_viewmllearnmat'

 L. 766      3018  LOAD_GLOBAL              gui_viewmllearnmat
             3020  CALL_FUNCTION_0       0  '0 positional arguments'
             3022  STORE_FAST               '_gui'

 L. 767      3024  LOAD_FAST                '_dcnnlog'
             3026  LOAD_STR                 'learning_curve'
             3028  BINARY_SUBSCR    
             3030  LOAD_FAST                '_gui'
             3032  STORE_ATTR               learnmat

 L. 768      3034  LOAD_DEREF               'self'
             3036  LOAD_ATTR                linestyle
             3038  LOAD_FAST                '_gui'
             3040  STORE_ATTR               linestyle

 L. 769      3042  LOAD_DEREF               'self'
             3044  LOAD_ATTR                fontstyle
             3046  LOAD_FAST                '_gui'
             3048  STORE_ATTR               fontstyle

 L. 770      3050  LOAD_FAST                '_gui'
             3052  LOAD_METHOD              setupGUI
             3054  LOAD_FAST                '_viewmllearnmat'
             3056  CALL_METHOD_1         1  '1 positional argument'
             3058  POP_TOP          

 L. 771      3060  LOAD_FAST                '_viewmllearnmat'
             3062  LOAD_METHOD              exec
             3064  CALL_METHOD_0         0  '0 positional arguments'
             3066  POP_TOP          

 L. 772      3068  LOAD_FAST                '_viewmllearnmat'
             3070  LOAD_METHOD              show
             3072  CALL_METHOD_0         0  '0 positional arguments'
             3074  POP_TOP          
           3076_0  COME_FROM          3006  '3006'

Parse error at or near `POP_TOP' instruction at offset 3074

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
    TrainMl15DWdcnnFromScratch = QtWidgets.QWidget()
    gui = trainml15dwdcnnfromscratch()
    gui.setupGUI(TrainMl15DWdcnnFromScratch)
    TrainMl15DWdcnnFromScratch.show()
    sys.exit(app.exec_())