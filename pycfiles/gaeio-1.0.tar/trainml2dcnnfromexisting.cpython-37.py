# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml2dcnnfromexisting.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 54015 bytes
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
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.cnnclassifier as ml_cnn
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
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

    def clickBtnTrainMl2DCnnFromExisting--- This code section failed: ---

 L. 595         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 597         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 598        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 599        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 600        50  LOAD_STR                 'Train 2D-CNN'

 L. 601        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 602        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 604        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_image_height_old'

 L. 605        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_image_width_old'

 L. 606        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtnewheight
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_image_height_new'

 L. 607       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewwidth
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_image_width_new'

 L. 608       126  LOAD_FAST                '_image_height_old'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'
              134  LOAD_FAST                '_image_width_old'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_TRUE    158  'to 158'

 L. 609       142  LOAD_FAST                '_image_height_new'
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

 L. 610       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 611       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 612       182  LOAD_STR                 'Train 2D-CNN'

 L. 613       184  LOAD_STR                 'Non-integer feature size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 614       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 615       194  LOAD_FAST                '_image_height_old'
              196  LOAD_CONST               2
              198  COMPARE_OP               <
              200  POP_JUMP_IF_TRUE    228  'to 228'
              202  LOAD_FAST                '_image_width_old'
              204  LOAD_CONST               2
              206  COMPARE_OP               <
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 616       210  LOAD_FAST                '_image_height_new'
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

 L. 617       228  LOAD_GLOBAL              vis_msg
              230  LOAD_ATTR                print
              232  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 618       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 619       252  LOAD_STR                 'Train 2D-CNN'

 L. 620       254  LOAD_STR                 'Features are not 2D'
              256  CALL_METHOD_3         3  '3 positional arguments'
              258  POP_TOP          

 L. 621       260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           224  '224'

 L. 623       264  LOAD_CONST               2
              266  LOAD_GLOBAL              int
              268  LOAD_FAST                '_image_height_old'
              270  LOAD_CONST               2
              272  BINARY_TRUE_DIVIDE
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  BINARY_MULTIPLY  
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  STORE_FAST               '_image_height_old'

 L. 624       284  LOAD_CONST               2
              286  LOAD_GLOBAL              int
              288  LOAD_FAST                '_image_width_old'
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BINARY_MULTIPLY  
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               '_image_width_old'

 L. 626       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                lwgfeature
              308  LOAD_METHOD              selectedItems
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               '_features'

 L. 627       314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainml2dcnnfromexisting.clickBtnTrainMl2DCnnFromExisting.<locals>.<listcomp>'
              318  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              320  LOAD_FAST                '_features'
              322  GET_ITER         
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               '_features'

 L. 628       328  LOAD_DEREF               'self'
              330  LOAD_ATTR                featurelist
              332  LOAD_DEREF               'self'
              334  LOAD_ATTR                cbbtarget
              336  LOAD_METHOD              currentIndex
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  BINARY_SUBSCR    
              342  STORE_FAST               '_target'

 L. 630       344  LOAD_FAST                '_target'
              346  LOAD_FAST                '_features'
              348  COMPARE_OP               in
          350_352  POP_JUMP_IF_FALSE   390  'to 390'

 L. 631       354  LOAD_GLOBAL              vis_msg
              356  LOAD_ATTR                print
              358  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Target also used as features'
              360  LOAD_STR                 'error'
              362  LOAD_CONST               ('type',)
              364  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              366  POP_TOP          

 L. 632       368  LOAD_GLOBAL              QtWidgets
              370  LOAD_ATTR                QMessageBox
              372  LOAD_METHOD              critical
              374  LOAD_DEREF               'self'
              376  LOAD_ATTR                msgbox

 L. 633       378  LOAD_STR                 'Train 2D-CNN'

 L. 634       380  LOAD_STR                 'Target also used as features'
              382  CALL_METHOD_3         3  '3 positional arguments'
              384  POP_TOP          

 L. 635       386  LOAD_CONST               None
              388  RETURN_VALUE     
            390_0  COME_FROM           350  '350'

 L. 637       390  LOAD_GLOBAL              len
              392  LOAD_DEREF               'self'
              394  LOAD_ATTR                ldtexisting
              396  LOAD_METHOD              text
              398  CALL_METHOD_0         0  '0 positional arguments'
              400  CALL_FUNCTION_1       1  '1 positional argument'
              402  LOAD_CONST               1
              404  COMPARE_OP               <
          406_408  POP_JUMP_IF_FALSE   446  'to 446'

 L. 638       410  LOAD_GLOBAL              vis_msg
              412  LOAD_ATTR                print
              414  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: No name specified for pre-trained network'

 L. 639       416  LOAD_STR                 'error'
              418  LOAD_CONST               ('type',)
              420  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              422  POP_TOP          

 L. 640       424  LOAD_GLOBAL              QtWidgets
              426  LOAD_ATTR                QMessageBox
              428  LOAD_METHOD              critical
              430  LOAD_DEREF               'self'
              432  LOAD_ATTR                msgbox

 L. 641       434  LOAD_STR                 'Train 2D-CNN'

 L. 642       436  LOAD_STR                 'No name specified for pre-trained network'
              438  CALL_METHOD_3         3  '3 positional arguments'
              440  POP_TOP          

 L. 643       442  LOAD_CONST               None
              444  RETURN_VALUE     
            446_0  COME_FROM           406  '406'

 L. 644       446  LOAD_GLOBAL              os
              448  LOAD_ATTR                path
              450  LOAD_METHOD              dirname
              452  LOAD_DEREF               'self'
              454  LOAD_ATTR                ldtexisting
              456  LOAD_METHOD              text
              458  CALL_METHOD_0         0  '0 positional arguments'
              460  CALL_METHOD_1         1  '1 positional argument'
              462  STORE_FAST               '_precnnpath'

 L. 645       464  LOAD_GLOBAL              os
              466  LOAD_ATTR                path
              468  LOAD_METHOD              splitext
              470  LOAD_GLOBAL              os
              472  LOAD_ATTR                path
              474  LOAD_METHOD              basename
              476  LOAD_DEREF               'self'
              478  LOAD_ATTR                ldtexisting
              480  LOAD_METHOD              text
              482  CALL_METHOD_0         0  '0 positional arguments'
              484  CALL_METHOD_1         1  '1 positional argument'
              486  CALL_METHOD_1         1  '1 positional argument'
              488  LOAD_CONST               0
              490  BINARY_SUBSCR    
              492  STORE_FAST               '_precnnname'

 L. 646       494  LOAD_DEREF               'self'
              496  LOAD_ATTR                cbbblockid
              498  LOAD_METHOD              currentIndex
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  STORE_FAST               '_blockidx'

 L. 647       504  LOAD_DEREF               'self'
              506  LOAD_ATTR                cbblayerid
              508  LOAD_METHOD              currentIndex
              510  CALL_METHOD_0         0  '0 positional arguments'
              512  STORE_FAST               '_layeridx'

 L. 648       514  LOAD_CONST               True
              516  STORE_FAST               '_trainable'

 L. 649       518  LOAD_DEREF               'self'
              520  LOAD_ATTR                cbbtrainable
              522  LOAD_METHOD              currentIndex
              524  CALL_METHOD_0         0  '0 positional arguments'
              526  LOAD_CONST               0
              528  COMPARE_OP               !=
          530_532  POP_JUMP_IF_FALSE   538  'to 538'

 L. 650       534  LOAD_CONST               False
              536  STORE_FAST               '_trainable'
            538_0  COME_FROM           530  '530'

 L. 652       538  LOAD_GLOBAL              ml_tfm
              540  LOAD_METHOD              getConvModelNChannel
              542  LOAD_FAST                '_precnnpath'
              544  LOAD_FAST                '_precnnname'
              546  CALL_METHOD_2         2  '2 positional arguments'
              548  LOAD_GLOBAL              len
              550  LOAD_FAST                '_features'
              552  CALL_FUNCTION_1       1  '1 positional argument'
              554  COMPARE_OP               !=
          556_558  POP_JUMP_IF_FALSE   596  'to 596'

 L. 653       560  LOAD_GLOBAL              vis_msg
              562  LOAD_ATTR                print
              564  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Feature channel number not match with pre-trained network'

 L. 654       566  LOAD_STR                 'error'
              568  LOAD_CONST               ('type',)
              570  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              572  POP_TOP          

 L. 655       574  LOAD_GLOBAL              QtWidgets
              576  LOAD_ATTR                QMessageBox
              578  LOAD_METHOD              critical
              580  LOAD_DEREF               'self'
              582  LOAD_ATTR                msgbox

 L. 656       584  LOAD_STR                 'Train 2D-CNN'

 L. 657       586  LOAD_STR                 'Feature channel number not match with pre-trained network'
              588  CALL_METHOD_3         3  '3 positional arguments'
              590  POP_TOP          

 L. 658       592  LOAD_CONST               None
              594  RETURN_VALUE     
            596_0  COME_FROM           556  '556'

 L. 660       596  LOAD_GLOBAL              basic_data
              598  LOAD_METHOD              str2int
              600  LOAD_DEREF               'self'
              602  LOAD_ATTR                ldtnconvblock
              604  LOAD_METHOD              text
              606  CALL_METHOD_0         0  '0 positional arguments'
              608  CALL_METHOD_1         1  '1 positional argument'
              610  STORE_FAST               '_nconvblock'

 L. 661       612  LOAD_CLOSURE             'self'
              614  BUILD_TUPLE_1         1 
              616  LOAD_LISTCOMP            '<code_object <listcomp>>'
              618  LOAD_STR                 'trainml2dcnnfromexisting.clickBtnTrainMl2DCnnFromExisting.<locals>.<listcomp>'
              620  MAKE_FUNCTION_8          'closure'
              622  LOAD_GLOBAL              range
              624  LOAD_FAST                '_nconvblock'
              626  CALL_FUNCTION_1       1  '1 positional argument'
              628  GET_ITER         
              630  CALL_FUNCTION_1       1  '1 positional argument'
              632  STORE_FAST               '_nconvlayer'

 L. 662       634  LOAD_CLOSURE             'self'
              636  BUILD_TUPLE_1         1 
              638  LOAD_LISTCOMP            '<code_object <listcomp>>'
              640  LOAD_STR                 'trainml2dcnnfromexisting.clickBtnTrainMl2DCnnFromExisting.<locals>.<listcomp>'
              642  MAKE_FUNCTION_8          'closure'
              644  LOAD_GLOBAL              range
              646  LOAD_FAST                '_nconvblock'
              648  CALL_FUNCTION_1       1  '1 positional argument'
              650  GET_ITER         
              652  CALL_FUNCTION_1       1  '1 positional argument'
              654  STORE_FAST               '_nconvfeature'

 L. 663       656  LOAD_GLOBAL              basic_data
              658  LOAD_METHOD              str2int
              660  LOAD_DEREF               'self'
              662  LOAD_ATTR                ldtnfclayer
              664  LOAD_METHOD              text
              666  CALL_METHOD_0         0  '0 positional arguments'
              668  CALL_METHOD_1         1  '1 positional argument'
              670  STORE_FAST               '_nfclayer'

 L. 664       672  LOAD_CLOSURE             'self'
              674  BUILD_TUPLE_1         1 
              676  LOAD_LISTCOMP            '<code_object <listcomp>>'
              678  LOAD_STR                 'trainml2dcnnfromexisting.clickBtnTrainMl2DCnnFromExisting.<locals>.<listcomp>'
              680  MAKE_FUNCTION_8          'closure'
              682  LOAD_GLOBAL              range
              684  LOAD_FAST                '_nfclayer'
              686  CALL_FUNCTION_1       1  '1 positional argument'
              688  GET_ITER         
              690  CALL_FUNCTION_1       1  '1 positional argument'
              692  STORE_FAST               '_nfcneuron'

 L. 665       694  LOAD_GLOBAL              basic_data
              696  LOAD_METHOD              str2int
              698  LOAD_DEREF               'self'
              700  LOAD_ATTR                ldtmaskheight
              702  LOAD_METHOD              text
              704  CALL_METHOD_0         0  '0 positional arguments'
              706  CALL_METHOD_1         1  '1 positional argument'
              708  STORE_FAST               '_patch_height'

 L. 666       710  LOAD_GLOBAL              basic_data
              712  LOAD_METHOD              str2int
              714  LOAD_DEREF               'self'
              716  LOAD_ATTR                ldtmaskwidth
              718  LOAD_METHOD              text
              720  CALL_METHOD_0         0  '0 positional arguments'
              722  CALL_METHOD_1         1  '1 positional argument'
              724  STORE_FAST               '_patch_width'

 L. 667       726  LOAD_GLOBAL              basic_data
              728  LOAD_METHOD              str2int
              730  LOAD_DEREF               'self'
              732  LOAD_ATTR                ldtpoolheight
              734  LOAD_METHOD              text
              736  CALL_METHOD_0         0  '0 positional arguments'
              738  CALL_METHOD_1         1  '1 positional argument'
              740  STORE_FAST               '_pool_height'

 L. 668       742  LOAD_GLOBAL              basic_data
              744  LOAD_METHOD              str2int
              746  LOAD_DEREF               'self'
              748  LOAD_ATTR                ldtpoolwidth
              750  LOAD_METHOD              text
              752  CALL_METHOD_0         0  '0 positional arguments'
              754  CALL_METHOD_1         1  '1 positional argument'
              756  STORE_FAST               '_pool_width'

 L. 669       758  LOAD_GLOBAL              basic_data
              760  LOAD_METHOD              str2int
              762  LOAD_DEREF               'self'
              764  LOAD_ATTR                ldtnepoch
              766  LOAD_METHOD              text
              768  CALL_METHOD_0         0  '0 positional arguments'
              770  CALL_METHOD_1         1  '1 positional argument'
              772  STORE_FAST               '_nepoch'

 L. 670       774  LOAD_GLOBAL              basic_data
              776  LOAD_METHOD              str2int
              778  LOAD_DEREF               'self'
              780  LOAD_ATTR                ldtbatchsize
              782  LOAD_METHOD              text
              784  CALL_METHOD_0         0  '0 positional arguments'
              786  CALL_METHOD_1         1  '1 positional argument'
              788  STORE_FAST               '_batchsize'

 L. 671       790  LOAD_GLOBAL              basic_data
              792  LOAD_METHOD              str2float
              794  LOAD_DEREF               'self'
              796  LOAD_ATTR                ldtlearnrate
              798  LOAD_METHOD              text
              800  CALL_METHOD_0         0  '0 positional arguments'
              802  CALL_METHOD_1         1  '1 positional argument'
              804  STORE_FAST               '_learning_rate'

 L. 672       806  LOAD_GLOBAL              basic_data
              808  LOAD_METHOD              str2float
              810  LOAD_DEREF               'self'
              812  LOAD_ATTR                ldtfcdropout
              814  LOAD_METHOD              text
              816  CALL_METHOD_0         0  '0 positional arguments'
              818  CALL_METHOD_1         1  '1 positional argument'
              820  STORE_FAST               '_dropout_prob_fclayer'

 L. 673       822  LOAD_FAST                '_nconvblock'
              824  LOAD_CONST               False
              826  COMPARE_OP               is
          828_830  POP_JUMP_IF_TRUE    842  'to 842'
              832  LOAD_FAST                '_nconvblock'
              834  LOAD_CONST               0
              836  COMPARE_OP               <=
          838_840  POP_JUMP_IF_FALSE   878  'to 878'
            842_0  COME_FROM           828  '828'

 L. 674       842  LOAD_GLOBAL              vis_msg
              844  LOAD_ATTR                print
              846  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Non-positive convolutional block number'

 L. 675       848  LOAD_STR                 'error'
              850  LOAD_CONST               ('type',)
              852  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              854  POP_TOP          

 L. 676       856  LOAD_GLOBAL              QtWidgets
              858  LOAD_ATTR                QMessageBox
              860  LOAD_METHOD              critical
              862  LOAD_DEREF               'self'
              864  LOAD_ATTR                msgbox

 L. 677       866  LOAD_STR                 'Train 2D-CNN'

 L. 678       868  LOAD_STR                 'Non-positive convolutional block number'
              870  CALL_METHOD_3         3  '3 positional arguments'
              872  POP_TOP          

 L. 679       874  LOAD_CONST               None
              876  RETURN_VALUE     
            878_0  COME_FROM           838  '838'

 L. 680       878  SETUP_LOOP          950  'to 950'
              880  LOAD_FAST                '_nconvlayer'
              882  GET_ITER         
            884_0  COME_FROM           904  '904'
              884  FOR_ITER            948  'to 948'
              886  STORE_FAST               '_i'

 L. 681       888  LOAD_FAST                '_i'
              890  LOAD_CONST               False
              892  COMPARE_OP               is
          894_896  POP_JUMP_IF_TRUE    908  'to 908'
              898  LOAD_FAST                '_i'
              900  LOAD_CONST               1
              902  COMPARE_OP               <
          904_906  POP_JUMP_IF_FALSE   884  'to 884'
            908_0  COME_FROM           894  '894'

 L. 682       908  LOAD_GLOBAL              vis_msg
              910  LOAD_ATTR                print
              912  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Non-positive convolutional layer number'

 L. 683       914  LOAD_STR                 'error'
              916  LOAD_CONST               ('type',)
              918  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              920  POP_TOP          

 L. 684       922  LOAD_GLOBAL              QtWidgets
              924  LOAD_ATTR                QMessageBox
              926  LOAD_METHOD              critical
              928  LOAD_DEREF               'self'
              930  LOAD_ATTR                msgbox

 L. 685       932  LOAD_STR                 'Train 2D-CNN'

 L. 686       934  LOAD_STR                 'Non-positive convolutional layer number'
              936  CALL_METHOD_3         3  '3 positional arguments'
              938  POP_TOP          

 L. 687       940  LOAD_CONST               None
              942  RETURN_VALUE     
          944_946  JUMP_BACK           884  'to 884'
              948  POP_BLOCK        
            950_0  COME_FROM_LOOP      878  '878'

 L. 688       950  SETUP_LOOP         1022  'to 1022'
              952  LOAD_FAST                '_nconvfeature'
              954  GET_ITER         
            956_0  COME_FROM           976  '976'
              956  FOR_ITER           1020  'to 1020'
              958  STORE_FAST               '_i'

 L. 689       960  LOAD_FAST                '_i'
              962  LOAD_CONST               False
              964  COMPARE_OP               is
          966_968  POP_JUMP_IF_TRUE    980  'to 980'
              970  LOAD_FAST                '_i'
              972  LOAD_CONST               1
              974  COMPARE_OP               <
          976_978  POP_JUMP_IF_FALSE   956  'to 956'
            980_0  COME_FROM           966  '966'

 L. 690       980  LOAD_GLOBAL              vis_msg
              982  LOAD_ATTR                print
              984  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Non-positive convolutional feature number'

 L. 691       986  LOAD_STR                 'error'
              988  LOAD_CONST               ('type',)
              990  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              992  POP_TOP          

 L. 692       994  LOAD_GLOBAL              QtWidgets
              996  LOAD_ATTR                QMessageBox
              998  LOAD_METHOD              critical
             1000  LOAD_DEREF               'self'
             1002  LOAD_ATTR                msgbox

 L. 693      1004  LOAD_STR                 'Train 2D-CNN'

 L. 694      1006  LOAD_STR                 'Non-positive convolutional feature number'
             1008  CALL_METHOD_3         3  '3 positional arguments'
             1010  POP_TOP          

 L. 695      1012  LOAD_CONST               None
             1014  RETURN_VALUE     
         1016_1018  JUMP_BACK           956  'to 956'
             1020  POP_BLOCK        
           1022_0  COME_FROM_LOOP      950  '950'

 L. 696      1022  LOAD_FAST                '_nfclayer'
             1024  LOAD_CONST               False
             1026  COMPARE_OP               is
         1028_1030  POP_JUMP_IF_TRUE   1042  'to 1042'
             1032  LOAD_FAST                '_nfclayer'
             1034  LOAD_CONST               0
             1036  COMPARE_OP               <=
         1038_1040  POP_JUMP_IF_FALSE  1078  'to 1078'
           1042_0  COME_FROM          1028  '1028'

 L. 697      1042  LOAD_GLOBAL              vis_msg
             1044  LOAD_ATTR                print
             1046  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Non-positive MLP layer number'
             1048  LOAD_STR                 'error'
             1050  LOAD_CONST               ('type',)
             1052  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1054  POP_TOP          

 L. 698      1056  LOAD_GLOBAL              QtWidgets
             1058  LOAD_ATTR                QMessageBox
             1060  LOAD_METHOD              critical
             1062  LOAD_DEREF               'self'
             1064  LOAD_ATTR                msgbox

 L. 699      1066  LOAD_STR                 'Train 2D-CNN'

 L. 700      1068  LOAD_STR                 'Non-positive MLP layer number'
             1070  CALL_METHOD_3         3  '3 positional arguments'
             1072  POP_TOP          

 L. 701      1074  LOAD_CONST               None
             1076  RETURN_VALUE     
           1078_0  COME_FROM          1038  '1038'

 L. 702      1078  SETUP_LOOP         1150  'to 1150'
             1080  LOAD_FAST                '_nfcneuron'
             1082  GET_ITER         
           1084_0  COME_FROM          1104  '1104'
             1084  FOR_ITER           1148  'to 1148'
             1086  STORE_FAST               '_i'

 L. 703      1088  LOAD_FAST                '_i'
             1090  LOAD_CONST               False
             1092  COMPARE_OP               is
         1094_1096  POP_JUMP_IF_TRUE   1108  'to 1108'
             1098  LOAD_FAST                '_i'
             1100  LOAD_CONST               1
             1102  COMPARE_OP               <
         1104_1106  POP_JUMP_IF_FALSE  1084  'to 1084'
           1108_0  COME_FROM          1094  '1094'

 L. 704      1108  LOAD_GLOBAL              vis_msg
             1110  LOAD_ATTR                print
             1112  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Non-positive MLP neuron number'

 L. 705      1114  LOAD_STR                 'error'
             1116  LOAD_CONST               ('type',)
             1118  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1120  POP_TOP          

 L. 706      1122  LOAD_GLOBAL              QtWidgets
             1124  LOAD_ATTR                QMessageBox
             1126  LOAD_METHOD              critical
             1128  LOAD_DEREF               'self'
             1130  LOAD_ATTR                msgbox

 L. 707      1132  LOAD_STR                 'Train 2D-CNN'

 L. 708      1134  LOAD_STR                 'Non-positive MLP neuron number'
             1136  CALL_METHOD_3         3  '3 positional arguments'
             1138  POP_TOP          

 L. 709      1140  LOAD_CONST               None
             1142  RETURN_VALUE     
         1144_1146  JUMP_BACK          1084  'to 1084'
             1148  POP_BLOCK        
           1150_0  COME_FROM_LOOP     1078  '1078'

 L. 710      1150  LOAD_FAST                '_patch_height'
             1152  LOAD_CONST               False
             1154  COMPARE_OP               is
         1156_1158  POP_JUMP_IF_TRUE   1190  'to 1190'
             1160  LOAD_FAST                '_patch_width'
             1162  LOAD_CONST               False
             1164  COMPARE_OP               is
         1166_1168  POP_JUMP_IF_TRUE   1190  'to 1190'

 L. 711      1170  LOAD_FAST                '_patch_height'
             1172  LOAD_CONST               1
             1174  COMPARE_OP               <
         1176_1178  POP_JUMP_IF_TRUE   1190  'to 1190'
             1180  LOAD_FAST                '_patch_width'
             1182  LOAD_CONST               1
             1184  COMPARE_OP               <
         1186_1188  POP_JUMP_IF_FALSE  1226  'to 1226'
           1190_0  COME_FROM          1176  '1176'
           1190_1  COME_FROM          1166  '1166'
           1190_2  COME_FROM          1156  '1156'

 L. 712      1190  LOAD_GLOBAL              vis_msg
             1192  LOAD_ATTR                print
             1194  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Non-positive convolutional patch size'

 L. 713      1196  LOAD_STR                 'error'
             1198  LOAD_CONST               ('type',)
             1200  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1202  POP_TOP          

 L. 714      1204  LOAD_GLOBAL              QtWidgets
             1206  LOAD_ATTR                QMessageBox
             1208  LOAD_METHOD              critical
             1210  LOAD_DEREF               'self'
             1212  LOAD_ATTR                msgbox

 L. 715      1214  LOAD_STR                 'Train 2D-CNN'

 L. 716      1216  LOAD_STR                 'Non-positive convolutional patch size'
             1218  CALL_METHOD_3         3  '3 positional arguments'
             1220  POP_TOP          

 L. 717      1222  LOAD_CONST               None
             1224  RETURN_VALUE     
           1226_0  COME_FROM          1186  '1186'

 L. 718      1226  LOAD_FAST                '_pool_height'
             1228  LOAD_CONST               False
             1230  COMPARE_OP               is
         1232_1234  POP_JUMP_IF_TRUE   1266  'to 1266'
             1236  LOAD_FAST                '_pool_width'
             1238  LOAD_CONST               False
             1240  COMPARE_OP               is
         1242_1244  POP_JUMP_IF_TRUE   1266  'to 1266'

 L. 719      1246  LOAD_FAST                '_pool_height'
             1248  LOAD_CONST               1
             1250  COMPARE_OP               <
         1252_1254  POP_JUMP_IF_TRUE   1266  'to 1266'
             1256  LOAD_FAST                '_pool_width'
             1258  LOAD_CONST               1
             1260  COMPARE_OP               <
         1262_1264  POP_JUMP_IF_FALSE  1302  'to 1302'
           1266_0  COME_FROM          1252  '1252'
           1266_1  COME_FROM          1242  '1242'
           1266_2  COME_FROM          1232  '1232'

 L. 720      1266  LOAD_GLOBAL              vis_msg
             1268  LOAD_ATTR                print
             1270  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Non-positive pooling size'
             1272  LOAD_STR                 'error'
             1274  LOAD_CONST               ('type',)
             1276  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1278  POP_TOP          

 L. 721      1280  LOAD_GLOBAL              QtWidgets
             1282  LOAD_ATTR                QMessageBox
             1284  LOAD_METHOD              critical
             1286  LOAD_DEREF               'self'
             1288  LOAD_ATTR                msgbox

 L. 722      1290  LOAD_STR                 'Train 2D-CNN'

 L. 723      1292  LOAD_STR                 'Non-positive pooling size'
             1294  CALL_METHOD_3         3  '3 positional arguments'
             1296  POP_TOP          

 L. 724      1298  LOAD_CONST               None
             1300  RETURN_VALUE     
           1302_0  COME_FROM          1262  '1262'

 L. 725      1302  LOAD_FAST                '_nepoch'
             1304  LOAD_CONST               False
             1306  COMPARE_OP               is
         1308_1310  POP_JUMP_IF_TRUE   1322  'to 1322'
             1312  LOAD_FAST                '_nepoch'
             1314  LOAD_CONST               0
             1316  COMPARE_OP               <=
         1318_1320  POP_JUMP_IF_FALSE  1358  'to 1358'
           1322_0  COME_FROM          1308  '1308'

 L. 726      1322  LOAD_GLOBAL              vis_msg
             1324  LOAD_ATTR                print
             1326  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Non-positive epoch number'
             1328  LOAD_STR                 'error'
             1330  LOAD_CONST               ('type',)
             1332  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1334  POP_TOP          

 L. 727      1336  LOAD_GLOBAL              QtWidgets
             1338  LOAD_ATTR                QMessageBox
             1340  LOAD_METHOD              critical
             1342  LOAD_DEREF               'self'
             1344  LOAD_ATTR                msgbox

 L. 728      1346  LOAD_STR                 'Train 2D-CNN'

 L. 729      1348  LOAD_STR                 'Non-positive epoch number'
             1350  CALL_METHOD_3         3  '3 positional arguments'
             1352  POP_TOP          

 L. 730      1354  LOAD_CONST               None
             1356  RETURN_VALUE     
           1358_0  COME_FROM          1318  '1318'

 L. 731      1358  LOAD_FAST                '_batchsize'
             1360  LOAD_CONST               False
             1362  COMPARE_OP               is
         1364_1366  POP_JUMP_IF_TRUE   1378  'to 1378'
             1368  LOAD_FAST                '_batchsize'
             1370  LOAD_CONST               0
             1372  COMPARE_OP               <=
         1374_1376  POP_JUMP_IF_FALSE  1414  'to 1414'
           1378_0  COME_FROM          1364  '1364'

 L. 732      1378  LOAD_GLOBAL              vis_msg
             1380  LOAD_ATTR                print
             1382  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Non-positive batch size'
             1384  LOAD_STR                 'error'
             1386  LOAD_CONST               ('type',)
             1388  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1390  POP_TOP          

 L. 733      1392  LOAD_GLOBAL              QtWidgets
             1394  LOAD_ATTR                QMessageBox
             1396  LOAD_METHOD              critical
             1398  LOAD_DEREF               'self'
             1400  LOAD_ATTR                msgbox

 L. 734      1402  LOAD_STR                 'Train 2D-CNN'

 L. 735      1404  LOAD_STR                 'Non-positive batch size'
             1406  CALL_METHOD_3         3  '3 positional arguments'
             1408  POP_TOP          

 L. 736      1410  LOAD_CONST               None
             1412  RETURN_VALUE     
           1414_0  COME_FROM          1374  '1374'

 L. 737      1414  LOAD_FAST                '_learning_rate'
             1416  LOAD_CONST               False
             1418  COMPARE_OP               is
         1420_1422  POP_JUMP_IF_TRUE   1434  'to 1434'
             1424  LOAD_FAST                '_learning_rate'
             1426  LOAD_CONST               0
             1428  COMPARE_OP               <=
         1430_1432  POP_JUMP_IF_FALSE  1470  'to 1470'
           1434_0  COME_FROM          1420  '1420'

 L. 738      1434  LOAD_GLOBAL              vis_msg
             1436  LOAD_ATTR                print
             1438  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Non-positive learning rate'
             1440  LOAD_STR                 'error'
             1442  LOAD_CONST               ('type',)
             1444  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1446  POP_TOP          

 L. 739      1448  LOAD_GLOBAL              QtWidgets
             1450  LOAD_ATTR                QMessageBox
             1452  LOAD_METHOD              critical
             1454  LOAD_DEREF               'self'
             1456  LOAD_ATTR                msgbox

 L. 740      1458  LOAD_STR                 'Train 2D-CNN'

 L. 741      1460  LOAD_STR                 'Non-positive learning rate'
             1462  CALL_METHOD_3         3  '3 positional arguments'
             1464  POP_TOP          

 L. 742      1466  LOAD_CONST               None
             1468  RETURN_VALUE     
           1470_0  COME_FROM          1430  '1430'

 L. 743      1470  LOAD_FAST                '_dropout_prob_fclayer'
             1472  LOAD_CONST               False
             1474  COMPARE_OP               is
         1476_1478  POP_JUMP_IF_TRUE   1490  'to 1490'
             1480  LOAD_FAST                '_dropout_prob_fclayer'
             1482  LOAD_CONST               0
             1484  COMPARE_OP               <=
         1486_1488  POP_JUMP_IF_FALSE  1526  'to 1526'
           1490_0  COME_FROM          1476  '1476'

 L. 744      1490  LOAD_GLOBAL              vis_msg
             1492  LOAD_ATTR                print
             1494  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: Negative dropout rate'
             1496  LOAD_STR                 'error'
             1498  LOAD_CONST               ('type',)
             1500  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1502  POP_TOP          

 L. 745      1504  LOAD_GLOBAL              QtWidgets
             1506  LOAD_ATTR                QMessageBox
             1508  LOAD_METHOD              critical
             1510  LOAD_DEREF               'self'
             1512  LOAD_ATTR                msgbox

 L. 746      1514  LOAD_STR                 'Train 2D-CNN'

 L. 747      1516  LOAD_STR                 'Negative dropout rate'
             1518  CALL_METHOD_3         3  '3 positional arguments'
             1520  POP_TOP          

 L. 748      1522  LOAD_CONST               None
             1524  RETURN_VALUE     
           1526_0  COME_FROM          1486  '1486'

 L. 750      1526  LOAD_GLOBAL              len
             1528  LOAD_DEREF               'self'
             1530  LOAD_ATTR                ldtexisting
             1532  LOAD_METHOD              text
             1534  CALL_METHOD_0         0  '0 positional arguments'
             1536  CALL_FUNCTION_1       1  '1 positional argument'
             1538  LOAD_CONST               1
             1540  COMPARE_OP               <
         1542_1544  POP_JUMP_IF_FALSE  1582  'to 1582'

 L. 751      1546  LOAD_GLOBAL              vis_msg
             1548  LOAD_ATTR                print
             1550  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: No pre-trained network specified'

 L. 752      1552  LOAD_STR                 'error'
             1554  LOAD_CONST               ('type',)
             1556  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1558  POP_TOP          

 L. 753      1560  LOAD_GLOBAL              QtWidgets
             1562  LOAD_ATTR                QMessageBox
             1564  LOAD_METHOD              critical
             1566  LOAD_DEREF               'self'
             1568  LOAD_ATTR                msgbox

 L. 754      1570  LOAD_STR                 'Train 2D-DCNN'

 L. 755      1572  LOAD_STR                 'No pre-trained network specified'
             1574  CALL_METHOD_3         3  '3 positional arguments'
             1576  POP_TOP          

 L. 756      1578  LOAD_CONST               None
             1580  RETURN_VALUE     
           1582_0  COME_FROM          1542  '1542'

 L. 757      1582  LOAD_GLOBAL              len
             1584  LOAD_DEREF               'self'
             1586  LOAD_ATTR                ldtsave
             1588  LOAD_METHOD              text
             1590  CALL_METHOD_0         0  '0 positional arguments'
             1592  CALL_FUNCTION_1       1  '1 positional argument'
             1594  LOAD_CONST               1
             1596  COMPARE_OP               <
         1598_1600  POP_JUMP_IF_FALSE  1638  'to 1638'

 L. 758      1602  LOAD_GLOBAL              vis_msg
             1604  LOAD_ATTR                print
             1606  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: No name specified for CNN network'
             1608  LOAD_STR                 'error'
             1610  LOAD_CONST               ('type',)
             1612  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1614  POP_TOP          

 L. 759      1616  LOAD_GLOBAL              QtWidgets
             1618  LOAD_ATTR                QMessageBox
             1620  LOAD_METHOD              critical
             1622  LOAD_DEREF               'self'
             1624  LOAD_ATTR                msgbox

 L. 760      1626  LOAD_STR                 'Train 2D-CNN'

 L. 761      1628  LOAD_STR                 'No name specified for CNN network'
             1630  CALL_METHOD_3         3  '3 positional arguments'
             1632  POP_TOP          

 L. 762      1634  LOAD_CONST               None
             1636  RETURN_VALUE     
           1638_0  COME_FROM          1598  '1598'

 L. 763      1638  LOAD_GLOBAL              os
             1640  LOAD_ATTR                path
             1642  LOAD_METHOD              dirname
             1644  LOAD_DEREF               'self'
             1646  LOAD_ATTR                ldtsave
             1648  LOAD_METHOD              text
             1650  CALL_METHOD_0         0  '0 positional arguments'
             1652  CALL_METHOD_1         1  '1 positional argument'
             1654  STORE_FAST               '_savepath'

 L. 764      1656  LOAD_GLOBAL              os
             1658  LOAD_ATTR                path
             1660  LOAD_METHOD              splitext
             1662  LOAD_GLOBAL              os
             1664  LOAD_ATTR                path
             1666  LOAD_METHOD              basename
             1668  LOAD_DEREF               'self'
             1670  LOAD_ATTR                ldtsave
             1672  LOAD_METHOD              text
             1674  CALL_METHOD_0         0  '0 positional arguments'
             1676  CALL_METHOD_1         1  '1 positional argument'
             1678  CALL_METHOD_1         1  '1 positional argument'
             1680  LOAD_CONST               0
             1682  BINARY_SUBSCR    
             1684  STORE_FAST               '_savename'

 L. 766      1686  LOAD_CONST               0
             1688  STORE_FAST               '_wdinl'

 L. 767      1690  LOAD_CONST               0
             1692  STORE_FAST               '_wdxl'

 L. 768      1694  LOAD_CONST               0
             1696  STORE_FAST               '_wdz'

 L. 769      1698  LOAD_DEREF               'self'
             1700  LOAD_ATTR                cbbornt
             1702  LOAD_METHOD              currentIndex
             1704  CALL_METHOD_0         0  '0 positional arguments'
             1706  LOAD_CONST               0
             1708  COMPARE_OP               ==
         1710_1712  POP_JUMP_IF_FALSE  1738  'to 1738'

 L. 770      1714  LOAD_GLOBAL              int
             1716  LOAD_FAST                '_image_width_old'
             1718  LOAD_CONST               2
             1720  BINARY_TRUE_DIVIDE
             1722  CALL_FUNCTION_1       1  '1 positional argument'
             1724  STORE_FAST               '_wdxl'

 L. 771      1726  LOAD_GLOBAL              int
             1728  LOAD_FAST                '_image_height_old'
             1730  LOAD_CONST               2
             1732  BINARY_TRUE_DIVIDE
             1734  CALL_FUNCTION_1       1  '1 positional argument'
             1736  STORE_FAST               '_wdz'
           1738_0  COME_FROM          1710  '1710'

 L. 772      1738  LOAD_DEREF               'self'
             1740  LOAD_ATTR                cbbornt
             1742  LOAD_METHOD              currentIndex
             1744  CALL_METHOD_0         0  '0 positional arguments'
             1746  LOAD_CONST               1
             1748  COMPARE_OP               ==
         1750_1752  POP_JUMP_IF_FALSE  1778  'to 1778'

 L. 773      1754  LOAD_GLOBAL              int
             1756  LOAD_FAST                '_image_width_old'
             1758  LOAD_CONST               2
             1760  BINARY_TRUE_DIVIDE
             1762  CALL_FUNCTION_1       1  '1 positional argument'
             1764  STORE_FAST               '_wdinl'

 L. 774      1766  LOAD_GLOBAL              int
             1768  LOAD_FAST                '_image_height_old'
             1770  LOAD_CONST               2
             1772  BINARY_TRUE_DIVIDE
             1774  CALL_FUNCTION_1       1  '1 positional argument'
             1776  STORE_FAST               '_wdz'
           1778_0  COME_FROM          1750  '1750'

 L. 775      1778  LOAD_DEREF               'self'
             1780  LOAD_ATTR                cbbornt
             1782  LOAD_METHOD              currentIndex
             1784  CALL_METHOD_0         0  '0 positional arguments'
             1786  LOAD_CONST               2
             1788  COMPARE_OP               ==
         1790_1792  POP_JUMP_IF_FALSE  1818  'to 1818'

 L. 776      1794  LOAD_GLOBAL              int
             1796  LOAD_FAST                '_image_width_old'
             1798  LOAD_CONST               2
             1800  BINARY_TRUE_DIVIDE
             1802  CALL_FUNCTION_1       1  '1 positional argument'
             1804  STORE_FAST               '_wdinl'

 L. 777      1806  LOAD_GLOBAL              int
             1808  LOAD_FAST                '_image_height_old'
             1810  LOAD_CONST               2
             1812  BINARY_TRUE_DIVIDE
             1814  CALL_FUNCTION_1       1  '1 positional argument'
             1816  STORE_FAST               '_wdxl'
           1818_0  COME_FROM          1790  '1790'

 L. 779      1818  LOAD_DEREF               'self'
             1820  LOAD_ATTR                survinfo
             1822  STORE_FAST               '_seisinfo'

 L. 781      1824  LOAD_GLOBAL              print
             1826  LOAD_STR                 'TrainMl2DCnnFromExisting: Step 1 - Get training samples:'
             1828  CALL_FUNCTION_1       1  '1 positional argument'
             1830  POP_TOP          

 L. 782      1832  LOAD_DEREF               'self'
             1834  LOAD_ATTR                traindataconfig
             1836  LOAD_STR                 'TrainPointSet'
             1838  BINARY_SUBSCR    
             1840  STORE_FAST               '_trainpoint'

 L. 783      1842  LOAD_GLOBAL              np
             1844  LOAD_METHOD              zeros
             1846  LOAD_CONST               0
             1848  LOAD_CONST               3
             1850  BUILD_LIST_2          2 
             1852  CALL_METHOD_1         1  '1 positional argument'
             1854  STORE_FAST               '_traindata'

 L. 784      1856  SETUP_LOOP         1932  'to 1932'
             1858  LOAD_FAST                '_trainpoint'
             1860  GET_ITER         
           1862_0  COME_FROM          1880  '1880'
             1862  FOR_ITER           1930  'to 1930'
             1864  STORE_FAST               '_p'

 L. 785      1866  LOAD_GLOBAL              point_ays
             1868  LOAD_METHOD              checkPoint
             1870  LOAD_DEREF               'self'
             1872  LOAD_ATTR                pointsetdata
             1874  LOAD_FAST                '_p'
             1876  BINARY_SUBSCR    
             1878  CALL_METHOD_1         1  '1 positional argument'
         1880_1882  POP_JUMP_IF_FALSE  1862  'to 1862'

 L. 786      1884  LOAD_GLOBAL              basic_mdt
             1886  LOAD_METHOD              exportMatDict
             1888  LOAD_DEREF               'self'
             1890  LOAD_ATTR                pointsetdata
             1892  LOAD_FAST                '_p'
             1894  BINARY_SUBSCR    
             1896  LOAD_STR                 'Inline'
             1898  LOAD_STR                 'Crossline'
             1900  LOAD_STR                 'Z'
             1902  BUILD_LIST_3          3 
             1904  CALL_METHOD_2         2  '2 positional arguments'
             1906  STORE_FAST               '_pt'

 L. 787      1908  LOAD_GLOBAL              np
             1910  LOAD_ATTR                concatenate
             1912  LOAD_FAST                '_traindata'
             1914  LOAD_FAST                '_pt'
             1916  BUILD_TUPLE_2         2 
             1918  LOAD_CONST               0
             1920  LOAD_CONST               ('axis',)
             1922  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1924  STORE_FAST               '_traindata'
         1926_1928  JUMP_BACK          1862  'to 1862'
             1930  POP_BLOCK        
           1932_0  COME_FROM_LOOP     1856  '1856'

 L. 788      1932  LOAD_GLOBAL              seis_ays
             1934  LOAD_ATTR                removeOutofSurveySample
             1936  LOAD_FAST                '_traindata'

 L. 789      1938  LOAD_FAST                '_seisinfo'
             1940  LOAD_STR                 'ILStart'
             1942  BINARY_SUBSCR    
             1944  LOAD_FAST                '_wdinl'
             1946  LOAD_FAST                '_seisinfo'
             1948  LOAD_STR                 'ILStep'
             1950  BINARY_SUBSCR    
             1952  BINARY_MULTIPLY  
             1954  BINARY_ADD       

 L. 790      1956  LOAD_FAST                '_seisinfo'
             1958  LOAD_STR                 'ILEnd'
             1960  BINARY_SUBSCR    
             1962  LOAD_FAST                '_wdinl'
             1964  LOAD_FAST                '_seisinfo'
             1966  LOAD_STR                 'ILStep'
             1968  BINARY_SUBSCR    
             1970  BINARY_MULTIPLY  
             1972  BINARY_SUBTRACT  

 L. 791      1974  LOAD_FAST                '_seisinfo'
             1976  LOAD_STR                 'XLStart'
             1978  BINARY_SUBSCR    
             1980  LOAD_FAST                '_wdxl'
             1982  LOAD_FAST                '_seisinfo'
             1984  LOAD_STR                 'XLStep'
             1986  BINARY_SUBSCR    
             1988  BINARY_MULTIPLY  
             1990  BINARY_ADD       

 L. 792      1992  LOAD_FAST                '_seisinfo'
             1994  LOAD_STR                 'XLEnd'
             1996  BINARY_SUBSCR    
             1998  LOAD_FAST                '_wdxl'
             2000  LOAD_FAST                '_seisinfo'
             2002  LOAD_STR                 'XLStep'
             2004  BINARY_SUBSCR    
             2006  BINARY_MULTIPLY  
             2008  BINARY_SUBTRACT  

 L. 793      2010  LOAD_FAST                '_seisinfo'
             2012  LOAD_STR                 'ZStart'
             2014  BINARY_SUBSCR    
             2016  LOAD_FAST                '_wdz'
             2018  LOAD_FAST                '_seisinfo'
             2020  LOAD_STR                 'ZStep'
             2022  BINARY_SUBSCR    
             2024  BINARY_MULTIPLY  
             2026  BINARY_ADD       

 L. 794      2028  LOAD_FAST                '_seisinfo'
             2030  LOAD_STR                 'ZEnd'
             2032  BINARY_SUBSCR    
             2034  LOAD_FAST                '_wdz'
             2036  LOAD_FAST                '_seisinfo'
             2038  LOAD_STR                 'ZStep'
             2040  BINARY_SUBSCR    
             2042  BINARY_MULTIPLY  
             2044  BINARY_SUBTRACT  
             2046  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             2048  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2050  STORE_FAST               '_traindata'

 L. 797      2052  LOAD_GLOBAL              np
             2054  LOAD_METHOD              shape
             2056  LOAD_FAST                '_traindata'
             2058  CALL_METHOD_1         1  '1 positional argument'
             2060  LOAD_CONST               0
             2062  BINARY_SUBSCR    
             2064  LOAD_CONST               0
             2066  COMPARE_OP               <=
         2068_2070  POP_JUMP_IF_FALSE  2108  'to 2108'

 L. 798      2072  LOAD_GLOBAL              vis_msg
             2074  LOAD_ATTR                print
             2076  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: No training sample found'
             2078  LOAD_STR                 'error'
             2080  LOAD_CONST               ('type',)
             2082  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2084  POP_TOP          

 L. 799      2086  LOAD_GLOBAL              QtWidgets
             2088  LOAD_ATTR                QMessageBox
             2090  LOAD_METHOD              critical
             2092  LOAD_DEREF               'self'
             2094  LOAD_ATTR                msgbox

 L. 800      2096  LOAD_STR                 'Train 2D-CNN'

 L. 801      2098  LOAD_STR                 'No training sample found'
             2100  CALL_METHOD_3         3  '3 positional arguments'
             2102  POP_TOP          

 L. 802      2104  LOAD_CONST               None
             2106  RETURN_VALUE     
           2108_0  COME_FROM          2068  '2068'

 L. 805      2108  LOAD_GLOBAL              print
             2110  LOAD_STR                 'TrainMl2DCnnFromExisting: Step 2 - Retrieve and interpolate images: (%d, %d) --> (%d, %d)'

 L. 806      2112  LOAD_FAST                '_image_height_old'
             2114  LOAD_FAST                '_image_width_old'
             2116  LOAD_FAST                '_image_height_new'
             2118  LOAD_FAST                '_image_width_new'
             2120  BUILD_TUPLE_4         4 
             2122  BINARY_MODULO    
             2124  CALL_FUNCTION_1       1  '1 positional argument'
             2126  POP_TOP          

 L. 807      2128  BUILD_MAP_0           0 
             2130  STORE_FAST               '_traindict'

 L. 808      2132  SETUP_LOOP         2204  'to 2204'
             2134  LOAD_FAST                '_features'
             2136  GET_ITER         
             2138  FOR_ITER           2202  'to 2202'
             2140  STORE_FAST               'f'

 L. 809      2142  LOAD_DEREF               'self'
             2144  LOAD_ATTR                seisdata
             2146  LOAD_FAST                'f'
             2148  BINARY_SUBSCR    
             2150  STORE_FAST               '_seisdata'

 L. 810      2152  LOAD_GLOBAL              seis_ays
             2154  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2156  LOAD_FAST                '_seisdata'
             2158  LOAD_FAST                '_traindata'
             2160  LOAD_DEREF               'self'
             2162  LOAD_ATTR                survinfo

 L. 811      2164  LOAD_FAST                '_wdinl'
             2166  LOAD_FAST                '_wdxl'
             2168  LOAD_FAST                '_wdz'

 L. 812      2170  LOAD_CONST               False
             2172  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2174  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2176  LOAD_CONST               None
             2178  LOAD_CONST               None
             2180  BUILD_SLICE_2         2 
             2182  LOAD_CONST               3
             2184  LOAD_CONST               None
             2186  BUILD_SLICE_2         2 
             2188  BUILD_TUPLE_2         2 
             2190  BINARY_SUBSCR    
             2192  LOAD_FAST                '_traindict'
             2194  LOAD_FAST                'f'
             2196  STORE_SUBSCR     
         2198_2200  JUMP_BACK          2138  'to 2138'
             2202  POP_BLOCK        
           2204_0  COME_FROM_LOOP     2132  '2132'

 L. 813      2204  LOAD_FAST                '_target'
             2206  LOAD_FAST                '_features'
             2208  COMPARE_OP               not-in
         2210_2212  POP_JUMP_IF_FALSE  2264  'to 2264'

 L. 814      2214  LOAD_DEREF               'self'
             2216  LOAD_ATTR                seisdata
             2218  LOAD_FAST                '_target'
             2220  BINARY_SUBSCR    
             2222  STORE_FAST               '_seisdata'

 L. 815      2224  LOAD_GLOBAL              seis_ays
             2226  LOAD_ATTR                retrieveSeisSampleFrom3DMat
             2228  LOAD_FAST                '_seisdata'
             2230  LOAD_FAST                '_traindata'
             2232  LOAD_DEREF               'self'
             2234  LOAD_ATTR                survinfo

 L. 816      2236  LOAD_CONST               False
             2238  LOAD_CONST               ('seisinfo', 'verbose')
             2240  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2242  LOAD_CONST               None
             2244  LOAD_CONST               None
             2246  BUILD_SLICE_2         2 
             2248  LOAD_CONST               3
             2250  LOAD_CONST               None
             2252  BUILD_SLICE_2         2 
             2254  BUILD_TUPLE_2         2 
             2256  BINARY_SUBSCR    
             2258  LOAD_FAST                '_traindict'
             2260  LOAD_FAST                '_target'
             2262  STORE_SUBSCR     
           2264_0  COME_FROM          2210  '2210'

 L. 818      2264  LOAD_DEREF               'self'
             2266  LOAD_ATTR                traindataconfig
             2268  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2270  BINARY_SUBSCR    
         2272_2274  POP_JUMP_IF_FALSE  2356  'to 2356'

 L. 819      2276  SETUP_LOOP         2356  'to 2356'
             2278  LOAD_FAST                '_features'
             2280  GET_ITER         
           2282_0  COME_FROM          2310  '2310'
             2282  FOR_ITER           2354  'to 2354'
             2284  STORE_FAST               'f'

 L. 820      2286  LOAD_GLOBAL              ml_aug
             2288  LOAD_METHOD              removeInvariantFeature
             2290  LOAD_FAST                '_traindict'
             2292  LOAD_FAST                'f'
             2294  CALL_METHOD_2         2  '2 positional arguments'
             2296  STORE_FAST               '_traindict'

 L. 821      2298  LOAD_GLOBAL              basic_mdt
             2300  LOAD_METHOD              maxDictConstantRow
             2302  LOAD_FAST                '_traindict'
             2304  CALL_METHOD_1         1  '1 positional argument'
             2306  LOAD_CONST               0
             2308  COMPARE_OP               <=
         2310_2312  POP_JUMP_IF_FALSE  2282  'to 2282'

 L. 822      2314  LOAD_GLOBAL              vis_msg
             2316  LOAD_ATTR                print
             2318  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: No training sample found'
             2320  LOAD_STR                 'error'
             2322  LOAD_CONST               ('type',)
             2324  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2326  POP_TOP          

 L. 823      2328  LOAD_GLOBAL              QtWidgets
             2330  LOAD_ATTR                QMessageBox
             2332  LOAD_METHOD              critical
             2334  LOAD_DEREF               'self'
             2336  LOAD_ATTR                msgbox

 L. 824      2338  LOAD_STR                 'Train 2D-CNN'

 L. 825      2340  LOAD_STR                 'No training sample found'
             2342  CALL_METHOD_3         3  '3 positional arguments'
             2344  POP_TOP          

 L. 826      2346  LOAD_CONST               None
             2348  RETURN_VALUE     
         2350_2352  JUMP_BACK          2282  'to 2282'
             2354  POP_BLOCK        
           2356_0  COME_FROM_LOOP     2276  '2276'
           2356_1  COME_FROM          2272  '2272'

 L. 828      2356  LOAD_GLOBAL              np
             2358  LOAD_METHOD              round
             2360  LOAD_FAST                '_traindict'
             2362  LOAD_FAST                '_target'
             2364  BINARY_SUBSCR    
             2366  CALL_METHOD_1         1  '1 positional argument'
             2368  LOAD_METHOD              astype
             2370  LOAD_GLOBAL              int
             2372  CALL_METHOD_1         1  '1 positional argument'
             2374  LOAD_FAST                '_traindict'
             2376  LOAD_FAST                '_target'
             2378  STORE_SUBSCR     

 L. 830      2380  LOAD_FAST                '_image_height_new'
             2382  LOAD_FAST                '_image_height_old'
             2384  COMPARE_OP               !=
         2386_2388  POP_JUMP_IF_TRUE   2400  'to 2400'
             2390  LOAD_FAST                '_image_width_new'
             2392  LOAD_FAST                '_image_width_old'
             2394  COMPARE_OP               !=
         2396_2398  POP_JUMP_IF_FALSE  2444  'to 2444'
           2400_0  COME_FROM          2386  '2386'

 L. 831      2400  SETUP_LOOP         2444  'to 2444'
             2402  LOAD_FAST                '_features'
             2404  GET_ITER         
             2406  FOR_ITER           2442  'to 2442'
             2408  STORE_FAST               'f'

 L. 832      2410  LOAD_GLOBAL              basic_image
             2412  LOAD_ATTR                changeImageSize
             2414  LOAD_FAST                '_traindict'
             2416  LOAD_FAST                'f'
             2418  BINARY_SUBSCR    

 L. 833      2420  LOAD_FAST                '_image_height_old'

 L. 834      2422  LOAD_FAST                '_image_width_old'

 L. 835      2424  LOAD_FAST                '_image_height_new'

 L. 836      2426  LOAD_FAST                '_image_width_new'
             2428  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2430  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2432  LOAD_FAST                '_traindict'
             2434  LOAD_FAST                'f'
             2436  STORE_SUBSCR     
         2438_2440  JUMP_BACK          2406  'to 2406'
             2442  POP_BLOCK        
           2444_0  COME_FROM_LOOP     2400  '2400'
           2444_1  COME_FROM          2396  '2396'

 L. 837      2444  LOAD_DEREF               'self'
             2446  LOAD_ATTR                traindataconfig
             2448  LOAD_STR                 'RotateFeature_Checked'
             2450  BINARY_SUBSCR    
             2452  LOAD_CONST               True
             2454  COMPARE_OP               is
         2456_2458  POP_JUMP_IF_FALSE  2588  'to 2588'

 L. 838      2460  SETUP_LOOP         2532  'to 2532'
             2462  LOAD_FAST                '_features'
             2464  GET_ITER         
             2466  FOR_ITER           2530  'to 2530'
             2468  STORE_FAST               'f'

 L. 839      2470  LOAD_FAST                '_image_height_new'
             2472  LOAD_FAST                '_image_width_new'
             2474  COMPARE_OP               ==
         2476_2478  POP_JUMP_IF_FALSE  2504  'to 2504'

 L. 840      2480  LOAD_GLOBAL              ml_aug
             2482  LOAD_METHOD              rotateImage6Way
             2484  LOAD_FAST                '_traindict'
             2486  LOAD_FAST                'f'
             2488  BINARY_SUBSCR    
             2490  LOAD_FAST                '_image_height_new'
             2492  LOAD_FAST                '_image_width_new'
             2494  CALL_METHOD_3         3  '3 positional arguments'
             2496  LOAD_FAST                '_traindict'
             2498  LOAD_FAST                'f'
             2500  STORE_SUBSCR     
             2502  JUMP_BACK          2466  'to 2466'
           2504_0  COME_FROM          2476  '2476'

 L. 842      2504  LOAD_GLOBAL              ml_aug
             2506  LOAD_METHOD              rotateImage4Way
             2508  LOAD_FAST                '_traindict'
             2510  LOAD_FAST                'f'
             2512  BINARY_SUBSCR    
             2514  LOAD_FAST                '_image_height_new'
             2516  LOAD_FAST                '_image_width_new'
             2518  CALL_METHOD_3         3  '3 positional arguments'
             2520  LOAD_FAST                '_traindict'
             2522  LOAD_FAST                'f'
             2524  STORE_SUBSCR     
         2526_2528  JUMP_BACK          2466  'to 2466'
             2530  POP_BLOCK        
           2532_0  COME_FROM_LOOP     2460  '2460'

 L. 844      2532  LOAD_FAST                '_image_height_new'
             2534  LOAD_FAST                '_image_width_new'
             2536  COMPARE_OP               ==
         2538_2540  POP_JUMP_IF_FALSE  2566  'to 2566'

 L. 846      2542  LOAD_GLOBAL              ml_aug
             2544  LOAD_METHOD              rotateImage6Way
             2546  LOAD_FAST                '_traindict'
             2548  LOAD_FAST                '_target'
             2550  BINARY_SUBSCR    
             2552  LOAD_CONST               1
             2554  LOAD_CONST               1
             2556  CALL_METHOD_3         3  '3 positional arguments'
             2558  LOAD_FAST                '_traindict'
             2560  LOAD_FAST                '_target'
             2562  STORE_SUBSCR     
             2564  JUMP_FORWARD       2588  'to 2588'
           2566_0  COME_FROM          2538  '2538'

 L. 849      2566  LOAD_GLOBAL              ml_aug
             2568  LOAD_METHOD              rotateImage4Way
             2570  LOAD_FAST                '_traindict'
             2572  LOAD_FAST                '_target'
             2574  BINARY_SUBSCR    
             2576  LOAD_CONST               1
             2578  LOAD_CONST               1
             2580  CALL_METHOD_3         3  '3 positional arguments'
             2582  LOAD_FAST                '_traindict'
             2584  LOAD_FAST                '_target'
             2586  STORE_SUBSCR     
           2588_0  COME_FROM          2564  '2564'
           2588_1  COME_FROM          2456  '2456'

 L. 851      2588  LOAD_GLOBAL              print
             2590  LOAD_STR                 'TrainMl2DCnnFromScratch: A total of %d valid training samples'
             2592  LOAD_GLOBAL              basic_mdt
             2594  LOAD_METHOD              maxDictConstantRow

 L. 852      2596  LOAD_FAST                '_traindict'
             2598  CALL_METHOD_1         1  '1 positional argument'
             2600  BINARY_MODULO    
             2602  CALL_FUNCTION_1       1  '1 positional argument'
             2604  POP_TOP          

 L. 854      2606  LOAD_GLOBAL              print
             2608  LOAD_STR                 'TrainMl2DCnnFromExisting: Step 3 - Balance labels'
             2610  CALL_FUNCTION_1       1  '1 positional argument'
             2612  POP_TOP          

 L. 855      2614  LOAD_DEREF               'self'
             2616  LOAD_ATTR                traindataconfig
             2618  LOAD_STR                 'BalanceTarget_Checked'
             2620  BINARY_SUBSCR    
         2622_2624  POP_JUMP_IF_FALSE  2666  'to 2666'

 L. 856      2626  LOAD_GLOBAL              ml_aug
             2628  LOAD_METHOD              balanceLabelbyExtension
             2630  LOAD_FAST                '_traindict'
             2632  LOAD_FAST                '_target'
             2634  CALL_METHOD_2         2  '2 positional arguments'
             2636  STORE_FAST               '_traindict'

 L. 857      2638  LOAD_GLOBAL              print
             2640  LOAD_STR                 'TrainMl2DCnnFromExisting: A total of %d training samples after balance'
             2642  LOAD_GLOBAL              np
             2644  LOAD_METHOD              shape
             2646  LOAD_FAST                '_traindict'
             2648  LOAD_FAST                '_target'
             2650  BINARY_SUBSCR    
             2652  CALL_METHOD_1         1  '1 positional argument'
             2654  LOAD_CONST               0
             2656  BINARY_SUBSCR    
             2658  BINARY_MODULO    
             2660  CALL_FUNCTION_1       1  '1 positional argument'
             2662  POP_TOP          
             2664  JUMP_FORWARD       2674  'to 2674'
           2666_0  COME_FROM          2622  '2622'

 L. 859      2666  LOAD_GLOBAL              print
             2668  LOAD_STR                 'TrainMl2DCnnFromExisting: No balance applied'
             2670  CALL_FUNCTION_1       1  '1 positional argument'
             2672  POP_TOP          
           2674_0  COME_FROM          2664  '2664'

 L. 861      2674  LOAD_GLOBAL              print
             2676  LOAD_STR                 'TrainMl2DCnnFromExisting: Step 4 - Start training'
             2678  CALL_FUNCTION_1       1  '1 positional argument'
             2680  POP_TOP          

 L. 863      2682  LOAD_GLOBAL              QtWidgets
             2684  LOAD_METHOD              QProgressDialog
             2686  CALL_METHOD_0         0  '0 positional arguments'
             2688  STORE_FAST               '_pgsdlg'

 L. 864      2690  LOAD_GLOBAL              QtGui
             2692  LOAD_METHOD              QIcon
             2694  CALL_METHOD_0         0  '0 positional arguments'
             2696  STORE_FAST               'icon'

 L. 865      2698  LOAD_FAST                'icon'
             2700  LOAD_METHOD              addPixmap
             2702  LOAD_GLOBAL              QtGui
             2704  LOAD_METHOD              QPixmap
             2706  LOAD_GLOBAL              os
             2708  LOAD_ATTR                path
             2710  LOAD_METHOD              join
             2712  LOAD_DEREF               'self'
             2714  LOAD_ATTR                iconpath
             2716  LOAD_STR                 'icons/new.png'
             2718  CALL_METHOD_2         2  '2 positional arguments'
             2720  CALL_METHOD_1         1  '1 positional argument'

 L. 866      2722  LOAD_GLOBAL              QtGui
             2724  LOAD_ATTR                QIcon
             2726  LOAD_ATTR                Normal
             2728  LOAD_GLOBAL              QtGui
             2730  LOAD_ATTR                QIcon
             2732  LOAD_ATTR                Off
             2734  CALL_METHOD_3         3  '3 positional arguments'
             2736  POP_TOP          

 L. 867      2738  LOAD_FAST                '_pgsdlg'
             2740  LOAD_METHOD              setWindowIcon
             2742  LOAD_FAST                'icon'
             2744  CALL_METHOD_1         1  '1 positional argument'
             2746  POP_TOP          

 L. 868      2748  LOAD_FAST                '_pgsdlg'
             2750  LOAD_METHOD              setWindowTitle
             2752  LOAD_STR                 'Train 2D-CNN'
             2754  CALL_METHOD_1         1  '1 positional argument'
             2756  POP_TOP          

 L. 869      2758  LOAD_FAST                '_pgsdlg'
             2760  LOAD_METHOD              setCancelButton
             2762  LOAD_CONST               None
             2764  CALL_METHOD_1         1  '1 positional argument'
             2766  POP_TOP          

 L. 870      2768  LOAD_FAST                '_pgsdlg'
             2770  LOAD_METHOD              setWindowFlags
             2772  LOAD_GLOBAL              QtCore
             2774  LOAD_ATTR                Qt
             2776  LOAD_ATTR                WindowStaysOnTopHint
             2778  CALL_METHOD_1         1  '1 positional argument'
             2780  POP_TOP          

 L. 871      2782  LOAD_FAST                '_pgsdlg'
             2784  LOAD_METHOD              forceShow
             2786  CALL_METHOD_0         0  '0 positional arguments'
             2788  POP_TOP          

 L. 872      2790  LOAD_FAST                '_pgsdlg'
             2792  LOAD_METHOD              setFixedWidth
             2794  LOAD_CONST               400
             2796  CALL_METHOD_1         1  '1 positional argument'
             2798  POP_TOP          

 L. 873      2800  LOAD_GLOBAL              ml_cnn
             2802  LOAD_ATTR                createCNNClassifierFromExisting
             2804  LOAD_FAST                '_traindict'

 L. 874      2806  LOAD_FAST                '_image_height_new'
             2808  LOAD_FAST                '_image_width_new'

 L. 875      2810  LOAD_FAST                '_features'
             2812  LOAD_FAST                '_target'

 L. 876      2814  LOAD_FAST                '_nepoch'
             2816  LOAD_FAST                '_batchsize'

 L. 877      2818  LOAD_FAST                '_nconvblock'

 L. 878      2820  LOAD_FAST                '_nconvlayer'
             2822  LOAD_FAST                '_nconvfeature'

 L. 879      2824  LOAD_FAST                '_nfclayer'
             2826  LOAD_FAST                '_nfcneuron'

 L. 880      2828  LOAD_FAST                '_pool_height'
             2830  LOAD_FAST                '_pool_width'

 L. 881      2832  LOAD_FAST                '_learning_rate'

 L. 882      2834  LOAD_FAST                '_dropout_prob_fclayer'

 L. 883      2836  LOAD_CONST               True

 L. 884      2838  LOAD_FAST                '_savepath'
             2840  LOAD_FAST                '_savename'

 L. 885      2842  LOAD_FAST                '_pgsdlg'

 L. 886      2844  LOAD_FAST                '_precnnpath'

 L. 887      2846  LOAD_FAST                '_precnnname'

 L. 888      2848  LOAD_FAST                '_blockidx'
             2850  LOAD_FAST                '_layeridx'

 L. 889      2852  LOAD_FAST                '_trainable'
             2854  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'nepoch', 'batchsize', 'nconvblock', 'nconvlayer', 'nconvfeature', 'nfclayer', 'nfcneuron', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprobfclayer', 'save2disk', 'savepath', 'savename', 'qpgsdlg', 'precnnpath', 'precnnname', 'blockidx', 'layeridx', 'trainable')
             2856  CALL_FUNCTION_KW_25    25  '25 total positional and keyword args'
             2858  STORE_FAST               '_cnnlog'

 L. 892      2860  LOAD_GLOBAL              QtWidgets
             2862  LOAD_ATTR                QMessageBox
             2864  LOAD_METHOD              information
             2866  LOAD_DEREF               'self'
             2868  LOAD_ATTR                msgbox

 L. 893      2870  LOAD_STR                 'Train 2D-CNN'

 L. 894      2872  LOAD_STR                 'CNN trained successfully'
             2874  CALL_METHOD_3         3  '3 positional arguments'
             2876  POP_TOP          

 L. 896      2878  LOAD_GLOBAL              QtWidgets
             2880  LOAD_ATTR                QMessageBox
             2882  LOAD_METHOD              question
             2884  LOAD_DEREF               'self'
             2886  LOAD_ATTR                msgbox
             2888  LOAD_STR                 'Train 2D-CNN'
             2890  LOAD_STR                 'View learning matrix?'

 L. 897      2892  LOAD_GLOBAL              QtWidgets
             2894  LOAD_ATTR                QMessageBox
             2896  LOAD_ATTR                Yes
             2898  LOAD_GLOBAL              QtWidgets
             2900  LOAD_ATTR                QMessageBox
             2902  LOAD_ATTR                No
             2904  BINARY_OR        

 L. 898      2906  LOAD_GLOBAL              QtWidgets
             2908  LOAD_ATTR                QMessageBox
             2910  LOAD_ATTR                Yes
             2912  CALL_METHOD_5         5  '5 positional arguments'
             2914  STORE_FAST               'reply'

 L. 900      2916  LOAD_FAST                'reply'
             2918  LOAD_GLOBAL              QtWidgets
             2920  LOAD_ATTR                QMessageBox
             2922  LOAD_ATTR                Yes
             2924  COMPARE_OP               ==
         2926_2928  POP_JUMP_IF_FALSE  2996  'to 2996'

 L. 901      2930  LOAD_GLOBAL              QtWidgets
             2932  LOAD_METHOD              QDialog
             2934  CALL_METHOD_0         0  '0 positional arguments'
             2936  STORE_FAST               '_viewmllearnmat'

 L. 902      2938  LOAD_GLOBAL              gui_viewmllearnmat
             2940  CALL_FUNCTION_0       0  '0 positional arguments'
             2942  STORE_FAST               '_gui'

 L. 903      2944  LOAD_FAST                '_cnnlog'
             2946  LOAD_STR                 'learning_curve'
             2948  BINARY_SUBSCR    
             2950  LOAD_FAST                '_gui'
             2952  STORE_ATTR               learnmat

 L. 904      2954  LOAD_DEREF               'self'
             2956  LOAD_ATTR                linestyle
             2958  LOAD_FAST                '_gui'
             2960  STORE_ATTR               linestyle

 L. 905      2962  LOAD_DEREF               'self'
             2964  LOAD_ATTR                fontstyle
             2966  LOAD_FAST                '_gui'
             2968  STORE_ATTR               fontstyle

 L. 906      2970  LOAD_FAST                '_gui'
             2972  LOAD_METHOD              setupGUI
             2974  LOAD_FAST                '_viewmllearnmat'
             2976  CALL_METHOD_1         1  '1 positional argument'
             2978  POP_TOP          

 L. 907      2980  LOAD_FAST                '_viewmllearnmat'
             2982  LOAD_METHOD              exec
             2984  CALL_METHOD_0         0  '0 positional arguments'
             2986  POP_TOP          

 L. 908      2988  LOAD_FAST                '_viewmllearnmat'
             2990  LOAD_METHOD              show
             2992  CALL_METHOD_0         0  '0 positional arguments'
             2994  POP_TOP          
           2996_0  COME_FROM          2926  '2926'

Parse error at or near `POP_TOP' instruction at offset 2994

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
    TrainMl2DCnnFromExisting = QtWidgets.QWidget()
    gui = trainml2dcnnfromexisting()
    gui.setupGUI(TrainMl2DCnnFromExisting)
    TrainMl2DCnnFromExisting.show()
    sys.exit(app.exec_())