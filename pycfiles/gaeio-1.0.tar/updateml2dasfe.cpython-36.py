# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\updateml2dasfe.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 40970 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.seismic.analysis import analysis as seis_ays
from cognitivegeo.src.pointset.analysis import analysis as point_ays
from cognitivegeo.src.basic.data import data as basic_data
from cognitivegeo.src.basic.matdict import matdict as basic_mdt
from cognitivegeo.src.basic.image import image as basic_image
from cognitivegeo.src.ml.augmentation import augmentation as ml_aug
from cognitivegeo.src.ml.tfmodel import tfmodel as ml_tfm
from cognitivegeo.src.ml.cnnclassifier import cnnclassifier as ml_cnn
from cognitivegeo.src.gui.viewml2dasfe import viewml2dasfe as gui_viewml2dasfe
from cognitivegeo.src.gui.viewmllearnmat import viewmllearnmat as gui_viewmllearnmat
from cognitivegeo.src.gui.configmltraindata import configmltraindata as gui_configmltraindata
from cognitivegeo.src.vis.messager import messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class updateml2dasfe(object):
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
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = True

    def setupGUI(self, UpdateMl2DAsfe):
        UpdateMl2DAsfe.setObjectName('UpdateMl2DAsfe')
        UpdateMl2DAsfe.setFixedSize(800, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UpdateMl2DAsfe.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(UpdateMl2DAsfe)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(UpdateMl2DAsfe)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lblornt = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(UpdateMl2DAsfe)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 220, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 220, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 220, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 260, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 260, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 220, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 220, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 220, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 260, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 260, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(UpdateMl2DAsfe)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(UpdateMl2DAsfe)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 130))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(UpdateMl2DAsfe)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 140, 180, 130))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(UpdateMl2DAsfe)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 310, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 350, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.lblfcdropout = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblfcdropout.setObjectName('lblfcdropout')
        self.lblfcdropout.setGeometry(QtCore.QRect(210, 390, 130, 30))
        self.ldtfcdropout = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtfcdropout.setObjectName('ldtfcdropout')
        self.ldtfcdropout.setGeometry(QtCore.QRect(350, 390, 40, 30))
        self.lblsave = QtWidgets.QLabel(UpdateMl2DAsfe)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 100, 30))
        self.ldtsave = QtWidgets.QLineEdit(UpdateMl2DAsfe)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(110, 440, 210, 30))
        self.btnsave = QtWidgets.QPushButton(UpdateMl2DAsfe)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 440, 60, 30))
        self.btnapply = QtWidgets.QPushButton(UpdateMl2DAsfe)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(UpdateMl2DAsfe)
        self.msgbox.setObjectName('msgbox')
        _center_x = UpdateMl2DAsfe.geometry().center().x()
        _center_y = UpdateMl2DAsfe.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(UpdateMl2DAsfe)
        QtCore.QMetaObject.connectSlotsByName(UpdateMl2DAsfe)

    def retranslateGUI(self, UpdateMl2DAsfe):
        self.dialog = UpdateMl2DAsfe
        _translate = QtCore.QCoreApplication.translate
        UpdateMl2DAsfe.setWindowTitle(_translate('UpdateMl2DAsfe', 'Update 2D-ASFE'))
        self.lblfrom.setText(_translate('UpdateMl2DAsfe', 'Select network:'))
        self.ldtfrom.setText(_translate('UpdateMl2DAsfe', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('UpdateMl2DAsfe', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('UpdateMl2DAsfe', 'Training features:'))
        self.lblornt.setText(_translate('UpdateMl2DAsfe', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.lbloldsize.setText(_translate('UpdateMl2DAsfe', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('UpdateMl2DAsfe', 'height='))
        self.ldtoldheight.setText(_translate('UpdateMl2DAsfe', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('UpdateMl2DAsfe', 'width='))
        self.ldtoldwidth.setText(_translate('UpdateMl2DAsfe', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('UpdateMl2DAsfe', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('UpdateMl2DAsfe', 'height='))
        self.ldtnewheight.setText(_translate('UpdateMl2DAsfe', ''))
        self.ldtnewheight.setEnabled(False)
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('UpdateMl2DAsfe', 'width='))
        self.ldtnewwidth.setText(_translate('UpdateMl2DAsfe', ''))
        self.ldtnewwidth.setEnabled(False)
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('UpdateMl2DAsfe', 'Pre-trained ASFE architecture:'))
        self.btnviewnetwork.setText(_translate('UpdateMl2DAsfe', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('UpdateMl2DAsfe', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('UpdateMl2DAsfe', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblnfclayer.setText(_translate('UpdateMl2DAsfe', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('UpdateMl2DAsfe', ''))
        self.ldtnfclayer.setEnabled(False)
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblmasksize.setText(_translate('UpdateMl2DAsfe', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('UpdateMl2DAsfe', 'height='))
        self.ldtmaskheight.setText(_translate('UpdateMl2DAsfe', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('UpdateMl2DAsfe', 'width='))
        self.ldtmaskwidth.setText(_translate('UpdateMl2DAsfe', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('UpdateMl2DAsfe', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('UpdateMl2DAsfe', 'height='))
        self.ldtpoolheight.setText(_translate('UpdateMl2DAsfe', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('UpdateMl2DAsfe', 'width='))
        self.ldtpoolwidth.setText(_translate('UpdateMl2DAsfe', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.btnconfigtraindata.setText(_translate('UpdateMl2DAsfe', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lblpara.setText(_translate('UpdateMl2DAsfe', 'Specify update parameters:'))
        self.lblnepoch.setText(_translate('UpdateMl2DAsfe', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('UpdateMl2DAsfe', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('UpdateMl2DAsfe', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('UpdateMl2DAsfe', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('UpdateMl2DAsfe', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('UpdateMl2DAsfe', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfcdropout.setText(_translate('UpdateMl2DAsfe', 'MLP dropout rate:'))
        self.lblfcdropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtfcdropout.setText(_translate('UpdateMl2DAsfe', '0.5'))
        self.ldtfcdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('UpdateMl2DAsfe', 'Save new-ASFE to:'))
        self.ldtsave.setText(_translate('UpdateMl2DAsfe', ''))
        self.btnsave.setText(_translate('UpdateMl2DAsfe', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('UpdateMl2DAsfe', 'Update 2D-ASFE'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnUpdateMl2DAsfe)

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.checkCNNModel(self.modelpath, self.modelname) is True:
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
            self.ldtoldheight.setText(str(3))
            self.ldtoldwidth.setText(str(3))
            _height = self.modelinfo['image_size'][0]
            _width = self.modelinfo['image_size'][1]
            self.ldtnewheight.setText(str(_height))
            self.ldtnewwidth.setText(str(_width))
            self.btnviewnetwork.setEnabled(True)
            self.ldtnconvblock.setText(str(self.modelinfo['number_conv_block']))
            self.ldtnfclayer.setText(str(self.modelinfo['number_fc_layer']))
            self.ldtmaskheight.setText(str(self.modelinfo['patch_size'][0]))
            self.ldtmaskwidth.setText(str(self.modelinfo['patch_size'][1]))
            self.ldtpoolheight.setText(str(self.modelinfo['pool_size'][0]))
            self.ldtpoolwidth.setText(str(self.modelinfo['pool_size'][1]))
        else:
            self.modelpath = ''
            self.modelname = ''
            self.modelinfo = None
            self.lwgfeature.clear()
            self.ldtoldheight.setText('')
            self.ldtnewheight.setText('')
            self.ldtoldwidth.setText('')
            self.ldtnewwidth.setText('')
            self.btnviewnetwork.setEnabled(False)
            self.ldtnconvblock.setText('')
            self.ldtnfclayer.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')

    def clickBtnFrom(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select ASFE Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def clickBtnViewNetwork(self):
        _viewml = QtWidgets.QDialog()
        _gui = gui_viewml2dasfe()
        _gui.linestyle = self.linestyle
        _gui.maskstyle = self.maskstyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewml)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewml.exec()
        _viewml.show()

    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Save ASFE Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtsave.setText(_file[0])

    def changeLdtNconvblock(self):
        if ml_tfm.checkCNNModel(self.modelpath, self.modelname) is True:
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

    def changeLdtNfclayer(self):
        if ml_tfm.checkCNNModel(self.modelpath, self.modelname) is True:
            _nlayer = self.modelinfo['number_fc_layer']
            self.twgnfclayer.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnfclayer.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.modelinfo['number_fc_neuron'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnfclayer.setItem(_idx, 1, item)

        else:
            self.twgnfclayer.setRowCount(0)

    def clickBtnConfigTrainData(self):
        _configtraindata = QtWidgets.QDialog()
        _gui = gui_configmltraindata()
        _gui.mltraindataconfig = self.traindataconfig
        _gui.pointsetlist = sorted(self.pointsetdata.keys())
        _gui.setupGUI(_configtraindata)
        _configtraindata.exec()
        self.traindataconfig = _gui.mltraindataconfig
        _configtraindata.show()

    def clickBtnUpdateMl2DAsfe(self):
        self.refreshMsgBox()
        if self.checkSurvInfo() is False:
            vis_msg.print('ERROR in UpdateMl2DAsfe: No seismic survey available', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 2D-ASFE', 'No seismic survey available')
            return
        if ml_tfm.checkCNNModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in UpdateMl2DAsfe: No pre-ASFE network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 2D-ASFE', 'No pre-ASFE network found')
            return
        for f in self.modelinfo['feature_list']:
            if self.checkSeisData(f) is False:
                vis_msg.print(("ERROR in UpdateMl2DAsfe: Feature '%s' not found in seismic data" % f), type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Update 2D-ASFE', "Feature '" + f + "' not found in seismic data")
                return

        _image_height_old = basic_data.str2int(self.ldtoldheight.text())
        _image_width_old = basic_data.str2int(self.ldtoldwidth.text())
        _image_height_new = basic_data.str2int(self.ldtnewheight.text())
        _image_width_new = basic_data.str2int(self.ldtnewwidth.text())
        if _image_height_old is False or _image_width_old is False or _image_height_new is False or _image_width_new is False:
            vis_msg.print('ERROR in UpdateMl2DAsfe: Non-integer feature size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 2D-ASFE', 'Non-integer feature size')
            return
        if _image_height_old < 2 or _image_width_old < 2 or _image_height_new < 2 or _image_width_new < 2:
            vis_msg.print('ERROR in UpdateMl2DAsfe: Features are not 2D', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 2D-ASFE', 'Features are not 2D')
            return
        _image_height_old = 2 * int(_image_height_old / 2) + 1
        _image_width_old = 2 * int(_image_width_old / 2) + 1
        _features = self.modelinfo['feature_list']
        _target = '_'.join(_features) + '_rotated'
        _nepoch = basic_data.str2int(self.ldtnepoch.text())
        _batchsize = basic_data.str2int(self.ldtbatchsize.text())
        _learning_rate = basic_data.str2float(self.ldtlearnrate.text())
        _dropout_prob_fclayer = basic_data.str2float(self.ldtfcdropout.text())
        if _nepoch is False or _nepoch <= 0:
            vis_msg.print('ERROR in UpdateMl2DAsfe: Non-positive epoch number', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 2D-ASFE', 'Non-positive epoch number')
            return
        if _batchsize is False or _batchsize <= 0:
            vis_msg.print('ERROR in UpdateMl2DAsfe: Non-positive batch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 2D-ASFE', 'Non-positive batch size')
            return
        if _learning_rate is False or _learning_rate <= 0:
            vis_msg.print('ERROR in UpdateMl2DAsfe: Non-positive learning rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 2D-ASFE', 'Non-positive learning rate')
            return
        if _dropout_prob_fclayer is False or _dropout_prob_fclayer <= 0:
            vis_msg.print('ERROR in UpdateMl2DAsfe: Negative dropout rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 2D-ASFE', 'Negative dropout rate')
            return
        if len(self.ldtsave.text()) < 1:
            vis_msg.print('ERROR in UpdateMl2DAsfe: No name specified for new-ASFE', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 2D-ASFE', 'No name specified for new-ASFE')
            return
        _savepath = os.path.dirname(self.ldtsave.text())
        _savename = os.path.splitext(os.path.basename(self.ldtsave.text()))[0]
        _wdinl = 0
        _wdxl = 0
        _wdz = 0
        if self.cbbornt.currentIndex() == 0:
            _wdxl = int(_image_width_old / 2)
            _wdz = int(_image_height_old / 2)
        if self.cbbornt.currentIndex() == 1:
            _wdinl = int(_image_width_old / 2)
            _wdz = int(_image_height_old / 2)
        if self.cbbornt.currentIndex() == 2:
            _wdinl = int(_image_width_old / 2)
            _wdxl = int(_image_height_old / 2)
        _seisinfo = self.survinfo
        print('UpdateMl2DAsfe: Step 1 - Get training samples:')
        _trainpoint = self.traindataconfig['TrainPointSet']
        _traindata = np.zeros([0, 3])
        for _p in _trainpoint:
            if point_ays.checkPoint(self.pointsetdata[_p]):
                _pt = basic_mdt.exportMatDict(self.pointsetdata[_p], ['Inline', 'Crossline', 'Z'])
                _traindata = np.concatenate((_traindata, _pt), axis=0)

        _traindata = seis_ays.removeOutofSurveySample(_traindata, inlstart=(_seisinfo['ILStart'] + _wdinl * _seisinfo['ILStep']),
          inlend=(_seisinfo['ILEnd'] - _wdinl * _seisinfo['ILStep']),
          xlstart=(_seisinfo['XLStart'] + _wdxl * _seisinfo['XLStep']),
          xlend=(_seisinfo['XLEnd'] - _wdxl * _seisinfo['XLStep']),
          zstart=(_seisinfo['ZStart'] + _wdz * _seisinfo['ZStep']),
          zend=(_seisinfo['ZEnd'] - _wdz * _seisinfo['ZStep']))
        if np.shape(_traindata)[0] <= 0:
            vis_msg.print('ERROR in UpdateMl2DAsfe: No training sample found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update 2D-ASFE', 'No training sample found')
            return
        print('UpdateMl2DAsfe: Step 2 - Retrieve and interpolate images: (%d, %d) --> (%d, %d)' % (
         _image_height_old, _image_width_old, _image_height_new, _image_width_new))
        _traindict = {}
        for f in _features:
            _seisdata = self.seisdata[f]
            _traindict[f] = seis_ays.retrieveSeisWindowFrom3DMat(_seisdata, _traindata, seisinfo=(self.survinfo), wdinl=_wdinl,
              wdxl=_wdxl,
              wdz=_wdz,
              verbose=False)[:, 3:]

        if self.traindataconfig['RemoveInvariantFeature_Checked']:
            for f in _features:
                _traindict = ml_aug.removeInvariantFeature(_traindict, f)
                if basic_mdt.maxDictConstantRow(_traindict) <= 0:
                    vis_msg.print('ERROR in UpdateMl2DAsfe: No training sample found', type='error')
                    QtWidgets.QMessageBox.critical(self.msgbox, 'Update 2D-ASFE', 'No training sample found')
                    return

        if _image_height_new != _image_height_old or _image_width_new != _image_width_old:
            for f in _features:
                _traindict[f] = basic_image.changeImageSize((_traindict[f]), image_height=_image_height_old,
                  image_width=_image_width_old,
                  image_height_new=_image_height_new,
                  image_width_new=_image_width_new)

        for f in _features:
            _traindict[f], _traindict[_target] = self.makeTarget(_traindict[f], _image_height_new, _image_width_new)

        print('UpdateMl2DAsfe: A total of %d valid training samples' % basic_mdt.maxDictConstantRow(_traindict))
        print('UpdateMl2DAsfe: Step 3 - Start training')
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Update 2D-ASFE')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _cnnlog = ml_cnn.updateCNNClassifier(_traindict, nepoch=_nepoch,
          batchsize=_batchsize,
          learningrate=_learning_rate,
          dropoutprobfclayer=_dropout_prob_fclayer,
          cnnpath=(self.modelpath),
          cnnname=(self.modelname),
          save2disk=True,
          savepath=_savepath,
          savename=_savename,
          qpgsdlg=_pgsdlg)
        QtWidgets.QMessageBox.information(self.msgbox, 'Update 2D-ASFE', 'ASFE updated successfully')
        reply = QtWidgets.QMessageBox.question(self.msgbox, 'Update 2D-ASFE', 'View learning matrix?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            _viewmllearnmat = QtWidgets.QDialog()
            _gui = gui_viewmllearnmat()
            _gui.learnmat = _cnnlog['learning_curve']
            self.linestyle = self.linestyle
            _gui.fontstyle = self.fontstyle
            _gui.setupGUI(_viewmllearnmat)
            _viewmllearnmat.exec()
            _viewmllearnmat.show()

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
        else:
            return True

    def checkSeisData(self, f):
        self.refreshMsgBox()
        return seis_ays.isSeis3DMatConsistentWithSeisInfo(self.seisdata[f], self.survinfo)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UpdateMl2DAsfe = QtWidgets.QWidget()
    gui = updateml2dasfe()
    gui.setupGUI(UpdateMl2DAsfe)
    UpdateMl2DAsfe.show()
    sys.exit(app.exec_())