# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\evaluatemlmlp.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 28412 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.fnnclassifier as ml_fnn
import cognitivegeo.src.gui.viewmlmlp as gui_viewmlmlp
import cognitivegeo.src.gui.viewmlconfmat as gui_viewmlconfmat
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class evaluatemlmlp(object):
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

    def setupGUI(self, EvaluateMlMlp):
        EvaluateMlMlp.setObjectName('EvaluateMlMlp')
        EvaluateMlMlp.setFixedSize(810, 420)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/check.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EvaluateMlMlp.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(EvaluateMlMlp)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(EvaluateMlMlp)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(EvaluateMlMlp)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 160))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblpatchsize = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblpatchsize.setObjectName('lblpatchsize')
        self.lblpatchsize.setGeometry(QtCore.QRect(10, 230, 80, 30))
        self.lblpatchheight = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblpatchheight.setObjectName('lblpatchheight')
        self.lblpatchheight.setGeometry(QtCore.QRect(110, 230, 50, 30))
        self.ldtpatchheight = QtWidgets.QLineEdit(EvaluateMlMlp)
        self.ldtpatchheight.setObjectName('ldtpatchheight')
        self.ldtpatchheight.setGeometry(QtCore.QRect(160, 230, 40, 30))
        self.lblpatchwidth = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblpatchwidth.setObjectName('lblpatchwidth')
        self.lblpatchwidth.setGeometry(QtCore.QRect(205, 230, 50, 30))
        self.ldtpatchwidth = QtWidgets.QLineEdit(EvaluateMlMlp)
        self.ldtpatchwidth.setObjectName('ldtpatchwidth')
        self.ldtpatchwidth.setGeometry(QtCore.QRect(255, 230, 40, 30))
        self.lblpatchdepth = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblpatchdepth.setObjectName('lblpatchdepth')
        self.lblpatchdepth.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtpatchdepth = QtWidgets.QLineEdit(EvaluateMlMlp)
        self.ldtpatchdepth.setObjectName('ldtpatchdepth')
        self.ldtpatchdepth.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblold = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblold.setObjectName('lblold')
        self.lblold.setGeometry(QtCore.QRect(50, 270, 60, 30))
        self.lbloldlength = QtWidgets.QLabel(EvaluateMlMlp)
        self.lbloldlength.setObjectName('lbloldlength')
        self.lbloldlength.setGeometry(QtCore.QRect(110, 270, 50, 30))
        self.ldtoldlength = QtWidgets.QLineEdit(EvaluateMlMlp)
        self.ldtoldlength.setObjectName('ldtoldlength')
        self.ldtoldlength.setGeometry(QtCore.QRect(160, 270, 40, 30))
        self.lbloldtotal = QtWidgets.QLabel(EvaluateMlMlp)
        self.lbloldtotal.setObjectName('lbloldtotal')
        self.lbloldtotal.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtoldtotal = QtWidgets.QLineEdit(EvaluateMlMlp)
        self.ldtoldtotal.setObjectName('ldtoldtotal')
        self.ldtoldtotal.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lblnew = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblnew.setObjectName('lblnew')
        self.lblnew.setGeometry(QtCore.QRect(50, 310, 60, 30))
        self.lblnewlength = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblnewlength.setObjectName('lblnewlength')
        self.lblnewlength.setGeometry(QtCore.QRect(110, 310, 50, 30))
        self.ldtnewlength = QtWidgets.QLineEdit(EvaluateMlMlp)
        self.ldtnewlength.setObjectName('ldtnewlength')
        self.ldtnewlength.setGeometry(QtCore.QRect(160, 310, 40, 30))
        self.lblnewtotal = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblnewtotal.setObjectName('lblnewtotal')
        self.lblnewtotal.setGeometry(QtCore.QRect(300, 310, 50, 30))
        self.ldtnewtotal = QtWidgets.QLineEdit(EvaluateMlMlp)
        self.ldtnewtotal.setObjectName('ldtnewtotal')
        self.ldtnewtotal.setGeometry(QtCore.QRect(350, 310, 40, 30))
        self.lbltarget = QtWidgets.QLabel(EvaluateMlMlp)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 360, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(EvaluateMlMlp)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 360, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(EvaluateMlMlp)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnlayer = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblnlayer.setObjectName('lblnlayer')
        self.lblnlayer.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnlayer = QtWidgets.QLineEdit(EvaluateMlMlp)
        self.ldtnlayer.setObjectName('ldtnlayer')
        self.ldtnlayer.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnlayer = QtWidgets.QTableWidget(EvaluateMlMlp)
        self.twgnlayer.setObjectName('twgnlayer')
        self.twgnlayer.setGeometry(QtCore.QRect(610, 100, 180, 160))
        self.twgnlayer.setColumnCount(2)
        self.twgnlayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnlayer.verticalHeader().hide()
        self.lblpara = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(410, 270, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(EvaluateMlMlp)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(410, 310, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(EvaluateMlMlp)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(550, 310, 40, 30))
        self.btnapply = QtWidgets.QPushButton(EvaluateMlMlp)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 360, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/check.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(EvaluateMlMlp)
        self.msgbox.setObjectName('msgbox')
        _center_x = EvaluateMlMlp.geometry().center().x()
        _center_y = EvaluateMlMlp.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(EvaluateMlMlp)
        QtCore.QMetaObject.connectSlotsByName(EvaluateMlMlp)

    def retranslateGUI(self, EvaluateMlMlp):
        self.dialog = EvaluateMlMlp
        _translate = QtCore.QCoreApplication.translate
        EvaluateMlMlp.setWindowTitle(_translate('EvaluateMlMlp', 'Evaluate MLP'))
        self.lblfrom.setText(_translate('EvaluateMlMlp', 'Select network:'))
        self.ldtfrom.setText(_translate('EvaluateMlMlp', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('EvaluateMlMlp', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('EvaluateMlMlp', 'Training features:'))
        self.lblpatchsize.setText(_translate('ApplyMlMlp', 'Patch\nsize:'))
        self.lblpatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpatchheight.setText(_translate('ApplyMlMlp', 'height=\ntime/depth'))
        self.ldtpatchheight.setText(_translate('ApplyMlMlp', '1'))
        self.ldtpatchheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpatchwidth.setText(_translate('ApplyMlMlp', 'width=\ncrossline'))
        self.ldtpatchwidth.setText(_translate('ApplyMlMlp', '1'))
        self.ldtpatchwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpatchdepth.setText(_translate('ApplyMlMlp', 'depth=\ninline'))
        self.ldtpatchdepth.setText(_translate('ApplyMlMlp', '1'))
        self.ldtpatchdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtpatchheight.textChanged.connect(self.changeLdtPatchSize)
        self.ldtpatchwidth.textChanged.connect(self.changeLdtPatchSize)
        self.ldtpatchdepth.textChanged.connect(self.changeLdtPatchSize)
        self.lblold.setText(_translate('EvaluateMlMlp', 'available:'))
        self.lbloldlength.setText(_translate('EvaluateMlMlp', 'length ='))
        self.ldtoldlength.setText(_translate('EvaluateMlMlp', ''))
        self.ldtoldlength.setEnabled(False)
        self.ldtoldlength.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldtotal.setText(_translate('EvaluateMlMlp', 'total ='))
        self.ldtoldtotal.setText(_translate('EvaluateMlMlp', ''))
        self.ldtoldtotal.setEnabled(False)
        self.ldtoldtotal.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnew.setText(_translate('EvaluateMlMlp', 'expected:'))
        self.lblnewlength.setText(_translate('EvaluateMlMlp', 'length ='))
        self.ldtnewlength.setText(_translate('EvaluateMlMlp', ''))
        self.ldtnewlength.setEnabled(False)
        self.ldtnewlength.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewtotal.setText(_translate('EvaluateMlMlp', 'total ='))
        self.ldtnewtotal.setText(_translate('EvaluateMlMlp', ''))
        self.ldtnewtotal.setEnabled(False)
        self.ldtnewtotal.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltarget.setText(_translate('EvaluateMlMlp', 'Training target:'))
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblnetwork.setText(_translate('EvaluateMlMlp', 'Pre-trained MLP architecture:'))
        self.btnviewnetwork.setText(_translate('EvaluateMlMlp', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnlayer.setText(_translate('EvaluateMlMlp', 'No. of MLP layers:'))
        self.lblnlayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnlayer.setText(_translate('EvaluateMlMlp', ''))
        self.ldtnlayer.setEnabled(False)
        self.ldtnlayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnlayer.textChanged.connect(self.changeLdtNlayer)
        self.twgnlayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblpara.setText(_translate('EvaluateMlMlp', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('EvaluateMlMlp', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('EvaluateMlMlp', '10000'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('EvaluateMlMlp', 'Evaluate MLP'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnEvaluateMlMlp)

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

    def clickBtnViewNetwork(self):
        _viewmlmlp = QtWidgets.QDialog()
        _gui = gui_viewmlmlp()
        _gui.linestyle = self.linestyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewmlmlp)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewmlmlp.exec()
        _viewmlmlp.show()

    def clickBtnEvaluateMlMlp--- This code section failed: ---

 L. 363         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 365         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 366        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in EvaluateMlMlp: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 367        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 368        44  LOAD_STR                 'Evaluate MLP'

 L. 369        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 370        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 372        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkFNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 373        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in EvaluateMlMlp: No MLP network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 374        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 375       100  LOAD_STR                 'Evaluate MLP'

 L. 376       102  LOAD_STR                 'No MLP network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 377       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 379       112  LOAD_FAST                'self'
              114  LOAD_ATTR                modelinfo
              116  LOAD_STR                 'feature_list'
              118  BINARY_SUBSCR    
              120  STORE_FAST               '_featurelist'

 L. 381       122  SETUP_LOOP          198  'to 198'
              124  LOAD_FAST                '_featurelist'
              126  GET_ITER         
            128_0  COME_FROM           144  '144'
              128  FOR_ITER            196  'to 196'
              130  STORE_FAST               'f'

 L. 382       132  LOAD_FAST                'self'
              134  LOAD_METHOD              checkSeisData
              136  LOAD_FAST                'f'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_CONST               False
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   128  'to 128'

 L. 383       146  LOAD_GLOBAL              vis_msg
              148  LOAD_ATTR                print
              150  LOAD_STR                 "ERROR in EvaluateMlMlp: Feature '%s' not found in seismic data"
              152  LOAD_FAST                'f'
              154  BINARY_MODULO    

 L. 384       156  LOAD_STR                 'error'
              158  LOAD_CONST               ('type',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  POP_TOP          

 L. 385       164  LOAD_GLOBAL              QtWidgets
              166  LOAD_ATTR                QMessageBox
              168  LOAD_METHOD              critical
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                msgbox

 L. 386       174  LOAD_STR                 'Evaluate MLP'

 L. 387       176  LOAD_STR                 "Feature '"
              178  LOAD_FAST                'f'
              180  BINARY_ADD       
              182  LOAD_STR                 "' not found in seismic data"
              184  BINARY_ADD       
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 388       190  LOAD_CONST               None
              192  RETURN_VALUE     
              194  JUMP_BACK           128  'to 128'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      122  '122'

 L. 390       198  LOAD_FAST                'self'
              200  LOAD_ATTR                modelinfo
              202  LOAD_STR                 'target'
              204  BINARY_SUBSCR    
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                seisdata
              210  LOAD_METHOD              keys
              212  CALL_METHOD_0         0  '0 positional arguments'
              214  COMPARE_OP               not-in
          216_218  POP_JUMP_IF_FALSE   280  'to 280'

 L. 391       220  LOAD_GLOBAL              vis_msg
              222  LOAD_ATTR                print
              224  LOAD_STR                 "EvauluateMlMlp: Target label '%s' not found in seismic data"

 L. 392       226  LOAD_FAST                'self'
              228  LOAD_ATTR                modelinfo
              230  LOAD_STR                 'target'
              232  BINARY_SUBSCR    
              234  BINARY_MODULO    
              236  LOAD_STR                 'error'
              238  LOAD_CONST               ('type',)
              240  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              242  POP_TOP          

 L. 393       244  LOAD_GLOBAL              QtWidgets
              246  LOAD_ATTR                QMessageBox
              248  LOAD_METHOD              critical
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                msgbox

 L. 394       254  LOAD_STR                 'Evaluate MLP'

 L. 395       256  LOAD_STR                 "Target label '"
              258  LOAD_FAST                'self'
              260  LOAD_ATTR                modelinfo
              262  LOAD_STR                 'target'
              264  BINARY_SUBSCR    
              266  BINARY_ADD       
              268  LOAD_STR                 "' not found in seismic data"
              270  BINARY_ADD       
              272  CALL_METHOD_3         3  '3 positional arguments'
              274  POP_TOP          

 L. 396       276  LOAD_CONST               None
              278  RETURN_VALUE     
            280_0  COME_FROM           216  '216'

 L. 398       280  LOAD_FAST                'self'
              282  LOAD_ATTR                ldtoldlength
              284  LOAD_METHOD              text
              286  CALL_METHOD_0         0  '0 positional arguments'
              288  LOAD_FAST                'self'
              290  LOAD_ATTR                ldtnewlength
              292  LOAD_METHOD              text
              294  CALL_METHOD_0         0  '0 positional arguments'
              296  COMPARE_OP               !=
          298_300  POP_JUMP_IF_TRUE    324  'to 324'

 L. 399       302  LOAD_FAST                'self'
              304  LOAD_ATTR                ldtoldtotal
              306  LOAD_METHOD              text
              308  CALL_METHOD_0         0  '0 positional arguments'
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                ldtnewtotal
              314  LOAD_METHOD              text
              316  CALL_METHOD_0         0  '0 positional arguments'
              318  COMPARE_OP               !=
          320_322  POP_JUMP_IF_FALSE   360  'to 360'
            324_0  COME_FROM           298  '298'

 L. 400       324  LOAD_GLOBAL              vis_msg
              326  LOAD_ATTR                print
              328  LOAD_STR                 'ERROR in EvauluateMlMlp: Feature length not match'
              330  LOAD_STR                 'error'
              332  LOAD_CONST               ('type',)
              334  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              336  POP_TOP          

 L. 401       338  LOAD_GLOBAL              QtWidgets
              340  LOAD_ATTR                QMessageBox
              342  LOAD_METHOD              critical
              344  LOAD_FAST                'self'
              346  LOAD_ATTR                msgbox

 L. 402       348  LOAD_STR                 'Evaluate MLP'

 L. 403       350  LOAD_STR                 'Feature length not match'
              352  CALL_METHOD_3         3  '3 positional arguments'
              354  POP_TOP          

 L. 404       356  LOAD_CONST               None
              358  RETURN_VALUE     
            360_0  COME_FROM           320  '320'

 L. 406       360  LOAD_GLOBAL              basic_data
              362  LOAD_METHOD              str2int
              364  LOAD_FAST                'self'
              366  LOAD_ATTR                ldtpatchheight
              368  LOAD_METHOD              text
              370  CALL_METHOD_0         0  '0 positional arguments'
              372  CALL_METHOD_1         1  '1 positional argument'
              374  STORE_FAST               '_patch_height'

 L. 407       376  LOAD_GLOBAL              basic_data
              378  LOAD_METHOD              str2int
              380  LOAD_FAST                'self'
              382  LOAD_ATTR                ldtpatchwidth
              384  LOAD_METHOD              text
              386  CALL_METHOD_0         0  '0 positional arguments'
              388  CALL_METHOD_1         1  '1 positional argument'
              390  STORE_FAST               '_patch_width'

 L. 408       392  LOAD_GLOBAL              basic_data
              394  LOAD_METHOD              str2int
              396  LOAD_FAST                'self'
              398  LOAD_ATTR                ldtpatchdepth
              400  LOAD_METHOD              text
              402  CALL_METHOD_0         0  '0 positional arguments'
              404  CALL_METHOD_1         1  '1 positional argument'
              406  STORE_FAST               '_patch_depth'

 L. 409       408  LOAD_FAST                '_patch_height'
              410  LOAD_CONST               False
              412  COMPARE_OP               is
          414_416  POP_JUMP_IF_TRUE    468  'to 468'
              418  LOAD_FAST                '_patch_width'
              420  LOAD_CONST               False
              422  COMPARE_OP               is
          424_426  POP_JUMP_IF_TRUE    468  'to 468'
              428  LOAD_FAST                '_patch_depth'
              430  LOAD_CONST               False
              432  COMPARE_OP               is
          434_436  POP_JUMP_IF_TRUE    468  'to 468'

 L. 410       438  LOAD_FAST                '_patch_height'
              440  LOAD_CONST               1
              442  COMPARE_OP               <
          444_446  POP_JUMP_IF_TRUE    468  'to 468'
              448  LOAD_FAST                '_patch_width'
              450  LOAD_CONST               1
              452  COMPARE_OP               <
          454_456  POP_JUMP_IF_TRUE    468  'to 468'
              458  LOAD_FAST                '_patch_depth'
              460  LOAD_CONST               1
              462  COMPARE_OP               <
          464_466  POP_JUMP_IF_FALSE   504  'to 504'
            468_0  COME_FROM           454  '454'
            468_1  COME_FROM           444  '444'
            468_2  COME_FROM           434  '434'
            468_3  COME_FROM           424  '424'
            468_4  COME_FROM           414  '414'

 L. 411       468  LOAD_GLOBAL              vis_msg
              470  LOAD_ATTR                print
              472  LOAD_STR                 'ERROR in EvaluateMlMlp: Non-positive feature size'
              474  LOAD_STR                 'error'
              476  LOAD_CONST               ('type',)
              478  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              480  POP_TOP          

 L. 412       482  LOAD_GLOBAL              QtWidgets
              484  LOAD_ATTR                QMessageBox
              486  LOAD_METHOD              critical
              488  LOAD_FAST                'self'
              490  LOAD_ATTR                msgbox

 L. 413       492  LOAD_STR                 'Evaluate MLP'

 L. 414       494  LOAD_STR                 'Non-positive feature size'
              496  CALL_METHOD_3         3  '3 positional arguments'
              498  POP_TOP          

 L. 415       500  LOAD_CONST               None
              502  RETURN_VALUE     
            504_0  COME_FROM           464  '464'

 L. 417       504  LOAD_GLOBAL              basic_data
              506  LOAD_METHOD              str2int
              508  LOAD_FAST                'self'
              510  LOAD_ATTR                ldtbatchsize
              512  LOAD_METHOD              text
              514  CALL_METHOD_0         0  '0 positional arguments'
              516  CALL_METHOD_1         1  '1 positional argument'
              518  STORE_FAST               '_batch'

 L. 418       520  LOAD_FAST                '_batch'
              522  LOAD_CONST               False
              524  COMPARE_OP               is
          526_528  POP_JUMP_IF_TRUE    540  'to 540'
              530  LOAD_FAST                '_batch'
              532  LOAD_CONST               1
              534  COMPARE_OP               <
          536_538  POP_JUMP_IF_FALSE   576  'to 576'
            540_0  COME_FROM           526  '526'

 L. 419       540  LOAD_GLOBAL              vis_msg
              542  LOAD_ATTR                print
              544  LOAD_STR                 'ERROR in EvaluateMlMlp: Non-positive batch size'
              546  LOAD_STR                 'error'
              548  LOAD_CONST               ('type',)
              550  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              552  POP_TOP          

 L. 420       554  LOAD_GLOBAL              QtWidgets
              556  LOAD_ATTR                QMessageBox
              558  LOAD_METHOD              critical
              560  LOAD_FAST                'self'
              562  LOAD_ATTR                msgbox

 L. 421       564  LOAD_STR                 'Evaluate MLP'

 L. 422       566  LOAD_STR                 'Non-positive batch size'
              568  CALL_METHOD_3         3  '3 positional arguments'
              570  POP_TOP          

 L. 423       572  LOAD_CONST               None
              574  RETURN_VALUE     
            576_0  COME_FROM           536  '536'

 L. 425       576  LOAD_CONST               2
              578  LOAD_GLOBAL              int
              580  LOAD_FAST                '_patch_height'
              582  LOAD_CONST               2
              584  BINARY_TRUE_DIVIDE
              586  CALL_FUNCTION_1       1  '1 positional argument'
              588  BINARY_MULTIPLY  
              590  LOAD_CONST               1
              592  BINARY_ADD       
              594  STORE_FAST               '_patch_height'

 L. 426       596  LOAD_CONST               2
              598  LOAD_GLOBAL              int
              600  LOAD_FAST                '_patch_width'
              602  LOAD_CONST               2
              604  BINARY_TRUE_DIVIDE
              606  CALL_FUNCTION_1       1  '1 positional argument'
              608  BINARY_MULTIPLY  
              610  LOAD_CONST               1
              612  BINARY_ADD       
              614  STORE_FAST               '_patch_width'

 L. 427       616  LOAD_CONST               2
              618  LOAD_GLOBAL              int
              620  LOAD_FAST                '_patch_depth'
              622  LOAD_CONST               2
              624  BINARY_TRUE_DIVIDE
              626  CALL_FUNCTION_1       1  '1 positional argument'
              628  BINARY_MULTIPLY  
              630  LOAD_CONST               1
              632  BINARY_ADD       
              634  STORE_FAST               '_patch_depth'

 L. 429       636  LOAD_FAST                'self'
              638  LOAD_ATTR                modelinfo
              640  LOAD_STR                 'number_label'
              642  BINARY_SUBSCR    
              644  STORE_FAST               '_nlabel'

 L. 430       646  LOAD_FAST                'self'
              648  LOAD_ATTR                modelinfo
              650  LOAD_STR                 'target'
              652  BINARY_SUBSCR    
              654  STORE_FAST               '_target'

 L. 432       656  LOAD_GLOBAL              int
              658  LOAD_FAST                '_patch_depth'
              660  LOAD_CONST               2
              662  BINARY_TRUE_DIVIDE
              664  CALL_FUNCTION_1       1  '1 positional argument'
              666  STORE_FAST               '_wdinl'

 L. 433       668  LOAD_GLOBAL              int
              670  LOAD_FAST                '_patch_width'
              672  LOAD_CONST               2
              674  BINARY_TRUE_DIVIDE
              676  CALL_FUNCTION_1       1  '1 positional argument'
              678  STORE_FAST               '_wdxl'

 L. 434       680  LOAD_GLOBAL              int
              682  LOAD_FAST                '_patch_height'
              684  LOAD_CONST               2
              686  BINARY_TRUE_DIVIDE
              688  CALL_FUNCTION_1       1  '1 positional argument'
              690  STORE_FAST               '_wdz'

 L. 436       692  LOAD_FAST                'self'
              694  LOAD_ATTR                survinfo
              696  STORE_FAST               '_seisinfo'

 L. 438       698  LOAD_GLOBAL              seis_ays
              700  LOAD_ATTR                removeOutofSurveySample
              702  LOAD_GLOBAL              seis_ays
              704  LOAD_METHOD              convertSeisInfoTo2DMat
              706  LOAD_FAST                'self'
              708  LOAD_ATTR                survinfo
              710  CALL_METHOD_1         1  '1 positional argument'

 L. 439       712  LOAD_FAST                '_seisinfo'
              714  LOAD_STR                 'ILStart'
              716  BINARY_SUBSCR    
              718  LOAD_FAST                '_wdinl'
              720  LOAD_FAST                '_seisinfo'
              722  LOAD_STR                 'ILStep'
              724  BINARY_SUBSCR    
              726  BINARY_MULTIPLY  
              728  BINARY_ADD       

 L. 440       730  LOAD_FAST                '_seisinfo'
              732  LOAD_STR                 'ILEnd'
              734  BINARY_SUBSCR    
              736  LOAD_FAST                '_wdinl'
              738  LOAD_FAST                '_seisinfo'
              740  LOAD_STR                 'ILStep'
              742  BINARY_SUBSCR    
              744  BINARY_MULTIPLY  
              746  BINARY_SUBTRACT  

 L. 441       748  LOAD_FAST                '_seisinfo'
              750  LOAD_STR                 'XLStart'
              752  BINARY_SUBSCR    
              754  LOAD_FAST                '_wdxl'
              756  LOAD_FAST                '_seisinfo'
              758  LOAD_STR                 'XLStep'
              760  BINARY_SUBSCR    
              762  BINARY_MULTIPLY  
              764  BINARY_ADD       

 L. 442       766  LOAD_FAST                '_seisinfo'
              768  LOAD_STR                 'XLEnd'
              770  BINARY_SUBSCR    
              772  LOAD_FAST                '_wdxl'
              774  LOAD_FAST                '_seisinfo'
              776  LOAD_STR                 'XLStep'
              778  BINARY_SUBSCR    
              780  BINARY_MULTIPLY  
              782  BINARY_SUBTRACT  

 L. 443       784  LOAD_FAST                '_seisinfo'
              786  LOAD_STR                 'ZStart'
              788  BINARY_SUBSCR    
              790  LOAD_FAST                '_wdz'
              792  LOAD_FAST                '_seisinfo'
              794  LOAD_STR                 'ZStep'
              796  BINARY_SUBSCR    
              798  BINARY_MULTIPLY  
              800  BINARY_ADD       

 L. 444       802  LOAD_FAST                '_seisinfo'
              804  LOAD_STR                 'ZEnd'
              806  BINARY_SUBSCR    
              808  LOAD_FAST                '_wdz'
              810  LOAD_FAST                '_seisinfo'
              812  LOAD_STR                 'ZStep'
              814  BINARY_SUBSCR    
              816  BINARY_MULTIPLY  
              818  BINARY_SUBTRACT  
              820  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
              822  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              824  STORE_FAST               '_data'

 L. 446       826  BUILD_MAP_0           0 
              828  STORE_FAST               '_seisdict'

 L. 447       830  LOAD_FAST                '_data'
              832  LOAD_CONST               None
              834  LOAD_CONST               None
              836  BUILD_SLICE_2         2 
              838  LOAD_CONST               0
              840  LOAD_CONST               1
              842  BUILD_SLICE_2         2 
              844  BUILD_TUPLE_2         2 
              846  BINARY_SUBSCR    
              848  LOAD_FAST                '_seisdict'
              850  LOAD_STR                 'Inline'
              852  STORE_SUBSCR     

 L. 448       854  LOAD_FAST                '_data'
              856  LOAD_CONST               None
              858  LOAD_CONST               None
              860  BUILD_SLICE_2         2 
              862  LOAD_CONST               1
              864  LOAD_CONST               2
              866  BUILD_SLICE_2         2 
              868  BUILD_TUPLE_2         2 
              870  BINARY_SUBSCR    
              872  LOAD_FAST                '_seisdict'
              874  LOAD_STR                 'Crossline'
              876  STORE_SUBSCR     

 L. 449       878  LOAD_FAST                '_data'
              880  LOAD_CONST               None
              882  LOAD_CONST               None
              884  BUILD_SLICE_2         2 
              886  LOAD_CONST               2
              888  LOAD_CONST               3
              890  BUILD_SLICE_2         2 
              892  BUILD_TUPLE_2         2 
              894  BINARY_SUBSCR    
              896  LOAD_FAST                '_seisdict'
              898  LOAD_STR                 'Z'
              900  STORE_SUBSCR     

 L. 451       902  LOAD_GLOBAL              basic_mdt
              904  LOAD_METHOD              maxDictConstantRow
              906  LOAD_FAST                '_seisdict'
              908  CALL_METHOD_1         1  '1 positional argument'
              910  STORE_FAST               '_nsample'

 L. 453       912  LOAD_GLOBAL              int
              914  LOAD_GLOBAL              np
              916  LOAD_METHOD              ceil
              918  LOAD_FAST                '_nsample'
              920  LOAD_FAST                '_batch'
              922  BINARY_TRUE_DIVIDE
              924  CALL_METHOD_1         1  '1 positional argument'
              926  CALL_FUNCTION_1       1  '1 positional argument'
              928  STORE_FAST               '_nloop'

 L. 456       930  LOAD_GLOBAL              QtWidgets
              932  LOAD_METHOD              QProgressDialog
              934  CALL_METHOD_0         0  '0 positional arguments'
              936  STORE_FAST               '_pgsdlg'

 L. 457       938  LOAD_GLOBAL              QtGui
              940  LOAD_METHOD              QIcon
              942  CALL_METHOD_0         0  '0 positional arguments'
              944  STORE_FAST               'icon'

 L. 458       946  LOAD_FAST                'icon'
              948  LOAD_METHOD              addPixmap
              950  LOAD_GLOBAL              QtGui
              952  LOAD_METHOD              QPixmap
              954  LOAD_GLOBAL              os
              956  LOAD_ATTR                path
              958  LOAD_METHOD              join
              960  LOAD_FAST                'self'
              962  LOAD_ATTR                iconpath
              964  LOAD_STR                 'icons/check.png'
              966  CALL_METHOD_2         2  '2 positional arguments'
              968  CALL_METHOD_1         1  '1 positional argument'

 L. 459       970  LOAD_GLOBAL              QtGui
              972  LOAD_ATTR                QIcon
              974  LOAD_ATTR                Normal
              976  LOAD_GLOBAL              QtGui
              978  LOAD_ATTR                QIcon
              980  LOAD_ATTR                Off
              982  CALL_METHOD_3         3  '3 positional arguments'
              984  POP_TOP          

 L. 460       986  LOAD_FAST                '_pgsdlg'
              988  LOAD_METHOD              setWindowIcon
              990  LOAD_FAST                'icon'
              992  CALL_METHOD_1         1  '1 positional argument'
              994  POP_TOP          

 L. 461       996  LOAD_FAST                '_pgsdlg'
              998  LOAD_METHOD              setWindowTitle
             1000  LOAD_STR                 'Evaluate MLP'
             1002  CALL_METHOD_1         1  '1 positional argument'
             1004  POP_TOP          

 L. 462      1006  LOAD_FAST                '_pgsdlg'
             1008  LOAD_METHOD              setCancelButton
             1010  LOAD_CONST               None
             1012  CALL_METHOD_1         1  '1 positional argument'
             1014  POP_TOP          

 L. 463      1016  LOAD_FAST                '_pgsdlg'
             1018  LOAD_METHOD              setWindowFlags
             1020  LOAD_GLOBAL              QtCore
             1022  LOAD_ATTR                Qt
             1024  LOAD_ATTR                WindowStaysOnTopHint
             1026  CALL_METHOD_1         1  '1 positional argument'
             1028  POP_TOP          

 L. 464      1030  LOAD_FAST                '_pgsdlg'
             1032  LOAD_METHOD              forceShow
             1034  CALL_METHOD_0         0  '0 positional arguments'
             1036  POP_TOP          

 L. 465      1038  LOAD_FAST                '_pgsdlg'
             1040  LOAD_METHOD              setFixedWidth
             1042  LOAD_CONST               400
             1044  CALL_METHOD_1         1  '1 positional argument'
             1046  POP_TOP          

 L. 466      1048  LOAD_FAST                '_pgsdlg'
             1050  LOAD_METHOD              setMaximum
             1052  LOAD_FAST                '_nloop'
             1054  CALL_METHOD_1         1  '1 positional argument'
             1056  POP_TOP          

 L. 468      1058  LOAD_GLOBAL              np
             1060  LOAD_METHOD              zeros
             1062  LOAD_FAST                '_nlabel'
             1064  LOAD_CONST               1
             1066  BINARY_ADD       
             1068  LOAD_FAST                '_nlabel'
             1070  LOAD_CONST               1
             1072  BINARY_ADD       
             1074  BUILD_LIST_2          2 
             1076  CALL_METHOD_1         1  '1 positional argument'
             1078  STORE_FAST               '_result'

 L. 469      1080  LOAD_CONST               0
             1082  STORE_FAST               'idxstart'

 L. 470  1084_1086  SETUP_LOOP         1488  'to 1488'
             1088  LOAD_GLOBAL              range
             1090  LOAD_FAST                '_nloop'
             1092  CALL_FUNCTION_1       1  '1 positional argument'
             1094  GET_ITER         
         1096_1098  FOR_ITER           1486  'to 1486'
             1100  STORE_FAST               'i'

 L. 472      1102  LOAD_GLOBAL              QtCore
             1104  LOAD_ATTR                QCoreApplication
             1106  LOAD_METHOD              instance
             1108  CALL_METHOD_0         0  '0 positional arguments'
             1110  LOAD_METHOD              processEvents
             1112  CALL_METHOD_0         0  '0 positional arguments'
             1114  POP_TOP          

 L. 474      1116  LOAD_GLOBAL              sys
             1118  LOAD_ATTR                stdout
             1120  LOAD_METHOD              write

 L. 475      1122  LOAD_STR                 '\r>>> Evaluate MLP, proceeding %.1f%% '
             1124  LOAD_GLOBAL              float
             1126  LOAD_FAST                'i'
             1128  CALL_FUNCTION_1       1  '1 positional argument'
             1130  LOAD_GLOBAL              float
             1132  LOAD_FAST                '_nloop'
             1134  CALL_FUNCTION_1       1  '1 positional argument'
             1136  BINARY_TRUE_DIVIDE
             1138  LOAD_CONST               100.0
             1140  BINARY_MULTIPLY  
             1142  BINARY_MODULO    
             1144  CALL_METHOD_1         1  '1 positional argument'
             1146  POP_TOP          

 L. 476      1148  LOAD_GLOBAL              sys
             1150  LOAD_ATTR                stdout
             1152  LOAD_METHOD              flush
             1154  CALL_METHOD_0         0  '0 positional arguments'
             1156  POP_TOP          

 L. 478      1158  LOAD_FAST                'idxstart'
             1160  LOAD_FAST                '_batch'
             1162  BINARY_ADD       
             1164  STORE_FAST               'idxend'

 L. 479      1166  LOAD_FAST                'idxend'
             1168  LOAD_FAST                '_nsample'
             1170  COMPARE_OP               >
         1172_1174  POP_JUMP_IF_FALSE  1180  'to 1180'

 L. 480      1176  LOAD_FAST                '_nsample'
             1178  STORE_FAST               'idxend'
           1180_0  COME_FROM          1172  '1172'

 L. 481      1180  LOAD_GLOBAL              np
             1182  LOAD_METHOD              linspace
             1184  LOAD_FAST                'idxstart'
             1186  LOAD_FAST                'idxend'
             1188  LOAD_CONST               1
             1190  BINARY_SUBTRACT  
             1192  LOAD_FAST                'idxend'
             1194  LOAD_FAST                'idxstart'
             1196  BINARY_SUBTRACT  
             1198  CALL_METHOD_3         3  '3 positional arguments'
             1200  LOAD_METHOD              astype
             1202  LOAD_GLOBAL              int
             1204  CALL_METHOD_1         1  '1 positional argument'
             1206  STORE_FAST               'idxlist'

 L. 482      1208  LOAD_FAST                'idxend'
             1210  STORE_FAST               'idxstart'

 L. 483      1212  LOAD_GLOBAL              basic_mdt
             1214  LOAD_METHOD              retrieveDictByIndex
             1216  LOAD_FAST                '_seisdict'
             1218  LOAD_FAST                'idxlist'
             1220  CALL_METHOD_2         2  '2 positional arguments'
             1222  STORE_FAST               '_dict'

 L. 485      1224  LOAD_FAST                '_dict'
             1226  LOAD_STR                 'Inline'
             1228  BINARY_SUBSCR    
             1230  STORE_FAST               '_targetdata'

 L. 486      1232  LOAD_GLOBAL              np
             1234  LOAD_ATTR                concatenate
             1236  LOAD_FAST                '_targetdata'
             1238  LOAD_FAST                '_dict'
             1240  LOAD_STR                 'Crossline'
             1242  BINARY_SUBSCR    
             1244  BUILD_TUPLE_2         2 
             1246  LOAD_CONST               1
             1248  LOAD_CONST               ('axis',)
             1250  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1252  STORE_FAST               '_targetdata'

 L. 487      1254  LOAD_GLOBAL              np
             1256  LOAD_ATTR                concatenate
             1258  LOAD_FAST                '_targetdata'
             1260  LOAD_FAST                '_dict'
             1262  LOAD_STR                 'Z'
             1264  BINARY_SUBSCR    
             1266  BUILD_TUPLE_2         2 
             1268  LOAD_CONST               1
             1270  LOAD_CONST               ('axis',)
             1272  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1274  STORE_FAST               '_targetdata'

 L. 488      1276  SETUP_LOOP         1348  'to 1348'
             1278  LOAD_FAST                '_featurelist'
             1280  GET_ITER         
             1282  FOR_ITER           1346  'to 1346'
             1284  STORE_FAST               'f'

 L. 489      1286  LOAD_FAST                'self'
             1288  LOAD_ATTR                seisdata
             1290  LOAD_FAST                'f'
             1292  BINARY_SUBSCR    
             1294  STORE_FAST               '_data'

 L. 490      1296  LOAD_GLOBAL              seis_ays
             1298  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1300  LOAD_FAST                '_data'
             1302  LOAD_FAST                '_targetdata'
             1304  LOAD_FAST                'self'
             1306  LOAD_ATTR                survinfo

 L. 491      1308  LOAD_FAST                '_wdinl'
             1310  LOAD_FAST                '_wdxl'
             1312  LOAD_FAST                '_wdz'

 L. 492      1314  LOAD_CONST               False
             1316  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1318  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1320  LOAD_CONST               None
             1322  LOAD_CONST               None
             1324  BUILD_SLICE_2         2 
             1326  LOAD_CONST               3
             1328  LOAD_CONST               None
             1330  BUILD_SLICE_2         2 
             1332  BUILD_TUPLE_2         2 
             1334  BINARY_SUBSCR    
             1336  LOAD_FAST                '_dict'
             1338  LOAD_FAST                'f'
             1340  STORE_SUBSCR     
         1342_1344  JUMP_BACK          1282  'to 1282'
             1346  POP_BLOCK        
           1348_0  COME_FROM_LOOP     1276  '1276'

 L. 493      1348  LOAD_FAST                '_target'
             1350  LOAD_FAST                '_featurelist'
             1352  COMPARE_OP               not-in
         1354_1356  POP_JUMP_IF_FALSE  1408  'to 1408'

 L. 494      1358  LOAD_FAST                'self'
             1360  LOAD_ATTR                seisdata
             1362  LOAD_FAST                '_target'
             1364  BINARY_SUBSCR    
             1366  STORE_FAST               '_data'

 L. 495      1368  LOAD_GLOBAL              seis_ays
             1370  LOAD_ATTR                retrieveSeisSampleFrom3DMat
             1372  LOAD_FAST                '_data'
             1374  LOAD_FAST                '_targetdata'

 L. 496      1376  LOAD_FAST                'self'
             1378  LOAD_ATTR                survinfo

 L. 497      1380  LOAD_CONST               False
             1382  LOAD_CONST               ('seisinfo', 'verbose')
             1384  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1386  LOAD_CONST               None
             1388  LOAD_CONST               None
             1390  BUILD_SLICE_2         2 
             1392  LOAD_CONST               3
             1394  LOAD_CONST               None
             1396  BUILD_SLICE_2         2 
             1398  BUILD_TUPLE_2         2 
             1400  BINARY_SUBSCR    
             1402  LOAD_FAST                '_dict'
             1404  LOAD_FAST                '_target'
             1406  STORE_SUBSCR     
           1408_0  COME_FROM          1354  '1354'

 L. 498      1408  LOAD_GLOBAL              np
             1410  LOAD_METHOD              round
             1412  LOAD_FAST                '_dict'
             1414  LOAD_FAST                '_target'
             1416  BINARY_SUBSCR    
             1418  CALL_METHOD_1         1  '1 positional argument'
             1420  LOAD_METHOD              astype
             1422  LOAD_GLOBAL              int
             1424  CALL_METHOD_1         1  '1 positional argument'
             1426  LOAD_FAST                '_dict'
             1428  LOAD_FAST                '_target'
             1430  STORE_SUBSCR     

 L. 500      1432  LOAD_GLOBAL              ml_fnn
             1434  LOAD_ATTR                evaluateFNNClassifier
             1436  LOAD_FAST                '_dict'

 L. 501      1438  LOAD_FAST                'self'
             1440  LOAD_ATTR                modelpath

 L. 502      1442  LOAD_FAST                'self'
             1444  LOAD_ATTR                modelname

 L. 503      1446  LOAD_FAST                '_batch'

 L. 504      1448  LOAD_CONST               True
             1450  LOAD_CONST               ('fnnpath', 'fnnname', 'batchsize', 'verbose')
             1452  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1454  STORE_FAST               '_confmatrix'

 L. 505      1456  LOAD_FAST                '_result'
             1458  LOAD_FAST                '_confmatrix'
             1460  LOAD_STR                 'confusion_matrix'
             1462  BINARY_SUBSCR    
             1464  BINARY_ADD       
             1466  STORE_FAST               '_result'

 L. 507      1468  LOAD_FAST                '_pgsdlg'
             1470  LOAD_METHOD              setValue
             1472  LOAD_FAST                'i'
             1474  LOAD_CONST               1
             1476  BINARY_ADD       
             1478  CALL_METHOD_1         1  '1 positional argument'
             1480  POP_TOP          
         1482_1484  JUMP_BACK          1096  'to 1096'
             1486  POP_BLOCK        
           1488_0  COME_FROM_LOOP     1084  '1084'

 L. 509      1488  LOAD_GLOBAL              print
             1490  LOAD_STR                 'Done'
             1492  CALL_FUNCTION_1       1  '1 positional argument'
             1494  POP_TOP          

 L. 511      1496  LOAD_FAST                '_result'
             1498  LOAD_CONST               0
             1500  LOAD_CONST               1
             1502  LOAD_CONST               None
             1504  BUILD_SLICE_2         2 
             1506  BUILD_TUPLE_2         2 
             1508  BINARY_SUBSCR    
             1510  LOAD_FAST                '_nloop'
             1512  BINARY_TRUE_DIVIDE
             1514  LOAD_FAST                '_result'
             1516  LOAD_CONST               0
             1518  LOAD_CONST               1
             1520  LOAD_CONST               None
             1522  BUILD_SLICE_2         2 
             1524  BUILD_TUPLE_2         2 
             1526  STORE_SUBSCR     

 L. 512      1528  LOAD_FAST                '_result'
             1530  LOAD_CONST               1
             1532  LOAD_CONST               None
             1534  BUILD_SLICE_2         2 
             1536  LOAD_CONST               0
             1538  BUILD_TUPLE_2         2 
             1540  BINARY_SUBSCR    
             1542  LOAD_FAST                '_nloop'
             1544  BINARY_TRUE_DIVIDE
             1546  LOAD_FAST                '_result'
             1548  LOAD_CONST               1
             1550  LOAD_CONST               None
             1552  BUILD_SLICE_2         2 
             1554  LOAD_CONST               0
             1556  BUILD_TUPLE_2         2 
             1558  STORE_SUBSCR     

 L. 513      1560  LOAD_GLOBAL              print
             1562  LOAD_FAST                '_result'
             1564  CALL_FUNCTION_1       1  '1 positional argument'
             1566  POP_TOP          

 L. 518      1568  LOAD_GLOBAL              QtWidgets
             1570  LOAD_METHOD              QDialog
             1572  CALL_METHOD_0         0  '0 positional arguments'
             1574  STORE_FAST               '_viewmlconfmat'

 L. 519      1576  LOAD_GLOBAL              gui_viewmlconfmat
             1578  CALL_FUNCTION_0       0  '0 positional arguments'
             1580  STORE_FAST               '_gui'

 L. 520      1582  LOAD_FAST                '_result'
             1584  LOAD_FAST                '_gui'
             1586  STORE_ATTR               confmat

 L. 521      1588  LOAD_FAST                '_gui'
             1590  LOAD_METHOD              setupGUI
             1592  LOAD_FAST                '_viewmlconfmat'
             1594  CALL_METHOD_1         1  '1 positional argument'
             1596  POP_TOP          

 L. 522      1598  LOAD_FAST                '_viewmlconfmat'
             1600  LOAD_METHOD              exec
             1602  CALL_METHOD_0         0  '0 positional arguments'
             1604  POP_TOP          

 L. 523      1606  LOAD_FAST                '_viewmlconfmat'
             1608  LOAD_METHOD              show
             1610  CALL_METHOD_0         0  '0 positional arguments'
             1612  POP_TOP          

Parse error at or near `CALL_METHOD_0' instruction at offset 1610

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
    EvaluateMlMlp = QtWidgets.QWidget()
    gui = evaluatemlmlp()
    gui.setupGUI(EvaluateMlMlp)
    EvaluateMlMlp.show()
    sys.exit(app.exec_())