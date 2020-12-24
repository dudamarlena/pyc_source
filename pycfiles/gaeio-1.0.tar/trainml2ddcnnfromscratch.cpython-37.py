# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml2ddcnnfromscratch.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 43821 bytes
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
import cognitivegeo.src.ml.dcnnsegmentor as ml_dcnn
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml2ddcnnfromscratch(object):
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

    def setupGUI(self, TrainMl2DDcnnFromScratch):
        TrainMl2DDcnnFromScratch.setObjectName('TrainMl2DDcnnFromScratch')
        TrainMl2DDcnnFromScratch.setFixedSize(810, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl2DDcnnFromScratch.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl2DDcnnFromScratch)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl2DDcnnFromScratch)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl2DDcnnFromScratch)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 50, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 50, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl2DDcnnFromScratch)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 90, 180, 200))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 50, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 50, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(TrainMl2DDcnnFromScratch)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 90, 180, 200))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 300, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 300, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 300, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 340, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 340, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 300, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 300, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 300, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 340, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 340, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl2DDcnnFromScratch)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 310, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 350, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.lbldropout = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 390, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 390, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl2DDcnnFromScratch)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl2DDcnnFromScratch)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 440, 180, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl2DDcnnFromScratch)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 440, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl2DDcnnFromScratch)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl2DDcnnFromScratch)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl2DDcnnFromScratch.geometry().center().x()
        _center_y = TrainMl2DDcnnFromScratch.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl2DDcnnFromScratch)
        QtCore.QMetaObject.connectSlotsByName(TrainMl2DDcnnFromScratch)

    def retranslateGUI(self, TrainMl2DDcnnFromScratch):
        self.dialog = TrainMl2DDcnnFromScratch
        _translate = QtCore.QCoreApplication.translate
        TrainMl2DDcnnFromScratch.setWindowTitle(_translate('TrainMl2DDcnnFromScratch', 'Train 2D-DCNN from scratch'))
        self.lblfeature.setText(_translate('TrainMl2DDcnnFromScratch', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl2DDcnnFromScratch', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl2DDcnnFromScratch', 'Select target:'))
        self.btnconfigtraindata.setText(_translate('TrainMl2DDcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('TrainMl2DDcnnFromScratch', 'Original\nimage\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl2DDcnnFromScratch', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl2DDcnnFromScratch', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl2DDcnnFromScratch', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl2DDcnnFromScratch', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl2DDcnnFromScratch', 'Interpolated\nimage\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl2DDcnnFromScratch', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl2DDcnnFromScratch', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl2DDcnnFromScratch', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl2DDcnnFromScratch', '32'))
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
                    item.setText(_translate('TrainMl2DDcnnFromScratch', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl2DDcnnFromScratch', 'Specify DCNN architecture:'))
        self.lblnconvblock.setText(_translate('TrainMl2DDcnnFromScratch', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl2DDcnnFromScratch', '3'))
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

        self.lbln1x1layer.setText(_translate('TrainMl2DDcnnFromScratch', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('TrainMl2DDcnnFromScratch', '2'))
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.twgn1x1layer.setRowCount(2)
        for _idx in range(int(self.ldtn1x1layer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl2DDcnnFromScratch', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgn1x1layer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgn1x1layer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl2DDcnnFromScratch', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl2DDcnnFromScratch', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl2DDcnnFromScratch', '3'))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('TrainMl2DDcnnFromScratch', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl2DDcnnFromScratch', '3'))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('TrainMl2DDcnnFromScratch', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl2DDcnnFromScratch', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl2DDcnnFromScratch', '2'))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl2DDcnnFromScratch', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl2DDcnnFromScratch', '2'))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('TrainMl2DDcnnFromScratch', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl2DDcnnFromScratch', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl2DDcnnFromScratch', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl2DDcnnFromScratch', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl2DDcnnFromScratch', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl2DDcnnFromScratch', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl2DDcnnFromScratch', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('TrainMl2DDcnnFromScratch', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('TrainMl2DDcnnFromScratch', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl2DDcnnFromScratch', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl2DDcnnFromScratch', ''))
        self.btnsave.setText(_translate('TrainMl2DDcnnFromScratch', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl2DDcnnFromScratch', 'Train 2D-DCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl2DDcnnFromScratch)

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

    def clickBtnTrainMl2DDcnnFromScratch--- This code section failed: ---

 L. 444         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 446         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 447        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 448        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 449        50  LOAD_STR                 'Train 2D-DCNN'

 L. 450        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 451        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 453        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_image_height'

 L. 454        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_image_width'

 L. 455        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtnewheight
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_image_height_new'

 L. 456       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewwidth
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_image_width_new'

 L. 457       126  LOAD_FAST                '_image_height'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'
              134  LOAD_FAST                '_image_width'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_TRUE    158  'to 158'

 L. 458       142  LOAD_FAST                '_image_height_new'
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

 L. 459       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 460       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 461       182  LOAD_STR                 'Train 2D-DCNN'

 L. 462       184  LOAD_STR                 'Non-integer feature size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 463       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 464       194  LOAD_FAST                '_image_height'
              196  LOAD_CONST               2
              198  COMPARE_OP               <
              200  POP_JUMP_IF_TRUE    228  'to 228'
              202  LOAD_FAST                '_image_width'
              204  LOAD_CONST               2
              206  COMPARE_OP               <
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 465       210  LOAD_FAST                '_image_height_new'
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

 L. 466       228  LOAD_GLOBAL              vis_msg
              230  LOAD_ATTR                print
              232  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 467       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 468       252  LOAD_STR                 'Train 2D-DCNN'

 L. 469       254  LOAD_STR                 'Features are not 2D'
              256  CALL_METHOD_3         3  '3 positional arguments'
              258  POP_TOP          

 L. 470       260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           224  '224'

 L. 472       264  LOAD_CONST               2
              266  LOAD_GLOBAL              int
              268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               2
              272  BINARY_TRUE_DIVIDE
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  BINARY_MULTIPLY  
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  STORE_FAST               '_image_height'

 L. 473       284  LOAD_CONST               2
              286  LOAD_GLOBAL              int
              288  LOAD_FAST                '_image_width'
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BINARY_MULTIPLY  
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               '_image_width'

 L. 475       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                lwgfeature
              308  LOAD_METHOD              selectedItems
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               '_features'

 L. 476       314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainml2ddcnnfromscratch.clickBtnTrainMl2DDcnnFromScratch.<locals>.<listcomp>'
              318  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              320  LOAD_FAST                '_features'
              322  GET_ITER         
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               '_features'

 L. 477       328  LOAD_DEREF               'self'
              330  LOAD_ATTR                featurelist
              332  LOAD_DEREF               'self'
              334  LOAD_ATTR                cbbtarget
              336  LOAD_METHOD              currentIndex
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  BINARY_SUBSCR    
              342  STORE_FAST               '_target'

 L. 479       344  LOAD_FAST                '_target'
              346  LOAD_FAST                '_features'
              348  COMPARE_OP               in
          350_352  POP_JUMP_IF_FALSE   390  'to 390'

 L. 480       354  LOAD_GLOBAL              vis_msg
              356  LOAD_ATTR                print
              358  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Target also used as features'
              360  LOAD_STR                 'error'
              362  LOAD_CONST               ('type',)
              364  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              366  POP_TOP          

 L. 481       368  LOAD_GLOBAL              QtWidgets
              370  LOAD_ATTR                QMessageBox
              372  LOAD_METHOD              critical
              374  LOAD_DEREF               'self'
              376  LOAD_ATTR                msgbox

 L. 482       378  LOAD_STR                 'Train 2D-DCNN'

 L. 483       380  LOAD_STR                 'Target also used as features'
              382  CALL_METHOD_3         3  '3 positional arguments'
              384  POP_TOP          

 L. 484       386  LOAD_CONST               None
              388  RETURN_VALUE     
            390_0  COME_FROM           350  '350'

 L. 486       390  LOAD_GLOBAL              basic_data
              392  LOAD_METHOD              str2int
              394  LOAD_DEREF               'self'
              396  LOAD_ATTR                ldtnconvblock
              398  LOAD_METHOD              text
              400  CALL_METHOD_0         0  '0 positional arguments'
              402  CALL_METHOD_1         1  '1 positional argument'
              404  STORE_FAST               '_nconvblock'

 L. 487       406  LOAD_CLOSURE             'self'
              408  BUILD_TUPLE_1         1 
              410  LOAD_LISTCOMP            '<code_object <listcomp>>'
              412  LOAD_STR                 'trainml2ddcnnfromscratch.clickBtnTrainMl2DDcnnFromScratch.<locals>.<listcomp>'
              414  MAKE_FUNCTION_8          'closure'
              416  LOAD_GLOBAL              range
              418  LOAD_FAST                '_nconvblock'
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  GET_ITER         
              424  CALL_FUNCTION_1       1  '1 positional argument'
              426  STORE_FAST               '_nconvlayer'

 L. 488       428  LOAD_CLOSURE             'self'
              430  BUILD_TUPLE_1         1 
              432  LOAD_LISTCOMP            '<code_object <listcomp>>'
              434  LOAD_STR                 'trainml2ddcnnfromscratch.clickBtnTrainMl2DDcnnFromScratch.<locals>.<listcomp>'
              436  MAKE_FUNCTION_8          'closure'
              438  LOAD_GLOBAL              range
              440  LOAD_FAST                '_nconvblock'
              442  CALL_FUNCTION_1       1  '1 positional argument'
              444  GET_ITER         
              446  CALL_FUNCTION_1       1  '1 positional argument'
              448  STORE_FAST               '_nconvfeature'

 L. 489       450  LOAD_GLOBAL              basic_data
              452  LOAD_METHOD              str2int
              454  LOAD_DEREF               'self'
              456  LOAD_ATTR                ldtn1x1layer
              458  LOAD_METHOD              text
              460  CALL_METHOD_0         0  '0 positional arguments'
              462  CALL_METHOD_1         1  '1 positional argument'
              464  STORE_FAST               '_n1x1layer'

 L. 490       466  LOAD_CLOSURE             'self'
              468  BUILD_TUPLE_1         1 
              470  LOAD_LISTCOMP            '<code_object <listcomp>>'
              472  LOAD_STR                 'trainml2ddcnnfromscratch.clickBtnTrainMl2DDcnnFromScratch.<locals>.<listcomp>'
              474  MAKE_FUNCTION_8          'closure'
              476  LOAD_GLOBAL              range
              478  LOAD_FAST                '_n1x1layer'
              480  CALL_FUNCTION_1       1  '1 positional argument'
              482  GET_ITER         
              484  CALL_FUNCTION_1       1  '1 positional argument'
              486  STORE_FAST               '_n1x1feature'

 L. 491       488  LOAD_GLOBAL              basic_data
              490  LOAD_METHOD              str2int
              492  LOAD_DEREF               'self'
              494  LOAD_ATTR                ldtmaskheight
              496  LOAD_METHOD              text
              498  CALL_METHOD_0         0  '0 positional arguments'
              500  CALL_METHOD_1         1  '1 positional argument'
              502  STORE_FAST               '_patch_height'

 L. 492       504  LOAD_GLOBAL              basic_data
              506  LOAD_METHOD              str2int
              508  LOAD_DEREF               'self'
              510  LOAD_ATTR                ldtmaskwidth
              512  LOAD_METHOD              text
              514  CALL_METHOD_0         0  '0 positional arguments'
              516  CALL_METHOD_1         1  '1 positional argument'
              518  STORE_FAST               '_patch_width'

 L. 493       520  LOAD_GLOBAL              basic_data
              522  LOAD_METHOD              str2int
              524  LOAD_DEREF               'self'
              526  LOAD_ATTR                ldtpoolheight
              528  LOAD_METHOD              text
              530  CALL_METHOD_0         0  '0 positional arguments'
              532  CALL_METHOD_1         1  '1 positional argument'
              534  STORE_FAST               '_pool_height'

 L. 494       536  LOAD_GLOBAL              basic_data
              538  LOAD_METHOD              str2int
              540  LOAD_DEREF               'self'
              542  LOAD_ATTR                ldtpoolwidth
              544  LOAD_METHOD              text
              546  CALL_METHOD_0         0  '0 positional arguments'
              548  CALL_METHOD_1         1  '1 positional argument'
              550  STORE_FAST               '_pool_width'

 L. 495       552  LOAD_GLOBAL              basic_data
              554  LOAD_METHOD              str2int
              556  LOAD_DEREF               'self'
              558  LOAD_ATTR                ldtnepoch
              560  LOAD_METHOD              text
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  CALL_METHOD_1         1  '1 positional argument'
              566  STORE_FAST               '_nepoch'

 L. 496       568  LOAD_GLOBAL              basic_data
              570  LOAD_METHOD              str2int
              572  LOAD_DEREF               'self'
              574  LOAD_ATTR                ldtbatchsize
              576  LOAD_METHOD              text
              578  CALL_METHOD_0         0  '0 positional arguments'
              580  CALL_METHOD_1         1  '1 positional argument'
              582  STORE_FAST               '_batchsize'

 L. 497       584  LOAD_GLOBAL              basic_data
              586  LOAD_METHOD              str2float
              588  LOAD_DEREF               'self'
              590  LOAD_ATTR                ldtlearnrate
              592  LOAD_METHOD              text
              594  CALL_METHOD_0         0  '0 positional arguments'
              596  CALL_METHOD_1         1  '1 positional argument'
              598  STORE_FAST               '_learning_rate'

 L. 498       600  LOAD_GLOBAL              basic_data
              602  LOAD_METHOD              str2float
              604  LOAD_DEREF               'self'
              606  LOAD_ATTR                ldtdropout
              608  LOAD_METHOD              text
              610  CALL_METHOD_0         0  '0 positional arguments'
              612  CALL_METHOD_1         1  '1 positional argument'
              614  STORE_FAST               '_dropout_prob'

 L. 499       616  LOAD_FAST                '_nconvblock'
              618  LOAD_CONST               False
              620  COMPARE_OP               is
          622_624  POP_JUMP_IF_TRUE    636  'to 636'
              626  LOAD_FAST                '_nconvblock'
              628  LOAD_CONST               0
              630  COMPARE_OP               <=
          632_634  POP_JUMP_IF_FALSE   672  'to 672'
            636_0  COME_FROM           622  '622'

 L. 500       636  LOAD_GLOBAL              vis_msg
              638  LOAD_ATTR                print
              640  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Non-positive convolutional block number'

 L. 501       642  LOAD_STR                 'error'
              644  LOAD_CONST               ('type',)
              646  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              648  POP_TOP          

 L. 502       650  LOAD_GLOBAL              QtWidgets
              652  LOAD_ATTR                QMessageBox
              654  LOAD_METHOD              critical
              656  LOAD_DEREF               'self'
              658  LOAD_ATTR                msgbox

 L. 503       660  LOAD_STR                 'Train 2D-DCNN'

 L. 504       662  LOAD_STR                 'Non-positive convolutional block number'
              664  CALL_METHOD_3         3  '3 positional arguments'
              666  POP_TOP          

 L. 505       668  LOAD_CONST               None
              670  RETURN_VALUE     
            672_0  COME_FROM           632  '632'

 L. 506       672  SETUP_LOOP          744  'to 744'
              674  LOAD_FAST                '_nconvlayer'
              676  GET_ITER         
            678_0  COME_FROM           698  '698'
              678  FOR_ITER            742  'to 742'
              680  STORE_FAST               '_i'

 L. 507       682  LOAD_FAST                '_i'
              684  LOAD_CONST               False
              686  COMPARE_OP               is
          688_690  POP_JUMP_IF_TRUE    702  'to 702'
              692  LOAD_FAST                '_i'
              694  LOAD_CONST               1
              696  COMPARE_OP               <
          698_700  POP_JUMP_IF_FALSE   678  'to 678'
            702_0  COME_FROM           688  '688'

 L. 508       702  LOAD_GLOBAL              vis_msg
              704  LOAD_ATTR                print
              706  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Non-positive convolutional layer number'

 L. 509       708  LOAD_STR                 'error'
              710  LOAD_CONST               ('type',)
              712  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              714  POP_TOP          

 L. 510       716  LOAD_GLOBAL              QtWidgets
              718  LOAD_ATTR                QMessageBox
              720  LOAD_METHOD              critical
              722  LOAD_DEREF               'self'
              724  LOAD_ATTR                msgbox

 L. 511       726  LOAD_STR                 'Train 2D-DCNN'

 L. 512       728  LOAD_STR                 'Non-positive convolutional layer number'
              730  CALL_METHOD_3         3  '3 positional arguments'
              732  POP_TOP          

 L. 513       734  LOAD_CONST               None
              736  RETURN_VALUE     
          738_740  JUMP_BACK           678  'to 678'
              742  POP_BLOCK        
            744_0  COME_FROM_LOOP      672  '672'

 L. 514       744  SETUP_LOOP          816  'to 816'
              746  LOAD_FAST                '_nconvfeature'
              748  GET_ITER         
            750_0  COME_FROM           770  '770'
              750  FOR_ITER            814  'to 814'
              752  STORE_FAST               '_i'

 L. 515       754  LOAD_FAST                '_i'
              756  LOAD_CONST               False
              758  COMPARE_OP               is
          760_762  POP_JUMP_IF_TRUE    774  'to 774'
              764  LOAD_FAST                '_i'
              766  LOAD_CONST               1
              768  COMPARE_OP               <
          770_772  POP_JUMP_IF_FALSE   750  'to 750'
            774_0  COME_FROM           760  '760'

 L. 516       774  LOAD_GLOBAL              vis_msg
              776  LOAD_ATTR                print
              778  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Non-positive convolutional feature number'

 L. 517       780  LOAD_STR                 'error'
              782  LOAD_CONST               ('type',)
              784  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              786  POP_TOP          

 L. 518       788  LOAD_GLOBAL              QtWidgets
              790  LOAD_ATTR                QMessageBox
              792  LOAD_METHOD              critical
              794  LOAD_DEREF               'self'
              796  LOAD_ATTR                msgbox

 L. 519       798  LOAD_STR                 'Train 2D-DCNN'

 L. 520       800  LOAD_STR                 'Non-positive convolutional feature number'
              802  CALL_METHOD_3         3  '3 positional arguments'
              804  POP_TOP          

 L. 521       806  LOAD_CONST               None
              808  RETURN_VALUE     
          810_812  JUMP_BACK           750  'to 750'
              814  POP_BLOCK        
            816_0  COME_FROM_LOOP      744  '744'

 L. 522       816  LOAD_FAST                '_n1x1layer'
              818  LOAD_CONST               False
              820  COMPARE_OP               is
          822_824  POP_JUMP_IF_TRUE    836  'to 836'
              826  LOAD_FAST                '_n1x1layer'
              828  LOAD_CONST               0
              830  COMPARE_OP               <=
          832_834  POP_JUMP_IF_FALSE   872  'to 872'
            836_0  COME_FROM           822  '822'

 L. 523       836  LOAD_GLOBAL              vis_msg
              838  LOAD_ATTR                print
              840  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Non-positive 1x1 convolutional layer number'

 L. 524       842  LOAD_STR                 'error'
              844  LOAD_CONST               ('type',)
              846  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              848  POP_TOP          

 L. 525       850  LOAD_GLOBAL              QtWidgets
              852  LOAD_ATTR                QMessageBox
              854  LOAD_METHOD              critical
              856  LOAD_DEREF               'self'
              858  LOAD_ATTR                msgbox

 L. 526       860  LOAD_STR                 'Train 2D-DCNN'

 L. 527       862  LOAD_STR                 'Non-positive 1x1 convolutional layer number'
              864  CALL_METHOD_3         3  '3 positional arguments'
              866  POP_TOP          

 L. 528       868  LOAD_CONST               None
              870  RETURN_VALUE     
            872_0  COME_FROM           832  '832'

 L. 529       872  SETUP_LOOP          944  'to 944'
              874  LOAD_FAST                '_n1x1feature'
              876  GET_ITER         
            878_0  COME_FROM           898  '898'
              878  FOR_ITER            942  'to 942'
              880  STORE_FAST               '_i'

 L. 530       882  LOAD_FAST                '_i'
              884  LOAD_CONST               False
              886  COMPARE_OP               is
          888_890  POP_JUMP_IF_TRUE    902  'to 902'
              892  LOAD_FAST                '_i'
              894  LOAD_CONST               1
              896  COMPARE_OP               <
          898_900  POP_JUMP_IF_FALSE   878  'to 878'
            902_0  COME_FROM           888  '888'

 L. 531       902  LOAD_GLOBAL              vis_msg
              904  LOAD_ATTR                print
              906  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Non-positive 1x1 convolutional feature number'

 L. 532       908  LOAD_STR                 'error'
              910  LOAD_CONST               ('type',)
              912  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              914  POP_TOP          

 L. 533       916  LOAD_GLOBAL              QtWidgets
              918  LOAD_ATTR                QMessageBox
              920  LOAD_METHOD              critical
              922  LOAD_DEREF               'self'
              924  LOAD_ATTR                msgbox

 L. 534       926  LOAD_STR                 'Train 2D-DCNN'

 L. 535       928  LOAD_STR                 'Non-positive 1x1 convolutional feature number'
              930  CALL_METHOD_3         3  '3 positional arguments'
              932  POP_TOP          

 L. 536       934  LOAD_CONST               None
              936  RETURN_VALUE     
          938_940  JUMP_BACK           878  'to 878'
              942  POP_BLOCK        
            944_0  COME_FROM_LOOP      872  '872'

 L. 537       944  LOAD_FAST                '_patch_height'
              946  LOAD_CONST               False
              948  COMPARE_OP               is
          950_952  POP_JUMP_IF_TRUE    984  'to 984'
              954  LOAD_FAST                '_patch_width'
              956  LOAD_CONST               False
              958  COMPARE_OP               is
          960_962  POP_JUMP_IF_TRUE    984  'to 984'

 L. 538       964  LOAD_FAST                '_patch_height'
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

 L. 539       984  LOAD_GLOBAL              vis_msg
              986  LOAD_ATTR                print
              988  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Non-positive convolutional patch size'
              990  LOAD_STR                 'error'
              992  LOAD_CONST               ('type',)
              994  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              996  POP_TOP          

 L. 540       998  LOAD_GLOBAL              QtWidgets
             1000  LOAD_ATTR                QMessageBox
             1002  LOAD_METHOD              critical
             1004  LOAD_DEREF               'self'
             1006  LOAD_ATTR                msgbox

 L. 541      1008  LOAD_STR                 'Train 2D-DCNN'

 L. 542      1010  LOAD_STR                 'Non-positive convolutional patch size'
             1012  CALL_METHOD_3         3  '3 positional arguments'
             1014  POP_TOP          

 L. 543      1016  LOAD_CONST               None
             1018  RETURN_VALUE     
           1020_0  COME_FROM           980  '980'

 L. 544      1020  LOAD_FAST                '_pool_height'
             1022  LOAD_CONST               False
             1024  COMPARE_OP               is
         1026_1028  POP_JUMP_IF_TRUE   1060  'to 1060'
             1030  LOAD_FAST                '_pool_width'
             1032  LOAD_CONST               False
             1034  COMPARE_OP               is
         1036_1038  POP_JUMP_IF_TRUE   1060  'to 1060'

 L. 545      1040  LOAD_FAST                '_pool_height'
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

 L. 546      1060  LOAD_GLOBAL              vis_msg
             1062  LOAD_ATTR                print
             1064  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Non-positive pooling size'
             1066  LOAD_STR                 'error'
             1068  LOAD_CONST               ('type',)
             1070  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1072  POP_TOP          

 L. 547      1074  LOAD_GLOBAL              QtWidgets
             1076  LOAD_ATTR                QMessageBox
             1078  LOAD_METHOD              critical
             1080  LOAD_DEREF               'self'
             1082  LOAD_ATTR                msgbox

 L. 548      1084  LOAD_STR                 'Train 2D-DCNN'

 L. 549      1086  LOAD_STR                 'Non-positive pooling size'
             1088  CALL_METHOD_3         3  '3 positional arguments'
             1090  POP_TOP          

 L. 550      1092  LOAD_CONST               None
             1094  RETURN_VALUE     
           1096_0  COME_FROM          1056  '1056'

 L. 551      1096  LOAD_FAST                '_nepoch'
             1098  LOAD_CONST               False
             1100  COMPARE_OP               is
         1102_1104  POP_JUMP_IF_TRUE   1116  'to 1116'
             1106  LOAD_FAST                '_nepoch'
             1108  LOAD_CONST               0
             1110  COMPARE_OP               <=
         1112_1114  POP_JUMP_IF_FALSE  1152  'to 1152'
           1116_0  COME_FROM          1102  '1102'

 L. 552      1116  LOAD_GLOBAL              vis_msg
             1118  LOAD_ATTR                print
             1120  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Non-positive epoch number'
             1122  LOAD_STR                 'error'
             1124  LOAD_CONST               ('type',)
             1126  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1128  POP_TOP          

 L. 553      1130  LOAD_GLOBAL              QtWidgets
             1132  LOAD_ATTR                QMessageBox
             1134  LOAD_METHOD              critical
             1136  LOAD_DEREF               'self'
             1138  LOAD_ATTR                msgbox

 L. 554      1140  LOAD_STR                 'Train 2D-DCNN'

 L. 555      1142  LOAD_STR                 'Non-positive epoch number'
             1144  CALL_METHOD_3         3  '3 positional arguments'
             1146  POP_TOP          

 L. 556      1148  LOAD_CONST               None
             1150  RETURN_VALUE     
           1152_0  COME_FROM          1112  '1112'

 L. 557      1152  LOAD_FAST                '_batchsize'
             1154  LOAD_CONST               False
             1156  COMPARE_OP               is
         1158_1160  POP_JUMP_IF_TRUE   1172  'to 1172'
             1162  LOAD_FAST                '_batchsize'
             1164  LOAD_CONST               0
             1166  COMPARE_OP               <=
         1168_1170  POP_JUMP_IF_FALSE  1208  'to 1208'
           1172_0  COME_FROM          1158  '1158'

 L. 558      1172  LOAD_GLOBAL              vis_msg
             1174  LOAD_ATTR                print
             1176  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Non-positive batch size'
             1178  LOAD_STR                 'error'
             1180  LOAD_CONST               ('type',)
             1182  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1184  POP_TOP          

 L. 559      1186  LOAD_GLOBAL              QtWidgets
             1188  LOAD_ATTR                QMessageBox
             1190  LOAD_METHOD              critical
             1192  LOAD_DEREF               'self'
             1194  LOAD_ATTR                msgbox

 L. 560      1196  LOAD_STR                 'Train 2D-DCNN'

 L. 561      1198  LOAD_STR                 'Non-positive batch size'
             1200  CALL_METHOD_3         3  '3 positional arguments'
             1202  POP_TOP          

 L. 562      1204  LOAD_CONST               None
             1206  RETURN_VALUE     
           1208_0  COME_FROM          1168  '1168'

 L. 563      1208  LOAD_FAST                '_learning_rate'
             1210  LOAD_CONST               False
             1212  COMPARE_OP               is
         1214_1216  POP_JUMP_IF_TRUE   1228  'to 1228'
             1218  LOAD_FAST                '_learning_rate'
             1220  LOAD_CONST               0
             1222  COMPARE_OP               <=
         1224_1226  POP_JUMP_IF_FALSE  1264  'to 1264'
           1228_0  COME_FROM          1214  '1214'

 L. 564      1228  LOAD_GLOBAL              vis_msg
             1230  LOAD_ATTR                print
             1232  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Non-positive learning rate'
             1234  LOAD_STR                 'error'
             1236  LOAD_CONST               ('type',)
             1238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1240  POP_TOP          

 L. 565      1242  LOAD_GLOBAL              QtWidgets
             1244  LOAD_ATTR                QMessageBox
             1246  LOAD_METHOD              critical
             1248  LOAD_DEREF               'self'
             1250  LOAD_ATTR                msgbox

 L. 566      1252  LOAD_STR                 'Train 2D-DCNN'

 L. 567      1254  LOAD_STR                 'Non-positive learning rate'
             1256  CALL_METHOD_3         3  '3 positional arguments'
             1258  POP_TOP          

 L. 568      1260  LOAD_CONST               None
             1262  RETURN_VALUE     
           1264_0  COME_FROM          1224  '1224'

 L. 569      1264  LOAD_FAST                '_dropout_prob'
             1266  LOAD_CONST               False
             1268  COMPARE_OP               is
         1270_1272  POP_JUMP_IF_TRUE   1284  'to 1284'
             1274  LOAD_FAST                '_dropout_prob'
             1276  LOAD_CONST               0
             1278  COMPARE_OP               <=
         1280_1282  POP_JUMP_IF_FALSE  1320  'to 1320'
           1284_0  COME_FROM          1270  '1270'

 L. 570      1284  LOAD_GLOBAL              vis_msg
             1286  LOAD_ATTR                print
             1288  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: Negative dropout rate'
             1290  LOAD_STR                 'error'
             1292  LOAD_CONST               ('type',)
             1294  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1296  POP_TOP          

 L. 571      1298  LOAD_GLOBAL              QtWidgets
             1300  LOAD_ATTR                QMessageBox
             1302  LOAD_METHOD              critical
             1304  LOAD_DEREF               'self'
             1306  LOAD_ATTR                msgbox

 L. 572      1308  LOAD_STR                 'Train 2D-DCNN'

 L. 573      1310  LOAD_STR                 'Negative dropout rate'
             1312  CALL_METHOD_3         3  '3 positional arguments'
             1314  POP_TOP          

 L. 574      1316  LOAD_CONST               None
             1318  RETURN_VALUE     
           1320_0  COME_FROM          1280  '1280'

 L. 576      1320  LOAD_GLOBAL              len
             1322  LOAD_DEREF               'self'
             1324  LOAD_ATTR                ldtsave
             1326  LOAD_METHOD              text
             1328  CALL_METHOD_0         0  '0 positional arguments'
             1330  CALL_FUNCTION_1       1  '1 positional argument'
             1332  LOAD_CONST               1
             1334  COMPARE_OP               <
         1336_1338  POP_JUMP_IF_FALSE  1376  'to 1376'

 L. 577      1340  LOAD_GLOBAL              vis_msg
             1342  LOAD_ATTR                print
             1344  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: No name specified for DCNN network'
             1346  LOAD_STR                 'error'
             1348  LOAD_CONST               ('type',)
             1350  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1352  POP_TOP          

 L. 578      1354  LOAD_GLOBAL              QtWidgets
             1356  LOAD_ATTR                QMessageBox
             1358  LOAD_METHOD              critical
             1360  LOAD_DEREF               'self'
             1362  LOAD_ATTR                msgbox

 L. 579      1364  LOAD_STR                 'Train 2D-DCNN'

 L. 580      1366  LOAD_STR                 'No name specified for DCNN network'
             1368  CALL_METHOD_3         3  '3 positional arguments'
             1370  POP_TOP          

 L. 581      1372  LOAD_CONST               None
             1374  RETURN_VALUE     
           1376_0  COME_FROM          1336  '1336'

 L. 582      1376  LOAD_GLOBAL              os
             1378  LOAD_ATTR                path
             1380  LOAD_METHOD              dirname
             1382  LOAD_DEREF               'self'
             1384  LOAD_ATTR                ldtsave
             1386  LOAD_METHOD              text
             1388  CALL_METHOD_0         0  '0 positional arguments'
             1390  CALL_METHOD_1         1  '1 positional argument'
             1392  STORE_FAST               '_savepath'

 L. 583      1394  LOAD_GLOBAL              os
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

 L. 585      1424  LOAD_CONST               0
             1426  STORE_FAST               '_wdinl'

 L. 586      1428  LOAD_CONST               0
             1430  STORE_FAST               '_wdxl'

 L. 587      1432  LOAD_CONST               0
             1434  STORE_FAST               '_wdz'

 L. 588      1436  LOAD_DEREF               'self'
             1438  LOAD_ATTR                cbbornt
             1440  LOAD_METHOD              currentIndex
             1442  CALL_METHOD_0         0  '0 positional arguments'
             1444  LOAD_CONST               0
             1446  COMPARE_OP               ==
         1448_1450  POP_JUMP_IF_FALSE  1476  'to 1476'

 L. 589      1452  LOAD_GLOBAL              int
             1454  LOAD_FAST                '_image_width'
             1456  LOAD_CONST               2
             1458  BINARY_TRUE_DIVIDE
             1460  CALL_FUNCTION_1       1  '1 positional argument'
             1462  STORE_FAST               '_wdxl'

 L. 590      1464  LOAD_GLOBAL              int
             1466  LOAD_FAST                '_image_height'
             1468  LOAD_CONST               2
             1470  BINARY_TRUE_DIVIDE
             1472  CALL_FUNCTION_1       1  '1 positional argument'
             1474  STORE_FAST               '_wdz'
           1476_0  COME_FROM          1448  '1448'

 L. 591      1476  LOAD_DEREF               'self'
             1478  LOAD_ATTR                cbbornt
             1480  LOAD_METHOD              currentIndex
             1482  CALL_METHOD_0         0  '0 positional arguments'
             1484  LOAD_CONST               1
             1486  COMPARE_OP               ==
         1488_1490  POP_JUMP_IF_FALSE  1516  'to 1516'

 L. 592      1492  LOAD_GLOBAL              int
             1494  LOAD_FAST                '_image_width'
             1496  LOAD_CONST               2
             1498  BINARY_TRUE_DIVIDE
             1500  CALL_FUNCTION_1       1  '1 positional argument'
             1502  STORE_FAST               '_wdinl'

 L. 593      1504  LOAD_GLOBAL              int
             1506  LOAD_FAST                '_image_height'
             1508  LOAD_CONST               2
             1510  BINARY_TRUE_DIVIDE
             1512  CALL_FUNCTION_1       1  '1 positional argument'
             1514  STORE_FAST               '_wdz'
           1516_0  COME_FROM          1488  '1488'

 L. 594      1516  LOAD_DEREF               'self'
             1518  LOAD_ATTR                cbbornt
             1520  LOAD_METHOD              currentIndex
             1522  CALL_METHOD_0         0  '0 positional arguments'
             1524  LOAD_CONST               2
             1526  COMPARE_OP               ==
         1528_1530  POP_JUMP_IF_FALSE  1556  'to 1556'

 L. 595      1532  LOAD_GLOBAL              int
             1534  LOAD_FAST                '_image_width'
             1536  LOAD_CONST               2
             1538  BINARY_TRUE_DIVIDE
             1540  CALL_FUNCTION_1       1  '1 positional argument'
             1542  STORE_FAST               '_wdinl'

 L. 596      1544  LOAD_GLOBAL              int
             1546  LOAD_FAST                '_image_height'
             1548  LOAD_CONST               2
             1550  BINARY_TRUE_DIVIDE
             1552  CALL_FUNCTION_1       1  '1 positional argument'
             1554  STORE_FAST               '_wdxl'
           1556_0  COME_FROM          1528  '1528'

 L. 598      1556  LOAD_DEREF               'self'
             1558  LOAD_ATTR                survinfo
             1560  STORE_FAST               '_seisinfo'

 L. 600      1562  LOAD_GLOBAL              print
             1564  LOAD_STR                 'TrainMl2DDcnnFromScratch: Step 1 - Get training samples:'
             1566  CALL_FUNCTION_1       1  '1 positional argument'
             1568  POP_TOP          

 L. 601      1570  LOAD_DEREF               'self'
             1572  LOAD_ATTR                traindataconfig
             1574  LOAD_STR                 'TrainPointSet'
             1576  BINARY_SUBSCR    
             1578  STORE_FAST               '_trainpoint'

 L. 602      1580  LOAD_GLOBAL              np
             1582  LOAD_METHOD              zeros
             1584  LOAD_CONST               0
             1586  LOAD_CONST               3
             1588  BUILD_LIST_2          2 
             1590  CALL_METHOD_1         1  '1 positional argument'
             1592  STORE_FAST               '_traindata'

 L. 603      1594  SETUP_LOOP         1670  'to 1670'
             1596  LOAD_FAST                '_trainpoint'
             1598  GET_ITER         
           1600_0  COME_FROM          1618  '1618'
             1600  FOR_ITER           1668  'to 1668'
             1602  STORE_FAST               '_p'

 L. 604      1604  LOAD_GLOBAL              point_ays
             1606  LOAD_METHOD              checkPoint
             1608  LOAD_DEREF               'self'
             1610  LOAD_ATTR                pointsetdata
             1612  LOAD_FAST                '_p'
             1614  BINARY_SUBSCR    
             1616  CALL_METHOD_1         1  '1 positional argument'
         1618_1620  POP_JUMP_IF_FALSE  1600  'to 1600'

 L. 605      1622  LOAD_GLOBAL              basic_mdt
             1624  LOAD_METHOD              exportMatDict
             1626  LOAD_DEREF               'self'
             1628  LOAD_ATTR                pointsetdata
             1630  LOAD_FAST                '_p'
             1632  BINARY_SUBSCR    
             1634  LOAD_STR                 'Inline'
             1636  LOAD_STR                 'Crossline'
             1638  LOAD_STR                 'Z'
             1640  BUILD_LIST_3          3 
             1642  CALL_METHOD_2         2  '2 positional arguments'
             1644  STORE_FAST               '_pt'

 L. 606      1646  LOAD_GLOBAL              np
             1648  LOAD_ATTR                concatenate
             1650  LOAD_FAST                '_traindata'
             1652  LOAD_FAST                '_pt'
             1654  BUILD_TUPLE_2         2 
             1656  LOAD_CONST               0
             1658  LOAD_CONST               ('axis',)
             1660  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1662  STORE_FAST               '_traindata'
         1664_1666  JUMP_BACK          1600  'to 1600'
             1668  POP_BLOCK        
           1670_0  COME_FROM_LOOP     1594  '1594'

 L. 607      1670  LOAD_GLOBAL              seis_ays
             1672  LOAD_ATTR                removeOutofSurveySample
             1674  LOAD_FAST                '_traindata'

 L. 608      1676  LOAD_FAST                '_seisinfo'
             1678  LOAD_STR                 'ILStart'
             1680  BINARY_SUBSCR    
             1682  LOAD_FAST                '_wdinl'
             1684  LOAD_FAST                '_seisinfo'
             1686  LOAD_STR                 'ILStep'
             1688  BINARY_SUBSCR    
             1690  BINARY_MULTIPLY  
             1692  BINARY_ADD       

 L. 609      1694  LOAD_FAST                '_seisinfo'
             1696  LOAD_STR                 'ILEnd'
             1698  BINARY_SUBSCR    
             1700  LOAD_FAST                '_wdinl'
             1702  LOAD_FAST                '_seisinfo'
             1704  LOAD_STR                 'ILStep'
             1706  BINARY_SUBSCR    
             1708  BINARY_MULTIPLY  
             1710  BINARY_SUBTRACT  

 L. 610      1712  LOAD_FAST                '_seisinfo'
             1714  LOAD_STR                 'XLStart'
             1716  BINARY_SUBSCR    
             1718  LOAD_FAST                '_wdxl'
             1720  LOAD_FAST                '_seisinfo'
             1722  LOAD_STR                 'XLStep'
             1724  BINARY_SUBSCR    
             1726  BINARY_MULTIPLY  
             1728  BINARY_ADD       

 L. 611      1730  LOAD_FAST                '_seisinfo'
             1732  LOAD_STR                 'XLEnd'
             1734  BINARY_SUBSCR    
             1736  LOAD_FAST                '_wdxl'
             1738  LOAD_FAST                '_seisinfo'
             1740  LOAD_STR                 'XLStep'
             1742  BINARY_SUBSCR    
             1744  BINARY_MULTIPLY  
             1746  BINARY_SUBTRACT  

 L. 612      1748  LOAD_FAST                '_seisinfo'
             1750  LOAD_STR                 'ZStart'
             1752  BINARY_SUBSCR    
             1754  LOAD_FAST                '_wdz'
             1756  LOAD_FAST                '_seisinfo'
             1758  LOAD_STR                 'ZStep'
             1760  BINARY_SUBSCR    
             1762  BINARY_MULTIPLY  
             1764  BINARY_ADD       

 L. 613      1766  LOAD_FAST                '_seisinfo'
             1768  LOAD_STR                 'ZEnd'
             1770  BINARY_SUBSCR    
             1772  LOAD_FAST                '_wdz'
             1774  LOAD_FAST                '_seisinfo'
             1776  LOAD_STR                 'ZStep'
             1778  BINARY_SUBSCR    
             1780  BINARY_MULTIPLY  
             1782  BINARY_SUBTRACT  
             1784  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1786  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1788  STORE_FAST               '_traindata'

 L. 616      1790  LOAD_GLOBAL              np
             1792  LOAD_METHOD              shape
             1794  LOAD_FAST                '_traindata'
             1796  CALL_METHOD_1         1  '1 positional argument'
             1798  LOAD_CONST               0
             1800  BINARY_SUBSCR    
             1802  LOAD_CONST               0
             1804  COMPARE_OP               <=
         1806_1808  POP_JUMP_IF_FALSE  1846  'to 1846'

 L. 617      1810  LOAD_GLOBAL              vis_msg
             1812  LOAD_ATTR                print
             1814  LOAD_STR                 'ERROR in TrainMl2DDCnnFromScratch: No training sample found'
             1816  LOAD_STR                 'error'
             1818  LOAD_CONST               ('type',)
             1820  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1822  POP_TOP          

 L. 618      1824  LOAD_GLOBAL              QtWidgets
             1826  LOAD_ATTR                QMessageBox
             1828  LOAD_METHOD              critical
             1830  LOAD_DEREF               'self'
             1832  LOAD_ATTR                msgbox

 L. 619      1834  LOAD_STR                 'Train 2D-DCNN'

 L. 620      1836  LOAD_STR                 'No training sample found'
             1838  CALL_METHOD_3         3  '3 positional arguments'
             1840  POP_TOP          

 L. 621      1842  LOAD_CONST               None
             1844  RETURN_VALUE     
           1846_0  COME_FROM          1806  '1806'

 L. 624      1846  LOAD_GLOBAL              print
             1848  LOAD_STR                 'TrainMl2DDcnnFromScratch: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 625      1850  LOAD_FAST                '_image_height'
             1852  LOAD_FAST                '_image_width'
             1854  LOAD_FAST                '_image_height_new'
             1856  LOAD_FAST                '_image_width_new'
             1858  BUILD_TUPLE_4         4 
             1860  BINARY_MODULO    
             1862  CALL_FUNCTION_1       1  '1 positional argument'
             1864  POP_TOP          

 L. 626      1866  BUILD_MAP_0           0 
             1868  STORE_FAST               '_traindict'

 L. 627      1870  SETUP_LOOP         1942  'to 1942'
             1872  LOAD_FAST                '_features'
             1874  GET_ITER         
             1876  FOR_ITER           1940  'to 1940'
             1878  STORE_FAST               'f'

 L. 628      1880  LOAD_DEREF               'self'
             1882  LOAD_ATTR                seisdata
             1884  LOAD_FAST                'f'
             1886  BINARY_SUBSCR    
             1888  STORE_FAST               '_seisdata'

 L. 629      1890  LOAD_GLOBAL              seis_ays
             1892  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1894  LOAD_FAST                '_seisdata'
             1896  LOAD_FAST                '_traindata'
             1898  LOAD_DEREF               'self'
             1900  LOAD_ATTR                survinfo

 L. 630      1902  LOAD_FAST                '_wdinl'
             1904  LOAD_FAST                '_wdxl'
             1906  LOAD_FAST                '_wdz'

 L. 631      1908  LOAD_CONST               False
             1910  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1912  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1914  LOAD_CONST               None
             1916  LOAD_CONST               None
             1918  BUILD_SLICE_2         2 
             1920  LOAD_CONST               3
             1922  LOAD_CONST               None
             1924  BUILD_SLICE_2         2 
             1926  BUILD_TUPLE_2         2 
             1928  BINARY_SUBSCR    
             1930  LOAD_FAST                '_traindict'
             1932  LOAD_FAST                'f'
             1934  STORE_SUBSCR     
         1936_1938  JUMP_BACK          1876  'to 1876'
             1940  POP_BLOCK        
           1942_0  COME_FROM_LOOP     1870  '1870'

 L. 632      1942  LOAD_FAST                '_target'
             1944  LOAD_FAST                '_features'
             1946  COMPARE_OP               not-in
         1948_1950  POP_JUMP_IF_FALSE  2008  'to 2008'

 L. 633      1952  LOAD_DEREF               'self'
             1954  LOAD_ATTR                seisdata
             1956  LOAD_FAST                '_target'
             1958  BINARY_SUBSCR    
             1960  STORE_FAST               '_seisdata'

 L. 634      1962  LOAD_GLOBAL              seis_ays
             1964  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1966  LOAD_FAST                '_seisdata'
             1968  LOAD_FAST                '_traindata'
             1970  LOAD_DEREF               'self'
             1972  LOAD_ATTR                survinfo

 L. 635      1974  LOAD_FAST                '_wdinl'

 L. 636      1976  LOAD_FAST                '_wdxl'

 L. 637      1978  LOAD_FAST                '_wdz'

 L. 638      1980  LOAD_CONST               False
             1982  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1984  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1986  LOAD_CONST               None
             1988  LOAD_CONST               None
             1990  BUILD_SLICE_2         2 
             1992  LOAD_CONST               3
             1994  LOAD_CONST               None
             1996  BUILD_SLICE_2         2 
             1998  BUILD_TUPLE_2         2 
             2000  BINARY_SUBSCR    
             2002  LOAD_FAST                '_traindict'
             2004  LOAD_FAST                '_target'
             2006  STORE_SUBSCR     
           2008_0  COME_FROM          1948  '1948'

 L. 640      2008  LOAD_DEREF               'self'
             2010  LOAD_ATTR                traindataconfig
             2012  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2014  BINARY_SUBSCR    
         2016_2018  POP_JUMP_IF_FALSE  2100  'to 2100'

 L. 641      2020  SETUP_LOOP         2100  'to 2100'
             2022  LOAD_FAST                '_features'
             2024  GET_ITER         
           2026_0  COME_FROM          2054  '2054'
             2026  FOR_ITER           2098  'to 2098'
             2028  STORE_FAST               'f'

 L. 642      2030  LOAD_GLOBAL              ml_aug
             2032  LOAD_METHOD              removeInvariantFeature
             2034  LOAD_FAST                '_traindict'
             2036  LOAD_FAST                'f'
             2038  CALL_METHOD_2         2  '2 positional arguments'
             2040  STORE_FAST               '_traindict'

 L. 643      2042  LOAD_GLOBAL              basic_mdt
             2044  LOAD_METHOD              maxDictConstantRow
             2046  LOAD_FAST                '_traindict'
             2048  CALL_METHOD_1         1  '1 positional argument'
             2050  LOAD_CONST               0
             2052  COMPARE_OP               <=
         2054_2056  POP_JUMP_IF_FALSE  2026  'to 2026'

 L. 644      2058  LOAD_GLOBAL              vis_msg
             2060  LOAD_ATTR                print
             2062  LOAD_STR                 'ERROR in TrainMl2DDcnnFromScratch: No training sample found'
             2064  LOAD_STR                 'error'
             2066  LOAD_CONST               ('type',)
             2068  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2070  POP_TOP          

 L. 645      2072  LOAD_GLOBAL              QtWidgets
             2074  LOAD_ATTR                QMessageBox
             2076  LOAD_METHOD              critical
             2078  LOAD_DEREF               'self'
             2080  LOAD_ATTR                msgbox

 L. 646      2082  LOAD_STR                 'Train 2D-DCNN'

 L. 647      2084  LOAD_STR                 'No training sample found'
             2086  CALL_METHOD_3         3  '3 positional arguments'
             2088  POP_TOP          

 L. 648      2090  LOAD_CONST               None
             2092  RETURN_VALUE     
         2094_2096  JUMP_BACK          2026  'to 2026'
             2098  POP_BLOCK        
           2100_0  COME_FROM_LOOP     2020  '2020'
           2100_1  COME_FROM          2016  '2016'

 L. 649      2100  LOAD_FAST                '_image_height_new'
             2102  LOAD_FAST                '_image_height'
             2104  COMPARE_OP               !=
         2106_2108  POP_JUMP_IF_TRUE   2120  'to 2120'
             2110  LOAD_FAST                '_image_width_new'
             2112  LOAD_FAST                '_image_width'
             2114  COMPARE_OP               !=
         2116_2118  POP_JUMP_IF_FALSE  2204  'to 2204'
           2120_0  COME_FROM          2106  '2106'

 L. 650      2120  SETUP_LOOP         2164  'to 2164'
             2122  LOAD_FAST                '_features'
             2124  GET_ITER         
             2126  FOR_ITER           2162  'to 2162'
             2128  STORE_FAST               'f'

 L. 651      2130  LOAD_GLOBAL              basic_image
             2132  LOAD_ATTR                changeImageSize
             2134  LOAD_FAST                '_traindict'
             2136  LOAD_FAST                'f'
             2138  BINARY_SUBSCR    

 L. 652      2140  LOAD_FAST                '_image_height'

 L. 653      2142  LOAD_FAST                '_image_width'

 L. 654      2144  LOAD_FAST                '_image_height_new'

 L. 655      2146  LOAD_FAST                '_image_width_new'
             2148  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2150  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2152  LOAD_FAST                '_traindict'
             2154  LOAD_FAST                'f'
             2156  STORE_SUBSCR     
         2158_2160  JUMP_BACK          2126  'to 2126'
             2162  POP_BLOCK        
           2164_0  COME_FROM_LOOP     2120  '2120'

 L. 656      2164  LOAD_FAST                '_target'
             2166  LOAD_FAST                '_features'
             2168  COMPARE_OP               not-in
         2170_2172  POP_JUMP_IF_FALSE  2204  'to 2204'

 L. 657      2174  LOAD_GLOBAL              basic_image
             2176  LOAD_ATTR                changeImageSize
             2178  LOAD_FAST                '_traindict'
             2180  LOAD_FAST                '_target'
             2182  BINARY_SUBSCR    

 L. 658      2184  LOAD_FAST                '_image_height'

 L. 659      2186  LOAD_FAST                '_image_width'

 L. 660      2188  LOAD_FAST                '_image_height_new'

 L. 661      2190  LOAD_FAST                '_image_width_new'
             2192  LOAD_STR                 'linear'
             2194  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2196  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2198  LOAD_FAST                '_traindict'
             2200  LOAD_FAST                '_target'
             2202  STORE_SUBSCR     
           2204_0  COME_FROM          2170  '2170'
           2204_1  COME_FROM          2116  '2116'

 L. 662      2204  LOAD_DEREF               'self'
             2206  LOAD_ATTR                traindataconfig
             2208  LOAD_STR                 'RotateFeature_Checked'
             2210  BINARY_SUBSCR    
             2212  LOAD_CONST               True
             2214  COMPARE_OP               is
         2216_2218  POP_JUMP_IF_FALSE  2358  'to 2358'

 L. 663      2220  SETUP_LOOP         2292  'to 2292'
             2222  LOAD_FAST                '_features'
             2224  GET_ITER         
             2226  FOR_ITER           2290  'to 2290'
             2228  STORE_FAST               'f'

 L. 664      2230  LOAD_FAST                '_image_height_new'
             2232  LOAD_FAST                '_image_width_new'
             2234  COMPARE_OP               ==
         2236_2238  POP_JUMP_IF_FALSE  2264  'to 2264'

 L. 665      2240  LOAD_GLOBAL              ml_aug
             2242  LOAD_METHOD              rotateImage6Way
             2244  LOAD_FAST                '_traindict'
             2246  LOAD_FAST                'f'
             2248  BINARY_SUBSCR    
             2250  LOAD_FAST                '_image_height_new'
             2252  LOAD_FAST                '_image_width_new'
             2254  CALL_METHOD_3         3  '3 positional arguments'
             2256  LOAD_FAST                '_traindict'
             2258  LOAD_FAST                'f'
             2260  STORE_SUBSCR     
             2262  JUMP_BACK          2226  'to 2226'
           2264_0  COME_FROM          2236  '2236'

 L. 667      2264  LOAD_GLOBAL              ml_aug
             2266  LOAD_METHOD              rotateImage4Way
             2268  LOAD_FAST                '_traindict'
             2270  LOAD_FAST                'f'
             2272  BINARY_SUBSCR    
             2274  LOAD_FAST                '_image_height_new'
             2276  LOAD_FAST                '_image_width_new'
             2278  CALL_METHOD_3         3  '3 positional arguments'
             2280  LOAD_FAST                '_traindict'
             2282  LOAD_FAST                'f'
             2284  STORE_SUBSCR     
         2286_2288  JUMP_BACK          2226  'to 2226'
             2290  POP_BLOCK        
           2292_0  COME_FROM_LOOP     2220  '2220'

 L. 668      2292  LOAD_FAST                '_target'
             2294  LOAD_FAST                '_features'
             2296  COMPARE_OP               not-in
         2298_2300  POP_JUMP_IF_FALSE  2358  'to 2358'

 L. 669      2302  LOAD_FAST                '_image_height_new'
             2304  LOAD_FAST                '_image_width_new'
             2306  COMPARE_OP               ==
         2308_2310  POP_JUMP_IF_FALSE  2336  'to 2336'

 L. 671      2312  LOAD_GLOBAL              ml_aug
             2314  LOAD_METHOD              rotateImage6Way
             2316  LOAD_FAST                '_traindict'
             2318  LOAD_FAST                '_target'
             2320  BINARY_SUBSCR    
             2322  LOAD_FAST                '_image_height_new'
             2324  LOAD_FAST                '_image_width_new'
             2326  CALL_METHOD_3         3  '3 positional arguments'
             2328  LOAD_FAST                '_traindict'
             2330  LOAD_FAST                '_target'
             2332  STORE_SUBSCR     
             2334  JUMP_FORWARD       2358  'to 2358'
           2336_0  COME_FROM          2308  '2308'

 L. 674      2336  LOAD_GLOBAL              ml_aug
             2338  LOAD_METHOD              rotateImage4Way
             2340  LOAD_FAST                '_traindict'
             2342  LOAD_FAST                '_target'
             2344  BINARY_SUBSCR    
             2346  LOAD_FAST                '_image_height_new'
             2348  LOAD_FAST                '_image_width_new'
             2350  CALL_METHOD_3         3  '3 positional arguments'
             2352  LOAD_FAST                '_traindict'
             2354  LOAD_FAST                '_target'
             2356  STORE_SUBSCR     
           2358_0  COME_FROM          2334  '2334'
           2358_1  COME_FROM          2298  '2298'
           2358_2  COME_FROM          2216  '2216'

 L. 676      2358  LOAD_GLOBAL              np
             2360  LOAD_METHOD              round
             2362  LOAD_FAST                '_traindict'
             2364  LOAD_FAST                '_target'
             2366  BINARY_SUBSCR    
             2368  CALL_METHOD_1         1  '1 positional argument'
             2370  LOAD_METHOD              astype
             2372  LOAD_GLOBAL              int
             2374  CALL_METHOD_1         1  '1 positional argument'
             2376  LOAD_FAST                '_traindict'
             2378  LOAD_FAST                '_target'
             2380  STORE_SUBSCR     

 L. 678      2382  LOAD_GLOBAL              print
             2384  LOAD_STR                 'TrainMl2DDcnnFromScratch: A total of %d valid training samples'
             2386  LOAD_GLOBAL              basic_mdt
             2388  LOAD_METHOD              maxDictConstantRow

 L. 679      2390  LOAD_FAST                '_traindict'
             2392  CALL_METHOD_1         1  '1 positional argument'
             2394  BINARY_MODULO    
             2396  CALL_FUNCTION_1       1  '1 positional argument'
             2398  POP_TOP          

 L. 681      2400  LOAD_GLOBAL              print
             2402  LOAD_STR                 'TrainMl2DDcnnFromScratch: Step 3 - Start training'
             2404  CALL_FUNCTION_1       1  '1 positional argument'
             2406  POP_TOP          

 L. 683      2408  LOAD_GLOBAL              QtWidgets
             2410  LOAD_METHOD              QProgressDialog
             2412  CALL_METHOD_0         0  '0 positional arguments'
             2414  STORE_FAST               '_pgsdlg'

 L. 684      2416  LOAD_GLOBAL              QtGui
             2418  LOAD_METHOD              QIcon
             2420  CALL_METHOD_0         0  '0 positional arguments'
             2422  STORE_FAST               'icon'

 L. 685      2424  LOAD_FAST                'icon'
             2426  LOAD_METHOD              addPixmap
             2428  LOAD_GLOBAL              QtGui
             2430  LOAD_METHOD              QPixmap
             2432  LOAD_GLOBAL              os
             2434  LOAD_ATTR                path
             2436  LOAD_METHOD              join
             2438  LOAD_DEREF               'self'
             2440  LOAD_ATTR                iconpath
             2442  LOAD_STR                 'icons/new.png'
             2444  CALL_METHOD_2         2  '2 positional arguments'
             2446  CALL_METHOD_1         1  '1 positional argument'

 L. 686      2448  LOAD_GLOBAL              QtGui
             2450  LOAD_ATTR                QIcon
             2452  LOAD_ATTR                Normal
             2454  LOAD_GLOBAL              QtGui
             2456  LOAD_ATTR                QIcon
             2458  LOAD_ATTR                Off
             2460  CALL_METHOD_3         3  '3 positional arguments'
             2462  POP_TOP          

 L. 687      2464  LOAD_FAST                '_pgsdlg'
             2466  LOAD_METHOD              setWindowIcon
             2468  LOAD_FAST                'icon'
             2470  CALL_METHOD_1         1  '1 positional argument'
             2472  POP_TOP          

 L. 688      2474  LOAD_FAST                '_pgsdlg'
             2476  LOAD_METHOD              setWindowTitle
             2478  LOAD_STR                 'Train 2D-DCNN'
             2480  CALL_METHOD_1         1  '1 positional argument'
             2482  POP_TOP          

 L. 689      2484  LOAD_FAST                '_pgsdlg'
             2486  LOAD_METHOD              setCancelButton
             2488  LOAD_CONST               None
             2490  CALL_METHOD_1         1  '1 positional argument'
             2492  POP_TOP          

 L. 690      2494  LOAD_FAST                '_pgsdlg'
             2496  LOAD_METHOD              setWindowFlags
             2498  LOAD_GLOBAL              QtCore
             2500  LOAD_ATTR                Qt
             2502  LOAD_ATTR                WindowStaysOnTopHint
             2504  CALL_METHOD_1         1  '1 positional argument'
             2506  POP_TOP          

 L. 691      2508  LOAD_FAST                '_pgsdlg'
             2510  LOAD_METHOD              forceShow
             2512  CALL_METHOD_0         0  '0 positional arguments'
             2514  POP_TOP          

 L. 692      2516  LOAD_FAST                '_pgsdlg'
             2518  LOAD_METHOD              setFixedWidth
             2520  LOAD_CONST               400
             2522  CALL_METHOD_1         1  '1 positional argument'
             2524  POP_TOP          

 L. 693      2526  LOAD_GLOBAL              ml_dcnn
             2528  LOAD_ATTR                createDCNNSegmentor
             2530  LOAD_FAST                '_traindict'

 L. 694      2532  LOAD_FAST                '_image_height_new'
             2534  LOAD_FAST                '_image_width_new'

 L. 695      2536  LOAD_FAST                '_features'
             2538  LOAD_FAST                '_target'

 L. 696      2540  LOAD_FAST                '_nepoch'
             2542  LOAD_FAST                '_batchsize'

 L. 697      2544  LOAD_FAST                '_nconvblock'
             2546  LOAD_FAST                '_nconvfeature'

 L. 698      2548  LOAD_FAST                '_nconvlayer'

 L. 699      2550  LOAD_FAST                '_n1x1layer'
             2552  LOAD_FAST                '_n1x1feature'

 L. 700      2554  LOAD_FAST                '_patch_height'
             2556  LOAD_FAST                '_patch_width'

 L. 701      2558  LOAD_FAST                '_pool_height'
             2560  LOAD_FAST                '_pool_width'

 L. 702      2562  LOAD_CONST               False

 L. 703      2564  LOAD_FAST                '_learning_rate'

 L. 704      2566  LOAD_FAST                '_dropout_prob'

 L. 705      2568  LOAD_CONST               True

 L. 706      2570  LOAD_FAST                '_savepath'
             2572  LOAD_FAST                '_savename'

 L. 707      2574  LOAD_FAST                '_pgsdlg'
             2576  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'nepoch', 'batchsize', 'nconvblock', 'nconvfeature', 'nconvlayer', 'n1x1layer', 'n1x1feature', 'patchheight', 'patchwidth', 'poolheight', 'poolwidth', 'batchnormalization', 'learningrate', 'dropoutprob', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2578  CALL_FUNCTION_KW_23    23  '23 total positional and keyword args'
             2580  STORE_FAST               '_dcnnlog'

 L. 710      2582  LOAD_GLOBAL              QtWidgets
             2584  LOAD_ATTR                QMessageBox
             2586  LOAD_METHOD              information
             2588  LOAD_DEREF               'self'
             2590  LOAD_ATTR                msgbox

 L. 711      2592  LOAD_STR                 'Train 2D-DCNN'

 L. 712      2594  LOAD_STR                 'DCNN trained successfully'
             2596  CALL_METHOD_3         3  '3 positional arguments'
             2598  POP_TOP          

 L. 714      2600  LOAD_GLOBAL              QtWidgets
             2602  LOAD_ATTR                QMessageBox
             2604  LOAD_METHOD              question
             2606  LOAD_DEREF               'self'
             2608  LOAD_ATTR                msgbox
             2610  LOAD_STR                 'Train 2D-DCNN'
             2612  LOAD_STR                 'View learning matrix?'

 L. 715      2614  LOAD_GLOBAL              QtWidgets
             2616  LOAD_ATTR                QMessageBox
             2618  LOAD_ATTR                Yes
             2620  LOAD_GLOBAL              QtWidgets
             2622  LOAD_ATTR                QMessageBox
             2624  LOAD_ATTR                No
             2626  BINARY_OR        

 L. 716      2628  LOAD_GLOBAL              QtWidgets
             2630  LOAD_ATTR                QMessageBox
             2632  LOAD_ATTR                Yes
             2634  CALL_METHOD_5         5  '5 positional arguments'
             2636  STORE_FAST               'reply'

 L. 718      2638  LOAD_FAST                'reply'
             2640  LOAD_GLOBAL              QtWidgets
             2642  LOAD_ATTR                QMessageBox
             2644  LOAD_ATTR                Yes
             2646  COMPARE_OP               ==
         2648_2650  POP_JUMP_IF_FALSE  2718  'to 2718'

 L. 719      2652  LOAD_GLOBAL              QtWidgets
             2654  LOAD_METHOD              QDialog
             2656  CALL_METHOD_0         0  '0 positional arguments'
             2658  STORE_FAST               '_viewmllearnmat'

 L. 720      2660  LOAD_GLOBAL              gui_viewmllearnmat
             2662  CALL_FUNCTION_0       0  '0 positional arguments'
             2664  STORE_FAST               '_gui'

 L. 721      2666  LOAD_FAST                '_dcnnlog'
             2668  LOAD_STR                 'learning_curve'
             2670  BINARY_SUBSCR    
             2672  LOAD_FAST                '_gui'
             2674  STORE_ATTR               learnmat

 L. 722      2676  LOAD_DEREF               'self'
             2678  LOAD_ATTR                linestyle
             2680  LOAD_FAST                '_gui'
             2682  STORE_ATTR               linestyle

 L. 723      2684  LOAD_DEREF               'self'
             2686  LOAD_ATTR                fontstyle
             2688  LOAD_FAST                '_gui'
             2690  STORE_ATTR               fontstyle

 L. 724      2692  LOAD_FAST                '_gui'
             2694  LOAD_METHOD              setupGUI
             2696  LOAD_FAST                '_viewmllearnmat'
             2698  CALL_METHOD_1         1  '1 positional argument'
             2700  POP_TOP          

 L. 725      2702  LOAD_FAST                '_viewmllearnmat'
             2704  LOAD_METHOD              exec
             2706  CALL_METHOD_0         0  '0 positional arguments'
             2708  POP_TOP          

 L. 726      2710  LOAD_FAST                '_viewmllearnmat'
             2712  LOAD_METHOD              show
             2714  CALL_METHOD_0         0  '0 positional arguments'
             2716  POP_TOP          
           2718_0  COME_FROM          2648  '2648'

Parse error at or near `POP_TOP' instruction at offset 2716

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
    TrainMl2DDcnnFromScratch = QtWidgets.QWidget()
    gui = trainml2ddcnnfromscratch()
    gui.setupGUI(TrainMl2DDcnnFromScratch)
    TrainMl2DDcnnFromScratch.show()
    sys.exit(app.exec_())