# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml2dwdcnnfromexisting.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 58217 bytes
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
import cognitivegeo.src.ml.wdcnnsegmentor as ml_wdcnn
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml2dwdcnnfromexisting(object):
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

    def setupGUI(self, TrainMl2DWdcnnFromExisting):
        TrainMl2DWdcnnFromExisting.setObjectName('TrainMl2DWdcnnFromExisting')
        TrainMl2DWdcnnFromExisting.setFixedSize(800, 630)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl2DWdcnnFromExisting.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl2DWdcnnFromExisting)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl2DWdcnnFromExisting)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl2DWdcnnFromExisting)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblweight = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblweight.setObjectName('lblweight')
        self.lblweight.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.cbbweight = QtWidgets.QComboBox(TrainMl2DWdcnnFromExisting)
        self.cbbweight.setObjectName('cbbweight')
        self.cbbweight.setGeometry(QtCore.QRect(110, 310, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblexisting = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblexisting.setObjectName('lblexisting')
        self.lblexisting.setGeometry(QtCore.QRect(410, 50, 100, 30))
        self.ldtexisting = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtexisting.setObjectName('ldtexisting')
        self.ldtexisting.setGeometry(QtCore.QRect(510, 50, 210, 30))
        self.btnexisting = QtWidgets.QPushButton(TrainMl2DWdcnnFromExisting)
        self.btnexisting.setObjectName('btnexisting')
        self.btnexisting.setGeometry(QtCore.QRect(730, 50, 60, 30))
        self.lblnconvblockexisting = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblnconvblockexisting.setObjectName('lblnconvblockexisting')
        self.lblnconvblockexisting.setGeometry(QtCore.QRect(410, 90, 130, 30))
        self.ldtnconvblockexisting = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtnconvblockexisting.setObjectName('ldtnconvblockexisting')
        self.ldtnconvblockexisting.setGeometry(QtCore.QRect(550, 90, 40, 30))
        self.twgnconvblockexisting = QtWidgets.QTableWidget(TrainMl2DWdcnnFromExisting)
        self.twgnconvblockexisting.setObjectName('twgnconvblockexisting')
        self.twgnconvblockexisting.setGeometry(QtCore.QRect(610, 90, 180, 150))
        self.twgnconvblockexisting.setColumnCount(3)
        self.twgnconvblockexisting.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblockexisting.verticalHeader().hide()
        self.lblblockid = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblblockid.setObjectName('lblblockid')
        self.lblblockid.setGeometry(QtCore.QRect(410, 130, 130, 30))
        self.cbbblockid = QtWidgets.QComboBox(TrainMl2DWdcnnFromExisting)
        self.cbbblockid.setObjectName('cbbblockid')
        self.cbbblockid.setGeometry(QtCore.QRect(550, 130, 40, 30))
        self.lbllayerid = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lbllayerid.setObjectName('lbllayerid')
        self.lbllayerid.setGeometry(QtCore.QRect(410, 170, 130, 30))
        self.cbblayerid = QtWidgets.QComboBox(TrainMl2DWdcnnFromExisting)
        self.cbblayerid.setObjectName('cbblayerid')
        self.cbblayerid.setGeometry(QtCore.QRect(550, 170, 40, 30))
        self.lbltrainable = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lbltrainable.setObjectName('lbltrainable')
        self.lbltrainable.setGeometry(QtCore.QRect(410, 210, 130, 30))
        self.cbbtrainable = QtWidgets.QComboBox(TrainMl2DWdcnnFromExisting)
        self.cbbtrainable.setObjectName('cbbtrainable')
        self.cbbtrainable.setGeometry(QtCore.QRect(550, 210, 40, 30))
        self.lblappend = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblappend.setObjectName('lblappend')
        self.lblappend.setGeometry(QtCore.QRect(410, 250, 200, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 290, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 290, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl2DWdcnnFromExisting)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 330, 180, 200))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 290, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 290, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(TrainMl2DWdcnnFromExisting)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 330, 180, 200))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 540, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 540, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 540, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 580, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 580, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 540, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 540, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 540, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 580, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 580, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl2DWdcnnFromExisting)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 360, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 360, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 400, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 400, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 400, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 400, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 440, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 440, 40, 30))
        self.lbldropout = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 440, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 440, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl2DWdcnnFromExisting)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 490, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl2DWdcnnFromExisting)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 490, 180, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl2DWdcnnFromExisting)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 490, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl2DWdcnnFromExisting)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(120, 580, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl2DWdcnnFromExisting)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl2DWdcnnFromExisting.geometry().center().x()
        _center_y = TrainMl2DWdcnnFromExisting.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl2DWdcnnFromExisting)
        QtCore.QMetaObject.connectSlotsByName(TrainMl2DWdcnnFromExisting)

    def retranslateGUI(self, TrainMl2DWdcnnFromExisting):
        self.dialog = TrainMl2DWdcnnFromExisting
        _translate = QtCore.QCoreApplication.translate
        TrainMl2DWdcnnFromExisting.setWindowTitle(_translate('TrainMl2DWdcnnFromExisting', 'Train 2D-WDCNN from pre-trained'))
        self.lblfeature.setText(_translate('TrainMl2DWdcnnFromExisting', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl2DWdcnnFromExisting', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl2DWdcnnFromExisting', 'Select target:'))
        self.lblweight.setText(_translate('TrainMl2DWdcnnFromExisting', 'Select weight:'))
        self.btnconfigtraindata.setText(_translate('TrainMl2DDcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('TrainMl2DWdcnnFromExisting', 'Original\nimage\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl2DWdcnnFromExisting', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl2DWdcnnFromExisting', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl2DWdcnnFromExisting', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl2DWdcnnFromExisting', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl2DWdcnnFromExisting', 'Interpolated\nimage\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl2DWdcnnFromExisting', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl2DWdcnnFromExisting', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl2DWdcnnFromExisting', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl2DWdcnnFromExisting', '32'))
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
                    item.setText(_translate('TrainMl2DWdcnnFromExisting', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
            self.cbbweight.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl2DWdcnnFromExisting', 'Specify WDCNN architecture:'))
        self.lblexisting.setText(_translate('TrainMl2DWdcnnFromExisting', 'Select pre-trained:'))
        self.ldtexisting.setText(_translate('TrainMl2DWdcnnFromExisting', ''))
        self.ldtexisting.textChanged.connect(self.changeLdtExisting)
        self.btnexisting.setText(_translate('TrainMl2DWdcnnFromExisting', 'Browse'))
        self.btnexisting.clicked.connect(self.clickBtnExisting)
        self.lblnconvblockexisting.setText(_translate('TrainMl2DWdcnnFromExisting', 'Available conv. blocks:'))
        self.lblnconvblockexisting.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblockexisting.setText(_translate('TrainMl2DWdcnnFromExisting', ''))
        self.ldtnconvblockexisting.setEnabled(False)
        self.ldtnconvblockexisting.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblockexisting.textChanged.connect(self.changeLdtNconvblockExisting)
        self.twgnconvblockexisting.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblblockid.setText(_translate('TrainMl2DWdcnnFromExisting', 'Select conv. block ID:'))
        self.lblblockid.setAlignment(QtCore.Qt.AlignRight)
        self.cbbblockid.currentIndexChanged.connect(self.changeCbbBlockid)
        self.lbllayerid.setText(_translate('TrainMl2DWdcnnFromExisting', 'Select conv. layer ID:'))
        self.lbllayerid.setAlignment(QtCore.Qt.AlignRight)
        self.lbltrainable.setText(_translate('TrainMl2DWdcnnFromExisting', 'Is trainable?:'))
        self.lbltrainable.setAlignment(QtCore.Qt.AlignRight)
        self.cbbtrainable.addItems(['Yes', 'No'])
        self.lblappend.setText(_translate('TrainMl2DWdcnnFromExisting', 'Append more blocks & layers:'))
        self.lblnconvblock.setText(_translate('TrainMl2DWdcnnFromExisting', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl2DWdcnnFromExisting', '2'))
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.twgnconvblock.setRowCount(2)
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

        self.lbln1x1layer.setText(_translate('TrainMl2DWdcnnFromExisting', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('TrainMl2DWdcnnFromExisting', '2'))
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.twgn1x1layer.setRowCount(2)
        for _idx in range(int(self.ldtn1x1layer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl2DWdcnnFromExisting', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgn1x1layer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgn1x1layer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl2DWdcnnFromExisting', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl2DWdcnnFromExisting', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl2DWdcnnFromExisting', ''))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskheight.setEnabled(False)
        self.lblmaskwidth.setText(_translate('TrainMl2DWdcnnFromExisting', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl2DWdcnnFromExisting', ''))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskwidth.setEnabled(False)
        self.lblpoolsize.setText(_translate('TrainMl2DWdcnnFromExisting', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl2DWdcnnFromExisting', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl2DWdcnnFromExisting', ''))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl2DWdcnnFromExisting', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl2DWdcnnFromExisting', ''))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('TrainMl2DWdcnnFromExisting', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl2DWdcnnFromExisting', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl2DWdcnnFromExisting', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl2DWdcnnFromExisting', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl2DWdcnnFromExisting', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl2DWdcnnFromExisting', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl2DWdcnnFromExisting', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('TrainMl2DWdcnnFromExisting', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('TrainMl2DWdcnnFromExisting', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl2DWdcnnFromExisting', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl2DWdcnnFromExisting', ''))
        self.btnsave.setText(_translate('TrainMl2DWdcnnFromExisting', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl2DWdcnnFromExisting', 'Train 2D-WDCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl2DWdcnnFromExisting)

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

    def clickBtnTrainMl2DWdcnnFromExisting--- This code section failed: ---

 L. 608         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 610         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 611        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 612        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 613        50  LOAD_STR                 'Train 2D-WDCNN'

 L. 614        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 615        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 617        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_image_height'

 L. 618        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_image_width'

 L. 619        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtnewheight
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_image_height_new'

 L. 620       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewwidth
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_image_width_new'

 L. 621       126  LOAD_FAST                '_image_height'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'
              134  LOAD_FAST                '_image_width'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_TRUE    158  'to 158'

 L. 622       142  LOAD_FAST                '_image_height_new'
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

 L. 623       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 624       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 625       182  LOAD_STR                 'Train 2D-WDCNN'

 L. 626       184  LOAD_STR                 'Non-integer feature size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 627       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 628       194  LOAD_FAST                '_image_height'
              196  LOAD_CONST               2
              198  COMPARE_OP               <
              200  POP_JUMP_IF_TRUE    228  'to 228'
              202  LOAD_FAST                '_image_width'
              204  LOAD_CONST               2
              206  COMPARE_OP               <
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 629       210  LOAD_FAST                '_image_height_new'
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

 L. 630       228  LOAD_GLOBAL              vis_msg
              230  LOAD_ATTR                print
              232  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 631       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 632       252  LOAD_STR                 'Train 2D-WDCNN'

 L. 633       254  LOAD_STR                 'Features are not 2D'
              256  CALL_METHOD_3         3  '3 positional arguments'
              258  POP_TOP          

 L. 634       260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           224  '224'

 L. 636       264  LOAD_CONST               2
              266  LOAD_GLOBAL              int
              268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               2
              272  BINARY_TRUE_DIVIDE
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  BINARY_MULTIPLY  
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  STORE_FAST               '_image_height'

 L. 637       284  LOAD_CONST               2
              286  LOAD_GLOBAL              int
              288  LOAD_FAST                '_image_width'
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BINARY_MULTIPLY  
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               '_image_width'

 L. 639       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                lwgfeature
              308  LOAD_METHOD              selectedItems
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               '_features'

 L. 640       314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainml2dwdcnnfromexisting.clickBtnTrainMl2DWdcnnFromExisting.<locals>.<listcomp>'
              318  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              320  LOAD_FAST                '_features'
              322  GET_ITER         
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               '_features'

 L. 641       328  LOAD_DEREF               'self'
              330  LOAD_ATTR                featurelist
              332  LOAD_DEREF               'self'
              334  LOAD_ATTR                cbbtarget
              336  LOAD_METHOD              currentIndex
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  BINARY_SUBSCR    
              342  STORE_FAST               '_target'

 L. 642       344  LOAD_DEREF               'self'
              346  LOAD_ATTR                featurelist
              348  LOAD_DEREF               'self'
              350  LOAD_ATTR                cbbweight
              352  LOAD_METHOD              currentIndex
              354  CALL_METHOD_0         0  '0 positional arguments'
              356  BINARY_SUBSCR    
              358  STORE_FAST               '_weight'

 L. 644       360  LOAD_FAST                '_target'
              362  LOAD_FAST                '_features'
              364  COMPARE_OP               in
          366_368  POP_JUMP_IF_FALSE   406  'to 406'

 L. 645       370  LOAD_GLOBAL              vis_msg
              372  LOAD_ATTR                print
              374  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Target also used as features'
              376  LOAD_STR                 'error'
              378  LOAD_CONST               ('type',)
              380  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              382  POP_TOP          

 L. 646       384  LOAD_GLOBAL              QtWidgets
              386  LOAD_ATTR                QMessageBox
              388  LOAD_METHOD              critical
              390  LOAD_DEREF               'self'
              392  LOAD_ATTR                msgbox

 L. 647       394  LOAD_STR                 'Train 2D-WDCNN'

 L. 648       396  LOAD_STR                 'Target also used as features'
              398  CALL_METHOD_3         3  '3 positional arguments'
              400  POP_TOP          

 L. 649       402  LOAD_CONST               None
              404  RETURN_VALUE     
            406_0  COME_FROM           366  '366'

 L. 650       406  LOAD_FAST                '_weight'
              408  LOAD_FAST                '_features'
              410  COMPARE_OP               in
          412_414  POP_JUMP_IF_FALSE   452  'to 452'

 L. 651       416  LOAD_GLOBAL              vis_msg
              418  LOAD_ATTR                print
              420  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Weight also used as features'
              422  LOAD_STR                 'error'
              424  LOAD_CONST               ('type',)
              426  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              428  POP_TOP          

 L. 652       430  LOAD_GLOBAL              QtWidgets
              432  LOAD_ATTR                QMessageBox
              434  LOAD_METHOD              critical
              436  LOAD_DEREF               'self'
              438  LOAD_ATTR                msgbox

 L. 653       440  LOAD_STR                 'Train 2D-WDCNN'

 L. 654       442  LOAD_STR                 'Weight also used as features'
              444  CALL_METHOD_3         3  '3 positional arguments'
              446  POP_TOP          

 L. 655       448  LOAD_CONST               None
              450  RETURN_VALUE     
            452_0  COME_FROM           412  '412'

 L. 657       452  LOAD_GLOBAL              len
              454  LOAD_DEREF               'self'
              456  LOAD_ATTR                ldtexisting
              458  LOAD_METHOD              text
              460  CALL_METHOD_0         0  '0 positional arguments'
              462  CALL_FUNCTION_1       1  '1 positional argument'
              464  LOAD_CONST               1
              466  COMPARE_OP               <
          468_470  POP_JUMP_IF_FALSE   508  'to 508'

 L. 658       472  LOAD_GLOBAL              vis_msg
              474  LOAD_ATTR                print
              476  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: No name specified for pre-trained network'

 L. 659       478  LOAD_STR                 'error'
              480  LOAD_CONST               ('type',)
              482  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              484  POP_TOP          

 L. 660       486  LOAD_GLOBAL              QtWidgets
              488  LOAD_ATTR                QMessageBox
              490  LOAD_METHOD              critical
              492  LOAD_DEREF               'self'
              494  LOAD_ATTR                msgbox

 L. 661       496  LOAD_STR                 'Train 2D-WDCNN'

 L. 662       498  LOAD_STR                 'No name specified for pre-trained network'
              500  CALL_METHOD_3         3  '3 positional arguments'
              502  POP_TOP          

 L. 663       504  LOAD_CONST               None
              506  RETURN_VALUE     
            508_0  COME_FROM           468  '468'

 L. 664       508  LOAD_GLOBAL              os
              510  LOAD_ATTR                path
              512  LOAD_METHOD              dirname
              514  LOAD_DEREF               'self'
              516  LOAD_ATTR                ldtexisting
              518  LOAD_METHOD              text
              520  CALL_METHOD_0         0  '0 positional arguments'
              522  CALL_METHOD_1         1  '1 positional argument'
              524  STORE_FAST               '_precnnpath'

 L. 665       526  LOAD_GLOBAL              os
              528  LOAD_ATTR                path
              530  LOAD_METHOD              splitext
              532  LOAD_GLOBAL              os
              534  LOAD_ATTR                path
              536  LOAD_METHOD              basename
              538  LOAD_DEREF               'self'
              540  LOAD_ATTR                ldtexisting
              542  LOAD_METHOD              text
              544  CALL_METHOD_0         0  '0 positional arguments'
              546  CALL_METHOD_1         1  '1 positional argument'
              548  CALL_METHOD_1         1  '1 positional argument'
              550  LOAD_CONST               0
              552  BINARY_SUBSCR    
              554  STORE_FAST               '_precnnname'

 L. 666       556  LOAD_DEREF               'self'
              558  LOAD_ATTR                cbbblockid
              560  LOAD_METHOD              currentIndex
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  STORE_FAST               '_blockidx'

 L. 667       566  LOAD_DEREF               'self'
              568  LOAD_ATTR                cbblayerid
              570  LOAD_METHOD              currentIndex
              572  CALL_METHOD_0         0  '0 positional arguments'
              574  STORE_FAST               '_layeridx'

 L. 668       576  LOAD_CONST               True
              578  STORE_FAST               '_trainable'

 L. 669       580  LOAD_DEREF               'self'
              582  LOAD_ATTR                cbbtrainable
              584  LOAD_METHOD              currentIndex
              586  CALL_METHOD_0         0  '0 positional arguments'
              588  LOAD_CONST               0
              590  COMPARE_OP               !=
          592_594  POP_JUMP_IF_FALSE   600  'to 600'

 L. 670       596  LOAD_CONST               False
              598  STORE_FAST               '_trainable'
            600_0  COME_FROM           592  '592'

 L. 672       600  LOAD_GLOBAL              ml_tfm
              602  LOAD_METHOD              getConvModelNChannel
              604  LOAD_FAST                '_precnnpath'
              606  LOAD_FAST                '_precnnname'
              608  CALL_METHOD_2         2  '2 positional arguments'
              610  LOAD_GLOBAL              len
              612  LOAD_FAST                '_features'
              614  CALL_FUNCTION_1       1  '1 positional argument'
              616  COMPARE_OP               !=
          618_620  POP_JUMP_IF_FALSE   658  'to 658'

 L. 673       622  LOAD_GLOBAL              vis_msg
              624  LOAD_ATTR                print
              626  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Feature channel number not match with pre-trained network'

 L. 674       628  LOAD_STR                 'error'
              630  LOAD_CONST               ('type',)
              632  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              634  POP_TOP          

 L. 675       636  LOAD_GLOBAL              QtWidgets
              638  LOAD_ATTR                QMessageBox
              640  LOAD_METHOD              critical
              642  LOAD_DEREF               'self'
              644  LOAD_ATTR                msgbox

 L. 676       646  LOAD_STR                 'Train 2D-WDCNN'

 L. 677       648  LOAD_STR                 'Feature channel number not match with pre-trained network'
              650  CALL_METHOD_3         3  '3 positional arguments'
              652  POP_TOP          

 L. 678       654  LOAD_CONST               None
              656  RETURN_VALUE     
            658_0  COME_FROM           618  '618'

 L. 680       658  LOAD_GLOBAL              basic_data
              660  LOAD_METHOD              str2int
              662  LOAD_DEREF               'self'
              664  LOAD_ATTR                ldtnconvblock
              666  LOAD_METHOD              text
              668  CALL_METHOD_0         0  '0 positional arguments'
              670  CALL_METHOD_1         1  '1 positional argument'
              672  STORE_FAST               '_nconvblock'

 L. 681       674  LOAD_CLOSURE             'self'
              676  BUILD_TUPLE_1         1 
              678  LOAD_LISTCOMP            '<code_object <listcomp>>'
              680  LOAD_STR                 'trainml2dwdcnnfromexisting.clickBtnTrainMl2DWdcnnFromExisting.<locals>.<listcomp>'
              682  MAKE_FUNCTION_8          'closure'
              684  LOAD_GLOBAL              range
              686  LOAD_FAST                '_nconvblock'
              688  CALL_FUNCTION_1       1  '1 positional argument'
              690  GET_ITER         
              692  CALL_FUNCTION_1       1  '1 positional argument'
              694  STORE_FAST               '_nconvlayer'

 L. 682       696  LOAD_CLOSURE             'self'
              698  BUILD_TUPLE_1         1 
              700  LOAD_LISTCOMP            '<code_object <listcomp>>'
              702  LOAD_STR                 'trainml2dwdcnnfromexisting.clickBtnTrainMl2DWdcnnFromExisting.<locals>.<listcomp>'
              704  MAKE_FUNCTION_8          'closure'
              706  LOAD_GLOBAL              range
              708  LOAD_FAST                '_nconvblock'
              710  CALL_FUNCTION_1       1  '1 positional argument'
              712  GET_ITER         
              714  CALL_FUNCTION_1       1  '1 positional argument'
              716  STORE_FAST               '_nconvfeature'

 L. 683       718  LOAD_GLOBAL              basic_data
              720  LOAD_METHOD              str2int
              722  LOAD_DEREF               'self'
              724  LOAD_ATTR                ldtn1x1layer
              726  LOAD_METHOD              text
              728  CALL_METHOD_0         0  '0 positional arguments'
              730  CALL_METHOD_1         1  '1 positional argument'
              732  STORE_FAST               '_n1x1layer'

 L. 684       734  LOAD_CLOSURE             'self'
              736  BUILD_TUPLE_1         1 
              738  LOAD_LISTCOMP            '<code_object <listcomp>>'
              740  LOAD_STR                 'trainml2dwdcnnfromexisting.clickBtnTrainMl2DWdcnnFromExisting.<locals>.<listcomp>'
              742  MAKE_FUNCTION_8          'closure'
              744  LOAD_GLOBAL              range
              746  LOAD_FAST                '_n1x1layer'
              748  CALL_FUNCTION_1       1  '1 positional argument'
              750  GET_ITER         
              752  CALL_FUNCTION_1       1  '1 positional argument'
              754  STORE_FAST               '_n1x1feature'

 L. 685       756  LOAD_GLOBAL              basic_data
              758  LOAD_METHOD              str2int
              760  LOAD_DEREF               'self'
              762  LOAD_ATTR                ldtmaskheight
              764  LOAD_METHOD              text
              766  CALL_METHOD_0         0  '0 positional arguments'
              768  CALL_METHOD_1         1  '1 positional argument'
              770  STORE_FAST               '_patch_height'

 L. 686       772  LOAD_GLOBAL              basic_data
              774  LOAD_METHOD              str2int
              776  LOAD_DEREF               'self'
              778  LOAD_ATTR                ldtmaskwidth
              780  LOAD_METHOD              text
              782  CALL_METHOD_0         0  '0 positional arguments'
              784  CALL_METHOD_1         1  '1 positional argument'
              786  STORE_FAST               '_patch_width'

 L. 687       788  LOAD_GLOBAL              basic_data
              790  LOAD_METHOD              str2int
              792  LOAD_DEREF               'self'
              794  LOAD_ATTR                ldtpoolheight
              796  LOAD_METHOD              text
              798  CALL_METHOD_0         0  '0 positional arguments'
              800  CALL_METHOD_1         1  '1 positional argument'
              802  STORE_FAST               '_pool_height'

 L. 688       804  LOAD_GLOBAL              basic_data
              806  LOAD_METHOD              str2int
              808  LOAD_DEREF               'self'
              810  LOAD_ATTR                ldtpoolwidth
              812  LOAD_METHOD              text
              814  CALL_METHOD_0         0  '0 positional arguments'
              816  CALL_METHOD_1         1  '1 positional argument'
              818  STORE_FAST               '_pool_width'

 L. 689       820  LOAD_GLOBAL              basic_data
              822  LOAD_METHOD              str2int
              824  LOAD_DEREF               'self'
              826  LOAD_ATTR                ldtnepoch
              828  LOAD_METHOD              text
              830  CALL_METHOD_0         0  '0 positional arguments'
              832  CALL_METHOD_1         1  '1 positional argument'
              834  STORE_FAST               '_nepoch'

 L. 690       836  LOAD_GLOBAL              basic_data
              838  LOAD_METHOD              str2int
              840  LOAD_DEREF               'self'
              842  LOAD_ATTR                ldtbatchsize
              844  LOAD_METHOD              text
              846  CALL_METHOD_0         0  '0 positional arguments'
              848  CALL_METHOD_1         1  '1 positional argument'
              850  STORE_FAST               '_batchsize'

 L. 691       852  LOAD_GLOBAL              basic_data
              854  LOAD_METHOD              str2float
              856  LOAD_DEREF               'self'
              858  LOAD_ATTR                ldtlearnrate
              860  LOAD_METHOD              text
              862  CALL_METHOD_0         0  '0 positional arguments'
              864  CALL_METHOD_1         1  '1 positional argument'
              866  STORE_FAST               '_learning_rate'

 L. 692       868  LOAD_GLOBAL              basic_data
              870  LOAD_METHOD              str2float
              872  LOAD_DEREF               'self'
              874  LOAD_ATTR                ldtdropout
              876  LOAD_METHOD              text
              878  CALL_METHOD_0         0  '0 positional arguments'
              880  CALL_METHOD_1         1  '1 positional argument'
              882  STORE_FAST               '_dropout_prob'

 L. 693       884  LOAD_FAST                '_nconvblock'
              886  LOAD_CONST               False
              888  COMPARE_OP               is
          890_892  POP_JUMP_IF_TRUE    904  'to 904'
              894  LOAD_FAST                '_nconvblock'
              896  LOAD_CONST               0
              898  COMPARE_OP               <=
          900_902  POP_JUMP_IF_FALSE   940  'to 940'
            904_0  COME_FROM           890  '890'

 L. 694       904  LOAD_GLOBAL              vis_msg
              906  LOAD_ATTR                print
              908  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Non-positive convolutional block number'

 L. 695       910  LOAD_STR                 'error'
              912  LOAD_CONST               ('type',)
              914  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              916  POP_TOP          

 L. 696       918  LOAD_GLOBAL              QtWidgets
              920  LOAD_ATTR                QMessageBox
              922  LOAD_METHOD              critical
              924  LOAD_DEREF               'self'
              926  LOAD_ATTR                msgbox

 L. 697       928  LOAD_STR                 'Train 2D-WDCNN'

 L. 698       930  LOAD_STR                 'Non-positive convolutional block number'
              932  CALL_METHOD_3         3  '3 positional arguments'
              934  POP_TOP          

 L. 699       936  LOAD_CONST               None
              938  RETURN_VALUE     
            940_0  COME_FROM           900  '900'

 L. 700       940  SETUP_LOOP         1012  'to 1012'
              942  LOAD_FAST                '_nconvlayer'
              944  GET_ITER         
            946_0  COME_FROM           966  '966'
              946  FOR_ITER           1010  'to 1010'
              948  STORE_FAST               '_i'

 L. 701       950  LOAD_FAST                '_i'
              952  LOAD_CONST               False
              954  COMPARE_OP               is
          956_958  POP_JUMP_IF_TRUE    970  'to 970'
              960  LOAD_FAST                '_i'
              962  LOAD_CONST               1
              964  COMPARE_OP               <
          966_968  POP_JUMP_IF_FALSE   946  'to 946'
            970_0  COME_FROM           956  '956'

 L. 702       970  LOAD_GLOBAL              vis_msg
              972  LOAD_ATTR                print
              974  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Non-positive convolutional layer number'

 L. 703       976  LOAD_STR                 'error'
              978  LOAD_CONST               ('type',)
              980  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              982  POP_TOP          

 L. 704       984  LOAD_GLOBAL              QtWidgets
              986  LOAD_ATTR                QMessageBox
              988  LOAD_METHOD              critical
              990  LOAD_DEREF               'self'
              992  LOAD_ATTR                msgbox

 L. 705       994  LOAD_STR                 'Train 2D-WDCNN'

 L. 706       996  LOAD_STR                 'Non-positive convolutional layer number'
              998  CALL_METHOD_3         3  '3 positional arguments'
             1000  POP_TOP          

 L. 707      1002  LOAD_CONST               None
             1004  RETURN_VALUE     
         1006_1008  JUMP_BACK           946  'to 946'
             1010  POP_BLOCK        
           1012_0  COME_FROM_LOOP      940  '940'

 L. 708      1012  SETUP_LOOP         1084  'to 1084'
             1014  LOAD_FAST                '_nconvfeature'
             1016  GET_ITER         
           1018_0  COME_FROM          1038  '1038'
             1018  FOR_ITER           1082  'to 1082'
             1020  STORE_FAST               '_i'

 L. 709      1022  LOAD_FAST                '_i'
             1024  LOAD_CONST               False
             1026  COMPARE_OP               is
         1028_1030  POP_JUMP_IF_TRUE   1042  'to 1042'
             1032  LOAD_FAST                '_i'
             1034  LOAD_CONST               1
             1036  COMPARE_OP               <
         1038_1040  POP_JUMP_IF_FALSE  1018  'to 1018'
           1042_0  COME_FROM          1028  '1028'

 L. 710      1042  LOAD_GLOBAL              vis_msg
             1044  LOAD_ATTR                print
             1046  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Non-positive convolutional feature number'

 L. 711      1048  LOAD_STR                 'error'
             1050  LOAD_CONST               ('type',)
             1052  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1054  POP_TOP          

 L. 712      1056  LOAD_GLOBAL              QtWidgets
             1058  LOAD_ATTR                QMessageBox
             1060  LOAD_METHOD              critical
             1062  LOAD_DEREF               'self'
             1064  LOAD_ATTR                msgbox

 L. 713      1066  LOAD_STR                 'Train 2D-WDCNN'

 L. 714      1068  LOAD_STR                 'Non-positive convolutional feature number'
             1070  CALL_METHOD_3         3  '3 positional arguments'
             1072  POP_TOP          

 L. 715      1074  LOAD_CONST               None
             1076  RETURN_VALUE     
         1078_1080  JUMP_BACK          1018  'to 1018'
             1082  POP_BLOCK        
           1084_0  COME_FROM_LOOP     1012  '1012'

 L. 716      1084  LOAD_FAST                '_n1x1layer'
             1086  LOAD_CONST               False
             1088  COMPARE_OP               is
         1090_1092  POP_JUMP_IF_TRUE   1104  'to 1104'
             1094  LOAD_FAST                '_n1x1layer'
             1096  LOAD_CONST               0
             1098  COMPARE_OP               <=
         1100_1102  POP_JUMP_IF_FALSE  1140  'to 1140'
           1104_0  COME_FROM          1090  '1090'

 L. 717      1104  LOAD_GLOBAL              vis_msg
             1106  LOAD_ATTR                print
             1108  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Non-positive 1x1 convolutional layer number'

 L. 718      1110  LOAD_STR                 'error'
             1112  LOAD_CONST               ('type',)
             1114  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1116  POP_TOP          

 L. 719      1118  LOAD_GLOBAL              QtWidgets
             1120  LOAD_ATTR                QMessageBox
             1122  LOAD_METHOD              critical
             1124  LOAD_DEREF               'self'
             1126  LOAD_ATTR                msgbox

 L. 720      1128  LOAD_STR                 'Train 2D-WDCNN'

 L. 721      1130  LOAD_STR                 'Non-positive 1x1 convolutional layer number'
             1132  CALL_METHOD_3         3  '3 positional arguments'
             1134  POP_TOP          

 L. 722      1136  LOAD_CONST               None
             1138  RETURN_VALUE     
           1140_0  COME_FROM          1100  '1100'

 L. 723      1140  SETUP_LOOP         1212  'to 1212'
             1142  LOAD_FAST                '_n1x1feature'
             1144  GET_ITER         
           1146_0  COME_FROM          1166  '1166'
             1146  FOR_ITER           1210  'to 1210'
             1148  STORE_FAST               '_i'

 L. 724      1150  LOAD_FAST                '_i'
             1152  LOAD_CONST               False
             1154  COMPARE_OP               is
         1156_1158  POP_JUMP_IF_TRUE   1170  'to 1170'
             1160  LOAD_FAST                '_i'
             1162  LOAD_CONST               1
             1164  COMPARE_OP               <
         1166_1168  POP_JUMP_IF_FALSE  1146  'to 1146'
           1170_0  COME_FROM          1156  '1156'

 L. 725      1170  LOAD_GLOBAL              vis_msg
             1172  LOAD_ATTR                print
             1174  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Non-positive 1x1 convolutional feature number'

 L. 726      1176  LOAD_STR                 'error'
             1178  LOAD_CONST               ('type',)
             1180  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1182  POP_TOP          

 L. 727      1184  LOAD_GLOBAL              QtWidgets
             1186  LOAD_ATTR                QMessageBox
             1188  LOAD_METHOD              critical
             1190  LOAD_DEREF               'self'
             1192  LOAD_ATTR                msgbox

 L. 728      1194  LOAD_STR                 'Train 2D-WDCNN'

 L. 729      1196  LOAD_STR                 'Non-positive 1x1 convolutional feature number'
             1198  CALL_METHOD_3         3  '3 positional arguments'
             1200  POP_TOP          

 L. 730      1202  LOAD_CONST               None
             1204  RETURN_VALUE     
         1206_1208  JUMP_BACK          1146  'to 1146'
             1210  POP_BLOCK        
           1212_0  COME_FROM_LOOP     1140  '1140'

 L. 731      1212  LOAD_FAST                '_patch_height'
             1214  LOAD_CONST               False
             1216  COMPARE_OP               is
         1218_1220  POP_JUMP_IF_TRUE   1252  'to 1252'
             1222  LOAD_FAST                '_patch_width'
             1224  LOAD_CONST               False
             1226  COMPARE_OP               is
         1228_1230  POP_JUMP_IF_TRUE   1252  'to 1252'

 L. 732      1232  LOAD_FAST                '_patch_height'
             1234  LOAD_CONST               1
             1236  COMPARE_OP               <
         1238_1240  POP_JUMP_IF_TRUE   1252  'to 1252'
             1242  LOAD_FAST                '_patch_width'
             1244  LOAD_CONST               1
             1246  COMPARE_OP               <
         1248_1250  POP_JUMP_IF_FALSE  1288  'to 1288'
           1252_0  COME_FROM          1238  '1238'
           1252_1  COME_FROM          1228  '1228'
           1252_2  COME_FROM          1218  '1218'

 L. 733      1252  LOAD_GLOBAL              vis_msg
             1254  LOAD_ATTR                print
             1256  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromScratch: Non-positive convolutional patch size'
             1258  LOAD_STR                 'error'
             1260  LOAD_CONST               ('type',)
             1262  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1264  POP_TOP          

 L. 734      1266  LOAD_GLOBAL              QtWidgets
             1268  LOAD_ATTR                QMessageBox
             1270  LOAD_METHOD              critical
             1272  LOAD_DEREF               'self'
             1274  LOAD_ATTR                msgbox

 L. 735      1276  LOAD_STR                 'Train 2D-WDCNN'

 L. 736      1278  LOAD_STR                 'Non-positive convolutional patch size'
             1280  CALL_METHOD_3         3  '3 positional arguments'
             1282  POP_TOP          

 L. 737      1284  LOAD_CONST               None
             1286  RETURN_VALUE     
           1288_0  COME_FROM          1248  '1248'

 L. 738      1288  LOAD_FAST                '_pool_height'
             1290  LOAD_CONST               False
             1292  COMPARE_OP               is
         1294_1296  POP_JUMP_IF_TRUE   1328  'to 1328'
             1298  LOAD_FAST                '_pool_width'
             1300  LOAD_CONST               False
             1302  COMPARE_OP               is
         1304_1306  POP_JUMP_IF_TRUE   1328  'to 1328'

 L. 739      1308  LOAD_FAST                '_pool_height'
             1310  LOAD_CONST               1
             1312  COMPARE_OP               <
         1314_1316  POP_JUMP_IF_TRUE   1328  'to 1328'
             1318  LOAD_FAST                '_pool_width'
             1320  LOAD_CONST               1
             1322  COMPARE_OP               <
         1324_1326  POP_JUMP_IF_FALSE  1364  'to 1364'
           1328_0  COME_FROM          1314  '1314'
           1328_1  COME_FROM          1304  '1304'
           1328_2  COME_FROM          1294  '1294'

 L. 740      1328  LOAD_GLOBAL              vis_msg
             1330  LOAD_ATTR                print
             1332  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Non-positive pooling size'
             1334  LOAD_STR                 'error'
             1336  LOAD_CONST               ('type',)
             1338  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1340  POP_TOP          

 L. 741      1342  LOAD_GLOBAL              QtWidgets
             1344  LOAD_ATTR                QMessageBox
             1346  LOAD_METHOD              critical
             1348  LOAD_DEREF               'self'
             1350  LOAD_ATTR                msgbox

 L. 742      1352  LOAD_STR                 'Train 2D-WDCNN'

 L. 743      1354  LOAD_STR                 'Non-positive pooling size'
             1356  CALL_METHOD_3         3  '3 positional arguments'
             1358  POP_TOP          

 L. 744      1360  LOAD_CONST               None
             1362  RETURN_VALUE     
           1364_0  COME_FROM          1324  '1324'

 L. 745      1364  LOAD_FAST                '_nepoch'
             1366  LOAD_CONST               False
             1368  COMPARE_OP               is
         1370_1372  POP_JUMP_IF_TRUE   1384  'to 1384'
             1374  LOAD_FAST                '_nepoch'
             1376  LOAD_CONST               0
             1378  COMPARE_OP               <=
         1380_1382  POP_JUMP_IF_FALSE  1420  'to 1420'
           1384_0  COME_FROM          1370  '1370'

 L. 746      1384  LOAD_GLOBAL              vis_msg
             1386  LOAD_ATTR                print
             1388  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Non-positive epoch number'
             1390  LOAD_STR                 'error'
             1392  LOAD_CONST               ('type',)
             1394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1396  POP_TOP          

 L. 747      1398  LOAD_GLOBAL              QtWidgets
             1400  LOAD_ATTR                QMessageBox
             1402  LOAD_METHOD              critical
             1404  LOAD_DEREF               'self'
             1406  LOAD_ATTR                msgbox

 L. 748      1408  LOAD_STR                 'Train 2D-WDCNN'

 L. 749      1410  LOAD_STR                 'Non-positive epoch number'
             1412  CALL_METHOD_3         3  '3 positional arguments'
             1414  POP_TOP          

 L. 750      1416  LOAD_CONST               None
             1418  RETURN_VALUE     
           1420_0  COME_FROM          1380  '1380'

 L. 751      1420  LOAD_FAST                '_batchsize'
             1422  LOAD_CONST               False
             1424  COMPARE_OP               is
         1426_1428  POP_JUMP_IF_TRUE   1440  'to 1440'
             1430  LOAD_FAST                '_batchsize'
             1432  LOAD_CONST               0
             1434  COMPARE_OP               <=
         1436_1438  POP_JUMP_IF_FALSE  1476  'to 1476'
           1440_0  COME_FROM          1426  '1426'

 L. 752      1440  LOAD_GLOBAL              vis_msg
             1442  LOAD_ATTR                print
             1444  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Non-positive batch size'
             1446  LOAD_STR                 'error'
             1448  LOAD_CONST               ('type',)
             1450  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1452  POP_TOP          

 L. 753      1454  LOAD_GLOBAL              QtWidgets
             1456  LOAD_ATTR                QMessageBox
             1458  LOAD_METHOD              critical
             1460  LOAD_DEREF               'self'
             1462  LOAD_ATTR                msgbox

 L. 754      1464  LOAD_STR                 'Train 2D-WDCNN'

 L. 755      1466  LOAD_STR                 'Non-positive batch size'
             1468  CALL_METHOD_3         3  '3 positional arguments'
             1470  POP_TOP          

 L. 756      1472  LOAD_CONST               None
             1474  RETURN_VALUE     
           1476_0  COME_FROM          1436  '1436'

 L. 757      1476  LOAD_FAST                '_learning_rate'
             1478  LOAD_CONST               False
             1480  COMPARE_OP               is
         1482_1484  POP_JUMP_IF_TRUE   1496  'to 1496'
             1486  LOAD_FAST                '_learning_rate'
             1488  LOAD_CONST               0
             1490  COMPARE_OP               <=
         1492_1494  POP_JUMP_IF_FALSE  1532  'to 1532'
           1496_0  COME_FROM          1482  '1482'

 L. 758      1496  LOAD_GLOBAL              vis_msg
             1498  LOAD_ATTR                print
             1500  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Non-positive learning rate'
             1502  LOAD_STR                 'error'
             1504  LOAD_CONST               ('type',)
             1506  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1508  POP_TOP          

 L. 759      1510  LOAD_GLOBAL              QtWidgets
             1512  LOAD_ATTR                QMessageBox
             1514  LOAD_METHOD              critical
             1516  LOAD_DEREF               'self'
             1518  LOAD_ATTR                msgbox

 L. 760      1520  LOAD_STR                 'Train 2D-WDCNN'

 L. 761      1522  LOAD_STR                 'Non-positive learning rate'
             1524  CALL_METHOD_3         3  '3 positional arguments'
             1526  POP_TOP          

 L. 762      1528  LOAD_CONST               None
             1530  RETURN_VALUE     
           1532_0  COME_FROM          1492  '1492'

 L. 763      1532  LOAD_FAST                '_dropout_prob'
             1534  LOAD_CONST               False
             1536  COMPARE_OP               is
         1538_1540  POP_JUMP_IF_TRUE   1552  'to 1552'
             1542  LOAD_FAST                '_dropout_prob'
             1544  LOAD_CONST               0
             1546  COMPARE_OP               <=
         1548_1550  POP_JUMP_IF_FALSE  1588  'to 1588'
           1552_0  COME_FROM          1538  '1538'

 L. 764      1552  LOAD_GLOBAL              vis_msg
             1554  LOAD_ATTR                print
             1556  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: Negative dropout rate'
             1558  LOAD_STR                 'error'
             1560  LOAD_CONST               ('type',)
             1562  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1564  POP_TOP          

 L. 765      1566  LOAD_GLOBAL              QtWidgets
             1568  LOAD_ATTR                QMessageBox
             1570  LOAD_METHOD              critical
             1572  LOAD_DEREF               'self'
             1574  LOAD_ATTR                msgbox

 L. 766      1576  LOAD_STR                 'Train 2D-WDCNN'

 L. 767      1578  LOAD_STR                 'Negative dropout rate'
             1580  CALL_METHOD_3         3  '3 positional arguments'
             1582  POP_TOP          

 L. 768      1584  LOAD_CONST               None
             1586  RETURN_VALUE     
           1588_0  COME_FROM          1548  '1548'

 L. 770      1588  LOAD_GLOBAL              len
             1590  LOAD_DEREF               'self'
             1592  LOAD_ATTR                ldtsave
             1594  LOAD_METHOD              text
             1596  CALL_METHOD_0         0  '0 positional arguments'
             1598  CALL_FUNCTION_1       1  '1 positional argument'
             1600  LOAD_CONST               1
             1602  COMPARE_OP               <
         1604_1606  POP_JUMP_IF_FALSE  1644  'to 1644'

 L. 771      1608  LOAD_GLOBAL              vis_msg
             1610  LOAD_ATTR                print
             1612  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: No name specified for new-WDCNN'
             1614  LOAD_STR                 'error'
             1616  LOAD_CONST               ('type',)
             1618  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1620  POP_TOP          

 L. 772      1622  LOAD_GLOBAL              QtWidgets
             1624  LOAD_ATTR                QMessageBox
             1626  LOAD_METHOD              critical
             1628  LOAD_DEREF               'self'
             1630  LOAD_ATTR                msgbox

 L. 773      1632  LOAD_STR                 'Train 2D-WDCNN'

 L. 774      1634  LOAD_STR                 'No name specified for new-WDCNN'
             1636  CALL_METHOD_3         3  '3 positional arguments'
             1638  POP_TOP          

 L. 775      1640  LOAD_CONST               None
             1642  RETURN_VALUE     
           1644_0  COME_FROM          1604  '1604'

 L. 776      1644  LOAD_GLOBAL              os
             1646  LOAD_ATTR                path
             1648  LOAD_METHOD              dirname
             1650  LOAD_DEREF               'self'
             1652  LOAD_ATTR                ldtsave
             1654  LOAD_METHOD              text
             1656  CALL_METHOD_0         0  '0 positional arguments'
             1658  CALL_METHOD_1         1  '1 positional argument'
             1660  STORE_FAST               '_savepath'

 L. 777      1662  LOAD_GLOBAL              os
             1664  LOAD_ATTR                path
             1666  LOAD_METHOD              splitext
             1668  LOAD_GLOBAL              os
             1670  LOAD_ATTR                path
             1672  LOAD_METHOD              basename
             1674  LOAD_DEREF               'self'
             1676  LOAD_ATTR                ldtsave
             1678  LOAD_METHOD              text
             1680  CALL_METHOD_0         0  '0 positional arguments'
             1682  CALL_METHOD_1         1  '1 positional argument'
             1684  CALL_METHOD_1         1  '1 positional argument'
             1686  LOAD_CONST               0
             1688  BINARY_SUBSCR    
             1690  STORE_FAST               '_savename'

 L. 779      1692  LOAD_CONST               0
             1694  STORE_FAST               '_wdinl'

 L. 780      1696  LOAD_CONST               0
             1698  STORE_FAST               '_wdxl'

 L. 781      1700  LOAD_CONST               0
             1702  STORE_FAST               '_wdz'

 L. 782      1704  LOAD_DEREF               'self'
             1706  LOAD_ATTR                cbbornt
             1708  LOAD_METHOD              currentIndex
             1710  CALL_METHOD_0         0  '0 positional arguments'
             1712  LOAD_CONST               0
             1714  COMPARE_OP               ==
         1716_1718  POP_JUMP_IF_FALSE  1744  'to 1744'

 L. 783      1720  LOAD_GLOBAL              int
             1722  LOAD_FAST                '_image_width'
             1724  LOAD_CONST               2
             1726  BINARY_TRUE_DIVIDE
             1728  CALL_FUNCTION_1       1  '1 positional argument'
             1730  STORE_FAST               '_wdxl'

 L. 784      1732  LOAD_GLOBAL              int
             1734  LOAD_FAST                '_image_height'
             1736  LOAD_CONST               2
             1738  BINARY_TRUE_DIVIDE
             1740  CALL_FUNCTION_1       1  '1 positional argument'
             1742  STORE_FAST               '_wdz'
           1744_0  COME_FROM          1716  '1716'

 L. 785      1744  LOAD_DEREF               'self'
             1746  LOAD_ATTR                cbbornt
             1748  LOAD_METHOD              currentIndex
             1750  CALL_METHOD_0         0  '0 positional arguments'
             1752  LOAD_CONST               1
             1754  COMPARE_OP               ==
         1756_1758  POP_JUMP_IF_FALSE  1784  'to 1784'

 L. 786      1760  LOAD_GLOBAL              int
             1762  LOAD_FAST                '_image_width'
             1764  LOAD_CONST               2
             1766  BINARY_TRUE_DIVIDE
             1768  CALL_FUNCTION_1       1  '1 positional argument'
             1770  STORE_FAST               '_wdinl'

 L. 787      1772  LOAD_GLOBAL              int
             1774  LOAD_FAST                '_image_height'
             1776  LOAD_CONST               2
             1778  BINARY_TRUE_DIVIDE
             1780  CALL_FUNCTION_1       1  '1 positional argument'
             1782  STORE_FAST               '_wdz'
           1784_0  COME_FROM          1756  '1756'

 L. 788      1784  LOAD_DEREF               'self'
             1786  LOAD_ATTR                cbbornt
             1788  LOAD_METHOD              currentIndex
             1790  CALL_METHOD_0         0  '0 positional arguments'
             1792  LOAD_CONST               2
             1794  COMPARE_OP               ==
         1796_1798  POP_JUMP_IF_FALSE  1824  'to 1824'

 L. 789      1800  LOAD_GLOBAL              int
             1802  LOAD_FAST                '_image_width'
             1804  LOAD_CONST               2
             1806  BINARY_TRUE_DIVIDE
             1808  CALL_FUNCTION_1       1  '1 positional argument'
             1810  STORE_FAST               '_wdinl'

 L. 790      1812  LOAD_GLOBAL              int
             1814  LOAD_FAST                '_image_height'
             1816  LOAD_CONST               2
             1818  BINARY_TRUE_DIVIDE
             1820  CALL_FUNCTION_1       1  '1 positional argument'
             1822  STORE_FAST               '_wdxl'
           1824_0  COME_FROM          1796  '1796'

 L. 792      1824  LOAD_DEREF               'self'
             1826  LOAD_ATTR                survinfo
             1828  STORE_FAST               '_seisinfo'

 L. 794      1830  LOAD_GLOBAL              print
             1832  LOAD_STR                 'TrainMl2DWdcnnFromExisting: Step 1 - Step 1 - Get training samples:'
             1834  CALL_FUNCTION_1       1  '1 positional argument'
             1836  POP_TOP          

 L. 795      1838  LOAD_DEREF               'self'
             1840  LOAD_ATTR                traindataconfig
             1842  LOAD_STR                 'TrainPointSet'
             1844  BINARY_SUBSCR    
             1846  STORE_FAST               '_trainpoint'

 L. 796      1848  LOAD_GLOBAL              np
             1850  LOAD_METHOD              zeros
             1852  LOAD_CONST               0
             1854  LOAD_CONST               3
             1856  BUILD_LIST_2          2 
             1858  CALL_METHOD_1         1  '1 positional argument'
             1860  STORE_FAST               '_traindata'

 L. 797      1862  SETUP_LOOP         1938  'to 1938'
             1864  LOAD_FAST                '_trainpoint'
             1866  GET_ITER         
           1868_0  COME_FROM          1886  '1886'
             1868  FOR_ITER           1936  'to 1936'
             1870  STORE_FAST               '_p'

 L. 798      1872  LOAD_GLOBAL              point_ays
             1874  LOAD_METHOD              checkPoint
             1876  LOAD_DEREF               'self'
             1878  LOAD_ATTR                pointsetdata
             1880  LOAD_FAST                '_p'
             1882  BINARY_SUBSCR    
             1884  CALL_METHOD_1         1  '1 positional argument'
         1886_1888  POP_JUMP_IF_FALSE  1868  'to 1868'

 L. 799      1890  LOAD_GLOBAL              basic_mdt
             1892  LOAD_METHOD              exportMatDict
             1894  LOAD_DEREF               'self'
             1896  LOAD_ATTR                pointsetdata
             1898  LOAD_FAST                '_p'
             1900  BINARY_SUBSCR    
             1902  LOAD_STR                 'Inline'
             1904  LOAD_STR                 'Crossline'
             1906  LOAD_STR                 'Z'
             1908  BUILD_LIST_3          3 
             1910  CALL_METHOD_2         2  '2 positional arguments'
             1912  STORE_FAST               '_pt'

 L. 800      1914  LOAD_GLOBAL              np
             1916  LOAD_ATTR                concatenate
             1918  LOAD_FAST                '_traindata'
             1920  LOAD_FAST                '_pt'
             1922  BUILD_TUPLE_2         2 
             1924  LOAD_CONST               0
             1926  LOAD_CONST               ('axis',)
             1928  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1930  STORE_FAST               '_traindata'
         1932_1934  JUMP_BACK          1868  'to 1868'
             1936  POP_BLOCK        
           1938_0  COME_FROM_LOOP     1862  '1862'

 L. 801      1938  LOAD_GLOBAL              seis_ays
             1940  LOAD_ATTR                removeOutofSurveySample
             1942  LOAD_FAST                '_traindata'

 L. 802      1944  LOAD_FAST                '_seisinfo'
             1946  LOAD_STR                 'ILStart'
             1948  BINARY_SUBSCR    
             1950  LOAD_FAST                '_wdinl'
             1952  LOAD_FAST                '_seisinfo'
             1954  LOAD_STR                 'ILStep'
             1956  BINARY_SUBSCR    
             1958  BINARY_MULTIPLY  
             1960  BINARY_ADD       

 L. 803      1962  LOAD_FAST                '_seisinfo'
             1964  LOAD_STR                 'ILEnd'
             1966  BINARY_SUBSCR    
             1968  LOAD_FAST                '_wdinl'
             1970  LOAD_FAST                '_seisinfo'
             1972  LOAD_STR                 'ILStep'
             1974  BINARY_SUBSCR    
             1976  BINARY_MULTIPLY  
             1978  BINARY_SUBTRACT  

 L. 804      1980  LOAD_FAST                '_seisinfo'
             1982  LOAD_STR                 'XLStart'
             1984  BINARY_SUBSCR    
             1986  LOAD_FAST                '_wdxl'
             1988  LOAD_FAST                '_seisinfo'
             1990  LOAD_STR                 'XLStep'
             1992  BINARY_SUBSCR    
             1994  BINARY_MULTIPLY  
             1996  BINARY_ADD       

 L. 805      1998  LOAD_FAST                '_seisinfo'
             2000  LOAD_STR                 'XLEnd'
             2002  BINARY_SUBSCR    
             2004  LOAD_FAST                '_wdxl'
             2006  LOAD_FAST                '_seisinfo'
             2008  LOAD_STR                 'XLStep'
             2010  BINARY_SUBSCR    
             2012  BINARY_MULTIPLY  
             2014  BINARY_SUBTRACT  

 L. 806      2016  LOAD_FAST                '_seisinfo'
             2018  LOAD_STR                 'ZStart'
             2020  BINARY_SUBSCR    
             2022  LOAD_FAST                '_wdz'
             2024  LOAD_FAST                '_seisinfo'
             2026  LOAD_STR                 'ZStep'
             2028  BINARY_SUBSCR    
             2030  BINARY_MULTIPLY  
             2032  BINARY_ADD       

 L. 807      2034  LOAD_FAST                '_seisinfo'
             2036  LOAD_STR                 'ZEnd'
             2038  BINARY_SUBSCR    
             2040  LOAD_FAST                '_wdz'
             2042  LOAD_FAST                '_seisinfo'
             2044  LOAD_STR                 'ZStep'
             2046  BINARY_SUBSCR    
             2048  BINARY_MULTIPLY  
             2050  BINARY_SUBTRACT  
             2052  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             2054  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2056  STORE_FAST               '_traindata'

 L. 810      2058  LOAD_GLOBAL              np
             2060  LOAD_METHOD              shape
             2062  LOAD_FAST                '_traindata'
             2064  CALL_METHOD_1         1  '1 positional argument'
             2066  LOAD_CONST               0
             2068  BINARY_SUBSCR    
             2070  LOAD_CONST               0
             2072  COMPARE_OP               <=
         2074_2076  POP_JUMP_IF_FALSE  2114  'to 2114'

 L. 811      2078  LOAD_GLOBAL              vis_msg
             2080  LOAD_ATTR                print
             2082  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: No training sample found'
             2084  LOAD_STR                 'error'
             2086  LOAD_CONST               ('type',)
             2088  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2090  POP_TOP          

 L. 812      2092  LOAD_GLOBAL              QtWidgets
             2094  LOAD_ATTR                QMessageBox
             2096  LOAD_METHOD              critical
             2098  LOAD_DEREF               'self'
             2100  LOAD_ATTR                msgbox

 L. 813      2102  LOAD_STR                 'Train 2D-WDCNN'

 L. 814      2104  LOAD_STR                 'No training sample found'
             2106  CALL_METHOD_3         3  '3 positional arguments'
             2108  POP_TOP          

 L. 815      2110  LOAD_CONST               None
             2112  RETURN_VALUE     
           2114_0  COME_FROM          2074  '2074'

 L. 818      2114  LOAD_GLOBAL              print
             2116  LOAD_STR                 'TrainMl2DWdcnnFromExisting: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 819      2118  LOAD_FAST                '_image_height'
             2120  LOAD_FAST                '_image_width'
             2122  LOAD_FAST                '_image_height_new'
             2124  LOAD_FAST                '_image_width_new'
             2126  BUILD_TUPLE_4         4 
             2128  BINARY_MODULO    
             2130  CALL_FUNCTION_1       1  '1 positional argument'
             2132  POP_TOP          

 L. 820      2134  BUILD_MAP_0           0 
             2136  STORE_FAST               '_traindict'

 L. 821      2138  SETUP_LOOP         2210  'to 2210'
             2140  LOAD_FAST                '_features'
             2142  GET_ITER         
             2144  FOR_ITER           2208  'to 2208'
             2146  STORE_FAST               'f'

 L. 822      2148  LOAD_DEREF               'self'
             2150  LOAD_ATTR                seisdata
             2152  LOAD_FAST                'f'
             2154  BINARY_SUBSCR    
             2156  STORE_FAST               '_seisdata'

 L. 823      2158  LOAD_GLOBAL              seis_ays
             2160  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2162  LOAD_FAST                '_seisdata'
             2164  LOAD_FAST                '_traindata'
             2166  LOAD_DEREF               'self'
             2168  LOAD_ATTR                survinfo

 L. 824      2170  LOAD_FAST                '_wdinl'
             2172  LOAD_FAST                '_wdxl'
             2174  LOAD_FAST                '_wdz'

 L. 825      2176  LOAD_CONST               False
             2178  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2180  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2182  LOAD_CONST               None
             2184  LOAD_CONST               None
             2186  BUILD_SLICE_2         2 
             2188  LOAD_CONST               3
             2190  LOAD_CONST               None
             2192  BUILD_SLICE_2         2 
             2194  BUILD_TUPLE_2         2 
             2196  BINARY_SUBSCR    
             2198  LOAD_FAST                '_traindict'
             2200  LOAD_FAST                'f'
             2202  STORE_SUBSCR     
         2204_2206  JUMP_BACK          2144  'to 2144'
             2208  POP_BLOCK        
           2210_0  COME_FROM_LOOP     2138  '2138'

 L. 826      2210  LOAD_FAST                '_target'
             2212  LOAD_FAST                '_features'
             2214  COMPARE_OP               not-in
         2216_2218  POP_JUMP_IF_FALSE  2276  'to 2276'

 L. 827      2220  LOAD_DEREF               'self'
             2222  LOAD_ATTR                seisdata
             2224  LOAD_FAST                '_target'
             2226  BINARY_SUBSCR    
             2228  STORE_FAST               '_seisdata'

 L. 828      2230  LOAD_GLOBAL              seis_ays
             2232  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2234  LOAD_FAST                '_seisdata'
             2236  LOAD_FAST                '_traindata'
             2238  LOAD_DEREF               'self'
             2240  LOAD_ATTR                survinfo

 L. 829      2242  LOAD_FAST                '_wdinl'

 L. 830      2244  LOAD_FAST                '_wdxl'

 L. 831      2246  LOAD_FAST                '_wdz'

 L. 832      2248  LOAD_CONST               False
             2250  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2252  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2254  LOAD_CONST               None
             2256  LOAD_CONST               None
             2258  BUILD_SLICE_2         2 
             2260  LOAD_CONST               3
             2262  LOAD_CONST               None
             2264  BUILD_SLICE_2         2 
             2266  BUILD_TUPLE_2         2 
             2268  BINARY_SUBSCR    
             2270  LOAD_FAST                '_traindict'
             2272  LOAD_FAST                '_target'
             2274  STORE_SUBSCR     
           2276_0  COME_FROM          2216  '2216'

 L. 833      2276  LOAD_FAST                '_weight'
             2278  LOAD_FAST                '_features'
             2280  COMPARE_OP               not-in
         2282_2284  POP_JUMP_IF_FALSE  2352  'to 2352'
             2286  LOAD_FAST                '_weight'
             2288  LOAD_FAST                '_target'
             2290  COMPARE_OP               !=
         2292_2294  POP_JUMP_IF_FALSE  2352  'to 2352'

 L. 834      2296  LOAD_DEREF               'self'
             2298  LOAD_ATTR                seisdata
             2300  LOAD_FAST                '_weight'
             2302  BINARY_SUBSCR    
             2304  STORE_FAST               '_seisdata'

 L. 835      2306  LOAD_GLOBAL              seis_ays
             2308  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2310  LOAD_FAST                '_seisdata'
             2312  LOAD_FAST                '_traindata'
             2314  LOAD_DEREF               'self'
             2316  LOAD_ATTR                survinfo

 L. 836      2318  LOAD_FAST                '_wdinl'

 L. 837      2320  LOAD_FAST                '_wdxl'

 L. 838      2322  LOAD_FAST                '_wdz'

 L. 839      2324  LOAD_CONST               False
             2326  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2328  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2330  LOAD_CONST               None
             2332  LOAD_CONST               None
             2334  BUILD_SLICE_2         2 
             2336  LOAD_CONST               3
             2338  LOAD_CONST               None
             2340  BUILD_SLICE_2         2 
             2342  BUILD_TUPLE_2         2 
             2344  BINARY_SUBSCR    
             2346  LOAD_FAST                '_traindict'
             2348  LOAD_FAST                '_weight'
             2350  STORE_SUBSCR     
           2352_0  COME_FROM          2292  '2292'
           2352_1  COME_FROM          2282  '2282'

 L. 841      2352  LOAD_DEREF               'self'
             2354  LOAD_ATTR                traindataconfig
             2356  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2358  BINARY_SUBSCR    
         2360_2362  POP_JUMP_IF_FALSE  2444  'to 2444'

 L. 842      2364  SETUP_LOOP         2444  'to 2444'
             2366  LOAD_FAST                '_features'
             2368  GET_ITER         
           2370_0  COME_FROM          2398  '2398'
             2370  FOR_ITER           2442  'to 2442'
             2372  STORE_FAST               'f'

 L. 843      2374  LOAD_GLOBAL              ml_aug
             2376  LOAD_METHOD              removeInvariantFeature
             2378  LOAD_FAST                '_traindict'
             2380  LOAD_FAST                'f'
             2382  CALL_METHOD_2         2  '2 positional arguments'
             2384  STORE_FAST               '_traindict'

 L. 844      2386  LOAD_GLOBAL              basic_mdt
             2388  LOAD_METHOD              maxDictConstantRow
             2390  LOAD_FAST                '_traindict'
             2392  CALL_METHOD_1         1  '1 positional argument'
             2394  LOAD_CONST               0
             2396  COMPARE_OP               <=
         2398_2400  POP_JUMP_IF_FALSE  2370  'to 2370'

 L. 845      2402  LOAD_GLOBAL              vis_msg
             2404  LOAD_ATTR                print
             2406  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: No training sample found'
             2408  LOAD_STR                 'error'
             2410  LOAD_CONST               ('type',)
             2412  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2414  POP_TOP          

 L. 846      2416  LOAD_GLOBAL              QtWidgets
             2418  LOAD_ATTR                QMessageBox
             2420  LOAD_METHOD              critical
             2422  LOAD_DEREF               'self'
             2424  LOAD_ATTR                msgbox

 L. 847      2426  LOAD_STR                 'Train 2D-WDCNN'

 L. 848      2428  LOAD_STR                 'No training sample found'
             2430  CALL_METHOD_3         3  '3 positional arguments'
             2432  POP_TOP          

 L. 849      2434  LOAD_CONST               None
             2436  RETURN_VALUE     
         2438_2440  JUMP_BACK          2370  'to 2370'
             2442  POP_BLOCK        
           2444_0  COME_FROM_LOOP     2364  '2364'
           2444_1  COME_FROM          2360  '2360'

 L. 850      2444  LOAD_DEREF               'self'
             2446  LOAD_ATTR                traindataconfig
             2448  LOAD_STR                 'RemoveZeroWeight_Checked'
             2450  BINARY_SUBSCR    
         2452_2454  POP_JUMP_IF_FALSE  2520  'to 2520'

 L. 851      2456  LOAD_GLOBAL              ml_aug
             2458  LOAD_METHOD              removeZeroWeight
             2460  LOAD_FAST                '_traindict'
             2462  LOAD_FAST                '_weight'
             2464  CALL_METHOD_2         2  '2 positional arguments'
             2466  STORE_FAST               '_traindict'

 L. 852      2468  LOAD_GLOBAL              basic_mdt
             2470  LOAD_METHOD              maxDictConstantRow
             2472  LOAD_FAST                '_traindict'
             2474  CALL_METHOD_1         1  '1 positional argument'
             2476  LOAD_CONST               0
             2478  COMPARE_OP               <=
         2480_2482  POP_JUMP_IF_FALSE  2520  'to 2520'

 L. 853      2484  LOAD_GLOBAL              vis_msg
             2486  LOAD_ATTR                print
             2488  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: No training sample found'
             2490  LOAD_STR                 'error'
             2492  LOAD_CONST               ('type',)
             2494  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2496  POP_TOP          

 L. 854      2498  LOAD_GLOBAL              QtWidgets
             2500  LOAD_ATTR                QMessageBox
             2502  LOAD_METHOD              critical
             2504  LOAD_DEREF               'self'
             2506  LOAD_ATTR                msgbox

 L. 855      2508  LOAD_STR                 'Train 2D-WDCNN'

 L. 856      2510  LOAD_STR                 'No training sample found'
             2512  CALL_METHOD_3         3  '3 positional arguments'
             2514  POP_TOP          

 L. 857      2516  LOAD_CONST               None
             2518  RETURN_VALUE     
           2520_0  COME_FROM          2480  '2480'
           2520_1  COME_FROM          2452  '2452'

 L. 859      2520  LOAD_GLOBAL              np
             2522  LOAD_METHOD              shape
             2524  LOAD_FAST                '_traindict'
             2526  LOAD_FAST                '_target'
             2528  BINARY_SUBSCR    
             2530  CALL_METHOD_1         1  '1 positional argument'
             2532  LOAD_CONST               0
             2534  BINARY_SUBSCR    
             2536  LOAD_CONST               0
             2538  COMPARE_OP               <=
         2540_2542  POP_JUMP_IF_FALSE  2580  'to 2580'

 L. 860      2544  LOAD_GLOBAL              vis_msg
             2546  LOAD_ATTR                print
             2548  LOAD_STR                 'ERROR in TrainMl2DWdcnnFromExisting: No training sample found'
             2550  LOAD_STR                 'error'
             2552  LOAD_CONST               ('type',)
             2554  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2556  POP_TOP          

 L. 861      2558  LOAD_GLOBAL              QtWidgets
             2560  LOAD_ATTR                QMessageBox
             2562  LOAD_METHOD              critical
             2564  LOAD_DEREF               'self'
             2566  LOAD_ATTR                msgbox

 L. 862      2568  LOAD_STR                 'Train 2D-WDCNN'

 L. 863      2570  LOAD_STR                 'No training sample found'
             2572  CALL_METHOD_3         3  '3 positional arguments'
             2574  POP_TOP          

 L. 864      2576  LOAD_CONST               None
             2578  RETURN_VALUE     
           2580_0  COME_FROM          2540  '2540'

 L. 866      2580  LOAD_FAST                '_image_height_new'
             2582  LOAD_FAST                '_image_height'
             2584  COMPARE_OP               !=
         2586_2588  POP_JUMP_IF_TRUE   2600  'to 2600'
             2590  LOAD_FAST                '_image_width_new'
             2592  LOAD_FAST                '_image_width'
             2594  COMPARE_OP               !=
         2596_2598  POP_JUMP_IF_FALSE  2734  'to 2734'
           2600_0  COME_FROM          2586  '2586'

 L. 867      2600  SETUP_LOOP         2644  'to 2644'
             2602  LOAD_FAST                '_features'
             2604  GET_ITER         
             2606  FOR_ITER           2642  'to 2642'
             2608  STORE_FAST               'f'

 L. 868      2610  LOAD_GLOBAL              basic_image
             2612  LOAD_ATTR                changeImageSize
             2614  LOAD_FAST                '_traindict'
             2616  LOAD_FAST                'f'
             2618  BINARY_SUBSCR    

 L. 869      2620  LOAD_FAST                '_image_height'

 L. 870      2622  LOAD_FAST                '_image_width'

 L. 871      2624  LOAD_FAST                '_image_height_new'

 L. 872      2626  LOAD_FAST                '_image_width_new'
             2628  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2630  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2632  LOAD_FAST                '_traindict'
             2634  LOAD_FAST                'f'
             2636  STORE_SUBSCR     
         2638_2640  JUMP_BACK          2606  'to 2606'
             2642  POP_BLOCK        
           2644_0  COME_FROM_LOOP     2600  '2600'

 L. 873      2644  LOAD_FAST                '_target'
             2646  LOAD_FAST                '_features'
             2648  COMPARE_OP               not-in
         2650_2652  POP_JUMP_IF_FALSE  2684  'to 2684'

 L. 874      2654  LOAD_GLOBAL              basic_image
             2656  LOAD_ATTR                changeImageSize
             2658  LOAD_FAST                '_traindict'
             2660  LOAD_FAST                '_target'
             2662  BINARY_SUBSCR    

 L. 875      2664  LOAD_FAST                '_image_height'

 L. 876      2666  LOAD_FAST                '_image_width'

 L. 877      2668  LOAD_FAST                '_image_height_new'

 L. 878      2670  LOAD_FAST                '_image_width_new'
             2672  LOAD_STR                 'linear'
             2674  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2676  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2678  LOAD_FAST                '_traindict'
             2680  LOAD_FAST                '_target'
             2682  STORE_SUBSCR     
           2684_0  COME_FROM          2650  '2650'

 L. 879      2684  LOAD_FAST                '_weight'
             2686  LOAD_FAST                '_features'
             2688  COMPARE_OP               not-in
         2690_2692  POP_JUMP_IF_FALSE  2734  'to 2734'
             2694  LOAD_FAST                '_weight'
             2696  LOAD_FAST                '_target'
             2698  COMPARE_OP               !=
         2700_2702  POP_JUMP_IF_FALSE  2734  'to 2734'

 L. 880      2704  LOAD_GLOBAL              basic_image
             2706  LOAD_ATTR                changeImageSize
             2708  LOAD_FAST                '_traindict'
             2710  LOAD_FAST                '_weight'
             2712  BINARY_SUBSCR    

 L. 881      2714  LOAD_FAST                '_image_height'

 L. 882      2716  LOAD_FAST                '_image_width'

 L. 883      2718  LOAD_FAST                '_image_height_new'

 L. 884      2720  LOAD_FAST                '_image_width_new'
             2722  LOAD_STR                 'linear'
             2724  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2726  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2728  LOAD_FAST                '_traindict'
             2730  LOAD_FAST                '_weight'
             2732  STORE_SUBSCR     
           2734_0  COME_FROM          2700  '2700'
           2734_1  COME_FROM          2690  '2690'
           2734_2  COME_FROM          2596  '2596'

 L. 885      2734  LOAD_DEREF               'self'
             2736  LOAD_ATTR                traindataconfig
             2738  LOAD_STR                 'RotateFeature_Checked'
             2740  BINARY_SUBSCR    
             2742  LOAD_CONST               True
             2744  COMPARE_OP               is
         2746_2748  POP_JUMP_IF_FALSE  2964  'to 2964'

 L. 886      2750  SETUP_LOOP         2822  'to 2822'
             2752  LOAD_FAST                '_features'
             2754  GET_ITER         
             2756  FOR_ITER           2820  'to 2820'
             2758  STORE_FAST               'f'

 L. 887      2760  LOAD_FAST                '_image_height_new'
             2762  LOAD_FAST                '_image_width_new'
             2764  COMPARE_OP               ==
         2766_2768  POP_JUMP_IF_FALSE  2794  'to 2794'

 L. 888      2770  LOAD_GLOBAL              ml_aug
             2772  LOAD_METHOD              rotateImage6Way
             2774  LOAD_FAST                '_traindict'
             2776  LOAD_FAST                'f'
             2778  BINARY_SUBSCR    
             2780  LOAD_FAST                '_image_height_new'
             2782  LOAD_FAST                '_image_width_new'
             2784  CALL_METHOD_3         3  '3 positional arguments'
             2786  LOAD_FAST                '_traindict'
             2788  LOAD_FAST                'f'
             2790  STORE_SUBSCR     
             2792  JUMP_BACK          2756  'to 2756'
           2794_0  COME_FROM          2766  '2766'

 L. 890      2794  LOAD_GLOBAL              ml_aug
             2796  LOAD_METHOD              rotateImage4Way
             2798  LOAD_FAST                '_traindict'
             2800  LOAD_FAST                'f'
             2802  BINARY_SUBSCR    
             2804  LOAD_FAST                '_image_height_new'
             2806  LOAD_FAST                '_image_width_new'
             2808  CALL_METHOD_3         3  '3 positional arguments'
             2810  LOAD_FAST                '_traindict'
             2812  LOAD_FAST                'f'
             2814  STORE_SUBSCR     
         2816_2818  JUMP_BACK          2756  'to 2756'
             2820  POP_BLOCK        
           2822_0  COME_FROM_LOOP     2750  '2750'

 L. 891      2822  LOAD_FAST                '_target'
             2824  LOAD_FAST                '_features'
             2826  COMPARE_OP               not-in
         2828_2830  POP_JUMP_IF_FALSE  2888  'to 2888'

 L. 892      2832  LOAD_FAST                '_image_height_new'
             2834  LOAD_FAST                '_image_width_new'
             2836  COMPARE_OP               ==
         2838_2840  POP_JUMP_IF_FALSE  2866  'to 2866'

 L. 894      2842  LOAD_GLOBAL              ml_aug
             2844  LOAD_METHOD              rotateImage6Way
             2846  LOAD_FAST                '_traindict'
             2848  LOAD_FAST                '_target'
             2850  BINARY_SUBSCR    
             2852  LOAD_FAST                '_image_height_new'
             2854  LOAD_FAST                '_image_width_new'
             2856  CALL_METHOD_3         3  '3 positional arguments'
             2858  LOAD_FAST                '_traindict'
             2860  LOAD_FAST                '_target'
             2862  STORE_SUBSCR     
             2864  JUMP_FORWARD       2888  'to 2888'
           2866_0  COME_FROM          2838  '2838'

 L. 897      2866  LOAD_GLOBAL              ml_aug
             2868  LOAD_METHOD              rotateImage4Way
             2870  LOAD_FAST                '_traindict'
             2872  LOAD_FAST                '_target'
             2874  BINARY_SUBSCR    
             2876  LOAD_FAST                '_image_height_new'
             2878  LOAD_FAST                '_image_width_new'
             2880  CALL_METHOD_3         3  '3 positional arguments'
             2882  LOAD_FAST                '_traindict'
             2884  LOAD_FAST                '_target'
             2886  STORE_SUBSCR     
           2888_0  COME_FROM          2864  '2864'
           2888_1  COME_FROM          2828  '2828'

 L. 898      2888  LOAD_FAST                '_weight'
             2890  LOAD_FAST                '_features'
             2892  COMPARE_OP               not-in
         2894_2896  POP_JUMP_IF_FALSE  2964  'to 2964'
             2898  LOAD_FAST                '_weight'
             2900  LOAD_FAST                '_target'
             2902  COMPARE_OP               !=
         2904_2906  POP_JUMP_IF_FALSE  2964  'to 2964'

 L. 899      2908  LOAD_FAST                '_image_height_new'
             2910  LOAD_FAST                '_image_width_new'
             2912  COMPARE_OP               ==
         2914_2916  POP_JUMP_IF_FALSE  2942  'to 2942'

 L. 901      2918  LOAD_GLOBAL              ml_aug
             2920  LOAD_METHOD              rotateImage6Way
             2922  LOAD_FAST                '_traindict'
             2924  LOAD_FAST                '_weight'
             2926  BINARY_SUBSCR    
             2928  LOAD_FAST                '_image_height_new'
             2930  LOAD_FAST                '_image_width_new'
             2932  CALL_METHOD_3         3  '3 positional arguments'
             2934  LOAD_FAST                '_traindict'
             2936  LOAD_FAST                '_weight'
             2938  STORE_SUBSCR     
             2940  JUMP_FORWARD       2964  'to 2964'
           2942_0  COME_FROM          2914  '2914'

 L. 904      2942  LOAD_GLOBAL              ml_aug
             2944  LOAD_METHOD              rotateImage4Way
             2946  LOAD_FAST                '_traindict'
             2948  LOAD_FAST                '_weight'
             2950  BINARY_SUBSCR    
             2952  LOAD_FAST                '_image_height_new'
             2954  LOAD_FAST                '_image_width_new'
             2956  CALL_METHOD_3         3  '3 positional arguments'
             2958  LOAD_FAST                '_traindict'
             2960  LOAD_FAST                '_weight'
             2962  STORE_SUBSCR     
           2964_0  COME_FROM          2940  '2940'
           2964_1  COME_FROM          2904  '2904'
           2964_2  COME_FROM          2894  '2894'
           2964_3  COME_FROM          2746  '2746'

 L. 906      2964  LOAD_GLOBAL              np
             2966  LOAD_METHOD              round
             2968  LOAD_FAST                '_traindict'
             2970  LOAD_FAST                '_target'
             2972  BINARY_SUBSCR    
             2974  CALL_METHOD_1         1  '1 positional argument'
             2976  LOAD_METHOD              astype
             2978  LOAD_GLOBAL              int
             2980  CALL_METHOD_1         1  '1 positional argument'
             2982  LOAD_FAST                '_traindict'
             2984  LOAD_FAST                '_target'
             2986  STORE_SUBSCR     

 L. 909      2988  LOAD_GLOBAL              print
             2990  LOAD_STR                 'TrainMl2DWdcnnFromExisting: A total of %d valid training samples'
             2992  LOAD_GLOBAL              basic_mdt
             2994  LOAD_METHOD              maxDictConstantRow

 L. 910      2996  LOAD_FAST                '_traindict'
             2998  CALL_METHOD_1         1  '1 positional argument'
             3000  BINARY_MODULO    
             3002  CALL_FUNCTION_1       1  '1 positional argument'
             3004  POP_TOP          

 L. 912      3006  LOAD_GLOBAL              print
             3008  LOAD_STR                 'TrainMl2DWdcnnFromExisting: Step 3 - Start training'
             3010  CALL_FUNCTION_1       1  '1 positional argument'
             3012  POP_TOP          

 L. 914      3014  LOAD_GLOBAL              QtWidgets
             3016  LOAD_METHOD              QProgressDialog
             3018  CALL_METHOD_0         0  '0 positional arguments'
             3020  STORE_FAST               '_pgsdlg'

 L. 915      3022  LOAD_GLOBAL              QtGui
             3024  LOAD_METHOD              QIcon
             3026  CALL_METHOD_0         0  '0 positional arguments'
             3028  STORE_FAST               'icon'

 L. 916      3030  LOAD_FAST                'icon'
             3032  LOAD_METHOD              addPixmap
             3034  LOAD_GLOBAL              QtGui
             3036  LOAD_METHOD              QPixmap
             3038  LOAD_GLOBAL              os
             3040  LOAD_ATTR                path
             3042  LOAD_METHOD              join
             3044  LOAD_DEREF               'self'
             3046  LOAD_ATTR                iconpath
             3048  LOAD_STR                 'icons/new.png'
             3050  CALL_METHOD_2         2  '2 positional arguments'
             3052  CALL_METHOD_1         1  '1 positional argument'

 L. 917      3054  LOAD_GLOBAL              QtGui
             3056  LOAD_ATTR                QIcon
             3058  LOAD_ATTR                Normal
             3060  LOAD_GLOBAL              QtGui
             3062  LOAD_ATTR                QIcon
             3064  LOAD_ATTR                Off
             3066  CALL_METHOD_3         3  '3 positional arguments'
             3068  POP_TOP          

 L. 918      3070  LOAD_FAST                '_pgsdlg'
             3072  LOAD_METHOD              setWindowIcon
             3074  LOAD_FAST                'icon'
             3076  CALL_METHOD_1         1  '1 positional argument'
             3078  POP_TOP          

 L. 919      3080  LOAD_FAST                '_pgsdlg'
             3082  LOAD_METHOD              setWindowTitle
             3084  LOAD_STR                 'Train 2D-WDCNN'
             3086  CALL_METHOD_1         1  '1 positional argument'
             3088  POP_TOP          

 L. 920      3090  LOAD_FAST                '_pgsdlg'
             3092  LOAD_METHOD              setCancelButton
             3094  LOAD_CONST               None
             3096  CALL_METHOD_1         1  '1 positional argument'
             3098  POP_TOP          

 L. 921      3100  LOAD_FAST                '_pgsdlg'
             3102  LOAD_METHOD              setWindowFlags
             3104  LOAD_GLOBAL              QtCore
             3106  LOAD_ATTR                Qt
             3108  LOAD_ATTR                WindowStaysOnTopHint
             3110  CALL_METHOD_1         1  '1 positional argument'
             3112  POP_TOP          

 L. 922      3114  LOAD_FAST                '_pgsdlg'
             3116  LOAD_METHOD              forceShow
             3118  CALL_METHOD_0         0  '0 positional arguments'
             3120  POP_TOP          

 L. 923      3122  LOAD_FAST                '_pgsdlg'
             3124  LOAD_METHOD              setFixedWidth
             3126  LOAD_CONST               400
             3128  CALL_METHOD_1         1  '1 positional argument'
             3130  POP_TOP          

 L. 924      3132  LOAD_GLOBAL              ml_wdcnn
             3134  LOAD_ATTR                createWDCNNSegmentorFromExisting
             3136  LOAD_FAST                '_traindict'

 L. 925      3138  LOAD_FAST                '_image_height_new'
             3140  LOAD_FAST                '_image_width_new'

 L. 926      3142  LOAD_FAST                '_features'
             3144  LOAD_FAST                '_target'
             3146  LOAD_FAST                '_weight'

 L. 927      3148  LOAD_FAST                '_nepoch'
             3150  LOAD_FAST                '_batchsize'

 L. 928      3152  LOAD_FAST                '_nconvblock'
             3154  LOAD_FAST                '_nconvfeature'

 L. 929      3156  LOAD_FAST                '_nconvlayer'

 L. 930      3158  LOAD_FAST                '_n1x1layer'
             3160  LOAD_FAST                '_n1x1feature'

 L. 931      3162  LOAD_FAST                '_pool_height'
             3164  LOAD_FAST                '_pool_width'

 L. 932      3166  LOAD_FAST                '_learning_rate'

 L. 933      3168  LOAD_FAST                '_dropout_prob'

 L. 934      3170  LOAD_CONST               True

 L. 935      3172  LOAD_FAST                '_savepath'
             3174  LOAD_FAST                '_savename'

 L. 936      3176  LOAD_FAST                '_pgsdlg'

 L. 937      3178  LOAD_FAST                '_precnnpath'

 L. 938      3180  LOAD_FAST                '_precnnname'

 L. 939      3182  LOAD_FAST                '_blockidx'
             3184  LOAD_FAST                '_layeridx'

 L. 940      3186  LOAD_FAST                '_trainable'
             3188  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'weight', 'nepoch', 'batchsize', 'nconvblock', 'nconvfeature', 'nconvlayer', 'n1x1layer', 'n1x1feature', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprob', 'save2disk', 'savepath', 'savename', 'qpgsdlg', 'precnnpath', 'precnnname', 'blockidx', 'layeridx', 'trainable')
             3190  CALL_FUNCTION_KW_26    26  '26 total positional and keyword args'
             3192  STORE_FAST               '_dcnnlog'

 L. 943      3194  LOAD_GLOBAL              QtWidgets
             3196  LOAD_ATTR                QMessageBox
             3198  LOAD_METHOD              information
             3200  LOAD_DEREF               'self'
             3202  LOAD_ATTR                msgbox

 L. 944      3204  LOAD_STR                 'Train 2D-WDCNN'

 L. 945      3206  LOAD_STR                 'WDCNN trained successfully'
             3208  CALL_METHOD_3         3  '3 positional arguments'
             3210  POP_TOP          

 L. 947      3212  LOAD_GLOBAL              QtWidgets
             3214  LOAD_ATTR                QMessageBox
             3216  LOAD_METHOD              question
             3218  LOAD_DEREF               'self'
             3220  LOAD_ATTR                msgbox
             3222  LOAD_STR                 'Train 2D-WDCNN'
             3224  LOAD_STR                 'View learning matrix?'

 L. 948      3226  LOAD_GLOBAL              QtWidgets
             3228  LOAD_ATTR                QMessageBox
             3230  LOAD_ATTR                Yes
             3232  LOAD_GLOBAL              QtWidgets
             3234  LOAD_ATTR                QMessageBox
             3236  LOAD_ATTR                No
             3238  BINARY_OR        

 L. 949      3240  LOAD_GLOBAL              QtWidgets
             3242  LOAD_ATTR                QMessageBox
             3244  LOAD_ATTR                Yes
             3246  CALL_METHOD_5         5  '5 positional arguments'
             3248  STORE_FAST               'reply'

 L. 951      3250  LOAD_FAST                'reply'
             3252  LOAD_GLOBAL              QtWidgets
             3254  LOAD_ATTR                QMessageBox
             3256  LOAD_ATTR                Yes
             3258  COMPARE_OP               ==
         3260_3262  POP_JUMP_IF_FALSE  3330  'to 3330'

 L. 952      3264  LOAD_GLOBAL              QtWidgets
             3266  LOAD_METHOD              QDialog
             3268  CALL_METHOD_0         0  '0 positional arguments'
             3270  STORE_FAST               '_viewmllearnmat'

 L. 953      3272  LOAD_GLOBAL              gui_viewmllearnmat
             3274  CALL_FUNCTION_0       0  '0 positional arguments'
             3276  STORE_FAST               '_gui'

 L. 954      3278  LOAD_FAST                '_dcnnlog'
             3280  LOAD_STR                 'learning_curve'
             3282  BINARY_SUBSCR    
             3284  LOAD_FAST                '_gui'
             3286  STORE_ATTR               learnmat

 L. 955      3288  LOAD_DEREF               'self'
             3290  LOAD_ATTR                linestyle
             3292  LOAD_FAST                '_gui'
             3294  STORE_ATTR               linestyle

 L. 956      3296  LOAD_DEREF               'self'
             3298  LOAD_ATTR                fontstyle
             3300  LOAD_FAST                '_gui'
             3302  STORE_ATTR               fontstyle

 L. 957      3304  LOAD_FAST                '_gui'
             3306  LOAD_METHOD              setupGUI
             3308  LOAD_FAST                '_viewmllearnmat'
             3310  CALL_METHOD_1         1  '1 positional argument'
             3312  POP_TOP          

 L. 958      3314  LOAD_FAST                '_viewmllearnmat'
             3316  LOAD_METHOD              exec
             3318  CALL_METHOD_0         0  '0 positional arguments'
             3320  POP_TOP          

 L. 959      3322  LOAD_FAST                '_viewmllearnmat'
             3324  LOAD_METHOD              show
             3326  CALL_METHOD_0         0  '0 positional arguments'
             3328  POP_TOP          
           3330_0  COME_FROM          3260  '3260'

Parse error at or near `POP_TOP' instruction at offset 3328

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
    TrainMl2DWdcnnFromExisting = QtWidgets.QWidget()
    gui = trainml2dwdcnnfromexisting()
    gui.setupGUI(TrainMl2DWdcnnFromExisting)
    TrainMl2DWdcnnFromExisting.show()
    sys.exit(app.exec_())