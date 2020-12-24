# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml2dasfefromexisting.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 54002 bytes
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

class trainml2dasfefromexisting(object):
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
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False

    def setupGUI(self, TrainMl2DAsfeFromExisting):
        TrainMl2DAsfeFromExisting.setObjectName('TrainMl2DAsfeFromExisting')
        TrainMl2DAsfeFromExisting.setFixedSize(800, 610)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl2DAsfeFromExisting.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl2DAsfeFromExisting)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl2DAsfeFromExisting)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblexisting = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblexisting.setObjectName('lblexisting')
        self.lblexisting.setGeometry(QtCore.QRect(410, 50, 100, 30))
        self.ldtexisting = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtexisting.setObjectName('ldtexisting')
        self.ldtexisting.setGeometry(QtCore.QRect(510, 50, 210, 30))
        self.btnexisting = QtWidgets.QPushButton(TrainMl2DAsfeFromExisting)
        self.btnexisting.setObjectName('btnexisting')
        self.btnexisting.setGeometry(QtCore.QRect(730, 50, 60, 30))
        self.lblnconvblockexisting = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblnconvblockexisting.setObjectName('lblnconvblockexisting')
        self.lblnconvblockexisting.setGeometry(QtCore.QRect(410, 90, 130, 30))
        self.ldtnconvblockexisting = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtnconvblockexisting.setObjectName('ldtnconvblockexisting')
        self.ldtnconvblockexisting.setGeometry(QtCore.QRect(550, 90, 40, 30))
        self.twgnconvblockexisting = QtWidgets.QTableWidget(TrainMl2DAsfeFromExisting)
        self.twgnconvblockexisting.setObjectName('twgnconvblockexisting')
        self.twgnconvblockexisting.setGeometry(QtCore.QRect(610, 90, 180, 150))
        self.twgnconvblockexisting.setColumnCount(3)
        self.twgnconvblockexisting.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblockexisting.verticalHeader().hide()
        self.lblblockid = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblblockid.setObjectName('lblblockid')
        self.lblblockid.setGeometry(QtCore.QRect(410, 130, 130, 30))
        self.cbbblockid = QtWidgets.QComboBox(TrainMl2DAsfeFromExisting)
        self.cbbblockid.setObjectName('cbbblockid')
        self.cbbblockid.setGeometry(QtCore.QRect(550, 130, 40, 30))
        self.lbllayerid = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lbllayerid.setObjectName('lbllayerid')
        self.lbllayerid.setGeometry(QtCore.QRect(410, 170, 130, 30))
        self.cbblayerid = QtWidgets.QComboBox(TrainMl2DAsfeFromExisting)
        self.cbblayerid.setObjectName('cbblayerid')
        self.cbblayerid.setGeometry(QtCore.QRect(550, 170, 40, 30))
        self.lbltrainable = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lbltrainable.setObjectName('lbltrainable')
        self.lbltrainable.setGeometry(QtCore.QRect(410, 210, 130, 30))
        self.cbbtrainable = QtWidgets.QComboBox(TrainMl2DAsfeFromExisting)
        self.cbbtrainable.setObjectName('cbbtrainable')
        self.cbbtrainable.setGeometry(QtCore.QRect(550, 210, 40, 30))
        self.lblappend = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblappend.setObjectName('lblappend')
        self.lblappend.setGeometry(QtCore.QRect(410, 250, 200, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 290, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 290, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl2DAsfeFromExisting)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 330, 180, 180))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 290, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 290, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(TrainMl2DAsfeFromExisting)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 330, 180, 180))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 520, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 520, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 520, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 560, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 560, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 520, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 520, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 520, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 560, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 560, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl2DAsfeFromExisting)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 260, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 260, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 300, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 300, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 300, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 300, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 340, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 340, 40, 30))
        self.lblfcdropout = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblfcdropout.setObjectName('lblfcdropout')
        self.lblfcdropout.setGeometry(QtCore.QRect(210, 340, 130, 30))
        self.ldtfcdropout = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtfcdropout.setObjectName('ldtfcdropout')
        self.ldtfcdropout.setGeometry(QtCore.QRect(350, 340, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl2DAsfeFromExisting)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 390, 100, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl2DAsfeFromExisting)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(110, 390, 210, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl2DAsfeFromExisting)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 390, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl2DAsfeFromExisting)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(120, 560, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl2DAsfeFromExisting)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl2DAsfeFromExisting.geometry().center().x()
        _center_y = TrainMl2DAsfeFromExisting.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl2DAsfeFromExisting)
        QtCore.QMetaObject.connectSlotsByName(TrainMl2DAsfeFromExisting)

    def retranslateGUI(self, TrainMl2DAsfeFromExisting):
        self.dialog = TrainMl2DAsfeFromExisting
        _translate = QtCore.QCoreApplication.translate
        TrainMl2DAsfeFromExisting.setWindowTitle(_translate('TrainMl2DAsfeFromExisting', 'Train 2D-ASFE from pre-trained'))
        self.lblfeature.setText(_translate('TrainMl2DAsfeFromExisting', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl2DAsfeFromExisting', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.btnconfigtraindata.setText(_translate('UpdateMl2DCnn', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('TrainMl2DAsfeFromExisting', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl2DAsfeFromExisting', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl2DAsfeFromExisting', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl2DAsfeFromExisting', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl2DAsfeFromExisting', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl2DAsfeFromExisting', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl2DAsfeFromExisting', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl2DAsfeFromExisting', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl2DAsfeFromExisting', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl2DAsfeFromExisting', '32'))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        if self.checkSurvInfo():
            self.featurelist.clear()
            self.lwgfeature.clear()
            _firstfeature = None
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    self.featurelist.append(i)
                    item = QtWidgets.QListWidgetItem(self.lwgfeature)
                    item.setText(_translate('TrainMl2DAsfeFromExisting', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
        self.lblnetwork.setText(_translate('TrainMl2DAsfeFromExisting', 'Specify ASFE architecture:'))
        self.lblexisting.setText(_translate('TrainMl2DAsfeFromExisting', 'Select pre-trained:'))
        self.ldtexisting.setText(_translate('TrainMl2DAsfeFromExisting', ''))
        self.ldtexisting.textChanged.connect(self.changeLdtExisting)
        self.btnexisting.setText(_translate('TrainMl2DAsfeFromExisting', 'Browse'))
        self.btnexisting.clicked.connect(self.clickBtnExisting)
        self.lblnconvblockexisting.setText(_translate('TrainMl2DAsfeFromExisting', 'Available conv. blocks:'))
        self.lblnconvblockexisting.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblockexisting.setText(_translate('TrainMl2DAsfeFromExisting', ''))
        self.ldtnconvblockexisting.setEnabled(False)
        self.ldtnconvblockexisting.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblockexisting.textChanged.connect(self.changeLdtNconvblockExisting)
        self.twgnconvblockexisting.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblblockid.setText(_translate('TrainMl2DAsfeFromExisting', 'Select conv. block ID:'))
        self.lblblockid.setAlignment(QtCore.Qt.AlignRight)
        self.cbbblockid.currentIndexChanged.connect(self.changeCbbBlockid)
        self.lbllayerid.setText(_translate('TrainMl2DAsfeFromExisting', 'Select conv. layer ID:'))
        self.lbllayerid.setAlignment(QtCore.Qt.AlignRight)
        self.lbltrainable.setText(_translate('TrainMl2DAsfeFromExisting', 'Is trainable?:'))
        self.lbltrainable.setAlignment(QtCore.Qt.AlignRight)
        self.cbbtrainable.addItems(['Yes', 'No'])
        self.lblappend.setText(_translate('TrainMl2DAsfeFromExisting', 'Append more blocks & layers:'))
        self.lblnconvblock.setText(_translate('TrainMl2DAsfeFromExisting', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl2DAsfeFromExisting', '3'))
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

        self.lblnfclayer.setText(_translate('TrainMl2DAsfeFromExisting', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('TrainMl2DAsfeFromExisting', '2'))
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.twgnfclayer.setRowCount(2)
        for _idx in range(int(self.ldtnfclayer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl2DAsfeFromExisting', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgnfclayer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgnfclayer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl2DAsfeFromExisting', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl2DAsfeFromExisting', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl2DAsfeFromExisting', ''))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskheight.setEnabled(False)
        self.lblmaskwidth.setText(_translate('TrainMl2DAsfeFromExisting', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl2DAsfeFromExisting', ''))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskwidth.setEnabled(False)
        self.lblpoolsize.setText(_translate('TrainMl2DAsfeFromExisting', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl2DAsfeFromExisting', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl2DAsfeFromExisting', ''))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl2DAsfeFromExisting', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl2DAsfeFromExisting', ''))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('TrainMl2DAsfeFromExisting', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl2DAsfeFromExisting', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl2DAsfeFromExisting', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl2DAsfeFromExisting', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl2DAsfeFromExisting', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl2DAsfeFromExisting', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl2DAsfeFromExisting', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfcdropout.setText(_translate('TrainMl2DAsfeFromExisting', 'MLP dropout rate:'))
        self.lblfcdropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtfcdropout.setText(_translate('TrainMl2DAsfeFromExisting', '0.5'))
        self.ldtfcdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl2DAsfeFromExisting', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl2DAsfeFromExisting', ''))
        self.btnsave.setText(_translate('TrainMl2DAsfeFromExisting', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl2DAsfeFromExisting', 'Train 2D-ASFE'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl2DAsfeFromExisting)

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

    def clickBtnTrainMl2DAsfeFromExisting--- This code section failed: ---

 L. 581         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 583         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 584        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 585        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 586        50  LOAD_STR                 'Train 2D-ASFE'

 L. 587        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 588        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 590        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_image_height_old'

 L. 591        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_image_width_old'

 L. 592        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtnewheight
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_image_height_new'

 L. 593       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewwidth
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_image_width_new'

 L. 594       126  LOAD_FAST                '_image_height_old'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'
              134  LOAD_FAST                '_image_width_old'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_TRUE    158  'to 158'

 L. 595       142  LOAD_FAST                '_image_height_new'
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

 L. 596       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 597       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 598       182  LOAD_STR                 'Train 2D-ASFE'

 L. 599       184  LOAD_STR                 'Non-integer feature size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 600       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 601       194  LOAD_FAST                '_image_height_old'
              196  LOAD_CONST               2
              198  COMPARE_OP               <
              200  POP_JUMP_IF_TRUE    228  'to 228'
              202  LOAD_FAST                '_image_width_old'
              204  LOAD_CONST               2
              206  COMPARE_OP               <
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 602       210  LOAD_FAST                '_image_height_new'
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

 L. 603       228  LOAD_GLOBAL              vis_msg
              230  LOAD_ATTR                print
              232  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 604       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 605       252  LOAD_STR                 'Train 2D-ASFE'

 L. 606       254  LOAD_STR                 'Features are not 2D'
              256  CALL_METHOD_3         3  '3 positional arguments'
              258  POP_TOP          

 L. 607       260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           224  '224'

 L. 609       264  LOAD_CONST               2
              266  LOAD_GLOBAL              int
              268  LOAD_FAST                '_image_height_old'
              270  LOAD_CONST               2
              272  BINARY_TRUE_DIVIDE
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  BINARY_MULTIPLY  
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  STORE_FAST               '_image_height_old'

 L. 610       284  LOAD_CONST               2
              286  LOAD_GLOBAL              int
              288  LOAD_FAST                '_image_width_old'
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BINARY_MULTIPLY  
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               '_image_width_old'

 L. 612       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                lwgfeature
              308  LOAD_METHOD              selectedItems
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               '_features'

 L. 613       314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainml2dasfefromexisting.clickBtnTrainMl2DAsfeFromExisting.<locals>.<listcomp>'
              318  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              320  LOAD_FAST                '_features'
              322  GET_ITER         
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               '_features'

 L. 614       328  LOAD_STR                 '_'
              330  LOAD_METHOD              join
              332  LOAD_FAST                '_features'
              334  CALL_METHOD_1         1  '1 positional argument'
              336  LOAD_STR                 '_rotated'
              338  BINARY_ADD       
              340  STORE_FAST               '_target'

 L. 616       342  LOAD_FAST                '_target'
              344  LOAD_FAST                '_features'
              346  COMPARE_OP               in
          348_350  POP_JUMP_IF_FALSE   388  'to 388'

 L. 617       352  LOAD_GLOBAL              vis_msg
              354  LOAD_ATTR                print
              356  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Target also used as features'
              358  LOAD_STR                 'error'
              360  LOAD_CONST               ('type',)
              362  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              364  POP_TOP          

 L. 618       366  LOAD_GLOBAL              QtWidgets
              368  LOAD_ATTR                QMessageBox
              370  LOAD_METHOD              critical
              372  LOAD_DEREF               'self'
              374  LOAD_ATTR                msgbox

 L. 619       376  LOAD_STR                 'Train 2D-ASFE'

 L. 620       378  LOAD_STR                 'Target also used as features'
              380  CALL_METHOD_3         3  '3 positional arguments'
              382  POP_TOP          

 L. 621       384  LOAD_CONST               None
              386  RETURN_VALUE     
            388_0  COME_FROM           348  '348'

 L. 623       388  LOAD_GLOBAL              len
              390  LOAD_DEREF               'self'
              392  LOAD_ATTR                ldtexisting
              394  LOAD_METHOD              text
              396  CALL_METHOD_0         0  '0 positional arguments'
              398  CALL_FUNCTION_1       1  '1 positional argument'
              400  LOAD_CONST               1
              402  COMPARE_OP               <
          404_406  POP_JUMP_IF_FALSE   444  'to 444'

 L. 624       408  LOAD_GLOBAL              vis_msg
              410  LOAD_ATTR                print
              412  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: No name specified for pre-trained network'

 L. 625       414  LOAD_STR                 'error'
              416  LOAD_CONST               ('type',)
              418  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              420  POP_TOP          

 L. 626       422  LOAD_GLOBAL              QtWidgets
              424  LOAD_ATTR                QMessageBox
              426  LOAD_METHOD              critical
              428  LOAD_DEREF               'self'
              430  LOAD_ATTR                msgbox

 L. 627       432  LOAD_STR                 'Train 2D-ASFE'

 L. 628       434  LOAD_STR                 'No name specified for pre-trained network'
              436  CALL_METHOD_3         3  '3 positional arguments'
              438  POP_TOP          

 L. 629       440  LOAD_CONST               None
              442  RETURN_VALUE     
            444_0  COME_FROM           404  '404'

 L. 630       444  LOAD_GLOBAL              os
              446  LOAD_ATTR                path
              448  LOAD_METHOD              dirname
              450  LOAD_DEREF               'self'
              452  LOAD_ATTR                ldtexisting
              454  LOAD_METHOD              text
              456  CALL_METHOD_0         0  '0 positional arguments'
              458  CALL_METHOD_1         1  '1 positional argument'
              460  STORE_FAST               '_precnnpath'

 L. 631       462  LOAD_GLOBAL              os
              464  LOAD_ATTR                path
              466  LOAD_METHOD              splitext
              468  LOAD_GLOBAL              os
              470  LOAD_ATTR                path
              472  LOAD_METHOD              basename
              474  LOAD_DEREF               'self'
              476  LOAD_ATTR                ldtexisting
              478  LOAD_METHOD              text
              480  CALL_METHOD_0         0  '0 positional arguments'
              482  CALL_METHOD_1         1  '1 positional argument'
              484  CALL_METHOD_1         1  '1 positional argument'
              486  LOAD_CONST               0
              488  BINARY_SUBSCR    
              490  STORE_FAST               '_precnnname'

 L. 632       492  LOAD_DEREF               'self'
              494  LOAD_ATTR                cbbblockid
              496  LOAD_METHOD              currentIndex
              498  CALL_METHOD_0         0  '0 positional arguments'
              500  STORE_FAST               '_blockidx'

 L. 633       502  LOAD_DEREF               'self'
              504  LOAD_ATTR                cbblayerid
              506  LOAD_METHOD              currentIndex
              508  CALL_METHOD_0         0  '0 positional arguments'
              510  STORE_FAST               '_layeridx'

 L. 634       512  LOAD_CONST               True
              514  STORE_FAST               '_trainable'

 L. 635       516  LOAD_DEREF               'self'
              518  LOAD_ATTR                cbbtrainable
              520  LOAD_METHOD              currentIndex
              522  CALL_METHOD_0         0  '0 positional arguments'
              524  LOAD_CONST               0
              526  COMPARE_OP               !=
          528_530  POP_JUMP_IF_FALSE   536  'to 536'

 L. 636       532  LOAD_CONST               False
              534  STORE_FAST               '_trainable'
            536_0  COME_FROM           528  '528'

 L. 638       536  LOAD_GLOBAL              ml_tfm
              538  LOAD_METHOD              getConvModelNChannel
              540  LOAD_FAST                '_precnnpath'
              542  LOAD_FAST                '_precnnname'
              544  CALL_METHOD_2         2  '2 positional arguments'
              546  LOAD_GLOBAL              len
              548  LOAD_FAST                '_features'
              550  CALL_FUNCTION_1       1  '1 positional argument'
              552  COMPARE_OP               !=
          554_556  POP_JUMP_IF_FALSE   594  'to 594'

 L. 639       558  LOAD_GLOBAL              vis_msg
              560  LOAD_ATTR                print
              562  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Feature channel number not match with pre-trained network'

 L. 640       564  LOAD_STR                 'error'
              566  LOAD_CONST               ('type',)
              568  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              570  POP_TOP          

 L. 641       572  LOAD_GLOBAL              QtWidgets
              574  LOAD_ATTR                QMessageBox
              576  LOAD_METHOD              critical
              578  LOAD_DEREF               'self'
              580  LOAD_ATTR                msgbox

 L. 642       582  LOAD_STR                 'Train 2D-ASFE'

 L. 643       584  LOAD_STR                 'Feature channel number not match with pre-trained network'
              586  CALL_METHOD_3         3  '3 positional arguments'
              588  POP_TOP          

 L. 644       590  LOAD_CONST               None
              592  RETURN_VALUE     
            594_0  COME_FROM           554  '554'

 L. 646       594  LOAD_GLOBAL              basic_data
              596  LOAD_METHOD              str2int
              598  LOAD_DEREF               'self'
              600  LOAD_ATTR                ldtnconvblock
              602  LOAD_METHOD              text
              604  CALL_METHOD_0         0  '0 positional arguments'
              606  CALL_METHOD_1         1  '1 positional argument'
              608  STORE_FAST               '_nconvblock'

 L. 647       610  LOAD_CLOSURE             'self'
              612  BUILD_TUPLE_1         1 
              614  LOAD_LISTCOMP            '<code_object <listcomp>>'
              616  LOAD_STR                 'trainml2dasfefromexisting.clickBtnTrainMl2DAsfeFromExisting.<locals>.<listcomp>'
              618  MAKE_FUNCTION_8          'closure'
              620  LOAD_GLOBAL              range
              622  LOAD_FAST                '_nconvblock'
              624  CALL_FUNCTION_1       1  '1 positional argument'
              626  GET_ITER         
              628  CALL_FUNCTION_1       1  '1 positional argument'
              630  STORE_FAST               '_nconvlayer'

 L. 648       632  LOAD_CLOSURE             'self'
              634  BUILD_TUPLE_1         1 
              636  LOAD_LISTCOMP            '<code_object <listcomp>>'
              638  LOAD_STR                 'trainml2dasfefromexisting.clickBtnTrainMl2DAsfeFromExisting.<locals>.<listcomp>'
              640  MAKE_FUNCTION_8          'closure'
              642  LOAD_GLOBAL              range
              644  LOAD_FAST                '_nconvblock'
              646  CALL_FUNCTION_1       1  '1 positional argument'
              648  GET_ITER         
              650  CALL_FUNCTION_1       1  '1 positional argument'
              652  STORE_FAST               '_nconvfeature'

 L. 649       654  LOAD_GLOBAL              basic_data
              656  LOAD_METHOD              str2int
              658  LOAD_DEREF               'self'
              660  LOAD_ATTR                ldtnfclayer
              662  LOAD_METHOD              text
              664  CALL_METHOD_0         0  '0 positional arguments'
              666  CALL_METHOD_1         1  '1 positional argument'
              668  STORE_FAST               '_nfclayer'

 L. 650       670  LOAD_CLOSURE             'self'
              672  BUILD_TUPLE_1         1 
              674  LOAD_LISTCOMP            '<code_object <listcomp>>'
              676  LOAD_STR                 'trainml2dasfefromexisting.clickBtnTrainMl2DAsfeFromExisting.<locals>.<listcomp>'
              678  MAKE_FUNCTION_8          'closure'
              680  LOAD_GLOBAL              range
              682  LOAD_FAST                '_nfclayer'
              684  CALL_FUNCTION_1       1  '1 positional argument'
              686  GET_ITER         
              688  CALL_FUNCTION_1       1  '1 positional argument'
              690  STORE_FAST               '_nfcneuron'

 L. 651       692  LOAD_GLOBAL              basic_data
              694  LOAD_METHOD              str2int
              696  LOAD_DEREF               'self'
              698  LOAD_ATTR                ldtmaskheight
              700  LOAD_METHOD              text
              702  CALL_METHOD_0         0  '0 positional arguments'
              704  CALL_METHOD_1         1  '1 positional argument'
              706  STORE_FAST               '_patch_height'

 L. 652       708  LOAD_GLOBAL              basic_data
              710  LOAD_METHOD              str2int
              712  LOAD_DEREF               'self'
              714  LOAD_ATTR                ldtmaskwidth
              716  LOAD_METHOD              text
              718  CALL_METHOD_0         0  '0 positional arguments'
              720  CALL_METHOD_1         1  '1 positional argument'
              722  STORE_FAST               '_patch_width'

 L. 653       724  LOAD_GLOBAL              basic_data
              726  LOAD_METHOD              str2int
              728  LOAD_DEREF               'self'
              730  LOAD_ATTR                ldtpoolheight
              732  LOAD_METHOD              text
              734  CALL_METHOD_0         0  '0 positional arguments'
              736  CALL_METHOD_1         1  '1 positional argument'
              738  STORE_FAST               '_pool_height'

 L. 654       740  LOAD_GLOBAL              basic_data
              742  LOAD_METHOD              str2int
              744  LOAD_DEREF               'self'
              746  LOAD_ATTR                ldtpoolwidth
              748  LOAD_METHOD              text
              750  CALL_METHOD_0         0  '0 positional arguments'
              752  CALL_METHOD_1         1  '1 positional argument'
              754  STORE_FAST               '_pool_width'

 L. 655       756  LOAD_GLOBAL              basic_data
              758  LOAD_METHOD              str2int
              760  LOAD_DEREF               'self'
              762  LOAD_ATTR                ldtnepoch
              764  LOAD_METHOD              text
              766  CALL_METHOD_0         0  '0 positional arguments'
              768  CALL_METHOD_1         1  '1 positional argument'
              770  STORE_FAST               '_nepoch'

 L. 656       772  LOAD_GLOBAL              basic_data
              774  LOAD_METHOD              str2int
              776  LOAD_DEREF               'self'
              778  LOAD_ATTR                ldtbatchsize
              780  LOAD_METHOD              text
              782  CALL_METHOD_0         0  '0 positional arguments'
              784  CALL_METHOD_1         1  '1 positional argument'
              786  STORE_FAST               '_batchsize'

 L. 657       788  LOAD_GLOBAL              basic_data
              790  LOAD_METHOD              str2float
              792  LOAD_DEREF               'self'
              794  LOAD_ATTR                ldtlearnrate
              796  LOAD_METHOD              text
              798  CALL_METHOD_0         0  '0 positional arguments'
              800  CALL_METHOD_1         1  '1 positional argument'
              802  STORE_FAST               '_learning_rate'

 L. 658       804  LOAD_GLOBAL              basic_data
              806  LOAD_METHOD              str2float
              808  LOAD_DEREF               'self'
              810  LOAD_ATTR                ldtfcdropout
              812  LOAD_METHOD              text
              814  CALL_METHOD_0         0  '0 positional arguments'
              816  CALL_METHOD_1         1  '1 positional argument'
              818  STORE_FAST               '_dropout_prob_fclayer'

 L. 659       820  LOAD_FAST                '_nconvblock'
              822  LOAD_CONST               False
              824  COMPARE_OP               is
          826_828  POP_JUMP_IF_TRUE    840  'to 840'
              830  LOAD_FAST                '_nconvblock'
              832  LOAD_CONST               0
              834  COMPARE_OP               <=
          836_838  POP_JUMP_IF_FALSE   876  'to 876'
            840_0  COME_FROM           826  '826'

 L. 660       840  LOAD_GLOBAL              vis_msg
              842  LOAD_ATTR                print
              844  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Non-positive convolutional block number'

 L. 661       846  LOAD_STR                 'error'
              848  LOAD_CONST               ('type',)
              850  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              852  POP_TOP          

 L. 662       854  LOAD_GLOBAL              QtWidgets
              856  LOAD_ATTR                QMessageBox
              858  LOAD_METHOD              critical
              860  LOAD_DEREF               'self'
              862  LOAD_ATTR                msgbox

 L. 663       864  LOAD_STR                 'Train 2D-ASFE'

 L. 664       866  LOAD_STR                 'Non-positive convolutional block number'
              868  CALL_METHOD_3         3  '3 positional arguments'
              870  POP_TOP          

 L. 665       872  LOAD_CONST               None
              874  RETURN_VALUE     
            876_0  COME_FROM           836  '836'

 L. 666       876  SETUP_LOOP          948  'to 948'
              878  LOAD_FAST                '_nconvlayer'
              880  GET_ITER         
            882_0  COME_FROM           902  '902'
              882  FOR_ITER            946  'to 946'
              884  STORE_FAST               '_i'

 L. 667       886  LOAD_FAST                '_i'
              888  LOAD_CONST               False
              890  COMPARE_OP               is
          892_894  POP_JUMP_IF_TRUE    906  'to 906'
              896  LOAD_FAST                '_i'
              898  LOAD_CONST               1
              900  COMPARE_OP               <
          902_904  POP_JUMP_IF_FALSE   882  'to 882'
            906_0  COME_FROM           892  '892'

 L. 668       906  LOAD_GLOBAL              vis_msg
              908  LOAD_ATTR                print
              910  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Non-positive convolutional layer number'

 L. 669       912  LOAD_STR                 'error'
              914  LOAD_CONST               ('type',)
              916  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              918  POP_TOP          

 L. 670       920  LOAD_GLOBAL              QtWidgets
              922  LOAD_ATTR                QMessageBox
              924  LOAD_METHOD              critical
              926  LOAD_DEREF               'self'
              928  LOAD_ATTR                msgbox

 L. 671       930  LOAD_STR                 'Train 2D-ASFE'

 L. 672       932  LOAD_STR                 'Non-positive convolutional layer number'
              934  CALL_METHOD_3         3  '3 positional arguments'
              936  POP_TOP          

 L. 673       938  LOAD_CONST               None
              940  RETURN_VALUE     
          942_944  JUMP_BACK           882  'to 882'
              946  POP_BLOCK        
            948_0  COME_FROM_LOOP      876  '876'

 L. 674       948  SETUP_LOOP         1020  'to 1020'
              950  LOAD_FAST                '_nconvfeature'
              952  GET_ITER         
            954_0  COME_FROM           974  '974'
              954  FOR_ITER           1018  'to 1018'
              956  STORE_FAST               '_i'

 L. 675       958  LOAD_FAST                '_i'
              960  LOAD_CONST               False
              962  COMPARE_OP               is
          964_966  POP_JUMP_IF_TRUE    978  'to 978'
              968  LOAD_FAST                '_i'
              970  LOAD_CONST               1
              972  COMPARE_OP               <
          974_976  POP_JUMP_IF_FALSE   954  'to 954'
            978_0  COME_FROM           964  '964'

 L. 676       978  LOAD_GLOBAL              vis_msg
              980  LOAD_ATTR                print
              982  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Non-positive convolutional feature number'

 L. 677       984  LOAD_STR                 'error'
              986  LOAD_CONST               ('type',)
              988  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              990  POP_TOP          

 L. 678       992  LOAD_GLOBAL              QtWidgets
              994  LOAD_ATTR                QMessageBox
              996  LOAD_METHOD              critical
              998  LOAD_DEREF               'self'
             1000  LOAD_ATTR                msgbox

 L. 679      1002  LOAD_STR                 'Train 2D-ASFE'

 L. 680      1004  LOAD_STR                 'Non-positive convolutional feature number'
             1006  CALL_METHOD_3         3  '3 positional arguments'
             1008  POP_TOP          

 L. 681      1010  LOAD_CONST               None
             1012  RETURN_VALUE     
         1014_1016  JUMP_BACK           954  'to 954'
             1018  POP_BLOCK        
           1020_0  COME_FROM_LOOP      948  '948'

 L. 682      1020  LOAD_FAST                '_nfclayer'
             1022  LOAD_CONST               False
             1024  COMPARE_OP               is
         1026_1028  POP_JUMP_IF_TRUE   1040  'to 1040'
             1030  LOAD_FAST                '_nfclayer'
             1032  LOAD_CONST               0
             1034  COMPARE_OP               <=
         1036_1038  POP_JUMP_IF_FALSE  1076  'to 1076'
           1040_0  COME_FROM          1026  '1026'

 L. 683      1040  LOAD_GLOBAL              vis_msg
             1042  LOAD_ATTR                print
             1044  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Non-positive MLP layer number'
             1046  LOAD_STR                 'error'
             1048  LOAD_CONST               ('type',)
             1050  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1052  POP_TOP          

 L. 684      1054  LOAD_GLOBAL              QtWidgets
             1056  LOAD_ATTR                QMessageBox
             1058  LOAD_METHOD              critical
             1060  LOAD_DEREF               'self'
             1062  LOAD_ATTR                msgbox

 L. 685      1064  LOAD_STR                 'Train 2D-ASFE'

 L. 686      1066  LOAD_STR                 'Non-positive MLP layer number'
             1068  CALL_METHOD_3         3  '3 positional arguments'
             1070  POP_TOP          

 L. 687      1072  LOAD_CONST               None
             1074  RETURN_VALUE     
           1076_0  COME_FROM          1036  '1036'

 L. 688      1076  SETUP_LOOP         1148  'to 1148'
             1078  LOAD_FAST                '_nfcneuron'
             1080  GET_ITER         
           1082_0  COME_FROM          1102  '1102'
             1082  FOR_ITER           1146  'to 1146'
             1084  STORE_FAST               '_i'

 L. 689      1086  LOAD_FAST                '_i'
             1088  LOAD_CONST               False
             1090  COMPARE_OP               is
         1092_1094  POP_JUMP_IF_TRUE   1106  'to 1106'
             1096  LOAD_FAST                '_i'
             1098  LOAD_CONST               1
             1100  COMPARE_OP               <
         1102_1104  POP_JUMP_IF_FALSE  1082  'to 1082'
           1106_0  COME_FROM          1092  '1092'

 L. 690      1106  LOAD_GLOBAL              vis_msg
             1108  LOAD_ATTR                print
             1110  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Non-positive MLP neuron number'
             1112  LOAD_STR                 'error'
             1114  LOAD_CONST               ('type',)
             1116  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1118  POP_TOP          

 L. 691      1120  LOAD_GLOBAL              QtWidgets
             1122  LOAD_ATTR                QMessageBox
             1124  LOAD_METHOD              critical
             1126  LOAD_DEREF               'self'
             1128  LOAD_ATTR                msgbox

 L. 692      1130  LOAD_STR                 'Train 2D-ASFE'

 L. 693      1132  LOAD_STR                 'Non-positive MLP neuron number'
             1134  CALL_METHOD_3         3  '3 positional arguments'
             1136  POP_TOP          

 L. 694      1138  LOAD_CONST               None
             1140  RETURN_VALUE     
         1142_1144  JUMP_BACK          1082  'to 1082'
             1146  POP_BLOCK        
           1148_0  COME_FROM_LOOP     1076  '1076'

 L. 695      1148  LOAD_FAST                '_patch_height'
             1150  LOAD_CONST               False
             1152  COMPARE_OP               is
         1154_1156  POP_JUMP_IF_TRUE   1188  'to 1188'
             1158  LOAD_FAST                '_patch_width'
             1160  LOAD_CONST               False
             1162  COMPARE_OP               is
         1164_1166  POP_JUMP_IF_TRUE   1188  'to 1188'

 L. 696      1168  LOAD_FAST                '_patch_height'
             1170  LOAD_CONST               1
             1172  COMPARE_OP               <
         1174_1176  POP_JUMP_IF_TRUE   1188  'to 1188'
             1178  LOAD_FAST                '_patch_width'
             1180  LOAD_CONST               1
             1182  COMPARE_OP               <
         1184_1186  POP_JUMP_IF_FALSE  1224  'to 1224'
           1188_0  COME_FROM          1174  '1174'
           1188_1  COME_FROM          1164  '1164'
           1188_2  COME_FROM          1154  '1154'

 L. 697      1188  LOAD_GLOBAL              vis_msg
             1190  LOAD_ATTR                print
             1192  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Non-positive convolutional patch size'

 L. 698      1194  LOAD_STR                 'error'
             1196  LOAD_CONST               ('type',)
             1198  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1200  POP_TOP          

 L. 699      1202  LOAD_GLOBAL              QtWidgets
             1204  LOAD_ATTR                QMessageBox
             1206  LOAD_METHOD              critical
             1208  LOAD_DEREF               'self'
             1210  LOAD_ATTR                msgbox

 L. 700      1212  LOAD_STR                 'Train 2D-ASFE'

 L. 701      1214  LOAD_STR                 'Non-positive convolutional patch size'
             1216  CALL_METHOD_3         3  '3 positional arguments'
             1218  POP_TOP          

 L. 702      1220  LOAD_CONST               None
             1222  RETURN_VALUE     
           1224_0  COME_FROM          1184  '1184'

 L. 703      1224  LOAD_FAST                '_pool_height'
             1226  LOAD_CONST               False
             1228  COMPARE_OP               is
         1230_1232  POP_JUMP_IF_TRUE   1264  'to 1264'
             1234  LOAD_FAST                '_pool_width'
             1236  LOAD_CONST               False
             1238  COMPARE_OP               is
         1240_1242  POP_JUMP_IF_TRUE   1264  'to 1264'

 L. 704      1244  LOAD_FAST                '_pool_height'
             1246  LOAD_CONST               1
             1248  COMPARE_OP               <
         1250_1252  POP_JUMP_IF_TRUE   1264  'to 1264'
             1254  LOAD_FAST                '_pool_width'
             1256  LOAD_CONST               1
             1258  COMPARE_OP               <
         1260_1262  POP_JUMP_IF_FALSE  1300  'to 1300'
           1264_0  COME_FROM          1250  '1250'
           1264_1  COME_FROM          1240  '1240'
           1264_2  COME_FROM          1230  '1230'

 L. 705      1264  LOAD_GLOBAL              vis_msg
             1266  LOAD_ATTR                print
             1268  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Non-positive pooling size'
             1270  LOAD_STR                 'error'
             1272  LOAD_CONST               ('type',)
             1274  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1276  POP_TOP          

 L. 706      1278  LOAD_GLOBAL              QtWidgets
             1280  LOAD_ATTR                QMessageBox
             1282  LOAD_METHOD              critical
             1284  LOAD_DEREF               'self'
             1286  LOAD_ATTR                msgbox

 L. 707      1288  LOAD_STR                 'Train 2D-ASFE'

 L. 708      1290  LOAD_STR                 'Non-positive pooling size'
             1292  CALL_METHOD_3         3  '3 positional arguments'
             1294  POP_TOP          

 L. 709      1296  LOAD_CONST               None
             1298  RETURN_VALUE     
           1300_0  COME_FROM          1260  '1260'

 L. 710      1300  LOAD_FAST                '_nepoch'
             1302  LOAD_CONST               False
             1304  COMPARE_OP               is
         1306_1308  POP_JUMP_IF_TRUE   1320  'to 1320'
             1310  LOAD_FAST                '_nepoch'
             1312  LOAD_CONST               0
             1314  COMPARE_OP               <=
         1316_1318  POP_JUMP_IF_FALSE  1356  'to 1356'
           1320_0  COME_FROM          1306  '1306'

 L. 711      1320  LOAD_GLOBAL              vis_msg
             1322  LOAD_ATTR                print
             1324  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Non-positive epoch number'
             1326  LOAD_STR                 'error'
             1328  LOAD_CONST               ('type',)
             1330  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1332  POP_TOP          

 L. 712      1334  LOAD_GLOBAL              QtWidgets
             1336  LOAD_ATTR                QMessageBox
             1338  LOAD_METHOD              critical
             1340  LOAD_DEREF               'self'
             1342  LOAD_ATTR                msgbox

 L. 713      1344  LOAD_STR                 'Train 2D-ASFE'

 L. 714      1346  LOAD_STR                 'Non-positive epoch number'
             1348  CALL_METHOD_3         3  '3 positional arguments'
             1350  POP_TOP          

 L. 715      1352  LOAD_CONST               None
             1354  RETURN_VALUE     
           1356_0  COME_FROM          1316  '1316'

 L. 716      1356  LOAD_FAST                '_batchsize'
             1358  LOAD_CONST               False
             1360  COMPARE_OP               is
         1362_1364  POP_JUMP_IF_TRUE   1376  'to 1376'
             1366  LOAD_FAST                '_batchsize'
             1368  LOAD_CONST               0
             1370  COMPARE_OP               <=
         1372_1374  POP_JUMP_IF_FALSE  1412  'to 1412'
           1376_0  COME_FROM          1362  '1362'

 L. 717      1376  LOAD_GLOBAL              vis_msg
             1378  LOAD_ATTR                print
             1380  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Non-positive batch size'
             1382  LOAD_STR                 'error'
             1384  LOAD_CONST               ('type',)
             1386  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1388  POP_TOP          

 L. 718      1390  LOAD_GLOBAL              QtWidgets
             1392  LOAD_ATTR                QMessageBox
             1394  LOAD_METHOD              critical
             1396  LOAD_DEREF               'self'
             1398  LOAD_ATTR                msgbox

 L. 719      1400  LOAD_STR                 'Train 2D-ASFE'

 L. 720      1402  LOAD_STR                 'Non-positive batch size'
             1404  CALL_METHOD_3         3  '3 positional arguments'
             1406  POP_TOP          

 L. 721      1408  LOAD_CONST               None
             1410  RETURN_VALUE     
           1412_0  COME_FROM          1372  '1372'

 L. 722      1412  LOAD_FAST                '_learning_rate'
             1414  LOAD_CONST               False
             1416  COMPARE_OP               is
         1418_1420  POP_JUMP_IF_TRUE   1432  'to 1432'
             1422  LOAD_FAST                '_learning_rate'
             1424  LOAD_CONST               0
             1426  COMPARE_OP               <=
         1428_1430  POP_JUMP_IF_FALSE  1468  'to 1468'
           1432_0  COME_FROM          1418  '1418'

 L. 723      1432  LOAD_GLOBAL              vis_msg
             1434  LOAD_ATTR                print
             1436  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Non-positive learning rate'
             1438  LOAD_STR                 'error'
             1440  LOAD_CONST               ('type',)
             1442  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1444  POP_TOP          

 L. 724      1446  LOAD_GLOBAL              QtWidgets
             1448  LOAD_ATTR                QMessageBox
             1450  LOAD_METHOD              critical
             1452  LOAD_DEREF               'self'
             1454  LOAD_ATTR                msgbox

 L. 725      1456  LOAD_STR                 'Train 2D-ASFE'

 L. 726      1458  LOAD_STR                 'Non-positive learning rate'
             1460  CALL_METHOD_3         3  '3 positional arguments'
             1462  POP_TOP          

 L. 727      1464  LOAD_CONST               None
             1466  RETURN_VALUE     
           1468_0  COME_FROM          1428  '1428'

 L. 728      1468  LOAD_FAST                '_dropout_prob_fclayer'
             1470  LOAD_CONST               False
             1472  COMPARE_OP               is
         1474_1476  POP_JUMP_IF_TRUE   1488  'to 1488'
             1478  LOAD_FAST                '_dropout_prob_fclayer'
             1480  LOAD_CONST               0
             1482  COMPARE_OP               <=
         1484_1486  POP_JUMP_IF_FALSE  1524  'to 1524'
           1488_0  COME_FROM          1474  '1474'

 L. 729      1488  LOAD_GLOBAL              vis_msg
             1490  LOAD_ATTR                print
             1492  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: Negative dropout rate'
             1494  LOAD_STR                 'error'
             1496  LOAD_CONST               ('type',)
             1498  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1500  POP_TOP          

 L. 730      1502  LOAD_GLOBAL              QtWidgets
             1504  LOAD_ATTR                QMessageBox
             1506  LOAD_METHOD              critical
             1508  LOAD_DEREF               'self'
             1510  LOAD_ATTR                msgbox

 L. 731      1512  LOAD_STR                 'Train 2D-ASFE'

 L. 732      1514  LOAD_STR                 'Negative dropout rate'
             1516  CALL_METHOD_3         3  '3 positional arguments'
             1518  POP_TOP          

 L. 733      1520  LOAD_CONST               None
             1522  RETURN_VALUE     
           1524_0  COME_FROM          1484  '1484'

 L. 735      1524  LOAD_GLOBAL              len
             1526  LOAD_DEREF               'self'
             1528  LOAD_ATTR                ldtexisting
             1530  LOAD_METHOD              text
             1532  CALL_METHOD_0         0  '0 positional arguments'
             1534  CALL_FUNCTION_1       1  '1 positional argument'
             1536  LOAD_CONST               1
             1538  COMPARE_OP               <
         1540_1542  POP_JUMP_IF_FALSE  1580  'to 1580'

 L. 736      1544  LOAD_GLOBAL              vis_msg
             1546  LOAD_ATTR                print
             1548  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: No pre-trained network specified'
             1550  LOAD_STR                 'error'
             1552  LOAD_CONST               ('type',)
             1554  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1556  POP_TOP          

 L. 737      1558  LOAD_GLOBAL              QtWidgets
             1560  LOAD_ATTR                QMessageBox
             1562  LOAD_METHOD              critical
             1564  LOAD_DEREF               'self'
             1566  LOAD_ATTR                msgbox

 L. 738      1568  LOAD_STR                 'Train 2D-DASFE'

 L. 739      1570  LOAD_STR                 'No pre-trained network specified'
             1572  CALL_METHOD_3         3  '3 positional arguments'
             1574  POP_TOP          

 L. 740      1576  LOAD_CONST               None
             1578  RETURN_VALUE     
           1580_0  COME_FROM          1540  '1540'

 L. 741      1580  LOAD_GLOBAL              len
             1582  LOAD_DEREF               'self'
             1584  LOAD_ATTR                ldtsave
             1586  LOAD_METHOD              text
             1588  CALL_METHOD_0         0  '0 positional arguments'
             1590  CALL_FUNCTION_1       1  '1 positional argument'
             1592  LOAD_CONST               1
             1594  COMPARE_OP               <
         1596_1598  POP_JUMP_IF_FALSE  1636  'to 1636'

 L. 742      1600  LOAD_GLOBAL              vis_msg
             1602  LOAD_ATTR                print
             1604  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: No name specified for ASFE network'
             1606  LOAD_STR                 'error'
             1608  LOAD_CONST               ('type',)
             1610  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1612  POP_TOP          

 L. 743      1614  LOAD_GLOBAL              QtWidgets
             1616  LOAD_ATTR                QMessageBox
             1618  LOAD_METHOD              critical
             1620  LOAD_DEREF               'self'
             1622  LOAD_ATTR                msgbox

 L. 744      1624  LOAD_STR                 'Train 2D-ASFE'

 L. 745      1626  LOAD_STR                 'No name specified for ASFE network'
             1628  CALL_METHOD_3         3  '3 positional arguments'
             1630  POP_TOP          

 L. 746      1632  LOAD_CONST               None
             1634  RETURN_VALUE     
           1636_0  COME_FROM          1596  '1596'

 L. 747      1636  LOAD_GLOBAL              os
             1638  LOAD_ATTR                path
             1640  LOAD_METHOD              dirname
             1642  LOAD_DEREF               'self'
             1644  LOAD_ATTR                ldtsave
             1646  LOAD_METHOD              text
             1648  CALL_METHOD_0         0  '0 positional arguments'
             1650  CALL_METHOD_1         1  '1 positional argument'
             1652  STORE_FAST               '_savepath'

 L. 748      1654  LOAD_GLOBAL              os
             1656  LOAD_ATTR                path
             1658  LOAD_METHOD              splitext
             1660  LOAD_GLOBAL              os
             1662  LOAD_ATTR                path
             1664  LOAD_METHOD              basename
             1666  LOAD_DEREF               'self'
             1668  LOAD_ATTR                ldtsave
             1670  LOAD_METHOD              text
             1672  CALL_METHOD_0         0  '0 positional arguments'
             1674  CALL_METHOD_1         1  '1 positional argument'
             1676  CALL_METHOD_1         1  '1 positional argument'
             1678  LOAD_CONST               0
             1680  BINARY_SUBSCR    
             1682  STORE_FAST               '_savename'

 L. 750      1684  LOAD_CONST               0
             1686  STORE_FAST               '_wdinl'

 L. 751      1688  LOAD_CONST               0
             1690  STORE_FAST               '_wdxl'

 L. 752      1692  LOAD_CONST               0
             1694  STORE_FAST               '_wdz'

 L. 753      1696  LOAD_DEREF               'self'
             1698  LOAD_ATTR                cbbornt
             1700  LOAD_METHOD              currentIndex
             1702  CALL_METHOD_0         0  '0 positional arguments'
             1704  LOAD_CONST               0
             1706  COMPARE_OP               ==
         1708_1710  POP_JUMP_IF_FALSE  1736  'to 1736'

 L. 754      1712  LOAD_GLOBAL              int
             1714  LOAD_FAST                '_image_width_old'
             1716  LOAD_CONST               2
             1718  BINARY_TRUE_DIVIDE
             1720  CALL_FUNCTION_1       1  '1 positional argument'
             1722  STORE_FAST               '_wdxl'

 L. 755      1724  LOAD_GLOBAL              int
             1726  LOAD_FAST                '_image_height_old'
             1728  LOAD_CONST               2
             1730  BINARY_TRUE_DIVIDE
             1732  CALL_FUNCTION_1       1  '1 positional argument'
             1734  STORE_FAST               '_wdz'
           1736_0  COME_FROM          1708  '1708'

 L. 756      1736  LOAD_DEREF               'self'
             1738  LOAD_ATTR                cbbornt
             1740  LOAD_METHOD              currentIndex
             1742  CALL_METHOD_0         0  '0 positional arguments'
             1744  LOAD_CONST               1
             1746  COMPARE_OP               ==
         1748_1750  POP_JUMP_IF_FALSE  1776  'to 1776'

 L. 757      1752  LOAD_GLOBAL              int
             1754  LOAD_FAST                '_image_width_old'
             1756  LOAD_CONST               2
             1758  BINARY_TRUE_DIVIDE
             1760  CALL_FUNCTION_1       1  '1 positional argument'
             1762  STORE_FAST               '_wdinl'

 L. 758      1764  LOAD_GLOBAL              int
             1766  LOAD_FAST                '_image_height_old'
             1768  LOAD_CONST               2
             1770  BINARY_TRUE_DIVIDE
             1772  CALL_FUNCTION_1       1  '1 positional argument'
             1774  STORE_FAST               '_wdz'
           1776_0  COME_FROM          1748  '1748'

 L. 759      1776  LOAD_DEREF               'self'
             1778  LOAD_ATTR                cbbornt
             1780  LOAD_METHOD              currentIndex
             1782  CALL_METHOD_0         0  '0 positional arguments'
             1784  LOAD_CONST               2
             1786  COMPARE_OP               ==
         1788_1790  POP_JUMP_IF_FALSE  1816  'to 1816'

 L. 760      1792  LOAD_GLOBAL              int
             1794  LOAD_FAST                '_image_width_old'
             1796  LOAD_CONST               2
             1798  BINARY_TRUE_DIVIDE
             1800  CALL_FUNCTION_1       1  '1 positional argument'
             1802  STORE_FAST               '_wdinl'

 L. 761      1804  LOAD_GLOBAL              int
             1806  LOAD_FAST                '_image_height_old'
             1808  LOAD_CONST               2
             1810  BINARY_TRUE_DIVIDE
             1812  CALL_FUNCTION_1       1  '1 positional argument'
             1814  STORE_FAST               '_wdxl'
           1816_0  COME_FROM          1788  '1788'

 L. 763      1816  LOAD_DEREF               'self'
             1818  LOAD_ATTR                survinfo
             1820  STORE_FAST               '_seisinfo'

 L. 765      1822  LOAD_GLOBAL              print
             1824  LOAD_STR                 'TrainMl2DAsfeFromExisting: Step 1 - Get training samples:'
             1826  CALL_FUNCTION_1       1  '1 positional argument'
             1828  POP_TOP          

 L. 766      1830  LOAD_DEREF               'self'
             1832  LOAD_ATTR                traindataconfig
             1834  LOAD_STR                 'TrainPointSet'
             1836  BINARY_SUBSCR    
             1838  STORE_FAST               '_trainpoint'

 L. 767      1840  LOAD_GLOBAL              np
             1842  LOAD_METHOD              zeros
             1844  LOAD_CONST               0
             1846  LOAD_CONST               3
             1848  BUILD_LIST_2          2 
             1850  CALL_METHOD_1         1  '1 positional argument'
             1852  STORE_FAST               '_traindata'

 L. 768      1854  SETUP_LOOP         1930  'to 1930'
             1856  LOAD_FAST                '_trainpoint'
             1858  GET_ITER         
           1860_0  COME_FROM          1878  '1878'
             1860  FOR_ITER           1928  'to 1928'
             1862  STORE_FAST               '_p'

 L. 769      1864  LOAD_GLOBAL              point_ays
             1866  LOAD_METHOD              checkPoint
             1868  LOAD_DEREF               'self'
             1870  LOAD_ATTR                pointsetdata
             1872  LOAD_FAST                '_p'
             1874  BINARY_SUBSCR    
             1876  CALL_METHOD_1         1  '1 positional argument'
         1878_1880  POP_JUMP_IF_FALSE  1860  'to 1860'

 L. 770      1882  LOAD_GLOBAL              basic_mdt
             1884  LOAD_METHOD              exportMatDict
             1886  LOAD_DEREF               'self'
             1888  LOAD_ATTR                pointsetdata
             1890  LOAD_FAST                '_p'
             1892  BINARY_SUBSCR    
             1894  LOAD_STR                 'Inline'
             1896  LOAD_STR                 'Crossline'
             1898  LOAD_STR                 'Z'
             1900  BUILD_LIST_3          3 
             1902  CALL_METHOD_2         2  '2 positional arguments'
             1904  STORE_FAST               '_pt'

 L. 771      1906  LOAD_GLOBAL              np
             1908  LOAD_ATTR                concatenate
             1910  LOAD_FAST                '_traindata'
             1912  LOAD_FAST                '_pt'
             1914  BUILD_TUPLE_2         2 
             1916  LOAD_CONST               0
             1918  LOAD_CONST               ('axis',)
             1920  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1922  STORE_FAST               '_traindata'
         1924_1926  JUMP_BACK          1860  'to 1860'
             1928  POP_BLOCK        
           1930_0  COME_FROM_LOOP     1854  '1854'

 L. 772      1930  LOAD_GLOBAL              seis_ays
             1932  LOAD_ATTR                removeOutofSurveySample
             1934  LOAD_FAST                '_traindata'

 L. 773      1936  LOAD_FAST                '_seisinfo'
             1938  LOAD_STR                 'ILStart'
             1940  BINARY_SUBSCR    
             1942  LOAD_FAST                '_wdinl'
             1944  LOAD_FAST                '_seisinfo'
             1946  LOAD_STR                 'ILStep'
             1948  BINARY_SUBSCR    
             1950  BINARY_MULTIPLY  
             1952  BINARY_ADD       

 L. 774      1954  LOAD_FAST                '_seisinfo'
             1956  LOAD_STR                 'ILEnd'
             1958  BINARY_SUBSCR    
             1960  LOAD_FAST                '_wdinl'
             1962  LOAD_FAST                '_seisinfo'
             1964  LOAD_STR                 'ILStep'
             1966  BINARY_SUBSCR    
             1968  BINARY_MULTIPLY  
             1970  BINARY_SUBTRACT  

 L. 775      1972  LOAD_FAST                '_seisinfo'
             1974  LOAD_STR                 'XLStart'
             1976  BINARY_SUBSCR    
             1978  LOAD_FAST                '_wdxl'
             1980  LOAD_FAST                '_seisinfo'
             1982  LOAD_STR                 'XLStep'
             1984  BINARY_SUBSCR    
             1986  BINARY_MULTIPLY  
             1988  BINARY_ADD       

 L. 776      1990  LOAD_FAST                '_seisinfo'
             1992  LOAD_STR                 'XLEnd'
             1994  BINARY_SUBSCR    
             1996  LOAD_FAST                '_wdxl'
             1998  LOAD_FAST                '_seisinfo'
             2000  LOAD_STR                 'XLStep'
             2002  BINARY_SUBSCR    
             2004  BINARY_MULTIPLY  
             2006  BINARY_SUBTRACT  

 L. 777      2008  LOAD_FAST                '_seisinfo'
             2010  LOAD_STR                 'ZStart'
             2012  BINARY_SUBSCR    
             2014  LOAD_FAST                '_wdz'
             2016  LOAD_FAST                '_seisinfo'
             2018  LOAD_STR                 'ZStep'
             2020  BINARY_SUBSCR    
             2022  BINARY_MULTIPLY  
             2024  BINARY_ADD       

 L. 778      2026  LOAD_FAST                '_seisinfo'
             2028  LOAD_STR                 'ZEnd'
             2030  BINARY_SUBSCR    
             2032  LOAD_FAST                '_wdz'
             2034  LOAD_FAST                '_seisinfo'
             2036  LOAD_STR                 'ZStep'
             2038  BINARY_SUBSCR    
             2040  BINARY_MULTIPLY  
             2042  BINARY_SUBTRACT  
             2044  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             2046  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2048  STORE_FAST               '_traindata'

 L. 781      2050  LOAD_GLOBAL              np
             2052  LOAD_METHOD              shape
             2054  LOAD_FAST                '_traindata'
             2056  CALL_METHOD_1         1  '1 positional argument'
             2058  LOAD_CONST               0
             2060  BINARY_SUBSCR    
             2062  LOAD_CONST               0
             2064  COMPARE_OP               <=
         2066_2068  POP_JUMP_IF_FALSE  2106  'to 2106'

 L. 782      2070  LOAD_GLOBAL              vis_msg
             2072  LOAD_ATTR                print
             2074  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: No training sample found'
             2076  LOAD_STR                 'error'
             2078  LOAD_CONST               ('type',)
             2080  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2082  POP_TOP          

 L. 783      2084  LOAD_GLOBAL              QtWidgets
             2086  LOAD_ATTR                QMessageBox
             2088  LOAD_METHOD              critical
             2090  LOAD_DEREF               'self'
             2092  LOAD_ATTR                msgbox

 L. 784      2094  LOAD_STR                 'Train 2D-ASFE'

 L. 785      2096  LOAD_STR                 'No training sample found'
             2098  CALL_METHOD_3         3  '3 positional arguments'
             2100  POP_TOP          

 L. 786      2102  LOAD_CONST               None
             2104  RETURN_VALUE     
           2106_0  COME_FROM          2066  '2066'

 L. 789      2106  LOAD_GLOBAL              print
             2108  LOAD_STR                 'TrainMl2DAsfeFromExisting: Step 2 - Retrieve and interpolate images: (%d, %d) --> (%d, %d)'

 L. 790      2110  LOAD_FAST                '_image_height_old'
             2112  LOAD_FAST                '_image_width_old'
             2114  LOAD_FAST                '_image_height_new'
             2116  LOAD_FAST                '_image_width_new'
             2118  BUILD_TUPLE_4         4 
             2120  BINARY_MODULO    
             2122  CALL_FUNCTION_1       1  '1 positional argument'
             2124  POP_TOP          

 L. 791      2126  BUILD_MAP_0           0 
             2128  STORE_FAST               '_traindict'

 L. 792      2130  SETUP_LOOP         2202  'to 2202'
             2132  LOAD_FAST                '_features'
             2134  GET_ITER         
             2136  FOR_ITER           2200  'to 2200'
             2138  STORE_FAST               'f'

 L. 793      2140  LOAD_DEREF               'self'
             2142  LOAD_ATTR                seisdata
             2144  LOAD_FAST                'f'
             2146  BINARY_SUBSCR    
             2148  STORE_FAST               '_seisdata'

 L. 794      2150  LOAD_GLOBAL              seis_ays
             2152  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2154  LOAD_FAST                '_seisdata'
             2156  LOAD_FAST                '_traindata'
             2158  LOAD_DEREF               'self'
             2160  LOAD_ATTR                survinfo

 L. 795      2162  LOAD_FAST                '_wdinl'
             2164  LOAD_FAST                '_wdxl'
             2166  LOAD_FAST                '_wdz'

 L. 796      2168  LOAD_CONST               False
             2170  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2172  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2174  LOAD_CONST               None
             2176  LOAD_CONST               None
             2178  BUILD_SLICE_2         2 
             2180  LOAD_CONST               3
             2182  LOAD_CONST               None
             2184  BUILD_SLICE_2         2 
             2186  BUILD_TUPLE_2         2 
             2188  BINARY_SUBSCR    
             2190  LOAD_FAST                '_traindict'
             2192  LOAD_FAST                'f'
             2194  STORE_SUBSCR     
         2196_2198  JUMP_BACK          2136  'to 2136'
             2200  POP_BLOCK        
           2202_0  COME_FROM_LOOP     2130  '2130'

 L. 798      2202  LOAD_DEREF               'self'
             2204  LOAD_ATTR                traindataconfig
             2206  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2208  BINARY_SUBSCR    
         2210_2212  POP_JUMP_IF_FALSE  2294  'to 2294'

 L. 799      2214  SETUP_LOOP         2294  'to 2294'
             2216  LOAD_FAST                '_features'
             2218  GET_ITER         
           2220_0  COME_FROM          2248  '2248'
             2220  FOR_ITER           2292  'to 2292'
             2222  STORE_FAST               'f'

 L. 800      2224  LOAD_GLOBAL              ml_aug
             2226  LOAD_METHOD              removeInvariantFeature
             2228  LOAD_FAST                '_traindict'
             2230  LOAD_FAST                'f'
             2232  CALL_METHOD_2         2  '2 positional arguments'
             2234  STORE_FAST               '_traindict'

 L. 801      2236  LOAD_GLOBAL              basic_mdt
             2238  LOAD_METHOD              maxDictConstantRow
             2240  LOAD_FAST                '_traindict'
             2242  CALL_METHOD_1         1  '1 positional argument'
             2244  LOAD_CONST               0
             2246  COMPARE_OP               <=
         2248_2250  POP_JUMP_IF_FALSE  2220  'to 2220'

 L. 802      2252  LOAD_GLOBAL              vis_msg
             2254  LOAD_ATTR                print
             2256  LOAD_STR                 'ERROR in TrainMl2DAsfeFromExisting: No training sample found'
             2258  LOAD_STR                 'error'
             2260  LOAD_CONST               ('type',)
             2262  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2264  POP_TOP          

 L. 803      2266  LOAD_GLOBAL              QtWidgets
             2268  LOAD_ATTR                QMessageBox
             2270  LOAD_METHOD              critical
             2272  LOAD_DEREF               'self'
             2274  LOAD_ATTR                msgbox

 L. 804      2276  LOAD_STR                 'Train 2D-ASFE'

 L. 805      2278  LOAD_STR                 'No training sample found'
             2280  CALL_METHOD_3         3  '3 positional arguments'
             2282  POP_TOP          

 L. 806      2284  LOAD_CONST               None
             2286  RETURN_VALUE     
         2288_2290  JUMP_BACK          2220  'to 2220'
             2292  POP_BLOCK        
           2294_0  COME_FROM_LOOP     2214  '2214'
           2294_1  COME_FROM          2210  '2210'

 L. 808      2294  LOAD_FAST                '_image_height_new'
             2296  LOAD_FAST                '_image_height_old'
             2298  COMPARE_OP               !=
         2300_2302  POP_JUMP_IF_TRUE   2314  'to 2314'
             2304  LOAD_FAST                '_image_width_new'
             2306  LOAD_FAST                '_image_width_old'
             2308  COMPARE_OP               !=
         2310_2312  POP_JUMP_IF_FALSE  2358  'to 2358'
           2314_0  COME_FROM          2300  '2300'

 L. 809      2314  SETUP_LOOP         2358  'to 2358'
             2316  LOAD_FAST                '_features'
             2318  GET_ITER         
             2320  FOR_ITER           2356  'to 2356'
             2322  STORE_FAST               'f'

 L. 810      2324  LOAD_GLOBAL              basic_image
             2326  LOAD_ATTR                changeImageSize
             2328  LOAD_FAST                '_traindict'
             2330  LOAD_FAST                'f'
             2332  BINARY_SUBSCR    

 L. 811      2334  LOAD_FAST                '_image_height_old'

 L. 812      2336  LOAD_FAST                '_image_width_old'

 L. 813      2338  LOAD_FAST                '_image_height_new'

 L. 814      2340  LOAD_FAST                '_image_width_new'
             2342  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2344  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2346  LOAD_FAST                '_traindict'
             2348  LOAD_FAST                'f'
             2350  STORE_SUBSCR     
         2352_2354  JUMP_BACK          2320  'to 2320'
             2356  POP_BLOCK        
           2358_0  COME_FROM_LOOP     2314  '2314'
           2358_1  COME_FROM          2310  '2310'

 L. 816      2358  SETUP_LOOP         2404  'to 2404'
             2360  LOAD_FAST                '_features'
             2362  GET_ITER         
             2364  FOR_ITER           2402  'to 2402'
             2366  STORE_FAST               'f'

 L. 818      2368  LOAD_DEREF               'self'
             2370  LOAD_METHOD              makeTarget
             2372  LOAD_FAST                '_traindict'
             2374  LOAD_FAST                'f'
             2376  BINARY_SUBSCR    
             2378  LOAD_FAST                '_image_height_new'
             2380  LOAD_FAST                '_image_width_new'
             2382  CALL_METHOD_3         3  '3 positional arguments'
             2384  UNPACK_SEQUENCE_2     2 
             2386  LOAD_FAST                '_traindict'
             2388  LOAD_FAST                'f'
             2390  STORE_SUBSCR     
             2392  LOAD_FAST                '_traindict'
             2394  LOAD_FAST                '_target'
             2396  STORE_SUBSCR     
         2398_2400  JUMP_BACK          2364  'to 2364'
             2402  POP_BLOCK        
           2404_0  COME_FROM_LOOP     2358  '2358'

 L. 820      2404  LOAD_GLOBAL              print
             2406  LOAD_STR                 'TrainMl2DCnnFromScratch: A total of %d valid training samples'
             2408  LOAD_GLOBAL              basic_mdt
             2410  LOAD_METHOD              maxDictConstantRow

 L. 821      2412  LOAD_FAST                '_traindict'
             2414  CALL_METHOD_1         1  '1 positional argument'
             2416  BINARY_MODULO    
             2418  CALL_FUNCTION_1       1  '1 positional argument'
             2420  POP_TOP          

 L. 823      2422  LOAD_GLOBAL              print
             2424  LOAD_STR                 'TrainMl2DAsfeFromExisting: Step 3 - Start training'
             2426  CALL_FUNCTION_1       1  '1 positional argument'
             2428  POP_TOP          

 L. 825      2430  LOAD_GLOBAL              QtWidgets
             2432  LOAD_METHOD              QProgressDialog
             2434  CALL_METHOD_0         0  '0 positional arguments'
             2436  STORE_FAST               '_pgsdlg'

 L. 826      2438  LOAD_GLOBAL              QtGui
             2440  LOAD_METHOD              QIcon
             2442  CALL_METHOD_0         0  '0 positional arguments'
             2444  STORE_FAST               'icon'

 L. 827      2446  LOAD_FAST                'icon'
             2448  LOAD_METHOD              addPixmap
             2450  LOAD_GLOBAL              QtGui
             2452  LOAD_METHOD              QPixmap
             2454  LOAD_GLOBAL              os
             2456  LOAD_ATTR                path
             2458  LOAD_METHOD              join
             2460  LOAD_DEREF               'self'
             2462  LOAD_ATTR                iconpath
             2464  LOAD_STR                 'icons/new.png'
             2466  CALL_METHOD_2         2  '2 positional arguments'
             2468  CALL_METHOD_1         1  '1 positional argument'

 L. 828      2470  LOAD_GLOBAL              QtGui
             2472  LOAD_ATTR                QIcon
             2474  LOAD_ATTR                Normal
             2476  LOAD_GLOBAL              QtGui
             2478  LOAD_ATTR                QIcon
             2480  LOAD_ATTR                Off
             2482  CALL_METHOD_3         3  '3 positional arguments'
             2484  POP_TOP          

 L. 829      2486  LOAD_FAST                '_pgsdlg'
             2488  LOAD_METHOD              setWindowIcon
             2490  LOAD_FAST                'icon'
             2492  CALL_METHOD_1         1  '1 positional argument'
             2494  POP_TOP          

 L. 830      2496  LOAD_FAST                '_pgsdlg'
             2498  LOAD_METHOD              setWindowTitle
             2500  LOAD_STR                 'Train 2D-ASFE'
             2502  CALL_METHOD_1         1  '1 positional argument'
             2504  POP_TOP          

 L. 831      2506  LOAD_FAST                '_pgsdlg'
             2508  LOAD_METHOD              setCancelButton
             2510  LOAD_CONST               None
             2512  CALL_METHOD_1         1  '1 positional argument'
             2514  POP_TOP          

 L. 832      2516  LOAD_FAST                '_pgsdlg'
             2518  LOAD_METHOD              setWindowFlags
             2520  LOAD_GLOBAL              QtCore
             2522  LOAD_ATTR                Qt
             2524  LOAD_ATTR                WindowStaysOnTopHint
             2526  CALL_METHOD_1         1  '1 positional argument'
             2528  POP_TOP          

 L. 833      2530  LOAD_FAST                '_pgsdlg'
             2532  LOAD_METHOD              forceShow
             2534  CALL_METHOD_0         0  '0 positional arguments'
             2536  POP_TOP          

 L. 834      2538  LOAD_FAST                '_pgsdlg'
             2540  LOAD_METHOD              setFixedWidth
             2542  LOAD_CONST               400
             2544  CALL_METHOD_1         1  '1 positional argument'
             2546  POP_TOP          

 L. 835      2548  LOAD_GLOBAL              ml_cnn
             2550  LOAD_ATTR                createCNNClassifierFromExisting
             2552  LOAD_FAST                '_traindict'

 L. 836      2554  LOAD_FAST                '_image_height_new'
             2556  LOAD_FAST                '_image_width_new'

 L. 837      2558  LOAD_FAST                '_features'
             2560  LOAD_FAST                '_target'

 L. 838      2562  LOAD_FAST                '_nepoch'
             2564  LOAD_FAST                '_batchsize'

 L. 839      2566  LOAD_FAST                '_nconvblock'

 L. 840      2568  LOAD_FAST                '_nconvlayer'
             2570  LOAD_FAST                '_nconvfeature'

 L. 841      2572  LOAD_FAST                '_nfclayer'
             2574  LOAD_FAST                '_nfcneuron'

 L. 842      2576  LOAD_FAST                '_pool_height'
             2578  LOAD_FAST                '_pool_width'

 L. 843      2580  LOAD_FAST                '_learning_rate'

 L. 844      2582  LOAD_FAST                '_dropout_prob_fclayer'

 L. 845      2584  LOAD_CONST               True

 L. 846      2586  LOAD_FAST                '_savepath'
             2588  LOAD_FAST                '_savename'

 L. 847      2590  LOAD_FAST                '_pgsdlg'

 L. 848      2592  LOAD_FAST                '_precnnpath'

 L. 849      2594  LOAD_FAST                '_precnnname'

 L. 850      2596  LOAD_FAST                '_blockidx'
             2598  LOAD_FAST                '_layeridx'

 L. 851      2600  LOAD_FAST                '_trainable'
             2602  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'nepoch', 'batchsize', 'nconvblock', 'nconvlayer', 'nconvfeature', 'nfclayer', 'nfcneuron', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprobfclayer', 'save2disk', 'savepath', 'savename', 'qpgsdlg', 'precnnpath', 'precnnname', 'blockidx', 'layeridx', 'trainable')
             2604  CALL_FUNCTION_KW_25    25  '25 total positional and keyword args'
             2606  STORE_FAST               '_cnnlog'

 L. 854      2608  LOAD_GLOBAL              QtWidgets
             2610  LOAD_ATTR                QMessageBox
             2612  LOAD_METHOD              information
             2614  LOAD_DEREF               'self'
             2616  LOAD_ATTR                msgbox

 L. 855      2618  LOAD_STR                 'Train 2D-ASFE'

 L. 856      2620  LOAD_STR                 'ASFE trained successfully'
             2622  CALL_METHOD_3         3  '3 positional arguments'
             2624  POP_TOP          

 L. 858      2626  LOAD_GLOBAL              QtWidgets
             2628  LOAD_ATTR                QMessageBox
             2630  LOAD_METHOD              question
             2632  LOAD_DEREF               'self'
             2634  LOAD_ATTR                msgbox
             2636  LOAD_STR                 'Train 2D-ASFE'
             2638  LOAD_STR                 'View learning matrix?'

 L. 859      2640  LOAD_GLOBAL              QtWidgets
             2642  LOAD_ATTR                QMessageBox
             2644  LOAD_ATTR                Yes
             2646  LOAD_GLOBAL              QtWidgets
             2648  LOAD_ATTR                QMessageBox
             2650  LOAD_ATTR                No
             2652  BINARY_OR        

 L. 860      2654  LOAD_GLOBAL              QtWidgets
             2656  LOAD_ATTR                QMessageBox
             2658  LOAD_ATTR                Yes
             2660  CALL_METHOD_5         5  '5 positional arguments'
             2662  STORE_FAST               'reply'

 L. 862      2664  LOAD_FAST                'reply'
             2666  LOAD_GLOBAL              QtWidgets
             2668  LOAD_ATTR                QMessageBox
             2670  LOAD_ATTR                Yes
             2672  COMPARE_OP               ==
         2674_2676  POP_JUMP_IF_FALSE  2744  'to 2744'

 L. 863      2678  LOAD_GLOBAL              QtWidgets
             2680  LOAD_METHOD              QDialog
             2682  CALL_METHOD_0         0  '0 positional arguments'
             2684  STORE_FAST               '_viewmllearnmat'

 L. 864      2686  LOAD_GLOBAL              gui_viewmllearnmat
             2688  CALL_FUNCTION_0       0  '0 positional arguments'
             2690  STORE_FAST               '_gui'

 L. 865      2692  LOAD_FAST                '_cnnlog'
             2694  LOAD_STR                 'learning_curve'
             2696  BINARY_SUBSCR    
             2698  LOAD_FAST                '_gui'
             2700  STORE_ATTR               learnmat

 L. 866      2702  LOAD_DEREF               'self'
             2704  LOAD_ATTR                linestyle
             2706  LOAD_FAST                '_gui'
             2708  STORE_ATTR               linestyle

 L. 867      2710  LOAD_DEREF               'self'
             2712  LOAD_ATTR                fontstyle
             2714  LOAD_FAST                '_gui'
             2716  STORE_ATTR               fontstyle

 L. 868      2718  LOAD_FAST                '_gui'
             2720  LOAD_METHOD              setupGUI
             2722  LOAD_FAST                '_viewmllearnmat'
             2724  CALL_METHOD_1         1  '1 positional argument'
             2726  POP_TOP          

 L. 869      2728  LOAD_FAST                '_viewmllearnmat'
             2730  LOAD_METHOD              exec
             2732  CALL_METHOD_0         0  '0 positional arguments'
             2734  POP_TOP          

 L. 870      2736  LOAD_FAST                '_viewmllearnmat'
             2738  LOAD_METHOD              show
             2740  CALL_METHOD_0         0  '0 positional arguments'
             2742  POP_TOP          
           2744_0  COME_FROM          2674  '2674'

Parse error at or near `POP_TOP' instruction at offset 2742

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
    TrainMl2DAsfeFromExisting = QtWidgets.QWidget()
    gui = trainml2dasfefromexisting()
    gui.setupGUI(TrainMl2DAsfeFromExisting)
    TrainMl2DAsfeFromExisting.show()
    sys.exit(app.exec_())