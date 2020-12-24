# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\updateml15ddcnn.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 42297 bytes
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
import cognitivegeo.src.ml.dcnnsegmentor15d as ml_dcnn15d
import cognitivegeo.src.gui.viewml15ddcnn as gui_viewml15ddcnn
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class updateml15ddcnn(object):
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

    def setupGUI(self, UpdateMl15DDcnn):
        UpdateMl15DDcnn.setObjectName('UpdateMl15DDcnn')
        UpdateMl15DDcnn.setFixedSize(810, 550)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UpdateMl15DDcnn.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(UpdateMl15DDcnn)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(UpdateMl15DDcnn)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(UpdateMl15DDcnn)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 230, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 230, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 230, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 270, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 270, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 230, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lbltarget = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 320, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(UpdateMl15DDcnn)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 320, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(UpdateMl15DDcnn)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(UpdateMl15DDcnn)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 210))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(UpdateMl15DDcnn)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 210))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 360, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 360, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 400, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 400, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 360, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 360, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 360, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 400, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 400, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(UpdateMl15DDcnn)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 370, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 370, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 410, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 410, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 410, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 410, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 450, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 450, 40, 30))
        self.lbldropout = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 450, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 450, 40, 30))
        self.lblsave = QtWidgets.QLabel(UpdateMl15DDcnn)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 500, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(UpdateMl15DDcnn)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 500, 180, 30))
        self.btnsave = QtWidgets.QPushButton(UpdateMl15DDcnn)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 500, 60, 30))
        self.btnapply = QtWidgets.QPushButton(UpdateMl15DDcnn)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 500, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(UpdateMl15DDcnn)
        self.msgbox.setObjectName('msgbox')
        _center_x = UpdateMl15DDcnn.geometry().center().x()
        _center_y = UpdateMl15DDcnn.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(UpdateMl15DDcnn)
        QtCore.QMetaObject.connectSlotsByName(UpdateMl15DDcnn)

    def retranslateGUI(self, UpdateMl15DDcnn):
        self.dialog = UpdateMl15DDcnn
        _translate = QtCore.QCoreApplication.translate
        UpdateMl15DDcnn.setWindowTitle(_translate('UpdateMl15DDcnn', 'Update 1.5D-DCNN'))
        self.lblfrom.setText(_translate('UpdateMl15DDcnn', 'Select network:'))
        self.ldtfrom.setText(_translate('UpdateMl15DDcnn', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('UpdateMl15DDcnn', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('UpdateMl15DDcnn', 'Training features:'))
        self.lblornt.setText(_translate('UpdateMl15DDcnn', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('UpdateMl15DDcnn', 'Training target:'))
        self.btnconfigtraindata.setText(_translate('TrainMl2DDcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('UpdateMl15DDcnn', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('UpdateMl15DDcnn', 'height='))
        self.ldtoldheight.setText(_translate('UpdateMl15DDcnn', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('UpdateMl15DDcnn', 'width='))
        self.ldtoldwidth.setText(_translate('UpdateMl15DDcnn', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('UpdateMl15DDcnn', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('UpdateMl15DDcnn', 'height='))
        self.ldtnewheight.setText(_translate('UpdateMl15DDcnn', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('UpdateMl15DDcnn', 'width='))
        self.ldtnewwidth.setText(_translate('UpdateMl15DDcnn', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('UpdateMl15DDcnn', 'Pre-trained DCNN architecture:'))
        self.btnviewnetwork.setText(_translate('UpdateMl15DDcnn', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('UpdateMl15DDcnn', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('UpdateMl15DDcnn', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('UpdateMl15DDcnn', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('UpdateMl15DDcnn', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('UpdateMl15DDcnn', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('UpdateMl15DDcnn', 'height='))
        self.ldtmaskheight.setText(_translate('UpdateMl15DDcnn', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('UpdateMl15DDcnn', 'width='))
        self.ldtmaskwidth.setText(_translate('UpdateMl15DDcnn', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('UpdateMl15DDcnn', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('UpdateMl15DDcnn', 'height='))
        self.ldtpoolheight.setText(_translate('UpdateMl15DDcnn', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('UpdateMl15DDcnn', 'width='))
        self.ldtpoolwidth.setText(_translate('UpdateMl15DDcnn', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('UpdateMl15DDcnn', 'Specify update parameters:'))
        self.lblnepoch.setText(_translate('UpdateMl15DDcnn', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('UpdateMl15DDcnn', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('UpdateMl15DDcnn', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('UpdateMl15DDcnn', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('UpdateMl15DDcnn', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('UpdateMl15DDcnn', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('UpdateMl15DDcnn', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('UpdateMl15DDcnn', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('UpdateMl15DDcnn', 'Save new-DCNN to:'))
        self.ldtsave.setText(_translate('UpdateMl15DDcnn', ''))
        self.btnsave.setText(_translate('UpdateMl15DDcnn', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('UpdateMl15DDcnn', 'Update 1.5D-DCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnUpdateMl15DDcnn)

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.check15DDCNNModel(self.modelpath, self.modelname) is True:
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
            self.btnviewnetwork.setEnabled(False)
            self.ldtnconvblock.setText('')
            self.ldtn1x1layer.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')

    def clickBtnFrom(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select DCNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def clickBtnViewNetwork(self):
        _viewmldcnn = QtWidgets.QDialog()
        _gui = gui_viewml15ddcnn()
        _gui.linestyle = self.linestyle
        _gui.maskstyle = self.maskstyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewmldcnn)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewmldcnn.exec()
        _viewmldcnn.show()

    def changeLdtNconvblock(self):
        if ml_tfm.check15DDCNNModel(self.modelpath, self.modelname) is True:
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
        if ml_tfm.check15DDCNNModel(self.modelpath, self.modelname) is True:
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
        _file = _dialog.getSaveFileName(None, 'Save DCNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
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

    def clickBtnUpdateMl15DDcnn--- This code section failed: ---

 L. 515         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 517         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 518        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in UpdateMl15DDcnn: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 519        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 520        44  LOAD_STR                 'Update 1.5D-DCNN'

 L. 521        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 522        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 524        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              check15DDCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 525        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in UpdateMl15DDcnn: No pre-DCNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 526        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 527       100  LOAD_STR                 'Update 1.5D-DCNN'

 L. 528       102  LOAD_STR                 'No pre-DCNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 529       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 531       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 532       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 533       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in UpdateMl15DDcnn: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    

 L. 534       152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 535       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 536       170  LOAD_STR                 'Update 1.5D-DCNN'

 L. 537       172  LOAD_STR                 "Feature '"
              174  LOAD_FAST                'f'
              176  BINARY_ADD       
              178  LOAD_STR                 "' not found in seismic data"
              180  BINARY_ADD       
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L. 538       186  LOAD_CONST               None
              188  RETURN_VALUE     
              190  JUMP_BACK           124  'to 124'
              192  POP_BLOCK        
            194_0  COME_FROM_LOOP      112  '112'

 L. 540       194  LOAD_GLOBAL              basic_data
              196  LOAD_METHOD              str2int
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                ldtoldheight
              202  LOAD_METHOD              text
              204  CALL_METHOD_0         0  '0 positional arguments'
              206  CALL_METHOD_1         1  '1 positional argument'
              208  STORE_FAST               '_image_height'

 L. 541       210  LOAD_GLOBAL              basic_data
              212  LOAD_METHOD              str2int
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                ldtoldwidth
              218  LOAD_METHOD              text
              220  CALL_METHOD_0         0  '0 positional arguments'
              222  CALL_METHOD_1         1  '1 positional argument'
              224  STORE_FAST               '_image_width'

 L. 542       226  LOAD_GLOBAL              basic_data
              228  LOAD_METHOD              str2int
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                ldtnewheight
              234  LOAD_METHOD              text
              236  CALL_METHOD_0         0  '0 positional arguments'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  STORE_FAST               '_image_height_new'

 L. 543       242  LOAD_GLOBAL              basic_data
              244  LOAD_METHOD              str2int
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                ldtnewwidth
              250  LOAD_METHOD              text
              252  CALL_METHOD_0         0  '0 positional arguments'
              254  CALL_METHOD_1         1  '1 positional argument'
              256  STORE_FAST               '_image_width_new'

 L. 544       258  LOAD_FAST                '_image_height'
              260  LOAD_CONST               False
              262  COMPARE_OP               is
          264_266  POP_JUMP_IF_TRUE    298  'to 298'
              268  LOAD_FAST                '_image_width'
              270  LOAD_CONST               False
              272  COMPARE_OP               is
          274_276  POP_JUMP_IF_TRUE    298  'to 298'

 L. 545       278  LOAD_FAST                '_image_height_new'
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

 L. 546       298  LOAD_GLOBAL              vis_msg
              300  LOAD_ATTR                print
              302  LOAD_STR                 'ERROR in UpdateMl15DDcnn: Non-integer feature size'
              304  LOAD_STR                 'error'
              306  LOAD_CONST               ('type',)
              308  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              310  POP_TOP          

 L. 547       312  LOAD_GLOBAL              QtWidgets
              314  LOAD_ATTR                QMessageBox
              316  LOAD_METHOD              critical
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                msgbox

 L. 548       322  LOAD_STR                 'Update 1.5D-DCNN'

 L. 549       324  LOAD_STR                 'Non-integer feature size'
              326  CALL_METHOD_3         3  '3 positional arguments'
              328  POP_TOP          

 L. 550       330  LOAD_CONST               None
              332  RETURN_VALUE     
            334_0  COME_FROM           294  '294'

 L. 551       334  LOAD_FAST                '_image_height'
              336  LOAD_CONST               2
              338  COMPARE_OP               <
          340_342  POP_JUMP_IF_TRUE    374  'to 374'
              344  LOAD_FAST                '_image_width'
              346  LOAD_CONST               2
              348  COMPARE_OP               <
          350_352  POP_JUMP_IF_TRUE    374  'to 374'

 L. 552       354  LOAD_FAST                '_image_height_new'
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

 L. 553       374  LOAD_GLOBAL              vis_msg
              376  LOAD_ATTR                print
              378  LOAD_STR                 'ERROR in UpdateMl15DDcnn: Features are not 2D'
              380  LOAD_STR                 'error'
              382  LOAD_CONST               ('type',)
              384  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              386  POP_TOP          

 L. 554       388  LOAD_GLOBAL              QtWidgets
              390  LOAD_ATTR                QMessageBox
              392  LOAD_METHOD              critical
              394  LOAD_FAST                'self'
              396  LOAD_ATTR                msgbox

 L. 555       398  LOAD_STR                 'Update 1.5D-DCNN'

 L. 556       400  LOAD_STR                 'Features are not 2D'
              402  CALL_METHOD_3         3  '3 positional arguments'
              404  POP_TOP          

 L. 557       406  LOAD_CONST               None
              408  RETURN_VALUE     
            410_0  COME_FROM           370  '370'

 L. 559       410  LOAD_CONST               2
              412  LOAD_GLOBAL              int
              414  LOAD_FAST                '_image_height'
              416  LOAD_CONST               2
              418  BINARY_TRUE_DIVIDE
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  BINARY_MULTIPLY  
              424  LOAD_CONST               1
              426  BINARY_ADD       
              428  STORE_FAST               '_image_height'

 L. 560       430  LOAD_CONST               2
              432  LOAD_GLOBAL              int
              434  LOAD_FAST                '_image_width'
              436  LOAD_CONST               2
              438  BINARY_TRUE_DIVIDE
              440  CALL_FUNCTION_1       1  '1 positional argument'
              442  BINARY_MULTIPLY  
              444  LOAD_CONST               1
              446  BINARY_ADD       
              448  STORE_FAST               '_image_width'

 L. 562       450  LOAD_FAST                'self'
              452  LOAD_ATTR                modelinfo
              454  LOAD_STR                 'target'
              456  BINARY_SUBSCR    
              458  LOAD_FAST                'self'
              460  LOAD_ATTR                seisdata
              462  LOAD_METHOD              keys
              464  CALL_METHOD_0         0  '0 positional arguments'
              466  COMPARE_OP               not-in
          468_470  POP_JUMP_IF_FALSE   532  'to 532'

 L. 563       472  LOAD_GLOBAL              vis_msg
              474  LOAD_ATTR                print
              476  LOAD_STR                 "ERROR in UpdateMl15DDcnn: Target label '%s' not found in seismic data"

 L. 564       478  LOAD_FAST                'self'
              480  LOAD_ATTR                modelinfo
              482  LOAD_STR                 'target'
              484  BINARY_SUBSCR    
              486  BINARY_MODULO    
              488  LOAD_STR                 'error'
              490  LOAD_CONST               ('type',)
              492  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              494  POP_TOP          

 L. 565       496  LOAD_GLOBAL              QtWidgets
              498  LOAD_ATTR                QMessageBox
              500  LOAD_METHOD              critical
              502  LOAD_FAST                'self'
              504  LOAD_ATTR                msgbox

 L. 566       506  LOAD_STR                 'Update 1.5D-DCNN'

 L. 567       508  LOAD_STR                 "Target label '"
              510  LOAD_FAST                'self'
              512  LOAD_ATTR                modelinfo
              514  LOAD_STR                 'target'
              516  BINARY_SUBSCR    
              518  BINARY_ADD       
              520  LOAD_STR                 ' not found in seismic data'
              522  BINARY_ADD       
              524  CALL_METHOD_3         3  '3 positional arguments'
              526  POP_TOP          

 L. 568       528  LOAD_CONST               None
              530  RETURN_VALUE     
            532_0  COME_FROM           468  '468'

 L. 570       532  LOAD_FAST                'self'
              534  LOAD_ATTR                modelinfo
              536  LOAD_STR                 'feature_list'
              538  BINARY_SUBSCR    
              540  STORE_FAST               '_features'

 L. 571       542  LOAD_FAST                'self'
              544  LOAD_ATTR                modelinfo
              546  LOAD_STR                 'target'
              548  BINARY_SUBSCR    
              550  STORE_FAST               '_target'

 L. 573       552  LOAD_GLOBAL              basic_data
              554  LOAD_METHOD              str2int
              556  LOAD_FAST                'self'
              558  LOAD_ATTR                ldtnepoch
              560  LOAD_METHOD              text
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  CALL_METHOD_1         1  '1 positional argument'
              566  STORE_FAST               '_nepoch'

 L. 574       568  LOAD_GLOBAL              basic_data
              570  LOAD_METHOD              str2int
              572  LOAD_FAST                'self'
              574  LOAD_ATTR                ldtbatchsize
              576  LOAD_METHOD              text
              578  CALL_METHOD_0         0  '0 positional arguments'
              580  CALL_METHOD_1         1  '1 positional argument'
              582  STORE_FAST               '_batchsize'

 L. 575       584  LOAD_GLOBAL              basic_data
              586  LOAD_METHOD              str2float
              588  LOAD_FAST                'self'
              590  LOAD_ATTR                ldtlearnrate
              592  LOAD_METHOD              text
              594  CALL_METHOD_0         0  '0 positional arguments'
              596  CALL_METHOD_1         1  '1 positional argument'
              598  STORE_FAST               '_learning_rate'

 L. 576       600  LOAD_GLOBAL              basic_data
              602  LOAD_METHOD              str2float
              604  LOAD_FAST                'self'
              606  LOAD_ATTR                ldtdropout
              608  LOAD_METHOD              text
              610  CALL_METHOD_0         0  '0 positional arguments'
              612  CALL_METHOD_1         1  '1 positional argument'
              614  STORE_FAST               '_dropout_prob'

 L. 577       616  LOAD_FAST                '_nepoch'
              618  LOAD_CONST               False
              620  COMPARE_OP               is
          622_624  POP_JUMP_IF_TRUE    636  'to 636'
              626  LOAD_FAST                '_nepoch'
              628  LOAD_CONST               0
              630  COMPARE_OP               <=
          632_634  POP_JUMP_IF_FALSE   672  'to 672'
            636_0  COME_FROM           622  '622'

 L. 578       636  LOAD_GLOBAL              vis_msg
              638  LOAD_ATTR                print
              640  LOAD_STR                 'ERROR in UpdateMl15DDcnn: Non-positive epoch number'
              642  LOAD_STR                 'error'
              644  LOAD_CONST               ('type',)
              646  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              648  POP_TOP          

 L. 579       650  LOAD_GLOBAL              QtWidgets
              652  LOAD_ATTR                QMessageBox
              654  LOAD_METHOD              critical
              656  LOAD_FAST                'self'
              658  LOAD_ATTR                msgbox

 L. 580       660  LOAD_STR                 'Update 1.5D-DCNN'

 L. 581       662  LOAD_STR                 'Non-positive epoch number'
              664  CALL_METHOD_3         3  '3 positional arguments'
              666  POP_TOP          

 L. 582       668  LOAD_CONST               None
              670  RETURN_VALUE     
            672_0  COME_FROM           632  '632'

 L. 583       672  LOAD_FAST                '_batchsize'
              674  LOAD_CONST               False
              676  COMPARE_OP               is
          678_680  POP_JUMP_IF_TRUE    692  'to 692'
              682  LOAD_FAST                '_batchsize'
              684  LOAD_CONST               0
              686  COMPARE_OP               <=
          688_690  POP_JUMP_IF_FALSE   728  'to 728'
            692_0  COME_FROM           678  '678'

 L. 584       692  LOAD_GLOBAL              vis_msg
              694  LOAD_ATTR                print
              696  LOAD_STR                 'ERROR in UpdateMl15DDcnn: Non-positive batch size'
              698  LOAD_STR                 'error'
              700  LOAD_CONST               ('type',)
              702  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              704  POP_TOP          

 L. 585       706  LOAD_GLOBAL              QtWidgets
              708  LOAD_ATTR                QMessageBox
              710  LOAD_METHOD              critical
              712  LOAD_FAST                'self'
              714  LOAD_ATTR                msgbox

 L. 586       716  LOAD_STR                 'Update 1.5D-DCNN'

 L. 587       718  LOAD_STR                 'Non-positive batch size'
              720  CALL_METHOD_3         3  '3 positional arguments'
              722  POP_TOP          

 L. 588       724  LOAD_CONST               None
              726  RETURN_VALUE     
            728_0  COME_FROM           688  '688'

 L. 589       728  LOAD_FAST                '_learning_rate'
              730  LOAD_CONST               False
              732  COMPARE_OP               is
          734_736  POP_JUMP_IF_TRUE    748  'to 748'
              738  LOAD_FAST                '_learning_rate'
              740  LOAD_CONST               0
              742  COMPARE_OP               <=
          744_746  POP_JUMP_IF_FALSE   784  'to 784'
            748_0  COME_FROM           734  '734'

 L. 590       748  LOAD_GLOBAL              vis_msg
              750  LOAD_ATTR                print
              752  LOAD_STR                 'ERROR in UpdateMl15DDcnn: Non-positive learning rate'
              754  LOAD_STR                 'error'
              756  LOAD_CONST               ('type',)
              758  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              760  POP_TOP          

 L. 591       762  LOAD_GLOBAL              QtWidgets
              764  LOAD_ATTR                QMessageBox
              766  LOAD_METHOD              critical
              768  LOAD_FAST                'self'
              770  LOAD_ATTR                msgbox

 L. 592       772  LOAD_STR                 'Update 1.5D-DCNN'

 L. 593       774  LOAD_STR                 'Non-positive learning rate'
              776  CALL_METHOD_3         3  '3 positional arguments'
              778  POP_TOP          

 L. 594       780  LOAD_CONST               None
              782  RETURN_VALUE     
            784_0  COME_FROM           744  '744'

 L. 595       784  LOAD_FAST                '_dropout_prob'
              786  LOAD_CONST               False
              788  COMPARE_OP               is
          790_792  POP_JUMP_IF_TRUE    804  'to 804'
              794  LOAD_FAST                '_dropout_prob'
              796  LOAD_CONST               0
              798  COMPARE_OP               <=
          800_802  POP_JUMP_IF_FALSE   840  'to 840'
            804_0  COME_FROM           790  '790'

 L. 596       804  LOAD_GLOBAL              vis_msg
              806  LOAD_ATTR                print
              808  LOAD_STR                 'ERROR in UpdateMl15DDcnn: Negative dropout rate'
              810  LOAD_STR                 'error'
              812  LOAD_CONST               ('type',)
              814  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              816  POP_TOP          

 L. 597       818  LOAD_GLOBAL              QtWidgets
              820  LOAD_ATTR                QMessageBox
              822  LOAD_METHOD              critical
              824  LOAD_FAST                'self'
              826  LOAD_ATTR                msgbox

 L. 598       828  LOAD_STR                 'Update 1.5D-DCNN'

 L. 599       830  LOAD_STR                 'Negative dropout rate'
              832  CALL_METHOD_3         3  '3 positional arguments'
              834  POP_TOP          

 L. 600       836  LOAD_CONST               None
              838  RETURN_VALUE     
            840_0  COME_FROM           800  '800'

 L. 602       840  LOAD_GLOBAL              len
              842  LOAD_FAST                'self'
              844  LOAD_ATTR                ldtsave
              846  LOAD_METHOD              text
              848  CALL_METHOD_0         0  '0 positional arguments'
              850  CALL_FUNCTION_1       1  '1 positional argument'
              852  LOAD_CONST               1
              854  COMPARE_OP               <
          856_858  POP_JUMP_IF_FALSE   896  'to 896'

 L. 603       860  LOAD_GLOBAL              vis_msg
              862  LOAD_ATTR                print
              864  LOAD_STR                 'ERROR in UpdateMl15DDcnn: No name specified for DCNN network'
              866  LOAD_STR                 'error'
              868  LOAD_CONST               ('type',)
              870  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              872  POP_TOP          

 L. 604       874  LOAD_GLOBAL              QtWidgets
              876  LOAD_ATTR                QMessageBox
              878  LOAD_METHOD              critical
              880  LOAD_FAST                'self'
              882  LOAD_ATTR                msgbox

 L. 605       884  LOAD_STR                 'Update 1.5D-DCNN'

 L. 606       886  LOAD_STR                 'No name specified for DCNN network'
              888  CALL_METHOD_3         3  '3 positional arguments'
              890  POP_TOP          

 L. 607       892  LOAD_CONST               None
              894  RETURN_VALUE     
            896_0  COME_FROM           856  '856'

 L. 608       896  LOAD_GLOBAL              os
              898  LOAD_ATTR                path
              900  LOAD_METHOD              dirname
              902  LOAD_FAST                'self'
              904  LOAD_ATTR                ldtsave
              906  LOAD_METHOD              text
              908  CALL_METHOD_0         0  '0 positional arguments'
              910  CALL_METHOD_1         1  '1 positional argument'
              912  STORE_FAST               '_savepath'

 L. 609       914  LOAD_GLOBAL              os
              916  LOAD_ATTR                path
              918  LOAD_METHOD              splitext
              920  LOAD_GLOBAL              os
              922  LOAD_ATTR                path
              924  LOAD_METHOD              basename
              926  LOAD_FAST                'self'
              928  LOAD_ATTR                ldtsave
              930  LOAD_METHOD              text
              932  CALL_METHOD_0         0  '0 positional arguments'
              934  CALL_METHOD_1         1  '1 positional argument'
              936  CALL_METHOD_1         1  '1 positional argument'
              938  LOAD_CONST               0
              940  BINARY_SUBSCR    
              942  STORE_FAST               '_savename'

 L. 611       944  LOAD_CONST               0
              946  STORE_FAST               '_wdinl'

 L. 612       948  LOAD_CONST               0
              950  STORE_FAST               '_wdxl'

 L. 613       952  LOAD_CONST               0
              954  STORE_FAST               '_wdz'

 L. 614       956  LOAD_CONST               0
              958  STORE_FAST               '_wdinltarget'

 L. 615       960  LOAD_CONST               0
              962  STORE_FAST               '_wdxltarget'

 L. 616       964  LOAD_CONST               0
              966  STORE_FAST               '_wdztarget'

 L. 617       968  LOAD_FAST                'self'
              970  LOAD_ATTR                cbbornt
              972  LOAD_METHOD              currentIndex
              974  CALL_METHOD_0         0  '0 positional arguments'
              976  LOAD_CONST               0
              978  COMPARE_OP               ==
          980_982  POP_JUMP_IF_FALSE  1020  'to 1020'

 L. 618       984  LOAD_GLOBAL              int
              986  LOAD_FAST                '_image_width'
              988  LOAD_CONST               2
              990  BINARY_TRUE_DIVIDE
              992  CALL_FUNCTION_1       1  '1 positional argument'
              994  STORE_FAST               '_wdxl'

 L. 619       996  LOAD_GLOBAL              int
              998  LOAD_FAST                '_image_height'
             1000  LOAD_CONST               2
             1002  BINARY_TRUE_DIVIDE
             1004  CALL_FUNCTION_1       1  '1 positional argument'
             1006  STORE_FAST               '_wdz'

 L. 620      1008  LOAD_GLOBAL              int
             1010  LOAD_FAST                '_image_height'
             1012  LOAD_CONST               2
             1014  BINARY_TRUE_DIVIDE
             1016  CALL_FUNCTION_1       1  '1 positional argument'
             1018  STORE_FAST               '_wdztarget'
           1020_0  COME_FROM           980  '980'

 L. 621      1020  LOAD_FAST                'self'
             1022  LOAD_ATTR                cbbornt
             1024  LOAD_METHOD              currentIndex
             1026  CALL_METHOD_0         0  '0 positional arguments'
             1028  LOAD_CONST               1
             1030  COMPARE_OP               ==
         1032_1034  POP_JUMP_IF_FALSE  1072  'to 1072'

 L. 622      1036  LOAD_GLOBAL              int
             1038  LOAD_FAST                '_image_width'
             1040  LOAD_CONST               2
             1042  BINARY_TRUE_DIVIDE
             1044  CALL_FUNCTION_1       1  '1 positional argument'
             1046  STORE_FAST               '_wdinl'

 L. 623      1048  LOAD_GLOBAL              int
             1050  LOAD_FAST                '_image_height'
             1052  LOAD_CONST               2
             1054  BINARY_TRUE_DIVIDE
             1056  CALL_FUNCTION_1       1  '1 positional argument'
             1058  STORE_FAST               '_wdz'

 L. 624      1060  LOAD_GLOBAL              int
             1062  LOAD_FAST                '_image_height'
             1064  LOAD_CONST               2
             1066  BINARY_TRUE_DIVIDE
             1068  CALL_FUNCTION_1       1  '1 positional argument'
             1070  STORE_FAST               '_wdztarget'
           1072_0  COME_FROM          1032  '1032'

 L. 625      1072  LOAD_FAST                'self'
             1074  LOAD_ATTR                cbbornt
             1076  LOAD_METHOD              currentIndex
             1078  CALL_METHOD_0         0  '0 positional arguments'
             1080  LOAD_CONST               2
             1082  COMPARE_OP               ==
         1084_1086  POP_JUMP_IF_FALSE  1124  'to 1124'

 L. 626      1088  LOAD_GLOBAL              int
             1090  LOAD_FAST                '_image_width'
             1092  LOAD_CONST               2
             1094  BINARY_TRUE_DIVIDE
             1096  CALL_FUNCTION_1       1  '1 positional argument'
             1098  STORE_FAST               '_wdinl'

 L. 627      1100  LOAD_GLOBAL              int
             1102  LOAD_FAST                '_image_height'
             1104  LOAD_CONST               2
             1106  BINARY_TRUE_DIVIDE
             1108  CALL_FUNCTION_1       1  '1 positional argument'
             1110  STORE_FAST               '_wdxl'

 L. 628      1112  LOAD_GLOBAL              int
             1114  LOAD_FAST                '_image_height'
             1116  LOAD_CONST               2
             1118  BINARY_TRUE_DIVIDE
             1120  CALL_FUNCTION_1       1  '1 positional argument'
             1122  STORE_FAST               '_wdxltarget'
           1124_0  COME_FROM          1084  '1084'

 L. 630      1124  LOAD_FAST                'self'
             1126  LOAD_ATTR                survinfo
             1128  STORE_FAST               '_seisinfo'

 L. 632      1130  LOAD_GLOBAL              print
             1132  LOAD_STR                 'UpdateMl15DDcnn: Step 1 - Get training samples:'
             1134  CALL_FUNCTION_1       1  '1 positional argument'
             1136  POP_TOP          

 L. 633      1138  LOAD_FAST                'self'
             1140  LOAD_ATTR                traindataconfig
             1142  LOAD_STR                 'TrainPointSet'
             1144  BINARY_SUBSCR    
             1146  STORE_FAST               '_trainpoint'

 L. 634      1148  LOAD_GLOBAL              np
             1150  LOAD_METHOD              zeros
             1152  LOAD_CONST               0
             1154  LOAD_CONST               3
             1156  BUILD_LIST_2          2 
             1158  CALL_METHOD_1         1  '1 positional argument'
             1160  STORE_FAST               '_traindata'

 L. 635      1162  SETUP_LOOP         1238  'to 1238'
             1164  LOAD_FAST                '_trainpoint'
             1166  GET_ITER         
           1168_0  COME_FROM          1186  '1186'
             1168  FOR_ITER           1236  'to 1236'
             1170  STORE_FAST               '_p'

 L. 636      1172  LOAD_GLOBAL              point_ays
             1174  LOAD_METHOD              checkPoint
             1176  LOAD_FAST                'self'
             1178  LOAD_ATTR                pointsetdata
             1180  LOAD_FAST                '_p'
             1182  BINARY_SUBSCR    
             1184  CALL_METHOD_1         1  '1 positional argument'
         1186_1188  POP_JUMP_IF_FALSE  1168  'to 1168'

 L. 637      1190  LOAD_GLOBAL              basic_mdt
             1192  LOAD_METHOD              exportMatDict
             1194  LOAD_FAST                'self'
             1196  LOAD_ATTR                pointsetdata
             1198  LOAD_FAST                '_p'
             1200  BINARY_SUBSCR    
             1202  LOAD_STR                 'Inline'
             1204  LOAD_STR                 'Crossline'
             1206  LOAD_STR                 'Z'
             1208  BUILD_LIST_3          3 
             1210  CALL_METHOD_2         2  '2 positional arguments'
             1212  STORE_FAST               '_pt'

 L. 638      1214  LOAD_GLOBAL              np
             1216  LOAD_ATTR                concatenate
             1218  LOAD_FAST                '_traindata'
             1220  LOAD_FAST                '_pt'
             1222  BUILD_TUPLE_2         2 
             1224  LOAD_CONST               0
             1226  LOAD_CONST               ('axis',)
             1228  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1230  STORE_FAST               '_traindata'
         1232_1234  JUMP_BACK          1168  'to 1168'
             1236  POP_BLOCK        
           1238_0  COME_FROM_LOOP     1162  '1162'

 L. 639      1238  LOAD_GLOBAL              seis_ays
             1240  LOAD_ATTR                removeOutofSurveySample
             1242  LOAD_FAST                '_traindata'

 L. 640      1244  LOAD_FAST                '_seisinfo'
             1246  LOAD_STR                 'ILStart'
             1248  BINARY_SUBSCR    
             1250  LOAD_FAST                '_wdinl'
             1252  LOAD_FAST                '_seisinfo'
             1254  LOAD_STR                 'ILStep'
             1256  BINARY_SUBSCR    
             1258  BINARY_MULTIPLY  
             1260  BINARY_ADD       

 L. 641      1262  LOAD_FAST                '_seisinfo'
             1264  LOAD_STR                 'ILEnd'
             1266  BINARY_SUBSCR    
             1268  LOAD_FAST                '_wdinl'
             1270  LOAD_FAST                '_seisinfo'
             1272  LOAD_STR                 'ILStep'
             1274  BINARY_SUBSCR    
             1276  BINARY_MULTIPLY  
             1278  BINARY_SUBTRACT  

 L. 642      1280  LOAD_FAST                '_seisinfo'
             1282  LOAD_STR                 'XLStart'
             1284  BINARY_SUBSCR    
             1286  LOAD_FAST                '_wdxl'
             1288  LOAD_FAST                '_seisinfo'
             1290  LOAD_STR                 'XLStep'
             1292  BINARY_SUBSCR    
             1294  BINARY_MULTIPLY  
             1296  BINARY_ADD       

 L. 643      1298  LOAD_FAST                '_seisinfo'
             1300  LOAD_STR                 'XLEnd'
             1302  BINARY_SUBSCR    
             1304  LOAD_FAST                '_wdxl'
             1306  LOAD_FAST                '_seisinfo'
             1308  LOAD_STR                 'XLStep'
             1310  BINARY_SUBSCR    
             1312  BINARY_MULTIPLY  
             1314  BINARY_SUBTRACT  

 L. 644      1316  LOAD_FAST                '_seisinfo'
             1318  LOAD_STR                 'ZStart'
             1320  BINARY_SUBSCR    
             1322  LOAD_FAST                '_wdz'
             1324  LOAD_FAST                '_seisinfo'
             1326  LOAD_STR                 'ZStep'
             1328  BINARY_SUBSCR    
             1330  BINARY_MULTIPLY  
             1332  BINARY_ADD       

 L. 645      1334  LOAD_FAST                '_seisinfo'
             1336  LOAD_STR                 'ZEnd'
             1338  BINARY_SUBSCR    
             1340  LOAD_FAST                '_wdz'
             1342  LOAD_FAST                '_seisinfo'
             1344  LOAD_STR                 'ZStep'
             1346  BINARY_SUBSCR    
             1348  BINARY_MULTIPLY  
             1350  BINARY_SUBTRACT  
             1352  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1354  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1356  STORE_FAST               '_traindata'

 L. 648      1358  LOAD_GLOBAL              np
             1360  LOAD_METHOD              shape
             1362  LOAD_FAST                '_traindata'
             1364  CALL_METHOD_1         1  '1 positional argument'
             1366  LOAD_CONST               0
             1368  BINARY_SUBSCR    
             1370  LOAD_CONST               0
             1372  COMPARE_OP               <=
         1374_1376  POP_JUMP_IF_FALSE  1414  'to 1414'

 L. 649      1378  LOAD_GLOBAL              vis_msg
             1380  LOAD_ATTR                print
             1382  LOAD_STR                 'ERROR in UpdateMl15DDcnn: No training sample found'
             1384  LOAD_STR                 'error'
             1386  LOAD_CONST               ('type',)
             1388  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1390  POP_TOP          

 L. 650      1392  LOAD_GLOBAL              QtWidgets
             1394  LOAD_ATTR                QMessageBox
             1396  LOAD_METHOD              critical
             1398  LOAD_FAST                'self'
             1400  LOAD_ATTR                msgbox

 L. 651      1402  LOAD_STR                 'Update 2D-DCNN'

 L. 652      1404  LOAD_STR                 'No training sample found'
             1406  CALL_METHOD_3         3  '3 positional arguments'
             1408  POP_TOP          

 L. 653      1410  LOAD_CONST               None
             1412  RETURN_VALUE     
           1414_0  COME_FROM          1374  '1374'

 L. 656      1414  LOAD_GLOBAL              print
             1416  LOAD_STR                 'UpdateMl15DDcnn: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 657      1418  LOAD_FAST                '_image_height'
             1420  LOAD_FAST                '_image_width'
             1422  LOAD_FAST                '_image_height_new'
             1424  LOAD_FAST                '_image_width_new'
             1426  BUILD_TUPLE_4         4 
             1428  BINARY_MODULO    
             1430  CALL_FUNCTION_1       1  '1 positional argument'
             1432  POP_TOP          

 L. 658      1434  BUILD_MAP_0           0 
             1436  STORE_FAST               '_traindict'

 L. 659      1438  SETUP_LOOP         1510  'to 1510'
             1440  LOAD_FAST                '_features'
             1442  GET_ITER         
             1444  FOR_ITER           1508  'to 1508'
             1446  STORE_FAST               'f'

 L. 660      1448  LOAD_FAST                'self'
             1450  LOAD_ATTR                seisdata
             1452  LOAD_FAST                'f'
             1454  BINARY_SUBSCR    
             1456  STORE_FAST               '_seisdata'

 L. 661      1458  LOAD_GLOBAL              seis_ays
             1460  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1462  LOAD_FAST                '_seisdata'
             1464  LOAD_FAST                '_traindata'
             1466  LOAD_FAST                'self'
             1468  LOAD_ATTR                survinfo

 L. 662      1470  LOAD_FAST                '_wdinl'
             1472  LOAD_FAST                '_wdxl'
             1474  LOAD_FAST                '_wdz'

 L. 663      1476  LOAD_CONST               False
             1478  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1480  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1482  LOAD_CONST               None
             1484  LOAD_CONST               None
             1486  BUILD_SLICE_2         2 
             1488  LOAD_CONST               3
             1490  LOAD_CONST               None
             1492  BUILD_SLICE_2         2 
             1494  BUILD_TUPLE_2         2 
             1496  BINARY_SUBSCR    
             1498  LOAD_FAST                '_traindict'
             1500  LOAD_FAST                'f'
             1502  STORE_SUBSCR     
         1504_1506  JUMP_BACK          1444  'to 1444'
             1508  POP_BLOCK        
           1510_0  COME_FROM_LOOP     1438  '1438'

 L. 664      1510  LOAD_FAST                '_target'
             1512  LOAD_FAST                '_features'
             1514  COMPARE_OP               not-in
         1516_1518  POP_JUMP_IF_FALSE  1576  'to 1576'

 L. 665      1520  LOAD_FAST                'self'
             1522  LOAD_ATTR                seisdata
             1524  LOAD_FAST                '_target'
             1526  BINARY_SUBSCR    
             1528  STORE_FAST               '_seisdata'

 L. 666      1530  LOAD_GLOBAL              seis_ays
             1532  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1534  LOAD_FAST                '_seisdata'
             1536  LOAD_FAST                '_traindata'
             1538  LOAD_FAST                'self'
             1540  LOAD_ATTR                survinfo

 L. 667      1542  LOAD_FAST                '_wdinltarget'

 L. 668      1544  LOAD_FAST                '_wdxltarget'

 L. 669      1546  LOAD_FAST                '_wdztarget'

 L. 670      1548  LOAD_CONST               False
             1550  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1552  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1554  LOAD_CONST               None
             1556  LOAD_CONST               None
             1558  BUILD_SLICE_2         2 
             1560  LOAD_CONST               3
             1562  LOAD_CONST               None
             1564  BUILD_SLICE_2         2 
             1566  BUILD_TUPLE_2         2 
             1568  BINARY_SUBSCR    
             1570  LOAD_FAST                '_traindict'
             1572  LOAD_FAST                '_target'
             1574  STORE_SUBSCR     
           1576_0  COME_FROM          1516  '1516'

 L. 672      1576  LOAD_FAST                'self'
             1578  LOAD_ATTR                traindataconfig
             1580  LOAD_STR                 'RemoveInvariantFeature_Checked'
             1582  BINARY_SUBSCR    
         1584_1586  POP_JUMP_IF_FALSE  1668  'to 1668'

 L. 673      1588  SETUP_LOOP         1668  'to 1668'
             1590  LOAD_FAST                '_features'
             1592  GET_ITER         
           1594_0  COME_FROM          1622  '1622'
             1594  FOR_ITER           1666  'to 1666'
             1596  STORE_FAST               'f'

 L. 674      1598  LOAD_GLOBAL              ml_aug
             1600  LOAD_METHOD              removeInvariantFeature
             1602  LOAD_FAST                '_traindict'
             1604  LOAD_FAST                'f'
             1606  CALL_METHOD_2         2  '2 positional arguments'
             1608  STORE_FAST               '_traindict'

 L. 675      1610  LOAD_GLOBAL              basic_mdt
             1612  LOAD_METHOD              maxDictConstantRow
             1614  LOAD_FAST                '_traindict'
             1616  CALL_METHOD_1         1  '1 positional argument'
             1618  LOAD_CONST               0
             1620  COMPARE_OP               <=
         1622_1624  POP_JUMP_IF_FALSE  1594  'to 1594'

 L. 676      1626  LOAD_GLOBAL              vis_msg
             1628  LOAD_ATTR                print
             1630  LOAD_STR                 'ERROR in UpdateMl15DDcnn: No training sample found'
             1632  LOAD_STR                 'error'
             1634  LOAD_CONST               ('type',)
             1636  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1638  POP_TOP          

 L. 677      1640  LOAD_GLOBAL              QtWidgets
             1642  LOAD_ATTR                QMessageBox
             1644  LOAD_METHOD              critical
             1646  LOAD_FAST                'self'
             1648  LOAD_ATTR                msgbox

 L. 678      1650  LOAD_STR                 'Update 1.5D-DCNN'

 L. 679      1652  LOAD_STR                 'No training sample found'
             1654  CALL_METHOD_3         3  '3 positional arguments'
             1656  POP_TOP          

 L. 680      1658  LOAD_CONST               None
             1660  RETURN_VALUE     
         1662_1664  JUMP_BACK          1594  'to 1594'
             1666  POP_BLOCK        
           1668_0  COME_FROM_LOOP     1588  '1588'
           1668_1  COME_FROM          1584  '1584'

 L. 681      1668  LOAD_FAST                '_image_height_new'
             1670  LOAD_FAST                '_image_height'
             1672  COMPARE_OP               !=
         1674_1676  POP_JUMP_IF_TRUE   1688  'to 1688'
             1678  LOAD_FAST                '_image_width_new'
             1680  LOAD_FAST                '_image_width'
             1682  COMPARE_OP               !=
         1684_1686  POP_JUMP_IF_FALSE  1732  'to 1732'
           1688_0  COME_FROM          1674  '1674'

 L. 682      1688  SETUP_LOOP         1732  'to 1732'
             1690  LOAD_FAST                '_features'
             1692  GET_ITER         
             1694  FOR_ITER           1730  'to 1730'
             1696  STORE_FAST               'f'

 L. 683      1698  LOAD_GLOBAL              basic_image
             1700  LOAD_ATTR                changeImageSize
             1702  LOAD_FAST                '_traindict'
             1704  LOAD_FAST                'f'
             1706  BINARY_SUBSCR    

 L. 684      1708  LOAD_FAST                '_image_height'

 L. 685      1710  LOAD_FAST                '_image_width'

 L. 686      1712  LOAD_FAST                '_image_height_new'

 L. 687      1714  LOAD_FAST                '_image_width_new'
             1716  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1718  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1720  LOAD_FAST                '_traindict'
             1722  LOAD_FAST                'f'
             1724  STORE_SUBSCR     
         1726_1728  JUMP_BACK          1694  'to 1694'
             1730  POP_BLOCK        
           1732_0  COME_FROM_LOOP     1688  '1688'
           1732_1  COME_FROM          1684  '1684'

 L. 688      1732  LOAD_FAST                '_image_height_new'
             1734  LOAD_FAST                '_image_height'
             1736  COMPARE_OP               !=
         1738_1740  POP_JUMP_IF_FALSE  1778  'to 1778'
             1742  LOAD_FAST                '_target'
             1744  LOAD_FAST                '_features'
             1746  COMPARE_OP               not-in
         1748_1750  POP_JUMP_IF_FALSE  1778  'to 1778'

 L. 689      1752  LOAD_GLOBAL              basic_curve
             1754  LOAD_ATTR                changeCurveSize
             1756  LOAD_FAST                '_traindict'
             1758  LOAD_FAST                '_target'
             1760  BINARY_SUBSCR    

 L. 690      1762  LOAD_FAST                '_image_height'

 L. 691      1764  LOAD_FAST                '_image_height_new'
             1766  LOAD_STR                 'linear'
             1768  LOAD_CONST               ('length', 'length_new', 'kind')
             1770  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1772  LOAD_FAST                '_traindict'
             1774  LOAD_FAST                '_target'
             1776  STORE_SUBSCR     
           1778_0  COME_FROM          1748  '1748'
           1778_1  COME_FROM          1738  '1738'

 L. 692      1778  LOAD_FAST                'self'
             1780  LOAD_ATTR                traindataconfig
             1782  LOAD_STR                 'RotateFeature_Checked'
             1784  BINARY_SUBSCR    
             1786  LOAD_CONST               True
             1788  COMPARE_OP               is
         1790_1792  POP_JUMP_IF_FALSE  1864  'to 1864'

 L. 693      1794  SETUP_LOOP         1832  'to 1832'
             1796  LOAD_FAST                '_features'
             1798  GET_ITER         
             1800  FOR_ITER           1830  'to 1830'
             1802  STORE_FAST               'f'

 L. 694      1804  LOAD_GLOBAL              ml_aug
             1806  LOAD_METHOD              rotateImage4Way
             1808  LOAD_FAST                '_traindict'
             1810  LOAD_FAST                'f'
             1812  BINARY_SUBSCR    
             1814  LOAD_FAST                '_image_height_new'
             1816  LOAD_FAST                '_image_width_new'
             1818  CALL_METHOD_3         3  '3 positional arguments'
             1820  LOAD_FAST                '_traindict'
             1822  LOAD_FAST                'f'
             1824  STORE_SUBSCR     
         1826_1828  JUMP_BACK          1800  'to 1800'
             1830  POP_BLOCK        
           1832_0  COME_FROM_LOOP     1794  '1794'

 L. 695      1832  LOAD_FAST                '_target'
             1834  LOAD_FAST                '_features'
             1836  COMPARE_OP               not-in
         1838_1840  POP_JUMP_IF_FALSE  1864  'to 1864'

 L. 696      1842  LOAD_GLOBAL              ml_aug
             1844  LOAD_METHOD              rotateImage4Way
             1846  LOAD_FAST                '_traindict'
             1848  LOAD_FAST                '_target'
             1850  BINARY_SUBSCR    
             1852  LOAD_FAST                '_image_height_new'
             1854  LOAD_CONST               1
             1856  CALL_METHOD_3         3  '3 positional arguments'
             1858  LOAD_FAST                '_traindict'
             1860  LOAD_FAST                '_target'
             1862  STORE_SUBSCR     
           1864_0  COME_FROM          1838  '1838'
           1864_1  COME_FROM          1790  '1790'

 L. 698      1864  LOAD_GLOBAL              np
             1866  LOAD_METHOD              round
             1868  LOAD_FAST                '_traindict'
             1870  LOAD_FAST                '_target'
             1872  BINARY_SUBSCR    
             1874  CALL_METHOD_1         1  '1 positional argument'
             1876  LOAD_METHOD              astype
             1878  LOAD_GLOBAL              int
             1880  CALL_METHOD_1         1  '1 positional argument'
             1882  LOAD_FAST                '_traindict'
             1884  LOAD_FAST                '_target'
             1886  STORE_SUBSCR     

 L. 701      1888  LOAD_GLOBAL              print
             1890  LOAD_STR                 'UpdateMl15DDcnn: A total of %d valid training samples'
             1892  LOAD_GLOBAL              basic_mdt
             1894  LOAD_METHOD              maxDictConstantRow
             1896  LOAD_FAST                '_traindict'
             1898  CALL_METHOD_1         1  '1 positional argument'
             1900  BINARY_MODULO    
             1902  CALL_FUNCTION_1       1  '1 positional argument'
             1904  POP_TOP          

 L. 703      1906  LOAD_GLOBAL              print
             1908  LOAD_STR                 'UpdateMl15DDcnn: Step 3 - Start training'
             1910  CALL_FUNCTION_1       1  '1 positional argument'
             1912  POP_TOP          

 L. 705      1914  LOAD_GLOBAL              QtWidgets
             1916  LOAD_METHOD              QProgressDialog
             1918  CALL_METHOD_0         0  '0 positional arguments'
             1920  STORE_FAST               '_pgsdlg'

 L. 706      1922  LOAD_GLOBAL              QtGui
             1924  LOAD_METHOD              QIcon
             1926  CALL_METHOD_0         0  '0 positional arguments'
             1928  STORE_FAST               'icon'

 L. 707      1930  LOAD_FAST                'icon'
             1932  LOAD_METHOD              addPixmap
             1934  LOAD_GLOBAL              QtGui
             1936  LOAD_METHOD              QPixmap
             1938  LOAD_GLOBAL              os
             1940  LOAD_ATTR                path
             1942  LOAD_METHOD              join
             1944  LOAD_FAST                'self'
             1946  LOAD_ATTR                iconpath
             1948  LOAD_STR                 'icons/update.png'
             1950  CALL_METHOD_2         2  '2 positional arguments'
             1952  CALL_METHOD_1         1  '1 positional argument'

 L. 708      1954  LOAD_GLOBAL              QtGui
             1956  LOAD_ATTR                QIcon
             1958  LOAD_ATTR                Normal
             1960  LOAD_GLOBAL              QtGui
             1962  LOAD_ATTR                QIcon
             1964  LOAD_ATTR                Off
             1966  CALL_METHOD_3         3  '3 positional arguments'
             1968  POP_TOP          

 L. 709      1970  LOAD_FAST                '_pgsdlg'
             1972  LOAD_METHOD              setWindowIcon
             1974  LOAD_FAST                'icon'
             1976  CALL_METHOD_1         1  '1 positional argument'
             1978  POP_TOP          

 L. 710      1980  LOAD_FAST                '_pgsdlg'
             1982  LOAD_METHOD              setWindowTitle
             1984  LOAD_STR                 'Update 1.5D-DCNN'
             1986  CALL_METHOD_1         1  '1 positional argument'
             1988  POP_TOP          

 L. 711      1990  LOAD_FAST                '_pgsdlg'
             1992  LOAD_METHOD              setCancelButton
             1994  LOAD_CONST               None
             1996  CALL_METHOD_1         1  '1 positional argument'
             1998  POP_TOP          

 L. 712      2000  LOAD_FAST                '_pgsdlg'
             2002  LOAD_METHOD              setWindowFlags
             2004  LOAD_GLOBAL              QtCore
             2006  LOAD_ATTR                Qt
             2008  LOAD_ATTR                WindowStaysOnTopHint
             2010  CALL_METHOD_1         1  '1 positional argument'
             2012  POP_TOP          

 L. 713      2014  LOAD_FAST                '_pgsdlg'
             2016  LOAD_METHOD              forceShow
             2018  CALL_METHOD_0         0  '0 positional arguments'
             2020  POP_TOP          

 L. 714      2022  LOAD_FAST                '_pgsdlg'
             2024  LOAD_METHOD              setFixedWidth
             2026  LOAD_CONST               400
             2028  CALL_METHOD_1         1  '1 positional argument'
             2030  POP_TOP          

 L. 715      2032  LOAD_GLOBAL              ml_dcnn15d
             2034  LOAD_ATTR                update15DDCNNSegmentor
             2036  LOAD_FAST                '_traindict'

 L. 716      2038  LOAD_FAST                '_image_height_new'
             2040  LOAD_FAST                '_image_width_new'

 L. 717      2042  LOAD_FAST                '_nepoch'
             2044  LOAD_FAST                '_batchsize'

 L. 718      2046  LOAD_FAST                '_learning_rate'

 L. 719      2048  LOAD_FAST                '_dropout_prob'

 L. 720      2050  LOAD_FAST                'self'
             2052  LOAD_ATTR                modelpath
             2054  LOAD_FAST                'self'
             2056  LOAD_ATTR                modelname

 L. 721      2058  LOAD_CONST               True

 L. 722      2060  LOAD_FAST                '_savepath'
             2062  LOAD_FAST                '_savename'

 L. 723      2064  LOAD_FAST                '_pgsdlg'
             2066  LOAD_CONST               ('imageheight', 'imagewidth', 'nepoch', 'batchsize', 'learningrate', 'dropoutprob', 'dcnnpath', 'dcnnname', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2068  CALL_FUNCTION_KW_13    13  '13 total positional and keyword args'
             2070  STORE_FAST               '_dccnlog'

 L. 725      2072  LOAD_GLOBAL              QtWidgets
             2074  LOAD_ATTR                QMessageBox
             2076  LOAD_METHOD              information
             2078  LOAD_FAST                'self'
             2080  LOAD_ATTR                msgbox

 L. 726      2082  LOAD_STR                 'Update 1.5D-DCNN'

 L. 727      2084  LOAD_STR                 'DCNN updated successfully'
             2086  CALL_METHOD_3         3  '3 positional arguments'
             2088  POP_TOP          

 L. 729      2090  LOAD_GLOBAL              QtWidgets
             2092  LOAD_ATTR                QMessageBox
             2094  LOAD_METHOD              question
             2096  LOAD_FAST                'self'
             2098  LOAD_ATTR                msgbox
             2100  LOAD_STR                 'Update 1.5D-DCNN'
             2102  LOAD_STR                 'View learning matrix?'

 L. 730      2104  LOAD_GLOBAL              QtWidgets
             2106  LOAD_ATTR                QMessageBox
             2108  LOAD_ATTR                Yes
             2110  LOAD_GLOBAL              QtWidgets
             2112  LOAD_ATTR                QMessageBox
             2114  LOAD_ATTR                No
             2116  BINARY_OR        

 L. 731      2118  LOAD_GLOBAL              QtWidgets
             2120  LOAD_ATTR                QMessageBox
             2122  LOAD_ATTR                Yes
             2124  CALL_METHOD_5         5  '5 positional arguments'
             2126  STORE_FAST               'reply'

 L. 733      2128  LOAD_FAST                'reply'
             2130  LOAD_GLOBAL              QtWidgets
             2132  LOAD_ATTR                QMessageBox
             2134  LOAD_ATTR                Yes
             2136  COMPARE_OP               ==
         2138_2140  POP_JUMP_IF_FALSE  2208  'to 2208'

 L. 734      2142  LOAD_GLOBAL              QtWidgets
             2144  LOAD_METHOD              QDialog
             2146  CALL_METHOD_0         0  '0 positional arguments'
             2148  STORE_FAST               '_viewmllearnmat'

 L. 735      2150  LOAD_GLOBAL              gui_viewmllearnmat
             2152  CALL_FUNCTION_0       0  '0 positional arguments'
             2154  STORE_FAST               '_gui'

 L. 736      2156  LOAD_FAST                '_dccnlog'
             2158  LOAD_STR                 'learning_curve'
             2160  BINARY_SUBSCR    
             2162  LOAD_FAST                '_gui'
             2164  STORE_ATTR               learnmat

 L. 737      2166  LOAD_FAST                'self'
             2168  LOAD_ATTR                linestyle
             2170  LOAD_FAST                '_gui'
             2172  STORE_ATTR               linestyle

 L. 738      2174  LOAD_FAST                'self'
             2176  LOAD_ATTR                fontstyle
             2178  LOAD_FAST                '_gui'
             2180  STORE_ATTR               fontstyle

 L. 739      2182  LOAD_FAST                '_gui'
             2184  LOAD_METHOD              setupGUI
             2186  LOAD_FAST                '_viewmllearnmat'
             2188  CALL_METHOD_1         1  '1 positional argument'
             2190  POP_TOP          

 L. 740      2192  LOAD_FAST                '_viewmllearnmat'
             2194  LOAD_METHOD              exec
             2196  CALL_METHOD_0         0  '0 positional arguments'
             2198  POP_TOP          

 L. 741      2200  LOAD_FAST                '_viewmllearnmat'
             2202  LOAD_METHOD              show
             2204  CALL_METHOD_0         0  '0 positional arguments'
             2206  POP_TOP          
           2208_0  COME_FROM          2138  '2138'

Parse error at or near `POP_TOP' instruction at offset 2206

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
    UpdateMl15DDcnn = QtWidgets.QWidget()
    gui = updateml15ddcnn()
    gui.setupGUI(UpdateMl15DDcnn)
    UpdateMl15DDcnn.show()
    sys.exit(app.exec_())