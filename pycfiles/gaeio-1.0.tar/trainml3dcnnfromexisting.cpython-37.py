# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml3dcnnfromexisting.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 55596 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.pointset.analysis as point_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.video as basic_video
import cognitivegeo.src.ml.augmentation as ml_aug
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.cnnclassifier3d as ml_cnn3d
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml3dcnnfromexisting(object):
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
    traindataconfig['BalanceTarget_Enabled'] = True
    traindataconfig['BalanceTarget_Checked'] = False
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False

    def setupGUI(self, TrainMl3DCnnFromExisting):
        TrainMl3DCnnFromExisting.setObjectName('TrainMl3DCnnFromExisting')
        TrainMl3DCnnFromExisting.setFixedSize(800, 650)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl3DCnnFromExisting.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl3DCnnFromExisting)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lbloldsize = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 130, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 130, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 130, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lblolddepth = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblolddepth.setObjectName('lblolddepth')
        self.lblolddepth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtolddepth = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtolddepth.setObjectName('ldtolddepth')
        self.ldtolddepth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 130, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 130, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 130, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewdepth = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblnewdepth.setObjectName('lblnewdepth')
        self.lblnewdepth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewdepth = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtnewdepth.setObjectName('ldtnewdepth')
        self.ldtnewdepth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl3DCnnFromExisting)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblexisting = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblexisting.setObjectName('lblexisting')
        self.lblexisting.setGeometry(QtCore.QRect(410, 50, 100, 30))
        self.ldtexisting = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtexisting.setObjectName('ldtexisting')
        self.ldtexisting.setGeometry(QtCore.QRect(510, 50, 210, 30))
        self.btnexisting = QtWidgets.QPushButton(TrainMl3DCnnFromExisting)
        self.btnexisting.setObjectName('btnexisting')
        self.btnexisting.setGeometry(QtCore.QRect(730, 50, 60, 30))
        self.lblnconvblockexisting = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblnconvblockexisting.setObjectName('lblnconvblockexisting')
        self.lblnconvblockexisting.setGeometry(QtCore.QRect(410, 90, 130, 30))
        self.ldtnconvblockexisting = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtnconvblockexisting.setObjectName('ldtnconvblockexisting')
        self.ldtnconvblockexisting.setGeometry(QtCore.QRect(550, 90, 40, 30))
        self.twgnconvblockexisting = QtWidgets.QTableWidget(TrainMl3DCnnFromExisting)
        self.twgnconvblockexisting.setObjectName('twgnconvblockexisting')
        self.twgnconvblockexisting.setGeometry(QtCore.QRect(610, 90, 180, 150))
        self.twgnconvblockexisting.setColumnCount(3)
        self.twgnconvblockexisting.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblockexisting.verticalHeader().hide()
        self.lblblockid = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblblockid.setObjectName('lblblockid')
        self.lblblockid.setGeometry(QtCore.QRect(410, 130, 130, 30))
        self.cbbblockid = QtWidgets.QComboBox(TrainMl3DCnnFromExisting)
        self.cbbblockid.setObjectName('cbbblockid')
        self.cbbblockid.setGeometry(QtCore.QRect(550, 130, 40, 30))
        self.lbllayerid = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lbllayerid.setObjectName('lbllayerid')
        self.lbllayerid.setGeometry(QtCore.QRect(410, 170, 130, 30))
        self.cbblayerid = QtWidgets.QComboBox(TrainMl3DCnnFromExisting)
        self.cbblayerid.setObjectName('cbblayerid')
        self.cbblayerid.setGeometry(QtCore.QRect(550, 170, 40, 30))
        self.lbltrainable = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lbltrainable.setObjectName('lbltrainable')
        self.lbltrainable.setGeometry(QtCore.QRect(410, 210, 130, 30))
        self.cbbtrainable = QtWidgets.QComboBox(TrainMl3DCnnFromExisting)
        self.cbbtrainable.setObjectName('cbbtrainable')
        self.cbbtrainable.setGeometry(QtCore.QRect(550, 210, 40, 30))
        self.lblappend = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblappend.setObjectName('lblappend')
        self.lblappend.setGeometry(QtCore.QRect(410, 250, 200, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 290, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 290, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl3DCnnFromExisting)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 330, 180, 180))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 290, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 290, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(TrainMl3DCnnFromExisting)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 330, 180, 180))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 520, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 520, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 520, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 560, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 560, 40, 30))
        self.lblmaskdepth = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblmaskdepth.setObjectName('lblmaskdepth')
        self.lblmaskdepth.setGeometry(QtCore.QRect(500, 600, 50, 30))
        self.ldtmaskdepth = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtmaskdepth.setObjectName('ldtmaskdepth')
        self.ldtmaskdepth.setGeometry(QtCore.QRect(550, 600, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 520, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 520, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 520, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 560, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 560, 40, 30))
        self.lblpooldepth = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblpooldepth.setObjectName('lblpooldepth')
        self.lblpooldepth.setGeometry(QtCore.QRect(700, 600, 50, 30))
        self.ldtpooldepth = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtpooldepth.setObjectName('ldtpooldepth')
        self.ldtpooldepth.setGeometry(QtCore.QRect(750, 600, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl3DCnnFromExisting)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 310, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 350, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.lblfcdropout = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblfcdropout.setObjectName('lblfcdropout')
        self.lblfcdropout.setGeometry(QtCore.QRect(210, 390, 130, 30))
        self.ldtfcdropout = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtfcdropout.setObjectName('ldtfcdropout')
        self.ldtfcdropout.setGeometry(QtCore.QRect(350, 390, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl3DCnnFromExisting)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 100, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl3DCnnFromExisting)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(110, 440, 210, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl3DCnnFromExisting)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 440, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl3DCnnFromExisting)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(120, 600, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl3DCnnFromExisting)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl3DCnnFromExisting.geometry().center().x()
        _center_y = TrainMl3DCnnFromExisting.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl3DCnnFromExisting)
        QtCore.QMetaObject.connectSlotsByName(TrainMl3DCnnFromExisting)

    def retranslateGUI(self, TrainMl3DCnnFromExisting):
        self.dialog = TrainMl3DCnnFromExisting
        _translate = QtCore.QCoreApplication.translate
        TrainMl3DCnnFromExisting.setWindowTitle(_translate('TrainMl3DCnnFromExisting', 'Train 3D-CNN from pre-trained'))
        self.lblfeature.setText(_translate('TrainMl3DCnnFromExisting', 'Select features:'))
        self.lbltarget.setText(_translate('TrainMl3DCnnFromExisting', 'Select target:'))
        self.lbloldsize.setText(_translate('TrainMl3DCnnFromExisting', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl3DCnnFromExisting', 'height=\ntime/depth'))
        self.ldtoldheight.setText(_translate('TrainMl3DCnnFromExisting', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl3DCnnFromExisting', 'width=\ncrossline'))
        self.ldtoldwidth.setText(_translate('TrainMl3DCnnFromExisting', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblolddepth.setText(_translate('TrainMl3DCnnFromExisting', 'depth=\ninline'))
        self.ldtolddepth.setText(_translate('TrainMl3DCnnFromExisting', ''))
        self.ldtolddepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl3DCnnFromExisting', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl3DCnnFromExisting', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl3DCnnFromExisting', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl3DCnnFromExisting', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl3DCnnFromExisting', '32'))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewdepth.setText(_translate('TrainMl3DCnnFromExisting', 'depth='))
        self.ldtnewdepth.setText(_translate('TrainMl3DCnnFromExisting', '32'))
        self.ldtnewdepth.setAlignment(QtCore.Qt.AlignCenter)
        if self.checkSurvInfo():
            self.featurelist.clear()
            self.lwgfeature.clear()
            self.cbbtarget.clear()
            _firstfeature = None
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    self.featurelist.append(i)
                    item = QtWidgets.QListWidgetItem(self.lwgfeature)
                    item.setText(_translate('TrainMl3DCnnFromExisting', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl3DCnnFromExisting', 'Specify CNN architecture:'))
        self.lblexisting.setText(_translate('TrainMl3DCnnFromExisting', 'Select pre-trained:'))
        self.ldtexisting.setText(_translate('TrainMl3DCnnFromExisting', ''))
        self.ldtexisting.textChanged.connect(self.changeLdtExisting)
        self.btnexisting.setText(_translate('TrainMl3DCnnFromExisting', 'Browse'))
        self.btnexisting.clicked.connect(self.clickBtnExisting)
        self.lblnconvblockexisting.setText(_translate('TrainMl3DCnnFromExisting', 'Available conv. blocks:'))
        self.lblnconvblockexisting.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblockexisting.setText(_translate('TrainMl3DCnnFromExisting', ''))
        self.ldtnconvblockexisting.setEnabled(False)
        self.ldtnconvblockexisting.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblockexisting.textChanged.connect(self.changeLdtNconvblockExisting)
        self.twgnconvblockexisting.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblblockid.setText(_translate('TrainMl3DCnnFromExisting', 'Select conv. block ID:'))
        self.lblblockid.setAlignment(QtCore.Qt.AlignRight)
        self.cbbblockid.currentIndexChanged.connect(self.changeCbbBlockid)
        self.lbllayerid.setText(_translate('TrainMl3DCnnFromExisting', 'Select conv. layer ID:'))
        self.lbllayerid.setAlignment(QtCore.Qt.AlignRight)
        self.lbltrainable.setText(_translate('TrainMl3DCnnFromExisting', 'Is trainable?:'))
        self.lbltrainable.setAlignment(QtCore.Qt.AlignRight)
        self.cbbtrainable.addItems(['Yes', 'No'])
        self.lblappend.setText(_translate('TrainMl3DCnnFromExisting', 'Append more blocks & layers:'))
        self.lblnconvblock.setText(_translate('TrainMl3DCnnFromExisting', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl3DCnnFromExisting', '2'))
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

        self.lblnfclayer.setText(_translate('TrainMl3DCnnFromExisting', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('TrainMl3DCnnFromExisting', '2'))
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.twgnfclayer.setRowCount(2)
        for _idx in range(int(self.ldtnfclayer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl3DCnnFromExisting', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgnfclayer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgnfclayer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl3DCnnFromExisting', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl3DCnnFromExisting', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl3DCnnFromExisting', ''))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskheight.setEnabled(False)
        self.lblmaskwidth.setText(_translate('TrainMl3DCnnFromExisting', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl3DCnnFromExisting', ''))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskwidth.setEnabled(False)
        self.lblmaskdepth.setText(_translate('TrainMl3DCnnFromExisting', 'depth='))
        self.ldtmaskdepth.setText(_translate('TrainMl3DCnnFromExisting', ''))
        self.ldtmaskdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskdepth.setEnabled(False)
        self.lblpoolsize.setText(_translate('TrainMl3DCnnFromExisting', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl3DCnnFromExisting', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl3DCnnFromExisting', ''))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl3DCnnFromExisting', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl3DCnnFromExisting', ''))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpooldepth.setText(_translate('TrainMl3DCnnFromExisting', 'depth='))
        self.ldtpooldepth.setText(_translate('TrainMl3DCnnFromExisting', ''))
        self.ldtpooldepth.setAlignment(QtCore.Qt.AlignCenter)
        self.btnconfigtraindata.setText(_translate('TrainMl3DCnnFromExisting', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lblpara.setText(_translate('TrainMl3DCnnFromExisting', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl3DCnnFromExisting', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl3DCnnFromExisting', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl3DCnnFromExisting', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl3DCnnFromExisting', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl3DCnnFromExisting', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl3DCnnFromExisting', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfcdropout.setText(_translate('TrainMl3DCnnFromExisting', 'MLP dropout rate:'))
        self.lblfcdropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtfcdropout.setText(_translate('TrainMl3DCnnFromExisting', '0.5'))
        self.ldtfcdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl3DCnnFromExisting', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl3DCnnFromExisting', ''))
        self.btnsave.setText(_translate('TrainMl3DCnnFromExisting', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl3DCnnFromExisting', 'Train 3D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl3DCnnFromExisting)

    def changeLdtExisting(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtexisting.text()):
            _modelpath = os.path.dirname(self.ldtexisting.text())
            _modelname = os.path.splitext(os.path.basename(self.ldtexisting.text()))[0]
        else:
            _modelpath = ''
            _modelname = ''
        if ml_tfm.is3DConvModel(_modelpath, _modelname) is True:
            _modelinfo = ml_tfm.getModelInfo(_modelpath, _modelname)
            self.ldtnconvblockexisting.setText(str(_modelinfo['number_conv_block']))
            self.ldtmaskheight.setText(str(_modelinfo['patch_size'][0]))
            self.ldtmaskwidth.setText(str(_modelinfo['patch_size'][1]))
            self.ldtmaskdepth.setText(str(_modelinfo['patch_size'][2]))
            self.ldtpoolheight.setText(str(_modelinfo['pool_size'][0]))
            self.ldtpoolwidth.setText(str(_modelinfo['pool_size'][1]))
            self.ldtpooldepth.setText(str(_modelinfo['pool_size'][2]))
        else:
            self.ldtnconvblockexisting.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtmaskdepth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')
            self.ldtmaskdepth.setText('')

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
        if ml_tfm.is3DConvModel(_modelpath, _modelname) is True:
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
        if ml_tfm.is3DConvModel(_modelpath, _modelname) is True:
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

    def clickBtnTrainMl3DCnnFromExisting--- This code section failed: ---

 L. 623         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 625         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 626        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 627        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 628        50  LOAD_STR                 'Train 3D-CNN'

 L. 629        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 630        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 632        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_video_height_old'

 L. 633        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_video_width_old'

 L. 634        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtolddepth
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_video_depth_old'

 L. 635       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewheight
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_video_height_new'

 L. 636       126  LOAD_GLOBAL              basic_data
              128  LOAD_METHOD              str2int
              130  LOAD_DEREF               'self'
              132  LOAD_ATTR                ldtnewwidth
              134  LOAD_METHOD              text
              136  CALL_METHOD_0         0  '0 positional arguments'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  STORE_FAST               '_video_width_new'

 L. 637       142  LOAD_GLOBAL              basic_data
              144  LOAD_METHOD              str2int
              146  LOAD_DEREF               'self'
              148  LOAD_ATTR                ldtnewdepth
              150  LOAD_METHOD              text
              152  CALL_METHOD_0         0  '0 positional arguments'
              154  CALL_METHOD_1         1  '1 positional argument'
              156  STORE_FAST               '_video_depth_new'

 L. 638       158  LOAD_FAST                '_video_height_old'
              160  LOAD_CONST               False
              162  COMPARE_OP               is
              164  POP_JUMP_IF_TRUE    206  'to 206'
              166  LOAD_FAST                '_video_width_old'
              168  LOAD_CONST               False
              170  COMPARE_OP               is
              172  POP_JUMP_IF_TRUE    206  'to 206'
              174  LOAD_FAST                '_video_depth_old'
              176  LOAD_CONST               False
              178  COMPARE_OP               is
              180  POP_JUMP_IF_TRUE    206  'to 206'

 L. 639       182  LOAD_FAST                '_video_height_new'
              184  LOAD_CONST               False
              186  COMPARE_OP               is
              188  POP_JUMP_IF_TRUE    206  'to 206'
              190  LOAD_FAST                '_video_width_new'
              192  LOAD_CONST               False
              194  COMPARE_OP               is
              196  POP_JUMP_IF_TRUE    206  'to 206'
              198  LOAD_FAST                '_video_depth_new'
              200  LOAD_CONST               False
              202  COMPARE_OP               is
              204  POP_JUMP_IF_FALSE   242  'to 242'
            206_0  COME_FROM           196  '196'
            206_1  COME_FROM           188  '188'
            206_2  COME_FROM           180  '180'
            206_3  COME_FROM           172  '172'
            206_4  COME_FROM           164  '164'

 L. 640       206  LOAD_GLOBAL              vis_msg
              208  LOAD_ATTR                print
              210  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Non-integer feature size'
              212  LOAD_STR                 'error'
              214  LOAD_CONST               ('type',)
              216  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              218  POP_TOP          

 L. 641       220  LOAD_GLOBAL              QtWidgets
              222  LOAD_ATTR                QMessageBox
              224  LOAD_METHOD              critical
              226  LOAD_DEREF               'self'
              228  LOAD_ATTR                msgbox

 L. 642       230  LOAD_STR                 'Train 3D-CNN'

 L. 643       232  LOAD_STR                 'Non-integer feature size'
              234  CALL_METHOD_3         3  '3 positional arguments'
              236  POP_TOP          

 L. 644       238  LOAD_CONST               None
              240  RETURN_VALUE     
            242_0  COME_FROM           204  '204'

 L. 645       242  LOAD_FAST                '_video_height_old'
              244  LOAD_CONST               2
              246  COMPARE_OP               <
          248_250  POP_JUMP_IF_TRUE    302  'to 302'
              252  LOAD_FAST                '_video_width_old'
              254  LOAD_CONST               2
              256  COMPARE_OP               <
          258_260  POP_JUMP_IF_TRUE    302  'to 302'
              262  LOAD_FAST                '_video_depth_old'
              264  LOAD_CONST               2
              266  COMPARE_OP               <
          268_270  POP_JUMP_IF_TRUE    302  'to 302'

 L. 646       272  LOAD_FAST                '_video_height_new'
              274  LOAD_CONST               2
              276  COMPARE_OP               <
          278_280  POP_JUMP_IF_TRUE    302  'to 302'
              282  LOAD_FAST                '_video_width_new'
              284  LOAD_CONST               2
              286  COMPARE_OP               <
          288_290  POP_JUMP_IF_TRUE    302  'to 302'
              292  LOAD_FAST                '_video_depth_new'
              294  LOAD_CONST               2
              296  COMPARE_OP               <
          298_300  POP_JUMP_IF_FALSE   338  'to 338'
            302_0  COME_FROM           288  '288'
            302_1  COME_FROM           278  '278'
            302_2  COME_FROM           268  '268'
            302_3  COME_FROM           258  '258'
            302_4  COME_FROM           248  '248'

 L. 647       302  LOAD_GLOBAL              vis_msg
              304  LOAD_ATTR                print
              306  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Features are not 3D'
              308  LOAD_STR                 'error'
              310  LOAD_CONST               ('type',)
              312  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              314  POP_TOP          

 L. 648       316  LOAD_GLOBAL              QtWidgets
              318  LOAD_ATTR                QMessageBox
              320  LOAD_METHOD              critical
              322  LOAD_DEREF               'self'
              324  LOAD_ATTR                msgbox

 L. 649       326  LOAD_STR                 'Train 3D-CNN'

 L. 650       328  LOAD_STR                 'Features are not 3D'
              330  CALL_METHOD_3         3  '3 positional arguments'
              332  POP_TOP          

 L. 651       334  LOAD_CONST               None
              336  RETURN_VALUE     
            338_0  COME_FROM           298  '298'

 L. 653       338  LOAD_CONST               2
              340  LOAD_GLOBAL              int
              342  LOAD_FAST                '_video_height_old'
              344  LOAD_CONST               2
              346  BINARY_TRUE_DIVIDE
              348  CALL_FUNCTION_1       1  '1 positional argument'
              350  BINARY_MULTIPLY  
              352  LOAD_CONST               1
              354  BINARY_ADD       
              356  STORE_FAST               '_video_height_old'

 L. 654       358  LOAD_CONST               2
              360  LOAD_GLOBAL              int
              362  LOAD_FAST                '_video_width_old'
              364  LOAD_CONST               2
              366  BINARY_TRUE_DIVIDE
              368  CALL_FUNCTION_1       1  '1 positional argument'
              370  BINARY_MULTIPLY  
              372  LOAD_CONST               1
              374  BINARY_ADD       
              376  STORE_FAST               '_video_width_old'

 L. 655       378  LOAD_CONST               2
              380  LOAD_GLOBAL              int
              382  LOAD_FAST                '_video_depth_old'
              384  LOAD_CONST               2
              386  BINARY_TRUE_DIVIDE
              388  CALL_FUNCTION_1       1  '1 positional argument'
              390  BINARY_MULTIPLY  
              392  LOAD_CONST               1
              394  BINARY_ADD       
              396  STORE_FAST               '_video_depth_old'

 L. 656       398  LOAD_FAST                '_video_height_old'
              400  LOAD_CONST               1
              402  COMPARE_OP               <=
          404_406  POP_JUMP_IF_TRUE    428  'to 428'
              408  LOAD_FAST                '_video_width_old'
              410  LOAD_CONST               1
              412  COMPARE_OP               <=
          414_416  POP_JUMP_IF_TRUE    428  'to 428'
              418  LOAD_FAST                '_video_depth_old'
              420  LOAD_CONST               1
              422  COMPARE_OP               <=
          424_426  POP_JUMP_IF_FALSE   464  'to 464'
            428_0  COME_FROM           414  '414'
            428_1  COME_FROM           404  '404'

 L. 657       428  LOAD_GLOBAL              vis_msg
              430  LOAD_ATTR                print
              432  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: wrong original video size'
              434  LOAD_STR                 'error'
              436  LOAD_CONST               ('type',)
              438  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              440  POP_TOP          

 L. 658       442  LOAD_GLOBAL              QtWidgets
              444  LOAD_ATTR                QMessageBox
              446  LOAD_METHOD              critical
              448  LOAD_DEREF               'self'
              450  LOAD_ATTR                msgbox

 L. 659       452  LOAD_STR                 'Train 3D-CNN'

 L. 660       454  LOAD_STR                 'Wrong original video size'
              456  CALL_METHOD_3         3  '3 positional arguments'
              458  POP_TOP          

 L. 661       460  LOAD_CONST               None
              462  RETURN_VALUE     
            464_0  COME_FROM           424  '424'

 L. 663       464  LOAD_DEREF               'self'
              466  LOAD_ATTR                lwgfeature
              468  LOAD_METHOD              selectedItems
              470  CALL_METHOD_0         0  '0 positional arguments'
              472  STORE_FAST               '_features'

 L. 664       474  LOAD_LISTCOMP            '<code_object <listcomp>>'
              476  LOAD_STR                 'trainml3dcnnfromexisting.clickBtnTrainMl3DCnnFromExisting.<locals>.<listcomp>'
              478  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              480  LOAD_FAST                '_features'
              482  GET_ITER         
              484  CALL_FUNCTION_1       1  '1 positional argument'
              486  STORE_FAST               '_features'

 L. 665       488  LOAD_DEREF               'self'
              490  LOAD_ATTR                featurelist
              492  LOAD_DEREF               'self'
              494  LOAD_ATTR                cbbtarget
              496  LOAD_METHOD              currentIndex
              498  CALL_METHOD_0         0  '0 positional arguments'
              500  BINARY_SUBSCR    
              502  STORE_FAST               '_target'

 L. 667       504  LOAD_GLOBAL              len
              506  LOAD_DEREF               'self'
              508  LOAD_ATTR                ldtexisting
              510  LOAD_METHOD              text
              512  CALL_METHOD_0         0  '0 positional arguments'
              514  CALL_FUNCTION_1       1  '1 positional argument'
              516  LOAD_CONST               1
              518  COMPARE_OP               <
          520_522  POP_JUMP_IF_FALSE   560  'to 560'

 L. 668       524  LOAD_GLOBAL              vis_msg
              526  LOAD_ATTR                print
              528  LOAD_STR                 'ERROR in TrainMl2DCnnFromExisting: No name specified for pre-trained network'
              530  LOAD_STR                 'error'
              532  LOAD_CONST               ('type',)
              534  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              536  POP_TOP          

 L. 669       538  LOAD_GLOBAL              QtWidgets
              540  LOAD_ATTR                QMessageBox
              542  LOAD_METHOD              critical
              544  LOAD_DEREF               'self'
              546  LOAD_ATTR                msgbox

 L. 670       548  LOAD_STR                 'Train 2D-CNN'

 L. 671       550  LOAD_STR                 'No name specified for pre-trained network'
              552  CALL_METHOD_3         3  '3 positional arguments'
              554  POP_TOP          

 L. 672       556  LOAD_CONST               None
              558  RETURN_VALUE     
            560_0  COME_FROM           520  '520'

 L. 673       560  LOAD_GLOBAL              os
              562  LOAD_ATTR                path
              564  LOAD_METHOD              dirname
              566  LOAD_DEREF               'self'
              568  LOAD_ATTR                ldtexisting
              570  LOAD_METHOD              text
              572  CALL_METHOD_0         0  '0 positional arguments'
              574  CALL_METHOD_1         1  '1 positional argument'
              576  STORE_FAST               '_precnnpath'

 L. 674       578  LOAD_GLOBAL              os
              580  LOAD_ATTR                path
              582  LOAD_METHOD              splitext
              584  LOAD_GLOBAL              os
              586  LOAD_ATTR                path
              588  LOAD_METHOD              basename
              590  LOAD_DEREF               'self'
              592  LOAD_ATTR                ldtexisting
              594  LOAD_METHOD              text
              596  CALL_METHOD_0         0  '0 positional arguments'
              598  CALL_METHOD_1         1  '1 positional argument'
              600  CALL_METHOD_1         1  '1 positional argument'
              602  LOAD_CONST               0
              604  BINARY_SUBSCR    
              606  STORE_FAST               '_precnnname'

 L. 675       608  LOAD_DEREF               'self'
              610  LOAD_ATTR                cbbblockid
              612  LOAD_METHOD              currentIndex
              614  CALL_METHOD_0         0  '0 positional arguments'
              616  STORE_FAST               '_blockidx'

 L. 676       618  LOAD_DEREF               'self'
              620  LOAD_ATTR                cbblayerid
              622  LOAD_METHOD              currentIndex
              624  CALL_METHOD_0         0  '0 positional arguments'
              626  STORE_FAST               '_layeridx'

 L. 677       628  LOAD_CONST               True
              630  STORE_FAST               '_trainable'

 L. 678       632  LOAD_DEREF               'self'
              634  LOAD_ATTR                cbbtrainable
              636  LOAD_METHOD              currentIndex
              638  CALL_METHOD_0         0  '0 positional arguments'
              640  LOAD_CONST               0
              642  COMPARE_OP               !=
          644_646  POP_JUMP_IF_FALSE   652  'to 652'

 L. 679       648  LOAD_CONST               False
              650  STORE_FAST               '_trainable'
            652_0  COME_FROM           644  '644'

 L. 681       652  LOAD_GLOBAL              ml_tfm
              654  LOAD_METHOD              get3DConvModelNChannel
              656  LOAD_FAST                '_precnnpath'
              658  LOAD_FAST                '_precnnname'
              660  CALL_METHOD_2         2  '2 positional arguments'
              662  LOAD_GLOBAL              len
              664  LOAD_FAST                '_features'
              666  CALL_FUNCTION_1       1  '1 positional argument'
              668  COMPARE_OP               !=
          670_672  POP_JUMP_IF_FALSE   710  'to 710'

 L. 682       674  LOAD_GLOBAL              vis_msg
              676  LOAD_ATTR                print
              678  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Feature channel number not match with pre-trained network'

 L. 683       680  LOAD_STR                 'error'
              682  LOAD_CONST               ('type',)
              684  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              686  POP_TOP          

 L. 684       688  LOAD_GLOBAL              QtWidgets
              690  LOAD_ATTR                QMessageBox
              692  LOAD_METHOD              critical
              694  LOAD_DEREF               'self'
              696  LOAD_ATTR                msgbox

 L. 685       698  LOAD_STR                 'Train 3D-CNN'

 L. 686       700  LOAD_STR                 'Feature channel number not match with pre-trained network'
              702  CALL_METHOD_3         3  '3 positional arguments'
              704  POP_TOP          

 L. 687       706  LOAD_CONST               None
              708  RETURN_VALUE     
            710_0  COME_FROM           670  '670'

 L. 689       710  LOAD_GLOBAL              basic_data
              712  LOAD_METHOD              str2int
              714  LOAD_DEREF               'self'
              716  LOAD_ATTR                ldtnconvblock
              718  LOAD_METHOD              text
              720  CALL_METHOD_0         0  '0 positional arguments'
              722  CALL_METHOD_1         1  '1 positional argument'
              724  STORE_FAST               '_nconvblock'

 L. 690       726  LOAD_CLOSURE             'self'
              728  BUILD_TUPLE_1         1 
              730  LOAD_LISTCOMP            '<code_object <listcomp>>'
              732  LOAD_STR                 'trainml3dcnnfromexisting.clickBtnTrainMl3DCnnFromExisting.<locals>.<listcomp>'
              734  MAKE_FUNCTION_8          'closure'
              736  LOAD_GLOBAL              range
              738  LOAD_FAST                '_nconvblock'
              740  CALL_FUNCTION_1       1  '1 positional argument'
              742  GET_ITER         
              744  CALL_FUNCTION_1       1  '1 positional argument'
              746  STORE_FAST               '_nconvlayer'

 L. 691       748  LOAD_CLOSURE             'self'
              750  BUILD_TUPLE_1         1 
              752  LOAD_LISTCOMP            '<code_object <listcomp>>'
              754  LOAD_STR                 'trainml3dcnnfromexisting.clickBtnTrainMl3DCnnFromExisting.<locals>.<listcomp>'
              756  MAKE_FUNCTION_8          'closure'
              758  LOAD_GLOBAL              range
              760  LOAD_FAST                '_nconvblock'
              762  CALL_FUNCTION_1       1  '1 positional argument'
              764  GET_ITER         
              766  CALL_FUNCTION_1       1  '1 positional argument'
              768  STORE_FAST               '_nconvfeature'

 L. 692       770  LOAD_GLOBAL              basic_data
              772  LOAD_METHOD              str2int
              774  LOAD_DEREF               'self'
              776  LOAD_ATTR                ldtnfclayer
              778  LOAD_METHOD              text
              780  CALL_METHOD_0         0  '0 positional arguments'
              782  CALL_METHOD_1         1  '1 positional argument'
              784  STORE_FAST               '_nfclayer'

 L. 693       786  LOAD_CLOSURE             'self'
              788  BUILD_TUPLE_1         1 
              790  LOAD_LISTCOMP            '<code_object <listcomp>>'
              792  LOAD_STR                 'trainml3dcnnfromexisting.clickBtnTrainMl3DCnnFromExisting.<locals>.<listcomp>'
              794  MAKE_FUNCTION_8          'closure'
              796  LOAD_GLOBAL              range
              798  LOAD_FAST                '_nfclayer'
              800  CALL_FUNCTION_1       1  '1 positional argument'
              802  GET_ITER         
              804  CALL_FUNCTION_1       1  '1 positional argument'
              806  STORE_FAST               '_nfcneuron'

 L. 694       808  LOAD_GLOBAL              basic_data
              810  LOAD_METHOD              str2int
              812  LOAD_DEREF               'self'
              814  LOAD_ATTR                ldtmaskheight
              816  LOAD_METHOD              text
              818  CALL_METHOD_0         0  '0 positional arguments'
              820  CALL_METHOD_1         1  '1 positional argument'
              822  STORE_FAST               '_patch_height'

 L. 695       824  LOAD_GLOBAL              basic_data
              826  LOAD_METHOD              str2int
              828  LOAD_DEREF               'self'
              830  LOAD_ATTR                ldtmaskwidth
              832  LOAD_METHOD              text
              834  CALL_METHOD_0         0  '0 positional arguments'
              836  CALL_METHOD_1         1  '1 positional argument'
              838  STORE_FAST               '_patch_width'

 L. 696       840  LOAD_GLOBAL              basic_data
              842  LOAD_METHOD              str2int
              844  LOAD_DEREF               'self'
              846  LOAD_ATTR                ldtmaskdepth
              848  LOAD_METHOD              text
              850  CALL_METHOD_0         0  '0 positional arguments'
              852  CALL_METHOD_1         1  '1 positional argument'
              854  STORE_FAST               '_patch_depth'

 L. 697       856  LOAD_GLOBAL              basic_data
              858  LOAD_METHOD              str2int
              860  LOAD_DEREF               'self'
              862  LOAD_ATTR                ldtpoolheight
              864  LOAD_METHOD              text
              866  CALL_METHOD_0         0  '0 positional arguments'
              868  CALL_METHOD_1         1  '1 positional argument'
              870  STORE_FAST               '_pool_height'

 L. 698       872  LOAD_GLOBAL              basic_data
              874  LOAD_METHOD              str2int
              876  LOAD_DEREF               'self'
              878  LOAD_ATTR                ldtpoolwidth
              880  LOAD_METHOD              text
              882  CALL_METHOD_0         0  '0 positional arguments'
              884  CALL_METHOD_1         1  '1 positional argument'
              886  STORE_FAST               '_pool_width'

 L. 699       888  LOAD_GLOBAL              basic_data
              890  LOAD_METHOD              str2int
              892  LOAD_DEREF               'self'
              894  LOAD_ATTR                ldtpooldepth
              896  LOAD_METHOD              text
              898  CALL_METHOD_0         0  '0 positional arguments'
              900  CALL_METHOD_1         1  '1 positional argument'
              902  STORE_FAST               '_pool_depth'

 L. 700       904  LOAD_GLOBAL              basic_data
              906  LOAD_METHOD              str2int
              908  LOAD_DEREF               'self'
              910  LOAD_ATTR                ldtnepoch
              912  LOAD_METHOD              text
              914  CALL_METHOD_0         0  '0 positional arguments'
              916  CALL_METHOD_1         1  '1 positional argument'
              918  STORE_FAST               '_nepoch'

 L. 701       920  LOAD_GLOBAL              basic_data
              922  LOAD_METHOD              str2int
              924  LOAD_DEREF               'self'
              926  LOAD_ATTR                ldtbatchsize
              928  LOAD_METHOD              text
              930  CALL_METHOD_0         0  '0 positional arguments'
              932  CALL_METHOD_1         1  '1 positional argument'
              934  STORE_FAST               '_batchsize'

 L. 702       936  LOAD_GLOBAL              basic_data
              938  LOAD_METHOD              str2float
              940  LOAD_DEREF               'self'
              942  LOAD_ATTR                ldtlearnrate
              944  LOAD_METHOD              text
              946  CALL_METHOD_0         0  '0 positional arguments'
              948  CALL_METHOD_1         1  '1 positional argument'
              950  STORE_FAST               '_learning_rate'

 L. 703       952  LOAD_GLOBAL              basic_data
              954  LOAD_METHOD              str2float
              956  LOAD_DEREF               'self'
              958  LOAD_ATTR                ldtfcdropout
              960  LOAD_METHOD              text
              962  CALL_METHOD_0         0  '0 positional arguments'
              964  CALL_METHOD_1         1  '1 positional argument'
              966  STORE_FAST               '_dropout_prob_fclayer'

 L. 704       968  LOAD_FAST                '_nconvblock'
              970  LOAD_CONST               False
              972  COMPARE_OP               is
          974_976  POP_JUMP_IF_TRUE    988  'to 988'
              978  LOAD_FAST                '_nconvblock'
              980  LOAD_CONST               0
              982  COMPARE_OP               <=
          984_986  POP_JUMP_IF_FALSE  1024  'to 1024'
            988_0  COME_FROM           974  '974'

 L. 705       988  LOAD_GLOBAL              vis_msg
              990  LOAD_ATTR                print
              992  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Non-positive convolutional block number'
              994  LOAD_STR                 'error'
              996  LOAD_CONST               ('type',)
              998  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1000  POP_TOP          

 L. 706      1002  LOAD_GLOBAL              QtWidgets
             1004  LOAD_ATTR                QMessageBox
             1006  LOAD_METHOD              critical
             1008  LOAD_DEREF               'self'
             1010  LOAD_ATTR                msgbox

 L. 707      1012  LOAD_STR                 'Train 3D-CNN'

 L. 708      1014  LOAD_STR                 'Non-positive convolutional block number'
             1016  CALL_METHOD_3         3  '3 positional arguments'
             1018  POP_TOP          

 L. 709      1020  LOAD_CONST               None
             1022  RETURN_VALUE     
           1024_0  COME_FROM           984  '984'

 L. 710      1024  SETUP_LOOP         1096  'to 1096'
             1026  LOAD_FAST                '_nconvlayer'
             1028  GET_ITER         
           1030_0  COME_FROM          1050  '1050'
             1030  FOR_ITER           1094  'to 1094'
             1032  STORE_FAST               '_i'

 L. 711      1034  LOAD_FAST                '_i'
             1036  LOAD_CONST               False
             1038  COMPARE_OP               is
         1040_1042  POP_JUMP_IF_TRUE   1054  'to 1054'
             1044  LOAD_FAST                '_i'
             1046  LOAD_CONST               1
             1048  COMPARE_OP               <
         1050_1052  POP_JUMP_IF_FALSE  1030  'to 1030'
           1054_0  COME_FROM          1040  '1040'

 L. 712      1054  LOAD_GLOBAL              vis_msg
             1056  LOAD_ATTR                print
             1058  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Non-positive convolutional layer number'

 L. 713      1060  LOAD_STR                 'error'
             1062  LOAD_CONST               ('type',)
             1064  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1066  POP_TOP          

 L. 714      1068  LOAD_GLOBAL              QtWidgets
             1070  LOAD_ATTR                QMessageBox
             1072  LOAD_METHOD              critical
             1074  LOAD_DEREF               'self'
             1076  LOAD_ATTR                msgbox

 L. 715      1078  LOAD_STR                 'Train 3D-CNN'

 L. 716      1080  LOAD_STR                 'Non-positive convolutional layer number'
             1082  CALL_METHOD_3         3  '3 positional arguments'
             1084  POP_TOP          

 L. 717      1086  LOAD_CONST               None
             1088  RETURN_VALUE     
         1090_1092  JUMP_BACK          1030  'to 1030'
             1094  POP_BLOCK        
           1096_0  COME_FROM_LOOP     1024  '1024'

 L. 718      1096  SETUP_LOOP         1168  'to 1168'
             1098  LOAD_FAST                '_nconvfeature'
             1100  GET_ITER         
           1102_0  COME_FROM          1122  '1122'
             1102  FOR_ITER           1166  'to 1166'
             1104  STORE_FAST               '_i'

 L. 719      1106  LOAD_FAST                '_i'
             1108  LOAD_CONST               False
             1110  COMPARE_OP               is
         1112_1114  POP_JUMP_IF_TRUE   1126  'to 1126'
             1116  LOAD_FAST                '_i'
             1118  LOAD_CONST               1
             1120  COMPARE_OP               <
         1122_1124  POP_JUMP_IF_FALSE  1102  'to 1102'
           1126_0  COME_FROM          1112  '1112'

 L. 720      1126  LOAD_GLOBAL              vis_msg
             1128  LOAD_ATTR                print
             1130  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Non-positive convolutional feature number'

 L. 721      1132  LOAD_STR                 'error'
             1134  LOAD_CONST               ('type',)
             1136  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1138  POP_TOP          

 L. 722      1140  LOAD_GLOBAL              QtWidgets
             1142  LOAD_ATTR                QMessageBox
             1144  LOAD_METHOD              critical
             1146  LOAD_DEREF               'self'
             1148  LOAD_ATTR                msgbox

 L. 723      1150  LOAD_STR                 'Train 3D-CNN'

 L. 724      1152  LOAD_STR                 'Non-positive convolutional feature number'
             1154  CALL_METHOD_3         3  '3 positional arguments'
             1156  POP_TOP          

 L. 725      1158  LOAD_CONST               None
             1160  RETURN_VALUE     
         1162_1164  JUMP_BACK          1102  'to 1102'
             1166  POP_BLOCK        
           1168_0  COME_FROM_LOOP     1096  '1096'

 L. 726      1168  LOAD_FAST                '_nfclayer'
             1170  LOAD_CONST               False
             1172  COMPARE_OP               is
         1174_1176  POP_JUMP_IF_TRUE   1188  'to 1188'
             1178  LOAD_FAST                '_nfclayer'
             1180  LOAD_CONST               0
             1182  COMPARE_OP               <=
         1184_1186  POP_JUMP_IF_FALSE  1224  'to 1224'
           1188_0  COME_FROM          1174  '1174'

 L. 727      1188  LOAD_GLOBAL              vis_msg
             1190  LOAD_ATTR                print
             1192  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Non-positive MLP layer number'
             1194  LOAD_STR                 'error'
             1196  LOAD_CONST               ('type',)
             1198  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1200  POP_TOP          

 L. 728      1202  LOAD_GLOBAL              QtWidgets
             1204  LOAD_ATTR                QMessageBox
             1206  LOAD_METHOD              critical
             1208  LOAD_DEREF               'self'
             1210  LOAD_ATTR                msgbox

 L. 729      1212  LOAD_STR                 'Train 3D-CNN'

 L. 730      1214  LOAD_STR                 'Non-positive MLP layer number'
             1216  CALL_METHOD_3         3  '3 positional arguments'
             1218  POP_TOP          

 L. 731      1220  LOAD_CONST               None
             1222  RETURN_VALUE     
           1224_0  COME_FROM          1184  '1184'

 L. 732      1224  SETUP_LOOP         1296  'to 1296'
             1226  LOAD_FAST                '_nfcneuron'
             1228  GET_ITER         
           1230_0  COME_FROM          1250  '1250'
             1230  FOR_ITER           1294  'to 1294'
             1232  STORE_FAST               '_i'

 L. 733      1234  LOAD_FAST                '_i'
             1236  LOAD_CONST               False
             1238  COMPARE_OP               is
         1240_1242  POP_JUMP_IF_TRUE   1254  'to 1254'
             1244  LOAD_FAST                '_i'
             1246  LOAD_CONST               1
             1248  COMPARE_OP               <
         1250_1252  POP_JUMP_IF_FALSE  1230  'to 1230'
           1254_0  COME_FROM          1240  '1240'

 L. 734      1254  LOAD_GLOBAL              vis_msg
             1256  LOAD_ATTR                print
             1258  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Non-positive MLP neuron number'

 L. 735      1260  LOAD_STR                 'error'
             1262  LOAD_CONST               ('type',)
             1264  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1266  POP_TOP          

 L. 736      1268  LOAD_GLOBAL              QtWidgets
             1270  LOAD_ATTR                QMessageBox
             1272  LOAD_METHOD              critical
             1274  LOAD_DEREF               'self'
             1276  LOAD_ATTR                msgbox

 L. 737      1278  LOAD_STR                 'Train 3D-CNN'

 L. 738      1280  LOAD_STR                 'Non-positive MLP neuron number'
             1282  CALL_METHOD_3         3  '3 positional arguments'
             1284  POP_TOP          

 L. 739      1286  LOAD_CONST               None
             1288  RETURN_VALUE     
         1290_1292  JUMP_BACK          1230  'to 1230'
             1294  POP_BLOCK        
           1296_0  COME_FROM_LOOP     1224  '1224'

 L. 740      1296  LOAD_FAST                '_patch_height'
             1298  LOAD_CONST               False
             1300  COMPARE_OP               is
         1302_1304  POP_JUMP_IF_TRUE   1356  'to 1356'
             1306  LOAD_FAST                '_patch_width'
             1308  LOAD_CONST               False
             1310  COMPARE_OP               is
         1312_1314  POP_JUMP_IF_TRUE   1356  'to 1356'
             1316  LOAD_FAST                '_patch_depth'
             1318  LOAD_CONST               False
             1320  COMPARE_OP               is
         1322_1324  POP_JUMP_IF_TRUE   1356  'to 1356'

 L. 741      1326  LOAD_FAST                '_patch_height'
             1328  LOAD_CONST               1
             1330  COMPARE_OP               <
         1332_1334  POP_JUMP_IF_TRUE   1356  'to 1356'
             1336  LOAD_FAST                '_patch_width'
             1338  LOAD_CONST               1
             1340  COMPARE_OP               <
         1342_1344  POP_JUMP_IF_TRUE   1356  'to 1356'
             1346  LOAD_FAST                '_patch_depth'
             1348  LOAD_CONST               1
             1350  COMPARE_OP               <
         1352_1354  POP_JUMP_IF_FALSE  1392  'to 1392'
           1356_0  COME_FROM          1342  '1342'
           1356_1  COME_FROM          1332  '1332'
           1356_2  COME_FROM          1322  '1322'
           1356_3  COME_FROM          1312  '1312'
           1356_4  COME_FROM          1302  '1302'

 L. 742      1356  LOAD_GLOBAL              vis_msg
             1358  LOAD_ATTR                print
             1360  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Non-positive convolutional patch size'

 L. 743      1362  LOAD_STR                 'error'
             1364  LOAD_CONST               ('type',)
             1366  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1368  POP_TOP          

 L. 744      1370  LOAD_GLOBAL              QtWidgets
             1372  LOAD_ATTR                QMessageBox
             1374  LOAD_METHOD              critical
             1376  LOAD_DEREF               'self'
             1378  LOAD_ATTR                msgbox

 L. 745      1380  LOAD_STR                 'Train 3D-CNN'

 L. 746      1382  LOAD_STR                 'Non-positive convolutional patch size'
             1384  CALL_METHOD_3         3  '3 positional arguments'
             1386  POP_TOP          

 L. 747      1388  LOAD_CONST               None
             1390  RETURN_VALUE     
           1392_0  COME_FROM          1352  '1352'

 L. 748      1392  LOAD_FAST                '_pool_height'
             1394  LOAD_CONST               False
             1396  COMPARE_OP               is
         1398_1400  POP_JUMP_IF_TRUE   1452  'to 1452'
             1402  LOAD_FAST                '_pool_width'
             1404  LOAD_CONST               False
             1406  COMPARE_OP               is
         1408_1410  POP_JUMP_IF_TRUE   1452  'to 1452'
             1412  LOAD_FAST                '_pool_depth'
             1414  LOAD_CONST               False
             1416  COMPARE_OP               is
         1418_1420  POP_JUMP_IF_TRUE   1452  'to 1452'

 L. 749      1422  LOAD_FAST                '_pool_height'
             1424  LOAD_CONST               1
             1426  COMPARE_OP               <
         1428_1430  POP_JUMP_IF_TRUE   1452  'to 1452'
             1432  LOAD_FAST                '_pool_width'
             1434  LOAD_CONST               1
             1436  COMPARE_OP               <
         1438_1440  POP_JUMP_IF_TRUE   1452  'to 1452'
             1442  LOAD_FAST                '_pool_depth'
             1444  LOAD_CONST               1
             1446  COMPARE_OP               <
         1448_1450  POP_JUMP_IF_FALSE  1488  'to 1488'
           1452_0  COME_FROM          1438  '1438'
           1452_1  COME_FROM          1428  '1428'
           1452_2  COME_FROM          1418  '1418'
           1452_3  COME_FROM          1408  '1408'
           1452_4  COME_FROM          1398  '1398'

 L. 750      1452  LOAD_GLOBAL              vis_msg
             1454  LOAD_ATTR                print
             1456  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Non-positive pooling size'

 L. 751      1458  LOAD_STR                 'error'
             1460  LOAD_CONST               ('type',)
             1462  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1464  POP_TOP          

 L. 752      1466  LOAD_GLOBAL              QtWidgets
             1468  LOAD_ATTR                QMessageBox
             1470  LOAD_METHOD              critical
             1472  LOAD_DEREF               'self'
             1474  LOAD_ATTR                msgbox

 L. 753      1476  LOAD_STR                 'Train 3D-CNN'

 L. 754      1478  LOAD_STR                 'Non-positive pooling size'
             1480  CALL_METHOD_3         3  '3 positional arguments'
             1482  POP_TOP          

 L. 755      1484  LOAD_CONST               None
             1486  RETURN_VALUE     
           1488_0  COME_FROM          1448  '1448'

 L. 756      1488  LOAD_FAST                '_nepoch'
             1490  LOAD_CONST               False
             1492  COMPARE_OP               is
         1494_1496  POP_JUMP_IF_TRUE   1508  'to 1508'
             1498  LOAD_FAST                '_nepoch'
             1500  LOAD_CONST               0
             1502  COMPARE_OP               <=
         1504_1506  POP_JUMP_IF_FALSE  1544  'to 1544'
           1508_0  COME_FROM          1494  '1494'

 L. 757      1508  LOAD_GLOBAL              vis_msg
             1510  LOAD_ATTR                print
             1512  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Non-positive epoch number'
             1514  LOAD_STR                 'error'
             1516  LOAD_CONST               ('type',)
             1518  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1520  POP_TOP          

 L. 758      1522  LOAD_GLOBAL              QtWidgets
             1524  LOAD_ATTR                QMessageBox
             1526  LOAD_METHOD              critical
             1528  LOAD_DEREF               'self'
             1530  LOAD_ATTR                msgbox

 L. 759      1532  LOAD_STR                 'Train 3D-CNN'

 L. 760      1534  LOAD_STR                 'Non-positive epoch number'
             1536  CALL_METHOD_3         3  '3 positional arguments'
             1538  POP_TOP          

 L. 761      1540  LOAD_CONST               None
             1542  RETURN_VALUE     
           1544_0  COME_FROM          1504  '1504'

 L. 762      1544  LOAD_FAST                '_batchsize'
             1546  LOAD_CONST               False
             1548  COMPARE_OP               is
         1550_1552  POP_JUMP_IF_TRUE   1564  'to 1564'
             1554  LOAD_FAST                '_batchsize'
             1556  LOAD_CONST               0
             1558  COMPARE_OP               <=
         1560_1562  POP_JUMP_IF_FALSE  1600  'to 1600'
           1564_0  COME_FROM          1550  '1550'

 L. 763      1564  LOAD_GLOBAL              vis_msg
             1566  LOAD_ATTR                print
             1568  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Non-positive batch size'
             1570  LOAD_STR                 'error'
             1572  LOAD_CONST               ('type',)
             1574  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1576  POP_TOP          

 L. 764      1578  LOAD_GLOBAL              QtWidgets
             1580  LOAD_ATTR                QMessageBox
             1582  LOAD_METHOD              critical
             1584  LOAD_DEREF               'self'
             1586  LOAD_ATTR                msgbox

 L. 765      1588  LOAD_STR                 'Train 3D-CNN'

 L. 766      1590  LOAD_STR                 'Non-positive batch size'
             1592  CALL_METHOD_3         3  '3 positional arguments'
             1594  POP_TOP          

 L. 767      1596  LOAD_CONST               None
             1598  RETURN_VALUE     
           1600_0  COME_FROM          1560  '1560'

 L. 768      1600  LOAD_FAST                '_learning_rate'
             1602  LOAD_CONST               False
             1604  COMPARE_OP               is
         1606_1608  POP_JUMP_IF_TRUE   1620  'to 1620'
             1610  LOAD_FAST                '_learning_rate'
             1612  LOAD_CONST               0
             1614  COMPARE_OP               <=
         1616_1618  POP_JUMP_IF_FALSE  1656  'to 1656'
           1620_0  COME_FROM          1606  '1606'

 L. 769      1620  LOAD_GLOBAL              vis_msg
             1622  LOAD_ATTR                print
             1624  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Non-positive learning rate'
             1626  LOAD_STR                 'error'
             1628  LOAD_CONST               ('type',)
             1630  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1632  POP_TOP          

 L. 770      1634  LOAD_GLOBAL              QtWidgets
             1636  LOAD_ATTR                QMessageBox
             1638  LOAD_METHOD              critical
             1640  LOAD_DEREF               'self'
             1642  LOAD_ATTR                msgbox

 L. 771      1644  LOAD_STR                 'Train 3D-CNN'

 L. 772      1646  LOAD_STR                 'Non-positive learning rate'
             1648  CALL_METHOD_3         3  '3 positional arguments'
             1650  POP_TOP          

 L. 773      1652  LOAD_CONST               None
             1654  RETURN_VALUE     
           1656_0  COME_FROM          1616  '1616'

 L. 774      1656  LOAD_FAST                '_dropout_prob_fclayer'
             1658  LOAD_CONST               False
             1660  COMPARE_OP               is
         1662_1664  POP_JUMP_IF_TRUE   1676  'to 1676'
             1666  LOAD_FAST                '_dropout_prob_fclayer'
             1668  LOAD_CONST               0
             1670  COMPARE_OP               <=
         1672_1674  POP_JUMP_IF_FALSE  1712  'to 1712'
           1676_0  COME_FROM          1662  '1662'

 L. 775      1676  LOAD_GLOBAL              vis_msg
             1678  LOAD_ATTR                print
             1680  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: Negative dropout rate'
             1682  LOAD_STR                 'error'
             1684  LOAD_CONST               ('type',)
             1686  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1688  POP_TOP          

 L. 776      1690  LOAD_GLOBAL              QtWidgets
             1692  LOAD_ATTR                QMessageBox
             1694  LOAD_METHOD              critical
             1696  LOAD_DEREF               'self'
             1698  LOAD_ATTR                msgbox

 L. 777      1700  LOAD_STR                 'Train 3D-CNN'

 L. 778      1702  LOAD_STR                 'Negative dropout rate'
             1704  CALL_METHOD_3         3  '3 positional arguments'
             1706  POP_TOP          

 L. 779      1708  LOAD_CONST               None
             1710  RETURN_VALUE     
           1712_0  COME_FROM          1672  '1672'

 L. 781      1712  LOAD_GLOBAL              len
             1714  LOAD_DEREF               'self'
             1716  LOAD_ATTR                ldtsave
             1718  LOAD_METHOD              text
             1720  CALL_METHOD_0         0  '0 positional arguments'
             1722  CALL_FUNCTION_1       1  '1 positional argument'
             1724  LOAD_CONST               1
             1726  COMPARE_OP               <
         1728_1730  POP_JUMP_IF_FALSE  1768  'to 1768'

 L. 782      1732  LOAD_GLOBAL              vis_msg
             1734  LOAD_ATTR                print
             1736  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: No name specified for CNN network'
             1738  LOAD_STR                 'error'
             1740  LOAD_CONST               ('type',)
             1742  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1744  POP_TOP          

 L. 783      1746  LOAD_GLOBAL              QtWidgets
             1748  LOAD_ATTR                QMessageBox
             1750  LOAD_METHOD              critical
             1752  LOAD_DEREF               'self'
             1754  LOAD_ATTR                msgbox

 L. 784      1756  LOAD_STR                 'Train 3D-CNN'

 L. 785      1758  LOAD_STR                 'No name specified for CNN network'
             1760  CALL_METHOD_3         3  '3 positional arguments'
             1762  POP_TOP          

 L. 786      1764  LOAD_CONST               None
             1766  RETURN_VALUE     
           1768_0  COME_FROM          1728  '1728'

 L. 787      1768  LOAD_GLOBAL              os
             1770  LOAD_ATTR                path
             1772  LOAD_METHOD              dirname
             1774  LOAD_DEREF               'self'
             1776  LOAD_ATTR                ldtsave
             1778  LOAD_METHOD              text
             1780  CALL_METHOD_0         0  '0 positional arguments'
             1782  CALL_METHOD_1         1  '1 positional argument'
             1784  STORE_FAST               '_savepath'

 L. 788      1786  LOAD_GLOBAL              os
             1788  LOAD_ATTR                path
             1790  LOAD_METHOD              splitext
             1792  LOAD_GLOBAL              os
             1794  LOAD_ATTR                path
             1796  LOAD_METHOD              basename
             1798  LOAD_DEREF               'self'
             1800  LOAD_ATTR                ldtsave
             1802  LOAD_METHOD              text
             1804  CALL_METHOD_0         0  '0 positional arguments'
             1806  CALL_METHOD_1         1  '1 positional argument'
             1808  CALL_METHOD_1         1  '1 positional argument'
             1810  LOAD_CONST               0
             1812  BINARY_SUBSCR    
             1814  STORE_FAST               '_savename'

 L. 790      1816  LOAD_GLOBAL              int
             1818  LOAD_FAST                '_video_depth_old'
             1820  LOAD_CONST               2
             1822  BINARY_TRUE_DIVIDE
             1824  CALL_FUNCTION_1       1  '1 positional argument'
             1826  STORE_FAST               '_wdinl'

 L. 791      1828  LOAD_GLOBAL              int
             1830  LOAD_FAST                '_video_width_old'
             1832  LOAD_CONST               2
             1834  BINARY_TRUE_DIVIDE
             1836  CALL_FUNCTION_1       1  '1 positional argument'
             1838  STORE_FAST               '_wdxl'

 L. 792      1840  LOAD_GLOBAL              int
             1842  LOAD_FAST                '_video_height_old'
             1844  LOAD_CONST               2
             1846  BINARY_TRUE_DIVIDE
             1848  CALL_FUNCTION_1       1  '1 positional argument'
             1850  STORE_FAST               '_wdz'

 L. 794      1852  LOAD_DEREF               'self'
             1854  LOAD_ATTR                survinfo
             1856  STORE_FAST               '_seisinfo'

 L. 796      1858  LOAD_GLOBAL              print
             1860  LOAD_STR                 'TrainMl3DCnnFromExistingFromScratch: Step 1 - Get training samples:'
             1862  CALL_FUNCTION_1       1  '1 positional argument'
             1864  POP_TOP          

 L. 797      1866  LOAD_DEREF               'self'
             1868  LOAD_ATTR                traindataconfig
             1870  LOAD_STR                 'TrainPointSet'
             1872  BINARY_SUBSCR    
             1874  STORE_FAST               '_trainpoint'

 L. 798      1876  LOAD_GLOBAL              np
             1878  LOAD_METHOD              zeros
             1880  LOAD_CONST               0
             1882  LOAD_CONST               3
             1884  BUILD_LIST_2          2 
             1886  CALL_METHOD_1         1  '1 positional argument'
             1888  STORE_FAST               '_traindata'

 L. 799      1890  SETUP_LOOP         1966  'to 1966'
             1892  LOAD_FAST                '_trainpoint'
             1894  GET_ITER         
           1896_0  COME_FROM          1914  '1914'
             1896  FOR_ITER           1964  'to 1964'
             1898  STORE_FAST               '_p'

 L. 800      1900  LOAD_GLOBAL              point_ays
             1902  LOAD_METHOD              checkPoint
             1904  LOAD_DEREF               'self'
             1906  LOAD_ATTR                pointsetdata
             1908  LOAD_FAST                '_p'
             1910  BINARY_SUBSCR    
             1912  CALL_METHOD_1         1  '1 positional argument'
         1914_1916  POP_JUMP_IF_FALSE  1896  'to 1896'

 L. 801      1918  LOAD_GLOBAL              basic_mdt
             1920  LOAD_METHOD              exportMatDict
             1922  LOAD_DEREF               'self'
             1924  LOAD_ATTR                pointsetdata
             1926  LOAD_FAST                '_p'
             1928  BINARY_SUBSCR    
             1930  LOAD_STR                 'Inline'
             1932  LOAD_STR                 'Crossline'
             1934  LOAD_STR                 'Z'
             1936  BUILD_LIST_3          3 
             1938  CALL_METHOD_2         2  '2 positional arguments'
             1940  STORE_FAST               '_pt'

 L. 802      1942  LOAD_GLOBAL              np
             1944  LOAD_ATTR                concatenate
             1946  LOAD_FAST                '_traindata'
             1948  LOAD_FAST                '_pt'
             1950  BUILD_TUPLE_2         2 
             1952  LOAD_CONST               0
             1954  LOAD_CONST               ('axis',)
             1956  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1958  STORE_FAST               '_traindata'
         1960_1962  JUMP_BACK          1896  'to 1896'
             1964  POP_BLOCK        
           1966_0  COME_FROM_LOOP     1890  '1890'

 L. 803      1966  LOAD_GLOBAL              seis_ays
             1968  LOAD_ATTR                removeOutofSurveySample
             1970  LOAD_FAST                '_traindata'

 L. 804      1972  LOAD_FAST                '_seisinfo'
             1974  LOAD_STR                 'ILStart'
             1976  BINARY_SUBSCR    
             1978  LOAD_FAST                '_wdinl'
             1980  LOAD_FAST                '_seisinfo'
             1982  LOAD_STR                 'ILStep'
             1984  BINARY_SUBSCR    
             1986  BINARY_MULTIPLY  
             1988  BINARY_ADD       

 L. 805      1990  LOAD_FAST                '_seisinfo'
             1992  LOAD_STR                 'ILEnd'
             1994  BINARY_SUBSCR    
             1996  LOAD_FAST                '_wdinl'
             1998  LOAD_FAST                '_seisinfo'
             2000  LOAD_STR                 'ILStep'
             2002  BINARY_SUBSCR    
             2004  BINARY_MULTIPLY  
             2006  BINARY_SUBTRACT  

 L. 806      2008  LOAD_FAST                '_seisinfo'
             2010  LOAD_STR                 'XLStart'
             2012  BINARY_SUBSCR    
             2014  LOAD_FAST                '_wdxl'
             2016  LOAD_FAST                '_seisinfo'
             2018  LOAD_STR                 'XLStep'
             2020  BINARY_SUBSCR    
             2022  BINARY_MULTIPLY  
             2024  BINARY_ADD       

 L. 807      2026  LOAD_FAST                '_seisinfo'
             2028  LOAD_STR                 'XLEnd'
             2030  BINARY_SUBSCR    
             2032  LOAD_FAST                '_wdxl'
             2034  LOAD_FAST                '_seisinfo'
             2036  LOAD_STR                 'XLStep'
             2038  BINARY_SUBSCR    
             2040  BINARY_MULTIPLY  
             2042  BINARY_SUBTRACT  

 L. 808      2044  LOAD_FAST                '_seisinfo'
             2046  LOAD_STR                 'ZStart'
             2048  BINARY_SUBSCR    
             2050  LOAD_FAST                '_wdz'
             2052  LOAD_FAST                '_seisinfo'
             2054  LOAD_STR                 'ZStep'
             2056  BINARY_SUBSCR    
             2058  BINARY_MULTIPLY  
             2060  BINARY_ADD       

 L. 809      2062  LOAD_FAST                '_seisinfo'
             2064  LOAD_STR                 'ZEnd'
             2066  BINARY_SUBSCR    
             2068  LOAD_FAST                '_wdz'
             2070  LOAD_FAST                '_seisinfo'
             2072  LOAD_STR                 'ZStep'
             2074  BINARY_SUBSCR    
             2076  BINARY_MULTIPLY  
             2078  BINARY_SUBTRACT  
             2080  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             2082  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2084  STORE_FAST               '_traindata'

 L. 812      2086  LOAD_GLOBAL              np
             2088  LOAD_METHOD              shape
             2090  LOAD_FAST                '_traindata'
             2092  CALL_METHOD_1         1  '1 positional argument'
             2094  LOAD_CONST               0
             2096  BINARY_SUBSCR    
             2098  LOAD_CONST               0
             2100  COMPARE_OP               <=
         2102_2104  POP_JUMP_IF_FALSE  2142  'to 2142'

 L. 813      2106  LOAD_GLOBAL              vis_msg
             2108  LOAD_ATTR                print
             2110  LOAD_STR                 'ERROR TrainMl3DCnnFromExisting: No training sample found'
             2112  LOAD_STR                 'error'
             2114  LOAD_CONST               ('type',)
             2116  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2118  POP_TOP          

 L. 814      2120  LOAD_GLOBAL              QtWidgets
             2122  LOAD_ATTR                QMessageBox
             2124  LOAD_METHOD              critical
             2126  LOAD_DEREF               'self'
             2128  LOAD_ATTR                msgbox

 L. 815      2130  LOAD_STR                 'Train 3D-CNN'

 L. 816      2132  LOAD_STR                 'No training sample found'
             2134  CALL_METHOD_3         3  '3 positional arguments'
             2136  POP_TOP          

 L. 817      2138  LOAD_CONST               None
             2140  RETURN_VALUE     
           2142_0  COME_FROM          2102  '2102'

 L. 820      2142  LOAD_GLOBAL              print
             2144  LOAD_STR                 'TrainMl3DCnnFromExisting: Step 2 - Retrieve and interpolate videos: (%d, %d, %d) --> (%d, %d, %d)'

 L. 821      2146  LOAD_FAST                '_video_height_old'
             2148  LOAD_FAST                '_video_width_old'
             2150  LOAD_FAST                '_video_depth_old'

 L. 822      2152  LOAD_FAST                '_video_height_new'
             2154  LOAD_FAST                '_video_width_new'
             2156  LOAD_FAST                '_video_depth_new'
             2158  BUILD_TUPLE_6         6 
             2160  BINARY_MODULO    
             2162  CALL_FUNCTION_1       1  '1 positional argument'
             2164  POP_TOP          

 L. 823      2166  BUILD_MAP_0           0 
             2168  STORE_FAST               '_traindict'

 L. 824      2170  SETUP_LOOP         2242  'to 2242'
             2172  LOAD_FAST                '_features'
             2174  GET_ITER         
             2176  FOR_ITER           2240  'to 2240'
             2178  STORE_FAST               'f'

 L. 825      2180  LOAD_DEREF               'self'
             2182  LOAD_ATTR                seisdata
             2184  LOAD_FAST                'f'
             2186  BINARY_SUBSCR    
             2188  STORE_FAST               '_seisdata'

 L. 826      2190  LOAD_GLOBAL              seis_ays
             2192  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2194  LOAD_FAST                '_seisdata'
             2196  LOAD_FAST                '_traindata'
             2198  LOAD_DEREF               'self'
             2200  LOAD_ATTR                survinfo

 L. 827      2202  LOAD_FAST                '_wdinl'
             2204  LOAD_FAST                '_wdxl'
             2206  LOAD_FAST                '_wdz'

 L. 828      2208  LOAD_CONST               False
             2210  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2212  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2214  LOAD_CONST               None
             2216  LOAD_CONST               None
             2218  BUILD_SLICE_2         2 
             2220  LOAD_CONST               3
             2222  LOAD_CONST               None
             2224  BUILD_SLICE_2         2 
             2226  BUILD_TUPLE_2         2 
             2228  BINARY_SUBSCR    
             2230  LOAD_FAST                '_traindict'
             2232  LOAD_FAST                'f'
             2234  STORE_SUBSCR     
         2236_2238  JUMP_BACK          2176  'to 2176'
             2240  POP_BLOCK        
           2242_0  COME_FROM_LOOP     2170  '2170'

 L. 829      2242  LOAD_FAST                '_target'
             2244  LOAD_FAST                '_features'
             2246  COMPARE_OP               not-in
         2248_2250  POP_JUMP_IF_FALSE  2302  'to 2302'

 L. 830      2252  LOAD_DEREF               'self'
             2254  LOAD_ATTR                seisdata
             2256  LOAD_FAST                '_target'
             2258  BINARY_SUBSCR    
             2260  STORE_FAST               '_seisdata'

 L. 831      2262  LOAD_GLOBAL              seis_ays
             2264  LOAD_ATTR                retrieveSeisSampleFrom3DMat
             2266  LOAD_FAST                '_seisdata'
             2268  LOAD_FAST                '_traindata'
             2270  LOAD_DEREF               'self'
             2272  LOAD_ATTR                survinfo

 L. 832      2274  LOAD_CONST               False
             2276  LOAD_CONST               ('seisinfo', 'verbose')
             2278  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2280  LOAD_CONST               None
             2282  LOAD_CONST               None
             2284  BUILD_SLICE_2         2 
             2286  LOAD_CONST               3
             2288  LOAD_CONST               None
             2290  BUILD_SLICE_2         2 
             2292  BUILD_TUPLE_2         2 
             2294  BINARY_SUBSCR    
             2296  LOAD_FAST                '_traindict'
             2298  LOAD_FAST                '_target'
             2300  STORE_SUBSCR     
           2302_0  COME_FROM          2248  '2248'

 L. 834      2302  LOAD_DEREF               'self'
             2304  LOAD_ATTR                traindataconfig
             2306  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2308  BINARY_SUBSCR    
         2310_2312  POP_JUMP_IF_FALSE  2394  'to 2394'

 L. 835      2314  SETUP_LOOP         2394  'to 2394'
             2316  LOAD_FAST                '_features'
             2318  GET_ITER         
           2320_0  COME_FROM          2348  '2348'
             2320  FOR_ITER           2392  'to 2392'
             2322  STORE_FAST               'f'

 L. 836      2324  LOAD_GLOBAL              ml_aug
             2326  LOAD_METHOD              removeInvariantFeature
             2328  LOAD_FAST                '_traindict'
             2330  LOAD_FAST                'f'
             2332  CALL_METHOD_2         2  '2 positional arguments'
             2334  STORE_FAST               '_traindict'

 L. 837      2336  LOAD_GLOBAL              basic_mdt
             2338  LOAD_METHOD              maxDictConstantRow
             2340  LOAD_FAST                '_traindict'
             2342  CALL_METHOD_1         1  '1 positional argument'
             2344  LOAD_CONST               0
             2346  COMPARE_OP               <=
         2348_2350  POP_JUMP_IF_FALSE  2320  'to 2320'

 L. 838      2352  LOAD_GLOBAL              vis_msg
             2354  LOAD_ATTR                print
             2356  LOAD_STR                 'ERROR in TrainMl3DCnnFromExisting: No training sample found'
             2358  LOAD_STR                 'error'
             2360  LOAD_CONST               ('type',)
             2362  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2364  POP_TOP          

 L. 839      2366  LOAD_GLOBAL              QtWidgets
             2368  LOAD_ATTR                QMessageBox
             2370  LOAD_METHOD              critical
             2372  LOAD_DEREF               'self'
             2374  LOAD_ATTR                msgbox

 L. 840      2376  LOAD_STR                 'Train 3D-CNN'

 L. 841      2378  LOAD_STR                 'No training sample found'
             2380  CALL_METHOD_3         3  '3 positional arguments'
             2382  POP_TOP          

 L. 842      2384  LOAD_CONST               None
             2386  RETURN_VALUE     
         2388_2390  JUMP_BACK          2320  'to 2320'
             2392  POP_BLOCK        
           2394_0  COME_FROM_LOOP     2314  '2314'
           2394_1  COME_FROM          2310  '2310'

 L. 844      2394  LOAD_GLOBAL              np
             2396  LOAD_METHOD              round
             2398  LOAD_FAST                '_traindict'
             2400  LOAD_FAST                '_target'
             2402  BINARY_SUBSCR    
             2404  CALL_METHOD_1         1  '1 positional argument'
             2406  LOAD_METHOD              astype
             2408  LOAD_GLOBAL              int
             2410  CALL_METHOD_1         1  '1 positional argument'
             2412  LOAD_FAST                '_traindict'
             2414  LOAD_FAST                '_target'
             2416  STORE_SUBSCR     

 L. 846      2418  LOAD_FAST                '_video_height_new'
             2420  LOAD_FAST                '_video_height_old'
             2422  COMPARE_OP               !=
         2424_2426  POP_JUMP_IF_TRUE   2448  'to 2448'

 L. 847      2428  LOAD_FAST                '_video_width_new'
             2430  LOAD_FAST                '_video_width_old'
             2432  COMPARE_OP               !=
         2434_2436  POP_JUMP_IF_TRUE   2448  'to 2448'

 L. 848      2438  LOAD_FAST                '_video_depth_new'
             2440  LOAD_FAST                '_video_depth_old'
             2442  COMPARE_OP               !=
         2444_2446  POP_JUMP_IF_FALSE  2496  'to 2496'
           2448_0  COME_FROM          2434  '2434'
           2448_1  COME_FROM          2424  '2424'

 L. 849      2448  SETUP_LOOP         2496  'to 2496'
             2450  LOAD_FAST                '_features'
             2452  GET_ITER         
             2454  FOR_ITER           2494  'to 2494'
             2456  STORE_FAST               'f'

 L. 850      2458  LOAD_GLOBAL              basic_video
             2460  LOAD_ATTR                changeVideoSize
             2462  LOAD_FAST                '_traindict'
             2464  LOAD_FAST                'f'
             2466  BINARY_SUBSCR    

 L. 851      2468  LOAD_FAST                '_video_height_old'

 L. 852      2470  LOAD_FAST                '_video_width_old'

 L. 853      2472  LOAD_FAST                '_video_depth_old'

 L. 854      2474  LOAD_FAST                '_video_height_new'

 L. 855      2476  LOAD_FAST                '_video_width_new'

 L. 856      2478  LOAD_FAST                '_video_depth_new'
             2480  LOAD_CONST               ('video_height', 'video_width', 'video_depth', 'video_height_new', 'video_width_new', 'video_depth_new')
             2482  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2484  LOAD_FAST                '_traindict'
             2486  LOAD_FAST                'f'
             2488  STORE_SUBSCR     
         2490_2492  JUMP_BACK          2454  'to 2454'
             2494  POP_BLOCK        
           2496_0  COME_FROM_LOOP     2448  '2448'
           2496_1  COME_FROM          2444  '2444'

 L. 858      2496  LOAD_GLOBAL              print
             2498  LOAD_STR                 'TrainMl3DCnnFromExisting: A total of %d valid training samples'

 L. 859      2500  LOAD_GLOBAL              basic_mdt
             2502  LOAD_METHOD              maxDictConstantRow
             2504  LOAD_FAST                '_traindict'
             2506  CALL_METHOD_1         1  '1 positional argument'
             2508  BINARY_MODULO    
             2510  CALL_FUNCTION_1       1  '1 positional argument'
             2512  POP_TOP          

 L. 861      2514  LOAD_GLOBAL              print
             2516  LOAD_STR                 'TrainMl3DCnnFromExisting: Step 3 - Balance labels'
             2518  CALL_FUNCTION_1       1  '1 positional argument'
             2520  POP_TOP          

 L. 862      2522  LOAD_DEREF               'self'
             2524  LOAD_ATTR                traindataconfig
             2526  LOAD_STR                 'BalanceTarget_Checked'
             2528  BINARY_SUBSCR    
         2530_2532  POP_JUMP_IF_FALSE  2574  'to 2574'

 L. 863      2534  LOAD_GLOBAL              ml_aug
             2536  LOAD_METHOD              balanceLabelbyExtension
             2538  LOAD_FAST                '_traindict'
             2540  LOAD_FAST                '_target'
             2542  CALL_METHOD_2         2  '2 positional arguments'
             2544  STORE_FAST               '_traindict'

 L. 864      2546  LOAD_GLOBAL              print

 L. 865      2548  LOAD_STR                 'TrainMl2DCnnFromScratch: A total of %d training samples after balance'

 L. 866      2550  LOAD_GLOBAL              np
             2552  LOAD_METHOD              shape
             2554  LOAD_FAST                '_traindict'
             2556  LOAD_FAST                '_target'
             2558  BINARY_SUBSCR    
             2560  CALL_METHOD_1         1  '1 positional argument'
             2562  LOAD_CONST               0
             2564  BINARY_SUBSCR    
             2566  BINARY_MODULO    
             2568  CALL_FUNCTION_1       1  '1 positional argument'
             2570  POP_TOP          
             2572  JUMP_FORWARD       2582  'to 2582'
           2574_0  COME_FROM          2530  '2530'

 L. 868      2574  LOAD_GLOBAL              print
             2576  LOAD_STR                 'TrainMl2DCnnFromScratch: No balance applied'
             2578  CALL_FUNCTION_1       1  '1 positional argument'
             2580  POP_TOP          
           2582_0  COME_FROM          2572  '2572'

 L. 870      2582  LOAD_GLOBAL              print
             2584  LOAD_STR                 'TrainMl3DCnnFromExisting: Step 4 - Start training'
             2586  CALL_FUNCTION_1       1  '1 positional argument'
             2588  POP_TOP          

 L. 872      2590  LOAD_GLOBAL              QtWidgets
             2592  LOAD_METHOD              QProgressDialog
             2594  CALL_METHOD_0         0  '0 positional arguments'
             2596  STORE_FAST               '_pgsdlg'

 L. 873      2598  LOAD_GLOBAL              QtGui
             2600  LOAD_METHOD              QIcon
             2602  CALL_METHOD_0         0  '0 positional arguments'
             2604  STORE_FAST               'icon'

 L. 874      2606  LOAD_FAST                'icon'
             2608  LOAD_METHOD              addPixmap
             2610  LOAD_GLOBAL              QtGui
             2612  LOAD_METHOD              QPixmap
             2614  LOAD_GLOBAL              os
             2616  LOAD_ATTR                path
             2618  LOAD_METHOD              join
             2620  LOAD_DEREF               'self'
             2622  LOAD_ATTR                iconpath
             2624  LOAD_STR                 'icons/new.png'
             2626  CALL_METHOD_2         2  '2 positional arguments'
             2628  CALL_METHOD_1         1  '1 positional argument'

 L. 875      2630  LOAD_GLOBAL              QtGui
             2632  LOAD_ATTR                QIcon
             2634  LOAD_ATTR                Normal
             2636  LOAD_GLOBAL              QtGui
             2638  LOAD_ATTR                QIcon
             2640  LOAD_ATTR                Off
             2642  CALL_METHOD_3         3  '3 positional arguments'
             2644  POP_TOP          

 L. 876      2646  LOAD_FAST                '_pgsdlg'
             2648  LOAD_METHOD              setWindowIcon
             2650  LOAD_FAST                'icon'
             2652  CALL_METHOD_1         1  '1 positional argument'
             2654  POP_TOP          

 L. 877      2656  LOAD_FAST                '_pgsdlg'
             2658  LOAD_METHOD              setWindowTitle
             2660  LOAD_STR                 'Train 3D-CNN'
             2662  CALL_METHOD_1         1  '1 positional argument'
             2664  POP_TOP          

 L. 878      2666  LOAD_FAST                '_pgsdlg'
             2668  LOAD_METHOD              setCancelButton
             2670  LOAD_CONST               None
             2672  CALL_METHOD_1         1  '1 positional argument'
             2674  POP_TOP          

 L. 879      2676  LOAD_FAST                '_pgsdlg'
             2678  LOAD_METHOD              setWindowFlags
             2680  LOAD_GLOBAL              QtCore
             2682  LOAD_ATTR                Qt
             2684  LOAD_ATTR                WindowStaysOnTopHint
             2686  CALL_METHOD_1         1  '1 positional argument'
             2688  POP_TOP          

 L. 880      2690  LOAD_FAST                '_pgsdlg'
             2692  LOAD_METHOD              forceShow
             2694  CALL_METHOD_0         0  '0 positional arguments'
             2696  POP_TOP          

 L. 881      2698  LOAD_FAST                '_pgsdlg'
             2700  LOAD_METHOD              setFixedWidth
             2702  LOAD_CONST               400
             2704  CALL_METHOD_1         1  '1 positional argument'
             2706  POP_TOP          

 L. 882      2708  LOAD_GLOBAL              ml_cnn3d
             2710  LOAD_ATTR                create3DCNNClassifierFromExisting
             2712  LOAD_FAST                '_traindict'

 L. 883      2714  LOAD_FAST                '_video_height_new'

 L. 884      2716  LOAD_FAST                '_video_width_new'

 L. 885      2718  LOAD_FAST                '_video_depth_new'

 L. 886      2720  LOAD_FAST                '_features'
             2722  LOAD_FAST                '_target'

 L. 887      2724  LOAD_FAST                '_nepoch'
             2726  LOAD_FAST                '_batchsize'

 L. 888      2728  LOAD_FAST                '_nconvblock'

 L. 889      2730  LOAD_FAST                '_nconvlayer'
             2732  LOAD_FAST                '_nconvfeature'

 L. 890      2734  LOAD_FAST                '_nfclayer'
             2736  LOAD_FAST                '_nfcneuron'

 L. 891      2738  LOAD_FAST                '_pool_height'
             2740  LOAD_FAST                '_pool_width'

 L. 892      2742  LOAD_FAST                '_pool_depth'

 L. 893      2744  LOAD_FAST                '_learning_rate'

 L. 894      2746  LOAD_FAST                '_dropout_prob_fclayer'

 L. 895      2748  LOAD_CONST               True

 L. 896      2750  LOAD_FAST                '_savepath'
             2752  LOAD_FAST                '_savename'

 L. 897      2754  LOAD_FAST                '_pgsdlg'

 L. 898      2756  LOAD_FAST                '_precnnpath'

 L. 899      2758  LOAD_FAST                '_precnnname'

 L. 900      2760  LOAD_FAST                '_blockidx'
             2762  LOAD_FAST                '_layeridx'

 L. 901      2764  LOAD_FAST                '_trainable'
             2766  LOAD_CONST               ('videoheight', 'videowidth', 'videodepth', 'features', 'target', 'nepoch', 'batchsize', 'nconvblock', 'nconvlayer', 'nconvfeature', 'nfclayer', 'nfcneuron', 'poolheight', 'poolwidth', 'pooldepth', 'learningrate', 'dropoutprobfclayer', 'save2disk', 'savepath', 'savename', 'qpgsdlg', 'precnnpath', 'precnnname', 'blockidx', 'layeridx', 'trainable')
             2768  CALL_FUNCTION_KW_27    27  '27 total positional and keyword args'
             2770  STORE_FAST               '_cnnlog'

 L. 904      2772  LOAD_GLOBAL              QtWidgets
             2774  LOAD_ATTR                QMessageBox
             2776  LOAD_METHOD              information
             2778  LOAD_DEREF               'self'
             2780  LOAD_ATTR                msgbox

 L. 905      2782  LOAD_STR                 'Train 3D-CNN'

 L. 906      2784  LOAD_STR                 'CNN trained successfully'
             2786  CALL_METHOD_3         3  '3 positional arguments'
             2788  POP_TOP          

 L. 908      2790  LOAD_GLOBAL              QtWidgets
             2792  LOAD_ATTR                QMessageBox
             2794  LOAD_METHOD              question
             2796  LOAD_DEREF               'self'
             2798  LOAD_ATTR                msgbox
             2800  LOAD_STR                 'Train 3D-CNN'
             2802  LOAD_STR                 'View learning matrix?'

 L. 909      2804  LOAD_GLOBAL              QtWidgets
             2806  LOAD_ATTR                QMessageBox
             2808  LOAD_ATTR                Yes
             2810  LOAD_GLOBAL              QtWidgets
             2812  LOAD_ATTR                QMessageBox
             2814  LOAD_ATTR                No
             2816  BINARY_OR        

 L. 910      2818  LOAD_GLOBAL              QtWidgets
             2820  LOAD_ATTR                QMessageBox
             2822  LOAD_ATTR                Yes
             2824  CALL_METHOD_5         5  '5 positional arguments'
             2826  STORE_FAST               'reply'

 L. 912      2828  LOAD_FAST                'reply'
             2830  LOAD_GLOBAL              QtWidgets
             2832  LOAD_ATTR                QMessageBox
             2834  LOAD_ATTR                Yes
             2836  COMPARE_OP               ==
         2838_2840  POP_JUMP_IF_FALSE  2908  'to 2908'

 L. 913      2842  LOAD_GLOBAL              QtWidgets
             2844  LOAD_METHOD              QDialog
             2846  CALL_METHOD_0         0  '0 positional arguments'
             2848  STORE_FAST               '_viewmllearnmat'

 L. 914      2850  LOAD_GLOBAL              gui_viewmllearnmat
             2852  CALL_FUNCTION_0       0  '0 positional arguments'
             2854  STORE_FAST               '_gui'

 L. 915      2856  LOAD_FAST                '_cnnlog'
             2858  LOAD_STR                 'learning_curve'
             2860  BINARY_SUBSCR    
             2862  LOAD_FAST                '_gui'
             2864  STORE_ATTR               learnmat

 L. 916      2866  LOAD_DEREF               'self'
             2868  LOAD_ATTR                linestyle
             2870  LOAD_FAST                '_gui'
             2872  STORE_ATTR               linestyle

 L. 917      2874  LOAD_DEREF               'self'
             2876  LOAD_ATTR                fontstyle
             2878  LOAD_FAST                '_gui'
             2880  STORE_ATTR               fontstyle

 L. 918      2882  LOAD_FAST                '_gui'
             2884  LOAD_METHOD              setupGUI
             2886  LOAD_FAST                '_viewmllearnmat'
             2888  CALL_METHOD_1         1  '1 positional argument'
             2890  POP_TOP          

 L. 919      2892  LOAD_FAST                '_viewmllearnmat'
             2894  LOAD_METHOD              exec
             2896  CALL_METHOD_0         0  '0 positional arguments'
             2898  POP_TOP          

 L. 920      2900  LOAD_FAST                '_viewmllearnmat'
             2902  LOAD_METHOD              show
             2904  CALL_METHOD_0         0  '0 positional arguments'
             2906  POP_TOP          
           2908_0  COME_FROM          2838  '2838'

Parse error at or near `POP_TOP' instruction at offset 2906

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
    TrainMl3DCnnFromExisting = QtWidgets.QWidget()
    gui = trainml3dcnnfromexisting()
    gui.setupGUI(TrainMl3DCnnFromExisting)
    TrainMl3DCnnFromExisting.show()
    sys.exit(app.exec_())