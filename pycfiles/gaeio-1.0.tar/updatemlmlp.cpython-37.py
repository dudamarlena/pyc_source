# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\updatemlmlp.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 35901 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.pointset.analysis as point_ays
import cognitivegeo.src.ml.augmentation as ml_aug
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.fnnclassifier as ml_fnn
import cognitivegeo.src.gui.viewmlmlp as gui_viewmlmlp
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
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

    def clickBtnUpdateMlMlp--- This code section failed: ---

 L. 448         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 450         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 451        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in UpdateMlMlp: No seismic data available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 452        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 453        44  LOAD_STR                 'Update MLP'

 L. 454        46  LOAD_STR                 'No seismic data available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 455        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 457        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkFNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 458        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in UpdateMlMlp: No MLP network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 459        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 460       100  LOAD_STR                 'Update MLP'

 L. 461       102  LOAD_STR                 'No MLP network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 462       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 464       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 465       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 466       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in UpdateMlMlp: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    

 L. 467       152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 468       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 469       170  LOAD_STR                 'Update MLP'

 L. 470       172  LOAD_STR                 "Feature '"
              174  LOAD_FAST                'f'
              176  BINARY_ADD       
              178  LOAD_STR                 "' not found in seismic data"
              180  BINARY_ADD       
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L. 471       186  LOAD_CONST               None
              188  RETURN_VALUE     
              190  JUMP_BACK           124  'to 124'
              192  POP_BLOCK        
            194_0  COME_FROM_LOOP      112  '112'

 L. 473       194  LOAD_FAST                'self'
              196  LOAD_ATTR                modelinfo
              198  LOAD_STR                 'target'
              200  BINARY_SUBSCR    
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                seisdata
              206  LOAD_METHOD              keys
              208  CALL_METHOD_0         0  '0 positional arguments'
              210  COMPARE_OP               not-in
          212_214  POP_JUMP_IF_FALSE   276  'to 276'

 L. 474       216  LOAD_GLOBAL              vis_msg
              218  LOAD_ATTR                print
              220  LOAD_STR                 "ERROR in EvauluateMlMlp: Target label '%s' not found in seismic data"

 L. 475       222  LOAD_FAST                'self'
              224  LOAD_ATTR                modelinfo
              226  LOAD_STR                 'target'
              228  BINARY_SUBSCR    
              230  BINARY_MODULO    
              232  LOAD_STR                 'error'
              234  LOAD_CONST               ('type',)
              236  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              238  POP_TOP          

 L. 476       240  LOAD_GLOBAL              QtWidgets
              242  LOAD_ATTR                QMessageBox
              244  LOAD_METHOD              critical
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                msgbox

 L. 477       250  LOAD_STR                 'Update MLP'

 L. 478       252  LOAD_STR                 "Target label '"
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                modelinfo
              258  LOAD_STR                 'target'
              260  BINARY_SUBSCR    
              262  BINARY_ADD       
              264  LOAD_STR                 "' not found in seismic data"
              266  BINARY_ADD       
              268  CALL_METHOD_3         3  '3 positional arguments'
              270  POP_TOP          

 L. 479       272  LOAD_CONST               None
              274  RETURN_VALUE     
            276_0  COME_FROM           212  '212'

 L. 481       276  LOAD_FAST                'self'
              278  LOAD_ATTR                ldtoldlength
              280  LOAD_METHOD              text
              282  CALL_METHOD_0         0  '0 positional arguments'
              284  LOAD_FAST                'self'
              286  LOAD_ATTR                ldtnewlength
              288  LOAD_METHOD              text
              290  CALL_METHOD_0         0  '0 positional arguments'
              292  COMPARE_OP               !=
          294_296  POP_JUMP_IF_TRUE    320  'to 320'

 L. 482       298  LOAD_FAST                'self'
              300  LOAD_ATTR                ldtoldtotal
              302  LOAD_METHOD              text
              304  CALL_METHOD_0         0  '0 positional arguments'
              306  LOAD_FAST                'self'
              308  LOAD_ATTR                ldtnewtotal
              310  LOAD_METHOD              text
              312  CALL_METHOD_0         0  '0 positional arguments'
              314  COMPARE_OP               !=
          316_318  POP_JUMP_IF_FALSE   356  'to 356'
            320_0  COME_FROM           294  '294'

 L. 483       320  LOAD_GLOBAL              vis_msg
              322  LOAD_ATTR                print
              324  LOAD_STR                 'ERROR in UpdateMlMlp: Feature length not match'
              326  LOAD_STR                 'error'
              328  LOAD_CONST               ('type',)
              330  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              332  POP_TOP          

 L. 484       334  LOAD_GLOBAL              QtWidgets
              336  LOAD_ATTR                QMessageBox
              338  LOAD_METHOD              critical
              340  LOAD_FAST                'self'
              342  LOAD_ATTR                msgbox

 L. 485       344  LOAD_STR                 'Update MLP'

 L. 486       346  LOAD_STR                 'Feature length not match'
              348  CALL_METHOD_3         3  '3 positional arguments'
              350  POP_TOP          

 L. 487       352  LOAD_CONST               None
              354  RETURN_VALUE     
            356_0  COME_FROM           316  '316'

 L. 489       356  LOAD_GLOBAL              basic_data
              358  LOAD_METHOD              str2int
              360  LOAD_FAST                'self'
              362  LOAD_ATTR                ldtpatchheight
              364  LOAD_METHOD              text
              366  CALL_METHOD_0         0  '0 positional arguments'
              368  CALL_METHOD_1         1  '1 positional argument'
              370  STORE_FAST               '_patch_height'

 L. 490       372  LOAD_GLOBAL              basic_data
              374  LOAD_METHOD              str2int
              376  LOAD_FAST                'self'
              378  LOAD_ATTR                ldtpatchwidth
              380  LOAD_METHOD              text
              382  CALL_METHOD_0         0  '0 positional arguments'
              384  CALL_METHOD_1         1  '1 positional argument'
              386  STORE_FAST               '_patch_width'

 L. 491       388  LOAD_GLOBAL              basic_data
              390  LOAD_METHOD              str2int
              392  LOAD_FAST                'self'
              394  LOAD_ATTR                ldtpatchdepth
              396  LOAD_METHOD              text
              398  CALL_METHOD_0         0  '0 positional arguments'
              400  CALL_METHOD_1         1  '1 positional argument'
              402  STORE_FAST               '_patch_depth'

 L. 492       404  LOAD_FAST                '_patch_height'
              406  LOAD_CONST               False
              408  COMPARE_OP               is
          410_412  POP_JUMP_IF_TRUE    464  'to 464'
              414  LOAD_FAST                '_patch_width'
              416  LOAD_CONST               False
              418  COMPARE_OP               is
          420_422  POP_JUMP_IF_TRUE    464  'to 464'
              424  LOAD_FAST                '_patch_depth'
              426  LOAD_CONST               False
              428  COMPARE_OP               is
          430_432  POP_JUMP_IF_TRUE    464  'to 464'

 L. 493       434  LOAD_FAST                '_patch_height'
              436  LOAD_CONST               1
              438  COMPARE_OP               <
          440_442  POP_JUMP_IF_TRUE    464  'to 464'
              444  LOAD_FAST                '_patch_width'
              446  LOAD_CONST               1
              448  COMPARE_OP               <
          450_452  POP_JUMP_IF_TRUE    464  'to 464'
              454  LOAD_FAST                '_patch_depth'
              456  LOAD_CONST               1
              458  COMPARE_OP               <
          460_462  POP_JUMP_IF_FALSE   500  'to 500'
            464_0  COME_FROM           450  '450'
            464_1  COME_FROM           440  '440'
            464_2  COME_FROM           430  '430'
            464_3  COME_FROM           420  '420'
            464_4  COME_FROM           410  '410'

 L. 494       464  LOAD_GLOBAL              vis_msg
              466  LOAD_ATTR                print
              468  LOAD_STR                 'ERROR in UpdateMlMlp: Non-positive patch size'
              470  LOAD_STR                 'error'
              472  LOAD_CONST               ('type',)
              474  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              476  POP_TOP          

 L. 495       478  LOAD_GLOBAL              QtWidgets
              480  LOAD_ATTR                QMessageBox
              482  LOAD_METHOD              critical
              484  LOAD_FAST                'self'
              486  LOAD_ATTR                msgbox

 L. 496       488  LOAD_STR                 'Update MLP'

 L. 497       490  LOAD_STR                 'Non-positive patch size'
              492  CALL_METHOD_3         3  '3 positional arguments'
              494  POP_TOP          

 L. 498       496  LOAD_CONST               None
              498  RETURN_VALUE     
            500_0  COME_FROM           460  '460'

 L. 500       500  LOAD_CONST               2
              502  LOAD_GLOBAL              int
              504  LOAD_FAST                '_patch_height'
              506  LOAD_CONST               2
              508  BINARY_TRUE_DIVIDE
              510  CALL_FUNCTION_1       1  '1 positional argument'
              512  BINARY_MULTIPLY  
              514  LOAD_CONST               1
              516  BINARY_ADD       
              518  STORE_FAST               '_patch_height'

 L. 501       520  LOAD_CONST               2
              522  LOAD_GLOBAL              int
              524  LOAD_FAST                '_patch_width'
              526  LOAD_CONST               2
              528  BINARY_TRUE_DIVIDE
              530  CALL_FUNCTION_1       1  '1 positional argument'
              532  BINARY_MULTIPLY  
              534  LOAD_CONST               1
              536  BINARY_ADD       
              538  STORE_FAST               '_patch_width'

 L. 502       540  LOAD_CONST               2
              542  LOAD_GLOBAL              int
              544  LOAD_FAST                '_patch_depth'
              546  LOAD_CONST               2
              548  BINARY_TRUE_DIVIDE
              550  CALL_FUNCTION_1       1  '1 positional argument'
              552  BINARY_MULTIPLY  
              554  LOAD_CONST               1
              556  BINARY_ADD       
              558  STORE_FAST               '_patch_depth'

 L. 504       560  LOAD_FAST                'self'
              562  LOAD_ATTR                modelinfo
              564  LOAD_STR                 'feature_list'
              566  BINARY_SUBSCR    
              568  STORE_FAST               '_features'

 L. 505       570  LOAD_FAST                'self'
              572  LOAD_ATTR                modelinfo
              574  LOAD_STR                 'target'
              576  BINARY_SUBSCR    
              578  STORE_FAST               '_target'

 L. 507       580  LOAD_GLOBAL              basic_data
              582  LOAD_METHOD              str2int
              584  LOAD_FAST                'self'
              586  LOAD_ATTR                ldtnepoch
              588  LOAD_METHOD              text
              590  CALL_METHOD_0         0  '0 positional arguments'
              592  CALL_METHOD_1         1  '1 positional argument'
              594  STORE_FAST               '_nepoch'

 L. 508       596  LOAD_GLOBAL              basic_data
              598  LOAD_METHOD              str2int
              600  LOAD_FAST                'self'
              602  LOAD_ATTR                ldtbatchsize
              604  LOAD_METHOD              text
              606  CALL_METHOD_0         0  '0 positional arguments'
              608  CALL_METHOD_1         1  '1 positional argument'
              610  STORE_FAST               '_batchsize'

 L. 509       612  LOAD_GLOBAL              basic_data
              614  LOAD_METHOD              str2float
              616  LOAD_FAST                'self'
              618  LOAD_ATTR                ldtlearnrate
              620  LOAD_METHOD              text
              622  CALL_METHOD_0         0  '0 positional arguments'
              624  CALL_METHOD_1         1  '1 positional argument'
              626  STORE_FAST               '_learning_rate'

 L. 510       628  LOAD_GLOBAL              basic_data
              630  LOAD_METHOD              str2float
              632  LOAD_FAST                'self'
              634  LOAD_ATTR                ldtfcdropout
              636  LOAD_METHOD              text
              638  CALL_METHOD_0         0  '0 positional arguments'
              640  CALL_METHOD_1         1  '1 positional argument'
              642  STORE_FAST               '_dropout_prob_fclayer'

 L. 511       644  LOAD_FAST                '_nepoch'
              646  LOAD_CONST               False
              648  COMPARE_OP               is
          650_652  POP_JUMP_IF_TRUE    664  'to 664'
              654  LOAD_FAST                '_nepoch'
              656  LOAD_CONST               0
              658  COMPARE_OP               <=
          660_662  POP_JUMP_IF_FALSE   700  'to 700'
            664_0  COME_FROM           650  '650'

 L. 512       664  LOAD_GLOBAL              vis_msg
              666  LOAD_ATTR                print
              668  LOAD_STR                 'ERROR in UpdateMlMlp: Non-positive epoch number'
              670  LOAD_STR                 'error'
              672  LOAD_CONST               ('type',)
              674  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              676  POP_TOP          

 L. 513       678  LOAD_GLOBAL              QtWidgets
              680  LOAD_ATTR                QMessageBox
              682  LOAD_METHOD              critical
              684  LOAD_FAST                'self'
              686  LOAD_ATTR                msgbox

 L. 514       688  LOAD_STR                 'Update MLP'

 L. 515       690  LOAD_STR                 'Non-positive epoch number'
              692  CALL_METHOD_3         3  '3 positional arguments'
              694  POP_TOP          

 L. 516       696  LOAD_CONST               None
              698  RETURN_VALUE     
            700_0  COME_FROM           660  '660'

 L. 517       700  LOAD_FAST                '_batchsize'
              702  LOAD_CONST               False
              704  COMPARE_OP               is
          706_708  POP_JUMP_IF_TRUE    720  'to 720'
              710  LOAD_FAST                '_batchsize'
              712  LOAD_CONST               0
              714  COMPARE_OP               <=
          716_718  POP_JUMP_IF_FALSE   756  'to 756'
            720_0  COME_FROM           706  '706'

 L. 518       720  LOAD_GLOBAL              vis_msg
              722  LOAD_ATTR                print
              724  LOAD_STR                 'ERROR in UpdateMlMlp: Non-positive batch size'
              726  LOAD_STR                 'error'
              728  LOAD_CONST               ('type',)
              730  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              732  POP_TOP          

 L. 519       734  LOAD_GLOBAL              QtWidgets
              736  LOAD_ATTR                QMessageBox
              738  LOAD_METHOD              critical
              740  LOAD_FAST                'self'
              742  LOAD_ATTR                msgbox

 L. 520       744  LOAD_STR                 'Update MLP'

 L. 521       746  LOAD_STR                 'Non-positive batch size'
              748  CALL_METHOD_3         3  '3 positional arguments'
              750  POP_TOP          

 L. 522       752  LOAD_CONST               None
              754  RETURN_VALUE     
            756_0  COME_FROM           716  '716'

 L. 523       756  LOAD_FAST                '_learning_rate'
              758  LOAD_CONST               False
              760  COMPARE_OP               is
          762_764  POP_JUMP_IF_TRUE    776  'to 776'
              766  LOAD_FAST                '_learning_rate'
              768  LOAD_CONST               0
              770  COMPARE_OP               <=
          772_774  POP_JUMP_IF_FALSE   812  'to 812'
            776_0  COME_FROM           762  '762'

 L. 524       776  LOAD_GLOBAL              vis_msg
              778  LOAD_ATTR                print
              780  LOAD_STR                 'ERROR in UpdateMlMlp: Non-positive learning rate'
              782  LOAD_STR                 'error'
              784  LOAD_CONST               ('type',)
              786  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              788  POP_TOP          

 L. 525       790  LOAD_GLOBAL              QtWidgets
              792  LOAD_ATTR                QMessageBox
              794  LOAD_METHOD              critical
              796  LOAD_FAST                'self'
              798  LOAD_ATTR                msgbox

 L. 526       800  LOAD_STR                 'Update MLP'

 L. 527       802  LOAD_STR                 'Non-positive learning rate'
              804  CALL_METHOD_3         3  '3 positional arguments'
              806  POP_TOP          

 L. 528       808  LOAD_CONST               None
              810  RETURN_VALUE     
            812_0  COME_FROM           772  '772'

 L. 529       812  LOAD_FAST                '_dropout_prob_fclayer'
              814  LOAD_CONST               False
              816  COMPARE_OP               is
          818_820  POP_JUMP_IF_TRUE    832  'to 832'
              822  LOAD_FAST                '_dropout_prob_fclayer'
              824  LOAD_CONST               0
              826  COMPARE_OP               <=
          828_830  POP_JUMP_IF_FALSE   868  'to 868'
            832_0  COME_FROM           818  '818'

 L. 530       832  LOAD_GLOBAL              vis_msg
              834  LOAD_ATTR                print
              836  LOAD_STR                 'ERROR in UpdateMlMlp: Negative dropout rate'
              838  LOAD_STR                 'error'
              840  LOAD_CONST               ('type',)
              842  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              844  POP_TOP          

 L. 531       846  LOAD_GLOBAL              QtWidgets
              848  LOAD_ATTR                QMessageBox
              850  LOAD_METHOD              critical
              852  LOAD_FAST                'self'
              854  LOAD_ATTR                msgbox

 L. 532       856  LOAD_STR                 'Update MLP'

 L. 533       858  LOAD_STR                 'Negative dropout rate'
              860  CALL_METHOD_3         3  '3 positional arguments'
              862  POP_TOP          

 L. 534       864  LOAD_CONST               None
              866  RETURN_VALUE     
            868_0  COME_FROM           828  '828'

 L. 536       868  LOAD_GLOBAL              len
              870  LOAD_FAST                'self'
              872  LOAD_ATTR                ldtsave
              874  LOAD_METHOD              text
              876  CALL_METHOD_0         0  '0 positional arguments'
              878  CALL_FUNCTION_1       1  '1 positional argument'
              880  LOAD_CONST               1
              882  COMPARE_OP               <
          884_886  POP_JUMP_IF_FALSE   924  'to 924'

 L. 537       888  LOAD_GLOBAL              vis_msg
              890  LOAD_ATTR                print
              892  LOAD_STR                 'ERROR in UpdateMlMlp: No name specified for MLP network'
              894  LOAD_STR                 'error'
              896  LOAD_CONST               ('type',)
              898  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              900  POP_TOP          

 L. 538       902  LOAD_GLOBAL              QtWidgets
              904  LOAD_ATTR                QMessageBox
              906  LOAD_METHOD              critical
              908  LOAD_FAST                'self'
              910  LOAD_ATTR                msgbox

 L. 539       912  LOAD_STR                 'Update MLP'

 L. 540       914  LOAD_STR                 'No name specified for MLP network'
              916  CALL_METHOD_3         3  '3 positional arguments'
              918  POP_TOP          

 L. 541       920  LOAD_CONST               None
              922  RETURN_VALUE     
            924_0  COME_FROM           884  '884'

 L. 542       924  LOAD_GLOBAL              os
              926  LOAD_ATTR                path
              928  LOAD_METHOD              dirname
              930  LOAD_FAST                'self'
              932  LOAD_ATTR                ldtsave
              934  LOAD_METHOD              text
              936  CALL_METHOD_0         0  '0 positional arguments'
              938  CALL_METHOD_1         1  '1 positional argument'
              940  STORE_FAST               '_savepath'

 L. 543       942  LOAD_GLOBAL              os
              944  LOAD_ATTR                path
              946  LOAD_METHOD              splitext
              948  LOAD_GLOBAL              os
              950  LOAD_ATTR                path
              952  LOAD_METHOD              basename
              954  LOAD_FAST                'self'
              956  LOAD_ATTR                ldtsave
              958  LOAD_METHOD              text
              960  CALL_METHOD_0         0  '0 positional arguments'
              962  CALL_METHOD_1         1  '1 positional argument'
              964  CALL_METHOD_1         1  '1 positional argument'
              966  LOAD_CONST               0
              968  BINARY_SUBSCR    
              970  STORE_FAST               '_savename'

 L. 545       972  LOAD_GLOBAL              int
              974  LOAD_FAST                '_patch_depth'
              976  LOAD_CONST               2
              978  BINARY_TRUE_DIVIDE
              980  CALL_FUNCTION_1       1  '1 positional argument'
              982  STORE_FAST               '_wdinl'

 L. 546       984  LOAD_GLOBAL              int
              986  LOAD_FAST                '_patch_width'
              988  LOAD_CONST               2
              990  BINARY_TRUE_DIVIDE
              992  CALL_FUNCTION_1       1  '1 positional argument'
              994  STORE_FAST               '_wdxl'

 L. 547       996  LOAD_GLOBAL              int
              998  LOAD_FAST                '_patch_height'
             1000  LOAD_CONST               2
             1002  BINARY_TRUE_DIVIDE
             1004  CALL_FUNCTION_1       1  '1 positional argument'
             1006  STORE_FAST               '_wdz'

 L. 549      1008  LOAD_FAST                'self'
             1010  LOAD_ATTR                survinfo
             1012  STORE_FAST               '_seisinfo'

 L. 551      1014  LOAD_GLOBAL              print
             1016  LOAD_STR                 'UpdateMlMlp: Step 1 - Get training samples:'
             1018  CALL_FUNCTION_1       1  '1 positional argument'
             1020  POP_TOP          

 L. 552      1022  LOAD_FAST                'self'
             1024  LOAD_ATTR                traindataconfig
             1026  LOAD_STR                 'TrainPointSet'
             1028  BINARY_SUBSCR    
             1030  STORE_FAST               '_trainpoint'

 L. 553      1032  LOAD_GLOBAL              np
             1034  LOAD_METHOD              zeros
             1036  LOAD_CONST               0
             1038  LOAD_CONST               3
             1040  BUILD_LIST_2          2 
             1042  CALL_METHOD_1         1  '1 positional argument'
             1044  STORE_FAST               '_traindata'

 L. 554      1046  SETUP_LOOP         1122  'to 1122'
             1048  LOAD_FAST                '_trainpoint'
             1050  GET_ITER         
           1052_0  COME_FROM          1070  '1070'
             1052  FOR_ITER           1120  'to 1120'
             1054  STORE_FAST               '_p'

 L. 555      1056  LOAD_GLOBAL              point_ays
             1058  LOAD_METHOD              checkPoint
             1060  LOAD_FAST                'self'
             1062  LOAD_ATTR                pointsetdata
             1064  LOAD_FAST                '_p'
             1066  BINARY_SUBSCR    
             1068  CALL_METHOD_1         1  '1 positional argument'
         1070_1072  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 556      1074  LOAD_GLOBAL              basic_mdt
             1076  LOAD_METHOD              exportMatDict
             1078  LOAD_FAST                'self'
             1080  LOAD_ATTR                pointsetdata
             1082  LOAD_FAST                '_p'
             1084  BINARY_SUBSCR    
             1086  LOAD_STR                 'Inline'
             1088  LOAD_STR                 'Crossline'
             1090  LOAD_STR                 'Z'
             1092  BUILD_LIST_3          3 
             1094  CALL_METHOD_2         2  '2 positional arguments'
             1096  STORE_FAST               '_pt'

 L. 557      1098  LOAD_GLOBAL              np
             1100  LOAD_ATTR                concatenate
             1102  LOAD_FAST                '_traindata'
             1104  LOAD_FAST                '_pt'
             1106  BUILD_TUPLE_2         2 
             1108  LOAD_CONST               0
             1110  LOAD_CONST               ('axis',)
             1112  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1114  STORE_FAST               '_traindata'
         1116_1118  JUMP_BACK          1052  'to 1052'
             1120  POP_BLOCK        
           1122_0  COME_FROM_LOOP     1046  '1046'

 L. 558      1122  LOAD_GLOBAL              seis_ays
             1124  LOAD_ATTR                removeOutofSurveySample
             1126  LOAD_FAST                '_traindata'

 L. 559      1128  LOAD_FAST                '_seisinfo'
             1130  LOAD_STR                 'ILStart'
             1132  BINARY_SUBSCR    
             1134  LOAD_FAST                '_wdinl'
             1136  LOAD_FAST                '_seisinfo'
             1138  LOAD_STR                 'ILStep'
             1140  BINARY_SUBSCR    
             1142  BINARY_MULTIPLY  
             1144  BINARY_ADD       

 L. 560      1146  LOAD_FAST                '_seisinfo'
             1148  LOAD_STR                 'ILEnd'
             1150  BINARY_SUBSCR    
             1152  LOAD_FAST                '_wdinl'
             1154  LOAD_FAST                '_seisinfo'
             1156  LOAD_STR                 'ILStep'
             1158  BINARY_SUBSCR    
             1160  BINARY_MULTIPLY  
             1162  BINARY_SUBTRACT  

 L. 561      1164  LOAD_FAST                '_seisinfo'
             1166  LOAD_STR                 'XLStart'
             1168  BINARY_SUBSCR    
             1170  LOAD_FAST                '_wdxl'
             1172  LOAD_FAST                '_seisinfo'
             1174  LOAD_STR                 'XLStep'
             1176  BINARY_SUBSCR    
             1178  BINARY_MULTIPLY  
             1180  BINARY_ADD       

 L. 562      1182  LOAD_FAST                '_seisinfo'
             1184  LOAD_STR                 'XLEnd'
             1186  BINARY_SUBSCR    
             1188  LOAD_FAST                '_wdxl'
             1190  LOAD_FAST                '_seisinfo'
             1192  LOAD_STR                 'XLStep'
             1194  BINARY_SUBSCR    
             1196  BINARY_MULTIPLY  
             1198  BINARY_SUBTRACT  

 L. 563      1200  LOAD_FAST                '_seisinfo'
             1202  LOAD_STR                 'ZStart'
             1204  BINARY_SUBSCR    
             1206  LOAD_FAST                '_wdz'
             1208  LOAD_FAST                '_seisinfo'
             1210  LOAD_STR                 'ZStep'
             1212  BINARY_SUBSCR    
             1214  BINARY_MULTIPLY  
             1216  BINARY_ADD       

 L. 564      1218  LOAD_FAST                '_seisinfo'
             1220  LOAD_STR                 'ZEnd'
             1222  BINARY_SUBSCR    
             1224  LOAD_FAST                '_wdz'
             1226  LOAD_FAST                '_seisinfo'
             1228  LOAD_STR                 'ZStep'
             1230  BINARY_SUBSCR    
             1232  BINARY_MULTIPLY  
             1234  BINARY_SUBTRACT  
             1236  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1238  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1240  STORE_FAST               '_traindata'

 L. 567      1242  LOAD_GLOBAL              np
             1244  LOAD_METHOD              shape
             1246  LOAD_FAST                '_traindata'
             1248  CALL_METHOD_1         1  '1 positional argument'
             1250  LOAD_CONST               0
             1252  BINARY_SUBSCR    
             1254  LOAD_CONST               0
             1256  COMPARE_OP               <=
         1258_1260  POP_JUMP_IF_FALSE  1298  'to 1298'

 L. 568      1262  LOAD_GLOBAL              vis_msg
             1264  LOAD_ATTR                print
             1266  LOAD_STR                 'ERROR in UpdateMlp: No training sample found'
             1268  LOAD_STR                 'error'
             1270  LOAD_CONST               ('type',)
             1272  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1274  POP_TOP          

 L. 569      1276  LOAD_GLOBAL              QtWidgets
             1278  LOAD_ATTR                QMessageBox
             1280  LOAD_METHOD              critical
             1282  LOAD_FAST                'self'
             1284  LOAD_ATTR                msgbox

 L. 570      1286  LOAD_STR                 'Update MLP'

 L. 571      1288  LOAD_STR                 'No training sample found'
             1290  CALL_METHOD_3         3  '3 positional arguments'
             1292  POP_TOP          

 L. 572      1294  LOAD_CONST               None
             1296  RETURN_VALUE     
           1298_0  COME_FROM          1258  '1258'

 L. 575      1298  LOAD_GLOBAL              print
             1300  LOAD_STR                 'UpdateMlMlp: Step 2 - Retrieve features'
             1302  CALL_FUNCTION_1       1  '1 positional argument'
             1304  POP_TOP          

 L. 576      1306  BUILD_MAP_0           0 
             1308  STORE_FAST               '_traindict'

 L. 577      1310  SETUP_LOOP         1382  'to 1382'
             1312  LOAD_FAST                '_features'
             1314  GET_ITER         
             1316  FOR_ITER           1380  'to 1380'
             1318  STORE_FAST               'f'

 L. 578      1320  LOAD_FAST                'self'
             1322  LOAD_ATTR                seisdata
             1324  LOAD_FAST                'f'
             1326  BINARY_SUBSCR    
             1328  STORE_FAST               '_seisdata'

 L. 579      1330  LOAD_GLOBAL              seis_ays
             1332  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1334  LOAD_FAST                '_seisdata'
             1336  LOAD_FAST                '_traindata'
             1338  LOAD_FAST                'self'
             1340  LOAD_ATTR                survinfo

 L. 580      1342  LOAD_FAST                '_wdinl'
             1344  LOAD_FAST                '_wdxl'
             1346  LOAD_FAST                '_wdz'

 L. 581      1348  LOAD_CONST               False
             1350  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1352  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1354  LOAD_CONST               None
             1356  LOAD_CONST               None
             1358  BUILD_SLICE_2         2 
             1360  LOAD_CONST               3
             1362  LOAD_CONST               None
             1364  BUILD_SLICE_2         2 
             1366  BUILD_TUPLE_2         2 
             1368  BINARY_SUBSCR    
             1370  LOAD_FAST                '_traindict'
             1372  LOAD_FAST                'f'
             1374  STORE_SUBSCR     
         1376_1378  JUMP_BACK          1316  'to 1316'
             1380  POP_BLOCK        
           1382_0  COME_FROM_LOOP     1310  '1310'

 L. 582      1382  LOAD_FAST                '_target'
             1384  LOAD_FAST                '_features'
             1386  COMPARE_OP               not-in
         1388_1390  POP_JUMP_IF_FALSE  1442  'to 1442'

 L. 583      1392  LOAD_FAST                'self'
             1394  LOAD_ATTR                seisdata
             1396  LOAD_FAST                '_target'
             1398  BINARY_SUBSCR    
             1400  STORE_FAST               '_seisdata'

 L. 584      1402  LOAD_GLOBAL              seis_ays
             1404  LOAD_ATTR                retrieveSeisSampleFrom3DMat
             1406  LOAD_FAST                '_seisdata'
             1408  LOAD_FAST                '_traindata'
             1410  LOAD_FAST                'self'
             1412  LOAD_ATTR                survinfo

 L. 585      1414  LOAD_CONST               False
             1416  LOAD_CONST               ('seisinfo', 'verbose')
             1418  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1420  LOAD_CONST               None
             1422  LOAD_CONST               None
             1424  BUILD_SLICE_2         2 
             1426  LOAD_CONST               3
             1428  LOAD_CONST               None
             1430  BUILD_SLICE_2         2 
             1432  BUILD_TUPLE_2         2 
             1434  BINARY_SUBSCR    
             1436  LOAD_FAST                '_traindict'
             1438  LOAD_FAST                '_target'
             1440  STORE_SUBSCR     
           1442_0  COME_FROM          1388  '1388'

 L. 587      1442  LOAD_FAST                'self'
             1444  LOAD_ATTR                traindataconfig
             1446  LOAD_STR                 'RemoveInvariantFeature_Checked'
             1448  BINARY_SUBSCR    
         1450_1452  POP_JUMP_IF_FALSE  1528  'to 1528'

 L. 588      1454  SETUP_LOOP         1528  'to 1528'
             1456  LOAD_FAST                '_features'
             1458  GET_ITER         
           1460_0  COME_FROM          1488  '1488'
             1460  FOR_ITER           1526  'to 1526'
             1462  STORE_FAST               'f'

 L. 589      1464  LOAD_GLOBAL              ml_aug
             1466  LOAD_METHOD              removeInvariantFeature
             1468  LOAD_FAST                '_traindict'
             1470  LOAD_FAST                'f'
             1472  CALL_METHOD_2         2  '2 positional arguments'
             1474  STORE_FAST               '_traindict'

 L. 590      1476  LOAD_GLOBAL              basic_mdt
             1478  LOAD_METHOD              maxDictConstantRow
             1480  LOAD_FAST                '_traindict'
             1482  CALL_METHOD_1         1  '1 positional argument'
             1484  LOAD_CONST               0
             1486  COMPARE_OP               <=
         1488_1490  POP_JUMP_IF_FALSE  1460  'to 1460'

 L. 591      1492  LOAD_GLOBAL              print
             1494  LOAD_STR                 'UpdateMlMlp: No training sample found'
             1496  CALL_FUNCTION_1       1  '1 positional argument'
             1498  POP_TOP          

 L. 592      1500  LOAD_GLOBAL              QtWidgets
             1502  LOAD_ATTR                QMessageBox
             1504  LOAD_METHOD              critical
             1506  LOAD_FAST                'self'
             1508  LOAD_ATTR                msgbox

 L. 593      1510  LOAD_STR                 'Update MLP'

 L. 594      1512  LOAD_STR                 'No training sample found'
             1514  CALL_METHOD_3         3  '3 positional arguments'
             1516  POP_TOP          

 L. 595      1518  LOAD_CONST               None
             1520  RETURN_VALUE     
         1522_1524  JUMP_BACK          1460  'to 1460'
             1526  POP_BLOCK        
           1528_0  COME_FROM_LOOP     1454  '1454'
           1528_1  COME_FROM          1450  '1450'

 L. 597      1528  LOAD_GLOBAL              np
             1530  LOAD_METHOD              round
             1532  LOAD_FAST                '_traindict'
             1534  LOAD_FAST                '_target'
             1536  BINARY_SUBSCR    
             1538  CALL_METHOD_1         1  '1 positional argument'
             1540  LOAD_METHOD              astype
             1542  LOAD_GLOBAL              int
             1544  CALL_METHOD_1         1  '1 positional argument'
             1546  LOAD_FAST                '_traindict'
             1548  LOAD_FAST                '_target'
             1550  STORE_SUBSCR     

 L. 599      1552  LOAD_GLOBAL              print
             1554  LOAD_STR                 'UpdateMlp: A total of %d valid training samples'
             1556  LOAD_GLOBAL              basic_mdt
             1558  LOAD_METHOD              maxDictConstantRow
             1560  LOAD_FAST                '_traindict'
             1562  CALL_METHOD_1         1  '1 positional argument'
             1564  BINARY_MODULO    
             1566  CALL_FUNCTION_1       1  '1 positional argument'
             1568  POP_TOP          

 L. 601      1570  LOAD_GLOBAL              print
             1572  LOAD_STR                 'UpdateMlMlp: Step 3 - Balance labels'
             1574  CALL_FUNCTION_1       1  '1 positional argument'
             1576  POP_TOP          

 L. 602      1578  LOAD_FAST                'self'
             1580  LOAD_ATTR                traindataconfig
             1582  LOAD_STR                 'BalanceTarget_Checked'
             1584  BINARY_SUBSCR    
         1586_1588  POP_JUMP_IF_FALSE  1630  'to 1630'

 L. 603      1590  LOAD_GLOBAL              ml_aug
             1592  LOAD_METHOD              balanceLabelbyExtension
             1594  LOAD_FAST                '_traindict'
             1596  LOAD_FAST                '_target'
             1598  CALL_METHOD_2         2  '2 positional arguments'
             1600  STORE_FAST               '_traindict'

 L. 604      1602  LOAD_GLOBAL              print
             1604  LOAD_STR                 'UpdateMlMlp: A total of %d training samples after balance'
             1606  LOAD_GLOBAL              np
             1608  LOAD_METHOD              shape
             1610  LOAD_FAST                '_traindict'
             1612  LOAD_FAST                '_target'
             1614  BINARY_SUBSCR    
             1616  CALL_METHOD_1         1  '1 positional argument'
             1618  LOAD_CONST               0
             1620  BINARY_SUBSCR    
             1622  BINARY_MODULO    
             1624  CALL_FUNCTION_1       1  '1 positional argument'
             1626  POP_TOP          
             1628  JUMP_FORWARD       1638  'to 1638'
           1630_0  COME_FROM          1586  '1586'

 L. 606      1630  LOAD_GLOBAL              print
             1632  LOAD_STR                 'UpdateMlMlp: No balance applied'
             1634  CALL_FUNCTION_1       1  '1 positional argument'
             1636  POP_TOP          
           1638_0  COME_FROM          1628  '1628'

 L. 608      1638  LOAD_GLOBAL              print
             1640  LOAD_STR                 'TrainMlMlp: Step 4 - Start training'
             1642  CALL_FUNCTION_1       1  '1 positional argument'
             1644  POP_TOP          

 L. 610      1646  LOAD_GLOBAL              QtWidgets
             1648  LOAD_METHOD              QProgressDialog
             1650  CALL_METHOD_0         0  '0 positional arguments'
             1652  STORE_FAST               '_pgsdlg'

 L. 611      1654  LOAD_GLOBAL              QtGui
             1656  LOAD_METHOD              QIcon
             1658  CALL_METHOD_0         0  '0 positional arguments'
             1660  STORE_FAST               'icon'

 L. 612      1662  LOAD_FAST                'icon'
             1664  LOAD_METHOD              addPixmap
             1666  LOAD_GLOBAL              QtGui
             1668  LOAD_METHOD              QPixmap
             1670  LOAD_GLOBAL              os
             1672  LOAD_ATTR                path
             1674  LOAD_METHOD              join
             1676  LOAD_FAST                'self'
             1678  LOAD_ATTR                iconpath
             1680  LOAD_STR                 'icons/new.png'
             1682  CALL_METHOD_2         2  '2 positional arguments'
             1684  CALL_METHOD_1         1  '1 positional argument'

 L. 613      1686  LOAD_GLOBAL              QtGui
             1688  LOAD_ATTR                QIcon
             1690  LOAD_ATTR                Normal
             1692  LOAD_GLOBAL              QtGui
             1694  LOAD_ATTR                QIcon
             1696  LOAD_ATTR                Off
             1698  CALL_METHOD_3         3  '3 positional arguments'
             1700  POP_TOP          

 L. 614      1702  LOAD_FAST                '_pgsdlg'
             1704  LOAD_METHOD              setWindowIcon
             1706  LOAD_FAST                'icon'
             1708  CALL_METHOD_1         1  '1 positional argument'
             1710  POP_TOP          

 L. 615      1712  LOAD_FAST                '_pgsdlg'
             1714  LOAD_METHOD              setWindowTitle
             1716  LOAD_STR                 'Train MLP'
             1718  CALL_METHOD_1         1  '1 positional argument'
             1720  POP_TOP          

 L. 616      1722  LOAD_FAST                '_pgsdlg'
             1724  LOAD_METHOD              setCancelButton
             1726  LOAD_CONST               None
             1728  CALL_METHOD_1         1  '1 positional argument'
             1730  POP_TOP          

 L. 617      1732  LOAD_FAST                '_pgsdlg'
             1734  LOAD_METHOD              setWindowFlags
             1736  LOAD_GLOBAL              QtCore
             1738  LOAD_ATTR                Qt
             1740  LOAD_ATTR                WindowStaysOnTopHint
             1742  CALL_METHOD_1         1  '1 positional argument'
             1744  POP_TOP          

 L. 618      1746  LOAD_FAST                '_pgsdlg'
             1748  LOAD_METHOD              forceShow
             1750  CALL_METHOD_0         0  '0 positional arguments'
             1752  POP_TOP          

 L. 619      1754  LOAD_FAST                '_pgsdlg'
             1756  LOAD_METHOD              setFixedWidth
             1758  LOAD_CONST               400
             1760  CALL_METHOD_1         1  '1 positional argument'
             1762  POP_TOP          

 L. 620      1764  LOAD_GLOBAL              ml_fnn
             1766  LOAD_ATTR                updateFNNClassifier
             1768  LOAD_FAST                '_traindict'

 L. 621      1770  LOAD_FAST                'self'
             1772  LOAD_ATTR                modelpath

 L. 622      1774  LOAD_FAST                'self'
             1776  LOAD_ATTR                modelname

 L. 623      1778  LOAD_FAST                '_nepoch'
             1780  LOAD_FAST                '_batchsize'

 L. 624      1782  LOAD_FAST                '_dropout_prob_fclayer'

 L. 625      1784  LOAD_FAST                '_learning_rate'

 L. 626      1786  LOAD_CONST               True

 L. 627      1788  LOAD_FAST                '_savepath'
             1790  LOAD_FAST                '_savename'

 L. 628      1792  LOAD_FAST                '_pgsdlg'
             1794  LOAD_CONST               ('fnnpath', 'fnnname', 'nepoch', 'batchsize', 'dropoutprobfclayer', 'learningrate', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             1796  CALL_FUNCTION_KW_11    11  '11 total positional and keyword args'
             1798  STORE_FAST               '_fnnlog'

 L. 630      1800  LOAD_GLOBAL              QtWidgets
             1802  LOAD_ATTR                QMessageBox
             1804  LOAD_METHOD              information
             1806  LOAD_FAST                'self'
             1808  LOAD_ATTR                msgbox

 L. 631      1810  LOAD_STR                 'Update MLP'

 L. 632      1812  LOAD_STR                 'MLP trained successfully'
             1814  CALL_METHOD_3         3  '3 positional arguments'
             1816  POP_TOP          

 L. 634      1818  LOAD_GLOBAL              QtWidgets
             1820  LOAD_ATTR                QMessageBox
             1822  LOAD_METHOD              question
             1824  LOAD_FAST                'self'
             1826  LOAD_ATTR                msgbox
             1828  LOAD_STR                 'Update MLP'
             1830  LOAD_STR                 'View learning matrix?'

 L. 635      1832  LOAD_GLOBAL              QtWidgets
             1834  LOAD_ATTR                QMessageBox
             1836  LOAD_ATTR                Yes
             1838  LOAD_GLOBAL              QtWidgets
             1840  LOAD_ATTR                QMessageBox
             1842  LOAD_ATTR                No
             1844  BINARY_OR        

 L. 636      1846  LOAD_GLOBAL              QtWidgets
             1848  LOAD_ATTR                QMessageBox
             1850  LOAD_ATTR                Yes
             1852  CALL_METHOD_5         5  '5 positional arguments'
             1854  STORE_FAST               'reply'

 L. 638      1856  LOAD_FAST                'reply'
             1858  LOAD_GLOBAL              QtWidgets
             1860  LOAD_ATTR                QMessageBox
             1862  LOAD_ATTR                Yes
             1864  COMPARE_OP               ==
         1866_1868  POP_JUMP_IF_FALSE  1936  'to 1936'

 L. 639      1870  LOAD_GLOBAL              QtWidgets
             1872  LOAD_METHOD              QDialog
             1874  CALL_METHOD_0         0  '0 positional arguments'
             1876  STORE_FAST               '_viewmllearnmat'

 L. 640      1878  LOAD_GLOBAL              gui_viewmllearnmat
             1880  CALL_FUNCTION_0       0  '0 positional arguments'
             1882  STORE_FAST               '_gui'

 L. 641      1884  LOAD_FAST                '_fnnlog'
             1886  LOAD_STR                 'learning_curve'
             1888  BINARY_SUBSCR    
             1890  LOAD_FAST                '_gui'
             1892  STORE_ATTR               learnmat

 L. 642      1894  LOAD_FAST                'self'
             1896  LOAD_ATTR                linestyle
             1898  LOAD_FAST                '_gui'
             1900  STORE_ATTR               linestyle

 L. 643      1902  LOAD_FAST                'self'
             1904  LOAD_ATTR                fontstyle
             1906  LOAD_FAST                '_gui'
             1908  STORE_ATTR               fontstyle

 L. 644      1910  LOAD_FAST                '_gui'
             1912  LOAD_METHOD              setupGUI
             1914  LOAD_FAST                '_viewmllearnmat'
             1916  CALL_METHOD_1         1  '1 positional argument'
             1918  POP_TOP          

 L. 645      1920  LOAD_FAST                '_viewmllearnmat'
             1922  LOAD_METHOD              exec
             1924  CALL_METHOD_0         0  '0 positional arguments'
             1926  POP_TOP          

 L. 646      1928  LOAD_FAST                '_viewmllearnmat'
             1930  LOAD_METHOD              show
             1932  CALL_METHOD_0         0  '0 positional arguments'
             1934  POP_TOP          
           1936_0  COME_FROM          1866  '1866'

Parse error at or near `POP_TOP' instruction at offset 1934

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