# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\updateml15dwdcnn.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 45836 bytes
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
import cognitivegeo.src.gui.viewml2dwdcnn as gui_viewml2dwdcnn
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class updateml15dwdcnn(object):
    survinfo = {}
    seisdata = {}
    pointsetdata = {}
    rootpath = ''
    linestyle = core_set.Visual['Line']
    maskstyle = core_set.Visual['Image']
    fontstyle = core_set.Visual['Font']
    iconpath = os.path.dirname(__file__)
    dialog = None
    modelpath = ''
    modelname = ''
    modelinfo = None
    traindataconfig = {}
    traindataconfig['TrainPointSet'] = []
    traindataconfig['RotateFeature_Enabled'] = True
    traindataconfig['RotateFeature_Checked'] = False
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False
    traindataconfig['RemoveZeroWeight_Enabled'] = True
    traindataconfig['RemoveZeroWeight_Checked'] = False

    def setupGUI(self, UpdateMl15DWdcnn):
        UpdateMl15DWdcnn.setObjectName('UpdateMl15DWdcnn')
        UpdateMl15DWdcnn.setFixedSize(810, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UpdateMl15DWdcnn.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(UpdateMl15DWdcnn)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(UpdateMl15DWdcnn)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(UpdateMl15DWdcnn)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 230, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 230, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 230, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 270, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 270, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 230, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lbltarget = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 320, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(UpdateMl15DWdcnn)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 320, 280, 30))
        self.lblweight = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblweight.setObjectName('lblweight')
        self.lblweight.setGeometry(QtCore.QRect(10, 370, 100, 30))
        self.cbbweight = QtWidgets.QComboBox(UpdateMl15DWdcnn)
        self.cbbweight.setObjectName('cbbweight')
        self.cbbweight.setGeometry(QtCore.QRect(110, 370, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(UpdateMl15DWdcnn)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(UpdateMl15DWdcnn)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 210))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(UpdateMl15DWdcnn)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 210))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 360, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 360, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 400, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 400, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 360, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 360, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 360, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 400, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 400, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(UpdateMl15DWdcnn)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 420, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 420, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 460, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 460, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 460, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 460, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 500, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 500, 40, 30))
        self.lbldropout = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 500, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 500, 40, 30))
        self.lblsave = QtWidgets.QLabel(UpdateMl15DWdcnn)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 550, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(UpdateMl15DWdcnn)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 550, 180, 30))
        self.btnsave = QtWidgets.QPushButton(UpdateMl15DWdcnn)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 550, 60, 30))
        self.btnapply = QtWidgets.QPushButton(UpdateMl15DWdcnn)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 550, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(UpdateMl15DWdcnn)
        self.msgbox.setObjectName('msgbox')
        _center_x = UpdateMl15DWdcnn.geometry().center().x()
        _center_y = UpdateMl15DWdcnn.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(UpdateMl15DWdcnn)
        QtCore.QMetaObject.connectSlotsByName(UpdateMl15DWdcnn)

    def retranslateGUI(self, UpdateMl15DWdcnn):
        self.dialog = UpdateMl15DWdcnn
        _translate = QtCore.QCoreApplication.translate
        UpdateMl15DWdcnn.setWindowTitle(_translate('UpdateMl15DWdcnn', 'Update 1.5D-WDCNN'))
        self.lblfrom.setText(_translate('UpdateMl15DWdcnn', 'Select network:'))
        self.ldtfrom.setText(_translate('UpdateMl15DWdcnn', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('UpdateMl15DWdcnn', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('UpdateMl15DWdcnn', 'Training features:'))
        self.lblornt.setText(_translate('UpdateMl15DWdcnn', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('UpdateMl15DWdcnn', 'Training target:'))
        self.lblweight.setText(_translate('UpdateMl15DWdcnn', 'Training weight:'))
        self.btnconfigtraindata.setText(_translate('TrainMl2DDcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('UpdateMl15DWdcnn', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('UpdateMl15DWdcnn', 'height='))
        self.ldtoldheight.setText(_translate('UpdateMl15DWdcnn', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('UpdateMl15DWdcnn', 'width='))
        self.ldtoldwidth.setText(_translate('UpdateMl15DWdcnn', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('UpdateMl15DWdcnn', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('UpdateMl15DWdcnn', 'height='))
        self.ldtnewheight.setText(_translate('UpdateMl15DWdcnn', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('UpdateMl15DWdcnn', 'width='))
        self.ldtnewwidth.setText(_translate('UpdateMl15DWdcnn', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('UpdateMl15DWdcnn', 'Pre-trained WDCNN architecture:'))
        self.btnviewnetwork.setText(_translate('UpdateMl15DWdcnn', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('UpdateMl15DWdcnn', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('UpdateMl15DWdcnn', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('UpdateMl15DWdcnn', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('UpdateMl15DWdcnn', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('UpdateMl15DWdcnn', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('UpdateMl15DWdcnn', 'height='))
        self.ldtmaskheight.setText(_translate('UpdateMl15DWdcnn', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('UpdateMl15DWdcnn', 'width='))
        self.ldtmaskwidth.setText(_translate('UpdateMl15DWdcnn', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('UpdateMl15DWdcnn', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('UpdateMl15DWdcnn', 'height='))
        self.ldtpoolheight.setText(_translate('UpdateMl15DWdcnn', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('UpdateMl15DWdcnn', 'width='))
        self.ldtpoolwidth.setText(_translate('UpdateMl15DWdcnn', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('UpdateMl15DWdcnn', 'Specify update parameters:'))
        self.lblnepoch.setText(_translate('UpdateMl15DWdcnn', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('UpdateMl15DWdcnn', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('UpdateMl15DWdcnn', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('UpdateMl15DWdcnn', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('UpdateMl15DWdcnn', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('UpdateMl15DWdcnn', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('UpdateMl15DWdcnn', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('UpdateMl15DWdcnn', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('UpdateMl15DWdcnn', 'Save new-WDCNN to:'))
        self.ldtsave.setText(_translate('UpdateMl15DWdcnn', ''))
        self.btnsave.setText(_translate('UpdateMl15DWdcnn', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('UpdateMl15DWdcnn', 'Update 1.5D-WDCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnUpdateMl15DWdcnn)

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.check15DWDCNNModel(self.modelpath, self.modelname) is True:
            self.modelinfo = ml_tfm.getModelInfo(self.modelpath, self.modelname)
            self.lwgfeature.clear()
            _firstfeature = None
            for f in self.modelinfo['feature_list']:
                item = QtWidgets.QListWidgetItem(self.lwgfeature)
                item.setText(f)
                self.lwgfeature.addItem(item)
                if _firstfeature is None:
                    _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            _height = self.modelinfo['image_size'][0]
            _width = self.modelinfo['image_size'][1]
            self.ldtnewheight.setText(str(_height))
            self.ldtnewwidth.setText(str(_width))
            self.cbbtarget.clear()
            self.cbbtarget.addItem(self.modelinfo['target'])
            self.cbbweight.clear()
            self.cbbweight.addItem(self.modelinfo['weight'])
            self.btnviewnetwork.setEnabled(True)
            self.ldtnconvblock.setText(str(self.modelinfo['number_conv_block']))
            self.ldtn1x1layer.setText(str(self.modelinfo['number_1x1_layer']))
            self.ldtmaskheight.setText(str(self.modelinfo['patch_size'][0]))
            self.ldtmaskwidth.setText(str(self.modelinfo['patch_size'][1]))
            self.ldtpoolheight.setText(str(self.modelinfo['pool_size'][0]))
            self.ldtpoolwidth.setText(str(self.modelinfo['pool_size'][1]))
        else:
            self.modelpath = ''
            self.modelname = ''
            self.modelinfo = None
            self.lwgfeature.clear()
            self.ldtnewheight.setText('')
            self.ldtnewwidth.setText('')
            self.cbbtarget.clear()
            self.cbbweight.clear()
            self.btnviewnetwork.setEnabled(False)
            self.ldtnconvblock.setText('')
            self.ldtn1x1layer.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')

    def clickBtnFrom(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select WDCNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def clickBtnViewNetwork(self):
        _viewml = QtWidgets.QDialog()
        _gui = gui_viewml2dwdcnn()
        _gui.linestyle = self.linestyle
        _gui.maskstyle = self.maskstyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewml)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewml.exec()
        _viewml.show()

    def changeLdtNconvblock(self):
        if ml_tfm.check15DWDCNNModel(self.modelpath, self.modelname) is True:
            _nlayer = self.modelinfo['number_conv_block']
            self.twgnconvblock.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblock.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.modelinfo['number_conv_layer'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblock.setItem(_idx, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.modelinfo['number_conv_feature'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblock.setItem(_idx, 2, item)

        else:
            self.twgnconvblock.setRowCount(0)

    def changeLdtN1x1layer(self):
        if ml_tfm.check15DWDCNNModel(self.modelpath, self.modelname) is True:
            _nlayer = self.modelinfo['number_1x1_layer']
            self.twgn1x1layer.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgn1x1layer.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.modelinfo['number_1x1_feature'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
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

    def clickBtnUpdateMl15DWdcnn--- This code section failed: ---

 L. 527         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 529         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 530        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in UpdateMl15DWdcnn: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 531        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 532        44  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 533        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 534        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 536        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              check15DWDCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 537        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in UpdateMl15DWdcnn: No pre-WDCNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 538        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 539       100  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 540       102  LOAD_STR                 'No pre-WDCNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 541       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 543       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 544       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 545       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in UpdateMl15DWdcnn: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    

 L. 546       152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 547       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 548       170  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 549       172  LOAD_STR                 "Feature '"
              174  LOAD_FAST                'f'
              176  BINARY_ADD       
              178  LOAD_STR                 "' not found in seismic data"
              180  BINARY_ADD       
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L. 550       186  LOAD_CONST               None
              188  RETURN_VALUE     
              190  JUMP_BACK           124  'to 124'
              192  POP_BLOCK        
            194_0  COME_FROM_LOOP      112  '112'

 L. 552       194  LOAD_GLOBAL              basic_data
              196  LOAD_METHOD              str2int
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                ldtoldheight
              202  LOAD_METHOD              text
              204  CALL_METHOD_0         0  '0 positional arguments'
              206  CALL_METHOD_1         1  '1 positional argument'
              208  STORE_FAST               '_image_height'

 L. 553       210  LOAD_GLOBAL              basic_data
              212  LOAD_METHOD              str2int
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                ldtoldwidth
              218  LOAD_METHOD              text
              220  CALL_METHOD_0         0  '0 positional arguments'
              222  CALL_METHOD_1         1  '1 positional argument'
              224  STORE_FAST               '_image_width'

 L. 554       226  LOAD_GLOBAL              basic_data
              228  LOAD_METHOD              str2int
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                ldtnewheight
              234  LOAD_METHOD              text
              236  CALL_METHOD_0         0  '0 positional arguments'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  STORE_FAST               '_image_height_new'

 L. 555       242  LOAD_GLOBAL              basic_data
              244  LOAD_METHOD              str2int
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                ldtnewwidth
              250  LOAD_METHOD              text
              252  CALL_METHOD_0         0  '0 positional arguments'
              254  CALL_METHOD_1         1  '1 positional argument'
              256  STORE_FAST               '_image_width_new'

 L. 556       258  LOAD_FAST                '_image_height'
              260  LOAD_CONST               False
              262  COMPARE_OP               is
          264_266  POP_JUMP_IF_TRUE    298  'to 298'
              268  LOAD_FAST                '_image_width'
              270  LOAD_CONST               False
              272  COMPARE_OP               is
          274_276  POP_JUMP_IF_TRUE    298  'to 298'

 L. 557       278  LOAD_FAST                '_image_height_new'
              280  LOAD_CONST               False
              282  COMPARE_OP               is
          284_286  POP_JUMP_IF_TRUE    298  'to 298'
              288  LOAD_FAST                '_image_width_new'
              290  LOAD_CONST               False
              292  COMPARE_OP               is
          294_296  POP_JUMP_IF_FALSE   334  'to 334'
            298_0  COME_FROM           284  '284'
            298_1  COME_FROM           274  '274'
            298_2  COME_FROM           264  '264'

 L. 558       298  LOAD_GLOBAL              vis_msg
              300  LOAD_ATTR                print
              302  LOAD_STR                 'ERROR in UpdateMl15DWdcnn: Non-integer feature size'
              304  LOAD_STR                 'error'
              306  LOAD_CONST               ('type',)
              308  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              310  POP_TOP          

 L. 559       312  LOAD_GLOBAL              QtWidgets
              314  LOAD_ATTR                QMessageBox
              316  LOAD_METHOD              critical
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                msgbox

 L. 560       322  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 561       324  LOAD_STR                 'Non-integer feature size'
              326  CALL_METHOD_3         3  '3 positional arguments'
              328  POP_TOP          

 L. 562       330  LOAD_CONST               None
              332  RETURN_VALUE     
            334_0  COME_FROM           294  '294'

 L. 563       334  LOAD_FAST                '_image_height'
              336  LOAD_CONST               2
              338  COMPARE_OP               <
          340_342  POP_JUMP_IF_TRUE    374  'to 374'
              344  LOAD_FAST                '_image_width'
              346  LOAD_CONST               2
              348  COMPARE_OP               <
          350_352  POP_JUMP_IF_TRUE    374  'to 374'

 L. 564       354  LOAD_FAST                '_image_height_new'
              356  LOAD_CONST               2
              358  COMPARE_OP               <
          360_362  POP_JUMP_IF_TRUE    374  'to 374'
              364  LOAD_FAST                '_image_width_new'
              366  LOAD_CONST               2
              368  COMPARE_OP               <
          370_372  POP_JUMP_IF_FALSE   410  'to 410'
            374_0  COME_FROM           360  '360'
            374_1  COME_FROM           350  '350'
            374_2  COME_FROM           340  '340'

 L. 565       374  LOAD_GLOBAL              vis_msg
              376  LOAD_ATTR                print
              378  LOAD_STR                 'ERROR in UpdateMl15DWdcnn: Features are not 2D'
              380  LOAD_STR                 'error'
              382  LOAD_CONST               ('type',)
              384  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              386  POP_TOP          

 L. 566       388  LOAD_GLOBAL              QtWidgets
              390  LOAD_ATTR                QMessageBox
              392  LOAD_METHOD              critical
              394  LOAD_FAST                'self'
              396  LOAD_ATTR                msgbox

 L. 567       398  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 568       400  LOAD_STR                 'Features are not 2D'
              402  CALL_METHOD_3         3  '3 positional arguments'
              404  POP_TOP          

 L. 569       406  LOAD_CONST               None
              408  RETURN_VALUE     
            410_0  COME_FROM           370  '370'

 L. 571       410  LOAD_CONST               2
              412  LOAD_GLOBAL              int
              414  LOAD_FAST                '_image_height'
              416  LOAD_CONST               2
              418  BINARY_TRUE_DIVIDE
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  BINARY_MULTIPLY  
              424  LOAD_CONST               1
              426  BINARY_ADD       
              428  STORE_FAST               '_image_height'

 L. 572       430  LOAD_CONST               2
              432  LOAD_GLOBAL              int
              434  LOAD_FAST                '_image_width'
              436  LOAD_CONST               2
              438  BINARY_TRUE_DIVIDE
              440  CALL_FUNCTION_1       1  '1 positional argument'
              442  BINARY_MULTIPLY  
              444  LOAD_CONST               1
              446  BINARY_ADD       
              448  STORE_FAST               '_image_width'

 L. 574       450  LOAD_FAST                'self'
              452  LOAD_ATTR                modelinfo
              454  LOAD_STR                 'target'
              456  BINARY_SUBSCR    
              458  LOAD_FAST                'self'
              460  LOAD_ATTR                seisdata
              462  LOAD_METHOD              keys
              464  CALL_METHOD_0         0  '0 positional arguments'
              466  COMPARE_OP               not-in
          468_470  POP_JUMP_IF_FALSE   532  'to 532'

 L. 575       472  LOAD_GLOBAL              vis_msg
              474  LOAD_ATTR                print
              476  LOAD_STR                 "ERROR in UpdateMl15DWdcnn: Target key '%s' not found in seismic data"

 L. 576       478  LOAD_FAST                'self'
              480  LOAD_ATTR                modelinfo
              482  LOAD_STR                 'target'
              484  BINARY_SUBSCR    
              486  BINARY_MODULO    
              488  LOAD_STR                 'error'
              490  LOAD_CONST               ('type',)
              492  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              494  POP_TOP          

 L. 577       496  LOAD_GLOBAL              QtWidgets
              498  LOAD_ATTR                QMessageBox
              500  LOAD_METHOD              critical
              502  LOAD_FAST                'self'
              504  LOAD_ATTR                msgbox

 L. 578       506  LOAD_STR                 'Update 1.5D-DWCNN'

 L. 579       508  LOAD_STR                 "Target key '"
              510  LOAD_FAST                'self'
              512  LOAD_ATTR                modelinfo
              514  LOAD_STR                 'target'
              516  BINARY_SUBSCR    
              518  BINARY_ADD       
              520  LOAD_STR                 ' not found in seismic data'
              522  BINARY_ADD       
              524  CALL_METHOD_3         3  '3 positional arguments'
              526  POP_TOP          

 L. 580       528  LOAD_CONST               None
              530  RETURN_VALUE     
            532_0  COME_FROM           468  '468'

 L. 581       532  LOAD_FAST                'self'
              534  LOAD_ATTR                modelinfo
              536  LOAD_STR                 'weight'
              538  BINARY_SUBSCR    
              540  LOAD_FAST                'self'
              542  LOAD_ATTR                seisdata
              544  LOAD_METHOD              keys
              546  CALL_METHOD_0         0  '0 positional arguments'
              548  COMPARE_OP               not-in
          550_552  POP_JUMP_IF_FALSE   614  'to 614'

 L. 582       554  LOAD_GLOBAL              vis_msg
              556  LOAD_ATTR                print
              558  LOAD_STR                 "ERROR in UpdateMl15DWdcnn: Weight key '%s' not found in seismic data"

 L. 583       560  LOAD_FAST                'self'
              562  LOAD_ATTR                modelinfo
              564  LOAD_STR                 'weight'
              566  BINARY_SUBSCR    
              568  BINARY_MODULO    
              570  LOAD_STR                 'error'
              572  LOAD_CONST               ('type',)
              574  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              576  POP_TOP          

 L. 584       578  LOAD_GLOBAL              QtWidgets
              580  LOAD_ATTR                QMessageBox
              582  LOAD_METHOD              critical
              584  LOAD_FAST                'self'
              586  LOAD_ATTR                msgbox

 L. 585       588  LOAD_STR                 'Update 1.5D-DWCNN'

 L. 586       590  LOAD_STR                 "Weight key '"
              592  LOAD_FAST                'self'
              594  LOAD_ATTR                modelinfo
              596  LOAD_STR                 'weight'
              598  BINARY_SUBSCR    
              600  BINARY_ADD       
              602  LOAD_STR                 ' not found in seismic data'
              604  BINARY_ADD       
              606  CALL_METHOD_3         3  '3 positional arguments'
              608  POP_TOP          

 L. 587       610  LOAD_CONST               None
              612  RETURN_VALUE     
            614_0  COME_FROM           550  '550'

 L. 589       614  LOAD_FAST                'self'
              616  LOAD_ATTR                modelinfo
              618  LOAD_STR                 'feature_list'
              620  BINARY_SUBSCR    
              622  STORE_FAST               '_features'

 L. 590       624  LOAD_FAST                'self'
              626  LOAD_ATTR                modelinfo
              628  LOAD_STR                 'target'
              630  BINARY_SUBSCR    
              632  STORE_FAST               '_target'

 L. 591       634  LOAD_FAST                'self'
              636  LOAD_ATTR                modelinfo
              638  LOAD_STR                 'weight'
              640  BINARY_SUBSCR    
              642  STORE_FAST               '_weight'

 L. 593       644  LOAD_GLOBAL              basic_data
              646  LOAD_METHOD              str2int
              648  LOAD_FAST                'self'
              650  LOAD_ATTR                ldtnepoch
              652  LOAD_METHOD              text
              654  CALL_METHOD_0         0  '0 positional arguments'
              656  CALL_METHOD_1         1  '1 positional argument'
              658  STORE_FAST               '_nepoch'

 L. 594       660  LOAD_GLOBAL              basic_data
              662  LOAD_METHOD              str2int
              664  LOAD_FAST                'self'
              666  LOAD_ATTR                ldtbatchsize
              668  LOAD_METHOD              text
              670  CALL_METHOD_0         0  '0 positional arguments'
              672  CALL_METHOD_1         1  '1 positional argument'
              674  STORE_FAST               '_batchsize'

 L. 595       676  LOAD_GLOBAL              basic_data
              678  LOAD_METHOD              str2float
              680  LOAD_FAST                'self'
              682  LOAD_ATTR                ldtlearnrate
              684  LOAD_METHOD              text
              686  CALL_METHOD_0         0  '0 positional arguments'
              688  CALL_METHOD_1         1  '1 positional argument'
              690  STORE_FAST               '_learning_rate'

 L. 596       692  LOAD_GLOBAL              basic_data
              694  LOAD_METHOD              str2float
              696  LOAD_FAST                'self'
              698  LOAD_ATTR                ldtdropout
              700  LOAD_METHOD              text
              702  CALL_METHOD_0         0  '0 positional arguments'
              704  CALL_METHOD_1         1  '1 positional argument'
              706  STORE_FAST               '_dropout_prob'

 L. 597       708  LOAD_FAST                '_nepoch'
              710  LOAD_CONST               False
              712  COMPARE_OP               is
          714_716  POP_JUMP_IF_TRUE    728  'to 728'
              718  LOAD_FAST                '_nepoch'
              720  LOAD_CONST               0
              722  COMPARE_OP               <=
          724_726  POP_JUMP_IF_FALSE   764  'to 764'
            728_0  COME_FROM           714  '714'

 L. 598       728  LOAD_GLOBAL              vis_msg
              730  LOAD_ATTR                print
              732  LOAD_STR                 'ERROR in UpdateMl15DWdcnn: Non-positive epoch number'
              734  LOAD_STR                 'error'
              736  LOAD_CONST               ('type',)
              738  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              740  POP_TOP          

 L. 599       742  LOAD_GLOBAL              QtWidgets
              744  LOAD_ATTR                QMessageBox
              746  LOAD_METHOD              critical
              748  LOAD_FAST                'self'
              750  LOAD_ATTR                msgbox

 L. 600       752  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 601       754  LOAD_STR                 'Non-positive epoch number'
              756  CALL_METHOD_3         3  '3 positional arguments'
              758  POP_TOP          

 L. 602       760  LOAD_CONST               None
              762  RETURN_VALUE     
            764_0  COME_FROM           724  '724'

 L. 603       764  LOAD_FAST                '_batchsize'
              766  LOAD_CONST               False
              768  COMPARE_OP               is
          770_772  POP_JUMP_IF_TRUE    784  'to 784'
              774  LOAD_FAST                '_batchsize'
              776  LOAD_CONST               0
              778  COMPARE_OP               <=
          780_782  POP_JUMP_IF_FALSE   820  'to 820'
            784_0  COME_FROM           770  '770'

 L. 604       784  LOAD_GLOBAL              vis_msg
              786  LOAD_ATTR                print
              788  LOAD_STR                 'ERROR in UpdateMl15DWdcnn: Non-positive batch size'
              790  LOAD_STR                 'error'
              792  LOAD_CONST               ('type',)
              794  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              796  POP_TOP          

 L. 605       798  LOAD_GLOBAL              QtWidgets
              800  LOAD_ATTR                QMessageBox
              802  LOAD_METHOD              critical
              804  LOAD_FAST                'self'
              806  LOAD_ATTR                msgbox

 L. 606       808  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 607       810  LOAD_STR                 'Non-positive batch size'
              812  CALL_METHOD_3         3  '3 positional arguments'
              814  POP_TOP          

 L. 608       816  LOAD_CONST               None
              818  RETURN_VALUE     
            820_0  COME_FROM           780  '780'

 L. 609       820  LOAD_FAST                '_learning_rate'
              822  LOAD_CONST               False
              824  COMPARE_OP               is
          826_828  POP_JUMP_IF_TRUE    840  'to 840'
              830  LOAD_FAST                '_learning_rate'
              832  LOAD_CONST               0
              834  COMPARE_OP               <=
          836_838  POP_JUMP_IF_FALSE   876  'to 876'
            840_0  COME_FROM           826  '826'

 L. 610       840  LOAD_GLOBAL              vis_msg
              842  LOAD_ATTR                print
              844  LOAD_STR                 'ERROR in UpdateMl15DWdcnn: Non-positive learning rate'
              846  LOAD_STR                 'error'
              848  LOAD_CONST               ('type',)
              850  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              852  POP_TOP          

 L. 611       854  LOAD_GLOBAL              QtWidgets
              856  LOAD_ATTR                QMessageBox
              858  LOAD_METHOD              critical
              860  LOAD_FAST                'self'
              862  LOAD_ATTR                msgbox

 L. 612       864  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 613       866  LOAD_STR                 'Non-positive learning rate'
              868  CALL_METHOD_3         3  '3 positional arguments'
              870  POP_TOP          

 L. 614       872  LOAD_CONST               None
              874  RETURN_VALUE     
            876_0  COME_FROM           836  '836'

 L. 615       876  LOAD_FAST                '_dropout_prob'
              878  LOAD_CONST               False
              880  COMPARE_OP               is
          882_884  POP_JUMP_IF_TRUE    896  'to 896'
              886  LOAD_FAST                '_dropout_prob'
              888  LOAD_CONST               0
              890  COMPARE_OP               <=
          892_894  POP_JUMP_IF_FALSE   932  'to 932'
            896_0  COME_FROM           882  '882'

 L. 616       896  LOAD_GLOBAL              vis_msg
              898  LOAD_ATTR                print
              900  LOAD_STR                 'ERROR in UpdateMl15DWdcnn: Negative dropout rate'
              902  LOAD_STR                 'error'
              904  LOAD_CONST               ('type',)
              906  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              908  POP_TOP          

 L. 617       910  LOAD_GLOBAL              QtWidgets
              912  LOAD_ATTR                QMessageBox
              914  LOAD_METHOD              critical
              916  LOAD_FAST                'self'
              918  LOAD_ATTR                msgbox

 L. 618       920  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 619       922  LOAD_STR                 'Negative dropout rate'
              924  CALL_METHOD_3         3  '3 positional arguments'
              926  POP_TOP          

 L. 620       928  LOAD_CONST               None
              930  RETURN_VALUE     
            932_0  COME_FROM           892  '892'

 L. 622       932  LOAD_GLOBAL              len
              934  LOAD_FAST                'self'
              936  LOAD_ATTR                ldtsave
              938  LOAD_METHOD              text
              940  CALL_METHOD_0         0  '0 positional arguments'
              942  CALL_FUNCTION_1       1  '1 positional argument'
              944  LOAD_CONST               1
              946  COMPARE_OP               <
          948_950  POP_JUMP_IF_FALSE   988  'to 988'

 L. 623       952  LOAD_GLOBAL              vis_msg
              954  LOAD_ATTR                print
              956  LOAD_STR                 'ERROR in UpdateMl15DWdcnn: No name specified for WDCNN network'
              958  LOAD_STR                 'error'
              960  LOAD_CONST               ('type',)
              962  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              964  POP_TOP          

 L. 624       966  LOAD_GLOBAL              QtWidgets
              968  LOAD_ATTR                QMessageBox
              970  LOAD_METHOD              critical
              972  LOAD_FAST                'self'
              974  LOAD_ATTR                msgbox

 L. 625       976  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 626       978  LOAD_STR                 'No name specified for WDCNN network'
              980  CALL_METHOD_3         3  '3 positional arguments'
              982  POP_TOP          

 L. 627       984  LOAD_CONST               None
              986  RETURN_VALUE     
            988_0  COME_FROM           948  '948'

 L. 628       988  LOAD_GLOBAL              os
              990  LOAD_ATTR                path
              992  LOAD_METHOD              dirname
              994  LOAD_FAST                'self'
              996  LOAD_ATTR                ldtsave
              998  LOAD_METHOD              text
             1000  CALL_METHOD_0         0  '0 positional arguments'
             1002  CALL_METHOD_1         1  '1 positional argument'
             1004  STORE_FAST               '_savepath'

 L. 629      1006  LOAD_GLOBAL              os
             1008  LOAD_ATTR                path
             1010  LOAD_METHOD              splitext
             1012  LOAD_GLOBAL              os
             1014  LOAD_ATTR                path
             1016  LOAD_METHOD              basename
             1018  LOAD_FAST                'self'
             1020  LOAD_ATTR                ldtsave
             1022  LOAD_METHOD              text
             1024  CALL_METHOD_0         0  '0 positional arguments'
             1026  CALL_METHOD_1         1  '1 positional argument'
             1028  CALL_METHOD_1         1  '1 positional argument'
             1030  LOAD_CONST               0
             1032  BINARY_SUBSCR    
             1034  STORE_FAST               '_savename'

 L. 631      1036  LOAD_CONST               0
             1038  STORE_FAST               '_wdinl'

 L. 632      1040  LOAD_CONST               0
             1042  STORE_FAST               '_wdxl'

 L. 633      1044  LOAD_CONST               0
             1046  STORE_FAST               '_wdz'

 L. 634      1048  LOAD_CONST               0
             1050  STORE_FAST               '_wdinltarget'

 L. 635      1052  LOAD_CONST               0
             1054  STORE_FAST               '_wdxltarget'

 L. 636      1056  LOAD_CONST               0
             1058  STORE_FAST               '_wdztarget'

 L. 637      1060  LOAD_FAST                'self'
             1062  LOAD_ATTR                cbbornt
             1064  LOAD_METHOD              currentIndex
             1066  CALL_METHOD_0         0  '0 positional arguments'
             1068  LOAD_CONST               0
             1070  COMPARE_OP               ==
         1072_1074  POP_JUMP_IF_FALSE  1112  'to 1112'

 L. 638      1076  LOAD_GLOBAL              int
             1078  LOAD_FAST                '_image_width'
             1080  LOAD_CONST               2
             1082  BINARY_TRUE_DIVIDE
             1084  CALL_FUNCTION_1       1  '1 positional argument'
             1086  STORE_FAST               '_wdxl'

 L. 639      1088  LOAD_GLOBAL              int
             1090  LOAD_FAST                '_image_height'
             1092  LOAD_CONST               2
             1094  BINARY_TRUE_DIVIDE
             1096  CALL_FUNCTION_1       1  '1 positional argument'
             1098  STORE_FAST               '_wdz'

 L. 640      1100  LOAD_GLOBAL              int
             1102  LOAD_FAST                '_image_height'
             1104  LOAD_CONST               2
             1106  BINARY_TRUE_DIVIDE
             1108  CALL_FUNCTION_1       1  '1 positional argument'
             1110  STORE_FAST               '_wdztarget'
           1112_0  COME_FROM          1072  '1072'

 L. 641      1112  LOAD_FAST                'self'
             1114  LOAD_ATTR                cbbornt
             1116  LOAD_METHOD              currentIndex
             1118  CALL_METHOD_0         0  '0 positional arguments'
             1120  LOAD_CONST               1
             1122  COMPARE_OP               ==
         1124_1126  POP_JUMP_IF_FALSE  1164  'to 1164'

 L. 642      1128  LOAD_GLOBAL              int
             1130  LOAD_FAST                '_image_width'
             1132  LOAD_CONST               2
             1134  BINARY_TRUE_DIVIDE
             1136  CALL_FUNCTION_1       1  '1 positional argument'
             1138  STORE_FAST               '_wdinl'

 L. 643      1140  LOAD_GLOBAL              int
             1142  LOAD_FAST                '_image_height'
             1144  LOAD_CONST               2
             1146  BINARY_TRUE_DIVIDE
             1148  CALL_FUNCTION_1       1  '1 positional argument'
             1150  STORE_FAST               '_wdz'

 L. 644      1152  LOAD_GLOBAL              int
             1154  LOAD_FAST                '_image_height'
             1156  LOAD_CONST               2
             1158  BINARY_TRUE_DIVIDE
             1160  CALL_FUNCTION_1       1  '1 positional argument'
             1162  STORE_FAST               '_wdztarget'
           1164_0  COME_FROM          1124  '1124'

 L. 645      1164  LOAD_FAST                'self'
             1166  LOAD_ATTR                cbbornt
             1168  LOAD_METHOD              currentIndex
             1170  CALL_METHOD_0         0  '0 positional arguments'
             1172  LOAD_CONST               2
             1174  COMPARE_OP               ==
         1176_1178  POP_JUMP_IF_FALSE  1216  'to 1216'

 L. 646      1180  LOAD_GLOBAL              int
             1182  LOAD_FAST                '_image_width'
             1184  LOAD_CONST               2
             1186  BINARY_TRUE_DIVIDE
             1188  CALL_FUNCTION_1       1  '1 positional argument'
             1190  STORE_FAST               '_wdinl'

 L. 647      1192  LOAD_GLOBAL              int
             1194  LOAD_FAST                '_image_height'
             1196  LOAD_CONST               2
             1198  BINARY_TRUE_DIVIDE
             1200  CALL_FUNCTION_1       1  '1 positional argument'
             1202  STORE_FAST               '_wdxl'

 L. 648      1204  LOAD_GLOBAL              int
             1206  LOAD_FAST                '_image_height'
             1208  LOAD_CONST               2
             1210  BINARY_TRUE_DIVIDE
             1212  CALL_FUNCTION_1       1  '1 positional argument'
             1214  STORE_FAST               '_wdxltarget'
           1216_0  COME_FROM          1176  '1176'

 L. 650      1216  LOAD_FAST                'self'
             1218  LOAD_ATTR                survinfo
             1220  STORE_FAST               '_seisinfo'

 L. 652      1222  LOAD_GLOBAL              print
             1224  LOAD_STR                 'UpdateMl15DWdcnn: Step 1 - Get training samples:'
             1226  CALL_FUNCTION_1       1  '1 positional argument'
             1228  POP_TOP          

 L. 653      1230  LOAD_FAST                'self'
             1232  LOAD_ATTR                traindataconfig
             1234  LOAD_STR                 'TrainPointSet'
             1236  BINARY_SUBSCR    
             1238  STORE_FAST               '_trainpoint'

 L. 654      1240  LOAD_GLOBAL              np
             1242  LOAD_METHOD              zeros
             1244  LOAD_CONST               0
             1246  LOAD_CONST               3
             1248  BUILD_LIST_2          2 
             1250  CALL_METHOD_1         1  '1 positional argument'
             1252  STORE_FAST               '_traindata'

 L. 655      1254  SETUP_LOOP         1330  'to 1330'
             1256  LOAD_FAST                '_trainpoint'
             1258  GET_ITER         
           1260_0  COME_FROM          1278  '1278'
             1260  FOR_ITER           1328  'to 1328'
             1262  STORE_FAST               '_p'

 L. 656      1264  LOAD_GLOBAL              point_ays
             1266  LOAD_METHOD              checkPoint
             1268  LOAD_FAST                'self'
             1270  LOAD_ATTR                pointsetdata
             1272  LOAD_FAST                '_p'
             1274  BINARY_SUBSCR    
             1276  CALL_METHOD_1         1  '1 positional argument'
         1278_1280  POP_JUMP_IF_FALSE  1260  'to 1260'

 L. 657      1282  LOAD_GLOBAL              basic_mdt
             1284  LOAD_METHOD              exportMatDict
             1286  LOAD_FAST                'self'
             1288  LOAD_ATTR                pointsetdata
             1290  LOAD_FAST                '_p'
             1292  BINARY_SUBSCR    
             1294  LOAD_STR                 'Inline'
             1296  LOAD_STR                 'Crossline'
             1298  LOAD_STR                 'Z'
             1300  BUILD_LIST_3          3 
             1302  CALL_METHOD_2         2  '2 positional arguments'
             1304  STORE_FAST               '_pt'

 L. 658      1306  LOAD_GLOBAL              np
             1308  LOAD_ATTR                concatenate
             1310  LOAD_FAST                '_traindata'
             1312  LOAD_FAST                '_pt'
             1314  BUILD_TUPLE_2         2 
             1316  LOAD_CONST               0
             1318  LOAD_CONST               ('axis',)
             1320  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1322  STORE_FAST               '_traindata'
         1324_1326  JUMP_BACK          1260  'to 1260'
             1328  POP_BLOCK        
           1330_0  COME_FROM_LOOP     1254  '1254'

 L. 659      1330  LOAD_GLOBAL              seis_ays
             1332  LOAD_ATTR                removeOutofSurveySample
             1334  LOAD_FAST                '_traindata'

 L. 660      1336  LOAD_FAST                '_seisinfo'
             1338  LOAD_STR                 'ILStart'
             1340  BINARY_SUBSCR    
             1342  LOAD_FAST                '_wdinl'
             1344  LOAD_FAST                '_seisinfo'
             1346  LOAD_STR                 'ILStep'
             1348  BINARY_SUBSCR    
             1350  BINARY_MULTIPLY  
             1352  BINARY_ADD       

 L. 661      1354  LOAD_FAST                '_seisinfo'
             1356  LOAD_STR                 'ILEnd'
             1358  BINARY_SUBSCR    
             1360  LOAD_FAST                '_wdinl'
             1362  LOAD_FAST                '_seisinfo'
             1364  LOAD_STR                 'ILStep'
             1366  BINARY_SUBSCR    
             1368  BINARY_MULTIPLY  
             1370  BINARY_SUBTRACT  

 L. 662      1372  LOAD_FAST                '_seisinfo'
             1374  LOAD_STR                 'XLStart'
             1376  BINARY_SUBSCR    
             1378  LOAD_FAST                '_wdxl'
             1380  LOAD_FAST                '_seisinfo'
             1382  LOAD_STR                 'XLStep'
             1384  BINARY_SUBSCR    
             1386  BINARY_MULTIPLY  
             1388  BINARY_ADD       

 L. 663      1390  LOAD_FAST                '_seisinfo'
             1392  LOAD_STR                 'XLEnd'
             1394  BINARY_SUBSCR    
             1396  LOAD_FAST                '_wdxl'
             1398  LOAD_FAST                '_seisinfo'
             1400  LOAD_STR                 'XLStep'
             1402  BINARY_SUBSCR    
             1404  BINARY_MULTIPLY  
             1406  BINARY_SUBTRACT  

 L. 664      1408  LOAD_FAST                '_seisinfo'
             1410  LOAD_STR                 'ZStart'
             1412  BINARY_SUBSCR    
             1414  LOAD_FAST                '_wdz'
             1416  LOAD_FAST                '_seisinfo'
             1418  LOAD_STR                 'ZStep'
             1420  BINARY_SUBSCR    
             1422  BINARY_MULTIPLY  
             1424  BINARY_ADD       

 L. 665      1426  LOAD_FAST                '_seisinfo'
             1428  LOAD_STR                 'ZEnd'
             1430  BINARY_SUBSCR    
             1432  LOAD_FAST                '_wdz'
             1434  LOAD_FAST                '_seisinfo'
             1436  LOAD_STR                 'ZStep'
             1438  BINARY_SUBSCR    
             1440  BINARY_MULTIPLY  
             1442  BINARY_SUBTRACT  
             1444  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1446  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1448  STORE_FAST               '_traindata'

 L. 668      1450  LOAD_GLOBAL              np
             1452  LOAD_METHOD              shape
             1454  LOAD_FAST                '_traindata'
             1456  CALL_METHOD_1         1  '1 positional argument'
             1458  LOAD_CONST               0
             1460  BINARY_SUBSCR    
             1462  LOAD_CONST               0
             1464  COMPARE_OP               <=
         1466_1468  POP_JUMP_IF_FALSE  1506  'to 1506'

 L. 669      1470  LOAD_GLOBAL              vis_msg
             1472  LOAD_ATTR                print
             1474  LOAD_STR                 'ERROR in UpdateMl15DWdcnn: No training sample found'
             1476  LOAD_STR                 'error'
             1478  LOAD_CONST               ('type',)
             1480  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1482  POP_TOP          

 L. 670      1484  LOAD_GLOBAL              QtWidgets
             1486  LOAD_ATTR                QMessageBox
             1488  LOAD_METHOD              critical
             1490  LOAD_FAST                'self'
             1492  LOAD_ATTR                msgbox

 L. 671      1494  LOAD_STR                 'Update 2D-WDCNN'

 L. 672      1496  LOAD_STR                 'No training sample found'
             1498  CALL_METHOD_3         3  '3 positional arguments'
             1500  POP_TOP          

 L. 673      1502  LOAD_CONST               None
             1504  RETURN_VALUE     
           1506_0  COME_FROM          1466  '1466'

 L. 676      1506  LOAD_GLOBAL              print
             1508  LOAD_STR                 'UpdateMl15DWdcnn: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 677      1510  LOAD_FAST                '_image_height'
             1512  LOAD_FAST                '_image_width'
             1514  LOAD_FAST                '_image_height_new'
             1516  LOAD_FAST                '_image_width_new'
             1518  BUILD_TUPLE_4         4 
             1520  BINARY_MODULO    
             1522  CALL_FUNCTION_1       1  '1 positional argument'
             1524  POP_TOP          

 L. 678      1526  BUILD_MAP_0           0 
             1528  STORE_FAST               '_traindict'

 L. 679      1530  SETUP_LOOP         1602  'to 1602'
             1532  LOAD_FAST                '_features'
             1534  GET_ITER         
             1536  FOR_ITER           1600  'to 1600'
             1538  STORE_FAST               'f'

 L. 680      1540  LOAD_FAST                'self'
             1542  LOAD_ATTR                seisdata
             1544  LOAD_FAST                'f'
             1546  BINARY_SUBSCR    
             1548  STORE_FAST               '_seisdata'

 L. 681      1550  LOAD_GLOBAL              seis_ays
             1552  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1554  LOAD_FAST                '_seisdata'
             1556  LOAD_FAST                '_traindata'
             1558  LOAD_FAST                'self'
             1560  LOAD_ATTR                survinfo

 L. 682      1562  LOAD_FAST                '_wdinl'
             1564  LOAD_FAST                '_wdxl'
             1566  LOAD_FAST                '_wdz'

 L. 683      1568  LOAD_CONST               False
             1570  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1572  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1574  LOAD_CONST               None
             1576  LOAD_CONST               None
             1578  BUILD_SLICE_2         2 
             1580  LOAD_CONST               3
             1582  LOAD_CONST               None
             1584  BUILD_SLICE_2         2 
             1586  BUILD_TUPLE_2         2 
             1588  BINARY_SUBSCR    
             1590  LOAD_FAST                '_traindict'
             1592  LOAD_FAST                'f'
             1594  STORE_SUBSCR     
         1596_1598  JUMP_BACK          1536  'to 1536'
             1600  POP_BLOCK        
           1602_0  COME_FROM_LOOP     1530  '1530'

 L. 684      1602  LOAD_FAST                '_target'
             1604  LOAD_FAST                '_features'
             1606  COMPARE_OP               not-in
         1608_1610  POP_JUMP_IF_FALSE  1668  'to 1668'

 L. 685      1612  LOAD_FAST                'self'
             1614  LOAD_ATTR                seisdata
             1616  LOAD_FAST                '_target'
             1618  BINARY_SUBSCR    
             1620  STORE_FAST               '_seisdata'

 L. 686      1622  LOAD_GLOBAL              seis_ays
             1624  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1626  LOAD_FAST                '_seisdata'
             1628  LOAD_FAST                '_traindata'
             1630  LOAD_FAST                'self'
             1632  LOAD_ATTR                survinfo

 L. 687      1634  LOAD_FAST                '_wdinltarget'

 L. 688      1636  LOAD_FAST                '_wdxltarget'

 L. 689      1638  LOAD_FAST                '_wdztarget'

 L. 690      1640  LOAD_CONST               False
             1642  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1644  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1646  LOAD_CONST               None
             1648  LOAD_CONST               None
             1650  BUILD_SLICE_2         2 
             1652  LOAD_CONST               3
             1654  LOAD_CONST               None
             1656  BUILD_SLICE_2         2 
             1658  BUILD_TUPLE_2         2 
             1660  BINARY_SUBSCR    
             1662  LOAD_FAST                '_traindict'
             1664  LOAD_FAST                '_target'
             1666  STORE_SUBSCR     
           1668_0  COME_FROM          1608  '1608'

 L. 691      1668  LOAD_FAST                '_weight'
             1670  LOAD_FAST                '_features'
             1672  COMPARE_OP               not-in
         1674_1676  POP_JUMP_IF_FALSE  1744  'to 1744'
             1678  LOAD_FAST                '_weight'
             1680  LOAD_FAST                '_target'
             1682  COMPARE_OP               !=
         1684_1686  POP_JUMP_IF_FALSE  1744  'to 1744'

 L. 692      1688  LOAD_FAST                'self'
             1690  LOAD_ATTR                seisdata
             1692  LOAD_FAST                '_weight'
             1694  BINARY_SUBSCR    
             1696  STORE_FAST               '_seisdata'

 L. 693      1698  LOAD_GLOBAL              seis_ays
             1700  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1702  LOAD_FAST                '_seisdata'
             1704  LOAD_FAST                '_traindata'
             1706  LOAD_FAST                'self'
             1708  LOAD_ATTR                survinfo

 L. 694      1710  LOAD_FAST                '_wdinltarget'

 L. 695      1712  LOAD_FAST                '_wdxltarget'

 L. 696      1714  LOAD_FAST                '_wdztarget'

 L. 697      1716  LOAD_CONST               False
             1718  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1720  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1722  LOAD_CONST               None
             1724  LOAD_CONST               None
             1726  BUILD_SLICE_2         2 
             1728  LOAD_CONST               3
             1730  LOAD_CONST               None
             1732  BUILD_SLICE_2         2 
             1734  BUILD_TUPLE_2         2 
             1736  BINARY_SUBSCR    
             1738  LOAD_FAST                '_traindict'
             1740  LOAD_FAST                '_weight'
             1742  STORE_SUBSCR     
           1744_0  COME_FROM          1684  '1684'
           1744_1  COME_FROM          1674  '1674'

 L. 699      1744  LOAD_FAST                'self'
             1746  LOAD_ATTR                traindataconfig
             1748  LOAD_STR                 'RemoveInvariantFeature_Checked'
             1750  BINARY_SUBSCR    
         1752_1754  POP_JUMP_IF_FALSE  1836  'to 1836'

 L. 700      1756  SETUP_LOOP         1836  'to 1836'
             1758  LOAD_FAST                '_features'
             1760  GET_ITER         
           1762_0  COME_FROM          1790  '1790'
             1762  FOR_ITER           1834  'to 1834'
             1764  STORE_FAST               'f'

 L. 701      1766  LOAD_GLOBAL              ml_aug
             1768  LOAD_METHOD              removeInvariantFeature
             1770  LOAD_FAST                '_traindict'
             1772  LOAD_FAST                'f'
             1774  CALL_METHOD_2         2  '2 positional arguments'
             1776  STORE_FAST               '_traindict'

 L. 702      1778  LOAD_GLOBAL              basic_mdt
             1780  LOAD_METHOD              maxDictConstantRow
             1782  LOAD_FAST                '_traindict'
             1784  CALL_METHOD_1         1  '1 positional argument'
             1786  LOAD_CONST               0
             1788  COMPARE_OP               <=
         1790_1792  POP_JUMP_IF_FALSE  1762  'to 1762'

 L. 703      1794  LOAD_GLOBAL              vis_msg
             1796  LOAD_ATTR                print
             1798  LOAD_STR                 'ERROR in UpdateMl15DWdcnn: No training sample found'
             1800  LOAD_STR                 'error'
             1802  LOAD_CONST               ('type',)
             1804  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1806  POP_TOP          

 L. 704      1808  LOAD_GLOBAL              QtWidgets
             1810  LOAD_ATTR                QMessageBox
             1812  LOAD_METHOD              critical
             1814  LOAD_FAST                'self'
             1816  LOAD_ATTR                msgbox

 L. 705      1818  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 706      1820  LOAD_STR                 'No training sample found'
             1822  CALL_METHOD_3         3  '3 positional arguments'
             1824  POP_TOP          

 L. 707      1826  LOAD_CONST               None
             1828  RETURN_VALUE     
         1830_1832  JUMP_BACK          1762  'to 1762'
             1834  POP_BLOCK        
           1836_0  COME_FROM_LOOP     1756  '1756'
           1836_1  COME_FROM          1752  '1752'

 L. 709      1836  LOAD_FAST                'self'
             1838  LOAD_ATTR                traindataconfig
             1840  LOAD_STR                 'RemoveZeroWeight_Checked'
             1842  BINARY_SUBSCR    
         1844_1846  POP_JUMP_IF_FALSE  1912  'to 1912'

 L. 710      1848  LOAD_GLOBAL              ml_aug
             1850  LOAD_METHOD              removeZeroWeight
             1852  LOAD_FAST                '_traindict'
             1854  LOAD_FAST                '_weight'
             1856  CALL_METHOD_2         2  '2 positional arguments'
             1858  STORE_FAST               '_traindict'

 L. 711      1860  LOAD_GLOBAL              basic_mdt
             1862  LOAD_METHOD              maxDictConstantRow
             1864  LOAD_FAST                '_traindict'
             1866  CALL_METHOD_1         1  '1 positional argument'
             1868  LOAD_CONST               0
             1870  COMPARE_OP               <=
         1872_1874  POP_JUMP_IF_FALSE  1912  'to 1912'

 L. 712      1876  LOAD_GLOBAL              vis_msg
             1878  LOAD_ATTR                print
             1880  LOAD_STR                 'ERROR in UpdateMl15DWdcnn: No training sample found'
             1882  LOAD_STR                 'error'
             1884  LOAD_CONST               ('type',)
             1886  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1888  POP_TOP          

 L. 713      1890  LOAD_GLOBAL              QtWidgets
             1892  LOAD_ATTR                QMessageBox
             1894  LOAD_METHOD              critical
             1896  LOAD_FAST                'self'
             1898  LOAD_ATTR                msgbox

 L. 714      1900  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 715      1902  LOAD_STR                 'No training sample found'
             1904  CALL_METHOD_3         3  '3 positional arguments'
             1906  POP_TOP          

 L. 716      1908  LOAD_CONST               None
             1910  RETURN_VALUE     
           1912_0  COME_FROM          1872  '1872'
           1912_1  COME_FROM          1844  '1844'

 L. 718      1912  LOAD_GLOBAL              np
             1914  LOAD_METHOD              shape
             1916  LOAD_FAST                '_traindict'
             1918  LOAD_FAST                '_target'
             1920  BINARY_SUBSCR    
             1922  CALL_METHOD_1         1  '1 positional argument'
             1924  LOAD_CONST               0
             1926  BINARY_SUBSCR    
             1928  LOAD_CONST               0
             1930  COMPARE_OP               <=
         1932_1934  POP_JUMP_IF_FALSE  1972  'to 1972'

 L. 719      1936  LOAD_GLOBAL              vis_msg
             1938  LOAD_ATTR                print
             1940  LOAD_STR                 'ERROR in UpdateMl15DWdcnn: No training sample found'
             1942  LOAD_STR                 'error'
             1944  LOAD_CONST               ('type',)
             1946  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1948  POP_TOP          

 L. 720      1950  LOAD_GLOBAL              QtWidgets
             1952  LOAD_ATTR                QMessageBox
             1954  LOAD_METHOD              critical
             1956  LOAD_FAST                'self'
             1958  LOAD_ATTR                msgbox

 L. 721      1960  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 722      1962  LOAD_STR                 'No training sample found'
             1964  CALL_METHOD_3         3  '3 positional arguments'
             1966  POP_TOP          

 L. 723      1968  LOAD_CONST               None
             1970  RETURN_VALUE     
           1972_0  COME_FROM          1932  '1932'

 L. 725      1972  LOAD_FAST                '_image_height_new'
             1974  LOAD_FAST                '_image_height'
             1976  COMPARE_OP               !=
         1978_1980  POP_JUMP_IF_TRUE   1992  'to 1992'
             1982  LOAD_FAST                '_image_width_new'
             1984  LOAD_FAST                '_image_width'
             1986  COMPARE_OP               !=
         1988_1990  POP_JUMP_IF_FALSE  2036  'to 2036'
           1992_0  COME_FROM          1978  '1978'

 L. 726      1992  SETUP_LOOP         2036  'to 2036'
             1994  LOAD_FAST                '_features'
             1996  GET_ITER         
             1998  FOR_ITER           2034  'to 2034'
             2000  STORE_FAST               'f'

 L. 727      2002  LOAD_GLOBAL              basic_image
             2004  LOAD_ATTR                changeImageSize
             2006  LOAD_FAST                '_traindict'
             2008  LOAD_FAST                'f'
             2010  BINARY_SUBSCR    

 L. 728      2012  LOAD_FAST                '_image_height'

 L. 729      2014  LOAD_FAST                '_image_width'

 L. 730      2016  LOAD_FAST                '_image_height_new'

 L. 731      2018  LOAD_FAST                '_image_width_new'
             2020  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2022  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2024  LOAD_FAST                '_traindict'
             2026  LOAD_FAST                'f'
             2028  STORE_SUBSCR     
         2030_2032  JUMP_BACK          1998  'to 1998'
             2034  POP_BLOCK        
           2036_0  COME_FROM_LOOP     1992  '1992'
           2036_1  COME_FROM          1988  '1988'

 L. 732      2036  LOAD_FAST                '_image_height_new'
             2038  LOAD_FAST                '_image_height'
             2040  COMPARE_OP               !=
         2042_2044  POP_JUMP_IF_FALSE  2082  'to 2082'
             2046  LOAD_FAST                '_target'
             2048  LOAD_FAST                '_features'
             2050  COMPARE_OP               not-in
         2052_2054  POP_JUMP_IF_FALSE  2082  'to 2082'

 L. 733      2056  LOAD_GLOBAL              basic_curve
             2058  LOAD_ATTR                changeCurveSize
             2060  LOAD_FAST                '_traindict'
             2062  LOAD_FAST                '_target'
             2064  BINARY_SUBSCR    

 L. 734      2066  LOAD_FAST                '_image_height'

 L. 735      2068  LOAD_FAST                '_image_height_new'
             2070  LOAD_STR                 'linear'
             2072  LOAD_CONST               ('length', 'length_new', 'kind')
             2074  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2076  LOAD_FAST                '_traindict'
             2078  LOAD_FAST                '_target'
             2080  STORE_SUBSCR     
           2082_0  COME_FROM          2052  '2052'
           2082_1  COME_FROM          2042  '2042'

 L. 736      2082  LOAD_FAST                '_image_height_new'
             2084  LOAD_FAST                '_image_height'
             2086  COMPARE_OP               !=
         2088_2090  POP_JUMP_IF_FALSE  2138  'to 2138'
             2092  LOAD_FAST                '_weight'
             2094  LOAD_FAST                '_features'
             2096  COMPARE_OP               not-in
         2098_2100  POP_JUMP_IF_FALSE  2138  'to 2138'
             2102  LOAD_FAST                '_weight'
             2104  LOAD_FAST                '_target'
             2106  COMPARE_OP               !=
         2108_2110  POP_JUMP_IF_FALSE  2138  'to 2138'

 L. 737      2112  LOAD_GLOBAL              basic_curve
             2114  LOAD_ATTR                changeCurveSize
             2116  LOAD_FAST                '_traindict'
             2118  LOAD_FAST                '_weight'
             2120  BINARY_SUBSCR    

 L. 738      2122  LOAD_FAST                '_image_height'

 L. 739      2124  LOAD_FAST                '_image_height_new'
             2126  LOAD_STR                 'linear'
             2128  LOAD_CONST               ('length', 'length_new', 'kind')
             2130  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2132  LOAD_FAST                '_traindict'
             2134  LOAD_FAST                '_weight'
             2136  STORE_SUBSCR     
           2138_0  COME_FROM          2108  '2108'
           2138_1  COME_FROM          2098  '2098'
           2138_2  COME_FROM          2088  '2088'

 L. 740      2138  LOAD_FAST                'self'
             2140  LOAD_ATTR                traindataconfig
             2142  LOAD_STR                 'RotateFeature_Checked'
             2144  BINARY_SUBSCR    
             2146  LOAD_CONST               True
             2148  COMPARE_OP               is
         2150_2152  POP_JUMP_IF_FALSE  2266  'to 2266'

 L. 741      2154  SETUP_LOOP         2192  'to 2192'
             2156  LOAD_FAST                '_features'
             2158  GET_ITER         
             2160  FOR_ITER           2190  'to 2190'
             2162  STORE_FAST               'f'

 L. 742      2164  LOAD_GLOBAL              ml_aug
             2166  LOAD_METHOD              rotateImage4Way
             2168  LOAD_FAST                '_traindict'
             2170  LOAD_FAST                'f'
             2172  BINARY_SUBSCR    
             2174  LOAD_FAST                '_image_height_new'
             2176  LOAD_FAST                '_image_width_new'
             2178  CALL_METHOD_3         3  '3 positional arguments'
             2180  LOAD_FAST                '_traindict'
             2182  LOAD_FAST                'f'
             2184  STORE_SUBSCR     
         2186_2188  JUMP_BACK          2160  'to 2160'
             2190  POP_BLOCK        
           2192_0  COME_FROM_LOOP     2154  '2154'

 L. 743      2192  LOAD_FAST                '_target'
             2194  LOAD_FAST                '_features'
             2196  COMPARE_OP               not-in
         2198_2200  POP_JUMP_IF_FALSE  2224  'to 2224'

 L. 744      2202  LOAD_GLOBAL              ml_aug
             2204  LOAD_METHOD              rotateImage4Way
             2206  LOAD_FAST                '_traindict'
             2208  LOAD_FAST                '_target'
             2210  BINARY_SUBSCR    
             2212  LOAD_FAST                '_image_height_new'
             2214  LOAD_CONST               1
             2216  CALL_METHOD_3         3  '3 positional arguments'
             2218  LOAD_FAST                '_traindict'
             2220  LOAD_FAST                '_target'
             2222  STORE_SUBSCR     
           2224_0  COME_FROM          2198  '2198'

 L. 745      2224  LOAD_FAST                '_weight'
             2226  LOAD_FAST                '_features'
             2228  COMPARE_OP               not-in
         2230_2232  POP_JUMP_IF_FALSE  2266  'to 2266'
             2234  LOAD_FAST                '_weight'
             2236  LOAD_FAST                '_target'
             2238  COMPARE_OP               !=
         2240_2242  POP_JUMP_IF_FALSE  2266  'to 2266'

 L. 746      2244  LOAD_GLOBAL              ml_aug
             2246  LOAD_METHOD              rotateImage4Way
             2248  LOAD_FAST                '_traindict'
             2250  LOAD_FAST                '_weight'
             2252  BINARY_SUBSCR    
             2254  LOAD_FAST                '_image_height_new'
             2256  LOAD_CONST               1
             2258  CALL_METHOD_3         3  '3 positional arguments'
             2260  LOAD_FAST                '_traindict'
             2262  LOAD_FAST                '_weight'
             2264  STORE_SUBSCR     
           2266_0  COME_FROM          2240  '2240'
           2266_1  COME_FROM          2230  '2230'
           2266_2  COME_FROM          2150  '2150'

 L. 748      2266  LOAD_GLOBAL              np
             2268  LOAD_METHOD              round
             2270  LOAD_FAST                '_traindict'
             2272  LOAD_FAST                '_target'
             2274  BINARY_SUBSCR    
             2276  CALL_METHOD_1         1  '1 positional argument'
             2278  LOAD_METHOD              astype
             2280  LOAD_GLOBAL              int
             2282  CALL_METHOD_1         1  '1 positional argument'
             2284  LOAD_FAST                '_traindict'
             2286  LOAD_FAST                '_target'
             2288  STORE_SUBSCR     

 L. 751      2290  LOAD_GLOBAL              print
             2292  LOAD_STR                 'UpdateMl15DWdcnn: A total of %d valid training samples'
             2294  LOAD_GLOBAL              basic_mdt
             2296  LOAD_METHOD              maxDictConstantRow
             2298  LOAD_FAST                '_traindict'
             2300  CALL_METHOD_1         1  '1 positional argument'
             2302  BINARY_MODULO    
             2304  CALL_FUNCTION_1       1  '1 positional argument'
             2306  POP_TOP          

 L. 753      2308  LOAD_GLOBAL              print
             2310  LOAD_STR                 'UpdateMl15DWdcnn: Step 3 - Start training'
             2312  CALL_FUNCTION_1       1  '1 positional argument'
             2314  POP_TOP          

 L. 755      2316  LOAD_GLOBAL              QtWidgets
             2318  LOAD_METHOD              QProgressDialog
             2320  CALL_METHOD_0         0  '0 positional arguments'
             2322  STORE_FAST               '_pgsdlg'

 L. 756      2324  LOAD_GLOBAL              QtGui
             2326  LOAD_METHOD              QIcon
             2328  CALL_METHOD_0         0  '0 positional arguments'
             2330  STORE_FAST               'icon'

 L. 757      2332  LOAD_FAST                'icon'
             2334  LOAD_METHOD              addPixmap
             2336  LOAD_GLOBAL              QtGui
             2338  LOAD_METHOD              QPixmap
             2340  LOAD_GLOBAL              os
             2342  LOAD_ATTR                path
             2344  LOAD_METHOD              join
             2346  LOAD_FAST                'self'
             2348  LOAD_ATTR                iconpath
             2350  LOAD_STR                 'icons/update.png'
             2352  CALL_METHOD_2         2  '2 positional arguments'
             2354  CALL_METHOD_1         1  '1 positional argument'

 L. 758      2356  LOAD_GLOBAL              QtGui
             2358  LOAD_ATTR                QIcon
             2360  LOAD_ATTR                Normal
             2362  LOAD_GLOBAL              QtGui
             2364  LOAD_ATTR                QIcon
             2366  LOAD_ATTR                Off
             2368  CALL_METHOD_3         3  '3 positional arguments'
             2370  POP_TOP          

 L. 759      2372  LOAD_FAST                '_pgsdlg'
             2374  LOAD_METHOD              setWindowIcon
             2376  LOAD_FAST                'icon'
             2378  CALL_METHOD_1         1  '1 positional argument'
             2380  POP_TOP          

 L. 760      2382  LOAD_FAST                '_pgsdlg'
             2384  LOAD_METHOD              setWindowTitle
             2386  LOAD_STR                 'Update 2D-DCNN'
             2388  CALL_METHOD_1         1  '1 positional argument'
             2390  POP_TOP          

 L. 761      2392  LOAD_FAST                '_pgsdlg'
             2394  LOAD_METHOD              setCancelButton
             2396  LOAD_CONST               None
             2398  CALL_METHOD_1         1  '1 positional argument'
             2400  POP_TOP          

 L. 762      2402  LOAD_FAST                '_pgsdlg'
             2404  LOAD_METHOD              setWindowFlags
             2406  LOAD_GLOBAL              QtCore
             2408  LOAD_ATTR                Qt
             2410  LOAD_ATTR                WindowStaysOnTopHint
             2412  CALL_METHOD_1         1  '1 positional argument'
             2414  POP_TOP          

 L. 763      2416  LOAD_FAST                '_pgsdlg'
             2418  LOAD_METHOD              forceShow
             2420  CALL_METHOD_0         0  '0 positional arguments'
             2422  POP_TOP          

 L. 764      2424  LOAD_FAST                '_pgsdlg'
             2426  LOAD_METHOD              setFixedWidth
             2428  LOAD_CONST               400
             2430  CALL_METHOD_1         1  '1 positional argument'
             2432  POP_TOP          

 L. 765      2434  LOAD_GLOBAL              ml_wdcnn15d
             2436  LOAD_ATTR                update15DWDCNNSegmentor
             2438  LOAD_FAST                '_traindict'

 L. 766      2440  LOAD_FAST                '_image_height_new'
             2442  LOAD_FAST                '_image_width_new'

 L. 767      2444  LOAD_FAST                '_nepoch'
             2446  LOAD_FAST                '_batchsize'

 L. 768      2448  LOAD_FAST                '_learning_rate'

 L. 769      2450  LOAD_FAST                '_dropout_prob'

 L. 770      2452  LOAD_FAST                'self'
             2454  LOAD_ATTR                modelpath
             2456  LOAD_FAST                'self'
             2458  LOAD_ATTR                modelname

 L. 771      2460  LOAD_CONST               True

 L. 772      2462  LOAD_FAST                '_savepath'
             2464  LOAD_FAST                '_savename'

 L. 773      2466  LOAD_FAST                '_pgsdlg'
             2468  LOAD_CONST               ('imageheight', 'imagewidth', 'nepoch', 'batchsize', 'learningrate', 'dropoutprob', 'wdcnnpath', 'wdcnnname', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2470  CALL_FUNCTION_KW_13    13  '13 total positional and keyword args'
             2472  STORE_FAST               '_dccnlog'

 L. 776      2474  LOAD_GLOBAL              QtWidgets
             2476  LOAD_ATTR                QMessageBox
             2478  LOAD_METHOD              information
             2480  LOAD_FAST                'self'
             2482  LOAD_ATTR                msgbox

 L. 777      2484  LOAD_STR                 'Update 1.5D-WDCNN'

 L. 778      2486  LOAD_STR                 'WDCNN updated successfully'
             2488  CALL_METHOD_3         3  '3 positional arguments'
             2490  POP_TOP          

 L. 780      2492  LOAD_GLOBAL              QtWidgets
             2494  LOAD_ATTR                QMessageBox
             2496  LOAD_METHOD              question
             2498  LOAD_FAST                'self'
             2500  LOAD_ATTR                msgbox
             2502  LOAD_STR                 'Update 1.5D-WDCNN'
             2504  LOAD_STR                 'View learning matrix?'

 L. 781      2506  LOAD_GLOBAL              QtWidgets
             2508  LOAD_ATTR                QMessageBox
             2510  LOAD_ATTR                Yes
             2512  LOAD_GLOBAL              QtWidgets
             2514  LOAD_ATTR                QMessageBox
             2516  LOAD_ATTR                No
             2518  BINARY_OR        

 L. 782      2520  LOAD_GLOBAL              QtWidgets
             2522  LOAD_ATTR                QMessageBox
             2524  LOAD_ATTR                Yes
             2526  CALL_METHOD_5         5  '5 positional arguments'
             2528  STORE_FAST               'reply'

 L. 784      2530  LOAD_FAST                'reply'
             2532  LOAD_GLOBAL              QtWidgets
             2534  LOAD_ATTR                QMessageBox
             2536  LOAD_ATTR                Yes
             2538  COMPARE_OP               ==
         2540_2542  POP_JUMP_IF_FALSE  2610  'to 2610'

 L. 785      2544  LOAD_GLOBAL              QtWidgets
             2546  LOAD_METHOD              QDialog
             2548  CALL_METHOD_0         0  '0 positional arguments'
             2550  STORE_FAST               '_viewmllearnmat'

 L. 786      2552  LOAD_GLOBAL              gui_viewmllearnmat
             2554  CALL_FUNCTION_0       0  '0 positional arguments'
             2556  STORE_FAST               '_gui'

 L. 787      2558  LOAD_FAST                '_dccnlog'
             2560  LOAD_STR                 'learning_curve'
             2562  BINARY_SUBSCR    
             2564  LOAD_FAST                '_gui'
             2566  STORE_ATTR               learnmat

 L. 788      2568  LOAD_FAST                'self'
             2570  LOAD_ATTR                linestyle
             2572  LOAD_FAST                '_gui'
             2574  STORE_ATTR               linestyle

 L. 789      2576  LOAD_FAST                'self'
             2578  LOAD_ATTR                fontstyle
             2580  LOAD_FAST                '_gui'
             2582  STORE_ATTR               fontstyle

 L. 790      2584  LOAD_FAST                '_gui'
             2586  LOAD_METHOD              setupGUI
             2588  LOAD_FAST                '_viewmllearnmat'
             2590  CALL_METHOD_1         1  '1 positional argument'
             2592  POP_TOP          

 L. 791      2594  LOAD_FAST                '_viewmllearnmat'
             2596  LOAD_METHOD              exec
             2598  CALL_METHOD_0         0  '0 positional arguments'
             2600  POP_TOP          

 L. 792      2602  LOAD_FAST                '_viewmllearnmat'
             2604  LOAD_METHOD              show
             2606  CALL_METHOD_0         0  '0 positional arguments'
             2608  POP_TOP          
           2610_0  COME_FROM          2540  '2540'

Parse error at or near `POP_TOP' instruction at offset 2608

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
    UpdateMl15DWdcnn = QtWidgets.QWidget()
    gui = updateml15dwdcnn()
    gui.setupGUI(UpdateMl15DWdcnn)
    UpdateMl15DWdcnn.show()
    sys.exit(app.exec_())