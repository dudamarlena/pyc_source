# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\evaluateml2dcnn.py
# Compiled at: 2019-12-15 21:49:29
# Size of source mod 2**32: 32977 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.image as basic_image
import cognitivegeo.src.vis.messager as vis_msg
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.cnnclassifier as ml_cnn
import cognitivegeo.src.gui.viewmlconfmat as gui_viewmlconfmat
import cognitivegeo.src.gui.viewml2dcnn as gui_viewml2dcnn
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class evaluateml2dcnn(object):
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

    def setupGUI(self, EvaluateMl2DCnn):
        EvaluateMl2DCnn.setObjectName('EvaluateMl2DCnn')
        EvaluateMl2DCnn.setFixedSize(800, 440)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/check.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EvaluateMl2DCnn.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(EvaluateMl2DCnn)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(EvaluateMl2DCnn)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(EvaluateMl2DCnn)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lblornt = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(EvaluateMl2DCnn)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 220, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 220, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(EvaluateMl2DCnn)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 220, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 260, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(EvaluateMl2DCnn)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 260, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 220, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 220, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(EvaluateMl2DCnn)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 220, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 260, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(EvaluateMl2DCnn)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 260, 40, 30))
        self.lbltarget = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(EvaluateMl2DCnn)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 310, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(EvaluateMl2DCnn)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(EvaluateMl2DCnn)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(EvaluateMl2DCnn)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 130))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(EvaluateMl2DCnn)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(EvaluateMl2DCnn)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 140, 180, 130))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(EvaluateMl2DCnn)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(EvaluateMl2DCnn)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(EvaluateMl2DCnn)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(EvaluateMl2DCnn)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.lblpara = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 360, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(EvaluateMl2DCnn)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(EvaluateMl2DCnn)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.btnapply = QtWidgets.QPushButton(EvaluateMl2DCnn)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 390, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/check.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(EvaluateMl2DCnn)
        self.msgbox.setObjectName('msgbox')
        _center_x = EvaluateMl2DCnn.geometry().center().x()
        _center_y = EvaluateMl2DCnn.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(EvaluateMl2DCnn)
        QtCore.QMetaObject.connectSlotsByName(EvaluateMl2DCnn)

    def retranslateGUI(self, EvaluateMl2DCnn):
        self.dialog = EvaluateMl2DCnn
        _translate = QtCore.QCoreApplication.translate
        EvaluateMl2DCnn.setWindowTitle(_translate('EvaluateMl2DCnn', 'Evaluate 2D-CNN'))
        self.lblfrom.setText(_translate('EvaluateMl2DCnn', 'Select network:'))
        self.ldtfrom.setText(_translate('EvaluateMl2DCnn', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('EvaluateMl2DCnn', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('EvaluateMl2DCnn', 'Training features:'))
        self.lblornt.setText(_translate('EvaluateMl2DCnn', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.lbloldsize.setText(_translate('EvaluateMl2DCnn', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('EvaluateMl2DCnn', 'height='))
        self.ldtoldheight.setText(_translate('EvaluateMl2DCnn', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('EvaluateMl2DCnn', 'width='))
        self.ldtoldwidth.setText(_translate('EvaluateMl2DCnn', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('EvaluateMl2DCnn', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('EvaluateMl2DCnn', 'height='))
        self.ldtnewheight.setText(_translate('EvaluateMl2DCnn', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewheight.setEnabled(False)
        self.lblnewwidth.setText(_translate('EvaluateMl2DCnn', 'width='))
        self.ldtnewwidth.setText(_translate('EvaluateMl2DCnn', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewwidth.setEnabled(False)
        self.lbltarget.setText(_translate('EvaluateMl2DCnn', 'Training target:'))
        self.lblnetwork.setText(_translate('EvaluateMl2DCnn', 'Pre-trained CNN architecture:'))
        self.btnviewnetwork.setText(_translate('EvaluateMl2DCnn', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('EvaluateMl2DCnn', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('EvaluateMl2DCnn', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblnfclayer.setText(_translate('EvaluateMl2DCnn', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('EvaluateMl2DCnn', ''))
        self.ldtnfclayer.setEnabled(False)
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblmasksize.setText(_translate('EvaluateMl2DCnn', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('EvaluateMl2DCnn', 'height='))
        self.ldtmaskheight.setText(_translate('EvaluateMl2DCnn', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('EvaluateMl2DCnn', 'width='))
        self.ldtmaskwidth.setText(_translate('EvaluateMl2DCnn', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('EvaluateMl2DCnn', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('EvaluateMl2DCnn', 'height='))
        self.ldtpoolheight.setText(_translate('EvaluateMl2DCnn', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('EvaluateMl2DCnn', 'width='))
        self.ldtpoolwidth.setText(_translate('EvaluateMl2DCnn', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('EvaluateMl2DCnn', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('EvaluateMl2DCnn', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('EvaluateMl2DCnn', '5000'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('EvaluateMl2DCnn', 'Evaluate 2D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnEvaluateMl2DCnn)

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
        _file = _dialog.getOpenFileName(None, 'Select CNN Network', (self.rootpath), filter='Tensorflow network files (*.meta);; All files (*.*)')
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

    def clickBtnEvaluateMl2DCnn--- This code section failed: ---

 L. 428         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 430         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 431        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in EvaulateMlCnn: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 432        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 433        44  LOAD_STR                 'Evaluate 2D-CNN'

 L. 434        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 435        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 437        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 438        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in EvaluateMl2DCnn: No CNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 439        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 440       100  LOAD_STR                 'Evaluate 2D-CNN'

 L. 441       102  LOAD_STR                 'No CNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 442       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 444       112  LOAD_FAST                'self'
              114  LOAD_ATTR                modelinfo
              116  LOAD_STR                 'feature_list'
              118  BINARY_SUBSCR    
              120  STORE_FAST               '_featurelist'

 L. 445       122  SETUP_LOOP          198  'to 198'
              124  LOAD_FAST                '_featurelist'
              126  GET_ITER         
            128_0  COME_FROM           144  '144'
              128  FOR_ITER            196  'to 196'
              130  STORE_FAST               'f'

 L. 446       132  LOAD_FAST                'self'
              134  LOAD_METHOD              checkSeisData
              136  LOAD_FAST                'f'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_CONST               False
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   128  'to 128'

 L. 447       146  LOAD_GLOBAL              vis_msg
              148  LOAD_ATTR                print
              150  LOAD_STR                 "ERROR in EvaluateMl2DCnn: Feature '%s' not found in seismic data"
              152  LOAD_FAST                'f'
              154  BINARY_MODULO    

 L. 448       156  LOAD_STR                 'error'
              158  LOAD_CONST               ('type',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  POP_TOP          

 L. 449       164  LOAD_GLOBAL              QtWidgets
              166  LOAD_ATTR                QMessageBox
              168  LOAD_METHOD              critical
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                msgbox

 L. 450       174  LOAD_STR                 'Evaluate 2D-CNN'

 L. 451       176  LOAD_STR                 "Feature '"
              178  LOAD_FAST                'f'
              180  BINARY_ADD       
              182  LOAD_STR                 "' not found in seismic data"
              184  BINARY_ADD       
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 452       190  LOAD_CONST               None
              192  RETURN_VALUE     
              194  JUMP_BACK           128  'to 128'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      122  '122'

 L. 454       198  LOAD_FAST                'self'
              200  LOAD_ATTR                modelinfo
              202  LOAD_STR                 'target'
              204  BINARY_SUBSCR    
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                seisdata
              210  LOAD_METHOD              keys
              212  CALL_METHOD_0         0  '0 positional arguments'
              214  COMPARE_OP               not-in
          216_218  POP_JUMP_IF_FALSE   280  'to 280'

 L. 455       220  LOAD_GLOBAL              vis_msg
              222  LOAD_ATTR                print
              224  LOAD_STR                 "ERROR in EvauluateMl2DCnn: Target label '%s' not found in seismic data"

 L. 456       226  LOAD_FAST                'self'
              228  LOAD_ATTR                modelinfo
              230  LOAD_STR                 'target'
              232  BINARY_SUBSCR    
              234  BINARY_MODULO    
              236  LOAD_STR                 'error'
              238  LOAD_CONST               ('type',)
              240  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              242  POP_TOP          

 L. 457       244  LOAD_GLOBAL              QtWidgets
              246  LOAD_ATTR                QMessageBox
              248  LOAD_METHOD              critical
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                msgbox

 L. 458       254  LOAD_STR                 'Evaluate 2D-CNN'

 L. 459       256  LOAD_STR                 "Target label '"
              258  LOAD_FAST                'self'
              260  LOAD_ATTR                modelinfo
              262  LOAD_STR                 'target'
              264  BINARY_SUBSCR    
              266  BINARY_ADD       
              268  LOAD_STR                 "' not found in seismic data"
              270  BINARY_ADD       
              272  CALL_METHOD_3         3  '3 positional arguments'
              274  POP_TOP          

 L. 460       276  LOAD_CONST               None
              278  RETURN_VALUE     
            280_0  COME_FROM           216  '216'

 L. 462       280  LOAD_GLOBAL              basic_data
              282  LOAD_METHOD              str2int
              284  LOAD_FAST                'self'
              286  LOAD_ATTR                ldtoldheight
              288  LOAD_METHOD              text
              290  CALL_METHOD_0         0  '0 positional arguments'
              292  CALL_METHOD_1         1  '1 positional argument'
              294  STORE_FAST               '_image_height_old'

 L. 463       296  LOAD_GLOBAL              basic_data
              298  LOAD_METHOD              str2int
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                ldtoldwidth
              304  LOAD_METHOD              text
              306  CALL_METHOD_0         0  '0 positional arguments'
              308  CALL_METHOD_1         1  '1 positional argument'
              310  STORE_FAST               '_image_width_old'

 L. 464       312  LOAD_GLOBAL              basic_data
              314  LOAD_METHOD              str2int
              316  LOAD_FAST                'self'
              318  LOAD_ATTR                ldtnewheight
              320  LOAD_METHOD              text
              322  CALL_METHOD_0         0  '0 positional arguments'
              324  CALL_METHOD_1         1  '1 positional argument'
              326  STORE_FAST               '_image_height_new'

 L. 465       328  LOAD_GLOBAL              basic_data
              330  LOAD_METHOD              str2int
              332  LOAD_FAST                'self'
              334  LOAD_ATTR                ldtnewwidth
              336  LOAD_METHOD              text
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  CALL_METHOD_1         1  '1 positional argument'
              342  STORE_FAST               '_image_width_new'

 L. 466       344  LOAD_FAST                '_image_height_old'
              346  LOAD_CONST               False
              348  COMPARE_OP               is
          350_352  POP_JUMP_IF_TRUE    384  'to 384'
              354  LOAD_FAST                '_image_width_old'
              356  LOAD_CONST               False
              358  COMPARE_OP               is
          360_362  POP_JUMP_IF_TRUE    384  'to 384'

 L. 467       364  LOAD_FAST                '_image_height_new'
              366  LOAD_CONST               False
              368  COMPARE_OP               is
          370_372  POP_JUMP_IF_TRUE    384  'to 384'
              374  LOAD_FAST                '_image_width_new'
              376  LOAD_CONST               False
              378  COMPARE_OP               is
          380_382  POP_JUMP_IF_FALSE   420  'to 420'
            384_0  COME_FROM           370  '370'
            384_1  COME_FROM           360  '360'
            384_2  COME_FROM           350  '350'

 L. 468       384  LOAD_GLOBAL              vis_msg
              386  LOAD_ATTR                print
              388  LOAD_STR                 'ERROR in EvaluateMl2DCnn: Non-integer feature size'
              390  LOAD_STR                 'error'
              392  LOAD_CONST               ('type',)
              394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              396  POP_TOP          

 L. 469       398  LOAD_GLOBAL              QtWidgets
              400  LOAD_ATTR                QMessageBox
              402  LOAD_METHOD              critical
              404  LOAD_FAST                'self'
              406  LOAD_ATTR                msgbox

 L. 470       408  LOAD_STR                 'Evaluate 2D-CNN'

 L. 471       410  LOAD_STR                 'Non-integer feature size'
              412  CALL_METHOD_3         3  '3 positional arguments'
              414  POP_TOP          

 L. 472       416  LOAD_CONST               None
              418  RETURN_VALUE     
            420_0  COME_FROM           380  '380'

 L. 473       420  LOAD_FAST                '_image_height_old'
              422  LOAD_CONST               2
              424  COMPARE_OP               <
          426_428  POP_JUMP_IF_TRUE    460  'to 460'
              430  LOAD_FAST                '_image_width_old'
              432  LOAD_CONST               2
              434  COMPARE_OP               <
          436_438  POP_JUMP_IF_TRUE    460  'to 460'

 L. 474       440  LOAD_FAST                '_image_height_new'
              442  LOAD_CONST               2
              444  COMPARE_OP               <
          446_448  POP_JUMP_IF_TRUE    460  'to 460'
              450  LOAD_FAST                '_image_width_new'
              452  LOAD_CONST               2
              454  COMPARE_OP               <
          456_458  POP_JUMP_IF_FALSE   496  'to 496'
            460_0  COME_FROM           446  '446'
            460_1  COME_FROM           436  '436'
            460_2  COME_FROM           426  '426'

 L. 475       460  LOAD_GLOBAL              vis_msg
              462  LOAD_ATTR                print
              464  LOAD_STR                 'ERROR in EvaluateMl2DCnn: Features are not 2D'
              466  LOAD_STR                 'error'
              468  LOAD_CONST               ('type',)
              470  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              472  POP_TOP          

 L. 476       474  LOAD_GLOBAL              QtWidgets
              476  LOAD_ATTR                QMessageBox
              478  LOAD_METHOD              critical
              480  LOAD_FAST                'self'
              482  LOAD_ATTR                msgbox

 L. 477       484  LOAD_STR                 'Evaluate 2D-CNN'

 L. 478       486  LOAD_STR                 'Features are not 2D'
              488  CALL_METHOD_3         3  '3 positional arguments'
              490  POP_TOP          

 L. 479       492  LOAD_CONST               None
              494  RETURN_VALUE     
            496_0  COME_FROM           456  '456'

 L. 481       496  LOAD_GLOBAL              basic_data
              498  LOAD_METHOD              str2int
              500  LOAD_FAST                'self'
              502  LOAD_ATTR                ldtbatchsize
              504  LOAD_METHOD              text
              506  CALL_METHOD_0         0  '0 positional arguments'
              508  CALL_METHOD_1         1  '1 positional argument'
              510  STORE_FAST               '_batch'

 L. 482       512  LOAD_FAST                '_batch'
              514  LOAD_CONST               False
              516  COMPARE_OP               is
          518_520  POP_JUMP_IF_TRUE    532  'to 532'
              522  LOAD_FAST                '_batch'
              524  LOAD_CONST               1
              526  COMPARE_OP               <
          528_530  POP_JUMP_IF_FALSE   568  'to 568'
            532_0  COME_FROM           518  '518'

 L. 483       532  LOAD_GLOBAL              vis_msg
              534  LOAD_ATTR                print
              536  LOAD_STR                 'ERROR in EvaluateMl2DCnn: Non-positive batch size'
              538  LOAD_STR                 'error'
              540  LOAD_CONST               ('type',)
              542  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              544  POP_TOP          

 L. 484       546  LOAD_GLOBAL              QtWidgets
              548  LOAD_ATTR                QMessageBox
              550  LOAD_METHOD              critical
              552  LOAD_FAST                'self'
              554  LOAD_ATTR                msgbox

 L. 485       556  LOAD_STR                 'Evaluate 2D-CNN'

 L. 486       558  LOAD_STR                 'Non-positive batch size'
              560  CALL_METHOD_3         3  '3 positional arguments'
              562  POP_TOP          

 L. 487       564  LOAD_CONST               None
              566  RETURN_VALUE     
            568_0  COME_FROM           528  '528'

 L. 489       568  LOAD_CONST               2
              570  LOAD_GLOBAL              int
              572  LOAD_FAST                '_image_height_old'
              574  LOAD_CONST               2
              576  BINARY_TRUE_DIVIDE
              578  CALL_FUNCTION_1       1  '1 positional argument'
              580  BINARY_MULTIPLY  
              582  LOAD_CONST               1
              584  BINARY_ADD       
              586  STORE_FAST               '_image_height_old'

 L. 490       588  LOAD_CONST               2
              590  LOAD_GLOBAL              int
              592  LOAD_FAST                '_image_width_old'
              594  LOAD_CONST               2
              596  BINARY_TRUE_DIVIDE
              598  CALL_FUNCTION_1       1  '1 positional argument'
              600  BINARY_MULTIPLY  
              602  LOAD_CONST               1
              604  BINARY_ADD       
              606  STORE_FAST               '_image_width_old'

 L. 492       608  LOAD_FAST                'self'
              610  LOAD_ATTR                modelinfo
              612  LOAD_STR                 'number_label'
              614  BINARY_SUBSCR    
              616  STORE_FAST               '_nlabel'

 L. 493       618  LOAD_FAST                'self'
              620  LOAD_ATTR                modelinfo
              622  LOAD_STR                 'target'
              624  BINARY_SUBSCR    
              626  STORE_FAST               '_target'

 L. 495       628  LOAD_CONST               0
              630  STORE_FAST               '_wdinl'

 L. 496       632  LOAD_CONST               0
              634  STORE_FAST               '_wdxl'

 L. 497       636  LOAD_CONST               0
              638  STORE_FAST               '_wdz'

 L. 498       640  LOAD_FAST                'self'
              642  LOAD_ATTR                cbbornt
              644  LOAD_METHOD              currentIndex
              646  CALL_METHOD_0         0  '0 positional arguments'
              648  LOAD_CONST               0
              650  COMPARE_OP               ==
          652_654  POP_JUMP_IF_FALSE   680  'to 680'

 L. 499       656  LOAD_GLOBAL              int
              658  LOAD_FAST                '_image_width_old'
              660  LOAD_CONST               2
              662  BINARY_TRUE_DIVIDE
              664  CALL_FUNCTION_1       1  '1 positional argument'
              666  STORE_FAST               '_wdxl'

 L. 500       668  LOAD_GLOBAL              int
              670  LOAD_FAST                '_image_height_old'
              672  LOAD_CONST               2
              674  BINARY_TRUE_DIVIDE
              676  CALL_FUNCTION_1       1  '1 positional argument'
              678  STORE_FAST               '_wdz'
            680_0  COME_FROM           652  '652'

 L. 501       680  LOAD_FAST                'self'
              682  LOAD_ATTR                cbbornt
              684  LOAD_METHOD              currentIndex
              686  CALL_METHOD_0         0  '0 positional arguments'
              688  LOAD_CONST               1
              690  COMPARE_OP               ==
          692_694  POP_JUMP_IF_FALSE   720  'to 720'

 L. 502       696  LOAD_GLOBAL              int
              698  LOAD_FAST                '_image_width_old'
              700  LOAD_CONST               2
              702  BINARY_TRUE_DIVIDE
              704  CALL_FUNCTION_1       1  '1 positional argument'
              706  STORE_FAST               '_wdinl'

 L. 503       708  LOAD_GLOBAL              int
              710  LOAD_FAST                '_image_height_old'
              712  LOAD_CONST               2
              714  BINARY_TRUE_DIVIDE
              716  CALL_FUNCTION_1       1  '1 positional argument'
              718  STORE_FAST               '_wdz'
            720_0  COME_FROM           692  '692'

 L. 504       720  LOAD_FAST                'self'
              722  LOAD_ATTR                cbbornt
              724  LOAD_METHOD              currentIndex
              726  CALL_METHOD_0         0  '0 positional arguments'
              728  LOAD_CONST               2
              730  COMPARE_OP               ==
          732_734  POP_JUMP_IF_FALSE   760  'to 760'

 L. 505       736  LOAD_GLOBAL              int
              738  LOAD_FAST                '_image_width_old'
              740  LOAD_CONST               2
              742  BINARY_TRUE_DIVIDE
              744  CALL_FUNCTION_1       1  '1 positional argument'
              746  STORE_FAST               '_wdinl'

 L. 506       748  LOAD_GLOBAL              int
              750  LOAD_FAST                '_image_height_old'
              752  LOAD_CONST               2
              754  BINARY_TRUE_DIVIDE
              756  CALL_FUNCTION_1       1  '1 positional argument'
              758  STORE_FAST               '_wdxl'
            760_0  COME_FROM           732  '732'

 L. 508       760  LOAD_FAST                'self'
              762  LOAD_ATTR                survinfo
              764  STORE_FAST               '_seisinfo'

 L. 510       766  LOAD_GLOBAL              seis_ays
              768  LOAD_ATTR                removeOutofSurveySample
              770  LOAD_GLOBAL              seis_ays
              772  LOAD_METHOD              convertSeisInfoTo2DMat
              774  LOAD_FAST                'self'
              776  LOAD_ATTR                survinfo
              778  CALL_METHOD_1         1  '1 positional argument'

 L. 511       780  LOAD_FAST                '_seisinfo'
              782  LOAD_STR                 'ILStart'
              784  BINARY_SUBSCR    
              786  LOAD_FAST                '_wdinl'
              788  LOAD_FAST                '_seisinfo'
              790  LOAD_STR                 'ILStep'
              792  BINARY_SUBSCR    
              794  BINARY_MULTIPLY  
              796  BINARY_ADD       

 L. 512       798  LOAD_FAST                '_seisinfo'
              800  LOAD_STR                 'ILEnd'
              802  BINARY_SUBSCR    
              804  LOAD_FAST                '_wdinl'
              806  LOAD_FAST                '_seisinfo'
              808  LOAD_STR                 'ILStep'
              810  BINARY_SUBSCR    
              812  BINARY_MULTIPLY  
              814  BINARY_SUBTRACT  

 L. 513       816  LOAD_FAST                '_seisinfo'
              818  LOAD_STR                 'XLStart'
              820  BINARY_SUBSCR    
              822  LOAD_FAST                '_wdxl'
              824  LOAD_FAST                '_seisinfo'
              826  LOAD_STR                 'XLStep'
              828  BINARY_SUBSCR    
              830  BINARY_MULTIPLY  
              832  BINARY_ADD       

 L. 514       834  LOAD_FAST                '_seisinfo'
              836  LOAD_STR                 'XLEnd'
              838  BINARY_SUBSCR    
              840  LOAD_FAST                '_wdxl'
              842  LOAD_FAST                '_seisinfo'
              844  LOAD_STR                 'XLStep'
              846  BINARY_SUBSCR    
              848  BINARY_MULTIPLY  
              850  BINARY_SUBTRACT  

 L. 515       852  LOAD_FAST                '_seisinfo'
              854  LOAD_STR                 'ZStart'
              856  BINARY_SUBSCR    
              858  LOAD_FAST                '_wdz'
              860  LOAD_FAST                '_seisinfo'
              862  LOAD_STR                 'ZStep'
              864  BINARY_SUBSCR    
              866  BINARY_MULTIPLY  
              868  BINARY_ADD       

 L. 516       870  LOAD_FAST                '_seisinfo'
              872  LOAD_STR                 'ZEnd'
              874  BINARY_SUBSCR    
              876  LOAD_FAST                '_wdz'
              878  LOAD_FAST                '_seisinfo'
              880  LOAD_STR                 'ZStep'
              882  BINARY_SUBSCR    
              884  BINARY_MULTIPLY  
              886  BINARY_SUBTRACT  
              888  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
              890  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              892  STORE_FAST               '_data'

 L. 518       894  BUILD_MAP_0           0 
              896  STORE_FAST               '_seisdict'

 L. 519       898  LOAD_FAST                '_data'
              900  LOAD_CONST               None
              902  LOAD_CONST               None
              904  BUILD_SLICE_2         2 
              906  LOAD_CONST               0
              908  LOAD_CONST               1
              910  BUILD_SLICE_2         2 
              912  BUILD_TUPLE_2         2 
              914  BINARY_SUBSCR    
              916  LOAD_FAST                '_seisdict'
              918  LOAD_STR                 'Inline'
              920  STORE_SUBSCR     

 L. 520       922  LOAD_FAST                '_data'
              924  LOAD_CONST               None
              926  LOAD_CONST               None
              928  BUILD_SLICE_2         2 
              930  LOAD_CONST               1
              932  LOAD_CONST               2
              934  BUILD_SLICE_2         2 
              936  BUILD_TUPLE_2         2 
              938  BINARY_SUBSCR    
              940  LOAD_FAST                '_seisdict'
              942  LOAD_STR                 'Crossline'
              944  STORE_SUBSCR     

 L. 521       946  LOAD_FAST                '_data'
              948  LOAD_CONST               None
              950  LOAD_CONST               None
              952  BUILD_SLICE_2         2 
              954  LOAD_CONST               2
              956  LOAD_CONST               3
              958  BUILD_SLICE_2         2 
              960  BUILD_TUPLE_2         2 
              962  BINARY_SUBSCR    
              964  LOAD_FAST                '_seisdict'
              966  LOAD_STR                 'Z'
              968  STORE_SUBSCR     

 L. 523       970  LOAD_GLOBAL              basic_mdt
              972  LOAD_METHOD              maxDictConstantRow
              974  LOAD_FAST                '_seisdict'
              976  CALL_METHOD_1         1  '1 positional argument'
              978  STORE_FAST               '_nsample'

 L. 525       980  LOAD_GLOBAL              int
              982  LOAD_GLOBAL              np
              984  LOAD_METHOD              ceil
              986  LOAD_FAST                '_nsample'
              988  LOAD_FAST                '_batch'
              990  BINARY_TRUE_DIVIDE
              992  CALL_METHOD_1         1  '1 positional argument'
              994  CALL_FUNCTION_1       1  '1 positional argument'
              996  STORE_FAST               '_nloop'

 L. 528       998  LOAD_GLOBAL              QtWidgets
             1000  LOAD_METHOD              QProgressDialog
             1002  CALL_METHOD_0         0  '0 positional arguments'
             1004  STORE_FAST               '_pgsdlg'

 L. 529      1006  LOAD_GLOBAL              QtGui
             1008  LOAD_METHOD              QIcon
             1010  CALL_METHOD_0         0  '0 positional arguments'
             1012  STORE_FAST               'icon'

 L. 530      1014  LOAD_FAST                'icon'
             1016  LOAD_METHOD              addPixmap
             1018  LOAD_GLOBAL              QtGui
             1020  LOAD_METHOD              QPixmap
             1022  LOAD_GLOBAL              os
             1024  LOAD_ATTR                path
             1026  LOAD_METHOD              join
             1028  LOAD_FAST                'self'
             1030  LOAD_ATTR                iconpath
             1032  LOAD_STR                 'icons/check.png'
             1034  CALL_METHOD_2         2  '2 positional arguments'
             1036  CALL_METHOD_1         1  '1 positional argument'

 L. 531      1038  LOAD_GLOBAL              QtGui
             1040  LOAD_ATTR                QIcon
             1042  LOAD_ATTR                Normal
             1044  LOAD_GLOBAL              QtGui
             1046  LOAD_ATTR                QIcon
             1048  LOAD_ATTR                Off
             1050  CALL_METHOD_3         3  '3 positional arguments'
             1052  POP_TOP          

 L. 532      1054  LOAD_FAST                '_pgsdlg'
             1056  LOAD_METHOD              setWindowIcon
             1058  LOAD_FAST                'icon'
             1060  CALL_METHOD_1         1  '1 positional argument'
             1062  POP_TOP          

 L. 533      1064  LOAD_FAST                '_pgsdlg'
             1066  LOAD_METHOD              setWindowTitle
             1068  LOAD_STR                 'Evaluate 2D-CNN'
             1070  CALL_METHOD_1         1  '1 positional argument'
             1072  POP_TOP          

 L. 534      1074  LOAD_FAST                '_pgsdlg'
             1076  LOAD_METHOD              setCancelButton
             1078  LOAD_CONST               None
             1080  CALL_METHOD_1         1  '1 positional argument'
             1082  POP_TOP          

 L. 535      1084  LOAD_FAST                '_pgsdlg'
             1086  LOAD_METHOD              setWindowFlags
             1088  LOAD_GLOBAL              QtCore
             1090  LOAD_ATTR                Qt
             1092  LOAD_ATTR                WindowStaysOnTopHint
             1094  CALL_METHOD_1         1  '1 positional argument'
             1096  POP_TOP          

 L. 536      1098  LOAD_FAST                '_pgsdlg'
             1100  LOAD_METHOD              forceShow
             1102  CALL_METHOD_0         0  '0 positional arguments'
             1104  POP_TOP          

 L. 537      1106  LOAD_FAST                '_pgsdlg'
             1108  LOAD_METHOD              setFixedWidth
             1110  LOAD_CONST               400
             1112  CALL_METHOD_1         1  '1 positional argument'
             1114  POP_TOP          

 L. 538      1116  LOAD_FAST                '_pgsdlg'
             1118  LOAD_METHOD              setMaximum
             1120  LOAD_FAST                '_nloop'
             1122  CALL_METHOD_1         1  '1 positional argument'
             1124  POP_TOP          

 L. 540      1126  LOAD_GLOBAL              np
             1128  LOAD_METHOD              zeros
             1130  LOAD_FAST                '_nlabel'
             1132  LOAD_CONST               1
             1134  BINARY_ADD       
             1136  LOAD_FAST                '_nlabel'
             1138  LOAD_CONST               1
             1140  BINARY_ADD       
             1142  BUILD_LIST_2          2 
             1144  CALL_METHOD_1         1  '1 positional argument'
             1146  STORE_FAST               '_result'

 L. 541      1148  LOAD_CONST               0
             1150  STORE_FAST               'idxstart'

 L. 542  1152_1154  SETUP_LOOP         1608  'to 1608'
             1156  LOAD_GLOBAL              range
             1158  LOAD_FAST                '_nloop'
             1160  CALL_FUNCTION_1       1  '1 positional argument'
             1162  GET_ITER         
         1164_1166  FOR_ITER           1606  'to 1606'
             1168  STORE_FAST               'i'

 L. 544      1170  LOAD_GLOBAL              QtCore
             1172  LOAD_ATTR                QCoreApplication
             1174  LOAD_METHOD              instance
             1176  CALL_METHOD_0         0  '0 positional arguments'
             1178  LOAD_METHOD              processEvents
             1180  CALL_METHOD_0         0  '0 positional arguments'
             1182  POP_TOP          

 L. 546      1184  LOAD_GLOBAL              sys
             1186  LOAD_ATTR                stdout
             1188  LOAD_METHOD              write

 L. 547      1190  LOAD_STR                 '\r>>> Evaluate 2D-CNN, proceeding %.1f%% '
             1192  LOAD_GLOBAL              float
             1194  LOAD_FAST                'i'
             1196  LOAD_CONST               1
             1198  BINARY_ADD       
             1200  CALL_FUNCTION_1       1  '1 positional argument'
             1202  LOAD_GLOBAL              float
             1204  LOAD_FAST                '_nloop'
             1206  CALL_FUNCTION_1       1  '1 positional argument'
             1208  BINARY_TRUE_DIVIDE
             1210  LOAD_CONST               100.0
             1212  BINARY_MULTIPLY  
             1214  BINARY_MODULO    
             1216  CALL_METHOD_1         1  '1 positional argument'
             1218  POP_TOP          

 L. 548      1220  LOAD_GLOBAL              sys
             1222  LOAD_ATTR                stdout
             1224  LOAD_METHOD              flush
             1226  CALL_METHOD_0         0  '0 positional arguments'
             1228  POP_TOP          

 L. 550      1230  LOAD_FAST                'idxstart'
             1232  LOAD_FAST                '_batch'
             1234  BINARY_ADD       
             1236  STORE_FAST               'idxend'

 L. 551      1238  LOAD_FAST                'idxend'
             1240  LOAD_FAST                '_nsample'
             1242  COMPARE_OP               >
         1244_1246  POP_JUMP_IF_FALSE  1252  'to 1252'

 L. 552      1248  LOAD_FAST                '_nsample'
             1250  STORE_FAST               'idxend'
           1252_0  COME_FROM          1244  '1244'

 L. 553      1252  LOAD_GLOBAL              np
             1254  LOAD_METHOD              linspace
             1256  LOAD_FAST                'idxstart'
             1258  LOAD_FAST                'idxend'
             1260  LOAD_CONST               1
             1262  BINARY_SUBTRACT  
             1264  LOAD_FAST                'idxend'
             1266  LOAD_FAST                'idxstart'
             1268  BINARY_SUBTRACT  
             1270  CALL_METHOD_3         3  '3 positional arguments'
             1272  LOAD_METHOD              astype
             1274  LOAD_GLOBAL              int
             1276  CALL_METHOD_1         1  '1 positional argument'
             1278  STORE_FAST               'idxlist'

 L. 554      1280  LOAD_FAST                'idxend'
             1282  STORE_FAST               'idxstart'

 L. 555      1284  LOAD_GLOBAL              basic_mdt
             1286  LOAD_METHOD              retrieveDictByIndex
             1288  LOAD_FAST                '_seisdict'
             1290  LOAD_FAST                'idxlist'
             1292  CALL_METHOD_2         2  '2 positional arguments'
             1294  STORE_FAST               '_dict'

 L. 557      1296  LOAD_FAST                '_dict'
             1298  LOAD_STR                 'Inline'
             1300  BINARY_SUBSCR    
             1302  STORE_FAST               '_targetdata'

 L. 558      1304  LOAD_GLOBAL              np
             1306  LOAD_ATTR                concatenate
             1308  LOAD_FAST                '_targetdata'
             1310  LOAD_FAST                '_dict'
             1312  LOAD_STR                 'Crossline'
             1314  BINARY_SUBSCR    
             1316  BUILD_TUPLE_2         2 
             1318  LOAD_CONST               1
             1320  LOAD_CONST               ('axis',)
             1322  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1324  STORE_FAST               '_targetdata'

 L. 559      1326  LOAD_GLOBAL              np
             1328  LOAD_ATTR                concatenate
             1330  LOAD_FAST                '_targetdata'
             1332  LOAD_FAST                '_dict'
             1334  LOAD_STR                 'Z'
             1336  BINARY_SUBSCR    
             1338  BUILD_TUPLE_2         2 
             1340  LOAD_CONST               1
             1342  LOAD_CONST               ('axis',)
             1344  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1346  STORE_FAST               '_targetdata'

 L. 560      1348  SETUP_LOOP         1468  'to 1468'
             1350  LOAD_FAST                '_featurelist'
             1352  GET_ITER         
           1354_0  COME_FROM          1430  '1430'
             1354  FOR_ITER           1466  'to 1466'
             1356  STORE_FAST               'f'

 L. 561      1358  LOAD_FAST                'self'
             1360  LOAD_ATTR                seisdata
             1362  LOAD_FAST                'f'
             1364  BINARY_SUBSCR    
             1366  STORE_FAST               '_data'

 L. 562      1368  LOAD_GLOBAL              seis_ays
             1370  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1372  LOAD_FAST                '_data'
             1374  LOAD_FAST                '_targetdata'
             1376  LOAD_FAST                'self'
             1378  LOAD_ATTR                survinfo

 L. 563      1380  LOAD_FAST                '_wdinl'
             1382  LOAD_FAST                '_wdxl'
             1384  LOAD_FAST                '_wdz'

 L. 564      1386  LOAD_CONST               False
             1388  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1390  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1392  LOAD_CONST               None
             1394  LOAD_CONST               None
             1396  BUILD_SLICE_2         2 
             1398  LOAD_CONST               3
             1400  LOAD_CONST               None
             1402  BUILD_SLICE_2         2 
             1404  BUILD_TUPLE_2         2 
             1406  BINARY_SUBSCR    
             1408  LOAD_FAST                '_dict'
             1410  LOAD_FAST                'f'
             1412  STORE_SUBSCR     

 L. 565      1414  LOAD_FAST                '_image_height_new'
             1416  LOAD_FAST                '_image_height_old'
             1418  COMPARE_OP               !=
         1420_1422  POP_JUMP_IF_TRUE   1434  'to 1434'
             1424  LOAD_FAST                '_image_width_new'
             1426  LOAD_FAST                '_image_width_old'
             1428  COMPARE_OP               !=
         1430_1432  POP_JUMP_IF_FALSE  1354  'to 1354'
           1434_0  COME_FROM          1420  '1420'

 L. 566      1434  LOAD_GLOBAL              basic_image
             1436  LOAD_ATTR                changeImageSize
             1438  LOAD_FAST                '_dict'
             1440  LOAD_FAST                'f'
             1442  BINARY_SUBSCR    

 L. 567      1444  LOAD_FAST                '_image_height_old'

 L. 568      1446  LOAD_FAST                '_image_width_old'

 L. 569      1448  LOAD_FAST                '_image_height_new'

 L. 570      1450  LOAD_FAST                '_image_width_new'
             1452  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1454  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1456  LOAD_FAST                '_dict'
             1458  LOAD_FAST                'f'
             1460  STORE_SUBSCR     
         1462_1464  JUMP_BACK          1354  'to 1354'
             1466  POP_BLOCK        
           1468_0  COME_FROM_LOOP     1348  '1348'

 L. 572      1468  LOAD_FAST                '_target'
             1470  LOAD_FAST                '_featurelist'
             1472  COMPARE_OP               not-in
         1474_1476  POP_JUMP_IF_FALSE  1528  'to 1528'

 L. 573      1478  LOAD_FAST                'self'
             1480  LOAD_ATTR                seisdata
             1482  LOAD_FAST                '_target'
             1484  BINARY_SUBSCR    
             1486  STORE_FAST               '_data'

 L. 574      1488  LOAD_GLOBAL              seis_ays
             1490  LOAD_ATTR                retrieveSeisSampleFrom3DMat
             1492  LOAD_FAST                '_data'
             1494  LOAD_FAST                '_targetdata'

 L. 575      1496  LOAD_FAST                'self'
             1498  LOAD_ATTR                survinfo

 L. 576      1500  LOAD_CONST               False
             1502  LOAD_CONST               ('seisinfo', 'verbose')
             1504  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1506  LOAD_CONST               None
             1508  LOAD_CONST               None
             1510  BUILD_SLICE_2         2 
             1512  LOAD_CONST               3
             1514  LOAD_CONST               None
             1516  BUILD_SLICE_2         2 
             1518  BUILD_TUPLE_2         2 
             1520  BINARY_SUBSCR    
             1522  LOAD_FAST                '_dict'
             1524  LOAD_FAST                '_target'
             1526  STORE_SUBSCR     
           1528_0  COME_FROM          1474  '1474'

 L. 577      1528  LOAD_GLOBAL              np
             1530  LOAD_METHOD              round
             1532  LOAD_FAST                '_dict'
             1534  LOAD_FAST                '_target'
             1536  BINARY_SUBSCR    
             1538  CALL_METHOD_1         1  '1 positional argument'
             1540  LOAD_METHOD              astype
             1542  LOAD_GLOBAL              int
             1544  CALL_METHOD_1         1  '1 positional argument'
             1546  LOAD_FAST                '_dict'
             1548  LOAD_FAST                '_target'
             1550  STORE_SUBSCR     

 L. 579      1552  LOAD_GLOBAL              ml_cnn
             1554  LOAD_ATTR                evaluateCNNClassifier
             1556  LOAD_FAST                '_dict'

 L. 580      1558  LOAD_FAST                'self'
             1560  LOAD_ATTR                modelpath

 L. 581      1562  LOAD_FAST                'self'
             1564  LOAD_ATTR                modelname

 L. 582      1566  LOAD_FAST                '_batch'

 L. 583      1568  LOAD_CONST               True
             1570  LOAD_CONST               ('cnnpath', 'cnnname', 'batchsize', 'verbose')
             1572  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1574  STORE_FAST               '_confmatrix'

 L. 584      1576  LOAD_FAST                '_result'
             1578  LOAD_FAST                '_confmatrix'
             1580  LOAD_STR                 'confusion_matrix'
             1582  BINARY_SUBSCR    
             1584  BINARY_ADD       
             1586  STORE_FAST               '_result'

 L. 586      1588  LOAD_FAST                '_pgsdlg'
             1590  LOAD_METHOD              setValue
             1592  LOAD_FAST                'i'
             1594  LOAD_CONST               1
             1596  BINARY_ADD       
             1598  CALL_METHOD_1         1  '1 positional argument'
             1600  POP_TOP          
         1602_1604  JUMP_BACK          1164  'to 1164'
             1606  POP_BLOCK        
           1608_0  COME_FROM_LOOP     1152  '1152'

 L. 588      1608  LOAD_GLOBAL              print
             1610  LOAD_STR                 'Done'
             1612  CALL_FUNCTION_1       1  '1 positional argument'
             1614  POP_TOP          

 L. 590      1616  LOAD_FAST                '_result'
             1618  LOAD_CONST               0
             1620  LOAD_CONST               1
             1622  LOAD_CONST               None
             1624  BUILD_SLICE_2         2 
             1626  BUILD_TUPLE_2         2 
             1628  BINARY_SUBSCR    
             1630  LOAD_FAST                '_nloop'
             1632  BINARY_TRUE_DIVIDE
             1634  LOAD_FAST                '_result'
             1636  LOAD_CONST               0
             1638  LOAD_CONST               1
             1640  LOAD_CONST               None
             1642  BUILD_SLICE_2         2 
             1644  BUILD_TUPLE_2         2 
             1646  STORE_SUBSCR     

 L. 591      1648  LOAD_FAST                '_result'
             1650  LOAD_CONST               1
             1652  LOAD_CONST               None
             1654  BUILD_SLICE_2         2 
             1656  LOAD_CONST               0
             1658  BUILD_TUPLE_2         2 
             1660  BINARY_SUBSCR    
             1662  LOAD_FAST                '_nloop'
             1664  BINARY_TRUE_DIVIDE
             1666  LOAD_FAST                '_result'
             1668  LOAD_CONST               1
             1670  LOAD_CONST               None
             1672  BUILD_SLICE_2         2 
             1674  LOAD_CONST               0
             1676  BUILD_TUPLE_2         2 
             1678  STORE_SUBSCR     

 L. 592      1680  LOAD_GLOBAL              print
             1682  LOAD_FAST                '_result'
             1684  CALL_FUNCTION_1       1  '1 positional argument'
             1686  POP_TOP          

 L. 597      1688  LOAD_GLOBAL              QtWidgets
             1690  LOAD_METHOD              QDialog
             1692  CALL_METHOD_0         0  '0 positional arguments'
             1694  STORE_FAST               '_viewmlconfmat'

 L. 598      1696  LOAD_GLOBAL              gui_viewmlconfmat
             1698  CALL_FUNCTION_0       0  '0 positional arguments'
             1700  STORE_FAST               '_gui'

 L. 599      1702  LOAD_FAST                '_result'
             1704  LOAD_FAST                '_gui'
             1706  STORE_ATTR               confmat

 L. 600      1708  LOAD_FAST                '_gui'
             1710  LOAD_METHOD              setupGUI
             1712  LOAD_FAST                '_viewmlconfmat'
             1714  CALL_METHOD_1         1  '1 positional argument'
             1716  POP_TOP          

 L. 601      1718  LOAD_FAST                '_viewmlconfmat'
             1720  LOAD_METHOD              exec
             1722  CALL_METHOD_0         0  '0 positional arguments'
             1724  POP_TOP          

 L. 602      1726  LOAD_FAST                '_viewmlconfmat'
             1728  LOAD_METHOD              show
             1730  CALL_METHOD_0         0  '0 positional arguments'
             1732  POP_TOP          

Parse error at or near `CALL_METHOD_0' instruction at offset 1730

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
    EvaluateMl2DCnn = QtWidgets.QWidget()
    gui = evaluateml2dcnn()
    gui.setupGUI(EvaluateMl2DCnn)
    EvaluateMl2DCnn.show()
    sys.exit(app.exec_())