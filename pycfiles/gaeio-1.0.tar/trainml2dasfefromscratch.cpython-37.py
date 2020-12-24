# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml2dasfefromscratch.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 42890 bytes
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

class trainml2dasfefromscratch(object):
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
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False

    def setupGUI(self, TrainMl2DAsfeFromScratch):
        TrainMl2DAsfeFromScratch.setObjectName('TrainMl2DAsfeFromScratch')
        TrainMl2DAsfeFromScratch.setFixedSize(800, 440)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl2DAsfeFromScratch.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl2DAsfeFromScratch)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl2DAsfeFromScratch)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 50, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 50, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl2DAsfeFromScratch)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 90, 180, 180))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 50, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 50, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(TrainMl2DAsfeFromScratch)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 90, 180, 180))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl2DAsfeFromScratch)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 260, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 260, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 300, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 300, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 300, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 300, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 340, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 340, 40, 30))
        self.lblfcdropout = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblfcdropout.setObjectName('lblfcdropout')
        self.lblfcdropout.setGeometry(QtCore.QRect(210, 340, 130, 30))
        self.ldtfcdropout = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtfcdropout.setObjectName('ldtfcdropout')
        self.ldtfcdropout.setGeometry(QtCore.QRect(350, 340, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl2DAsfeFromScratch)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 390, 100, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl2DAsfeFromScratch)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(110, 390, 210, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl2DAsfeFromScratch)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 390, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl2DAsfeFromScratch)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 390, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl2DAsfeFromScratch)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl2DAsfeFromScratch.geometry().center().x()
        _center_y = TrainMl2DAsfeFromScratch.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl2DAsfeFromScratch)
        QtCore.QMetaObject.connectSlotsByName(TrainMl2DAsfeFromScratch)

    def retranslateGUI(self, TrainMl2DAsfeFromScratch):
        self.dialog = TrainMl2DAsfeFromScratch
        _translate = QtCore.QCoreApplication.translate
        TrainMl2DAsfeFromScratch.setWindowTitle(_translate('TrainMl2DAsfeFromScratch', 'Train 2D-ASFE from scratch'))
        self.lblfeature.setText(_translate('TrainMl2DAsfeFromScratch', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl2DAsfeFromScratch', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbloldsize.setText(_translate('TrainMl2DAsfeFromScratch', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl2DAsfeFromScratch', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl2DAsfeFromScratch', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl2DAsfeFromScratch', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl2DAsfeFromScratch', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl2DAsfeFromScratch', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl2DAsfeFromScratch', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl2DAsfeFromScratch', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl2DAsfeFromScratch', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl2DAsfeFromScratch', '32'))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        if self.checkSurvInfo():
            self.featurelist.clear()
            self.lwgfeature.clear()
            _firstfeature = None
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    self.featurelist.append(i)
                    item = QtWidgets.QListWidgetItem(self.lwgfeature)
                    item.setText(_translate('TrainMl2DAsfeFromScratch', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
        self.lblnetwork.setText(_translate('TrainMl2DAsfeFromScratch', 'Specify ASFE architecture:'))
        self.lblnconvblock.setText(_translate('TrainMl2DAsfeFromScratch', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl2DAsfeFromScratch', '3'))
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

        self.lblnfclayer.setText(_translate('TrainMl2DAsfeFromScratch', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('TrainMl2DAsfeFromScratch', '2'))
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.twgnfclayer.setRowCount(2)
        for _idx in range(int(self.ldtnfclayer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl2DAsfeFromScratch', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgnfclayer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgnfclayer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl2DAsfeFromScratch', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl2DAsfeFromScratch', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl2DAsfeFromScratch', '3'))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('TrainMl2DAsfeFromScratch', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl2DAsfeFromScratch', '3'))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('TrainMl2DAsfeFromScratch', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl2DAsfeFromScratch', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl2DAsfeFromScratch', '2'))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl2DAsfeFromScratch', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl2DAsfeFromScratch', '2'))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfcdropout.setText(_translate('TrainMl2DAsfeFromScratch', 'MLP dropout rate:'))
        self.lblfcdropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtfcdropout.setText(_translate('TrainMl2DAsfeFromScratch', '0.5'))
        self.ldtfcdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.btnconfigtraindata.setText(_translate('TrainMl2DAsfeFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lblpara.setText(_translate('TrainMl2DAsfeFromScratch', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl2DAsfeFromScratch', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl2DAsfeFromScratch', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl2DAsfeFromScratch', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl2DAsfeFromScratch', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl2DAsfeFromScratch', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl2DAsfeFromScratch', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl2DAsfeFromScratch', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl2DAsfeFromScratch', ''))
        self.btnsave.setText(_translate('TrainMl2DAsfeFromScratch', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl2DAsfeFromScratch', 'Train 2D-ASFE'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl2DAsfeFromScratch)

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
        _file = _dialog.getSaveFileName(None, 'Save ASFE Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
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

    def clickBtnTrainMl2DAsfeFromScratch--- This code section failed: ---

 L. 425         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 427         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 428        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 429        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 430        50  LOAD_STR                 'Train 2D-ASFE'

 L. 431        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 432        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 434        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_image_height_old'

 L. 435        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_image_width_old'

 L. 436        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtnewheight
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_image_height_new'

 L. 437       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewwidth
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_image_width_new'

 L. 438       126  LOAD_FAST                '_image_height_old'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'
              134  LOAD_FAST                '_image_width_old'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_TRUE    158  'to 158'

 L. 439       142  LOAD_FAST                '_image_height_new'
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

 L. 440       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 441       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 442       182  LOAD_STR                 'Train 2D-ASFE'

 L. 443       184  LOAD_STR                 'Non-integer feature size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 444       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 445       194  LOAD_FAST                '_image_height_old'
              196  LOAD_CONST               2
              198  COMPARE_OP               <
              200  POP_JUMP_IF_TRUE    228  'to 228'
              202  LOAD_FAST                '_image_width_old'
              204  LOAD_CONST               2
              206  COMPARE_OP               <
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 446       210  LOAD_FAST                '_image_height_new'
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

 L. 447       228  LOAD_GLOBAL              vis_msg
              230  LOAD_ATTR                print
              232  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 448       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 449       252  LOAD_STR                 'Train 2D-ASFE'

 L. 450       254  LOAD_STR                 'Features are not 2D'
              256  CALL_METHOD_3         3  '3 positional arguments'
              258  POP_TOP          

 L. 451       260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           224  '224'

 L. 453       264  LOAD_CONST               2
              266  LOAD_GLOBAL              int
              268  LOAD_FAST                '_image_height_old'
              270  LOAD_CONST               2
              272  BINARY_TRUE_DIVIDE
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  BINARY_MULTIPLY  
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  STORE_FAST               '_image_height_old'

 L. 454       284  LOAD_CONST               2
              286  LOAD_GLOBAL              int
              288  LOAD_FAST                '_image_width_old'
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BINARY_MULTIPLY  
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               '_image_width_old'

 L. 456       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                lwgfeature
              308  LOAD_METHOD              selectedItems
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               '_features'

 L. 457       314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainml2dasfefromscratch.clickBtnTrainMl2DAsfeFromScratch.<locals>.<listcomp>'
              318  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              320  LOAD_FAST                '_features'
              322  GET_ITER         
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               '_features'

 L. 458       328  LOAD_STR                 '_'
              330  LOAD_METHOD              join
              332  LOAD_FAST                '_features'
              334  CALL_METHOD_1         1  '1 positional argument'
              336  LOAD_STR                 '_rotated'
              338  BINARY_ADD       
              340  STORE_FAST               '_target'

 L. 460       342  LOAD_FAST                '_target'
              344  LOAD_FAST                '_features'
              346  COMPARE_OP               in
          348_350  POP_JUMP_IF_FALSE   388  'to 388'

 L. 461       352  LOAD_GLOBAL              vis_msg
              354  LOAD_ATTR                print
              356  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Target also used as features'
              358  LOAD_STR                 'error'
              360  LOAD_CONST               ('type',)
              362  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              364  POP_TOP          

 L. 462       366  LOAD_GLOBAL              QtWidgets
              368  LOAD_ATTR                QMessageBox
              370  LOAD_METHOD              critical
              372  LOAD_DEREF               'self'
              374  LOAD_ATTR                msgbox

 L. 463       376  LOAD_STR                 'Train 2D-ASFE'

 L. 464       378  LOAD_STR                 'Target also used as features'
              380  CALL_METHOD_3         3  '3 positional arguments'
              382  POP_TOP          

 L. 465       384  LOAD_CONST               None
              386  RETURN_VALUE     
            388_0  COME_FROM           348  '348'

 L. 467       388  LOAD_GLOBAL              basic_data
              390  LOAD_METHOD              str2int
              392  LOAD_DEREF               'self'
              394  LOAD_ATTR                ldtnconvblock
              396  LOAD_METHOD              text
              398  CALL_METHOD_0         0  '0 positional arguments'
              400  CALL_METHOD_1         1  '1 positional argument'
              402  STORE_FAST               '_nconvblock'

 L. 468       404  LOAD_CLOSURE             'self'
              406  BUILD_TUPLE_1         1 
              408  LOAD_LISTCOMP            '<code_object <listcomp>>'
              410  LOAD_STR                 'trainml2dasfefromscratch.clickBtnTrainMl2DAsfeFromScratch.<locals>.<listcomp>'
              412  MAKE_FUNCTION_8          'closure'
              414  LOAD_GLOBAL              range
              416  LOAD_FAST                '_nconvblock'
              418  CALL_FUNCTION_1       1  '1 positional argument'
              420  GET_ITER         
              422  CALL_FUNCTION_1       1  '1 positional argument'
              424  STORE_FAST               '_nconvlayer'

 L. 469       426  LOAD_CLOSURE             'self'
              428  BUILD_TUPLE_1         1 
              430  LOAD_LISTCOMP            '<code_object <listcomp>>'
              432  LOAD_STR                 'trainml2dasfefromscratch.clickBtnTrainMl2DAsfeFromScratch.<locals>.<listcomp>'
              434  MAKE_FUNCTION_8          'closure'
              436  LOAD_GLOBAL              range
              438  LOAD_FAST                '_nconvblock'
              440  CALL_FUNCTION_1       1  '1 positional argument'
              442  GET_ITER         
              444  CALL_FUNCTION_1       1  '1 positional argument'
              446  STORE_FAST               '_nconvfeature'

 L. 470       448  LOAD_GLOBAL              basic_data
              450  LOAD_METHOD              str2int
              452  LOAD_DEREF               'self'
              454  LOAD_ATTR                ldtnfclayer
              456  LOAD_METHOD              text
              458  CALL_METHOD_0         0  '0 positional arguments'
              460  CALL_METHOD_1         1  '1 positional argument'
              462  STORE_FAST               '_nfclayer'

 L. 471       464  LOAD_CLOSURE             'self'
              466  BUILD_TUPLE_1         1 
              468  LOAD_LISTCOMP            '<code_object <listcomp>>'
              470  LOAD_STR                 'trainml2dasfefromscratch.clickBtnTrainMl2DAsfeFromScratch.<locals>.<listcomp>'
              472  MAKE_FUNCTION_8          'closure'
              474  LOAD_GLOBAL              range
              476  LOAD_FAST                '_nfclayer'
              478  CALL_FUNCTION_1       1  '1 positional argument'
              480  GET_ITER         
              482  CALL_FUNCTION_1       1  '1 positional argument'
              484  STORE_FAST               '_nfcneuron'

 L. 472       486  LOAD_GLOBAL              basic_data
              488  LOAD_METHOD              str2int
              490  LOAD_DEREF               'self'
              492  LOAD_ATTR                ldtmaskheight
              494  LOAD_METHOD              text
              496  CALL_METHOD_0         0  '0 positional arguments'
              498  CALL_METHOD_1         1  '1 positional argument'
              500  STORE_FAST               '_patch_height'

 L. 473       502  LOAD_GLOBAL              basic_data
              504  LOAD_METHOD              str2int
              506  LOAD_DEREF               'self'
              508  LOAD_ATTR                ldtmaskwidth
              510  LOAD_METHOD              text
              512  CALL_METHOD_0         0  '0 positional arguments'
              514  CALL_METHOD_1         1  '1 positional argument'
              516  STORE_FAST               '_patch_width'

 L. 474       518  LOAD_GLOBAL              basic_data
              520  LOAD_METHOD              str2int
              522  LOAD_DEREF               'self'
              524  LOAD_ATTR                ldtpoolheight
              526  LOAD_METHOD              text
              528  CALL_METHOD_0         0  '0 positional arguments'
              530  CALL_METHOD_1         1  '1 positional argument'
              532  STORE_FAST               '_pool_height'

 L. 475       534  LOAD_GLOBAL              basic_data
              536  LOAD_METHOD              str2int
              538  LOAD_DEREF               'self'
              540  LOAD_ATTR                ldtpoolwidth
              542  LOAD_METHOD              text
              544  CALL_METHOD_0         0  '0 positional arguments'
              546  CALL_METHOD_1         1  '1 positional argument'
              548  STORE_FAST               '_pool_width'

 L. 476       550  LOAD_GLOBAL              basic_data
              552  LOAD_METHOD              str2int
              554  LOAD_DEREF               'self'
              556  LOAD_ATTR                ldtnepoch
              558  LOAD_METHOD              text
              560  CALL_METHOD_0         0  '0 positional arguments'
              562  CALL_METHOD_1         1  '1 positional argument'
              564  STORE_FAST               '_nepoch'

 L. 477       566  LOAD_GLOBAL              basic_data
              568  LOAD_METHOD              str2int
              570  LOAD_DEREF               'self'
              572  LOAD_ATTR                ldtbatchsize
              574  LOAD_METHOD              text
              576  CALL_METHOD_0         0  '0 positional arguments'
              578  CALL_METHOD_1         1  '1 positional argument'
              580  STORE_FAST               '_batchsize'

 L. 478       582  LOAD_GLOBAL              float
              584  LOAD_DEREF               'self'
              586  LOAD_ATTR                ldtlearnrate
              588  LOAD_METHOD              text
              590  CALL_METHOD_0         0  '0 positional arguments'
              592  CALL_FUNCTION_1       1  '1 positional argument'
              594  STORE_FAST               '_learning_rate'

 L. 479       596  LOAD_GLOBAL              float
              598  LOAD_DEREF               'self'
              600  LOAD_ATTR                ldtfcdropout
              602  LOAD_METHOD              text
              604  CALL_METHOD_0         0  '0 positional arguments'
              606  CALL_FUNCTION_1       1  '1 positional argument'
              608  STORE_FAST               '_dropout_prob_fclayer'

 L. 480       610  LOAD_FAST                '_nconvblock'
              612  LOAD_CONST               False
              614  COMPARE_OP               is
          616_618  POP_JUMP_IF_TRUE    630  'to 630'
              620  LOAD_FAST                '_nconvblock'
              622  LOAD_CONST               0
              624  COMPARE_OP               <=
          626_628  POP_JUMP_IF_FALSE   666  'to 666'
            630_0  COME_FROM           616  '616'

 L. 481       630  LOAD_GLOBAL              vis_msg
              632  LOAD_ATTR                print
              634  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Non-positive convolutional block number'

 L. 482       636  LOAD_STR                 'error'
              638  LOAD_CONST               ('type',)
              640  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              642  POP_TOP          

 L. 483       644  LOAD_GLOBAL              QtWidgets
              646  LOAD_ATTR                QMessageBox
              648  LOAD_METHOD              critical
              650  LOAD_DEREF               'self'
              652  LOAD_ATTR                msgbox

 L. 484       654  LOAD_STR                 'Train 2D-ASFE'

 L. 485       656  LOAD_STR                 'Non-positive convolutional block number'
              658  CALL_METHOD_3         3  '3 positional arguments'
              660  POP_TOP          

 L. 486       662  LOAD_CONST               None
              664  RETURN_VALUE     
            666_0  COME_FROM           626  '626'

 L. 487       666  SETUP_LOOP          738  'to 738'
              668  LOAD_FAST                '_nconvlayer'
              670  GET_ITER         
            672_0  COME_FROM           692  '692'
              672  FOR_ITER            736  'to 736'
              674  STORE_FAST               '_i'

 L. 488       676  LOAD_FAST                '_i'
              678  LOAD_CONST               False
              680  COMPARE_OP               is
          682_684  POP_JUMP_IF_TRUE    696  'to 696'
              686  LOAD_FAST                '_i'
              688  LOAD_CONST               1
              690  COMPARE_OP               <
          692_694  POP_JUMP_IF_FALSE   672  'to 672'
            696_0  COME_FROM           682  '682'

 L. 489       696  LOAD_GLOBAL              vis_msg
              698  LOAD_ATTR                print
              700  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Non-positive convolutional layer number'

 L. 490       702  LOAD_STR                 'error'
              704  LOAD_CONST               ('type',)
              706  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              708  POP_TOP          

 L. 491       710  LOAD_GLOBAL              QtWidgets
              712  LOAD_ATTR                QMessageBox
              714  LOAD_METHOD              critical
              716  LOAD_DEREF               'self'
              718  LOAD_ATTR                msgbox

 L. 492       720  LOAD_STR                 'Train 2D-ASFE'

 L. 493       722  LOAD_STR                 'Non-positive convolutional layer number'
              724  CALL_METHOD_3         3  '3 positional arguments'
              726  POP_TOP          

 L. 494       728  LOAD_CONST               None
              730  RETURN_VALUE     
          732_734  JUMP_BACK           672  'to 672'
              736  POP_BLOCK        
            738_0  COME_FROM_LOOP      666  '666'

 L. 495       738  SETUP_LOOP          810  'to 810'
              740  LOAD_FAST                '_nconvfeature'
              742  GET_ITER         
            744_0  COME_FROM           764  '764'
              744  FOR_ITER            808  'to 808'
              746  STORE_FAST               '_i'

 L. 496       748  LOAD_FAST                '_i'
              750  LOAD_CONST               False
              752  COMPARE_OP               is
          754_756  POP_JUMP_IF_TRUE    768  'to 768'
              758  LOAD_FAST                '_i'
              760  LOAD_CONST               1
              762  COMPARE_OP               <
          764_766  POP_JUMP_IF_FALSE   744  'to 744'
            768_0  COME_FROM           754  '754'

 L. 497       768  LOAD_GLOBAL              vis_msg
              770  LOAD_ATTR                print
              772  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Non-positive convolutional feature number'

 L. 498       774  LOAD_STR                 'error'
              776  LOAD_CONST               ('type',)
              778  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              780  POP_TOP          

 L. 499       782  LOAD_GLOBAL              QtWidgets
              784  LOAD_ATTR                QMessageBox
              786  LOAD_METHOD              critical
              788  LOAD_DEREF               'self'
              790  LOAD_ATTR                msgbox

 L. 500       792  LOAD_STR                 'Train 2D-ASFE'

 L. 501       794  LOAD_STR                 'Non-positive convolutional feature number'
              796  CALL_METHOD_3         3  '3 positional arguments'
              798  POP_TOP          

 L. 502       800  LOAD_CONST               None
              802  RETURN_VALUE     
          804_806  JUMP_BACK           744  'to 744'
              808  POP_BLOCK        
            810_0  COME_FROM_LOOP      738  '738'

 L. 503       810  LOAD_FAST                '_nfclayer'
              812  LOAD_CONST               False
              814  COMPARE_OP               is
          816_818  POP_JUMP_IF_TRUE    830  'to 830'
              820  LOAD_FAST                '_nfclayer'
              822  LOAD_CONST               0
              824  COMPARE_OP               <=
          826_828  POP_JUMP_IF_FALSE   866  'to 866'
            830_0  COME_FROM           816  '816'

 L. 504       830  LOAD_GLOBAL              vis_msg
              832  LOAD_ATTR                print
              834  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Non-positive MLP layer number'
              836  LOAD_STR                 'error'
              838  LOAD_CONST               ('type',)
              840  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              842  POP_TOP          

 L. 505       844  LOAD_GLOBAL              QtWidgets
              846  LOAD_ATTR                QMessageBox
              848  LOAD_METHOD              critical
              850  LOAD_DEREF               'self'
              852  LOAD_ATTR                msgbox

 L. 506       854  LOAD_STR                 'Train 2D-ASFE'

 L. 507       856  LOAD_STR                 'Non-positive MLP layer number'
              858  CALL_METHOD_3         3  '3 positional arguments'
              860  POP_TOP          

 L. 508       862  LOAD_CONST               None
              864  RETURN_VALUE     
            866_0  COME_FROM           826  '826'

 L. 509       866  SETUP_LOOP          938  'to 938'
              868  LOAD_FAST                '_nfcneuron'
              870  GET_ITER         
            872_0  COME_FROM           892  '892'
              872  FOR_ITER            936  'to 936'
              874  STORE_FAST               '_i'

 L. 510       876  LOAD_FAST                '_i'
              878  LOAD_CONST               False
              880  COMPARE_OP               is
          882_884  POP_JUMP_IF_TRUE    896  'to 896'
              886  LOAD_FAST                '_i'
              888  LOAD_CONST               1
              890  COMPARE_OP               <
          892_894  POP_JUMP_IF_FALSE   872  'to 872'
            896_0  COME_FROM           882  '882'

 L. 511       896  LOAD_GLOBAL              vis_msg
              898  LOAD_ATTR                print
              900  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Non-positive MLP neuron number'
              902  LOAD_STR                 'error'
              904  LOAD_CONST               ('type',)
              906  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              908  POP_TOP          

 L. 512       910  LOAD_GLOBAL              QtWidgets
              912  LOAD_ATTR                QMessageBox
              914  LOAD_METHOD              critical
              916  LOAD_DEREF               'self'
              918  LOAD_ATTR                msgbox

 L. 513       920  LOAD_STR                 'Train 2D-ASFE'

 L. 514       922  LOAD_STR                 'Non-positive MLP neuron number'
              924  CALL_METHOD_3         3  '3 positional arguments'
              926  POP_TOP          

 L. 515       928  LOAD_CONST               None
              930  RETURN_VALUE     
          932_934  JUMP_BACK           872  'to 872'
              936  POP_BLOCK        
            938_0  COME_FROM_LOOP      866  '866'

 L. 516       938  LOAD_FAST                '_patch_height'
              940  LOAD_CONST               False
              942  COMPARE_OP               is
          944_946  POP_JUMP_IF_TRUE    978  'to 978'
              948  LOAD_FAST                '_patch_width'
              950  LOAD_CONST               False
              952  COMPARE_OP               is
          954_956  POP_JUMP_IF_TRUE    978  'to 978'

 L. 517       958  LOAD_FAST                '_patch_height'
              960  LOAD_CONST               1
              962  COMPARE_OP               <
          964_966  POP_JUMP_IF_TRUE    978  'to 978'
              968  LOAD_FAST                '_patch_width'
              970  LOAD_CONST               1
              972  COMPARE_OP               <
          974_976  POP_JUMP_IF_FALSE  1014  'to 1014'
            978_0  COME_FROM           964  '964'
            978_1  COME_FROM           954  '954'
            978_2  COME_FROM           944  '944'

 L. 518       978  LOAD_GLOBAL              vis_msg
              980  LOAD_ATTR                print
              982  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Non-positive convolutional patch size'

 L. 519       984  LOAD_STR                 'error'
              986  LOAD_CONST               ('type',)
              988  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              990  POP_TOP          

 L. 520       992  LOAD_GLOBAL              QtWidgets
              994  LOAD_ATTR                QMessageBox
              996  LOAD_METHOD              critical
              998  LOAD_DEREF               'self'
             1000  LOAD_ATTR                msgbox

 L. 521      1002  LOAD_STR                 'Train 2D-ASFE'

 L. 522      1004  LOAD_STR                 'Non-positive convolutional patch size'
             1006  CALL_METHOD_3         3  '3 positional arguments'
             1008  POP_TOP          

 L. 523      1010  LOAD_CONST               None
             1012  RETURN_VALUE     
           1014_0  COME_FROM           974  '974'

 L. 524      1014  LOAD_FAST                '_pool_height'
             1016  LOAD_CONST               False
             1018  COMPARE_OP               is
         1020_1022  POP_JUMP_IF_TRUE   1054  'to 1054'
             1024  LOAD_FAST                '_pool_width'
             1026  LOAD_CONST               False
             1028  COMPARE_OP               is
         1030_1032  POP_JUMP_IF_TRUE   1054  'to 1054'

 L. 525      1034  LOAD_FAST                '_pool_height'
             1036  LOAD_CONST               1
             1038  COMPARE_OP               <
         1040_1042  POP_JUMP_IF_TRUE   1054  'to 1054'
             1044  LOAD_FAST                '_pool_width'
             1046  LOAD_CONST               1
             1048  COMPARE_OP               <
         1050_1052  POP_JUMP_IF_FALSE  1090  'to 1090'
           1054_0  COME_FROM          1040  '1040'
           1054_1  COME_FROM          1030  '1030'
           1054_2  COME_FROM          1020  '1020'

 L. 526      1054  LOAD_GLOBAL              vis_msg
             1056  LOAD_ATTR                print
             1058  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Non-positive pooling size'
             1060  LOAD_STR                 'error'
             1062  LOAD_CONST               ('type',)
             1064  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1066  POP_TOP          

 L. 527      1068  LOAD_GLOBAL              QtWidgets
             1070  LOAD_ATTR                QMessageBox
             1072  LOAD_METHOD              critical
             1074  LOAD_DEREF               'self'
             1076  LOAD_ATTR                msgbox

 L. 528      1078  LOAD_STR                 'Train 2D-ASFE'

 L. 529      1080  LOAD_STR                 'Non-positive pooling size'
             1082  CALL_METHOD_3         3  '3 positional arguments'
             1084  POP_TOP          

 L. 530      1086  LOAD_CONST               None
             1088  RETURN_VALUE     
           1090_0  COME_FROM          1050  '1050'

 L. 531      1090  LOAD_FAST                '_nepoch'
             1092  LOAD_CONST               False
             1094  COMPARE_OP               is
         1096_1098  POP_JUMP_IF_TRUE   1110  'to 1110'
             1100  LOAD_FAST                '_nepoch'
             1102  LOAD_CONST               0
             1104  COMPARE_OP               <=
         1106_1108  POP_JUMP_IF_FALSE  1146  'to 1146'
           1110_0  COME_FROM          1096  '1096'

 L. 532      1110  LOAD_GLOBAL              vis_msg
             1112  LOAD_ATTR                print
             1114  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Non-positive epoch number'
             1116  LOAD_STR                 'error'
             1118  LOAD_CONST               ('type',)
             1120  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1122  POP_TOP          

 L. 533      1124  LOAD_GLOBAL              QtWidgets
             1126  LOAD_ATTR                QMessageBox
             1128  LOAD_METHOD              critical
             1130  LOAD_DEREF               'self'
             1132  LOAD_ATTR                msgbox

 L. 534      1134  LOAD_STR                 'Train 2D-ASFE'

 L. 535      1136  LOAD_STR                 'Non-positive epoch number'
             1138  CALL_METHOD_3         3  '3 positional arguments'
             1140  POP_TOP          

 L. 536      1142  LOAD_CONST               None
             1144  RETURN_VALUE     
           1146_0  COME_FROM          1106  '1106'

 L. 537      1146  LOAD_FAST                '_batchsize'
             1148  LOAD_CONST               False
             1150  COMPARE_OP               is
         1152_1154  POP_JUMP_IF_TRUE   1166  'to 1166'
             1156  LOAD_FAST                '_batchsize'
             1158  LOAD_CONST               0
             1160  COMPARE_OP               <=
         1162_1164  POP_JUMP_IF_FALSE  1202  'to 1202'
           1166_0  COME_FROM          1152  '1152'

 L. 538      1166  LOAD_GLOBAL              vis_msg
             1168  LOAD_ATTR                print
             1170  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Non-positive batch size'
             1172  LOAD_STR                 'error'
             1174  LOAD_CONST               ('type',)
             1176  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1178  POP_TOP          

 L. 539      1180  LOAD_GLOBAL              QtWidgets
             1182  LOAD_ATTR                QMessageBox
             1184  LOAD_METHOD              critical
             1186  LOAD_DEREF               'self'
             1188  LOAD_ATTR                msgbox

 L. 540      1190  LOAD_STR                 'Train 2D-ASFE'

 L. 541      1192  LOAD_STR                 'Non-positive batch size'
             1194  CALL_METHOD_3         3  '3 positional arguments'
             1196  POP_TOP          

 L. 542      1198  LOAD_CONST               None
             1200  RETURN_VALUE     
           1202_0  COME_FROM          1162  '1162'

 L. 543      1202  LOAD_FAST                '_learning_rate'
             1204  LOAD_CONST               False
             1206  COMPARE_OP               is
         1208_1210  POP_JUMP_IF_TRUE   1222  'to 1222'
             1212  LOAD_FAST                '_learning_rate'
             1214  LOAD_CONST               0
             1216  COMPARE_OP               <=
         1218_1220  POP_JUMP_IF_FALSE  1258  'to 1258'
           1222_0  COME_FROM          1208  '1208'

 L. 544      1222  LOAD_GLOBAL              vis_msg
             1224  LOAD_ATTR                print
             1226  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Non-positive learning rate'
             1228  LOAD_STR                 'error'
             1230  LOAD_CONST               ('type',)
             1232  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1234  POP_TOP          

 L. 545      1236  LOAD_GLOBAL              QtWidgets
             1238  LOAD_ATTR                QMessageBox
             1240  LOAD_METHOD              critical
             1242  LOAD_DEREF               'self'
             1244  LOAD_ATTR                msgbox

 L. 546      1246  LOAD_STR                 'Train 2D-ASFE'

 L. 547      1248  LOAD_STR                 'Non-positive learning rate'
             1250  CALL_METHOD_3         3  '3 positional arguments'
             1252  POP_TOP          

 L. 548      1254  LOAD_CONST               None
             1256  RETURN_VALUE     
           1258_0  COME_FROM          1218  '1218'

 L. 549      1258  LOAD_FAST                '_dropout_prob_fclayer'
             1260  LOAD_CONST               False
             1262  COMPARE_OP               is
         1264_1266  POP_JUMP_IF_TRUE   1278  'to 1278'
             1268  LOAD_FAST                '_dropout_prob_fclayer'
             1270  LOAD_CONST               0
             1272  COMPARE_OP               <=
         1274_1276  POP_JUMP_IF_FALSE  1314  'to 1314'
           1278_0  COME_FROM          1264  '1264'

 L. 550      1278  LOAD_GLOBAL              vis_msg
             1280  LOAD_ATTR                print
             1282  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: Negative dropout rate'
             1284  LOAD_STR                 'error'
             1286  LOAD_CONST               ('type',)
             1288  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1290  POP_TOP          

 L. 551      1292  LOAD_GLOBAL              QtWidgets
             1294  LOAD_ATTR                QMessageBox
             1296  LOAD_METHOD              critical
             1298  LOAD_DEREF               'self'
             1300  LOAD_ATTR                msgbox

 L. 552      1302  LOAD_STR                 'Train 2D-ASFE'

 L. 553      1304  LOAD_STR                 'Negative dropout rate'
             1306  CALL_METHOD_3         3  '3 positional arguments'
             1308  POP_TOP          

 L. 554      1310  LOAD_CONST               None
             1312  RETURN_VALUE     
           1314_0  COME_FROM          1274  '1274'

 L. 556      1314  LOAD_GLOBAL              len
             1316  LOAD_DEREF               'self'
             1318  LOAD_ATTR                ldtsave
             1320  LOAD_METHOD              text
             1322  CALL_METHOD_0         0  '0 positional arguments'
             1324  CALL_FUNCTION_1       1  '1 positional argument'
             1326  LOAD_CONST               1
             1328  COMPARE_OP               <
         1330_1332  POP_JUMP_IF_FALSE  1370  'to 1370'

 L. 557      1334  LOAD_GLOBAL              vis_msg
             1336  LOAD_ATTR                print
             1338  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: No name specified for ASFE network'
             1340  LOAD_STR                 'error'
             1342  LOAD_CONST               ('type',)
             1344  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1346  POP_TOP          

 L. 558      1348  LOAD_GLOBAL              QtWidgets
             1350  LOAD_ATTR                QMessageBox
             1352  LOAD_METHOD              critical
             1354  LOAD_DEREF               'self'
             1356  LOAD_ATTR                msgbox

 L. 559      1358  LOAD_STR                 'Train 2D-ASFE'

 L. 560      1360  LOAD_STR                 'No name specified for ASFE network'
             1362  CALL_METHOD_3         3  '3 positional arguments'
             1364  POP_TOP          

 L. 561      1366  LOAD_CONST               None
             1368  RETURN_VALUE     
           1370_0  COME_FROM          1330  '1330'

 L. 562      1370  LOAD_GLOBAL              os
             1372  LOAD_ATTR                path
             1374  LOAD_METHOD              dirname
             1376  LOAD_DEREF               'self'
             1378  LOAD_ATTR                ldtsave
             1380  LOAD_METHOD              text
             1382  CALL_METHOD_0         0  '0 positional arguments'
             1384  CALL_METHOD_1         1  '1 positional argument'
             1386  STORE_FAST               '_savepath'

 L. 563      1388  LOAD_GLOBAL              os
             1390  LOAD_ATTR                path
             1392  LOAD_METHOD              splitext
             1394  LOAD_GLOBAL              os
             1396  LOAD_ATTR                path
             1398  LOAD_METHOD              basename
             1400  LOAD_DEREF               'self'
             1402  LOAD_ATTR                ldtsave
             1404  LOAD_METHOD              text
             1406  CALL_METHOD_0         0  '0 positional arguments'
             1408  CALL_METHOD_1         1  '1 positional argument'
             1410  CALL_METHOD_1         1  '1 positional argument'
             1412  LOAD_CONST               0
             1414  BINARY_SUBSCR    
             1416  STORE_FAST               '_savename'

 L. 565      1418  LOAD_CONST               0
             1420  STORE_FAST               '_wdinl'

 L. 566      1422  LOAD_CONST               0
             1424  STORE_FAST               '_wdxl'

 L. 567      1426  LOAD_CONST               0
             1428  STORE_FAST               '_wdz'

 L. 568      1430  LOAD_DEREF               'self'
             1432  LOAD_ATTR                cbbornt
             1434  LOAD_METHOD              currentIndex
             1436  CALL_METHOD_0         0  '0 positional arguments'
             1438  LOAD_CONST               0
             1440  COMPARE_OP               ==
         1442_1444  POP_JUMP_IF_FALSE  1470  'to 1470'

 L. 569      1446  LOAD_GLOBAL              int
             1448  LOAD_FAST                '_image_width_old'
             1450  LOAD_CONST               2
             1452  BINARY_TRUE_DIVIDE
             1454  CALL_FUNCTION_1       1  '1 positional argument'
             1456  STORE_FAST               '_wdxl'

 L. 570      1458  LOAD_GLOBAL              int
             1460  LOAD_FAST                '_image_height_old'
             1462  LOAD_CONST               2
             1464  BINARY_TRUE_DIVIDE
             1466  CALL_FUNCTION_1       1  '1 positional argument'
             1468  STORE_FAST               '_wdz'
           1470_0  COME_FROM          1442  '1442'

 L. 571      1470  LOAD_DEREF               'self'
             1472  LOAD_ATTR                cbbornt
             1474  LOAD_METHOD              currentIndex
             1476  CALL_METHOD_0         0  '0 positional arguments'
             1478  LOAD_CONST               1
             1480  COMPARE_OP               ==
         1482_1484  POP_JUMP_IF_FALSE  1510  'to 1510'

 L. 572      1486  LOAD_GLOBAL              int
             1488  LOAD_FAST                '_image_width_old'
             1490  LOAD_CONST               2
             1492  BINARY_TRUE_DIVIDE
             1494  CALL_FUNCTION_1       1  '1 positional argument'
             1496  STORE_FAST               '_wdinl'

 L. 573      1498  LOAD_GLOBAL              int
             1500  LOAD_FAST                '_image_height_old'
             1502  LOAD_CONST               2
             1504  BINARY_TRUE_DIVIDE
             1506  CALL_FUNCTION_1       1  '1 positional argument'
             1508  STORE_FAST               '_wdz'
           1510_0  COME_FROM          1482  '1482'

 L. 574      1510  LOAD_DEREF               'self'
             1512  LOAD_ATTR                cbbornt
             1514  LOAD_METHOD              currentIndex
             1516  CALL_METHOD_0         0  '0 positional arguments'
             1518  LOAD_CONST               2
             1520  COMPARE_OP               ==
         1522_1524  POP_JUMP_IF_FALSE  1550  'to 1550'

 L. 575      1526  LOAD_GLOBAL              int
             1528  LOAD_FAST                '_image_width_old'
             1530  LOAD_CONST               2
             1532  BINARY_TRUE_DIVIDE
             1534  CALL_FUNCTION_1       1  '1 positional argument'
             1536  STORE_FAST               '_wdinl'

 L. 576      1538  LOAD_GLOBAL              int
             1540  LOAD_FAST                '_image_height_old'
             1542  LOAD_CONST               2
             1544  BINARY_TRUE_DIVIDE
             1546  CALL_FUNCTION_1       1  '1 positional argument'
             1548  STORE_FAST               '_wdxl'
           1550_0  COME_FROM          1522  '1522'

 L. 578      1550  LOAD_DEREF               'self'
             1552  LOAD_ATTR                survinfo
             1554  STORE_FAST               '_seisinfo'

 L. 580      1556  LOAD_GLOBAL              print
             1558  LOAD_STR                 'TrainMl2DAsfeFromScratch: Step 1 - Get training samples:'
             1560  CALL_FUNCTION_1       1  '1 positional argument'
             1562  POP_TOP          

 L. 581      1564  LOAD_DEREF               'self'
             1566  LOAD_ATTR                traindataconfig
             1568  LOAD_STR                 'TrainPointSet'
             1570  BINARY_SUBSCR    
             1572  STORE_FAST               '_trainpoint'

 L. 582      1574  LOAD_GLOBAL              np
             1576  LOAD_METHOD              zeros
             1578  LOAD_CONST               0
             1580  LOAD_CONST               3
             1582  BUILD_LIST_2          2 
             1584  CALL_METHOD_1         1  '1 positional argument'
             1586  STORE_FAST               '_traindata'

 L. 583      1588  SETUP_LOOP         1664  'to 1664'
             1590  LOAD_FAST                '_trainpoint'
             1592  GET_ITER         
           1594_0  COME_FROM          1612  '1612'
             1594  FOR_ITER           1662  'to 1662'
             1596  STORE_FAST               '_p'

 L. 584      1598  LOAD_GLOBAL              point_ays
             1600  LOAD_METHOD              checkPoint
             1602  LOAD_DEREF               'self'
             1604  LOAD_ATTR                pointsetdata
             1606  LOAD_FAST                '_p'
             1608  BINARY_SUBSCR    
             1610  CALL_METHOD_1         1  '1 positional argument'
         1612_1614  POP_JUMP_IF_FALSE  1594  'to 1594'

 L. 585      1616  LOAD_GLOBAL              basic_mdt
             1618  LOAD_METHOD              exportMatDict
             1620  LOAD_DEREF               'self'
             1622  LOAD_ATTR                pointsetdata
             1624  LOAD_FAST                '_p'
             1626  BINARY_SUBSCR    
             1628  LOAD_STR                 'Inline'
             1630  LOAD_STR                 'Crossline'
             1632  LOAD_STR                 'Z'
             1634  BUILD_LIST_3          3 
             1636  CALL_METHOD_2         2  '2 positional arguments'
             1638  STORE_FAST               '_pt'

 L. 586      1640  LOAD_GLOBAL              np
             1642  LOAD_ATTR                concatenate
             1644  LOAD_FAST                '_traindata'
             1646  LOAD_FAST                '_pt'
             1648  BUILD_TUPLE_2         2 
             1650  LOAD_CONST               0
             1652  LOAD_CONST               ('axis',)
             1654  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1656  STORE_FAST               '_traindata'
         1658_1660  JUMP_BACK          1594  'to 1594'
             1662  POP_BLOCK        
           1664_0  COME_FROM_LOOP     1588  '1588'

 L. 587      1664  LOAD_GLOBAL              seis_ays
             1666  LOAD_ATTR                removeOutofSurveySample
             1668  LOAD_FAST                '_traindata'

 L. 588      1670  LOAD_FAST                '_seisinfo'
             1672  LOAD_STR                 'ILStart'
             1674  BINARY_SUBSCR    
             1676  LOAD_FAST                '_wdinl'
             1678  LOAD_FAST                '_seisinfo'
             1680  LOAD_STR                 'ILStep'
             1682  BINARY_SUBSCR    
             1684  BINARY_MULTIPLY  
             1686  BINARY_ADD       

 L. 589      1688  LOAD_FAST                '_seisinfo'
             1690  LOAD_STR                 'ILEnd'
             1692  BINARY_SUBSCR    
             1694  LOAD_FAST                '_wdinl'
             1696  LOAD_FAST                '_seisinfo'
             1698  LOAD_STR                 'ILStep'
             1700  BINARY_SUBSCR    
             1702  BINARY_MULTIPLY  
             1704  BINARY_SUBTRACT  

 L. 590      1706  LOAD_FAST                '_seisinfo'
             1708  LOAD_STR                 'XLStart'
             1710  BINARY_SUBSCR    
             1712  LOAD_FAST                '_wdxl'
             1714  LOAD_FAST                '_seisinfo'
             1716  LOAD_STR                 'XLStep'
             1718  BINARY_SUBSCR    
             1720  BINARY_MULTIPLY  
             1722  BINARY_ADD       

 L. 591      1724  LOAD_FAST                '_seisinfo'
             1726  LOAD_STR                 'XLEnd'
             1728  BINARY_SUBSCR    
             1730  LOAD_FAST                '_wdxl'
             1732  LOAD_FAST                '_seisinfo'
             1734  LOAD_STR                 'XLStep'
             1736  BINARY_SUBSCR    
             1738  BINARY_MULTIPLY  
             1740  BINARY_SUBTRACT  

 L. 592      1742  LOAD_FAST                '_seisinfo'
             1744  LOAD_STR                 'ZStart'
             1746  BINARY_SUBSCR    
             1748  LOAD_FAST                '_wdz'
             1750  LOAD_FAST                '_seisinfo'
             1752  LOAD_STR                 'ZStep'
             1754  BINARY_SUBSCR    
             1756  BINARY_MULTIPLY  
             1758  BINARY_ADD       

 L. 593      1760  LOAD_FAST                '_seisinfo'
             1762  LOAD_STR                 'ZEnd'
             1764  BINARY_SUBSCR    
             1766  LOAD_FAST                '_wdz'
             1768  LOAD_FAST                '_seisinfo'
             1770  LOAD_STR                 'ZStep'
             1772  BINARY_SUBSCR    
             1774  BINARY_MULTIPLY  
             1776  BINARY_SUBTRACT  
             1778  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1780  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1782  STORE_FAST               '_traindata'

 L. 596      1784  LOAD_GLOBAL              np
             1786  LOAD_METHOD              shape
             1788  LOAD_FAST                '_traindata'
             1790  CALL_METHOD_1         1  '1 positional argument'
             1792  LOAD_CONST               0
             1794  BINARY_SUBSCR    
             1796  LOAD_CONST               0
             1798  COMPARE_OP               <=
         1800_1802  POP_JUMP_IF_FALSE  1840  'to 1840'

 L. 597      1804  LOAD_GLOBAL              vis_msg
             1806  LOAD_ATTR                print
             1808  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: No training sample found'
             1810  LOAD_STR                 'error'
             1812  LOAD_CONST               ('type',)
             1814  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1816  POP_TOP          

 L. 598      1818  LOAD_GLOBAL              QtWidgets
             1820  LOAD_ATTR                QMessageBox
             1822  LOAD_METHOD              critical
             1824  LOAD_DEREF               'self'
             1826  LOAD_ATTR                msgbox

 L. 599      1828  LOAD_STR                 'Train 2D-ASFE'

 L. 600      1830  LOAD_STR                 'No training sample found'
             1832  CALL_METHOD_3         3  '3 positional arguments'
             1834  POP_TOP          

 L. 601      1836  LOAD_CONST               None
             1838  RETURN_VALUE     
           1840_0  COME_FROM          1800  '1800'

 L. 604      1840  LOAD_GLOBAL              print
             1842  LOAD_STR                 'TrainMl2DAsfeFromScratch: Step 2 - Retrieve and interpolate images: (%d, %d) --> (%d, %d)'

 L. 605      1844  LOAD_FAST                '_image_height_old'
             1846  LOAD_FAST                '_image_width_old'
             1848  LOAD_FAST                '_image_height_new'
             1850  LOAD_FAST                '_image_width_new'
             1852  BUILD_TUPLE_4         4 
             1854  BINARY_MODULO    
             1856  CALL_FUNCTION_1       1  '1 positional argument'
             1858  POP_TOP          

 L. 606      1860  BUILD_MAP_0           0 
             1862  STORE_FAST               '_traindict'

 L. 607      1864  SETUP_LOOP         1936  'to 1936'
             1866  LOAD_FAST                '_features'
             1868  GET_ITER         
             1870  FOR_ITER           1934  'to 1934'
             1872  STORE_FAST               'f'

 L. 608      1874  LOAD_DEREF               'self'
             1876  LOAD_ATTR                seisdata
             1878  LOAD_FAST                'f'
             1880  BINARY_SUBSCR    
             1882  STORE_FAST               '_seisdata'

 L. 609      1884  LOAD_GLOBAL              seis_ays
             1886  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1888  LOAD_FAST                '_seisdata'
             1890  LOAD_FAST                '_traindata'
             1892  LOAD_DEREF               'self'
             1894  LOAD_ATTR                survinfo

 L. 610      1896  LOAD_FAST                '_wdinl'
             1898  LOAD_FAST                '_wdxl'
             1900  LOAD_FAST                '_wdz'

 L. 611      1902  LOAD_CONST               False
             1904  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1906  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1908  LOAD_CONST               None
             1910  LOAD_CONST               None
             1912  BUILD_SLICE_2         2 
             1914  LOAD_CONST               3
             1916  LOAD_CONST               None
             1918  BUILD_SLICE_2         2 
             1920  BUILD_TUPLE_2         2 
             1922  BINARY_SUBSCR    
             1924  LOAD_FAST                '_traindict'
             1926  LOAD_FAST                'f'
             1928  STORE_SUBSCR     
         1930_1932  JUMP_BACK          1870  'to 1870'
             1934  POP_BLOCK        
           1936_0  COME_FROM_LOOP     1864  '1864'

 L. 613      1936  LOAD_DEREF               'self'
             1938  LOAD_ATTR                traindataconfig
             1940  LOAD_STR                 'RemoveInvariantFeature_Checked'
             1942  BINARY_SUBSCR    
         1944_1946  POP_JUMP_IF_FALSE  2028  'to 2028'

 L. 614      1948  SETUP_LOOP         2028  'to 2028'
             1950  LOAD_FAST                '_features'
             1952  GET_ITER         
           1954_0  COME_FROM          1982  '1982'
             1954  FOR_ITER           2026  'to 2026'
             1956  STORE_FAST               'f'

 L. 615      1958  LOAD_GLOBAL              ml_aug
             1960  LOAD_METHOD              removeInvariantFeature
             1962  LOAD_FAST                '_traindict'
             1964  LOAD_FAST                'f'
             1966  CALL_METHOD_2         2  '2 positional arguments'
             1968  STORE_FAST               '_traindict'

 L. 616      1970  LOAD_GLOBAL              basic_mdt
             1972  LOAD_METHOD              maxDictConstantRow
             1974  LOAD_FAST                '_traindict'
             1976  CALL_METHOD_1         1  '1 positional argument'
             1978  LOAD_CONST               0
             1980  COMPARE_OP               <=
         1982_1984  POP_JUMP_IF_FALSE  1954  'to 1954'

 L. 617      1986  LOAD_GLOBAL              vis_msg
             1988  LOAD_ATTR                print
             1990  LOAD_STR                 'ERROR in TrainMl2DAsfeFromScratch: No training sample found'
             1992  LOAD_STR                 'error'
             1994  LOAD_CONST               ('type',)
             1996  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1998  POP_TOP          

 L. 618      2000  LOAD_GLOBAL              QtWidgets
             2002  LOAD_ATTR                QMessageBox
             2004  LOAD_METHOD              critical
             2006  LOAD_DEREF               'self'
             2008  LOAD_ATTR                msgbox

 L. 619      2010  LOAD_STR                 'Train 2D-ASFE'

 L. 620      2012  LOAD_STR                 'No training sample found'
             2014  CALL_METHOD_3         3  '3 positional arguments'
             2016  POP_TOP          

 L. 621      2018  LOAD_CONST               None
             2020  RETURN_VALUE     
         2022_2024  JUMP_BACK          1954  'to 1954'
             2026  POP_BLOCK        
           2028_0  COME_FROM_LOOP     1948  '1948'
           2028_1  COME_FROM          1944  '1944'

 L. 623      2028  LOAD_FAST                '_image_height_new'
             2030  LOAD_FAST                '_image_height_old'
             2032  COMPARE_OP               !=
         2034_2036  POP_JUMP_IF_TRUE   2048  'to 2048'
             2038  LOAD_FAST                '_image_width_new'
             2040  LOAD_FAST                '_image_width_old'
             2042  COMPARE_OP               !=
         2044_2046  POP_JUMP_IF_FALSE  2092  'to 2092'
           2048_0  COME_FROM          2034  '2034'

 L. 624      2048  SETUP_LOOP         2092  'to 2092'
             2050  LOAD_FAST                '_features'
             2052  GET_ITER         
             2054  FOR_ITER           2090  'to 2090'
             2056  STORE_FAST               'f'

 L. 625      2058  LOAD_GLOBAL              basic_image
             2060  LOAD_ATTR                changeImageSize
             2062  LOAD_FAST                '_traindict'
             2064  LOAD_FAST                'f'
             2066  BINARY_SUBSCR    

 L. 626      2068  LOAD_FAST                '_image_height_old'

 L. 627      2070  LOAD_FAST                '_image_width_old'

 L. 628      2072  LOAD_FAST                '_image_height_new'

 L. 629      2074  LOAD_FAST                '_image_width_new'
             2076  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2078  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2080  LOAD_FAST                '_traindict'
             2082  LOAD_FAST                'f'
             2084  STORE_SUBSCR     
         2086_2088  JUMP_BACK          2054  'to 2054'
             2090  POP_BLOCK        
           2092_0  COME_FROM_LOOP     2048  '2048'
           2092_1  COME_FROM          2044  '2044'

 L. 631      2092  SETUP_LOOP         2138  'to 2138'
             2094  LOAD_FAST                '_features'
             2096  GET_ITER         
             2098  FOR_ITER           2136  'to 2136'
             2100  STORE_FAST               'f'

 L. 633      2102  LOAD_DEREF               'self'
             2104  LOAD_METHOD              makeTarget
             2106  LOAD_FAST                '_traindict'
             2108  LOAD_FAST                'f'
             2110  BINARY_SUBSCR    
             2112  LOAD_FAST                '_image_height_new'
             2114  LOAD_FAST                '_image_width_new'
             2116  CALL_METHOD_3         3  '3 positional arguments'
             2118  UNPACK_SEQUENCE_2     2 
             2120  LOAD_FAST                '_traindict'
             2122  LOAD_FAST                'f'
             2124  STORE_SUBSCR     
             2126  LOAD_FAST                '_traindict'
             2128  LOAD_FAST                '_target'
             2130  STORE_SUBSCR     
         2132_2134  JUMP_BACK          2098  'to 2098'
             2136  POP_BLOCK        
           2138_0  COME_FROM_LOOP     2092  '2092'

 L. 636      2138  LOAD_GLOBAL              print
             2140  LOAD_STR                 'TrainMl2DAsfeFromScratch: A total of %d valid training samples'
             2142  LOAD_GLOBAL              basic_mdt
             2144  LOAD_METHOD              maxDictConstantRow

 L. 637      2146  LOAD_FAST                '_traindict'
             2148  CALL_METHOD_1         1  '1 positional argument'
             2150  BINARY_MODULO    
             2152  CALL_FUNCTION_1       1  '1 positional argument'
             2154  POP_TOP          

 L. 639      2156  LOAD_GLOBAL              print
             2158  LOAD_STR                 'TrainMl2DAsfeFromScratch: Step 3 - Start training'
             2160  CALL_FUNCTION_1       1  '1 positional argument'
             2162  POP_TOP          

 L. 641      2164  LOAD_GLOBAL              QtWidgets
             2166  LOAD_METHOD              QProgressDialog
             2168  CALL_METHOD_0         0  '0 positional arguments'
             2170  STORE_FAST               '_pgsdlg'

 L. 642      2172  LOAD_GLOBAL              QtGui
             2174  LOAD_METHOD              QIcon
             2176  CALL_METHOD_0         0  '0 positional arguments'
             2178  STORE_FAST               'icon'

 L. 643      2180  LOAD_FAST                'icon'
             2182  LOAD_METHOD              addPixmap
             2184  LOAD_GLOBAL              QtGui
             2186  LOAD_METHOD              QPixmap
             2188  LOAD_GLOBAL              os
             2190  LOAD_ATTR                path
             2192  LOAD_METHOD              join
             2194  LOAD_DEREF               'self'
             2196  LOAD_ATTR                iconpath
             2198  LOAD_STR                 'icons/new.png'
             2200  CALL_METHOD_2         2  '2 positional arguments'
             2202  CALL_METHOD_1         1  '1 positional argument'

 L. 644      2204  LOAD_GLOBAL              QtGui
             2206  LOAD_ATTR                QIcon
             2208  LOAD_ATTR                Normal
             2210  LOAD_GLOBAL              QtGui
             2212  LOAD_ATTR                QIcon
             2214  LOAD_ATTR                Off
             2216  CALL_METHOD_3         3  '3 positional arguments'
             2218  POP_TOP          

 L. 645      2220  LOAD_FAST                '_pgsdlg'
             2222  LOAD_METHOD              setWindowIcon
             2224  LOAD_FAST                'icon'
             2226  CALL_METHOD_1         1  '1 positional argument'
             2228  POP_TOP          

 L. 646      2230  LOAD_FAST                '_pgsdlg'
             2232  LOAD_METHOD              setWindowTitle
             2234  LOAD_STR                 'Train 2D-ASFE'
             2236  CALL_METHOD_1         1  '1 positional argument'
             2238  POP_TOP          

 L. 647      2240  LOAD_FAST                '_pgsdlg'
             2242  LOAD_METHOD              setCancelButton
             2244  LOAD_CONST               None
             2246  CALL_METHOD_1         1  '1 positional argument'
             2248  POP_TOP          

 L. 648      2250  LOAD_FAST                '_pgsdlg'
             2252  LOAD_METHOD              setWindowFlags
             2254  LOAD_GLOBAL              QtCore
             2256  LOAD_ATTR                Qt
             2258  LOAD_ATTR                WindowStaysOnTopHint
             2260  CALL_METHOD_1         1  '1 positional argument'
             2262  POP_TOP          

 L. 649      2264  LOAD_FAST                '_pgsdlg'
             2266  LOAD_METHOD              forceShow
             2268  CALL_METHOD_0         0  '0 positional arguments'
             2270  POP_TOP          

 L. 650      2272  LOAD_FAST                '_pgsdlg'
             2274  LOAD_METHOD              setFixedWidth
             2276  LOAD_CONST               400
             2278  CALL_METHOD_1         1  '1 positional argument'
             2280  POP_TOP          

 L. 651      2282  LOAD_GLOBAL              ml_cnn
             2284  LOAD_ATTR                createCNNClassifier
             2286  LOAD_FAST                '_traindict'

 L. 652      2288  LOAD_FAST                '_image_height_new'
             2290  LOAD_FAST                '_image_width_new'

 L. 653      2292  LOAD_FAST                '_features'
             2294  LOAD_FAST                '_target'

 L. 654      2296  LOAD_FAST                '_nepoch'
             2298  LOAD_FAST                '_batchsize'

 L. 655      2300  LOAD_FAST                '_nconvblock'

 L. 656      2302  LOAD_FAST                '_nconvlayer'
             2304  LOAD_FAST                '_nconvfeature'

 L. 657      2306  LOAD_FAST                '_nfclayer'
             2308  LOAD_FAST                '_nfcneuron'

 L. 658      2310  LOAD_FAST                '_patch_height'
             2312  LOAD_FAST                '_patch_width'

 L. 659      2314  LOAD_FAST                '_pool_height'
             2316  LOAD_FAST                '_pool_width'

 L. 660      2318  LOAD_FAST                '_learning_rate'

 L. 661      2320  LOAD_FAST                '_dropout_prob_fclayer'

 L. 662      2322  LOAD_CONST               True

 L. 663      2324  LOAD_FAST                '_savepath'
             2326  LOAD_FAST                '_savename'

 L. 664      2328  LOAD_FAST                '_pgsdlg'
             2330  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'nepoch', 'batchsize', 'nconvblock', 'nconvlayer', 'nconvfeature', 'nfclayer', 'nfcneuron', 'patchheight', 'patchwidth', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprobfclayer', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2332  CALL_FUNCTION_KW_22    22  '22 total positional and keyword args'
             2334  STORE_FAST               '_cnnlog'

 L. 666      2336  LOAD_GLOBAL              QtWidgets
             2338  LOAD_ATTR                QMessageBox
             2340  LOAD_METHOD              information
             2342  LOAD_DEREF               'self'
             2344  LOAD_ATTR                msgbox

 L. 667      2346  LOAD_STR                 'Train 2D-ASFE'

 L. 668      2348  LOAD_STR                 'ASFE trained successfully'
             2350  CALL_METHOD_3         3  '3 positional arguments'
             2352  POP_TOP          

 L. 670      2354  LOAD_GLOBAL              QtWidgets
             2356  LOAD_ATTR                QMessageBox
             2358  LOAD_METHOD              question
             2360  LOAD_DEREF               'self'
             2362  LOAD_ATTR                msgbox
             2364  LOAD_STR                 'Train 2D-ASFE'
             2366  LOAD_STR                 'View learning matrix?'

 L. 671      2368  LOAD_GLOBAL              QtWidgets
             2370  LOAD_ATTR                QMessageBox
             2372  LOAD_ATTR                Yes
             2374  LOAD_GLOBAL              QtWidgets
             2376  LOAD_ATTR                QMessageBox
             2378  LOAD_ATTR                No
             2380  BINARY_OR        

 L. 672      2382  LOAD_GLOBAL              QtWidgets
             2384  LOAD_ATTR                QMessageBox
             2386  LOAD_ATTR                Yes
             2388  CALL_METHOD_5         5  '5 positional arguments'
             2390  STORE_FAST               'reply'

 L. 674      2392  LOAD_FAST                'reply'
             2394  LOAD_GLOBAL              QtWidgets
             2396  LOAD_ATTR                QMessageBox
             2398  LOAD_ATTR                Yes
             2400  COMPARE_OP               ==
         2402_2404  POP_JUMP_IF_FALSE  2472  'to 2472'

 L. 675      2406  LOAD_GLOBAL              QtWidgets
             2408  LOAD_METHOD              QDialog
             2410  CALL_METHOD_0         0  '0 positional arguments'
             2412  STORE_FAST               '_viewmllearnmat'

 L. 676      2414  LOAD_GLOBAL              gui_viewmllearnmat
             2416  CALL_FUNCTION_0       0  '0 positional arguments'
             2418  STORE_FAST               '_gui'

 L. 677      2420  LOAD_FAST                '_cnnlog'
             2422  LOAD_STR                 'learning_curve'
             2424  BINARY_SUBSCR    
             2426  LOAD_FAST                '_gui'
             2428  STORE_ATTR               learnmat

 L. 678      2430  LOAD_DEREF               'self'
             2432  LOAD_ATTR                linestyle
             2434  LOAD_FAST                '_gui'
             2436  STORE_ATTR               linestyle

 L. 679      2438  LOAD_DEREF               'self'
             2440  LOAD_ATTR                fontstyle
             2442  LOAD_FAST                '_gui'
             2444  STORE_ATTR               fontstyle

 L. 680      2446  LOAD_FAST                '_gui'
             2448  LOAD_METHOD              setupGUI
             2450  LOAD_FAST                '_viewmllearnmat'
             2452  CALL_METHOD_1         1  '1 positional argument'
             2454  POP_TOP          

 L. 681      2456  LOAD_FAST                '_viewmllearnmat'
             2458  LOAD_METHOD              exec
             2460  CALL_METHOD_0         0  '0 positional arguments'
             2462  POP_TOP          

 L. 682      2464  LOAD_FAST                '_viewmllearnmat'
             2466  LOAD_METHOD              show
             2468  CALL_METHOD_0         0  '0 positional arguments'
             2470  POP_TOP          
           2472_0  COME_FROM          2402  '2402'

Parse error at or near `POP_TOP' instruction at offset 2470

    def makeTarget(self, imagedata, imageheight, imagewidth):
        nimage = np.shape(imagedata)[0]
        labelrotated = np.zeros([4 * nimage, 1])
        if imageheight == imagewidth:
            labelrotated = np.zeros([6 * nimage, 1])
        imagerotated = imagedata
        imagerotated_180 = basic_image.rotateImage(imagedata, image_height=imageheight, image_width=imagewidth, flag='180')
        imagerotated = np.concatenate((imagerotated, imagerotated_180), axis=0)
        labelrotated[nimage:2 * nimage, :] = 1
        imagerotated_lr = basic_image.rotateImage(imagedata, image_height=imageheight, image_width=imagewidth, flag='lr')
        imagerotated = np.concatenate((imagerotated, imagerotated_lr), axis=0)
        labelrotated[2 * nimage:3 * nimage, :] = 2
        imagerotated_ud = basic_image.rotateImage(imagedata, image_height=imageheight, image_width=imagewidth, flag='ud')
        imagerotated = np.concatenate((imagerotated, imagerotated_ud), axis=0)
        labelrotated[3 * nimage:4 * nimage, :] = 3
        if imageheight == imagewidth:
            imagerotated_90 = basic_image.rotateImage(imagedata, image_height=imageheight, image_width=imagewidth, flag='90')
            imagerotated = np.concatenate((imagerotated, imagerotated_90), axis=0)
            labelrotated[4 * nimage:5 * nimage, :] = 4
            imagerotated_270 = basic_image.rotateImage(imagedata, image_height=imageheight, image_width=imagewidth, flag='270')
            imagerotated = np.concatenate((imagerotated, imagerotated_270), axis=0)
            labelrotated[5 * nimage:6 * nimage, :] = 5
        return (imagerotated, labelrotated)

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
    TrainMl2DAsfeFromScratch = QtWidgets.QWidget()
    gui = trainml2dasfefromscratch()
    gui.setupGUI(TrainMl2DAsfeFromScratch)
    TrainMl2DAsfeFromScratch.show()
    sys.exit(app.exec_())