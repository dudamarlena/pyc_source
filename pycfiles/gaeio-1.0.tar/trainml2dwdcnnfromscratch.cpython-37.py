# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml2dwdcnnfromscratch.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 47666 bytes
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
import cognitivegeo.src.ml.wdcnnsegmentor as ml_wdcnn
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml2dwdcnnfromscratch(object):
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
    traindataconfig['RotateFeature_Enabled'] = True
    traindataconfig['RotateFeature_Checked'] = False
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False
    traindataconfig['RemoveZeroWeight_Enabled'] = True
    traindataconfig['RemoveZeroWeight_Checked'] = False

    def setupGUI(self, TrainMl2DWdcnnFromScratch):
        TrainMl2DWdcnnFromScratch.setObjectName('TrainMl2DWdcnnFromScratch')
        TrainMl2DWdcnnFromScratch.setFixedSize(810, 540)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl2DWdcnnFromScratch.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl2DWdcnnFromScratch)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl2DWdcnnFromScratch)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl2DWdcnnFromScratch)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblweight = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblweight.setObjectName('lblweight')
        self.lblweight.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.cbbweight = QtWidgets.QComboBox(TrainMl2DWdcnnFromScratch)
        self.cbbweight.setObjectName('cbbweight')
        self.cbbweight.setGeometry(QtCore.QRect(110, 310, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 50, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 50, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl2DWdcnnFromScratch)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 90, 180, 200))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 50, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 50, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(TrainMl2DWdcnnFromScratch)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 90, 180, 200))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 300, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 300, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 300, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 340, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 340, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 300, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 300, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 300, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 340, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 340, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl2DWdcnnFromScratch)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 360, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 360, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 400, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 400, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 400, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 400, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 440, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 440, 40, 30))
        self.lbldropout = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 440, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 440, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl2DWdcnnFromScratch)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 490, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl2DWdcnnFromScratch)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 490, 180, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl2DWdcnnFromScratch)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 490, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl2DWdcnnFromScratch)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 490, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl2DWdcnnFromScratch)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl2DWdcnnFromScratch.geometry().center().x()
        _center_y = TrainMl2DWdcnnFromScratch.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl2DWdcnnFromScratch)
        QtCore.QMetaObject.connectSlotsByName(TrainMl2DWdcnnFromScratch)

    def retranslateGUI(self, TrainMl2DWdcnnFromScratch):
        self.dialog = TrainMl2DWdcnnFromScratch
        _translate = QtCore.QCoreApplication.translate
        TrainMl2DWdcnnFromScratch.setWindowTitle(_translate('TrainMl2DWdcnnFromScratch', 'Train 2D-WDCNN from scratch'))
        self.lblfeature.setText(_translate('TrainMl2DWdcnnFromScratch', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl2DWdcnnFromScratch', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl2DWdcnnFromScratch', 'Select target:'))
        self.lblweight.setText(_translate('TrainMl2DWdcnnFromScratch', 'Select weight:'))
        self.btnconfigtraindata.setText(_translate('TrainMl2DWdcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('TrainMl2DWdcnnFromScratch', 'Original\nimage\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl2DWdcnnFromScratch', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl2DWdcnnFromScratch', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl2DWdcnnFromScratch', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl2DWdcnnFromScratch', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl2DWdcnnFromScratch', 'Interpolated\nimage\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl2DWdcnnFromScratch', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl2DWdcnnFromScratch', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl2DWdcnnFromScratch', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl2DWdcnnFromScratch', '32'))
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
                    item.setText(_translate('TrainMl2DWdcnnFromScratch', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
            self.cbbweight.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl2DWdcnnFromScratch', 'Specify WDCNN architecture:'))
        self.lblnconvblock.setText(_translate('TrainMl2DWdcnnFromScratch', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl2DWdcnnFromScratch', '3'))
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

        self.lbln1x1layer.setText(_translate('TrainMl2DWdcnnFromScratch', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('TrainMl2DWdcnnFromScratch', '2'))
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.twgn1x1layer.setRowCount(2)
        for _idx in range(int(self.ldtn1x1layer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl2DWdcnnFromScratch', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgn1x1layer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgn1x1layer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl2DWdcnnFromScratch', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl2DWdcnnFromScratch', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl2DWdcnnFromScratch', '3'))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('TrainMl2DWdcnnFromScratch', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl2DWdcnnFromScratch', '3'))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('TrainMl2DWdcnnFromScratch', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl2DWdcnnFromScratch', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl2DWdcnnFromScratch', '2'))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl2DWdcnnFromScratch', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl2DWdcnnFromScratch', '2'))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('TrainMl2DWdcnnFromScratch', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl2DWdcnnFromScratch', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl2DWdcnnFromScratch', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl2DWdcnnFromScratch', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl2DWdcnnFromScratch', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl2DWdcnnFromScratch', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl2DWdcnnFromScratch', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('TrainMl2DWdcnnFromScratch', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('TrainMl2DWdcnnFromScratch', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl2DWdcnnFromScratch', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl2DWdcnnFromScratch', ''))
        self.btnsave.setText(_translate('TrainMl2DWdcnnFromScratch', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl2DWdcnnFromScratch', 'Train 2D-WDCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl2DWdcnnFromScratch)

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
        _file = _dialog.getSaveFileName(None, 'Save WDCNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
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

    def clickBtnTrainMl2DWdcnnFromScratch--- This code section failed: ---

 L. 455         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 457         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 458        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 459        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 460        50  LOAD_STR                 'Train 2D-WDCNN'

 L. 461        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 462        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 464        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_image_height'

 L. 465        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_image_width'

 L. 466        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtnewheight
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_image_height_new'

 L. 467       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewwidth
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_image_width_new'

 L. 468       126  LOAD_FAST                '_image_height'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'
              134  LOAD_FAST                '_image_width'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_TRUE    158  'to 158'

 L. 469       142  LOAD_FAST                '_image_height_new'
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

 L. 470       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 471       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 472       182  LOAD_STR                 'Train 2D-WDCNN'

 L. 473       184  LOAD_STR                 'Non-integer feature size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 474       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 475       194  LOAD_FAST                '_image_height'
              196  LOAD_CONST               2
              198  COMPARE_OP               <
              200  POP_JUMP_IF_TRUE    228  'to 228'
              202  LOAD_FAST                '_image_width'
              204  LOAD_CONST               2
              206  COMPARE_OP               <
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 476       210  LOAD_FAST                '_image_height_new'
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

 L. 477       228  LOAD_GLOBAL              vis_msg
              230  LOAD_ATTR                print
              232  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 478       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 479       252  LOAD_STR                 'Train 2D-WDCNN'

 L. 480       254  LOAD_STR                 'Features are not 2D'
              256  CALL_METHOD_3         3  '3 positional arguments'
              258  POP_TOP          

 L. 481       260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           224  '224'

 L. 483       264  LOAD_CONST               2
              266  LOAD_GLOBAL              int
              268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               2
              272  BINARY_TRUE_DIVIDE
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  BINARY_MULTIPLY  
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  STORE_FAST               '_image_height'

 L. 484       284  LOAD_CONST               2
              286  LOAD_GLOBAL              int
              288  LOAD_FAST                '_image_width'
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BINARY_MULTIPLY  
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               '_image_width'

 L. 486       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                lwgfeature
              308  LOAD_METHOD              selectedItems
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               '_features'

 L. 487       314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainml2dwdcnnfromscratch.clickBtnTrainMl2DWdcnnFromScratch.<locals>.<listcomp>'
              318  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              320  LOAD_FAST                '_features'
              322  GET_ITER         
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               '_features'

 L. 488       328  LOAD_DEREF               'self'
              330  LOAD_ATTR                featurelist
              332  LOAD_DEREF               'self'
              334  LOAD_ATTR                cbbtarget
              336  LOAD_METHOD              currentIndex
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  BINARY_SUBSCR    
              342  STORE_FAST               '_target'

 L. 489       344  LOAD_DEREF               'self'
              346  LOAD_ATTR                featurelist
              348  LOAD_DEREF               'self'
              350  LOAD_ATTR                cbbweight
              352  LOAD_METHOD              currentIndex
              354  CALL_METHOD_0         0  '0 positional arguments'
              356  BINARY_SUBSCR    
              358  STORE_FAST               '_weight'

 L. 491       360  LOAD_FAST                '_target'
              362  LOAD_FAST                '_features'
              364  COMPARE_OP               in
          366_368  POP_JUMP_IF_FALSE   406  'to 406'

 L. 492       370  LOAD_GLOBAL              vis_msg
              372  LOAD_ATTR                print
              374  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Target also used as features'
              376  LOAD_STR                 'error'
              378  LOAD_CONST               ('type',)
              380  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              382  POP_TOP          

 L. 493       384  LOAD_GLOBAL              QtWidgets
              386  LOAD_ATTR                QMessageBox
              388  LOAD_METHOD              critical
              390  LOAD_DEREF               'self'
              392  LOAD_ATTR                msgbox

 L. 494       394  LOAD_STR                 'Train 2D-DCNN'

 L. 495       396  LOAD_STR                 'Target also used as features'
              398  CALL_METHOD_3         3  '3 positional arguments'
              400  POP_TOP          

 L. 496       402  LOAD_CONST               None
              404  RETURN_VALUE     
            406_0  COME_FROM           366  '366'

 L. 498       406  LOAD_FAST                '_weight'
              408  LOAD_FAST                '_features'
              410  COMPARE_OP               in
          412_414  POP_JUMP_IF_FALSE   452  'to 452'

 L. 499       416  LOAD_GLOBAL              vis_msg
              418  LOAD_ATTR                print
              420  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Weight also used as features'
              422  LOAD_STR                 'error'
              424  LOAD_CONST               ('type',)
              426  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              428  POP_TOP          

 L. 500       430  LOAD_GLOBAL              QtWidgets
              432  LOAD_ATTR                QMessageBox
              434  LOAD_METHOD              critical
              436  LOAD_DEREF               'self'
              438  LOAD_ATTR                msgbox

 L. 501       440  LOAD_STR                 'Train 2D-WDCNN'

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
              474  LOAD_STR                 'trainml2dwdcnnfromscratch.clickBtnTrainMl2DWdcnnFromScratch.<locals>.<listcomp>'
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
              496  LOAD_STR                 'trainml2dwdcnnfromscratch.clickBtnTrainMl2DWdcnnFromScratch.<locals>.<listcomp>'
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
              534  LOAD_STR                 'trainml2dwdcnnfromscratch.clickBtnTrainMl2DWdcnnFromScratch.<locals>.<listcomp>'
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
              702  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Non-positive convolutional block number'

 L. 520       704  LOAD_STR                 'error'
              706  LOAD_CONST               ('type',)
              708  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              710  POP_TOP          

 L. 521       712  LOAD_GLOBAL              QtWidgets
              714  LOAD_ATTR                QMessageBox
              716  LOAD_METHOD              critical
              718  LOAD_DEREF               'self'
              720  LOAD_ATTR                msgbox

 L. 522       722  LOAD_STR                 'Train 2D-WDCNN'

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
              768  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Non-positive convolutional layer number'

 L. 528       770  LOAD_STR                 'error'
              772  LOAD_CONST               ('type',)
              774  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              776  POP_TOP          

 L. 529       778  LOAD_GLOBAL              QtWidgets
              780  LOAD_ATTR                QMessageBox
              782  LOAD_METHOD              critical
              784  LOAD_DEREF               'self'
              786  LOAD_ATTR                msgbox

 L. 530       788  LOAD_STR                 'Train 2D-WDCNN'

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
              840  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Non-positive convolutional feature number'

 L. 536       842  LOAD_STR                 'error'
              844  LOAD_CONST               ('type',)
              846  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              848  POP_TOP          

 L. 537       850  LOAD_GLOBAL              QtWidgets
              852  LOAD_ATTR                QMessageBox
              854  LOAD_METHOD              critical
              856  LOAD_DEREF               'self'
              858  LOAD_ATTR                msgbox

 L. 538       860  LOAD_STR                 'Train 2D-WDCNN'

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
              902  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Non-positive 1x1 convolutional layer number'

 L. 543       904  LOAD_STR                 'error'
              906  LOAD_CONST               ('type',)
              908  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              910  POP_TOP          

 L. 544       912  LOAD_GLOBAL              QtWidgets
              914  LOAD_ATTR                QMessageBox
              916  LOAD_METHOD              critical
              918  LOAD_DEREF               'self'
              920  LOAD_ATTR                msgbox

 L. 545       922  LOAD_STR                 'Train 2D-WDCNN'

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
              968  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Non-positive 1x1 convolutional feature number'

 L. 551       970  LOAD_STR                 'error'
              972  LOAD_CONST               ('type',)
              974  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              976  POP_TOP          

 L. 552       978  LOAD_GLOBAL              QtWidgets
              980  LOAD_ATTR                QMessageBox
              982  LOAD_METHOD              critical
              984  LOAD_DEREF               'self'
              986  LOAD_ATTR                msgbox

 L. 553       988  LOAD_STR                 'Train 2D-WDCNN'

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
             1050  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Non-positive convolutional patch size'
             1052  LOAD_STR                 'error'
             1054  LOAD_CONST               ('type',)
             1056  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1058  POP_TOP          

 L. 559      1060  LOAD_GLOBAL              QtWidgets
             1062  LOAD_ATTR                QMessageBox
             1064  LOAD_METHOD              critical
             1066  LOAD_DEREF               'self'
             1068  LOAD_ATTR                msgbox

 L. 560      1070  LOAD_STR                 'Train 2D-WDCNN'

 L. 561      1072  LOAD_STR                 'Non-positive convolutional patch size'
             1074  CALL_METHOD_3         3  '3 positional arguments'
             1076  POP_TOP          

 L. 562      1078  LOAD_CONST               None
             1080  RETURN_VALUE     
           1082_0  COME_FROM          1042  '1042'

 L. 563      1082  LOAD_FAST                '_pool_height'
             1084  LOAD_CONST               False
             1086  COMPARE_OP               is
         1088_1090  POP_JUMP_IF_TRUE   1122  'to 1122'
             1092  LOAD_FAST                '_pool_width'
             1094  LOAD_CONST               False
             1096  COMPARE_OP               is
         1098_1100  POP_JUMP_IF_TRUE   1122  'to 1122'

 L. 564      1102  LOAD_FAST                '_pool_height'
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

 L. 565      1122  LOAD_GLOBAL              vis_msg
             1124  LOAD_ATTR                print
             1126  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Non-positive pooling size'
             1128  LOAD_STR                 'error'
             1130  LOAD_CONST               ('type',)
             1132  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1134  POP_TOP          

 L. 566      1136  LOAD_GLOBAL              QtWidgets
             1138  LOAD_ATTR                QMessageBox
             1140  LOAD_METHOD              critical
             1142  LOAD_DEREF               'self'
             1144  LOAD_ATTR                msgbox

 L. 567      1146  LOAD_STR                 'Train 2D-WDCNN'

 L. 568      1148  LOAD_STR                 'Non-positive pooling size'
             1150  CALL_METHOD_3         3  '3 positional arguments'
             1152  POP_TOP          

 L. 569      1154  LOAD_CONST               None
             1156  RETURN_VALUE     
           1158_0  COME_FROM          1118  '1118'

 L. 570      1158  LOAD_FAST                '_nepoch'
             1160  LOAD_CONST               False
             1162  COMPARE_OP               is
         1164_1166  POP_JUMP_IF_TRUE   1178  'to 1178'
             1168  LOAD_FAST                '_nepoch'
             1170  LOAD_CONST               0
             1172  COMPARE_OP               <=
         1174_1176  POP_JUMP_IF_FALSE  1214  'to 1214'
           1178_0  COME_FROM          1164  '1164'

 L. 571      1178  LOAD_GLOBAL              vis_msg
             1180  LOAD_ATTR                print
             1182  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Non-positive epoch number'
             1184  LOAD_STR                 'error'
             1186  LOAD_CONST               ('type',)
             1188  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1190  POP_TOP          

 L. 572      1192  LOAD_GLOBAL              QtWidgets
             1194  LOAD_ATTR                QMessageBox
             1196  LOAD_METHOD              critical
             1198  LOAD_DEREF               'self'
             1200  LOAD_ATTR                msgbox

 L. 573      1202  LOAD_STR                 'Train 2D-WDCNN'

 L. 574      1204  LOAD_STR                 'Non-positive epoch number'
             1206  CALL_METHOD_3         3  '3 positional arguments'
             1208  POP_TOP          

 L. 575      1210  LOAD_CONST               None
             1212  RETURN_VALUE     
           1214_0  COME_FROM          1174  '1174'

 L. 576      1214  LOAD_FAST                '_batchsize'
             1216  LOAD_CONST               False
             1218  COMPARE_OP               is
         1220_1222  POP_JUMP_IF_TRUE   1234  'to 1234'
             1224  LOAD_FAST                '_batchsize'
             1226  LOAD_CONST               0
             1228  COMPARE_OP               <=
         1230_1232  POP_JUMP_IF_FALSE  1270  'to 1270'
           1234_0  COME_FROM          1220  '1220'

 L. 577      1234  LOAD_GLOBAL              vis_msg
             1236  LOAD_ATTR                print
             1238  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Non-positive batch size'
             1240  LOAD_STR                 'error'
             1242  LOAD_CONST               ('type',)
             1244  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1246  POP_TOP          

 L. 578      1248  LOAD_GLOBAL              QtWidgets
             1250  LOAD_ATTR                QMessageBox
             1252  LOAD_METHOD              critical
             1254  LOAD_DEREF               'self'
             1256  LOAD_ATTR                msgbox

 L. 579      1258  LOAD_STR                 'Train 2D-WDCNN'

 L. 580      1260  LOAD_STR                 'Non-positive batch size'
             1262  CALL_METHOD_3         3  '3 positional arguments'
             1264  POP_TOP          

 L. 581      1266  LOAD_CONST               None
             1268  RETURN_VALUE     
           1270_0  COME_FROM          1230  '1230'

 L. 582      1270  LOAD_FAST                '_learning_rate'
             1272  LOAD_CONST               False
             1274  COMPARE_OP               is
         1276_1278  POP_JUMP_IF_TRUE   1290  'to 1290'
             1280  LOAD_FAST                '_learning_rate'
             1282  LOAD_CONST               0
             1284  COMPARE_OP               <=
         1286_1288  POP_JUMP_IF_FALSE  1326  'to 1326'
           1290_0  COME_FROM          1276  '1276'

 L. 583      1290  LOAD_GLOBAL              vis_msg
             1292  LOAD_ATTR                print
             1294  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Non-positive learning rate'
             1296  LOAD_STR                 'error'
             1298  LOAD_CONST               ('type',)
             1300  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1302  POP_TOP          

 L. 584      1304  LOAD_GLOBAL              QtWidgets
             1306  LOAD_ATTR                QMessageBox
             1308  LOAD_METHOD              critical
             1310  LOAD_DEREF               'self'
             1312  LOAD_ATTR                msgbox

 L. 585      1314  LOAD_STR                 'Train 2D-WDCNN'

 L. 586      1316  LOAD_STR                 'Non-positive learning rate'
             1318  CALL_METHOD_3         3  '3 positional arguments'
             1320  POP_TOP          

 L. 587      1322  LOAD_CONST               None
             1324  RETURN_VALUE     
           1326_0  COME_FROM          1286  '1286'

 L. 588      1326  LOAD_FAST                '_dropout_prob'
             1328  LOAD_CONST               False
             1330  COMPARE_OP               is
         1332_1334  POP_JUMP_IF_TRUE   1346  'to 1346'
             1336  LOAD_FAST                '_dropout_prob'
             1338  LOAD_CONST               0
             1340  COMPARE_OP               <=
         1342_1344  POP_JUMP_IF_FALSE  1382  'to 1382'
           1346_0  COME_FROM          1332  '1332'

 L. 589      1346  LOAD_GLOBAL              vis_msg
             1348  LOAD_ATTR                print
             1350  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Negative dropout rate'
             1352  LOAD_STR                 'error'
             1354  LOAD_CONST               ('type',)
             1356  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1358  POP_TOP          

 L. 590      1360  LOAD_GLOBAL              QtWidgets
             1362  LOAD_ATTR                QMessageBox
             1364  LOAD_METHOD              critical
             1366  LOAD_DEREF               'self'
             1368  LOAD_ATTR                msgbox

 L. 591      1370  LOAD_STR                 'Train 2D-WDCNN'

 L. 592      1372  LOAD_STR                 'Negative dropout rate'
             1374  CALL_METHOD_3         3  '3 positional arguments'
             1376  POP_TOP          

 L. 593      1378  LOAD_CONST               None
             1380  RETURN_VALUE     
           1382_0  COME_FROM          1342  '1342'

 L. 595      1382  LOAD_GLOBAL              len
             1384  LOAD_DEREF               'self'
             1386  LOAD_ATTR                ldtsave
             1388  LOAD_METHOD              text
             1390  CALL_METHOD_0         0  '0 positional arguments'
             1392  CALL_FUNCTION_1       1  '1 positional argument'
             1394  LOAD_CONST               1
             1396  COMPARE_OP               <
         1398_1400  POP_JUMP_IF_FALSE  1438  'to 1438'

 L. 596      1402  LOAD_GLOBAL              vis_msg
             1404  LOAD_ATTR                print
             1406  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: No name specified for new-WDCNN'
             1408  LOAD_STR                 'error'
             1410  LOAD_CONST               ('type',)
             1412  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1414  POP_TOP          

 L. 597      1416  LOAD_GLOBAL              QtWidgets
             1418  LOAD_ATTR                QMessageBox
             1420  LOAD_METHOD              critical
             1422  LOAD_DEREF               'self'
             1424  LOAD_ATTR                msgbox

 L. 598      1426  LOAD_STR                 'Train 2D-WDCNN'

 L. 599      1428  LOAD_STR                 'No name specified for new-WDCNN'
             1430  CALL_METHOD_3         3  '3 positional arguments'
             1432  POP_TOP          

 L. 600      1434  LOAD_CONST               None
             1436  RETURN_VALUE     
           1438_0  COME_FROM          1398  '1398'

 L. 601      1438  LOAD_GLOBAL              os
             1440  LOAD_ATTR                path
             1442  LOAD_METHOD              dirname
             1444  LOAD_DEREF               'self'
             1446  LOAD_ATTR                ldtsave
             1448  LOAD_METHOD              text
             1450  CALL_METHOD_0         0  '0 positional arguments'
             1452  CALL_METHOD_1         1  '1 positional argument'
             1454  STORE_FAST               '_savepath'

 L. 602      1456  LOAD_GLOBAL              os
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

 L. 604      1486  LOAD_CONST               0
             1488  STORE_FAST               '_wdinl'

 L. 605      1490  LOAD_CONST               0
             1492  STORE_FAST               '_wdxl'

 L. 606      1494  LOAD_CONST               0
             1496  STORE_FAST               '_wdz'

 L. 607      1498  LOAD_DEREF               'self'
             1500  LOAD_ATTR                cbbornt
             1502  LOAD_METHOD              currentIndex
             1504  CALL_METHOD_0         0  '0 positional arguments'
             1506  LOAD_CONST               0
             1508  COMPARE_OP               ==
         1510_1512  POP_JUMP_IF_FALSE  1538  'to 1538'

 L. 608      1514  LOAD_GLOBAL              int
             1516  LOAD_FAST                '_image_width'
             1518  LOAD_CONST               2
             1520  BINARY_TRUE_DIVIDE
             1522  CALL_FUNCTION_1       1  '1 positional argument'
             1524  STORE_FAST               '_wdxl'

 L. 609      1526  LOAD_GLOBAL              int
             1528  LOAD_FAST                '_image_height'
             1530  LOAD_CONST               2
             1532  BINARY_TRUE_DIVIDE
             1534  CALL_FUNCTION_1       1  '1 positional argument'
             1536  STORE_FAST               '_wdz'
           1538_0  COME_FROM          1510  '1510'

 L. 610      1538  LOAD_DEREF               'self'
             1540  LOAD_ATTR                cbbornt
             1542  LOAD_METHOD              currentIndex
             1544  CALL_METHOD_0         0  '0 positional arguments'
             1546  LOAD_CONST               1
             1548  COMPARE_OP               ==
         1550_1552  POP_JUMP_IF_FALSE  1578  'to 1578'

 L. 611      1554  LOAD_GLOBAL              int
             1556  LOAD_FAST                '_image_width'
             1558  LOAD_CONST               2
             1560  BINARY_TRUE_DIVIDE
             1562  CALL_FUNCTION_1       1  '1 positional argument'
             1564  STORE_FAST               '_wdinl'

 L. 612      1566  LOAD_GLOBAL              int
             1568  LOAD_FAST                '_image_height'
             1570  LOAD_CONST               2
             1572  BINARY_TRUE_DIVIDE
             1574  CALL_FUNCTION_1       1  '1 positional argument'
             1576  STORE_FAST               '_wdz'
           1578_0  COME_FROM          1550  '1550'

 L. 613      1578  LOAD_DEREF               'self'
             1580  LOAD_ATTR                cbbornt
             1582  LOAD_METHOD              currentIndex
             1584  CALL_METHOD_0         0  '0 positional arguments'
             1586  LOAD_CONST               2
             1588  COMPARE_OP               ==
         1590_1592  POP_JUMP_IF_FALSE  1618  'to 1618'

 L. 614      1594  LOAD_GLOBAL              int
             1596  LOAD_FAST                '_image_width'
             1598  LOAD_CONST               2
             1600  BINARY_TRUE_DIVIDE
             1602  CALL_FUNCTION_1       1  '1 positional argument'
             1604  STORE_FAST               '_wdinl'

 L. 615      1606  LOAD_GLOBAL              int
             1608  LOAD_FAST                '_image_height'
             1610  LOAD_CONST               2
             1612  BINARY_TRUE_DIVIDE
             1614  CALL_FUNCTION_1       1  '1 positional argument'
             1616  STORE_FAST               '_wdxl'
           1618_0  COME_FROM          1590  '1590'

 L. 617      1618  LOAD_DEREF               'self'
             1620  LOAD_ATTR                survinfo
             1622  STORE_FAST               '_seisinfo'

 L. 619      1624  LOAD_GLOBAL              print
             1626  LOAD_STR                 'TrainMl2DWdcnnFromScratch: Step 1 - Get training samples:'
             1628  CALL_FUNCTION_1       1  '1 positional argument'
             1630  POP_TOP          

 L. 620      1632  LOAD_DEREF               'self'
             1634  LOAD_ATTR                traindataconfig
             1636  LOAD_STR                 'TrainPointSet'
             1638  BINARY_SUBSCR    
             1640  STORE_FAST               '_trainpoint'

 L. 621      1642  LOAD_GLOBAL              np
             1644  LOAD_METHOD              zeros
             1646  LOAD_CONST               0
             1648  LOAD_CONST               3
             1650  BUILD_LIST_2          2 
             1652  CALL_METHOD_1         1  '1 positional argument'
             1654  STORE_FAST               '_traindata'

 L. 622      1656  SETUP_LOOP         1732  'to 1732'
             1658  LOAD_FAST                '_trainpoint'
             1660  GET_ITER         
           1662_0  COME_FROM          1680  '1680'
             1662  FOR_ITER           1730  'to 1730'
             1664  STORE_FAST               '_p'

 L. 623      1666  LOAD_GLOBAL              point_ays
             1668  LOAD_METHOD              checkPoint
             1670  LOAD_DEREF               'self'
             1672  LOAD_ATTR                pointsetdata
             1674  LOAD_FAST                '_p'
             1676  BINARY_SUBSCR    
             1678  CALL_METHOD_1         1  '1 positional argument'
         1680_1682  POP_JUMP_IF_FALSE  1662  'to 1662'

 L. 624      1684  LOAD_GLOBAL              basic_mdt
             1686  LOAD_METHOD              exportMatDict
             1688  LOAD_DEREF               'self'
             1690  LOAD_ATTR                pointsetdata
             1692  LOAD_FAST                '_p'
             1694  BINARY_SUBSCR    
             1696  LOAD_STR                 'Inline'
             1698  LOAD_STR                 'Crossline'
             1700  LOAD_STR                 'Z'
             1702  BUILD_LIST_3          3 
             1704  CALL_METHOD_2         2  '2 positional arguments'
             1706  STORE_FAST               '_pt'

 L. 625      1708  LOAD_GLOBAL              np
             1710  LOAD_ATTR                concatenate
             1712  LOAD_FAST                '_traindata'
             1714  LOAD_FAST                '_pt'
             1716  BUILD_TUPLE_2         2 
             1718  LOAD_CONST               0
             1720  LOAD_CONST               ('axis',)
             1722  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1724  STORE_FAST               '_traindata'
         1726_1728  JUMP_BACK          1662  'to 1662'
             1730  POP_BLOCK        
           1732_0  COME_FROM_LOOP     1656  '1656'

 L. 626      1732  LOAD_GLOBAL              seis_ays
             1734  LOAD_ATTR                removeOutofSurveySample
             1736  LOAD_FAST                '_traindata'

 L. 627      1738  LOAD_FAST                '_seisinfo'
             1740  LOAD_STR                 'ILStart'
             1742  BINARY_SUBSCR    
             1744  LOAD_FAST                '_wdinl'
             1746  LOAD_FAST                '_seisinfo'
             1748  LOAD_STR                 'ILStep'
             1750  BINARY_SUBSCR    
             1752  BINARY_MULTIPLY  
             1754  BINARY_ADD       

 L. 628      1756  LOAD_FAST                '_seisinfo'
             1758  LOAD_STR                 'ILEnd'
             1760  BINARY_SUBSCR    
             1762  LOAD_FAST                '_wdinl'
             1764  LOAD_FAST                '_seisinfo'
             1766  LOAD_STR                 'ILStep'
             1768  BINARY_SUBSCR    
             1770  BINARY_MULTIPLY  
             1772  BINARY_SUBTRACT  

 L. 629      1774  LOAD_FAST                '_seisinfo'
             1776  LOAD_STR                 'XLStart'
             1778  BINARY_SUBSCR    
             1780  LOAD_FAST                '_wdxl'
             1782  LOAD_FAST                '_seisinfo'
             1784  LOAD_STR                 'XLStep'
             1786  BINARY_SUBSCR    
             1788  BINARY_MULTIPLY  
             1790  BINARY_ADD       

 L. 630      1792  LOAD_FAST                '_seisinfo'
             1794  LOAD_STR                 'XLEnd'
             1796  BINARY_SUBSCR    
             1798  LOAD_FAST                '_wdxl'
             1800  LOAD_FAST                '_seisinfo'
             1802  LOAD_STR                 'XLStep'
             1804  BINARY_SUBSCR    
             1806  BINARY_MULTIPLY  
             1808  BINARY_SUBTRACT  

 L. 631      1810  LOAD_FAST                '_seisinfo'
             1812  LOAD_STR                 'ZStart'
             1814  BINARY_SUBSCR    
             1816  LOAD_FAST                '_wdz'
             1818  LOAD_FAST                '_seisinfo'
             1820  LOAD_STR                 'ZStep'
             1822  BINARY_SUBSCR    
             1824  BINARY_MULTIPLY  
             1826  BINARY_ADD       

 L. 632      1828  LOAD_FAST                '_seisinfo'
             1830  LOAD_STR                 'ZEnd'
             1832  BINARY_SUBSCR    
             1834  LOAD_FAST                '_wdz'
             1836  LOAD_FAST                '_seisinfo'
             1838  LOAD_STR                 'ZStep'
             1840  BINARY_SUBSCR    
             1842  BINARY_MULTIPLY  
             1844  BINARY_SUBTRACT  
             1846  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1848  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1850  STORE_FAST               '_traindata'

 L. 634      1852  LOAD_GLOBAL              np
             1854  LOAD_METHOD              shape
             1856  LOAD_FAST                '_traindata'
             1858  CALL_METHOD_1         1  '1 positional argument'
             1860  LOAD_CONST               0
             1862  BINARY_SUBSCR    
             1864  LOAD_CONST               0
             1866  COMPARE_OP               <=
         1868_1870  POP_JUMP_IF_FALSE  1908  'to 1908'

 L. 635      1872  LOAD_GLOBAL              vis_msg
             1874  LOAD_ATTR                print
             1876  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: No training sample found'
             1878  LOAD_STR                 'error'
             1880  LOAD_CONST               ('type',)
             1882  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1884  POP_TOP          

 L. 636      1886  LOAD_GLOBAL              QtWidgets
             1888  LOAD_ATTR                QMessageBox
             1890  LOAD_METHOD              critical
             1892  LOAD_DEREF               'self'
             1894  LOAD_ATTR                msgbox

 L. 637      1896  LOAD_STR                 'Train 2D-WDCNN'

 L. 638      1898  LOAD_STR                 'No training sample found'
             1900  CALL_METHOD_3         3  '3 positional arguments'
             1902  POP_TOP          

 L. 639      1904  LOAD_CONST               None
             1906  RETURN_VALUE     
           1908_0  COME_FROM          1868  '1868'

 L. 642      1908  LOAD_GLOBAL              print
             1910  LOAD_STR                 'TrainMl2DWdcnnFromScratch: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 643      1912  LOAD_FAST                '_image_height'
             1914  LOAD_FAST                '_image_width'
             1916  LOAD_FAST                '_image_height_new'
             1918  LOAD_FAST                '_image_width_new'
             1920  BUILD_TUPLE_4         4 
             1922  BINARY_MODULO    
             1924  CALL_FUNCTION_1       1  '1 positional argument'
             1926  POP_TOP          

 L. 644      1928  BUILD_MAP_0           0 
             1930  STORE_FAST               '_traindict'

 L. 645      1932  SETUP_LOOP         2004  'to 2004'
             1934  LOAD_FAST                '_features'
             1936  GET_ITER         
             1938  FOR_ITER           2002  'to 2002'
             1940  STORE_FAST               'f'

 L. 646      1942  LOAD_DEREF               'self'
             1944  LOAD_ATTR                seisdata
             1946  LOAD_FAST                'f'
             1948  BINARY_SUBSCR    
             1950  STORE_FAST               '_seisdata'

 L. 647      1952  LOAD_GLOBAL              seis_ays
             1954  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1956  LOAD_FAST                '_seisdata'
             1958  LOAD_FAST                '_traindata'
             1960  LOAD_DEREF               'self'
             1962  LOAD_ATTR                survinfo

 L. 648      1964  LOAD_FAST                '_wdinl'
             1966  LOAD_FAST                '_wdxl'
             1968  LOAD_FAST                '_wdz'

 L. 649      1970  LOAD_CONST               False
             1972  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1974  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1976  LOAD_CONST               None
             1978  LOAD_CONST               None
             1980  BUILD_SLICE_2         2 
             1982  LOAD_CONST               3
             1984  LOAD_CONST               None
             1986  BUILD_SLICE_2         2 
             1988  BUILD_TUPLE_2         2 
             1990  BINARY_SUBSCR    
             1992  LOAD_FAST                '_traindict'
             1994  LOAD_FAST                'f'
             1996  STORE_SUBSCR     
         1998_2000  JUMP_BACK          1938  'to 1938'
             2002  POP_BLOCK        
           2004_0  COME_FROM_LOOP     1932  '1932'

 L. 650      2004  LOAD_FAST                '_target'
             2006  LOAD_FAST                '_features'
             2008  COMPARE_OP               not-in
         2010_2012  POP_JUMP_IF_FALSE  2070  'to 2070'

 L. 651      2014  LOAD_DEREF               'self'
             2016  LOAD_ATTR                seisdata
             2018  LOAD_FAST                '_target'
             2020  BINARY_SUBSCR    
             2022  STORE_FAST               '_seisdata'

 L. 652      2024  LOAD_GLOBAL              seis_ays
             2026  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2028  LOAD_FAST                '_seisdata'
             2030  LOAD_FAST                '_traindata'
             2032  LOAD_DEREF               'self'
             2034  LOAD_ATTR                survinfo

 L. 653      2036  LOAD_FAST                '_wdinl'

 L. 654      2038  LOAD_FAST                '_wdxl'

 L. 655      2040  LOAD_FAST                '_wdz'

 L. 656      2042  LOAD_CONST               False
             2044  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2046  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2048  LOAD_CONST               None
             2050  LOAD_CONST               None
             2052  BUILD_SLICE_2         2 
             2054  LOAD_CONST               3
             2056  LOAD_CONST               None
             2058  BUILD_SLICE_2         2 
             2060  BUILD_TUPLE_2         2 
             2062  BINARY_SUBSCR    
             2064  LOAD_FAST                '_traindict'
             2066  LOAD_FAST                '_target'
             2068  STORE_SUBSCR     
           2070_0  COME_FROM          2010  '2010'

 L. 657      2070  LOAD_FAST                '_weight'
             2072  LOAD_FAST                '_features'
             2074  COMPARE_OP               not-in
         2076_2078  POP_JUMP_IF_FALSE  2146  'to 2146'
             2080  LOAD_FAST                '_weight'
             2082  LOAD_FAST                '_target'
             2084  COMPARE_OP               !=
         2086_2088  POP_JUMP_IF_FALSE  2146  'to 2146'

 L. 658      2090  LOAD_DEREF               'self'
             2092  LOAD_ATTR                seisdata
             2094  LOAD_FAST                '_weight'
             2096  BINARY_SUBSCR    
             2098  STORE_FAST               '_seisdata'

 L. 659      2100  LOAD_GLOBAL              seis_ays
             2102  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2104  LOAD_FAST                '_seisdata'
             2106  LOAD_FAST                '_traindata'
             2108  LOAD_DEREF               'self'
             2110  LOAD_ATTR                survinfo

 L. 660      2112  LOAD_FAST                '_wdinl'

 L. 661      2114  LOAD_FAST                '_wdxl'

 L. 662      2116  LOAD_FAST                '_wdz'

 L. 663      2118  LOAD_CONST               False
             2120  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2122  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2124  LOAD_CONST               None
             2126  LOAD_CONST               None
             2128  BUILD_SLICE_2         2 
             2130  LOAD_CONST               3
             2132  LOAD_CONST               None
             2134  BUILD_SLICE_2         2 
             2136  BUILD_TUPLE_2         2 
             2138  BINARY_SUBSCR    
             2140  LOAD_FAST                '_traindict'
             2142  LOAD_FAST                '_weight'
             2144  STORE_SUBSCR     
           2146_0  COME_FROM          2086  '2086'
           2146_1  COME_FROM          2076  '2076'

 L. 665      2146  LOAD_DEREF               'self'
             2148  LOAD_ATTR                traindataconfig
             2150  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2152  BINARY_SUBSCR    
         2154_2156  POP_JUMP_IF_FALSE  2238  'to 2238'

 L. 666      2158  SETUP_LOOP         2238  'to 2238'
             2160  LOAD_FAST                '_features'
             2162  GET_ITER         
           2164_0  COME_FROM          2192  '2192'
             2164  FOR_ITER           2236  'to 2236'
             2166  STORE_FAST               'f'

 L. 667      2168  LOAD_GLOBAL              ml_aug
             2170  LOAD_METHOD              removeInvariantFeature
             2172  LOAD_FAST                '_traindict'
             2174  LOAD_FAST                'f'
             2176  CALL_METHOD_2         2  '2 positional arguments'
             2178  STORE_FAST               '_traindict'

 L. 668      2180  LOAD_GLOBAL              basic_mdt
             2182  LOAD_METHOD              maxDictConstantRow
             2184  LOAD_FAST                '_traindict'
             2186  CALL_METHOD_1         1  '1 positional argument'
             2188  LOAD_CONST               0
             2190  COMPARE_OP               <=
         2192_2194  POP_JUMP_IF_FALSE  2164  'to 2164'

 L. 669      2196  LOAD_GLOBAL              vis_msg
             2198  LOAD_ATTR                print
             2200  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: No training sample found'
             2202  LOAD_STR                 'error'
             2204  LOAD_CONST               ('type',)
             2206  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2208  POP_TOP          

 L. 670      2210  LOAD_GLOBAL              QtWidgets
             2212  LOAD_ATTR                QMessageBox
             2214  LOAD_METHOD              critical
             2216  LOAD_DEREF               'self'
             2218  LOAD_ATTR                msgbox

 L. 671      2220  LOAD_STR                 'Train 2D-WDCNN'

 L. 672      2222  LOAD_STR                 'No training sample found'
             2224  CALL_METHOD_3         3  '3 positional arguments'
             2226  POP_TOP          

 L. 673      2228  LOAD_CONST               None
             2230  RETURN_VALUE     
         2232_2234  JUMP_BACK          2164  'to 2164'
             2236  POP_BLOCK        
           2238_0  COME_FROM_LOOP     2158  '2158'
           2238_1  COME_FROM          2154  '2154'

 L. 674      2238  LOAD_DEREF               'self'
             2240  LOAD_ATTR                traindataconfig
             2242  LOAD_STR                 'RemoveZeroWeight_Checked'
             2244  BINARY_SUBSCR    
         2246_2248  POP_JUMP_IF_FALSE  2314  'to 2314'

 L. 675      2250  LOAD_GLOBAL              ml_aug
             2252  LOAD_METHOD              removeZeroWeight
             2254  LOAD_FAST                '_traindict'
             2256  LOAD_FAST                '_weight'
             2258  CALL_METHOD_2         2  '2 positional arguments'
             2260  STORE_FAST               '_traindict'

 L. 676      2262  LOAD_GLOBAL              basic_mdt
             2264  LOAD_METHOD              maxDictConstantRow
             2266  LOAD_FAST                '_traindict'
             2268  CALL_METHOD_1         1  '1 positional argument'
             2270  LOAD_CONST               0
             2272  COMPARE_OP               <=
         2274_2276  POP_JUMP_IF_FALSE  2314  'to 2314'

 L. 677      2278  LOAD_GLOBAL              vis_msg
             2280  LOAD_ATTR                print
             2282  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: No training sample found'
             2284  LOAD_STR                 'error'
             2286  LOAD_CONST               ('type',)
             2288  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2290  POP_TOP          

 L. 678      2292  LOAD_GLOBAL              QtWidgets
             2294  LOAD_ATTR                QMessageBox
             2296  LOAD_METHOD              critical
             2298  LOAD_DEREF               'self'
             2300  LOAD_ATTR                msgbox

 L. 679      2302  LOAD_STR                 'Train 2D-WDCNN'

 L. 680      2304  LOAD_STR                 'No training sample found'
             2306  CALL_METHOD_3         3  '3 positional arguments'
             2308  POP_TOP          

 L. 681      2310  LOAD_CONST               None
             2312  RETURN_VALUE     
           2314_0  COME_FROM          2274  '2274'
           2314_1  COME_FROM          2246  '2246'

 L. 683      2314  LOAD_GLOBAL              np
             2316  LOAD_METHOD              shape
             2318  LOAD_FAST                '_traindict'
             2320  LOAD_FAST                '_target'
             2322  BINARY_SUBSCR    
             2324  CALL_METHOD_1         1  '1 positional argument'
             2326  LOAD_CONST               0
             2328  BINARY_SUBSCR    
             2330  LOAD_CONST               0
             2332  COMPARE_OP               <=
         2334_2336  POP_JUMP_IF_FALSE  2374  'to 2374'

 L. 684      2338  LOAD_GLOBAL              vis_msg
             2340  LOAD_ATTR                print
             2342  LOAD_STR                 'ERROR in TrainMl2DDCnnFromScratch: No training sample found'
             2344  LOAD_STR                 'error'
             2346  LOAD_CONST               ('type',)
             2348  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2350  POP_TOP          

 L. 685      2352  LOAD_GLOBAL              QtWidgets
             2354  LOAD_ATTR                QMessageBox
             2356  LOAD_METHOD              critical
             2358  LOAD_DEREF               'self'
             2360  LOAD_ATTR                msgbox

 L. 686      2362  LOAD_STR                 'Train 2D-WDCNN'

 L. 687      2364  LOAD_STR                 'No training sample found'
             2366  CALL_METHOD_3         3  '3 positional arguments'
             2368  POP_TOP          

 L. 688      2370  LOAD_CONST               None
             2372  RETURN_VALUE     
           2374_0  COME_FROM          2334  '2334'

 L. 690      2374  LOAD_FAST                '_image_height_new'
             2376  LOAD_FAST                '_image_height'
             2378  COMPARE_OP               !=
         2380_2382  POP_JUMP_IF_TRUE   2394  'to 2394'
             2384  LOAD_FAST                '_image_width_new'
             2386  LOAD_FAST                '_image_width'
             2388  COMPARE_OP               !=
         2390_2392  POP_JUMP_IF_FALSE  2528  'to 2528'
           2394_0  COME_FROM          2380  '2380'

 L. 691      2394  SETUP_LOOP         2438  'to 2438'
             2396  LOAD_FAST                '_features'
             2398  GET_ITER         
             2400  FOR_ITER           2436  'to 2436'
             2402  STORE_FAST               'f'

 L. 692      2404  LOAD_GLOBAL              basic_image
             2406  LOAD_ATTR                changeImageSize
             2408  LOAD_FAST                '_traindict'
             2410  LOAD_FAST                'f'
             2412  BINARY_SUBSCR    

 L. 693      2414  LOAD_FAST                '_image_height'

 L. 694      2416  LOAD_FAST                '_image_width'

 L. 695      2418  LOAD_FAST                '_image_height_new'

 L. 696      2420  LOAD_FAST                '_image_width_new'
             2422  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2424  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2426  LOAD_FAST                '_traindict'
             2428  LOAD_FAST                'f'
             2430  STORE_SUBSCR     
         2432_2434  JUMP_BACK          2400  'to 2400'
             2436  POP_BLOCK        
           2438_0  COME_FROM_LOOP     2394  '2394'

 L. 697      2438  LOAD_FAST                '_target'
             2440  LOAD_FAST                '_features'
             2442  COMPARE_OP               not-in
         2444_2446  POP_JUMP_IF_FALSE  2478  'to 2478'

 L. 698      2448  LOAD_GLOBAL              basic_image
             2450  LOAD_ATTR                changeImageSize
             2452  LOAD_FAST                '_traindict'
             2454  LOAD_FAST                '_target'
             2456  BINARY_SUBSCR    

 L. 699      2458  LOAD_FAST                '_image_height'

 L. 700      2460  LOAD_FAST                '_image_width'

 L. 701      2462  LOAD_FAST                '_image_height_new'

 L. 702      2464  LOAD_FAST                '_image_width_new'
             2466  LOAD_STR                 'linear'
             2468  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2470  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2472  LOAD_FAST                '_traindict'
             2474  LOAD_FAST                '_target'
             2476  STORE_SUBSCR     
           2478_0  COME_FROM          2444  '2444'

 L. 703      2478  LOAD_FAST                '_weight'
             2480  LOAD_FAST                '_features'
             2482  COMPARE_OP               not-in
         2484_2486  POP_JUMP_IF_FALSE  2528  'to 2528'
             2488  LOAD_FAST                '_weight'
             2490  LOAD_FAST                '_target'
             2492  COMPARE_OP               !=
         2494_2496  POP_JUMP_IF_FALSE  2528  'to 2528'

 L. 704      2498  LOAD_GLOBAL              basic_image
             2500  LOAD_ATTR                changeImageSize
             2502  LOAD_FAST                '_traindict'
             2504  LOAD_FAST                '_weight'
             2506  BINARY_SUBSCR    

 L. 705      2508  LOAD_FAST                '_image_height'

 L. 706      2510  LOAD_FAST                '_image_width'

 L. 707      2512  LOAD_FAST                '_image_height_new'

 L. 708      2514  LOAD_FAST                '_image_width_new'
             2516  LOAD_STR                 'linear'
             2518  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2520  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2522  LOAD_FAST                '_traindict'
             2524  LOAD_FAST                '_weight'
             2526  STORE_SUBSCR     
           2528_0  COME_FROM          2494  '2494'
           2528_1  COME_FROM          2484  '2484'
           2528_2  COME_FROM          2390  '2390'

 L. 709      2528  LOAD_DEREF               'self'
             2530  LOAD_ATTR                traindataconfig
             2532  LOAD_STR                 'RotateFeature_Checked'
             2534  BINARY_SUBSCR    
             2536  LOAD_CONST               True
             2538  COMPARE_OP               is
         2540_2542  POP_JUMP_IF_FALSE  2758  'to 2758'

 L. 710      2544  SETUP_LOOP         2616  'to 2616'
             2546  LOAD_FAST                '_features'
             2548  GET_ITER         
             2550  FOR_ITER           2614  'to 2614'
             2552  STORE_FAST               'f'

 L. 711      2554  LOAD_FAST                '_image_height_new'
             2556  LOAD_FAST                '_image_width_new'
             2558  COMPARE_OP               ==
         2560_2562  POP_JUMP_IF_FALSE  2588  'to 2588'

 L. 712      2564  LOAD_GLOBAL              ml_aug
             2566  LOAD_METHOD              rotateImage6Way
             2568  LOAD_FAST                '_traindict'
             2570  LOAD_FAST                'f'
             2572  BINARY_SUBSCR    
             2574  LOAD_FAST                '_image_height_new'
             2576  LOAD_FAST                '_image_width_new'
             2578  CALL_METHOD_3         3  '3 positional arguments'
             2580  LOAD_FAST                '_traindict'
             2582  LOAD_FAST                'f'
             2584  STORE_SUBSCR     
             2586  JUMP_BACK          2550  'to 2550'
           2588_0  COME_FROM          2560  '2560'

 L. 714      2588  LOAD_GLOBAL              ml_aug
             2590  LOAD_METHOD              rotateImage4Way
             2592  LOAD_FAST                '_traindict'
             2594  LOAD_FAST                'f'
             2596  BINARY_SUBSCR    
             2598  LOAD_FAST                '_image_height_new'
             2600  LOAD_FAST                '_image_width_new'
             2602  CALL_METHOD_3         3  '3 positional arguments'
             2604  LOAD_FAST                '_traindict'
             2606  LOAD_FAST                'f'
             2608  STORE_SUBSCR     
         2610_2612  JUMP_BACK          2550  'to 2550'
             2614  POP_BLOCK        
           2616_0  COME_FROM_LOOP     2544  '2544'

 L. 715      2616  LOAD_FAST                '_target'
             2618  LOAD_FAST                '_features'
             2620  COMPARE_OP               not-in
         2622_2624  POP_JUMP_IF_FALSE  2682  'to 2682'

 L. 716      2626  LOAD_FAST                '_image_height_new'
             2628  LOAD_FAST                '_image_width_new'
             2630  COMPARE_OP               ==
         2632_2634  POP_JUMP_IF_FALSE  2660  'to 2660'

 L. 718      2636  LOAD_GLOBAL              ml_aug
             2638  LOAD_METHOD              rotateImage6Way
             2640  LOAD_FAST                '_traindict'
             2642  LOAD_FAST                '_target'
             2644  BINARY_SUBSCR    
             2646  LOAD_FAST                '_image_height_new'
             2648  LOAD_FAST                '_image_width_new'
             2650  CALL_METHOD_3         3  '3 positional arguments'
             2652  LOAD_FAST                '_traindict'
             2654  LOAD_FAST                '_target'
             2656  STORE_SUBSCR     
             2658  JUMP_FORWARD       2682  'to 2682'
           2660_0  COME_FROM          2632  '2632'

 L. 721      2660  LOAD_GLOBAL              ml_aug
             2662  LOAD_METHOD              rotateImage4Way
             2664  LOAD_FAST                '_traindict'
             2666  LOAD_FAST                '_target'
             2668  BINARY_SUBSCR    
             2670  LOAD_FAST                '_image_height_new'
             2672  LOAD_FAST                '_image_width_new'
             2674  CALL_METHOD_3         3  '3 positional arguments'
             2676  LOAD_FAST                '_traindict'
             2678  LOAD_FAST                '_target'
             2680  STORE_SUBSCR     
           2682_0  COME_FROM          2658  '2658'
           2682_1  COME_FROM          2622  '2622'

 L. 722      2682  LOAD_FAST                '_weight'
             2684  LOAD_FAST                '_features'
             2686  COMPARE_OP               not-in
         2688_2690  POP_JUMP_IF_FALSE  2758  'to 2758'
             2692  LOAD_FAST                '_weight'
             2694  LOAD_FAST                '_target'
             2696  COMPARE_OP               !=
         2698_2700  POP_JUMP_IF_FALSE  2758  'to 2758'

 L. 723      2702  LOAD_FAST                '_image_height_new'
             2704  LOAD_FAST                '_image_width_new'
             2706  COMPARE_OP               ==
         2708_2710  POP_JUMP_IF_FALSE  2736  'to 2736'

 L. 725      2712  LOAD_GLOBAL              ml_aug
             2714  LOAD_METHOD              rotateImage6Way
             2716  LOAD_FAST                '_traindict'
             2718  LOAD_FAST                '_weight'
             2720  BINARY_SUBSCR    
             2722  LOAD_FAST                '_image_height_new'
             2724  LOAD_FAST                '_image_width_new'
             2726  CALL_METHOD_3         3  '3 positional arguments'
             2728  LOAD_FAST                '_traindict'
             2730  LOAD_FAST                '_weight'
             2732  STORE_SUBSCR     
             2734  JUMP_FORWARD       2758  'to 2758'
           2736_0  COME_FROM          2708  '2708'

 L. 728      2736  LOAD_GLOBAL              ml_aug
             2738  LOAD_METHOD              rotateImage4Way
             2740  LOAD_FAST                '_traindict'
             2742  LOAD_FAST                '_weight'
             2744  BINARY_SUBSCR    
             2746  LOAD_FAST                '_image_height_new'
             2748  LOAD_FAST                '_image_width_new'
             2750  CALL_METHOD_3         3  '3 positional arguments'
             2752  LOAD_FAST                '_traindict'
             2754  LOAD_FAST                '_weight'
             2756  STORE_SUBSCR     
           2758_0  COME_FROM          2734  '2734'
           2758_1  COME_FROM          2698  '2698'
           2758_2  COME_FROM          2688  '2688'
           2758_3  COME_FROM          2540  '2540'

 L. 730      2758  LOAD_GLOBAL              np
             2760  LOAD_METHOD              round
             2762  LOAD_FAST                '_traindict'
             2764  LOAD_FAST                '_target'
             2766  BINARY_SUBSCR    
             2768  CALL_METHOD_1         1  '1 positional argument'
             2770  LOAD_METHOD              astype
             2772  LOAD_GLOBAL              int
             2774  CALL_METHOD_1         1  '1 positional argument'
             2776  LOAD_FAST                '_traindict'
             2778  LOAD_FAST                '_target'
             2780  STORE_SUBSCR     

 L. 733      2782  LOAD_GLOBAL              print
             2784  LOAD_STR                 'TrainMl2DWdcnnFromScratch: A total of %d valid training samples'
             2786  LOAD_GLOBAL              basic_mdt
             2788  LOAD_METHOD              maxDictConstantRow

 L. 734      2790  LOAD_FAST                '_traindict'
             2792  CALL_METHOD_1         1  '1 positional argument'
             2794  BINARY_MODULO    
             2796  CALL_FUNCTION_1       1  '1 positional argument'
             2798  POP_TOP          

 L. 736      2800  LOAD_GLOBAL              print
             2802  LOAD_STR                 'TrainMl2DWdcnnFromScratch: Step 3 - Start training'
             2804  CALL_FUNCTION_1       1  '1 positional argument'
             2806  POP_TOP          

 L. 738      2808  LOAD_GLOBAL              QtWidgets
             2810  LOAD_METHOD              QProgressDialog
             2812  CALL_METHOD_0         0  '0 positional arguments'
             2814  STORE_FAST               '_pgsdlg'

 L. 739      2816  LOAD_GLOBAL              QtGui
             2818  LOAD_METHOD              QIcon
             2820  CALL_METHOD_0         0  '0 positional arguments'
             2822  STORE_FAST               'icon'

 L. 740      2824  LOAD_FAST                'icon'
             2826  LOAD_METHOD              addPixmap
             2828  LOAD_GLOBAL              QtGui
             2830  LOAD_METHOD              QPixmap
             2832  LOAD_GLOBAL              os
             2834  LOAD_ATTR                path
             2836  LOAD_METHOD              join
             2838  LOAD_DEREF               'self'
             2840  LOAD_ATTR                iconpath
             2842  LOAD_STR                 'icons/new.png'
             2844  CALL_METHOD_2         2  '2 positional arguments'
             2846  CALL_METHOD_1         1  '1 positional argument'

 L. 741      2848  LOAD_GLOBAL              QtGui
             2850  LOAD_ATTR                QIcon
             2852  LOAD_ATTR                Normal
             2854  LOAD_GLOBAL              QtGui
             2856  LOAD_ATTR                QIcon
             2858  LOAD_ATTR                Off
             2860  CALL_METHOD_3         3  '3 positional arguments'
             2862  POP_TOP          

 L. 742      2864  LOAD_FAST                '_pgsdlg'
             2866  LOAD_METHOD              setWindowIcon
             2868  LOAD_FAST                'icon'
             2870  CALL_METHOD_1         1  '1 positional argument'
             2872  POP_TOP          

 L. 743      2874  LOAD_FAST                '_pgsdlg'
             2876  LOAD_METHOD              setWindowTitle
             2878  LOAD_STR                 'Train 2D-WDCNN'
             2880  CALL_METHOD_1         1  '1 positional argument'
             2882  POP_TOP          

 L. 744      2884  LOAD_FAST                '_pgsdlg'
             2886  LOAD_METHOD              setCancelButton
             2888  LOAD_CONST               None
             2890  CALL_METHOD_1         1  '1 positional argument'
             2892  POP_TOP          

 L. 745      2894  LOAD_FAST                '_pgsdlg'
             2896  LOAD_METHOD              setWindowFlags
             2898  LOAD_GLOBAL              QtCore
             2900  LOAD_ATTR                Qt
             2902  LOAD_ATTR                WindowStaysOnTopHint
             2904  CALL_METHOD_1         1  '1 positional argument'
             2906  POP_TOP          

 L. 746      2908  LOAD_FAST                '_pgsdlg'
             2910  LOAD_METHOD              forceShow
             2912  CALL_METHOD_0         0  '0 positional arguments'
             2914  POP_TOP          

 L. 747      2916  LOAD_FAST                '_pgsdlg'
             2918  LOAD_METHOD              setFixedWidth
             2920  LOAD_CONST               400
             2922  CALL_METHOD_1         1  '1 positional argument'
             2924  POP_TOP          

 L. 748      2926  LOAD_GLOBAL              ml_wdcnn
             2928  LOAD_ATTR                createWDCNNSegmentor
             2930  LOAD_FAST                '_traindict'

 L. 749      2932  LOAD_FAST                '_image_height_new'
             2934  LOAD_FAST                '_image_width_new'

 L. 750      2936  LOAD_FAST                '_features'
             2938  LOAD_FAST                '_target'
             2940  LOAD_FAST                '_weight'

 L. 751      2942  LOAD_FAST                '_nepoch'
             2944  LOAD_FAST                '_batchsize'

 L. 752      2946  LOAD_FAST                '_nconvblock'
             2948  LOAD_FAST                '_nconvfeature'

 L. 753      2950  LOAD_FAST                '_nconvlayer'

 L. 754      2952  LOAD_FAST                '_n1x1layer'
             2954  LOAD_FAST                '_n1x1feature'

 L. 755      2956  LOAD_FAST                '_patch_height'
             2958  LOAD_FAST                '_patch_width'

 L. 756      2960  LOAD_FAST                '_pool_height'
             2962  LOAD_FAST                '_pool_width'

 L. 757      2964  LOAD_CONST               False

 L. 758      2966  LOAD_FAST                '_learning_rate'

 L. 759      2968  LOAD_FAST                '_dropout_prob'

 L. 760      2970  LOAD_CONST               True

 L. 761      2972  LOAD_FAST                '_savepath'
             2974  LOAD_FAST                '_savename'

 L. 762      2976  LOAD_FAST                '_pgsdlg'
             2978  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'weight', 'nepoch', 'batchsize', 'nconvblock', 'nconvfeature', 'nconvlayer', 'n1x1layer', 'n1x1feature', 'patchheight', 'patchwidth', 'poolheight', 'poolwidth', 'batchnormalization', 'learningrate', 'dropoutprob', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2980  CALL_FUNCTION_KW_24    24  '24 total positional and keyword args'
             2982  STORE_FAST               '_dcnnlog'

 L. 765      2984  LOAD_GLOBAL              QtWidgets
             2986  LOAD_ATTR                QMessageBox
             2988  LOAD_METHOD              information
             2990  LOAD_DEREF               'self'
             2992  LOAD_ATTR                msgbox

 L. 766      2994  LOAD_STR                 'Train 2D-WDCNN'

 L. 767      2996  LOAD_STR                 'WDCNN trained successfully'
             2998  CALL_METHOD_3         3  '3 positional arguments'
             3000  POP_TOP          

 L. 769      3002  LOAD_GLOBAL              QtWidgets
             3004  LOAD_ATTR                QMessageBox
             3006  LOAD_METHOD              question
             3008  LOAD_DEREF               'self'
             3010  LOAD_ATTR                msgbox
             3012  LOAD_STR                 'Train 2D-WDCNN'
             3014  LOAD_STR                 'View learning matrix?'

 L. 770      3016  LOAD_GLOBAL              QtWidgets
             3018  LOAD_ATTR                QMessageBox
             3020  LOAD_ATTR                Yes
             3022  LOAD_GLOBAL              QtWidgets
             3024  LOAD_ATTR                QMessageBox
             3026  LOAD_ATTR                No
             3028  BINARY_OR        

 L. 771      3030  LOAD_GLOBAL              QtWidgets
             3032  LOAD_ATTR                QMessageBox
             3034  LOAD_ATTR                Yes
             3036  CALL_METHOD_5         5  '5 positional arguments'
             3038  STORE_FAST               'reply'

 L. 773      3040  LOAD_FAST                'reply'
             3042  LOAD_GLOBAL              QtWidgets
             3044  LOAD_ATTR                QMessageBox
             3046  LOAD_ATTR                Yes
             3048  COMPARE_OP               ==
         3050_3052  POP_JUMP_IF_FALSE  3120  'to 3120'

 L. 774      3054  LOAD_GLOBAL              QtWidgets
             3056  LOAD_METHOD              QDialog
             3058  CALL_METHOD_0         0  '0 positional arguments'
             3060  STORE_FAST               '_viewmllearnmat'

 L. 775      3062  LOAD_GLOBAL              gui_viewmllearnmat
             3064  CALL_FUNCTION_0       0  '0 positional arguments'
             3066  STORE_FAST               '_gui'

 L. 776      3068  LOAD_FAST                '_dcnnlog'
             3070  LOAD_STR                 'learning_curve'
             3072  BINARY_SUBSCR    
             3074  LOAD_FAST                '_gui'
             3076  STORE_ATTR               learnmat

 L. 777      3078  LOAD_DEREF               'self'
             3080  LOAD_ATTR                linestyle
             3082  LOAD_FAST                '_gui'
             3084  STORE_ATTR               linestyle

 L. 778      3086  LOAD_DEREF               'self'
             3088  LOAD_ATTR                fontstyle
             3090  LOAD_FAST                '_gui'
             3092  STORE_ATTR               fontstyle

 L. 779      3094  LOAD_FAST                '_gui'
             3096  LOAD_METHOD              setupGUI
             3098  LOAD_FAST                '_viewmllearnmat'
             3100  CALL_METHOD_1         1  '1 positional argument'
             3102  POP_TOP          

 L. 780      3104  LOAD_FAST                '_viewmllearnmat'
             3106  LOAD_METHOD              exec
             3108  CALL_METHOD_0         0  '0 positional arguments'
             3110  POP_TOP          

 L. 781      3112  LOAD_FAST                '_viewmllearnmat'
             3114  LOAD_METHOD              show
             3116  CALL_METHOD_0         0  '0 positional arguments'
             3118  POP_TOP          
           3120_0  COME_FROM          3050  '3050'

Parse error at or near `POP_TOP' instruction at offset 3118

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
    TrainMl2DWdcnnFromScratch = QtWidgets.QWidget()
    gui = trainml2dwdcnnfromscratch()
    gui.setupGUI(TrainMl2DWdcnnFromScratch)
    TrainMl2DWdcnnFromScratch.show()
    sys.exit(app.exec_())