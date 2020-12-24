# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\updateml2dcae.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 41994 bytes
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
import cognitivegeo.src.ml.caereconstructor as ml_cae
import cognitivegeo.src.gui.viewml2dcae as gui_viewml2dcae
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class updateml2dcae(object):
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

    def setupGUI(self, UpdateMl2DCae):
        UpdateMl2DCae.setObjectName('UpdateMl2DCae')
        UpdateMl2DCae.setFixedSize(810, 550)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UpdateMl2DCae.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(UpdateMl2DCae)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(UpdateMl2DCae)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(UpdateMl2DCae)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(UpdateMl2DCae)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 230, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(UpdateMl2DCae)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 230, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 230, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(UpdateMl2DCae)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 270, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 270, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 230, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lbltarget = QtWidgets.QLabel(UpdateMl2DCae)
        self.lbltarget.setObjectName('lbltargete')
        self.lbltarget.setGeometry(QtCore.QRect(10, 320, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(UpdateMl2DCae)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 320, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(UpdateMl2DCae)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(UpdateMl2DCae)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 210))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(UpdateMl2DCae)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(UpdateMl2DCae)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 210))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 360, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 360, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 400, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 400, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 360, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 360, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 360, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 400, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 400, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(UpdateMl2DCae)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 370, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 370, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 410, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 410, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 410, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 410, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(UpdateMl2DCae)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 450, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 450, 40, 30))
        self.lbldropout = QtWidgets.QLabel(UpdateMl2DCae)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 450, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 450, 40, 30))
        self.lblsave = QtWidgets.QLabel(UpdateMl2DCae)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 500, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(UpdateMl2DCae)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 500, 180, 30))
        self.btnsave = QtWidgets.QPushButton(UpdateMl2DCae)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 500, 60, 30))
        self.btnapply = QtWidgets.QPushButton(UpdateMl2DCae)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 500, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(UpdateMl2DCae)
        self.msgbox.setObjectName('msgbox')
        _center_x = UpdateMl2DCae.geometry().center().x()
        _center_y = UpdateMl2DCae.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(UpdateMl2DCae)
        QtCore.QMetaObject.connectSlotsByName(UpdateMl2DCae)

    def retranslateGUI(self, UpdateMl2DCae):
        self.dialog = UpdateMl2DCae
        _translate = QtCore.QCoreApplication.translate
        UpdateMl2DCae.setWindowTitle(_translate('UpdateMl2DCae', 'Update 2D-CAE'))
        self.lblfrom.setText(_translate('UpdateMl2DCae', 'Select network:'))
        self.ldtfrom.setText(_translate('UpdateMl2DCae', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('UpdateMl2DCae', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('UpdateMl2DCae', 'Training features:'))
        self.lblornt.setText(_translate('UpdateMl2DCae', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('UpdateMl2DCae', 'Training target:'))
        self.btnconfigtraindata.setText(_translate('TrainMl2DDcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('UpdateMl2DCae', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('UpdateMl2DCae', 'height='))
        self.ldtoldheight.setText(_translate('UpdateMl2DCae', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('UpdateMl2DCae', 'width='))
        self.ldtoldwidth.setText(_translate('UpdateMl2DCae', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('UpdateMl2DCae', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('UpdateMl2DCae', 'height='))
        self.ldtnewheight.setText(_translate('UpdateMl2DCae', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('UpdateMl2DCae', 'width='))
        self.ldtnewwidth.setText(_translate('UpdateMl2DCae', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('UpdateMl2DCae', 'Pre-trained CAE architecture:'))
        self.btnviewnetwork.setText(_translate('UpdateMl2DCae', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('UpdateMl2DCae', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('UpdateMl2DCae', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('UpdateMl2DCae', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('UpdateMl2DCae', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('UpdateMl2DCae', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('UpdateMl2DCae', 'height='))
        self.ldtmaskheight.setText(_translate('UpdateMl2DCae', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('UpdateMl2DCae', 'width='))
        self.ldtmaskwidth.setText(_translate('UpdateMl2DCae', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('UpdateMl2DCae', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('UpdateMl2DCae', 'height='))
        self.ldtpoolheight.setText(_translate('UpdateMl2DCae', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('UpdateMl2DCae', 'width='))
        self.ldtpoolwidth.setText(_translate('UpdateMl2DCae', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('UpdateMl2DCae', 'Specify update parameters:'))
        self.lblnepoch.setText(_translate('UpdateMl2DCae', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('UpdateMl2DCae', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('UpdateMl2DCae', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('UpdateMl2DCae', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('UpdateMl2DCae', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('UpdateMl2DCae', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('UpdateMl2DCae', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('UpdateMl2DCae', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('UpdateMl2DCae', 'Save new-CAE to:'))
        self.ldtsave.setText(_translate('UpdateMl2DCae', ''))
        self.btnsave.setText(_translate('UpdateMl2DCae', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('UpdateMl2DCae', 'Update 2D-CAE'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnUpdateMl2DCae)

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.checkCAEModel(self.modelpath, self.modelname) is True:
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
        _file = _dialog.getOpenFileName(None, 'Select CAE Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def clickBtnViewNetwork(self):
        _viewmlcae = QtWidgets.QDialog()
        _gui = gui_viewml2dcae()
        _gui.linestyle = self.linestyle
        _gui.maskstyle = self.maskstyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewmlcae)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewmlcae.exec()
        _viewmlcae.show()

    def changeLdtNconvblock(self):
        if ml_tfm.checkCAEModel(self.modelpath, self.modelname) is True:
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
        if ml_tfm.checkCAEModel(self.modelpath, self.modelname) is True:
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
        _file = _dialog.getSaveFileName(None, 'Save CAE Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
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

    def clickBtnUpdateMl2DCae--- This code section failed: ---

 L. 514         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 516         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 517        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in UpdateMl2DCae: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 518        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 519        44  LOAD_STR                 'Update 2D-CAE'

 L. 520        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 521        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 523        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkCAEModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 524        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in UpdateMl2DCae: No pre-CAE network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 525        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 526       100  LOAD_STR                 'Update 2D-CAE'

 L. 527       102  LOAD_STR                 'No pre-CAE network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 528       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 530       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 531       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 532       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in UpdateMl2DCae: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    

 L. 533       152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 534       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 535       170  LOAD_STR                 'Update 2D-CAE'

 L. 536       172  LOAD_STR                 "Feature '"
              174  LOAD_FAST                'f'
              176  BINARY_ADD       
              178  LOAD_STR                 "' not found in seismic data"
              180  BINARY_ADD       
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L. 537       186  LOAD_CONST               None
              188  RETURN_VALUE     
              190  JUMP_BACK           124  'to 124'
              192  POP_BLOCK        
            194_0  COME_FROM_LOOP      112  '112'

 L. 539       194  LOAD_GLOBAL              basic_data
              196  LOAD_METHOD              str2int
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                ldtoldheight
              202  LOAD_METHOD              text
              204  CALL_METHOD_0         0  '0 positional arguments'
              206  CALL_METHOD_1         1  '1 positional argument'
              208  STORE_FAST               '_image_height'

 L. 540       210  LOAD_GLOBAL              basic_data
              212  LOAD_METHOD              str2int
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                ldtoldwidth
              218  LOAD_METHOD              text
              220  CALL_METHOD_0         0  '0 positional arguments'
              222  CALL_METHOD_1         1  '1 positional argument'
              224  STORE_FAST               '_image_width'

 L. 541       226  LOAD_GLOBAL              basic_data
              228  LOAD_METHOD              str2int
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                ldtnewheight
              234  LOAD_METHOD              text
              236  CALL_METHOD_0         0  '0 positional arguments'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  STORE_FAST               '_image_height_new'

 L. 542       242  LOAD_GLOBAL              basic_data
              244  LOAD_METHOD              str2int
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                ldtnewwidth
              250  LOAD_METHOD              text
              252  CALL_METHOD_0         0  '0 positional arguments'
              254  CALL_METHOD_1         1  '1 positional argument'
              256  STORE_FAST               '_image_width_new'

 L. 543       258  LOAD_FAST                '_image_height'
              260  LOAD_CONST               False
              262  COMPARE_OP               is
          264_266  POP_JUMP_IF_TRUE    298  'to 298'
              268  LOAD_FAST                '_image_width'
              270  LOAD_CONST               False
              272  COMPARE_OP               is
          274_276  POP_JUMP_IF_TRUE    298  'to 298'

 L. 544       278  LOAD_FAST                '_image_height_new'
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

 L. 545       298  LOAD_GLOBAL              vis_msg
              300  LOAD_ATTR                print
              302  LOAD_STR                 'ERROR in UpdateMl2DCae: Non-integer feature size'
              304  LOAD_STR                 'error'
              306  LOAD_CONST               ('type',)
              308  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              310  POP_TOP          

 L. 546       312  LOAD_GLOBAL              QtWidgets
              314  LOAD_ATTR                QMessageBox
              316  LOAD_METHOD              critical
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                msgbox

 L. 547       322  LOAD_STR                 'Update 2D-CAE'

 L. 548       324  LOAD_STR                 'Non-integer feature size'
              326  CALL_METHOD_3         3  '3 positional arguments'
              328  POP_TOP          

 L. 549       330  LOAD_CONST               None
              332  RETURN_VALUE     
            334_0  COME_FROM           294  '294'

 L. 550       334  LOAD_FAST                '_image_height'
              336  LOAD_CONST               2
              338  COMPARE_OP               <
          340_342  POP_JUMP_IF_TRUE    374  'to 374'
              344  LOAD_FAST                '_image_width'
              346  LOAD_CONST               2
              348  COMPARE_OP               <
          350_352  POP_JUMP_IF_TRUE    374  'to 374'

 L. 551       354  LOAD_FAST                '_image_height_new'
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

 L. 552       374  LOAD_GLOBAL              vis_msg
              376  LOAD_ATTR                print
              378  LOAD_STR                 'ERROR in UpdateMl2DCae: Features are not 2D'
              380  LOAD_STR                 'error'
              382  LOAD_CONST               ('type',)
              384  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              386  POP_TOP          

 L. 553       388  LOAD_GLOBAL              QtWidgets
              390  LOAD_ATTR                QMessageBox
              392  LOAD_METHOD              critical
              394  LOAD_FAST                'self'
              396  LOAD_ATTR                msgbox

 L. 554       398  LOAD_STR                 'Update 2D-CAE'

 L. 555       400  LOAD_STR                 'Features are not 2D'
              402  CALL_METHOD_3         3  '3 positional arguments'
              404  POP_TOP          

 L. 556       406  LOAD_CONST               None
              408  RETURN_VALUE     
            410_0  COME_FROM           370  '370'

 L. 558       410  LOAD_CONST               2
              412  LOAD_GLOBAL              int
              414  LOAD_FAST                '_image_height'
              416  LOAD_CONST               2
              418  BINARY_TRUE_DIVIDE
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  BINARY_MULTIPLY  
              424  LOAD_CONST               1
              426  BINARY_ADD       
              428  STORE_FAST               '_image_height'

 L. 559       430  LOAD_CONST               2
              432  LOAD_GLOBAL              int
              434  LOAD_FAST                '_image_width'
              436  LOAD_CONST               2
              438  BINARY_TRUE_DIVIDE
              440  CALL_FUNCTION_1       1  '1 positional argument'
              442  BINARY_MULTIPLY  
              444  LOAD_CONST               1
              446  BINARY_ADD       
              448  STORE_FAST               '_image_width'

 L. 561       450  LOAD_FAST                'self'
              452  LOAD_ATTR                modelinfo
              454  LOAD_STR                 'target'
              456  BINARY_SUBSCR    
              458  LOAD_FAST                'self'
              460  LOAD_ATTR                seisdata
              462  LOAD_METHOD              keys
              464  CALL_METHOD_0         0  '0 positional arguments'
              466  COMPARE_OP               not-in
          468_470  POP_JUMP_IF_FALSE   532  'to 532'

 L. 562       472  LOAD_GLOBAL              vis_msg
              474  LOAD_ATTR                print
              476  LOAD_STR                 "ERROR in UpdateMl2DCae: Target label '%s' not found in seismic data"

 L. 563       478  LOAD_FAST                'self'
              480  LOAD_ATTR                modelinfo
              482  LOAD_STR                 'target'
              484  BINARY_SUBSCR    
              486  BINARY_MODULO    
              488  LOAD_STR                 'error'
              490  LOAD_CONST               ('type',)
              492  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              494  POP_TOP          

 L. 564       496  LOAD_GLOBAL              QtWidgets
              498  LOAD_ATTR                QMessageBox
              500  LOAD_METHOD              critical
              502  LOAD_FAST                'self'
              504  LOAD_ATTR                msgbox

 L. 565       506  LOAD_STR                 'Update 2D-CAE'

 L. 566       508  LOAD_STR                 "Target label '"
              510  LOAD_FAST                'self'
              512  LOAD_ATTR                modelinfo
              514  LOAD_STR                 'target'
              516  BINARY_SUBSCR    
              518  BINARY_ADD       
              520  LOAD_STR                 ' not found in seismic data'
              522  BINARY_ADD       
              524  CALL_METHOD_3         3  '3 positional arguments'
              526  POP_TOP          

 L. 567       528  LOAD_CONST               None
              530  RETURN_VALUE     
            532_0  COME_FROM           468  '468'

 L. 569       532  LOAD_FAST                'self'
              534  LOAD_ATTR                modelinfo
              536  LOAD_STR                 'feature_list'
              538  BINARY_SUBSCR    
              540  STORE_FAST               '_features'

 L. 570       542  LOAD_FAST                'self'
              544  LOAD_ATTR                modelinfo
              546  LOAD_STR                 'target'
              548  BINARY_SUBSCR    
              550  STORE_FAST               '_target'

 L. 572       552  LOAD_GLOBAL              basic_data
              554  LOAD_METHOD              str2int
              556  LOAD_FAST                'self'
              558  LOAD_ATTR                ldtnepoch
              560  LOAD_METHOD              text
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  CALL_METHOD_1         1  '1 positional argument'
              566  STORE_FAST               '_nepoch'

 L. 573       568  LOAD_GLOBAL              basic_data
              570  LOAD_METHOD              str2int
              572  LOAD_FAST                'self'
              574  LOAD_ATTR                ldtbatchsize
              576  LOAD_METHOD              text
              578  CALL_METHOD_0         0  '0 positional arguments'
              580  CALL_METHOD_1         1  '1 positional argument'
              582  STORE_FAST               '_batchsize'

 L. 574       584  LOAD_GLOBAL              basic_data
              586  LOAD_METHOD              str2float
              588  LOAD_FAST                'self'
              590  LOAD_ATTR                ldtlearnrate
              592  LOAD_METHOD              text
              594  CALL_METHOD_0         0  '0 positional arguments'
              596  CALL_METHOD_1         1  '1 positional argument'
              598  STORE_FAST               '_learning_rate'

 L. 575       600  LOAD_GLOBAL              basic_data
              602  LOAD_METHOD              str2float
              604  LOAD_FAST                'self'
              606  LOAD_ATTR                ldtdropout
              608  LOAD_METHOD              text
              610  CALL_METHOD_0         0  '0 positional arguments'
              612  CALL_METHOD_1         1  '1 positional argument'
              614  STORE_FAST               '_dropout_prob'

 L. 576       616  LOAD_FAST                '_nepoch'
              618  LOAD_CONST               False
              620  COMPARE_OP               is
          622_624  POP_JUMP_IF_TRUE    636  'to 636'
              626  LOAD_FAST                '_nepoch'
              628  LOAD_CONST               0
              630  COMPARE_OP               <=
          632_634  POP_JUMP_IF_FALSE   672  'to 672'
            636_0  COME_FROM           622  '622'

 L. 577       636  LOAD_GLOBAL              vis_msg
              638  LOAD_ATTR                print
              640  LOAD_STR                 'ERROR in UpdateMl2DCae: Non-positive epoch number'
              642  LOAD_STR                 'error'
              644  LOAD_CONST               ('type',)
              646  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              648  POP_TOP          

 L. 578       650  LOAD_GLOBAL              QtWidgets
              652  LOAD_ATTR                QMessageBox
              654  LOAD_METHOD              critical
              656  LOAD_FAST                'self'
              658  LOAD_ATTR                msgbox

 L. 579       660  LOAD_STR                 'Update 2D-CAE'

 L. 580       662  LOAD_STR                 'Non-positive epoch number'
              664  CALL_METHOD_3         3  '3 positional arguments'
              666  POP_TOP          

 L. 581       668  LOAD_CONST               None
              670  RETURN_VALUE     
            672_0  COME_FROM           632  '632'

 L. 582       672  LOAD_FAST                '_batchsize'
              674  LOAD_CONST               False
              676  COMPARE_OP               is
          678_680  POP_JUMP_IF_TRUE    692  'to 692'
              682  LOAD_FAST                '_batchsize'
              684  LOAD_CONST               0
              686  COMPARE_OP               <=
          688_690  POP_JUMP_IF_FALSE   728  'to 728'
            692_0  COME_FROM           678  '678'

 L. 583       692  LOAD_GLOBAL              vis_msg
              694  LOAD_ATTR                print
              696  LOAD_STR                 'ERROR in UpdateMl2DCae: Non-positive batch size'
              698  LOAD_STR                 'error'
              700  LOAD_CONST               ('type',)
              702  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              704  POP_TOP          

 L. 584       706  LOAD_GLOBAL              QtWidgets
              708  LOAD_ATTR                QMessageBox
              710  LOAD_METHOD              critical
              712  LOAD_FAST                'self'
              714  LOAD_ATTR                msgbox

 L. 585       716  LOAD_STR                 'Update 2D-CAE'

 L. 586       718  LOAD_STR                 'Non-positive batch size'
              720  CALL_METHOD_3         3  '3 positional arguments'
              722  POP_TOP          

 L. 587       724  LOAD_CONST               None
              726  RETURN_VALUE     
            728_0  COME_FROM           688  '688'

 L. 588       728  LOAD_FAST                '_learning_rate'
              730  LOAD_CONST               False
              732  COMPARE_OP               is
          734_736  POP_JUMP_IF_TRUE    748  'to 748'
              738  LOAD_FAST                '_learning_rate'
              740  LOAD_CONST               0
              742  COMPARE_OP               <=
          744_746  POP_JUMP_IF_FALSE   784  'to 784'
            748_0  COME_FROM           734  '734'

 L. 589       748  LOAD_GLOBAL              vis_msg
              750  LOAD_ATTR                print
              752  LOAD_STR                 'ERROR in UpdateMl2DCae: Non-positive learning rate'
              754  LOAD_STR                 'error'
              756  LOAD_CONST               ('type',)
              758  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              760  POP_TOP          

 L. 590       762  LOAD_GLOBAL              QtWidgets
              764  LOAD_ATTR                QMessageBox
              766  LOAD_METHOD              critical
              768  LOAD_FAST                'self'
              770  LOAD_ATTR                msgbox

 L. 591       772  LOAD_STR                 'Update 2D-CAE'

 L. 592       774  LOAD_STR                 'Non-positive learning rate'
              776  CALL_METHOD_3         3  '3 positional arguments'
              778  POP_TOP          

 L. 593       780  LOAD_CONST               None
              782  RETURN_VALUE     
            784_0  COME_FROM           744  '744'

 L. 594       784  LOAD_FAST                '_dropout_prob'
              786  LOAD_CONST               False
              788  COMPARE_OP               is
          790_792  POP_JUMP_IF_TRUE    804  'to 804'
              794  LOAD_FAST                '_dropout_prob'
              796  LOAD_CONST               0
              798  COMPARE_OP               <=
          800_802  POP_JUMP_IF_FALSE   840  'to 840'
            804_0  COME_FROM           790  '790'

 L. 595       804  LOAD_GLOBAL              vis_msg
              806  LOAD_ATTR                print
              808  LOAD_STR                 'ERROR in UpdateMl2DCae: Negative dropout rate'
              810  LOAD_STR                 'error'
              812  LOAD_CONST               ('type',)
              814  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              816  POP_TOP          

 L. 596       818  LOAD_GLOBAL              QtWidgets
              820  LOAD_ATTR                QMessageBox
              822  LOAD_METHOD              critical
              824  LOAD_FAST                'self'
              826  LOAD_ATTR                msgbox

 L. 597       828  LOAD_STR                 'Update 2D-CAE'

 L. 598       830  LOAD_STR                 'Negative dropout rate'
              832  CALL_METHOD_3         3  '3 positional arguments'
              834  POP_TOP          

 L. 599       836  LOAD_CONST               None
              838  RETURN_VALUE     
            840_0  COME_FROM           800  '800'

 L. 601       840  LOAD_GLOBAL              len
              842  LOAD_FAST                'self'
              844  LOAD_ATTR                ldtsave
              846  LOAD_METHOD              text
              848  CALL_METHOD_0         0  '0 positional arguments'
              850  CALL_FUNCTION_1       1  '1 positional argument'
              852  LOAD_CONST               1
              854  COMPARE_OP               <
          856_858  POP_JUMP_IF_FALSE   896  'to 896'

 L. 602       860  LOAD_GLOBAL              vis_msg
              862  LOAD_ATTR                print
              864  LOAD_STR                 'ERROR in UpdateMl2DCae: No name specified for new-CAE'
              866  LOAD_STR                 'error'
              868  LOAD_CONST               ('type',)
              870  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              872  POP_TOP          

 L. 603       874  LOAD_GLOBAL              QtWidgets
              876  LOAD_ATTR                QMessageBox
              878  LOAD_METHOD              critical
              880  LOAD_FAST                'self'
              882  LOAD_ATTR                msgbox

 L. 604       884  LOAD_STR                 'Update 2D-CAE'

 L. 605       886  LOAD_STR                 'No name specified for new-CAE'
              888  CALL_METHOD_3         3  '3 positional arguments'
              890  POP_TOP          

 L. 606       892  LOAD_CONST               None
              894  RETURN_VALUE     
            896_0  COME_FROM           856  '856'

 L. 607       896  LOAD_GLOBAL              os
              898  LOAD_ATTR                path
              900  LOAD_METHOD              dirname
              902  LOAD_FAST                'self'
              904  LOAD_ATTR                ldtsave
              906  LOAD_METHOD              text
              908  CALL_METHOD_0         0  '0 positional arguments'
              910  CALL_METHOD_1         1  '1 positional argument'
              912  STORE_FAST               '_savepath'

 L. 608       914  LOAD_GLOBAL              os
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

 L. 610       944  LOAD_CONST               0
              946  STORE_FAST               '_wdinl'

 L. 611       948  LOAD_CONST               0
              950  STORE_FAST               '_wdxl'

 L. 612       952  LOAD_CONST               0
              954  STORE_FAST               '_wdz'

 L. 613       956  LOAD_FAST                'self'
              958  LOAD_ATTR                cbbornt
              960  LOAD_METHOD              currentIndex
              962  CALL_METHOD_0         0  '0 positional arguments'
              964  LOAD_CONST               0
              966  COMPARE_OP               ==
          968_970  POP_JUMP_IF_FALSE   996  'to 996'

 L. 614       972  LOAD_GLOBAL              int
              974  LOAD_FAST                '_image_width'
              976  LOAD_CONST               2
              978  BINARY_TRUE_DIVIDE
              980  CALL_FUNCTION_1       1  '1 positional argument'
              982  STORE_FAST               '_wdxl'

 L. 615       984  LOAD_GLOBAL              int
              986  LOAD_FAST                '_image_height'
              988  LOAD_CONST               2
              990  BINARY_TRUE_DIVIDE
              992  CALL_FUNCTION_1       1  '1 positional argument'
              994  STORE_FAST               '_wdz'
            996_0  COME_FROM           968  '968'

 L. 616       996  LOAD_FAST                'self'
              998  LOAD_ATTR                cbbornt
             1000  LOAD_METHOD              currentIndex
             1002  CALL_METHOD_0         0  '0 positional arguments'
             1004  LOAD_CONST               1
             1006  COMPARE_OP               ==
         1008_1010  POP_JUMP_IF_FALSE  1036  'to 1036'

 L. 617      1012  LOAD_GLOBAL              int
             1014  LOAD_FAST                '_image_width'
             1016  LOAD_CONST               2
             1018  BINARY_TRUE_DIVIDE
             1020  CALL_FUNCTION_1       1  '1 positional argument'
             1022  STORE_FAST               '_wdinl'

 L. 618      1024  LOAD_GLOBAL              int
             1026  LOAD_FAST                '_image_height'
             1028  LOAD_CONST               2
             1030  BINARY_TRUE_DIVIDE
             1032  CALL_FUNCTION_1       1  '1 positional argument'
             1034  STORE_FAST               '_wdz'
           1036_0  COME_FROM          1008  '1008'

 L. 619      1036  LOAD_FAST                'self'
             1038  LOAD_ATTR                cbbornt
             1040  LOAD_METHOD              currentIndex
             1042  CALL_METHOD_0         0  '0 positional arguments'
             1044  LOAD_CONST               2
             1046  COMPARE_OP               ==
         1048_1050  POP_JUMP_IF_FALSE  1076  'to 1076'

 L. 620      1052  LOAD_GLOBAL              int
             1054  LOAD_FAST                '_image_width'
             1056  LOAD_CONST               2
             1058  BINARY_TRUE_DIVIDE
             1060  CALL_FUNCTION_1       1  '1 positional argument'
             1062  STORE_FAST               '_wdinl'

 L. 621      1064  LOAD_GLOBAL              int
             1066  LOAD_FAST                '_image_height'
             1068  LOAD_CONST               2
             1070  BINARY_TRUE_DIVIDE
             1072  CALL_FUNCTION_1       1  '1 positional argument'
             1074  STORE_FAST               '_wdxl'
           1076_0  COME_FROM          1048  '1048'

 L. 623      1076  LOAD_FAST                'self'
             1078  LOAD_ATTR                survinfo
             1080  STORE_FAST               '_seisinfo'

 L. 625      1082  LOAD_GLOBAL              print
             1084  LOAD_STR                 'UpdateMl2DCae: Step 1 - Get training samples:'
             1086  CALL_FUNCTION_1       1  '1 positional argument'
             1088  POP_TOP          

 L. 626      1090  LOAD_FAST                'self'
             1092  LOAD_ATTR                traindataconfig
             1094  LOAD_STR                 'TrainPointSet'
             1096  BINARY_SUBSCR    
             1098  STORE_FAST               '_trainpoint'

 L. 627      1100  LOAD_GLOBAL              np
             1102  LOAD_METHOD              zeros
             1104  LOAD_CONST               0
             1106  LOAD_CONST               3
             1108  BUILD_LIST_2          2 
             1110  CALL_METHOD_1         1  '1 positional argument'
             1112  STORE_FAST               '_traindata'

 L. 628      1114  SETUP_LOOP         1190  'to 1190'
             1116  LOAD_FAST                '_trainpoint'
             1118  GET_ITER         
           1120_0  COME_FROM          1138  '1138'
             1120  FOR_ITER           1188  'to 1188'
             1122  STORE_FAST               '_p'

 L. 629      1124  LOAD_GLOBAL              point_ays
             1126  LOAD_METHOD              checkPoint
             1128  LOAD_FAST                'self'
             1130  LOAD_ATTR                pointsetdata
             1132  LOAD_FAST                '_p'
             1134  BINARY_SUBSCR    
             1136  CALL_METHOD_1         1  '1 positional argument'
         1138_1140  POP_JUMP_IF_FALSE  1120  'to 1120'

 L. 630      1142  LOAD_GLOBAL              basic_mdt
             1144  LOAD_METHOD              exportMatDict
             1146  LOAD_FAST                'self'
             1148  LOAD_ATTR                pointsetdata
             1150  LOAD_FAST                '_p'
             1152  BINARY_SUBSCR    
             1154  LOAD_STR                 'Inline'
             1156  LOAD_STR                 'Crossline'
             1158  LOAD_STR                 'Z'
             1160  BUILD_LIST_3          3 
             1162  CALL_METHOD_2         2  '2 positional arguments'
             1164  STORE_FAST               '_pt'

 L. 631      1166  LOAD_GLOBAL              np
             1168  LOAD_ATTR                concatenate
             1170  LOAD_FAST                '_traindata'
             1172  LOAD_FAST                '_pt'
             1174  BUILD_TUPLE_2         2 
             1176  LOAD_CONST               0
             1178  LOAD_CONST               ('axis',)
             1180  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1182  STORE_FAST               '_traindata'
         1184_1186  JUMP_BACK          1120  'to 1120'
             1188  POP_BLOCK        
           1190_0  COME_FROM_LOOP     1114  '1114'

 L. 632      1190  LOAD_GLOBAL              seis_ays
             1192  LOAD_ATTR                removeOutofSurveySample
             1194  LOAD_FAST                '_traindata'

 L. 633      1196  LOAD_FAST                '_seisinfo'
             1198  LOAD_STR                 'ILStart'
             1200  BINARY_SUBSCR    
             1202  LOAD_FAST                '_wdinl'
             1204  LOAD_FAST                '_seisinfo'
             1206  LOAD_STR                 'ILStep'
             1208  BINARY_SUBSCR    
             1210  BINARY_MULTIPLY  
             1212  BINARY_ADD       

 L. 634      1214  LOAD_FAST                '_seisinfo'
             1216  LOAD_STR                 'ILEnd'
             1218  BINARY_SUBSCR    
             1220  LOAD_FAST                '_wdinl'
             1222  LOAD_FAST                '_seisinfo'
             1224  LOAD_STR                 'ILStep'
             1226  BINARY_SUBSCR    
             1228  BINARY_MULTIPLY  
             1230  BINARY_SUBTRACT  

 L. 635      1232  LOAD_FAST                '_seisinfo'
             1234  LOAD_STR                 'XLStart'
             1236  BINARY_SUBSCR    
             1238  LOAD_FAST                '_wdxl'
             1240  LOAD_FAST                '_seisinfo'
             1242  LOAD_STR                 'XLStep'
             1244  BINARY_SUBSCR    
             1246  BINARY_MULTIPLY  
             1248  BINARY_ADD       

 L. 636      1250  LOAD_FAST                '_seisinfo'
             1252  LOAD_STR                 'XLEnd'
             1254  BINARY_SUBSCR    
             1256  LOAD_FAST                '_wdxl'
             1258  LOAD_FAST                '_seisinfo'
             1260  LOAD_STR                 'XLStep'
             1262  BINARY_SUBSCR    
             1264  BINARY_MULTIPLY  
             1266  BINARY_SUBTRACT  

 L. 637      1268  LOAD_FAST                '_seisinfo'
             1270  LOAD_STR                 'ZStart'
             1272  BINARY_SUBSCR    
             1274  LOAD_FAST                '_wdz'
             1276  LOAD_FAST                '_seisinfo'
             1278  LOAD_STR                 'ZStep'
             1280  BINARY_SUBSCR    
             1282  BINARY_MULTIPLY  
             1284  BINARY_ADD       

 L. 638      1286  LOAD_FAST                '_seisinfo'
             1288  LOAD_STR                 'ZEnd'
             1290  BINARY_SUBSCR    
             1292  LOAD_FAST                '_wdz'
             1294  LOAD_FAST                '_seisinfo'
             1296  LOAD_STR                 'ZStep'
             1298  BINARY_SUBSCR    
             1300  BINARY_MULTIPLY  
             1302  BINARY_SUBTRACT  
             1304  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1306  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1308  STORE_FAST               '_traindata'

 L. 641      1310  LOAD_GLOBAL              np
             1312  LOAD_METHOD              shape
             1314  LOAD_FAST                '_traindata'
             1316  CALL_METHOD_1         1  '1 positional argument'
             1318  LOAD_CONST               0
             1320  BINARY_SUBSCR    
             1322  LOAD_CONST               0
             1324  COMPARE_OP               <=
         1326_1328  POP_JUMP_IF_FALSE  1366  'to 1366'

 L. 642      1330  LOAD_GLOBAL              vis_msg
             1332  LOAD_ATTR                print
             1334  LOAD_STR                 'ERROR in UpdateMl2DCae: No training sample found'
             1336  LOAD_STR                 'error'
             1338  LOAD_CONST               ('type',)
             1340  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1342  POP_TOP          

 L. 643      1344  LOAD_GLOBAL              QtWidgets
             1346  LOAD_ATTR                QMessageBox
             1348  LOAD_METHOD              critical
             1350  LOAD_FAST                'self'
             1352  LOAD_ATTR                msgbox

 L. 644      1354  LOAD_STR                 'Update 2D-CAE'

 L. 645      1356  LOAD_STR                 'No training sample found'
             1358  CALL_METHOD_3         3  '3 positional arguments'
             1360  POP_TOP          

 L. 646      1362  LOAD_CONST               None
             1364  RETURN_VALUE     
           1366_0  COME_FROM          1326  '1326'

 L. 649      1366  LOAD_GLOBAL              print
             1368  LOAD_STR                 'UpdateMl2DCae: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 650      1370  LOAD_FAST                '_image_height'
             1372  LOAD_FAST                '_image_width'
             1374  LOAD_FAST                '_image_height_new'
             1376  LOAD_FAST                '_image_width_new'
             1378  BUILD_TUPLE_4         4 
             1380  BINARY_MODULO    
             1382  CALL_FUNCTION_1       1  '1 positional argument'
             1384  POP_TOP          

 L. 651      1386  BUILD_MAP_0           0 
             1388  STORE_FAST               '_traindict'

 L. 652      1390  SETUP_LOOP         1462  'to 1462'
             1392  LOAD_FAST                '_features'
             1394  GET_ITER         
             1396  FOR_ITER           1460  'to 1460'
             1398  STORE_FAST               'f'

 L. 653      1400  LOAD_FAST                'self'
             1402  LOAD_ATTR                seisdata
             1404  LOAD_FAST                'f'
             1406  BINARY_SUBSCR    
             1408  STORE_FAST               '_seisdata'

 L. 654      1410  LOAD_GLOBAL              seis_ays
             1412  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1414  LOAD_FAST                '_seisdata'
             1416  LOAD_FAST                '_traindata'
             1418  LOAD_FAST                'self'
             1420  LOAD_ATTR                survinfo

 L. 655      1422  LOAD_FAST                '_wdinl'
             1424  LOAD_FAST                '_wdxl'
             1426  LOAD_FAST                '_wdz'

 L. 656      1428  LOAD_CONST               False
             1430  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1432  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1434  LOAD_CONST               None
             1436  LOAD_CONST               None
             1438  BUILD_SLICE_2         2 
             1440  LOAD_CONST               3
             1442  LOAD_CONST               None
             1444  BUILD_SLICE_2         2 
             1446  BUILD_TUPLE_2         2 
             1448  BINARY_SUBSCR    
             1450  LOAD_FAST                '_traindict'
             1452  LOAD_FAST                'f'
             1454  STORE_SUBSCR     
         1456_1458  JUMP_BACK          1396  'to 1396'
             1460  POP_BLOCK        
           1462_0  COME_FROM_LOOP     1390  '1390'

 L. 657      1462  LOAD_FAST                '_target'
             1464  LOAD_FAST                '_features'
             1466  COMPARE_OP               not-in
         1468_1470  POP_JUMP_IF_FALSE  1528  'to 1528'

 L. 658      1472  LOAD_FAST                'self'
             1474  LOAD_ATTR                seisdata
             1476  LOAD_FAST                '_target'
             1478  BINARY_SUBSCR    
             1480  STORE_FAST               '_seisdata'

 L. 659      1482  LOAD_GLOBAL              seis_ays
             1484  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1486  LOAD_FAST                '_seisdata'
             1488  LOAD_FAST                '_traindata'
             1490  LOAD_FAST                'self'
             1492  LOAD_ATTR                survinfo

 L. 660      1494  LOAD_FAST                '_wdinl'
             1496  LOAD_FAST                '_wdxl'
             1498  LOAD_FAST                '_wdz'

 L. 661      1500  LOAD_CONST               False
             1502  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1504  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1506  LOAD_CONST               None
             1508  LOAD_CONST               None
             1510  BUILD_SLICE_2         2 
             1512  LOAD_CONST               3
             1514  LOAD_CONST               None
             1516  BUILD_SLICE_2         2 
             1518  BUILD_TUPLE_2         2 
             1520  BINARY_SUBSCR    
             1522  LOAD_FAST                '_traindict'
             1524  LOAD_FAST                '_target'
             1526  STORE_SUBSCR     
           1528_0  COME_FROM          1468  '1468'

 L. 662      1528  LOAD_FAST                'self'
             1530  LOAD_ATTR                traindataconfig
             1532  LOAD_STR                 'RemoveInvariantFeature_Checked'
             1534  BINARY_SUBSCR    
         1536_1538  POP_JUMP_IF_FALSE  1620  'to 1620'

 L. 663      1540  SETUP_LOOP         1620  'to 1620'
             1542  LOAD_FAST                '_features'
             1544  GET_ITER         
           1546_0  COME_FROM          1574  '1574'
             1546  FOR_ITER           1618  'to 1618'
             1548  STORE_FAST               'f'

 L. 664      1550  LOAD_GLOBAL              ml_aug
             1552  LOAD_METHOD              removeInvariantFeature
             1554  LOAD_FAST                '_traindict'
             1556  LOAD_FAST                'f'
             1558  CALL_METHOD_2         2  '2 positional arguments'
             1560  STORE_FAST               '_traindict'

 L. 665      1562  LOAD_GLOBAL              basic_mdt
             1564  LOAD_METHOD              maxDictConstantRow
             1566  LOAD_FAST                '_traindict'
             1568  CALL_METHOD_1         1  '1 positional argument'
             1570  LOAD_CONST               0
             1572  COMPARE_OP               <=
         1574_1576  POP_JUMP_IF_FALSE  1546  'to 1546'

 L. 666      1578  LOAD_GLOBAL              vis_msg
             1580  LOAD_ATTR                print
             1582  LOAD_STR                 'ERROR in UpdateMl2DCae: No training sample found'
             1584  LOAD_STR                 'error'
             1586  LOAD_CONST               ('type',)
             1588  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1590  POP_TOP          

 L. 667      1592  LOAD_GLOBAL              QtWidgets
             1594  LOAD_ATTR                QMessageBox
             1596  LOAD_METHOD              critical
             1598  LOAD_FAST                'self'
             1600  LOAD_ATTR                msgbox

 L. 668      1602  LOAD_STR                 'Update 2D-CAE'

 L. 669      1604  LOAD_STR                 'No training sample found'
             1606  CALL_METHOD_3         3  '3 positional arguments'
             1608  POP_TOP          

 L. 670      1610  LOAD_CONST               None
             1612  RETURN_VALUE     
         1614_1616  JUMP_BACK          1546  'to 1546'
             1618  POP_BLOCK        
           1620_0  COME_FROM_LOOP     1540  '1540'
           1620_1  COME_FROM          1536  '1536'

 L. 671      1620  LOAD_FAST                '_image_height_new'
             1622  LOAD_FAST                '_image_height'
             1624  COMPARE_OP               !=
         1626_1628  POP_JUMP_IF_TRUE   1640  'to 1640'
             1630  LOAD_FAST                '_image_width_new'
             1632  LOAD_FAST                '_image_width'
             1634  COMPARE_OP               !=
         1636_1638  POP_JUMP_IF_FALSE  1724  'to 1724'
           1640_0  COME_FROM          1626  '1626'

 L. 672      1640  SETUP_LOOP         1684  'to 1684'
             1642  LOAD_FAST                '_features'
             1644  GET_ITER         
             1646  FOR_ITER           1682  'to 1682'
             1648  STORE_FAST               'f'

 L. 673      1650  LOAD_GLOBAL              basic_image
             1652  LOAD_ATTR                changeImageSize
             1654  LOAD_FAST                '_traindict'
             1656  LOAD_FAST                'f'
             1658  BINARY_SUBSCR    

 L. 674      1660  LOAD_FAST                '_image_height'

 L. 675      1662  LOAD_FAST                '_image_width'

 L. 676      1664  LOAD_FAST                '_image_height_new'

 L. 677      1666  LOAD_FAST                '_image_width_new'
             1668  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1670  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1672  LOAD_FAST                '_traindict'
             1674  LOAD_FAST                'f'
             1676  STORE_SUBSCR     
         1678_1680  JUMP_BACK          1646  'to 1646'
             1682  POP_BLOCK        
           1684_0  COME_FROM_LOOP     1640  '1640'

 L. 678      1684  LOAD_FAST                '_target'
             1686  LOAD_FAST                '_features'
             1688  COMPARE_OP               not-in
         1690_1692  POP_JUMP_IF_FALSE  1724  'to 1724'

 L. 679      1694  LOAD_GLOBAL              basic_image
             1696  LOAD_ATTR                changeImageSize
             1698  LOAD_FAST                '_traindict'
             1700  LOAD_FAST                '_target'
             1702  BINARY_SUBSCR    

 L. 680      1704  LOAD_FAST                '_image_height'

 L. 681      1706  LOAD_FAST                '_image_width'

 L. 682      1708  LOAD_FAST                '_image_height_new'

 L. 683      1710  LOAD_FAST                '_image_width_new'
             1712  LOAD_STR                 'linear'
             1714  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             1716  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1718  LOAD_FAST                '_traindict'
             1720  LOAD_FAST                '_target'
             1722  STORE_SUBSCR     
           1724_0  COME_FROM          1690  '1690'
           1724_1  COME_FROM          1636  '1636'

 L. 684      1724  LOAD_FAST                'self'
             1726  LOAD_ATTR                traindataconfig
             1728  LOAD_STR                 'RotateFeature_Checked'
             1730  BINARY_SUBSCR    
             1732  LOAD_CONST               True
             1734  COMPARE_OP               is
         1736_1738  POP_JUMP_IF_FALSE  1878  'to 1878'

 L. 685      1740  SETUP_LOOP         1812  'to 1812'
             1742  LOAD_FAST                '_features'
             1744  GET_ITER         
             1746  FOR_ITER           1810  'to 1810'
             1748  STORE_FAST               'f'

 L. 686      1750  LOAD_FAST                '_image_height_new'
             1752  LOAD_FAST                '_image_width_new'
             1754  COMPARE_OP               ==
         1756_1758  POP_JUMP_IF_FALSE  1784  'to 1784'

 L. 687      1760  LOAD_GLOBAL              ml_aug
             1762  LOAD_METHOD              rotateImage6Way
             1764  LOAD_FAST                '_traindict'
             1766  LOAD_FAST                'f'
             1768  BINARY_SUBSCR    
             1770  LOAD_FAST                '_image_height_new'
             1772  LOAD_FAST                '_image_width_new'
             1774  CALL_METHOD_3         3  '3 positional arguments'
             1776  LOAD_FAST                '_traindict'
             1778  LOAD_FAST                'f'
             1780  STORE_SUBSCR     
             1782  JUMP_BACK          1746  'to 1746'
           1784_0  COME_FROM          1756  '1756'

 L. 689      1784  LOAD_GLOBAL              ml_aug
             1786  LOAD_METHOD              rotateImage4Way
             1788  LOAD_FAST                '_traindict'
             1790  LOAD_FAST                'f'
             1792  BINARY_SUBSCR    
             1794  LOAD_FAST                '_image_height_new'
             1796  LOAD_FAST                '_image_width_new'
             1798  CALL_METHOD_3         3  '3 positional arguments'
             1800  LOAD_FAST                '_traindict'
             1802  LOAD_FAST                'f'
             1804  STORE_SUBSCR     
         1806_1808  JUMP_BACK          1746  'to 1746'
             1810  POP_BLOCK        
           1812_0  COME_FROM_LOOP     1740  '1740'

 L. 690      1812  LOAD_FAST                '_target'
             1814  LOAD_FAST                '_features'
             1816  COMPARE_OP               not-in
         1818_1820  POP_JUMP_IF_FALSE  1878  'to 1878'

 L. 691      1822  LOAD_FAST                '_image_height_new'
             1824  LOAD_FAST                '_image_width_new'
             1826  COMPARE_OP               ==
         1828_1830  POP_JUMP_IF_FALSE  1856  'to 1856'

 L. 693      1832  LOAD_GLOBAL              ml_aug
             1834  LOAD_METHOD              rotateImage6Way
             1836  LOAD_FAST                '_traindict'
             1838  LOAD_FAST                '_target'
             1840  BINARY_SUBSCR    
             1842  LOAD_FAST                '_image_height_new'
             1844  LOAD_FAST                '_image_width_new'
             1846  CALL_METHOD_3         3  '3 positional arguments'
             1848  LOAD_FAST                '_traindict'
             1850  LOAD_FAST                '_target'
             1852  STORE_SUBSCR     
             1854  JUMP_FORWARD       1878  'to 1878'
           1856_0  COME_FROM          1828  '1828'

 L. 696      1856  LOAD_GLOBAL              ml_aug
             1858  LOAD_METHOD              rotateImage4Way
             1860  LOAD_FAST                '_traindict'
             1862  LOAD_FAST                '_target'
             1864  BINARY_SUBSCR    
             1866  LOAD_FAST                '_image_height_new'
             1868  LOAD_FAST                '_image_width_new'
             1870  CALL_METHOD_3         3  '3 positional arguments'
             1872  LOAD_FAST                '_traindict'
             1874  LOAD_FAST                '_target'
             1876  STORE_SUBSCR     
           1878_0  COME_FROM          1854  '1854'
           1878_1  COME_FROM          1818  '1818'
           1878_2  COME_FROM          1736  '1736'

 L. 699      1878  LOAD_GLOBAL              print
             1880  LOAD_STR                 'UpdateMl2DCae: A total of %d valid training samples'
             1882  LOAD_GLOBAL              basic_mdt
             1884  LOAD_METHOD              maxDictConstantRow
             1886  LOAD_FAST                '_traindict'
             1888  CALL_METHOD_1         1  '1 positional argument'
             1890  BINARY_MODULO    
             1892  CALL_FUNCTION_1       1  '1 positional argument'
             1894  POP_TOP          

 L. 701      1896  LOAD_GLOBAL              print
             1898  LOAD_STR                 'UpdateMl2DCae: Step 3 - Start training'
             1900  CALL_FUNCTION_1       1  '1 positional argument'
             1902  POP_TOP          

 L. 703      1904  LOAD_GLOBAL              QtWidgets
             1906  LOAD_METHOD              QProgressDialog
             1908  CALL_METHOD_0         0  '0 positional arguments'
             1910  STORE_FAST               '_pgsdlg'

 L. 704      1912  LOAD_GLOBAL              QtGui
             1914  LOAD_METHOD              QIcon
             1916  CALL_METHOD_0         0  '0 positional arguments'
             1918  STORE_FAST               'icon'

 L. 705      1920  LOAD_FAST                'icon'
             1922  LOAD_METHOD              addPixmap
             1924  LOAD_GLOBAL              QtGui
             1926  LOAD_METHOD              QPixmap
             1928  LOAD_GLOBAL              os
             1930  LOAD_ATTR                path
             1932  LOAD_METHOD              join
             1934  LOAD_FAST                'self'
             1936  LOAD_ATTR                iconpath
             1938  LOAD_STR                 'icons/update.png'
             1940  CALL_METHOD_2         2  '2 positional arguments'
             1942  CALL_METHOD_1         1  '1 positional argument'

 L. 706      1944  LOAD_GLOBAL              QtGui
             1946  LOAD_ATTR                QIcon
             1948  LOAD_ATTR                Normal
             1950  LOAD_GLOBAL              QtGui
             1952  LOAD_ATTR                QIcon
             1954  LOAD_ATTR                Off
             1956  CALL_METHOD_3         3  '3 positional arguments'
             1958  POP_TOP          

 L. 707      1960  LOAD_FAST                '_pgsdlg'
             1962  LOAD_METHOD              setWindowIcon
             1964  LOAD_FAST                'icon'
             1966  CALL_METHOD_1         1  '1 positional argument'
             1968  POP_TOP          

 L. 708      1970  LOAD_FAST                '_pgsdlg'
             1972  LOAD_METHOD              setWindowTitle
             1974  LOAD_STR                 'Update 2D-CAE'
             1976  CALL_METHOD_1         1  '1 positional argument'
             1978  POP_TOP          

 L. 709      1980  LOAD_FAST                '_pgsdlg'
             1982  LOAD_METHOD              setCancelButton
             1984  LOAD_CONST               None
             1986  CALL_METHOD_1         1  '1 positional argument'
             1988  POP_TOP          

 L. 710      1990  LOAD_FAST                '_pgsdlg'
             1992  LOAD_METHOD              setWindowFlags
             1994  LOAD_GLOBAL              QtCore
             1996  LOAD_ATTR                Qt
             1998  LOAD_ATTR                WindowStaysOnTopHint
             2000  CALL_METHOD_1         1  '1 positional argument'
             2002  POP_TOP          

 L. 711      2004  LOAD_FAST                '_pgsdlg'
             2006  LOAD_METHOD              forceShow
             2008  CALL_METHOD_0         0  '0 positional arguments'
             2010  POP_TOP          

 L. 712      2012  LOAD_FAST                '_pgsdlg'
             2014  LOAD_METHOD              setFixedWidth
             2016  LOAD_CONST               400
             2018  CALL_METHOD_1         1  '1 positional argument'
             2020  POP_TOP          

 L. 713      2022  LOAD_GLOBAL              ml_cae
             2024  LOAD_ATTR                updateCAEReconstructor
             2026  LOAD_FAST                '_traindict'

 L. 714      2028  LOAD_FAST                '_image_height_new'
             2030  LOAD_FAST                '_image_width_new'

 L. 715      2032  LOAD_FAST                '_nepoch'
             2034  LOAD_FAST                '_batchsize'

 L. 716      2036  LOAD_FAST                '_learning_rate'

 L. 717      2038  LOAD_FAST                '_dropout_prob'

 L. 718      2040  LOAD_FAST                'self'
             2042  LOAD_ATTR                modelpath
             2044  LOAD_FAST                'self'
             2046  LOAD_ATTR                modelname

 L. 719      2048  LOAD_CONST               True

 L. 720      2050  LOAD_FAST                '_savepath'
             2052  LOAD_FAST                '_savename'

 L. 721      2054  LOAD_FAST                '_pgsdlg'
             2056  LOAD_CONST               ('imageheight', 'imagewidth', 'nepoch', 'batchsize', 'learningrate', 'dropoutprob', 'caepath', 'caename', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2058  CALL_FUNCTION_KW_13    13  '13 total positional and keyword args'
             2060  STORE_FAST               '_caelog'

 L. 723      2062  LOAD_GLOBAL              QtWidgets
             2064  LOAD_ATTR                QMessageBox
             2066  LOAD_METHOD              information
             2068  LOAD_FAST                'self'
             2070  LOAD_ATTR                msgbox

 L. 724      2072  LOAD_STR                 'Update 2D-CAE'

 L. 725      2074  LOAD_STR                 'CAE updated successfully'
             2076  CALL_METHOD_3         3  '3 positional arguments'
             2078  POP_TOP          

 L. 727      2080  LOAD_GLOBAL              QtWidgets
             2082  LOAD_ATTR                QMessageBox
             2084  LOAD_METHOD              question
             2086  LOAD_FAST                'self'
             2088  LOAD_ATTR                msgbox
             2090  LOAD_STR                 'Update 2D-CAE'
             2092  LOAD_STR                 'View learning matrix?'

 L. 728      2094  LOAD_GLOBAL              QtWidgets
             2096  LOAD_ATTR                QMessageBox
             2098  LOAD_ATTR                Yes
             2100  LOAD_GLOBAL              QtWidgets
             2102  LOAD_ATTR                QMessageBox
             2104  LOAD_ATTR                No
             2106  BINARY_OR        

 L. 729      2108  LOAD_GLOBAL              QtWidgets
             2110  LOAD_ATTR                QMessageBox
             2112  LOAD_ATTR                Yes
             2114  CALL_METHOD_5         5  '5 positional arguments'
             2116  STORE_FAST               'reply'

 L. 731      2118  LOAD_FAST                'reply'
             2120  LOAD_GLOBAL              QtWidgets
             2122  LOAD_ATTR                QMessageBox
             2124  LOAD_ATTR                Yes
             2126  COMPARE_OP               ==
         2128_2130  POP_JUMP_IF_FALSE  2198  'to 2198'

 L. 732      2132  LOAD_GLOBAL              QtWidgets
             2134  LOAD_METHOD              QDialog
             2136  CALL_METHOD_0         0  '0 positional arguments'
             2138  STORE_FAST               '_viewmllearnmat'

 L. 733      2140  LOAD_GLOBAL              gui_viewmllearnmat
             2142  CALL_FUNCTION_0       0  '0 positional arguments'
             2144  STORE_FAST               '_gui'

 L. 734      2146  LOAD_FAST                '_caelog'
             2148  LOAD_STR                 'learning_curve'
             2150  BINARY_SUBSCR    
             2152  LOAD_FAST                '_gui'
             2154  STORE_ATTR               learnmat

 L. 735      2156  LOAD_FAST                'self'
             2158  LOAD_ATTR                linestyle
             2160  LOAD_FAST                '_gui'
             2162  STORE_ATTR               linestyle

 L. 736      2164  LOAD_FAST                'self'
             2166  LOAD_ATTR                fontstyle
             2168  LOAD_FAST                '_gui'
             2170  STORE_ATTR               fontstyle

 L. 737      2172  LOAD_FAST                '_gui'
             2174  LOAD_METHOD              setupGUI
             2176  LOAD_FAST                '_viewmllearnmat'
             2178  CALL_METHOD_1         1  '1 positional argument'
             2180  POP_TOP          

 L. 738      2182  LOAD_FAST                '_viewmllearnmat'
             2184  LOAD_METHOD              exec
             2186  CALL_METHOD_0         0  '0 positional arguments'
             2188  POP_TOP          

 L. 739      2190  LOAD_FAST                '_viewmllearnmat'
             2192  LOAD_METHOD              show
             2194  CALL_METHOD_0         0  '0 positional arguments'
             2196  POP_TOP          
           2198_0  COME_FROM          2128  '2128'

Parse error at or near `POP_TOP' instruction at offset 2196

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
    UpdateMl2DCae = QtWidgets.QWidget()
    gui = updateml2dcae()
    gui.setupGUI(UpdateMl2DCae)
    UpdateMl2DCae.show()
    sys.exit(app.exec_())