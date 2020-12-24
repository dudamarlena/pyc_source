# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\extractml2dcnn.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 33776 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.seismic.analysis import analysis as seis_ays
from cognitivegeo.src.basic.data import data as basic_data
from cognitivegeo.src.basic.image import image as basic_image
from cognitivegeo.src.ml.tfmodel import tfmodel as ml_tfm
from cognitivegeo.src.ml.cnnclassifier import cnnclassifier as ml_cnn
from cognitivegeo.src.gui.viewml2dcnn import viewml2dcnn as gui_viewml2dcnn
from cognitivegeo.src.vis.messager import messager as vis_msg
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

    def clickBtnExtractMl2DCnn(self):
        self.refreshMsgBox()
        if self.checkSurvInfo() is False:
            vis_msg.print('ERROR in ExtractMl2DCnn: No seismic survey available', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Extract 2D-CNN', 'No seismic survey available')
            return
        if ml_tfm.checkCNNModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in ExtractMl2DCnn: No CNN network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Extract 2D-CNN', 'No CNN network found')
            return
        _featurelist = self.modelinfo['feature_list']
        for f in _featurelist:
            if self.checkSeisData(f) is False:
                vis_msg.print(("ERROR in ExtractMl2DCnn: Feature '%s' not found in seismic data" % f), type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Extract 2D-CNN', "Feature '" + f + "' not found in seismic data")
                return

        _image_height_old = basic_data.str2int(self.ldtoldheight.text())
        _image_width_old = basic_data.str2int(self.ldtoldwidth.text())
        _image_height_new = basic_data.str2int(self.ldtnewheight.text())
        _image_width_new = basic_data.str2int(self.ldtnewwidth.text())
        if _image_height_old is False or _image_width_old is False or _image_height_new is False or _image_width_new is False:
            vis_msg.print('ERROR in ExtractMl2DCnn: Non-integer feature size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Extract 2D-CNN', 'Non-integer feature size')
            return
        if _image_height_old < 2 or _image_width_old < 2 or _image_height_new < 2 or _image_width_new < 2:
            vis_msg.print('ERROR in ExtractMl2DCnn: Features are not 2D', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Extract 2D-CNN', 'Features are not 2D')
            return
        _batch = basic_data.str2int(self.ldtbatchsize.text())
        if _batch is False or _batch < 1:
            vis_msg.print('ERROR in ExtractMl2DCnn: Non-positive batch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Extract 2D-CNN', 'Non-positive batch size')
            return
        if len(self.ldtsave.text()) < 1:
            vis_msg.print('ERROR in ExtractMl2DCnn: No prefix specified', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Extract 2D-CNN', 'No prefix specified')
            return
        if self.ldtsave.text() + '1' in self.seisdata.keys():
            if self.checkSeisData(self.ldtsave.text() + '1'):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Extract 2D-CNN', 'Prefix ' + self.ldtsave.text() + ' already exists. Overwrite?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
        _image_height_old = 2 * int(_image_height_old / 2) + 1
        _image_width_old = 2 * int(_image_width_old / 2) + 1
        _nsample = np.shape(self.seisdata[_featurelist[0]])[0]
        _nloop = int(np.ceil(_nsample / _batch))
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/retrieve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Extract 2D-CNN')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _pgsdlg.setMaximum(_nloop)
        _wdinl = 0
        _wdxl = 0
        _wdz = 0
        if self.cbbornt.currentIndex() == 0:
            _wdxl = int(_image_width_old / 2)
            _wdz = int(_image_height_old / 2)
        if self.cbbornt.currentIndex() == 1:
            _wdinl = int(_image_width_old / 2)
            _wdz = int(_image_height_old / 2)
        if self.cbbornt.currentIndex() == 2:
            _wdinl = int(_image_width_old / 2)
            _wdxl = int(_image_height_old / 2)
        _seisdata = seis_ays.convertSeisInfoTo2DMat(self.survinfo)
        _modelinfo = np.load(os.path.join(self.modelpath, self.modelname + '_modelinfo.npy')).item()
        _nblock = _modelinfo['number_conv_block']
        _nlayer = _modelinfo['number_conv_layer']
        _nfeature = _modelinfo['number_conv_feature']
        _featureidx = self.cbbtype.currentIndex()
        _blockidx = 0
        _layeridx = 0
        for i in range(_nblock):
            if sum(_nlayer[0:i + 1]) >= _featureidx + 1:
                _blockidx = i
                _layeridx = _featureidx - sum(_nlayer[0:i])
                break

        _nfeature = _nfeature[_blockidx]
        _result = np.zeros([_nsample, _nfeature])
        idxstart = 0
        for i in range(_nloop):
            QtCore.QCoreApplication.instance().processEvents()
            sys.stdout.write('\r>>> Extract 2D-CNN, proceeding %.1f%% ' % (float(i) / float(_nloop) * 100.0))
            sys.stdout.flush()
            idxend = idxstart + _batch
            if idxend > _nsample:
                idxend = _nsample
            idxlist = np.linspace(idxstart, idxend - 1, idxend - idxstart).astype(int)
            idxstart = idxend
            _targetdata = _seisdata[idxlist, 0:3]
            _dict = {}
            for f in _featurelist:
                _data = self.seisdata[f]
                _dict[f] = seis_ays.retrieveSeisWindowFrom3DMat(_data, _targetdata, seisinfo=(self.survinfo), wdinl=_wdinl,
                  wdxl=_wdxl,
                  wdz=_wdz,
                  verbose=False)[:, 3:]
                if _image_height_new != _image_height_old or _image_width_new != _image_width_old:
                    _dict[f] = basic_image.changeImageSize((_dict[f]), image_height=_image_height_old,
                      image_width=_image_width_old,
                      image_height_new=_image_height_new,
                      image_width_new=_image_width_new)

            _result[idxlist, 0:_nfeature] = ml_cnn.extractCNNConvFeature(_dict, cnnpath=(self.modelpath),
              cnnname=(self.modelname),
              blockidx=_blockidx,
              layeridx=_layeridx,
              batchsize=_batch,
              location='center',
              verbose=True)
            _pgsdlg.setValue(i + 1)

        print('Done')
        for i in range(_nfeature):
            self.seisdata[self.ldtsave.text() + str(i + 1)] = np.transpose(np.reshape(_result[:, i:i + 1], [
             self.survinfo['ILNum'],
             self.survinfo['XLNum'],
             self.survinfo['ZNum']]), [
             2, 1, 0])

        QtWidgets.QMessageBox.information(self.msgbox, 'Extract 2D-CNN', str(_nfeature) + ' CNN features extracted successfully')

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
    ExtractMl2DCnn = QtWidgets.QWidget()
    gui = extractml2dcnn()
    gui.setupGUI(ExtractMl2DCnn)
    ExtractMl2DCnn.show()
    sys.exit(app.exec_())