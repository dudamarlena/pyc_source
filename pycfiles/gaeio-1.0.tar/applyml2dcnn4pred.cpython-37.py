# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\applyml2dcnn4pred.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 31751 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.basic.image as basic_image
import cognitivegeo.src.vis.messager as vis_msg
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.cnnclassifier as ml_cnn
import cognitivegeo.src.gui.viewml2dcnn as gui_viewml2dcnn
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class applyml2dcnn4pred(object):
    survinfo = {}
    seisdata = {}
    rootpath = ''
    linestyle = core_set.Visual['Line']
    maskstyle = core_set.Visual['Image']
    fontstyle = core_set.Visual['Font']
    iconpath = os.path.dirname(__file__)
    dialog = None
    modelpath = ''
    modelname = ''
    modelinfo = None

    def setupGUI(self, ApplyMl2DCnn4Pred):
        ApplyMl2DCnn4Pred.setObjectName('ApplyMl2DCnn4Pred')
        ApplyMl2DCnn4Pred.setFixedSize(800, 440)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ApplyMl2DCnn4Pred.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ApplyMl2DCnn4Pred)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ApplyMl2DCnn4Pred)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ApplyMl2DCnn4Pred)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lblornt = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(ApplyMl2DCnn4Pred)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 220, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 220, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(ApplyMl2DCnn4Pred)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 220, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 260, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(ApplyMl2DCnn4Pred)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 260, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 220, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 220, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(ApplyMl2DCnn4Pred)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 220, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 260, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(ApplyMl2DCnn4Pred)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 260, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ApplyMl2DCnn4Pred)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ApplyMl2DCnn4Pred)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ApplyMl2DCnn4Pred)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 130))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(ApplyMl2DCnn4Pred)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(ApplyMl2DCnn4Pred)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 140, 180, 130))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ApplyMl2DCnn4Pred)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ApplyMl2DCnn4Pred)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ApplyMl2DCnn4Pred)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ApplyMl2DCnn4Pred)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.lblpara = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ApplyMl2DCnn4Pred)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblsave = QtWidgets.QLabel(ApplyMl2DCnn4Pred)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ApplyMl2DCnn4Pred)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.btnapply = QtWidgets.QPushButton(ApplyMl2DCnn4Pred)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 390, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ApplyMl2DCnn4Pred)
        self.msgbox.setObjectName('msgbox')
        _center_x = ApplyMl2DCnn4Pred.geometry().center().x()
        _center_y = ApplyMl2DCnn4Pred.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ApplyMl2DCnn4Pred)
        QtCore.QMetaObject.connectSlotsByName(ApplyMl2DCnn4Pred)

    def retranslateGUI(self, ApplyMl2DCnn4Pred):
        self.dialog = ApplyMl2DCnn4Pred
        _translate = QtCore.QCoreApplication.translate
        ApplyMl2DCnn4Pred.setWindowTitle(_translate('ApplyMl2DCnn4Pred', 'Apply 2D-CNN for prediction'))
        self.lblfrom.setText(_translate('ApplyMl2DCnn4Pred', 'Select network:'))
        self.ldtfrom.setText(_translate('ApplyMl2DCnn4Pred', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ApplyMl2DCnn4Pred', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ApplyMl2DCnn4Pred', 'Training features:'))
        self.lblornt.setText(_translate('ApplyMl2DCnn4Pred', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.lbloldsize.setText(_translate('ApplyMl2DCnn4Pred', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('ApplyMl2DCnn4Pred', 'height='))
        self.ldtoldheight.setText(_translate('ApplyMl2DCnn4Pred', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('ApplyMl2DCnn4Pred', 'width='))
        self.ldtoldwidth.setText(_translate('ApplyMl2DCnn4Pred', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('ApplyMl2DCnn4Pred', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('ApplyMl2DCnn4Pred', 'height='))
        self.ldtnewheight.setText(_translate('ApplyMl2DCnn4Pred', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewheight.setEnabled(False)
        self.lblnewwidth.setText(_translate('ApplyMl2DCnn4Pred', 'width='))
        self.ldtnewwidth.setText(_translate('ApplyMl2DCnn4Pred', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewwidth.setEnabled(False)
        self.lblnetwork.setText(_translate('ApplyMl2DCnn4Pred', 'Pre-trained CNN architecture:'))
        self.btnviewnetwork.setText(_translate('ApplyMl2DCnn4Pred', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('ApplyMl2DCnn4Pred', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ApplyMl2DCnn4Pred', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblnfclayer.setText(_translate('ApplyMl2DCnn4Pred', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('ApplyMl2DCnn4Pred', ''))
        self.ldtnfclayer.setEnabled(False)
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblmasksize.setText(_translate('ApplyMl2DCnn4Pred', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ApplyMl2DCnn4Pred', 'height='))
        self.ldtmaskheight.setText(_translate('ApplyMl2DCnn4Pred', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ApplyMl2DCnn4Pred', 'width='))
        self.ldtmaskwidth.setText(_translate('ApplyMl2DCnn4Pred', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ApplyMl2DCnn4Pred', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ApplyMl2DCnn4Pred', 'height='))
        self.ldtpoolheight.setText(_translate('ApplyMl2DCnn4Pred', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ApplyMl2DCnn4Pred', 'width='))
        self.ldtpoolwidth.setText(_translate('ApplyMl2DCnn4Pred', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ApplyMl2DCnn4Pred', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ApplyMl2DCnn4Pred', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ApplyMl2DCnn4Pred', '5000'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('ApplyMl2DCnn4Pred', 'Output name='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ApplyMl2DCnn4Pred', 'cnn'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('ApplyMl2DCnn4Pred', 'Apply 2D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnApplyMl2DCnn4Pred)

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
            _featurelist = self.modelinfo['feature_list']
            _firstfeature = None
            for f in _featurelist:
                item = QtWidgets.QListWidgetItem(self.lwgfeature)
                item.setText(f)
                self.lwgfeature.addItem(item)
                if _firstfeature is None:
                    _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            _height = self.modelinfo['image_size'][0]
            _width = self.modelinfo['image_size'][1]
            self.ldtnewheight.setText(str(_height))
            self.ldtnewwidth.setText(str(_width))
            self.ldtoldheight.setText(str(3))
            self.ldtoldwidth.setText(str(3))
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

    def clickBtnApplyMl2DCnn4Pred--- This code section failed: ---

 L. 426         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 428         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 429        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in ApplyMl2DCnn4Pred: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 430        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 431        44  LOAD_STR                 'Apply 2D-CNN'

 L. 432        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 433        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 434        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 435        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in ApplyMl2DCnn4Pred: No CNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 436        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 437       100  LOAD_STR                 'Apply 2D-CNN'

 L. 438       102  LOAD_STR                 'No CNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 439       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 441       112  LOAD_FAST                'self'
              114  LOAD_ATTR                modelinfo
              116  LOAD_STR                 'feature_list'
              118  BINARY_SUBSCR    
              120  STORE_FAST               '_featurelist'

 L. 442       122  SETUP_LOOP          198  'to 198'
              124  LOAD_FAST                '_featurelist'
              126  GET_ITER         
            128_0  COME_FROM           144  '144'
              128  FOR_ITER            196  'to 196'
              130  STORE_FAST               'f'

 L. 443       132  LOAD_FAST                'self'
              134  LOAD_METHOD              checkSeisData
              136  LOAD_FAST                'f'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_CONST               False
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   128  'to 128'

 L. 444       146  LOAD_GLOBAL              vis_msg
              148  LOAD_ATTR                print
              150  LOAD_STR                 "ERROR in ApplyMl2DCnn4Pred: Feature '%s' not found in seismic data"
              152  LOAD_FAST                'f'
              154  BINARY_MODULO    

 L. 445       156  LOAD_STR                 'error'
              158  LOAD_CONST               ('type',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  POP_TOP          

 L. 446       164  LOAD_GLOBAL              QtWidgets
              166  LOAD_ATTR                QMessageBox
              168  LOAD_METHOD              critical
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                msgbox

 L. 447       174  LOAD_STR                 'Apply 2D-CNN'

 L. 448       176  LOAD_STR                 "Feature '"
              178  LOAD_FAST                'f'
              180  BINARY_ADD       
              182  LOAD_STR                 "' not found in seismic data"
              184  BINARY_ADD       
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 449       190  LOAD_CONST               None
              192  RETURN_VALUE     
              194  JUMP_BACK           128  'to 128'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      122  '122'

 L. 451       198  LOAD_GLOBAL              basic_data
              200  LOAD_METHOD              str2int
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                ldtoldheight
              206  LOAD_METHOD              text
              208  CALL_METHOD_0         0  '0 positional arguments'
              210  CALL_METHOD_1         1  '1 positional argument'
              212  STORE_FAST               '_image_height_old'

 L. 452       214  LOAD_GLOBAL              basic_data
              216  LOAD_METHOD              str2int
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                ldtoldwidth
              222  LOAD_METHOD              text
              224  CALL_METHOD_0         0  '0 positional arguments'
              226  CALL_METHOD_1         1  '1 positional argument'
              228  STORE_FAST               '_image_width_old'

 L. 453       230  LOAD_GLOBAL              basic_data
              232  LOAD_METHOD              str2int
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                ldtnewheight
              238  LOAD_METHOD              text
              240  CALL_METHOD_0         0  '0 positional arguments'
              242  CALL_METHOD_1         1  '1 positional argument'
              244  STORE_FAST               '_image_height_new'

 L. 454       246  LOAD_GLOBAL              basic_data
              248  LOAD_METHOD              str2int
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                ldtnewwidth
              254  LOAD_METHOD              text
              256  CALL_METHOD_0         0  '0 positional arguments'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  STORE_FAST               '_image_width_new'

 L. 455       262  LOAD_FAST                '_image_height_old'
              264  LOAD_CONST               False
              266  COMPARE_OP               is
          268_270  POP_JUMP_IF_TRUE    302  'to 302'
              272  LOAD_FAST                '_image_width_old'
              274  LOAD_CONST               False
              276  COMPARE_OP               is
          278_280  POP_JUMP_IF_TRUE    302  'to 302'

 L. 456       282  LOAD_FAST                '_image_height_new'
              284  LOAD_CONST               False
              286  COMPARE_OP               is
          288_290  POP_JUMP_IF_TRUE    302  'to 302'
              292  LOAD_FAST                '_image_width_new'
              294  LOAD_CONST               False
              296  COMPARE_OP               is
          298_300  POP_JUMP_IF_FALSE   338  'to 338'
            302_0  COME_FROM           288  '288'
            302_1  COME_FROM           278  '278'
            302_2  COME_FROM           268  '268'

 L. 457       302  LOAD_GLOBAL              vis_msg
              304  LOAD_ATTR                print
              306  LOAD_STR                 'ERROR in ApplyMl2DCnn4Pred: Non-integer feature size'
              308  LOAD_STR                 'error'
              310  LOAD_CONST               ('type',)
              312  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              314  POP_TOP          

 L. 458       316  LOAD_GLOBAL              QtWidgets
              318  LOAD_ATTR                QMessageBox
              320  LOAD_METHOD              critical
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                msgbox

 L. 459       326  LOAD_STR                 'Apply 2D-CNN'

 L. 460       328  LOAD_STR                 'Non-integer feature size'
              330  CALL_METHOD_3         3  '3 positional arguments'
              332  POP_TOP          

 L. 461       334  LOAD_CONST               None
              336  RETURN_VALUE     
            338_0  COME_FROM           298  '298'

 L. 462       338  LOAD_FAST                '_image_height_old'
              340  LOAD_CONST               2
              342  COMPARE_OP               <
          344_346  POP_JUMP_IF_TRUE    378  'to 378'
              348  LOAD_FAST                '_image_width_old'
              350  LOAD_CONST               2
              352  COMPARE_OP               <
          354_356  POP_JUMP_IF_TRUE    378  'to 378'

 L. 463       358  LOAD_FAST                '_image_height_new'
              360  LOAD_CONST               2
              362  COMPARE_OP               <
          364_366  POP_JUMP_IF_TRUE    378  'to 378'
              368  LOAD_FAST                '_image_width_new'
              370  LOAD_CONST               2
              372  COMPARE_OP               <
          374_376  POP_JUMP_IF_FALSE   414  'to 414'
            378_0  COME_FROM           364  '364'
            378_1  COME_FROM           354  '354'
            378_2  COME_FROM           344  '344'

 L. 464       378  LOAD_GLOBAL              vis_msg
              380  LOAD_ATTR                print
              382  LOAD_STR                 'ERROR in ApplyMl2DCnn4Pred: Features are not 2D'
              384  LOAD_STR                 'error'
              386  LOAD_CONST               ('type',)
              388  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              390  POP_TOP          

 L. 465       392  LOAD_GLOBAL              QtWidgets
              394  LOAD_ATTR                QMessageBox
              396  LOAD_METHOD              critical
              398  LOAD_FAST                'self'
              400  LOAD_ATTR                msgbox

 L. 466       402  LOAD_STR                 'Apply 2D-CNN'

 L. 467       404  LOAD_STR                 'Features are not 2D'
              406  CALL_METHOD_3         3  '3 positional arguments'
              408  POP_TOP          

 L. 468       410  LOAD_CONST               None
              412  RETURN_VALUE     
            414_0  COME_FROM           374  '374'

 L. 470       414  LOAD_GLOBAL              basic_data
              416  LOAD_METHOD              str2int
              418  LOAD_FAST                'self'
              420  LOAD_ATTR                ldtbatchsize
              422  LOAD_METHOD              text
              424  CALL_METHOD_0         0  '0 positional arguments'
              426  CALL_METHOD_1         1  '1 positional argument'
              428  STORE_FAST               '_batch'

 L. 471       430  LOAD_FAST                '_batch'
              432  LOAD_CONST               False
              434  COMPARE_OP               is
          436_438  POP_JUMP_IF_TRUE    450  'to 450'
              440  LOAD_FAST                '_batch'
              442  LOAD_CONST               1
              444  COMPARE_OP               <
          446_448  POP_JUMP_IF_FALSE   486  'to 486'
            450_0  COME_FROM           436  '436'

 L. 472       450  LOAD_GLOBAL              vis_msg
              452  LOAD_ATTR                print
              454  LOAD_STR                 'ERROR in ApplyMl2DCnn4Pred: Non-positive batch size'
              456  LOAD_STR                 'error'
              458  LOAD_CONST               ('type',)
              460  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              462  POP_TOP          

 L. 473       464  LOAD_GLOBAL              QtWidgets
              466  LOAD_ATTR                QMessageBox
              468  LOAD_METHOD              critical
              470  LOAD_FAST                'self'
              472  LOAD_ATTR                msgbox

 L. 474       474  LOAD_STR                 'Apply 2D-CNN'

 L. 475       476  LOAD_STR                 'Non-positive batch size'
              478  CALL_METHOD_3         3  '3 positional arguments'
              480  POP_TOP          

 L. 476       482  LOAD_CONST               None
              484  RETURN_VALUE     
            486_0  COME_FROM           446  '446'

 L. 478       486  LOAD_GLOBAL              len
              488  LOAD_FAST                'self'
              490  LOAD_ATTR                ldtsave
              492  LOAD_METHOD              text
              494  CALL_METHOD_0         0  '0 positional arguments'
              496  CALL_FUNCTION_1       1  '1 positional argument'
              498  LOAD_CONST               1
              500  COMPARE_OP               <
          502_504  POP_JUMP_IF_FALSE   542  'to 542'

 L. 479       506  LOAD_GLOBAL              vis_msg
              508  LOAD_ATTR                print
              510  LOAD_STR                 'ERROR in ApplyMl2DCnn4Pred: No name specified'
              512  LOAD_STR                 'error'
              514  LOAD_CONST               ('type',)
              516  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              518  POP_TOP          

 L. 480       520  LOAD_GLOBAL              QtWidgets
              522  LOAD_ATTR                QMessageBox
              524  LOAD_METHOD              critical
              526  LOAD_FAST                'self'
              528  LOAD_ATTR                msgbox

 L. 481       530  LOAD_STR                 'Apply 2D-CNN'

 L. 482       532  LOAD_STR                 'No name specified'
              534  CALL_METHOD_3         3  '3 positional arguments'
              536  POP_TOP          

 L. 483       538  LOAD_CONST               None
              540  RETURN_VALUE     
            542_0  COME_FROM           502  '502'

 L. 484       542  LOAD_FAST                'self'
              544  LOAD_ATTR                ldtsave
              546  LOAD_METHOD              text
              548  CALL_METHOD_0         0  '0 positional arguments'
              550  LOAD_FAST                'self'
              552  LOAD_ATTR                seisdata
              554  LOAD_METHOD              keys
              556  CALL_METHOD_0         0  '0 positional arguments'
              558  COMPARE_OP               in
          560_562  POP_JUMP_IF_FALSE   648  'to 648'
              564  LOAD_FAST                'self'
              566  LOAD_METHOD              checkSeisData
              568  LOAD_FAST                'self'
              570  LOAD_ATTR                ldtsave
              572  LOAD_METHOD              text
              574  CALL_METHOD_0         0  '0 positional arguments'
              576  CALL_METHOD_1         1  '1 positional argument'
          578_580  POP_JUMP_IF_FALSE   648  'to 648'

 L. 485       582  LOAD_GLOBAL              QtWidgets
              584  LOAD_ATTR                QMessageBox
              586  LOAD_METHOD              question
              588  LOAD_FAST                'self'
              590  LOAD_ATTR                msgbox
              592  LOAD_STR                 'Apply 2D-CNN'

 L. 486       594  LOAD_FAST                'self'
              596  LOAD_ATTR                ldtsave
              598  LOAD_METHOD              text
              600  CALL_METHOD_0         0  '0 positional arguments'
              602  LOAD_STR                 ' already exists. Overwrite?'
              604  BINARY_ADD       

 L. 487       606  LOAD_GLOBAL              QtWidgets
              608  LOAD_ATTR                QMessageBox
              610  LOAD_ATTR                Yes
              612  LOAD_GLOBAL              QtWidgets
              614  LOAD_ATTR                QMessageBox
              616  LOAD_ATTR                No
              618  BINARY_OR        

 L. 488       620  LOAD_GLOBAL              QtWidgets
              622  LOAD_ATTR                QMessageBox
              624  LOAD_ATTR                No
              626  CALL_METHOD_5         5  '5 positional arguments'
              628  STORE_FAST               'reply'

 L. 490       630  LOAD_FAST                'reply'
              632  LOAD_GLOBAL              QtWidgets
              634  LOAD_ATTR                QMessageBox
              636  LOAD_ATTR                No
              638  COMPARE_OP               ==
          640_642  POP_JUMP_IF_FALSE   648  'to 648'

 L. 491       644  LOAD_CONST               None
              646  RETURN_VALUE     
            648_0  COME_FROM           640  '640'
            648_1  COME_FROM           578  '578'
            648_2  COME_FROM           560  '560'

 L. 493       648  LOAD_CONST               2
              650  LOAD_GLOBAL              int
              652  LOAD_FAST                '_image_height_old'
              654  LOAD_CONST               2
              656  BINARY_TRUE_DIVIDE
              658  CALL_FUNCTION_1       1  '1 positional argument'
              660  BINARY_MULTIPLY  
              662  LOAD_CONST               1
              664  BINARY_ADD       
              666  STORE_FAST               '_image_height_old'

 L. 494       668  LOAD_CONST               2
              670  LOAD_GLOBAL              int
              672  LOAD_FAST                '_image_width_old'
              674  LOAD_CONST               2
              676  BINARY_TRUE_DIVIDE
              678  CALL_FUNCTION_1       1  '1 positional argument'
              680  BINARY_MULTIPLY  
              682  LOAD_CONST               1
              684  BINARY_ADD       
              686  STORE_FAST               '_image_width_old'

 L. 496       688  LOAD_GLOBAL              np
              690  LOAD_METHOD              shape
              692  LOAD_FAST                'self'
              694  LOAD_ATTR                seisdata
              696  LOAD_FAST                '_featurelist'
              698  LOAD_CONST               0
              700  BINARY_SUBSCR    
              702  BINARY_SUBSCR    
              704  CALL_METHOD_1         1  '1 positional argument'
              706  LOAD_CONST               0
              708  BINARY_SUBSCR    
              710  STORE_FAST               '_nsample'

 L. 498       712  LOAD_GLOBAL              int
              714  LOAD_GLOBAL              np
              716  LOAD_METHOD              ceil
              718  LOAD_FAST                '_nsample'
              720  LOAD_FAST                '_batch'
              722  BINARY_TRUE_DIVIDE
              724  CALL_METHOD_1         1  '1 positional argument'
              726  CALL_FUNCTION_1       1  '1 positional argument'
              728  STORE_FAST               '_nloop'

 L. 501       730  LOAD_GLOBAL              QtWidgets
              732  LOAD_METHOD              QProgressDialog
              734  CALL_METHOD_0         0  '0 positional arguments'
              736  STORE_FAST               '_pgsdlg'

 L. 502       738  LOAD_GLOBAL              QtGui
              740  LOAD_METHOD              QIcon
              742  CALL_METHOD_0         0  '0 positional arguments'
              744  STORE_FAST               'icon'

 L. 503       746  LOAD_FAST                'icon'
              748  LOAD_METHOD              addPixmap
              750  LOAD_GLOBAL              QtGui
              752  LOAD_METHOD              QPixmap
              754  LOAD_GLOBAL              os
              756  LOAD_ATTR                path
              758  LOAD_METHOD              join
              760  LOAD_FAST                'self'
              762  LOAD_ATTR                iconpath
              764  LOAD_STR                 'icons/apply.png'
              766  CALL_METHOD_2         2  '2 positional arguments'
              768  CALL_METHOD_1         1  '1 positional argument'

 L. 504       770  LOAD_GLOBAL              QtGui
              772  LOAD_ATTR                QIcon
              774  LOAD_ATTR                Normal
              776  LOAD_GLOBAL              QtGui
              778  LOAD_ATTR                QIcon
              780  LOAD_ATTR                Off
              782  CALL_METHOD_3         3  '3 positional arguments'
              784  POP_TOP          

 L. 505       786  LOAD_FAST                '_pgsdlg'
              788  LOAD_METHOD              setWindowIcon
              790  LOAD_FAST                'icon'
              792  CALL_METHOD_1         1  '1 positional argument'
              794  POP_TOP          

 L. 506       796  LOAD_FAST                '_pgsdlg'
              798  LOAD_METHOD              setWindowTitle
              800  LOAD_STR                 'Apply 2D-CNN'
              802  CALL_METHOD_1         1  '1 positional argument'
              804  POP_TOP          

 L. 507       806  LOAD_FAST                '_pgsdlg'
              808  LOAD_METHOD              setCancelButton
              810  LOAD_CONST               None
              812  CALL_METHOD_1         1  '1 positional argument'
              814  POP_TOP          

 L. 508       816  LOAD_FAST                '_pgsdlg'
              818  LOAD_METHOD              setWindowFlags
              820  LOAD_GLOBAL              QtCore
              822  LOAD_ATTR                Qt
              824  LOAD_ATTR                WindowStaysOnTopHint
              826  CALL_METHOD_1         1  '1 positional argument'
              828  POP_TOP          

 L. 509       830  LOAD_FAST                '_pgsdlg'
              832  LOAD_METHOD              forceShow
              834  CALL_METHOD_0         0  '0 positional arguments'
              836  POP_TOP          

 L. 510       838  LOAD_FAST                '_pgsdlg'
              840  LOAD_METHOD              setFixedWidth
              842  LOAD_CONST               400
              844  CALL_METHOD_1         1  '1 positional argument'
              846  POP_TOP          

 L. 511       848  LOAD_FAST                '_pgsdlg'
              850  LOAD_METHOD              setMaximum
              852  LOAD_FAST                '_nloop'
              854  CALL_METHOD_1         1  '1 positional argument'
              856  POP_TOP          

 L. 513       858  LOAD_CONST               0
              860  STORE_FAST               '_wdinl'

 L. 514       862  LOAD_CONST               0
              864  STORE_FAST               '_wdxl'

 L. 515       866  LOAD_CONST               0
              868  STORE_FAST               '_wdz'

 L. 516       870  LOAD_FAST                'self'
              872  LOAD_ATTR                cbbornt
              874  LOAD_METHOD              currentIndex
              876  CALL_METHOD_0         0  '0 positional arguments'
              878  LOAD_CONST               0
              880  COMPARE_OP               ==
          882_884  POP_JUMP_IF_FALSE   910  'to 910'

 L. 517       886  LOAD_GLOBAL              int
              888  LOAD_FAST                '_image_width_old'
              890  LOAD_CONST               2
              892  BINARY_TRUE_DIVIDE
              894  CALL_FUNCTION_1       1  '1 positional argument'
              896  STORE_FAST               '_wdxl'

 L. 518       898  LOAD_GLOBAL              int
              900  LOAD_FAST                '_image_height_old'
              902  LOAD_CONST               2
              904  BINARY_TRUE_DIVIDE
              906  CALL_FUNCTION_1       1  '1 positional argument'
              908  STORE_FAST               '_wdz'
            910_0  COME_FROM           882  '882'

 L. 519       910  LOAD_FAST                'self'
              912  LOAD_ATTR                cbbornt
              914  LOAD_METHOD              currentIndex
              916  CALL_METHOD_0         0  '0 positional arguments'
              918  LOAD_CONST               1
              920  COMPARE_OP               ==
          922_924  POP_JUMP_IF_FALSE   950  'to 950'

 L. 520       926  LOAD_GLOBAL              int
              928  LOAD_FAST                '_image_width_old'
              930  LOAD_CONST               2
              932  BINARY_TRUE_DIVIDE
              934  CALL_FUNCTION_1       1  '1 positional argument'
              936  STORE_FAST               '_wdinl'

 L. 521       938  LOAD_GLOBAL              int
              940  LOAD_FAST                '_image_height_old'
              942  LOAD_CONST               2
              944  BINARY_TRUE_DIVIDE
              946  CALL_FUNCTION_1       1  '1 positional argument'
              948  STORE_FAST               '_wdz'
            950_0  COME_FROM           922  '922'

 L. 522       950  LOAD_FAST                'self'
              952  LOAD_ATTR                cbbornt
              954  LOAD_METHOD              currentIndex
              956  CALL_METHOD_0         0  '0 positional arguments'
              958  LOAD_CONST               2
              960  COMPARE_OP               ==
          962_964  POP_JUMP_IF_FALSE   990  'to 990'

 L. 523       966  LOAD_GLOBAL              int
              968  LOAD_FAST                '_image_width_old'
              970  LOAD_CONST               2
              972  BINARY_TRUE_DIVIDE
              974  CALL_FUNCTION_1       1  '1 positional argument'
              976  STORE_FAST               '_wdinl'

 L. 524       978  LOAD_GLOBAL              int
              980  LOAD_FAST                '_image_height_old'
              982  LOAD_CONST               2
              984  BINARY_TRUE_DIVIDE
              986  CALL_FUNCTION_1       1  '1 positional argument'
              988  STORE_FAST               '_wdxl'
            990_0  COME_FROM           962  '962'

 L. 526       990  LOAD_GLOBAL              seis_ays
              992  LOAD_METHOD              convertSeisInfoTo2DMat
              994  LOAD_FAST                'self'
              996  LOAD_ATTR                survinfo
              998  CALL_METHOD_1         1  '1 positional argument'
             1000  STORE_FAST               '_seisdata'

 L. 528      1002  LOAD_GLOBAL              np
             1004  LOAD_METHOD              zeros
             1006  LOAD_FAST                '_nsample'
             1008  LOAD_CONST               1
             1010  BUILD_LIST_2          2 
             1012  CALL_METHOD_1         1  '1 positional argument'
             1014  STORE_FAST               '_result'

 L. 529      1016  LOAD_CONST               0
             1018  STORE_FAST               'idxstart'

 L. 530  1020_1022  SETUP_LOOP         1344  'to 1344'
             1024  LOAD_GLOBAL              range
             1026  LOAD_FAST                '_nloop'
             1028  CALL_FUNCTION_1       1  '1 positional argument'
             1030  GET_ITER         
         1032_1034  FOR_ITER           1342  'to 1342'
             1036  STORE_FAST               'i'

 L. 532      1038  LOAD_GLOBAL              QtCore
             1040  LOAD_ATTR                QCoreApplication
             1042  LOAD_METHOD              instance
             1044  CALL_METHOD_0         0  '0 positional arguments'
             1046  LOAD_METHOD              processEvents
             1048  CALL_METHOD_0         0  '0 positional arguments'
             1050  POP_TOP          

 L. 534      1052  LOAD_GLOBAL              sys
             1054  LOAD_ATTR                stdout
             1056  LOAD_METHOD              write

 L. 535      1058  LOAD_STR                 '\r>>> Apply 2D-CNN, proceeding %.1f%% '
             1060  LOAD_GLOBAL              float
             1062  LOAD_FAST                'i'
             1064  CALL_FUNCTION_1       1  '1 positional argument'
             1066  LOAD_GLOBAL              float
             1068  LOAD_FAST                '_nloop'
             1070  CALL_FUNCTION_1       1  '1 positional argument'
             1072  BINARY_TRUE_DIVIDE
             1074  LOAD_CONST               100.0
             1076  BINARY_MULTIPLY  
             1078  BINARY_MODULO    
             1080  CALL_METHOD_1         1  '1 positional argument'
             1082  POP_TOP          

 L. 536      1084  LOAD_GLOBAL              sys
             1086  LOAD_ATTR                stdout
             1088  LOAD_METHOD              flush
             1090  CALL_METHOD_0         0  '0 positional arguments'
             1092  POP_TOP          

 L. 538      1094  LOAD_FAST                'idxstart'
             1096  LOAD_FAST                '_batch'
             1098  BINARY_ADD       
             1100  STORE_FAST               'idxend'

 L. 539      1102  LOAD_FAST                'idxend'
             1104  LOAD_FAST                '_nsample'
             1106  COMPARE_OP               >
         1108_1110  POP_JUMP_IF_FALSE  1116  'to 1116'

 L. 540      1112  LOAD_FAST                '_nsample'
             1114  STORE_FAST               'idxend'
           1116_0  COME_FROM          1108  '1108'

 L. 541      1116  LOAD_GLOBAL              np
             1118  LOAD_METHOD              linspace
             1120  LOAD_FAST                'idxstart'
             1122  LOAD_FAST                'idxend'
             1124  LOAD_CONST               1
             1126  BINARY_SUBTRACT  
             1128  LOAD_FAST                'idxend'
             1130  LOAD_FAST                'idxstart'
             1132  BINARY_SUBTRACT  
             1134  CALL_METHOD_3         3  '3 positional arguments'
             1136  LOAD_METHOD              astype
             1138  LOAD_GLOBAL              int
             1140  CALL_METHOD_1         1  '1 positional argument'
             1142  STORE_FAST               'idxlist'

 L. 542      1144  LOAD_FAST                'idxend'
             1146  STORE_FAST               'idxstart'

 L. 544      1148  LOAD_FAST                '_seisdata'
             1150  LOAD_FAST                'idxlist'
             1152  LOAD_CONST               0
             1154  LOAD_CONST               3
             1156  BUILD_SLICE_2         2 
             1158  BUILD_TUPLE_2         2 
             1160  BINARY_SUBSCR    
             1162  STORE_FAST               '_targetdata'

 L. 546      1164  BUILD_MAP_0           0 
             1166  STORE_FAST               '_dict'

 L. 547      1168  SETUP_LOOP         1288  'to 1288'
             1170  LOAD_FAST                '_featurelist'
             1172  GET_ITER         
           1174_0  COME_FROM          1250  '1250'
             1174  FOR_ITER           1286  'to 1286'
             1176  STORE_FAST               'f'

 L. 548      1178  LOAD_FAST                'self'
             1180  LOAD_ATTR                seisdata
             1182  LOAD_FAST                'f'
             1184  BINARY_SUBSCR    
             1186  STORE_FAST               '_data'

 L. 549      1188  LOAD_GLOBAL              seis_ays
             1190  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1192  LOAD_FAST                '_data'
             1194  LOAD_FAST                '_targetdata'
             1196  LOAD_FAST                'self'
             1198  LOAD_ATTR                survinfo

 L. 550      1200  LOAD_FAST                '_wdinl'
             1202  LOAD_FAST                '_wdxl'
             1204  LOAD_FAST                '_wdz'

 L. 551      1206  LOAD_CONST               False
             1208  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1210  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1212  LOAD_CONST               None
             1214  LOAD_CONST               None
             1216  BUILD_SLICE_2         2 
             1218  LOAD_CONST               3
             1220  LOAD_CONST               None
             1222  BUILD_SLICE_2         2 
             1224  BUILD_TUPLE_2         2 
             1226  BINARY_SUBSCR    
             1228  LOAD_FAST                '_dict'
             1230  LOAD_FAST                'f'
             1232  STORE_SUBSCR     

 L. 552      1234  LOAD_FAST                '_image_height_new'
             1236  LOAD_FAST                '_image_height_old'
             1238  COMPARE_OP               !=
         1240_1242  POP_JUMP_IF_TRUE   1254  'to 1254'
             1244  LOAD_FAST                '_image_width_new'
             1246  LOAD_FAST                '_image_width_old'
             1248  COMPARE_OP               !=
         1250_1252  POP_JUMP_IF_FALSE  1174  'to 1174'
           1254_0  COME_FROM          1240  '1240'

 L. 553      1254  LOAD_GLOBAL              basic_image
             1256  LOAD_ATTR                changeImageSize
             1258  LOAD_FAST                '_dict'
             1260  LOAD_FAST                'f'
             1262  BINARY_SUBSCR    

 L. 554      1264  LOAD_FAST                '_image_height_old'

 L. 555      1266  LOAD_FAST                '_image_width_old'

 L. 556      1268  LOAD_FAST                '_image_height_new'

 L. 557      1270  LOAD_FAST                '_image_width_new'
             1272  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1274  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1276  LOAD_FAST                '_dict'
             1278  LOAD_FAST                'f'
             1280  STORE_SUBSCR     
         1282_1284  JUMP_BACK          1174  'to 1174'
             1286  POP_BLOCK        
           1288_0  COME_FROM_LOOP     1168  '1168'

 L. 560      1288  LOAD_GLOBAL              ml_cnn
             1290  LOAD_ATTR                predictFromCNNClassifier
             1292  LOAD_FAST                '_dict'

 L. 561      1294  LOAD_FAST                'self'
             1296  LOAD_ATTR                modelpath

 L. 562      1298  LOAD_FAST                'self'
             1300  LOAD_ATTR                modelname

 L. 563      1302  LOAD_FAST                '_batch'

 L. 564      1304  LOAD_CONST               True
             1306  LOAD_CONST               ('cnnpath', 'cnnname', 'batchsize', 'verbose')
             1308  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1310  LOAD_FAST                '_result'
             1312  LOAD_FAST                'idxlist'
             1314  LOAD_CONST               0
             1316  LOAD_CONST               1
             1318  BUILD_SLICE_2         2 
             1320  BUILD_TUPLE_2         2 
             1322  STORE_SUBSCR     

 L. 567      1324  LOAD_FAST                '_pgsdlg'
             1326  LOAD_METHOD              setValue
             1328  LOAD_FAST                'i'
             1330  LOAD_CONST               1
             1332  BINARY_ADD       
             1334  CALL_METHOD_1         1  '1 positional argument'
             1336  POP_TOP          
         1338_1340  JUMP_BACK          1032  'to 1032'
             1342  POP_BLOCK        
           1344_0  COME_FROM_LOOP     1020  '1020'

 L. 569      1344  LOAD_GLOBAL              print
             1346  LOAD_STR                 'Done'
             1348  CALL_FUNCTION_1       1  '1 positional argument'
             1350  POP_TOP          

 L. 570      1352  LOAD_GLOBAL              np
             1354  LOAD_METHOD              transpose
             1356  LOAD_GLOBAL              np
             1358  LOAD_METHOD              reshape
             1360  LOAD_FAST                '_result'

 L. 571      1362  LOAD_FAST                'self'
             1364  LOAD_ATTR                survinfo
             1366  LOAD_STR                 'ILNum'
             1368  BINARY_SUBSCR    
             1370  LOAD_FAST                'self'
             1372  LOAD_ATTR                survinfo
             1374  LOAD_STR                 'XLNum'
             1376  BINARY_SUBSCR    

 L. 572      1378  LOAD_FAST                'self'
             1380  LOAD_ATTR                survinfo
             1382  LOAD_STR                 'ZNum'
             1384  BINARY_SUBSCR    
             1386  BUILD_LIST_3          3 
             1388  CALL_METHOD_2         2  '2 positional arguments'

 L. 573      1390  LOAD_CONST               2
             1392  LOAD_CONST               1
             1394  LOAD_CONST               0
             1396  BUILD_LIST_3          3 
             1398  CALL_METHOD_2         2  '2 positional arguments'
             1400  LOAD_FAST                'self'
             1402  LOAD_ATTR                seisdata
             1404  LOAD_FAST                'self'
             1406  LOAD_ATTR                ldtsave
             1408  LOAD_METHOD              text
             1410  CALL_METHOD_0         0  '0 positional arguments'
             1412  STORE_SUBSCR     

 L. 575      1414  LOAD_GLOBAL              QtWidgets
             1416  LOAD_ATTR                QMessageBox
             1418  LOAD_METHOD              information
             1420  LOAD_FAST                'self'
             1422  LOAD_ATTR                msgbox

 L. 576      1424  LOAD_STR                 'Apply 2D-CNN'

 L. 577      1426  LOAD_STR                 'CNN applied successfully'
             1428  CALL_METHOD_3         3  '3 positional arguments'
             1430  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 1428

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
    ApplyMl2DCnn4Pred = QtWidgets.QWidget()
    gui = applyml2dcnn4pred()
    gui.setupGUI(ApplyMl2DCnn4Pred)
    ApplyMl2DCnn4Pred.show()
    sys.exit(app.exec_())