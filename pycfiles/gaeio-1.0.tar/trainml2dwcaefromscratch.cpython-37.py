# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml2dwcaefromscratch.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 46417 bytes
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
import cognitivegeo.src.ml.wcaereconstructor as ml_wcae
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml2dwcaefromscratch(object):
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

    def setupGUI(self, TrainMl2DWcaeFromScratch):
        TrainMl2DWcaeFromScratch.setObjectName('TrainMl2DWcaeFromScratch')
        TrainMl2DWcaeFromScratch.setFixedSize(810, 540)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl2DWcaeFromScratch.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl2DWcaeFromScratch)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl2DWcaeFromScratch)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl2DWcaeFromScratch)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblweight = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblweight.setObjectName('lblweight')
        self.lblweight.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.cbbweight = QtWidgets.QComboBox(TrainMl2DWcaeFromScratch)
        self.cbbweight.setObjectName('cbbweight')
        self.cbbweight.setGeometry(QtCore.QRect(110, 310, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 50, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 50, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl2DWcaeFromScratch)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 90, 180, 200))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 50, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 50, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(TrainMl2DWcaeFromScratch)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 90, 180, 200))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 300, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 300, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 300, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 340, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 340, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 300, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 300, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 300, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 340, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 340, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl2DWcaeFromScratch)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 360, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 360, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 400, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 400, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 400, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 400, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 440, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 440, 40, 30))
        self.lbldropout = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 440, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 440, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl2DWcaeFromScratch)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 490, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl2DWcaeFromScratch)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 490, 180, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl2DWcaeFromScratch)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 490, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl2DWcaeFromScratch)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 490, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl2DWcaeFromScratch)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl2DWcaeFromScratch.geometry().center().x()
        _center_y = TrainMl2DWcaeFromScratch.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl2DWcaeFromScratch)
        QtCore.QMetaObject.connectSlotsByName(TrainMl2DWcaeFromScratch)

    def retranslateGUI(self, TrainMl2DWcaeFromScratch):
        self.dialog = TrainMl2DWcaeFromScratch
        _translate = QtCore.QCoreApplication.translate
        TrainMl2DWcaeFromScratch.setWindowTitle(_translate('TrainMl2DWcaeFromScratch', 'Train 2D-WCAE from scratch'))
        self.lblfeature.setText(_translate('TrainMl2DWcaeFromScratch', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl2DWcaeFromScratch', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl2DWcaeFromScratch', 'Select target:'))
        self.lblweight.setText(_translate('TrainMl2DWcaeFromScratch', 'Select weight:'))
        self.lbloldsize.setText(_translate('TrainMl2DWcaeFromScratch', 'Original\nimage\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl2DWcaeFromScratch', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl2DWcaeFromScratch', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl2DWcaeFromScratch', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl2DWcaeFromScratch', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl2DWcaeFromScratch', 'Interpolated\nimage\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl2DWcaeFromScratch', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl2DWcaeFromScratch', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl2DWcaeFromScratch', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl2DWcaeFromScratch', '32'))
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
                    item.setText(_translate('TrainMl2DWcaeFromScratch', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
            self.cbbweight.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl2DWcaeFromScratch', 'Specify WCAE architecture:'))
        self.lblnconvblock.setText(_translate('TrainMl2DWcaeFromScratch', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl2DWcaeFromScratch', '3'))
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

        self.lbln1x1layer.setText(_translate('TrainMl2DWcaeFromScratch', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('TrainMl2DWcaeFromScratch', '2'))
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.twgn1x1layer.setRowCount(2)
        for _idx in range(int(self.ldtn1x1layer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl2DWcaeFromScratch', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgn1x1layer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgn1x1layer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl2DWcaeFromScratch', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl2DWcaeFromScratch', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl2DWcaeFromScratch', '3'))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('TrainMl2DWcaeFromScratch', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl2DWcaeFromScratch', '3'))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('TrainMl2DWcaeFromScratch', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl2DWcaeFromScratch', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl2DWcaeFromScratch', '2'))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl2DWcaeFromScratch', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl2DWcaeFromScratch', '2'))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.btnconfigtraindata.setText(_translate('TrainMl2DWcaeFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lblpara.setText(_translate('TrainMl2DWcaeFromScratch', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl2DWcaeFromScratch', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl2DWcaeFromScratch', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl2DWcaeFromScratch', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl2DWcaeFromScratch', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl2DWcaeFromScratch', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl2DWcaeFromScratch', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('TrainMl2DWcaeFromScratch', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('TrainMl2DWcaeFromScratch', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl2DWcaeFromScratch', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl2DWcaeFromScratch', ''))
        self.btnsave.setText(_translate('TrainMl2DWcaeFromScratch', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl2DWcaeFromScratch', 'Train 2D-WCAE'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl2DWcaeFromScratch)

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
        _file = _dialog.getSaveFileName(None, 'Save WCAE Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
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

    def clickBtnTrainMl2DWcaeFromScratch--- This code section failed: ---

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
               30  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 459        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 460        50  LOAD_STR                 'Train 2D-WCAE'

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
              162  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 471       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 472       182  LOAD_STR                 'Train 2D-WCAE'

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
              232  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 478       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 479       252  LOAD_STR                 'Train 2D-WCAE'

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
              316  LOAD_STR                 'trainml2dwcaefromscratch.clickBtnTrainMl2DWcaeFromScratch.<locals>.<listcomp>'
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

 L. 491       360  LOAD_GLOBAL              basic_data
              362  LOAD_METHOD              str2int
              364  LOAD_DEREF               'self'
              366  LOAD_ATTR                ldtnconvblock
              368  LOAD_METHOD              text
              370  CALL_METHOD_0         0  '0 positional arguments'
              372  CALL_METHOD_1         1  '1 positional argument'
              374  STORE_FAST               '_nconvblock'

 L. 492       376  LOAD_CLOSURE             'self'
              378  BUILD_TUPLE_1         1 
              380  LOAD_LISTCOMP            '<code_object <listcomp>>'
              382  LOAD_STR                 'trainml2dwcaefromscratch.clickBtnTrainMl2DWcaeFromScratch.<locals>.<listcomp>'
              384  MAKE_FUNCTION_8          'closure'
              386  LOAD_GLOBAL              range
              388  LOAD_FAST                '_nconvblock'
              390  CALL_FUNCTION_1       1  '1 positional argument'
              392  GET_ITER         
              394  CALL_FUNCTION_1       1  '1 positional argument'
              396  STORE_FAST               '_nconvlayer'

 L. 493       398  LOAD_CLOSURE             'self'
              400  BUILD_TUPLE_1         1 
              402  LOAD_LISTCOMP            '<code_object <listcomp>>'
              404  LOAD_STR                 'trainml2dwcaefromscratch.clickBtnTrainMl2DWcaeFromScratch.<locals>.<listcomp>'
              406  MAKE_FUNCTION_8          'closure'
              408  LOAD_GLOBAL              range
              410  LOAD_FAST                '_nconvblock'
              412  CALL_FUNCTION_1       1  '1 positional argument'
              414  GET_ITER         
              416  CALL_FUNCTION_1       1  '1 positional argument'
              418  STORE_FAST               '_nconvfeature'

 L. 494       420  LOAD_GLOBAL              basic_data
              422  LOAD_METHOD              str2int
              424  LOAD_DEREF               'self'
              426  LOAD_ATTR                ldtn1x1layer
              428  LOAD_METHOD              text
              430  CALL_METHOD_0         0  '0 positional arguments'
              432  CALL_METHOD_1         1  '1 positional argument'
              434  STORE_FAST               '_n1x1layer'

 L. 495       436  LOAD_CLOSURE             'self'
              438  BUILD_TUPLE_1         1 
              440  LOAD_LISTCOMP            '<code_object <listcomp>>'
              442  LOAD_STR                 'trainml2dwcaefromscratch.clickBtnTrainMl2DWcaeFromScratch.<locals>.<listcomp>'
              444  MAKE_FUNCTION_8          'closure'
              446  LOAD_GLOBAL              range
              448  LOAD_FAST                '_n1x1layer'
              450  CALL_FUNCTION_1       1  '1 positional argument'
              452  GET_ITER         
              454  CALL_FUNCTION_1       1  '1 positional argument'
              456  STORE_FAST               '_n1x1feature'

 L. 496       458  LOAD_GLOBAL              basic_data
              460  LOAD_METHOD              str2int
              462  LOAD_DEREF               'self'
              464  LOAD_ATTR                ldtmaskheight
              466  LOAD_METHOD              text
              468  CALL_METHOD_0         0  '0 positional arguments'
              470  CALL_METHOD_1         1  '1 positional argument'
              472  STORE_FAST               '_patch_height'

 L. 497       474  LOAD_GLOBAL              basic_data
              476  LOAD_METHOD              str2int
              478  LOAD_DEREF               'self'
              480  LOAD_ATTR                ldtmaskwidth
              482  LOAD_METHOD              text
              484  CALL_METHOD_0         0  '0 positional arguments'
              486  CALL_METHOD_1         1  '1 positional argument'
              488  STORE_FAST               '_patch_width'

 L. 498       490  LOAD_GLOBAL              basic_data
              492  LOAD_METHOD              str2int
              494  LOAD_DEREF               'self'
              496  LOAD_ATTR                ldtpoolheight
              498  LOAD_METHOD              text
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  CALL_METHOD_1         1  '1 positional argument'
              504  STORE_FAST               '_pool_height'

 L. 499       506  LOAD_GLOBAL              basic_data
              508  LOAD_METHOD              str2int
              510  LOAD_DEREF               'self'
              512  LOAD_ATTR                ldtpoolwidth
              514  LOAD_METHOD              text
              516  CALL_METHOD_0         0  '0 positional arguments'
              518  CALL_METHOD_1         1  '1 positional argument'
              520  STORE_FAST               '_pool_width'

 L. 500       522  LOAD_GLOBAL              basic_data
              524  LOAD_METHOD              str2int
              526  LOAD_DEREF               'self'
              528  LOAD_ATTR                ldtnepoch
              530  LOAD_METHOD              text
              532  CALL_METHOD_0         0  '0 positional arguments'
              534  CALL_METHOD_1         1  '1 positional argument'
              536  STORE_FAST               '_nepoch'

 L. 501       538  LOAD_GLOBAL              basic_data
              540  LOAD_METHOD              str2int
              542  LOAD_DEREF               'self'
              544  LOAD_ATTR                ldtbatchsize
              546  LOAD_METHOD              text
              548  CALL_METHOD_0         0  '0 positional arguments'
              550  CALL_METHOD_1         1  '1 positional argument'
              552  STORE_FAST               '_batchsize'

 L. 502       554  LOAD_GLOBAL              basic_data
              556  LOAD_METHOD              str2float
              558  LOAD_DEREF               'self'
              560  LOAD_ATTR                ldtlearnrate
              562  LOAD_METHOD              text
              564  CALL_METHOD_0         0  '0 positional arguments'
              566  CALL_METHOD_1         1  '1 positional argument'
              568  STORE_FAST               '_learning_rate'

 L. 503       570  LOAD_GLOBAL              basic_data
              572  LOAD_METHOD              str2float
              574  LOAD_DEREF               'self'
              576  LOAD_ATTR                ldtdropout
              578  LOAD_METHOD              text
              580  CALL_METHOD_0         0  '0 positional arguments'
              582  CALL_METHOD_1         1  '1 positional argument'
              584  STORE_FAST               '_dropout_prob'

 L. 504       586  LOAD_FAST                '_nconvblock'
              588  LOAD_CONST               False
              590  COMPARE_OP               is
          592_594  POP_JUMP_IF_TRUE    606  'to 606'
              596  LOAD_FAST                '_nconvblock'
              598  LOAD_CONST               0
              600  COMPARE_OP               <=
          602_604  POP_JUMP_IF_FALSE   642  'to 642'
            606_0  COME_FROM           592  '592'

 L. 505       606  LOAD_GLOBAL              vis_msg
              608  LOAD_ATTR                print
              610  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: Non-positive convolutional block number'

 L. 506       612  LOAD_STR                 'error'
              614  LOAD_CONST               ('type',)
              616  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              618  POP_TOP          

 L. 507       620  LOAD_GLOBAL              QtWidgets
              622  LOAD_ATTR                QMessageBox
              624  LOAD_METHOD              critical
              626  LOAD_DEREF               'self'
              628  LOAD_ATTR                msgbox

 L. 508       630  LOAD_STR                 'Train 2D-WCAE'

 L. 509       632  LOAD_STR                 'Non-positive convolutional block number'
              634  CALL_METHOD_3         3  '3 positional arguments'
              636  POP_TOP          

 L. 510       638  LOAD_CONST               None
              640  RETURN_VALUE     
            642_0  COME_FROM           602  '602'

 L. 511       642  SETUP_LOOP          714  'to 714'
              644  LOAD_FAST                '_nconvlayer'
              646  GET_ITER         
            648_0  COME_FROM           668  '668'
              648  FOR_ITER            712  'to 712'
              650  STORE_FAST               '_i'

 L. 512       652  LOAD_FAST                '_i'
              654  LOAD_CONST               False
              656  COMPARE_OP               is
          658_660  POP_JUMP_IF_TRUE    672  'to 672'
              662  LOAD_FAST                '_i'
              664  LOAD_CONST               1
              666  COMPARE_OP               <
          668_670  POP_JUMP_IF_FALSE   648  'to 648'
            672_0  COME_FROM           658  '658'

 L. 513       672  LOAD_GLOBAL              vis_msg
              674  LOAD_ATTR                print
              676  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: Non-positive convolutional layer number'

 L. 514       678  LOAD_STR                 'error'
              680  LOAD_CONST               ('type',)
              682  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              684  POP_TOP          

 L. 515       686  LOAD_GLOBAL              QtWidgets
              688  LOAD_ATTR                QMessageBox
              690  LOAD_METHOD              critical
              692  LOAD_DEREF               'self'
              694  LOAD_ATTR                msgbox

 L. 516       696  LOAD_STR                 'Train 2D-WCAE'

 L. 517       698  LOAD_STR                 'Non-positive convolutional layer number'
              700  CALL_METHOD_3         3  '3 positional arguments'
              702  POP_TOP          

 L. 518       704  LOAD_CONST               None
              706  RETURN_VALUE     
          708_710  JUMP_BACK           648  'to 648'
              712  POP_BLOCK        
            714_0  COME_FROM_LOOP      642  '642'

 L. 519       714  SETUP_LOOP          786  'to 786'
              716  LOAD_FAST                '_nconvfeature'
              718  GET_ITER         
            720_0  COME_FROM           740  '740'
              720  FOR_ITER            784  'to 784'
              722  STORE_FAST               '_i'

 L. 520       724  LOAD_FAST                '_i'
              726  LOAD_CONST               False
              728  COMPARE_OP               is
          730_732  POP_JUMP_IF_TRUE    744  'to 744'
              734  LOAD_FAST                '_i'
              736  LOAD_CONST               1
              738  COMPARE_OP               <
          740_742  POP_JUMP_IF_FALSE   720  'to 720'
            744_0  COME_FROM           730  '730'

 L. 521       744  LOAD_GLOBAL              vis_msg
              746  LOAD_ATTR                print
              748  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: Non-positive convolutional feature number'

 L. 522       750  LOAD_STR                 'error'
              752  LOAD_CONST               ('type',)
              754  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              756  POP_TOP          

 L. 523       758  LOAD_GLOBAL              QtWidgets
              760  LOAD_ATTR                QMessageBox
              762  LOAD_METHOD              critical
              764  LOAD_DEREF               'self'
              766  LOAD_ATTR                msgbox

 L. 524       768  LOAD_STR                 'Train 2D-WCAE'

 L. 525       770  LOAD_STR                 'Non-positive convolutional feature number'
              772  CALL_METHOD_3         3  '3 positional arguments'
              774  POP_TOP          

 L. 526       776  LOAD_CONST               None
              778  RETURN_VALUE     
          780_782  JUMP_BACK           720  'to 720'
              784  POP_BLOCK        
            786_0  COME_FROM_LOOP      714  '714'

 L. 527       786  LOAD_FAST                '_n1x1layer'
              788  LOAD_CONST               False
              790  COMPARE_OP               is
          792_794  POP_JUMP_IF_TRUE    806  'to 806'
              796  LOAD_FAST                '_n1x1layer'
              798  LOAD_CONST               0
              800  COMPARE_OP               <=
          802_804  POP_JUMP_IF_FALSE   842  'to 842'
            806_0  COME_FROM           792  '792'

 L. 528       806  LOAD_GLOBAL              vis_msg
              808  LOAD_ATTR                print
              810  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: Non-positive 1x1 convolutional layer number'

 L. 529       812  LOAD_STR                 'error'
              814  LOAD_CONST               ('type',)
              816  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              818  POP_TOP          

 L. 530       820  LOAD_GLOBAL              QtWidgets
              822  LOAD_ATTR                QMessageBox
              824  LOAD_METHOD              critical
              826  LOAD_DEREF               'self'
              828  LOAD_ATTR                msgbox

 L. 531       830  LOAD_STR                 'Train 2D-WCAE'

 L. 532       832  LOAD_STR                 'Non-positive 1x1 convolutional layer number'
              834  CALL_METHOD_3         3  '3 positional arguments'
              836  POP_TOP          

 L. 533       838  LOAD_CONST               None
              840  RETURN_VALUE     
            842_0  COME_FROM           802  '802'

 L. 534       842  SETUP_LOOP          914  'to 914'
              844  LOAD_FAST                '_n1x1feature'
              846  GET_ITER         
            848_0  COME_FROM           868  '868'
              848  FOR_ITER            912  'to 912'
              850  STORE_FAST               '_i'

 L. 535       852  LOAD_FAST                '_i'
              854  LOAD_CONST               False
              856  COMPARE_OP               is
          858_860  POP_JUMP_IF_TRUE    872  'to 872'
              862  LOAD_FAST                '_i'
              864  LOAD_CONST               1
              866  COMPARE_OP               <
          868_870  POP_JUMP_IF_FALSE   848  'to 848'
            872_0  COME_FROM           858  '858'

 L. 536       872  LOAD_GLOBAL              vis_msg
              874  LOAD_ATTR                print
              876  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: Non-positive 1x1 convolutional feature number'

 L. 537       878  LOAD_STR                 'error'
              880  LOAD_CONST               ('type',)
              882  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              884  POP_TOP          

 L. 538       886  LOAD_GLOBAL              QtWidgets
              888  LOAD_ATTR                QMessageBox
              890  LOAD_METHOD              critical
              892  LOAD_DEREF               'self'
              894  LOAD_ATTR                msgbox

 L. 539       896  LOAD_STR                 'Train 2D-WCAE'

 L. 540       898  LOAD_STR                 'Non-positive 1x1 convolutional feature number'
              900  CALL_METHOD_3         3  '3 positional arguments'
              902  POP_TOP          

 L. 541       904  LOAD_CONST               None
              906  RETURN_VALUE     
          908_910  JUMP_BACK           848  'to 848'
              912  POP_BLOCK        
            914_0  COME_FROM_LOOP      842  '842'

 L. 542       914  LOAD_FAST                '_patch_height'
              916  LOAD_CONST               False
              918  COMPARE_OP               is
          920_922  POP_JUMP_IF_TRUE    954  'to 954'
              924  LOAD_FAST                '_patch_width'
              926  LOAD_CONST               False
              928  COMPARE_OP               is
          930_932  POP_JUMP_IF_TRUE    954  'to 954'

 L. 543       934  LOAD_FAST                '_patch_height'
              936  LOAD_CONST               1
              938  COMPARE_OP               <
          940_942  POP_JUMP_IF_TRUE    954  'to 954'
              944  LOAD_FAST                '_patch_width'
              946  LOAD_CONST               1
              948  COMPARE_OP               <
          950_952  POP_JUMP_IF_FALSE   990  'to 990'
            954_0  COME_FROM           940  '940'
            954_1  COME_FROM           930  '930'
            954_2  COME_FROM           920  '920'

 L. 544       954  LOAD_GLOBAL              vis_msg
              956  LOAD_ATTR                print
              958  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: Non-positive convolutional patch size'

 L. 545       960  LOAD_STR                 'error'
              962  LOAD_CONST               ('type',)
              964  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              966  POP_TOP          

 L. 546       968  LOAD_GLOBAL              QtWidgets
              970  LOAD_ATTR                QMessageBox
              972  LOAD_METHOD              critical
              974  LOAD_DEREF               'self'
              976  LOAD_ATTR                msgbox

 L. 547       978  LOAD_STR                 'Train 2D-WCAE'

 L. 548       980  LOAD_STR                 'Non-positive convolutional patch size'
              982  CALL_METHOD_3         3  '3 positional arguments'
              984  POP_TOP          

 L. 549       986  LOAD_CONST               None
              988  RETURN_VALUE     
            990_0  COME_FROM           950  '950'

 L. 550       990  LOAD_FAST                '_pool_height'
              992  LOAD_CONST               False
              994  COMPARE_OP               is
          996_998  POP_JUMP_IF_TRUE   1030  'to 1030'
             1000  LOAD_FAST                '_pool_width'
             1002  LOAD_CONST               False
             1004  COMPARE_OP               is
         1006_1008  POP_JUMP_IF_TRUE   1030  'to 1030'

 L. 551      1010  LOAD_FAST                '_pool_height'
             1012  LOAD_CONST               1
             1014  COMPARE_OP               <
         1016_1018  POP_JUMP_IF_TRUE   1030  'to 1030'
             1020  LOAD_FAST                '_pool_width'
             1022  LOAD_CONST               1
             1024  COMPARE_OP               <
         1026_1028  POP_JUMP_IF_FALSE  1066  'to 1066'
           1030_0  COME_FROM          1016  '1016'
           1030_1  COME_FROM          1006  '1006'
           1030_2  COME_FROM           996  '996'

 L. 552      1030  LOAD_GLOBAL              vis_msg
             1032  LOAD_ATTR                print
             1034  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: Non-positive pooling size'
             1036  LOAD_STR                 'error'
             1038  LOAD_CONST               ('type',)
             1040  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1042  POP_TOP          

 L. 553      1044  LOAD_GLOBAL              QtWidgets
             1046  LOAD_ATTR                QMessageBox
             1048  LOAD_METHOD              critical
             1050  LOAD_DEREF               'self'
             1052  LOAD_ATTR                msgbox

 L. 554      1054  LOAD_STR                 'Train 2D-WCAE'

 L. 555      1056  LOAD_STR                 'Non-positive pooling size'
             1058  CALL_METHOD_3         3  '3 positional arguments'
             1060  POP_TOP          

 L. 556      1062  LOAD_CONST               None
             1064  RETURN_VALUE     
           1066_0  COME_FROM          1026  '1026'

 L. 557      1066  LOAD_FAST                '_nepoch'
             1068  LOAD_CONST               False
             1070  COMPARE_OP               is
         1072_1074  POP_JUMP_IF_TRUE   1086  'to 1086'
             1076  LOAD_FAST                '_nepoch'
             1078  LOAD_CONST               0
             1080  COMPARE_OP               <=
         1082_1084  POP_JUMP_IF_FALSE  1122  'to 1122'
           1086_0  COME_FROM          1072  '1072'

 L. 558      1086  LOAD_GLOBAL              vis_msg
             1088  LOAD_ATTR                print
             1090  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: Non-positive epoch number'
             1092  LOAD_STR                 'error'
             1094  LOAD_CONST               ('type',)
             1096  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1098  POP_TOP          

 L. 559      1100  LOAD_GLOBAL              QtWidgets
             1102  LOAD_ATTR                QMessageBox
             1104  LOAD_METHOD              critical
             1106  LOAD_DEREF               'self'
             1108  LOAD_ATTR                msgbox

 L. 560      1110  LOAD_STR                 'Train 2D-WCAE'

 L. 561      1112  LOAD_STR                 'Non-positive epoch number'
             1114  CALL_METHOD_3         3  '3 positional arguments'
             1116  POP_TOP          

 L. 562      1118  LOAD_CONST               None
             1120  RETURN_VALUE     
           1122_0  COME_FROM          1082  '1082'

 L. 563      1122  LOAD_FAST                '_batchsize'
             1124  LOAD_CONST               False
             1126  COMPARE_OP               is
         1128_1130  POP_JUMP_IF_TRUE   1142  'to 1142'
             1132  LOAD_FAST                '_batchsize'
             1134  LOAD_CONST               0
             1136  COMPARE_OP               <=
         1138_1140  POP_JUMP_IF_FALSE  1178  'to 1178'
           1142_0  COME_FROM          1128  '1128'

 L. 564      1142  LOAD_GLOBAL              vis_msg
             1144  LOAD_ATTR                print
             1146  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: Non-positive batch size'
             1148  LOAD_STR                 'error'
             1150  LOAD_CONST               ('type',)
             1152  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1154  POP_TOP          

 L. 565      1156  LOAD_GLOBAL              QtWidgets
             1158  LOAD_ATTR                QMessageBox
             1160  LOAD_METHOD              critical
             1162  LOAD_DEREF               'self'
             1164  LOAD_ATTR                msgbox

 L. 566      1166  LOAD_STR                 'Train 2D-WCAE'

 L. 567      1168  LOAD_STR                 'Non-positive batch size'
             1170  CALL_METHOD_3         3  '3 positional arguments'
             1172  POP_TOP          

 L. 568      1174  LOAD_CONST               None
             1176  RETURN_VALUE     
           1178_0  COME_FROM          1138  '1138'

 L. 569      1178  LOAD_FAST                '_learning_rate'
             1180  LOAD_CONST               False
             1182  COMPARE_OP               is
         1184_1186  POP_JUMP_IF_TRUE   1198  'to 1198'
             1188  LOAD_FAST                '_learning_rate'
             1190  LOAD_CONST               0
             1192  COMPARE_OP               <=
         1194_1196  POP_JUMP_IF_FALSE  1234  'to 1234'
           1198_0  COME_FROM          1184  '1184'

 L. 570      1198  LOAD_GLOBAL              vis_msg
             1200  LOAD_ATTR                print
             1202  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: Non-positive learning rate'
             1204  LOAD_STR                 'error'
             1206  LOAD_CONST               ('type',)
             1208  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1210  POP_TOP          

 L. 571      1212  LOAD_GLOBAL              QtWidgets
             1214  LOAD_ATTR                QMessageBox
             1216  LOAD_METHOD              critical
             1218  LOAD_DEREF               'self'
             1220  LOAD_ATTR                msgbox

 L. 572      1222  LOAD_STR                 'Train 2D-WCAE'

 L. 573      1224  LOAD_STR                 'Non-positive learning rate'
             1226  CALL_METHOD_3         3  '3 positional arguments'
             1228  POP_TOP          

 L. 574      1230  LOAD_CONST               None
             1232  RETURN_VALUE     
           1234_0  COME_FROM          1194  '1194'

 L. 575      1234  LOAD_FAST                '_dropout_prob'
             1236  LOAD_CONST               False
             1238  COMPARE_OP               is
         1240_1242  POP_JUMP_IF_TRUE   1254  'to 1254'
             1244  LOAD_FAST                '_dropout_prob'
             1246  LOAD_CONST               0
             1248  COMPARE_OP               <=
         1250_1252  POP_JUMP_IF_FALSE  1290  'to 1290'
           1254_0  COME_FROM          1240  '1240'

 L. 576      1254  LOAD_GLOBAL              vis_msg
             1256  LOAD_ATTR                print
             1258  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: Negative dropout rate'
             1260  LOAD_STR                 'error'
             1262  LOAD_CONST               ('type',)
             1264  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1266  POP_TOP          

 L. 577      1268  LOAD_GLOBAL              QtWidgets
             1270  LOAD_ATTR                QMessageBox
             1272  LOAD_METHOD              critical
             1274  LOAD_DEREF               'self'
             1276  LOAD_ATTR                msgbox

 L. 578      1278  LOAD_STR                 'Train 2D-WCAE'

 L. 579      1280  LOAD_STR                 'Negative dropout rate'
             1282  CALL_METHOD_3         3  '3 positional arguments'
             1284  POP_TOP          

 L. 580      1286  LOAD_CONST               None
             1288  RETURN_VALUE     
           1290_0  COME_FROM          1250  '1250'

 L. 582      1290  LOAD_GLOBAL              len
             1292  LOAD_DEREF               'self'
             1294  LOAD_ATTR                ldtsave
             1296  LOAD_METHOD              text
             1298  CALL_METHOD_0         0  '0 positional arguments'
             1300  CALL_FUNCTION_1       1  '1 positional argument'
             1302  LOAD_CONST               1
             1304  COMPARE_OP               <
         1306_1308  POP_JUMP_IF_FALSE  1346  'to 1346'

 L. 583      1310  LOAD_GLOBAL              vis_msg
             1312  LOAD_ATTR                print
             1314  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: No name specified for WCAE network'
             1316  LOAD_STR                 'error'
             1318  LOAD_CONST               ('type',)
             1320  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1322  POP_TOP          

 L. 584      1324  LOAD_GLOBAL              QtWidgets
             1326  LOAD_ATTR                QMessageBox
             1328  LOAD_METHOD              critical
             1330  LOAD_DEREF               'self'
             1332  LOAD_ATTR                msgbox

 L. 585      1334  LOAD_STR                 'Train 2D-WCAE'

 L. 586      1336  LOAD_STR                 'No name specified for WCAE network'
             1338  CALL_METHOD_3         3  '3 positional arguments'
             1340  POP_TOP          

 L. 587      1342  LOAD_CONST               None
             1344  RETURN_VALUE     
           1346_0  COME_FROM          1306  '1306'

 L. 588      1346  LOAD_GLOBAL              os
             1348  LOAD_ATTR                path
             1350  LOAD_METHOD              dirname
             1352  LOAD_DEREF               'self'
             1354  LOAD_ATTR                ldtsave
             1356  LOAD_METHOD              text
             1358  CALL_METHOD_0         0  '0 positional arguments'
             1360  CALL_METHOD_1         1  '1 positional argument'
             1362  STORE_FAST               '_savepath'

 L. 589      1364  LOAD_GLOBAL              os
             1366  LOAD_ATTR                path
             1368  LOAD_METHOD              splitext
             1370  LOAD_GLOBAL              os
             1372  LOAD_ATTR                path
             1374  LOAD_METHOD              basename
             1376  LOAD_DEREF               'self'
             1378  LOAD_ATTR                ldtsave
             1380  LOAD_METHOD              text
             1382  CALL_METHOD_0         0  '0 positional arguments'
             1384  CALL_METHOD_1         1  '1 positional argument'
             1386  CALL_METHOD_1         1  '1 positional argument'
             1388  LOAD_CONST               0
             1390  BINARY_SUBSCR    
             1392  STORE_FAST               '_savename'

 L. 591      1394  LOAD_CONST               0
             1396  STORE_FAST               '_wdinl'

 L. 592      1398  LOAD_CONST               0
             1400  STORE_FAST               '_wdxl'

 L. 593      1402  LOAD_CONST               0
             1404  STORE_FAST               '_wdz'

 L. 594      1406  LOAD_DEREF               'self'
             1408  LOAD_ATTR                cbbornt
             1410  LOAD_METHOD              currentIndex
             1412  CALL_METHOD_0         0  '0 positional arguments'
             1414  LOAD_CONST               0
             1416  COMPARE_OP               ==
         1418_1420  POP_JUMP_IF_FALSE  1446  'to 1446'

 L. 595      1422  LOAD_GLOBAL              int
             1424  LOAD_FAST                '_image_width'
             1426  LOAD_CONST               2
             1428  BINARY_TRUE_DIVIDE
             1430  CALL_FUNCTION_1       1  '1 positional argument'
             1432  STORE_FAST               '_wdxl'

 L. 596      1434  LOAD_GLOBAL              int
             1436  LOAD_FAST                '_image_height'
             1438  LOAD_CONST               2
             1440  BINARY_TRUE_DIVIDE
             1442  CALL_FUNCTION_1       1  '1 positional argument'
             1444  STORE_FAST               '_wdz'
           1446_0  COME_FROM          1418  '1418'

 L. 597      1446  LOAD_DEREF               'self'
             1448  LOAD_ATTR                cbbornt
             1450  LOAD_METHOD              currentIndex
             1452  CALL_METHOD_0         0  '0 positional arguments'
             1454  LOAD_CONST               1
             1456  COMPARE_OP               ==
         1458_1460  POP_JUMP_IF_FALSE  1486  'to 1486'

 L. 598      1462  LOAD_GLOBAL              int
             1464  LOAD_FAST                '_image_width'
             1466  LOAD_CONST               2
             1468  BINARY_TRUE_DIVIDE
             1470  CALL_FUNCTION_1       1  '1 positional argument'
             1472  STORE_FAST               '_wdinl'

 L. 599      1474  LOAD_GLOBAL              int
             1476  LOAD_FAST                '_image_height'
             1478  LOAD_CONST               2
             1480  BINARY_TRUE_DIVIDE
             1482  CALL_FUNCTION_1       1  '1 positional argument'
             1484  STORE_FAST               '_wdz'
           1486_0  COME_FROM          1458  '1458'

 L. 600      1486  LOAD_DEREF               'self'
             1488  LOAD_ATTR                cbbornt
             1490  LOAD_METHOD              currentIndex
             1492  CALL_METHOD_0         0  '0 positional arguments'
             1494  LOAD_CONST               2
             1496  COMPARE_OP               ==
         1498_1500  POP_JUMP_IF_FALSE  1526  'to 1526'

 L. 601      1502  LOAD_GLOBAL              int
             1504  LOAD_FAST                '_image_width'
             1506  LOAD_CONST               2
             1508  BINARY_TRUE_DIVIDE
             1510  CALL_FUNCTION_1       1  '1 positional argument'
             1512  STORE_FAST               '_wdinl'

 L. 602      1514  LOAD_GLOBAL              int
             1516  LOAD_FAST                '_image_height'
             1518  LOAD_CONST               2
             1520  BINARY_TRUE_DIVIDE
             1522  CALL_FUNCTION_1       1  '1 positional argument'
             1524  STORE_FAST               '_wdxl'
           1526_0  COME_FROM          1498  '1498'

 L. 604      1526  LOAD_DEREF               'self'
             1528  LOAD_ATTR                survinfo
             1530  STORE_FAST               '_seisinfo'

 L. 606      1532  LOAD_GLOBAL              print
             1534  LOAD_STR                 'TrainMl2DWcaeFromScratch: Step 1 - Get training samples:'
             1536  CALL_FUNCTION_1       1  '1 positional argument'
             1538  POP_TOP          

 L. 607      1540  LOAD_DEREF               'self'
             1542  LOAD_ATTR                traindataconfig
             1544  LOAD_STR                 'TrainPointSet'
             1546  BINARY_SUBSCR    
             1548  STORE_FAST               '_trainpoint'

 L. 608      1550  LOAD_GLOBAL              np
             1552  LOAD_METHOD              zeros
             1554  LOAD_CONST               0
             1556  LOAD_CONST               3
             1558  BUILD_LIST_2          2 
             1560  CALL_METHOD_1         1  '1 positional argument'
             1562  STORE_FAST               '_traindata'

 L. 609      1564  SETUP_LOOP         1640  'to 1640'
             1566  LOAD_FAST                '_trainpoint'
             1568  GET_ITER         
           1570_0  COME_FROM          1588  '1588'
             1570  FOR_ITER           1638  'to 1638'
             1572  STORE_FAST               '_p'

 L. 610      1574  LOAD_GLOBAL              point_ays
             1576  LOAD_METHOD              checkPoint
             1578  LOAD_DEREF               'self'
             1580  LOAD_ATTR                pointsetdata
             1582  LOAD_FAST                '_p'
             1584  BINARY_SUBSCR    
             1586  CALL_METHOD_1         1  '1 positional argument'
         1588_1590  POP_JUMP_IF_FALSE  1570  'to 1570'

 L. 611      1592  LOAD_GLOBAL              basic_mdt
             1594  LOAD_METHOD              exportMatDict
             1596  LOAD_DEREF               'self'
             1598  LOAD_ATTR                pointsetdata
             1600  LOAD_FAST                '_p'
             1602  BINARY_SUBSCR    
             1604  LOAD_STR                 'Inline'
             1606  LOAD_STR                 'Crossline'
             1608  LOAD_STR                 'Z'
             1610  BUILD_LIST_3          3 
             1612  CALL_METHOD_2         2  '2 positional arguments'
             1614  STORE_FAST               '_pt'

 L. 612      1616  LOAD_GLOBAL              np
             1618  LOAD_ATTR                concatenate
             1620  LOAD_FAST                '_traindata'
             1622  LOAD_FAST                '_pt'
             1624  BUILD_TUPLE_2         2 
             1626  LOAD_CONST               0
             1628  LOAD_CONST               ('axis',)
             1630  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1632  STORE_FAST               '_traindata'
         1634_1636  JUMP_BACK          1570  'to 1570'
             1638  POP_BLOCK        
           1640_0  COME_FROM_LOOP     1564  '1564'

 L. 613      1640  LOAD_GLOBAL              seis_ays
             1642  LOAD_ATTR                removeOutofSurveySample
             1644  LOAD_FAST                '_traindata'

 L. 614      1646  LOAD_FAST                '_seisinfo'
             1648  LOAD_STR                 'ILStart'
             1650  BINARY_SUBSCR    
             1652  LOAD_FAST                '_wdinl'
             1654  LOAD_FAST                '_seisinfo'
             1656  LOAD_STR                 'ILStep'
             1658  BINARY_SUBSCR    
             1660  BINARY_MULTIPLY  
             1662  BINARY_ADD       

 L. 615      1664  LOAD_FAST                '_seisinfo'
             1666  LOAD_STR                 'ILEnd'
             1668  BINARY_SUBSCR    
             1670  LOAD_FAST                '_wdinl'
             1672  LOAD_FAST                '_seisinfo'
             1674  LOAD_STR                 'ILStep'
             1676  BINARY_SUBSCR    
             1678  BINARY_MULTIPLY  
             1680  BINARY_SUBTRACT  

 L. 616      1682  LOAD_FAST                '_seisinfo'
             1684  LOAD_STR                 'XLStart'
             1686  BINARY_SUBSCR    
             1688  LOAD_FAST                '_wdxl'
             1690  LOAD_FAST                '_seisinfo'
             1692  LOAD_STR                 'XLStep'
             1694  BINARY_SUBSCR    
             1696  BINARY_MULTIPLY  
             1698  BINARY_ADD       

 L. 617      1700  LOAD_FAST                '_seisinfo'
             1702  LOAD_STR                 'XLEnd'
             1704  BINARY_SUBSCR    
             1706  LOAD_FAST                '_wdxl'
             1708  LOAD_FAST                '_seisinfo'
             1710  LOAD_STR                 'XLStep'
             1712  BINARY_SUBSCR    
             1714  BINARY_MULTIPLY  
             1716  BINARY_SUBTRACT  

 L. 618      1718  LOAD_FAST                '_seisinfo'
             1720  LOAD_STR                 'ZStart'
             1722  BINARY_SUBSCR    
             1724  LOAD_FAST                '_wdz'
             1726  LOAD_FAST                '_seisinfo'
             1728  LOAD_STR                 'ZStep'
             1730  BINARY_SUBSCR    
             1732  BINARY_MULTIPLY  
             1734  BINARY_ADD       

 L. 619      1736  LOAD_FAST                '_seisinfo'
             1738  LOAD_STR                 'ZEnd'
             1740  BINARY_SUBSCR    
             1742  LOAD_FAST                '_wdz'
             1744  LOAD_FAST                '_seisinfo'
             1746  LOAD_STR                 'ZStep'
             1748  BINARY_SUBSCR    
             1750  BINARY_MULTIPLY  
             1752  BINARY_SUBTRACT  
             1754  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1756  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1758  STORE_FAST               '_traindata'

 L. 622      1760  LOAD_GLOBAL              np
             1762  LOAD_METHOD              shape
             1764  LOAD_FAST                '_traindata'
             1766  CALL_METHOD_1         1  '1 positional argument'
             1768  LOAD_CONST               0
             1770  BINARY_SUBSCR    
             1772  LOAD_CONST               0
             1774  COMPARE_OP               <=
         1776_1778  POP_JUMP_IF_FALSE  1816  'to 1816'

 L. 623      1780  LOAD_GLOBAL              vis_msg
             1782  LOAD_ATTR                print
             1784  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: No training sample found'
             1786  LOAD_STR                 'error'
             1788  LOAD_CONST               ('type',)
             1790  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1792  POP_TOP          

 L. 624      1794  LOAD_GLOBAL              QtWidgets
             1796  LOAD_ATTR                QMessageBox
             1798  LOAD_METHOD              critical
             1800  LOAD_DEREF               'self'
             1802  LOAD_ATTR                msgbox

 L. 625      1804  LOAD_STR                 'Train 2D-WCAE'

 L. 626      1806  LOAD_STR                 'No training sample found'
             1808  CALL_METHOD_3         3  '3 positional arguments'
             1810  POP_TOP          

 L. 627      1812  LOAD_CONST               None
             1814  RETURN_VALUE     
           1816_0  COME_FROM          1776  '1776'

 L. 630      1816  LOAD_GLOBAL              print
             1818  LOAD_STR                 'TrainMl2DWcaeFromScratch: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 631      1820  LOAD_FAST                '_image_height'
             1822  LOAD_FAST                '_image_width'
             1824  LOAD_FAST                '_image_height_new'
             1826  LOAD_FAST                '_image_width_new'
             1828  BUILD_TUPLE_4         4 
             1830  BINARY_MODULO    
             1832  CALL_FUNCTION_1       1  '1 positional argument'
             1834  POP_TOP          

 L. 632      1836  BUILD_MAP_0           0 
             1838  STORE_FAST               '_traindict'

 L. 633      1840  SETUP_LOOP         1912  'to 1912'
             1842  LOAD_FAST                '_features'
             1844  GET_ITER         
             1846  FOR_ITER           1910  'to 1910'
             1848  STORE_FAST               'f'

 L. 634      1850  LOAD_DEREF               'self'
             1852  LOAD_ATTR                seisdata
             1854  LOAD_FAST                'f'
             1856  BINARY_SUBSCR    
             1858  STORE_FAST               '_seisdata'

 L. 635      1860  LOAD_GLOBAL              seis_ays
             1862  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1864  LOAD_FAST                '_seisdata'
             1866  LOAD_FAST                '_traindata'
             1868  LOAD_DEREF               'self'
             1870  LOAD_ATTR                survinfo

 L. 636      1872  LOAD_FAST                '_wdinl'
             1874  LOAD_FAST                '_wdxl'
             1876  LOAD_FAST                '_wdz'

 L. 637      1878  LOAD_CONST               False
             1880  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1882  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1884  LOAD_CONST               None
             1886  LOAD_CONST               None
             1888  BUILD_SLICE_2         2 
             1890  LOAD_CONST               3
             1892  LOAD_CONST               None
             1894  BUILD_SLICE_2         2 
             1896  BUILD_TUPLE_2         2 
             1898  BINARY_SUBSCR    
             1900  LOAD_FAST                '_traindict'
             1902  LOAD_FAST                'f'
             1904  STORE_SUBSCR     
         1906_1908  JUMP_BACK          1846  'to 1846'
             1910  POP_BLOCK        
           1912_0  COME_FROM_LOOP     1840  '1840'

 L. 638      1912  LOAD_FAST                '_target'
             1914  LOAD_FAST                '_features'
             1916  COMPARE_OP               not-in
         1918_1920  POP_JUMP_IF_FALSE  1978  'to 1978'

 L. 639      1922  LOAD_DEREF               'self'
             1924  LOAD_ATTR                seisdata
             1926  LOAD_FAST                '_target'
             1928  BINARY_SUBSCR    
             1930  STORE_FAST               '_seisdata'

 L. 640      1932  LOAD_GLOBAL              seis_ays
             1934  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1936  LOAD_FAST                '_seisdata'
             1938  LOAD_FAST                '_traindata'
             1940  LOAD_DEREF               'self'
             1942  LOAD_ATTR                survinfo

 L. 641      1944  LOAD_FAST                '_wdinl'
             1946  LOAD_FAST                '_wdxl'
             1948  LOAD_FAST                '_wdz'

 L. 642      1950  LOAD_CONST               False
             1952  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1954  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1956  LOAD_CONST               None
             1958  LOAD_CONST               None
             1960  BUILD_SLICE_2         2 
             1962  LOAD_CONST               3
             1964  LOAD_CONST               None
             1966  BUILD_SLICE_2         2 
             1968  BUILD_TUPLE_2         2 
             1970  BINARY_SUBSCR    
             1972  LOAD_FAST                '_traindict'
             1974  LOAD_FAST                '_target'
             1976  STORE_SUBSCR     
           1978_0  COME_FROM          1918  '1918'

 L. 643      1978  LOAD_FAST                '_weight'
             1980  LOAD_FAST                '_features'
             1982  COMPARE_OP               not-in
         1984_1986  POP_JUMP_IF_FALSE  2054  'to 2054'
             1988  LOAD_FAST                '_weight'
             1990  LOAD_FAST                '_target'
             1992  COMPARE_OP               !=
         1994_1996  POP_JUMP_IF_FALSE  2054  'to 2054'

 L. 644      1998  LOAD_DEREF               'self'
             2000  LOAD_ATTR                seisdata
             2002  LOAD_FAST                '_weight'
             2004  BINARY_SUBSCR    
             2006  STORE_FAST               '_seisdata'

 L. 645      2008  LOAD_GLOBAL              seis_ays
             2010  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2012  LOAD_FAST                '_seisdata'
             2014  LOAD_FAST                '_traindata'
             2016  LOAD_DEREF               'self'
             2018  LOAD_ATTR                survinfo

 L. 646      2020  LOAD_FAST                '_wdinl'
             2022  LOAD_FAST                '_wdxl'
             2024  LOAD_FAST                '_wdz'

 L. 647      2026  LOAD_CONST               False
             2028  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2030  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2032  LOAD_CONST               None
             2034  LOAD_CONST               None
             2036  BUILD_SLICE_2         2 
             2038  LOAD_CONST               3
             2040  LOAD_CONST               None
             2042  BUILD_SLICE_2         2 
             2044  BUILD_TUPLE_2         2 
             2046  BINARY_SUBSCR    
             2048  LOAD_FAST                '_traindict'
             2050  LOAD_FAST                '_weight'
             2052  STORE_SUBSCR     
           2054_0  COME_FROM          1994  '1994'
           2054_1  COME_FROM          1984  '1984'

 L. 648      2054  LOAD_DEREF               'self'
             2056  LOAD_ATTR                traindataconfig
             2058  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2060  BINARY_SUBSCR    
         2062_2064  POP_JUMP_IF_FALSE  2146  'to 2146'

 L. 649      2066  SETUP_LOOP         2146  'to 2146'
             2068  LOAD_FAST                '_features'
             2070  GET_ITER         
           2072_0  COME_FROM          2100  '2100'
             2072  FOR_ITER           2144  'to 2144'
             2074  STORE_FAST               'f'

 L. 650      2076  LOAD_GLOBAL              ml_aug
             2078  LOAD_METHOD              removeInvariantFeature
             2080  LOAD_FAST                '_traindict'
             2082  LOAD_FAST                'f'
             2084  CALL_METHOD_2         2  '2 positional arguments'
             2086  STORE_FAST               '_traindict'

 L. 651      2088  LOAD_GLOBAL              basic_mdt
             2090  LOAD_METHOD              maxDictConstantRow
             2092  LOAD_FAST                '_traindict'
             2094  CALL_METHOD_1         1  '1 positional argument'
             2096  LOAD_CONST               0
             2098  COMPARE_OP               <=
         2100_2102  POP_JUMP_IF_FALSE  2072  'to 2072'

 L. 652      2104  LOAD_GLOBAL              vis_msg
             2106  LOAD_ATTR                print
             2108  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: No training sample found'
             2110  LOAD_STR                 'error'
             2112  LOAD_CONST               ('type',)
             2114  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2116  POP_TOP          

 L. 653      2118  LOAD_GLOBAL              QtWidgets
             2120  LOAD_ATTR                QMessageBox
             2122  LOAD_METHOD              critical
             2124  LOAD_DEREF               'self'
             2126  LOAD_ATTR                msgbox

 L. 654      2128  LOAD_STR                 'Train 2D-WCAE'

 L. 655      2130  LOAD_STR                 'No training sample found'
             2132  CALL_METHOD_3         3  '3 positional arguments'
             2134  POP_TOP          

 L. 656      2136  LOAD_CONST               None
             2138  RETURN_VALUE     
         2140_2142  JUMP_BACK          2072  'to 2072'
             2144  POP_BLOCK        
           2146_0  COME_FROM_LOOP     2066  '2066'
           2146_1  COME_FROM          2062  '2062'

 L. 657      2146  LOAD_DEREF               'self'
             2148  LOAD_ATTR                traindataconfig
             2150  LOAD_STR                 'RemoveZeroWeight_Checked'
             2152  BINARY_SUBSCR    
         2154_2156  POP_JUMP_IF_FALSE  2222  'to 2222'

 L. 658      2158  LOAD_GLOBAL              ml_aug
             2160  LOAD_METHOD              removeZeroWeight
             2162  LOAD_FAST                '_traindict'
             2164  LOAD_FAST                '_weight'
             2166  CALL_METHOD_2         2  '2 positional arguments'
             2168  STORE_FAST               '_traindict'

 L. 659      2170  LOAD_GLOBAL              basic_mdt
             2172  LOAD_METHOD              maxDictConstantRow
             2174  LOAD_FAST                '_traindict'
             2176  CALL_METHOD_1         1  '1 positional argument'
             2178  LOAD_CONST               0
             2180  COMPARE_OP               <=
         2182_2184  POP_JUMP_IF_FALSE  2222  'to 2222'

 L. 660      2186  LOAD_GLOBAL              vis_msg
             2188  LOAD_ATTR                print
             2190  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: No training sample found'
             2192  LOAD_STR                 'error'
             2194  LOAD_CONST               ('type',)
             2196  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2198  POP_TOP          

 L. 661      2200  LOAD_GLOBAL              QtWidgets
             2202  LOAD_ATTR                QMessageBox
             2204  LOAD_METHOD              critical
             2206  LOAD_DEREF               'self'
             2208  LOAD_ATTR                msgbox

 L. 662      2210  LOAD_STR                 'Train 2D-WCAE'

 L. 663      2212  LOAD_STR                 'No training sample found'
             2214  CALL_METHOD_3         3  '3 positional arguments'
             2216  POP_TOP          

 L. 664      2218  LOAD_CONST               None
             2220  RETURN_VALUE     
           2222_0  COME_FROM          2182  '2182'
           2222_1  COME_FROM          2154  '2154'

 L. 666      2222  LOAD_GLOBAL              np
             2224  LOAD_METHOD              shape
             2226  LOAD_FAST                '_traindict'
             2228  LOAD_FAST                '_target'
             2230  BINARY_SUBSCR    
             2232  CALL_METHOD_1         1  '1 positional argument'
             2234  LOAD_CONST               0
             2236  BINARY_SUBSCR    
             2238  LOAD_CONST               0
             2240  COMPARE_OP               <=
         2242_2244  POP_JUMP_IF_FALSE  2282  'to 2282'

 L. 667      2246  LOAD_GLOBAL              vis_msg
             2248  LOAD_ATTR                print
             2250  LOAD_STR                 'ERROR in TrainMl2DWcaeFromScratch: No training sample found'
             2252  LOAD_STR                 'error'
             2254  LOAD_CONST               ('type',)
             2256  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2258  POP_TOP          

 L. 668      2260  LOAD_GLOBAL              QtWidgets
             2262  LOAD_ATTR                QMessageBox
             2264  LOAD_METHOD              critical
             2266  LOAD_DEREF               'self'
             2268  LOAD_ATTR                msgbox

 L. 669      2270  LOAD_STR                 'Train 2D-WCAE'

 L. 670      2272  LOAD_STR                 'No training sample found'
             2274  CALL_METHOD_3         3  '3 positional arguments'
             2276  POP_TOP          

 L. 671      2278  LOAD_CONST               None
             2280  RETURN_VALUE     
           2282_0  COME_FROM          2242  '2242'

 L. 673      2282  LOAD_FAST                '_image_height_new'
             2284  LOAD_FAST                '_image_height'
             2286  COMPARE_OP               !=
         2288_2290  POP_JUMP_IF_TRUE   2302  'to 2302'
             2292  LOAD_FAST                '_image_width_new'
             2294  LOAD_FAST                '_image_width'
             2296  COMPARE_OP               !=
         2298_2300  POP_JUMP_IF_FALSE  2436  'to 2436'
           2302_0  COME_FROM          2288  '2288'

 L. 674      2302  SETUP_LOOP         2346  'to 2346'
             2304  LOAD_FAST                '_features'
             2306  GET_ITER         
             2308  FOR_ITER           2344  'to 2344'
             2310  STORE_FAST               'f'

 L. 675      2312  LOAD_GLOBAL              basic_image
             2314  LOAD_ATTR                changeImageSize
             2316  LOAD_FAST                '_traindict'
             2318  LOAD_FAST                'f'
             2320  BINARY_SUBSCR    

 L. 676      2322  LOAD_FAST                '_image_height'

 L. 677      2324  LOAD_FAST                '_image_width'

 L. 678      2326  LOAD_FAST                '_image_height_new'

 L. 679      2328  LOAD_FAST                '_image_width_new'
             2330  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2332  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2334  LOAD_FAST                '_traindict'
             2336  LOAD_FAST                'f'
             2338  STORE_SUBSCR     
         2340_2342  JUMP_BACK          2308  'to 2308'
             2344  POP_BLOCK        
           2346_0  COME_FROM_LOOP     2302  '2302'

 L. 680      2346  LOAD_FAST                '_target'
             2348  LOAD_FAST                '_features'
             2350  COMPARE_OP               not-in
         2352_2354  POP_JUMP_IF_FALSE  2386  'to 2386'

 L. 681      2356  LOAD_GLOBAL              basic_image
             2358  LOAD_ATTR                changeImageSize
             2360  LOAD_FAST                '_traindict'
             2362  LOAD_FAST                '_target'
             2364  BINARY_SUBSCR    

 L. 682      2366  LOAD_FAST                '_image_height'

 L. 683      2368  LOAD_FAST                '_image_width'

 L. 684      2370  LOAD_FAST                '_image_height_new'

 L. 685      2372  LOAD_FAST                '_image_width_new'
             2374  LOAD_STR                 'linear'
             2376  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2378  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2380  LOAD_FAST                '_traindict'
             2382  LOAD_FAST                '_target'
             2384  STORE_SUBSCR     
           2386_0  COME_FROM          2352  '2352'

 L. 686      2386  LOAD_FAST                '_weight'
             2388  LOAD_FAST                '_features'
             2390  COMPARE_OP               not-in
         2392_2394  POP_JUMP_IF_FALSE  2436  'to 2436'
             2396  LOAD_FAST                '_weight'
             2398  LOAD_FAST                '_target'
             2400  COMPARE_OP               !=
         2402_2404  POP_JUMP_IF_FALSE  2436  'to 2436'

 L. 687      2406  LOAD_GLOBAL              basic_image
             2408  LOAD_ATTR                changeImageSize
             2410  LOAD_FAST                '_traindict'
             2412  LOAD_FAST                '_weight'
             2414  BINARY_SUBSCR    

 L. 688      2416  LOAD_FAST                '_image_height'

 L. 689      2418  LOAD_FAST                '_image_width'

 L. 690      2420  LOAD_FAST                '_image_height_new'

 L. 691      2422  LOAD_FAST                '_image_width_new'
             2424  LOAD_STR                 'linear'
             2426  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2428  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2430  LOAD_FAST                '_traindict'
             2432  LOAD_FAST                '_weight'
             2434  STORE_SUBSCR     
           2436_0  COME_FROM          2402  '2402'
           2436_1  COME_FROM          2392  '2392'
           2436_2  COME_FROM          2298  '2298'

 L. 692      2436  LOAD_DEREF               'self'
             2438  LOAD_ATTR                traindataconfig
             2440  LOAD_STR                 'RotateFeature_Checked'
             2442  BINARY_SUBSCR    
             2444  LOAD_CONST               True
             2446  COMPARE_OP               is
         2448_2450  POP_JUMP_IF_FALSE  2666  'to 2666'

 L. 693      2452  SETUP_LOOP         2524  'to 2524'
             2454  LOAD_FAST                '_features'
             2456  GET_ITER         
             2458  FOR_ITER           2522  'to 2522'
             2460  STORE_FAST               'f'

 L. 694      2462  LOAD_FAST                '_image_height_new'
             2464  LOAD_FAST                '_image_width_new'
             2466  COMPARE_OP               ==
         2468_2470  POP_JUMP_IF_FALSE  2496  'to 2496'

 L. 695      2472  LOAD_GLOBAL              ml_aug
             2474  LOAD_METHOD              rotateImage6Way
             2476  LOAD_FAST                '_traindict'
             2478  LOAD_FAST                'f'
             2480  BINARY_SUBSCR    
             2482  LOAD_FAST                '_image_height_new'
             2484  LOAD_FAST                '_image_width_new'
             2486  CALL_METHOD_3         3  '3 positional arguments'
             2488  LOAD_FAST                '_traindict'
             2490  LOAD_FAST                'f'
             2492  STORE_SUBSCR     
             2494  JUMP_BACK          2458  'to 2458'
           2496_0  COME_FROM          2468  '2468'

 L. 697      2496  LOAD_GLOBAL              ml_aug
             2498  LOAD_METHOD              rotateImage4Way
             2500  LOAD_FAST                '_traindict'
             2502  LOAD_FAST                'f'
             2504  BINARY_SUBSCR    
             2506  LOAD_FAST                '_image_height_new'
             2508  LOAD_FAST                '_image_width_new'
             2510  CALL_METHOD_3         3  '3 positional arguments'
             2512  LOAD_FAST                '_traindict'
             2514  LOAD_FAST                'f'
             2516  STORE_SUBSCR     
         2518_2520  JUMP_BACK          2458  'to 2458'
             2522  POP_BLOCK        
           2524_0  COME_FROM_LOOP     2452  '2452'

 L. 698      2524  LOAD_FAST                '_target'
             2526  LOAD_FAST                '_features'
             2528  COMPARE_OP               not-in
         2530_2532  POP_JUMP_IF_FALSE  2590  'to 2590'

 L. 699      2534  LOAD_FAST                '_image_height_new'
             2536  LOAD_FAST                '_image_width_new'
             2538  COMPARE_OP               ==
         2540_2542  POP_JUMP_IF_FALSE  2568  'to 2568'

 L. 701      2544  LOAD_GLOBAL              ml_aug
             2546  LOAD_METHOD              rotateImage6Way
             2548  LOAD_FAST                '_traindict'
             2550  LOAD_FAST                '_target'
             2552  BINARY_SUBSCR    
             2554  LOAD_FAST                '_image_height_new'
             2556  LOAD_FAST                '_image_width_new'
             2558  CALL_METHOD_3         3  '3 positional arguments'
             2560  LOAD_FAST                '_traindict'
             2562  LOAD_FAST                '_target'
             2564  STORE_SUBSCR     
             2566  JUMP_FORWARD       2590  'to 2590'
           2568_0  COME_FROM          2540  '2540'

 L. 704      2568  LOAD_GLOBAL              ml_aug
             2570  LOAD_METHOD              rotateImage4Way
             2572  LOAD_FAST                '_traindict'
             2574  LOAD_FAST                '_target'
             2576  BINARY_SUBSCR    
             2578  LOAD_FAST                '_image_height_new'
             2580  LOAD_FAST                '_image_width_new'
             2582  CALL_METHOD_3         3  '3 positional arguments'
             2584  LOAD_FAST                '_traindict'
             2586  LOAD_FAST                '_target'
             2588  STORE_SUBSCR     
           2590_0  COME_FROM          2566  '2566'
           2590_1  COME_FROM          2530  '2530'

 L. 705      2590  LOAD_FAST                '_weight'
             2592  LOAD_FAST                '_features'
             2594  COMPARE_OP               not-in
         2596_2598  POP_JUMP_IF_FALSE  2666  'to 2666'
             2600  LOAD_FAST                '_weight'
             2602  LOAD_FAST                '_target'
             2604  COMPARE_OP               !=
         2606_2608  POP_JUMP_IF_FALSE  2666  'to 2666'

 L. 706      2610  LOAD_FAST                '_image_height_new'
             2612  LOAD_FAST                '_image_width_new'
             2614  COMPARE_OP               ==
         2616_2618  POP_JUMP_IF_FALSE  2644  'to 2644'

 L. 708      2620  LOAD_GLOBAL              ml_aug
             2622  LOAD_METHOD              rotateImage6Way
             2624  LOAD_FAST                '_traindict'
             2626  LOAD_FAST                '_weight'
             2628  BINARY_SUBSCR    
             2630  LOAD_FAST                '_image_height_new'
             2632  LOAD_FAST                '_image_width_new'
             2634  CALL_METHOD_3         3  '3 positional arguments'
             2636  LOAD_FAST                '_traindict'
             2638  LOAD_FAST                '_weight'
             2640  STORE_SUBSCR     
             2642  JUMP_FORWARD       2666  'to 2666'
           2644_0  COME_FROM          2616  '2616'

 L. 711      2644  LOAD_GLOBAL              ml_aug
             2646  LOAD_METHOD              rotateImage4Way
             2648  LOAD_FAST                '_traindict'
             2650  LOAD_FAST                '_weight'
             2652  BINARY_SUBSCR    
             2654  LOAD_FAST                '_image_height_new'
             2656  LOAD_FAST                '_image_width_new'
             2658  CALL_METHOD_3         3  '3 positional arguments'
             2660  LOAD_FAST                '_traindict'
             2662  LOAD_FAST                '_weight'
             2664  STORE_SUBSCR     
           2666_0  COME_FROM          2642  '2642'
           2666_1  COME_FROM          2606  '2606'
           2666_2  COME_FROM          2596  '2596'
           2666_3  COME_FROM          2448  '2448'

 L. 714      2666  LOAD_GLOBAL              print
             2668  LOAD_STR                 'TrainMl2DWcaeFromScratch: A total of %d valid training samples'
             2670  LOAD_GLOBAL              basic_mdt
             2672  LOAD_METHOD              maxDictConstantRow

 L. 715      2674  LOAD_FAST                '_traindict'
             2676  CALL_METHOD_1         1  '1 positional argument'
             2678  BINARY_MODULO    
             2680  CALL_FUNCTION_1       1  '1 positional argument'
             2682  POP_TOP          

 L. 717      2684  LOAD_GLOBAL              print
             2686  LOAD_STR                 'TrainMl2DWcaeFromScratch: Step 3 - Start training'
             2688  CALL_FUNCTION_1       1  '1 positional argument'
             2690  POP_TOP          

 L. 719      2692  LOAD_GLOBAL              QtWidgets
             2694  LOAD_METHOD              QProgressDialog
             2696  CALL_METHOD_0         0  '0 positional arguments'
             2698  STORE_FAST               '_pgsdlg'

 L. 720      2700  LOAD_GLOBAL              QtGui
             2702  LOAD_METHOD              QIcon
             2704  CALL_METHOD_0         0  '0 positional arguments'
             2706  STORE_FAST               'icon'

 L. 721      2708  LOAD_FAST                'icon'
             2710  LOAD_METHOD              addPixmap
             2712  LOAD_GLOBAL              QtGui
             2714  LOAD_METHOD              QPixmap
             2716  LOAD_GLOBAL              os
             2718  LOAD_ATTR                path
             2720  LOAD_METHOD              join
             2722  LOAD_DEREF               'self'
             2724  LOAD_ATTR                iconpath
             2726  LOAD_STR                 'icons/new.png'
             2728  CALL_METHOD_2         2  '2 positional arguments'
             2730  CALL_METHOD_1         1  '1 positional argument'

 L. 722      2732  LOAD_GLOBAL              QtGui
             2734  LOAD_ATTR                QIcon
             2736  LOAD_ATTR                Normal
             2738  LOAD_GLOBAL              QtGui
             2740  LOAD_ATTR                QIcon
             2742  LOAD_ATTR                Off
             2744  CALL_METHOD_3         3  '3 positional arguments'
             2746  POP_TOP          

 L. 723      2748  LOAD_FAST                '_pgsdlg'
             2750  LOAD_METHOD              setWindowIcon
             2752  LOAD_FAST                'icon'
             2754  CALL_METHOD_1         1  '1 positional argument'
             2756  POP_TOP          

 L. 724      2758  LOAD_FAST                '_pgsdlg'
             2760  LOAD_METHOD              setWindowTitle
             2762  LOAD_STR                 'Train 2D-CAE'
             2764  CALL_METHOD_1         1  '1 positional argument'
             2766  POP_TOP          

 L. 725      2768  LOAD_FAST                '_pgsdlg'
             2770  LOAD_METHOD              setCancelButton
             2772  LOAD_CONST               None
             2774  CALL_METHOD_1         1  '1 positional argument'
             2776  POP_TOP          

 L. 726      2778  LOAD_FAST                '_pgsdlg'
             2780  LOAD_METHOD              setWindowFlags
             2782  LOAD_GLOBAL              QtCore
             2784  LOAD_ATTR                Qt
             2786  LOAD_ATTR                WindowStaysOnTopHint
             2788  CALL_METHOD_1         1  '1 positional argument'
             2790  POP_TOP          

 L. 727      2792  LOAD_FAST                '_pgsdlg'
             2794  LOAD_METHOD              forceShow
             2796  CALL_METHOD_0         0  '0 positional arguments'
             2798  POP_TOP          

 L. 728      2800  LOAD_FAST                '_pgsdlg'
             2802  LOAD_METHOD              setFixedWidth
             2804  LOAD_CONST               400
             2806  CALL_METHOD_1         1  '1 positional argument'
             2808  POP_TOP          

 L. 729      2810  LOAD_GLOBAL              ml_wcae
             2812  LOAD_ATTR                createWCAEReconstructor
             2814  LOAD_FAST                '_traindict'

 L. 730      2816  LOAD_FAST                '_image_height_new'
             2818  LOAD_FAST                '_image_width_new'

 L. 731      2820  LOAD_FAST                '_features'

 L. 732      2822  LOAD_FAST                '_target'
             2824  LOAD_FAST                '_weight'

 L. 733      2826  LOAD_FAST                '_nepoch'
             2828  LOAD_FAST                '_batchsize'

 L. 734      2830  LOAD_FAST                '_nconvblock'
             2832  LOAD_FAST                '_nconvfeature'

 L. 735      2834  LOAD_FAST                '_nconvlayer'

 L. 736      2836  LOAD_FAST                '_n1x1layer'
             2838  LOAD_FAST                '_n1x1feature'

 L. 737      2840  LOAD_FAST                '_patch_height'
             2842  LOAD_FAST                '_patch_width'

 L. 738      2844  LOAD_FAST                '_pool_height'
             2846  LOAD_FAST                '_pool_width'

 L. 739      2848  LOAD_FAST                '_learning_rate'

 L. 740      2850  LOAD_FAST                '_dropout_prob'

 L. 741      2852  LOAD_CONST               True

 L. 742      2854  LOAD_FAST                '_savepath'
             2856  LOAD_FAST                '_savename'

 L. 743      2858  LOAD_FAST                '_pgsdlg'
             2860  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'weight', 'nepoch', 'batchsize', 'nconvblock', 'nconvfeature', 'nconvlayer', 'n1x1layer', 'n1x1feature', 'patchheight', 'patchwidth', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprob', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2862  CALL_FUNCTION_KW_23    23  '23 total positional and keyword args'
             2864  STORE_FAST               '_caelog'

 L. 746      2866  LOAD_GLOBAL              QtWidgets
             2868  LOAD_ATTR                QMessageBox
             2870  LOAD_METHOD              information
             2872  LOAD_DEREF               'self'
             2874  LOAD_ATTR                msgbox

 L. 747      2876  LOAD_STR                 'Train 2D-WCAE'

 L. 748      2878  LOAD_STR                 'WCAE trained successfully'
             2880  CALL_METHOD_3         3  '3 positional arguments'
             2882  POP_TOP          

 L. 750      2884  LOAD_GLOBAL              QtWidgets
             2886  LOAD_ATTR                QMessageBox
             2888  LOAD_METHOD              question
             2890  LOAD_DEREF               'self'
             2892  LOAD_ATTR                msgbox
             2894  LOAD_STR                 'Train 2D-WCAE'
             2896  LOAD_STR                 'View learning matrix?'

 L. 751      2898  LOAD_GLOBAL              QtWidgets
             2900  LOAD_ATTR                QMessageBox
             2902  LOAD_ATTR                Yes
             2904  LOAD_GLOBAL              QtWidgets
             2906  LOAD_ATTR                QMessageBox
             2908  LOAD_ATTR                No
             2910  BINARY_OR        

 L. 752      2912  LOAD_GLOBAL              QtWidgets
             2914  LOAD_ATTR                QMessageBox
             2916  LOAD_ATTR                Yes
             2918  CALL_METHOD_5         5  '5 positional arguments'
             2920  STORE_FAST               'reply'

 L. 754      2922  LOAD_FAST                'reply'
             2924  LOAD_GLOBAL              QtWidgets
             2926  LOAD_ATTR                QMessageBox
             2928  LOAD_ATTR                Yes
             2930  COMPARE_OP               ==
         2932_2934  POP_JUMP_IF_FALSE  3002  'to 3002'

 L. 755      2936  LOAD_GLOBAL              QtWidgets
             2938  LOAD_METHOD              QDialog
             2940  CALL_METHOD_0         0  '0 positional arguments'
             2942  STORE_FAST               '_viewmllearnmat'

 L. 756      2944  LOAD_GLOBAL              gui_viewmllearnmat
             2946  CALL_FUNCTION_0       0  '0 positional arguments'
             2948  STORE_FAST               '_gui'

 L. 757      2950  LOAD_FAST                '_caelog'
             2952  LOAD_STR                 'learning_curve'
             2954  BINARY_SUBSCR    
             2956  LOAD_FAST                '_gui'
             2958  STORE_ATTR               learnmat

 L. 758      2960  LOAD_DEREF               'self'
             2962  LOAD_ATTR                linestyle
             2964  LOAD_FAST                '_gui'
             2966  STORE_ATTR               linestyle

 L. 759      2968  LOAD_DEREF               'self'
             2970  LOAD_ATTR                fontstyle
             2972  LOAD_FAST                '_gui'
             2974  STORE_ATTR               fontstyle

 L. 760      2976  LOAD_FAST                '_gui'
             2978  LOAD_METHOD              setupGUI
             2980  LOAD_FAST                '_viewmllearnmat'
             2982  CALL_METHOD_1         1  '1 positional argument'
             2984  POP_TOP          

 L. 761      2986  LOAD_FAST                '_viewmllearnmat'
             2988  LOAD_METHOD              exec
             2990  CALL_METHOD_0         0  '0 positional arguments'
             2992  POP_TOP          

 L. 762      2994  LOAD_FAST                '_viewmllearnmat'
             2996  LOAD_METHOD              show
             2998  CALL_METHOD_0         0  '0 positional arguments'
             3000  POP_TOP          
           3002_0  COME_FROM          2932  '2932'

Parse error at or near `POP_TOP' instruction at offset 3000

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
    TrainMl2DWcaeFromScratch = QtWidgets.QWidget()
    gui = trainml2dwcaefromscratch()
    gui.setupGUI(TrainMl2DWcaeFromScratch)
    TrainMl2DWcaeFromScratch.show()
    sys.exit(app.exec_())