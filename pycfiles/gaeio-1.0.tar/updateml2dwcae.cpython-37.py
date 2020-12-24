# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\updateml2dwcae.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 45732 bytes
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
import cognitivegeo.src.ml.wcaereconstructor as ml_wcae
import cognitivegeo.src.gui.viewml2dwcae as gui_viewml2dwcae
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class updateml2dwcae(object):
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

    def setupGUI(self, UpdateMl2DWcae):
        UpdateMl2DWcae.setObjectName('UpdateMl2DWcae')
        UpdateMl2DWcae.setFixedSize(810, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UpdateMl2DWcae.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(UpdateMl2DWcae)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(UpdateMl2DWcae)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(UpdateMl2DWcae)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 230, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 230, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 230, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 270, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 270, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 230, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lbltarget = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lbltarget.setObjectName('lbltargete')
        self.lbltarget.setGeometry(QtCore.QRect(10, 320, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(UpdateMl2DWcae)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 320, 280, 30))
        self.lblweight = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblweight.setObjectName('lblweight')
        self.lblweight.setGeometry(QtCore.QRect(10, 370, 100, 30))
        self.cbbweight = QtWidgets.QComboBox(UpdateMl2DWcae)
        self.cbbweight.setObjectName('cbbweight')
        self.cbbweight.setGeometry(QtCore.QRect(110, 370, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(UpdateMl2DWcae)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(UpdateMl2DWcae)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 210))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(UpdateMl2DWcae)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 210))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 360, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 360, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 400, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 400, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 360, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 360, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 360, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 400, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 400, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(UpdateMl2DWcae)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 420, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 420, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 460, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 460, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 460, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 460, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 500, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 500, 40, 30))
        self.lbldropout = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 500, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 500, 40, 30))
        self.lblsave = QtWidgets.QLabel(UpdateMl2DWcae)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 550, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(UpdateMl2DWcae)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 550, 180, 30))
        self.btnsave = QtWidgets.QPushButton(UpdateMl2DWcae)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 550, 60, 30))
        self.btnapply = QtWidgets.QPushButton(UpdateMl2DWcae)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 550, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(UpdateMl2DWcae)
        self.msgbox.setObjectName('msgbox')
        _center_x = UpdateMl2DWcae.geometry().center().x()
        _center_y = UpdateMl2DWcae.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(UpdateMl2DWcae)
        QtCore.QMetaObject.connectSlotsByName(UpdateMl2DWcae)

    def retranslateGUI(self, UpdateMl2DWcae):
        self.dialog = UpdateMl2DWcae
        _translate = QtCore.QCoreApplication.translate
        UpdateMl2DWcae.setWindowTitle(_translate('UpdateMl2DWcae', 'Update 2D-WCAE'))
        self.lblfrom.setText(_translate('UpdateMl2DWcae', 'Select network:'))
        self.ldtfrom.setText(_translate('UpdateMl2DWcae', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('UpdateMl2DWcae', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('UpdateMl2DWcae', 'Training features:'))
        self.lblornt.setText(_translate('UpdateMl2DWcae', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('UpdateMl2DWcae', 'Training target:'))
        self.lblweight.setText(_translate('UpdateMl2DWcae', 'Training weight:'))
        self.btnconfigtraindata.setText(_translate('TrainMl2DDcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('UpdateMl2DWcae', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('UpdateMl2DWcae', 'height='))
        self.ldtoldheight.setText(_translate('UpdateMl2DWcae', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('UpdateMl2DWcae', 'width='))
        self.ldtoldwidth.setText(_translate('UpdateMl2DWcae', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('UpdateMl2DWcae', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('UpdateMl2DWcae', 'height='))
        self.ldtnewheight.setText(_translate('UpdateMl2DWcae', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('UpdateMl2DWcae', 'width='))
        self.ldtnewwidth.setText(_translate('UpdateMl2DWcae', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('UpdateMl2DWcae', 'Pre-trained WCAE architecture:'))
        self.btnviewnetwork.setText(_translate('UpdateMl2DWcae', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('UpdateMl2DWcae', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('UpdateMl2DWcae', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('UpdateMl2DWcae', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('UpdateMl2DWcae', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('UpdateMl2DWcae', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('UpdateMl2DWcae', 'height='))
        self.ldtmaskheight.setText(_translate('UpdateMl2DWcae', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('UpdateMl2DWcae', 'width='))
        self.ldtmaskwidth.setText(_translate('UpdateMl2DWcae', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('UpdateMl2DWcae', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('UpdateMl2DWcae', 'height='))
        self.ldtpoolheight.setText(_translate('UpdateMl2DWcae', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('UpdateMl2DWcae', 'width='))
        self.ldtpoolwidth.setText(_translate('UpdateMl2DWcae', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('UpdateMl2DWcae', 'Specify update parameters:'))
        self.lblnepoch.setText(_translate('UpdateMl2DWcae', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('UpdateMl2DWcae', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('UpdateMl2DWcae', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('UpdateMl2DWcae', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('UpdateMl2DWcae', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('UpdateMl2DWcae', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('UpdateMl2DWcae', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('UpdateMl2DWcae', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('UpdateMl2DWcae', 'Save new-WCAE to:'))
        self.ldtsave.setText(_translate('UpdateMl2DWcae', ''))
        self.btnsave.setText(_translate('UpdateMl2DWcae', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('UpdateMl2DWcae', 'Update 2D-WCAE'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnUpdateMl2DWcae)

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.checkWCAEModel(self.modelpath, self.modelname) is True:
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
        _file = _dialog.getOpenFileName(None, 'Select CAE Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def clickBtnViewNetwork(self):
        _viewml = QtWidgets.QDialog()
        _gui = gui_viewml2dwcae()
        _gui.linestyle = self.linestyle
        _gui.maskstyle = self.maskstyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewml)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewml.exec()
        _viewml.show()

    def changeLdtNconvblock(self):
        if ml_tfm.checkWCAEModel(self.modelpath, self.modelname) is True:
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
        if ml_tfm.checkWCAEModel(self.modelpath, self.modelname) is True:
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

    def clickBtnUpdateMl2DWcae--- This code section failed: ---

 L. 526         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 528         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 529        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in UpdateMl2DWcae: No seismic data available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 530        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 531        44  LOAD_STR                 'Update 2D-WCAE'

 L. 532        46  LOAD_STR                 'No seismic data available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 533        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 535        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkWCAEModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 536        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in UpdateMl2DWcae: No pre-WCAE network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 537        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 538       100  LOAD_STR                 'Update 2D-WCAE'

 L. 539       102  LOAD_STR                 'No pre-WCAE network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 540       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 542       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 543       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 544       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in UpdateMl2DWcae: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    

 L. 545       152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 546       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 547       170  LOAD_STR                 'Update 2D-WCAE'

 L. 548       172  LOAD_STR                 "Feature '"
              174  LOAD_FAST                'f'
              176  BINARY_ADD       
              178  LOAD_STR                 "' not found in seismic data"
              180  BINARY_ADD       
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L. 549       186  LOAD_CONST               None
              188  RETURN_VALUE     
              190  JUMP_BACK           124  'to 124'
              192  POP_BLOCK        
            194_0  COME_FROM_LOOP      112  '112'

 L. 551       194  LOAD_GLOBAL              basic_data
              196  LOAD_METHOD              str2int
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                ldtoldheight
              202  LOAD_METHOD              text
              204  CALL_METHOD_0         0  '0 positional arguments'
              206  CALL_METHOD_1         1  '1 positional argument'
              208  STORE_FAST               '_image_height'

 L. 552       210  LOAD_GLOBAL              basic_data
              212  LOAD_METHOD              str2int
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                ldtoldwidth
              218  LOAD_METHOD              text
              220  CALL_METHOD_0         0  '0 positional arguments'
              222  CALL_METHOD_1         1  '1 positional argument'
              224  STORE_FAST               '_image_width'

 L. 553       226  LOAD_GLOBAL              basic_data
              228  LOAD_METHOD              str2int
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                ldtnewheight
              234  LOAD_METHOD              text
              236  CALL_METHOD_0         0  '0 positional arguments'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  STORE_FAST               '_image_height_new'

 L. 554       242  LOAD_GLOBAL              basic_data
              244  LOAD_METHOD              str2int
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                ldtnewwidth
              250  LOAD_METHOD              text
              252  CALL_METHOD_0         0  '0 positional arguments'
              254  CALL_METHOD_1         1  '1 positional argument'
              256  STORE_FAST               '_image_width_new'

 L. 555       258  LOAD_FAST                '_image_height'
              260  LOAD_CONST               False
              262  COMPARE_OP               is
          264_266  POP_JUMP_IF_TRUE    298  'to 298'
              268  LOAD_FAST                '_image_width'
              270  LOAD_CONST               False
              272  COMPARE_OP               is
          274_276  POP_JUMP_IF_TRUE    298  'to 298'

 L. 556       278  LOAD_FAST                '_image_height_new'
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

 L. 557       298  LOAD_GLOBAL              vis_msg
              300  LOAD_ATTR                print
              302  LOAD_STR                 'ERROR in UpdateMl2DWcae: Non-integer feature size'
              304  LOAD_STR                 'error'
              306  LOAD_CONST               ('type',)
              308  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              310  POP_TOP          

 L. 558       312  LOAD_GLOBAL              QtWidgets
              314  LOAD_ATTR                QMessageBox
              316  LOAD_METHOD              critical
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                msgbox

 L. 559       322  LOAD_STR                 'Update 2D-WCAE'

 L. 560       324  LOAD_STR                 'Non-integer feature size'
              326  CALL_METHOD_3         3  '3 positional arguments'
              328  POP_TOP          

 L. 561       330  LOAD_CONST               None
              332  RETURN_VALUE     
            334_0  COME_FROM           294  '294'

 L. 562       334  LOAD_FAST                '_image_height'
              336  LOAD_CONST               2
              338  COMPARE_OP               <
          340_342  POP_JUMP_IF_TRUE    374  'to 374'
              344  LOAD_FAST                '_image_width'
              346  LOAD_CONST               2
              348  COMPARE_OP               <
          350_352  POP_JUMP_IF_TRUE    374  'to 374'

 L. 563       354  LOAD_FAST                '_image_height_new'
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

 L. 564       374  LOAD_GLOBAL              vis_msg
              376  LOAD_ATTR                print
              378  LOAD_STR                 'ERROR in UpdateMl2DWcae: Features are not 2D'
              380  LOAD_STR                 'error'
              382  LOAD_CONST               ('type',)
              384  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              386  POP_TOP          

 L. 565       388  LOAD_GLOBAL              QtWidgets
              390  LOAD_ATTR                QMessageBox
              392  LOAD_METHOD              critical
              394  LOAD_FAST                'self'
              396  LOAD_ATTR                msgbox

 L. 566       398  LOAD_STR                 'Update 2D-WCAE'

 L. 567       400  LOAD_STR                 'Features are not 2D'
              402  CALL_METHOD_3         3  '3 positional arguments'
              404  POP_TOP          

 L. 568       406  LOAD_CONST               None
              408  RETURN_VALUE     
            410_0  COME_FROM           370  '370'

 L. 570       410  LOAD_CONST               2
              412  LOAD_GLOBAL              int
              414  LOAD_FAST                '_image_height'
              416  LOAD_CONST               2
              418  BINARY_TRUE_DIVIDE
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  BINARY_MULTIPLY  
              424  LOAD_CONST               1
              426  BINARY_ADD       
              428  STORE_FAST               '_image_height'

 L. 571       430  LOAD_CONST               2
              432  LOAD_GLOBAL              int
              434  LOAD_FAST                '_image_width'
              436  LOAD_CONST               2
              438  BINARY_TRUE_DIVIDE
              440  CALL_FUNCTION_1       1  '1 positional argument'
              442  BINARY_MULTIPLY  
              444  LOAD_CONST               1
              446  BINARY_ADD       
              448  STORE_FAST               '_image_width'

 L. 573       450  LOAD_FAST                'self'
              452  LOAD_ATTR                modelinfo
              454  LOAD_STR                 'target'
              456  BINARY_SUBSCR    
              458  LOAD_FAST                'self'
              460  LOAD_ATTR                seisdata
              462  LOAD_METHOD              keys
              464  CALL_METHOD_0         0  '0 positional arguments'
              466  COMPARE_OP               not-in
          468_470  POP_JUMP_IF_FALSE   532  'to 532'

 L. 574       472  LOAD_GLOBAL              vis_msg
              474  LOAD_ATTR                print
              476  LOAD_STR                 "ERROR in UpdateMl2DWcae: Target '%s' not found in seismic data"

 L. 575       478  LOAD_FAST                'self'
              480  LOAD_ATTR                modelinfo
              482  LOAD_STR                 'target'
              484  BINARY_SUBSCR    
              486  BINARY_MODULO    
              488  LOAD_STR                 'error'
              490  LOAD_CONST               ('type',)
              492  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              494  POP_TOP          

 L. 576       496  LOAD_GLOBAL              QtWidgets
              498  LOAD_ATTR                QMessageBox
              500  LOAD_METHOD              critical
              502  LOAD_FAST                'self'
              504  LOAD_ATTR                msgbox

 L. 577       506  LOAD_STR                 'Update 2D-WCAE'

 L. 578       508  LOAD_STR                 "Target '"
              510  LOAD_FAST                'self'
              512  LOAD_ATTR                modelinfo
              514  LOAD_STR                 'target'
              516  BINARY_SUBSCR    
              518  BINARY_ADD       
              520  LOAD_STR                 ' not found in seismic data'
              522  BINARY_ADD       
              524  CALL_METHOD_3         3  '3 positional arguments'
              526  POP_TOP          

 L. 579       528  LOAD_CONST               None
              530  RETURN_VALUE     
            532_0  COME_FROM           468  '468'

 L. 580       532  LOAD_FAST                'self'
              534  LOAD_ATTR                modelinfo
              536  LOAD_STR                 'weight'
              538  BINARY_SUBSCR    
              540  LOAD_FAST                'self'
              542  LOAD_ATTR                seisdata
              544  LOAD_METHOD              keys
              546  CALL_METHOD_0         0  '0 positional arguments'
              548  COMPARE_OP               not-in
          550_552  POP_JUMP_IF_FALSE   614  'to 614'

 L. 581       554  LOAD_GLOBAL              vis_msg
              556  LOAD_ATTR                print
              558  LOAD_STR                 "ERROR in UpdateMl2DWcae: Weight '%s' not found in seismic data"

 L. 582       560  LOAD_FAST                'self'
              562  LOAD_ATTR                modelinfo
              564  LOAD_STR                 'weight'
              566  BINARY_SUBSCR    
              568  BINARY_MODULO    
              570  LOAD_STR                 'error'
              572  LOAD_CONST               ('type',)
              574  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              576  POP_TOP          

 L. 583       578  LOAD_GLOBAL              QtWidgets
              580  LOAD_ATTR                QMessageBox
              582  LOAD_METHOD              critical
              584  LOAD_FAST                'self'
              586  LOAD_ATTR                msgbox

 L. 584       588  LOAD_STR                 'Update 2D-WCAE'

 L. 585       590  LOAD_STR                 "Weight '"
              592  LOAD_FAST                'self'
              594  LOAD_ATTR                modelinfo
              596  LOAD_STR                 'target'
              598  BINARY_SUBSCR    
              600  BINARY_ADD       
              602  LOAD_STR                 ' not found in seismic data'
              604  BINARY_ADD       
              606  CALL_METHOD_3         3  '3 positional arguments'
              608  POP_TOP          

 L. 586       610  LOAD_CONST               None
              612  RETURN_VALUE     
            614_0  COME_FROM           550  '550'

 L. 588       614  LOAD_FAST                'self'
              616  LOAD_ATTR                modelinfo
              618  LOAD_STR                 'feature_list'
              620  BINARY_SUBSCR    
              622  STORE_FAST               '_features'

 L. 589       624  LOAD_FAST                'self'
              626  LOAD_ATTR                modelinfo
              628  LOAD_STR                 'target'
              630  BINARY_SUBSCR    
              632  STORE_FAST               '_target'

 L. 590       634  LOAD_FAST                'self'
              636  LOAD_ATTR                modelinfo
              638  LOAD_STR                 'weight'
              640  BINARY_SUBSCR    
              642  STORE_FAST               '_weight'

 L. 592       644  LOAD_GLOBAL              basic_data
              646  LOAD_METHOD              str2int
              648  LOAD_FAST                'self'
              650  LOAD_ATTR                ldtnepoch
              652  LOAD_METHOD              text
              654  CALL_METHOD_0         0  '0 positional arguments'
              656  CALL_METHOD_1         1  '1 positional argument'
              658  STORE_FAST               '_nepoch'

 L. 593       660  LOAD_GLOBAL              basic_data
              662  LOAD_METHOD              str2int
              664  LOAD_FAST                'self'
              666  LOAD_ATTR                ldtbatchsize
              668  LOAD_METHOD              text
              670  CALL_METHOD_0         0  '0 positional arguments'
              672  CALL_METHOD_1         1  '1 positional argument'
              674  STORE_FAST               '_batchsize'

 L. 594       676  LOAD_GLOBAL              basic_data
              678  LOAD_METHOD              str2float
              680  LOAD_FAST                'self'
              682  LOAD_ATTR                ldtlearnrate
              684  LOAD_METHOD              text
              686  CALL_METHOD_0         0  '0 positional arguments'
              688  CALL_METHOD_1         1  '1 positional argument'
              690  STORE_FAST               '_learning_rate'

 L. 595       692  LOAD_GLOBAL              basic_data
              694  LOAD_METHOD              str2float
              696  LOAD_FAST                'self'
              698  LOAD_ATTR                ldtdropout
              700  LOAD_METHOD              text
              702  CALL_METHOD_0         0  '0 positional arguments'
              704  CALL_METHOD_1         1  '1 positional argument'
              706  STORE_FAST               '_dropout_prob'

 L. 596       708  LOAD_FAST                '_nepoch'
              710  LOAD_CONST               False
              712  COMPARE_OP               is
          714_716  POP_JUMP_IF_TRUE    728  'to 728'
              718  LOAD_FAST                '_nepoch'
              720  LOAD_CONST               0
              722  COMPARE_OP               <=
          724_726  POP_JUMP_IF_FALSE   764  'to 764'
            728_0  COME_FROM           714  '714'

 L. 597       728  LOAD_GLOBAL              vis_msg
              730  LOAD_ATTR                print
              732  LOAD_STR                 'ERROR in UpdateMl2DWcae: Non-positive epoch number'
              734  LOAD_STR                 'error'
              736  LOAD_CONST               ('type',)
              738  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              740  POP_TOP          

 L. 598       742  LOAD_GLOBAL              QtWidgets
              744  LOAD_ATTR                QMessageBox
              746  LOAD_METHOD              critical
              748  LOAD_FAST                'self'
              750  LOAD_ATTR                msgbox

 L. 599       752  LOAD_STR                 'Update 2D-WCAE'

 L. 600       754  LOAD_STR                 'Non-positive epoch number'
              756  CALL_METHOD_3         3  '3 positional arguments'
              758  POP_TOP          

 L. 601       760  LOAD_CONST               None
              762  RETURN_VALUE     
            764_0  COME_FROM           724  '724'

 L. 602       764  LOAD_FAST                '_batchsize'
              766  LOAD_CONST               False
              768  COMPARE_OP               is
          770_772  POP_JUMP_IF_TRUE    784  'to 784'
              774  LOAD_FAST                '_batchsize'
              776  LOAD_CONST               0
              778  COMPARE_OP               <=
          780_782  POP_JUMP_IF_FALSE   820  'to 820'
            784_0  COME_FROM           770  '770'

 L. 603       784  LOAD_GLOBAL              vis_msg
              786  LOAD_ATTR                print
              788  LOAD_STR                 'ERROR in UpdateMl2DWcae: Non-positive batch size'
              790  LOAD_STR                 'error'
              792  LOAD_CONST               ('type',)
              794  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              796  POP_TOP          

 L. 604       798  LOAD_GLOBAL              QtWidgets
              800  LOAD_ATTR                QMessageBox
              802  LOAD_METHOD              critical
              804  LOAD_FAST                'self'
              806  LOAD_ATTR                msgbox

 L. 605       808  LOAD_STR                 'Update 2D-WCAE'

 L. 606       810  LOAD_STR                 'Non-positive batch size'
              812  CALL_METHOD_3         3  '3 positional arguments'
              814  POP_TOP          

 L. 607       816  LOAD_CONST               None
              818  RETURN_VALUE     
            820_0  COME_FROM           780  '780'

 L. 608       820  LOAD_FAST                '_learning_rate'
              822  LOAD_CONST               False
              824  COMPARE_OP               is
          826_828  POP_JUMP_IF_TRUE    840  'to 840'
              830  LOAD_FAST                '_learning_rate'
              832  LOAD_CONST               0
              834  COMPARE_OP               <=
          836_838  POP_JUMP_IF_FALSE   876  'to 876'
            840_0  COME_FROM           826  '826'

 L. 609       840  LOAD_GLOBAL              vis_msg
              842  LOAD_ATTR                print
              844  LOAD_STR                 'ERROR in UpdateMl2DWcae: Non-positive learning rate'
              846  LOAD_STR                 'error'
              848  LOAD_CONST               ('type',)
              850  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              852  POP_TOP          

 L. 610       854  LOAD_GLOBAL              QtWidgets
              856  LOAD_ATTR                QMessageBox
              858  LOAD_METHOD              critical
              860  LOAD_FAST                'self'
              862  LOAD_ATTR                msgbox

 L. 611       864  LOAD_STR                 'Update 2D-WCAE'

 L. 612       866  LOAD_STR                 'Non-positive learning rate'
              868  CALL_METHOD_3         3  '3 positional arguments'
              870  POP_TOP          

 L. 613       872  LOAD_CONST               None
              874  RETURN_VALUE     
            876_0  COME_FROM           836  '836'

 L. 614       876  LOAD_FAST                '_dropout_prob'
              878  LOAD_CONST               False
              880  COMPARE_OP               is
          882_884  POP_JUMP_IF_TRUE    896  'to 896'
              886  LOAD_FAST                '_dropout_prob'
              888  LOAD_CONST               0
              890  COMPARE_OP               <=
          892_894  POP_JUMP_IF_FALSE   932  'to 932'
            896_0  COME_FROM           882  '882'

 L. 615       896  LOAD_GLOBAL              vis_msg
              898  LOAD_ATTR                print
              900  LOAD_STR                 'ERROR in UpdateMl2DWcae: Negative dropout rate'
              902  LOAD_STR                 'error'
              904  LOAD_CONST               ('type',)
              906  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              908  POP_TOP          

 L. 616       910  LOAD_GLOBAL              QtWidgets
              912  LOAD_ATTR                QMessageBox
              914  LOAD_METHOD              critical
              916  LOAD_FAST                'self'
              918  LOAD_ATTR                msgbox

 L. 617       920  LOAD_STR                 'Update 2D-WCAE'

 L. 618       922  LOAD_STR                 'Negative dropout rate'
              924  CALL_METHOD_3         3  '3 positional arguments'
              926  POP_TOP          

 L. 619       928  LOAD_CONST               None
              930  RETURN_VALUE     
            932_0  COME_FROM           892  '892'

 L. 621       932  LOAD_GLOBAL              len
              934  LOAD_FAST                'self'
              936  LOAD_ATTR                ldtsave
              938  LOAD_METHOD              text
              940  CALL_METHOD_0         0  '0 positional arguments'
              942  CALL_FUNCTION_1       1  '1 positional argument'
              944  LOAD_CONST               1
              946  COMPARE_OP               <
          948_950  POP_JUMP_IF_FALSE   988  'to 988'

 L. 622       952  LOAD_GLOBAL              vis_msg
              954  LOAD_ATTR                print
              956  LOAD_STR                 'ERROR in UpdateMl2DWcae: No name specified for new-WCAE'
              958  LOAD_STR                 'error'
              960  LOAD_CONST               ('type',)
              962  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              964  POP_TOP          

 L. 623       966  LOAD_GLOBAL              QtWidgets
              968  LOAD_ATTR                QMessageBox
              970  LOAD_METHOD              critical
              972  LOAD_FAST                'self'
              974  LOAD_ATTR                msgbox

 L. 624       976  LOAD_STR                 'Update 2DW-CAE'

 L. 625       978  LOAD_STR                 'No name specified for new-CAE'
              980  CALL_METHOD_3         3  '3 positional arguments'
              982  POP_TOP          

 L. 626       984  LOAD_CONST               None
              986  RETURN_VALUE     
            988_0  COME_FROM           948  '948'

 L. 627       988  LOAD_GLOBAL              os
              990  LOAD_ATTR                path
              992  LOAD_METHOD              dirname
              994  LOAD_FAST                'self'
              996  LOAD_ATTR                ldtsave
              998  LOAD_METHOD              text
             1000  CALL_METHOD_0         0  '0 positional arguments'
             1002  CALL_METHOD_1         1  '1 positional argument'
             1004  STORE_FAST               '_savepath'

 L. 628      1006  LOAD_GLOBAL              os
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

 L. 630      1036  LOAD_CONST               0
             1038  STORE_FAST               '_wdinl'

 L. 631      1040  LOAD_CONST               0
             1042  STORE_FAST               '_wdxl'

 L. 632      1044  LOAD_CONST               0
             1046  STORE_FAST               '_wdz'

 L. 633      1048  LOAD_FAST                'self'
             1050  LOAD_ATTR                cbbornt
             1052  LOAD_METHOD              currentIndex
             1054  CALL_METHOD_0         0  '0 positional arguments'
             1056  LOAD_CONST               0
             1058  COMPARE_OP               ==
         1060_1062  POP_JUMP_IF_FALSE  1088  'to 1088'

 L. 634      1064  LOAD_GLOBAL              int
             1066  LOAD_FAST                '_image_width'
             1068  LOAD_CONST               2
             1070  BINARY_TRUE_DIVIDE
             1072  CALL_FUNCTION_1       1  '1 positional argument'
             1074  STORE_FAST               '_wdxl'

 L. 635      1076  LOAD_GLOBAL              int
             1078  LOAD_FAST                '_image_height'
             1080  LOAD_CONST               2
             1082  BINARY_TRUE_DIVIDE
             1084  CALL_FUNCTION_1       1  '1 positional argument'
             1086  STORE_FAST               '_wdz'
           1088_0  COME_FROM          1060  '1060'

 L. 636      1088  LOAD_FAST                'self'
             1090  LOAD_ATTR                cbbornt
             1092  LOAD_METHOD              currentIndex
             1094  CALL_METHOD_0         0  '0 positional arguments'
             1096  LOAD_CONST               1
             1098  COMPARE_OP               ==
         1100_1102  POP_JUMP_IF_FALSE  1128  'to 1128'

 L. 637      1104  LOAD_GLOBAL              int
             1106  LOAD_FAST                '_image_width'
             1108  LOAD_CONST               2
             1110  BINARY_TRUE_DIVIDE
             1112  CALL_FUNCTION_1       1  '1 positional argument'
             1114  STORE_FAST               '_wdinl'

 L. 638      1116  LOAD_GLOBAL              int
             1118  LOAD_FAST                '_image_height'
             1120  LOAD_CONST               2
             1122  BINARY_TRUE_DIVIDE
             1124  CALL_FUNCTION_1       1  '1 positional argument'
             1126  STORE_FAST               '_wdz'
           1128_0  COME_FROM          1100  '1100'

 L. 639      1128  LOAD_FAST                'self'
             1130  LOAD_ATTR                cbbornt
             1132  LOAD_METHOD              currentIndex
             1134  CALL_METHOD_0         0  '0 positional arguments'
             1136  LOAD_CONST               2
             1138  COMPARE_OP               ==
         1140_1142  POP_JUMP_IF_FALSE  1168  'to 1168'

 L. 640      1144  LOAD_GLOBAL              int
             1146  LOAD_FAST                '_image_width'
             1148  LOAD_CONST               2
             1150  BINARY_TRUE_DIVIDE
             1152  CALL_FUNCTION_1       1  '1 positional argument'
             1154  STORE_FAST               '_wdinl'

 L. 641      1156  LOAD_GLOBAL              int
             1158  LOAD_FAST                '_image_height'
             1160  LOAD_CONST               2
             1162  BINARY_TRUE_DIVIDE
             1164  CALL_FUNCTION_1       1  '1 positional argument'
             1166  STORE_FAST               '_wdxl'
           1168_0  COME_FROM          1140  '1140'

 L. 643      1168  LOAD_FAST                'self'
             1170  LOAD_ATTR                survinfo
             1172  STORE_FAST               '_seisinfo'

 L. 645      1174  LOAD_GLOBAL              print
             1176  LOAD_STR                 'UpdateMl2DWcae: Step 1 - Get training samples:'
             1178  CALL_FUNCTION_1       1  '1 positional argument'
             1180  POP_TOP          

 L. 646      1182  LOAD_FAST                'self'
             1184  LOAD_ATTR                traindataconfig
             1186  LOAD_STR                 'TrainPointSet'
             1188  BINARY_SUBSCR    
             1190  STORE_FAST               '_trainpoint'

 L. 647      1192  LOAD_GLOBAL              np
             1194  LOAD_METHOD              zeros
             1196  LOAD_CONST               0
             1198  LOAD_CONST               3
             1200  BUILD_LIST_2          2 
             1202  CALL_METHOD_1         1  '1 positional argument'
             1204  STORE_FAST               '_traindata'

 L. 648      1206  SETUP_LOOP         1282  'to 1282'
             1208  LOAD_FAST                '_trainpoint'
             1210  GET_ITER         
           1212_0  COME_FROM          1230  '1230'
             1212  FOR_ITER           1280  'to 1280'
             1214  STORE_FAST               '_p'

 L. 649      1216  LOAD_GLOBAL              point_ays
             1218  LOAD_METHOD              checkPoint
             1220  LOAD_FAST                'self'
             1222  LOAD_ATTR                pointsetdata
             1224  LOAD_FAST                '_p'
             1226  BINARY_SUBSCR    
             1228  CALL_METHOD_1         1  '1 positional argument'
         1230_1232  POP_JUMP_IF_FALSE  1212  'to 1212'

 L. 650      1234  LOAD_GLOBAL              basic_mdt
             1236  LOAD_METHOD              exportMatDict
             1238  LOAD_FAST                'self'
             1240  LOAD_ATTR                pointsetdata
             1242  LOAD_FAST                '_p'
             1244  BINARY_SUBSCR    
             1246  LOAD_STR                 'Inline'
             1248  LOAD_STR                 'Crossline'
             1250  LOAD_STR                 'Z'
             1252  BUILD_LIST_3          3 
             1254  CALL_METHOD_2         2  '2 positional arguments'
             1256  STORE_FAST               '_pt'

 L. 651      1258  LOAD_GLOBAL              np
             1260  LOAD_ATTR                concatenate
             1262  LOAD_FAST                '_traindata'
             1264  LOAD_FAST                '_pt'
             1266  BUILD_TUPLE_2         2 
             1268  LOAD_CONST               0
             1270  LOAD_CONST               ('axis',)
             1272  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1274  STORE_FAST               '_traindata'
         1276_1278  JUMP_BACK          1212  'to 1212'
             1280  POP_BLOCK        
           1282_0  COME_FROM_LOOP     1206  '1206'

 L. 652      1282  LOAD_GLOBAL              seis_ays
             1284  LOAD_ATTR                removeOutofSurveySample
             1286  LOAD_FAST                '_traindata'

 L. 653      1288  LOAD_FAST                '_seisinfo'
             1290  LOAD_STR                 'ILStart'
             1292  BINARY_SUBSCR    
             1294  LOAD_FAST                '_wdinl'
             1296  LOAD_FAST                '_seisinfo'
             1298  LOAD_STR                 'ILStep'
             1300  BINARY_SUBSCR    
             1302  BINARY_MULTIPLY  
             1304  BINARY_ADD       

 L. 654      1306  LOAD_FAST                '_seisinfo'
             1308  LOAD_STR                 'ILEnd'
             1310  BINARY_SUBSCR    
             1312  LOAD_FAST                '_wdinl'
             1314  LOAD_FAST                '_seisinfo'
             1316  LOAD_STR                 'ILStep'
             1318  BINARY_SUBSCR    
             1320  BINARY_MULTIPLY  
             1322  BINARY_SUBTRACT  

 L. 655      1324  LOAD_FAST                '_seisinfo'
             1326  LOAD_STR                 'XLStart'
             1328  BINARY_SUBSCR    
             1330  LOAD_FAST                '_wdxl'
             1332  LOAD_FAST                '_seisinfo'
             1334  LOAD_STR                 'XLStep'
             1336  BINARY_SUBSCR    
             1338  BINARY_MULTIPLY  
             1340  BINARY_ADD       

 L. 656      1342  LOAD_FAST                '_seisinfo'
             1344  LOAD_STR                 'XLEnd'
             1346  BINARY_SUBSCR    
             1348  LOAD_FAST                '_wdxl'
             1350  LOAD_FAST                '_seisinfo'
             1352  LOAD_STR                 'XLStep'
             1354  BINARY_SUBSCR    
             1356  BINARY_MULTIPLY  
             1358  BINARY_SUBTRACT  

 L. 657      1360  LOAD_FAST                '_seisinfo'
             1362  LOAD_STR                 'ZStart'
             1364  BINARY_SUBSCR    
             1366  LOAD_FAST                '_wdz'
             1368  LOAD_FAST                '_seisinfo'
             1370  LOAD_STR                 'ZStep'
             1372  BINARY_SUBSCR    
             1374  BINARY_MULTIPLY  
             1376  BINARY_ADD       

 L. 658      1378  LOAD_FAST                '_seisinfo'
             1380  LOAD_STR                 'ZEnd'
             1382  BINARY_SUBSCR    
             1384  LOAD_FAST                '_wdz'
             1386  LOAD_FAST                '_seisinfo'
             1388  LOAD_STR                 'ZStep'
             1390  BINARY_SUBSCR    
             1392  BINARY_MULTIPLY  
             1394  BINARY_SUBTRACT  
             1396  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1398  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1400  STORE_FAST               '_traindata'

 L. 661      1402  LOAD_GLOBAL              np
             1404  LOAD_METHOD              shape
             1406  LOAD_FAST                '_traindata'
             1408  CALL_METHOD_1         1  '1 positional argument'
             1410  LOAD_CONST               0
             1412  BINARY_SUBSCR    
             1414  LOAD_CONST               0
             1416  COMPARE_OP               <=
         1418_1420  POP_JUMP_IF_FALSE  1458  'to 1458'

 L. 662      1422  LOAD_GLOBAL              vis_msg
             1424  LOAD_ATTR                print
             1426  LOAD_STR                 'ERROR in UpdateMl2DWcae: No training sample found'
             1428  LOAD_STR                 'error'
             1430  LOAD_CONST               ('type',)
             1432  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1434  POP_TOP          

 L. 663      1436  LOAD_GLOBAL              QtWidgets
             1438  LOAD_ATTR                QMessageBox
             1440  LOAD_METHOD              critical
             1442  LOAD_FAST                'self'
             1444  LOAD_ATTR                msgbox

 L. 664      1446  LOAD_STR                 'Update 2D-WCAE'

 L. 665      1448  LOAD_STR                 'No training sample found'
             1450  CALL_METHOD_3         3  '3 positional arguments'
             1452  POP_TOP          

 L. 666      1454  LOAD_CONST               None
             1456  RETURN_VALUE     
           1458_0  COME_FROM          1418  '1418'

 L. 669      1458  LOAD_GLOBAL              print
             1460  LOAD_STR                 'UpdateMl2DWcae: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 670      1462  LOAD_FAST                '_image_height'
             1464  LOAD_FAST                '_image_width'
             1466  LOAD_FAST                '_image_height_new'
             1468  LOAD_FAST                '_image_width_new'
             1470  BUILD_TUPLE_4         4 
             1472  BINARY_MODULO    
             1474  CALL_FUNCTION_1       1  '1 positional argument'
             1476  POP_TOP          

 L. 671      1478  BUILD_MAP_0           0 
             1480  STORE_FAST               '_traindict'

 L. 672      1482  SETUP_LOOP         1554  'to 1554'
             1484  LOAD_FAST                '_features'
             1486  GET_ITER         
             1488  FOR_ITER           1552  'to 1552'
             1490  STORE_FAST               'f'

 L. 673      1492  LOAD_FAST                'self'
             1494  LOAD_ATTR                seisdata
             1496  LOAD_FAST                'f'
             1498  BINARY_SUBSCR    
             1500  STORE_FAST               '_seisdata'

 L. 674      1502  LOAD_GLOBAL              seis_ays
             1504  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1506  LOAD_FAST                '_seisdata'
             1508  LOAD_FAST                '_traindata'
             1510  LOAD_FAST                'self'
             1512  LOAD_ATTR                survinfo

 L. 675      1514  LOAD_FAST                '_wdinl'
             1516  LOAD_FAST                '_wdxl'
             1518  LOAD_FAST                '_wdz'

 L. 676      1520  LOAD_CONST               False
             1522  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1524  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1526  LOAD_CONST               None
             1528  LOAD_CONST               None
             1530  BUILD_SLICE_2         2 
             1532  LOAD_CONST               3
             1534  LOAD_CONST               None
             1536  BUILD_SLICE_2         2 
             1538  BUILD_TUPLE_2         2 
             1540  BINARY_SUBSCR    
             1542  LOAD_FAST                '_traindict'
             1544  LOAD_FAST                'f'
             1546  STORE_SUBSCR     
         1548_1550  JUMP_BACK          1488  'to 1488'
             1552  POP_BLOCK        
           1554_0  COME_FROM_LOOP     1482  '1482'

 L. 677      1554  LOAD_FAST                '_target'
             1556  LOAD_FAST                '_features'
             1558  COMPARE_OP               not-in
         1560_1562  POP_JUMP_IF_FALSE  1620  'to 1620'

 L. 678      1564  LOAD_FAST                'self'
             1566  LOAD_ATTR                seisdata
             1568  LOAD_FAST                '_target'
             1570  BINARY_SUBSCR    
             1572  STORE_FAST               '_seisdata'

 L. 679      1574  LOAD_GLOBAL              seis_ays
             1576  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1578  LOAD_FAST                '_seisdata'
             1580  LOAD_FAST                '_traindata'
             1582  LOAD_FAST                'self'
             1584  LOAD_ATTR                survinfo

 L. 680      1586  LOAD_FAST                '_wdinl'
             1588  LOAD_FAST                '_wdxl'
             1590  LOAD_FAST                '_wdz'

 L. 681      1592  LOAD_CONST               False
             1594  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1596  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1598  LOAD_CONST               None
             1600  LOAD_CONST               None
             1602  BUILD_SLICE_2         2 
             1604  LOAD_CONST               3
             1606  LOAD_CONST               None
             1608  BUILD_SLICE_2         2 
             1610  BUILD_TUPLE_2         2 
             1612  BINARY_SUBSCR    
             1614  LOAD_FAST                '_traindict'
             1616  LOAD_FAST                '_target'
             1618  STORE_SUBSCR     
           1620_0  COME_FROM          1560  '1560'

 L. 682      1620  LOAD_FAST                '_weight'
             1622  LOAD_FAST                '_features'
             1624  COMPARE_OP               not-in
         1626_1628  POP_JUMP_IF_FALSE  1696  'to 1696'
             1630  LOAD_FAST                '_weight'
             1632  LOAD_FAST                '_target'
             1634  COMPARE_OP               !=
         1636_1638  POP_JUMP_IF_FALSE  1696  'to 1696'

 L. 683      1640  LOAD_FAST                'self'
             1642  LOAD_ATTR                seisdata
             1644  LOAD_FAST                '_weight'
             1646  BINARY_SUBSCR    
             1648  STORE_FAST               '_seisdata'

 L. 684      1650  LOAD_GLOBAL              seis_ays
             1652  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1654  LOAD_FAST                '_seisdata'
             1656  LOAD_FAST                '_traindata'
             1658  LOAD_FAST                'self'
             1660  LOAD_ATTR                survinfo

 L. 685      1662  LOAD_FAST                '_wdinl'
             1664  LOAD_FAST                '_wdxl'
             1666  LOAD_FAST                '_wdz'

 L. 686      1668  LOAD_CONST               False
             1670  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1672  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1674  LOAD_CONST               None
             1676  LOAD_CONST               None
             1678  BUILD_SLICE_2         2 
             1680  LOAD_CONST               3
             1682  LOAD_CONST               None
             1684  BUILD_SLICE_2         2 
             1686  BUILD_TUPLE_2         2 
             1688  BINARY_SUBSCR    
             1690  LOAD_FAST                '_traindict'
             1692  LOAD_FAST                '_weight'
             1694  STORE_SUBSCR     
           1696_0  COME_FROM          1636  '1636'
           1696_1  COME_FROM          1626  '1626'

 L. 687      1696  LOAD_FAST                'self'
             1698  LOAD_ATTR                traindataconfig
             1700  LOAD_STR                 'RemoveInvariantFeature_Checked'
             1702  BINARY_SUBSCR    
         1704_1706  POP_JUMP_IF_FALSE  1788  'to 1788'

 L. 688      1708  SETUP_LOOP         1788  'to 1788'
             1710  LOAD_FAST                '_features'
             1712  GET_ITER         
           1714_0  COME_FROM          1742  '1742'
             1714  FOR_ITER           1786  'to 1786'
             1716  STORE_FAST               'f'

 L. 689      1718  LOAD_GLOBAL              ml_aug
             1720  LOAD_METHOD              removeInvariantFeature
             1722  LOAD_FAST                '_traindict'
             1724  LOAD_FAST                'f'
             1726  CALL_METHOD_2         2  '2 positional arguments'
             1728  STORE_FAST               '_traindict'

 L. 690      1730  LOAD_GLOBAL              basic_mdt
             1732  LOAD_METHOD              maxDictConstantRow
             1734  LOAD_FAST                '_traindict'
             1736  CALL_METHOD_1         1  '1 positional argument'
             1738  LOAD_CONST               0
             1740  COMPARE_OP               <=
         1742_1744  POP_JUMP_IF_FALSE  1714  'to 1714'

 L. 691      1746  LOAD_GLOBAL              vis_msg
             1748  LOAD_ATTR                print
             1750  LOAD_STR                 'ERROR in UpdateMl2DWcae: No training sample found'
             1752  LOAD_STR                 'error'
             1754  LOAD_CONST               ('type',)
             1756  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1758  POP_TOP          

 L. 692      1760  LOAD_GLOBAL              QtWidgets
             1762  LOAD_ATTR                QMessageBox
             1764  LOAD_METHOD              critical
             1766  LOAD_FAST                'self'
             1768  LOAD_ATTR                msgbox

 L. 693      1770  LOAD_STR                 'Update 2D-WCAE'

 L. 694      1772  LOAD_STR                 'No training sample found'
             1774  CALL_METHOD_3         3  '3 positional arguments'
             1776  POP_TOP          

 L. 695      1778  LOAD_CONST               None
             1780  RETURN_VALUE     
         1782_1784  JUMP_BACK          1714  'to 1714'
             1786  POP_BLOCK        
           1788_0  COME_FROM_LOOP     1708  '1708'
           1788_1  COME_FROM          1704  '1704'

 L. 696      1788  LOAD_FAST                'self'
             1790  LOAD_ATTR                traindataconfig
             1792  LOAD_STR                 'RemoveZeroWeight_Checked'
             1794  BINARY_SUBSCR    
         1796_1798  POP_JUMP_IF_FALSE  1864  'to 1864'

 L. 697      1800  LOAD_GLOBAL              ml_aug
             1802  LOAD_METHOD              removeZeroWeight
             1804  LOAD_FAST                '_traindict'
             1806  LOAD_FAST                '_weight'
             1808  CALL_METHOD_2         2  '2 positional arguments'
             1810  STORE_FAST               '_traindict'

 L. 698      1812  LOAD_GLOBAL              basic_mdt
             1814  LOAD_METHOD              maxDictConstantRow
             1816  LOAD_FAST                '_traindict'
             1818  CALL_METHOD_1         1  '1 positional argument'
             1820  LOAD_CONST               0
             1822  COMPARE_OP               <=
         1824_1826  POP_JUMP_IF_FALSE  1864  'to 1864'

 L. 699      1828  LOAD_GLOBAL              vis_msg
             1830  LOAD_ATTR                print
             1832  LOAD_STR                 'ERROR in UpdateMl2DWcae: No training sample found'
             1834  LOAD_STR                 'error'
             1836  LOAD_CONST               ('type',)
             1838  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1840  POP_TOP          

 L. 700      1842  LOAD_GLOBAL              QtWidgets
             1844  LOAD_ATTR                QMessageBox
             1846  LOAD_METHOD              critical
             1848  LOAD_FAST                'self'
             1850  LOAD_ATTR                msgbox

 L. 701      1852  LOAD_STR                 'Update 2D-WCAE'

 L. 702      1854  LOAD_STR                 'No training sample found'
             1856  CALL_METHOD_3         3  '3 positional arguments'
             1858  POP_TOP          

 L. 703      1860  LOAD_CONST               None
             1862  RETURN_VALUE     
           1864_0  COME_FROM          1824  '1824'
           1864_1  COME_FROM          1796  '1796'

 L. 705      1864  LOAD_GLOBAL              np
             1866  LOAD_METHOD              shape
             1868  LOAD_FAST                '_traindict'
             1870  LOAD_FAST                '_target'
             1872  BINARY_SUBSCR    
             1874  CALL_METHOD_1         1  '1 positional argument'
             1876  LOAD_CONST               0
             1878  BINARY_SUBSCR    
             1880  LOAD_CONST               0
             1882  COMPARE_OP               <=
         1884_1886  POP_JUMP_IF_FALSE  1924  'to 1924'

 L. 706      1888  LOAD_GLOBAL              vis_msg
             1890  LOAD_ATTR                print
             1892  LOAD_STR                 'ERROR in UpdateMl2DWcae: No training sample found'
             1894  LOAD_STR                 'error'
             1896  LOAD_CONST               ('type',)
             1898  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1900  POP_TOP          

 L. 707      1902  LOAD_GLOBAL              QtWidgets
             1904  LOAD_ATTR                QMessageBox
             1906  LOAD_METHOD              critical
             1908  LOAD_FAST                'self'
             1910  LOAD_ATTR                msgbox

 L. 708      1912  LOAD_STR                 'Update 2D-WCAE'

 L. 709      1914  LOAD_STR                 'No training sample found'
             1916  CALL_METHOD_3         3  '3 positional arguments'
             1918  POP_TOP          

 L. 710      1920  LOAD_CONST               None
             1922  RETURN_VALUE     
           1924_0  COME_FROM          1884  '1884'

 L. 712      1924  LOAD_FAST                '_image_height_new'
             1926  LOAD_FAST                '_image_height'
             1928  COMPARE_OP               !=
         1930_1932  POP_JUMP_IF_TRUE   1944  'to 1944'
             1934  LOAD_FAST                '_image_width_new'
             1936  LOAD_FAST                '_image_width'
             1938  COMPARE_OP               !=
         1940_1942  POP_JUMP_IF_FALSE  2078  'to 2078'
           1944_0  COME_FROM          1930  '1930'

 L. 713      1944  SETUP_LOOP         1988  'to 1988'
             1946  LOAD_FAST                '_features'
             1948  GET_ITER         
             1950  FOR_ITER           1986  'to 1986'
             1952  STORE_FAST               'f'

 L. 714      1954  LOAD_GLOBAL              basic_image
             1956  LOAD_ATTR                changeImageSize
             1958  LOAD_FAST                '_traindict'
             1960  LOAD_FAST                'f'
             1962  BINARY_SUBSCR    

 L. 715      1964  LOAD_FAST                '_image_height'

 L. 716      1966  LOAD_FAST                '_image_width'

 L. 717      1968  LOAD_FAST                '_image_height_new'

 L. 718      1970  LOAD_FAST                '_image_width_new'
             1972  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1974  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1976  LOAD_FAST                '_traindict'
             1978  LOAD_FAST                'f'
             1980  STORE_SUBSCR     
         1982_1984  JUMP_BACK          1950  'to 1950'
             1986  POP_BLOCK        
           1988_0  COME_FROM_LOOP     1944  '1944'

 L. 719      1988  LOAD_FAST                '_target'
             1990  LOAD_FAST                '_features'
             1992  COMPARE_OP               not-in
         1994_1996  POP_JUMP_IF_FALSE  2028  'to 2028'

 L. 720      1998  LOAD_GLOBAL              basic_image
             2000  LOAD_ATTR                changeImageSize
             2002  LOAD_FAST                '_traindict'
             2004  LOAD_FAST                '_target'
             2006  BINARY_SUBSCR    

 L. 721      2008  LOAD_FAST                '_image_height'

 L. 722      2010  LOAD_FAST                '_image_width'

 L. 723      2012  LOAD_FAST                '_image_height_new'

 L. 724      2014  LOAD_FAST                '_image_width_new'
             2016  LOAD_STR                 'linear'
             2018  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2020  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2022  LOAD_FAST                '_traindict'
             2024  LOAD_FAST                '_target'
             2026  STORE_SUBSCR     
           2028_0  COME_FROM          1994  '1994'

 L. 725      2028  LOAD_FAST                '_weight'
             2030  LOAD_FAST                '_features'
             2032  COMPARE_OP               not-in
         2034_2036  POP_JUMP_IF_FALSE  2078  'to 2078'
             2038  LOAD_FAST                '_weight'
             2040  LOAD_FAST                '_target'
             2042  COMPARE_OP               !=
         2044_2046  POP_JUMP_IF_FALSE  2078  'to 2078'

 L. 726      2048  LOAD_GLOBAL              basic_image
             2050  LOAD_ATTR                changeImageSize
             2052  LOAD_FAST                '_traindict'
             2054  LOAD_FAST                '_weight'
             2056  BINARY_SUBSCR    

 L. 727      2058  LOAD_FAST                '_image_height'

 L. 728      2060  LOAD_FAST                '_image_width'

 L. 729      2062  LOAD_FAST                '_image_height_new'

 L. 730      2064  LOAD_FAST                '_image_width_new'
             2066  LOAD_STR                 'linear'
             2068  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2070  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2072  LOAD_FAST                '_traindict'
             2074  LOAD_FAST                '_weight'
             2076  STORE_SUBSCR     
           2078_0  COME_FROM          2044  '2044'
           2078_1  COME_FROM          2034  '2034'
           2078_2  COME_FROM          1940  '1940'

 L. 731      2078  LOAD_FAST                'self'
             2080  LOAD_ATTR                traindataconfig
             2082  LOAD_STR                 'RotateFeature_Checked'
             2084  BINARY_SUBSCR    
             2086  LOAD_CONST               True
             2088  COMPARE_OP               is
         2090_2092  POP_JUMP_IF_FALSE  2308  'to 2308'

 L. 732      2094  SETUP_LOOP         2166  'to 2166'
             2096  LOAD_FAST                '_features'
             2098  GET_ITER         
             2100  FOR_ITER           2164  'to 2164'
             2102  STORE_FAST               'f'

 L. 733      2104  LOAD_FAST                '_image_height_new'
             2106  LOAD_FAST                '_image_width_new'
             2108  COMPARE_OP               ==
         2110_2112  POP_JUMP_IF_FALSE  2138  'to 2138'

 L. 734      2114  LOAD_GLOBAL              ml_aug
             2116  LOAD_METHOD              rotateImage6Way
             2118  LOAD_FAST                '_traindict'
             2120  LOAD_FAST                'f'
             2122  BINARY_SUBSCR    
             2124  LOAD_FAST                '_image_height_new'
             2126  LOAD_FAST                '_image_width_new'
             2128  CALL_METHOD_3         3  '3 positional arguments'
             2130  LOAD_FAST                '_traindict'
             2132  LOAD_FAST                'f'
             2134  STORE_SUBSCR     
             2136  JUMP_BACK          2100  'to 2100'
           2138_0  COME_FROM          2110  '2110'

 L. 736      2138  LOAD_GLOBAL              ml_aug
             2140  LOAD_METHOD              rotateImage4Way
             2142  LOAD_FAST                '_traindict'
             2144  LOAD_FAST                'f'
             2146  BINARY_SUBSCR    
             2148  LOAD_FAST                '_image_height_new'
             2150  LOAD_FAST                '_image_width_new'
             2152  CALL_METHOD_3         3  '3 positional arguments'
             2154  LOAD_FAST                '_traindict'
             2156  LOAD_FAST                'f'
             2158  STORE_SUBSCR     
         2160_2162  JUMP_BACK          2100  'to 2100'
             2164  POP_BLOCK        
           2166_0  COME_FROM_LOOP     2094  '2094'

 L. 737      2166  LOAD_FAST                '_target'
             2168  LOAD_FAST                '_features'
             2170  COMPARE_OP               not-in
         2172_2174  POP_JUMP_IF_FALSE  2232  'to 2232'

 L. 738      2176  LOAD_FAST                '_image_height_new'
             2178  LOAD_FAST                '_image_width_new'
             2180  COMPARE_OP               ==
         2182_2184  POP_JUMP_IF_FALSE  2210  'to 2210'

 L. 740      2186  LOAD_GLOBAL              ml_aug
             2188  LOAD_METHOD              rotateImage6Way
             2190  LOAD_FAST                '_traindict'
             2192  LOAD_FAST                '_target'
             2194  BINARY_SUBSCR    
             2196  LOAD_FAST                '_image_height_new'
             2198  LOAD_FAST                '_image_width_new'
             2200  CALL_METHOD_3         3  '3 positional arguments'
             2202  LOAD_FAST                '_traindict'
             2204  LOAD_FAST                '_target'
             2206  STORE_SUBSCR     
             2208  JUMP_FORWARD       2232  'to 2232'
           2210_0  COME_FROM          2182  '2182'

 L. 743      2210  LOAD_GLOBAL              ml_aug
             2212  LOAD_METHOD              rotateImage4Way
             2214  LOAD_FAST                '_traindict'
             2216  LOAD_FAST                '_target'
             2218  BINARY_SUBSCR    
             2220  LOAD_FAST                '_image_height_new'
             2222  LOAD_FAST                '_image_width_new'
             2224  CALL_METHOD_3         3  '3 positional arguments'
             2226  LOAD_FAST                '_traindict'
             2228  LOAD_FAST                '_target'
             2230  STORE_SUBSCR     
           2232_0  COME_FROM          2208  '2208'
           2232_1  COME_FROM          2172  '2172'

 L. 744      2232  LOAD_FAST                '_weight'
             2234  LOAD_FAST                '_features'
             2236  COMPARE_OP               not-in
         2238_2240  POP_JUMP_IF_FALSE  2308  'to 2308'
             2242  LOAD_FAST                '_weight'
             2244  LOAD_FAST                '_target'
             2246  COMPARE_OP               !=
         2248_2250  POP_JUMP_IF_FALSE  2308  'to 2308'

 L. 745      2252  LOAD_FAST                '_image_height_new'
             2254  LOAD_FAST                '_image_width_new'
             2256  COMPARE_OP               ==
         2258_2260  POP_JUMP_IF_FALSE  2286  'to 2286'

 L. 747      2262  LOAD_GLOBAL              ml_aug
             2264  LOAD_METHOD              rotateImage6Way
             2266  LOAD_FAST                '_traindict'
             2268  LOAD_FAST                '_weight'
             2270  BINARY_SUBSCR    
             2272  LOAD_FAST                '_image_height_new'
             2274  LOAD_FAST                '_image_width_new'
             2276  CALL_METHOD_3         3  '3 positional arguments'
             2278  LOAD_FAST                '_traindict'
             2280  LOAD_FAST                '_weight'
             2282  STORE_SUBSCR     
             2284  JUMP_FORWARD       2308  'to 2308'
           2286_0  COME_FROM          2258  '2258'

 L. 750      2286  LOAD_GLOBAL              ml_aug
             2288  LOAD_METHOD              rotateImage4Way
             2290  LOAD_FAST                '_traindict'
             2292  LOAD_FAST                '_weight'
             2294  BINARY_SUBSCR    
             2296  LOAD_FAST                '_image_height_new'
             2298  LOAD_FAST                '_image_width_new'
             2300  CALL_METHOD_3         3  '3 positional arguments'
             2302  LOAD_FAST                '_traindict'
             2304  LOAD_FAST                '_weight'
             2306  STORE_SUBSCR     
           2308_0  COME_FROM          2284  '2284'
           2308_1  COME_FROM          2248  '2248'
           2308_2  COME_FROM          2238  '2238'
           2308_3  COME_FROM          2090  '2090'

 L. 753      2308  LOAD_GLOBAL              print
             2310  LOAD_STR                 'UpdateMl2DWcae: A total of %d valid training samples'
             2312  LOAD_GLOBAL              basic_mdt
             2314  LOAD_METHOD              maxDictConstantRow
             2316  LOAD_FAST                '_traindict'
             2318  CALL_METHOD_1         1  '1 positional argument'
             2320  BINARY_MODULO    
             2322  CALL_FUNCTION_1       1  '1 positional argument'
             2324  POP_TOP          

 L. 755      2326  LOAD_GLOBAL              print
             2328  LOAD_STR                 'UpdateMl2DWcae: Step 3 - Start training'
             2330  CALL_FUNCTION_1       1  '1 positional argument'
             2332  POP_TOP          

 L. 757      2334  LOAD_GLOBAL              QtWidgets
             2336  LOAD_METHOD              QProgressDialog
             2338  CALL_METHOD_0         0  '0 positional arguments'
             2340  STORE_FAST               '_pgsdlg'

 L. 758      2342  LOAD_GLOBAL              QtGui
             2344  LOAD_METHOD              QIcon
             2346  CALL_METHOD_0         0  '0 positional arguments'
             2348  STORE_FAST               'icon'

 L. 759      2350  LOAD_FAST                'icon'
             2352  LOAD_METHOD              addPixmap
             2354  LOAD_GLOBAL              QtGui
             2356  LOAD_METHOD              QPixmap
             2358  LOAD_GLOBAL              os
             2360  LOAD_ATTR                path
             2362  LOAD_METHOD              join
             2364  LOAD_FAST                'self'
             2366  LOAD_ATTR                iconpath
             2368  LOAD_STR                 'icons/update.png'
             2370  CALL_METHOD_2         2  '2 positional arguments'
             2372  CALL_METHOD_1         1  '1 positional argument'

 L. 760      2374  LOAD_GLOBAL              QtGui
             2376  LOAD_ATTR                QIcon
             2378  LOAD_ATTR                Normal
             2380  LOAD_GLOBAL              QtGui
             2382  LOAD_ATTR                QIcon
             2384  LOAD_ATTR                Off
             2386  CALL_METHOD_3         3  '3 positional arguments'
             2388  POP_TOP          

 L. 761      2390  LOAD_FAST                '_pgsdlg'
             2392  LOAD_METHOD              setWindowIcon
             2394  LOAD_FAST                'icon'
             2396  CALL_METHOD_1         1  '1 positional argument'
             2398  POP_TOP          

 L. 762      2400  LOAD_FAST                '_pgsdlg'
             2402  LOAD_METHOD              setWindowTitle
             2404  LOAD_STR                 'Update 2D-CAE'
             2406  CALL_METHOD_1         1  '1 positional argument'
             2408  POP_TOP          

 L. 763      2410  LOAD_FAST                '_pgsdlg'
             2412  LOAD_METHOD              setCancelButton
             2414  LOAD_CONST               None
             2416  CALL_METHOD_1         1  '1 positional argument'
             2418  POP_TOP          

 L. 764      2420  LOAD_FAST                '_pgsdlg'
             2422  LOAD_METHOD              setWindowFlags
             2424  LOAD_GLOBAL              QtCore
             2426  LOAD_ATTR                Qt
             2428  LOAD_ATTR                WindowStaysOnTopHint
             2430  CALL_METHOD_1         1  '1 positional argument'
             2432  POP_TOP          

 L. 765      2434  LOAD_FAST                '_pgsdlg'
             2436  LOAD_METHOD              forceShow
             2438  CALL_METHOD_0         0  '0 positional arguments'
             2440  POP_TOP          

 L. 766      2442  LOAD_FAST                '_pgsdlg'
             2444  LOAD_METHOD              setFixedWidth
             2446  LOAD_CONST               400
             2448  CALL_METHOD_1         1  '1 positional argument'
             2450  POP_TOP          

 L. 767      2452  LOAD_GLOBAL              ml_wcae
             2454  LOAD_ATTR                updateWCAEReconstructor
             2456  LOAD_FAST                '_traindict'

 L. 768      2458  LOAD_FAST                '_image_height_new'
             2460  LOAD_FAST                '_image_width_new'

 L. 769      2462  LOAD_FAST                '_nepoch'
             2464  LOAD_FAST                '_batchsize'

 L. 770      2466  LOAD_FAST                '_learning_rate'

 L. 771      2468  LOAD_FAST                '_dropout_prob'

 L. 772      2470  LOAD_FAST                'self'
             2472  LOAD_ATTR                modelpath
             2474  LOAD_FAST                'self'
             2476  LOAD_ATTR                modelname

 L. 773      2478  LOAD_CONST               True

 L. 774      2480  LOAD_FAST                '_savepath'
             2482  LOAD_FAST                '_savename'

 L. 775      2484  LOAD_FAST                '_pgsdlg'
             2486  LOAD_CONST               ('imageheight', 'imagewidth', 'nepoch', 'batchsize', 'learningrate', 'dropoutprob', 'wcaepath', 'wcaename', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2488  CALL_FUNCTION_KW_13    13  '13 total positional and keyword args'
             2490  STORE_FAST               '_caelog'

 L. 777      2492  LOAD_GLOBAL              QtWidgets
             2494  LOAD_ATTR                QMessageBox
             2496  LOAD_METHOD              information
             2498  LOAD_FAST                'self'
             2500  LOAD_ATTR                msgbox

 L. 778      2502  LOAD_STR                 'Update 2D-WCAE'

 L. 779      2504  LOAD_STR                 'WCAE updated successfully'
             2506  CALL_METHOD_3         3  '3 positional arguments'
             2508  POP_TOP          

 L. 781      2510  LOAD_GLOBAL              QtWidgets
             2512  LOAD_ATTR                QMessageBox
             2514  LOAD_METHOD              question
             2516  LOAD_FAST                'self'
             2518  LOAD_ATTR                msgbox
             2520  LOAD_STR                 'Update 2D-WCAE'
             2522  LOAD_STR                 'View learning matrix?'

 L. 782      2524  LOAD_GLOBAL              QtWidgets
             2526  LOAD_ATTR                QMessageBox
             2528  LOAD_ATTR                Yes
             2530  LOAD_GLOBAL              QtWidgets
             2532  LOAD_ATTR                QMessageBox
             2534  LOAD_ATTR                No
             2536  BINARY_OR        

 L. 783      2538  LOAD_GLOBAL              QtWidgets
             2540  LOAD_ATTR                QMessageBox
             2542  LOAD_ATTR                Yes
             2544  CALL_METHOD_5         5  '5 positional arguments'
             2546  STORE_FAST               'reply'

 L. 785      2548  LOAD_FAST                'reply'
             2550  LOAD_GLOBAL              QtWidgets
             2552  LOAD_ATTR                QMessageBox
             2554  LOAD_ATTR                Yes
             2556  COMPARE_OP               ==
         2558_2560  POP_JUMP_IF_FALSE  2628  'to 2628'

 L. 786      2562  LOAD_GLOBAL              QtWidgets
             2564  LOAD_METHOD              QDialog
             2566  CALL_METHOD_0         0  '0 positional arguments'
             2568  STORE_FAST               '_viewmllearnmat'

 L. 787      2570  LOAD_GLOBAL              gui_viewmllearnmat
             2572  CALL_FUNCTION_0       0  '0 positional arguments'
             2574  STORE_FAST               '_gui'

 L. 788      2576  LOAD_FAST                '_caelog'
             2578  LOAD_STR                 'learning_curve'
             2580  BINARY_SUBSCR    
             2582  LOAD_FAST                '_gui'
             2584  STORE_ATTR               learnmat

 L. 789      2586  LOAD_FAST                'self'
             2588  LOAD_ATTR                linestyle
             2590  LOAD_FAST                '_gui'
             2592  STORE_ATTR               linestyle

 L. 790      2594  LOAD_FAST                'self'
             2596  LOAD_ATTR                fontstyle
             2598  LOAD_FAST                '_gui'
             2600  STORE_ATTR               fontstyle

 L. 791      2602  LOAD_FAST                '_gui'
             2604  LOAD_METHOD              setupGUI
             2606  LOAD_FAST                '_viewmllearnmat'
             2608  CALL_METHOD_1         1  '1 positional argument'
             2610  POP_TOP          

 L. 792      2612  LOAD_FAST                '_viewmllearnmat'
             2614  LOAD_METHOD              exec
             2616  CALL_METHOD_0         0  '0 positional arguments'
             2618  POP_TOP          

 L. 793      2620  LOAD_FAST                '_viewmllearnmat'
             2622  LOAD_METHOD              show
             2624  CALL_METHOD_0         0  '0 positional arguments'
             2626  POP_TOP          
           2628_0  COME_FROM          2558  '2558'

Parse error at or near `POP_TOP' instruction at offset 2626

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
    UpdateMl2DWcae = QtWidgets.QWidget()
    gui = updateml2dwcae()
    gui.setupGUI(UpdateMl2DWcae)
    UpdateMl2DWcae.show()
    sys.exit(app.exec_())