# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\updateml2dcnn.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 41410 bytes
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
import cognitivegeo.src.gui.viewml2dcnn as gui_viewml2dcnn
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class updateml2dcnn(object):
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
    traindataconfig['BalanceTarget_Enabled'] = True
    traindataconfig['BalanceTarget_Checked'] = False
    traindataconfig['RotateFeature_Enabled'] = True
    traindataconfig['RotateFeature_Checked'] = False
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False

    def setupGUI(self, UpdateMl2DCnn):
        UpdateMl2DCnn.setObjectName('UpdateMl2DCnn')
        UpdateMl2DCnn.setFixedSize(800, 540)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UpdateMl2DCnn.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(UpdateMl2DCnn)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(UpdateMl2DCnn)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lblornt = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(UpdateMl2DCnn)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 220, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 220, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 220, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 260, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 260, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 220, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 220, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 220, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 260, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 260, 40, 30))
        self.lbltarget = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(UpdateMl2DCnn)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 310, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(UpdateMl2DCnn)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(UpdateMl2DCnn)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 130))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(UpdateMl2DCnn)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 140, 180, 130))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(UpdateMl2DCnn)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 360, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 360, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 400, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 400, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 400, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 400, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 440, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 440, 40, 30))
        self.lblfcdropout = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblfcdropout.setObjectName('lblfcdropout')
        self.lblfcdropout.setGeometry(QtCore.QRect(210, 440, 130, 30))
        self.ldtfcdropout = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtfcdropout.setObjectName('ldtfcdropout')
        self.ldtfcdropout.setGeometry(QtCore.QRect(350, 440, 40, 30))
        self.lblsave = QtWidgets.QLabel(UpdateMl2DCnn)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 490, 100, 30))
        self.ldtsave = QtWidgets.QLineEdit(UpdateMl2DCnn)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(110, 490, 210, 30))
        self.btnsave = QtWidgets.QPushButton(UpdateMl2DCnn)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 490, 60, 30))
        self.btnapply = QtWidgets.QPushButton(UpdateMl2DCnn)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 490, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(UpdateMl2DCnn)
        self.msgbox.setObjectName('msgbox')
        _center_x = UpdateMl2DCnn.geometry().center().x()
        _center_y = UpdateMl2DCnn.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(UpdateMl2DCnn)
        QtCore.QMetaObject.connectSlotsByName(UpdateMl2DCnn)

    def retranslateGUI(self, UpdateMl2DCnn):
        self.dialog = UpdateMl2DCnn
        _translate = QtCore.QCoreApplication.translate
        UpdateMl2DCnn.setWindowTitle(_translate('UpdateMl2DCnn', 'Update 2D-CNN'))
        self.lblfrom.setText(_translate('UpdateMl2DCnn', 'Select network:'))
        self.ldtfrom.setText(_translate('UpdateMl2DCnn', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('UpdateMl2DCnn', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('UpdateMl2DCnn', 'Training features:'))
        self.lblornt.setText(_translate('UpdateMl2DCnn', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.lbltarget.setText(_translate('UpdateMl2DCnn', 'Training target:'))
        self.lbloldsize.setText(_translate('UpdateMl2DCnn', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('UpdateMl2DCnn', 'height='))
        self.ldtoldheight.setText(_translate('UpdateMl2DCnn', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('UpdateMl2DCnn', 'width='))
        self.ldtoldwidth.setText(_translate('UpdateMl2DCnn', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('UpdateMl2DCnn', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('UpdateMl2DCnn', 'height='))
        self.ldtnewheight.setText(_translate('UpdateMl2DCnn', ''))
        self.ldtnewheight.setEnabled(False)
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('UpdateMl2DCnn', 'width='))
        self.ldtnewwidth.setText(_translate('UpdateMl2DCnn', ''))
        self.ldtnewwidth.setEnabled(False)
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('UpdateMl2DCnn', 'Pre-trained CNN architecture:'))
        self.btnviewnetwork.setText(_translate('UpdateMl2DCnn', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('UpdateMl2DCnn', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('UpdateMl2DCnn', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblnfclayer.setText(_translate('UpdateMl2DCnn', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('UpdateMl2DCnn', ''))
        self.ldtnfclayer.setEnabled(False)
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblmasksize.setText(_translate('UpdateMl2DCnn', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('UpdateMl2DCnn', 'height='))
        self.ldtmaskheight.setText(_translate('UpdateMl2DCnn', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('UpdateMl2DCnn', 'width='))
        self.ldtmaskwidth.setText(_translate('UpdateMl2DCnn', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('UpdateMl2DCnn', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('UpdateMl2DCnn', 'height='))
        self.ldtpoolheight.setText(_translate('UpdateMl2DCnn', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('UpdateMl2DCnn', 'width='))
        self.ldtpoolwidth.setText(_translate('UpdateMl2DCnn', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.btnconfigtraindata.setText(_translate('UpdateMl2DCnn', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lblpara.setText(_translate('UpdateMl2DCnn', 'Specify update parameters:'))
        self.lblnepoch.setText(_translate('UpdateMl2DCnn', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('UpdateMl2DCnn', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('UpdateMl2DCnn', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('UpdateMl2DCnn', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('UpdateMl2DCnn', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('UpdateMl2DCnn', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfcdropout.setText(_translate('UpdateMl2DCnn', 'MLP dropout rate:'))
        self.lblfcdropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtfcdropout.setText(_translate('UpdateMl2DCnn', '0.5'))
        self.ldtfcdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('UpdateMl2DCnn', 'Save new-CNN to:'))
        self.ldtsave.setText(_translate('UpdateMl2DCnn', ''))
        self.btnsave.setText(_translate('UpdateMl2DCnn', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('UpdateMl2DCnn', 'Update 2D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnUpdateMl2DCnn)

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
            self.cbbtarget.clear()
            self.cbbtarget.addItem(self.modelinfo['target'])
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
            self.cbbtarget.clear()
            self.btnviewnetwork.setEnabled(False)
            self.ldtnconvblock.setText('')
            self.ldtnfclayer.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')

    def clickBtnFrom(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select CNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def clickBtnViewNetwork(self):
        _viewmlcnn = QtWidgets.QDialog()
        _gui = gui_viewml2dcnn()
        _gui.linestyle = self.linestyle
        _gui.maskstyle = self.maskstyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewmlcnn)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewmlcnn.exec()
        _viewmlcnn.show()

    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Save CNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
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

    def clickBtnUpdateMl2DCnn--- This code section failed: ---

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
               24  LOAD_STR                 'ERROR in UpdateMl2DCnn: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 518        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 519        44  LOAD_STR                 'Update 2D-CNN'

 L. 520        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 521        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 523        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkCNNModel
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
               80  LOAD_STR                 'ERROR in UpdateMl2DCnn: No pre-CNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 525        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 526       100  LOAD_STR                 'Update 2D-CNN'

 L. 527       102  LOAD_STR                 'No pre-CNN network found'
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
              146  LOAD_STR                 "ERROR in UpdateMl2DCnn: Feature '%s' not found in seismic data"
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

 L. 535       170  LOAD_STR                 'Update 2D-CNN'

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

 L. 538       194  LOAD_FAST                'self'
              196  LOAD_ATTR                modelinfo
              198  LOAD_STR                 'target'
              200  BINARY_SUBSCR    
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                seisdata
              206  LOAD_METHOD              keys
              208  CALL_METHOD_0         0  '0 positional arguments'
              210  COMPARE_OP               not-in
          212_214  POP_JUMP_IF_FALSE   276  'to 276'

 L. 539       216  LOAD_GLOBAL              vis_msg
              218  LOAD_ATTR                print
              220  LOAD_STR                 "ERROR in UpdateMl2DCnn: Target label '%s' not found in seismic data"

 L. 540       222  LOAD_FAST                'self'
              224  LOAD_ATTR                modelinfo
              226  LOAD_STR                 'target'
              228  BINARY_SUBSCR    
              230  BINARY_MODULO    
              232  LOAD_STR                 'error'
              234  LOAD_CONST               ('type',)
              236  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              238  POP_TOP          

 L. 541       240  LOAD_GLOBAL              QtWidgets
              242  LOAD_ATTR                QMessageBox
              244  LOAD_METHOD              critical
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                msgbox

 L. 542       250  LOAD_STR                 'Update 2D-CNN'

 L. 543       252  LOAD_STR                 "Target label '"
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                modelinfo
              258  LOAD_STR                 'target'
              260  BINARY_SUBSCR    
              262  BINARY_ADD       
              264  LOAD_STR                 ' not found in seismic data'
              266  BINARY_ADD       
              268  CALL_METHOD_3         3  '3 positional arguments'
              270  POP_TOP          

 L. 544       272  LOAD_CONST               None
              274  RETURN_VALUE     
            276_0  COME_FROM           212  '212'

 L. 546       276  LOAD_GLOBAL              basic_data
              278  LOAD_METHOD              str2int
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                ldtoldheight
              284  LOAD_METHOD              text
              286  CALL_METHOD_0         0  '0 positional arguments'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  STORE_FAST               '_image_height_old'

 L. 547       292  LOAD_GLOBAL              basic_data
              294  LOAD_METHOD              str2int
              296  LOAD_FAST                'self'
              298  LOAD_ATTR                ldtoldwidth
              300  LOAD_METHOD              text
              302  CALL_METHOD_0         0  '0 positional arguments'
              304  CALL_METHOD_1         1  '1 positional argument'
              306  STORE_FAST               '_image_width_old'

 L. 548       308  LOAD_GLOBAL              basic_data
              310  LOAD_METHOD              str2int
              312  LOAD_FAST                'self'
              314  LOAD_ATTR                ldtnewheight
              316  LOAD_METHOD              text
              318  CALL_METHOD_0         0  '0 positional arguments'
              320  CALL_METHOD_1         1  '1 positional argument'
              322  STORE_FAST               '_image_height_new'

 L. 549       324  LOAD_GLOBAL              basic_data
              326  LOAD_METHOD              str2int
              328  LOAD_FAST                'self'
              330  LOAD_ATTR                ldtnewwidth
              332  LOAD_METHOD              text
              334  CALL_METHOD_0         0  '0 positional arguments'
              336  CALL_METHOD_1         1  '1 positional argument'
              338  STORE_FAST               '_image_width_new'

 L. 550       340  LOAD_FAST                '_image_height_old'
              342  LOAD_CONST               False
              344  COMPARE_OP               is
          346_348  POP_JUMP_IF_TRUE    380  'to 380'
              350  LOAD_FAST                '_image_width_old'
              352  LOAD_CONST               False
              354  COMPARE_OP               is
          356_358  POP_JUMP_IF_TRUE    380  'to 380'

 L. 551       360  LOAD_FAST                '_image_height_new'
              362  LOAD_CONST               False
              364  COMPARE_OP               is
          366_368  POP_JUMP_IF_TRUE    380  'to 380'
              370  LOAD_FAST                '_image_width_new'
              372  LOAD_CONST               False
              374  COMPARE_OP               is
          376_378  POP_JUMP_IF_FALSE   416  'to 416'
            380_0  COME_FROM           366  '366'
            380_1  COME_FROM           356  '356'
            380_2  COME_FROM           346  '346'

 L. 552       380  LOAD_GLOBAL              vis_msg
              382  LOAD_ATTR                print
              384  LOAD_STR                 'ERROR in UpdateMl2DCnn: Non-integer feature size'
              386  LOAD_STR                 'error'
              388  LOAD_CONST               ('type',)
              390  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              392  POP_TOP          

 L. 553       394  LOAD_GLOBAL              QtWidgets
              396  LOAD_ATTR                QMessageBox
              398  LOAD_METHOD              critical
              400  LOAD_FAST                'self'
              402  LOAD_ATTR                msgbox

 L. 554       404  LOAD_STR                 'Update 2D-CNN'

 L. 555       406  LOAD_STR                 'Non-integer feature size'
              408  CALL_METHOD_3         3  '3 positional arguments'
              410  POP_TOP          

 L. 556       412  LOAD_CONST               None
              414  RETURN_VALUE     
            416_0  COME_FROM           376  '376'

 L. 557       416  LOAD_FAST                '_image_height_old'
              418  LOAD_CONST               2
              420  COMPARE_OP               <
          422_424  POP_JUMP_IF_TRUE    456  'to 456'
              426  LOAD_FAST                '_image_width_old'
              428  LOAD_CONST               2
              430  COMPARE_OP               <
          432_434  POP_JUMP_IF_TRUE    456  'to 456'

 L. 558       436  LOAD_FAST                '_image_height_new'
              438  LOAD_CONST               2
              440  COMPARE_OP               <
          442_444  POP_JUMP_IF_TRUE    456  'to 456'
              446  LOAD_FAST                '_image_width_new'
              448  LOAD_CONST               2
              450  COMPARE_OP               <
          452_454  POP_JUMP_IF_FALSE   492  'to 492'
            456_0  COME_FROM           442  '442'
            456_1  COME_FROM           432  '432'
            456_2  COME_FROM           422  '422'

 L. 559       456  LOAD_GLOBAL              vis_msg
              458  LOAD_ATTR                print
              460  LOAD_STR                 'ERROR in UpdateMl2DCnn: Features are not 2D'
              462  LOAD_STR                 'error'
              464  LOAD_CONST               ('type',)
              466  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              468  POP_TOP          

 L. 560       470  LOAD_GLOBAL              QtWidgets
              472  LOAD_ATTR                QMessageBox
              474  LOAD_METHOD              critical
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                msgbox

 L. 561       480  LOAD_STR                 'Update 2D-CNN'

 L. 562       482  LOAD_STR                 'Features are not 2D'
              484  CALL_METHOD_3         3  '3 positional arguments'
              486  POP_TOP          

 L. 563       488  LOAD_CONST               None
              490  RETURN_VALUE     
            492_0  COME_FROM           452  '452'

 L. 565       492  LOAD_CONST               2
              494  LOAD_GLOBAL              int
              496  LOAD_FAST                '_image_height_old'
              498  LOAD_CONST               2
              500  BINARY_TRUE_DIVIDE
              502  CALL_FUNCTION_1       1  '1 positional argument'
              504  BINARY_MULTIPLY  
              506  LOAD_CONST               1
              508  BINARY_ADD       
              510  STORE_FAST               '_image_height_old'

 L. 566       512  LOAD_CONST               2
              514  LOAD_GLOBAL              int
              516  LOAD_FAST                '_image_width_old'
              518  LOAD_CONST               2
              520  BINARY_TRUE_DIVIDE
              522  CALL_FUNCTION_1       1  '1 positional argument'
              524  BINARY_MULTIPLY  
              526  LOAD_CONST               1
              528  BINARY_ADD       
              530  STORE_FAST               '_image_width_old'

 L. 568       532  LOAD_FAST                'self'
              534  LOAD_ATTR                modelinfo
              536  LOAD_STR                 'feature_list'
              538  BINARY_SUBSCR    
              540  STORE_FAST               '_features'

 L. 569       542  LOAD_FAST                'self'
              544  LOAD_ATTR                modelinfo
              546  LOAD_STR                 'target'
              548  BINARY_SUBSCR    
              550  STORE_FAST               '_target'

 L. 571       552  LOAD_GLOBAL              basic_data
              554  LOAD_METHOD              str2int
              556  LOAD_FAST                'self'
              558  LOAD_ATTR                ldtnepoch
              560  LOAD_METHOD              text
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  CALL_METHOD_1         1  '1 positional argument'
              566  STORE_FAST               '_nepoch'

 L. 572       568  LOAD_GLOBAL              basic_data
              570  LOAD_METHOD              str2int
              572  LOAD_FAST                'self'
              574  LOAD_ATTR                ldtbatchsize
              576  LOAD_METHOD              text
              578  CALL_METHOD_0         0  '0 positional arguments'
              580  CALL_METHOD_1         1  '1 positional argument'
              582  STORE_FAST               '_batchsize'

 L. 573       584  LOAD_GLOBAL              basic_data
              586  LOAD_METHOD              str2float
              588  LOAD_FAST                'self'
              590  LOAD_ATTR                ldtlearnrate
              592  LOAD_METHOD              text
              594  CALL_METHOD_0         0  '0 positional arguments'
              596  CALL_METHOD_1         1  '1 positional argument'
              598  STORE_FAST               '_learning_rate'

 L. 574       600  LOAD_GLOBAL              basic_data
              602  LOAD_METHOD              str2float
              604  LOAD_FAST                'self'
              606  LOAD_ATTR                ldtfcdropout
              608  LOAD_METHOD              text
              610  CALL_METHOD_0         0  '0 positional arguments'
              612  CALL_METHOD_1         1  '1 positional argument'
              614  STORE_FAST               '_dropout_prob_fclayer'

 L. 575       616  LOAD_FAST                '_nepoch'
              618  LOAD_CONST               False
              620  COMPARE_OP               is
          622_624  POP_JUMP_IF_TRUE    636  'to 636'
              626  LOAD_FAST                '_nepoch'
              628  LOAD_CONST               0
              630  COMPARE_OP               <=
          632_634  POP_JUMP_IF_FALSE   672  'to 672'
            636_0  COME_FROM           622  '622'

 L. 576       636  LOAD_GLOBAL              vis_msg
              638  LOAD_ATTR                print
              640  LOAD_STR                 'ERROR in UpdateMl2DCnn: Non-positive epoch number'
              642  LOAD_STR                 'error'
              644  LOAD_CONST               ('type',)
              646  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              648  POP_TOP          

 L. 577       650  LOAD_GLOBAL              QtWidgets
              652  LOAD_ATTR                QMessageBox
              654  LOAD_METHOD              critical
              656  LOAD_FAST                'self'
              658  LOAD_ATTR                msgbox

 L. 578       660  LOAD_STR                 'Update 2D-CNN'

 L. 579       662  LOAD_STR                 'Non-positive epoch number'
              664  CALL_METHOD_3         3  '3 positional arguments'
              666  POP_TOP          

 L. 580       668  LOAD_CONST               None
              670  RETURN_VALUE     
            672_0  COME_FROM           632  '632'

 L. 581       672  LOAD_FAST                '_batchsize'
              674  LOAD_CONST               False
              676  COMPARE_OP               is
          678_680  POP_JUMP_IF_TRUE    692  'to 692'
              682  LOAD_FAST                '_batchsize'
              684  LOAD_CONST               0
              686  COMPARE_OP               <=
          688_690  POP_JUMP_IF_FALSE   728  'to 728'
            692_0  COME_FROM           678  '678'

 L. 582       692  LOAD_GLOBAL              vis_msg
              694  LOAD_ATTR                print
              696  LOAD_STR                 'ERROR in UpdateMl2DCnn: Non-positive batch size'
              698  LOAD_STR                 'error'
              700  LOAD_CONST               ('type',)
              702  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              704  POP_TOP          

 L. 583       706  LOAD_GLOBAL              QtWidgets
              708  LOAD_ATTR                QMessageBox
              710  LOAD_METHOD              critical
              712  LOAD_FAST                'self'
              714  LOAD_ATTR                msgbox

 L. 584       716  LOAD_STR                 'Update 2D-CNN'

 L. 585       718  LOAD_STR                 'Non-positive batch size'
              720  CALL_METHOD_3         3  '3 positional arguments'
              722  POP_TOP          

 L. 586       724  LOAD_CONST               None
              726  RETURN_VALUE     
            728_0  COME_FROM           688  '688'

 L. 587       728  LOAD_FAST                '_learning_rate'
              730  LOAD_CONST               False
              732  COMPARE_OP               is
          734_736  POP_JUMP_IF_TRUE    748  'to 748'
              738  LOAD_FAST                '_learning_rate'
              740  LOAD_CONST               0
              742  COMPARE_OP               <=
          744_746  POP_JUMP_IF_FALSE   784  'to 784'
            748_0  COME_FROM           734  '734'

 L. 588       748  LOAD_GLOBAL              vis_msg
              750  LOAD_ATTR                print
              752  LOAD_STR                 'ERROR in UpdateMl2DCnn: Non-positive learning rate'
              754  LOAD_STR                 'error'
              756  LOAD_CONST               ('type',)
              758  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              760  POP_TOP          

 L. 589       762  LOAD_GLOBAL              QtWidgets
              764  LOAD_ATTR                QMessageBox
              766  LOAD_METHOD              critical
              768  LOAD_FAST                'self'
              770  LOAD_ATTR                msgbox

 L. 590       772  LOAD_STR                 'Update 2D-CNN'

 L. 591       774  LOAD_STR                 'Non-positive learning rate'
              776  CALL_METHOD_3         3  '3 positional arguments'
              778  POP_TOP          

 L. 592       780  LOAD_CONST               None
              782  RETURN_VALUE     
            784_0  COME_FROM           744  '744'

 L. 593       784  LOAD_FAST                '_dropout_prob_fclayer'
              786  LOAD_CONST               False
              788  COMPARE_OP               is
          790_792  POP_JUMP_IF_TRUE    804  'to 804'
              794  LOAD_FAST                '_dropout_prob_fclayer'
              796  LOAD_CONST               0
              798  COMPARE_OP               <=
          800_802  POP_JUMP_IF_FALSE   840  'to 840'
            804_0  COME_FROM           790  '790'

 L. 594       804  LOAD_GLOBAL              vis_msg
              806  LOAD_ATTR                print
              808  LOAD_STR                 'ERROR in UpdateMl2DCnn: Negative dropout rate'
              810  LOAD_STR                 'error'
              812  LOAD_CONST               ('type',)
              814  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              816  POP_TOP          

 L. 595       818  LOAD_GLOBAL              QtWidgets
              820  LOAD_ATTR                QMessageBox
              822  LOAD_METHOD              critical
              824  LOAD_FAST                'self'
              826  LOAD_ATTR                msgbox

 L. 596       828  LOAD_STR                 'Update 2D-CNN'

 L. 597       830  LOAD_STR                 'Negative dropout rate'
              832  CALL_METHOD_3         3  '3 positional arguments'
              834  POP_TOP          

 L. 598       836  LOAD_CONST               None
              838  RETURN_VALUE     
            840_0  COME_FROM           800  '800'

 L. 600       840  LOAD_GLOBAL              len
              842  LOAD_FAST                'self'
              844  LOAD_ATTR                ldtsave
              846  LOAD_METHOD              text
              848  CALL_METHOD_0         0  '0 positional arguments'
              850  CALL_FUNCTION_1       1  '1 positional argument'
              852  LOAD_CONST               1
              854  COMPARE_OP               <
          856_858  POP_JUMP_IF_FALSE   896  'to 896'

 L. 601       860  LOAD_GLOBAL              vis_msg
              862  LOAD_ATTR                print
              864  LOAD_STR                 'ERROR in UpdateMl2DCnn: No name specified for new-CNN'
              866  LOAD_STR                 'error'
              868  LOAD_CONST               ('type',)
              870  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              872  POP_TOP          

 L. 602       874  LOAD_GLOBAL              QtWidgets
              876  LOAD_ATTR                QMessageBox
              878  LOAD_METHOD              critical
              880  LOAD_FAST                'self'
              882  LOAD_ATTR                msgbox

 L. 603       884  LOAD_STR                 'Update 2D-CNN'

 L. 604       886  LOAD_STR                 'No name specified for new-CNN'
              888  CALL_METHOD_3         3  '3 positional arguments'
              890  POP_TOP          

 L. 605       892  LOAD_CONST               None
              894  RETURN_VALUE     
            896_0  COME_FROM           856  '856'

 L. 606       896  LOAD_GLOBAL              os
              898  LOAD_ATTR                path
              900  LOAD_METHOD              dirname
              902  LOAD_FAST                'self'
              904  LOAD_ATTR                ldtsave
              906  LOAD_METHOD              text
              908  CALL_METHOD_0         0  '0 positional arguments'
              910  CALL_METHOD_1         1  '1 positional argument'
              912  STORE_FAST               '_savepath'

 L. 607       914  LOAD_GLOBAL              os
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

 L. 609       944  LOAD_CONST               0
              946  STORE_FAST               '_wdinl'

 L. 610       948  LOAD_CONST               0
              950  STORE_FAST               '_wdxl'

 L. 611       952  LOAD_CONST               0
              954  STORE_FAST               '_wdz'

 L. 612       956  LOAD_FAST                'self'
              958  LOAD_ATTR                cbbornt
              960  LOAD_METHOD              currentIndex
              962  CALL_METHOD_0         0  '0 positional arguments'
              964  LOAD_CONST               0
              966  COMPARE_OP               ==
          968_970  POP_JUMP_IF_FALSE   996  'to 996'

 L. 613       972  LOAD_GLOBAL              int
              974  LOAD_FAST                '_image_width_old'
              976  LOAD_CONST               2
              978  BINARY_TRUE_DIVIDE
              980  CALL_FUNCTION_1       1  '1 positional argument'
              982  STORE_FAST               '_wdxl'

 L. 614       984  LOAD_GLOBAL              int
              986  LOAD_FAST                '_image_height_old'
              988  LOAD_CONST               2
              990  BINARY_TRUE_DIVIDE
              992  CALL_FUNCTION_1       1  '1 positional argument'
              994  STORE_FAST               '_wdz'
            996_0  COME_FROM           968  '968'

 L. 615       996  LOAD_FAST                'self'
              998  LOAD_ATTR                cbbornt
             1000  LOAD_METHOD              currentIndex
             1002  CALL_METHOD_0         0  '0 positional arguments'
             1004  LOAD_CONST               1
             1006  COMPARE_OP               ==
         1008_1010  POP_JUMP_IF_FALSE  1036  'to 1036'

 L. 616      1012  LOAD_GLOBAL              int
             1014  LOAD_FAST                '_image_width_old'
             1016  LOAD_CONST               2
             1018  BINARY_TRUE_DIVIDE
             1020  CALL_FUNCTION_1       1  '1 positional argument'
             1022  STORE_FAST               '_wdinl'

 L. 617      1024  LOAD_GLOBAL              int
             1026  LOAD_FAST                '_image_height_old'
             1028  LOAD_CONST               2
             1030  BINARY_TRUE_DIVIDE
             1032  CALL_FUNCTION_1       1  '1 positional argument'
             1034  STORE_FAST               '_wdz'
           1036_0  COME_FROM          1008  '1008'

 L. 618      1036  LOAD_FAST                'self'
             1038  LOAD_ATTR                cbbornt
             1040  LOAD_METHOD              currentIndex
             1042  CALL_METHOD_0         0  '0 positional arguments'
             1044  LOAD_CONST               2
             1046  COMPARE_OP               ==
         1048_1050  POP_JUMP_IF_FALSE  1076  'to 1076'

 L. 619      1052  LOAD_GLOBAL              int
             1054  LOAD_FAST                '_image_width_old'
             1056  LOAD_CONST               2
             1058  BINARY_TRUE_DIVIDE
             1060  CALL_FUNCTION_1       1  '1 positional argument'
             1062  STORE_FAST               '_wdinl'

 L. 620      1064  LOAD_GLOBAL              int
             1066  LOAD_FAST                '_image_height_old'
             1068  LOAD_CONST               2
             1070  BINARY_TRUE_DIVIDE
             1072  CALL_FUNCTION_1       1  '1 positional argument'
             1074  STORE_FAST               '_wdxl'
           1076_0  COME_FROM          1048  '1048'

 L. 622      1076  LOAD_FAST                'self'
             1078  LOAD_ATTR                survinfo
             1080  STORE_FAST               '_seisinfo'

 L. 624      1082  LOAD_GLOBAL              print
             1084  LOAD_STR                 'UpdateMl2DCnn: Step 1 - Get training samples:'
             1086  CALL_FUNCTION_1       1  '1 positional argument'
             1088  POP_TOP          

 L. 625      1090  LOAD_FAST                'self'
             1092  LOAD_ATTR                traindataconfig
             1094  LOAD_STR                 'TrainPointSet'
             1096  BINARY_SUBSCR    
             1098  STORE_FAST               '_trainpoint'

 L. 626      1100  LOAD_GLOBAL              np
             1102  LOAD_METHOD              zeros
             1104  LOAD_CONST               0
             1106  LOAD_CONST               3
             1108  BUILD_LIST_2          2 
             1110  CALL_METHOD_1         1  '1 positional argument'
             1112  STORE_FAST               '_traindata'

 L. 627      1114  SETUP_LOOP         1190  'to 1190'
             1116  LOAD_FAST                '_trainpoint'
             1118  GET_ITER         
           1120_0  COME_FROM          1138  '1138'
             1120  FOR_ITER           1188  'to 1188'
             1122  STORE_FAST               '_p'

 L. 628      1124  LOAD_GLOBAL              point_ays
             1126  LOAD_METHOD              checkPoint
             1128  LOAD_FAST                'self'
             1130  LOAD_ATTR                pointsetdata
             1132  LOAD_FAST                '_p'
             1134  BINARY_SUBSCR    
             1136  CALL_METHOD_1         1  '1 positional argument'
         1138_1140  POP_JUMP_IF_FALSE  1120  'to 1120'

 L. 629      1142  LOAD_GLOBAL              basic_mdt
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

 L. 630      1166  LOAD_GLOBAL              np
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

 L. 631      1190  LOAD_GLOBAL              seis_ays
             1192  LOAD_ATTR                removeOutofSurveySample
             1194  LOAD_FAST                '_traindata'

 L. 632      1196  LOAD_FAST                '_seisinfo'
             1198  LOAD_STR                 'ILStart'
             1200  BINARY_SUBSCR    
             1202  LOAD_FAST                '_wdinl'
             1204  LOAD_FAST                '_seisinfo'
             1206  LOAD_STR                 'ILStep'
             1208  BINARY_SUBSCR    
             1210  BINARY_MULTIPLY  
             1212  BINARY_ADD       

 L. 633      1214  LOAD_FAST                '_seisinfo'
             1216  LOAD_STR                 'ILEnd'
             1218  BINARY_SUBSCR    
             1220  LOAD_FAST                '_wdinl'
             1222  LOAD_FAST                '_seisinfo'
             1224  LOAD_STR                 'ILStep'
             1226  BINARY_SUBSCR    
             1228  BINARY_MULTIPLY  
             1230  BINARY_SUBTRACT  

 L. 634      1232  LOAD_FAST                '_seisinfo'
             1234  LOAD_STR                 'XLStart'
             1236  BINARY_SUBSCR    
             1238  LOAD_FAST                '_wdxl'
             1240  LOAD_FAST                '_seisinfo'
             1242  LOAD_STR                 'XLStep'
             1244  BINARY_SUBSCR    
             1246  BINARY_MULTIPLY  
             1248  BINARY_ADD       

 L. 635      1250  LOAD_FAST                '_seisinfo'
             1252  LOAD_STR                 'XLEnd'
             1254  BINARY_SUBSCR    
             1256  LOAD_FAST                '_wdxl'
             1258  LOAD_FAST                '_seisinfo'
             1260  LOAD_STR                 'XLStep'
             1262  BINARY_SUBSCR    
             1264  BINARY_MULTIPLY  
             1266  BINARY_SUBTRACT  

 L. 636      1268  LOAD_FAST                '_seisinfo'
             1270  LOAD_STR                 'ZStart'
             1272  BINARY_SUBSCR    
             1274  LOAD_FAST                '_wdz'
             1276  LOAD_FAST                '_seisinfo'
             1278  LOAD_STR                 'ZStep'
             1280  BINARY_SUBSCR    
             1282  BINARY_MULTIPLY  
             1284  BINARY_ADD       

 L. 637      1286  LOAD_FAST                '_seisinfo'
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

 L. 640      1310  LOAD_GLOBAL              np
             1312  LOAD_METHOD              shape
             1314  LOAD_FAST                '_traindata'
             1316  CALL_METHOD_1         1  '1 positional argument'
             1318  LOAD_CONST               0
             1320  BINARY_SUBSCR    
             1322  LOAD_CONST               0
             1324  COMPARE_OP               <=
         1326_1328  POP_JUMP_IF_FALSE  1366  'to 1366'

 L. 641      1330  LOAD_GLOBAL              vis_msg
             1332  LOAD_ATTR                print
             1334  LOAD_STR                 'ERROR in UpdateMl2DCnn: No training sample found'
             1336  LOAD_STR                 'error'
             1338  LOAD_CONST               ('type',)
             1340  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1342  POP_TOP          

 L. 642      1344  LOAD_GLOBAL              QtWidgets
             1346  LOAD_ATTR                QMessageBox
             1348  LOAD_METHOD              critical
             1350  LOAD_FAST                'self'
             1352  LOAD_ATTR                msgbox

 L. 643      1354  LOAD_STR                 'Update 2D-CNN'

 L. 644      1356  LOAD_STR                 'No training sample found'
             1358  CALL_METHOD_3         3  '3 positional arguments'
             1360  POP_TOP          

 L. 645      1362  LOAD_CONST               None
             1364  RETURN_VALUE     
           1366_0  COME_FROM          1326  '1326'

 L. 648      1366  LOAD_GLOBAL              print
             1368  LOAD_STR                 'UpdateMl2DCnn: Step 2 - Retrieve and interpolate images: (%d, %d) --> (%d, %d)'

 L. 649      1370  LOAD_FAST                '_image_height_old'
             1372  LOAD_FAST                '_image_width_old'
             1374  LOAD_FAST                '_image_height_new'
             1376  LOAD_FAST                '_image_width_new'
             1378  BUILD_TUPLE_4         4 
             1380  BINARY_MODULO    
             1382  CALL_FUNCTION_1       1  '1 positional argument'
             1384  POP_TOP          

 L. 650      1386  BUILD_MAP_0           0 
             1388  STORE_FAST               '_traindict'

 L. 651      1390  SETUP_LOOP         1462  'to 1462'
             1392  LOAD_FAST                '_features'
             1394  GET_ITER         
             1396  FOR_ITER           1460  'to 1460'
             1398  STORE_FAST               'f'

 L. 652      1400  LOAD_FAST                'self'
             1402  LOAD_ATTR                seisdata
             1404  LOAD_FAST                'f'
             1406  BINARY_SUBSCR    
             1408  STORE_FAST               '_seisdata'

 L. 653      1410  LOAD_GLOBAL              seis_ays
             1412  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1414  LOAD_FAST                '_seisdata'
             1416  LOAD_FAST                '_traindata'
             1418  LOAD_FAST                'self'
             1420  LOAD_ATTR                survinfo

 L. 654      1422  LOAD_FAST                '_wdinl'
             1424  LOAD_FAST                '_wdxl'
             1426  LOAD_FAST                '_wdz'

 L. 655      1428  LOAD_CONST               False
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

 L. 656      1462  LOAD_FAST                '_target'
             1464  LOAD_FAST                '_features'
             1466  COMPARE_OP               not-in
         1468_1470  POP_JUMP_IF_FALSE  1522  'to 1522'

 L. 657      1472  LOAD_FAST                'self'
             1474  LOAD_ATTR                seisdata
             1476  LOAD_FAST                '_target'
             1478  BINARY_SUBSCR    
             1480  STORE_FAST               '_seisdata'

 L. 658      1482  LOAD_GLOBAL              seis_ays
             1484  LOAD_ATTR                retrieveSeisSampleFrom3DMat
             1486  LOAD_FAST                '_seisdata'
             1488  LOAD_FAST                '_traindata'
             1490  LOAD_FAST                'self'
             1492  LOAD_ATTR                survinfo

 L. 659      1494  LOAD_CONST               False
             1496  LOAD_CONST               ('seisinfo', 'verbose')
             1498  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1500  LOAD_CONST               None
             1502  LOAD_CONST               None
             1504  BUILD_SLICE_2         2 
             1506  LOAD_CONST               3
             1508  LOAD_CONST               None
             1510  BUILD_SLICE_2         2 
             1512  BUILD_TUPLE_2         2 
             1514  BINARY_SUBSCR    
             1516  LOAD_FAST                '_traindict'
             1518  LOAD_FAST                '_target'
             1520  STORE_SUBSCR     
           1522_0  COME_FROM          1468  '1468'

 L. 661      1522  LOAD_FAST                'self'
             1524  LOAD_ATTR                traindataconfig
             1526  LOAD_STR                 'RemoveInvariantFeature_Checked'
             1528  BINARY_SUBSCR    
         1530_1532  POP_JUMP_IF_FALSE  1614  'to 1614'

 L. 662      1534  SETUP_LOOP         1614  'to 1614'
             1536  LOAD_FAST                '_features'
             1538  GET_ITER         
           1540_0  COME_FROM          1568  '1568'
             1540  FOR_ITER           1612  'to 1612'
             1542  STORE_FAST               'f'

 L. 663      1544  LOAD_GLOBAL              ml_aug
             1546  LOAD_METHOD              removeInvariantFeature
             1548  LOAD_FAST                '_traindict'
             1550  LOAD_FAST                'f'
             1552  CALL_METHOD_2         2  '2 positional arguments'
             1554  STORE_FAST               '_traindict'

 L. 664      1556  LOAD_GLOBAL              basic_mdt
             1558  LOAD_METHOD              maxDictConstantRow
             1560  LOAD_FAST                '_traindict'
             1562  CALL_METHOD_1         1  '1 positional argument'
             1564  LOAD_CONST               0
             1566  COMPARE_OP               <=
         1568_1570  POP_JUMP_IF_FALSE  1540  'to 1540'

 L. 665      1572  LOAD_GLOBAL              vis_msg
             1574  LOAD_ATTR                print
             1576  LOAD_STR                 'ERROR in UpdateMl2DCnn: No training sample found'
             1578  LOAD_STR                 'error'
             1580  LOAD_CONST               ('type',)
             1582  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1584  POP_TOP          

 L. 666      1586  LOAD_GLOBAL              QtWidgets
             1588  LOAD_ATTR                QMessageBox
             1590  LOAD_METHOD              critical
             1592  LOAD_FAST                'self'
             1594  LOAD_ATTR                msgbox

 L. 667      1596  LOAD_STR                 'Update 2D-CNN'

 L. 668      1598  LOAD_STR                 'No training sample found'
             1600  CALL_METHOD_3         3  '3 positional arguments'
             1602  POP_TOP          

 L. 669      1604  LOAD_CONST               None
             1606  RETURN_VALUE     
         1608_1610  JUMP_BACK          1540  'to 1540'
             1612  POP_BLOCK        
           1614_0  COME_FROM_LOOP     1534  '1534'
           1614_1  COME_FROM          1530  '1530'

 L. 671      1614  LOAD_GLOBAL              np
             1616  LOAD_METHOD              round
             1618  LOAD_FAST                '_traindict'
             1620  LOAD_FAST                '_target'
             1622  BINARY_SUBSCR    
             1624  CALL_METHOD_1         1  '1 positional argument'
             1626  LOAD_METHOD              astype
             1628  LOAD_GLOBAL              int
             1630  CALL_METHOD_1         1  '1 positional argument'
             1632  LOAD_FAST                '_traindict'
             1634  LOAD_FAST                '_target'
             1636  STORE_SUBSCR     

 L. 673      1638  LOAD_FAST                '_image_height_new'
             1640  LOAD_FAST                '_image_height_old'
             1642  COMPARE_OP               !=
         1644_1646  POP_JUMP_IF_TRUE   1658  'to 1658'
             1648  LOAD_FAST                '_image_width_new'
             1650  LOAD_FAST                '_image_width_old'
             1652  COMPARE_OP               !=
         1654_1656  POP_JUMP_IF_FALSE  1702  'to 1702'
           1658_0  COME_FROM          1644  '1644'

 L. 674      1658  SETUP_LOOP         1702  'to 1702'
             1660  LOAD_FAST                '_features'
             1662  GET_ITER         
             1664  FOR_ITER           1700  'to 1700'
             1666  STORE_FAST               'f'

 L. 675      1668  LOAD_GLOBAL              basic_image
             1670  LOAD_ATTR                changeImageSize
             1672  LOAD_FAST                '_traindict'
             1674  LOAD_FAST                'f'
             1676  BINARY_SUBSCR    

 L. 676      1678  LOAD_FAST                '_image_height_old'

 L. 677      1680  LOAD_FAST                '_image_width_old'

 L. 678      1682  LOAD_FAST                '_image_height_new'

 L. 679      1684  LOAD_FAST                '_image_width_new'
             1686  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1688  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1690  LOAD_FAST                '_traindict'
             1692  LOAD_FAST                'f'
             1694  STORE_SUBSCR     
         1696_1698  JUMP_BACK          1664  'to 1664'
             1700  POP_BLOCK        
           1702_0  COME_FROM_LOOP     1658  '1658'
           1702_1  COME_FROM          1654  '1654'

 L. 680      1702  LOAD_FAST                'self'
             1704  LOAD_ATTR                traindataconfig
             1706  LOAD_STR                 'RotateFeature_Checked'
             1708  BINARY_SUBSCR    
             1710  LOAD_CONST               True
             1712  COMPARE_OP               is
         1714_1716  POP_JUMP_IF_FALSE  1846  'to 1846'

 L. 681      1718  SETUP_LOOP         1790  'to 1790'
             1720  LOAD_FAST                '_features'
             1722  GET_ITER         
             1724  FOR_ITER           1788  'to 1788'
             1726  STORE_FAST               'f'

 L. 682      1728  LOAD_FAST                '_image_height_new'
             1730  LOAD_FAST                '_image_width_new'
             1732  COMPARE_OP               ==
         1734_1736  POP_JUMP_IF_FALSE  1762  'to 1762'

 L. 683      1738  LOAD_GLOBAL              ml_aug
             1740  LOAD_METHOD              rotateImage6Way
             1742  LOAD_FAST                '_traindict'
             1744  LOAD_FAST                'f'
             1746  BINARY_SUBSCR    
             1748  LOAD_FAST                '_image_height_new'
             1750  LOAD_FAST                '_image_width_new'
             1752  CALL_METHOD_3         3  '3 positional arguments'
             1754  LOAD_FAST                '_traindict'
             1756  LOAD_FAST                'f'
             1758  STORE_SUBSCR     
             1760  JUMP_BACK          1724  'to 1724'
           1762_0  COME_FROM          1734  '1734'

 L. 685      1762  LOAD_GLOBAL              ml_aug
             1764  LOAD_METHOD              rotateImage4Way
             1766  LOAD_FAST                '_traindict'
             1768  LOAD_FAST                'f'
             1770  BINARY_SUBSCR    
             1772  LOAD_FAST                '_image_height_new'
             1774  LOAD_FAST                '_image_width_new'
             1776  CALL_METHOD_3         3  '3 positional arguments'
             1778  LOAD_FAST                '_traindict'
             1780  LOAD_FAST                'f'
             1782  STORE_SUBSCR     
         1784_1786  JUMP_BACK          1724  'to 1724'
             1788  POP_BLOCK        
           1790_0  COME_FROM_LOOP     1718  '1718'

 L. 687      1790  LOAD_FAST                '_image_height_new'
             1792  LOAD_FAST                '_image_width_new'
             1794  COMPARE_OP               ==
         1796_1798  POP_JUMP_IF_FALSE  1824  'to 1824'

 L. 689      1800  LOAD_GLOBAL              ml_aug
             1802  LOAD_METHOD              rotateImage6Way
             1804  LOAD_FAST                '_traindict'
             1806  LOAD_FAST                '_target'
             1808  BINARY_SUBSCR    
             1810  LOAD_CONST               1
             1812  LOAD_CONST               1
             1814  CALL_METHOD_3         3  '3 positional arguments'
             1816  LOAD_FAST                '_traindict'
             1818  LOAD_FAST                '_target'
             1820  STORE_SUBSCR     
             1822  JUMP_FORWARD       1846  'to 1846'
           1824_0  COME_FROM          1796  '1796'

 L. 692      1824  LOAD_GLOBAL              ml_aug
             1826  LOAD_METHOD              rotateImage4Way
             1828  LOAD_FAST                '_traindict'
             1830  LOAD_FAST                '_target'
             1832  BINARY_SUBSCR    
             1834  LOAD_CONST               1
             1836  LOAD_CONST               1
             1838  CALL_METHOD_3         3  '3 positional arguments'
             1840  LOAD_FAST                '_traindict'
             1842  LOAD_FAST                '_target'
             1844  STORE_SUBSCR     
           1846_0  COME_FROM          1822  '1822'
           1846_1  COME_FROM          1714  '1714'

 L. 694      1846  LOAD_GLOBAL              print
             1848  LOAD_STR                 'UpdateMl2DCnn: A total of %d valid training samples'
             1850  LOAD_GLOBAL              basic_mdt
             1852  LOAD_METHOD              maxDictConstantRow
             1854  LOAD_FAST                '_traindict'
             1856  CALL_METHOD_1         1  '1 positional argument'
             1858  BINARY_MODULO    
             1860  CALL_FUNCTION_1       1  '1 positional argument'
             1862  POP_TOP          

 L. 696      1864  LOAD_GLOBAL              print
             1866  LOAD_STR                 'UpdateMl2DCnn: Step 3 - Balance labels'
             1868  CALL_FUNCTION_1       1  '1 positional argument'
             1870  POP_TOP          

 L. 697      1872  LOAD_FAST                'self'
             1874  LOAD_ATTR                traindataconfig
             1876  LOAD_STR                 'BalanceTarget_Checked'
             1878  BINARY_SUBSCR    
         1880_1882  POP_JUMP_IF_FALSE  1924  'to 1924'

 L. 698      1884  LOAD_GLOBAL              ml_aug
             1886  LOAD_METHOD              balanceLabelbyExtension
             1888  LOAD_FAST                '_traindict'
             1890  LOAD_FAST                '_target'
             1892  CALL_METHOD_2         2  '2 positional arguments'
             1894  STORE_FAST               '_traindict'

 L. 699      1896  LOAD_GLOBAL              print
             1898  LOAD_STR                 'UpdateMl2DCnn: A total of %d training samples after balance'
             1900  LOAD_GLOBAL              np
             1902  LOAD_METHOD              shape
             1904  LOAD_FAST                '_traindict'
             1906  LOAD_FAST                '_target'
             1908  BINARY_SUBSCR    
             1910  CALL_METHOD_1         1  '1 positional argument'
             1912  LOAD_CONST               0
             1914  BINARY_SUBSCR    
             1916  BINARY_MODULO    
             1918  CALL_FUNCTION_1       1  '1 positional argument'
             1920  POP_TOP          
             1922  JUMP_FORWARD       1932  'to 1932'
           1924_0  COME_FROM          1880  '1880'

 L. 701      1924  LOAD_GLOBAL              print
             1926  LOAD_STR                 'UpdateMl2DCnn: No balance applied'
             1928  CALL_FUNCTION_1       1  '1 positional argument'
             1930  POP_TOP          
           1932_0  COME_FROM          1922  '1922'

 L. 703      1932  LOAD_GLOBAL              print
             1934  LOAD_STR                 'UpdateMl2DCnn: Step 4 - Start training'
             1936  CALL_FUNCTION_1       1  '1 positional argument'
             1938  POP_TOP          

 L. 705      1940  LOAD_GLOBAL              QtWidgets
             1942  LOAD_METHOD              QProgressDialog
             1944  CALL_METHOD_0         0  '0 positional arguments'
             1946  STORE_FAST               '_pgsdlg'

 L. 706      1948  LOAD_GLOBAL              QtGui
             1950  LOAD_METHOD              QIcon
             1952  CALL_METHOD_0         0  '0 positional arguments'
             1954  STORE_FAST               'icon'

 L. 707      1956  LOAD_FAST                'icon'
             1958  LOAD_METHOD              addPixmap
             1960  LOAD_GLOBAL              QtGui
             1962  LOAD_METHOD              QPixmap
             1964  LOAD_GLOBAL              os
             1966  LOAD_ATTR                path
             1968  LOAD_METHOD              join
             1970  LOAD_FAST                'self'
             1972  LOAD_ATTR                iconpath
             1974  LOAD_STR                 'icons/update.png'
             1976  CALL_METHOD_2         2  '2 positional arguments'
             1978  CALL_METHOD_1         1  '1 positional argument'

 L. 708      1980  LOAD_GLOBAL              QtGui
             1982  LOAD_ATTR                QIcon
             1984  LOAD_ATTR                Normal
             1986  LOAD_GLOBAL              QtGui
             1988  LOAD_ATTR                QIcon
             1990  LOAD_ATTR                Off
             1992  CALL_METHOD_3         3  '3 positional arguments'
             1994  POP_TOP          

 L. 709      1996  LOAD_FAST                '_pgsdlg'
             1998  LOAD_METHOD              setWindowIcon
             2000  LOAD_FAST                'icon'
             2002  CALL_METHOD_1         1  '1 positional argument'
             2004  POP_TOP          

 L. 710      2006  LOAD_FAST                '_pgsdlg'
             2008  LOAD_METHOD              setWindowTitle
             2010  LOAD_STR                 'Update 2D-CNN'
             2012  CALL_METHOD_1         1  '1 positional argument'
             2014  POP_TOP          

 L. 711      2016  LOAD_FAST                '_pgsdlg'
             2018  LOAD_METHOD              setCancelButton
             2020  LOAD_CONST               None
             2022  CALL_METHOD_1         1  '1 positional argument'
             2024  POP_TOP          

 L. 712      2026  LOAD_FAST                '_pgsdlg'
             2028  LOAD_METHOD              setWindowFlags
             2030  LOAD_GLOBAL              QtCore
             2032  LOAD_ATTR                Qt
             2034  LOAD_ATTR                WindowStaysOnTopHint
             2036  CALL_METHOD_1         1  '1 positional argument'
             2038  POP_TOP          

 L. 713      2040  LOAD_FAST                '_pgsdlg'
             2042  LOAD_METHOD              forceShow
             2044  CALL_METHOD_0         0  '0 positional arguments'
             2046  POP_TOP          

 L. 714      2048  LOAD_FAST                '_pgsdlg'
             2050  LOAD_METHOD              setFixedWidth
             2052  LOAD_CONST               400
             2054  CALL_METHOD_1         1  '1 positional argument'
             2056  POP_TOP          

 L. 715      2058  LOAD_GLOBAL              ml_cnn
             2060  LOAD_ATTR                updateCNNClassifier
             2062  LOAD_FAST                '_traindict'

 L. 716      2064  LOAD_FAST                '_nepoch'
             2066  LOAD_FAST                '_batchsize'

 L. 717      2068  LOAD_FAST                '_learning_rate'

 L. 718      2070  LOAD_FAST                '_dropout_prob_fclayer'

 L. 719      2072  LOAD_FAST                'self'
             2074  LOAD_ATTR                modelpath
             2076  LOAD_FAST                'self'
             2078  LOAD_ATTR                modelname

 L. 720      2080  LOAD_CONST               True

 L. 721      2082  LOAD_FAST                '_savepath'
             2084  LOAD_FAST                '_savename'

 L. 722      2086  LOAD_FAST                '_pgsdlg'
             2088  LOAD_CONST               ('nepoch', 'batchsize', 'learningrate', 'dropoutprobfclayer', 'cnnpath', 'cnnname', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             2090  CALL_FUNCTION_KW_11    11  '11 total positional and keyword args'
             2092  STORE_FAST               '_cnnlog'

 L. 724      2094  LOAD_GLOBAL              QtWidgets
             2096  LOAD_ATTR                QMessageBox
             2098  LOAD_METHOD              information
             2100  LOAD_FAST                'self'
             2102  LOAD_ATTR                msgbox

 L. 725      2104  LOAD_STR                 'Update 2D-CNN'

 L. 726      2106  LOAD_STR                 'CNN updated successfully'
             2108  CALL_METHOD_3         3  '3 positional arguments'
             2110  POP_TOP          

 L. 728      2112  LOAD_GLOBAL              QtWidgets
             2114  LOAD_ATTR                QMessageBox
             2116  LOAD_METHOD              question
             2118  LOAD_FAST                'self'
             2120  LOAD_ATTR                msgbox
             2122  LOAD_STR                 'Update 2D-CNN'
             2124  LOAD_STR                 'View learning matrix?'

 L. 729      2126  LOAD_GLOBAL              QtWidgets
             2128  LOAD_ATTR                QMessageBox
             2130  LOAD_ATTR                Yes
             2132  LOAD_GLOBAL              QtWidgets
             2134  LOAD_ATTR                QMessageBox
             2136  LOAD_ATTR                No
             2138  BINARY_OR        

 L. 730      2140  LOAD_GLOBAL              QtWidgets
             2142  LOAD_ATTR                QMessageBox
             2144  LOAD_ATTR                Yes
             2146  CALL_METHOD_5         5  '5 positional arguments'
             2148  STORE_FAST               'reply'

 L. 732      2150  LOAD_FAST                'reply'
             2152  LOAD_GLOBAL              QtWidgets
             2154  LOAD_ATTR                QMessageBox
             2156  LOAD_ATTR                Yes
             2158  COMPARE_OP               ==
         2160_2162  POP_JUMP_IF_FALSE  2230  'to 2230'

 L. 733      2164  LOAD_GLOBAL              QtWidgets
             2166  LOAD_METHOD              QDialog
             2168  CALL_METHOD_0         0  '0 positional arguments'
             2170  STORE_FAST               '_viewmllearnmat'

 L. 734      2172  LOAD_GLOBAL              gui_viewmllearnmat
             2174  CALL_FUNCTION_0       0  '0 positional arguments'
             2176  STORE_FAST               '_gui'

 L. 735      2178  LOAD_FAST                '_cnnlog'
             2180  LOAD_STR                 'learning_curve'
             2182  BINARY_SUBSCR    
             2184  LOAD_FAST                '_gui'
             2186  STORE_ATTR               learnmat

 L. 736      2188  LOAD_FAST                'self'
             2190  LOAD_ATTR                linestyle
             2192  LOAD_FAST                'self'
             2194  STORE_ATTR               linestyle

 L. 737      2196  LOAD_FAST                'self'
             2198  LOAD_ATTR                fontstyle
             2200  LOAD_FAST                '_gui'
             2202  STORE_ATTR               fontstyle

 L. 738      2204  LOAD_FAST                '_gui'
             2206  LOAD_METHOD              setupGUI
             2208  LOAD_FAST                '_viewmllearnmat'
             2210  CALL_METHOD_1         1  '1 positional argument'
             2212  POP_TOP          

 L. 739      2214  LOAD_FAST                '_viewmllearnmat'
             2216  LOAD_METHOD              exec
             2218  CALL_METHOD_0         0  '0 positional arguments'
             2220  POP_TOP          

 L. 740      2222  LOAD_FAST                '_viewmllearnmat'
             2224  LOAD_METHOD              show
             2226  CALL_METHOD_0         0  '0 positional arguments'
             2228  POP_TOP          
           2230_0  COME_FROM          2160  '2160'

Parse error at or near `POP_TOP' instruction at offset 2228

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
    UpdateMl2DCnn = QtWidgets.QWidget()
    gui = updateml2dcnn()
    gui.setupGUI(UpdateMl2DCnn)
    UpdateMl2DCnn.show()
    sys.exit(app.exec_())