# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\applyml3dcnn4prob.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 36101 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.video as basic_video
import cognitivegeo.src.vis.messager as vis_msg
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.cnnclassifier3d as ml_cnn3d
import cognitivegeo.src.gui.viewml3dcnn as gui_viewml3dcnn
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class applyml3dcnn4prob(object):
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

    def setupGUI(self, ApplyMl3DCnn4Prob):
        ApplyMl3DCnn4Prob.setObjectName('ApplyMl3DCnn4Prob')
        ApplyMl3DCnn4Prob.setFixedSize(800, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ApplyMl3DCnn4Prob.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ApplyMl3DCnn4Prob)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ApplyMl3DCnn4Prob)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lbloldsize = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 180, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 180, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 180, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 220, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 220, 40, 30))
        self.lblolddepth = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblolddepth.setObjectName('lblolddepth')
        self.lblolddepth.setGeometry(QtCore.QRect(100, 260, 50, 30))
        self.ldtolddepth = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtolddepth.setObjectName('ldtolddepth')
        self.ldtolddepth.setGeometry(QtCore.QRect(150, 260, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 180, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 180, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 180, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 220, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 220, 40, 30))
        self.lblnewdepth = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblnewdepth.setObjectName('lblnewdepth')
        self.lblnewdepth.setGeometry(QtCore.QRect(300, 260, 50, 30))
        self.ldtnewdepth = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtnewdepth.setObjectName('ldtnewdepth')
        self.ldtnewdepth.setGeometry(QtCore.QRect(350, 260, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ApplyMl3DCnn4Prob)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ApplyMl3DCnn4Prob)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 130))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(ApplyMl3DCnn4Prob)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 140, 180, 130))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblmaskdepth = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblmaskdepth.setObjectName('lblmaskdepth')
        self.lblmaskdepth.setGeometry(QtCore.QRect(500, 360, 50, 30))
        self.ldtmaskdepth = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtmaskdepth.setObjectName('ldtmaskdepth')
        self.ldtmaskdepth.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.lblpooldepth = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblpooldepth.setObjectName('lblpooldepth')
        self.lblpooldepth.setGeometry(QtCore.QRect(700, 360, 50, 30))
        self.ldtpooldepth = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtpooldepth.setObjectName('ldtpooldepth')
        self.ldtpooldepth.setGeometry(QtCore.QRect(750, 360, 40, 30))
        self.lblpara = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblsave = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ApplyMl3DCnn4Prob)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.lbltarget = QtWidgets.QLabel(ApplyMl3DCnn4Prob)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(250, 350, 50, 30))
        self.lwgtarget = QtWidgets.QListWidget(ApplyMl3DCnn4Prob)
        self.lwgtarget.setObjectName('lwgtarget')
        self.lwgtarget.setGeometry(QtCore.QRect(300, 350, 90, 70))
        self.lwgtarget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.btnapply = QtWidgets.QPushButton(ApplyMl3DCnn4Prob)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(320, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ApplyMl3DCnn4Prob)
        self.msgbox.setObjectName('msgbox')
        _center_x = ApplyMl3DCnn4Prob.geometry().center().x()
        _center_y = ApplyMl3DCnn4Prob.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ApplyMl3DCnn4Prob)
        QtCore.QMetaObject.connectSlotsByName(ApplyMl3DCnn4Prob)

    def retranslateGUI(self, ApplyMl3DCnn4Prob):
        self.dialog = ApplyMl3DCnn4Prob
        _translate = QtCore.QCoreApplication.translate
        ApplyMl3DCnn4Prob.setWindowTitle(_translate('ApplyMl3DCnn4Prob', 'Apply 3D-CNN for probability'))
        self.lblfrom.setText(_translate('ApplyMl3DCnn4Prob', 'Select network:'))
        self.ldtfrom.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ApplyMl3DCnn4Prob', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ApplyMl3DCnn4Prob', 'Training features:'))
        self.lbloldsize.setText(_translate('ApplyMl3DCnn4Prob', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('ApplyMl3DCnn4Prob', 'height=\ntime/depth'))
        self.ldtoldheight.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('ApplyMl3DCnn4Prob', 'width=\ncrosslien'))
        self.ldtoldwidth.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblolddepth.setText(_translate('ApplyMl3DCnn4Prob', 'depth=\ninline'))
        self.ldtolddepth.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtolddepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('ApplyMl3DCnn4Prob', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('ApplyMl3DCnn4Prob', 'height='))
        self.ldtnewheight.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewheight.setEnabled(False)
        self.lblnewwidth.setText(_translate('ApplyMl3DCnn4Prob', 'width='))
        self.ldtnewwidth.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewwidth.setEnabled(False)
        self.lblnewdepth.setText(_translate('ApplyMl3DCnn4Prob', 'depth='))
        self.ldtnewdepth.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtnewdepth.setEnabled(False)
        self.ldtnewdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('ApplyMl3DCnn4Prob', 'Pre-trained CNN architecture:'))
        self.btnviewnetwork.setText(_translate('ApplyMl3DCnn4Prob', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('ApplyMl3DCnn4Prob', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblnfclayer.setText(_translate('ApplyMl3DCnn4Prob', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtnfclayer.setEnabled(False)
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblmasksize.setText(_translate('ApplyMl3DCnn4Prob', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ApplyMl3DCnn4Prob', 'height='))
        self.ldtmaskheight.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ApplyMl3DCnn4Prob', 'width='))
        self.ldtmaskwidth.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskdepth.setText(_translate('ApplyMl3DCnn4Prob', 'depth='))
        self.ldtmaskdepth.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtmaskdepth.setEnabled(False)
        self.ldtmaskdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ApplyMl3DCnn4Prob', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ApplyMl3DCnn4Prob', 'height='))
        self.ldtpoolheight.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ApplyMl3DCnn4Prob', 'width='))
        self.ldtpoolwidth.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpooldepth.setText(_translate('ApplyMl3DCnn4Prob', 'depth='))
        self.ldtpooldepth.setText(_translate('ApplyMl3DCnn4Prob', ''))
        self.ldtpooldepth.setEnabled(False)
        self.ldtpooldepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ApplyMl3DCnn4Prob', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ApplyMl3DCnn4Prob', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ApplyMl3DCnn4Prob', '5000'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('ApplyMl3DCnn4Prob', 'Output prefix='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ApplyMl3DCnn4Prob', 'cnn3d_prob_'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltarget.setText(_translate('ApplyMl3DCnn4Prob', 'Target ='))
        self.btnapply.setText(_translate('ApplyMl3DCnn4Prob', 'Apply 3D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnApplyMl3DCnn4Prob)

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
            self.btnviewnetwork.setEnabled(True)
            self.ldtnconvblock.setText(str(self.modelinfo['number_conv_block']))
            self.ldtnfclayer.setText(str(self.modelinfo['number_fc_layer']))
            self.ldtmaskheight.setText(str(self.modelinfo['patch_size'][0]))
            self.ldtmaskwidth.setText(str(self.modelinfo['patch_size'][1]))
            self.ldtmaskdepth.setText(str(self.modelinfo['patch_size'][2]))
            self.ldtpoolheight.setText(str(self.modelinfo['pool_size'][0]))
            self.ldtpoolwidth.setText(str(self.modelinfo['pool_size'][1]))
            self.ldtpooldepth.setText(str(self.modelinfo['pool_size'][2]))
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
            self.ldtolddepth.setText('')
            self.ldtnewdepth.setText('')
            self.btnviewnetwork.setEnabled(False)
            self.ldtnconvblock.setText('')
            self.ldtnfclayer.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtmaskdepth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')
            self.ldtpooldepth.setText('')
            self.lwgtarget.clear()

    def clickBtnFrom(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select CNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
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

    def clickBtnApplyMl3DCnn4Prob--- This code section failed: ---

 L. 476         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 478         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 479        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in ApplyMl3DCnn4Prob: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 480        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 481        44  LOAD_STR                 'Apply 3D-CNN'

 L. 482        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 483        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 484        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              check3DCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 485        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in ApplyMl3DCnn4Prob: No CNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 486        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 487       100  LOAD_STR                 'Apply 3D-CNN'

 L. 488       102  LOAD_STR                 'No CNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 489       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 490       112  LOAD_FAST                'self'
              114  LOAD_ATTR                modelinfo
              116  LOAD_STR                 'feature_list'
              118  BINARY_SUBSCR    
              120  STORE_FAST               '_featurelist'

 L. 491       122  SETUP_LOOP          198  'to 198'
              124  LOAD_FAST                '_featurelist'
              126  GET_ITER         
            128_0  COME_FROM           144  '144'
              128  FOR_ITER            196  'to 196'
              130  STORE_FAST               'f'

 L. 492       132  LOAD_FAST                'self'
              134  LOAD_METHOD              checkSeisData
              136  LOAD_FAST                'f'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_CONST               False
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   128  'to 128'

 L. 493       146  LOAD_GLOBAL              vis_msg
              148  LOAD_ATTR                print
              150  LOAD_STR                 "ERROR in ApplyMl3DCnn4Prob: Feature '%s' not found in seismic data"
              152  LOAD_FAST                'f'
              154  BINARY_MODULO    

 L. 494       156  LOAD_STR                 'error'
              158  LOAD_CONST               ('type',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  POP_TOP          

 L. 495       164  LOAD_GLOBAL              QtWidgets
              166  LOAD_ATTR                QMessageBox
              168  LOAD_METHOD              critical
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                msgbox

 L. 496       174  LOAD_STR                 'Apply 3D-CNN'

 L. 497       176  LOAD_STR                 "Feature '"
              178  LOAD_FAST                'f'
              180  BINARY_ADD       
              182  LOAD_STR                 "' not found in seismic data"
              184  BINARY_ADD       
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 498       190  LOAD_CONST               None
              192  RETURN_VALUE     
              194  JUMP_BACK           128  'to 128'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      122  '122'

 L. 500       198  LOAD_GLOBAL              basic_data
              200  LOAD_METHOD              str2int
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                ldtoldheight
              206  LOAD_METHOD              text
              208  CALL_METHOD_0         0  '0 positional arguments'
              210  CALL_METHOD_1         1  '1 positional argument'
              212  STORE_FAST               '_video_height_old'

 L. 501       214  LOAD_GLOBAL              basic_data
              216  LOAD_METHOD              str2int
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                ldtoldwidth
              222  LOAD_METHOD              text
              224  CALL_METHOD_0         0  '0 positional arguments'
              226  CALL_METHOD_1         1  '1 positional argument'
              228  STORE_FAST               '_video_width_old'

 L. 502       230  LOAD_GLOBAL              basic_data
              232  LOAD_METHOD              str2int
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                ldtolddepth
              238  LOAD_METHOD              text
              240  CALL_METHOD_0         0  '0 positional arguments'
              242  CALL_METHOD_1         1  '1 positional argument'
              244  STORE_FAST               '_video_depth_old'

 L. 503       246  LOAD_GLOBAL              basic_data
              248  LOAD_METHOD              str2int
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                ldtnewheight
              254  LOAD_METHOD              text
              256  CALL_METHOD_0         0  '0 positional arguments'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  STORE_FAST               '_video_height_new'

 L. 504       262  LOAD_GLOBAL              basic_data
              264  LOAD_METHOD              str2int
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                ldtnewwidth
              270  LOAD_METHOD              text
              272  CALL_METHOD_0         0  '0 positional arguments'
              274  CALL_METHOD_1         1  '1 positional argument'
              276  STORE_FAST               '_video_width_new'

 L. 505       278  LOAD_GLOBAL              basic_data
              280  LOAD_METHOD              str2int
              282  LOAD_FAST                'self'
              284  LOAD_ATTR                ldtnewdepth
              286  LOAD_METHOD              text
              288  CALL_METHOD_0         0  '0 positional arguments'
              290  CALL_METHOD_1         1  '1 positional argument'
              292  STORE_FAST               '_video_depth_new'

 L. 506       294  LOAD_FAST                '_video_height_old'
              296  LOAD_CONST               False
              298  COMPARE_OP               is
          300_302  POP_JUMP_IF_TRUE    354  'to 354'
              304  LOAD_FAST                '_video_width_old'
              306  LOAD_CONST               False
              308  COMPARE_OP               is
          310_312  POP_JUMP_IF_TRUE    354  'to 354'
              314  LOAD_FAST                '_video_depth_old'
              316  LOAD_CONST               False
              318  COMPARE_OP               is
          320_322  POP_JUMP_IF_TRUE    354  'to 354'

 L. 507       324  LOAD_FAST                '_video_height_new'
              326  LOAD_CONST               False
              328  COMPARE_OP               is
          330_332  POP_JUMP_IF_TRUE    354  'to 354'
              334  LOAD_FAST                '_video_width_new'
              336  LOAD_CONST               False
              338  COMPARE_OP               is
          340_342  POP_JUMP_IF_TRUE    354  'to 354'
              344  LOAD_FAST                '_video_depth_new'
              346  LOAD_CONST               False
              348  COMPARE_OP               is
          350_352  POP_JUMP_IF_FALSE   390  'to 390'
            354_0  COME_FROM           340  '340'
            354_1  COME_FROM           330  '330'
            354_2  COME_FROM           320  '320'
            354_3  COME_FROM           310  '310'
            354_4  COME_FROM           300  '300'

 L. 508       354  LOAD_GLOBAL              vis_msg
              356  LOAD_ATTR                print
              358  LOAD_STR                 'ERROR in ApplyMl3DCnn4Prob: Non-integer feature size'
              360  LOAD_STR                 'error'
              362  LOAD_CONST               ('type',)
              364  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              366  POP_TOP          

 L. 509       368  LOAD_GLOBAL              QtWidgets
              370  LOAD_ATTR                QMessageBox
              372  LOAD_METHOD              critical
              374  LOAD_FAST                'self'
              376  LOAD_ATTR                msgbox

 L. 510       378  LOAD_STR                 'Apply 3D-CNN'

 L. 511       380  LOAD_STR                 'Non-integer feature size'
              382  CALL_METHOD_3         3  '3 positional arguments'
              384  POP_TOP          

 L. 512       386  LOAD_CONST               None
              388  RETURN_VALUE     
            390_0  COME_FROM           350  '350'

 L. 513       390  LOAD_FAST                '_video_height_old'
              392  LOAD_CONST               2
              394  COMPARE_OP               <
          396_398  POP_JUMP_IF_TRUE    450  'to 450'
              400  LOAD_FAST                '_video_width_old'
              402  LOAD_CONST               2
              404  COMPARE_OP               <
          406_408  POP_JUMP_IF_TRUE    450  'to 450'
              410  LOAD_FAST                '_video_depth_old'
              412  LOAD_CONST               2
              414  COMPARE_OP               <
          416_418  POP_JUMP_IF_TRUE    450  'to 450'

 L. 514       420  LOAD_FAST                '_video_height_new'
              422  LOAD_CONST               2
              424  COMPARE_OP               <
          426_428  POP_JUMP_IF_TRUE    450  'to 450'
              430  LOAD_FAST                '_video_width_new'
              432  LOAD_CONST               2
              434  COMPARE_OP               <
          436_438  POP_JUMP_IF_TRUE    450  'to 450'
              440  LOAD_FAST                '_video_depth_new'
              442  LOAD_CONST               2
              444  COMPARE_OP               <
          446_448  POP_JUMP_IF_FALSE   486  'to 486'
            450_0  COME_FROM           436  '436'
            450_1  COME_FROM           426  '426'
            450_2  COME_FROM           416  '416'
            450_3  COME_FROM           406  '406'
            450_4  COME_FROM           396  '396'

 L. 515       450  LOAD_GLOBAL              vis_msg
              452  LOAD_ATTR                print
              454  LOAD_STR                 'ERROR in ApplyMl2DCnn: Features are not 3D '
              456  LOAD_STR                 'error'
              458  LOAD_CONST               ('type',)
              460  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              462  POP_TOP          

 L. 516       464  LOAD_GLOBAL              QtWidgets
              466  LOAD_ATTR                QMessageBox
              468  LOAD_METHOD              critical
              470  LOAD_FAST                'self'
              472  LOAD_ATTR                msgbox

 L. 517       474  LOAD_STR                 'Apply 2D-CNN'

 L. 518       476  LOAD_STR                 'Features are not 3D '
              478  CALL_METHOD_3         3  '3 positional arguments'
              480  POP_TOP          

 L. 519       482  LOAD_CONST               None
              484  RETURN_VALUE     
            486_0  COME_FROM           446  '446'

 L. 521       486  LOAD_GLOBAL              basic_data
              488  LOAD_METHOD              str2int
              490  LOAD_FAST                'self'
              492  LOAD_ATTR                ldtbatchsize
              494  LOAD_METHOD              text
              496  CALL_METHOD_0         0  '0 positional arguments'
              498  CALL_METHOD_1         1  '1 positional argument'
              500  STORE_FAST               '_batch'

 L. 522       502  LOAD_FAST                '_batch'
              504  LOAD_CONST               False
              506  COMPARE_OP               is
          508_510  POP_JUMP_IF_TRUE    522  'to 522'
              512  LOAD_FAST                '_batch'
              514  LOAD_CONST               1
              516  COMPARE_OP               <
          518_520  POP_JUMP_IF_FALSE   558  'to 558'
            522_0  COME_FROM           508  '508'

 L. 523       522  LOAD_GLOBAL              vis_msg
              524  LOAD_ATTR                print
              526  LOAD_STR                 'ERROR in ApplyMl3DCnn4Prob: Non-positive batch size'
              528  LOAD_STR                 'error'
              530  LOAD_CONST               ('type',)
              532  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              534  POP_TOP          

 L. 524       536  LOAD_GLOBAL              QtWidgets
              538  LOAD_ATTR                QMessageBox
              540  LOAD_METHOD              critical
              542  LOAD_FAST                'self'
              544  LOAD_ATTR                msgbox

 L. 525       546  LOAD_STR                 'Apply 3D-CNN'

 L. 526       548  LOAD_STR                 'Non-positive batch size'
              550  CALL_METHOD_3         3  '3 positional arguments'
              552  POP_TOP          

 L. 527       554  LOAD_CONST               None
              556  RETURN_VALUE     
            558_0  COME_FROM           518  '518'

 L. 529       558  LOAD_GLOBAL              len
              560  LOAD_FAST                'self'
              562  LOAD_ATTR                ldtsave
              564  LOAD_METHOD              text
              566  CALL_METHOD_0         0  '0 positional arguments'
              568  CALL_FUNCTION_1       1  '1 positional argument'
              570  LOAD_CONST               1
              572  COMPARE_OP               <
          574_576  POP_JUMP_IF_FALSE   614  'to 614'

 L. 530       578  LOAD_GLOBAL              vis_msg
              580  LOAD_ATTR                print
              582  LOAD_STR                 'ERROR in ApplyMl3DCnn4Prob: No prefix specified'
              584  LOAD_STR                 'error'
              586  LOAD_CONST               ('type',)
              588  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              590  POP_TOP          

 L. 531       592  LOAD_GLOBAL              QtWidgets
              594  LOAD_ATTR                QMessageBox
              596  LOAD_METHOD              critical
              598  LOAD_FAST                'self'
              600  LOAD_ATTR                msgbox

 L. 532       602  LOAD_STR                 'Apply 3D-CNN'

 L. 533       604  LOAD_STR                 'No prefix specified'
              606  CALL_METHOD_3         3  '3 positional arguments'
              608  POP_TOP          

 L. 534       610  LOAD_CONST               None
              612  RETURN_VALUE     
            614_0  COME_FROM           574  '574'

 L. 536       614  LOAD_GLOBAL              len
              616  LOAD_FAST                'self'
              618  LOAD_ATTR                lwgtarget
              620  LOAD_METHOD              selectedItems
              622  CALL_METHOD_0         0  '0 positional arguments'
              624  CALL_FUNCTION_1       1  '1 positional argument'
              626  LOAD_CONST               1
              628  COMPARE_OP               <
          630_632  POP_JUMP_IF_FALSE   670  'to 670'

 L. 537       634  LOAD_GLOBAL              vis_msg
              636  LOAD_ATTR                print
              638  LOAD_STR                 'ERROR in ApplyMl3DCnn4Prob: No target label specified'
              640  LOAD_STR                 'error'
              642  LOAD_CONST               ('type',)
              644  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              646  POP_TOP          

 L. 538       648  LOAD_GLOBAL              QtWidgets
              650  LOAD_ATTR                QMessageBox
              652  LOAD_METHOD              critical
              654  LOAD_FAST                'self'
              656  LOAD_ATTR                msgbox

 L. 539       658  LOAD_STR                 'Apply 3D-CNN'

 L. 540       660  LOAD_STR                 'No target label specified'
              662  CALL_METHOD_3         3  '3 positional arguments'
              664  POP_TOP          

 L. 541       666  LOAD_CONST               None
              668  RETURN_VALUE     
            670_0  COME_FROM           630  '630'

 L. 542       670  LOAD_LISTCOMP            '<code_object <listcomp>>'
              672  LOAD_STR                 'applyml3dcnn4prob.clickBtnApplyMl3DCnn4Prob.<locals>.<listcomp>'
              674  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              676  LOAD_FAST                'self'
              678  LOAD_ATTR                lwgtarget
              680  LOAD_METHOD              selectedItems
              682  CALL_METHOD_0         0  '0 positional arguments'
              684  GET_ITER         
              686  CALL_FUNCTION_1       1  '1 positional argument'
              688  STORE_FAST               '_labellist'

 L. 543       690  SETUP_LOOP          844  'to 844'
              692  LOAD_FAST                '_labellist'
              694  GET_ITER         
            696_0  COME_FROM           832  '832'
            696_1  COME_FROM           752  '752'
            696_2  COME_FROM           726  '726'
              696  FOR_ITER            842  'to 842'
              698  STORE_FAST               '_label'

 L. 544       700  LOAD_FAST                'self'
              702  LOAD_ATTR                ldtsave
              704  LOAD_METHOD              text
              706  CALL_METHOD_0         0  '0 positional arguments'
              708  LOAD_GLOBAL              str
              710  LOAD_FAST                '_label'
              712  CALL_FUNCTION_1       1  '1 positional argument'
              714  BINARY_ADD       
              716  LOAD_FAST                'self'
              718  LOAD_ATTR                seisdata
              720  LOAD_METHOD              keys
              722  CALL_METHOD_0         0  '0 positional arguments'
              724  COMPARE_OP               in
          726_728  POP_JUMP_IF_FALSE   696  'to 696'

 L. 545       730  LOAD_FAST                'self'
              732  LOAD_METHOD              checkSeisData
              734  LOAD_FAST                'self'
              736  LOAD_ATTR                ldtsave
              738  LOAD_METHOD              text
              740  CALL_METHOD_0         0  '0 positional arguments'
              742  LOAD_GLOBAL              str
              744  LOAD_FAST                '_label'
              746  CALL_FUNCTION_1       1  '1 positional argument'
              748  BINARY_ADD       
              750  CALL_METHOD_1         1  '1 positional argument'
          752_754  POP_JUMP_IF_FALSE   696  'to 696'

 L. 546       756  LOAD_GLOBAL              QtWidgets
              758  LOAD_ATTR                QMessageBox
              760  LOAD_METHOD              question
              762  LOAD_FAST                'self'
              764  LOAD_ATTR                msgbox
              766  LOAD_STR                 'Apply 3D-CNN'

 L. 547       768  LOAD_FAST                'self'
              770  LOAD_ATTR                ldtsave
              772  LOAD_METHOD              text
              774  CALL_METHOD_0         0  '0 positional arguments'
              776  LOAD_STR                 ' already exists. Overwrite?'
              778  BINARY_ADD       

 L. 548       780  LOAD_GLOBAL              QtWidgets
              782  LOAD_ATTR                QMessageBox
              784  LOAD_ATTR                Yes
              786  LOAD_GLOBAL              QtWidgets
              788  LOAD_ATTR                QMessageBox
              790  LOAD_ATTR                No
              792  BINARY_OR        

 L. 549       794  LOAD_GLOBAL              QtWidgets
              796  LOAD_ATTR                QMessageBox
              798  LOAD_ATTR                No
              800  CALL_METHOD_5         5  '5 positional arguments'
              802  STORE_FAST               'reply'

 L. 550       804  LOAD_FAST                'reply'
              806  LOAD_GLOBAL              QtWidgets
              808  LOAD_ATTR                QMessageBox
              810  LOAD_ATTR                No
              812  COMPARE_OP               ==
          814_816  POP_JUMP_IF_FALSE   822  'to 822'

 L. 551       818  LOAD_CONST               None
              820  RETURN_VALUE     
            822_0  COME_FROM           814  '814'

 L. 552       822  LOAD_FAST                'reply'
              824  LOAD_GLOBAL              QtWidgets
              826  LOAD_ATTR                QMessageBox
              828  LOAD_ATTR                Yes
              830  COMPARE_OP               ==
          832_834  POP_JUMP_IF_FALSE   696  'to 696'

 L. 553       836  BREAK_LOOP       
          838_840  JUMP_BACK           696  'to 696'
              842  POP_BLOCK        
            844_0  COME_FROM_LOOP      690  '690'

 L. 555       844  LOAD_CONST               2
              846  LOAD_GLOBAL              int
              848  LOAD_FAST                '_video_height_old'
              850  LOAD_CONST               2
              852  BINARY_TRUE_DIVIDE
              854  CALL_FUNCTION_1       1  '1 positional argument'
              856  BINARY_MULTIPLY  
              858  LOAD_CONST               1
              860  BINARY_ADD       
              862  STORE_FAST               '_video_height_old'

 L. 556       864  LOAD_CONST               2
              866  LOAD_GLOBAL              int
              868  LOAD_FAST                '_video_width_old'
              870  LOAD_CONST               2
              872  BINARY_TRUE_DIVIDE
              874  CALL_FUNCTION_1       1  '1 positional argument'
              876  BINARY_MULTIPLY  
              878  LOAD_CONST               1
              880  BINARY_ADD       
              882  STORE_FAST               '_video_width_old'

 L. 557       884  LOAD_CONST               2
              886  LOAD_GLOBAL              int
              888  LOAD_FAST                '_video_depth_old'
              890  LOAD_CONST               2
              892  BINARY_TRUE_DIVIDE
              894  CALL_FUNCTION_1       1  '1 positional argument'
              896  BINARY_MULTIPLY  
              898  LOAD_CONST               1
              900  BINARY_ADD       
              902  STORE_FAST               '_video_depth_old'

 L. 559       904  LOAD_GLOBAL              np
              906  LOAD_METHOD              shape
              908  LOAD_FAST                'self'
              910  LOAD_ATTR                seisdata
              912  LOAD_FAST                '_featurelist'
              914  LOAD_CONST               0
              916  BINARY_SUBSCR    
              918  BINARY_SUBSCR    
              920  CALL_METHOD_1         1  '1 positional argument'
              922  LOAD_CONST               0
              924  BINARY_SUBSCR    
              926  STORE_FAST               '_nsample'

 L. 561       928  LOAD_GLOBAL              int
              930  LOAD_GLOBAL              np
              932  LOAD_METHOD              ceil
              934  LOAD_FAST                '_nsample'
              936  LOAD_FAST                '_batch'
              938  BINARY_TRUE_DIVIDE
              940  CALL_METHOD_1         1  '1 positional argument'
              942  CALL_FUNCTION_1       1  '1 positional argument'
              944  STORE_FAST               '_nloop'

 L. 564       946  LOAD_GLOBAL              QtWidgets
              948  LOAD_METHOD              QProgressDialog
              950  CALL_METHOD_0         0  '0 positional arguments'
              952  STORE_FAST               '_pgsdlg'

 L. 565       954  LOAD_GLOBAL              QtGui
              956  LOAD_METHOD              QIcon
              958  CALL_METHOD_0         0  '0 positional arguments'
              960  STORE_FAST               'icon'

 L. 566       962  LOAD_FAST                'icon'
              964  LOAD_METHOD              addPixmap
              966  LOAD_GLOBAL              QtGui
              968  LOAD_METHOD              QPixmap
              970  LOAD_GLOBAL              os
              972  LOAD_ATTR                path
              974  LOAD_METHOD              join
              976  LOAD_FAST                'self'
              978  LOAD_ATTR                iconpath
              980  LOAD_STR                 'icons/apply.png'
              982  CALL_METHOD_2         2  '2 positional arguments'
              984  CALL_METHOD_1         1  '1 positional argument'

 L. 567       986  LOAD_GLOBAL              QtGui
              988  LOAD_ATTR                QIcon
              990  LOAD_ATTR                Normal
              992  LOAD_GLOBAL              QtGui
              994  LOAD_ATTR                QIcon
              996  LOAD_ATTR                Off
              998  CALL_METHOD_3         3  '3 positional arguments'
             1000  POP_TOP          

 L. 568      1002  LOAD_FAST                '_pgsdlg'
             1004  LOAD_METHOD              setWindowIcon
             1006  LOAD_FAST                'icon'
             1008  CALL_METHOD_1         1  '1 positional argument'
             1010  POP_TOP          

 L. 569      1012  LOAD_FAST                '_pgsdlg'
             1014  LOAD_METHOD              setWindowTitle
             1016  LOAD_STR                 'Apply 3D-CNN'
             1018  CALL_METHOD_1         1  '1 positional argument'
             1020  POP_TOP          

 L. 570      1022  LOAD_FAST                '_pgsdlg'
             1024  LOAD_METHOD              setCancelButton
             1026  LOAD_CONST               None
             1028  CALL_METHOD_1         1  '1 positional argument'
             1030  POP_TOP          

 L. 571      1032  LOAD_FAST                '_pgsdlg'
             1034  LOAD_METHOD              setWindowFlags
             1036  LOAD_GLOBAL              QtCore
             1038  LOAD_ATTR                Qt
             1040  LOAD_ATTR                WindowStaysOnTopHint
             1042  CALL_METHOD_1         1  '1 positional argument'
             1044  POP_TOP          

 L. 572      1046  LOAD_FAST                '_pgsdlg'
             1048  LOAD_METHOD              forceShow
             1050  CALL_METHOD_0         0  '0 positional arguments'
             1052  POP_TOP          

 L. 573      1054  LOAD_FAST                '_pgsdlg'
             1056  LOAD_METHOD              setFixedWidth
             1058  LOAD_CONST               400
             1060  CALL_METHOD_1         1  '1 positional argument'
             1062  POP_TOP          

 L. 574      1064  LOAD_FAST                '_pgsdlg'
             1066  LOAD_METHOD              setMaximum
             1068  LOAD_FAST                '_nloop'
             1070  CALL_METHOD_1         1  '1 positional argument'
             1072  POP_TOP          

 L. 576      1074  LOAD_GLOBAL              int
             1076  LOAD_FAST                '_video_depth_old'
             1078  LOAD_CONST               2
             1080  BINARY_TRUE_DIVIDE
             1082  CALL_FUNCTION_1       1  '1 positional argument'
             1084  STORE_FAST               '_wdinl'

 L. 577      1086  LOAD_GLOBAL              int
             1088  LOAD_FAST                '_video_width_old'
             1090  LOAD_CONST               2
             1092  BINARY_TRUE_DIVIDE
             1094  CALL_FUNCTION_1       1  '1 positional argument'
             1096  STORE_FAST               '_wdxl'

 L. 578      1098  LOAD_GLOBAL              int
             1100  LOAD_FAST                '_video_height_old'
             1102  LOAD_CONST               2
             1104  BINARY_TRUE_DIVIDE
             1106  CALL_FUNCTION_1       1  '1 positional argument'
             1108  STORE_FAST               '_wdz'

 L. 580      1110  LOAD_GLOBAL              seis_ays
             1112  LOAD_METHOD              convertSeisInfoTo2DMat
             1114  LOAD_FAST                'self'
             1116  LOAD_ATTR                survinfo
             1118  CALL_METHOD_1         1  '1 positional argument'
             1120  STORE_FAST               '_seisdata'

 L. 582      1122  LOAD_GLOBAL              np
             1124  LOAD_METHOD              zeros
             1126  LOAD_FAST                '_nsample'
             1128  LOAD_GLOBAL              len
             1130  LOAD_FAST                '_labellist'
             1132  CALL_FUNCTION_1       1  '1 positional argument'
             1134  BUILD_LIST_2          2 
             1136  CALL_METHOD_1         1  '1 positional argument'
             1138  STORE_FAST               '_result'

 L. 583      1140  LOAD_CONST               0
             1142  STORE_FAST               'idxstart'

 L. 584  1144_1146  SETUP_LOOP         1484  'to 1484'
             1148  LOAD_GLOBAL              range
             1150  LOAD_FAST                '_nloop'
             1152  CALL_FUNCTION_1       1  '1 positional argument'
             1154  GET_ITER         
         1156_1158  FOR_ITER           1482  'to 1482'
             1160  STORE_FAST               'i'

 L. 586      1162  LOAD_GLOBAL              QtCore
             1164  LOAD_ATTR                QCoreApplication
             1166  LOAD_METHOD              instance
             1168  CALL_METHOD_0         0  '0 positional arguments'
             1170  LOAD_METHOD              processEvents
             1172  CALL_METHOD_0         0  '0 positional arguments'
             1174  POP_TOP          

 L. 588      1176  LOAD_GLOBAL              sys
             1178  LOAD_ATTR                stdout
             1180  LOAD_METHOD              write

 L. 589      1182  LOAD_STR                 '\r>>> Apply 3D-CNN, proceeding %.1f%% '
             1184  LOAD_GLOBAL              float
             1186  LOAD_FAST                'i'
             1188  CALL_FUNCTION_1       1  '1 positional argument'
             1190  LOAD_GLOBAL              float
             1192  LOAD_FAST                '_nloop'
             1194  CALL_FUNCTION_1       1  '1 positional argument'
             1196  BINARY_TRUE_DIVIDE
             1198  LOAD_CONST               100.0
             1200  BINARY_MULTIPLY  
             1202  BINARY_MODULO    
             1204  CALL_METHOD_1         1  '1 positional argument'
             1206  POP_TOP          

 L. 590      1208  LOAD_GLOBAL              sys
             1210  LOAD_ATTR                stdout
             1212  LOAD_METHOD              flush
             1214  CALL_METHOD_0         0  '0 positional arguments'
             1216  POP_TOP          

 L. 592      1218  LOAD_FAST                'idxstart'
             1220  LOAD_FAST                '_batch'
             1222  BINARY_ADD       
             1224  STORE_FAST               'idxend'

 L. 593      1226  LOAD_FAST                'idxend'
             1228  LOAD_FAST                '_nsample'
             1230  COMPARE_OP               >
         1232_1234  POP_JUMP_IF_FALSE  1240  'to 1240'

 L. 594      1236  LOAD_FAST                '_nsample'
             1238  STORE_FAST               'idxend'
           1240_0  COME_FROM          1232  '1232'

 L. 595      1240  LOAD_GLOBAL              np
             1242  LOAD_METHOD              linspace
             1244  LOAD_FAST                'idxstart'
             1246  LOAD_FAST                'idxend'
             1248  LOAD_CONST               1
             1250  BINARY_SUBTRACT  
             1252  LOAD_FAST                'idxend'
             1254  LOAD_FAST                'idxstart'
             1256  BINARY_SUBTRACT  
             1258  CALL_METHOD_3         3  '3 positional arguments'
             1260  LOAD_METHOD              astype
             1262  LOAD_GLOBAL              int
             1264  CALL_METHOD_1         1  '1 positional argument'
             1266  STORE_FAST               'idxlist'

 L. 596      1268  LOAD_FAST                'idxend'
             1270  STORE_FAST               'idxstart'

 L. 598      1272  LOAD_FAST                '_seisdata'
             1274  LOAD_FAST                'idxlist'
             1276  LOAD_CONST               0
             1278  LOAD_CONST               3
             1280  BUILD_SLICE_2         2 
             1282  BUILD_TUPLE_2         2 
             1284  BINARY_SUBSCR    
             1286  STORE_FAST               '_targetdata'

 L. 600      1288  BUILD_MAP_0           0 
             1290  STORE_FAST               '_dict'

 L. 601      1292  SETUP_LOOP         1426  'to 1426'
             1294  LOAD_FAST                '_featurelist'
             1296  GET_ITER         
           1298_0  COME_FROM          1384  '1384'
             1298  FOR_ITER           1424  'to 1424'
             1300  STORE_FAST               'f'

 L. 602      1302  LOAD_FAST                'self'
             1304  LOAD_ATTR                seisdata
             1306  LOAD_FAST                'f'
             1308  BINARY_SUBSCR    
             1310  STORE_FAST               '_data'

 L. 603      1312  LOAD_GLOBAL              seis_ays
             1314  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1316  LOAD_FAST                '_data'
             1318  LOAD_FAST                '_targetdata'
             1320  LOAD_FAST                'self'
             1322  LOAD_ATTR                survinfo

 L. 604      1324  LOAD_FAST                '_wdinl'
             1326  LOAD_FAST                '_wdxl'
             1328  LOAD_FAST                '_wdz'

 L. 605      1330  LOAD_CONST               False
             1332  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1334  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1336  LOAD_CONST               None
             1338  LOAD_CONST               None
             1340  BUILD_SLICE_2         2 
             1342  LOAD_CONST               3
             1344  LOAD_CONST               None
             1346  BUILD_SLICE_2         2 
             1348  BUILD_TUPLE_2         2 
             1350  BINARY_SUBSCR    
             1352  LOAD_FAST                '_dict'
             1354  LOAD_FAST                'f'
             1356  STORE_SUBSCR     

 L. 606      1358  LOAD_FAST                '_video_height_new'
             1360  LOAD_FAST                '_video_height_old'
             1362  COMPARE_OP               !=
         1364_1366  POP_JUMP_IF_TRUE   1388  'to 1388'

 L. 607      1368  LOAD_FAST                '_video_width_new'
             1370  LOAD_FAST                '_video_width_old'
             1372  COMPARE_OP               !=
         1374_1376  POP_JUMP_IF_TRUE   1388  'to 1388'

 L. 608      1378  LOAD_FAST                '_video_depth_new'
             1380  LOAD_FAST                '_video_depth_old'
             1382  COMPARE_OP               !=
         1384_1386  POP_JUMP_IF_FALSE  1298  'to 1298'
           1388_0  COME_FROM          1374  '1374'
           1388_1  COME_FROM          1364  '1364'

 L. 609      1388  LOAD_GLOBAL              basic_video
             1390  LOAD_ATTR                changeVideoSize
             1392  LOAD_FAST                '_dict'
             1394  LOAD_FAST                'f'
             1396  BINARY_SUBSCR    

 L. 610      1398  LOAD_FAST                '_video_height_old'

 L. 611      1400  LOAD_FAST                '_video_width_old'

 L. 612      1402  LOAD_FAST                '_video_depth_old'

 L. 613      1404  LOAD_FAST                '_video_height_new'

 L. 614      1406  LOAD_FAST                '_video_width_new'

 L. 615      1408  LOAD_FAST                '_video_depth_new'
             1410  LOAD_CONST               ('video_height', 'video_width', 'video_depth', 'video_height_new', 'video_width_new', 'video_depth_new')
             1412  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1414  LOAD_FAST                '_dict'
             1416  LOAD_FAST                'f'
             1418  STORE_SUBSCR     
         1420_1422  JUMP_BACK          1298  'to 1298'
             1424  POP_BLOCK        
           1426_0  COME_FROM_LOOP     1292  '1292'

 L. 617      1426  LOAD_GLOBAL              ml_cnn3d
             1428  LOAD_ATTR                probabilityFrom3DCNNClassifier
             1430  LOAD_FAST                '_dict'

 L. 618      1432  LOAD_FAST                'self'
             1434  LOAD_ATTR                modelpath

 L. 619      1436  LOAD_FAST                'self'
             1438  LOAD_ATTR                modelname

 L. 620      1440  LOAD_FAST                '_labellist'

 L. 621      1442  LOAD_FAST                '_batch'

 L. 622      1444  LOAD_CONST               True
             1446  LOAD_CONST               ('cnn3dpath', 'cnn3dname', 'targetlist', 'batchsize', 'verbose')
             1448  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1450  LOAD_FAST                '_result'
             1452  LOAD_FAST                'idxlist'
             1454  LOAD_CONST               None
             1456  LOAD_CONST               None
             1458  BUILD_SLICE_2         2 
             1460  BUILD_TUPLE_2         2 
             1462  STORE_SUBSCR     

 L. 625      1464  LOAD_FAST                '_pgsdlg'
             1466  LOAD_METHOD              setValue
             1468  LOAD_FAST                'i'
             1470  LOAD_CONST               1
             1472  BINARY_ADD       
             1474  CALL_METHOD_1         1  '1 positional argument'
             1476  POP_TOP          
         1478_1480  JUMP_BACK          1156  'to 1156'
             1482  POP_BLOCK        
           1484_0  COME_FROM_LOOP     1144  '1144'

 L. 627      1484  LOAD_GLOBAL              print
             1486  LOAD_STR                 'Done'
             1488  CALL_FUNCTION_1       1  '1 positional argument'
             1490  POP_TOP          

 L. 629      1492  SETUP_LOOP         1610  'to 1610'
             1494  LOAD_GLOBAL              range
             1496  LOAD_GLOBAL              len
             1498  LOAD_FAST                '_labellist'
             1500  CALL_FUNCTION_1       1  '1 positional argument'
             1502  CALL_FUNCTION_1       1  '1 positional argument'
             1504  GET_ITER         
             1506  FOR_ITER           1608  'to 1608'
             1508  STORE_FAST               'i'

 L. 630      1510  LOAD_GLOBAL              np
             1512  LOAD_METHOD              transpose
             1514  LOAD_GLOBAL              np
             1516  LOAD_METHOD              reshape
             1518  LOAD_FAST                '_result'
             1520  LOAD_CONST               None
             1522  LOAD_CONST               None
             1524  BUILD_SLICE_2         2 
             1526  LOAD_FAST                'i'
             1528  LOAD_FAST                'i'
             1530  LOAD_CONST               1
             1532  BINARY_ADD       
             1534  BUILD_SLICE_2         2 
             1536  BUILD_TUPLE_2         2 
             1538  BINARY_SUBSCR    

 L. 631      1540  LOAD_FAST                'self'
             1542  LOAD_ATTR                survinfo
             1544  LOAD_STR                 'ILNum'
             1546  BINARY_SUBSCR    

 L. 632      1548  LOAD_FAST                'self'
             1550  LOAD_ATTR                survinfo
             1552  LOAD_STR                 'XLNum'
             1554  BINARY_SUBSCR    

 L. 633      1556  LOAD_FAST                'self'
             1558  LOAD_ATTR                survinfo
             1560  LOAD_STR                 'ZNum'
             1562  BINARY_SUBSCR    
             1564  BUILD_LIST_3          3 
             1566  CALL_METHOD_2         2  '2 positional arguments'

 L. 634      1568  LOAD_CONST               2
             1570  LOAD_CONST               1
             1572  LOAD_CONST               0
             1574  BUILD_LIST_3          3 
             1576  CALL_METHOD_2         2  '2 positional arguments'
             1578  LOAD_FAST                'self'
             1580  LOAD_ATTR                seisdata
             1582  LOAD_FAST                'self'
             1584  LOAD_ATTR                ldtsave
             1586  LOAD_METHOD              text
             1588  CALL_METHOD_0         0  '0 positional arguments'
             1590  LOAD_GLOBAL              str
             1592  LOAD_FAST                '_labellist'
             1594  LOAD_FAST                'i'
             1596  BINARY_SUBSCR    
             1598  CALL_FUNCTION_1       1  '1 positional argument'
             1600  BINARY_ADD       
             1602  STORE_SUBSCR     
         1604_1606  JUMP_BACK          1506  'to 1506'
             1608  POP_BLOCK        
           1610_0  COME_FROM_LOOP     1492  '1492'

 L. 636      1610  LOAD_GLOBAL              QtWidgets
             1612  LOAD_ATTR                QMessageBox
             1614  LOAD_METHOD              information
             1616  LOAD_FAST                'self'
             1618  LOAD_ATTR                msgbox

 L. 637      1620  LOAD_STR                 'Apply 3D-CNN'

 L. 638      1622  LOAD_STR                 'CNN applied successfully'
             1624  CALL_METHOD_3         3  '3 positional arguments'
             1626  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 1624

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
    ApplyMl3DCnn4Prob = QtWidgets.QWidget()
    gui = applyml3dcnn4prob()
    gui.setupGUI(ApplyMl3DCnn4Prob)
    ApplyMl3DCnn4Prob.show()
    sys.exit(app.exec_())