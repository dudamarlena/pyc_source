# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainmlmlp.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 30700 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.pointset.analysis as point_ays
import cognitivegeo.src.ml.augmentation as ml_aug
import cognitivegeo.src.ml.fnnclassifier as ml_fnn
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
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

    def clickBtnTrainMlMlp--- This code section failed: ---

 L. 354         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 356         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 357        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMlMlp: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 358        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 359        50  LOAD_STR                 'Train MLP'

 L. 360        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 361        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 363        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtpatchheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_patch_height'

 L. 364        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtpatchwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_patch_width'

 L. 365        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtpatchdepth
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_patch_depth'

 L. 366       110  LOAD_FAST                '_patch_height'
              112  LOAD_CONST               False
              114  COMPARE_OP               is
              116  POP_JUMP_IF_TRUE    158  'to 158'
              118  LOAD_FAST                '_patch_width'
              120  LOAD_CONST               False
              122  COMPARE_OP               is
              124  POP_JUMP_IF_TRUE    158  'to 158'
              126  LOAD_FAST                '_patch_depth'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'

 L. 367       134  LOAD_FAST                '_patch_height'
              136  LOAD_CONST               1
              138  COMPARE_OP               <
              140  POP_JUMP_IF_TRUE    158  'to 158'
              142  LOAD_FAST                '_patch_width'
              144  LOAD_CONST               1
              146  COMPARE_OP               <
              148  POP_JUMP_IF_TRUE    158  'to 158'
              150  LOAD_FAST                '_patch_depth'
              152  LOAD_CONST               1
              154  COMPARE_OP               <
              156  POP_JUMP_IF_FALSE   194  'to 194'
            158_0  COME_FROM           148  '148'
            158_1  COME_FROM           140  '140'
            158_2  COME_FROM           132  '132'
            158_3  COME_FROM           124  '124'
            158_4  COME_FROM           116  '116'

 L. 368       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMlMlp: Non-positive patch size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 369       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 370       182  LOAD_STR                 'Train MLP'

 L. 371       184  LOAD_STR                 'Non-positive patch size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 372       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 374       194  LOAD_CONST               2
              196  LOAD_GLOBAL              int
              198  LOAD_FAST                '_patch_height'
              200  LOAD_CONST               2
              202  BINARY_TRUE_DIVIDE
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  BINARY_MULTIPLY  
              208  LOAD_CONST               1
              210  BINARY_ADD       
              212  STORE_FAST               '_patch_height'

 L. 375       214  LOAD_CONST               2
              216  LOAD_GLOBAL              int
              218  LOAD_FAST                '_patch_width'
              220  LOAD_CONST               2
              222  BINARY_TRUE_DIVIDE
              224  CALL_FUNCTION_1       1  '1 positional argument'
              226  BINARY_MULTIPLY  
              228  LOAD_CONST               1
              230  BINARY_ADD       
              232  STORE_FAST               '_patch_width'

 L. 376       234  LOAD_CONST               2
              236  LOAD_GLOBAL              int
              238  LOAD_FAST                '_patch_depth'
              240  LOAD_CONST               2
              242  BINARY_TRUE_DIVIDE
              244  CALL_FUNCTION_1       1  '1 positional argument'
              246  BINARY_MULTIPLY  
              248  LOAD_CONST               1
              250  BINARY_ADD       
              252  STORE_FAST               '_patch_depth'

 L. 378       254  LOAD_DEREF               'self'
              256  LOAD_ATTR                lwgfeature
              258  LOAD_METHOD              selectedItems
              260  CALL_METHOD_0         0  '0 positional arguments'
              262  STORE_FAST               '_features'

 L. 379       264  LOAD_LISTCOMP            '<code_object <listcomp>>'
              266  LOAD_STR                 'trainmlmlp.clickBtnTrainMlMlp.<locals>.<listcomp>'
              268  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              270  LOAD_FAST                '_features'
              272  GET_ITER         
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  STORE_FAST               '_features'

 L. 380       278  LOAD_DEREF               'self'
              280  LOAD_ATTR                featurelist
              282  LOAD_DEREF               'self'
              284  LOAD_ATTR                cbbtarget
              286  LOAD_METHOD              currentIndex
              288  CALL_METHOD_0         0  '0 positional arguments'
              290  BINARY_SUBSCR    
              292  STORE_FAST               '_target'

 L. 382       294  LOAD_GLOBAL              basic_data
              296  LOAD_METHOD              str2int
              298  LOAD_DEREF               'self'
              300  LOAD_ATTR                ldtnlayer
              302  LOAD_METHOD              text
              304  CALL_METHOD_0         0  '0 positional arguments'
              306  CALL_METHOD_1         1  '1 positional argument'
              308  STORE_FAST               '_nlayer'

 L. 383       310  LOAD_CLOSURE             'self'
              312  BUILD_TUPLE_1         1 
              314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainmlmlp.clickBtnTrainMlMlp.<locals>.<listcomp>'
              318  MAKE_FUNCTION_8          'closure'
              320  LOAD_GLOBAL              range
              322  LOAD_FAST                '_nlayer'
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  GET_ITER         
              328  CALL_FUNCTION_1       1  '1 positional argument'
              330  STORE_FAST               '_nneuron'

 L. 384       332  LOAD_GLOBAL              basic_data
              334  LOAD_METHOD              str2int
              336  LOAD_DEREF               'self'
              338  LOAD_ATTR                ldtnepoch
              340  LOAD_METHOD              text
              342  CALL_METHOD_0         0  '0 positional arguments'
              344  CALL_METHOD_1         1  '1 positional argument'
              346  STORE_FAST               '_nepoch'

 L. 385       348  LOAD_GLOBAL              basic_data
              350  LOAD_METHOD              str2int
              352  LOAD_DEREF               'self'
              354  LOAD_ATTR                ldtbatchsize
              356  LOAD_METHOD              text
              358  CALL_METHOD_0         0  '0 positional arguments'
              360  CALL_METHOD_1         1  '1 positional argument'
              362  STORE_FAST               '_batchsize'

 L. 386       364  LOAD_GLOBAL              basic_data
              366  LOAD_METHOD              str2float
              368  LOAD_DEREF               'self'
              370  LOAD_ATTR                ldtlearnrate
              372  LOAD_METHOD              text
              374  CALL_METHOD_0         0  '0 positional arguments'
              376  CALL_METHOD_1         1  '1 positional argument'
              378  STORE_FAST               '_learning_rate'

 L. 387       380  LOAD_GLOBAL              basic_data
              382  LOAD_METHOD              str2float
              384  LOAD_DEREF               'self'
              386  LOAD_ATTR                ldtfcdropout
              388  LOAD_METHOD              text
              390  CALL_METHOD_0         0  '0 positional arguments'
              392  CALL_METHOD_1         1  '1 positional argument'
              394  STORE_FAST               '_dropout_prob_fclayer'

 L. 388       396  LOAD_FAST                '_nlayer'
              398  LOAD_CONST               False
              400  COMPARE_OP               is
          402_404  POP_JUMP_IF_TRUE    416  'to 416'
              406  LOAD_FAST                '_nlayer'
              408  LOAD_CONST               0
              410  COMPARE_OP               <=
          412_414  POP_JUMP_IF_FALSE   452  'to 452'
            416_0  COME_FROM           402  '402'

 L. 389       416  LOAD_GLOBAL              vis_msg
              418  LOAD_ATTR                print
              420  LOAD_STR                 'ERROR in TrainMlMlp: Non-positive layer number'
              422  LOAD_STR                 'error'
              424  LOAD_CONST               ('type',)
              426  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              428  POP_TOP          

 L. 390       430  LOAD_GLOBAL              QtWidgets
              432  LOAD_ATTR                QMessageBox
              434  LOAD_METHOD              critical
              436  LOAD_DEREF               'self'
              438  LOAD_ATTR                msgbox

 L. 391       440  LOAD_STR                 'Train MLP'

 L. 392       442  LOAD_STR                 'Non-positive layer number'
              444  CALL_METHOD_3         3  '3 positional arguments'
              446  POP_TOP          

 L. 393       448  LOAD_CONST               None
              450  RETURN_VALUE     
            452_0  COME_FROM           412  '412'

 L. 394       452  SETUP_LOOP          524  'to 524'
              454  LOAD_FAST                '_nneuron'
              456  GET_ITER         
            458_0  COME_FROM           478  '478'
              458  FOR_ITER            522  'to 522'
              460  STORE_FAST               '_i'

 L. 395       462  LOAD_FAST                '_i'
              464  LOAD_CONST               False
              466  COMPARE_OP               is
          468_470  POP_JUMP_IF_TRUE    482  'to 482'
              472  LOAD_FAST                '_i'
              474  LOAD_CONST               0
              476  COMPARE_OP               <=
          478_480  POP_JUMP_IF_FALSE   458  'to 458'
            482_0  COME_FROM           468  '468'

 L. 396       482  LOAD_GLOBAL              vis_msg
              484  LOAD_ATTR                print
              486  LOAD_STR                 'ERROR in TrainMlMlp: Non-positive neuron number'
              488  LOAD_STR                 'error'
              490  LOAD_CONST               ('type',)
              492  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              494  POP_TOP          

 L. 397       496  LOAD_GLOBAL              QtWidgets
              498  LOAD_ATTR                QMessageBox
              500  LOAD_METHOD              critical
              502  LOAD_DEREF               'self'
              504  LOAD_ATTR                msgbox

 L. 398       506  LOAD_STR                 'Train MLP'

 L. 399       508  LOAD_STR                 'Non-positive neuron number'
              510  CALL_METHOD_3         3  '3 positional arguments'
              512  POP_TOP          

 L. 400       514  LOAD_CONST               None
              516  RETURN_VALUE     
          518_520  JUMP_BACK           458  'to 458'
              522  POP_BLOCK        
            524_0  COME_FROM_LOOP      452  '452'

 L. 401       524  LOAD_FAST                '_nepoch'
              526  LOAD_CONST               False
              528  COMPARE_OP               is
          530_532  POP_JUMP_IF_TRUE    544  'to 544'
              534  LOAD_FAST                '_nepoch'
              536  LOAD_CONST               0
              538  COMPARE_OP               <=
          540_542  POP_JUMP_IF_FALSE   580  'to 580'
            544_0  COME_FROM           530  '530'

 L. 402       544  LOAD_GLOBAL              vis_msg
              546  LOAD_ATTR                print
              548  LOAD_STR                 'ERROR in TrainMlMlp: Non-positive nepoch'
              550  LOAD_STR                 'error'
              552  LOAD_CONST               ('type',)
              554  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              556  POP_TOP          

 L. 403       558  LOAD_GLOBAL              QtWidgets
              560  LOAD_ATTR                QMessageBox
              562  LOAD_METHOD              critical
              564  LOAD_DEREF               'self'
              566  LOAD_ATTR                msgbox

 L. 404       568  LOAD_STR                 'Train MLP'

 L. 405       570  LOAD_STR                 'Non-positive nepoch'
              572  CALL_METHOD_3         3  '3 positional arguments'
              574  POP_TOP          

 L. 406       576  LOAD_CONST               None
              578  RETURN_VALUE     
            580_0  COME_FROM           540  '540'

 L. 407       580  LOAD_FAST                '_batchsize'
              582  LOAD_CONST               False
              584  COMPARE_OP               is
          586_588  POP_JUMP_IF_TRUE    600  'to 600'
              590  LOAD_FAST                '_batchsize'
              592  LOAD_CONST               0
              594  COMPARE_OP               <=
          596_598  POP_JUMP_IF_FALSE   636  'to 636'
            600_0  COME_FROM           586  '586'

 L. 408       600  LOAD_GLOBAL              vis_msg
              602  LOAD_ATTR                print
              604  LOAD_STR                 'ERROR in TrainMlMlp: Non-positive batch size'
              606  LOAD_STR                 'error'
              608  LOAD_CONST               ('type',)
              610  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              612  POP_TOP          

 L. 409       614  LOAD_GLOBAL              QtWidgets
              616  LOAD_ATTR                QMessageBox
              618  LOAD_METHOD              critical
              620  LOAD_DEREF               'self'
              622  LOAD_ATTR                msgbox

 L. 410       624  LOAD_STR                 'Train MLP'

 L. 411       626  LOAD_STR                 'Non-positive batch size'
              628  CALL_METHOD_3         3  '3 positional arguments'
              630  POP_TOP          

 L. 412       632  LOAD_CONST               None
              634  RETURN_VALUE     
            636_0  COME_FROM           596  '596'

 L. 413       636  LOAD_FAST                '_learning_rate'
              638  LOAD_CONST               False
              640  COMPARE_OP               is
          642_644  POP_JUMP_IF_TRUE    656  'to 656'
              646  LOAD_FAST                '_learning_rate'
              648  LOAD_CONST               0
              650  COMPARE_OP               <=
          652_654  POP_JUMP_IF_FALSE   692  'to 692'
            656_0  COME_FROM           642  '642'

 L. 414       656  LOAD_GLOBAL              vis_msg
              658  LOAD_ATTR                print
              660  LOAD_STR                 'ERROR in TrainMlMlp: Non-positive learning rate'
              662  LOAD_STR                 'error'
              664  LOAD_CONST               ('type',)
              666  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              668  POP_TOP          

 L. 415       670  LOAD_GLOBAL              QtWidgets
              672  LOAD_ATTR                QMessageBox
              674  LOAD_METHOD              critical
              676  LOAD_DEREF               'self'
              678  LOAD_ATTR                msgbox

 L. 416       680  LOAD_STR                 'Train MLP'

 L. 417       682  LOAD_STR                 'Non-positive learning rate'
              684  CALL_METHOD_3         3  '3 positional arguments'
              686  POP_TOP          

 L. 418       688  LOAD_CONST               None
              690  RETURN_VALUE     
            692_0  COME_FROM           652  '652'

 L. 419       692  LOAD_FAST                '_dropout_prob_fclayer'
              694  LOAD_CONST               False
              696  COMPARE_OP               is
          698_700  POP_JUMP_IF_TRUE    712  'to 712'
              702  LOAD_FAST                '_dropout_prob_fclayer'
              704  LOAD_CONST               0
              706  COMPARE_OP               <=
          708_710  POP_JUMP_IF_FALSE   748  'to 748'
            712_0  COME_FROM           698  '698'

 L. 420       712  LOAD_GLOBAL              vis_msg
              714  LOAD_ATTR                print
              716  LOAD_STR                 'ERROR in TrainMlMlp: Negative dropout rate'
              718  LOAD_STR                 'error'
              720  LOAD_CONST               ('type',)
              722  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              724  POP_TOP          

 L. 421       726  LOAD_GLOBAL              QtWidgets
              728  LOAD_ATTR                QMessageBox
              730  LOAD_METHOD              critical
              732  LOAD_DEREF               'self'
              734  LOAD_ATTR                msgbox

 L. 422       736  LOAD_STR                 'Train MLP'

 L. 423       738  LOAD_STR                 'Negative dropout rate'
              740  CALL_METHOD_3         3  '3 positional arguments'
              742  POP_TOP          

 L. 424       744  LOAD_CONST               None
              746  RETURN_VALUE     
            748_0  COME_FROM           708  '708'

 L. 426       748  LOAD_GLOBAL              len
              750  LOAD_DEREF               'self'
              752  LOAD_ATTR                ldtsave
              754  LOAD_METHOD              text
              756  CALL_METHOD_0         0  '0 positional arguments'
              758  CALL_FUNCTION_1       1  '1 positional argument'
              760  LOAD_CONST               1
              762  COMPARE_OP               <
          764_766  POP_JUMP_IF_FALSE   804  'to 804'

 L. 427       768  LOAD_GLOBAL              vis_msg
              770  LOAD_ATTR                print
              772  LOAD_STR                 'ERROR in TrainMlMlp: No name specified for MLP network'
              774  LOAD_STR                 'error'
              776  LOAD_CONST               ('type',)
              778  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              780  POP_TOP          

 L. 428       782  LOAD_GLOBAL              QtWidgets
              784  LOAD_ATTR                QMessageBox
              786  LOAD_METHOD              critical
              788  LOAD_DEREF               'self'
              790  LOAD_ATTR                msgbox

 L. 429       792  LOAD_STR                 'Train MLP'

 L. 430       794  LOAD_STR                 'No name specified for MLP network'
              796  CALL_METHOD_3         3  '3 positional arguments'
              798  POP_TOP          

 L. 431       800  LOAD_CONST               None
              802  RETURN_VALUE     
            804_0  COME_FROM           764  '764'

 L. 432       804  LOAD_GLOBAL              os
              806  LOAD_ATTR                path
              808  LOAD_METHOD              dirname
              810  LOAD_DEREF               'self'
              812  LOAD_ATTR                ldtsave
              814  LOAD_METHOD              text
              816  CALL_METHOD_0         0  '0 positional arguments'
              818  CALL_METHOD_1         1  '1 positional argument'
              820  STORE_FAST               '_savepath'

 L. 433       822  LOAD_GLOBAL              os
              824  LOAD_ATTR                path
              826  LOAD_METHOD              splitext
              828  LOAD_GLOBAL              os
              830  LOAD_ATTR                path
              832  LOAD_METHOD              basename
              834  LOAD_DEREF               'self'
              836  LOAD_ATTR                ldtsave
              838  LOAD_METHOD              text
              840  CALL_METHOD_0         0  '0 positional arguments'
              842  CALL_METHOD_1         1  '1 positional argument'
              844  CALL_METHOD_1         1  '1 positional argument'
              846  LOAD_CONST               0
              848  BINARY_SUBSCR    
              850  STORE_FAST               '_savename'

 L. 435       852  LOAD_FAST                '_target'
              854  LOAD_FAST                '_features'
              856  COMPARE_OP               in
          858_860  POP_JUMP_IF_FALSE   898  'to 898'

 L. 436       862  LOAD_GLOBAL              vis_msg
              864  LOAD_ATTR                print
              866  LOAD_STR                 'ERROR in TrainMlMlp: Target also used as features'
              868  LOAD_STR                 'error'
              870  LOAD_CONST               ('type',)
              872  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              874  POP_TOP          

 L. 437       876  LOAD_GLOBAL              QtWidgets
              878  LOAD_ATTR                QMessageBox
              880  LOAD_METHOD              critical
              882  LOAD_DEREF               'self'
              884  LOAD_ATTR                msgbox

 L. 438       886  LOAD_STR                 'Train MLP'

 L. 439       888  LOAD_STR                 'Target also used as features'
              890  CALL_METHOD_3         3  '3 positional arguments'
              892  POP_TOP          

 L. 440       894  LOAD_CONST               None
              896  RETURN_VALUE     
            898_0  COME_FROM           858  '858'

 L. 442       898  LOAD_GLOBAL              int
              900  LOAD_FAST                '_patch_depth'
              902  LOAD_CONST               2
              904  BINARY_TRUE_DIVIDE
              906  CALL_FUNCTION_1       1  '1 positional argument'
              908  STORE_FAST               '_wdinl'

 L. 443       910  LOAD_GLOBAL              int
              912  LOAD_FAST                '_patch_width'
              914  LOAD_CONST               2
              916  BINARY_TRUE_DIVIDE
              918  CALL_FUNCTION_1       1  '1 positional argument'
              920  STORE_FAST               '_wdxl'

 L. 444       922  LOAD_GLOBAL              int
              924  LOAD_FAST                '_patch_height'
              926  LOAD_CONST               2
              928  BINARY_TRUE_DIVIDE
              930  CALL_FUNCTION_1       1  '1 positional argument'
              932  STORE_FAST               '_wdz'

 L. 446       934  LOAD_DEREF               'self'
              936  LOAD_ATTR                survinfo
              938  STORE_FAST               '_seisinfo'

 L. 448       940  LOAD_GLOBAL              print
              942  LOAD_STR                 'TrainMlMlp: Step 1 - Get training samples:'
              944  CALL_FUNCTION_1       1  '1 positional argument'
              946  POP_TOP          

 L. 449       948  LOAD_DEREF               'self'
              950  LOAD_ATTR                traindataconfig
              952  LOAD_STR                 'TrainPointSet'
              954  BINARY_SUBSCR    
              956  STORE_FAST               '_trainpoint'

 L. 450       958  LOAD_GLOBAL              np
              960  LOAD_METHOD              zeros
              962  LOAD_CONST               0
              964  LOAD_CONST               3
              966  BUILD_LIST_2          2 
              968  CALL_METHOD_1         1  '1 positional argument'
              970  STORE_FAST               '_traindata'

 L. 451       972  SETUP_LOOP         1048  'to 1048'
              974  LOAD_FAST                '_trainpoint'
              976  GET_ITER         
            978_0  COME_FROM           996  '996'
              978  FOR_ITER           1046  'to 1046'
              980  STORE_FAST               '_p'

 L. 452       982  LOAD_GLOBAL              point_ays
              984  LOAD_METHOD              checkPoint
              986  LOAD_DEREF               'self'
              988  LOAD_ATTR                pointsetdata
              990  LOAD_FAST                '_p'
              992  BINARY_SUBSCR    
              994  CALL_METHOD_1         1  '1 positional argument'
          996_998  POP_JUMP_IF_FALSE   978  'to 978'

 L. 453      1000  LOAD_GLOBAL              basic_mdt
             1002  LOAD_METHOD              exportMatDict
             1004  LOAD_DEREF               'self'
             1006  LOAD_ATTR                pointsetdata
             1008  LOAD_FAST                '_p'
             1010  BINARY_SUBSCR    
             1012  LOAD_STR                 'Inline'
             1014  LOAD_STR                 'Crossline'
             1016  LOAD_STR                 'Z'
             1018  BUILD_LIST_3          3 
             1020  CALL_METHOD_2         2  '2 positional arguments'
             1022  STORE_FAST               '_pt'

 L. 454      1024  LOAD_GLOBAL              np
             1026  LOAD_ATTR                concatenate
             1028  LOAD_FAST                '_traindata'
             1030  LOAD_FAST                '_pt'
             1032  BUILD_TUPLE_2         2 
             1034  LOAD_CONST               0
             1036  LOAD_CONST               ('axis',)
             1038  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1040  STORE_FAST               '_traindata'
         1042_1044  JUMP_BACK           978  'to 978'
             1046  POP_BLOCK        
           1048_0  COME_FROM_LOOP      972  '972'

 L. 455      1048  LOAD_GLOBAL              seis_ays
             1050  LOAD_ATTR                removeOutofSurveySample
             1052  LOAD_FAST                '_traindata'

 L. 456      1054  LOAD_FAST                '_seisinfo'
             1056  LOAD_STR                 'ILStart'
             1058  BINARY_SUBSCR    
             1060  LOAD_FAST                '_wdinl'
             1062  LOAD_FAST                '_seisinfo'
             1064  LOAD_STR                 'ILStep'
             1066  BINARY_SUBSCR    
             1068  BINARY_MULTIPLY  
             1070  BINARY_ADD       

 L. 457      1072  LOAD_FAST                '_seisinfo'
             1074  LOAD_STR                 'ILEnd'
             1076  BINARY_SUBSCR    
             1078  LOAD_FAST                '_wdinl'
             1080  LOAD_FAST                '_seisinfo'
             1082  LOAD_STR                 'ILStep'
             1084  BINARY_SUBSCR    
             1086  BINARY_MULTIPLY  
             1088  BINARY_SUBTRACT  

 L. 458      1090  LOAD_FAST                '_seisinfo'
             1092  LOAD_STR                 'XLStart'
             1094  BINARY_SUBSCR    
             1096  LOAD_FAST                '_wdxl'
             1098  LOAD_FAST                '_seisinfo'
             1100  LOAD_STR                 'XLStep'
             1102  BINARY_SUBSCR    
             1104  BINARY_MULTIPLY  
             1106  BINARY_ADD       

 L. 459      1108  LOAD_FAST                '_seisinfo'
             1110  LOAD_STR                 'XLEnd'
             1112  BINARY_SUBSCR    
             1114  LOAD_FAST                '_wdxl'
             1116  LOAD_FAST                '_seisinfo'
             1118  LOAD_STR                 'XLStep'
             1120  BINARY_SUBSCR    
             1122  BINARY_MULTIPLY  
             1124  BINARY_SUBTRACT  

 L. 460      1126  LOAD_FAST                '_seisinfo'
             1128  LOAD_STR                 'ZStart'
             1130  BINARY_SUBSCR    
             1132  LOAD_FAST                '_wdz'
             1134  LOAD_FAST                '_seisinfo'
             1136  LOAD_STR                 'ZStep'
             1138  BINARY_SUBSCR    
             1140  BINARY_MULTIPLY  
             1142  BINARY_ADD       

 L. 461      1144  LOAD_FAST                '_seisinfo'
             1146  LOAD_STR                 'ZEnd'
             1148  BINARY_SUBSCR    
             1150  LOAD_FAST                '_wdz'
             1152  LOAD_FAST                '_seisinfo'
             1154  LOAD_STR                 'ZStep'
             1156  BINARY_SUBSCR    
             1158  BINARY_MULTIPLY  
             1160  BINARY_SUBTRACT  
             1162  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1164  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1166  STORE_FAST               '_traindata'

 L. 464      1168  LOAD_GLOBAL              np
             1170  LOAD_METHOD              shape
             1172  LOAD_FAST                '_traindata'
             1174  CALL_METHOD_1         1  '1 positional argument'
             1176  LOAD_CONST               0
             1178  BINARY_SUBSCR    
             1180  LOAD_CONST               0
             1182  COMPARE_OP               <=
         1184_1186  POP_JUMP_IF_FALSE  1224  'to 1224'

 L. 465      1188  LOAD_GLOBAL              vis_msg
             1190  LOAD_ATTR                print
             1192  LOAD_STR                 'ERROR in TrainMlMlp: No training sample found'
             1194  LOAD_STR                 'error'
             1196  LOAD_CONST               ('type',)
             1198  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1200  POP_TOP          

 L. 466      1202  LOAD_GLOBAL              QtWidgets
             1204  LOAD_ATTR                QMessageBox
             1206  LOAD_METHOD              critical
             1208  LOAD_DEREF               'self'
             1210  LOAD_ATTR                msgbox

 L. 467      1212  LOAD_STR                 'Train MLP'

 L. 468      1214  LOAD_STR                 'No training sample found'
             1216  CALL_METHOD_3         3  '3 positional arguments'
             1218  POP_TOP          

 L. 469      1220  LOAD_CONST               None
             1222  RETURN_VALUE     
           1224_0  COME_FROM          1184  '1184'

 L. 472      1224  LOAD_GLOBAL              print
             1226  LOAD_STR                 'TrainMlMlp: Step 2 - Retrieve features'
             1228  CALL_FUNCTION_1       1  '1 positional argument'
             1230  POP_TOP          

 L. 473      1232  BUILD_MAP_0           0 
             1234  STORE_FAST               '_traindict'

 L. 474      1236  SETUP_LOOP         1308  'to 1308'
             1238  LOAD_FAST                '_features'
             1240  GET_ITER         
             1242  FOR_ITER           1306  'to 1306'
             1244  STORE_FAST               'f'

 L. 475      1246  LOAD_DEREF               'self'
             1248  LOAD_ATTR                seisdata
             1250  LOAD_FAST                'f'
             1252  BINARY_SUBSCR    
             1254  STORE_FAST               '_seisdata'

 L. 476      1256  LOAD_GLOBAL              seis_ays
             1258  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1260  LOAD_FAST                '_seisdata'
             1262  LOAD_FAST                '_traindata'
             1264  LOAD_DEREF               'self'
             1266  LOAD_ATTR                survinfo

 L. 477      1268  LOAD_FAST                '_wdinl'
             1270  LOAD_FAST                '_wdxl'
             1272  LOAD_FAST                '_wdz'

 L. 478      1274  LOAD_CONST               False
             1276  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1278  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1280  LOAD_CONST               None
             1282  LOAD_CONST               None
             1284  BUILD_SLICE_2         2 
             1286  LOAD_CONST               3
             1288  LOAD_CONST               None
             1290  BUILD_SLICE_2         2 
             1292  BUILD_TUPLE_2         2 
             1294  BINARY_SUBSCR    
             1296  LOAD_FAST                '_traindict'
             1298  LOAD_FAST                'f'
             1300  STORE_SUBSCR     
         1302_1304  JUMP_BACK          1242  'to 1242'
             1306  POP_BLOCK        
           1308_0  COME_FROM_LOOP     1236  '1236'

 L. 479      1308  LOAD_FAST                '_target'
             1310  LOAD_FAST                '_features'
             1312  COMPARE_OP               not-in
         1314_1316  POP_JUMP_IF_FALSE  1368  'to 1368'

 L. 480      1318  LOAD_DEREF               'self'
             1320  LOAD_ATTR                seisdata
             1322  LOAD_FAST                '_target'
             1324  BINARY_SUBSCR    
             1326  STORE_FAST               '_seisdata'

 L. 481      1328  LOAD_GLOBAL              seis_ays
             1330  LOAD_ATTR                retrieveSeisSampleFrom3DMat
             1332  LOAD_FAST                '_seisdata'
             1334  LOAD_FAST                '_traindata'
             1336  LOAD_DEREF               'self'
             1338  LOAD_ATTR                survinfo

 L. 482      1340  LOAD_CONST               False
             1342  LOAD_CONST               ('seisinfo', 'verbose')
             1344  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1346  LOAD_CONST               None
             1348  LOAD_CONST               None
             1350  BUILD_SLICE_2         2 
             1352  LOAD_CONST               3
             1354  LOAD_CONST               None
             1356  BUILD_SLICE_2         2 
             1358  BUILD_TUPLE_2         2 
             1360  BINARY_SUBSCR    
             1362  LOAD_FAST                '_traindict'
             1364  LOAD_FAST                '_target'
             1366  STORE_SUBSCR     
           1368_0  COME_FROM          1314  '1314'

 L. 484      1368  LOAD_DEREF               'self'
             1370  LOAD_ATTR                traindataconfig
             1372  LOAD_STR                 'RemoveInvariantFeature_Checked'
             1374  BINARY_SUBSCR    
         1376_1378  POP_JUMP_IF_FALSE  1460  'to 1460'

 L. 485      1380  SETUP_LOOP         1460  'to 1460'
             1382  LOAD_FAST                '_features'
             1384  GET_ITER         
           1386_0  COME_FROM          1414  '1414'
             1386  FOR_ITER           1458  'to 1458'
             1388  STORE_FAST               'f'

 L. 486      1390  LOAD_GLOBAL              ml_aug
             1392  LOAD_METHOD              removeInvariantFeature
             1394  LOAD_FAST                '_traindict'
             1396  LOAD_FAST                'f'
             1398  CALL_METHOD_2         2  '2 positional arguments'
             1400  STORE_FAST               '_traindict'

 L. 487      1402  LOAD_GLOBAL              basic_mdt
             1404  LOAD_METHOD              maxDictConstantRow
             1406  LOAD_FAST                '_traindict'
             1408  CALL_METHOD_1         1  '1 positional argument'
             1410  LOAD_CONST               0
             1412  COMPARE_OP               <=
         1414_1416  POP_JUMP_IF_FALSE  1386  'to 1386'

 L. 488      1418  LOAD_GLOBAL              vis_msg
             1420  LOAD_ATTR                print
             1422  LOAD_STR                 'ERROR in TrainMlMlp: No training sample found'
             1424  LOAD_STR                 'error'
             1426  LOAD_CONST               ('tpe',)
             1428  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1430  POP_TOP          

 L. 489      1432  LOAD_GLOBAL              QtWidgets
             1434  LOAD_ATTR                QMessageBox
             1436  LOAD_METHOD              critical
             1438  LOAD_DEREF               'self'
             1440  LOAD_ATTR                msgbox

 L. 490      1442  LOAD_STR                 'Train MLP'

 L. 491      1444  LOAD_STR                 'No training sample found'
             1446  CALL_METHOD_3         3  '3 positional arguments'
             1448  POP_TOP          

 L. 492      1450  LOAD_CONST               None
             1452  RETURN_VALUE     
         1454_1456  JUMP_BACK          1386  'to 1386'
             1458  POP_BLOCK        
           1460_0  COME_FROM_LOOP     1380  '1380'
           1460_1  COME_FROM          1376  '1376'

 L. 494      1460  LOAD_GLOBAL              np
             1462  LOAD_METHOD              round
             1464  LOAD_FAST                '_traindict'
             1466  LOAD_FAST                '_target'
             1468  BINARY_SUBSCR    
             1470  CALL_METHOD_1         1  '1 positional argument'
             1472  LOAD_METHOD              astype
             1474  LOAD_GLOBAL              int
             1476  CALL_METHOD_1         1  '1 positional argument'
             1478  LOAD_FAST                '_traindict'
             1480  LOAD_FAST                '_target'
             1482  STORE_SUBSCR     

 L. 496      1484  LOAD_GLOBAL              print
             1486  LOAD_STR                 'TrainMlMlp: A total of %d valid training samples'
             1488  LOAD_GLOBAL              basic_mdt
             1490  LOAD_METHOD              maxDictConstantRow
             1492  LOAD_FAST                '_traindict'
             1494  CALL_METHOD_1         1  '1 positional argument'
             1496  BINARY_MODULO    
             1498  CALL_FUNCTION_1       1  '1 positional argument'
             1500  POP_TOP          

 L. 498      1502  LOAD_GLOBAL              print
             1504  LOAD_STR                 'TrainMlMlp: Step 3 - Balance labels'
             1506  CALL_FUNCTION_1       1  '1 positional argument'
             1508  POP_TOP          

 L. 499      1510  LOAD_DEREF               'self'
             1512  LOAD_ATTR                traindataconfig
             1514  LOAD_STR                 'BalanceTarget_Checked'
             1516  BINARY_SUBSCR    
         1518_1520  POP_JUMP_IF_FALSE  1562  'to 1562'

 L. 500      1522  LOAD_GLOBAL              ml_aug
             1524  LOAD_METHOD              balanceLabelbyExtension
             1526  LOAD_FAST                '_traindict'
             1528  LOAD_FAST                '_target'
             1530  CALL_METHOD_2         2  '2 positional arguments'
             1532  STORE_FAST               '_traindict'

 L. 501      1534  LOAD_GLOBAL              print
             1536  LOAD_STR                 'TrainMlMlp: A total of %d training samples after balance'
             1538  LOAD_GLOBAL              np
             1540  LOAD_METHOD              shape
             1542  LOAD_FAST                '_traindict'
             1544  LOAD_FAST                '_target'
             1546  BINARY_SUBSCR    
             1548  CALL_METHOD_1         1  '1 positional argument'
             1550  LOAD_CONST               0
             1552  BINARY_SUBSCR    
             1554  BINARY_MODULO    
             1556  CALL_FUNCTION_1       1  '1 positional argument'
             1558  POP_TOP          
             1560  JUMP_FORWARD       1570  'to 1570'
           1562_0  COME_FROM          1518  '1518'

 L. 503      1562  LOAD_GLOBAL              print
             1564  LOAD_STR                 'TrainMlMlp: No balance applied'
             1566  CALL_FUNCTION_1       1  '1 positional argument'
             1568  POP_TOP          
           1570_0  COME_FROM          1560  '1560'

 L. 505      1570  LOAD_GLOBAL              print
             1572  LOAD_STR                 'TrainMlMlp: Step 4 - Start training'
             1574  CALL_FUNCTION_1       1  '1 positional argument'
             1576  POP_TOP          

 L. 507      1578  LOAD_GLOBAL              QtWidgets
             1580  LOAD_METHOD              QProgressDialog
             1582  CALL_METHOD_0         0  '0 positional arguments'
             1584  STORE_FAST               '_pgsdlg'

 L. 508      1586  LOAD_GLOBAL              QtGui
             1588  LOAD_METHOD              QIcon
             1590  CALL_METHOD_0         0  '0 positional arguments'
             1592  STORE_FAST               'icon'

 L. 509      1594  LOAD_FAST                'icon'
             1596  LOAD_METHOD              addPixmap
             1598  LOAD_GLOBAL              QtGui
             1600  LOAD_METHOD              QPixmap
             1602  LOAD_GLOBAL              os
             1604  LOAD_ATTR                path
             1606  LOAD_METHOD              join
             1608  LOAD_DEREF               'self'
             1610  LOAD_ATTR                iconpath
             1612  LOAD_STR                 'icons/new.png'
             1614  CALL_METHOD_2         2  '2 positional arguments'
             1616  CALL_METHOD_1         1  '1 positional argument'

 L. 510      1618  LOAD_GLOBAL              QtGui
             1620  LOAD_ATTR                QIcon
             1622  LOAD_ATTR                Normal
             1624  LOAD_GLOBAL              QtGui
             1626  LOAD_ATTR                QIcon
             1628  LOAD_ATTR                Off
             1630  CALL_METHOD_3         3  '3 positional arguments'
             1632  POP_TOP          

 L. 511      1634  LOAD_FAST                '_pgsdlg'
             1636  LOAD_METHOD              setWindowIcon
             1638  LOAD_FAST                'icon'
             1640  CALL_METHOD_1         1  '1 positional argument'
             1642  POP_TOP          

 L. 512      1644  LOAD_FAST                '_pgsdlg'
             1646  LOAD_METHOD              setWindowTitle
             1648  LOAD_STR                 'Train MLP'
             1650  CALL_METHOD_1         1  '1 positional argument'
             1652  POP_TOP          

 L. 513      1654  LOAD_FAST                '_pgsdlg'
             1656  LOAD_METHOD              setCancelButton
             1658  LOAD_CONST               None
             1660  CALL_METHOD_1         1  '1 positional argument'
             1662  POP_TOP          

 L. 514      1664  LOAD_FAST                '_pgsdlg'
             1666  LOAD_METHOD              setWindowFlags
             1668  LOAD_GLOBAL              QtCore
             1670  LOAD_ATTR                Qt
             1672  LOAD_ATTR                WindowStaysOnTopHint
             1674  CALL_METHOD_1         1  '1 positional argument'
             1676  POP_TOP          

 L. 515      1678  LOAD_FAST                '_pgsdlg'
             1680  LOAD_METHOD              forceShow
             1682  CALL_METHOD_0         0  '0 positional arguments'
             1684  POP_TOP          

 L. 516      1686  LOAD_FAST                '_pgsdlg'
             1688  LOAD_METHOD              setFixedWidth
             1690  LOAD_CONST               400
             1692  CALL_METHOD_1         1  '1 positional argument'
             1694  POP_TOP          

 L. 517      1696  LOAD_GLOBAL              ml_fnn
             1698  LOAD_ATTR                createFNNClassifier
             1700  LOAD_FAST                '_traindict'

 L. 518      1702  LOAD_FAST                '_features'
             1704  LOAD_FAST                '_target'

 L. 519      1706  LOAD_FAST                '_nepoch'
             1708  LOAD_FAST                '_batchsize'

 L. 520      1710  LOAD_FAST                '_nlayer'
             1712  LOAD_FAST                '_nneuron'

 L. 521      1714  LOAD_FAST                '_learning_rate'

 L. 522      1716  LOAD_FAST                '_dropout_prob_fclayer'

 L. 523      1718  LOAD_CONST               True

 L. 524      1720  LOAD_FAST                '_savepath'
             1722  LOAD_FAST                '_savename'

 L. 525      1724  LOAD_FAST                '_pgsdlg'
             1726  LOAD_CONST               ('features', 'target', 'nepoch', 'batchsize', 'nlayer', 'nneuron', 'learningrate', 'dropoutprobfclayer', 'save2disk', 'savepath', 'savename', 'qpgsdlg')
             1728  CALL_FUNCTION_KW_13    13  '13 total positional and keyword args'
             1730  STORE_FAST               '_fnnlog'

 L. 527      1732  LOAD_GLOBAL              QtWidgets
             1734  LOAD_ATTR                QMessageBox
             1736  LOAD_METHOD              information
             1738  LOAD_DEREF               'self'
             1740  LOAD_ATTR                msgbox

 L. 528      1742  LOAD_STR                 'Train MLP'

 L. 529      1744  LOAD_STR                 'MLP trained successfully'
             1746  CALL_METHOD_3         3  '3 positional arguments'
             1748  POP_TOP          

 L. 531      1750  LOAD_GLOBAL              QtWidgets
             1752  LOAD_ATTR                QMessageBox
             1754  LOAD_METHOD              question
             1756  LOAD_DEREF               'self'
             1758  LOAD_ATTR                msgbox
             1760  LOAD_STR                 'Train MLP'
             1762  LOAD_STR                 'View learning matrix?'

 L. 532      1764  LOAD_GLOBAL              QtWidgets
             1766  LOAD_ATTR                QMessageBox
             1768  LOAD_ATTR                Yes
             1770  LOAD_GLOBAL              QtWidgets
             1772  LOAD_ATTR                QMessageBox
             1774  LOAD_ATTR                No
             1776  BINARY_OR        

 L. 533      1778  LOAD_GLOBAL              QtWidgets
             1780  LOAD_ATTR                QMessageBox
             1782  LOAD_ATTR                Yes
             1784  CALL_METHOD_5         5  '5 positional arguments'
             1786  STORE_FAST               'reply'

 L. 535      1788  LOAD_FAST                'reply'
             1790  LOAD_GLOBAL              QtWidgets
             1792  LOAD_ATTR                QMessageBox
             1794  LOAD_ATTR                Yes
             1796  COMPARE_OP               ==
         1798_1800  POP_JUMP_IF_FALSE  1868  'to 1868'

 L. 536      1802  LOAD_GLOBAL              QtWidgets
             1804  LOAD_METHOD              QDialog
             1806  CALL_METHOD_0         0  '0 positional arguments'
             1808  STORE_FAST               '_viewmllearnmat'

 L. 537      1810  LOAD_GLOBAL              gui_viewmllearnmat
             1812  CALL_FUNCTION_0       0  '0 positional arguments'
             1814  STORE_FAST               '_gui'

 L. 538      1816  LOAD_FAST                '_fnnlog'
             1818  LOAD_STR                 'learning_curve'
             1820  BINARY_SUBSCR    
             1822  LOAD_FAST                '_gui'
             1824  STORE_ATTR               learnmat

 L. 539      1826  LOAD_DEREF               'self'
             1828  LOAD_ATTR                linestyle
             1830  LOAD_FAST                '_gui'
             1832  STORE_ATTR               linestyle

 L. 540      1834  LOAD_DEREF               'self'
             1836  LOAD_ATTR                fontstyle
             1838  LOAD_FAST                '_gui'
             1840  STORE_ATTR               fontstyle

 L. 541      1842  LOAD_FAST                '_gui'
             1844  LOAD_METHOD              setupGUI
             1846  LOAD_FAST                '_viewmllearnmat'
             1848  CALL_METHOD_1         1  '1 positional argument'
             1850  POP_TOP          

 L. 542      1852  LOAD_FAST                '_viewmllearnmat'
             1854  LOAD_METHOD              exec
             1856  CALL_METHOD_0         0  '0 positional arguments'
             1858  POP_TOP          

 L. 543      1860  LOAD_FAST                '_viewmllearnmat'
             1862  LOAD_METHOD              show
             1864  CALL_METHOD_0         0  '0 positional arguments'
             1866  POP_TOP          
           1868_0  COME_FROM          1798  '1798'

Parse error at or near `POP_TOP' instruction at offset 1866

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
    TrainMlMlp = QtWidgets.QWidget()
    gui = trainmlmlp()
    gui.setupGUI(TrainMlMlp)
    TrainMlMlp.show()
    sys.exit(app.exec_())