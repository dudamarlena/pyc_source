# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\updatemlmlp.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 35901 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.basic.data import data as basic_data
from cognitivegeo.src.basic.matdict import matdict as basic_mdt
from cognitivegeo.src.seismic.analysis import analysis as seis_ays
from cognitivegeo.src.pointset.analysis import analysis as point_ays
from cognitivegeo.src.ml.augmentation import augmentation as ml_aug
from cognitivegeo.src.ml.tfmodel import tfmodel as ml_tfm
from cognitivegeo.src.ml.fnnclassifier import fnnclassifier as ml_fnn
from cognitivegeo.src.gui.viewmlmlp import viewmlmlp as gui_viewmlmlp
from cognitivegeo.src.gui.viewmllearnmat import viewmllearnmat as gui_viewmllearnmat
from cognitivegeo.src.gui.configmltraindata import configmltraindata as gui_configmltraindata
from cognitivegeo.src.vis.messager import messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class updatemlmlp(object):
    survinfo = {}
    seisdata = {}
    pointsetdata = {}
    rootpath = ''
    linestyle = core_set.Visual['Line']
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
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False

    def setupGUI(self, UpdateMlMlp):
        UpdateMlMlp.setObjectName('UpdateMlMlp')
        UpdateMlMlp.setFixedSize(810, 470)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        UpdateMlMlp.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(UpdateMlMlp)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(UpdateMlMlp)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(UpdateMlMlp)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(UpdateMlMlp)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 160))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblpatchsize = QtWidgets.QLabel(UpdateMlMlp)
        self.lblpatchsize.setObjectName('lblpatchsize')
        self.lblpatchsize.setGeometry(QtCore.QRect(10, 230, 80, 30))
        self.lblpatchheight = QtWidgets.QLabel(UpdateMlMlp)
        self.lblpatchheight.setObjectName('lblpatchheight')
        self.lblpatchheight.setGeometry(QtCore.QRect(110, 230, 50, 30))
        self.ldtpatchheight = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtpatchheight.setObjectName('ldtpatchheight')
        self.ldtpatchheight.setGeometry(QtCore.QRect(160, 230, 40, 30))
        self.lblpatchwidth = QtWidgets.QLabel(UpdateMlMlp)
        self.lblpatchwidth.setObjectName('lblpatchwidth')
        self.lblpatchwidth.setGeometry(QtCore.QRect(205, 230, 50, 30))
        self.ldtpatchwidth = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtpatchwidth.setObjectName('ldtpatchwidth')
        self.ldtpatchwidth.setGeometry(QtCore.QRect(255, 230, 40, 30))
        self.lblpatchdepth = QtWidgets.QLabel(UpdateMlMlp)
        self.lblpatchdepth.setObjectName('lblpatchdepth')
        self.lblpatchdepth.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtpatchdepth = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtpatchdepth.setObjectName('ldtpatchdepth')
        self.ldtpatchdepth.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblold = QtWidgets.QLabel(UpdateMlMlp)
        self.lblold.setObjectName('lblold')
        self.lblold.setGeometry(QtCore.QRect(50, 270, 60, 30))
        self.lbloldlength = QtWidgets.QLabel(UpdateMlMlp)
        self.lbloldlength.setObjectName('lbloldlength')
        self.lbloldlength.setGeometry(QtCore.QRect(110, 270, 50, 30))
        self.ldtoldlength = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtoldlength.setObjectName('ldtoldlength')
        self.ldtoldlength.setGeometry(QtCore.QRect(160, 270, 40, 30))
        self.lbloldtotal = QtWidgets.QLabel(UpdateMlMlp)
        self.lbloldtotal.setObjectName('lbloldtotal')
        self.lbloldtotal.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtoldtotal = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtoldtotal.setObjectName('ldtoldtotal')
        self.ldtoldtotal.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lblnew = QtWidgets.QLabel(UpdateMlMlp)
        self.lblnew.setObjectName('lblnew')
        self.lblnew.setGeometry(QtCore.QRect(50, 310, 60, 30))
        self.lblnewlength = QtWidgets.QLabel(UpdateMlMlp)
        self.lblnewlength.setObjectName('lblnewlength')
        self.lblnewlength.setGeometry(QtCore.QRect(110, 310, 50, 30))
        self.ldtnewlength = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtnewlength.setObjectName('ldtnewlength')
        self.ldtnewlength.setGeometry(QtCore.QRect(160, 310, 40, 30))
        self.lblnewtotal = QtWidgets.QLabel(UpdateMlMlp)
        self.lblnewtotal.setObjectName('lblnewtotal')
        self.lblnewtotal.setGeometry(QtCore.QRect(300, 310, 50, 30))
        self.ldtnewtotal = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtnewtotal.setObjectName('ldtnewtotal')
        self.ldtnewtotal.setGeometry(QtCore.QRect(350, 310, 40, 30))
        self.lbltarget = QtWidgets.QLabel(UpdateMlMlp)
        self.lbltarget.setObjectName('lbltargete')
        self.lbltarget.setGeometry(QtCore.QRect(10, 360, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(UpdateMlMlp)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 360, 110, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(UpdateMlMlp)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 360, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblnetwork = QtWidgets.QLabel(UpdateMlMlp)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(UpdateMlMlp)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnlayer = QtWidgets.QLabel(UpdateMlMlp)
        self.lblnlayer.setObjectName('lblnlayer')
        self.lblnlayer.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnlayer = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtnlayer.setObjectName('ldtnlayer')
        self.ldtnlayer.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnlayer = QtWidgets.QTableWidget(UpdateMlMlp)
        self.twgnlayer.setObjectName('twgnlayer')
        self.twgnlayer.setGeometry(QtCore.QRect(610, 100, 180, 240))
        self.twgnlayer.setColumnCount(2)
        self.twgnlayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnlayer.verticalHeader().hide()
        self.lblpara = QtWidgets.QLabel(UpdateMlMlp)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(410, 150, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(UpdateMlMlp)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(410, 190, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(550, 190, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(UpdateMlMlp)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(410, 230, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(550, 230, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(UpdateMlMlp)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(410, 270, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(550, 270, 40, 30))
        self.lblfcdropout = QtWidgets.QLabel(UpdateMlMlp)
        self.lblfcdropout.setObjectName('lblfcdropout')
        self.lblfcdropout.setGeometry(QtCore.QRect(410, 310, 130, 30))
        self.ldtfcdropout = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtfcdropout.setObjectName('ldtfcdropout')
        self.ldtfcdropout.setGeometry(QtCore.QRect(550, 310, 40, 30))
        self.lblsave = QtWidgets.QLabel(UpdateMlMlp)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 410, 100, 30))
        self.ldtsave = QtWidgets.QLineEdit(UpdateMlMlp)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(110, 410, 210, 30))
        self.btnsave = QtWidgets.QPushButton(UpdateMlMlp)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 410, 60, 30))
        self.btnapply = QtWidgets.QPushButton(UpdateMlMlp)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 410, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/update.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(UpdateMlMlp)
        self.msgbox.setObjectName('msgbox')
        _center_x = UpdateMlMlp.geometry().center().x()
        _center_y = UpdateMlMlp.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(UpdateMlMlp)
        QtCore.QMetaObject.connectSlotsByName(UpdateMlMlp)

    def retranslateGUI(self, UpdateMlMlp):
        self.dialog = UpdateMlMlp
        _translate = QtCore.QCoreApplication.translate
        UpdateMlMlp.setWindowTitle(_translate('UpdateMlMlp', 'Evaluate MLP'))
        self.lblfrom.setText(_translate('UpdateMlMlp', 'Select network:'))
        self.ldtfrom.setText(_translate('UpdateMlMlp', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('UpdateMlMlp', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('UpdateMlMlp', 'Training features:'))
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblpatchsize.setText(_translate('UpdateMlMlp', 'Patch\nsize:'))
        self.lblpatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpatchheight.setText(_translate('UpdateMlMlp', 'height=\ntime/depth'))
        self.ldtpatchheight.setText(_translate('UpdateMlMlp', '1'))
        self.ldtpatchheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpatchwidth.setText(_translate('UpdateMlMlp', 'width=\ncrossline'))
        self.ldtpatchwidth.setText(_translate('UpdateMlMlp', '1'))
        self.ldtpatchwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpatchdepth.setText(_translate('UpdateMlMlp', 'depth=\ninline'))
        self.ldtpatchdepth.setText(_translate('UpdateMlMlp', '1'))
        self.ldtpatchdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtpatchheight.textChanged.connect(self.changeLdtPatchSize)
        self.ldtpatchwidth.textChanged.connect(self.changeLdtPatchSize)
        self.ldtpatchdepth.textChanged.connect(self.changeLdtPatchSize)
        self.lblold.setText(_translate('UpdateMlMlp', 'available:'))
        self.lbloldlength.setText(_translate('UpdateMlMlp', 'length ='))
        self.ldtoldlength.setText(_translate('UpdateMlMlp', ''))
        self.ldtoldlength.setEnabled(False)
        self.ldtoldlength.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldtotal.setText(_translate('UpdateMlMlp', 'total ='))
        self.ldtoldtotal.setText(_translate('UpdateMlMlp', ''))
        self.ldtoldtotal.setEnabled(False)
        self.ldtoldtotal.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnew.setText(_translate('UpdateMlMlp', 'expected:'))
        self.lblnewlength.setText(_translate('UpdateMlMlp', 'length ='))
        self.ldtnewlength.setText(_translate('UpdateMlMlp', ''))
        self.ldtnewlength.setEnabled(False)
        self.ldtnewlength.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewtotal.setText(_translate('UpdateMlMlp', 'total ='))
        self.ldtnewtotal.setText(_translate('UpdateMlMlp', ''))
        self.ldtnewtotal.setEnabled(False)
        self.ldtnewtotal.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltarget.setText(_translate('UpdateMlMlp', 'Training target:'))
        self.btnconfigtraindata.setText(_translate('TrainMlMlp', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lblnetwork.setText(_translate('UpdateMlMlp', 'Pre-trained MLP architecture:'))
        self.btnviewnetwork.setText(_translate('UpdateMlMlp', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnlayer.setText(_translate('UpdateMlMlp', 'No. of MLP layers:'))
        self.lblnlayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnlayer.setText(_translate('UpdateMlMlp', ''))
        self.ldtnlayer.setEnabled(False)
        self.ldtnlayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnlayer.textChanged.connect(self.changeLdtNlayer)
        self.twgnlayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblpara.setText(_translate('UpdateMlMlp', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('UpdateMlMlp', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('UpdateMlMlp', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('UpdateMlMlp', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('UpdateMlMlp', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('UpdateMlMlp', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('UpdateMlMlp', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfcdropout.setText(_translate('UpdateMlMlp', 'MLP dropout rate:'))
        self.lblfcdropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtfcdropout.setText(_translate('UpdateMlMlp', '0.5'))
        self.ldtfcdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('UpdateMlMlp', 'Save new-MLP to:'))
        self.ldtsave.setText(_translate('UpdateMlMlp', ''))
        self.btnsave.setText(_translate('UpdateMlMlp', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('UpdateMlMlp', 'Evaluate MLP'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnUpdateMlMlp)

    def clickBtnFrom(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select MLP Network', (self.rootpath), filter='Tensorflow network files (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.checkFNNModel(self.modelpath, self.modelname) is True:
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
            _len = self.getFeatureLength(_firstfeature.text())
            self.ldtoldlength.setText(str(_len))
            _len = self.modelinfo['feature_length'][0]
            self.ldtnewlength.setText(str(_len))
            _len = self.getTotalFeatureLength(self.modelinfo['feature_list'])
            self.ldtoldtotal.setText(str(_len))
            self.ldtnewtotal.setText(str(self.modelinfo['number_feature']))
            self.cbbtarget.clear()
            self.cbbtarget.addItem(self.modelinfo['target'])
            self.btnviewnetwork.setEnabled(True)
            self.ldtnlayer.setText(str(self.modelinfo['number_layer']))
        else:
            self.modelpath = ''
            self.modelname = ''
            self.modelinfo = None
            self.lwgfeature.clear()
            self.ldtoldlength.setText('')
            self.ldtoldtotal.setText('')
            self.ldtnewlength.setText('')
            self.ldtnewtotal.setText('')
            self.cbbtarget.clear()
            self.btnviewnetwork.setEnabled(False)
            self.ldtnlayer.setText('')

    def changeLwgFeature(self):
        if ml_tfm.checkFNNModel(self.modelpath, self.modelname):
            _len = self.getFeatureLength(self.lwgfeature.currentItem().text())
            self.ldtoldlength.setText(str(_len))
            _len = self.modelinfo['feature_length'][self.lwgfeature.currentIndex().row()]
            self.ldtnewlength.setText(str(_len))

    def changeLdtPatchSize(self):
        if ml_tfm.checkFNNModel(self.modelpath, self.modelname):
            _len = self.getFeatureLength(self.lwgfeature.currentItem().text())
            self.ldtoldlength.setText(str(_len))
            _len = self.getTotalFeatureLength(self.modelinfo['feature_list'])
            self.ldtoldtotal.setText(str(_len))

    def changeLdtNlayer(self):
        if ml_tfm.checkFNNModel(self.modelpath, self.modelname) is True:
            _nlayer = self.modelinfo['number_layer']
            self.twgnlayer.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnlayer.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.modelinfo['number_neuron'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnlayer.setItem(_idx, 1, item)

        else:
            self.twgnlayer.setRowCount(0)

    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Save MLP Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtsave.setText(_file[0])

    def clickBtnViewNetwork(self):
        _viewmlmlp = QtWidgets.QDialog()
        _gui = gui_viewmlmlp()
        _gui.linestyle = self.linestyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewmlmlp)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewmlmlp.exec()
        _viewmlmlp.show()

    def clickBtnConfigTrainData(self):
        _configtraindata = QtWidgets.QDialog()
        _gui = gui_configmltraindata()
        _gui.mltraindataconfig = self.traindataconfig
        _gui.pointsetlist = sorted(self.pointsetdata.keys())
        _gui.setupGUI(_configtraindata)
        _configtraindata.exec()
        self.traindataconfig = _gui.mltraindataconfig
        _configtraindata.show()

    def clickBtnUpdateMlMlp(self):
        self.refreshMsgBox()
        if self.checkSurvInfo() is False:
            vis_msg.print('ERROR in UpdateMlMlp: No seismic data available', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update MLP', 'No seismic data available')
            return
        if ml_tfm.checkFNNModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in UpdateMlMlp: No MLP network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update MLP', 'No MLP network found')
            return
        for f in self.modelinfo['feature_list']:
            if self.checkSeisData(f) is False:
                vis_msg.print(("ERROR in UpdateMlMlp: Feature '%s' not found in seismic data" % f), type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Update MLP', "Feature '" + f + "' not found in seismic data")
                return

        if self.modelinfo['target'] not in self.seisdata.keys():
            vis_msg.print(("ERROR in EvauluateMlMlp: Target label '%s' not found in seismic data" % self.modelinfo['target']),
              type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update MLP', "Target label '" + self.modelinfo['target'] + "' not found in seismic data")
            return
        if self.ldtoldlength.text() != self.ldtnewlength.text() or self.ldtoldtotal.text() != self.ldtnewtotal.text():
            vis_msg.print('ERROR in UpdateMlMlp: Feature length not match', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update MLP', 'Feature length not match')
            return
        _patch_height = basic_data.str2int(self.ldtpatchheight.text())
        _patch_width = basic_data.str2int(self.ldtpatchwidth.text())
        _patch_depth = basic_data.str2int(self.ldtpatchdepth.text())
        if _patch_height is False or _patch_width is False or _patch_depth is False or _patch_height < 1 or _patch_width < 1 or _patch_depth < 1:
            vis_msg.print('ERROR in UpdateMlMlp: Non-positive patch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update MLP', 'Non-positive patch size')
            return
        _patch_height = 2 * int(_patch_height / 2) + 1
        _patch_width = 2 * int(_patch_width / 2) + 1
        _patch_depth = 2 * int(_patch_depth / 2) + 1
        _features = self.modelinfo['feature_list']
        _target = self.modelinfo['target']
        _nepoch = basic_data.str2int(self.ldtnepoch.text())
        _batchsize = basic_data.str2int(self.ldtbatchsize.text())
        _learning_rate = basic_data.str2float(self.ldtlearnrate.text())
        _dropout_prob_fclayer = basic_data.str2float(self.ldtfcdropout.text())
        if _nepoch is False or _nepoch <= 0:
            vis_msg.print('ERROR in UpdateMlMlp: Non-positive epoch number', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update MLP', 'Non-positive epoch number')
            return
        if _batchsize is False or _batchsize <= 0:
            vis_msg.print('ERROR in UpdateMlMlp: Non-positive batch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update MLP', 'Non-positive batch size')
            return
        if _learning_rate is False or _learning_rate <= 0:
            vis_msg.print('ERROR in UpdateMlMlp: Non-positive learning rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update MLP', 'Non-positive learning rate')
            return
        if _dropout_prob_fclayer is False or _dropout_prob_fclayer <= 0:
            vis_msg.print('ERROR in UpdateMlMlp: Negative dropout rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update MLP', 'Negative dropout rate')
            return
        if len(self.ldtsave.text()) < 1:
            vis_msg.print('ERROR in UpdateMlMlp: No name specified for MLP network', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update MLP', 'No name specified for MLP network')
            return
        _savepath = os.path.dirname(self.ldtsave.text())
        _savename = os.path.splitext(os.path.basename(self.ldtsave.text()))[0]
        _wdinl = int(_patch_depth / 2)
        _wdxl = int(_patch_width / 2)
        _wdz = int(_patch_height / 2)
        _seisinfo = self.survinfo
        print('UpdateMlMlp: Step 1 - Get training samples:')
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
            vis_msg.print('ERROR in UpdateMlp: No training sample found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Update MLP', 'No training sample found')
            return
        print('UpdateMlMlp: Step 2 - Retrieve features')
        _traindict = {}
        for f in _features:
            _seisdata = self.seisdata[f]
            _traindict[f] = seis_ays.retrieveSeisWindowFrom3DMat(_seisdata, _traindata, seisinfo=(self.survinfo), wdinl=_wdinl,
              wdxl=_wdxl,
              wdz=_wdz,
              verbose=False)[:, 3:]

        if _target not in _features:
            _seisdata = self.seisdata[_target]
            _traindict[_target] = seis_ays.retrieveSeisSampleFrom3DMat(_seisdata, _traindata, seisinfo=(self.survinfo), verbose=False)[:, 3:]
        else:
            if self.traindataconfig['RemoveInvariantFeature_Checked']:
                for f in _features:
                    _traindict = ml_aug.removeInvariantFeature(_traindict, f)
                    if basic_mdt.maxDictConstantRow(_traindict) <= 0:
                        print('UpdateMlMlp: No training sample found')
                        QtWidgets.QMessageBox.critical(self.msgbox, 'Update MLP', 'No training sample found')
                        return

            _traindict[_target] = np.round(_traindict[_target]).astype(int)
            print('UpdateMlp: A total of %d valid training samples' % basic_mdt.maxDictConstantRow(_traindict))
            print('UpdateMlMlp: Step 3 - Balance labels')
            if self.traindataconfig['BalanceTarget_Checked']:
                _traindict = ml_aug.balanceLabelbyExtension(_traindict, _target)
                print('UpdateMlMlp: A total of %d training samples after balance' % np.shape(_traindict[_target])[0])
            else:
                print('UpdateMlMlp: No balance applied')
        print('TrainMlMlp: Step 4 - Start training')
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Train MLP')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _fnnlog = ml_fnn.updateFNNClassifier(_traindict, fnnpath=(self.modelpath),
          fnnname=(self.modelname),
          nepoch=_nepoch,
          batchsize=_batchsize,
          dropoutprobfclayer=_dropout_prob_fclayer,
          learningrate=_learning_rate,
          save2disk=True,
          savepath=_savepath,
          savename=_savename,
          qpgsdlg=_pgsdlg)
        QtWidgets.QMessageBox.information(self.msgbox, 'Update MLP', 'MLP trained successfully')
        reply = QtWidgets.QMessageBox.question(self.msgbox, 'Update MLP', 'View learning matrix?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            _viewmllearnmat = QtWidgets.QDialog()
            _gui = gui_viewmllearnmat()
            _gui.learnmat = _fnnlog['learning_curve']
            _gui.linestyle = self.linestyle
            _gui.fontstyle = self.fontstyle
            _gui.setupGUI(_viewmllearnmat)
            _viewmllearnmat.exec()
            _viewmllearnmat.show()

    def getTotalFeatureLength(self, featurelist):
        _len = 0
        for f in featurelist:
            if self.checkSurvInfo() and f in self.seisdata.keys() and self.checkSeisData(f):
                _len = _len + self.getFeatureLength(f)

        return _len

    def getFeatureLength(self, feature):
        _len = 0
        if self.checkSurvInfo():
            if feature in self.seisdata.keys():
                if self.checkSeisData(feature):
                    _dims = np.shape(self.seisdata[feature])[1:]
                    _len = 1
                    for i in _dims:
                        _len = _len * i

        _len = _len * basic_data.str2int(self.ldtpatchheight.text()) * basic_data.str2int(self.ldtpatchwidth.text()) * basic_data.str2int(self.ldtpatchdepth.text())
        return _len

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
    UpdateMlMlp = QtWidgets.QWidget()
    gui = updatemlmlp()
    gui.setupGUI(UpdateMlMlp)
    UpdateMlMlp.show()
    sys.exit(app.exec_())