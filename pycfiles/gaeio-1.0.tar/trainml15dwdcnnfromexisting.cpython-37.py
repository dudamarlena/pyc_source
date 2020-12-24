# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml15dwdcnnfromexisting.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 57914 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.pointset.analysis as point_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.curve as basic_curve
import cognitivegeo.src.basic.image as basic_image
import cognitivegeo.src.ml.augmentation as ml_aug
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.wdcnnsegmentor15d as ml_wdcnn15d
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml15dwdcnnfromexisting(object):
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
    traindataconfig['RemoveZeroWeight_Enabled'] = True
    traindataconfig['RemoveZeroWeight_Checked'] = False

    def setupGUI(self, TrainMl15DWdcnnFromExisting):
        TrainMl15DWdcnnFromExisting.setObjectName('TrainMl15DWdcnnFromExisting')
        TrainMl15DWdcnnFromExisting.setFixedSize(800, 630)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl15DWdcnnFromExisting.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl15DWdcnnFromExisting)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl15DWdcnnFromExisting)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lbltarget.setObjectName('lbltargete')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl15DWdcnnFromExisting)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblweight = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblweight.setObjectName('lblweight')
        self.lblweight.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.cbbweight = QtWidgets.QComboBox(TrainMl15DWdcnnFromExisting)
        self.cbbweight.setObjectName('cbbweight')
        self.cbbweight.setGeometry(QtCore.QRect(110, 310, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblexisting = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblexisting.setObjectName('lblexisting')
        self.lblexisting.setGeometry(QtCore.QRect(410, 50, 100, 30))
        self.ldtexisting = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtexisting.setObjectName('ldtexisting')
        self.ldtexisting.setGeometry(QtCore.QRect(510, 50, 210, 30))
        self.btnexisting = QtWidgets.QPushButton(TrainMl15DWdcnnFromExisting)
        self.btnexisting.setObjectName('btnexisting')
        self.btnexisting.setGeometry(QtCore.QRect(730, 50, 60, 30))
        self.lblnconvblockexisting = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblnconvblockexisting.setObjectName('lblnconvblockexisting')
        self.lblnconvblockexisting.setGeometry(QtCore.QRect(410, 90, 130, 30))
        self.ldtnconvblockexisting = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtnconvblockexisting.setObjectName('ldtnconvblockexisting')
        self.ldtnconvblockexisting.setGeometry(QtCore.QRect(550, 90, 40, 30))
        self.twgnconvblockexisting = QtWidgets.QTableWidget(TrainMl15DWdcnnFromExisting)
        self.twgnconvblockexisting.setObjectName('twgnconvblockexisting')
        self.twgnconvblockexisting.setGeometry(QtCore.QRect(610, 90, 180, 150))
        self.twgnconvblockexisting.setColumnCount(3)
        self.twgnconvblockexisting.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblockexisting.verticalHeader().hide()
        self.lblblockid = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblblockid.setObjectName('lblblockid')
        self.lblblockid.setGeometry(QtCore.QRect(410, 130, 130, 30))
        self.cbbblockid = QtWidgets.QComboBox(TrainMl15DWdcnnFromExisting)
        self.cbbblockid.setObjectName('cbbblockid')
        self.cbbblockid.setGeometry(QtCore.QRect(550, 130, 40, 30))
        self.lbllayerid = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lbllayerid.setObjectName('lbllayerid')
        self.lbllayerid.setGeometry(QtCore.QRect(410, 170, 130, 30))
        self.cbblayerid = QtWidgets.QComboBox(TrainMl15DWdcnnFromExisting)
        self.cbblayerid.setObjectName('cbblayerid')
        self.cbblayerid.setGeometry(QtCore.QRect(550, 170, 40, 30))
        self.lbltrainable = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lbltrainable.setObjectName('lbltrainable')
        self.lbltrainable.setGeometry(QtCore.QRect(410, 210, 130, 30))
        self.cbbtrainable = QtWidgets.QComboBox(TrainMl15DWdcnnFromExisting)
        self.cbbtrainable.setObjectName('cbbtrainable')
        self.cbbtrainable.setGeometry(QtCore.QRect(550, 210, 40, 30))
        self.lblappend = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblappend.setObjectName('lblappend')
        self.lblappend.setGeometry(QtCore.QRect(410, 250, 200, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 290, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 290, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl15DWdcnnFromExisting)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 330, 180, 200))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 290, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 290, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(TrainMl15DWdcnnFromExisting)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 330, 180, 200))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 540, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 540, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 540, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 580, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 580, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 540, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 540, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 540, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 580, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 580, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl15DWdcnnFromExisting)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 360, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 360, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 400, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 400, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 400, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 400, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 440, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 440, 40, 30))
        self.lbldropout = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 440, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 440, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl15DWdcnnFromExisting)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 490, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl15DWdcnnFromExisting)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 490, 180, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl15DWdcnnFromExisting)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 490, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl15DWdcnnFromExisting)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(120, 580, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl15DWdcnnFromExisting)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl15DWdcnnFromExisting.geometry().center().x()
        _center_y = TrainMl15DWdcnnFromExisting.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl15DWdcnnFromExisting)
        QtCore.QMetaObject.connectSlotsByName(TrainMl15DWdcnnFromExisting)

    def retranslateGUI(self, TrainMl15DWdcnnFromExisting):
        self.dialog = TrainMl15DWdcnnFromExisting
        _translate = QtCore.QCoreApplication.translate
        TrainMl15DWdcnnFromExisting.setWindowTitle(_translate('TrainMl15DWdcnnFromExisting', 'Train 1.5D-WDCNN from pre-trained'))
        self.lblfeature.setText(_translate('TrainMl15DWdcnnFromExisting', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl15DWdcnnFromExisting', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl15DWdcnnFromExisting', 'Select target:'))
        self.lblweight.setText(_translate('TrainMl15DWdcnnFromExisting', 'Select weight:'))
        self.btnconfigtraindata.setText(_translate('TrainMl2DDcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('TrainMl15DWdcnnFromExisting', 'Original\nimage\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl15DWdcnnFromExisting', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl15DWdcnnFromExisting', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl15DWdcnnFromExisting', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl15DWdcnnFromExisting', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl15DWdcnnFromExisting', 'Interpolated\nimage\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl15DWdcnnFromExisting', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl15DWdcnnFromExisting', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl15DWdcnnFromExisting', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl15DWdcnnFromExisting', '32'))
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
                    item.setText(_translate('TrainMl15DWdcnnFromExisting', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
            self.cbbweight.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl15DWdcnnFromExisting', 'Specify WDCNN architecture:'))
        self.lblexisting.setText(_translate('TrainMl15DWdcnnFromExisting', 'Select pre-trained:'))
        self.ldtexisting.setText(_translate('TrainMl15DWdcnnFromExisting', ''))
        self.ldtexisting.textChanged.connect(self.changeLdtExisting)
        self.btnexisting.setText(_translate('TrainMl15DWdcnnFromExisting', 'Browse'))
        self.btnexisting.clicked.connect(self.clickBtnExisting)
        self.lblnconvblockexisting.setText(_translate('TrainMl15DWdcnnFromExisting', 'Available conv. blocks:'))
        self.lblnconvblockexisting.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblockexisting.setText(_translate('TrainMl15DWdcnnFromExisting', ''))
        self.ldtnconvblockexisting.setEnabled(False)
        self.ldtnconvblockexisting.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblockexisting.textChanged.connect(self.changeLdtNconvblockExisting)
        self.twgnconvblockexisting.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblblockid.setText(_translate('TrainMl15DWdcnnFromExisting', 'Select conv. block ID:'))
        self.lblblockid.setAlignment(QtCore.Qt.AlignRight)
        self.cbbblockid.currentIndexChanged.connect(self.changeCbbBlockid)
        self.lbllayerid.setText(_translate('TrainMl15DWdcnnFromExisting', 'Select conv. layer ID:'))
        self.lbllayerid.setAlignment(QtCore.Qt.AlignRight)
        self.lbltrainable.setText(_translate('TrainMl15DWdcnnFromExisting', 'Is trainable?:'))
        self.lbltrainable.setAlignment(QtCore.Qt.AlignRight)
        self.cbbtrainable.addItems(['Yes', 'No'])
        self.lblappend.setText(_translate('TrainMl15DWdcnnFromExisting', 'Append more blocks & layers:'))
        self.lblnconvblock.setText(_translate('TrainMl15DWdcnnFromExisting', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl15DWdcnnFromExisting', '2'))
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

        self.lbln1x1layer.setText(_translate('TrainMl15DWdcnnFromExisting', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('TrainMl15DWdcnnFromExisting', '2'))
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.twgn1x1layer.setRowCount(2)
        for _idx in range(int(self.ldtn1x1layer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl15DWdcnnFromExisting', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgn1x1layer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgn1x1layer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl15DWdcnnFromExisting', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl15DWdcnnFromExisting', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl15DWdcnnFromExisting', ''))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskheight.setEnabled(False)
        self.lblmaskwidth.setText(_translate('TrainMl15DWdcnnFromExisting', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl15DWdcnnFromExisting', ''))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskwidth.setEnabled(False)
        self.lblpoolsize.setText(_translate('TrainMl15DWdcnnFromExisting', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl15DWdcnnFromExisting', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl15DWdcnnFromExisting', ''))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl15DWdcnnFromExisting', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl15DWdcnnFromExisting', ''))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('TrainMl15DWdcnnFromExisting', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl15DWdcnnFromExisting', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl15DWdcnnFromExisting', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl15DWdcnnFromExisting', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl15DWdcnnFromExisting', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl15DWdcnnFromExisting', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl15DWdcnnFromExisting', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('TrainMl15DWdcnnFromExisting', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('TrainMl15DWdcnnFromExisting', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl15DWdcnnFromExisting', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl15DWdcnnFromExisting', ''))
        self.btnsave.setText(_translate('TrainMl15DWdcnnFromExisting', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl15DWdcnnFromExisting', 'Train 1.5D-WDCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl15DWdcnnFromExisting)

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

    def clickBtnTrainMl15DWdcnnFromExisting--- This code section failed: ---

 L. 609         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 611         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 612        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 613        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 614        50  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 615        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 616        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 618        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_image_height'

 L. 619        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_image_width'

 L. 620        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtnewheight
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_image_height_new'

 L. 621       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewwidth
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_image_width_new'

 L. 622       126  LOAD_FAST                '_image_height'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'
              134  LOAD_FAST                '_image_width'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_TRUE    158  'to 158'

 L. 623       142  LOAD_FAST                '_image_height_new'
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

 L. 624       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 625       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 626       182  LOAD_STR                 'Train 1.5D-DCNN'

 L. 627       184  LOAD_STR                 'Non-integer feature size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 628       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 629       194  LOAD_FAST                '_image_height'
              196  LOAD_CONST               2
              198  COMPARE_OP               <
              200  POP_JUMP_IF_TRUE    228  'to 228'
              202  LOAD_FAST                '_image_width'
              204  LOAD_CONST               2
              206  COMPARE_OP               <
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 630       210  LOAD_FAST                '_image_height_new'
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

 L. 631       228  LOAD_GLOBAL              vis_msg
              230  LOAD_ATTR                print
              232  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 632       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 633       252  LOAD_STR                 'Train 1.5D-DCNN'

 L. 634       254  LOAD_STR                 'Features are not 2D'
              256  CALL_METHOD_3         3  '3 positional arguments'
              258  POP_TOP          

 L. 635       260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           224  '224'

 L. 637       264  LOAD_CONST               2
              266  LOAD_GLOBAL              int
              268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               2
              272  BINARY_TRUE_DIVIDE
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  BINARY_MULTIPLY  
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  STORE_FAST               '_image_height'

 L. 638       284  LOAD_CONST               2
              286  LOAD_GLOBAL              int
              288  LOAD_FAST                '_image_width'
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BINARY_MULTIPLY  
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               '_image_width'

 L. 640       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                lwgfeature
              308  LOAD_METHOD              selectedItems
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               '_features'

 L. 641       314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainml15dwdcnnfromexisting.clickBtnTrainMl15DWdcnnFromExisting.<locals>.<listcomp>'
              318  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              320  LOAD_FAST                '_features'
              322  GET_ITER         
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               '_features'

 L. 642       328  LOAD_DEREF               'self'
              330  LOAD_ATTR                featurelist
              332  LOAD_DEREF               'self'
              334  LOAD_ATTR                cbbtarget
              336  LOAD_METHOD              currentIndex
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  BINARY_SUBSCR    
              342  STORE_FAST               '_target'

 L. 643       344  LOAD_DEREF               'self'
              346  LOAD_ATTR                featurelist
              348  LOAD_DEREF               'self'
              350  LOAD_ATTR                cbbweight
              352  LOAD_METHOD              currentIndex
              354  CALL_METHOD_0         0  '0 positional arguments'
              356  BINARY_SUBSCR    
              358  STORE_FAST               '_weight'

 L. 645       360  LOAD_FAST                '_target'
              362  LOAD_FAST                '_features'
              364  COMPARE_OP               in
          366_368  POP_JUMP_IF_FALSE   406  'to 406'

 L. 646       370  LOAD_GLOBAL              vis_msg
              372  LOAD_ATTR                print
              374  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Target also used as features'
              376  LOAD_STR                 'error'
              378  LOAD_CONST               ('type',)
              380  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              382  POP_TOP          

 L. 647       384  LOAD_GLOBAL              QtWidgets
              386  LOAD_ATTR                QMessageBox
              388  LOAD_METHOD              critical
              390  LOAD_DEREF               'self'
              392  LOAD_ATTR                msgbox

 L. 648       394  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 649       396  LOAD_STR                 'Target also used as features'
              398  CALL_METHOD_3         3  '3 positional arguments'
              400  POP_TOP          

 L. 650       402  LOAD_CONST               None
              404  RETURN_VALUE     
            406_0  COME_FROM           366  '366'

 L. 651       406  LOAD_FAST                '_weight'
              408  LOAD_FAST                '_features'
              410  COMPARE_OP               in
          412_414  POP_JUMP_IF_FALSE   452  'to 452'

 L. 652       416  LOAD_GLOBAL              vis_msg
              418  LOAD_ATTR                print
              420  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Weight also used as features'
              422  LOAD_STR                 'error'
              424  LOAD_CONST               ('type',)
              426  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              428  POP_TOP          

 L. 653       430  LOAD_GLOBAL              QtWidgets
              432  LOAD_ATTR                QMessageBox
              434  LOAD_METHOD              critical
              436  LOAD_DEREF               'self'
              438  LOAD_ATTR                msgbox

 L. 654       440  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 655       442  LOAD_STR                 'Weight also used as features'
              444  CALL_METHOD_3         3  '3 positional arguments'
              446  POP_TOP          

 L. 656       448  LOAD_CONST               None
              450  RETURN_VALUE     
            452_0  COME_FROM           412  '412'

 L. 658       452  LOAD_GLOBAL              len
              454  LOAD_DEREF               'self'
              456  LOAD_ATTR                ldtexisting
              458  LOAD_METHOD              text
              460  CALL_METHOD_0         0  '0 positional arguments'
              462  CALL_FUNCTION_1       1  '1 positional argument'
              464  LOAD_CONST               1
              466  COMPARE_OP               <
          468_470  POP_JUMP_IF_FALSE   508  'to 508'

 L. 659       472  LOAD_GLOBAL              vis_msg
              474  LOAD_ATTR                print
              476  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: No name specified for pre-trained network'

 L. 660       478  LOAD_STR                 'error'
              480  LOAD_CONST               ('type',)
              482  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              484  POP_TOP          

 L. 661       486  LOAD_GLOBAL              QtWidgets
              488  LOAD_ATTR                QMessageBox
              490  LOAD_METHOD              critical
              492  LOAD_DEREF               'self'
              494  LOAD_ATTR                msgbox

 L. 662       496  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 663       498  LOAD_STR                 'No name specified for pre-trained network'
              500  CALL_METHOD_3         3  '3 positional arguments'
              502  POP_TOP          

 L. 664       504  LOAD_CONST               None
              506  RETURN_VALUE     
            508_0  COME_FROM           468  '468'

 L. 665       508  LOAD_GLOBAL              os
              510  LOAD_ATTR                path
              512  LOAD_METHOD              dirname
              514  LOAD_DEREF               'self'
              516  LOAD_ATTR                ldtexisting
              518  LOAD_METHOD              text
              520  CALL_METHOD_0         0  '0 positional arguments'
              522  CALL_METHOD_1         1  '1 positional argument'
              524  STORE_FAST               '_precnnpath'

 L. 666       526  LOAD_GLOBAL              os
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

 L. 667       556  LOAD_DEREF               'self'
              558  LOAD_ATTR                cbbblockid
              560  LOAD_METHOD              currentIndex
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  STORE_FAST               '_blockidx'

 L. 668       566  LOAD_DEREF               'self'
              568  LOAD_ATTR                cbblayerid
              570  LOAD_METHOD              currentIndex
              572  CALL_METHOD_0         0  '0 positional arguments'
              574  STORE_FAST               '_layeridx'

 L. 669       576  LOAD_CONST               True
              578  STORE_FAST               '_trainable'

 L. 670       580  LOAD_DEREF               'self'
              582  LOAD_ATTR                cbbtrainable
              584  LOAD_METHOD              currentIndex
              586  CALL_METHOD_0         0  '0 positional arguments'
              588  LOAD_CONST               0
              590  COMPARE_OP               !=
          592_594  POP_JUMP_IF_FALSE   600  'to 600'

 L. 671       596  LOAD_CONST               False
              598  STORE_FAST               '_trainable'
            600_0  COME_FROM           592  '592'

 L. 673       600  LOAD_GLOBAL              ml_tfm
              602  LOAD_METHOD              getConvModelNChannel
              604  LOAD_FAST                '_precnnpath'
              606  LOAD_FAST                '_precnnname'
              608  CALL_METHOD_2         2  '2 positional arguments'
              610  LOAD_GLOBAL              len
              612  LOAD_FAST                '_features'
              614  CALL_FUNCTION_1       1  '1 positional argument'
              616  COMPARE_OP               !=
          618_620  POP_JUMP_IF_FALSE   658  'to 658'

 L. 674       622  LOAD_GLOBAL              vis_msg
              624  LOAD_ATTR                print
              626  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Feature channel number not match with pre-trained network'

 L. 675       628  LOAD_STR                 'error'
              630  LOAD_CONST               ('type',)
              632  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              634  POP_TOP          

 L. 676       636  LOAD_GLOBAL              QtWidgets
              638  LOAD_ATTR                QMessageBox
              640  LOAD_METHOD              critical
              642  LOAD_DEREF               'self'
              644  LOAD_ATTR                msgbox

 L. 677       646  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 678       648  LOAD_STR                 'Feature channel number not match with pre-trained network'
              650  CALL_METHOD_3         3  '3 positional arguments'
              652  POP_TOP          

 L. 679       654  LOAD_CONST               None
              656  RETURN_VALUE     
            658_0  COME_FROM           618  '618'

 L. 681       658  LOAD_GLOBAL              basic_data
              660  LOAD_METHOD              str2int
              662  LOAD_DEREF               'self'
              664  LOAD_ATTR                ldtnconvblock
              666  LOAD_METHOD              text
              668  CALL_METHOD_0         0  '0 positional arguments'
              670  CALL_METHOD_1         1  '1 positional argument'
              672  STORE_FAST               '_nconvblock'

 L. 682       674  LOAD_CLOSURE             'self'
              676  BUILD_TUPLE_1         1 
              678  LOAD_LISTCOMP            '<code_object <listcomp>>'
              680  LOAD_STR                 'trainml15dwdcnnfromexisting.clickBtnTrainMl15DWdcnnFromExisting.<locals>.<listcomp>'
              682  MAKE_FUNCTION_8          'closure'
              684  LOAD_GLOBAL              range
              686  LOAD_FAST                '_nconvblock'
              688  CALL_FUNCTION_1       1  '1 positional argument'
              690  GET_ITER         
              692  CALL_FUNCTION_1       1  '1 positional argument'
              694  STORE_FAST               '_nconvlayer'

 L. 683       696  LOAD_CLOSURE             'self'
              698  BUILD_TUPLE_1         1 
              700  LOAD_LISTCOMP            '<code_object <listcomp>>'
              702  LOAD_STR                 'trainml15dwdcnnfromexisting.clickBtnTrainMl15DWdcnnFromExisting.<locals>.<listcomp>'
              704  MAKE_FUNCTION_8          'closure'
              706  LOAD_GLOBAL              range
              708  LOAD_FAST                '_nconvblock'
              710  CALL_FUNCTION_1       1  '1 positional argument'
              712  GET_ITER         
              714  CALL_FUNCTION_1       1  '1 positional argument'
              716  STORE_FAST               '_nconvfeature'

 L. 684       718  LOAD_GLOBAL              basic_data
              720  LOAD_METHOD              str2int
              722  LOAD_DEREF               'self'
              724  LOAD_ATTR                ldtn1x1layer
              726  LOAD_METHOD              text
              728  CALL_METHOD_0         0  '0 positional arguments'
              730  CALL_METHOD_1         1  '1 positional argument'
              732  STORE_FAST               '_n1x1layer'

 L. 685       734  LOAD_CLOSURE             'self'
              736  BUILD_TUPLE_1         1 
              738  LOAD_LISTCOMP            '<code_object <listcomp>>'
              740  LOAD_STR                 'trainml15dwdcnnfromexisting.clickBtnTrainMl15DWdcnnFromExisting.<locals>.<listcomp>'
              742  MAKE_FUNCTION_8          'closure'
              744  LOAD_GLOBAL              range
              746  LOAD_FAST                '_n1x1layer'
              748  CALL_FUNCTION_1       1  '1 positional argument'
              750  GET_ITER         
              752  CALL_FUNCTION_1       1  '1 positional argument'
              754  STORE_FAST               '_n1x1feature'

 L. 686       756  LOAD_GLOBAL              basic_data
              758  LOAD_METHOD              str2int
              760  LOAD_DEREF               'self'
              762  LOAD_ATTR                ldtmaskheight
              764  LOAD_METHOD              text
              766  CALL_METHOD_0         0  '0 positional arguments'
              768  CALL_METHOD_1         1  '1 positional argument'
              770  STORE_FAST               '_patch_height'

 L. 687       772  LOAD_GLOBAL              basic_data
              774  LOAD_METHOD              str2int
              776  LOAD_DEREF               'self'
              778  LOAD_ATTR                ldtmaskwidth
              780  LOAD_METHOD              text
              782  CALL_METHOD_0         0  '0 positional arguments'
              784  CALL_METHOD_1         1  '1 positional argument'
              786  STORE_FAST               '_patch_width'

 L. 688       788  LOAD_GLOBAL              basic_data
              790  LOAD_METHOD              str2int
              792  LOAD_DEREF               'self'
              794  LOAD_ATTR                ldtpoolheight
              796  LOAD_METHOD              text
              798  CALL_METHOD_0         0  '0 positional arguments'
              800  CALL_METHOD_1         1  '1 positional argument'
              802  STORE_FAST               '_pool_height'

 L. 689       804  LOAD_GLOBAL              basic_data
              806  LOAD_METHOD              str2int
              808  LOAD_DEREF               'self'
              810  LOAD_ATTR                ldtpoolwidth
              812  LOAD_METHOD              text
              814  CALL_METHOD_0         0  '0 positional arguments'
              816  CALL_METHOD_1         1  '1 positional argument'
              818  STORE_FAST               '_pool_width'

 L. 690       820  LOAD_GLOBAL              basic_data
              822  LOAD_METHOD              str2int
              824  LOAD_DEREF               'self'
              826  LOAD_ATTR                ldtnepoch
              828  LOAD_METHOD              text
              830  CALL_METHOD_0         0  '0 positional arguments'
              832  CALL_METHOD_1         1  '1 positional argument'
              834  STORE_FAST               '_nepoch'

 L. 691       836  LOAD_GLOBAL              basic_data
              838  LOAD_METHOD              str2int
              840  LOAD_DEREF               'self'
              842  LOAD_ATTR                ldtbatchsize
              844  LOAD_METHOD              text
              846  CALL_METHOD_0         0  '0 positional arguments'
              848  CALL_METHOD_1         1  '1 positional argument'
              850  STORE_FAST               '_batchsize'

 L. 692       852  LOAD_GLOBAL              basic_data
              854  LOAD_METHOD              str2float
              856  LOAD_DEREF               'self'
              858  LOAD_ATTR                ldtlearnrate
              860  LOAD_METHOD              text
              862  CALL_METHOD_0         0  '0 positional arguments'
              864  CALL_METHOD_1         1  '1 positional argument'
              866  STORE_FAST               '_learning_rate'

 L. 693       868  LOAD_GLOBAL              basic_data
              870  LOAD_METHOD              str2float
              872  LOAD_DEREF               'self'
              874  LOAD_ATTR                ldtdropout
              876  LOAD_METHOD              text
              878  CALL_METHOD_0         0  '0 positional arguments'
              880  CALL_METHOD_1         1  '1 positional argument'
              882  STORE_FAST               '_dropout_prob'

 L. 694       884  LOAD_FAST                '_nconvblock'
              886  LOAD_CONST               False
              888  COMPARE_OP               is
          890_892  POP_JUMP_IF_TRUE    904  'to 904'
              894  LOAD_FAST                '_nconvblock'
              896  LOAD_CONST               0
              898  COMPARE_OP               <=
          900_902  POP_JUMP_IF_FALSE   940  'to 940'
            904_0  COME_FROM           890  '890'

 L. 695       904  LOAD_GLOBAL              vis_msg
              906  LOAD_ATTR                print
              908  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Non-positive convolutional block number'

 L. 696       910  LOAD_STR                 'error'
              912  LOAD_CONST               ('type',)
              914  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              916  POP_TOP          

 L. 697       918  LOAD_GLOBAL              QtWidgets
              920  LOAD_ATTR                QMessageBox
              922  LOAD_METHOD              critical
              924  LOAD_DEREF               'self'
              926  LOAD_ATTR                msgbox

 L. 698       928  LOAD_STR                 'Train 1.5D-DCNN'

 L. 699       930  LOAD_STR                 'Non-positive convolutional block number'
              932  CALL_METHOD_3         3  '3 positional arguments'
              934  POP_TOP          

 L. 700       936  LOAD_CONST               None
              938  RETURN_VALUE     
            940_0  COME_FROM           900  '900'

 L. 701       940  SETUP_LOOP         1012  'to 1012'
              942  LOAD_FAST                '_nconvlayer'
              944  GET_ITER         
            946_0  COME_FROM           966  '966'
              946  FOR_ITER           1010  'to 1010'
              948  STORE_FAST               '_i'

 L. 702       950  LOAD_FAST                '_i'
              952  LOAD_CONST               False
              954  COMPARE_OP               is
          956_958  POP_JUMP_IF_TRUE    970  'to 970'
              960  LOAD_FAST                '_i'
              962  LOAD_CONST               1
              964  COMPARE_OP               <
          966_968  POP_JUMP_IF_FALSE   946  'to 946'
            970_0  COME_FROM           956  '956'

 L. 703       970  LOAD_GLOBAL              vis_msg
              972  LOAD_ATTR                print
              974  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Non-positive convolutional layer number'

 L. 704       976  LOAD_STR                 'error'
              978  LOAD_CONST               ('type',)
              980  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              982  POP_TOP          

 L. 705       984  LOAD_GLOBAL              QtWidgets
              986  LOAD_ATTR                QMessageBox
              988  LOAD_METHOD              critical
              990  LOAD_DEREF               'self'
              992  LOAD_ATTR                msgbox

 L. 706       994  LOAD_STR                 'Train 1.5D-DCNN'

 L. 707       996  LOAD_STR                 'Non-positive convolutional layer number'
              998  CALL_METHOD_3         3  '3 positional arguments'
             1000  POP_TOP          

 L. 708      1002  LOAD_CONST               None
             1004  RETURN_VALUE     
         1006_1008  JUMP_BACK           946  'to 946'
             1010  POP_BLOCK        
           1012_0  COME_FROM_LOOP      940  '940'

 L. 709      1012  SETUP_LOOP         1084  'to 1084'
             1014  LOAD_FAST                '_nconvfeature'
             1016  GET_ITER         
           1018_0  COME_FROM          1038  '1038'
             1018  FOR_ITER           1082  'to 1082'
             1020  STORE_FAST               '_i'

 L. 710      1022  LOAD_FAST                '_i'
             1024  LOAD_CONST               False
             1026  COMPARE_OP               is
         1028_1030  POP_JUMP_IF_TRUE   1042  'to 1042'
             1032  LOAD_FAST                '_i'
             1034  LOAD_CONST               1
             1036  COMPARE_OP               <
         1038_1040  POP_JUMP_IF_FALSE  1018  'to 1018'
           1042_0  COME_FROM          1028  '1028'

 L. 711      1042  LOAD_GLOBAL              vis_msg
             1044  LOAD_ATTR                print
             1046  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Non-positive convolutional feature number'

 L. 712      1048  LOAD_STR                 'error'
             1050  LOAD_CONST               ('type',)
             1052  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1054  POP_TOP          

 L. 713      1056  LOAD_GLOBAL              QtWidgets
             1058  LOAD_ATTR                QMessageBox
             1060  LOAD_METHOD              critical
             1062  LOAD_DEREF               'self'
             1064  LOAD_ATTR                msgbox

 L. 714      1066  LOAD_STR                 'Train 1.5D-DCNN'

 L. 715      1068  LOAD_STR                 'Non-positive convolutional feature number'
             1070  CALL_METHOD_3         3  '3 positional arguments'
             1072  POP_TOP          

 L. 716      1074  LOAD_CONST               None
             1076  RETURN_VALUE     
         1078_1080  JUMP_BACK          1018  'to 1018'
             1082  POP_BLOCK        
           1084_0  COME_FROM_LOOP     1012  '1012'

 L. 717      1084  LOAD_FAST                '_n1x1layer'
             1086  LOAD_CONST               False
             1088  COMPARE_OP               is
         1090_1092  POP_JUMP_IF_TRUE   1104  'to 1104'
             1094  LOAD_FAST                '_n1x1layer'
             1096  LOAD_CONST               0
             1098  COMPARE_OP               <=
         1100_1102  POP_JUMP_IF_FALSE  1140  'to 1140'
           1104_0  COME_FROM          1090  '1090'

 L. 718      1104  LOAD_GLOBAL              vis_msg
             1106  LOAD_ATTR                print
             1108  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Non-positive 1x1 convolutional layer number'

 L. 719      1110  LOAD_STR                 'error'
             1112  LOAD_CONST               ('type',)
             1114  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1116  POP_TOP          

 L. 720      1118  LOAD_GLOBAL              QtWidgets
             1120  LOAD_ATTR                QMessageBox
             1122  LOAD_METHOD              critical
             1124  LOAD_DEREF               'self'
             1126  LOAD_ATTR                msgbox

 L. 721      1128  LOAD_STR                 'Train 1.5D-DCNN'

 L. 722      1130  LOAD_STR                 'Non-positive 1x1 convolutional layer number'
             1132  CALL_METHOD_3         3  '3 positional arguments'
             1134  POP_TOP          

 L. 723      1136  LOAD_CONST               None
             1138  RETURN_VALUE     
           1140_0  COME_FROM          1100  '1100'

 L. 724      1140  SETUP_LOOP         1212  'to 1212'
             1142  LOAD_FAST                '_n1x1feature'
             1144  GET_ITER         
           1146_0  COME_FROM          1166  '1166'
             1146  FOR_ITER           1210  'to 1210'
             1148  STORE_FAST               '_i'

 L. 725      1150  LOAD_FAST                '_i'
             1152  LOAD_CONST               False
             1154  COMPARE_OP               is
         1156_1158  POP_JUMP_IF_TRUE   1170  'to 1170'
             1160  LOAD_FAST                '_i'
             1162  LOAD_CONST               1
             1164  COMPARE_OP               <
         1166_1168  POP_JUMP_IF_FALSE  1146  'to 1146'
           1170_0  COME_FROM          1156  '1156'

 L. 726      1170  LOAD_GLOBAL              vis_msg
             1172  LOAD_ATTR                print
             1174  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Non-positive 1x1 convolutional feature number'

 L. 727      1176  LOAD_STR                 'error'
             1178  LOAD_CONST               ('type',)
             1180  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1182  POP_TOP          

 L. 728      1184  LOAD_GLOBAL              QtWidgets
             1186  LOAD_ATTR                QMessageBox
             1188  LOAD_METHOD              critical
             1190  LOAD_DEREF               'self'
             1192  LOAD_ATTR                msgbox

 L. 729      1194  LOAD_STR                 'Train 1.5D-DCNN'

 L. 730      1196  LOAD_STR                 'Non-positive 1x1 convolutional feature number'
             1198  CALL_METHOD_3         3  '3 positional arguments'
             1200  POP_TOP          

 L. 731      1202  LOAD_CONST               None
             1204  RETURN_VALUE     
         1206_1208  JUMP_BACK          1146  'to 1146'
             1210  POP_BLOCK        
           1212_0  COME_FROM_LOOP     1140  '1140'

 L. 732      1212  LOAD_FAST                '_patch_height'
             1214  LOAD_CONST               False
             1216  COMPARE_OP               is
         1218_1220  POP_JUMP_IF_TRUE   1252  'to 1252'
             1222  LOAD_FAST                '_patch_width'
             1224  LOAD_CONST               False
             1226  COMPARE_OP               is
         1228_1230  POP_JUMP_IF_TRUE   1252  'to 1252'

 L. 733      1232  LOAD_FAST                '_patch_height'
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

 L. 734      1252  LOAD_GLOBAL              vis_msg
             1254  LOAD_ATTR                print
             1256  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Non-positive convolutional patch size'

 L. 735      1258  LOAD_STR                 'error'
             1260  LOAD_CONST               ('type',)
             1262  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1264  POP_TOP          

 L. 736      1266  LOAD_GLOBAL              QtWidgets
             1268  LOAD_ATTR                QMessageBox
             1270  LOAD_METHOD              critical
             1272  LOAD_DEREF               'self'
             1274  LOAD_ATTR                msgbox

 L. 737      1276  LOAD_STR                 'Train 1.5D-DCNN'

 L. 738      1278  LOAD_STR                 'Non-positive convolutional patch size'
             1280  CALL_METHOD_3         3  '3 positional arguments'
             1282  POP_TOP          

 L. 739      1284  LOAD_CONST               None
             1286  RETURN_VALUE     
           1288_0  COME_FROM          1248  '1248'

 L. 740      1288  LOAD_FAST                '_pool_height'
             1290  LOAD_CONST               False
             1292  COMPARE_OP               is
         1294_1296  POP_JUMP_IF_TRUE   1328  'to 1328'
             1298  LOAD_FAST                '_pool_width'
             1300  LOAD_CONST               False
             1302  COMPARE_OP               is
         1304_1306  POP_JUMP_IF_TRUE   1328  'to 1328'

 L. 741      1308  LOAD_FAST                '_pool_height'
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

 L. 742      1328  LOAD_GLOBAL              vis_msg
             1330  LOAD_ATTR                print
             1332  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Non-positive pooling size'
             1334  LOAD_STR                 'error'
             1336  LOAD_CONST               ('type',)
             1338  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1340  POP_TOP          

 L. 743      1342  LOAD_GLOBAL              QtWidgets
             1344  LOAD_ATTR                QMessageBox
             1346  LOAD_METHOD              critical
             1348  LOAD_DEREF               'self'
             1350  LOAD_ATTR                msgbox

 L. 744      1352  LOAD_STR                 'Train 1.5D-DCNN'

 L. 745      1354  LOAD_STR                 'Non-positive pooling size'
             1356  CALL_METHOD_3         3  '3 positional arguments'
             1358  POP_TOP          

 L. 746      1360  LOAD_CONST               None
             1362  RETURN_VALUE     
           1364_0  COME_FROM          1324  '1324'

 L. 747      1364  LOAD_FAST                '_nepoch'
             1366  LOAD_CONST               False
             1368  COMPARE_OP               is
         1370_1372  POP_JUMP_IF_TRUE   1384  'to 1384'
             1374  LOAD_FAST                '_nepoch'
             1376  LOAD_CONST               0
             1378  COMPARE_OP               <=
         1380_1382  POP_JUMP_IF_FALSE  1420  'to 1420'
           1384_0  COME_FROM          1370  '1370'

 L. 748      1384  LOAD_GLOBAL              vis_msg
             1386  LOAD_ATTR                print
             1388  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Non-positive epoch number'
             1390  LOAD_STR                 'error'
             1392  LOAD_CONST               ('type',)
             1394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1396  POP_TOP          

 L. 749      1398  LOAD_GLOBAL              QtWidgets
             1400  LOAD_ATTR                QMessageBox
             1402  LOAD_METHOD              critical
             1404  LOAD_DEREF               'self'
             1406  LOAD_ATTR                msgbox

 L. 750      1408  LOAD_STR                 'Train 1.5D-DCNN'

 L. 751      1410  LOAD_STR                 'Non-positive epoch number'
             1412  CALL_METHOD_3         3  '3 positional arguments'
             1414  POP_TOP          

 L. 752      1416  LOAD_CONST               None
             1418  RETURN_VALUE     
           1420_0  COME_FROM          1380  '1380'

 L. 753      1420  LOAD_FAST                '_batchsize'
             1422  LOAD_CONST               False
             1424  COMPARE_OP               is
         1426_1428  POP_JUMP_IF_TRUE   1440  'to 1440'
             1430  LOAD_FAST                '_batchsize'
             1432  LOAD_CONST               0
             1434  COMPARE_OP               <=
         1436_1438  POP_JUMP_IF_FALSE  1476  'to 1476'
           1440_0  COME_FROM          1426  '1426'

 L. 754      1440  LOAD_GLOBAL              vis_msg
             1442  LOAD_ATTR                print
             1444  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Non-positive batch size'
             1446  LOAD_STR                 'error'
             1448  LOAD_CONST               ('tyep',)
             1450  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1452  POP_TOP          

 L. 755      1454  LOAD_GLOBAL              QtWidgets
             1456  LOAD_ATTR                QMessageBox
             1458  LOAD_METHOD              critical
             1460  LOAD_DEREF               'self'
             1462  LOAD_ATTR                msgbox

 L. 756      1464  LOAD_STR                 'Train 1.5D-DCNN'

 L. 757      1466  LOAD_STR                 'Non-positive batch size'
             1468  CALL_METHOD_3         3  '3 positional arguments'
             1470  POP_TOP          

 L. 758      1472  LOAD_CONST               None
             1474  RETURN_VALUE     
           1476_0  COME_FROM          1436  '1436'

 L. 759      1476  LOAD_FAST                '_learning_rate'
             1478  LOAD_CONST               False
             1480  COMPARE_OP               is
         1482_1484  POP_JUMP_IF_TRUE   1496  'to 1496'
             1486  LOAD_FAST                '_learning_rate'
             1488  LOAD_CONST               0
             1490  COMPARE_OP               <=
         1492_1494  POP_JUMP_IF_FALSE  1532  'to 1532'
           1496_0  COME_FROM          1482  '1482'

 L. 760      1496  LOAD_GLOBAL              vis_msg
             1498  LOAD_ATTR                print
             1500  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Non-positive learning rate'
             1502  LOAD_STR                 'error'
             1504  LOAD_CONST               ('type',)
             1506  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1508  POP_TOP          

 L. 761      1510  LOAD_GLOBAL              QtWidgets
             1512  LOAD_ATTR                QMessageBox
             1514  LOAD_METHOD              critical
             1516  LOAD_DEREF               'self'
             1518  LOAD_ATTR                msgbox

 L. 762      1520  LOAD_STR                 'Train 1.5D-DCNN'

 L. 763      1522  LOAD_STR                 'Non-positive learning rate'
             1524  CALL_METHOD_3         3  '3 positional arguments'
             1526  POP_TOP          

 L. 764      1528  LOAD_CONST               None
             1530  RETURN_VALUE     
           1532_0  COME_FROM          1492  '1492'

 L. 765      1532  LOAD_FAST                '_dropout_prob'
             1534  LOAD_CONST               False
             1536  COMPARE_OP               is
         1538_1540  POP_JUMP_IF_TRUE   1552  'to 1552'
             1542  LOAD_FAST                '_dropout_prob'
             1544  LOAD_CONST               0
             1546  COMPARE_OP               <=
         1548_1550  POP_JUMP_IF_FALSE  1588  'to 1588'
           1552_0  COME_FROM          1538  '1538'

 L. 766      1552  LOAD_GLOBAL              vis_msg
             1554  LOAD_ATTR                print
             1556  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: Negative dropout rate'
             1558  LOAD_STR                 'error'
             1560  LOAD_CONST               ('type',)
             1562  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1564  POP_TOP          

 L. 767      1566  LOAD_GLOBAL              QtWidgets
             1568  LOAD_ATTR                QMessageBox
             1570  LOAD_METHOD              critical
             1572  LOAD_DEREF               'self'
             1574  LOAD_ATTR                msgbox

 L. 768      1576  LOAD_STR                 'Train 1.5D-DCNN'

 L. 769      1578  LOAD_STR                 'Negative dropout rate'
             1580  CALL_METHOD_3         3  '3 positional arguments'
             1582  POP_TOP          

 L. 770      1584  LOAD_CONST               None
             1586  RETURN_VALUE     
           1588_0  COME_FROM          1548  '1548'

 L. 772      1588  LOAD_GLOBAL              len
             1590  LOAD_DEREF               'self'
             1592  LOAD_ATTR                ldtsave
             1594  LOAD_METHOD              text
             1596  CALL_METHOD_0         0  '0 positional arguments'
             1598  CALL_FUNCTION_1       1  '1 positional argument'
             1600  LOAD_CONST               1
             1602  COMPARE_OP               <
         1604_1606  POP_JUMP_IF_FALSE  1644  'to 1644'

 L. 773      1608  LOAD_GLOBAL              vis_msg
             1610  LOAD_ATTR                print
             1612  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: No name specified for WDCNN network'

 L. 774      1614  LOAD_STR                 'error'
             1616  LOAD_CONST               ('type',)
             1618  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1620  POP_TOP          

 L. 775      1622  LOAD_GLOBAL              QtWidgets
             1624  LOAD_ATTR                QMessageBox
             1626  LOAD_METHOD              critical
             1628  LOAD_DEREF               'self'
             1630  LOAD_ATTR                msgbox

 L. 776      1632  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 777      1634  LOAD_STR                 'No name specified for WDCNN network'
             1636  CALL_METHOD_3         3  '3 positional arguments'
             1638  POP_TOP          

 L. 778      1640  LOAD_CONST               None
             1642  RETURN_VALUE     
           1644_0  COME_FROM          1604  '1604'

 L. 779      1644  LOAD_GLOBAL              os
             1646  LOAD_ATTR                path
             1648  LOAD_METHOD              dirname
             1650  LOAD_DEREF               'self'
             1652  LOAD_ATTR                ldtsave
             1654  LOAD_METHOD              text
             1656  CALL_METHOD_0         0  '0 positional arguments'
             1658  CALL_METHOD_1         1  '1 positional argument'
             1660  STORE_FAST               '_savepath'

 L. 780      1662  LOAD_GLOBAL              os
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

 L. 782      1692  LOAD_CONST               0
             1694  STORE_FAST               '_wdinl'

 L. 783      1696  LOAD_CONST               0
             1698  STORE_FAST               '_wdxl'

 L. 784      1700  LOAD_CONST               0
             1702  STORE_FAST               '_wdz'

 L. 785      1704  LOAD_CONST               0
             1706  STORE_FAST               '_wdinltarget'

 L. 786      1708  LOAD_CONST               0
             1710  STORE_FAST               '_wdxltarget'

 L. 787      1712  LOAD_CONST               0
             1714  STORE_FAST               '_wdztarget'

 L. 788      1716  LOAD_DEREF               'self'
             1718  LOAD_ATTR                cbbornt
             1720  LOAD_METHOD              currentIndex
             1722  CALL_METHOD_0         0  '0 positional arguments'
             1724  LOAD_CONST               0
             1726  COMPARE_OP               ==
         1728_1730  POP_JUMP_IF_FALSE  1768  'to 1768'

 L. 789      1732  LOAD_GLOBAL              int
             1734  LOAD_FAST                '_image_width'
             1736  LOAD_CONST               2
             1738  BINARY_TRUE_DIVIDE
             1740  CALL_FUNCTION_1       1  '1 positional argument'
             1742  STORE_FAST               '_wdxl'

 L. 790      1744  LOAD_GLOBAL              int
             1746  LOAD_FAST                '_image_height'
             1748  LOAD_CONST               2
             1750  BINARY_TRUE_DIVIDE
             1752  CALL_FUNCTION_1       1  '1 positional argument'
             1754  STORE_FAST               '_wdz'

 L. 791      1756  LOAD_GLOBAL              int
             1758  LOAD_FAST                '_image_height'
             1760  LOAD_CONST               2
             1762  BINARY_TRUE_DIVIDE
             1764  CALL_FUNCTION_1       1  '1 positional argument'
             1766  STORE_FAST               '_wdztarget'
           1768_0  COME_FROM          1728  '1728'

 L. 792      1768  LOAD_DEREF               'self'
             1770  LOAD_ATTR                cbbornt
             1772  LOAD_METHOD              currentIndex
             1774  CALL_METHOD_0         0  '0 positional arguments'
             1776  LOAD_CONST               1
             1778  COMPARE_OP               ==
         1780_1782  POP_JUMP_IF_FALSE  1820  'to 1820'

 L. 793      1784  LOAD_GLOBAL              int
             1786  LOAD_FAST                '_image_width'
             1788  LOAD_CONST               2
             1790  BINARY_TRUE_DIVIDE
             1792  CALL_FUNCTION_1       1  '1 positional argument'
             1794  STORE_FAST               '_wdinl'

 L. 794      1796  LOAD_GLOBAL              int
             1798  LOAD_FAST                '_image_height'
             1800  LOAD_CONST               2
             1802  BINARY_TRUE_DIVIDE
             1804  CALL_FUNCTION_1       1  '1 positional argument'
             1806  STORE_FAST               '_wdz'

 L. 795      1808  LOAD_GLOBAL              int
             1810  LOAD_FAST                '_image_height'
             1812  LOAD_CONST               2
             1814  BINARY_TRUE_DIVIDE
             1816  CALL_FUNCTION_1       1  '1 positional argument'
             1818  STORE_FAST               '_wdztarget'
           1820_0  COME_FROM          1780  '1780'

 L. 796      1820  LOAD_DEREF               'self'
             1822  LOAD_ATTR                cbbornt
             1824  LOAD_METHOD              currentIndex
             1826  CALL_METHOD_0         0  '0 positional arguments'
             1828  LOAD_CONST               2
             1830  COMPARE_OP               ==
         1832_1834  POP_JUMP_IF_FALSE  1872  'to 1872'

 L. 797      1836  LOAD_GLOBAL              int
             1838  LOAD_FAST                '_image_width'
             1840  LOAD_CONST               2
             1842  BINARY_TRUE_DIVIDE
             1844  CALL_FUNCTION_1       1  '1 positional argument'
             1846  STORE_FAST               '_wdinl'

 L. 798      1848  LOAD_GLOBAL              int
             1850  LOAD_FAST                '_image_height'
             1852  LOAD_CONST               2
             1854  BINARY_TRUE_DIVIDE
             1856  CALL_FUNCTION_1       1  '1 positional argument'
             1858  STORE_FAST               '_wdxl'

 L. 799      1860  LOAD_GLOBAL              int
             1862  LOAD_FAST                '_image_height'
             1864  LOAD_CONST               2
             1866  BINARY_TRUE_DIVIDE
             1868  CALL_FUNCTION_1       1  '1 positional argument'
             1870  STORE_FAST               '_wdxltarget'
           1872_0  COME_FROM          1832  '1832'

 L. 801      1872  LOAD_DEREF               'self'
             1874  LOAD_ATTR                survinfo
             1876  STORE_FAST               '_seisinfo'

 L. 803      1878  LOAD_GLOBAL              print
             1880  LOAD_STR                 'TrainMl15DWdcnnFromExisting: Step 1 - Step 1 - Get training samples:'
             1882  CALL_FUNCTION_1       1  '1 positional argument'
             1884  POP_TOP          

 L. 804      1886  LOAD_DEREF               'self'
             1888  LOAD_ATTR                traindataconfig
             1890  LOAD_STR                 'TrainPointSet'
             1892  BINARY_SUBSCR    
             1894  STORE_FAST               '_trainpoint'

 L. 805      1896  LOAD_GLOBAL              np
             1898  LOAD_METHOD              zeros
             1900  LOAD_CONST               0
             1902  LOAD_CONST               3
             1904  BUILD_LIST_2          2 
             1906  CALL_METHOD_1         1  '1 positional argument'
             1908  STORE_FAST               '_traindata'

 L. 806      1910  SETUP_LOOP         1986  'to 1986'
             1912  LOAD_FAST                '_trainpoint'
             1914  GET_ITER         
           1916_0  COME_FROM          1934  '1934'
             1916  FOR_ITER           1984  'to 1984'
             1918  STORE_FAST               '_p'

 L. 807      1920  LOAD_GLOBAL              point_ays
             1922  LOAD_METHOD              checkPoint
             1924  LOAD_DEREF               'self'
             1926  LOAD_ATTR                pointsetdata
             1928  LOAD_FAST                '_p'
             1930  BINARY_SUBSCR    
             1932  CALL_METHOD_1         1  '1 positional argument'
         1934_1936  POP_JUMP_IF_FALSE  1916  'to 1916'

 L. 808      1938  LOAD_GLOBAL              basic_mdt
             1940  LOAD_METHOD              exportMatDict
             1942  LOAD_DEREF               'self'
             1944  LOAD_ATTR                pointsetdata
             1946  LOAD_FAST                '_p'
             1948  BINARY_SUBSCR    
             1950  LOAD_STR                 'Inline'
             1952  LOAD_STR                 'Crossline'
             1954  LOAD_STR                 'Z'
             1956  BUILD_LIST_3          3 
             1958  CALL_METHOD_2         2  '2 positional arguments'
             1960  STORE_FAST               '_pt'

 L. 809      1962  LOAD_GLOBAL              np
             1964  LOAD_ATTR                concatenate
             1966  LOAD_FAST                '_traindata'
             1968  LOAD_FAST                '_pt'
             1970  BUILD_TUPLE_2         2 
             1972  LOAD_CONST               0
             1974  LOAD_CONST               ('axis',)
             1976  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1978  STORE_FAST               '_traindata'
         1980_1982  JUMP_BACK          1916  'to 1916'
             1984  POP_BLOCK        
           1986_0  COME_FROM_LOOP     1910  '1910'

 L. 810      1986  LOAD_GLOBAL              seis_ays
             1988  LOAD_ATTR                removeOutofSurveySample
             1990  LOAD_FAST                '_traindata'

 L. 811      1992  LOAD_FAST                '_seisinfo'
             1994  LOAD_STR                 'ILStart'
             1996  BINARY_SUBSCR    
             1998  LOAD_FAST                '_wdinl'
             2000  LOAD_FAST                '_seisinfo'
             2002  LOAD_STR                 'ILStep'
             2004  BINARY_SUBSCR    
             2006  BINARY_MULTIPLY  
             2008  BINARY_ADD       

 L. 812      2010  LOAD_FAST                '_seisinfo'
             2012  LOAD_STR                 'ILEnd'
             2014  BINARY_SUBSCR    
             2016  LOAD_FAST                '_wdinl'
             2018  LOAD_FAST                '_seisinfo'
             2020  LOAD_STR                 'ILStep'
             2022  BINARY_SUBSCR    
             2024  BINARY_MULTIPLY  
             2026  BINARY_SUBTRACT  

 L. 813      2028  LOAD_FAST                '_seisinfo'
             2030  LOAD_STR                 'XLStart'
             2032  BINARY_SUBSCR    
             2034  LOAD_FAST                '_wdxl'
             2036  LOAD_FAST                '_seisinfo'
             2038  LOAD_STR                 'XLStep'
             2040  BINARY_SUBSCR    
             2042  BINARY_MULTIPLY  
             2044  BINARY_ADD       

 L. 814      2046  LOAD_FAST                '_seisinfo'
             2048  LOAD_STR                 'XLEnd'
             2050  BINARY_SUBSCR    
             2052  LOAD_FAST                '_wdxl'
             2054  LOAD_FAST                '_seisinfo'
             2056  LOAD_STR                 'XLStep'
             2058  BINARY_SUBSCR    
             2060  BINARY_MULTIPLY  
             2062  BINARY_SUBTRACT  

 L. 815      2064  LOAD_FAST                '_seisinfo'
             2066  LOAD_STR                 'ZStart'
             2068  BINARY_SUBSCR    
             2070  LOAD_FAST                '_wdz'
             2072  LOAD_FAST                '_seisinfo'
             2074  LOAD_STR                 'ZStep'
             2076  BINARY_SUBSCR    
             2078  BINARY_MULTIPLY  
             2080  BINARY_ADD       

 L. 816      2082  LOAD_FAST                '_seisinfo'
             2084  LOAD_STR                 'ZEnd'
             2086  BINARY_SUBSCR    
             2088  LOAD_FAST                '_wdz'
             2090  LOAD_FAST                '_seisinfo'
             2092  LOAD_STR                 'ZStep'
             2094  BINARY_SUBSCR    
             2096  BINARY_MULTIPLY  
             2098  BINARY_SUBTRACT  
             2100  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             2102  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2104  STORE_FAST               '_traindata'

 L. 819      2106  LOAD_GLOBAL              np
             2108  LOAD_METHOD              shape
             2110  LOAD_FAST                '_traindata'
             2112  CALL_METHOD_1         1  '1 positional argument'
             2114  LOAD_CONST               0
             2116  BINARY_SUBSCR    
             2118  LOAD_CONST               0
             2120  COMPARE_OP               <=
         2122_2124  POP_JUMP_IF_FALSE  2162  'to 2162'

 L. 820      2126  LOAD_GLOBAL              vis_msg
             2128  LOAD_ATTR                print
             2130  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: No training sample found'
             2132  LOAD_STR                 'error'
             2134  LOAD_CONST               ('type',)
             2136  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2138  POP_TOP          

 L. 821      2140  LOAD_GLOBAL              QtWidgets
             2142  LOAD_ATTR                QMessageBox
             2144  LOAD_METHOD              critical
             2146  LOAD_DEREF               'self'
             2148  LOAD_ATTR                msgbox

 L. 822      2150  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 823      2152  LOAD_STR                 'No training sample found'
             2154  CALL_METHOD_3         3  '3 positional arguments'
             2156  POP_TOP          

 L. 824      2158  LOAD_CONST               None
             2160  RETURN_VALUE     
           2162_0  COME_FROM          2122  '2122'

 L. 827      2162  LOAD_GLOBAL              print
             2164  LOAD_STR                 'TrainMl15DWdcnnFromExisting: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 828      2166  LOAD_FAST                '_image_height'
             2168  LOAD_FAST                '_image_width'
             2170  LOAD_FAST                '_image_height_new'
             2172  LOAD_FAST                '_image_width_new'
             2174  BUILD_TUPLE_4         4 
             2176  BINARY_MODULO    
             2178  CALL_FUNCTION_1       1  '1 positional argument'
             2180  POP_TOP          

 L. 829      2182  BUILD_MAP_0           0 
             2184  STORE_FAST               '_traindict'

 L. 830      2186  SETUP_LOOP         2258  'to 2258'
             2188  LOAD_FAST                '_features'
             2190  GET_ITER         
             2192  FOR_ITER           2256  'to 2256'
             2194  STORE_FAST               'f'

 L. 831      2196  LOAD_DEREF               'self'
             2198  LOAD_ATTR                seisdata
             2200  LOAD_FAST                'f'
             2202  BINARY_SUBSCR    
             2204  STORE_FAST               '_seisdata'

 L. 832      2206  LOAD_GLOBAL              seis_ays
             2208  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2210  LOAD_FAST                '_seisdata'
             2212  LOAD_FAST                '_traindata'
             2214  LOAD_DEREF               'self'
             2216  LOAD_ATTR                survinfo

 L. 833      2218  LOAD_FAST                '_wdinl'
             2220  LOAD_FAST                '_wdxl'
             2222  LOAD_FAST                '_wdz'

 L. 834      2224  LOAD_CONST               False
             2226  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2228  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2230  LOAD_CONST               None
             2232  LOAD_CONST               None
             2234  BUILD_SLICE_2         2 
             2236  LOAD_CONST               3
             2238  LOAD_CONST               None
             2240  BUILD_SLICE_2         2 
             2242  BUILD_TUPLE_2         2 
             2244  BINARY_SUBSCR    
             2246  LOAD_FAST                '_traindict'
             2248  LOAD_FAST                'f'
             2250  STORE_SUBSCR     
         2252_2254  JUMP_BACK          2192  'to 2192'
             2256  POP_BLOCK        
           2258_0  COME_FROM_LOOP     2186  '2186'

 L. 835      2258  LOAD_FAST                '_target'
             2260  LOAD_FAST                '_features'
             2262  COMPARE_OP               not-in
         2264_2266  POP_JUMP_IF_FALSE  2324  'to 2324'

 L. 836      2268  LOAD_DEREF               'self'
             2270  LOAD_ATTR                seisdata
             2272  LOAD_FAST                '_target'
             2274  BINARY_SUBSCR    
             2276  STORE_FAST               '_seisdata'

 L. 837      2278  LOAD_GLOBAL              seis_ays
             2280  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2282  LOAD_FAST                '_seisdata'
             2284  LOAD_FAST                '_traindata'
             2286  LOAD_DEREF               'self'
             2288  LOAD_ATTR                survinfo

 L. 838      2290  LOAD_FAST                '_wdinltarget'

 L. 839      2292  LOAD_FAST                '_wdxltarget'

 L. 840      2294  LOAD_FAST                '_wdztarget'

 L. 841      2296  LOAD_CONST               False
             2298  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2300  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2302  LOAD_CONST               None
             2304  LOAD_CONST               None
             2306  BUILD_SLICE_2         2 
             2308  LOAD_CONST               3
             2310  LOAD_CONST               None
             2312  BUILD_SLICE_2         2 
             2314  BUILD_TUPLE_2         2 
             2316  BINARY_SUBSCR    
             2318  LOAD_FAST                '_traindict'
             2320  LOAD_FAST                '_target'
             2322  STORE_SUBSCR     
           2324_0  COME_FROM          2264  '2264'

 L. 842      2324  LOAD_FAST                '_weight'
             2326  LOAD_FAST                '_features'
             2328  COMPARE_OP               not-in
         2330_2332  POP_JUMP_IF_FALSE  2400  'to 2400'
             2334  LOAD_FAST                '_weight'
             2336  LOAD_FAST                '_target'
             2338  COMPARE_OP               !=
         2340_2342  POP_JUMP_IF_FALSE  2400  'to 2400'

 L. 843      2344  LOAD_DEREF               'self'
             2346  LOAD_ATTR                seisdata
             2348  LOAD_FAST                '_weight'
             2350  BINARY_SUBSCR    
             2352  STORE_FAST               '_seisdata'

 L. 844      2354  LOAD_GLOBAL              seis_ays
             2356  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2358  LOAD_FAST                '_seisdata'
             2360  LOAD_FAST                '_traindata'
             2362  LOAD_DEREF               'self'
             2364  LOAD_ATTR                survinfo

 L. 845      2366  LOAD_FAST                '_wdinltarget'

 L. 846      2368  LOAD_FAST                '_wdxltarget'

 L. 847      2370  LOAD_FAST                '_wdztarget'

 L. 848      2372  LOAD_CONST               False
             2374  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2376  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2378  LOAD_CONST               None
             2380  LOAD_CONST               None
             2382  BUILD_SLICE_2         2 
             2384  LOAD_CONST               3
             2386  LOAD_CONST               None
             2388  BUILD_SLICE_2         2 
             2390  BUILD_TUPLE_2         2 
             2392  BINARY_SUBSCR    
             2394  LOAD_FAST                '_traindict'
             2396  LOAD_FAST                '_weight'
             2398  STORE_SUBSCR     
           2400_0  COME_FROM          2340  '2340'
           2400_1  COME_FROM          2330  '2330'

 L. 850      2400  LOAD_DEREF               'self'
             2402  LOAD_ATTR                traindataconfig
             2404  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2406  BINARY_SUBSCR    
         2408_2410  POP_JUMP_IF_FALSE  2492  'to 2492'

 L. 851      2412  SETUP_LOOP         2492  'to 2492'
             2414  LOAD_FAST                '_features'
             2416  GET_ITER         
           2418_0  COME_FROM          2446  '2446'
             2418  FOR_ITER           2490  'to 2490'
             2420  STORE_FAST               'f'

 L. 852      2422  LOAD_GLOBAL              ml_aug
             2424  LOAD_METHOD              removeInvariantFeature
             2426  LOAD_FAST                '_traindict'
             2428  LOAD_FAST                'f'
             2430  CALL_METHOD_2         2  '2 positional arguments'
             2432  STORE_FAST               '_traindict'

 L. 853      2434  LOAD_GLOBAL              basic_mdt
             2436  LOAD_METHOD              maxDictConstantRow
             2438  LOAD_FAST                '_traindict'
             2440  CALL_METHOD_1         1  '1 positional argument'
             2442  LOAD_CONST               0
             2444  COMPARE_OP               <=
         2446_2448  POP_JUMP_IF_FALSE  2418  'to 2418'

 L. 854      2450  LOAD_GLOBAL              vis_msg
             2452  LOAD_ATTR                print
             2454  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: No training sample found'

 L. 855      2456  LOAD_STR                 'error'
             2458  LOAD_CONST               ('type',)
             2460  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2462  POP_TOP          

 L. 856      2464  LOAD_GLOBAL              QtWidgets
             2466  LOAD_ATTR                QMessageBox
             2468  LOAD_METHOD              critical
             2470  LOAD_DEREF               'self'
             2472  LOAD_ATTR                msgbox

 L. 857      2474  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 858      2476  LOAD_STR                 'No training sample found'
             2478  CALL_METHOD_3         3  '3 positional arguments'
             2480  POP_TOP          

 L. 859      2482  LOAD_CONST               None
             2484  RETURN_VALUE     
         2486_2488  JUMP_BACK          2418  'to 2418'
             2490  POP_BLOCK        
           2492_0  COME_FROM_LOOP     2412  '2412'
           2492_1  COME_FROM          2408  '2408'

 L. 860      2492  LOAD_DEREF               'self'
             2494  LOAD_ATTR                traindataconfig
             2496  LOAD_STR                 'RemoveZeroWeight_Checked'
             2498  BINARY_SUBSCR    
         2500_2502  POP_JUMP_IF_FALSE  2568  'to 2568'

 L. 861      2504  LOAD_GLOBAL              ml_aug
             2506  LOAD_METHOD              removeZeroWeight
             2508  LOAD_FAST                '_traindict'
             2510  LOAD_FAST                '_weight'
             2512  CALL_METHOD_2         2  '2 positional arguments'
             2514  STORE_FAST               '_traindict'

 L. 862      2516  LOAD_GLOBAL              basic_mdt
             2518  LOAD_METHOD              maxDictConstantRow
             2520  LOAD_FAST                '_traindict'
             2522  CALL_METHOD_1         1  '1 positional argument'
             2524  LOAD_CONST               0
             2526  COMPARE_OP               <=
         2528_2530  POP_JUMP_IF_FALSE  2568  'to 2568'

 L. 863      2532  LOAD_GLOBAL              vis_msg
             2534  LOAD_ATTR                print
             2536  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: No training sample found'
             2538  LOAD_STR                 'error'
             2540  LOAD_CONST               ('type',)
             2542  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2544  POP_TOP          

 L. 864      2546  LOAD_GLOBAL              QtWidgets
             2548  LOAD_ATTR                QMessageBox
             2550  LOAD_METHOD              critical
             2552  LOAD_DEREF               'self'
             2554  LOAD_ATTR                msgbox

 L. 865      2556  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 866      2558  LOAD_STR                 'No training sample found'
             2560  CALL_METHOD_3         3  '3 positional arguments'
             2562  POP_TOP          

 L. 867      2564  LOAD_CONST               None
             2566  RETURN_VALUE     
           2568_0  COME_FROM          2528  '2528'
           2568_1  COME_FROM          2500  '2500'

 L. 869      2568  LOAD_GLOBAL              np
             2570  LOAD_METHOD              shape
             2572  LOAD_FAST                '_traindict'
             2574  LOAD_FAST                '_target'
             2576  BINARY_SUBSCR    
             2578  CALL_METHOD_1         1  '1 positional argument'
             2580  LOAD_CONST               0
             2582  BINARY_SUBSCR    
             2584  LOAD_CONST               0
             2586  COMPARE_OP               <=
         2588_2590  POP_JUMP_IF_FALSE  2628  'to 2628'

 L. 870      2592  LOAD_GLOBAL              vis_msg
             2594  LOAD_ATTR                print
             2596  LOAD_STR                 'ERROR in TrainMl15DWdcnnFromExisting: No training sample found'
             2598  LOAD_STR                 'error'
             2600  LOAD_CONST               ('type',)
             2602  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2604  POP_TOP          

 L. 871      2606  LOAD_GLOBAL              QtWidgets
             2608  LOAD_ATTR                QMessageBox
             2610  LOAD_METHOD              critical
             2612  LOAD_DEREF               'self'
             2614  LOAD_ATTR                msgbox

 L. 872      2616  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 873      2618  LOAD_STR                 'No training sample found'
             2620  CALL_METHOD_3         3  '3 positional arguments'
             2622  POP_TOP          

 L. 874      2624  LOAD_CONST               None
             2626  RETURN_VALUE     
           2628_0  COME_FROM          2588  '2588'

 L. 876      2628  LOAD_FAST                '_image_height_new'
             2630  LOAD_FAST                '_image_height'
             2632  COMPARE_OP               !=
         2634_2636  POP_JUMP_IF_TRUE   2648  'to 2648'
             2638  LOAD_FAST                '_image_width_new'
             2640  LOAD_FAST                '_image_width'
             2642  COMPARE_OP               !=
         2644_2646  POP_JUMP_IF_FALSE  2692  'to 2692'
           2648_0  COME_FROM          2634  '2634'

 L. 877      2648  SETUP_LOOP         2692  'to 2692'
             2650  LOAD_FAST                '_features'
             2652  GET_ITER         
             2654  FOR_ITER           2690  'to 2690'
             2656  STORE_FAST               'f'

 L. 878      2658  LOAD_GLOBAL              basic_image
             2660  LOAD_ATTR                changeImageSize
             2662  LOAD_FAST                '_traindict'
             2664  LOAD_FAST                'f'
             2666  BINARY_SUBSCR    

 L. 879      2668  LOAD_FAST                '_image_height'

 L. 880      2670  LOAD_FAST                '_image_width'

 L. 881      2672  LOAD_FAST                '_image_height_new'

 L. 882      2674  LOAD_FAST                '_image_width_new'
             2676  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2678  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2680  LOAD_FAST                '_traindict'
             2682  LOAD_FAST                'f'
             2684  STORE_SUBSCR     
         2686_2688  JUMP_BACK          2654  'to 2654'
             2690  POP_BLOCK        
           2692_0  COME_FROM_LOOP     2648  '2648'
           2692_1  COME_FROM          2644  '2644'

 L. 883      2692  LOAD_FAST                '_image_height_new'
             2694  LOAD_FAST                '_image_height'
             2696  COMPARE_OP               !=
         2698_2700  POP_JUMP_IF_FALSE  2738  'to 2738'
             2702  LOAD_FAST                '_target'
             2704  LOAD_FAST                '_features'
             2706  COMPARE_OP               not-in
         2708_2710  POP_JUMP_IF_FALSE  2738  'to 2738'

 L. 884      2712  LOAD_GLOBAL              basic_curve
             2714  LOAD_ATTR                changeCurveSize
             2716  LOAD_FAST                '_traindict'
             2718  LOAD_FAST                '_target'
             2720  BINARY_SUBSCR    

 L. 885      2722  LOAD_FAST                '_image_height'

 L. 886      2724  LOAD_FAST                '_image_height_new'
             2726  LOAD_STR                 'linear'
             2728  LOAD_CONST               ('length', 'length_new', 'kind')
             2730  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2732  LOAD_FAST                '_traindict'
             2734  LOAD_FAST                '_target'
             2736  STORE_SUBSCR     
           2738_0  COME_FROM          2708  '2708'
           2738_1  COME_FROM          2698  '2698'

 L. 887      2738  LOAD_FAST                '_image_height_new'
             2740  LOAD_FAST                '_image_height'
             2742  COMPARE_OP               !=
         2744_2746  POP_JUMP_IF_FALSE  2794  'to 2794'
             2748  LOAD_FAST                '_weight'
             2750  LOAD_FAST                '_features'
             2752  COMPARE_OP               not-in
         2754_2756  POP_JUMP_IF_FALSE  2794  'to 2794'
             2758  LOAD_FAST                '_weight'
             2760  LOAD_FAST                '_target'
             2762  COMPARE_OP               !=
         2764_2766  POP_JUMP_IF_FALSE  2794  'to 2794'

 L. 888      2768  LOAD_GLOBAL              basic_curve
             2770  LOAD_ATTR                changeCurveSize
             2772  LOAD_FAST                '_traindict'
             2774  LOAD_FAST                '_weight'
             2776  BINARY_SUBSCR    

 L. 889      2778  LOAD_FAST                '_image_height'

 L. 890      2780  LOAD_FAST                '_image_height_new'
             2782  LOAD_STR                 'linear'
             2784  LOAD_CONST               ('length', 'length_new', 'kind')
             2786  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2788  LOAD_FAST                '_traindict'
             2790  LOAD_FAST                '_weight'
             2792  STORE_SUBSCR     
           2794_0  COME_FROM          2764  '2764'
           2794_1  COME_FROM          2754  '2754'
           2794_2  COME_FROM          2744  '2744'

 L. 891      2794  LOAD_DEREF               'self'
             2796  LOAD_ATTR                traindataconfig
             2798  LOAD_STR                 'RotateFeature_Checked'
             2800  BINARY_SUBSCR    
             2802  LOAD_CONST               True
             2804  COMPARE_OP               is
         2806_2808  POP_JUMP_IF_FALSE  2922  'to 2922'

 L. 892      2810  SETUP_LOOP         2848  'to 2848'
             2812  LOAD_FAST                '_features'
             2814  GET_ITER         
             2816  FOR_ITER           2846  'to 2846'
             2818  STORE_FAST               'f'

 L. 893      2820  LOAD_GLOBAL              ml_aug
             2822  LOAD_METHOD              rotateImage4Way
             2824  LOAD_FAST                '_traindict'
             2826  LOAD_FAST                'f'
             2828  BINARY_SUBSCR    
             2830  LOAD_FAST                '_image_height_new'
             2832  LOAD_FAST                '_image_width_new'
             2834  CALL_METHOD_3         3  '3 positional arguments'
             2836  LOAD_FAST                '_traindict'
             2838  LOAD_FAST                'f'
             2840  STORE_SUBSCR     
         2842_2844  JUMP_BACK          2816  'to 2816'
             2846  POP_BLOCK        
           2848_0  COME_FROM_LOOP     2810  '2810'

 L. 894      2848  LOAD_FAST                '_target'
             2850  LOAD_FAST                '_features'
             2852  COMPARE_OP               not-in
         2854_2856  POP_JUMP_IF_FALSE  2880  'to 2880'

 L. 895      2858  LOAD_GLOBAL              ml_aug
             2860  LOAD_METHOD              rotateImage4Way
             2862  LOAD_FAST                '_traindict'
             2864  LOAD_FAST                '_target'
             2866  BINARY_SUBSCR    
             2868  LOAD_FAST                '_image_height_new'
             2870  LOAD_CONST               1
             2872  CALL_METHOD_3         3  '3 positional arguments'
             2874  LOAD_FAST                '_traindict'
             2876  LOAD_FAST                '_target'
             2878  STORE_SUBSCR     
           2880_0  COME_FROM          2854  '2854'

 L. 896      2880  LOAD_FAST                '_weight'
             2882  LOAD_FAST                '_features'
             2884  COMPARE_OP               not-in
         2886_2888  POP_JUMP_IF_FALSE  2922  'to 2922'
             2890  LOAD_FAST                '_weight'
             2892  LOAD_FAST                '_target'
             2894  COMPARE_OP               !=
         2896_2898  POP_JUMP_IF_FALSE  2922  'to 2922'

 L. 897      2900  LOAD_GLOBAL              ml_aug
             2902  LOAD_METHOD              rotateImage4Way
             2904  LOAD_FAST                '_traindict'
             2906  LOAD_FAST                '_weight'
             2908  BINARY_SUBSCR    
             2910  LOAD_FAST                '_image_height_new'
             2912  LOAD_CONST               1
             2914  CALL_METHOD_3         3  '3 positional arguments'
             2916  LOAD_FAST                '_traindict'
             2918  LOAD_FAST                '_weight'
             2920  STORE_SUBSCR     
           2922_0  COME_FROM          2896  '2896'
           2922_1  COME_FROM          2886  '2886'
           2922_2  COME_FROM          2806  '2806'

 L. 899      2922  LOAD_GLOBAL              np
             2924  LOAD_METHOD              round
             2926  LOAD_FAST                '_traindict'
             2928  LOAD_FAST                '_target'
             2930  BINARY_SUBSCR    
             2932  CALL_METHOD_1         1  '1 positional argument'
             2934  LOAD_METHOD              astype
             2936  LOAD_GLOBAL              int
             2938  CALL_METHOD_1         1  '1 positional argument'
             2940  LOAD_FAST                '_traindict'
             2942  LOAD_FAST                '_target'
             2944  STORE_SUBSCR     

 L. 902      2946  LOAD_GLOBAL              print
             2948  LOAD_STR                 'TrainMl15DWdcnnFromExisting: A total of %d valid training samples'
             2950  LOAD_GLOBAL              basic_mdt
             2952  LOAD_METHOD              maxDictConstantRow

 L. 903      2954  LOAD_FAST                '_traindict'
             2956  CALL_METHOD_1         1  '1 positional argument'
             2958  BINARY_MODULO    
             2960  CALL_FUNCTION_1       1  '1 positional argument'
             2962  POP_TOP          

 L. 905      2964  LOAD_GLOBAL              print
             2966  LOAD_STR                 'TrainMl15DWdcnnFromExisting: Step 3 - Start training'
             2968  CALL_FUNCTION_1       1  '1 positional argument'
             2970  POP_TOP          

 L. 907      2972  LOAD_GLOBAL              QtWidgets
             2974  LOAD_METHOD              QProgressDialog
             2976  CALL_METHOD_0         0  '0 positional arguments'
             2978  STORE_FAST               '_pgsdlg'

 L. 908      2980  LOAD_GLOBAL              QtGui
             2982  LOAD_METHOD              QIcon
             2984  CALL_METHOD_0         0  '0 positional arguments'
             2986  STORE_FAST               'icon'

 L. 909      2988  LOAD_FAST                'icon'
             2990  LOAD_METHOD              addPixmap
             2992  LOAD_GLOBAL              QtGui
             2994  LOAD_METHOD              QPixmap
             2996  LOAD_GLOBAL              os
             2998  LOAD_ATTR                path
             3000  LOAD_METHOD              join
             3002  LOAD_DEREF               'self'
             3004  LOAD_ATTR                iconpath
             3006  LOAD_STR                 'icons/new.png'
             3008  CALL_METHOD_2         2  '2 positional arguments'
             3010  CALL_METHOD_1         1  '1 positional argument'

 L. 910      3012  LOAD_GLOBAL              QtGui
             3014  LOAD_ATTR                QIcon
             3016  LOAD_ATTR                Normal
             3018  LOAD_GLOBAL              QtGui
             3020  LOAD_ATTR                QIcon
             3022  LOAD_ATTR                Off
             3024  CALL_METHOD_3         3  '3 positional arguments'
             3026  POP_TOP          

 L. 911      3028  LOAD_FAST                '_pgsdlg'
             3030  LOAD_METHOD              setWindowIcon
             3032  LOAD_FAST                'icon'
             3034  CALL_METHOD_1         1  '1 positional argument'
             3036  POP_TOP          

 L. 912      3038  LOAD_FAST                '_pgsdlg'
             3040  LOAD_METHOD              setWindowTitle
             3042  LOAD_STR                 'Train 1.5D-WDCNN'
             3044  CALL_METHOD_1         1  '1 positional argument'
             3046  POP_TOP          

 L. 913      3048  LOAD_FAST                '_pgsdlg'
             3050  LOAD_METHOD              setCancelButton
             3052  LOAD_CONST               None
             3054  CALL_METHOD_1         1  '1 positional argument'
             3056  POP_TOP          

 L. 914      3058  LOAD_FAST                '_pgsdlg'
             3060  LOAD_METHOD              setWindowFlags
             3062  LOAD_GLOBAL              QtCore
             3064  LOAD_ATTR                Qt
             3066  LOAD_ATTR                WindowStaysOnTopHint
             3068  CALL_METHOD_1         1  '1 positional argument'
             3070  POP_TOP          

 L. 915      3072  LOAD_FAST                '_pgsdlg'
             3074  LOAD_METHOD              forceShow
             3076  CALL_METHOD_0         0  '0 positional arguments'
             3078  POP_TOP          

 L. 916      3080  LOAD_FAST                '_pgsdlg'
             3082  LOAD_METHOD              setFixedWidth
             3084  LOAD_CONST               400
             3086  CALL_METHOD_1         1  '1 positional argument'
             3088  POP_TOP          

 L. 917      3090  LOAD_GLOBAL              ml_wdcnn15d
             3092  LOAD_ATTR                create15DWDCNNSegmentorFromExisting
             3094  LOAD_FAST                '_traindict'

 L. 918      3096  LOAD_FAST                '_image_height_new'

 L. 919      3098  LOAD_FAST                '_image_width_new'

 L. 920      3100  LOAD_FAST                '_features'
             3102  LOAD_FAST                '_target'
             3104  LOAD_FAST                '_weight'

 L. 921      3106  LOAD_FAST                '_nepoch'
             3108  LOAD_FAST                '_batchsize'

 L. 922      3110  LOAD_FAST                '_nconvblock'
             3112  LOAD_FAST                '_nconvfeature'

 L. 923      3114  LOAD_FAST                '_nconvlayer'

 L. 924      3116  LOAD_FAST                '_n1x1layer'
             3118  LOAD_FAST                '_n1x1feature'

 L. 925      3120  LOAD_FAST                '_pool_height'
             3122  LOAD_FAST                '_pool_width'

 L. 926      3124  LOAD_FAST                '_learning_rate'

 L. 927      3126  LOAD_FAST                '_dropout_prob'

 L. 928      3128  LOAD_CONST               True

 L. 929      3130  LOAD_FAST                '_savepath'
             3132  LOAD_FAST                '_savename'

 L. 930      3134  LOAD_FAST                '_pgsdlg'

 L. 931      3136  LOAD_FAST                '_precnnpath'

 L. 932      3138  LOAD_FAST                '_precnnname'

 L. 933      3140  LOAD_FAST                '_blockidx'
             3142  LOAD_FAST                '_layeridx'

 L. 934      3144  LOAD_FAST                '_trainable'
             3146  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'weight', 'nepoch', 'batchsize', 'nconvblock', 'nconvfeature', 'nconvlayer', 'n1x1layer', 'n1x1feature', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprob', 'save2disk', 'savepath', 'savename', 'qpgsdlg', 'precnnpath', 'precnnname', 'blockidx', 'layeridx', 'trainable')
             3148  CALL_FUNCTION_KW_26    26  '26 total positional and keyword args'
             3150  STORE_FAST               '_dcnnlog'

 L. 937      3152  LOAD_GLOBAL              QtWidgets
             3154  LOAD_ATTR                QMessageBox
             3156  LOAD_METHOD              information
             3158  LOAD_DEREF               'self'
             3160  LOAD_ATTR                msgbox

 L. 938      3162  LOAD_STR                 'Train 1.5D-WDCNN'

 L. 939      3164  LOAD_STR                 'DCNN trained successfully'
             3166  CALL_METHOD_3         3  '3 positional arguments'
             3168  POP_TOP          

 L. 941      3170  LOAD_GLOBAL              QtWidgets
             3172  LOAD_ATTR                QMessageBox
             3174  LOAD_METHOD              question
             3176  LOAD_DEREF               'self'
             3178  LOAD_ATTR                msgbox
             3180  LOAD_STR                 'Train 1.5D-WDCNN'
             3182  LOAD_STR                 'View learning matrix?'

 L. 942      3184  LOAD_GLOBAL              QtWidgets
             3186  LOAD_ATTR                QMessageBox
             3188  LOAD_ATTR                Yes
             3190  LOAD_GLOBAL              QtWidgets
             3192  LOAD_ATTR                QMessageBox
             3194  LOAD_ATTR                No
             3196  BINARY_OR        

 L. 943      3198  LOAD_GLOBAL              QtWidgets
             3200  LOAD_ATTR                QMessageBox
             3202  LOAD_ATTR                Yes
             3204  CALL_METHOD_5         5  '5 positional arguments'
             3206  STORE_FAST               'reply'

 L. 945      3208  LOAD_FAST                'reply'
             3210  LOAD_GLOBAL              QtWidgets
             3212  LOAD_ATTR                QMessageBox
             3214  LOAD_ATTR                Yes
             3216  COMPARE_OP               ==
         3218_3220  POP_JUMP_IF_FALSE  3288  'to 3288'

 L. 946      3222  LOAD_GLOBAL              QtWidgets
             3224  LOAD_METHOD              QDialog
             3226  CALL_METHOD_0         0  '0 positional arguments'
             3228  STORE_FAST               '_viewmllearnmat'

 L. 947      3230  LOAD_GLOBAL              gui_viewmllearnmat
             3232  CALL_FUNCTION_0       0  '0 positional arguments'
             3234  STORE_FAST               '_gui'

 L. 948      3236  LOAD_FAST                '_dcnnlog'
             3238  LOAD_STR                 'learning_curve'
             3240  BINARY_SUBSCR    
             3242  LOAD_FAST                '_gui'
             3244  STORE_ATTR               learnmat

 L. 949      3246  LOAD_DEREF               'self'
             3248  LOAD_ATTR                linestyle
             3250  LOAD_FAST                '_gui'
             3252  STORE_ATTR               linestyle

 L. 950      3254  LOAD_DEREF               'self'
             3256  LOAD_ATTR                fontstyle
             3258  LOAD_FAST                '_gui'
             3260  STORE_ATTR               fontstyle

 L. 951      3262  LOAD_FAST                '_gui'
             3264  LOAD_METHOD              setupGUI
             3266  LOAD_FAST                '_viewmllearnmat'
             3268  CALL_METHOD_1         1  '1 positional argument'
             3270  POP_TOP          

 L. 952      3272  LOAD_FAST                '_viewmllearnmat'
             3274  LOAD_METHOD              exec
             3276  CALL_METHOD_0         0  '0 positional arguments'
             3278  POP_TOP          

 L. 953      3280  LOAD_FAST                '_viewmllearnmat'
             3282  LOAD_METHOD              show
             3284  CALL_METHOD_0         0  '0 positional arguments'
             3286  POP_TOP          
           3288_0  COME_FROM          3218  '3218'

Parse error at or near `POP_TOP' instruction at offset 3286

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
    TrainMl15DWdcnnFromExisting = QtWidgets.QWidget()
    gui = trainml15dwdcnnfromexisting()
    gui.setupGUI(TrainMl15DWdcnnFromExisting)
    TrainMl15DWdcnnFromExisting.show()
    sys.exit(app.exec_())