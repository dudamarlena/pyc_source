# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\extractml2dcnn.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 33776 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.image as basic_image
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.cnnclassifier as ml_cnn
import cognitivegeo.src.gui.viewml2dcnn as gui_viewml2dcnn
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class extractml2dcnn(object):
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

    def setupGUI(self, ExtractMl2DCnn):
        ExtractMl2DCnn.setObjectName('ExtractMl2DCnn')
        ExtractMl2DCnn.setFixedSize(800, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/retrieve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ExtractMl2DCnn.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ExtractMl2DCnn)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ExtractMl2DCnn)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ExtractMl2DCnn)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lblornt = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(ExtractMl2DCnn)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 220, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 220, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(ExtractMl2DCnn)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 220, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 260, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(ExtractMl2DCnn)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 260, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 220, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 220, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(ExtractMl2DCnn)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 220, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 260, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(ExtractMl2DCnn)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 260, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ExtractMl2DCnn)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ExtractMl2DCnn)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ExtractMl2DCnn)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 130))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(ExtractMl2DCnn)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(ExtractMl2DCnn)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 140, 180, 130))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ExtractMl2DCnn)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ExtractMl2DCnn)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ExtractMl2DCnn)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ExtractMl2DCnn)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.lblpara = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ExtractMl2DCnn)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lbltype = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lbltype.setObjectName('lbltype')
        self.lbltype.setGeometry(QtCore.QRect(10, 400, 130, 30))
        self.cbbtype = QtWidgets.QComboBox(ExtractMl2DCnn)
        self.cbbtype.setObjectName('cbbtype')
        self.cbbtype.setGeometry(QtCore.QRect(150, 400, 240, 30))
        self.lblsave = QtWidgets.QLabel(ExtractMl2DCnn)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExtractMl2DCnn)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(150, 440, 100, 30))
        self.btnapply = QtWidgets.QPushButton(ExtractMl2DCnn)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/retrieve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ExtractMl2DCnn)
        self.msgbox.setObjectName('msgbox')
        _center_x = ExtractMl2DCnn.geometry().center().x()
        _center_y = ExtractMl2DCnn.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ExtractMl2DCnn)
        QtCore.QMetaObject.connectSlotsByName(ExtractMl2DCnn)

    def retranslateGUI(self, ExtractMl2DCnn):
        self.dialog = ExtractMl2DCnn
        _translate = QtCore.QCoreApplication.translate
        ExtractMl2DCnn.setWindowTitle(_translate('ExtractMl2DCnn', 'Extract 2D-CNN'))
        self.lblfrom.setText(_translate('ExtractMl2DCnn', 'Select network:'))
        self.ldtfrom.setText(_translate('ExtractMl2DCnn', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ExtractMl2DCnn', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ExtractMl2DCnn', 'Training features:'))
        self.lblornt.setText(_translate('ExtractMl2DCnn', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.lbloldsize.setText(_translate('ExtractMl2DCnn', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('ExtractMl2DCnn', 'height='))
        self.ldtoldheight.setText(_translate('ExtractMl2DCnn', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('ExtractMl2DCnn', 'width='))
        self.ldtoldwidth.setText(_translate('ExtractMl2DCnn', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('ExtractMl2DCnn', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('ExtractMl2DCnn', 'height='))
        self.ldtnewheight.setText(_translate('ExtractMl2DCnn', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewheight.setEnabled(False)
        self.lblnewwidth.setText(_translate('ExtractMl2DCnn', 'width='))
        self.ldtnewwidth.setText(_translate('ExtractMl2DCnn', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewwidth.setEnabled(False)
        self.lblnetwork.setText(_translate('ExtractMl2DCnn', 'Pre-trained CNN architecture:'))
        self.btnviewnetwork.setText(_translate('ApplyMlCnn', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('ApplyMl2DCnn', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ApplyMl2DCnn', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblnfclayer.setText(_translate('ApplyMl2DCnn', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('ApplyMl2DCnn', ''))
        self.ldtnfclayer.setEnabled(False)
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblmasksize.setText(_translate('ExtractMl2DCnn', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ExtractMl2DCnn', 'height='))
        self.ldtmaskheight.setText(_translate('ExtractMl2DCnn', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ExtractMl2DCnn', 'width='))
        self.ldtmaskwidth.setText(_translate('ExtractMl2DCnn', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ExtractMl2DCnn', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ExtractMl2DCnn', 'height='))
        self.ldtpoolheight.setText(_translate('ExtractMl2DCnn', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ExtractMl2DCnn', 'width='))
        self.ldtpoolwidth.setText(_translate('ExtractMl2DCnn', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ExtractMl2DCnn', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ExtractMl2DCnn', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ExtractMl2DCnn', '5000'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltype.setText(_translate('ExtractMl2DCnn', 'Target layer='))
        self.lbltype.setAlignment(QtCore.Qt.AlignRight)
        self.lblsave.setText(_translate('ExtractMl2DCnn', 'Output prefix='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ExtractMl2DCnn', 'cnn_feature_'))
        self.btnapply.setText(_translate('ExtractMl2DCnn', 'Extract 2D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnExtractMl2DCnn)

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
            self.cbbtype.clear()
            _nblock = self.modelinfo['number_conv_block']
            _nlayer = self.modelinfo['number_conv_layer']
            _nfeature = self.modelinfo['number_conv_feature']
            _featurelist = []
            for i in range(_nblock):
                for j in range(_nlayer[i]):
                    _featurelist.append('Convolution block No. ' + str(i + 1) + ', layer No. ' + str(j + 1) + ' ----- ' + str(_nfeature[i]) + ' masks')

            self.cbbtype.addItems(_featurelist)
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
            self.cbbtype.clear()

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

    def clickBtnExtractMl2DCnn--- This code section failed: ---

 L. 447         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 449         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 450        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in ExtractMl2DCnn: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 451        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 452        44  LOAD_STR                 'Extract 2D-CNN'

 L. 453        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 454        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 456        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 457        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in ExtractMl2DCnn: No CNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 458        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 459       100  LOAD_STR                 'Extract 2D-CNN'

 L. 460       102  LOAD_STR                 'No CNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 461       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 463       112  LOAD_FAST                'self'
              114  LOAD_ATTR                modelinfo
              116  LOAD_STR                 'feature_list'
              118  BINARY_SUBSCR    
              120  STORE_FAST               '_featurelist'

 L. 464       122  SETUP_LOOP          198  'to 198'
              124  LOAD_FAST                '_featurelist'
              126  GET_ITER         
            128_0  COME_FROM           144  '144'
              128  FOR_ITER            196  'to 196'
              130  STORE_FAST               'f'

 L. 465       132  LOAD_FAST                'self'
              134  LOAD_METHOD              checkSeisData
              136  LOAD_FAST                'f'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_CONST               False
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   128  'to 128'

 L. 466       146  LOAD_GLOBAL              vis_msg
              148  LOAD_ATTR                print
              150  LOAD_STR                 "ERROR in ExtractMl2DCnn: Feature '%s' not found in seismic data"
              152  LOAD_FAST                'f'
              154  BINARY_MODULO    

 L. 467       156  LOAD_STR                 'error'
              158  LOAD_CONST               ('type',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  POP_TOP          

 L. 468       164  LOAD_GLOBAL              QtWidgets
              166  LOAD_ATTR                QMessageBox
              168  LOAD_METHOD              critical
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                msgbox

 L. 469       174  LOAD_STR                 'Extract 2D-CNN'

 L. 470       176  LOAD_STR                 "Feature '"
              178  LOAD_FAST                'f'
              180  BINARY_ADD       
              182  LOAD_STR                 "' not found in seismic data"
              184  BINARY_ADD       
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 471       190  LOAD_CONST               None
              192  RETURN_VALUE     
              194  JUMP_BACK           128  'to 128'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      122  '122'

 L. 473       198  LOAD_GLOBAL              basic_data
              200  LOAD_METHOD              str2int
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                ldtoldheight
              206  LOAD_METHOD              text
              208  CALL_METHOD_0         0  '0 positional arguments'
              210  CALL_METHOD_1         1  '1 positional argument'
              212  STORE_FAST               '_image_height_old'

 L. 474       214  LOAD_GLOBAL              basic_data
              216  LOAD_METHOD              str2int
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                ldtoldwidth
              222  LOAD_METHOD              text
              224  CALL_METHOD_0         0  '0 positional arguments'
              226  CALL_METHOD_1         1  '1 positional argument'
              228  STORE_FAST               '_image_width_old'

 L. 475       230  LOAD_GLOBAL              basic_data
              232  LOAD_METHOD              str2int
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                ldtnewheight
              238  LOAD_METHOD              text
              240  CALL_METHOD_0         0  '0 positional arguments'
              242  CALL_METHOD_1         1  '1 positional argument'
              244  STORE_FAST               '_image_height_new'

 L. 476       246  LOAD_GLOBAL              basic_data
              248  LOAD_METHOD              str2int
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                ldtnewwidth
              254  LOAD_METHOD              text
              256  CALL_METHOD_0         0  '0 positional arguments'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  STORE_FAST               '_image_width_new'

 L. 477       262  LOAD_FAST                '_image_height_old'
              264  LOAD_CONST               False
              266  COMPARE_OP               is
          268_270  POP_JUMP_IF_TRUE    302  'to 302'
              272  LOAD_FAST                '_image_width_old'
              274  LOAD_CONST               False
              276  COMPARE_OP               is
          278_280  POP_JUMP_IF_TRUE    302  'to 302'

 L. 478       282  LOAD_FAST                '_image_height_new'
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

 L. 479       302  LOAD_GLOBAL              vis_msg
              304  LOAD_ATTR                print
              306  LOAD_STR                 'ERROR in ExtractMl2DCnn: Non-integer feature size'
              308  LOAD_STR                 'error'
              310  LOAD_CONST               ('type',)
              312  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              314  POP_TOP          

 L. 480       316  LOAD_GLOBAL              QtWidgets
              318  LOAD_ATTR                QMessageBox
              320  LOAD_METHOD              critical
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                msgbox

 L. 481       326  LOAD_STR                 'Extract 2D-CNN'

 L. 482       328  LOAD_STR                 'Non-integer feature size'
              330  CALL_METHOD_3         3  '3 positional arguments'
              332  POP_TOP          

 L. 483       334  LOAD_CONST               None
              336  RETURN_VALUE     
            338_0  COME_FROM           298  '298'

 L. 484       338  LOAD_FAST                '_image_height_old'
              340  LOAD_CONST               2
              342  COMPARE_OP               <
          344_346  POP_JUMP_IF_TRUE    378  'to 378'
              348  LOAD_FAST                '_image_width_old'
              350  LOAD_CONST               2
              352  COMPARE_OP               <
          354_356  POP_JUMP_IF_TRUE    378  'to 378'

 L. 485       358  LOAD_FAST                '_image_height_new'
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

 L. 486       378  LOAD_GLOBAL              vis_msg
              380  LOAD_ATTR                print
              382  LOAD_STR                 'ERROR in ExtractMl2DCnn: Features are not 2D'
              384  LOAD_STR                 'error'
              386  LOAD_CONST               ('type',)
              388  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              390  POP_TOP          

 L. 487       392  LOAD_GLOBAL              QtWidgets
              394  LOAD_ATTR                QMessageBox
              396  LOAD_METHOD              critical
              398  LOAD_FAST                'self'
              400  LOAD_ATTR                msgbox

 L. 488       402  LOAD_STR                 'Extract 2D-CNN'

 L. 489       404  LOAD_STR                 'Features are not 2D'
              406  CALL_METHOD_3         3  '3 positional arguments'
              408  POP_TOP          

 L. 490       410  LOAD_CONST               None
              412  RETURN_VALUE     
            414_0  COME_FROM           374  '374'

 L. 492       414  LOAD_GLOBAL              basic_data
              416  LOAD_METHOD              str2int
              418  LOAD_FAST                'self'
              420  LOAD_ATTR                ldtbatchsize
              422  LOAD_METHOD              text
              424  CALL_METHOD_0         0  '0 positional arguments'
              426  CALL_METHOD_1         1  '1 positional argument'
              428  STORE_FAST               '_batch'

 L. 493       430  LOAD_FAST                '_batch'
              432  LOAD_CONST               False
              434  COMPARE_OP               is
          436_438  POP_JUMP_IF_TRUE    450  'to 450'
              440  LOAD_FAST                '_batch'
              442  LOAD_CONST               1
              444  COMPARE_OP               <
          446_448  POP_JUMP_IF_FALSE   486  'to 486'
            450_0  COME_FROM           436  '436'

 L. 494       450  LOAD_GLOBAL              vis_msg
              452  LOAD_ATTR                print
              454  LOAD_STR                 'ERROR in ExtractMl2DCnn: Non-positive batch size'
              456  LOAD_STR                 'error'
              458  LOAD_CONST               ('type',)
              460  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              462  POP_TOP          

 L. 495       464  LOAD_GLOBAL              QtWidgets
              466  LOAD_ATTR                QMessageBox
              468  LOAD_METHOD              critical
              470  LOAD_FAST                'self'
              472  LOAD_ATTR                msgbox

 L. 496       474  LOAD_STR                 'Extract 2D-CNN'

 L. 497       476  LOAD_STR                 'Non-positive batch size'
              478  CALL_METHOD_3         3  '3 positional arguments'
              480  POP_TOP          

 L. 498       482  LOAD_CONST               None
              484  RETURN_VALUE     
            486_0  COME_FROM           446  '446'

 L. 500       486  LOAD_GLOBAL              len
              488  LOAD_FAST                'self'
              490  LOAD_ATTR                ldtsave
              492  LOAD_METHOD              text
              494  CALL_METHOD_0         0  '0 positional arguments'
              496  CALL_FUNCTION_1       1  '1 positional argument'
              498  LOAD_CONST               1
              500  COMPARE_OP               <
          502_504  POP_JUMP_IF_FALSE   542  'to 542'

 L. 501       506  LOAD_GLOBAL              vis_msg
              508  LOAD_ATTR                print
              510  LOAD_STR                 'ERROR in ExtractMl2DCnn: No prefix specified'
              512  LOAD_STR                 'error'
              514  LOAD_CONST               ('type',)
              516  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              518  POP_TOP          

 L. 502       520  LOAD_GLOBAL              QtWidgets
              522  LOAD_ATTR                QMessageBox
              524  LOAD_METHOD              critical
              526  LOAD_FAST                'self'
              528  LOAD_ATTR                msgbox

 L. 503       530  LOAD_STR                 'Extract 2D-CNN'

 L. 504       532  LOAD_STR                 'No prefix specified'
              534  CALL_METHOD_3         3  '3 positional arguments'
              536  POP_TOP          

 L. 505       538  LOAD_CONST               None
              540  RETURN_VALUE     
            542_0  COME_FROM           502  '502'

 L. 506       542  LOAD_FAST                'self'
              544  LOAD_ATTR                ldtsave
              546  LOAD_METHOD              text
              548  CALL_METHOD_0         0  '0 positional arguments'
              550  LOAD_STR                 '1'
              552  BINARY_ADD       
              554  LOAD_FAST                'self'
              556  LOAD_ATTR                seisdata
              558  LOAD_METHOD              keys
              560  CALL_METHOD_0         0  '0 positional arguments'
              562  COMPARE_OP               in
          564_566  POP_JUMP_IF_FALSE   660  'to 660'

 L. 507       568  LOAD_FAST                'self'
              570  LOAD_METHOD              checkSeisData
              572  LOAD_FAST                'self'
              574  LOAD_ATTR                ldtsave
              576  LOAD_METHOD              text
              578  CALL_METHOD_0         0  '0 positional arguments'
              580  LOAD_STR                 '1'
              582  BINARY_ADD       
              584  CALL_METHOD_1         1  '1 positional argument'
          586_588  POP_JUMP_IF_FALSE   660  'to 660'

 L. 508       590  LOAD_GLOBAL              QtWidgets
              592  LOAD_ATTR                QMessageBox
              594  LOAD_METHOD              question
              596  LOAD_FAST                'self'
              598  LOAD_ATTR                msgbox
              600  LOAD_STR                 'Extract 2D-CNN'

 L. 509       602  LOAD_STR                 'Prefix '
              604  LOAD_FAST                'self'
              606  LOAD_ATTR                ldtsave
              608  LOAD_METHOD              text
              610  CALL_METHOD_0         0  '0 positional arguments'
              612  BINARY_ADD       
              614  LOAD_STR                 ' already exists. Overwrite?'
              616  BINARY_ADD       

 L. 510       618  LOAD_GLOBAL              QtWidgets
              620  LOAD_ATTR                QMessageBox
              622  LOAD_ATTR                Yes
              624  LOAD_GLOBAL              QtWidgets
              626  LOAD_ATTR                QMessageBox
              628  LOAD_ATTR                No
              630  BINARY_OR        

 L. 511       632  LOAD_GLOBAL              QtWidgets
              634  LOAD_ATTR                QMessageBox
              636  LOAD_ATTR                No
              638  CALL_METHOD_5         5  '5 positional arguments'
              640  STORE_FAST               'reply'

 L. 513       642  LOAD_FAST                'reply'
              644  LOAD_GLOBAL              QtWidgets
              646  LOAD_ATTR                QMessageBox
              648  LOAD_ATTR                No
              650  COMPARE_OP               ==
          652_654  POP_JUMP_IF_FALSE   660  'to 660'

 L. 514       656  LOAD_CONST               None
              658  RETURN_VALUE     
            660_0  COME_FROM           652  '652'
            660_1  COME_FROM           586  '586'
            660_2  COME_FROM           564  '564'

 L. 516       660  LOAD_CONST               2
              662  LOAD_GLOBAL              int
              664  LOAD_FAST                '_image_height_old'
              666  LOAD_CONST               2
              668  BINARY_TRUE_DIVIDE
              670  CALL_FUNCTION_1       1  '1 positional argument'
              672  BINARY_MULTIPLY  
              674  LOAD_CONST               1
              676  BINARY_ADD       
              678  STORE_FAST               '_image_height_old'

 L. 517       680  LOAD_CONST               2
              682  LOAD_GLOBAL              int
              684  LOAD_FAST                '_image_width_old'
              686  LOAD_CONST               2
              688  BINARY_TRUE_DIVIDE
              690  CALL_FUNCTION_1       1  '1 positional argument'
              692  BINARY_MULTIPLY  
              694  LOAD_CONST               1
              696  BINARY_ADD       
              698  STORE_FAST               '_image_width_old'

 L. 519       700  LOAD_GLOBAL              np
              702  LOAD_METHOD              shape
              704  LOAD_FAST                'self'
              706  LOAD_ATTR                seisdata
              708  LOAD_FAST                '_featurelist'
              710  LOAD_CONST               0
              712  BINARY_SUBSCR    
              714  BINARY_SUBSCR    
              716  CALL_METHOD_1         1  '1 positional argument'
              718  LOAD_CONST               0
              720  BINARY_SUBSCR    
              722  STORE_FAST               '_nsample'

 L. 521       724  LOAD_GLOBAL              int
              726  LOAD_GLOBAL              np
              728  LOAD_METHOD              ceil
              730  LOAD_FAST                '_nsample'
              732  LOAD_FAST                '_batch'
              734  BINARY_TRUE_DIVIDE
              736  CALL_METHOD_1         1  '1 positional argument'
              738  CALL_FUNCTION_1       1  '1 positional argument'
              740  STORE_FAST               '_nloop'

 L. 524       742  LOAD_GLOBAL              QtWidgets
              744  LOAD_METHOD              QProgressDialog
              746  CALL_METHOD_0         0  '0 positional arguments'
              748  STORE_FAST               '_pgsdlg'

 L. 525       750  LOAD_GLOBAL              QtGui
              752  LOAD_METHOD              QIcon
              754  CALL_METHOD_0         0  '0 positional arguments'
              756  STORE_FAST               'icon'

 L. 526       758  LOAD_FAST                'icon'
              760  LOAD_METHOD              addPixmap
              762  LOAD_GLOBAL              QtGui
              764  LOAD_METHOD              QPixmap
              766  LOAD_GLOBAL              os
              768  LOAD_ATTR                path
              770  LOAD_METHOD              join
              772  LOAD_FAST                'self'
              774  LOAD_ATTR                iconpath
              776  LOAD_STR                 'icons/retrieve.png'
              778  CALL_METHOD_2         2  '2 positional arguments'
              780  CALL_METHOD_1         1  '1 positional argument'

 L. 527       782  LOAD_GLOBAL              QtGui
              784  LOAD_ATTR                QIcon
              786  LOAD_ATTR                Normal
              788  LOAD_GLOBAL              QtGui
              790  LOAD_ATTR                QIcon
              792  LOAD_ATTR                Off
              794  CALL_METHOD_3         3  '3 positional arguments'
              796  POP_TOP          

 L. 528       798  LOAD_FAST                '_pgsdlg'
              800  LOAD_METHOD              setWindowIcon
              802  LOAD_FAST                'icon'
              804  CALL_METHOD_1         1  '1 positional argument'
              806  POP_TOP          

 L. 529       808  LOAD_FAST                '_pgsdlg'
              810  LOAD_METHOD              setWindowTitle
              812  LOAD_STR                 'Extract 2D-CNN'
              814  CALL_METHOD_1         1  '1 positional argument'
              816  POP_TOP          

 L. 530       818  LOAD_FAST                '_pgsdlg'
              820  LOAD_METHOD              setCancelButton
              822  LOAD_CONST               None
              824  CALL_METHOD_1         1  '1 positional argument'
              826  POP_TOP          

 L. 531       828  LOAD_FAST                '_pgsdlg'
              830  LOAD_METHOD              setWindowFlags
              832  LOAD_GLOBAL              QtCore
              834  LOAD_ATTR                Qt
              836  LOAD_ATTR                WindowStaysOnTopHint
              838  CALL_METHOD_1         1  '1 positional argument'
              840  POP_TOP          

 L. 532       842  LOAD_FAST                '_pgsdlg'
              844  LOAD_METHOD              forceShow
              846  CALL_METHOD_0         0  '0 positional arguments'
              848  POP_TOP          

 L. 533       850  LOAD_FAST                '_pgsdlg'
              852  LOAD_METHOD              setFixedWidth
              854  LOAD_CONST               400
              856  CALL_METHOD_1         1  '1 positional argument'
              858  POP_TOP          

 L. 534       860  LOAD_FAST                '_pgsdlg'
              862  LOAD_METHOD              setMaximum
              864  LOAD_FAST                '_nloop'
              866  CALL_METHOD_1         1  '1 positional argument'
              868  POP_TOP          

 L. 537       870  LOAD_CONST               0
              872  STORE_FAST               '_wdinl'

 L. 538       874  LOAD_CONST               0
              876  STORE_FAST               '_wdxl'

 L. 539       878  LOAD_CONST               0
              880  STORE_FAST               '_wdz'

 L. 540       882  LOAD_FAST                'self'
              884  LOAD_ATTR                cbbornt
              886  LOAD_METHOD              currentIndex
              888  CALL_METHOD_0         0  '0 positional arguments'
              890  LOAD_CONST               0
              892  COMPARE_OP               ==
          894_896  POP_JUMP_IF_FALSE   922  'to 922'

 L. 541       898  LOAD_GLOBAL              int
              900  LOAD_FAST                '_image_width_old'
              902  LOAD_CONST               2
              904  BINARY_TRUE_DIVIDE
              906  CALL_FUNCTION_1       1  '1 positional argument'
              908  STORE_FAST               '_wdxl'

 L. 542       910  LOAD_GLOBAL              int
              912  LOAD_FAST                '_image_height_old'
              914  LOAD_CONST               2
              916  BINARY_TRUE_DIVIDE
              918  CALL_FUNCTION_1       1  '1 positional argument'
              920  STORE_FAST               '_wdz'
            922_0  COME_FROM           894  '894'

 L. 543       922  LOAD_FAST                'self'
              924  LOAD_ATTR                cbbornt
              926  LOAD_METHOD              currentIndex
              928  CALL_METHOD_0         0  '0 positional arguments'
              930  LOAD_CONST               1
              932  COMPARE_OP               ==
          934_936  POP_JUMP_IF_FALSE   962  'to 962'

 L. 544       938  LOAD_GLOBAL              int
              940  LOAD_FAST                '_image_width_old'
              942  LOAD_CONST               2
              944  BINARY_TRUE_DIVIDE
              946  CALL_FUNCTION_1       1  '1 positional argument'
              948  STORE_FAST               '_wdinl'

 L. 545       950  LOAD_GLOBAL              int
              952  LOAD_FAST                '_image_height_old'
              954  LOAD_CONST               2
              956  BINARY_TRUE_DIVIDE
              958  CALL_FUNCTION_1       1  '1 positional argument'
              960  STORE_FAST               '_wdz'
            962_0  COME_FROM           934  '934'

 L. 546       962  LOAD_FAST                'self'
              964  LOAD_ATTR                cbbornt
              966  LOAD_METHOD              currentIndex
              968  CALL_METHOD_0         0  '0 positional arguments'
              970  LOAD_CONST               2
              972  COMPARE_OP               ==
          974_976  POP_JUMP_IF_FALSE  1002  'to 1002'

 L. 547       978  LOAD_GLOBAL              int
              980  LOAD_FAST                '_image_width_old'
              982  LOAD_CONST               2
              984  BINARY_TRUE_DIVIDE
              986  CALL_FUNCTION_1       1  '1 positional argument'
              988  STORE_FAST               '_wdinl'

 L. 548       990  LOAD_GLOBAL              int
              992  LOAD_FAST                '_image_height_old'
              994  LOAD_CONST               2
              996  BINARY_TRUE_DIVIDE
              998  CALL_FUNCTION_1       1  '1 positional argument'
             1000  STORE_FAST               '_wdxl'
           1002_0  COME_FROM           974  '974'

 L. 550      1002  LOAD_GLOBAL              seis_ays
             1004  LOAD_METHOD              convertSeisInfoTo2DMat
             1006  LOAD_FAST                'self'
             1008  LOAD_ATTR                survinfo
             1010  CALL_METHOD_1         1  '1 positional argument'
             1012  STORE_FAST               '_seisdata'

 L. 552      1014  LOAD_GLOBAL              np
             1016  LOAD_METHOD              load
             1018  LOAD_GLOBAL              os
             1020  LOAD_ATTR                path
             1022  LOAD_METHOD              join
             1024  LOAD_FAST                'self'
             1026  LOAD_ATTR                modelpath
             1028  LOAD_FAST                'self'
             1030  LOAD_ATTR                modelname
             1032  LOAD_STR                 '_modelinfo.npy'
             1034  BINARY_ADD       
             1036  CALL_METHOD_2         2  '2 positional arguments'
             1038  CALL_METHOD_1         1  '1 positional argument'
             1040  LOAD_METHOD              item
             1042  CALL_METHOD_0         0  '0 positional arguments'
             1044  STORE_FAST               '_modelinfo'

 L. 553      1046  LOAD_FAST                '_modelinfo'
             1048  LOAD_STR                 'number_conv_block'
             1050  BINARY_SUBSCR    
             1052  STORE_FAST               '_nblock'

 L. 554      1054  LOAD_FAST                '_modelinfo'
             1056  LOAD_STR                 'number_conv_layer'
             1058  BINARY_SUBSCR    
             1060  STORE_FAST               '_nlayer'

 L. 555      1062  LOAD_FAST                '_modelinfo'
             1064  LOAD_STR                 'number_conv_feature'
             1066  BINARY_SUBSCR    
             1068  STORE_FAST               '_nfeature'

 L. 557      1070  LOAD_FAST                'self'
             1072  LOAD_ATTR                cbbtype
             1074  LOAD_METHOD              currentIndex
             1076  CALL_METHOD_0         0  '0 positional arguments'
             1078  STORE_FAST               '_featureidx'

 L. 558      1080  LOAD_CONST               0
             1082  STORE_FAST               '_blockidx'

 L. 559      1084  LOAD_CONST               0
             1086  STORE_FAST               '_layeridx'

 L. 560      1088  SETUP_LOOP         1164  'to 1164'
             1090  LOAD_GLOBAL              range
             1092  LOAD_FAST                '_nblock'
             1094  CALL_FUNCTION_1       1  '1 positional argument'
             1096  GET_ITER         
           1098_0  COME_FROM          1128  '1128'
             1098  FOR_ITER           1162  'to 1162'
             1100  STORE_FAST               'i'

 L. 561      1102  LOAD_GLOBAL              sum
             1104  LOAD_FAST                '_nlayer'
             1106  LOAD_CONST               0
             1108  LOAD_FAST                'i'
             1110  LOAD_CONST               1
             1112  BINARY_ADD       
             1114  BUILD_SLICE_2         2 
             1116  BINARY_SUBSCR    
             1118  CALL_FUNCTION_1       1  '1 positional argument'
             1120  LOAD_FAST                '_featureidx'
             1122  LOAD_CONST               1
             1124  BINARY_ADD       
             1126  COMPARE_OP               >=
         1128_1130  POP_JUMP_IF_FALSE  1098  'to 1098'

 L. 562      1132  LOAD_FAST                'i'
             1134  STORE_FAST               '_blockidx'

 L. 563      1136  LOAD_FAST                '_featureidx'
             1138  LOAD_GLOBAL              sum
             1140  LOAD_FAST                '_nlayer'
             1142  LOAD_CONST               0
             1144  LOAD_FAST                'i'
             1146  BUILD_SLICE_2         2 
             1148  BINARY_SUBSCR    
             1150  CALL_FUNCTION_1       1  '1 positional argument'
             1152  BINARY_SUBTRACT  
             1154  STORE_FAST               '_layeridx'

 L. 564      1156  BREAK_LOOP       
         1158_1160  JUMP_BACK          1098  'to 1098'
             1162  POP_BLOCK        
           1164_0  COME_FROM_LOOP     1088  '1088'

 L. 566      1164  LOAD_FAST                '_nfeature'
             1166  LOAD_FAST                '_blockidx'
             1168  BINARY_SUBSCR    
             1170  STORE_FAST               '_nfeature'

 L. 567      1172  LOAD_GLOBAL              np
             1174  LOAD_METHOD              zeros
             1176  LOAD_FAST                '_nsample'
             1178  LOAD_FAST                '_nfeature'
             1180  BUILD_LIST_2          2 
             1182  CALL_METHOD_1         1  '1 positional argument'
             1184  STORE_FAST               '_result'

 L. 568      1186  LOAD_CONST               0
             1188  STORE_FAST               'idxstart'

 L. 569  1190_1192  SETUP_LOOP         1520  'to 1520'
             1194  LOAD_GLOBAL              range
             1196  LOAD_FAST                '_nloop'
             1198  CALL_FUNCTION_1       1  '1 positional argument'
             1200  GET_ITER         
         1202_1204  FOR_ITER           1518  'to 1518'
             1206  STORE_FAST               'i'

 L. 571      1208  LOAD_GLOBAL              QtCore
             1210  LOAD_ATTR                QCoreApplication
             1212  LOAD_METHOD              instance
             1214  CALL_METHOD_0         0  '0 positional arguments'
             1216  LOAD_METHOD              processEvents
             1218  CALL_METHOD_0         0  '0 positional arguments'
             1220  POP_TOP          

 L. 573      1222  LOAD_GLOBAL              sys
             1224  LOAD_ATTR                stdout
             1226  LOAD_METHOD              write

 L. 574      1228  LOAD_STR                 '\r>>> Extract 2D-CNN, proceeding %.1f%% '
             1230  LOAD_GLOBAL              float
             1232  LOAD_FAST                'i'
             1234  CALL_FUNCTION_1       1  '1 positional argument'
             1236  LOAD_GLOBAL              float
             1238  LOAD_FAST                '_nloop'
             1240  CALL_FUNCTION_1       1  '1 positional argument'
             1242  BINARY_TRUE_DIVIDE
             1244  LOAD_CONST               100.0
             1246  BINARY_MULTIPLY  
             1248  BINARY_MODULO    
             1250  CALL_METHOD_1         1  '1 positional argument'
             1252  POP_TOP          

 L. 575      1254  LOAD_GLOBAL              sys
             1256  LOAD_ATTR                stdout
             1258  LOAD_METHOD              flush
             1260  CALL_METHOD_0         0  '0 positional arguments'
             1262  POP_TOP          

 L. 577      1264  LOAD_FAST                'idxstart'
             1266  LOAD_FAST                '_batch'
             1268  BINARY_ADD       
             1270  STORE_FAST               'idxend'

 L. 578      1272  LOAD_FAST                'idxend'
             1274  LOAD_FAST                '_nsample'
             1276  COMPARE_OP               >
         1278_1280  POP_JUMP_IF_FALSE  1286  'to 1286'

 L. 579      1282  LOAD_FAST                '_nsample'
             1284  STORE_FAST               'idxend'
           1286_0  COME_FROM          1278  '1278'

 L. 580      1286  LOAD_GLOBAL              np
             1288  LOAD_METHOD              linspace
             1290  LOAD_FAST                'idxstart'
             1292  LOAD_FAST                'idxend'
             1294  LOAD_CONST               1
             1296  BINARY_SUBTRACT  
             1298  LOAD_FAST                'idxend'
             1300  LOAD_FAST                'idxstart'
             1302  BINARY_SUBTRACT  
             1304  CALL_METHOD_3         3  '3 positional arguments'
             1306  LOAD_METHOD              astype
             1308  LOAD_GLOBAL              int
             1310  CALL_METHOD_1         1  '1 positional argument'
             1312  STORE_FAST               'idxlist'

 L. 581      1314  LOAD_FAST                'idxend'
             1316  STORE_FAST               'idxstart'

 L. 583      1318  LOAD_FAST                '_seisdata'
             1320  LOAD_FAST                'idxlist'
             1322  LOAD_CONST               0
             1324  LOAD_CONST               3
             1326  BUILD_SLICE_2         2 
             1328  BUILD_TUPLE_2         2 
             1330  BINARY_SUBSCR    
             1332  STORE_FAST               '_targetdata'

 L. 585      1334  BUILD_MAP_0           0 
             1336  STORE_FAST               '_dict'

 L. 586      1338  SETUP_LOOP         1458  'to 1458'
             1340  LOAD_FAST                '_featurelist'
             1342  GET_ITER         
           1344_0  COME_FROM          1420  '1420'
             1344  FOR_ITER           1456  'to 1456'
             1346  STORE_FAST               'f'

 L. 587      1348  LOAD_FAST                'self'
             1350  LOAD_ATTR                seisdata
             1352  LOAD_FAST                'f'
             1354  BINARY_SUBSCR    
             1356  STORE_FAST               '_data'

 L. 588      1358  LOAD_GLOBAL              seis_ays
             1360  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1362  LOAD_FAST                '_data'
             1364  LOAD_FAST                '_targetdata'
             1366  LOAD_FAST                'self'
             1368  LOAD_ATTR                survinfo

 L. 589      1370  LOAD_FAST                '_wdinl'
             1372  LOAD_FAST                '_wdxl'
             1374  LOAD_FAST                '_wdz'

 L. 590      1376  LOAD_CONST               False
             1378  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1380  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1382  LOAD_CONST               None
             1384  LOAD_CONST               None
             1386  BUILD_SLICE_2         2 
             1388  LOAD_CONST               3
             1390  LOAD_CONST               None
             1392  BUILD_SLICE_2         2 
             1394  BUILD_TUPLE_2         2 
             1396  BINARY_SUBSCR    
             1398  LOAD_FAST                '_dict'
             1400  LOAD_FAST                'f'
             1402  STORE_SUBSCR     

 L. 591      1404  LOAD_FAST                '_image_height_new'
             1406  LOAD_FAST                '_image_height_old'
             1408  COMPARE_OP               !=
         1410_1412  POP_JUMP_IF_TRUE   1424  'to 1424'
             1414  LOAD_FAST                '_image_width_new'
             1416  LOAD_FAST                '_image_width_old'
             1418  COMPARE_OP               !=
         1420_1422  POP_JUMP_IF_FALSE  1344  'to 1344'
           1424_0  COME_FROM          1410  '1410'

 L. 592      1424  LOAD_GLOBAL              basic_image
             1426  LOAD_ATTR                changeImageSize
             1428  LOAD_FAST                '_dict'
             1430  LOAD_FAST                'f'
             1432  BINARY_SUBSCR    

 L. 593      1434  LOAD_FAST                '_image_height_old'

 L. 594      1436  LOAD_FAST                '_image_width_old'

 L. 595      1438  LOAD_FAST                '_image_height_new'

 L. 596      1440  LOAD_FAST                '_image_width_new'
             1442  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1444  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1446  LOAD_FAST                '_dict'
             1448  LOAD_FAST                'f'
             1450  STORE_SUBSCR     
         1452_1454  JUMP_BACK          1344  'to 1344'
             1456  POP_BLOCK        
           1458_0  COME_FROM_LOOP     1338  '1338'

 L. 599      1458  LOAD_GLOBAL              ml_cnn
             1460  LOAD_ATTR                extractCNNConvFeature
             1462  LOAD_FAST                '_dict'

 L. 600      1464  LOAD_FAST                'self'
             1466  LOAD_ATTR                modelpath

 L. 601      1468  LOAD_FAST                'self'
             1470  LOAD_ATTR                modelname

 L. 602      1472  LOAD_FAST                '_blockidx'

 L. 603      1474  LOAD_FAST                '_layeridx'

 L. 604      1476  LOAD_FAST                '_batch'

 L. 605      1478  LOAD_STR                 'center'

 L. 606      1480  LOAD_CONST               True
             1482  LOAD_CONST               ('cnnpath', 'cnnname', 'blockidx', 'layeridx', 'batchsize', 'location', 'verbose')
             1484  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
             1486  LOAD_FAST                '_result'
             1488  LOAD_FAST                'idxlist'
             1490  LOAD_CONST               0
             1492  LOAD_FAST                '_nfeature'
             1494  BUILD_SLICE_2         2 
             1496  BUILD_TUPLE_2         2 
             1498  STORE_SUBSCR     

 L. 608      1500  LOAD_FAST                '_pgsdlg'
             1502  LOAD_METHOD              setValue
             1504  LOAD_FAST                'i'
             1506  LOAD_CONST               1
             1508  BINARY_ADD       
             1510  CALL_METHOD_1         1  '1 positional argument'
             1512  POP_TOP          
         1514_1516  JUMP_BACK          1202  'to 1202'
             1518  POP_BLOCK        
           1520_0  COME_FROM_LOOP     1190  '1190'

 L. 610      1520  LOAD_GLOBAL              print
             1522  LOAD_STR                 'Done'
             1524  CALL_FUNCTION_1       1  '1 positional argument'
             1526  POP_TOP          

 L. 611      1528  SETUP_LOOP         1642  'to 1642'
             1530  LOAD_GLOBAL              range
             1532  LOAD_FAST                '_nfeature'
             1534  CALL_FUNCTION_1       1  '1 positional argument'
             1536  GET_ITER         
             1538  FOR_ITER           1640  'to 1640'
             1540  STORE_FAST               'i'

 L. 612      1542  LOAD_GLOBAL              np
             1544  LOAD_METHOD              transpose
             1546  LOAD_GLOBAL              np
             1548  LOAD_METHOD              reshape
             1550  LOAD_FAST                '_result'
             1552  LOAD_CONST               None
             1554  LOAD_CONST               None
             1556  BUILD_SLICE_2         2 
             1558  LOAD_FAST                'i'
             1560  LOAD_FAST                'i'
             1562  LOAD_CONST               1
             1564  BINARY_ADD       
             1566  BUILD_SLICE_2         2 
             1568  BUILD_TUPLE_2         2 
             1570  BINARY_SUBSCR    

 L. 613      1572  LOAD_FAST                'self'
             1574  LOAD_ATTR                survinfo
             1576  LOAD_STR                 'ILNum'
             1578  BINARY_SUBSCR    

 L. 614      1580  LOAD_FAST                'self'
             1582  LOAD_ATTR                survinfo
             1584  LOAD_STR                 'XLNum'
             1586  BINARY_SUBSCR    

 L. 615      1588  LOAD_FAST                'self'
             1590  LOAD_ATTR                survinfo
             1592  LOAD_STR                 'ZNum'
             1594  BINARY_SUBSCR    
             1596  BUILD_LIST_3          3 
             1598  CALL_METHOD_2         2  '2 positional arguments'

 L. 616      1600  LOAD_CONST               2
             1602  LOAD_CONST               1
             1604  LOAD_CONST               0
             1606  BUILD_LIST_3          3 
             1608  CALL_METHOD_2         2  '2 positional arguments'
             1610  LOAD_FAST                'self'
             1612  LOAD_ATTR                seisdata
             1614  LOAD_FAST                'self'
             1616  LOAD_ATTR                ldtsave
             1618  LOAD_METHOD              text
             1620  CALL_METHOD_0         0  '0 positional arguments'
             1622  LOAD_GLOBAL              str
             1624  LOAD_FAST                'i'
             1626  LOAD_CONST               1
             1628  BINARY_ADD       
             1630  CALL_FUNCTION_1       1  '1 positional argument'
             1632  BINARY_ADD       
             1634  STORE_SUBSCR     
         1636_1638  JUMP_BACK          1538  'to 1538'
             1640  POP_BLOCK        
           1642_0  COME_FROM_LOOP     1528  '1528'

 L. 618      1642  LOAD_GLOBAL              QtWidgets
             1644  LOAD_ATTR                QMessageBox
             1646  LOAD_METHOD              information
             1648  LOAD_FAST                'self'
             1650  LOAD_ATTR                msgbox

 L. 619      1652  LOAD_STR                 'Extract 2D-CNN'

 L. 620      1654  LOAD_GLOBAL              str
             1656  LOAD_FAST                '_nfeature'
             1658  CALL_FUNCTION_1       1  '1 positional argument'
             1660  LOAD_STR                 ' CNN features extracted successfully'
             1662  BINARY_ADD       
             1664  CALL_METHOD_3         3  '3 positional arguments'
             1666  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 1664

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
    ExtractMl2DCnn = QtWidgets.QWidget()
    gui = extractml2dcnn()
    gui.setupGUI(ExtractMl2DCnn)
    ExtractMl2DCnn.show()
    sys.exit(app.exec_())