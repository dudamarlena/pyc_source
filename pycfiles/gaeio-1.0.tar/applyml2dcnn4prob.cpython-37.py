# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\applyml2dcnn4prob.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 33528 bytes
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

class applyml2dcnn4prob(object):
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

    def setupGUI(self, ApplyMl2DCnn4Prob):
        ApplyMl2DCnn4Prob.setObjectName('ApplyMl2DCnn4Prob')
        ApplyMl2DCnn4Prob.setFixedSize(800, 440)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ApplyMl2DCnn4Prob.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ApplyMl2DCnn4Prob)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ApplyMl2DCnn4Prob)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ApplyMl2DCnn4Prob)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lblornt = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(ApplyMl2DCnn4Prob)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 220, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 220, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(ApplyMl2DCnn4Prob)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 220, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 260, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(ApplyMl2DCnn4Prob)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 260, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 220, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 220, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(ApplyMl2DCnn4Prob)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 220, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 260, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(ApplyMl2DCnn4Prob)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 260, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ApplyMl2DCnn4Prob)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ApplyMl2DCnn4Prob)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ApplyMl2DCnn4Prob)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 130))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(ApplyMl2DCnn4Prob)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(ApplyMl2DCnn4Prob)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 140, 180, 130))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ApplyMl2DCnn4Prob)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ApplyMl2DCnn4Prob)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ApplyMl2DCnn4Prob)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ApplyMl2DCnn4Prob)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.lblpara = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ApplyMl2DCnn4Prob)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblsave = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ApplyMl2DCnn4Prob)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(150, 390, 100, 30))
        self.lbltarget = QtWidgets.QLabel(ApplyMl2DCnn4Prob)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(250, 350, 50, 30))
        self.lwgtarget = QtWidgets.QListWidget(ApplyMl2DCnn4Prob)
        self.lwgtarget.setObjectName('lwgtarget')
        self.lwgtarget.setGeometry(QtCore.QRect(300, 350, 90, 70))
        self.lwgtarget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.btnapply = QtWidgets.QPushButton(ApplyMl2DCnn4Prob)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 390, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ApplyMl2DCnn4Prob)
        self.msgbox.setObjectName('msgbox')
        _center_x = ApplyMl2DCnn4Prob.geometry().center().x()
        _center_y = ApplyMl2DCnn4Prob.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ApplyMl2DCnn4Prob)
        QtCore.QMetaObject.connectSlotsByName(ApplyMl2DCnn4Prob)

    def retranslateGUI(self, ApplyMl2DCnn4Prob):
        self.dialog = ApplyMl2DCnn4Prob
        _translate = QtCore.QCoreApplication.translate
        ApplyMl2DCnn4Prob.setWindowTitle(_translate('ApplyMl2DCnn4Prob', 'Apply 2D-CNN for probability'))
        self.lblfrom.setText(_translate('ApplyMl2DCnn4Prob', 'Select network:'))
        self.ldtfrom.setText(_translate('ApplyMl2DCnn4Prob', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ApplyMl2DCnn4Prob', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ApplyMl2DCnn4Prob', 'Training features:'))
        self.lblornt.setText(_translate('ApplyMl2DCnn4Prob', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.lbloldsize.setText(_translate('ApplyMl2DCnn4Prob', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('ApplyMl2DCnn4Prob', 'height='))
        self.ldtoldheight.setText(_translate('ApplyMl2DCnn4Prob', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('ApplyMl2DCnn4Prob', 'width='))
        self.ldtoldwidth.setText(_translate('ApplyMl2DCnn4Prob', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('ApplyMl2DCnn4Prob', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('ApplyMl2DCnn4Prob', 'height='))
        self.ldtnewheight.setText(_translate('ApplyMl2DCnn4Prob', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewheight.setEnabled(False)
        self.lblnewwidth.setText(_translate('ApplyMl2DCnn4Prob', 'width='))
        self.ldtnewwidth.setText(_translate('ApplyMl2DCnn4Prob', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewwidth.setEnabled(False)
        self.lblnetwork.setText(_translate('ApplyMl2DCnn4Prob', 'Pre-trained CNN architecture:'))
        self.btnviewnetwork.setText(_translate('ApplyMl2DCnn4Prob', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('ApplyMl2DCnn4Prob', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ApplyMl2DCnn4Prob', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblnfclayer.setText(_translate('ApplyMl2DCnn4Prob', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('ApplyMl2DCnn4Prob', ''))
        self.ldtnfclayer.setEnabled(False)
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblmasksize.setText(_translate('ApplyMl2DCnn4Prob', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ApplyMl2DCnn4Prob', 'height='))
        self.ldtmaskheight.setText(_translate('ApplyMl2DCnn4Prob', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ApplyMl2DCnn4Prob', 'width='))
        self.ldtmaskwidth.setText(_translate('ApplyMl2DCnn4Prob', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ApplyMl2DCnn4Prob', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ApplyMl2DCnn4Prob', 'height='))
        self.ldtpoolheight.setText(_translate('ApplyMl2DCnn4Prob', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ApplyMl2DCnn4Prob', 'width='))
        self.ldtpoolwidth.setText(_translate('ApplyMl2DCnn4Prob', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ApplyMl2DCnn4Prob', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ApplyMl2DCnn4Prob', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ApplyMl2DCnn4Prob', '5000'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('ApplyMl2DCnn4Prob', 'Output prefix='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ApplyMl2DCnn4Prob', 'cnn_prob_'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltarget.setText(_translate('ApplyMl2DCnn4Prob', 'Target ='))
        self.btnapply.setText(_translate('ApplyMl2DCnn4Prob', 'Apply 2D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnApplyMl2DCnn4Prob)

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
            self.lwgtarget.clear()
            self.lwgtarget.addItems([str(_t) for _t in range(self.modelinfo['number_label'])])
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
            self.lwgtarget.clear()

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

    def clickBtnApplyMl2DCnn4Prob--- This code section failed: ---

 L. 439         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 441         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 442        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in ApplyMl2DCnn4Prob: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 443        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 444        44  LOAD_STR                 'Apply 2D-CNN'

 L. 445        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 446        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 447        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 448        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in ApplyMl2DCnn4Prob: No CNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 449        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 450       100  LOAD_STR                 'Apply 2D-CNN'

 L. 451       102  LOAD_STR                 'No CNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 452       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 454       112  LOAD_FAST                'self'
              114  LOAD_ATTR                modelinfo
              116  LOAD_STR                 'feature_list'
              118  BINARY_SUBSCR    
              120  STORE_FAST               '_featurelist'

 L. 455       122  SETUP_LOOP          198  'to 198'
              124  LOAD_FAST                '_featurelist'
              126  GET_ITER         
            128_0  COME_FROM           144  '144'
              128  FOR_ITER            196  'to 196'
              130  STORE_FAST               'f'

 L. 456       132  LOAD_FAST                'self'
              134  LOAD_METHOD              checkSeisData
              136  LOAD_FAST                'f'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_CONST               False
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   128  'to 128'

 L. 457       146  LOAD_GLOBAL              vis_msg
              148  LOAD_ATTR                print
              150  LOAD_STR                 "ERROR in ApplyMl2DCnn4Prob: Feature '%s' not found in seismic data"
              152  LOAD_FAST                'f'
              154  BINARY_MODULO    

 L. 458       156  LOAD_STR                 'error'
              158  LOAD_CONST               ('type',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  POP_TOP          

 L. 459       164  LOAD_GLOBAL              QtWidgets
              166  LOAD_ATTR                QMessageBox
              168  LOAD_METHOD              critical
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                msgbox

 L. 460       174  LOAD_STR                 'Apply 2D-CNN'

 L. 461       176  LOAD_STR                 "Feature '"
              178  LOAD_FAST                'f'
              180  BINARY_ADD       
              182  LOAD_STR                 "' not found in seismic data"
              184  BINARY_ADD       
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 462       190  LOAD_CONST               None
              192  RETURN_VALUE     
              194  JUMP_BACK           128  'to 128'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      122  '122'

 L. 464       198  LOAD_GLOBAL              basic_data
              200  LOAD_METHOD              str2int
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                ldtoldheight
              206  LOAD_METHOD              text
              208  CALL_METHOD_0         0  '0 positional arguments'
              210  CALL_METHOD_1         1  '1 positional argument'
              212  STORE_FAST               '_image_height_old'

 L. 465       214  LOAD_GLOBAL              basic_data
              216  LOAD_METHOD              str2int
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                ldtoldwidth
              222  LOAD_METHOD              text
              224  CALL_METHOD_0         0  '0 positional arguments'
              226  CALL_METHOD_1         1  '1 positional argument'
              228  STORE_FAST               '_image_width_old'

 L. 466       230  LOAD_GLOBAL              basic_data
              232  LOAD_METHOD              str2int
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                ldtnewheight
              238  LOAD_METHOD              text
              240  CALL_METHOD_0         0  '0 positional arguments'
              242  CALL_METHOD_1         1  '1 positional argument'
              244  STORE_FAST               '_image_height_new'

 L. 467       246  LOAD_GLOBAL              basic_data
              248  LOAD_METHOD              str2int
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                ldtnewwidth
              254  LOAD_METHOD              text
              256  CALL_METHOD_0         0  '0 positional arguments'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  STORE_FAST               '_image_width_new'

 L. 468       262  LOAD_FAST                '_image_height_old'
              264  LOAD_CONST               False
              266  COMPARE_OP               is
          268_270  POP_JUMP_IF_TRUE    302  'to 302'
              272  LOAD_FAST                '_image_width_old'
              274  LOAD_CONST               False
              276  COMPARE_OP               is
          278_280  POP_JUMP_IF_TRUE    302  'to 302'

 L. 469       282  LOAD_FAST                '_image_height_new'
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

 L. 470       302  LOAD_GLOBAL              vis_msg
              304  LOAD_ATTR                print
              306  LOAD_STR                 'ERROR in ApplyMl2DCnn4Prob: Non-integer feature size'
              308  LOAD_STR                 'error'
              310  LOAD_CONST               ('type',)
              312  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              314  POP_TOP          

 L. 471       316  LOAD_GLOBAL              QtWidgets
              318  LOAD_ATTR                QMessageBox
              320  LOAD_METHOD              critical
              322  LOAD_FAST                'self'
              324  LOAD_ATTR                msgbox

 L. 472       326  LOAD_STR                 'Apply 2D-CNN'

 L. 473       328  LOAD_STR                 'Non-integer feature size'
              330  CALL_METHOD_3         3  '3 positional arguments'
              332  POP_TOP          

 L. 474       334  LOAD_CONST               None
              336  RETURN_VALUE     
            338_0  COME_FROM           298  '298'

 L. 475       338  LOAD_FAST                '_image_height_old'
              340  LOAD_CONST               2
              342  COMPARE_OP               <
          344_346  POP_JUMP_IF_TRUE    378  'to 378'
              348  LOAD_FAST                '_image_width_old'
              350  LOAD_CONST               2
              352  COMPARE_OP               <
          354_356  POP_JUMP_IF_TRUE    378  'to 378'

 L. 476       358  LOAD_FAST                '_image_height_new'
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

 L. 477       378  LOAD_GLOBAL              vis_msg
              380  LOAD_ATTR                print
              382  LOAD_STR                 'ERROR in ApplyMl2DCnn4Prob: Features are not 2D'
              384  LOAD_STR                 'error'
              386  LOAD_CONST               ('type',)
              388  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              390  POP_TOP          

 L. 478       392  LOAD_GLOBAL              QtWidgets
              394  LOAD_ATTR                QMessageBox
              396  LOAD_METHOD              critical
              398  LOAD_FAST                'self'
              400  LOAD_ATTR                msgbox

 L. 479       402  LOAD_STR                 'Apply 2D-CNN'

 L. 480       404  LOAD_STR                 'Features are not 2D'
              406  CALL_METHOD_3         3  '3 positional arguments'
              408  POP_TOP          

 L. 481       410  LOAD_CONST               None
              412  RETURN_VALUE     
            414_0  COME_FROM           374  '374'

 L. 483       414  LOAD_GLOBAL              basic_data
              416  LOAD_METHOD              str2int
              418  LOAD_FAST                'self'
              420  LOAD_ATTR                ldtbatchsize
              422  LOAD_METHOD              text
              424  CALL_METHOD_0         0  '0 positional arguments'
              426  CALL_METHOD_1         1  '1 positional argument'
              428  STORE_FAST               '_batch'

 L. 484       430  LOAD_FAST                '_batch'
              432  LOAD_CONST               False
              434  COMPARE_OP               is
          436_438  POP_JUMP_IF_TRUE    450  'to 450'
              440  LOAD_FAST                '_batch'
              442  LOAD_CONST               1
              444  COMPARE_OP               <
          446_448  POP_JUMP_IF_FALSE   486  'to 486'
            450_0  COME_FROM           436  '436'

 L. 485       450  LOAD_GLOBAL              vis_msg
              452  LOAD_ATTR                print
              454  LOAD_STR                 'ERROR in ApplyMl2DCnn4Prob: Non-positive batch size'
              456  LOAD_STR                 'error'
              458  LOAD_CONST               ('type',)
              460  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              462  POP_TOP          

 L. 486       464  LOAD_GLOBAL              QtWidgets
              466  LOAD_ATTR                QMessageBox
              468  LOAD_METHOD              critical
              470  LOAD_FAST                'self'
              472  LOAD_ATTR                msgbox

 L. 487       474  LOAD_STR                 'Apply 2D-CNN'

 L. 488       476  LOAD_STR                 'Non-positive batch size'
              478  CALL_METHOD_3         3  '3 positional arguments'
              480  POP_TOP          

 L. 489       482  LOAD_CONST               None
              484  RETURN_VALUE     
            486_0  COME_FROM           446  '446'

 L. 491       486  LOAD_GLOBAL              len
              488  LOAD_FAST                'self'
              490  LOAD_ATTR                ldtsave
              492  LOAD_METHOD              text
              494  CALL_METHOD_0         0  '0 positional arguments'
              496  CALL_FUNCTION_1       1  '1 positional argument'
              498  LOAD_CONST               1
              500  COMPARE_OP               <
          502_504  POP_JUMP_IF_FALSE   542  'to 542'

 L. 492       506  LOAD_GLOBAL              vis_msg
              508  LOAD_ATTR                print
              510  LOAD_STR                 'ERROR in ApplyMl2DCnn4Prob: No prefix specified'
              512  LOAD_STR                 'error'
              514  LOAD_CONST               ('type',)
              516  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              518  POP_TOP          

 L. 493       520  LOAD_GLOBAL              QtWidgets
              522  LOAD_ATTR                QMessageBox
              524  LOAD_METHOD              critical
              526  LOAD_FAST                'self'
              528  LOAD_ATTR                msgbox

 L. 494       530  LOAD_STR                 'Apply 2D-CNN'

 L. 495       532  LOAD_STR                 'No prefix specified'
              534  CALL_METHOD_3         3  '3 positional arguments'
              536  POP_TOP          

 L. 496       538  LOAD_CONST               None
              540  RETURN_VALUE     
            542_0  COME_FROM           502  '502'

 L. 498       542  LOAD_GLOBAL              len
              544  LOAD_FAST                'self'
              546  LOAD_ATTR                lwgtarget
              548  LOAD_METHOD              selectedItems
              550  CALL_METHOD_0         0  '0 positional arguments'
              552  CALL_FUNCTION_1       1  '1 positional argument'
              554  LOAD_CONST               1
              556  COMPARE_OP               <
          558_560  POP_JUMP_IF_FALSE   598  'to 598'

 L. 499       562  LOAD_GLOBAL              vis_msg
              564  LOAD_ATTR                print
              566  LOAD_STR                 'ERROR in ApplyMl2DCnn4Prob: No target label specified'
              568  LOAD_STR                 'error'
              570  LOAD_CONST               ('type',)
              572  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              574  POP_TOP          

 L. 500       576  LOAD_GLOBAL              QtWidgets
              578  LOAD_ATTR                QMessageBox
              580  LOAD_METHOD              critical
              582  LOAD_FAST                'self'
              584  LOAD_ATTR                msgbox

 L. 501       586  LOAD_STR                 'Apply 2D-CNN'

 L. 502       588  LOAD_STR                 'No target label specified'
              590  CALL_METHOD_3         3  '3 positional arguments'
              592  POP_TOP          

 L. 503       594  LOAD_CONST               None
              596  RETURN_VALUE     
            598_0  COME_FROM           558  '558'

 L. 504       598  LOAD_LISTCOMP            '<code_object <listcomp>>'
              600  LOAD_STR                 'applyml2dcnn4prob.clickBtnApplyMl2DCnn4Prob.<locals>.<listcomp>'
              602  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              604  LOAD_FAST                'self'
              606  LOAD_ATTR                lwgtarget
              608  LOAD_METHOD              selectedItems
              610  CALL_METHOD_0         0  '0 positional arguments'
              612  GET_ITER         
              614  CALL_FUNCTION_1       1  '1 positional argument'
              616  STORE_FAST               '_labellist'

 L. 505       618  SETUP_LOOP          772  'to 772'
              620  LOAD_FAST                '_labellist'
              622  GET_ITER         
            624_0  COME_FROM           760  '760'
            624_1  COME_FROM           680  '680'
            624_2  COME_FROM           654  '654'
              624  FOR_ITER            770  'to 770'
              626  STORE_FAST               '_label'

 L. 506       628  LOAD_FAST                'self'
              630  LOAD_ATTR                ldtsave
              632  LOAD_METHOD              text
              634  CALL_METHOD_0         0  '0 positional arguments'
              636  LOAD_GLOBAL              str
              638  LOAD_FAST                '_label'
              640  CALL_FUNCTION_1       1  '1 positional argument'
              642  BINARY_ADD       
              644  LOAD_FAST                'self'
              646  LOAD_ATTR                seisdata
              648  LOAD_METHOD              keys
              650  CALL_METHOD_0         0  '0 positional arguments'
              652  COMPARE_OP               in
          654_656  POP_JUMP_IF_FALSE   624  'to 624'

 L. 507       658  LOAD_FAST                'self'
              660  LOAD_METHOD              checkSeisData
              662  LOAD_FAST                'self'
              664  LOAD_ATTR                ldtsave
              666  LOAD_METHOD              text
              668  CALL_METHOD_0         0  '0 positional arguments'
              670  LOAD_GLOBAL              str
              672  LOAD_FAST                '_label'
              674  CALL_FUNCTION_1       1  '1 positional argument'
              676  BINARY_ADD       
              678  CALL_METHOD_1         1  '1 positional argument'
          680_682  POP_JUMP_IF_FALSE   624  'to 624'

 L. 508       684  LOAD_GLOBAL              QtWidgets
              686  LOAD_ATTR                QMessageBox
              688  LOAD_METHOD              question
              690  LOAD_FAST                'self'
              692  LOAD_ATTR                msgbox
              694  LOAD_STR                 'Apply 2D-CNN'

 L. 509       696  LOAD_FAST                'self'
              698  LOAD_ATTR                ldtsave
              700  LOAD_METHOD              text
              702  CALL_METHOD_0         0  '0 positional arguments'
              704  LOAD_STR                 ' already exists. Overwrite?'
              706  BINARY_ADD       

 L. 510       708  LOAD_GLOBAL              QtWidgets
              710  LOAD_ATTR                QMessageBox
              712  LOAD_ATTR                Yes
              714  LOAD_GLOBAL              QtWidgets
              716  LOAD_ATTR                QMessageBox
              718  LOAD_ATTR                No
              720  BINARY_OR        

 L. 511       722  LOAD_GLOBAL              QtWidgets
              724  LOAD_ATTR                QMessageBox
              726  LOAD_ATTR                No
              728  CALL_METHOD_5         5  '5 positional arguments'
              730  STORE_FAST               'reply'

 L. 512       732  LOAD_FAST                'reply'
              734  LOAD_GLOBAL              QtWidgets
              736  LOAD_ATTR                QMessageBox
              738  LOAD_ATTR                No
              740  COMPARE_OP               ==
          742_744  POP_JUMP_IF_FALSE   750  'to 750'

 L. 513       746  LOAD_CONST               None
              748  RETURN_VALUE     
            750_0  COME_FROM           742  '742'

 L. 514       750  LOAD_FAST                'reply'
              752  LOAD_GLOBAL              QtWidgets
              754  LOAD_ATTR                QMessageBox
              756  LOAD_ATTR                Yes
              758  COMPARE_OP               ==
          760_762  POP_JUMP_IF_FALSE   624  'to 624'

 L. 515       764  BREAK_LOOP       
          766_768  JUMP_BACK           624  'to 624'
              770  POP_BLOCK        
            772_0  COME_FROM_LOOP      618  '618'

 L. 517       772  LOAD_CONST               2
              774  LOAD_GLOBAL              int
              776  LOAD_FAST                '_image_height_old'
              778  LOAD_CONST               2
              780  BINARY_TRUE_DIVIDE
              782  CALL_FUNCTION_1       1  '1 positional argument'
              784  BINARY_MULTIPLY  
              786  LOAD_CONST               1
              788  BINARY_ADD       
              790  STORE_FAST               '_image_height_old'

 L. 518       792  LOAD_CONST               2
              794  LOAD_GLOBAL              int
              796  LOAD_FAST                '_image_width_old'
              798  LOAD_CONST               2
              800  BINARY_TRUE_DIVIDE
              802  CALL_FUNCTION_1       1  '1 positional argument'
              804  BINARY_MULTIPLY  
              806  LOAD_CONST               1
              808  BINARY_ADD       
              810  STORE_FAST               '_image_width_old'

 L. 520       812  LOAD_GLOBAL              np
              814  LOAD_METHOD              shape
              816  LOAD_FAST                'self'
              818  LOAD_ATTR                seisdata
              820  LOAD_FAST                '_featurelist'
              822  LOAD_CONST               0
              824  BINARY_SUBSCR    
              826  BINARY_SUBSCR    
              828  CALL_METHOD_1         1  '1 positional argument'
              830  LOAD_CONST               0
              832  BINARY_SUBSCR    
              834  STORE_FAST               '_nsample'

 L. 522       836  LOAD_GLOBAL              int
              838  LOAD_GLOBAL              np
              840  LOAD_METHOD              ceil
              842  LOAD_FAST                '_nsample'
              844  LOAD_FAST                '_batch'
              846  BINARY_TRUE_DIVIDE
              848  CALL_METHOD_1         1  '1 positional argument'
              850  CALL_FUNCTION_1       1  '1 positional argument'
              852  STORE_FAST               '_nloop'

 L. 525       854  LOAD_GLOBAL              QtWidgets
              856  LOAD_METHOD              QProgressDialog
              858  CALL_METHOD_0         0  '0 positional arguments'
              860  STORE_FAST               '_pgsdlg'

 L. 526       862  LOAD_GLOBAL              QtGui
              864  LOAD_METHOD              QIcon
              866  CALL_METHOD_0         0  '0 positional arguments'
              868  STORE_FAST               'icon'

 L. 527       870  LOAD_FAST                'icon'
              872  LOAD_METHOD              addPixmap
              874  LOAD_GLOBAL              QtGui
              876  LOAD_METHOD              QPixmap
              878  LOAD_GLOBAL              os
              880  LOAD_ATTR                path
              882  LOAD_METHOD              join
              884  LOAD_FAST                'self'
              886  LOAD_ATTR                iconpath
              888  LOAD_STR                 'icons/apply.png'
              890  CALL_METHOD_2         2  '2 positional arguments'
              892  CALL_METHOD_1         1  '1 positional argument'

 L. 528       894  LOAD_GLOBAL              QtGui
              896  LOAD_ATTR                QIcon
              898  LOAD_ATTR                Normal
              900  LOAD_GLOBAL              QtGui
              902  LOAD_ATTR                QIcon
              904  LOAD_ATTR                Off
              906  CALL_METHOD_3         3  '3 positional arguments'
              908  POP_TOP          

 L. 529       910  LOAD_FAST                '_pgsdlg'
              912  LOAD_METHOD              setWindowIcon
              914  LOAD_FAST                'icon'
              916  CALL_METHOD_1         1  '1 positional argument'
              918  POP_TOP          

 L. 530       920  LOAD_FAST                '_pgsdlg'
              922  LOAD_METHOD              setWindowTitle
              924  LOAD_STR                 'Apply 2D-CNN'
              926  CALL_METHOD_1         1  '1 positional argument'
              928  POP_TOP          

 L. 531       930  LOAD_FAST                '_pgsdlg'
              932  LOAD_METHOD              setCancelButton
              934  LOAD_CONST               None
              936  CALL_METHOD_1         1  '1 positional argument'
              938  POP_TOP          

 L. 532       940  LOAD_FAST                '_pgsdlg'
              942  LOAD_METHOD              setWindowFlags
              944  LOAD_GLOBAL              QtCore
              946  LOAD_ATTR                Qt
              948  LOAD_ATTR                WindowStaysOnTopHint
              950  CALL_METHOD_1         1  '1 positional argument'
              952  POP_TOP          

 L. 533       954  LOAD_FAST                '_pgsdlg'
              956  LOAD_METHOD              forceShow
              958  CALL_METHOD_0         0  '0 positional arguments'
              960  POP_TOP          

 L. 534       962  LOAD_FAST                '_pgsdlg'
              964  LOAD_METHOD              setFixedWidth
              966  LOAD_CONST               400
              968  CALL_METHOD_1         1  '1 positional argument'
              970  POP_TOP          

 L. 535       972  LOAD_FAST                '_pgsdlg'
              974  LOAD_METHOD              setMaximum
              976  LOAD_FAST                '_nloop'
              978  CALL_METHOD_1         1  '1 positional argument'
              980  POP_TOP          

 L. 537       982  LOAD_CONST               0
              984  STORE_FAST               '_wdinl'

 L. 538       986  LOAD_CONST               0
              988  STORE_FAST               '_wdxl'

 L. 539       990  LOAD_CONST               0
              992  STORE_FAST               '_wdz'

 L. 540       994  LOAD_FAST                'self'
              996  LOAD_ATTR                cbbornt
              998  LOAD_METHOD              currentIndex
             1000  CALL_METHOD_0         0  '0 positional arguments'
             1002  LOAD_CONST               0
             1004  COMPARE_OP               ==
         1006_1008  POP_JUMP_IF_FALSE  1034  'to 1034'

 L. 541      1010  LOAD_GLOBAL              int
             1012  LOAD_FAST                '_image_width_old'
             1014  LOAD_CONST               2
             1016  BINARY_TRUE_DIVIDE
             1018  CALL_FUNCTION_1       1  '1 positional argument'
             1020  STORE_FAST               '_wdxl'

 L. 542      1022  LOAD_GLOBAL              int
             1024  LOAD_FAST                '_image_height_old'
             1026  LOAD_CONST               2
             1028  BINARY_TRUE_DIVIDE
             1030  CALL_FUNCTION_1       1  '1 positional argument'
             1032  STORE_FAST               '_wdz'
           1034_0  COME_FROM          1006  '1006'

 L. 543      1034  LOAD_FAST                'self'
             1036  LOAD_ATTR                cbbornt
             1038  LOAD_METHOD              currentIndex
             1040  CALL_METHOD_0         0  '0 positional arguments'
             1042  LOAD_CONST               1
             1044  COMPARE_OP               ==
         1046_1048  POP_JUMP_IF_FALSE  1074  'to 1074'

 L. 544      1050  LOAD_GLOBAL              int
             1052  LOAD_FAST                '_image_width_old'
             1054  LOAD_CONST               2
             1056  BINARY_TRUE_DIVIDE
             1058  CALL_FUNCTION_1       1  '1 positional argument'
             1060  STORE_FAST               '_wdinl'

 L. 545      1062  LOAD_GLOBAL              int
             1064  LOAD_FAST                '_image_height_old'
             1066  LOAD_CONST               2
             1068  BINARY_TRUE_DIVIDE
             1070  CALL_FUNCTION_1       1  '1 positional argument'
             1072  STORE_FAST               '_wdz'
           1074_0  COME_FROM          1046  '1046'

 L. 546      1074  LOAD_FAST                'self'
             1076  LOAD_ATTR                cbbornt
             1078  LOAD_METHOD              currentIndex
             1080  CALL_METHOD_0         0  '0 positional arguments'
             1082  LOAD_CONST               2
             1084  COMPARE_OP               ==
         1086_1088  POP_JUMP_IF_FALSE  1114  'to 1114'

 L. 547      1090  LOAD_GLOBAL              int
             1092  LOAD_FAST                '_image_width_old'
             1094  LOAD_CONST               2
             1096  BINARY_TRUE_DIVIDE
             1098  CALL_FUNCTION_1       1  '1 positional argument'
             1100  STORE_FAST               '_wdinl'

 L. 548      1102  LOAD_GLOBAL              int
             1104  LOAD_FAST                '_image_height_old'
             1106  LOAD_CONST               2
             1108  BINARY_TRUE_DIVIDE
             1110  CALL_FUNCTION_1       1  '1 positional argument'
             1112  STORE_FAST               '_wdxl'
           1114_0  COME_FROM          1086  '1086'

 L. 550      1114  LOAD_GLOBAL              seis_ays
             1116  LOAD_METHOD              convertSeisInfoTo2DMat
             1118  LOAD_FAST                'self'
             1120  LOAD_ATTR                survinfo
             1122  CALL_METHOD_1         1  '1 positional argument'
             1124  STORE_FAST               '_seisdata'

 L. 552      1126  LOAD_GLOBAL              np
             1128  LOAD_METHOD              zeros
             1130  LOAD_FAST                '_nsample'
             1132  LOAD_GLOBAL              len
             1134  LOAD_FAST                '_labellist'
             1136  CALL_FUNCTION_1       1  '1 positional argument'
             1138  BUILD_LIST_2          2 
             1140  CALL_METHOD_1         1  '1 positional argument'
             1142  STORE_FAST               '_result'

 L. 553      1144  LOAD_CONST               0
             1146  STORE_FAST               'idxstart'

 L. 554  1148_1150  SETUP_LOOP         1474  'to 1474'
             1152  LOAD_GLOBAL              range
             1154  LOAD_FAST                '_nloop'
             1156  CALL_FUNCTION_1       1  '1 positional argument'
             1158  GET_ITER         
         1160_1162  FOR_ITER           1472  'to 1472'
             1164  STORE_FAST               'i'

 L. 556      1166  LOAD_GLOBAL              QtCore
             1168  LOAD_ATTR                QCoreApplication
             1170  LOAD_METHOD              instance
             1172  CALL_METHOD_0         0  '0 positional arguments'
             1174  LOAD_METHOD              processEvents
             1176  CALL_METHOD_0         0  '0 positional arguments'
             1178  POP_TOP          

 L. 558      1180  LOAD_GLOBAL              sys
             1182  LOAD_ATTR                stdout
             1184  LOAD_METHOD              write

 L. 559      1186  LOAD_STR                 '\r>>> Apply 2D-CNN, proceeding %.1f%% '
             1188  LOAD_GLOBAL              float
             1190  LOAD_FAST                'i'
             1192  CALL_FUNCTION_1       1  '1 positional argument'
             1194  LOAD_GLOBAL              float
             1196  LOAD_FAST                '_nloop'
             1198  CALL_FUNCTION_1       1  '1 positional argument'
             1200  BINARY_TRUE_DIVIDE
             1202  LOAD_CONST               100.0
             1204  BINARY_MULTIPLY  
             1206  BINARY_MODULO    
             1208  CALL_METHOD_1         1  '1 positional argument'
             1210  POP_TOP          

 L. 560      1212  LOAD_GLOBAL              sys
             1214  LOAD_ATTR                stdout
             1216  LOAD_METHOD              flush
             1218  CALL_METHOD_0         0  '0 positional arguments'
             1220  POP_TOP          

 L. 562      1222  LOAD_FAST                'idxstart'
             1224  LOAD_FAST                '_batch'
             1226  BINARY_ADD       
             1228  STORE_FAST               'idxend'

 L. 563      1230  LOAD_FAST                'idxend'
             1232  LOAD_FAST                '_nsample'
             1234  COMPARE_OP               >
         1236_1238  POP_JUMP_IF_FALSE  1244  'to 1244'

 L. 564      1240  LOAD_FAST                '_nsample'
             1242  STORE_FAST               'idxend'
           1244_0  COME_FROM          1236  '1236'

 L. 565      1244  LOAD_GLOBAL              np
             1246  LOAD_METHOD              linspace
             1248  LOAD_FAST                'idxstart'
             1250  LOAD_FAST                'idxend'
             1252  LOAD_CONST               1
             1254  BINARY_SUBTRACT  
             1256  LOAD_FAST                'idxend'
             1258  LOAD_FAST                'idxstart'
             1260  BINARY_SUBTRACT  
             1262  CALL_METHOD_3         3  '3 positional arguments'
             1264  LOAD_METHOD              astype
             1266  LOAD_GLOBAL              int
             1268  CALL_METHOD_1         1  '1 positional argument'
             1270  STORE_FAST               'idxlist'

 L. 566      1272  LOAD_FAST                'idxend'
             1274  STORE_FAST               'idxstart'

 L. 568      1276  LOAD_FAST                '_seisdata'
             1278  LOAD_FAST                'idxlist'
             1280  LOAD_CONST               0
             1282  LOAD_CONST               3
             1284  BUILD_SLICE_2         2 
             1286  BUILD_TUPLE_2         2 
             1288  BINARY_SUBSCR    
             1290  STORE_FAST               '_targetdata'

 L. 570      1292  BUILD_MAP_0           0 
             1294  STORE_FAST               '_dict'

 L. 571      1296  SETUP_LOOP         1416  'to 1416'
             1298  LOAD_FAST                '_featurelist'
             1300  GET_ITER         
           1302_0  COME_FROM          1378  '1378'
             1302  FOR_ITER           1414  'to 1414'
             1304  STORE_FAST               'f'

 L. 572      1306  LOAD_FAST                'self'
             1308  LOAD_ATTR                seisdata
             1310  LOAD_FAST                'f'
             1312  BINARY_SUBSCR    
             1314  STORE_FAST               '_data'

 L. 573      1316  LOAD_GLOBAL              seis_ays
             1318  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1320  LOAD_FAST                '_data'
             1322  LOAD_FAST                '_targetdata'
             1324  LOAD_FAST                'self'
             1326  LOAD_ATTR                survinfo

 L. 574      1328  LOAD_FAST                '_wdinl'
             1330  LOAD_FAST                '_wdxl'
             1332  LOAD_FAST                '_wdz'

 L. 575      1334  LOAD_CONST               False
             1336  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1338  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1340  LOAD_CONST               None
             1342  LOAD_CONST               None
             1344  BUILD_SLICE_2         2 
             1346  LOAD_CONST               3
             1348  LOAD_CONST               None
             1350  BUILD_SLICE_2         2 
             1352  BUILD_TUPLE_2         2 
             1354  BINARY_SUBSCR    
             1356  LOAD_FAST                '_dict'
             1358  LOAD_FAST                'f'
             1360  STORE_SUBSCR     

 L. 576      1362  LOAD_FAST                '_image_height_new'
             1364  LOAD_FAST                '_image_height_old'
             1366  COMPARE_OP               !=
         1368_1370  POP_JUMP_IF_TRUE   1382  'to 1382'
             1372  LOAD_FAST                '_image_width_new'
             1374  LOAD_FAST                '_image_width_old'
             1376  COMPARE_OP               !=
         1378_1380  POP_JUMP_IF_FALSE  1302  'to 1302'
           1382_0  COME_FROM          1368  '1368'

 L. 577      1382  LOAD_GLOBAL              basic_image
             1384  LOAD_ATTR                changeImageSize
             1386  LOAD_FAST                '_dict'
             1388  LOAD_FAST                'f'
             1390  BINARY_SUBSCR    

 L. 578      1392  LOAD_FAST                '_image_height_old'

 L. 579      1394  LOAD_FAST                '_image_width_old'

 L. 580      1396  LOAD_FAST                '_image_height_new'

 L. 581      1398  LOAD_FAST                '_image_width_new'
             1400  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1402  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1404  LOAD_FAST                '_dict'
             1406  LOAD_FAST                'f'
             1408  STORE_SUBSCR     
         1410_1412  JUMP_BACK          1302  'to 1302'
             1414  POP_BLOCK        
           1416_0  COME_FROM_LOOP     1296  '1296'

 L. 584      1416  LOAD_GLOBAL              ml_cnn
             1418  LOAD_ATTR                probabilityFromCNNClassifier
             1420  LOAD_FAST                '_dict'

 L. 585      1422  LOAD_FAST                'self'
             1424  LOAD_ATTR                modelpath

 L. 586      1426  LOAD_FAST                'self'
             1428  LOAD_ATTR                modelname

 L. 587      1430  LOAD_FAST                '_labellist'

 L. 588      1432  LOAD_FAST                '_batch'

 L. 589      1434  LOAD_CONST               True
             1436  LOAD_CONST               ('cnnpath', 'cnnname', 'targetlist', 'batchsize', 'verbose')
             1438  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1440  LOAD_FAST                '_result'
             1442  LOAD_FAST                'idxlist'
             1444  LOAD_CONST               None
             1446  LOAD_CONST               None
             1448  BUILD_SLICE_2         2 
             1450  BUILD_TUPLE_2         2 
             1452  STORE_SUBSCR     

 L. 592      1454  LOAD_FAST                '_pgsdlg'
             1456  LOAD_METHOD              setValue
             1458  LOAD_FAST                'i'
             1460  LOAD_CONST               1
             1462  BINARY_ADD       
             1464  CALL_METHOD_1         1  '1 positional argument'
             1466  POP_TOP          
         1468_1470  JUMP_BACK          1160  'to 1160'
             1472  POP_BLOCK        
           1474_0  COME_FROM_LOOP     1148  '1148'

 L. 594      1474  LOAD_GLOBAL              print
             1476  LOAD_STR                 'Done'
             1478  CALL_FUNCTION_1       1  '1 positional argument'
             1480  POP_TOP          

 L. 596      1482  SETUP_LOOP         1600  'to 1600'
             1484  LOAD_GLOBAL              range
             1486  LOAD_GLOBAL              len
             1488  LOAD_FAST                '_labellist'
             1490  CALL_FUNCTION_1       1  '1 positional argument'
             1492  CALL_FUNCTION_1       1  '1 positional argument'
             1494  GET_ITER         
             1496  FOR_ITER           1598  'to 1598'
             1498  STORE_FAST               'i'

 L. 597      1500  LOAD_GLOBAL              np
             1502  LOAD_METHOD              transpose
             1504  LOAD_GLOBAL              np
             1506  LOAD_METHOD              reshape
             1508  LOAD_FAST                '_result'
             1510  LOAD_CONST               None
             1512  LOAD_CONST               None
             1514  BUILD_SLICE_2         2 
             1516  LOAD_FAST                'i'
             1518  LOAD_FAST                'i'
             1520  LOAD_CONST               1
             1522  BINARY_ADD       
             1524  BUILD_SLICE_2         2 
             1526  BUILD_TUPLE_2         2 
             1528  BINARY_SUBSCR    

 L. 598      1530  LOAD_FAST                'self'
             1532  LOAD_ATTR                survinfo
             1534  LOAD_STR                 'ILNum'
             1536  BINARY_SUBSCR    

 L. 599      1538  LOAD_FAST                'self'
             1540  LOAD_ATTR                survinfo
             1542  LOAD_STR                 'XLNum'
             1544  BINARY_SUBSCR    

 L. 600      1546  LOAD_FAST                'self'
             1548  LOAD_ATTR                survinfo
             1550  LOAD_STR                 'ZNum'
             1552  BINARY_SUBSCR    
             1554  BUILD_LIST_3          3 
             1556  CALL_METHOD_2         2  '2 positional arguments'

 L. 601      1558  LOAD_CONST               2
             1560  LOAD_CONST               1
             1562  LOAD_CONST               0
             1564  BUILD_LIST_3          3 
             1566  CALL_METHOD_2         2  '2 positional arguments'
             1568  LOAD_FAST                'self'
             1570  LOAD_ATTR                seisdata
             1572  LOAD_FAST                'self'
             1574  LOAD_ATTR                ldtsave
             1576  LOAD_METHOD              text
             1578  CALL_METHOD_0         0  '0 positional arguments'
             1580  LOAD_GLOBAL              str
             1582  LOAD_FAST                '_labellist'
             1584  LOAD_FAST                'i'
             1586  BINARY_SUBSCR    
             1588  CALL_FUNCTION_1       1  '1 positional argument'
             1590  BINARY_ADD       
             1592  STORE_SUBSCR     
         1594_1596  JUMP_BACK          1496  'to 1496'
             1598  POP_BLOCK        
           1600_0  COME_FROM_LOOP     1482  '1482'

 L. 603      1600  LOAD_GLOBAL              QtWidgets
             1602  LOAD_ATTR                QMessageBox
             1604  LOAD_METHOD              information
             1606  LOAD_FAST                'self'
             1608  LOAD_ATTR                msgbox

 L. 604      1610  LOAD_STR                 'Apply 2D-CNN'

 L. 605      1612  LOAD_STR                 'CNN applied successfully'
             1614  CALL_METHOD_3         3  '3 positional arguments'
             1616  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 1614

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
    ApplyMl2DCnn4Prob = QtWidgets.QWidget()
    gui = applyml2dcnn4prob()
    gui.setupGUI(ApplyMl2DCnn4Prob)
    ApplyMl2DCnn4Prob.show()
    sys.exit(app.exec_())