# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\applymlmlp4pred.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 27195 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.vis.messager as vis_msg
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.fnnclassifier as ml_fnn
import cognitivegeo.src.gui.viewmlmlp as gui_viewmlmlp
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class applymlmlp4pred(object):
    survinfo = {}
    seisdata = {}
    rootpath = ''
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    iconpath = os.path.dirname(__file__)
    dialog = None
    modelpath = ''
    modelname = ''
    modelinfo = None

    def setupGUI(self, ApplyMlMlp4Pred):
        ApplyMlMlp4Pred.setObjectName('ApplyMlMlp4Pred')
        ApplyMlMlp4Pred.setFixedSize(810, 470)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ApplyMlMlp4Pred.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ApplyMlMlp4Pred)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ApplyMlMlp4Pred)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 160))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblpatchsize = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblpatchsize.setObjectName('lblpatchsize')
        self.lblpatchsize.setGeometry(QtCore.QRect(10, 230, 80, 30))
        self.lblpatchheight = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblpatchheight.setObjectName('lblpatchheight')
        self.lblpatchheight.setGeometry(QtCore.QRect(110, 230, 50, 30))
        self.ldtpatchheight = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtpatchheight.setObjectName('ldtpatchheight')
        self.ldtpatchheight.setGeometry(QtCore.QRect(160, 230, 40, 30))
        self.lblpatchwidth = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblpatchwidth.setObjectName('lblpatchwidth')
        self.lblpatchwidth.setGeometry(QtCore.QRect(205, 230, 50, 30))
        self.ldtpatchwidth = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtpatchwidth.setObjectName('ldtpatchwidth')
        self.ldtpatchwidth.setGeometry(QtCore.QRect(255, 230, 40, 30))
        self.lblpatchdepth = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblpatchdepth.setObjectName('lblpatchdepth')
        self.lblpatchdepth.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtpatchdepth = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtpatchdepth.setObjectName('ldtpatchdepth')
        self.ldtpatchdepth.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblold = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblold.setObjectName('lblold')
        self.lblold.setGeometry(QtCore.QRect(50, 270, 60, 30))
        self.lbloldlength = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lbloldlength.setObjectName('lbloldlength')
        self.lbloldlength.setGeometry(QtCore.QRect(110, 270, 50, 30))
        self.ldtoldlength = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtoldlength.setObjectName('ldtoldlength')
        self.ldtoldlength.setGeometry(QtCore.QRect(160, 270, 40, 30))
        self.lbloldtotal = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lbloldtotal.setObjectName('lbloldtotal')
        self.lbloldtotal.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtoldtotal = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtoldtotal.setObjectName('ldtoldtotal')
        self.ldtoldtotal.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lblnew = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblnew.setObjectName('lblnew')
        self.lblnew.setGeometry(QtCore.QRect(50, 310, 60, 30))
        self.lblnewlength = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblnewlength.setObjectName('lblnewlength')
        self.lblnewlength.setGeometry(QtCore.QRect(110, 310, 50, 30))
        self.ldtnewlength = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtnewlength.setObjectName('ldtnewlength')
        self.ldtnewlength.setGeometry(QtCore.QRect(160, 310, 40, 30))
        self.lblnewtotal = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblnewtotal.setObjectName('lblnewtotal')
        self.lblnewtotal.setGeometry(QtCore.QRect(300, 310, 50, 30))
        self.ldtnewtotal = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtnewtotal.setObjectName('ldtnewtotal')
        self.ldtnewtotal.setGeometry(QtCore.QRect(350, 310, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ApplyMlMlp4Pred)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnlayer = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblnlayer.setObjectName('lblnlayer')
        self.lblnlayer.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnlayer = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtnlayer.setObjectName('ldtnlayer')
        self.ldtnlayer.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnlayer = QtWidgets.QTableWidget(ApplyMlMlp4Pred)
        self.twgnlayer.setObjectName('twgnlayer')
        self.twgnlayer.setGeometry(QtCore.QRect(610, 100, 180, 160))
        self.twgnlayer.setColumnCount(2)
        self.twgnlayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnlayer.verticalHeader().hide()
        self.lblpara = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(410, 270, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(410, 310, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(550, 310, 40, 30))
        self.lblsave = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(410, 360, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.btnapply = QtWidgets.QPushButton(ApplyMlMlp4Pred)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(320, 410, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ApplyMlMlp4Pred)
        self.msgbox.setObjectName('msgbox')
        _center_x = ApplyMlMlp4Pred.geometry().center().x()
        _center_y = ApplyMlMlp4Pred.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ApplyMlMlp4Pred)
        QtCore.QMetaObject.connectSlotsByName(ApplyMlMlp4Pred)

    def retranslateGUI(self, ApplyMlMlp4Pred):
        self.dialog = ApplyMlMlp4Pred
        _translate = QtCore.QCoreApplication.translate
        ApplyMlMlp4Pred.setWindowTitle(_translate('ApplyMlMlp4Pred', 'Apply MLP for prediction'))
        self.lblfrom.setText(_translate('ApplyMlMlp4Pred', 'Select network:'))
        self.ldtfrom.setText(_translate('ApplyMlMlp4Pred', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ApplyMlMlp4Pred', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ApplyMlMlp4Pred', 'Training features:'))
        self.lblpatchsize.setText(_translate('ApplyMlMlp4Pred', 'Patch\nsize:'))
        self.lblpatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpatchheight.setText(_translate('ApplyMlMlp4Pred', 'height=\ntime/depth'))
        self.ldtpatchheight.setText(_translate('ApplyMlMlp4Pred', '1'))
        self.ldtpatchheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpatchwidth.setText(_translate('ApplyMlMlp4Pred', 'width=\ncrossline'))
        self.ldtpatchwidth.setText(_translate('ApplyMlMlp4Pred', '1'))
        self.ldtpatchwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpatchdepth.setText(_translate('ApplyMlMlp4Pred', 'depth=\ninline'))
        self.ldtpatchdepth.setText(_translate('ApplyMlMlp4Pred', '1'))
        self.ldtpatchdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtpatchheight.textChanged.connect(self.changeLdtPatchSize)
        self.ldtpatchwidth.textChanged.connect(self.changeLdtPatchSize)
        self.ldtpatchdepth.textChanged.connect(self.changeLdtPatchSize)
        self.lblold.setText(_translate('ApplyMlMlp4Pred', 'available:'))
        self.lbloldlength.setText(_translate('ApplyMlMlp4Pred', 'length ='))
        self.ldtoldlength.setText(_translate('ApplyMlMlp4Pred', ''))
        self.ldtoldlength.setEnabled(False)
        self.ldtoldlength.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldtotal.setText(_translate('ApplyMlMlp4Pred', 'total ='))
        self.ldtoldtotal.setText(_translate('ApplyMlMlp4Pred', ''))
        self.ldtoldtotal.setEnabled(False)
        self.ldtoldtotal.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnew.setText(_translate('ApplyMlMlp4Pred', 'expected:'))
        self.lblnewlength.setText(_translate('ApplyMlMlp4Pred', 'length ='))
        self.ldtnewlength.setText(_translate('ApplyMlMlp4Pred', ''))
        self.ldtnewlength.setEnabled(False)
        self.ldtnewlength.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewtotal.setText(_translate('ApplyMlMlp4Pred', 'total ='))
        self.ldtnewtotal.setText(_translate('ApplyMlMlp4Pred', ''))
        self.ldtnewtotal.setEnabled(False)
        self.ldtnewtotal.setAlignment(QtCore.Qt.AlignCenter)
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblnetwork.setText(_translate('ApplyMlMlp4Pred', 'Pre-trained MLP architecture:'))
        self.btnviewnetwork.setText(_translate('ApplyMlMlp4Pred', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnlayer.setText(_translate('ApplyMlMlp4Pred', 'No. of MLP layers:'))
        self.lblnlayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnlayer.setText(_translate('ApplyMlMlp4Pred', ''))
        self.ldtnlayer.setEnabled(False)
        self.ldtnlayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnlayer.textChanged.connect(self.changeLdtNlayer)
        self.twgnlayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblpara.setText(_translate('ApplyMlMlp4Pred', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ApplyMlMlp4Pred', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ApplyMlMlp4Pred', '10000'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('ApplyMlMlp4Pred', 'Output name='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ApplyMlMlp4Pred', 'mlp'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('ApplyMlMlp4Pred', 'Apply MLP'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnApplyMlMlp4Pred)

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
            _featurelist = self.modelinfo['feature_list']
            _firstfeature = None
            for f in _featurelist:
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
            _len = self.getTotalFeatureLength(_featurelist)
            self.ldtoldtotal.setText(str(_len))
            self.ldtnewtotal.setText(str(self.modelinfo['number_feature']))
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

    def clickBtnViewNetwork(self):
        _viewmlmlp = QtWidgets.QDialog()
        _gui = gui_viewmlmlp()
        _gui.linestyle = self.linestyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewmlmlp)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewmlmlp.exec()
        _viewmlmlp.show()

    def clickBtnApplyMlMlp4Pred--- This code section failed: ---

 L. 362         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 364         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 365        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in ApplyMlMlp4Pred: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 366        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 367        44  LOAD_STR                 'Apply MLP'

 L. 368        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 369        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 371        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkFNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 372        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in ApplyMlMlp4Pred: No MLP network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 373        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 374       100  LOAD_STR                 'Apply MLP'

 L. 375       102  LOAD_STR                 'No MLP network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 376       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 378       112  LOAD_FAST                'self'
              114  LOAD_ATTR                modelinfo
              116  LOAD_STR                 'feature_list'
              118  BINARY_SUBSCR    
              120  STORE_FAST               '_featurelist'

 L. 380       122  SETUP_LOOP          198  'to 198'
              124  LOAD_FAST                '_featurelist'
              126  GET_ITER         
            128_0  COME_FROM           144  '144'
              128  FOR_ITER            196  'to 196'
              130  STORE_FAST               'f'

 L. 381       132  LOAD_FAST                'self'
              134  LOAD_METHOD              checkSeisData
              136  LOAD_FAST                'f'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_CONST               False
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   128  'to 128'

 L. 382       146  LOAD_GLOBAL              vis_msg
              148  LOAD_ATTR                print
              150  LOAD_STR                 "ERROR in ApplyMlMlp4Pred: Feature '%s' not found in seismic data"
              152  LOAD_FAST                'f'
              154  BINARY_MODULO    

 L. 383       156  LOAD_STR                 'error'
              158  LOAD_CONST               ('type',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  POP_TOP          

 L. 384       164  LOAD_GLOBAL              QtWidgets
              166  LOAD_ATTR                QMessageBox
              168  LOAD_METHOD              critical
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                msgbox

 L. 385       174  LOAD_STR                 'Apply MLP'

 L. 386       176  LOAD_STR                 "Feature '"
              178  LOAD_FAST                'f'
              180  BINARY_ADD       
              182  LOAD_STR                 "' not found in seismic data"
              184  BINARY_ADD       
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 387       190  LOAD_CONST               None
              192  RETURN_VALUE     
              194  JUMP_BACK           128  'to 128'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      122  '122'

 L. 389       198  LOAD_FAST                'self'
              200  LOAD_ATTR                ldtoldlength
              202  LOAD_METHOD              text
              204  CALL_METHOD_0         0  '0 positional arguments'
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                ldtnewlength
              210  LOAD_METHOD              text
              212  CALL_METHOD_0         0  '0 positional arguments'
              214  COMPARE_OP               !=
              216  POP_JUMP_IF_TRUE    240  'to 240'

 L. 390       218  LOAD_FAST                'self'
              220  LOAD_ATTR                ldtoldtotal
              222  LOAD_METHOD              text
              224  CALL_METHOD_0         0  '0 positional arguments'
              226  LOAD_FAST                'self'
              228  LOAD_ATTR                ldtnewtotal
              230  LOAD_METHOD              text
              232  CALL_METHOD_0         0  '0 positional arguments'
              234  COMPARE_OP               !=
          236_238  POP_JUMP_IF_FALSE   276  'to 276'
            240_0  COME_FROM           216  '216'

 L. 391       240  LOAD_GLOBAL              vis_msg
              242  LOAD_ATTR                print
              244  LOAD_STR                 'ERROR in ApplyMlMlp4Pred: Feature length not match'
              246  LOAD_STR                 'error'
              248  LOAD_CONST               ('type',)
              250  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              252  POP_TOP          

 L. 392       254  LOAD_GLOBAL              QtWidgets
              256  LOAD_ATTR                QMessageBox
              258  LOAD_METHOD              critical
              260  LOAD_FAST                'self'
              262  LOAD_ATTR                msgbox

 L. 393       264  LOAD_STR                 'Apply MLP'

 L. 394       266  LOAD_STR                 'Feature length not match'
              268  CALL_METHOD_3         3  '3 positional arguments'
              270  POP_TOP          

 L. 395       272  LOAD_CONST               None
              274  RETURN_VALUE     
            276_0  COME_FROM           236  '236'

 L. 397       276  LOAD_GLOBAL              basic_data
              278  LOAD_METHOD              str2int
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                ldtpatchheight
              284  LOAD_METHOD              text
              286  CALL_METHOD_0         0  '0 positional arguments'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  STORE_FAST               '_patch_height'

 L. 398       292  LOAD_GLOBAL              basic_data
              294  LOAD_METHOD              str2int
              296  LOAD_FAST                'self'
              298  LOAD_ATTR                ldtpatchwidth
              300  LOAD_METHOD              text
              302  CALL_METHOD_0         0  '0 positional arguments'
              304  CALL_METHOD_1         1  '1 positional argument'
              306  STORE_FAST               '_patch_width'

 L. 399       308  LOAD_GLOBAL              basic_data
              310  LOAD_METHOD              str2int
              312  LOAD_FAST                'self'
              314  LOAD_ATTR                ldtpatchdepth
              316  LOAD_METHOD              text
              318  CALL_METHOD_0         0  '0 positional arguments'
              320  CALL_METHOD_1         1  '1 positional argument'
              322  STORE_FAST               '_patch_depth'

 L. 400       324  LOAD_FAST                '_patch_height'
              326  LOAD_CONST               False
              328  COMPARE_OP               is
          330_332  POP_JUMP_IF_TRUE    384  'to 384'
              334  LOAD_FAST                '_patch_width'
              336  LOAD_CONST               False
              338  COMPARE_OP               is
          340_342  POP_JUMP_IF_TRUE    384  'to 384'
              344  LOAD_FAST                '_patch_depth'
              346  LOAD_CONST               False
              348  COMPARE_OP               is
          350_352  POP_JUMP_IF_TRUE    384  'to 384'

 L. 401       354  LOAD_FAST                '_patch_height'
              356  LOAD_CONST               1
              358  COMPARE_OP               <
          360_362  POP_JUMP_IF_TRUE    384  'to 384'
              364  LOAD_FAST                '_patch_width'
              366  LOAD_CONST               1
              368  COMPARE_OP               <
          370_372  POP_JUMP_IF_TRUE    384  'to 384'
              374  LOAD_FAST                '_patch_depth'
              376  LOAD_CONST               1
              378  COMPARE_OP               <
          380_382  POP_JUMP_IF_FALSE   420  'to 420'
            384_0  COME_FROM           370  '370'
            384_1  COME_FROM           360  '360'
            384_2  COME_FROM           350  '350'
            384_3  COME_FROM           340  '340'
            384_4  COME_FROM           330  '330'

 L. 402       384  LOAD_GLOBAL              vis_msg
              386  LOAD_ATTR                print
              388  LOAD_STR                 'ERROR in ApplyMlMlp4Pred: Non-positive feature size'
              390  LOAD_STR                 'error'
              392  LOAD_CONST               ('type',)
              394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              396  POP_TOP          

 L. 403       398  LOAD_GLOBAL              QtWidgets
              400  LOAD_ATTR                QMessageBox
              402  LOAD_METHOD              critical
              404  LOAD_FAST                'self'
              406  LOAD_ATTR                msgbox

 L. 404       408  LOAD_STR                 'Apply MLP'

 L. 405       410  LOAD_STR                 'Non-positive feature size'
              412  CALL_METHOD_3         3  '3 positional arguments'
              414  POP_TOP          

 L. 406       416  LOAD_CONST               None
              418  RETURN_VALUE     
            420_0  COME_FROM           380  '380'

 L. 408       420  LOAD_GLOBAL              basic_data
              422  LOAD_METHOD              str2int
              424  LOAD_FAST                'self'
              426  LOAD_ATTR                ldtbatchsize
              428  LOAD_METHOD              text
              430  CALL_METHOD_0         0  '0 positional arguments'
              432  CALL_METHOD_1         1  '1 positional argument'
              434  STORE_FAST               '_batch'

 L. 409       436  LOAD_FAST                '_batch'
              438  LOAD_CONST               False
              440  COMPARE_OP               is
          442_444  POP_JUMP_IF_TRUE    456  'to 456'
              446  LOAD_FAST                '_batch'
              448  LOAD_CONST               1
              450  COMPARE_OP               <
          452_454  POP_JUMP_IF_FALSE   492  'to 492'
            456_0  COME_FROM           442  '442'

 L. 410       456  LOAD_GLOBAL              vis_msg
              458  LOAD_ATTR                print
              460  LOAD_STR                 'ERROR in ApplyMlMlp4Pred: Non-positive batch size'
              462  LOAD_STR                 'error'
              464  LOAD_CONST               ('type',)
              466  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              468  POP_TOP          

 L. 411       470  LOAD_GLOBAL              QtWidgets
              472  LOAD_ATTR                QMessageBox
              474  LOAD_METHOD              critical
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                msgbox

 L. 412       480  LOAD_STR                 'Apply MLP'

 L. 413       482  LOAD_STR                 'Non-positive batch size'
              484  CALL_METHOD_3         3  '3 positional arguments'
              486  POP_TOP          

 L. 414       488  LOAD_CONST               None
              490  RETURN_VALUE     
            492_0  COME_FROM           452  '452'

 L. 415       492  LOAD_GLOBAL              len
              494  LOAD_FAST                'self'
              496  LOAD_ATTR                ldtsave
              498  LOAD_METHOD              text
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  CALL_FUNCTION_1       1  '1 positional argument'
              504  LOAD_CONST               1
              506  COMPARE_OP               <
          508_510  POP_JUMP_IF_FALSE   548  'to 548'

 L. 416       512  LOAD_GLOBAL              vis_msg
              514  LOAD_ATTR                print
              516  LOAD_STR                 'ERROR in ApplyMlMlp4Pred: No name specified'
              518  LOAD_STR                 'error'
              520  LOAD_CONST               ('type',)
              522  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              524  POP_TOP          

 L. 417       526  LOAD_GLOBAL              QtWidgets
              528  LOAD_ATTR                QMessageBox
              530  LOAD_METHOD              critical
              532  LOAD_FAST                'self'
              534  LOAD_ATTR                msgbox

 L. 418       536  LOAD_STR                 'Apply MLP'

 L. 419       538  LOAD_STR                 'No name specified'
              540  CALL_METHOD_3         3  '3 positional arguments'
              542  POP_TOP          

 L. 420       544  LOAD_CONST               None
              546  RETURN_VALUE     
            548_0  COME_FROM           508  '508'

 L. 421       548  LOAD_FAST                'self'
              550  LOAD_ATTR                ldtsave
              552  LOAD_METHOD              text
              554  CALL_METHOD_0         0  '0 positional arguments'
              556  LOAD_FAST                'self'
              558  LOAD_ATTR                seisdata
              560  LOAD_METHOD              keys
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  COMPARE_OP               in
          566_568  POP_JUMP_IF_FALSE   654  'to 654'
              570  LOAD_FAST                'self'
              572  LOAD_METHOD              checkSeisData
              574  LOAD_FAST                'self'
              576  LOAD_ATTR                ldtsave
              578  LOAD_METHOD              text
              580  CALL_METHOD_0         0  '0 positional arguments'
              582  CALL_METHOD_1         1  '1 positional argument'
          584_586  POP_JUMP_IF_FALSE   654  'to 654'

 L. 422       588  LOAD_GLOBAL              QtWidgets
              590  LOAD_ATTR                QMessageBox
              592  LOAD_METHOD              question
              594  LOAD_FAST                'self'
              596  LOAD_ATTR                msgbox
              598  LOAD_STR                 'Apply MLP'

 L. 423       600  LOAD_FAST                'self'
              602  LOAD_ATTR                ldtsave
              604  LOAD_METHOD              text
              606  CALL_METHOD_0         0  '0 positional arguments'
              608  LOAD_STR                 ' already exists. Overwrite?'
              610  BINARY_ADD       

 L. 424       612  LOAD_GLOBAL              QtWidgets
              614  LOAD_ATTR                QMessageBox
              616  LOAD_ATTR                Yes
              618  LOAD_GLOBAL              QtWidgets
              620  LOAD_ATTR                QMessageBox
              622  LOAD_ATTR                No
              624  BINARY_OR        

 L. 425       626  LOAD_GLOBAL              QtWidgets
              628  LOAD_ATTR                QMessageBox
              630  LOAD_ATTR                No
              632  CALL_METHOD_5         5  '5 positional arguments'
              634  STORE_FAST               'reply'

 L. 427       636  LOAD_FAST                'reply'
              638  LOAD_GLOBAL              QtWidgets
              640  LOAD_ATTR                QMessageBox
              642  LOAD_ATTR                No
              644  COMPARE_OP               ==
          646_648  POP_JUMP_IF_FALSE   654  'to 654'

 L. 428       650  LOAD_CONST               None
              652  RETURN_VALUE     
            654_0  COME_FROM           646  '646'
            654_1  COME_FROM           584  '584'
            654_2  COME_FROM           566  '566'

 L. 430       654  LOAD_CONST               2
              656  LOAD_GLOBAL              int
              658  LOAD_FAST                '_patch_height'
              660  LOAD_CONST               2
              662  BINARY_TRUE_DIVIDE
              664  CALL_FUNCTION_1       1  '1 positional argument'
              666  BINARY_MULTIPLY  
              668  LOAD_CONST               1
              670  BINARY_ADD       
              672  STORE_FAST               '_patch_height'

 L. 431       674  LOAD_CONST               2
              676  LOAD_GLOBAL              int
              678  LOAD_FAST                '_patch_width'
              680  LOAD_CONST               2
              682  BINARY_TRUE_DIVIDE
              684  CALL_FUNCTION_1       1  '1 positional argument'
              686  BINARY_MULTIPLY  
              688  LOAD_CONST               1
              690  BINARY_ADD       
              692  STORE_FAST               '_patch_width'

 L. 432       694  LOAD_CONST               2
              696  LOAD_GLOBAL              int
              698  LOAD_FAST                '_patch_depth'
              700  LOAD_CONST               2
              702  BINARY_TRUE_DIVIDE
              704  CALL_FUNCTION_1       1  '1 positional argument'
              706  BINARY_MULTIPLY  
              708  LOAD_CONST               1
              710  BINARY_ADD       
              712  STORE_FAST               '_patch_depth'

 L. 434       714  LOAD_GLOBAL              np
              716  LOAD_METHOD              shape
              718  LOAD_FAST                'self'
              720  LOAD_ATTR                seisdata
              722  LOAD_FAST                '_featurelist'
              724  LOAD_CONST               0
              726  BINARY_SUBSCR    
              728  BINARY_SUBSCR    
              730  CALL_METHOD_1         1  '1 positional argument'
              732  LOAD_CONST               0
              734  BINARY_SUBSCR    
              736  STORE_FAST               '_nsample'

 L. 436       738  LOAD_GLOBAL              int
              740  LOAD_GLOBAL              np
              742  LOAD_METHOD              ceil
              744  LOAD_FAST                '_nsample'
              746  LOAD_FAST                '_batch'
              748  BINARY_TRUE_DIVIDE
              750  CALL_METHOD_1         1  '1 positional argument'
              752  CALL_FUNCTION_1       1  '1 positional argument'
              754  STORE_FAST               '_nloop'

 L. 439       756  LOAD_GLOBAL              QtWidgets
              758  LOAD_METHOD              QProgressDialog
              760  CALL_METHOD_0         0  '0 positional arguments'
              762  STORE_FAST               '_pgsdlg'

 L. 440       764  LOAD_GLOBAL              QtGui
              766  LOAD_METHOD              QIcon
              768  CALL_METHOD_0         0  '0 positional arguments'
              770  STORE_FAST               'icon'

 L. 441       772  LOAD_FAST                'icon'
              774  LOAD_METHOD              addPixmap
              776  LOAD_GLOBAL              QtGui
              778  LOAD_METHOD              QPixmap
              780  LOAD_GLOBAL              os
              782  LOAD_ATTR                path
              784  LOAD_METHOD              join
              786  LOAD_FAST                'self'
              788  LOAD_ATTR                iconpath
              790  LOAD_STR                 'icons/apply.png'
              792  CALL_METHOD_2         2  '2 positional arguments'
              794  CALL_METHOD_1         1  '1 positional argument'

 L. 442       796  LOAD_GLOBAL              QtGui
              798  LOAD_ATTR                QIcon
              800  LOAD_ATTR                Normal
              802  LOAD_GLOBAL              QtGui
              804  LOAD_ATTR                QIcon
              806  LOAD_ATTR                Off
              808  CALL_METHOD_3         3  '3 positional arguments'
              810  POP_TOP          

 L. 443       812  LOAD_FAST                '_pgsdlg'
              814  LOAD_METHOD              setWindowIcon
              816  LOAD_FAST                'icon'
              818  CALL_METHOD_1         1  '1 positional argument'
              820  POP_TOP          

 L. 444       822  LOAD_FAST                '_pgsdlg'
              824  LOAD_METHOD              setWindowTitle
              826  LOAD_STR                 'Apply MLP'
              828  CALL_METHOD_1         1  '1 positional argument'
              830  POP_TOP          

 L. 445       832  LOAD_FAST                '_pgsdlg'
              834  LOAD_METHOD              setCancelButton
              836  LOAD_CONST               None
              838  CALL_METHOD_1         1  '1 positional argument'
              840  POP_TOP          

 L. 446       842  LOAD_FAST                '_pgsdlg'
              844  LOAD_METHOD              setWindowFlags
              846  LOAD_GLOBAL              QtCore
              848  LOAD_ATTR                Qt
              850  LOAD_ATTR                WindowStaysOnTopHint
              852  CALL_METHOD_1         1  '1 positional argument'
              854  POP_TOP          

 L. 447       856  LOAD_FAST                '_pgsdlg'
              858  LOAD_METHOD              forceShow
              860  CALL_METHOD_0         0  '0 positional arguments'
              862  POP_TOP          

 L. 448       864  LOAD_FAST                '_pgsdlg'
              866  LOAD_METHOD              setFixedWidth
              868  LOAD_CONST               400
              870  CALL_METHOD_1         1  '1 positional argument'
              872  POP_TOP          

 L. 449       874  LOAD_FAST                '_pgsdlg'
              876  LOAD_METHOD              setMaximum
              878  LOAD_FAST                '_nloop'
              880  CALL_METHOD_1         1  '1 positional argument'
              882  POP_TOP          

 L. 452       884  LOAD_GLOBAL              int
              886  LOAD_FAST                '_patch_depth'
              888  LOAD_CONST               2
              890  BINARY_TRUE_DIVIDE
              892  CALL_FUNCTION_1       1  '1 positional argument'
              894  STORE_FAST               '_wdinl'

 L. 453       896  LOAD_GLOBAL              int
              898  LOAD_FAST                '_patch_width'
              900  LOAD_CONST               2
              902  BINARY_TRUE_DIVIDE
              904  CALL_FUNCTION_1       1  '1 positional argument'
              906  STORE_FAST               '_wdxl'

 L. 454       908  LOAD_GLOBAL              int
              910  LOAD_FAST                '_patch_height'
              912  LOAD_CONST               2
              914  BINARY_TRUE_DIVIDE
              916  CALL_FUNCTION_1       1  '1 positional argument'
              918  STORE_FAST               '_wdz'

 L. 456       920  LOAD_GLOBAL              seis_ays
              922  LOAD_METHOD              convertSeisInfoTo2DMat
              924  LOAD_FAST                'self'
              926  LOAD_ATTR                survinfo
              928  CALL_METHOD_1         1  '1 positional argument'
              930  STORE_FAST               '_seisdata'

 L. 458       932  LOAD_GLOBAL              np
              934  LOAD_METHOD              zeros
              936  LOAD_FAST                '_nsample'
              938  LOAD_CONST               1
              940  BUILD_LIST_2          2 
              942  CALL_METHOD_1         1  '1 positional argument'
              944  STORE_FAST               '_result'

 L. 459       946  LOAD_CONST               0
              948  STORE_FAST               'idxstart'

 L. 460   950_952  SETUP_LOOP         1226  'to 1226'
              954  LOAD_GLOBAL              range
              956  LOAD_FAST                '_nloop'
              958  CALL_FUNCTION_1       1  '1 positional argument'
              960  GET_ITER         
          962_964  FOR_ITER           1224  'to 1224'
              966  STORE_FAST               'i'

 L. 462       968  LOAD_GLOBAL              QtCore
              970  LOAD_ATTR                QCoreApplication
              972  LOAD_METHOD              instance
              974  CALL_METHOD_0         0  '0 positional arguments'
              976  LOAD_METHOD              processEvents
              978  CALL_METHOD_0         0  '0 positional arguments'
              980  POP_TOP          

 L. 464       982  LOAD_GLOBAL              sys
              984  LOAD_ATTR                stdout
              986  LOAD_METHOD              write

 L. 465       988  LOAD_STR                 '\r>>> Apply MLP, proceeding %.1f%% '
              990  LOAD_GLOBAL              float
              992  LOAD_FAST                'i'
              994  CALL_FUNCTION_1       1  '1 positional argument'
              996  LOAD_GLOBAL              float
              998  LOAD_FAST                '_nloop'
             1000  CALL_FUNCTION_1       1  '1 positional argument'
             1002  BINARY_TRUE_DIVIDE
             1004  LOAD_CONST               100.0
             1006  BINARY_MULTIPLY  
             1008  BINARY_MODULO    
             1010  CALL_METHOD_1         1  '1 positional argument'
             1012  POP_TOP          

 L. 466      1014  LOAD_GLOBAL              sys
             1016  LOAD_ATTR                stdout
             1018  LOAD_METHOD              flush
             1020  CALL_METHOD_0         0  '0 positional arguments'
             1022  POP_TOP          

 L. 468      1024  LOAD_FAST                'idxstart'
             1026  LOAD_FAST                '_batch'
             1028  BINARY_ADD       
             1030  STORE_FAST               'idxend'

 L. 469      1032  LOAD_FAST                'idxend'
             1034  LOAD_FAST                '_nsample'
             1036  COMPARE_OP               >
         1038_1040  POP_JUMP_IF_FALSE  1046  'to 1046'

 L. 470      1042  LOAD_FAST                '_nsample'
             1044  STORE_FAST               'idxend'
           1046_0  COME_FROM          1038  '1038'

 L. 471      1046  LOAD_GLOBAL              np
             1048  LOAD_METHOD              linspace
             1050  LOAD_FAST                'idxstart'
             1052  LOAD_FAST                'idxend'
             1054  LOAD_CONST               1
             1056  BINARY_SUBTRACT  
             1058  LOAD_FAST                'idxend'
             1060  LOAD_FAST                'idxstart'
             1062  BINARY_SUBTRACT  
             1064  CALL_METHOD_3         3  '3 positional arguments'
             1066  LOAD_METHOD              astype
             1068  LOAD_GLOBAL              int
             1070  CALL_METHOD_1         1  '1 positional argument'
             1072  STORE_FAST               'idxlist'

 L. 472      1074  LOAD_FAST                'idxend'
             1076  STORE_FAST               'idxstart'

 L. 474      1078  LOAD_FAST                '_seisdata'
             1080  LOAD_FAST                'idxlist'
             1082  LOAD_CONST               0
             1084  LOAD_CONST               3
             1086  BUILD_SLICE_2         2 
             1088  BUILD_TUPLE_2         2 
             1090  BINARY_SUBSCR    
             1092  STORE_FAST               '_targetdata'

 L. 476      1094  BUILD_MAP_0           0 
             1096  STORE_FAST               '_dict'

 L. 477      1098  SETUP_LOOP         1170  'to 1170'
             1100  LOAD_FAST                '_featurelist'
             1102  GET_ITER         
             1104  FOR_ITER           1168  'to 1168'
             1106  STORE_FAST               'f'

 L. 478      1108  LOAD_FAST                'self'
             1110  LOAD_ATTR                seisdata
             1112  LOAD_FAST                'f'
             1114  BINARY_SUBSCR    
             1116  STORE_FAST               '_data'

 L. 479      1118  LOAD_GLOBAL              seis_ays
             1120  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1122  LOAD_FAST                '_data'
             1124  LOAD_FAST                '_targetdata'
             1126  LOAD_FAST                'self'
             1128  LOAD_ATTR                survinfo

 L. 480      1130  LOAD_FAST                '_wdinl'
             1132  LOAD_FAST                '_wdxl'
             1134  LOAD_FAST                '_wdz'

 L. 481      1136  LOAD_CONST               False
             1138  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1140  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1142  LOAD_CONST               None
             1144  LOAD_CONST               None
             1146  BUILD_SLICE_2         2 
             1148  LOAD_CONST               3
             1150  LOAD_CONST               None
             1152  BUILD_SLICE_2         2 
             1154  BUILD_TUPLE_2         2 
             1156  BINARY_SUBSCR    
             1158  LOAD_FAST                '_dict'
             1160  LOAD_FAST                'f'
             1162  STORE_SUBSCR     
         1164_1166  JUMP_BACK          1104  'to 1104'
             1168  POP_BLOCK        
           1170_0  COME_FROM_LOOP     1098  '1098'

 L. 482      1170  LOAD_GLOBAL              ml_fnn
             1172  LOAD_ATTR                predictionFromFNNClassifier
             1174  LOAD_FAST                '_dict'

 L. 483      1176  LOAD_FAST                'self'
             1178  LOAD_ATTR                modelpath

 L. 484      1180  LOAD_FAST                'self'
             1182  LOAD_ATTR                modelname

 L. 485      1184  LOAD_FAST                '_batch'

 L. 486      1186  LOAD_CONST               True
             1188  LOAD_CONST               ('fnnpath', 'fnnname', 'batchsize', 'verbose')
             1190  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1192  LOAD_FAST                '_result'
             1194  LOAD_FAST                'idxlist'
             1196  LOAD_CONST               0
             1198  LOAD_CONST               1
             1200  BUILD_SLICE_2         2 
             1202  BUILD_TUPLE_2         2 
             1204  STORE_SUBSCR     

 L. 488      1206  LOAD_FAST                '_pgsdlg'
             1208  LOAD_METHOD              setValue
             1210  LOAD_FAST                'i'
             1212  LOAD_CONST               1
             1214  BINARY_ADD       
             1216  CALL_METHOD_1         1  '1 positional argument'
             1218  POP_TOP          
         1220_1222  JUMP_BACK           962  'to 962'
             1224  POP_BLOCK        
           1226_0  COME_FROM_LOOP      950  '950'

 L. 490      1226  LOAD_GLOBAL              print
             1228  LOAD_STR                 'Done'
             1230  CALL_FUNCTION_1       1  '1 positional argument'
             1232  POP_TOP          

 L. 491      1234  LOAD_GLOBAL              np
             1236  LOAD_METHOD              transpose
             1238  LOAD_GLOBAL              np
             1240  LOAD_METHOD              reshape
             1242  LOAD_FAST                '_result'

 L. 492      1244  LOAD_FAST                'self'
             1246  LOAD_ATTR                survinfo
             1248  LOAD_STR                 'ILNum'
             1250  BINARY_SUBSCR    
             1252  LOAD_FAST                'self'
             1254  LOAD_ATTR                survinfo
             1256  LOAD_STR                 'XLNum'
             1258  BINARY_SUBSCR    

 L. 493      1260  LOAD_FAST                'self'
             1262  LOAD_ATTR                survinfo
             1264  LOAD_STR                 'ZNum'
             1266  BINARY_SUBSCR    
             1268  BUILD_LIST_3          3 
             1270  CALL_METHOD_2         2  '2 positional arguments'

 L. 494      1272  LOAD_CONST               2
             1274  LOAD_CONST               1
             1276  LOAD_CONST               0
             1278  BUILD_LIST_3          3 
             1280  CALL_METHOD_2         2  '2 positional arguments'
             1282  LOAD_FAST                'self'
             1284  LOAD_ATTR                seisdata
             1286  LOAD_FAST                'self'
             1288  LOAD_ATTR                ldtsave
             1290  LOAD_METHOD              text
             1292  CALL_METHOD_0         0  '0 positional arguments'
             1294  STORE_SUBSCR     

 L. 496      1296  LOAD_GLOBAL              QtWidgets
             1298  LOAD_ATTR                QMessageBox
             1300  LOAD_METHOD              information
             1302  LOAD_FAST                'self'
             1304  LOAD_ATTR                msgbox

 L. 497      1306  LOAD_STR                 'Apply MLP'

 L. 498      1308  LOAD_STR                 'MLP applied successfully'
             1310  CALL_METHOD_3         3  '3 positional arguments'
             1312  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 1310

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
    ApplyMlMlp4Pred = QtWidgets.QWidget()
    gui = applymlmlp4pred()
    gui.setupGUI(ApplyMlMlp4Pred)
    ApplyMlMlp4Pred.show()
    sys.exit(app.exec_())