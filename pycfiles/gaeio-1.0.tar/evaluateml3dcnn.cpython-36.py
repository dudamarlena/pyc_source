# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\evaluateml3dcnn.py
# Compiled at: 2019-12-15 21:49:29
# Size of source mod 2**32: 35417 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.seismic.analysis import analysis as seis_ays
from cognitivegeo.src.basic.data import data as basic_data
from cognitivegeo.src.basic.matdict import matdict as basic_mdt
from cognitivegeo.src.basic.video import video as basic_video
from cognitivegeo.src.vis.messager import messager as vis_msg
from cognitivegeo.src.ml.tfmodel import tfmodel as ml_tfm
from cognitivegeo.src.ml.cnnclassifier3d import cnnclassifier3d as ml_cnn3d
from cognitivegeo.src.gui.viewmlconfmat import viewmlconfmat as gui_viewmlconfmat
from cognitivegeo.src.gui.viewml3dcnn import viewml3dcnn as gui_viewml3dcnn
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class evaluateml3dcnn(object):
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

    def setupGUI(self, EvaluateMl3DCnn):
        EvaluateMl3DCnn.setObjectName('EvaluateMl3DCnn')
        EvaluateMl3DCnn.setFixedSize(800, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/check.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EvaluateMl3DCnn.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(EvaluateMl3DCnn)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(EvaluateMl3DCnn)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lbloldsize = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 180, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 180, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 180, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 220, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 220, 40, 30))
        self.lblolddepth = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblolddepth.setObjectName('lblolddepth')
        self.lblolddepth.setGeometry(QtCore.QRect(100, 260, 50, 30))
        self.ldtolddepth = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtolddepth.setObjectName('ldtolddepth')
        self.ldtolddepth.setGeometry(QtCore.QRect(150, 260, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 180, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 180, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 180, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 220, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 220, 40, 30))
        self.lblnewdepth = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblnewdepth.setObjectName('lblnewdepth')
        self.lblnewdepth.setGeometry(QtCore.QRect(300, 260, 50, 30))
        self.ldtnewdepth = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtnewdepth.setObjectName('ldtnewdepth')
        self.ldtnewdepth.setGeometry(QtCore.QRect(350, 260, 40, 30))
        self.lbltarget = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(EvaluateMl3DCnn)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 310, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(EvaluateMl3DCnn)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(EvaluateMl3DCnn)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 130))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(EvaluateMl3DCnn)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 140, 180, 130))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblmaskdepth = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblmaskdepth.setObjectName('lblmaskdepth')
        self.lblmaskdepth.setGeometry(QtCore.QRect(500, 360, 50, 30))
        self.ldtmaskdepth = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtmaskdepth.setObjectName('ldtmaskdepth')
        self.ldtmaskdepth.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.lblpooldepth = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblpooldepth.setObjectName('lblpooldepth')
        self.lblpooldepth.setGeometry(QtCore.QRect(700, 360, 50, 30))
        self.ldtpooldepth = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtpooldepth.setObjectName('ldtpooldepth')
        self.ldtpooldepth.setGeometry(QtCore.QRect(750, 360, 40, 30))
        self.lblpara = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 360, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(EvaluateMl3DCnn)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(EvaluateMl3DCnn)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.btnapply = QtWidgets.QPushButton(EvaluateMl3DCnn)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(320, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/check.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(EvaluateMl3DCnn)
        self.msgbox.setObjectName('msgbox')
        _center_x = EvaluateMl3DCnn.geometry().center().x()
        _center_y = EvaluateMl3DCnn.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(EvaluateMl3DCnn)
        QtCore.QMetaObject.connectSlotsByName(EvaluateMl3DCnn)

    def retranslateGUI(self, EvaluateMl3DCnn):
        self.dialog = EvaluateMl3DCnn
        _translate = QtCore.QCoreApplication.translate
        EvaluateMl3DCnn.setWindowTitle(_translate('EvaluateMl3DCnn', 'Evaluate 3D-CNN'))
        self.lblfrom.setText(_translate('EvaluateMl3DCnn', 'Select network:'))
        self.ldtfrom.setText(_translate('EvaluateMl3DCnn', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('EvaluateMl3DCnn', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('EvaluateMl3DCnn', 'Training features:'))
        self.lbloldsize.setText(_translate('EvaluateMl3DCnn', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('EvaluateMl3DCnn', 'height=\ntime/depth'))
        self.ldtoldheight.setText(_translate('EvaluateMl3DCnn', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('EvaluateMl3DCnn', 'width=\ncrossline'))
        self.ldtoldwidth.setText(_translate('EvaluateMl3DCnn', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblolddepth.setText(_translate('EvaluateMl3DCnn', 'depth=\ninline'))
        self.ldtolddepth.setText(_translate('EvaluateMl3DCnn', ''))
        self.ldtolddepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('EvaluateMl3DCnn', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('EvaluateMl3DCnn', 'height='))
        self.ldtnewheight.setText(_translate('EvaluateMl3DCnn', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewheight.setEnabled(False)
        self.lblnewwidth.setText(_translate('EvaluateMl3DCnn', 'width='))
        self.ldtnewwidth.setText(_translate('EvaluateMl3DCnn', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewwidth.setEnabled(False)
        self.lblnewdepth.setText(_translate('EvaluateMl3DCnn', 'depth='))
        self.ldtnewdepth.setText(_translate('EvaluateMl3DCnn', ''))
        self.ldtnewdepth.setEnabled(False)
        self.ldtnewdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltarget.setText(_translate('EvaluateMl3DCnn', 'Training target:'))
        self.lblnetwork.setText(_translate('EvaluateMl3DCnn', 'Pre-trained CNN architecture:'))
        self.btnviewnetwork.setText(_translate('EvaluateMl3DCnn', 'View'))
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
        self.lblmasksize.setText(_translate('EvaluateMl3DCnn', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('EvaluateMl3DCnn', 'height='))
        self.ldtmaskheight.setText(_translate('EvaluateMl3DCnn', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('EvaluateMl3DCnn', 'width='))
        self.ldtmaskwidth.setText(_translate('EvaluateMl3DCnn', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskdepth.setText(_translate('EvaluateMl3DCnn', 'depth='))
        self.ldtmaskdepth.setText(_translate('EvaluateMl3DCnn', ''))
        self.ldtmaskdepth.setEnabled(False)
        self.ldtmaskdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('EvaluateMl3DCnn', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('EvaluateMl3DCnn', 'height='))
        self.ldtpoolheight.setText(_translate('EvaluateMl3DCnn', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('EvaluateMl3DCnn', 'width='))
        self.ldtpoolwidth.setText(_translate('EvaluateMl3DCnn', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpooldepth.setText(_translate('EvaluateMl3DCnn', 'depth='))
        self.ldtpooldepth.setText(_translate('EvaluateMl3DCnn', ''))
        self.ldtpooldepth.setEnabled(False)
        self.ldtpooldepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('EvaluateMl3DCnn', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('EvaluateMl3DCnn', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('EvaluateMl3DCnn', '5000'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('EvaluateMl3DCnn', 'Evaluate 3D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnEvaluateMl3DCnn)

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.check3DCNNModel(self.modelpath, self.modelname) is True:
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
            _height = self.modelinfo['video_size'][0]
            _width = self.modelinfo['video_size'][1]
            _depth = self.modelinfo['video_size'][2]
            self.ldtnewheight.setText(str(_height))
            self.ldtnewwidth.setText(str(_width))
            self.ldtnewdepth.setText(str(_depth))
            self.ldtoldheight.setText(str(3))
            self.ldtoldwidth.setText(str(3))
            self.ldtolddepth.setText(str(3))
            self.cbbtarget.clear()
            self.cbbtarget.addItem(self.modelinfo['target'])
            self.btnviewnetwork.setEnabled(True)
            self.ldtnconvblock.setText(str(self.modelinfo['number_conv_block']))
            self.ldtnfclayer.setText(str(self.modelinfo['number_fc_layer']))
            self.ldtmaskheight.setText(str(self.modelinfo['patch_size'][0]))
            self.ldtmaskwidth.setText(str(self.modelinfo['patch_size'][1]))
            self.ldtmaskdepth.setText(str(self.modelinfo['patch_size'][2]))
            self.ldtpoolheight.setText(str(self.modelinfo['pool_size'][0]))
            self.ldtpoolwidth.setText(str(self.modelinfo['pool_size'][1]))
            self.ldtpooldepth.setText(str(self.modelinfo['pool_size'][2]))
        else:
            self.modelpath = ''
            self.modelname = ''
            self.modelinfo = None
            self.lwgfeature.clear()
            self.ldtoldheight.setText('')
            self.ldtnewheight.setText('')
            self.ldtoldwidth.setText('')
            self.ldtnewwidth.setText('')
            self.ldtolddepth.setText('')
            self.ldtnewdepth.setText('')
            self.cbbtarget.clear()
            self.btnviewnetwork.setEnabled(False)
            self.ldtnconvblock.setText('')
            self.ldtnfclayer.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtmaskdepth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')
            self.ldtpooldepth.setText('')

    def clickBtnFrom(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select CNN Network', (self.rootpath), filter='Tensorflow network files (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def clickBtnViewNetwork(self):
        _viewmlcnn = QtWidgets.QDialog()
        _gui = gui_viewml3dcnn()
        _gui.linestyle = self.linestyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewmlcnn)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewmlcnn.exec()
        _viewmlcnn.show()

    def changeLdtNconvblock(self):
        if ml_tfm.check3DCNNModel(self.modelpath, self.modelname) is True:
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
        if ml_tfm.check3DCNNModel(self.modelpath, self.modelname) is True:
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

    def clickBtnEvaluateMl3DCnn(self):
        self.refreshMsgBox()
        if self.checkSurvInfo() is False:
            vis_msg.print('ERROR in EvaluateMl3DCnn: No seismic survey available', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Evaluate 3D-CNN', 'No seismic survey available')
            return
        if ml_tfm.check3DCNNModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in EvaluateMl3DCnn: No CNN network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Evaluate 3D-CNN', 'No CNN network found')
            return
        _featurelist = self.modelinfo['feature_list']
        for f in _featurelist:
            if self.checkSeisData(f) is False:
                vis_msg.print(("ERROR in EvaluateMl3DCnn: Feature '%s' not found in seismic data" % f), type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Evaluate 3D-CNN', "Feature '" + f + "' not found in seismic data")
                return

        if self.modelinfo['target'] not in self.seisdata.keys():
            vis_msg.print(("ERROR in EvauluateMlCnn: Target label '%s' not found in seismic data" % self.modelinfo['target']),
              type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Evaluate 3D-CNN', "Target label '" + self.modelinfo['target'] + "' not found in seismic data")
            return
        _video_height_old = basic_data.str2int(self.ldtoldheight.text())
        _video_width_old = basic_data.str2int(self.ldtoldwidth.text())
        _video_depth_old = basic_data.str2int(self.ldtolddepth.text())
        _video_height_new = basic_data.str2int(self.ldtnewheight.text())
        _video_width_new = basic_data.str2int(self.ldtnewwidth.text())
        _video_depth_new = basic_data.str2int(self.ldtnewdepth.text())
        if _video_height_old is False or _video_width_old is False or _video_depth_old is False or _video_height_new is False or _video_width_new is False or _video_depth_new is False:
            vis_msg.print('ERROR in EvaluateMl3DCnn: Non-integer feature size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Evaluate 3D-CNN', 'Non-integer feature size')
            return
        if _video_height_old < 2 or _video_width_old < 2 or _video_depth_old < 2 or _video_height_new < 2 or _video_width_new < 2 or _video_depth_new < 2:
            vis_msg.print('ERROR in EvaluateMl2DCnn: Features are not 3D ', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Evaluate 2D-CNN', 'Features are not 3D ')
            return
        _batch = basic_data.str2int(self.ldtbatchsize.text())
        if _batch is False or _batch < 1:
            vis_msg.print('ERROR in EvaluateMl3DCnn: Non-positive batch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Evaluate 3D-CNN', 'Non-positive batch size')
            return
        _video_height_old = 2 * int(_video_height_old / 2) + 1
        _video_width_old = 2 * int(_video_width_old / 2) + 1
        _video_depth_old = 2 * int(_video_depth_old / 2) + 1
        _nlabel = self.modelinfo['number_label']
        _target = self.modelinfo['target']
        _wdinl = int(_video_depth_old / 2)
        _wdxl = int(_video_width_old / 2)
        _wdz = int(_video_height_old / 2)
        _seisinfo = self.survinfo
        _data = seis_ays.removeOutofSurveySample((seis_ays.convertSeisInfoTo2DMat(self.survinfo)), inlstart=(_seisinfo['ILStart'] + _wdinl * _seisinfo['ILStep']),
          inlend=(_seisinfo['ILEnd'] - _wdinl * _seisinfo['ILStep']),
          xlstart=(_seisinfo['XLStart'] + _wdxl * _seisinfo['XLStep']),
          xlend=(_seisinfo['XLEnd'] - _wdxl * _seisinfo['XLStep']),
          zstart=(_seisinfo['ZStart'] + _wdz * _seisinfo['ZStep']),
          zend=(_seisinfo['ZEnd'] - _wdz * _seisinfo['ZStep']))
        _seisdict = {}
        _seisdict['Inline'] = _data[:, 0:1]
        _seisdict['Crossline'] = _data[:, 1:2]
        _seisdict['Z'] = _data[:, 2:3]
        _nsample = basic_mdt.maxDictConstantRow(_seisdict)
        _nloop = int(np.ceil(_nsample / _batch))
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/check.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Evaluate 3D-CNN')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _pgsdlg.setMaximum(_nloop)
        _result = np.zeros([_nlabel + 1, _nlabel + 1])
        idxstart = 0
        for i in range(_nloop):
            sys.stdout.write('\r>>> Evaluate 3D-CNN, proceeding %.1f%% ' % (float(i + 1) / float(_nloop) * 100.0))
            sys.stdout.flush()
            QtCore.QCoreApplication.instance().processEvents()
            idxend = idxstart + _batch
            if idxend > _nsample:
                idxend = _nsample
            idxlist = np.linspace(idxstart, idxend - 1, idxend - idxstart).astype(int)
            idxstart = idxend
            _dict = basic_mdt.retrieveDictByIndex(_seisdict, idxlist)
            _targetdata = _dict['Inline']
            _targetdata = np.concatenate((_targetdata, _dict['Crossline']), axis=1)
            _targetdata = np.concatenate((_targetdata, _dict['Z']), axis=1)
            for f in _featurelist:
                _data = self.seisdata[f]
                _dict[f] = seis_ays.retrieveSeisWindowFrom3DMat(_data, _targetdata, seisinfo=(self.survinfo), wdinl=_wdinl,
                  wdxl=_wdxl,
                  wdz=_wdz,
                  verbose=False)[:, 3:]
                if _video_height_new != _video_height_old or _video_width_new != _video_width_old or _video_depth_new != _video_depth_old:
                    _dict[f] = basic_video.changeVideoSize((_dict[f]), video_height=_video_height_old,
                      video_width=_video_width_old,
                      video_depth=_video_depth_old,
                      video_height_new=_video_height_new,
                      video_width_new=_video_width_new,
                      video_depth_new=_video_depth_new)

            if _target not in _featurelist:
                _data = self.seisdata[_target]
                _dict[_target] = seis_ays.retrieveSeisSampleFrom3DMat(_data, _targetdata, seisinfo=(self.survinfo),
                  verbose=False)[:, 3:]
            _dict[_target] = np.round(_dict[_target]).astype(int)
            _confmatrix = ml_cnn3d.evaluate3DCNNClassifier(_dict, cnn3dpath=(self.modelpath),
              cnn3dname=(self.modelname),
              verbose=True)
            _result = _result + _confmatrix['confusion_matrix']
            _pgsdlg.setValue(i + 1)

        print('Done')
        _result[0, 1:] = _result[0, 1:] / _nloop
        _result[1:, 0] = _result[1:, 0] / _nloop
        print(_result)
        _viewmlconfmat = QtWidgets.QDialog()
        _gui = gui_viewmlconfmat()
        _gui.confmat = _result
        _gui.setupGUI(_viewmlconfmat)
        _viewmlconfmat.exec()
        _viewmlconfmat.show()

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
    EvaluateMl3DCnn = QtWidgets.QWidget()
    gui = evaluateml3dcnn()
    gui.setupGUI(EvaluateMl3DCnn)
    EvaluateMl3DCnn.show()
    sys.exit(app.exec_())