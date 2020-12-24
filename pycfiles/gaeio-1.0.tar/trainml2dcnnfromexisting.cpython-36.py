# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml2dcnnfromexisting.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 54015 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.seismic.analysis import analysis as seis_ays
from cognitivegeo.src.pointset.analysis import analysis as point_ays
from cognitivegeo.src.basic.data import data as basic_data
from cognitivegeo.src.basic.matdict import matdict as basic_mdt
from cognitivegeo.src.basic.image import image as basic_image
from cognitivegeo.src.ml.augmentation import augmentation as ml_aug
from cognitivegeo.src.ml.tfmodel import tfmodel as ml_tfm
from cognitivegeo.src.ml.cnnclassifier import cnnclassifier as ml_cnn
from cognitivegeo.src.gui.viewmllearnmat import viewmllearnmat as gui_viewmllearnmat
from cognitivegeo.src.gui.configmltraindata import configmltraindata as gui_configmltraindata
from cognitivegeo.src.vis.messager import messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml2dcnnfromexisting(object):
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
    traindataconfig['BalanceTarget_Enabled'] = True
    traindataconfig['BalanceTarget_Checked'] = False
    traindataconfig['RotateFeature_Enabled'] = True
    traindataconfig['RotateFeature_Checked'] = False
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False

    def setupGUI(self, TrainMl2DCnnFromExisting):
        TrainMl2DCnnFromExisting.setObjectName('TrainMl2DCnnFromExisting')
        TrainMl2DCnnFromExisting.setFixedSize(800, 610)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl2DCnnFromExisting.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl2DCnnFromExisting)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl2DCnnFromExisting)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl2DCnnFromExisting)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblexisting = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblexisting.setObjectName('lblexisting')
        self.lblexisting.setGeometry(QtCore.QRect(410, 50, 100, 30))
        self.ldtexisting = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtexisting.setObjectName('ldtexisting')
        self.ldtexisting.setGeometry(QtCore.QRect(510, 50, 210, 30))
        self.btnexisting = QtWidgets.QPushButton(TrainMl2DCnnFromExisting)
        self.btnexisting.setObjectName('btnexisting')
        self.btnexisting.setGeometry(QtCore.QRect(730, 50, 60, 30))
        self.lblnconvblockexisting = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblnconvblockexisting.setObjectName('lblnconvblockexisting')
        self.lblnconvblockexisting.setGeometry(QtCore.QRect(410, 90, 130, 30))
        self.ldtnconvblockexisting = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtnconvblockexisting.setObjectName('ldtnconvblockexisting')
        self.ldtnconvblockexisting.setGeometry(QtCore.QRect(550, 90, 40, 30))
        self.twgnconvblockexisting = QtWidgets.QTableWidget(TrainMl2DCnnFromExisting)
        self.twgnconvblockexisting.setObjectName('twgnconvblockexisting')
        self.twgnconvblockexisting.setGeometry(QtCore.QRect(610, 90, 180, 150))
        self.twgnconvblockexisting.setColumnCount(3)
        self.twgnconvblockexisting.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblockexisting.verticalHeader().hide()
        self.lblblockid = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblblockid.setObjectName('lblblockid')
        self.lblblockid.setGeometry(QtCore.QRect(410, 130, 130, 30))
        self.cbbblockid = QtWidgets.QComboBox(TrainMl2DCnnFromExisting)
        self.cbbblockid.setObjectName('cbbblockid')
        self.cbbblockid.setGeometry(QtCore.QRect(550, 130, 40, 30))
        self.lbllayerid = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lbllayerid.setObjectName('lbllayerid')
        self.lbllayerid.setGeometry(QtCore.QRect(410, 170, 130, 30))
        self.cbblayerid = QtWidgets.QComboBox(TrainMl2DCnnFromExisting)
        self.cbblayerid.setObjectName('cbblayerid')
        self.cbblayerid.setGeometry(QtCore.QRect(550, 170, 40, 30))
        self.lbltrainable = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lbltrainable.setObjectName('lbltrainable')
        self.lbltrainable.setGeometry(QtCore.QRect(410, 210, 130, 30))
        self.cbbtrainable = QtWidgets.QComboBox(TrainMl2DCnnFromExisting)
        self.cbbtrainable.setObjectName('cbbtrainable')
        self.cbbtrainable.setGeometry(QtCore.QRect(550, 210, 40, 30))
        self.lblappend = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblappend.setObjectName('lblappend')
        self.lblappend.setGeometry(QtCore.QRect(410, 250, 200, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 290, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 290, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl2DCnnFromExisting)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 330, 180, 180))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 290, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 290, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(TrainMl2DCnnFromExisting)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 330, 180, 180))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 520, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 520, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 520, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 560, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 560, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 520, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 520, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 520, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 560, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 560, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl2DCnnFromExisting)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 310, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 350, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.lblfcdropout = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblfcdropout.setObjectName('lblfcdropout')
        self.lblfcdropout.setGeometry(QtCore.QRect(210, 390, 130, 30))
        self.ldtfcdropout = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtfcdropout.setObjectName('ldtfcdropout')
        self.ldtfcdropout.setGeometry(QtCore.QRect(350, 390, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl2DCnnFromExisting)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 100, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl2DCnnFromExisting)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(110, 440, 210, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl2DCnnFromExisting)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 440, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl2DCnnFromExisting)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(120, 560, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl2DCnnFromExisting)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl2DCnnFromExisting.geometry().center().x()
        _center_y = TrainMl2DCnnFromExisting.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl2DCnnFromExisting)
        QtCore.QMetaObject.connectSlotsByName(TrainMl2DCnnFromExisting)

    def retranslateGUI(self, TrainMl2DCnnFromExisting):
        self.dialog = TrainMl2DCnnFromExisting
        _translate = QtCore.QCoreApplication.translate
        TrainMl2DCnnFromExisting.setWindowTitle(_translate('TrainMl2DCnnFromExisting', 'Train 2D-CNN from pre-trained'))
        self.lblfeature.setText(_translate('TrainMl2DCnnFromExisting', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl2DCnnFromExisting', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl2DCnnFromExisting', 'Select target:'))
        self.btnconfigtraindata.setText(_translate('UpdateMl2DCnn', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('TrainMl2DCnnFromExisting', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl2DCnnFromExisting', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl2DCnnFromExisting', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl2DCnnFromExisting', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl2DCnnFromExisting', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl2DCnnFromExisting', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl2DCnnFromExisting', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl2DCnnFromExisting', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl2DCnnFromExisting', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl2DCnnFromExisting', '32'))
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
                    item.setText(_translate('TrainMl2DCnnFromExisting', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl2DCnnFromExisting', 'Specify CNN architecture:'))
        self.lblexisting.setText(_translate('TrainMl2DCnnFromExisting', 'Select pre-trained:'))
        self.ldtexisting.setText(_translate('TrainMl2DCnnFromExisting', ''))
        self.ldtexisting.textChanged.connect(self.changeLdtExisting)
        self.btnexisting.setText(_translate('TrainMl2DCnnFromExisting', 'Browse'))
        self.btnexisting.clicked.connect(self.clickBtnExisting)
        self.lblnconvblockexisting.setText(_translate('TrainMl2DCnnFromExisting', 'Available conv. blocks:'))
        self.lblnconvblockexisting.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblockexisting.setText(_translate('TrainMl2DCnnFromExisting', ''))
        self.ldtnconvblockexisting.setEnabled(False)
        self.ldtnconvblockexisting.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblockexisting.textChanged.connect(self.changeLdtNconvblockExisting)
        self.twgnconvblockexisting.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblblockid.setText(_translate('TrainMl2DCnnFromExisting', 'Select conv. block ID:'))
        self.lblblockid.setAlignment(QtCore.Qt.AlignRight)
        self.cbbblockid.currentIndexChanged.connect(self.changeCbbBlockid)
        self.lbllayerid.setText(_translate('TrainMl2DCnnFromExisting', 'Select conv. layer ID:'))
        self.lbllayerid.setAlignment(QtCore.Qt.AlignRight)
        self.lbltrainable.setText(_translate('TrainMl2DCnnFromExisting', 'Is trainable?:'))
        self.lbltrainable.setAlignment(QtCore.Qt.AlignRight)
        self.cbbtrainable.addItems(['Yes', 'No'])
        self.lblappend.setText(_translate('TrainMl2DCnnFromExisting', 'Append more blocks & layers:'))
        self.lblnconvblock.setText(_translate('TrainMl2DCnnFromExisting', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl2DCnnFromExisting', '3'))
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

        self.lblnfclayer.setText(_translate('TrainMl2DCnnFromExisting', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('TrainMl2DCnnFromExisting', '2'))
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.twgnfclayer.setRowCount(2)
        for _idx in range(int(self.ldtnfclayer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl2DCnnFromExisting', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgnfclayer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgnfclayer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl2DCnnFromExisting', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl2DCnnFromExisting', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl2DCnnFromExisting', ''))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskheight.setEnabled(False)
        self.lblmaskwidth.setText(_translate('TrainMl2DCnnFromExisting', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl2DCnnFromExisting', ''))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskwidth.setEnabled(False)
        self.lblpoolsize.setText(_translate('TrainMl2DCnnFromExisting', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl2DCnnFromExisting', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl2DCnnFromExisting', ''))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl2DCnnFromExisting', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl2DCnnFromExisting', ''))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('TrainMl2DCnnFromExisting', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl2DCnnFromExisting', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl2DCnnFromExisting', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl2DCnnFromExisting', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl2DCnnFromExisting', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl2DCnnFromExisting', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl2DCnnFromExisting', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfcdropout.setText(_translate('TrainMl2DCnnFromExisting', 'MLP dropout rate:'))
        self.lblfcdropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtfcdropout.setText(_translate('TrainMl2DCnnFromExisting', '0.5'))
        self.ldtfcdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl2DCnnFromExisting', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl2DCnnFromExisting', ''))
        self.btnsave.setText(_translate('TrainMl2DCnnFromExisting', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl2DCnnFromExisting', 'Train 2D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl2DCnnFromExisting)

    def changeLdtExisting(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtexisting.text()):
            _modelpath = os.path.dirname(self.ldtexisting.text())
            _modelname = os.path.splitext(os.path.basename(self.ldtexisting.text()))[0]
        else:
            _modelpath = ''
            _modelname = ''
        if ml_tfm.isConvModel(_modelpath, _modelname) is True:
            _modelinfo = ml_tfm.getModelInfo(_modelpath, _modelname)
            self.ldtnconvblockexisting.setText(str(_modelinfo['number_conv_block']))
            self.ldtmaskheight.setText(str(_modelinfo['patch_size'][0]))
            self.ldtmaskwidth.setText(str(_modelinfo['patch_size'][1]))
            self.ldtpoolheight.setText(str(_modelinfo['pool_size'][0]))
            self.ldtpoolwidth.setText(str(_modelinfo['pool_size'][1]))
        else:
            self.ldtnconvblockexisting.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')

    def clickBtnExisting(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select pre-trained Network', (self.rootpath), filter='Tensorflow network files (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtexisting.setText(_file[0])

    def changeLdtNconvblockExisting(self):
        if os.path.exists(self.ldtexisting.text()):
            _modelpath = os.path.dirname(self.ldtexisting.text())
            _modelname = os.path.splitext(os.path.basename(self.ldtexisting.text()))[0]
        else:
            _modelpath = ''
            _modelname = ''
        if ml_tfm.isConvModel(_modelpath, _modelname) is True:
            _modelinfo = ml_tfm.getModelInfo(_modelpath, _modelname)
            _nlayer = _modelinfo['number_conv_block']
            self.twgnconvblockexisting.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblockexisting.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_modelinfo['number_conv_layer'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblockexisting.setItem(_idx, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_modelinfo['number_conv_feature'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblockexisting.setItem(_idx, 2, item)

            self.cbbblockid.clear()
            self.cbbblockid.addItems([str(_i + 1) for _i in range(_nlayer)])
        else:
            self.twgnconvblockexisting.setRowCount(0)
            self.cbbblockid.clear()

    def changeCbbBlockid(self):
        if os.path.exists(self.ldtexisting.text()):
            _modelpath = os.path.dirname(self.ldtexisting.text())
            _modelname = os.path.splitext(os.path.basename(self.ldtexisting.text()))[0]
        else:
            _modelpath = ''
            _modelname = ''
        if ml_tfm.isConvModel(_modelpath, _modelname) is True:
            _modelinfo = ml_tfm.getModelInfo(_modelpath, _modelname)
            _blockid = self.cbbblockid.currentIndex()
            self.cbblayerid.clear()
            self.cbblayerid.addItems([str(_i + 1) for _i in range(_modelinfo['number_conv_layer'][_blockid])])
        else:
            self.cbblayerid.clear()

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

    def clickBtnTrainMl2DCnnFromExisting(self):
        self.refreshMsgBox()
        if len(self.lwgfeature.selectedItems()) < 1:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: No feature selected for training', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'No feature selected for training')
            return
        _image_height_old = basic_data.str2int(self.ldtoldheight.text())
        _image_width_old = basic_data.str2int(self.ldtoldwidth.text())
        _image_height_new = basic_data.str2int(self.ldtnewheight.text())
        _image_width_new = basic_data.str2int(self.ldtnewwidth.text())
        if _image_height_old is False or _image_width_old is False or _image_height_new is False or _image_width_new is False:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Non-integer feature size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Non-integer feature size')
            return
        if _image_height_old < 2 or _image_width_old < 2 or _image_height_new < 2 or _image_width_new < 2:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Features are not 2D', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Features are not 2D')
            return
        _image_height_old = 2 * int(_image_height_old / 2) + 1
        _image_width_old = 2 * int(_image_width_old / 2) + 1
        _features = self.lwgfeature.selectedItems()
        _features = [f.text() for f in _features]
        _target = self.featurelist[self.cbbtarget.currentIndex()]
        if _target in _features:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Target also used as features', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Target also used as features')
            return
        if len(self.ldtexisting.text()) < 1:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: No name specified for pre-trained network', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'No name specified for pre-trained network')
            return
        _precnnpath = os.path.dirname(self.ldtexisting.text())
        _precnnname = os.path.splitext(os.path.basename(self.ldtexisting.text()))[0]
        _blockidx = self.cbbblockid.currentIndex()
        _layeridx = self.cbblayerid.currentIndex()
        _trainable = True
        if self.cbbtrainable.currentIndex() != 0:
            _trainable = False
        if ml_tfm.getConvModelNChannel(_precnnpath, _precnnname) != len(_features):
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Feature channel number not match with pre-trained network', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Feature channel number not match with pre-trained network')
            return
        _nconvblock = basic_data.str2int(self.ldtnconvblock.text())
        _nconvlayer = [basic_data.str2int(self.twgnconvblock.item(i, 1).text()) for i in range(_nconvblock)]
        _nconvfeature = [basic_data.str2int(self.twgnconvblock.item(i, 2).text()) for i in range(_nconvblock)]
        _nfclayer = basic_data.str2int(self.ldtnfclayer.text())
        _nfcneuron = [basic_data.str2int(self.twgnfclayer.item(i, 1).text()) for i in range(_nfclayer)]
        _patch_height = basic_data.str2int(self.ldtmaskheight.text())
        _patch_width = basic_data.str2int(self.ldtmaskwidth.text())
        _pool_height = basic_data.str2int(self.ldtpoolheight.text())
        _pool_width = basic_data.str2int(self.ldtpoolwidth.text())
        _nepoch = basic_data.str2int(self.ldtnepoch.text())
        _batchsize = basic_data.str2int(self.ldtbatchsize.text())
        _learning_rate = basic_data.str2float(self.ldtlearnrate.text())
        _dropout_prob_fclayer = basic_data.str2float(self.ldtfcdropout.text())
        if _nconvblock is False or _nconvblock <= 0:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Non-positive convolutional block number', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Non-positive convolutional block number')
            return
        for _i in _nconvlayer:
            if _i is False or _i < 1:
                vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Non-positive convolutional layer number', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Non-positive convolutional layer number')
                return

        for _i in _nconvfeature:
            if _i is False or _i < 1:
                vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Non-positive convolutional feature number', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Non-positive convolutional feature number')
                return

        if _nfclayer is False or _nfclayer <= 0:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Non-positive MLP layer number', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Non-positive MLP layer number')
            return
        for _i in _nfcneuron:
            if _i is False or _i < 1:
                vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Non-positive MLP neuron number', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Non-positive MLP neuron number')
                return

        if _patch_height is False or _patch_width is False or _patch_height < 1 or _patch_width < 1:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Non-positive convolutional patch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Non-positive convolutional patch size')
            return
        if _pool_height is False or _pool_width is False or _pool_height < 1 or _pool_width < 1:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Non-positive pooling size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Non-positive pooling size')
            return
        if _nepoch is False or _nepoch <= 0:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Non-positive epoch number', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Non-positive epoch number')
            return
        if _batchsize is False or _batchsize <= 0:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Non-positive batch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Non-positive batch size')
            return
        if _learning_rate is False or _learning_rate <= 0:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Non-positive learning rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Non-positive learning rate')
            return
        if _dropout_prob_fclayer is False or _dropout_prob_fclayer <= 0:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: Negative dropout rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'Negative dropout rate')
            return
        if len(self.ldtexisting.text()) < 1:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: No pre-trained network specified', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-DCNN', 'No pre-trained network specified')
            return
        if len(self.ldtsave.text()) < 1:
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: No name specified for CNN network', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'No name specified for CNN network')
            return
        _savepath = os.path.dirname(self.ldtsave.text())
        _savename = os.path.splitext(os.path.basename(self.ldtsave.text()))[0]
        _wdinl = 0
        _wdxl = 0
        _wdz = 0
        if self.cbbornt.currentIndex() == 0:
            _wdxl = int(_image_width_old / 2)
            _wdz = int(_image_height_old / 2)
        if self.cbbornt.currentIndex() == 1:
            _wdinl = int(_image_width_old / 2)
            _wdz = int(_image_height_old / 2)
        if self.cbbornt.currentIndex() == 2:
            _wdinl = int(_image_width_old / 2)
            _wdxl = int(_image_height_old / 2)
        _seisinfo = self.survinfo
        print('TrainMl2DCnnFromExisting: Step 1 - Get training samples:')
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
            vis_msg.print('ERROR in TrainMl2DCnnFromExisting: No training sample found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'No training sample found')
            return
        print('TrainMl2DCnnFromExisting: Step 2 - Retrieve and interpolate images: (%d, %d) --> (%d, %d)' % (
         _image_height_old, _image_width_old, _image_height_new, _image_width_new))
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
                    vis_msg.print('ERROR in TrainMl2DCnnFromExisting: No training sample found', type='error')
                    QtWidgets.QMessageBox.critical(self.msgbox, 'Train 2D-CNN', 'No training sample found')
                    return

        _traindict[_target] = np.round(_traindict[_target]).astype(int)
        if _image_height_new != _image_height_old or _image_width_new != _image_width_old:
            for f in _features:
                _traindict[f] = basic_image.changeImageSize((_traindict[f]), image_height=_image_height_old,
                  image_width=_image_width_old,
                  image_height_new=_image_height_new,
                  image_width_new=_image_width_new)

        else:
            if self.traindataconfig['RotateFeature_Checked'] is True:
                for f in _features:
                    if _image_height_new == _image_width_new:
                        _traindict[f] = ml_aug.rotateImage6Way(_traindict[f], _image_height_new, _image_width_new)
                    else:
                        _traindict[f] = ml_aug.rotateImage4Way(_traindict[f], _image_height_new, _image_width_new)

                if _image_height_new == _image_width_new:
                    _traindict[_target] = ml_aug.rotateImage6Way(_traindict[_target], 1, 1)
                else:
                    _traindict[_target] = ml_aug.rotateImage4Way(_traindict[_target], 1, 1)
            print('TrainMl2DCnnFromScratch: A total of %d valid training samples' % basic_mdt.maxDictConstantRow(_traindict))
            print('TrainMl2DCnnFromExisting: Step 3 - Balance labels')
            if self.traindataconfig['BalanceTarget_Checked']:
                _traindict = ml_aug.balanceLabelbyExtension(_traindict, _target)
                print('TrainMl2DCnnFromExisting: A total of %d training samples after balance' % np.shape(_traindict[_target])[0])
            else:
                print('TrainMl2DCnnFromExisting: No balance applied')
        print('TrainMl2DCnnFromExisting: Step 4 - Start training')
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Train 2D-CNN')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _cnnlog = ml_cnn.createCNNClassifierFromExisting(_traindict, imageheight=_image_height_new,
          imagewidth=_image_width_new,
          features=_features,
          target=_target,
          nepoch=_nepoch,
          batchsize=_batchsize,
          nconvblock=_nconvblock,
          nconvlayer=_nconvlayer,
          nconvfeature=_nconvfeature,
          nfclayer=_nfclayer,
          nfcneuron=_nfcneuron,
          poolheight=_pool_height,
          poolwidth=_pool_width,
          learningrate=_learning_rate,
          dropoutprobfclayer=_dropout_prob_fclayer,
          save2disk=True,
          savepath=_savepath,
          savename=_savename,
          qpgsdlg=_pgsdlg,
          precnnpath=_precnnpath,
          precnnname=_precnnname,
          blockidx=_blockidx,
          layeridx=_layeridx,
          trainable=_trainable)
        QtWidgets.QMessageBox.information(self.msgbox, 'Train 2D-CNN', 'CNN trained successfully')
        reply = QtWidgets.QMessageBox.question(self.msgbox, 'Train 2D-CNN', 'View learning matrix?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
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
    TrainMl2DCnnFromExisting = QtWidgets.QWidget()
    gui = trainml2dcnnfromexisting()
    gui.setupGUI(TrainMl2DCnnFromExisting)
    TrainMl2DCnnFromExisting.show()
    sys.exit(app.exec_())