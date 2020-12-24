# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml2dcaefromscratch.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 43082 bytes
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
import cognitivegeo.src.ml.caereconstructor as ml_cae
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml2dcaefromscratch(object):
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

    def setupGUI(self, TrainMl2DCaeFromScratch):
        TrainMl2DCaeFromScratch.setObjectName('TrainMl2DCaeFromScratch')
        TrainMl2DCaeFromScratch.setFixedSize(810, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl2DCaeFromScratch.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl2DCaeFromScratch)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl2DCaeFromScratch)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl2DCaeFromScratch)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 50, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 50, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl2DCaeFromScratch)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 90, 180, 200))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 50, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 50, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(TrainMl2DCaeFromScratch)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 90, 180, 200))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 300, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 300, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 300, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 340, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 340, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 300, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 300, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 300, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 340, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 340, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl2DCaeFromScratch)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 310, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 350, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.lbldropout = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 390, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 390, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl2DCaeFromScratch)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl2DCaeFromScratch)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 440, 180, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl2DCaeFromScratch)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 440, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl2DCaeFromScratch)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl2DCaeFromScratch)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl2DCaeFromScratch.geometry().center().x()
        _center_y = TrainMl2DCaeFromScratch.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl2DCaeFromScratch)
        QtCore.QMetaObject.connectSlotsByName(TrainMl2DCaeFromScratch)

    def retranslateGUI(self, TrainMl2DCaeFromScratch):
        self.dialog = TrainMl2DCaeFromScratch
        _translate = QtCore.QCoreApplication.translate
        TrainMl2DCaeFromScratch.setWindowTitle(_translate('TrainMl2DCaeFromScratch', 'Train 2D-CAE from scratch'))
        self.lblfeature.setText(_translate('TrainMl2DCaeFromScratch', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl2DCaeFromScratch', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl2DCaeFromScratch', 'Select target:'))
        self.btnconfigtraindata.setText(_translate('TrainMl2DCaeFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('TrainMl2DCaeFromScratch', 'Original\nimage\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl2DCaeFromScratch', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl2DCaeFromScratch', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl2DCaeFromScratch', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl2DCaeFromScratch', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl2DCaeFromScratch', 'Interpolated\nimage\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl2DCaeFromScratch', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl2DCaeFromScratch', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl2DCaeFromScratch', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl2DCaeFromScratch', '32'))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        if self.checkSurvInfo() is True:
            self.featurelist.clear()
            self.lwgfeature.clear()
            self.cbbtarget.clear()
            _firstfeature = None
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    self.featurelist.append(i)
                    item = QtWidgets.QListWidgetItem(self.lwgfeature)
                    item.setText(_translate('TrainMl2DCaeFromScratch', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl2DCaeFromScratch', 'Specify CAE architecture:'))
        self.lblnconvblock.setText(_translate('TrainMl2DCaeFromScratch', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl2DCaeFromScratch', '3'))
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

        self.lbln1x1layer.setText(_translate('TrainMl2DCaeFromScratch', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('TrainMl2DCaeFromScratch', '2'))
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.twgn1x1layer.setRowCount(2)
        for _idx in range(int(self.ldtn1x1layer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl2DCaeFromScratch', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgn1x1layer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgn1x1layer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl2DCaeFromScratch', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl2DCaeFromScratch', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl2DCaeFromScratch', '3'))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('TrainMl2DCaeFromScratch', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl2DCaeFromScratch', '3'))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('TrainMl2DCaeFromScratch', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl2DCaeFromScratch', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl2DCaeFromScratch', '2'))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl2DCaeFromScratch', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl2DCaeFromScratch', '2'))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('TrainMl2DCaeFromScratch', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl2DCaeFromScratch', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl2DCaeFromScratch', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl2DCaeFromScratch', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl2DCaeFromScratch', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl2DCaeFromScratch', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl2DCaeFromScratch', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('TrainMl2DCaeFromScratch', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('TrainMl2DCaeFromScratch', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl2DCaeFromScratch', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl2DCaeFromScratch', ''))
        self.btnsave.setText(_translate('TrainMl2DCaeFromScratch', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl2DCaeFromScratch', 'Train 2D-CAE'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl2DCaeFromScratch)

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
        _file = _dialog.getSaveFileName(None, 'Save CAE Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
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

    def clickBtnTrainMl2DCaeFromScratch--- This code section failed: ---

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
               30  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 448        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 449        50  LOAD_STR                 'Train 2D-CAE'

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
              162  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 460       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 461       182  LOAD_STR                 'Train 2D-CAE'

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
              232  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 467       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 468       252  LOAD_STR                 'Train 2D-CAE'

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
              316  LOAD_STR                 'trainml2dcaefromscratch.clickBtnTrainMl2DCaeFromScratch.<locals>.<listcomp>'
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

 L. 479       344  LOAD_GLOBAL              basic_data
              346  LOAD_METHOD              str2int
              348  LOAD_DEREF               'self'
              350  LOAD_ATTR                ldtnconvblock
              352  LOAD_METHOD              text
              354  CALL_METHOD_0         0  '0 positional arguments'
              356  CALL_METHOD_1         1  '1 positional argument'
              358  STORE_FAST               '_nconvblock'

 L. 480       360  LOAD_CLOSURE             'self'
              362  BUILD_TUPLE_1         1 
              364  LOAD_LISTCOMP            '<code_object <listcomp>>'
              366  LOAD_STR                 'trainml2dcaefromscratch.clickBtnTrainMl2DCaeFromScratch.<locals>.<listcomp>'
              368  MAKE_FUNCTION_8          'closure'
              370  LOAD_GLOBAL              range
              372  LOAD_FAST                '_nconvblock'
              374  CALL_FUNCTION_1       1  '1 positional argument'
              376  GET_ITER         
              378  CALL_FUNCTION_1       1  '1 positional argument'
              380  STORE_FAST               '_nconvlayer'

 L. 481       382  LOAD_CLOSURE             'self'
              384  BUILD_TUPLE_1         1 
              386  LOAD_LISTCOMP            '<code_object <listcomp>>'
              388  LOAD_STR                 'trainml2dcaefromscratch.clickBtnTrainMl2DCaeFromScratch.<locals>.<listcomp>'
              390  MAKE_FUNCTION_8          'closure'
              392  LOAD_GLOBAL              range
              394  LOAD_FAST                '_nconvblock'
              396  CALL_FUNCTION_1       1  '1 positional argument'
              398  GET_ITER         
              400  CALL_FUNCTION_1       1  '1 positional argument'
              402  STORE_FAST               '_nconvfeature'

 L. 482       404  LOAD_GLOBAL              basic_data
              406  LOAD_METHOD              str2int
              408  LOAD_DEREF               'self'
              410  LOAD_ATTR                ldtn1x1layer
              412  LOAD_METHOD              text
              414  CALL_METHOD_0         0  '0 positional arguments'
              416  CALL_METHOD_1         1  '1 positional argument'
              418  STORE_FAST               '_n1x1layer'

 L. 483       420  LOAD_CLOSURE             'self'
              422  BUILD_TUPLE_1         1 
              424  LOAD_LISTCOMP            '<code_object <listcomp>>'
              426  LOAD_STR                 'trainml2dcaefromscratch.clickBtnTrainMl2DCaeFromScratch.<locals>.<listcomp>'
              428  MAKE_FUNCTION_8          'closure'
              430  LOAD_GLOBAL              range
              432  LOAD_FAST                '_n1x1layer'
              434  CALL_FUNCTION_1       1  '1 positional argument'
              436  GET_ITER         
              438  CALL_FUNCTION_1       1  '1 positional argument'
              440  STORE_FAST               '_n1x1feature'

 L. 484       442  LOAD_GLOBAL              basic_data
              444  LOAD_METHOD              str2int
              446  LOAD_DEREF               'self'
              448  LOAD_ATTR                ldtmaskheight
              450  LOAD_METHOD              text
              452  CALL_METHOD_0         0  '0 positional arguments'
              454  CALL_METHOD_1         1  '1 positional argument'
              456  STORE_FAST               '_patch_height'

 L. 485       458  LOAD_GLOBAL              basic_data
              460  LOAD_METHOD              str2int
              462  LOAD_DEREF               'self'
              464  LOAD_ATTR                ldtmaskwidth
              466  LOAD_METHOD              text
              468  CALL_METHOD_0         0  '0 positional arguments'
              470  CALL_METHOD_1         1  '1 positional argument'
              472  STORE_FAST               '_patch_width'

 L. 486       474  LOAD_GLOBAL              basic_data
              476  LOAD_METHOD              str2int
              478  LOAD_DEREF               'self'
              480  LOAD_ATTR                ldtpoolheight
              482  LOAD_METHOD              text
              484  CALL_METHOD_0         0  '0 positional arguments'
              486  CALL_METHOD_1         1  '1 positional argument'
              488  STORE_FAST               '_pool_height'

 L. 487       490  LOAD_GLOBAL              basic_data
              492  LOAD_METHOD              str2int
              494  LOAD_DEREF               'self'
              496  LOAD_ATTR                ldtpoolwidth
              498  LOAD_METHOD              text
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  CALL_METHOD_1         1  '1 positional argument'
              504  STORE_FAST               '_pool_width'

 L. 488       506  LOAD_GLOBAL              basic_data
              508  LOAD_METHOD              str2int
              510  LOAD_DEREF               'self'
              512  LOAD_ATTR                ldtnepoch
              514  LOAD_METHOD              text
              516  CALL_METHOD_0         0  '0 positional arguments'
              518  CALL_METHOD_1         1  '1 positional argument'
              520  STORE_FAST               '_nepoch'

 L. 489       522  LOAD_GLOBAL              basic_data
              524  LOAD_METHOD              str2int
              526  LOAD_DEREF               'self'
              528  LOAD_ATTR                ldtbatchsize
              530  LOAD_METHOD              text
              532  CALL_METHOD_0         0  '0 positional arguments'
              534  CALL_METHOD_1         1  '1 positional argument'
              536  STORE_FAST               '_batchsize'

 L. 490       538  LOAD_GLOBAL              basic_data
              540  LOAD_METHOD              str2float
              542  LOAD_DEREF               'self'
              544  LOAD_ATTR                ldtlearnrate
              546  LOAD_METHOD              text
              548  CALL_METHOD_0         0  '0 positional arguments'
              550  CALL_METHOD_1         1  '1 positional argument'
              552  STORE_FAST               '_learning_rate'

 L. 491       554  LOAD_GLOBAL              basic_data
              556  LOAD_METHOD              str2float
              558  LOAD_DEREF               'self'
              560  LOAD_ATTR                ldtdropout
              562  LOAD_METHOD              text
              564  CALL_METHOD_0         0  '0 positional arguments'
              566  CALL_METHOD_1         1  '1 positional argument'
              568  STORE_FAST               '_dropout_prob'

 L. 492       570  LOAD_FAST                '_nconvblock'
              572  LOAD_CONST               False
              574  COMPARE_OP               is
          576_578  POP_JUMP_IF_TRUE    590  'to 590'
              580  LOAD_FAST                '_nconvblock'
              582  LOAD_CONST               0
              584  COMPARE_OP               <=
          586_588  POP_JUMP_IF_FALSE   626  'to 626'
            590_0  COME_FROM           576  '576'

 L. 493       590  LOAD_GLOBAL              vis_msg
              592  LOAD_ATTR                print
              594  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: Non-positive convolutional block number'

 L. 494       596  LOAD_STR                 'error'
              598  LOAD_CONST               ('type',)
              600  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              602  POP_TOP          

 L. 495       604  LOAD_GLOBAL              QtWidgets
              606  LOAD_ATTR                QMessageBox
              608  LOAD_METHOD              critical
              610  LOAD_DEREF               'self'
              612  LOAD_ATTR                msgbox

 L. 496       614  LOAD_STR                 'Train 2D-CAE'

 L. 497       616  LOAD_STR                 'Non-positive convolutional block number'
              618  CALL_METHOD_3         3  '3 positional arguments'
              620  POP_TOP          

 L. 498       622  LOAD_CONST               None
              624  RETURN_VALUE     
            626_0  COME_FROM           586  '586'

 L. 499       626  SETUP_LOOP          698  'to 698'
              628  LOAD_FAST                '_nconvlayer'
              630  GET_ITER         
            632_0  COME_FROM           652  '652'
              632  FOR_ITER            696  'to 696'
              634  STORE_FAST               '_i'

 L. 500       636  LOAD_FAST                '_i'
              638  LOAD_CONST               False
              640  COMPARE_OP               is
          642_644  POP_JUMP_IF_TRUE    656  'to 656'
              646  LOAD_FAST                '_i'
              648  LOAD_CONST               1
              650  COMPARE_OP               <
          652_654  POP_JUMP_IF_FALSE   632  'to 632'
            656_0  COME_FROM           642  '642'

 L. 501       656  LOAD_GLOBAL              vis_msg
              658  LOAD_ATTR                print
              660  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: Non-positive convolutional layer number'

 L. 502       662  LOAD_STR                 'error'
              664  LOAD_CONST               ('type',)
              666  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              668  POP_TOP          

 L. 503       670  LOAD_GLOBAL              QtWidgets
              672  LOAD_ATTR                QMessageBox
              674  LOAD_METHOD              critical
              676  LOAD_DEREF               'self'
              678  LOAD_ATTR                msgbox

 L. 504       680  LOAD_STR                 'Train 2D-CAE'

 L. 505       682  LOAD_STR                 'Non-positive convolutional layer number'
              684  CALL_METHOD_3         3  '3 positional arguments'
              686  POP_TOP          

 L. 506       688  LOAD_CONST               None
              690  RETURN_VALUE     
          692_694  JUMP_BACK           632  'to 632'
              696  POP_BLOCK        
            698_0  COME_FROM_LOOP      626  '626'

 L. 507       698  SETUP_LOOP          770  'to 770'
              700  LOAD_FAST                '_nconvfeature'
              702  GET_ITER         
            704_0  COME_FROM           724  '724'
              704  FOR_ITER            768  'to 768'
              706  STORE_FAST               '_i'

 L. 508       708  LOAD_FAST                '_i'
              710  LOAD_CONST               False
              712  COMPARE_OP               is
          714_716  POP_JUMP_IF_TRUE    728  'to 728'
              718  LOAD_FAST                '_i'
              720  LOAD_CONST               1
              722  COMPARE_OP               <
          724_726  POP_JUMP_IF_FALSE   704  'to 704'
            728_0  COME_FROM           714  '714'

 L. 509       728  LOAD_GLOBAL              vis_msg
              730  LOAD_ATTR                print
              732  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: Non-positive convolutional feature number'

 L. 510       734  LOAD_STR                 'error'
              736  LOAD_CONST               ('type',)
              738  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              740  POP_TOP          

 L. 511       742  LOAD_GLOBAL              QtWidgets
              744  LOAD_ATTR                QMessageBox
              746  LOAD_METHOD              critical
              748  LOAD_DEREF               'self'
              750  LOAD_ATTR                msgbox

 L. 512       752  LOAD_STR                 'Train 2D-CAE'

 L. 513       754  LOAD_STR                 'Non-positive convolutional feature number'
              756  CALL_METHOD_3         3  '3 positional arguments'
              758  POP_TOP          

 L. 514       760  LOAD_CONST               None
              762  RETURN_VALUE     
          764_766  JUMP_BACK           704  'to 704'
              768  POP_BLOCK        
            770_0  COME_FROM_LOOP      698  '698'

 L. 515       770  LOAD_FAST                '_n1x1layer'
              772  LOAD_CONST               False
              774  COMPARE_OP               is
          776_778  POP_JUMP_IF_TRUE    790  'to 790'
              780  LOAD_FAST                '_n1x1layer'
              782  LOAD_CONST               0
              784  COMPARE_OP               <=
          786_788  POP_JUMP_IF_FALSE   826  'to 826'
            790_0  COME_FROM           776  '776'

 L. 516       790  LOAD_GLOBAL              vis_msg
              792  LOAD_ATTR                print
              794  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: Non-positive 1x1 convolutional layer number'

 L. 517       796  LOAD_STR                 'error'
              798  LOAD_CONST               ('type',)
              800  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              802  POP_TOP          

 L. 518       804  LOAD_GLOBAL              QtWidgets
              806  LOAD_ATTR                QMessageBox
              808  LOAD_METHOD              critical
              810  LOAD_DEREF               'self'
              812  LOAD_ATTR                msgbox

 L. 519       814  LOAD_STR                 'Train 2D-CAE'

 L. 520       816  LOAD_STR                 'Non-positive 1x1 convolutional layer number'
              818  CALL_METHOD_3         3  '3 positional arguments'
              820  POP_TOP          

 L. 521       822  LOAD_CONST               None
              824  RETURN_VALUE     
            826_0  COME_FROM           786  '786'

 L. 522       826  SETUP_LOOP          898  'to 898'
              828  LOAD_FAST                '_n1x1feature'
              830  GET_ITER         
            832_0  COME_FROM           852  '852'
              832  FOR_ITER            896  'to 896'
              834  STORE_FAST               '_i'

 L. 523       836  LOAD_FAST                '_i'
              838  LOAD_CONST               False
              840  COMPARE_OP               is
          842_844  POP_JUMP_IF_TRUE    856  'to 856'
              846  LOAD_FAST                '_i'
              848  LOAD_CONST               1
              850  COMPARE_OP               <
          852_854  POP_JUMP_IF_FALSE   832  'to 832'
            856_0  COME_FROM           842  '842'

 L. 524       856  LOAD_GLOBAL              vis_msg
              858  LOAD_ATTR                print
              860  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: Non-positive 1x1 convolutional feature number'

 L. 525       862  LOAD_STR                 'error'
              864  LOAD_CONST               ('type',)
              866  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              868  POP_TOP          

 L. 526       870  LOAD_GLOBAL              QtWidgets
              872  LOAD_ATTR                QMessageBox
              874  LOAD_METHOD              critical
              876  LOAD_DEREF               'self'
              878  LOAD_ATTR                msgbox

 L. 527       880  LOAD_STR                 'Train 2D-CAE'

 L. 528       882  LOAD_STR                 'Non-positive 1x1 convolutional feature number'
              884  CALL_METHOD_3         3  '3 positional arguments'
              886  POP_TOP          

 L. 529       888  LOAD_CONST               None
              890  RETURN_VALUE     
          892_894  JUMP_BACK           832  'to 832'
              896  POP_BLOCK        
            898_0  COME_FROM_LOOP      826  '826'

 L. 530       898  LOAD_FAST                '_patch_height'
              900  LOAD_CONST               False
              902  COMPARE_OP               is
          904_906  POP_JUMP_IF_TRUE    938  'to 938'
              908  LOAD_FAST                '_patch_width'
              910  LOAD_CONST               False
              912  COMPARE_OP               is
          914_916  POP_JUMP_IF_TRUE    938  'to 938'

 L. 531       918  LOAD_FAST                '_patch_height'
              920  LOAD_CONST               1
              922  COMPARE_OP               <
          924_926  POP_JUMP_IF_TRUE    938  'to 938'
              928  LOAD_FAST                '_patch_width'
              930  LOAD_CONST               1
              932  COMPARE_OP               <
          934_936  POP_JUMP_IF_FALSE   974  'to 974'
            938_0  COME_FROM           924  '924'
            938_1  COME_FROM           914  '914'
            938_2  COME_FROM           904  '904'

 L. 532       938  LOAD_GLOBAL              vis_msg
              940  LOAD_ATTR                print
              942  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: Non-positive convolutional patch size'

 L. 533       944  LOAD_STR                 'error'
              946  LOAD_CONST               ('type',)
              948  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              950  POP_TOP          

 L. 534       952  LOAD_GLOBAL              QtWidgets
              954  LOAD_ATTR                QMessageBox
              956  LOAD_METHOD              critical
              958  LOAD_DEREF               'self'
              960  LOAD_ATTR                msgbox

 L. 535       962  LOAD_STR                 'Train 2D-CAE'

 L. 536       964  LOAD_STR                 'Non-positive convolutional patch size'
              966  CALL_METHOD_3         3  '3 positional arguments'
              968  POP_TOP          

 L. 537       970  LOAD_CONST               None
              972  RETURN_VALUE     
            974_0  COME_FROM           934  '934'

 L. 538       974  LOAD_FAST                '_pool_height'
              976  LOAD_CONST               False
              978  COMPARE_OP               is
          980_982  POP_JUMP_IF_TRUE   1014  'to 1014'
              984  LOAD_FAST                '_pool_width'
              986  LOAD_CONST               False
              988  COMPARE_OP               is
          990_992  POP_JUMP_IF_TRUE   1014  'to 1014'

 L. 539       994  LOAD_FAST                '_pool_height'
              996  LOAD_CONST               1
              998  COMPARE_OP               <
         1000_1002  POP_JUMP_IF_TRUE   1014  'to 1014'
             1004  LOAD_FAST                '_pool_width'
             1006  LOAD_CONST               1
             1008  COMPARE_OP               <
         1010_1012  POP_JUMP_IF_FALSE  1050  'to 1050'
           1014_0  COME_FROM          1000  '1000'
           1014_1  COME_FROM           990  '990'
           1014_2  COME_FROM           980  '980'

 L. 540      1014  LOAD_GLOBAL              vis_msg
             1016  LOAD_ATTR                print
             1018  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: Non-positive pooling size'
             1020  LOAD_STR                 'error'
             1022  LOAD_CONST               ('type',)
             1024  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1026  POP_TOP          

 L. 541      1028  LOAD_GLOBAL              QtWidgets
             1030  LOAD_ATTR                QMessageBox
             1032  LOAD_METHOD              critical
             1034  LOAD_DEREF               'self'
             1036  LOAD_ATTR                msgbox

 L. 542      1038  LOAD_STR                 'Train 2D-CAE'

 L. 543      1040  LOAD_STR                 'Non-positive pooling size'
             1042  CALL_METHOD_3         3  '3 positional arguments'
             1044  POP_TOP          

 L. 544      1046  LOAD_CONST               None
             1048  RETURN_VALUE     
           1050_0  COME_FROM          1010  '1010'

 L. 545      1050  LOAD_FAST                '_nepoch'
             1052  LOAD_CONST               False
             1054  COMPARE_OP               is
         1056_1058  POP_JUMP_IF_TRUE   1070  'to 1070'
             1060  LOAD_FAST                '_nepoch'
             1062  LOAD_CONST               0
             1064  COMPARE_OP               <=
         1066_1068  POP_JUMP_IF_FALSE  1106  'to 1106'
           1070_0  COME_FROM          1056  '1056'

 L. 546      1070  LOAD_GLOBAL              vis_msg
             1072  LOAD_ATTR                print
             1074  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: Non-positive epoch number'
             1076  LOAD_STR                 'error'
             1078  LOAD_CONST               ('type',)
             1080  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1082  POP_TOP          

 L. 547      1084  LOAD_GLOBAL              QtWidgets
             1086  LOAD_ATTR                QMessageBox
             1088  LOAD_METHOD              critical
             1090  LOAD_DEREF               'self'
             1092  LOAD_ATTR                msgbox

 L. 548      1094  LOAD_STR                 'Train 2D-CAE'

 L. 549      1096  LOAD_STR                 'Non-positive epoch number'
             1098  CALL_METHOD_3         3  '3 positional arguments'
             1100  POP_TOP          

 L. 550      1102  LOAD_CONST               None
             1104  RETURN_VALUE     
           1106_0  COME_FROM          1066  '1066'

 L. 551      1106  LOAD_FAST                '_batchsize'
             1108  LOAD_CONST               False
             1110  COMPARE_OP               is
         1112_1114  POP_JUMP_IF_TRUE   1126  'to 1126'
             1116  LOAD_FAST                '_batchsize'
             1118  LOAD_CONST               0
             1120  COMPARE_OP               <=
         1122_1124  POP_JUMP_IF_FALSE  1162  'to 1162'
           1126_0  COME_FROM          1112  '1112'

 L. 552      1126  LOAD_GLOBAL              vis_msg
             1128  LOAD_ATTR                print
             1130  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: Non-positive batch size'
             1132  LOAD_STR                 'error'
             1134  LOAD_CONST               ('type',)
             1136  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1138  POP_TOP          

 L. 553      1140  LOAD_GLOBAL              QtWidgets
             1142  LOAD_ATTR                QMessageBox
             1144  LOAD_METHOD              critical
             1146  LOAD_DEREF               'self'
             1148  LOAD_ATTR                msgbox

 L. 554      1150  LOAD_STR                 'Train 2D-CAE'

 L. 555      1152  LOAD_STR                 'Non-positive batch size'
             1154  CALL_METHOD_3         3  '3 positional arguments'
             1156  POP_TOP          

 L. 556      1158  LOAD_CONST               None
             1160  RETURN_VALUE     
           1162_0  COME_FROM          1122  '1122'

 L. 557      1162  LOAD_FAST                '_learning_rate'
             1164  LOAD_CONST               False
             1166  COMPARE_OP               is
         1168_1170  POP_JUMP_IF_TRUE   1182  'to 1182'
             1172  LOAD_FAST                '_learning_rate'
             1174  LOAD_CONST               0
             1176  COMPARE_OP               <=
         1178_1180  POP_JUMP_IF_FALSE  1218  'to 1218'
           1182_0  COME_FROM          1168  '1168'

 L. 558      1182  LOAD_GLOBAL              vis_msg
             1184  LOAD_ATTR                print
             1186  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: Non-positive learning rate'
             1188  LOAD_STR                 'error'
             1190  LOAD_CONST               ('type',)
             1192  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1194  POP_TOP          

 L. 559      1196  LOAD_GLOBAL              QtWidgets
             1198  LOAD_ATTR                QMessageBox
             1200  LOAD_METHOD              critical
             1202  LOAD_DEREF               'self'
             1204  LOAD_ATTR                msgbox

 L. 560      1206  LOAD_STR                 'Train 2D-CAE'

 L. 561      1208  LOAD_STR                 'Non-positive learning rate'
             1210  CALL_METHOD_3         3  '3 positional arguments'
             1212  POP_TOP          

 L. 562      1214  LOAD_CONST               None
             1216  RETURN_VALUE     
           1218_0  COME_FROM          1178  '1178'

 L. 563      1218  LOAD_FAST                '_dropout_prob'
             1220  LOAD_CONST               False
             1222  COMPARE_OP               is
         1224_1226  POP_JUMP_IF_TRUE   1238  'to 1238'
             1228  LOAD_FAST                '_dropout_prob'
             1230  LOAD_CONST               0
             1232  COMPARE_OP               <=
         1234_1236  POP_JUMP_IF_FALSE  1274  'to 1274'
           1238_0  COME_FROM          1224  '1224'

 L. 564      1238  LOAD_GLOBAL              vis_msg
             1240  LOAD_ATTR                print
             1242  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: Negative dropout rate'
             1244  LOAD_STR                 'error'
             1246  LOAD_CONST               ('type',)
             1248  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1250  POP_TOP          

 L. 565      1252  LOAD_GLOBAL              QtWidgets
             1254  LOAD_ATTR                QMessageBox
             1256  LOAD_METHOD              critical
             1258  LOAD_DEREF               'self'
             1260  LOAD_ATTR                msgbox

 L. 566      1262  LOAD_STR                 'Train 2D-CAE'

 L. 567      1264  LOAD_STR                 'Negative dropout rate'
             1266  CALL_METHOD_3         3  '3 positional arguments'
             1268  POP_TOP          

 L. 568      1270  LOAD_CONST               None
             1272  RETURN_VALUE     
           1274_0  COME_FROM          1234  '1234'

 L. 570      1274  LOAD_GLOBAL              len
             1276  LOAD_DEREF               'self'
             1278  LOAD_ATTR                ldtsave
             1280  LOAD_METHOD              text
             1282  CALL_METHOD_0         0  '0 positional arguments'
             1284  CALL_FUNCTION_1       1  '1 positional argument'
             1286  LOAD_CONST               1
             1288  COMPARE_OP               <
         1290_1292  POP_JUMP_IF_FALSE  1330  'to 1330'

 L. 571      1294  LOAD_GLOBAL              vis_msg
             1296  LOAD_ATTR                print
             1298  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: No name specified for CAE network'
             1300  LOAD_STR                 'error'
             1302  LOAD_CONST               ('type',)
             1304  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1306  POP_TOP          

 L. 572      1308  LOAD_GLOBAL              QtWidgets
             1310  LOAD_ATTR                QMessageBox
             1312  LOAD_METHOD              critical
             1314  LOAD_DEREF               'self'
             1316  LOAD_ATTR                msgbox

 L. 573      1318  LOAD_STR                 'Train 2D-CAE'

 L. 574      1320  LOAD_STR                 'No name specified for CAE network'
             1322  CALL_METHOD_3         3  '3 positional arguments'
             1324  POP_TOP          

 L. 575      1326  LOAD_CONST               None
             1328  RETURN_VALUE     
           1330_0  COME_FROM          1290  '1290'

 L. 576      1330  LOAD_GLOBAL              os
             1332  LOAD_ATTR                path
             1334  LOAD_METHOD              dirname
             1336  LOAD_DEREF               'self'
             1338  LOAD_ATTR                ldtsave
             1340  LOAD_METHOD              text
             1342  CALL_METHOD_0         0  '0 positional arguments'
             1344  CALL_METHOD_1         1  '1 positional argument'
             1346  STORE_FAST               '_savepath'

 L. 577      1348  LOAD_GLOBAL              os
             1350  LOAD_ATTR                path
             1352  LOAD_METHOD              splitext
             1354  LOAD_GLOBAL              os
             1356  LOAD_ATTR                path
             1358  LOAD_METHOD              basename
             1360  LOAD_DEREF               'self'
             1362  LOAD_ATTR                ldtsave
             1364  LOAD_METHOD              text
             1366  CALL_METHOD_0         0  '0 positional arguments'
             1368  CALL_METHOD_1         1  '1 positional argument'
             1370  CALL_METHOD_1         1  '1 positional argument'
             1372  LOAD_CONST               0
             1374  BINARY_SUBSCR    
             1376  STORE_FAST               '_savename'

 L. 579      1378  LOAD_CONST               0
             1380  STORE_FAST               '_wdinl'

 L. 580      1382  LOAD_CONST               0
             1384  STORE_FAST               '_wdxl'

 L. 581      1386  LOAD_CONST               0
             1388  STORE_FAST               '_wdz'

 L. 582      1390  LOAD_DEREF               'self'
             1392  LOAD_ATTR                cbbornt
             1394  LOAD_METHOD              currentIndex
             1396  CALL_METHOD_0         0  '0 positional arguments'
             1398  LOAD_CONST               0
             1400  COMPARE_OP               ==
         1402_1404  POP_JUMP_IF_FALSE  1430  'to 1430'

 L. 583      1406  LOAD_GLOBAL              int
             1408  LOAD_FAST                '_image_width'
             1410  LOAD_CONST               2
             1412  BINARY_TRUE_DIVIDE
             1414  CALL_FUNCTION_1       1  '1 positional argument'
             1416  STORE_FAST               '_wdxl'

 L. 584      1418  LOAD_GLOBAL              int
             1420  LOAD_FAST                '_image_height'
             1422  LOAD_CONST               2
             1424  BINARY_TRUE_DIVIDE
             1426  CALL_FUNCTION_1       1  '1 positional argument'
             1428  STORE_FAST               '_wdz'
           1430_0  COME_FROM          1402  '1402'

 L. 585      1430  LOAD_DEREF               'self'
             1432  LOAD_ATTR                cbbornt
             1434  LOAD_METHOD              currentIndex
             1436  CALL_METHOD_0         0  '0 positional arguments'
             1438  LOAD_CONST               1
             1440  COMPARE_OP               ==
         1442_1444  POP_JUMP_IF_FALSE  1470  'to 1470'

 L. 586      1446  LOAD_GLOBAL              int
             1448  LOAD_FAST                '_image_width'
             1450  LOAD_CONST               2
             1452  BINARY_TRUE_DIVIDE
             1454  CALL_FUNCTION_1       1  '1 positional argument'
             1456  STORE_FAST               '_wdinl'

 L. 587      1458  LOAD_GLOBAL              int
             1460  LOAD_FAST                '_image_height'
             1462  LOAD_CONST               2
             1464  BINARY_TRUE_DIVIDE
             1466  CALL_FUNCTION_1       1  '1 positional argument'
             1468  STORE_FAST               '_wdz'
           1470_0  COME_FROM          1442  '1442'

 L. 588      1470  LOAD_DEREF               'self'
             1472  LOAD_ATTR                cbbornt
             1474  LOAD_METHOD              currentIndex
             1476  CALL_METHOD_0         0  '0 positional arguments'
             1478  LOAD_CONST               2
             1480  COMPARE_OP               ==
         1482_1484  POP_JUMP_IF_FALSE  1510  'to 1510'

 L. 589      1486  LOAD_GLOBAL              int
             1488  LOAD_FAST                '_image_width'
             1490  LOAD_CONST               2
             1492  BINARY_TRUE_DIVIDE
             1494  CALL_FUNCTION_1       1  '1 positional argument'
             1496  STORE_FAST               '_wdinl'

 L. 590      1498  LOAD_GLOBAL              int
             1500  LOAD_FAST                '_image_height'
             1502  LOAD_CONST               2
             1504  BINARY_TRUE_DIVIDE
             1506  CALL_FUNCTION_1       1  '1 positional argument'
             1508  STORE_FAST               '_wdxl'
           1510_0  COME_FROM          1482  '1482'

 L. 592      1510  LOAD_DEREF               'self'
             1512  LOAD_ATTR                survinfo
             1514  STORE_FAST               '_seisinfo'

 L. 594      1516  LOAD_GLOBAL              print
             1518  LOAD_STR                 'TrainMl2DCaeFromScratch: Step 1 - Get training samples:'
             1520  CALL_FUNCTION_1       1  '1 positional argument'
             1522  POP_TOP          

 L. 595      1524  LOAD_DEREF               'self'
             1526  LOAD_ATTR                traindataconfig
             1528  LOAD_STR                 'TrainPointSet'
             1530  BINARY_SUBSCR    
             1532  STORE_FAST               '_trainpoint'

 L. 596      1534  LOAD_GLOBAL              np
             1536  LOAD_METHOD              zeros
             1538  LOAD_CONST               0
             1540  LOAD_CONST               3
             1542  BUILD_LIST_2          2 
             1544  CALL_METHOD_1         1  '1 positional argument'
             1546  STORE_FAST               '_traindata'

 L. 597      1548  SETUP_LOOP         1624  'to 1624'
             1550  LOAD_FAST                '_trainpoint'
             1552  GET_ITER         
           1554_0  COME_FROM          1572  '1572'
             1554  FOR_ITER           1622  'to 1622'
             1556  STORE_FAST               '_p'

 L. 598      1558  LOAD_GLOBAL              point_ays
             1560  LOAD_METHOD              checkPoint
             1562  LOAD_DEREF               'self'
             1564  LOAD_ATTR                pointsetdata
             1566  LOAD_FAST                '_p'
             1568  BINARY_SUBSCR    
             1570  CALL_METHOD_1         1  '1 positional argument'
         1572_1574  POP_JUMP_IF_FALSE  1554  'to 1554'

 L. 599      1576  LOAD_GLOBAL              basic_mdt
             1578  LOAD_METHOD              exportMatDict
             1580  LOAD_DEREF               'self'
             1582  LOAD_ATTR                pointsetdata
             1584  LOAD_FAST                '_p'
             1586  BINARY_SUBSCR    
             1588  LOAD_STR                 'Inline'
             1590  LOAD_STR                 'Crossline'
             1592  LOAD_STR                 'Z'
             1594  BUILD_LIST_3          3 
             1596  CALL_METHOD_2         2  '2 positional arguments'
             1598  STORE_FAST               '_pt'

 L. 600      1600  LOAD_GLOBAL              np
             1602  LOAD_ATTR                concatenate
             1604  LOAD_FAST                '_traindata'
             1606  LOAD_FAST                '_pt'
             1608  BUILD_TUPLE_2         2 
             1610  LOAD_CONST               0
             1612  LOAD_CONST               ('axis',)
             1614  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1616  STORE_FAST               '_traindata'
         1618_1620  JUMP_BACK          1554  'to 1554'
             1622  POP_BLOCK        
           1624_0  COME_FROM_LOOP     1548  '1548'

 L. 601      1624  LOAD_GLOBAL              seis_ays
             1626  LOAD_ATTR                removeOutofSurveySample
             1628  LOAD_FAST                '_traindata'

 L. 602      1630  LOAD_FAST                '_seisinfo'
             1632  LOAD_STR                 'ILStart'
             1634  BINARY_SUBSCR    
             1636  LOAD_FAST                '_wdinl'
             1638  LOAD_FAST                '_seisinfo'
             1640  LOAD_STR                 'ILStep'
             1642  BINARY_SUBSCR    
             1644  BINARY_MULTIPLY  
             1646  BINARY_ADD       

 L. 603      1648  LOAD_FAST                '_seisinfo'
             1650  LOAD_STR                 'ILEnd'
             1652  BINARY_SUBSCR    
             1654  LOAD_FAST                '_wdinl'
             1656  LOAD_FAST                '_seisinfo'
             1658  LOAD_STR                 'ILStep'
             1660  BINARY_SUBSCR    
             1662  BINARY_MULTIPLY  
             1664  BINARY_SUBTRACT  

 L. 604      1666  LOAD_FAST                '_seisinfo'
             1668  LOAD_STR                 'XLStart'
             1670  BINARY_SUBSCR    
             1672  LOAD_FAST                '_wdxl'
             1674  LOAD_FAST                '_seisinfo'
             1676  LOAD_STR                 'XLStep'
             1678  BINARY_SUBSCR    
             1680  BINARY_MULTIPLY  
             1682  BINARY_ADD       

 L. 605      1684  LOAD_FAST                '_seisinfo'
             1686  LOAD_STR                 'XLEnd'
             1688  BINARY_SUBSCR    
             1690  LOAD_FAST                '_wdxl'
             1692  LOAD_FAST                '_seisinfo'
             1694  LOAD_STR                 'XLStep'
             1696  BINARY_SUBSCR    
             1698  BINARY_MULTIPLY  
             1700  BINARY_SUBTRACT  

 L. 606      1702  LOAD_FAST                '_seisinfo'
             1704  LOAD_STR                 'ZStart'
             1706  BINARY_SUBSCR    
             1708  LOAD_FAST                '_wdz'
             1710  LOAD_FAST                '_seisinfo'
             1712  LOAD_STR                 'ZStep'
             1714  BINARY_SUBSCR    
             1716  BINARY_MULTIPLY  
             1718  BINARY_ADD       

 L. 607      1720  LOAD_FAST                '_seisinfo'
             1722  LOAD_STR                 'ZEnd'
             1724  BINARY_SUBSCR    
             1726  LOAD_FAST                '_wdz'
             1728  LOAD_FAST                '_seisinfo'
             1730  LOAD_STR                 'ZStep'
             1732  BINARY_SUBSCR    
             1734  BINARY_MULTIPLY  
             1736  BINARY_SUBTRACT  
             1738  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1740  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1742  STORE_FAST               '_traindata'

 L. 610      1744  LOAD_GLOBAL              np
             1746  LOAD_METHOD              shape
             1748  LOAD_FAST                '_traindata'
             1750  CALL_METHOD_1         1  '1 positional argument'
             1752  LOAD_CONST               0
             1754  BINARY_SUBSCR    
             1756  LOAD_CONST               0
             1758  COMPARE_OP               <=
         1760_1762  POP_JUMP_IF_FALSE  1800  'to 1800'

 L. 611      1764  LOAD_GLOBAL              vis_msg
             1766  LOAD_ATTR                print
             1768  LOAD_STR                 'ERROR in TrainMl2DDCnnFromScratch: No training sample found'
             1770  LOAD_STR                 'error'
             1772  LOAD_CONST               ('type',)
             1774  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1776  POP_TOP          

 L. 612      1778  LOAD_GLOBAL              QtWidgets
             1780  LOAD_ATTR                QMessageBox
             1782  LOAD_METHOD              critical
             1784  LOAD_DEREF               'self'
             1786  LOAD_ATTR                msgbox

 L. 613      1788  LOAD_STR                 'Train 2D-CAE'

 L. 614      1790  LOAD_STR                 'No training sample found'
             1792  CALL_METHOD_3         3  '3 positional arguments'
             1794  POP_TOP          

 L. 615      1796  LOAD_CONST               None
             1798  RETURN_VALUE     
           1800_0  COME_FROM          1760  '1760'

 L. 618      1800  LOAD_GLOBAL              print
             1802  LOAD_STR                 'TrainMl2DCaeFromScratch: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 619      1804  LOAD_FAST                '_image_height'
             1806  LOAD_FAST                '_image_width'
             1808  LOAD_FAST                '_image_height_new'
             1810  LOAD_FAST                '_image_width_new'
             1812  BUILD_TUPLE_4         4 
             1814  BINARY_MODULO    
             1816  CALL_FUNCTION_1       1  '1 positional argument'
             1818  POP_TOP          

 L. 620      1820  BUILD_MAP_0           0 
             1822  STORE_FAST               '_traindict'

 L. 621      1824  SETUP_LOOP         1896  'to 1896'
             1826  LOAD_FAST                '_features'
             1828  GET_ITER         
             1830  FOR_ITER           1894  'to 1894'
             1832  STORE_FAST               'f'

 L. 622      1834  LOAD_DEREF               'self'
             1836  LOAD_ATTR                seisdata
             1838  LOAD_FAST                'f'
             1840  BINARY_SUBSCR    
             1842  STORE_FAST               '_seisdata'

 L. 623      1844  LOAD_GLOBAL              seis_ays
             1846  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1848  LOAD_FAST                '_seisdata'
             1850  LOAD_FAST                '_traindata'
             1852  LOAD_DEREF               'self'
             1854  LOAD_ATTR                survinfo

 L. 624      1856  LOAD_FAST                '_wdinl'
             1858  LOAD_FAST                '_wdxl'
             1860  LOAD_FAST                '_wdz'

 L. 625      1862  LOAD_CONST               False
             1864  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1866  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1868  LOAD_CONST               None
             1870  LOAD_CONST               None
             1872  BUILD_SLICE_2         2 
             1874  LOAD_CONST               3
             1876  LOAD_CONST               None
             1878  BUILD_SLICE_2         2 
             1880  BUILD_TUPLE_2         2 
             1882  BINARY_SUBSCR    
             1884  LOAD_FAST                '_traindict'
             1886  LOAD_FAST                'f'
             1888  STORE_SUBSCR     
         1890_1892  JUMP_BACK          1830  'to 1830'
             1894  POP_BLOCK        
           1896_0  COME_FROM_LOOP     1824  '1824'

 L. 626      1896  LOAD_FAST                '_target'
             1898  LOAD_FAST                '_features'
             1900  COMPARE_OP               not-in
         1902_1904  POP_JUMP_IF_FALSE  1962  'to 1962'

 L. 627      1906  LOAD_DEREF               'self'
             1908  LOAD_ATTR                seisdata
             1910  LOAD_FAST                '_target'
             1912  BINARY_SUBSCR    
             1914  STORE_FAST               '_seisdata'

 L. 628      1916  LOAD_GLOBAL              seis_ays
             1918  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1920  LOAD_FAST                '_seisdata'
             1922  LOAD_FAST                '_traindata'
             1924  LOAD_DEREF               'self'
             1926  LOAD_ATTR                survinfo

 L. 629      1928  LOAD_FAST                '_wdinl'
             1930  LOAD_FAST                '_wdxl'
             1932  LOAD_FAST                '_wdz'

 L. 630      1934  LOAD_CONST               False
             1936  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1938  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1940  LOAD_CONST               None
             1942  LOAD_CONST               None
             1944  BUILD_SLICE_2         2 
             1946  LOAD_CONST               3
             1948  LOAD_CONST               None
             1950  BUILD_SLICE_2         2 
             1952  BUILD_TUPLE_2         2 
             1954  BINARY_SUBSCR    
             1956  LOAD_FAST                '_traindict'
             1958  LOAD_FAST                '_target'
             1960  STORE_SUBSCR     
           1962_0  COME_FROM          1902  '1902'

 L. 631      1962  LOAD_DEREF               'self'
             1964  LOAD_ATTR                traindataconfig
             1966  LOAD_STR                 'RemoveInvariantFeature_Checked'
             1968  BINARY_SUBSCR    
         1970_1972  POP_JUMP_IF_FALSE  2054  'to 2054'

 L. 632      1974  SETUP_LOOP         2054  'to 2054'
             1976  LOAD_FAST                '_features'
             1978  GET_ITER         
           1980_0  COME_FROM          2008  '2008'
             1980  FOR_ITER           2052  'to 2052'
             1982  STORE_FAST               'f'

 L. 633      1984  LOAD_GLOBAL              ml_aug
             1986  LOAD_METHOD              removeInvariantFeature
             1988  LOAD_FAST                '_traindict'
             1990  LOAD_FAST                'f'
             1992  CALL_METHOD_2         2  '2 positional arguments'
             1994  STORE_FAST               '_traindict'

 L. 634      1996  LOAD_GLOBAL              basic_mdt
             1998  LOAD_METHOD              maxDictConstantRow
             2000  LOAD_FAST                '_traindict'
             2002  CALL_METHOD_1         1  '1 positional argument'
             2004  LOAD_CONST               0
             2006  COMPARE_OP               <=
         2008_2010  POP_JUMP_IF_FALSE  1980  'to 1980'

 L. 635      2012  LOAD_GLOBAL              vis_msg
             2014  LOAD_ATTR                print
             2016  LOAD_STR                 'ERROR in TrainMl2DCaeFromScratch: No training sample found'

 L. 636      2018  LOAD_STR                 'error'
             2020  LOAD_CONST               ('type',)
             2022  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2024  POP_TOP          

 L. 637      2026  LOAD_GLOBAL              QtWidgets
             2028  LOAD_ATTR                QMessageBox
             2030  LOAD_METHOD              critical
             2032  LOAD_DEREF               'self'
             2034  LOAD_ATTR                msgbox

 L. 638      2036  LOAD_STR                 'Train 2D-DCNN'

 L. 639      2038  LOAD_STR                 'No training sample found'
             2040  CALL_METHOD_3         3  '3 positional arguments'
             2042  POP_TOP          

 L. 640      2044  LOAD_CONST               None
             2046  RETURN_VALUE     
         2048_2050  JUMP_BACK          1980  'to 1980'
             2052  POP_BLOCK        
           2054_0  COME_FROM_LOOP     1974  '1974'
           2054_1  COME_FROM          1970  '1970'

 L. 641      2054  LOAD_FAST                '_image_height_new'
             2056  LOAD_FAST                '_image_height'
             2058  COMPARE_OP               !=
         2060_2062  POP_JUMP_IF_TRUE   2074  'to 2074'
             2064  LOAD_FAST                '_image_width_new'
             2066  LOAD_FAST                '_image_width'
             2068  COMPARE_OP               !=
         2070_2072  POP_JUMP_IF_FALSE  2158  'to 2158'
           2074_0  COME_FROM          2060  '2060'

 L. 642      2074  SETUP_LOOP         2118  'to 2118'
             2076  LOAD_FAST                '_features'
             2078  GET_ITER         
             2080  FOR_ITER           2116  'to 2116'
             2082  STORE_FAST               'f'

 L. 643      2084  LOAD_GLOBAL              basic_image
             2086  LOAD_ATTR                changeImageSize
             2088  LOAD_FAST                '_traindict'
             2090  LOAD_FAST                'f'
             2092  BINARY_SUBSCR    

 L. 644      2094  LOAD_FAST                '_image_height'

 L. 645      2096  LOAD_FAST                '_image_width'

 L. 646      2098  LOAD_FAST                '_image_height_new'

 L. 647      2100  LOAD_FAST                '_image_width_new'
             2102  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2104  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2106  LOAD_FAST                '_traindict'
             2108  LOAD_FAST                'f'
             2110  STORE_SUBSCR     
         2112_2114  JUMP_BACK          2080  'to 2080'
             2116  POP_BLOCK        
           2118_0  COME_FROM_LOOP     2074  '2074'

 L. 648      2118  LOAD_FAST                '_target'
             2120  LOAD_FAST                '_features'
             2122  COMPARE_OP               not-in
         2124_2126  POP_JUMP_IF_FALSE  2158  'to 2158'

 L. 649      2128  LOAD_GLOBAL              basic_image
             2130  LOAD_ATTR                changeImageSize
             2132  LOAD_FAST                '_traindict'
             2134  LOAD_FAST                '_target'
             2136  BINARY_SUBSCR    

 L. 650      2138  LOAD_FAST                '_image_height'

 L. 651      2140  LOAD_FAST                '_image_width'

 L. 652      2142  LOAD_FAST                '_image_height_new'

 L. 653      2144  LOAD_FAST                '_image_width_new'
             2146  LOAD_STR                 'linear'
             2148  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2150  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2152  LOAD_FAST                '_traindict'
             2154  LOAD_FAST                '_target'
             2156  STORE_SUBSCR     
           2158_0  COME_FROM          2124  '2124'
           2158_1  COME_FROM          2070  '2070'

 L. 654      2158  LOAD_DEREF               'self'
             2160  LOAD_ATTR                traindataconfig
             2162  LOAD_STR                 'RotateFeature_Checked'
             2164  BINARY_SUBSCR    
             2166  LOAD_CONST               True
             2168  COMPARE_OP               is
         2170_2172  POP_JUMP_IF_FALSE  2312  'to 2312'

 L. 655      2174  SETUP_LOOP         2246  'to 2246'
             2176  LOAD_FAST                '_features'
             2178  GET_ITER         
             2180  FOR_ITER           2244  'to 2244'
             2182  STORE_FAST               'f'

 L. 656      2184  LOAD_FAST                '_image_height_new'
             2186  LOAD_FAST                '_image_width_new'
             2188  COMPARE_OP               ==
         2190_2192  POP_JUMP_IF_FALSE  2218  'to 2218'

 L. 657      2194  LOAD_GLOBAL              ml_aug
             2196  LOAD_METHOD              rotateImage6Way
             2198  LOAD_FAST                '_traindict'
             2200  LOAD_FAST                'f'
             2202  BINARY_SUBSCR    
             2204  LOAD_FAST                '_image_height_new'
             2206  LOAD_FAST                '_image_width_new'
             2208  CALL_METHOD_3         3  '3 positional arguments'
             2210  LOAD_FAST                '_traindict'
             2212  LOAD_FAST                'f'
             2214  STORE_SUBSCR     
             2216  JUMP_BACK          2180  'to 2180'
           2218_0  COME_FROM          2190  '2190'

 L. 659      2218  LOAD_GLOBAL              ml_aug
             2220  LOAD_METHOD              rotateImage4Way
             2222  LOAD_FAST                '_traindict'
             2224  LOAD_FAST                'f'
             2226  BINARY_SUBSCR    
             2228  LOAD_FAST                '_image_height_new'
             2230  LOAD_FAST                '_image_width_new'
             2232  CALL_METHOD_3         3  '3 positional arguments'
             2234  LOAD_FAST                '_traindict'
             2236  LOAD_FAST                'f'
             2238  STORE_SUBSCR     
         2240_2242  JUMP_BACK          2180  'to 2180'
             2244  POP_BLOCK        
           2246_0  COME_FROM_LOOP     2174  '2174'

 L. 660      2246  LOAD_FAST                '_target'
             2248  LOAD_FAST                '_features'
             2250  COMPARE_OP               not-in
         2252_2254  POP_JUMP_IF_FALSE  2312  'to 2312'

 L. 661      2256  LOAD_FAST                '_image_height_new'
             2258  LOAD_FAST                '_image_width_new'
             2260  COMPARE_OP               ==
         2262_2264  POP_JUMP_IF_FALSE  2290  'to 2290'

 L. 663      2266  LOAD_GLOBAL              ml_aug
             2268  LOAD_METHOD              rotateImage6Way
             2270  LOAD_FAST                '_traindict'
             2272  LOAD_FAST                '_target'
             2274  BINARY_SUBSCR    
             2276  LOAD_FAST                '_image_height_new'
             2278  LOAD_FAST                '_image_width_new'
             2280  CALL_METHOD_3         3  '3 positional arguments'
             2282  LOAD_FAST                '_traindict'
             2284  LOAD_FAST                '_target'
             2286  STORE_SUBSCR     
             2288  JUMP_FORWARD       2312  'to 2312'
           2290_0  COME_FROM          2262  '2262'

 L. 666      2290  LOAD_GLOBAL              ml_aug
             2292  LOAD_METHOD              rotateImage4Way
             2294  LOAD_FAST                '_traindict'
             2296  LOAD_FAST                '_target'
             2298  BINARY_SUBSCR    
             2300  LOAD_FAST                '_image_height_new'
             2302  LOAD_FAST                '_image_width_new'
             2304  CALL_METHOD_3         3  '3 positional arguments'
             2306  LOAD_FAST                '_traindict'
             2308  LOAD_FAST                '_target'
             2310  STORE_SUBSCR     
           2312_0  COME_FROM          2288  '2288'
           2312_1  COME_FROM          2252  '2252'
           2312_2  COME_FROM          2170  '2170'

 L. 669      2312  LOAD_GLOBAL              print
             2314  LOAD_STR                 'TrainMl2DCaeFromScratch: A total of %d valid training samples'
             2316  LOAD_GLOBAL              basic_mdt
             2318  LOAD_METHOD              maxDictConstantRow

 L. 670      2320  LOAD_FAST                '_traindict'
             2322  CALL_METHOD_1         1  '1 positional argument'
             2324  BINARY_MODULO    
             2326  CALL_FUNCTION_1       1  '1 positional argument'
             2328  POP_TOP          

 L. 672      2330  LOAD_GLOBAL              print
             2332  LOAD_STR                 'TrainMl2DCaeFromScratch: Step 3 - Start training'
             2334  CALL_FUNCTION_1       1  '1 positional argument'
             2336  POP_TOP          

 L. 674      2338  LOAD_GLOBAL              QtWidgets
             2340  LOAD_METHOD              QProgressDialog
             2342  CALL_METHOD_0         0  '0 positional arguments'
             2344  STORE_FAST               '_pgsdlg'

 L. 675      2346  LOAD_GLOBAL              QtGui
             2348  LOAD_METHOD              QIcon
             2350  CALL_METHOD_0         0  '0 positional arguments'
             2352  STORE_FAST               'icon'

 L. 676      2354  LOAD_FAST                'icon'
             2356  LOAD_METHOD              addPixmap
             2358  LOAD_GLOBAL              QtGui
             2360  LOAD_METHOD              QPixmap
             2362  LOAD_GLOBAL              os
             2364  LOAD_ATTR                path
             2366  LOAD_METHOD              join
             2368  LOAD_DEREF               'self'
             2370  LOAD_ATTR                iconpath
             2372  LOAD_STR                 'icons/new.png'
             2374  CALL_METHOD_2         2  '2 positional arguments'
             2376  CALL_METHOD_1         1  '1 positional argument'

 L. 677      2378  LOAD_GLOBAL              QtGui
             2380  LOAD_ATTR                QIcon
             2382  LOAD_ATTR                Normal
             2384  LOAD_GLOBAL              QtGui
             2386  LOAD_ATTR                QIcon
             2388  LOAD_ATTR                Off
             2390  CALL_METHOD_3         3  '3 positional arguments'
             2392  POP_TOP          

 L. 678      2394  LOAD_FAST                '_pgsdlg'
             2396  LOAD_METHOD              setWindowIcon
             2398  LOAD_FAST                'icon'
             2400  CALL_METHOD_1         1  '1 positional argument'
             2402  POP_TOP          

 L. 679      2404  LOAD_FAST                '_pgsdlg'
             2406  LOAD_METHOD              setWindowTitle
             2408  LOAD_STR                 'Train 2D-CAE'
             2410  CALL_METHOD_1         1  '1 positional argument'
             2412  POP_TOP          

 L. 680      2414  LOAD_FAST                '_pgsdlg'
             2416  LOAD_METHOD              setCancelButton
             2418  LOAD_CONST               None
             2420  CALL_METHOD_1         1  '1 positional argument'
             2422  POP_TOP          

 L. 681      2424  LOAD_FAST                '_pgsdlg'
             2426  LOAD_METHOD              setWindowFlags
             2428  LOAD_GLOBAL              QtCore
             2430  LOAD_ATTR                Qt
             2432  LOAD_ATTR                WindowStaysOnTopHint
             2434  CALL_METHOD_1         1  '1 positional argument'
             2436  POP_TOP          

 L. 682      2438  LOAD_FAST                '_pgsdlg'
             2440  LOAD_METHOD              forceShow
             2442  CALL_METHOD_0         0  '0 positional arguments'
             2444  POP_TOP          

 L. 683      2446  LOAD_FAST                '_pgsdlg'
             2448  LOAD_METHOD              setFixedWidth
             2450  LOAD_CONST               400
             2452  CALL_METHOD_1         1  '1 positional argument'
             2454  POP_TOP          

 L. 684      2456  LOAD_GLOBAL              ml_cae
             2458  LOAD_ATTR                createCAEReconstructor
             2460  LOAD_FAST                '_traindict'

 L. 685      2462  LOAD_FAST                '_image_height_new'
             2464  LOAD_FAST                '_image_width_new'

 L. 686      2466  LOAD_FAST                '_features'
             2468  LOAD_FAST                '_target'

 L. 687      2470  LOAD_FAST                '_nepoch'
             2472  LOAD_FAST                '_batchsize'

 L. 688      2474  LOAD_FAST                '_nconvblock'
             2476  LOAD_FAST                '_nconvfeature'

 L. 689      2478  LOAD_FAST                '_nconvlayer'

 L. 690      2480  LOAD_FAST                '_n1x1layer'
             2482  LOAD_FAST                '_n1x1feature'

 L. 691      2484  LOAD_FAST                '_patch_height'
             2486  LOAD_FAST                '_patch_width'

 L. 692      2488  LOAD_FAST                '_pool_height'
             2490  LOAD_FAST                '_pool_width'

 L. 693      2492  LOAD_FAST                '_learning_rate'

 L. 694      2494  LOAD_FAST                '_dropout_prob'

 L. 695      2496  LOAD_CONST               True

 L. 696      2498  LOAD_FAST                '_savepath'
             2500  LOAD_FAST                '_savename'

 L. 697      2502  LOAD_FAST                '_pgsdlg'
             2504  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'nepoch', 'batchsize', 'nconvblock', 'nconvfeature', 'nconvlayer', 'n1x1layer', 'n1x1feature', 'patchheight', 'patchwidth', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprob', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2506  CALL_FUNCTION_KW_22    22  '22 total positional and keyword args'
             2508  STORE_FAST               '_caelog'

 L. 700      2510  LOAD_GLOBAL              QtWidgets
             2512  LOAD_ATTR                QMessageBox
             2514  LOAD_METHOD              information
             2516  LOAD_DEREF               'self'
             2518  LOAD_ATTR                msgbox

 L. 701      2520  LOAD_STR                 'Train 2D-CAE'

 L. 702      2522  LOAD_STR                 'CAE trained successfully'
             2524  CALL_METHOD_3         3  '3 positional arguments'
             2526  POP_TOP          

 L. 704      2528  LOAD_GLOBAL              QtWidgets
             2530  LOAD_ATTR                QMessageBox
             2532  LOAD_METHOD              question
             2534  LOAD_DEREF               'self'
             2536  LOAD_ATTR                msgbox
             2538  LOAD_STR                 'Train 2D-CAE'
             2540  LOAD_STR                 'View learning matrix?'

 L. 705      2542  LOAD_GLOBAL              QtWidgets
             2544  LOAD_ATTR                QMessageBox
             2546  LOAD_ATTR                Yes
             2548  LOAD_GLOBAL              QtWidgets
             2550  LOAD_ATTR                QMessageBox
             2552  LOAD_ATTR                No
             2554  BINARY_OR        

 L. 706      2556  LOAD_GLOBAL              QtWidgets
             2558  LOAD_ATTR                QMessageBox
             2560  LOAD_ATTR                Yes
             2562  CALL_METHOD_5         5  '5 positional arguments'
             2564  STORE_FAST               'reply'

 L. 708      2566  LOAD_FAST                'reply'
             2568  LOAD_GLOBAL              QtWidgets
             2570  LOAD_ATTR                QMessageBox
             2572  LOAD_ATTR                Yes
             2574  COMPARE_OP               ==
         2576_2578  POP_JUMP_IF_FALSE  2646  'to 2646'

 L. 709      2580  LOAD_GLOBAL              QtWidgets
             2582  LOAD_METHOD              QDialog
             2584  CALL_METHOD_0         0  '0 positional arguments'
             2586  STORE_FAST               '_viewmllearnmat'

 L. 710      2588  LOAD_GLOBAL              gui_viewmllearnmat
             2590  CALL_FUNCTION_0       0  '0 positional arguments'
             2592  STORE_FAST               '_gui'

 L. 711      2594  LOAD_FAST                '_caelog'
             2596  LOAD_STR                 'learning_curve'
             2598  BINARY_SUBSCR    
             2600  LOAD_FAST                '_gui'
             2602  STORE_ATTR               learnmat

 L. 712      2604  LOAD_DEREF               'self'
             2606  LOAD_ATTR                linestyle
             2608  LOAD_FAST                '_gui'
             2610  STORE_ATTR               linestyle

 L. 713      2612  LOAD_DEREF               'self'
             2614  LOAD_ATTR                fontstyle
             2616  LOAD_FAST                '_gui'
             2618  STORE_ATTR               fontstyle

 L. 714      2620  LOAD_FAST                '_gui'
             2622  LOAD_METHOD              setupGUI
             2624  LOAD_FAST                '_viewmllearnmat'
             2626  CALL_METHOD_1         1  '1 positional argument'
             2628  POP_TOP          

 L. 715      2630  LOAD_FAST                '_viewmllearnmat'
             2632  LOAD_METHOD              exec
             2634  CALL_METHOD_0         0  '0 positional arguments'
             2636  POP_TOP          

 L. 716      2638  LOAD_FAST                '_viewmllearnmat'
             2640  LOAD_METHOD              show
             2642  CALL_METHOD_0         0  '0 positional arguments'
             2644  POP_TOP          
           2646_0  COME_FROM          2576  '2576'

Parse error at or near `POP_TOP' instruction at offset 2644

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
    TrainMl2DCaeFromScratch = QtWidgets.QWidget()
    gui = trainml2dcaefromscratch()
    gui.setupGUI(TrainMl2DCaeFromScratch)
    TrainMl2DCaeFromScratch.show()
    sys.exit(app.exec_())