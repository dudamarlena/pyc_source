# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\applymlmlp4prob.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 28959 bytes
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

class applymlmlp4prob(object):
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

    def setupGUI(self, ApplyMlMlp4Prob):
        ApplyMlMlp4Prob.setObjectName('ApplyMlMlp4Prob')
        ApplyMlMlp4Prob.setFixedSize(810, 470)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ApplyMlMlp4Prob.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ApplyMlMlp4Prob)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ApplyMlMlp4Prob)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ApplyMlMlp4Prob)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 160))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblpatchsize = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblpatchsize.setObjectName('lblpatchsize')
        self.lblpatchsize.setGeometry(QtCore.QRect(10, 230, 80, 30))
        self.lblpatchheight = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblpatchheight.setObjectName('lblpatchheight')
        self.lblpatchheight.setGeometry(QtCore.QRect(110, 230, 50, 30))
        self.ldtpatchheight = QtWidgets.QLineEdit(ApplyMlMlp4Prob)
        self.ldtpatchheight.setObjectName('ldtpatchheight')
        self.ldtpatchheight.setGeometry(QtCore.QRect(160, 230, 40, 30))
        self.lblpatchwidth = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblpatchwidth.setObjectName('lblpatchwidth')
        self.lblpatchwidth.setGeometry(QtCore.QRect(205, 230, 50, 30))
        self.ldtpatchwidth = QtWidgets.QLineEdit(ApplyMlMlp4Prob)
        self.ldtpatchwidth.setObjectName('ldtpatchwidth')
        self.ldtpatchwidth.setGeometry(QtCore.QRect(255, 230, 40, 30))
        self.lblpatchdepth = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblpatchdepth.setObjectName('lblpatchdepth')
        self.lblpatchdepth.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtpatchdepth = QtWidgets.QLineEdit(ApplyMlMlp4Prob)
        self.ldtpatchdepth.setObjectName('ldtpatchdepth')
        self.ldtpatchdepth.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblold = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblold.setObjectName('lblold')
        self.lblold.setGeometry(QtCore.QRect(50, 270, 60, 30))
        self.lbloldlength = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lbloldlength.setObjectName('lbloldlength')
        self.lbloldlength.setGeometry(QtCore.QRect(110, 270, 50, 30))
        self.ldtoldlength = QtWidgets.QLineEdit(ApplyMlMlp4Prob)
        self.ldtoldlength.setObjectName('ldtoldlength')
        self.ldtoldlength.setGeometry(QtCore.QRect(160, 270, 40, 30))
        self.lbloldtotal = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lbloldtotal.setObjectName('lbloldtotal')
        self.lbloldtotal.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtoldtotal = QtWidgets.QLineEdit(ApplyMlMlp4Prob)
        self.ldtoldtotal.setObjectName('ldtoldtotal')
        self.ldtoldtotal.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lblnew = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblnew.setObjectName('lblnew')
        self.lblnew.setGeometry(QtCore.QRect(50, 310, 60, 30))
        self.lblnewlength = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblnewlength.setObjectName('lblnewlength')
        self.lblnewlength.setGeometry(QtCore.QRect(110, 310, 50, 30))
        self.ldtnewlength = QtWidgets.QLineEdit(ApplyMlMlp4Prob)
        self.ldtnewlength.setObjectName('ldtnewlength')
        self.ldtnewlength.setGeometry(QtCore.QRect(160, 310, 40, 30))
        self.lblnewtotal = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblnewtotal.setObjectName('lblnewtotal')
        self.lblnewtotal.setGeometry(QtCore.QRect(300, 310, 50, 30))
        self.ldtnewtotal = QtWidgets.QLineEdit(ApplyMlMlp4Prob)
        self.ldtnewtotal.setObjectName('ldtnewtotal')
        self.ldtnewtotal.setGeometry(QtCore.QRect(350, 310, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ApplyMlMlp4Prob)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnlayer = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblnlayer.setObjectName('lblnlayer')
        self.lblnlayer.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnlayer = QtWidgets.QLineEdit(ApplyMlMlp4Prob)
        self.ldtnlayer.setObjectName('ldtnlayer')
        self.ldtnlayer.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnlayer = QtWidgets.QTableWidget(ApplyMlMlp4Prob)
        self.twgnlayer.setObjectName('twgnlayer')
        self.twgnlayer.setGeometry(QtCore.QRect(610, 100, 180, 160))
        self.twgnlayer.setColumnCount(2)
        self.twgnlayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnlayer.verticalHeader().hide()
        self.lblpara = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(410, 270, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(410, 310, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ApplyMlMlp4Prob)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(550, 310, 40, 30))
        self.lblsave = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(410, 360, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ApplyMlMlp4Prob)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(550, 360, 100, 30))
        self.lbltarget = QtWidgets.QLabel(ApplyMlMlp4Prob)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(650, 310, 50, 30))
        self.lwgtarget = QtWidgets.QListWidget(ApplyMlMlp4Prob)
        self.lwgtarget.setObjectName('lwgtarget')
        self.lwgtarget.setGeometry(QtCore.QRect(700, 310, 90, 70))
        self.lwgtarget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.btnapply = QtWidgets.QPushButton(ApplyMlMlp4Prob)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(320, 410, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ApplyMlMlp4Prob)
        self.msgbox.setObjectName('msgbox')
        _center_x = ApplyMlMlp4Prob.geometry().center().x()
        _center_y = ApplyMlMlp4Prob.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ApplyMlMlp4Prob)
        QtCore.QMetaObject.connectSlotsByName(ApplyMlMlp4Prob)

    def retranslateGUI(self, ApplyMlMlp4Prob):
        self.dialog = ApplyMlMlp4Prob
        _translate = QtCore.QCoreApplication.translate
        ApplyMlMlp4Prob.setWindowTitle(_translate('ApplyMlMlp4Prob', 'Apply MLP for probability'))
        self.lblfrom.setText(_translate('ApplyMlMlp4Prob', 'Select network:'))
        self.ldtfrom.setText(_translate('ApplyMlMlp4Prob', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ApplyMlMlp4Prob', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ApplyMlMlp4Prob', 'Training features:'))
        self.lblpatchsize.setText(_translate('ApplyMlMlp4Prob', 'Patch\nsize:'))
        self.lblpatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpatchheight.setText(_translate('ApplyMlMlp4Prob', 'height=\ntime/depth'))
        self.ldtpatchheight.setText(_translate('ApplyMlMlp4Prob', '1'))
        self.ldtpatchheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpatchwidth.setText(_translate('ApplyMlMlp4Prob', 'width=\ncrossline'))
        self.ldtpatchwidth.setText(_translate('ApplyMlMlp4Prob', '1'))
        self.ldtpatchwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpatchdepth.setText(_translate('ApplyMlMlp4Prob', 'depth=\ninline'))
        self.ldtpatchdepth.setText(_translate('ApplyMlMlp4Prob', '1'))
        self.ldtpatchdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtpatchheight.textChanged.connect(self.changeLdtPatchSize)
        self.ldtpatchwidth.textChanged.connect(self.changeLdtPatchSize)
        self.ldtpatchdepth.textChanged.connect(self.changeLdtPatchSize)
        self.lblold.setText(_translate('ApplyMlMlp4Prob', 'available:'))
        self.lbloldlength.setText(_translate('ApplyMlMlp4Prob', 'length ='))
        self.ldtoldlength.setText(_translate('ApplyMlMlp4Prob', ''))
        self.ldtoldlength.setEnabled(False)
        self.ldtoldlength.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldtotal.setText(_translate('ApplyMlMlp4Prob', 'total ='))
        self.ldtoldtotal.setText(_translate('ApplyMlMlp4Prob', ''))
        self.ldtoldtotal.setEnabled(False)
        self.ldtoldtotal.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnew.setText(_translate('ApplyMlMlp4Prob', 'expected:'))
        self.lblnewlength.setText(_translate('ApplyMlMlp4Prob', 'length ='))
        self.ldtnewlength.setText(_translate('ApplyMlMlp4Prob', ''))
        self.ldtnewlength.setEnabled(False)
        self.ldtnewlength.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewtotal.setText(_translate('ApplyMlMlp4Prob', 'total ='))
        self.ldtnewtotal.setText(_translate('ApplyMlMlp4Prob', ''))
        self.ldtnewtotal.setEnabled(False)
        self.ldtnewtotal.setAlignment(QtCore.Qt.AlignCenter)
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblnetwork.setText(_translate('ApplyMlMlp4Prob', 'Pre-trained MLP architecture:'))
        self.btnviewnetwork.setText(_translate('ApplyMlMlp4Prob', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnlayer.setText(_translate('ApplyMlMlp4Prob', 'No. of MLP layers:'))
        self.lblnlayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnlayer.setText(_translate('ApplyMlMlp4Prob', ''))
        self.ldtnlayer.setEnabled(False)
        self.ldtnlayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnlayer.textChanged.connect(self.changeLdtNlayer)
        self.twgnlayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblpara.setText(_translate('ApplyMlMlp4Prob', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ApplyMlMlp4Prob', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ApplyMlMlp4Prob', '10000'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('ApplyMlMlp4Prob', 'Output prefix='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ApplyMlMlp4Prob', 'mlp_prob_'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltarget.setText(_translate('ApplyMlMlp4Prob', 'Target ='))
        self.btnapply.setText(_translate('ApplyMlMlp4Prob', 'Apply MLP'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnApplyMlMlp4Prob)

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
            self.lwgtarget.clear()
            self.lwgtarget.addItems([str(_t) for _t in range(self.modelinfo['number_label'])])
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
            self.lwgtarget.clear()

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

    def clickBtnApplyMlMlp4Prob--- This code section failed: ---

 L. 375         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 377         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 378        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in ApplyMlMlp4Prob: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 379        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 380        44  LOAD_STR                 'Apply MLP'

 L. 381        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 382        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 384        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkFNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 385        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in ApplyMlMlp4Prob: No MLP network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 386        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 387       100  LOAD_STR                 'Apply MLP'

 L. 388       102  LOAD_STR                 'No MLP network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 389       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 391       112  LOAD_FAST                'self'
              114  LOAD_ATTR                modelinfo
              116  LOAD_STR                 'feature_list'
              118  BINARY_SUBSCR    
              120  STORE_FAST               '_featurelist'

 L. 393       122  SETUP_LOOP          198  'to 198'
              124  LOAD_FAST                '_featurelist'
              126  GET_ITER         
            128_0  COME_FROM           144  '144'
              128  FOR_ITER            196  'to 196'
              130  STORE_FAST               'f'

 L. 394       132  LOAD_FAST                'self'
              134  LOAD_METHOD              checkSeisData
              136  LOAD_FAST                'f'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_CONST               False
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   128  'to 128'

 L. 395       146  LOAD_GLOBAL              vis_msg
              148  LOAD_ATTR                print
              150  LOAD_STR                 "ERROR in ApplyMlMlp4Prob: Feature '%s' not found in seismic data"
              152  LOAD_FAST                'f'
              154  BINARY_MODULO    

 L. 396       156  LOAD_STR                 'error'
              158  LOAD_CONST               ('type',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  POP_TOP          

 L. 397       164  LOAD_GLOBAL              QtWidgets
              166  LOAD_ATTR                QMessageBox
              168  LOAD_METHOD              critical
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                msgbox

 L. 398       174  LOAD_STR                 'Apply MLP'

 L. 399       176  LOAD_STR                 "Feature '"
              178  LOAD_FAST                'f'
              180  BINARY_ADD       
              182  LOAD_STR                 "' not found in seismic data"
              184  BINARY_ADD       
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 400       190  LOAD_CONST               None
              192  RETURN_VALUE     
              194  JUMP_BACK           128  'to 128'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      122  '122'

 L. 402       198  LOAD_FAST                'self'
              200  LOAD_ATTR                ldtoldlength
              202  LOAD_METHOD              text
              204  CALL_METHOD_0         0  '0 positional arguments'
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                ldtnewlength
              210  LOAD_METHOD              text
              212  CALL_METHOD_0         0  '0 positional arguments'
              214  COMPARE_OP               !=
              216  POP_JUMP_IF_TRUE    240  'to 240'

 L. 403       218  LOAD_FAST                'self'
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

 L. 404       240  LOAD_GLOBAL              vis_msg
              242  LOAD_ATTR                print
              244  LOAD_STR                 'ERROR in ApplyMlMlp4Prob: Feature length not match'
              246  LOAD_STR                 'error'
              248  LOAD_CONST               ('type',)
              250  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              252  POP_TOP          

 L. 405       254  LOAD_GLOBAL              QtWidgets
              256  LOAD_ATTR                QMessageBox
              258  LOAD_METHOD              critical
              260  LOAD_FAST                'self'
              262  LOAD_ATTR                msgbox

 L. 406       264  LOAD_STR                 'Apply MLP'

 L. 407       266  LOAD_STR                 'Feature length not match'
              268  CALL_METHOD_3         3  '3 positional arguments'
              270  POP_TOP          

 L. 408       272  LOAD_CONST               None
              274  RETURN_VALUE     
            276_0  COME_FROM           236  '236'

 L. 410       276  LOAD_GLOBAL              basic_data
              278  LOAD_METHOD              str2int
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                ldtpatchheight
              284  LOAD_METHOD              text
              286  CALL_METHOD_0         0  '0 positional arguments'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  STORE_FAST               '_patch_height'

 L. 411       292  LOAD_GLOBAL              basic_data
              294  LOAD_METHOD              str2int
              296  LOAD_FAST                'self'
              298  LOAD_ATTR                ldtpatchwidth
              300  LOAD_METHOD              text
              302  CALL_METHOD_0         0  '0 positional arguments'
              304  CALL_METHOD_1         1  '1 positional argument'
              306  STORE_FAST               '_patch_width'

 L. 412       308  LOAD_GLOBAL              basic_data
              310  LOAD_METHOD              str2int
              312  LOAD_FAST                'self'
              314  LOAD_ATTR                ldtpatchdepth
              316  LOAD_METHOD              text
              318  CALL_METHOD_0         0  '0 positional arguments'
              320  CALL_METHOD_1         1  '1 positional argument'
              322  STORE_FAST               '_patch_depth'

 L. 413       324  LOAD_FAST                '_patch_height'
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

 L. 414       354  LOAD_FAST                '_patch_height'
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

 L. 415       384  LOAD_GLOBAL              vis_msg
              386  LOAD_ATTR                print
              388  LOAD_STR                 'ERROR in ApplyMlMlp4Prob: Non-positive feature size'
              390  LOAD_STR                 'error'
              392  LOAD_CONST               ('type',)
              394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              396  POP_TOP          

 L. 416       398  LOAD_GLOBAL              QtWidgets
              400  LOAD_ATTR                QMessageBox
              402  LOAD_METHOD              critical
              404  LOAD_FAST                'self'
              406  LOAD_ATTR                msgbox

 L. 417       408  LOAD_STR                 'Apply MLP'

 L. 418       410  LOAD_STR                 'Non-positive feature size'
              412  CALL_METHOD_3         3  '3 positional arguments'
              414  POP_TOP          

 L. 419       416  LOAD_CONST               None
              418  RETURN_VALUE     
            420_0  COME_FROM           380  '380'

 L. 421       420  LOAD_GLOBAL              basic_data
              422  LOAD_METHOD              str2int
              424  LOAD_FAST                'self'
              426  LOAD_ATTR                ldtbatchsize
              428  LOAD_METHOD              text
              430  CALL_METHOD_0         0  '0 positional arguments'
              432  CALL_METHOD_1         1  '1 positional argument'
              434  STORE_FAST               '_batch'

 L. 422       436  LOAD_FAST                '_batch'
              438  LOAD_CONST               False
              440  COMPARE_OP               is
          442_444  POP_JUMP_IF_TRUE    456  'to 456'
              446  LOAD_FAST                '_batch'
              448  LOAD_CONST               1
              450  COMPARE_OP               <
          452_454  POP_JUMP_IF_FALSE   492  'to 492'
            456_0  COME_FROM           442  '442'

 L. 423       456  LOAD_GLOBAL              vis_msg
              458  LOAD_ATTR                print
              460  LOAD_STR                 'ERROR in ApplyMlMlp4Prob: Non-positive batch size'
              462  LOAD_STR                 'error'
              464  LOAD_CONST               ('type',)
              466  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              468  POP_TOP          

 L. 424       470  LOAD_GLOBAL              QtWidgets
              472  LOAD_ATTR                QMessageBox
              474  LOAD_METHOD              critical
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                msgbox

 L. 425       480  LOAD_STR                 'Apply MLP'

 L. 426       482  LOAD_STR                 'Non-positive batch size'
              484  CALL_METHOD_3         3  '3 positional arguments'
              486  POP_TOP          

 L. 427       488  LOAD_CONST               None
              490  RETURN_VALUE     
            492_0  COME_FROM           452  '452'

 L. 428       492  LOAD_GLOBAL              len
              494  LOAD_FAST                'self'
              496  LOAD_ATTR                ldtsave
              498  LOAD_METHOD              text
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  CALL_FUNCTION_1       1  '1 positional argument'
              504  LOAD_CONST               1
              506  COMPARE_OP               <
          508_510  POP_JUMP_IF_FALSE   548  'to 548'

 L. 429       512  LOAD_GLOBAL              vis_msg
              514  LOAD_ATTR                print
              516  LOAD_STR                 'ERROR in ApplyMlMlp4Prob: No prefix specified'
              518  LOAD_STR                 'error'
              520  LOAD_CONST               ('type',)
              522  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              524  POP_TOP          

 L. 430       526  LOAD_GLOBAL              QtWidgets
              528  LOAD_ATTR                QMessageBox
              530  LOAD_METHOD              critical
              532  LOAD_FAST                'self'
              534  LOAD_ATTR                msgbox

 L. 431       536  LOAD_STR                 'Apply MLP'

 L. 432       538  LOAD_STR                 'No prefix specified'
              540  CALL_METHOD_3         3  '3 positional arguments'
              542  POP_TOP          

 L. 433       544  LOAD_CONST               None
              546  RETURN_VALUE     
            548_0  COME_FROM           508  '508'

 L. 435       548  LOAD_GLOBAL              len
              550  LOAD_FAST                'self'
              552  LOAD_ATTR                lwgtarget
              554  LOAD_METHOD              selectedItems
              556  CALL_METHOD_0         0  '0 positional arguments'
              558  CALL_FUNCTION_1       1  '1 positional argument'
              560  LOAD_CONST               1
              562  COMPARE_OP               <
          564_566  POP_JUMP_IF_FALSE   604  'to 604'

 L. 436       568  LOAD_GLOBAL              vis_msg
              570  LOAD_ATTR                print
              572  LOAD_STR                 'ERROR in ApplyMlMlp4Prob: No target label specified'
              574  LOAD_STR                 'error'
              576  LOAD_CONST               ('type',)
              578  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              580  POP_TOP          

 L. 437       582  LOAD_GLOBAL              QtWidgets
              584  LOAD_ATTR                QMessageBox
              586  LOAD_METHOD              critical
              588  LOAD_FAST                'self'
              590  LOAD_ATTR                msgbox

 L. 438       592  LOAD_STR                 'Apply MLP'

 L. 439       594  LOAD_STR                 'No target label specified'
              596  CALL_METHOD_3         3  '3 positional arguments'
              598  POP_TOP          

 L. 440       600  LOAD_CONST               None
              602  RETURN_VALUE     
            604_0  COME_FROM           564  '564'

 L. 441       604  LOAD_LISTCOMP            '<code_object <listcomp>>'
              606  LOAD_STR                 'applymlmlp4prob.clickBtnApplyMlMlp4Prob.<locals>.<listcomp>'
              608  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              610  LOAD_FAST                'self'
              612  LOAD_ATTR                lwgtarget
              614  LOAD_METHOD              selectedItems
              616  CALL_METHOD_0         0  '0 positional arguments'
              618  GET_ITER         
              620  CALL_FUNCTION_1       1  '1 positional argument'
              622  STORE_FAST               '_labellist'

 L. 442       624  SETUP_LOOP          778  'to 778'
              626  LOAD_FAST                '_labellist'
              628  GET_ITER         
            630_0  COME_FROM           766  '766'
            630_1  COME_FROM           686  '686'
            630_2  COME_FROM           660  '660'
              630  FOR_ITER            776  'to 776'
              632  STORE_FAST               '_label'

 L. 443       634  LOAD_FAST                'self'
              636  LOAD_ATTR                ldtsave
              638  LOAD_METHOD              text
              640  CALL_METHOD_0         0  '0 positional arguments'
              642  LOAD_GLOBAL              str
              644  LOAD_FAST                '_label'
              646  CALL_FUNCTION_1       1  '1 positional argument'
              648  BINARY_ADD       
              650  LOAD_FAST                'self'
              652  LOAD_ATTR                seisdata
              654  LOAD_METHOD              keys
              656  CALL_METHOD_0         0  '0 positional arguments'
              658  COMPARE_OP               in
          660_662  POP_JUMP_IF_FALSE   630  'to 630'

 L. 444       664  LOAD_FAST                'self'
              666  LOAD_METHOD              checkSeisData
              668  LOAD_FAST                'self'
              670  LOAD_ATTR                ldtsave
              672  LOAD_METHOD              text
              674  CALL_METHOD_0         0  '0 positional arguments'
              676  LOAD_GLOBAL              str
              678  LOAD_FAST                '_label'
              680  CALL_FUNCTION_1       1  '1 positional argument'
              682  BINARY_ADD       
              684  CALL_METHOD_1         1  '1 positional argument'
          686_688  POP_JUMP_IF_FALSE   630  'to 630'

 L. 445       690  LOAD_GLOBAL              QtWidgets
              692  LOAD_ATTR                QMessageBox
              694  LOAD_METHOD              question
              696  LOAD_FAST                'self'
              698  LOAD_ATTR                msgbox
              700  LOAD_STR                 'Apply MLP'

 L. 446       702  LOAD_FAST                'self'
              704  LOAD_ATTR                ldtsave
              706  LOAD_METHOD              text
              708  CALL_METHOD_0         0  '0 positional arguments'
              710  LOAD_STR                 ' already exists. Overwrite?'
              712  BINARY_ADD       

 L. 447       714  LOAD_GLOBAL              QtWidgets
              716  LOAD_ATTR                QMessageBox
              718  LOAD_ATTR                Yes
              720  LOAD_GLOBAL              QtWidgets
              722  LOAD_ATTR                QMessageBox
              724  LOAD_ATTR                No
              726  BINARY_OR        

 L. 448       728  LOAD_GLOBAL              QtWidgets
              730  LOAD_ATTR                QMessageBox
              732  LOAD_ATTR                No
              734  CALL_METHOD_5         5  '5 positional arguments'
              736  STORE_FAST               'reply'

 L. 449       738  LOAD_FAST                'reply'
              740  LOAD_GLOBAL              QtWidgets
              742  LOAD_ATTR                QMessageBox
              744  LOAD_ATTR                No
              746  COMPARE_OP               ==
          748_750  POP_JUMP_IF_FALSE   756  'to 756'

 L. 450       752  LOAD_CONST               None
              754  RETURN_VALUE     
            756_0  COME_FROM           748  '748'

 L. 451       756  LOAD_FAST                'reply'
              758  LOAD_GLOBAL              QtWidgets
              760  LOAD_ATTR                QMessageBox
              762  LOAD_ATTR                Yes
              764  COMPARE_OP               ==
          766_768  POP_JUMP_IF_FALSE   630  'to 630'

 L. 452       770  BREAK_LOOP       
          772_774  JUMP_BACK           630  'to 630'
              776  POP_BLOCK        
            778_0  COME_FROM_LOOP      624  '624'

 L. 454       778  LOAD_CONST               2
              780  LOAD_GLOBAL              int
              782  LOAD_FAST                '_patch_height'
              784  LOAD_CONST               2
              786  BINARY_TRUE_DIVIDE
              788  CALL_FUNCTION_1       1  '1 positional argument'
              790  BINARY_MULTIPLY  
              792  LOAD_CONST               1
              794  BINARY_ADD       
              796  STORE_FAST               '_patch_height'

 L. 455       798  LOAD_CONST               2
              800  LOAD_GLOBAL              int
              802  LOAD_FAST                '_patch_width'
              804  LOAD_CONST               2
              806  BINARY_TRUE_DIVIDE
              808  CALL_FUNCTION_1       1  '1 positional argument'
              810  BINARY_MULTIPLY  
              812  LOAD_CONST               1
              814  BINARY_ADD       
              816  STORE_FAST               '_patch_width'

 L. 456       818  LOAD_CONST               2
              820  LOAD_GLOBAL              int
              822  LOAD_FAST                '_patch_depth'
              824  LOAD_CONST               2
              826  BINARY_TRUE_DIVIDE
              828  CALL_FUNCTION_1       1  '1 positional argument'
              830  BINARY_MULTIPLY  
              832  LOAD_CONST               1
              834  BINARY_ADD       
              836  STORE_FAST               '_patch_depth'

 L. 458       838  LOAD_GLOBAL              np
              840  LOAD_METHOD              shape
              842  LOAD_FAST                'self'
              844  LOAD_ATTR                seisdata
              846  LOAD_FAST                '_featurelist'
              848  LOAD_CONST               0
              850  BINARY_SUBSCR    
              852  BINARY_SUBSCR    
              854  CALL_METHOD_1         1  '1 positional argument'
              856  LOAD_CONST               0
              858  BINARY_SUBSCR    
              860  STORE_FAST               '_nsample'

 L. 460       862  LOAD_GLOBAL              int
              864  LOAD_GLOBAL              np
              866  LOAD_METHOD              ceil
              868  LOAD_FAST                '_nsample'
              870  LOAD_FAST                '_batch'
              872  BINARY_TRUE_DIVIDE
              874  CALL_METHOD_1         1  '1 positional argument'
              876  CALL_FUNCTION_1       1  '1 positional argument'
              878  STORE_FAST               '_nloop'

 L. 463       880  LOAD_GLOBAL              QtWidgets
              882  LOAD_METHOD              QProgressDialog
              884  CALL_METHOD_0         0  '0 positional arguments'
              886  STORE_FAST               '_pgsdlg'

 L. 464       888  LOAD_GLOBAL              QtGui
              890  LOAD_METHOD              QIcon
              892  CALL_METHOD_0         0  '0 positional arguments'
              894  STORE_FAST               'icon'

 L. 465       896  LOAD_FAST                'icon'
              898  LOAD_METHOD              addPixmap
              900  LOAD_GLOBAL              QtGui
              902  LOAD_METHOD              QPixmap
              904  LOAD_GLOBAL              os
              906  LOAD_ATTR                path
              908  LOAD_METHOD              join
              910  LOAD_FAST                'self'
              912  LOAD_ATTR                iconpath
              914  LOAD_STR                 'icons/apply.png'
              916  CALL_METHOD_2         2  '2 positional arguments'
              918  CALL_METHOD_1         1  '1 positional argument'

 L. 466       920  LOAD_GLOBAL              QtGui
              922  LOAD_ATTR                QIcon
              924  LOAD_ATTR                Normal
              926  LOAD_GLOBAL              QtGui
              928  LOAD_ATTR                QIcon
              930  LOAD_ATTR                Off
              932  CALL_METHOD_3         3  '3 positional arguments'
              934  POP_TOP          

 L. 467       936  LOAD_FAST                '_pgsdlg'
              938  LOAD_METHOD              setWindowIcon
              940  LOAD_FAST                'icon'
              942  CALL_METHOD_1         1  '1 positional argument'
              944  POP_TOP          

 L. 468       946  LOAD_FAST                '_pgsdlg'
              948  LOAD_METHOD              setWindowTitle
              950  LOAD_STR                 'Apply MLP'
              952  CALL_METHOD_1         1  '1 positional argument'
              954  POP_TOP          

 L. 469       956  LOAD_FAST                '_pgsdlg'
              958  LOAD_METHOD              setCancelButton
              960  LOAD_CONST               None
              962  CALL_METHOD_1         1  '1 positional argument'
              964  POP_TOP          

 L. 470       966  LOAD_FAST                '_pgsdlg'
              968  LOAD_METHOD              setWindowFlags
              970  LOAD_GLOBAL              QtCore
              972  LOAD_ATTR                Qt
              974  LOAD_ATTR                WindowStaysOnTopHint
              976  CALL_METHOD_1         1  '1 positional argument'
              978  POP_TOP          

 L. 471       980  LOAD_FAST                '_pgsdlg'
              982  LOAD_METHOD              forceShow
              984  CALL_METHOD_0         0  '0 positional arguments'
              986  POP_TOP          

 L. 472       988  LOAD_FAST                '_pgsdlg'
              990  LOAD_METHOD              setFixedWidth
              992  LOAD_CONST               400
              994  CALL_METHOD_1         1  '1 positional argument'
              996  POP_TOP          

 L. 473       998  LOAD_FAST                '_pgsdlg'
             1000  LOAD_METHOD              setMaximum
             1002  LOAD_FAST                '_nloop'
             1004  CALL_METHOD_1         1  '1 positional argument'
             1006  POP_TOP          

 L. 476      1008  LOAD_GLOBAL              int
             1010  LOAD_FAST                '_patch_depth'
             1012  LOAD_CONST               2
             1014  BINARY_TRUE_DIVIDE
             1016  CALL_FUNCTION_1       1  '1 positional argument'
             1018  STORE_FAST               '_wdinl'

 L. 477      1020  LOAD_GLOBAL              int
             1022  LOAD_FAST                '_patch_width'
             1024  LOAD_CONST               2
             1026  BINARY_TRUE_DIVIDE
             1028  CALL_FUNCTION_1       1  '1 positional argument'
             1030  STORE_FAST               '_wdxl'

 L. 478      1032  LOAD_GLOBAL              int
             1034  LOAD_FAST                '_patch_height'
             1036  LOAD_CONST               2
             1038  BINARY_TRUE_DIVIDE
             1040  CALL_FUNCTION_1       1  '1 positional argument'
             1042  STORE_FAST               '_wdz'

 L. 480      1044  LOAD_GLOBAL              seis_ays
             1046  LOAD_METHOD              convertSeisInfoTo2DMat
             1048  LOAD_FAST                'self'
             1050  LOAD_ATTR                survinfo
             1052  CALL_METHOD_1         1  '1 positional argument'
             1054  STORE_FAST               '_seisdata'

 L. 482      1056  LOAD_GLOBAL              np
             1058  LOAD_METHOD              zeros
             1060  LOAD_FAST                '_nsample'
             1062  LOAD_GLOBAL              len
             1064  LOAD_FAST                '_labellist'
             1066  CALL_FUNCTION_1       1  '1 positional argument'
             1068  BUILD_LIST_2          2 
             1070  CALL_METHOD_1         1  '1 positional argument'
             1072  STORE_FAST               '_result'

 L. 483      1074  LOAD_CONST               0
             1076  STORE_FAST               'idxstart'

 L. 484  1078_1080  SETUP_LOOP         1356  'to 1356'
             1082  LOAD_GLOBAL              range
             1084  LOAD_FAST                '_nloop'
             1086  CALL_FUNCTION_1       1  '1 positional argument'
             1088  GET_ITER         
         1090_1092  FOR_ITER           1354  'to 1354'
             1094  STORE_FAST               'i'

 L. 486      1096  LOAD_GLOBAL              QtCore
             1098  LOAD_ATTR                QCoreApplication
             1100  LOAD_METHOD              instance
             1102  CALL_METHOD_0         0  '0 positional arguments'
             1104  LOAD_METHOD              processEvents
             1106  CALL_METHOD_0         0  '0 positional arguments'
             1108  POP_TOP          

 L. 488      1110  LOAD_GLOBAL              sys
             1112  LOAD_ATTR                stdout
             1114  LOAD_METHOD              write

 L. 489      1116  LOAD_STR                 '\r>>> Apply MLP, proceeding %.1f%% '
             1118  LOAD_GLOBAL              float
             1120  LOAD_FAST                'i'
             1122  CALL_FUNCTION_1       1  '1 positional argument'
             1124  LOAD_GLOBAL              float
             1126  LOAD_FAST                '_nloop'
             1128  CALL_FUNCTION_1       1  '1 positional argument'
             1130  BINARY_TRUE_DIVIDE
             1132  LOAD_CONST               100.0
             1134  BINARY_MULTIPLY  
             1136  BINARY_MODULO    
             1138  CALL_METHOD_1         1  '1 positional argument'
             1140  POP_TOP          

 L. 490      1142  LOAD_GLOBAL              sys
             1144  LOAD_ATTR                stdout
             1146  LOAD_METHOD              flush
             1148  CALL_METHOD_0         0  '0 positional arguments'
             1150  POP_TOP          

 L. 492      1152  LOAD_FAST                'idxstart'
             1154  LOAD_FAST                '_batch'
             1156  BINARY_ADD       
             1158  STORE_FAST               'idxend'

 L. 493      1160  LOAD_FAST                'idxend'
             1162  LOAD_FAST                '_nsample'
             1164  COMPARE_OP               >
         1166_1168  POP_JUMP_IF_FALSE  1174  'to 1174'

 L. 494      1170  LOAD_FAST                '_nsample'
             1172  STORE_FAST               'idxend'
           1174_0  COME_FROM          1166  '1166'

 L. 495      1174  LOAD_GLOBAL              np
             1176  LOAD_METHOD              linspace
             1178  LOAD_FAST                'idxstart'
             1180  LOAD_FAST                'idxend'
             1182  LOAD_CONST               1
             1184  BINARY_SUBTRACT  
             1186  LOAD_FAST                'idxend'
             1188  LOAD_FAST                'idxstart'
             1190  BINARY_SUBTRACT  
             1192  CALL_METHOD_3         3  '3 positional arguments'
             1194  LOAD_METHOD              astype
             1196  LOAD_GLOBAL              int
             1198  CALL_METHOD_1         1  '1 positional argument'
             1200  STORE_FAST               'idxlist'

 L. 496      1202  LOAD_FAST                'idxend'
             1204  STORE_FAST               'idxstart'

 L. 498      1206  LOAD_FAST                '_seisdata'
             1208  LOAD_FAST                'idxlist'
             1210  LOAD_CONST               0
             1212  LOAD_CONST               3
             1214  BUILD_SLICE_2         2 
             1216  BUILD_TUPLE_2         2 
             1218  BINARY_SUBSCR    
             1220  STORE_FAST               '_targetdata'

 L. 500      1222  BUILD_MAP_0           0 
             1224  STORE_FAST               '_dict'

 L. 501      1226  SETUP_LOOP         1298  'to 1298'
             1228  LOAD_FAST                '_featurelist'
             1230  GET_ITER         
             1232  FOR_ITER           1296  'to 1296'
             1234  STORE_FAST               'f'

 L. 502      1236  LOAD_FAST                'self'
             1238  LOAD_ATTR                seisdata
             1240  LOAD_FAST                'f'
             1242  BINARY_SUBSCR    
             1244  STORE_FAST               '_data'

 L. 503      1246  LOAD_GLOBAL              seis_ays
             1248  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1250  LOAD_FAST                '_data'
             1252  LOAD_FAST                '_targetdata'
             1254  LOAD_FAST                'self'
             1256  LOAD_ATTR                survinfo

 L. 504      1258  LOAD_FAST                '_wdinl'
             1260  LOAD_FAST                '_wdxl'
             1262  LOAD_FAST                '_wdz'

 L. 505      1264  LOAD_CONST               False
             1266  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1268  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1270  LOAD_CONST               None
             1272  LOAD_CONST               None
             1274  BUILD_SLICE_2         2 
             1276  LOAD_CONST               3
             1278  LOAD_CONST               None
             1280  BUILD_SLICE_2         2 
             1282  BUILD_TUPLE_2         2 
             1284  BINARY_SUBSCR    
             1286  LOAD_FAST                '_dict'
             1288  LOAD_FAST                'f'
             1290  STORE_SUBSCR     
         1292_1294  JUMP_BACK          1232  'to 1232'
             1296  POP_BLOCK        
           1298_0  COME_FROM_LOOP     1226  '1226'

 L. 506      1298  LOAD_GLOBAL              ml_fnn
             1300  LOAD_ATTR                probabilityFromFNNClassifier
             1302  LOAD_FAST                '_dict'

 L. 507      1304  LOAD_FAST                'self'
             1306  LOAD_ATTR                modelpath

 L. 508      1308  LOAD_FAST                'self'
             1310  LOAD_ATTR                modelname

 L. 509      1312  LOAD_FAST                '_labellist'

 L. 510      1314  LOAD_FAST                '_batch'

 L. 511      1316  LOAD_CONST               True
             1318  LOAD_CONST               ('fnnpath', 'fnnname', 'targetlist', 'batchsize', 'verbose')
             1320  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1322  LOAD_FAST                '_result'
             1324  LOAD_FAST                'idxlist'
             1326  LOAD_CONST               None
             1328  LOAD_CONST               None
             1330  BUILD_SLICE_2         2 
             1332  BUILD_TUPLE_2         2 
             1334  STORE_SUBSCR     

 L. 513      1336  LOAD_FAST                '_pgsdlg'
             1338  LOAD_METHOD              setValue
             1340  LOAD_FAST                'i'
             1342  LOAD_CONST               1
             1344  BINARY_ADD       
             1346  CALL_METHOD_1         1  '1 positional argument'
             1348  POP_TOP          
         1350_1352  JUMP_BACK          1090  'to 1090'
             1354  POP_BLOCK        
           1356_0  COME_FROM_LOOP     1078  '1078'

 L. 515      1356  LOAD_GLOBAL              print
             1358  LOAD_STR                 'Done'
             1360  CALL_FUNCTION_1       1  '1 positional argument'
             1362  POP_TOP          

 L. 517      1364  SETUP_LOOP         1482  'to 1482'
             1366  LOAD_GLOBAL              range
             1368  LOAD_GLOBAL              len
             1370  LOAD_FAST                '_labellist'
             1372  CALL_FUNCTION_1       1  '1 positional argument'
             1374  CALL_FUNCTION_1       1  '1 positional argument'
             1376  GET_ITER         
             1378  FOR_ITER           1480  'to 1480'
             1380  STORE_FAST               'i'

 L. 518      1382  LOAD_GLOBAL              np
             1384  LOAD_METHOD              transpose
             1386  LOAD_GLOBAL              np
             1388  LOAD_METHOD              reshape
             1390  LOAD_FAST                '_result'
             1392  LOAD_CONST               None
             1394  LOAD_CONST               None
             1396  BUILD_SLICE_2         2 
             1398  LOAD_FAST                'i'
             1400  LOAD_FAST                'i'
             1402  LOAD_CONST               1
             1404  BINARY_ADD       
             1406  BUILD_SLICE_2         2 
             1408  BUILD_TUPLE_2         2 
             1410  BINARY_SUBSCR    

 L. 519      1412  LOAD_FAST                'self'
             1414  LOAD_ATTR                survinfo
             1416  LOAD_STR                 'ILNum'
             1418  BINARY_SUBSCR    

 L. 520      1420  LOAD_FAST                'self'
             1422  LOAD_ATTR                survinfo
             1424  LOAD_STR                 'XLNum'
             1426  BINARY_SUBSCR    

 L. 521      1428  LOAD_FAST                'self'
             1430  LOAD_ATTR                survinfo
             1432  LOAD_STR                 'ZNum'
             1434  BINARY_SUBSCR    
             1436  BUILD_LIST_3          3 
             1438  CALL_METHOD_2         2  '2 positional arguments'

 L. 522      1440  LOAD_CONST               2
             1442  LOAD_CONST               1
             1444  LOAD_CONST               0
             1446  BUILD_LIST_3          3 
             1448  CALL_METHOD_2         2  '2 positional arguments'
             1450  LOAD_FAST                'self'
             1452  LOAD_ATTR                seisdata
             1454  LOAD_FAST                'self'
             1456  LOAD_ATTR                ldtsave
             1458  LOAD_METHOD              text
             1460  CALL_METHOD_0         0  '0 positional arguments'
             1462  LOAD_GLOBAL              str
             1464  LOAD_FAST                '_labellist'
             1466  LOAD_FAST                'i'
             1468  BINARY_SUBSCR    
             1470  CALL_FUNCTION_1       1  '1 positional argument'
             1472  BINARY_ADD       
             1474  STORE_SUBSCR     
         1476_1478  JUMP_BACK          1378  'to 1378'
             1480  POP_BLOCK        
           1482_0  COME_FROM_LOOP     1364  '1364'

 L. 524      1482  LOAD_GLOBAL              QtWidgets
             1484  LOAD_ATTR                QMessageBox
             1486  LOAD_METHOD              information
             1488  LOAD_FAST                'self'
             1490  LOAD_ATTR                msgbox

 L. 525      1492  LOAD_STR                 'Apply MLP'

 L. 526      1494  LOAD_STR                 'MLP applied successfully'
             1496  CALL_METHOD_3         3  '3 positional arguments'
             1498  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 1496

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
    ApplyMlMlp4Prob = QtWidgets.QWidget()
    gui = applymlmlp4prob()
    gui.setupGUI(ApplyMlMlp4Prob)
    ApplyMlMlp4Prob.show()
    sys.exit(app.exec_())