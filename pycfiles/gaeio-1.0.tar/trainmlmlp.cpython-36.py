# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainmlmlp.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 30700 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.basic.data import data as basic_data
from cognitivegeo.src.basic.matdict import matdict as basic_mdt
from cognitivegeo.src.seismic.analysis import analysis as seis_ays
from cognitivegeo.src.pointset.analysis import analysis as point_ays
from cognitivegeo.src.ml.augmentation import augmentation as ml_aug
from cognitivegeo.src.ml.fnnclassifier import fnnclassifier as ml_fnn
from cognitivegeo.src.gui.viewmllearnmat import viewmllearnmat as gui_viewmllearnmat
from cognitivegeo.src.gui.configmltraindata import configmltraindata as gui_configmltraindata
from cognitivegeo.src.vis.messager import messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainmlmlp(object):
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
    traindataconfig['BalanceTarget_Enabled'] = True
    traindataconfig['BalanceTarget_Checked'] = False
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False

    def setupGUI(self, TrainMlMlp):
        TrainMlMlp.setObjectName('TrainMlMlp')
        TrainMlMlp.setFixedSize(810, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMlMlp.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMlMlp)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMlMlp)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 200))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblpatchsize = QtWidgets.QLabel(TrainMlMlp)
        self.lblpatchsize.setObjectName('lblpatchsize')
        self.lblpatchsize.setGeometry(QtCore.QRect(10, 220, 80, 30))
        self.lblpatchheight = QtWidgets.QLabel(TrainMlMlp)
        self.lblpatchheight.setObjectName('lblpatchheight')
        self.lblpatchheight.setGeometry(QtCore.QRect(110, 220, 50, 30))
        self.ldtpatchheight = QtWidgets.QLineEdit(TrainMlMlp)
        self.ldtpatchheight.setObjectName('ldtpatchheight')
        self.ldtpatchheight.setGeometry(QtCore.QRect(160, 220, 40, 30))
        self.lblpatchwidth = QtWidgets.QLabel(TrainMlMlp)
        self.lblpatchwidth.setObjectName('lblpatchwidth')
        self.lblpatchwidth.setGeometry(QtCore.QRect(205, 220, 50, 30))
        self.ldtpatchwidth = QtWidgets.QLineEdit(TrainMlMlp)
        self.ldtpatchwidth.setObjectName('ldtpatchwidth')
        self.ldtpatchwidth.setGeometry(QtCore.QRect(255, 220, 40, 30))
        self.lblpatchdepth = QtWidgets.QLabel(TrainMlMlp)
        self.lblpatchdepth.setObjectName('lblpatchdepth')
        self.lblpatchdepth.setGeometry(QtCore.QRect(300, 220, 50, 30))
        self.ldtpatchdepth = QtWidgets.QLineEdit(TrainMlMlp)
        self.ldtpatchdepth.setObjectName('ldtpatchdepth')
        self.ldtpatchdepth.setGeometry(QtCore.QRect(350, 220, 40, 30))
        self.lbllength = QtWidgets.QLabel(TrainMlMlp)
        self.lbllength.setObjectName('lbllength')
        self.lbllength.setGeometry(QtCore.QRect(110, 260, 50, 30))
        self.ldtlength = QtWidgets.QLineEdit(TrainMlMlp)
        self.ldtlength.setObjectName('ldtlength')
        self.ldtlength.setGeometry(QtCore.QRect(160, 260, 40, 30))
        self.lbltotal = QtWidgets.QLabel(TrainMlMlp)
        self.lbltotal.setObjectName('lbltotal')
        self.lbltotal.setGeometry(QtCore.QRect(300, 260, 50, 30))
        self.ldttotal = QtWidgets.QLineEdit(TrainMlMlp)
        self.ldttotal.setObjectName('ldttotal')
        self.ldttotal.setGeometry(QtCore.QRect(350, 260, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMlMlp)
        self.lbltarget.setObjectName('lbltargete')
        self.lbltarget.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMlMlp)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 310, 110, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMlMlp)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 310, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblnetwork = QtWidgets.QLabel(TrainMlMlp)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblnlayer = QtWidgets.QLabel(TrainMlMlp)
        self.lblnlayer.setObjectName('lblnlayer')
        self.lblnlayer.setGeometry(QtCore.QRect(410, 50, 130, 30))
        self.ldtnlayer = QtWidgets.QLineEdit(TrainMlMlp)
        self.ldtnlayer.setObjectName('ldtnlayer')
        self.ldtnlayer.setGeometry(QtCore.QRect(550, 50, 40, 30))
        self.twgnlayer = QtWidgets.QTableWidget(TrainMlMlp)
        self.twgnlayer.setObjectName('twgnlayer')
        self.twgnlayer.setGeometry(QtCore.QRect(610, 50, 180, 240))
        self.twgnlayer.setColumnCount(2)
        self.twgnlayer.verticalHeader().hide()
        self.lblpara = QtWidgets.QLabel(TrainMlMlp)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(410, 100, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMlMlp)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(410, 140, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMlMlp)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(550, 140, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMlMlp)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(410, 180, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMlMlp)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(550, 180, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMlMlp)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(410, 220, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMlMlp)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(550, 220, 40, 30))
        self.lblfcdropout = QtWidgets.QLabel(TrainMlMlp)
        self.lblfcdropout.setObjectName('lblfcdropout')
        self.lblfcdropout.setGeometry(QtCore.QRect(410, 260, 130, 30))
        self.ldtfcdropout = QtWidgets.QLineEdit(TrainMlMlp)
        self.ldtfcdropout.setObjectName('ldtfcdropout')
        self.ldtfcdropout.setGeometry(QtCore.QRect(550, 260, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMlMlp)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 360, 100, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMlMlp)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(110, 360, 210, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMlMlp)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 360, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMlMlp)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 360, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMlMlp)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMlMlp.geometry().center().x()
        _center_y = TrainMlMlp.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMlMlp)
        QtCore.QMetaObject.connectSlotsByName(TrainMlMlp)

    def retranslateGUI(self, TrainMlMlp):
        self.dialog = TrainMlMlp
        _translate = QtCore.QCoreApplication.translate
        TrainMlMlp.setWindowTitle(_translate('TrainMlMlp', 'Train MLP'))
        self.lblfeature.setText(_translate('TrainMlMlp', 'Select features:'))
        self.lbltarget.setText(_translate('TrainMlMlp', 'Select target:'))
        self.btnconfigtraindata.setText(_translate('TrainMlMlp', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lblpatchsize.setText(_translate('TrainMlMlp', 'Patch\nsize:'))
        self.lblpatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpatchheight.setText(_translate('TrainMlMlp', 'height=\ntime/depth'))
        self.ldtpatchheight.setText(_translate('TrainMlMlp', '1'))
        self.ldtpatchheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpatchwidth.setText(_translate('TrainMlMlp', 'width=\ncrossline'))
        self.ldtpatchwidth.setText(_translate('TrainMlMlp', '1'))
        self.ldtpatchwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpatchdepth.setText(_translate('TrainMlMlp', 'depth=\ninline'))
        self.ldtpatchdepth.setText(_translate('TrainMlMlp', '1'))
        self.ldtpatchdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtpatchheight.textChanged.connect(self.changeLdtPatchSize)
        self.ldtpatchwidth.textChanged.connect(self.changeLdtPatchSize)
        self.ldtpatchdepth.textChanged.connect(self.changeLdtPatchSize)
        self.lbllength.setText(_translate('TrainMlMlp', 'length ='))
        self.ldtlength.setText(_translate('TrainMlMlp', ''))
        self.ldtlength.setEnabled(False)
        self.ldtlength.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltotal.setText(_translate('TrainMlMlp', 'total ='))
        self.ldttotal.setText(_translate('TrainMlMlp', ''))
        self.ldttotal.setEnabled(False)
        self.ldttotal.setAlignment(QtCore.Qt.AlignCenter)
        if self.checkSurvInfo() is True:
            self.featurelist.clear()
            self.lwgfeature.clear()
            self.cbbtarget.clear()
            _firstfeature = None
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    self.featurelist.append(i)
                    item = QtWidgets.QListWidgetItem(self.lwgfeature)
                    item.setText(_translate('TrainMlMlp', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            _len = self.getFeatureLength(_firstfeature.text())
            self.ldtlength.setText(_translate('TrainMlMlp', str(_len)))
            _len = self.getTotalFeatureLength([_firstfeature.text()])
            self.ldttotal.setText(_translate('TrainMlMlp', str(_len)))
            self.cbbtarget.addItems(self.featurelist)
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblnetwork.setText(_translate('TrainMlMlp', 'Specify MLP architecture:'))
        self.lblnlayer.setText(_translate('TrainMlMlp', 'No. of MLP layers:'))
        self.lblnlayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnlayer.setText(_translate('TrainMlMlp', '2'))
        self.ldtnlayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnlayer.textChanged.connect(self.changeLdtNlayer)
        self.twgnlayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.twgnlayer.setRowCount(2)
        for _idx in range(int(self.ldtnlayer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMlMlp', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgnlayer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgnlayer.setItem(_idx, 1, item)

        self.lblpara.setText(_translate('TrainMlMlp', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMlMlp', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMlMlp', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMlMlp', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMlMlp', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMlMlp', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMlMlp', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfcdropout.setText(_translate('TrainMlMlp', 'MLP dropout rate:'))
        self.lblfcdropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtfcdropout.setText(_translate('TrainMlMlp', '0.5'))
        self.ldtfcdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMlMlp', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMlMlp', ''))
        self.btnsave.setText(_translate('TrainMlMlp', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMlMlp', 'Train MLP'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMlMlp)

    def changeLwgFeature(self):
        _len = self.getFeatureLength(self.lwgfeature.currentItem().text())
        self.ldtlength.setText(str(_len))
        _featurelist = self.lwgfeature.selectedItems()
        _featurelist = [f.text() for f in _featurelist]
        _len = self.getTotalFeatureLength(_featurelist)
        self.ldttotal.setText(str(_len))

    def changeLdtPatchSize(self):
        if self.checkSurvInfo():
            if self.checkSeisData(self.lwgfeature.currentItem().text()):
                _len = self.getFeatureLength(self.lwgfeature.currentItem().text())
                self.ldtlength.setText(str(_len))
                _featurelist = self.lwgfeature.selectedItems()
                _featurelist = [f.text() for f in _featurelist]
                _len = self.getTotalFeatureLength(_featurelist)
                self.ldttotal.setText(str(_len))

    def changeLdtNlayer(self):
        if len(self.ldtnlayer.text()) > 0:
            _nlayer = int(self.ldtnlayer.text())
            self.twgnlayer.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnlayer.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(1024))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgnlayer.setItem(_idx, 1, item)

        else:
            self.twgnlayer.setRowCount(0)

    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Save MLP Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
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

    def clickBtnTrainMlMlp(self):
        self.refreshMsgBox()
        if len(self.lwgfeature.selectedItems()) < 1:
            vis_msg.print('ERROR in TrainMlMlp: No feature selected for training', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train MLP', 'No feature selected for training')
            return
        _patch_height = basic_data.str2int(self.ldtpatchheight.text())
        _patch_width = basic_data.str2int(self.ldtpatchwidth.text())
        _patch_depth = basic_data.str2int(self.ldtpatchdepth.text())
        if _patch_height is False or _patch_width is False or _patch_depth is False or _patch_height < 1 or _patch_width < 1 or _patch_depth < 1:
            vis_msg.print('ERROR in TrainMlMlp: Non-positive patch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train MLP', 'Non-positive patch size')
            return
        _patch_height = 2 * int(_patch_height / 2) + 1
        _patch_width = 2 * int(_patch_width / 2) + 1
        _patch_depth = 2 * int(_patch_depth / 2) + 1
        _features = self.lwgfeature.selectedItems()
        _features = [f.text() for f in _features]
        _target = self.featurelist[self.cbbtarget.currentIndex()]
        _nlayer = basic_data.str2int(self.ldtnlayer.text())
        _nneuron = [basic_data.str2int(self.twgnlayer.item(i, 1).text()) for i in range(_nlayer)]
        _nepoch = basic_data.str2int(self.ldtnepoch.text())
        _batchsize = basic_data.str2int(self.ldtbatchsize.text())
        _learning_rate = basic_data.str2float(self.ldtlearnrate.text())
        _dropout_prob_fclayer = basic_data.str2float(self.ldtfcdropout.text())
        if _nlayer is False or _nlayer <= 0:
            vis_msg.print('ERROR in TrainMlMlp: Non-positive layer number', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train MLP', 'Non-positive layer number')
            return
        for _i in _nneuron:
            if _i is False or _i <= 0:
                vis_msg.print('ERROR in TrainMlMlp: Non-positive neuron number', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Train MLP', 'Non-positive neuron number')
                return

        if _nepoch is False or _nepoch <= 0:
            vis_msg.print('ERROR in TrainMlMlp: Non-positive nepoch', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train MLP', 'Non-positive nepoch')
            return
        if _batchsize is False or _batchsize <= 0:
            vis_msg.print('ERROR in TrainMlMlp: Non-positive batch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train MLP', 'Non-positive batch size')
            return
        if _learning_rate is False or _learning_rate <= 0:
            vis_msg.print('ERROR in TrainMlMlp: Non-positive learning rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train MLP', 'Non-positive learning rate')
            return
        if _dropout_prob_fclayer is False or _dropout_prob_fclayer <= 0:
            vis_msg.print('ERROR in TrainMlMlp: Negative dropout rate', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train MLP', 'Negative dropout rate')
            return
        if len(self.ldtsave.text()) < 1:
            vis_msg.print('ERROR in TrainMlMlp: No name specified for MLP network', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train MLP', 'No name specified for MLP network')
            return
        _savepath = os.path.dirname(self.ldtsave.text())
        _savename = os.path.splitext(os.path.basename(self.ldtsave.text()))[0]
        if _target in _features:
            vis_msg.print('ERROR in TrainMlMlp: Target also used as features', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train MLP', 'Target also used as features')
            return
        _wdinl = int(_patch_depth / 2)
        _wdxl = int(_patch_width / 2)
        _wdz = int(_patch_height / 2)
        _seisinfo = self.survinfo
        print('TrainMlMlp: Step 1 - Get training samples:')
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
            vis_msg.print('ERROR in TrainMlMlp: No training sample found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Train MLP', 'No training sample found')
            return
        print('TrainMlMlp: Step 2 - Retrieve features')
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
                        vis_msg.print('ERROR in TrainMlMlp: No training sample found', tpe='error')
                        QtWidgets.QMessageBox.critical(self.msgbox, 'Train MLP', 'No training sample found')
                        return

            _traindict[_target] = np.round(_traindict[_target]).astype(int)
            print('TrainMlMlp: A total of %d valid training samples' % basic_mdt.maxDictConstantRow(_traindict))
            print('TrainMlMlp: Step 3 - Balance labels')
            if self.traindataconfig['BalanceTarget_Checked']:
                _traindict = ml_aug.balanceLabelbyExtension(_traindict, _target)
                print('TrainMlMlp: A total of %d training samples after balance' % np.shape(_traindict[_target])[0])
            else:
                print('TrainMlMlp: No balance applied')
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
        _fnnlog = ml_fnn.createFNNClassifier(_traindict, features=_features,
          target=_target,
          nepoch=_nepoch,
          batchsize=_batchsize,
          nlayer=_nlayer,
          nneuron=_nneuron,
          learningrate=_learning_rate,
          dropoutprobfclayer=_dropout_prob_fclayer,
          save2disk=True,
          savepath=_savepath,
          savename=_savename,
          qpgsdlg=_pgsdlg)
        QtWidgets.QMessageBox.information(self.msgbox, 'Train MLP', 'MLP trained successfully')
        reply = QtWidgets.QMessageBox.question(self.msgbox, 'Train MLP', 'View learning matrix?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
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
    TrainMlMlp = QtWidgets.QWidget()
    gui = trainmlmlp()
    gui.setupGUI(TrainMlMlp)
    TrainMlMlp.show()
    sys.exit(app.exec_())