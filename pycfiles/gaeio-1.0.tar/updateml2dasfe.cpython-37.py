# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\updateml2dasfe.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 40970 bytes
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
import cognitivegeo.src.gui.viewml2dasfe as gui_viewml2dasfe
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
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

    def clickBtnUpdateMl2DAsfe--- This code section failed: ---

 L. 499         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 501         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 502        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in UpdateMl2DAsfe: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 503        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 504        44  LOAD_STR                 'Update 2D-ASFE'

 L. 505        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 506        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 508        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 509        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in UpdateMl2DAsfe: No pre-ASFE network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 510        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 511       100  LOAD_STR                 'Update 2D-ASFE'

 L. 512       102  LOAD_STR                 'No pre-ASFE network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 513       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 515       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 516       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 517       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in UpdateMl2DAsfe: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    

 L. 518       152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 519       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 520       170  LOAD_STR                 'Update 2D-ASFE'

 L. 521       172  LOAD_STR                 "Feature '"
              174  LOAD_FAST                'f'
              176  BINARY_ADD       
              178  LOAD_STR                 "' not found in seismic data"
              180  BINARY_ADD       
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L. 522       186  LOAD_CONST               None
              188  RETURN_VALUE     
              190  JUMP_BACK           124  'to 124'
              192  POP_BLOCK        
            194_0  COME_FROM_LOOP      112  '112'

 L. 524       194  LOAD_GLOBAL              basic_data
              196  LOAD_METHOD              str2int
              198  LOAD_FAST                'self'
              200  LOAD_ATTR                ldtoldheight
              202  LOAD_METHOD              text
              204  CALL_METHOD_0         0  '0 positional arguments'
              206  CALL_METHOD_1         1  '1 positional argument'
              208  STORE_FAST               '_image_height_old'

 L. 525       210  LOAD_GLOBAL              basic_data
              212  LOAD_METHOD              str2int
              214  LOAD_FAST                'self'
              216  LOAD_ATTR                ldtoldwidth
              218  LOAD_METHOD              text
              220  CALL_METHOD_0         0  '0 positional arguments'
              222  CALL_METHOD_1         1  '1 positional argument'
              224  STORE_FAST               '_image_width_old'

 L. 526       226  LOAD_GLOBAL              basic_data
              228  LOAD_METHOD              str2int
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                ldtnewheight
              234  LOAD_METHOD              text
              236  CALL_METHOD_0         0  '0 positional arguments'
              238  CALL_METHOD_1         1  '1 positional argument'
              240  STORE_FAST               '_image_height_new'

 L. 527       242  LOAD_GLOBAL              basic_data
              244  LOAD_METHOD              str2int
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                ldtnewwidth
              250  LOAD_METHOD              text
              252  CALL_METHOD_0         0  '0 positional arguments'
              254  CALL_METHOD_1         1  '1 positional argument'
              256  STORE_FAST               '_image_width_new'

 L. 528       258  LOAD_FAST                '_image_height_old'
              260  LOAD_CONST               False
              262  COMPARE_OP               is
          264_266  POP_JUMP_IF_TRUE    298  'to 298'
              268  LOAD_FAST                '_image_width_old'
              270  LOAD_CONST               False
              272  COMPARE_OP               is
          274_276  POP_JUMP_IF_TRUE    298  'to 298'

 L. 529       278  LOAD_FAST                '_image_height_new'
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

 L. 530       298  LOAD_GLOBAL              vis_msg
              300  LOAD_ATTR                print
              302  LOAD_STR                 'ERROR in UpdateMl2DAsfe: Non-integer feature size'
              304  LOAD_STR                 'error'
              306  LOAD_CONST               ('type',)
              308  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              310  POP_TOP          

 L. 531       312  LOAD_GLOBAL              QtWidgets
              314  LOAD_ATTR                QMessageBox
              316  LOAD_METHOD              critical
              318  LOAD_FAST                'self'
              320  LOAD_ATTR                msgbox

 L. 532       322  LOAD_STR                 'Update 2D-ASFE'

 L. 533       324  LOAD_STR                 'Non-integer feature size'
              326  CALL_METHOD_3         3  '3 positional arguments'
              328  POP_TOP          

 L. 534       330  LOAD_CONST               None
              332  RETURN_VALUE     
            334_0  COME_FROM           294  '294'

 L. 535       334  LOAD_FAST                '_image_height_old'
              336  LOAD_CONST               2
              338  COMPARE_OP               <
          340_342  POP_JUMP_IF_TRUE    374  'to 374'
              344  LOAD_FAST                '_image_width_old'
              346  LOAD_CONST               2
              348  COMPARE_OP               <
          350_352  POP_JUMP_IF_TRUE    374  'to 374'

 L. 536       354  LOAD_FAST                '_image_height_new'
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

 L. 537       374  LOAD_GLOBAL              vis_msg
              376  LOAD_ATTR                print
              378  LOAD_STR                 'ERROR in UpdateMl2DAsfe: Features are not 2D'
              380  LOAD_STR                 'error'
              382  LOAD_CONST               ('type',)
              384  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              386  POP_TOP          

 L. 538       388  LOAD_GLOBAL              QtWidgets
              390  LOAD_ATTR                QMessageBox
              392  LOAD_METHOD              critical
              394  LOAD_FAST                'self'
              396  LOAD_ATTR                msgbox

 L. 539       398  LOAD_STR                 'Update 2D-ASFE'

 L. 540       400  LOAD_STR                 'Features are not 2D'
              402  CALL_METHOD_3         3  '3 positional arguments'
              404  POP_TOP          

 L. 541       406  LOAD_CONST               None
              408  RETURN_VALUE     
            410_0  COME_FROM           370  '370'

 L. 543       410  LOAD_CONST               2
              412  LOAD_GLOBAL              int
              414  LOAD_FAST                '_image_height_old'
              416  LOAD_CONST               2
              418  BINARY_TRUE_DIVIDE
              420  CALL_FUNCTION_1       1  '1 positional argument'
              422  BINARY_MULTIPLY  
              424  LOAD_CONST               1
              426  BINARY_ADD       
              428  STORE_FAST               '_image_height_old'

 L. 544       430  LOAD_CONST               2
              432  LOAD_GLOBAL              int
              434  LOAD_FAST                '_image_width_old'
              436  LOAD_CONST               2
              438  BINARY_TRUE_DIVIDE
              440  CALL_FUNCTION_1       1  '1 positional argument'
              442  BINARY_MULTIPLY  
              444  LOAD_CONST               1
              446  BINARY_ADD       
              448  STORE_FAST               '_image_width_old'

 L. 546       450  LOAD_FAST                'self'
              452  LOAD_ATTR                modelinfo
              454  LOAD_STR                 'feature_list'
              456  BINARY_SUBSCR    
              458  STORE_FAST               '_features'

 L. 547       460  LOAD_STR                 '_'
              462  LOAD_METHOD              join
              464  LOAD_FAST                '_features'
              466  CALL_METHOD_1         1  '1 positional argument'
              468  LOAD_STR                 '_rotated'
              470  BINARY_ADD       
              472  STORE_FAST               '_target'

 L. 549       474  LOAD_GLOBAL              basic_data
              476  LOAD_METHOD              str2int
              478  LOAD_FAST                'self'
              480  LOAD_ATTR                ldtnepoch
              482  LOAD_METHOD              text
              484  CALL_METHOD_0         0  '0 positional arguments'
              486  CALL_METHOD_1         1  '1 positional argument'
              488  STORE_FAST               '_nepoch'

 L. 550       490  LOAD_GLOBAL              basic_data
              492  LOAD_METHOD              str2int
              494  LOAD_FAST                'self'
              496  LOAD_ATTR                ldtbatchsize
              498  LOAD_METHOD              text
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  CALL_METHOD_1         1  '1 positional argument'
              504  STORE_FAST               '_batchsize'

 L. 551       506  LOAD_GLOBAL              basic_data
              508  LOAD_METHOD              str2float
              510  LOAD_FAST                'self'
              512  LOAD_ATTR                ldtlearnrate
              514  LOAD_METHOD              text
              516  CALL_METHOD_0         0  '0 positional arguments'
              518  CALL_METHOD_1         1  '1 positional argument'
              520  STORE_FAST               '_learning_rate'

 L. 552       522  LOAD_GLOBAL              basic_data
              524  LOAD_METHOD              str2float
              526  LOAD_FAST                'self'
              528  LOAD_ATTR                ldtfcdropout
              530  LOAD_METHOD              text
              532  CALL_METHOD_0         0  '0 positional arguments'
              534  CALL_METHOD_1         1  '1 positional argument'
              536  STORE_FAST               '_dropout_prob_fclayer'

 L. 553       538  LOAD_FAST                '_nepoch'
              540  LOAD_CONST               False
              542  COMPARE_OP               is
          544_546  POP_JUMP_IF_TRUE    558  'to 558'
              548  LOAD_FAST                '_nepoch'
              550  LOAD_CONST               0
              552  COMPARE_OP               <=
          554_556  POP_JUMP_IF_FALSE   594  'to 594'
            558_0  COME_FROM           544  '544'

 L. 554       558  LOAD_GLOBAL              vis_msg
              560  LOAD_ATTR                print
              562  LOAD_STR                 'ERROR in UpdateMl2DAsfe: Non-positive epoch number'
              564  LOAD_STR                 'error'
              566  LOAD_CONST               ('type',)
              568  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              570  POP_TOP          

 L. 555       572  LOAD_GLOBAL              QtWidgets
              574  LOAD_ATTR                QMessageBox
              576  LOAD_METHOD              critical
              578  LOAD_FAST                'self'
              580  LOAD_ATTR                msgbox

 L. 556       582  LOAD_STR                 'Update 2D-ASFE'

 L. 557       584  LOAD_STR                 'Non-positive epoch number'
              586  CALL_METHOD_3         3  '3 positional arguments'
              588  POP_TOP          

 L. 558       590  LOAD_CONST               None
              592  RETURN_VALUE     
            594_0  COME_FROM           554  '554'

 L. 559       594  LOAD_FAST                '_batchsize'
              596  LOAD_CONST               False
              598  COMPARE_OP               is
          600_602  POP_JUMP_IF_TRUE    614  'to 614'
              604  LOAD_FAST                '_batchsize'
              606  LOAD_CONST               0
              608  COMPARE_OP               <=
          610_612  POP_JUMP_IF_FALSE   650  'to 650'
            614_0  COME_FROM           600  '600'

 L. 560       614  LOAD_GLOBAL              vis_msg
              616  LOAD_ATTR                print
              618  LOAD_STR                 'ERROR in UpdateMl2DAsfe: Non-positive batch size'
              620  LOAD_STR                 'error'
              622  LOAD_CONST               ('type',)
              624  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              626  POP_TOP          

 L. 561       628  LOAD_GLOBAL              QtWidgets
              630  LOAD_ATTR                QMessageBox
              632  LOAD_METHOD              critical
              634  LOAD_FAST                'self'
              636  LOAD_ATTR                msgbox

 L. 562       638  LOAD_STR                 'Update 2D-ASFE'

 L. 563       640  LOAD_STR                 'Non-positive batch size'
              642  CALL_METHOD_3         3  '3 positional arguments'
              644  POP_TOP          

 L. 564       646  LOAD_CONST               None
              648  RETURN_VALUE     
            650_0  COME_FROM           610  '610'

 L. 565       650  LOAD_FAST                '_learning_rate'
              652  LOAD_CONST               False
              654  COMPARE_OP               is
          656_658  POP_JUMP_IF_TRUE    670  'to 670'
              660  LOAD_FAST                '_learning_rate'
              662  LOAD_CONST               0
              664  COMPARE_OP               <=
          666_668  POP_JUMP_IF_FALSE   706  'to 706'
            670_0  COME_FROM           656  '656'

 L. 566       670  LOAD_GLOBAL              vis_msg
              672  LOAD_ATTR                print
              674  LOAD_STR                 'ERROR in UpdateMl2DAsfe: Non-positive learning rate'
              676  LOAD_STR                 'error'
              678  LOAD_CONST               ('type',)
              680  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              682  POP_TOP          

 L. 567       684  LOAD_GLOBAL              QtWidgets
              686  LOAD_ATTR                QMessageBox
              688  LOAD_METHOD              critical
              690  LOAD_FAST                'self'
              692  LOAD_ATTR                msgbox

 L. 568       694  LOAD_STR                 'Update 2D-ASFE'

 L. 569       696  LOAD_STR                 'Non-positive learning rate'
              698  CALL_METHOD_3         3  '3 positional arguments'
              700  POP_TOP          

 L. 570       702  LOAD_CONST               None
              704  RETURN_VALUE     
            706_0  COME_FROM           666  '666'

 L. 571       706  LOAD_FAST                '_dropout_prob_fclayer'
              708  LOAD_CONST               False
              710  COMPARE_OP               is
          712_714  POP_JUMP_IF_TRUE    726  'to 726'
              716  LOAD_FAST                '_dropout_prob_fclayer'
              718  LOAD_CONST               0
              720  COMPARE_OP               <=
          722_724  POP_JUMP_IF_FALSE   762  'to 762'
            726_0  COME_FROM           712  '712'

 L. 572       726  LOAD_GLOBAL              vis_msg
              728  LOAD_ATTR                print
              730  LOAD_STR                 'ERROR in UpdateMl2DAsfe: Negative dropout rate'
              732  LOAD_STR                 'error'
              734  LOAD_CONST               ('type',)
              736  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              738  POP_TOP          

 L. 573       740  LOAD_GLOBAL              QtWidgets
              742  LOAD_ATTR                QMessageBox
              744  LOAD_METHOD              critical
              746  LOAD_FAST                'self'
              748  LOAD_ATTR                msgbox

 L. 574       750  LOAD_STR                 'Update 2D-ASFE'

 L. 575       752  LOAD_STR                 'Negative dropout rate'
              754  CALL_METHOD_3         3  '3 positional arguments'
              756  POP_TOP          

 L. 576       758  LOAD_CONST               None
              760  RETURN_VALUE     
            762_0  COME_FROM           722  '722'

 L. 578       762  LOAD_GLOBAL              len
              764  LOAD_FAST                'self'
              766  LOAD_ATTR                ldtsave
              768  LOAD_METHOD              text
              770  CALL_METHOD_0         0  '0 positional arguments'
              772  CALL_FUNCTION_1       1  '1 positional argument'
              774  LOAD_CONST               1
              776  COMPARE_OP               <
          778_780  POP_JUMP_IF_FALSE   818  'to 818'

 L. 579       782  LOAD_GLOBAL              vis_msg
              784  LOAD_ATTR                print
              786  LOAD_STR                 'ERROR in UpdateMl2DAsfe: No name specified for new-ASFE'
              788  LOAD_STR                 'error'
              790  LOAD_CONST               ('type',)
              792  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              794  POP_TOP          

 L. 580       796  LOAD_GLOBAL              QtWidgets
              798  LOAD_ATTR                QMessageBox
              800  LOAD_METHOD              critical
              802  LOAD_FAST                'self'
              804  LOAD_ATTR                msgbox

 L. 581       806  LOAD_STR                 'Update 2D-ASFE'

 L. 582       808  LOAD_STR                 'No name specified for new-ASFE'
              810  CALL_METHOD_3         3  '3 positional arguments'
              812  POP_TOP          

 L. 583       814  LOAD_CONST               None
              816  RETURN_VALUE     
            818_0  COME_FROM           778  '778'

 L. 584       818  LOAD_GLOBAL              os
              820  LOAD_ATTR                path
              822  LOAD_METHOD              dirname
              824  LOAD_FAST                'self'
              826  LOAD_ATTR                ldtsave
              828  LOAD_METHOD              text
              830  CALL_METHOD_0         0  '0 positional arguments'
              832  CALL_METHOD_1         1  '1 positional argument'
              834  STORE_FAST               '_savepath'

 L. 585       836  LOAD_GLOBAL              os
              838  LOAD_ATTR                path
              840  LOAD_METHOD              splitext
              842  LOAD_GLOBAL              os
              844  LOAD_ATTR                path
              846  LOAD_METHOD              basename
              848  LOAD_FAST                'self'
              850  LOAD_ATTR                ldtsave
              852  LOAD_METHOD              text
              854  CALL_METHOD_0         0  '0 positional arguments'
              856  CALL_METHOD_1         1  '1 positional argument'
              858  CALL_METHOD_1         1  '1 positional argument'
              860  LOAD_CONST               0
              862  BINARY_SUBSCR    
              864  STORE_FAST               '_savename'

 L. 587       866  LOAD_CONST               0
              868  STORE_FAST               '_wdinl'

 L. 588       870  LOAD_CONST               0
              872  STORE_FAST               '_wdxl'

 L. 589       874  LOAD_CONST               0
              876  STORE_FAST               '_wdz'

 L. 590       878  LOAD_FAST                'self'
              880  LOAD_ATTR                cbbornt
              882  LOAD_METHOD              currentIndex
              884  CALL_METHOD_0         0  '0 positional arguments'
              886  LOAD_CONST               0
              888  COMPARE_OP               ==
          890_892  POP_JUMP_IF_FALSE   918  'to 918'

 L. 591       894  LOAD_GLOBAL              int
              896  LOAD_FAST                '_image_width_old'
              898  LOAD_CONST               2
              900  BINARY_TRUE_DIVIDE
              902  CALL_FUNCTION_1       1  '1 positional argument'
              904  STORE_FAST               '_wdxl'

 L. 592       906  LOAD_GLOBAL              int
              908  LOAD_FAST                '_image_height_old'
              910  LOAD_CONST               2
              912  BINARY_TRUE_DIVIDE
              914  CALL_FUNCTION_1       1  '1 positional argument'
              916  STORE_FAST               '_wdz'
            918_0  COME_FROM           890  '890'

 L. 593       918  LOAD_FAST                'self'
              920  LOAD_ATTR                cbbornt
              922  LOAD_METHOD              currentIndex
              924  CALL_METHOD_0         0  '0 positional arguments'
              926  LOAD_CONST               1
              928  COMPARE_OP               ==
          930_932  POP_JUMP_IF_FALSE   958  'to 958'

 L. 594       934  LOAD_GLOBAL              int
              936  LOAD_FAST                '_image_width_old'
              938  LOAD_CONST               2
              940  BINARY_TRUE_DIVIDE
              942  CALL_FUNCTION_1       1  '1 positional argument'
              944  STORE_FAST               '_wdinl'

 L. 595       946  LOAD_GLOBAL              int
              948  LOAD_FAST                '_image_height_old'
              950  LOAD_CONST               2
              952  BINARY_TRUE_DIVIDE
              954  CALL_FUNCTION_1       1  '1 positional argument'
              956  STORE_FAST               '_wdz'
            958_0  COME_FROM           930  '930'

 L. 596       958  LOAD_FAST                'self'
              960  LOAD_ATTR                cbbornt
              962  LOAD_METHOD              currentIndex
              964  CALL_METHOD_0         0  '0 positional arguments'
              966  LOAD_CONST               2
              968  COMPARE_OP               ==
          970_972  POP_JUMP_IF_FALSE   998  'to 998'

 L. 597       974  LOAD_GLOBAL              int
              976  LOAD_FAST                '_image_width_old'
              978  LOAD_CONST               2
              980  BINARY_TRUE_DIVIDE
              982  CALL_FUNCTION_1       1  '1 positional argument'
              984  STORE_FAST               '_wdinl'

 L. 598       986  LOAD_GLOBAL              int
              988  LOAD_FAST                '_image_height_old'
              990  LOAD_CONST               2
              992  BINARY_TRUE_DIVIDE
              994  CALL_FUNCTION_1       1  '1 positional argument'
              996  STORE_FAST               '_wdxl'
            998_0  COME_FROM           970  '970'

 L. 600       998  LOAD_FAST                'self'
             1000  LOAD_ATTR                survinfo
             1002  STORE_FAST               '_seisinfo'

 L. 602      1004  LOAD_GLOBAL              print
             1006  LOAD_STR                 'UpdateMl2DAsfe: Step 1 - Get training samples:'
             1008  CALL_FUNCTION_1       1  '1 positional argument'
             1010  POP_TOP          

 L. 603      1012  LOAD_FAST                'self'
             1014  LOAD_ATTR                traindataconfig
             1016  LOAD_STR                 'TrainPointSet'
             1018  BINARY_SUBSCR    
             1020  STORE_FAST               '_trainpoint'

 L. 604      1022  LOAD_GLOBAL              np
             1024  LOAD_METHOD              zeros
             1026  LOAD_CONST               0
             1028  LOAD_CONST               3
             1030  BUILD_LIST_2          2 
             1032  CALL_METHOD_1         1  '1 positional argument'
             1034  STORE_FAST               '_traindata'

 L. 605      1036  SETUP_LOOP         1112  'to 1112'
             1038  LOAD_FAST                '_trainpoint'
             1040  GET_ITER         
           1042_0  COME_FROM          1060  '1060'
             1042  FOR_ITER           1110  'to 1110'
             1044  STORE_FAST               '_p'

 L. 606      1046  LOAD_GLOBAL              point_ays
             1048  LOAD_METHOD              checkPoint
             1050  LOAD_FAST                'self'
             1052  LOAD_ATTR                pointsetdata
             1054  LOAD_FAST                '_p'
             1056  BINARY_SUBSCR    
             1058  CALL_METHOD_1         1  '1 positional argument'
         1060_1062  POP_JUMP_IF_FALSE  1042  'to 1042'

 L. 607      1064  LOAD_GLOBAL              basic_mdt
             1066  LOAD_METHOD              exportMatDict
             1068  LOAD_FAST                'self'
             1070  LOAD_ATTR                pointsetdata
             1072  LOAD_FAST                '_p'
             1074  BINARY_SUBSCR    
             1076  LOAD_STR                 'Inline'
             1078  LOAD_STR                 'Crossline'
             1080  LOAD_STR                 'Z'
             1082  BUILD_LIST_3          3 
             1084  CALL_METHOD_2         2  '2 positional arguments'
             1086  STORE_FAST               '_pt'

 L. 608      1088  LOAD_GLOBAL              np
             1090  LOAD_ATTR                concatenate
             1092  LOAD_FAST                '_traindata'
             1094  LOAD_FAST                '_pt'
             1096  BUILD_TUPLE_2         2 
             1098  LOAD_CONST               0
             1100  LOAD_CONST               ('axis',)
             1102  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1104  STORE_FAST               '_traindata'
         1106_1108  JUMP_BACK          1042  'to 1042'
             1110  POP_BLOCK        
           1112_0  COME_FROM_LOOP     1036  '1036'

 L. 609      1112  LOAD_GLOBAL              seis_ays
             1114  LOAD_ATTR                removeOutofSurveySample
             1116  LOAD_FAST                '_traindata'

 L. 610      1118  LOAD_FAST                '_seisinfo'
             1120  LOAD_STR                 'ILStart'
             1122  BINARY_SUBSCR    
             1124  LOAD_FAST                '_wdinl'
             1126  LOAD_FAST                '_seisinfo'
             1128  LOAD_STR                 'ILStep'
             1130  BINARY_SUBSCR    
             1132  BINARY_MULTIPLY  
             1134  BINARY_ADD       

 L. 611      1136  LOAD_FAST                '_seisinfo'
             1138  LOAD_STR                 'ILEnd'
             1140  BINARY_SUBSCR    
             1142  LOAD_FAST                '_wdinl'
             1144  LOAD_FAST                '_seisinfo'
             1146  LOAD_STR                 'ILStep'
             1148  BINARY_SUBSCR    
             1150  BINARY_MULTIPLY  
             1152  BINARY_SUBTRACT  

 L. 612      1154  LOAD_FAST                '_seisinfo'
             1156  LOAD_STR                 'XLStart'
             1158  BINARY_SUBSCR    
             1160  LOAD_FAST                '_wdxl'
             1162  LOAD_FAST                '_seisinfo'
             1164  LOAD_STR                 'XLStep'
             1166  BINARY_SUBSCR    
             1168  BINARY_MULTIPLY  
             1170  BINARY_ADD       

 L. 613      1172  LOAD_FAST                '_seisinfo'
             1174  LOAD_STR                 'XLEnd'
             1176  BINARY_SUBSCR    
             1178  LOAD_FAST                '_wdxl'
             1180  LOAD_FAST                '_seisinfo'
             1182  LOAD_STR                 'XLStep'
             1184  BINARY_SUBSCR    
             1186  BINARY_MULTIPLY  
             1188  BINARY_SUBTRACT  

 L. 614      1190  LOAD_FAST                '_seisinfo'
             1192  LOAD_STR                 'ZStart'
             1194  BINARY_SUBSCR    
             1196  LOAD_FAST                '_wdz'
             1198  LOAD_FAST                '_seisinfo'
             1200  LOAD_STR                 'ZStep'
             1202  BINARY_SUBSCR    
             1204  BINARY_MULTIPLY  
             1206  BINARY_ADD       

 L. 615      1208  LOAD_FAST                '_seisinfo'
             1210  LOAD_STR                 'ZEnd'
             1212  BINARY_SUBSCR    
             1214  LOAD_FAST                '_wdz'
             1216  LOAD_FAST                '_seisinfo'
             1218  LOAD_STR                 'ZStep'
             1220  BINARY_SUBSCR    
             1222  BINARY_MULTIPLY  
             1224  BINARY_SUBTRACT  
             1226  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1228  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1230  STORE_FAST               '_traindata'

 L. 618      1232  LOAD_GLOBAL              np
             1234  LOAD_METHOD              shape
             1236  LOAD_FAST                '_traindata'
             1238  CALL_METHOD_1         1  '1 positional argument'
             1240  LOAD_CONST               0
             1242  BINARY_SUBSCR    
             1244  LOAD_CONST               0
             1246  COMPARE_OP               <=
         1248_1250  POP_JUMP_IF_FALSE  1288  'to 1288'

 L. 619      1252  LOAD_GLOBAL              vis_msg
             1254  LOAD_ATTR                print
             1256  LOAD_STR                 'ERROR in UpdateMl2DAsfe: No training sample found'
             1258  LOAD_STR                 'error'
             1260  LOAD_CONST               ('type',)
             1262  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1264  POP_TOP          

 L. 620      1266  LOAD_GLOBAL              QtWidgets
             1268  LOAD_ATTR                QMessageBox
             1270  LOAD_METHOD              critical
             1272  LOAD_FAST                'self'
             1274  LOAD_ATTR                msgbox

 L. 621      1276  LOAD_STR                 'Update 2D-ASFE'

 L. 622      1278  LOAD_STR                 'No training sample found'
             1280  CALL_METHOD_3         3  '3 positional arguments'
             1282  POP_TOP          

 L. 623      1284  LOAD_CONST               None
             1286  RETURN_VALUE     
           1288_0  COME_FROM          1248  '1248'

 L. 626      1288  LOAD_GLOBAL              print
             1290  LOAD_STR                 'UpdateMl2DAsfe: Step 2 - Retrieve and interpolate images: (%d, %d) --> (%d, %d)'

 L. 627      1292  LOAD_FAST                '_image_height_old'
             1294  LOAD_FAST                '_image_width_old'
             1296  LOAD_FAST                '_image_height_new'
             1298  LOAD_FAST                '_image_width_new'
             1300  BUILD_TUPLE_4         4 
             1302  BINARY_MODULO    
             1304  CALL_FUNCTION_1       1  '1 positional argument'
             1306  POP_TOP          

 L. 628      1308  BUILD_MAP_0           0 
             1310  STORE_FAST               '_traindict'

 L. 629      1312  SETUP_LOOP         1384  'to 1384'
             1314  LOAD_FAST                '_features'
             1316  GET_ITER         
             1318  FOR_ITER           1382  'to 1382'
             1320  STORE_FAST               'f'

 L. 630      1322  LOAD_FAST                'self'
             1324  LOAD_ATTR                seisdata
             1326  LOAD_FAST                'f'
             1328  BINARY_SUBSCR    
             1330  STORE_FAST               '_seisdata'

 L. 631      1332  LOAD_GLOBAL              seis_ays
             1334  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1336  LOAD_FAST                '_seisdata'
             1338  LOAD_FAST                '_traindata'
             1340  LOAD_FAST                'self'
             1342  LOAD_ATTR                survinfo

 L. 632      1344  LOAD_FAST                '_wdinl'
             1346  LOAD_FAST                '_wdxl'
             1348  LOAD_FAST                '_wdz'

 L. 633      1350  LOAD_CONST               False
             1352  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1354  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1356  LOAD_CONST               None
             1358  LOAD_CONST               None
             1360  BUILD_SLICE_2         2 
             1362  LOAD_CONST               3
             1364  LOAD_CONST               None
             1366  BUILD_SLICE_2         2 
             1368  BUILD_TUPLE_2         2 
             1370  BINARY_SUBSCR    
             1372  LOAD_FAST                '_traindict'
             1374  LOAD_FAST                'f'
             1376  STORE_SUBSCR     
         1378_1380  JUMP_BACK          1318  'to 1318'
             1382  POP_BLOCK        
           1384_0  COME_FROM_LOOP     1312  '1312'

 L. 635      1384  LOAD_FAST                'self'
             1386  LOAD_ATTR                traindataconfig
             1388  LOAD_STR                 'RemoveInvariantFeature_Checked'
             1390  BINARY_SUBSCR    
         1392_1394  POP_JUMP_IF_FALSE  1476  'to 1476'

 L. 636      1396  SETUP_LOOP         1476  'to 1476'
             1398  LOAD_FAST                '_features'
             1400  GET_ITER         
           1402_0  COME_FROM          1430  '1430'
             1402  FOR_ITER           1474  'to 1474'
             1404  STORE_FAST               'f'

 L. 637      1406  LOAD_GLOBAL              ml_aug
             1408  LOAD_METHOD              removeInvariantFeature
             1410  LOAD_FAST                '_traindict'
             1412  LOAD_FAST                'f'
             1414  CALL_METHOD_2         2  '2 positional arguments'
             1416  STORE_FAST               '_traindict'

 L. 638      1418  LOAD_GLOBAL              basic_mdt
             1420  LOAD_METHOD              maxDictConstantRow
             1422  LOAD_FAST                '_traindict'
             1424  CALL_METHOD_1         1  '1 positional argument'
             1426  LOAD_CONST               0
             1428  COMPARE_OP               <=
         1430_1432  POP_JUMP_IF_FALSE  1402  'to 1402'

 L. 639      1434  LOAD_GLOBAL              vis_msg
             1436  LOAD_ATTR                print
             1438  LOAD_STR                 'ERROR in UpdateMl2DAsfe: No training sample found'
             1440  LOAD_STR                 'error'
             1442  LOAD_CONST               ('type',)
             1444  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1446  POP_TOP          

 L. 640      1448  LOAD_GLOBAL              QtWidgets
             1450  LOAD_ATTR                QMessageBox
             1452  LOAD_METHOD              critical
             1454  LOAD_FAST                'self'
             1456  LOAD_ATTR                msgbox

 L. 641      1458  LOAD_STR                 'Update 2D-ASFE'

 L. 642      1460  LOAD_STR                 'No training sample found'
             1462  CALL_METHOD_3         3  '3 positional arguments'
             1464  POP_TOP          

 L. 643      1466  LOAD_CONST               None
             1468  RETURN_VALUE     
         1470_1472  JUMP_BACK          1402  'to 1402'
             1474  POP_BLOCK        
           1476_0  COME_FROM_LOOP     1396  '1396'
           1476_1  COME_FROM          1392  '1392'

 L. 645      1476  LOAD_FAST                '_image_height_new'
             1478  LOAD_FAST                '_image_height_old'
             1480  COMPARE_OP               !=
         1482_1484  POP_JUMP_IF_TRUE   1496  'to 1496'
             1486  LOAD_FAST                '_image_width_new'
             1488  LOAD_FAST                '_image_width_old'
             1490  COMPARE_OP               !=
         1492_1494  POP_JUMP_IF_FALSE  1540  'to 1540'
           1496_0  COME_FROM          1482  '1482'

 L. 646      1496  SETUP_LOOP         1540  'to 1540'
             1498  LOAD_FAST                '_features'
             1500  GET_ITER         
             1502  FOR_ITER           1538  'to 1538'
             1504  STORE_FAST               'f'

 L. 647      1506  LOAD_GLOBAL              basic_image
             1508  LOAD_ATTR                changeImageSize
             1510  LOAD_FAST                '_traindict'
             1512  LOAD_FAST                'f'
             1514  BINARY_SUBSCR    

 L. 648      1516  LOAD_FAST                '_image_height_old'

 L. 649      1518  LOAD_FAST                '_image_width_old'

 L. 650      1520  LOAD_FAST                '_image_height_new'

 L. 651      1522  LOAD_FAST                '_image_width_new'
             1524  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1526  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1528  LOAD_FAST                '_traindict'
             1530  LOAD_FAST                'f'
             1532  STORE_SUBSCR     
         1534_1536  JUMP_BACK          1502  'to 1502'
             1538  POP_BLOCK        
           1540_0  COME_FROM_LOOP     1496  '1496'
           1540_1  COME_FROM          1492  '1492'

 L. 653      1540  SETUP_LOOP         1586  'to 1586'
             1542  LOAD_FAST                '_features'
             1544  GET_ITER         
             1546  FOR_ITER           1584  'to 1584'
             1548  STORE_FAST               'f'

 L. 655      1550  LOAD_FAST                'self'
             1552  LOAD_METHOD              makeTarget
             1554  LOAD_FAST                '_traindict'
             1556  LOAD_FAST                'f'
             1558  BINARY_SUBSCR    
             1560  LOAD_FAST                '_image_height_new'
             1562  LOAD_FAST                '_image_width_new'
             1564  CALL_METHOD_3         3  '3 positional arguments'
             1566  UNPACK_SEQUENCE_2     2 
             1568  LOAD_FAST                '_traindict'
             1570  LOAD_FAST                'f'
             1572  STORE_SUBSCR     
             1574  LOAD_FAST                '_traindict'
             1576  LOAD_FAST                '_target'
             1578  STORE_SUBSCR     
         1580_1582  JUMP_BACK          1546  'to 1546'
             1584  POP_BLOCK        
           1586_0  COME_FROM_LOOP     1540  '1540'

 L. 657      1586  LOAD_GLOBAL              print
             1588  LOAD_STR                 'UpdateMl2DAsfe: A total of %d valid training samples'
             1590  LOAD_GLOBAL              basic_mdt
             1592  LOAD_METHOD              maxDictConstantRow
             1594  LOAD_FAST                '_traindict'
             1596  CALL_METHOD_1         1  '1 positional argument'
             1598  BINARY_MODULO    
             1600  CALL_FUNCTION_1       1  '1 positional argument'
             1602  POP_TOP          

 L. 659      1604  LOAD_GLOBAL              print
             1606  LOAD_STR                 'UpdateMl2DAsfe: Step 3 - Start training'
             1608  CALL_FUNCTION_1       1  '1 positional argument'
             1610  POP_TOP          

 L. 661      1612  LOAD_GLOBAL              QtWidgets
             1614  LOAD_METHOD              QProgressDialog
             1616  CALL_METHOD_0         0  '0 positional arguments'
             1618  STORE_FAST               '_pgsdlg'

 L. 662      1620  LOAD_GLOBAL              QtGui
             1622  LOAD_METHOD              QIcon
             1624  CALL_METHOD_0         0  '0 positional arguments'
             1626  STORE_FAST               'icon'

 L. 663      1628  LOAD_FAST                'icon'
             1630  LOAD_METHOD              addPixmap
             1632  LOAD_GLOBAL              QtGui
             1634  LOAD_METHOD              QPixmap
             1636  LOAD_GLOBAL              os
             1638  LOAD_ATTR                path
             1640  LOAD_METHOD              join
             1642  LOAD_FAST                'self'
             1644  LOAD_ATTR                iconpath
             1646  LOAD_STR                 'icons/update.png'
             1648  CALL_METHOD_2         2  '2 positional arguments'
             1650  CALL_METHOD_1         1  '1 positional argument'

 L. 664      1652  LOAD_GLOBAL              QtGui
             1654  LOAD_ATTR                QIcon
             1656  LOAD_ATTR                Normal
             1658  LOAD_GLOBAL              QtGui
             1660  LOAD_ATTR                QIcon
             1662  LOAD_ATTR                Off
             1664  CALL_METHOD_3         3  '3 positional arguments'
             1666  POP_TOP          

 L. 665      1668  LOAD_FAST                '_pgsdlg'
             1670  LOAD_METHOD              setWindowIcon
             1672  LOAD_FAST                'icon'
             1674  CALL_METHOD_1         1  '1 positional argument'
             1676  POP_TOP          

 L. 666      1678  LOAD_FAST                '_pgsdlg'
             1680  LOAD_METHOD              setWindowTitle
             1682  LOAD_STR                 'Update 2D-ASFE'
             1684  CALL_METHOD_1         1  '1 positional argument'
             1686  POP_TOP          

 L. 667      1688  LOAD_FAST                '_pgsdlg'
             1690  LOAD_METHOD              setCancelButton
             1692  LOAD_CONST               None
             1694  CALL_METHOD_1         1  '1 positional argument'
             1696  POP_TOP          

 L. 668      1698  LOAD_FAST                '_pgsdlg'
             1700  LOAD_METHOD              setWindowFlags
             1702  LOAD_GLOBAL              QtCore
             1704  LOAD_ATTR                Qt
             1706  LOAD_ATTR                WindowStaysOnTopHint
             1708  CALL_METHOD_1         1  '1 positional argument'
             1710  POP_TOP          

 L. 669      1712  LOAD_FAST                '_pgsdlg'
             1714  LOAD_METHOD              forceShow
             1716  CALL_METHOD_0         0  '0 positional arguments'
             1718  POP_TOP          

 L. 670      1720  LOAD_FAST                '_pgsdlg'
             1722  LOAD_METHOD              setFixedWidth
             1724  LOAD_CONST               400
             1726  CALL_METHOD_1         1  '1 positional argument'
             1728  POP_TOP          

 L. 671      1730  LOAD_GLOBAL              ml_cnn
             1732  LOAD_ATTR                updateCNNClassifier
             1734  LOAD_FAST                '_traindict'

 L. 672      1736  LOAD_FAST                '_nepoch'
             1738  LOAD_FAST                '_batchsize'

 L. 673      1740  LOAD_FAST                '_learning_rate'

 L. 674      1742  LOAD_FAST                '_dropout_prob_fclayer'

 L. 675      1744  LOAD_FAST                'self'
             1746  LOAD_ATTR                modelpath
             1748  LOAD_FAST                'self'
             1750  LOAD_ATTR                modelname

 L. 676      1752  LOAD_CONST               True

 L. 677      1754  LOAD_FAST                '_savepath'
             1756  LOAD_FAST                '_savename'

 L. 678      1758  LOAD_FAST                '_pgsdlg'
             1760  LOAD_CONST               ('nepoch', 'batchsize', 'learningrate', 'dropoutprobfclayer', 'cnnpath', 'cnnname', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             1762  CALL_FUNCTION_KW_11    11  '11 total positional and keyword args'
             1764  STORE_FAST               '_cnnlog'

 L. 680      1766  LOAD_GLOBAL              QtWidgets
             1768  LOAD_ATTR                QMessageBox
             1770  LOAD_METHOD              information
             1772  LOAD_FAST                'self'
             1774  LOAD_ATTR                msgbox

 L. 681      1776  LOAD_STR                 'Update 2D-ASFE'

 L. 682      1778  LOAD_STR                 'ASFE updated successfully'
             1780  CALL_METHOD_3         3  '3 positional arguments'
             1782  POP_TOP          

 L. 684      1784  LOAD_GLOBAL              QtWidgets
             1786  LOAD_ATTR                QMessageBox
             1788  LOAD_METHOD              question
             1790  LOAD_FAST                'self'
             1792  LOAD_ATTR                msgbox
             1794  LOAD_STR                 'Update 2D-ASFE'
             1796  LOAD_STR                 'View learning matrix?'

 L. 685      1798  LOAD_GLOBAL              QtWidgets
             1800  LOAD_ATTR                QMessageBox
             1802  LOAD_ATTR                Yes
             1804  LOAD_GLOBAL              QtWidgets
             1806  LOAD_ATTR                QMessageBox
             1808  LOAD_ATTR                No
             1810  BINARY_OR        

 L. 686      1812  LOAD_GLOBAL              QtWidgets
             1814  LOAD_ATTR                QMessageBox
             1816  LOAD_ATTR                Yes
             1818  CALL_METHOD_5         5  '5 positional arguments'
             1820  STORE_FAST               'reply'

 L. 688      1822  LOAD_FAST                'reply'
             1824  LOAD_GLOBAL              QtWidgets
             1826  LOAD_ATTR                QMessageBox
             1828  LOAD_ATTR                Yes
             1830  COMPARE_OP               ==
         1832_1834  POP_JUMP_IF_FALSE  1902  'to 1902'

 L. 689      1836  LOAD_GLOBAL              QtWidgets
             1838  LOAD_METHOD              QDialog
             1840  CALL_METHOD_0         0  '0 positional arguments'
             1842  STORE_FAST               '_viewmllearnmat'

 L. 690      1844  LOAD_GLOBAL              gui_viewmllearnmat
             1846  CALL_FUNCTION_0       0  '0 positional arguments'
             1848  STORE_FAST               '_gui'

 L. 691      1850  LOAD_FAST                '_cnnlog'
             1852  LOAD_STR                 'learning_curve'
             1854  BINARY_SUBSCR    
             1856  LOAD_FAST                '_gui'
             1858  STORE_ATTR               learnmat

 L. 692      1860  LOAD_FAST                'self'
             1862  LOAD_ATTR                linestyle
             1864  LOAD_FAST                'self'
             1866  STORE_ATTR               linestyle

 L. 693      1868  LOAD_FAST                'self'
             1870  LOAD_ATTR                fontstyle
             1872  LOAD_FAST                '_gui'
             1874  STORE_ATTR               fontstyle

 L. 694      1876  LOAD_FAST                '_gui'
             1878  LOAD_METHOD              setupGUI
             1880  LOAD_FAST                '_viewmllearnmat'
             1882  CALL_METHOD_1         1  '1 positional argument'
             1884  POP_TOP          

 L. 695      1886  LOAD_FAST                '_viewmllearnmat'
             1888  LOAD_METHOD              exec
             1890  CALL_METHOD_0         0  '0 positional arguments'
             1892  POP_TOP          

 L. 696      1894  LOAD_FAST                '_viewmllearnmat'
             1896  LOAD_METHOD              show
             1898  CALL_METHOD_0         0  '0 positional arguments'
             1900  POP_TOP          
           1902_0  COME_FROM          1832  '1832'

Parse error at or near `POP_TOP' instruction at offset 1900

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
    UpdateMl2DAsfe = QtWidgets.QWidget()
    gui = updateml2dasfe()
    gui.setupGUI(UpdateMl2DAsfe)
    UpdateMl2DAsfe.show()
    sys.exit(app.exec_())