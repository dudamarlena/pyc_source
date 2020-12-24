# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\applyml3dcnn4pred.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 34324 bytes
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

class applyml3dcnn4pred(object):
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

    def setupGUI(self, ApplyMl3DCnn4Pred):
        ApplyMl3DCnn4Pred.setObjectName('ApplyMl3DCnn4Pred')
        ApplyMl3DCnn4Pred.setFixedSize(800, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ApplyMl3DCnn4Pred.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ApplyMl3DCnn4Pred)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ApplyMl3DCnn4Pred)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lbloldsize = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 180, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 180, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 180, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 220, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 220, 40, 30))
        self.lblolddepth = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblolddepth.setObjectName('lblolddepth')
        self.lblolddepth.setGeometry(QtCore.QRect(100, 260, 50, 30))
        self.ldtolddepth = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtolddepth.setObjectName('ldtolddepth')
        self.ldtolddepth.setGeometry(QtCore.QRect(150, 260, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 180, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 180, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 180, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 220, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 220, 40, 30))
        self.lblnewdepth = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblnewdepth.setObjectName('lblnewdepth')
        self.lblnewdepth.setGeometry(QtCore.QRect(300, 260, 50, 30))
        self.ldtnewdepth = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtnewdepth.setObjectName('ldtnewdepth')
        self.ldtnewdepth.setGeometry(QtCore.QRect(350, 260, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ApplyMl3DCnn4Pred)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ApplyMl3DCnn4Pred)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 130))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(ApplyMl3DCnn4Pred)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 140, 180, 130))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblmaskdepth = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblmaskdepth.setObjectName('lblmaskdepth')
        self.lblmaskdepth.setGeometry(QtCore.QRect(500, 360, 50, 30))
        self.ldtmaskdepth = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtmaskdepth.setObjectName('ldtmaskdepth')
        self.ldtmaskdepth.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.lblpooldepth = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblpooldepth.setObjectName('lblpooldepth')
        self.lblpooldepth.setGeometry(QtCore.QRect(700, 360, 50, 30))
        self.ldtpooldepth = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtpooldepth.setObjectName('ldtpooldepth')
        self.ldtpooldepth.setGeometry(QtCore.QRect(750, 360, 40, 30))
        self.lblpara = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblsave = QtWidgets.QLabel(ApplyMl3DCnn4Pred)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ApplyMl3DCnn4Pred)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.btnapply = QtWidgets.QPushButton(ApplyMl3DCnn4Pred)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(320, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ApplyMl3DCnn4Pred)
        self.msgbox.setObjectName('msgbox')
        _center_x = ApplyMl3DCnn4Pred.geometry().center().x()
        _center_y = ApplyMl3DCnn4Pred.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ApplyMl3DCnn4Pred)
        QtCore.QMetaObject.connectSlotsByName(ApplyMl3DCnn4Pred)

    def retranslateGUI(self, ApplyMl3DCnn4Pred):
        self.dialog = ApplyMl3DCnn4Pred
        _translate = QtCore.QCoreApplication.translate
        ApplyMl3DCnn4Pred.setWindowTitle(_translate('ApplyMl3DCnn4Pred', 'Apply 3D-CNN for prediction'))
        self.lblfrom.setText(_translate('ApplyMl3DCnn4Pred', 'Select network:'))
        self.ldtfrom.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ApplyMl3DCnn4Pred', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ApplyMl3DCnn4Pred', 'Training features:'))
        self.lbloldsize.setText(_translate('ApplyMl3DCnn4Pred', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('ApplyMl3DCnn4Pred', 'height=\ntime/depth'))
        self.ldtoldheight.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('ApplyMl3DCnn4Pred', 'width=\ncrosslien'))
        self.ldtoldwidth.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblolddepth.setText(_translate('ApplyMl3DCnn4Pred', 'depth=\ninline'))
        self.ldtolddepth.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtolddepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('ApplyMl3DCnn4Pred', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('ApplyMl3DCnn4Pred', 'height='))
        self.ldtnewheight.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewheight.setEnabled(False)
        self.lblnewwidth.setText(_translate('ApplyMl3DCnn4Pred', 'width='))
        self.ldtnewwidth.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewwidth.setEnabled(False)
        self.lblnewdepth.setText(_translate('ApplyMl3DCnn4Pred', 'depth='))
        self.ldtnewdepth.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtnewdepth.setEnabled(False)
        self.ldtnewdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('ApplyMl3DCnn4Pred', 'Pre-trained CNN architecture:'))
        self.btnviewnetwork.setText(_translate('ApplyMl3DCnn4Pred', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('ApplyMl3DCnn4Pred', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblnfclayer.setText(_translate('ApplyMl3DCnn4Pred', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtnfclayer.setEnabled(False)
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblmasksize.setText(_translate('ApplyMl3DCnn4Pred', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ApplyMl3DCnn4Pred', 'height='))
        self.ldtmaskheight.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ApplyMl3DCnn4Pred', 'width='))
        self.ldtmaskwidth.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskdepth.setText(_translate('ApplyMl3DCnn4Pred', 'depth='))
        self.ldtmaskdepth.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtmaskdepth.setEnabled(False)
        self.ldtmaskdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ApplyMl3DCnn4Pred', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ApplyMl3DCnn4Pred', 'height='))
        self.ldtpoolheight.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ApplyMl3DCnn4Pred', 'width='))
        self.ldtpoolwidth.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpooldepth.setText(_translate('ApplyMl3DCnn4Pred', 'depth='))
        self.ldtpooldepth.setText(_translate('ApplyMl3DCnn4Pred', ''))
        self.ldtpooldepth.setEnabled(False)
        self.ldtpooldepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ApplyMl3DCnn4Pred', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ApplyMl3DCnn4Pred', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ApplyMl3DCnn4Pred', '5000'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('ApplyMl3DCnn4Pred', 'Output name='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ApplyMl3DCnn4Pred', 'cnn3d'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('ApplyMl3DCnn4Pred', 'Apply 3D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnApplyMl3DCnn4Pred)

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

    def clickBtnApplyMl3DCnn4Pred--- This code section failed: ---

 L. 463         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 465         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 466        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in ApplyMl3DCnn4Pred: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 467        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 468        44  LOAD_STR                 'Apply 3D-CNN'

 L. 469        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 470        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 471        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              check3DCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 472        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in ApplyMl3DCnn4Pred: No CNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 473        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 474       100  LOAD_STR                 'Apply 3D-CNN'

 L. 475       102  LOAD_STR                 'No CNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 476       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 477       112  LOAD_FAST                'self'
              114  LOAD_ATTR                modelinfo
              116  LOAD_STR                 'feature_list'
              118  BINARY_SUBSCR    
              120  STORE_FAST               '_featurelist'

 L. 478       122  SETUP_LOOP          198  'to 198'
              124  LOAD_FAST                '_featurelist'
              126  GET_ITER         
            128_0  COME_FROM           144  '144'
              128  FOR_ITER            196  'to 196'
              130  STORE_FAST               'f'

 L. 479       132  LOAD_FAST                'self'
              134  LOAD_METHOD              checkSeisData
              136  LOAD_FAST                'f'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_CONST               False
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   128  'to 128'

 L. 480       146  LOAD_GLOBAL              vis_msg
              148  LOAD_ATTR                print
              150  LOAD_STR                 "ERROR in ApplyMl3DCnn4Pred: Feature '%s' not found in seismic data"
              152  LOAD_FAST                'f'
              154  BINARY_MODULO    

 L. 481       156  LOAD_STR                 'error'
              158  LOAD_CONST               ('type',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  POP_TOP          

 L. 482       164  LOAD_GLOBAL              QtWidgets
              166  LOAD_ATTR                QMessageBox
              168  LOAD_METHOD              critical
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                msgbox

 L. 483       174  LOAD_STR                 'Apply 3D-CNN'

 L. 484       176  LOAD_STR                 "Feature '"
              178  LOAD_FAST                'f'
              180  BINARY_ADD       
              182  LOAD_STR                 "' not found in seismic data"
              184  BINARY_ADD       
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 485       190  LOAD_CONST               None
              192  RETURN_VALUE     
              194  JUMP_BACK           128  'to 128'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      122  '122'

 L. 487       198  LOAD_GLOBAL              basic_data
              200  LOAD_METHOD              str2int
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                ldtoldheight
              206  LOAD_METHOD              text
              208  CALL_METHOD_0         0  '0 positional arguments'
              210  CALL_METHOD_1         1  '1 positional argument'
              212  STORE_FAST               '_video_height_old'

 L. 488       214  LOAD_GLOBAL              basic_data
              216  LOAD_METHOD              str2int
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                ldtoldwidth
              222  LOAD_METHOD              text
              224  CALL_METHOD_0         0  '0 positional arguments'
              226  CALL_METHOD_1         1  '1 positional argument'
              228  STORE_FAST               '_video_width_old'

 L. 489       230  LOAD_GLOBAL              basic_data
              232  LOAD_METHOD              str2int
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                ldtolddepth
              238  LOAD_METHOD              text
              240  CALL_METHOD_0         0  '0 positional arguments'
              242  CALL_METHOD_1         1  '1 positional argument'
              244  STORE_FAST               '_video_depth_old'

 L. 490       246  LOAD_GLOBAL              basic_data
              248  LOAD_METHOD              str2int
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                ldtnewheight
              254  LOAD_METHOD              text
              256  CALL_METHOD_0         0  '0 positional arguments'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  STORE_FAST               '_video_height_new'

 L. 491       262  LOAD_GLOBAL              basic_data
              264  LOAD_METHOD              str2int
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                ldtnewwidth
              270  LOAD_METHOD              text
              272  CALL_METHOD_0         0  '0 positional arguments'
              274  CALL_METHOD_1         1  '1 positional argument'
              276  STORE_FAST               '_video_width_new'

 L. 492       278  LOAD_GLOBAL              basic_data
              280  LOAD_METHOD              str2int
              282  LOAD_FAST                'self'
              284  LOAD_ATTR                ldtnewdepth
              286  LOAD_METHOD              text
              288  CALL_METHOD_0         0  '0 positional arguments'
              290  CALL_METHOD_1         1  '1 positional argument'
              292  STORE_FAST               '_video_depth_new'

 L. 493       294  LOAD_FAST                '_video_height_old'
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

 L. 494       324  LOAD_FAST                '_video_height_new'
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

 L. 495       354  LOAD_GLOBAL              vis_msg
              356  LOAD_ATTR                print
              358  LOAD_STR                 'ERROR in ApplyMl3DCnn4Pred: Non-integer feature size'
              360  LOAD_STR                 'error'
              362  LOAD_CONST               ('type',)
              364  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              366  POP_TOP          

 L. 496       368  LOAD_GLOBAL              QtWidgets
              370  LOAD_ATTR                QMessageBox
              372  LOAD_METHOD              critical
              374  LOAD_FAST                'self'
              376  LOAD_ATTR                msgbox

 L. 497       378  LOAD_STR                 'Apply 3D-CNN'

 L. 498       380  LOAD_STR                 'Non-integer feature size'
              382  CALL_METHOD_3         3  '3 positional arguments'
              384  POP_TOP          

 L. 499       386  LOAD_CONST               None
              388  RETURN_VALUE     
            390_0  COME_FROM           350  '350'

 L. 500       390  LOAD_FAST                '_video_height_old'
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

 L. 501       420  LOAD_FAST                '_video_height_new'
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

 L. 502       450  LOAD_GLOBAL              vis_msg
              452  LOAD_ATTR                print
              454  LOAD_STR                 'ERROR in ApplyMl2DCnn: Features are not 3D '
              456  LOAD_STR                 'error'
              458  LOAD_CONST               ('type',)
              460  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              462  POP_TOP          

 L. 503       464  LOAD_GLOBAL              QtWidgets
              466  LOAD_ATTR                QMessageBox
              468  LOAD_METHOD              critical
              470  LOAD_FAST                'self'
              472  LOAD_ATTR                msgbox

 L. 504       474  LOAD_STR                 'Apply 2D-CNN'

 L. 505       476  LOAD_STR                 'Features are not 3D '
              478  CALL_METHOD_3         3  '3 positional arguments'
              480  POP_TOP          

 L. 506       482  LOAD_CONST               None
              484  RETURN_VALUE     
            486_0  COME_FROM           446  '446'

 L. 508       486  LOAD_GLOBAL              basic_data
              488  LOAD_METHOD              str2int
              490  LOAD_FAST                'self'
              492  LOAD_ATTR                ldtbatchsize
              494  LOAD_METHOD              text
              496  CALL_METHOD_0         0  '0 positional arguments'
              498  CALL_METHOD_1         1  '1 positional argument'
              500  STORE_FAST               '_batch'

 L. 509       502  LOAD_FAST                '_batch'
              504  LOAD_CONST               False
              506  COMPARE_OP               is
          508_510  POP_JUMP_IF_TRUE    522  'to 522'
              512  LOAD_FAST                '_batch'
              514  LOAD_CONST               1
              516  COMPARE_OP               <
          518_520  POP_JUMP_IF_FALSE   558  'to 558'
            522_0  COME_FROM           508  '508'

 L. 510       522  LOAD_GLOBAL              vis_msg
              524  LOAD_ATTR                print
              526  LOAD_STR                 'ERROR in ApplyMl3DCnn4Pred: Non-positive batch size'
              528  LOAD_STR                 'error'
              530  LOAD_CONST               ('type',)
              532  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              534  POP_TOP          

 L. 511       536  LOAD_GLOBAL              QtWidgets
              538  LOAD_ATTR                QMessageBox
              540  LOAD_METHOD              critical
              542  LOAD_FAST                'self'
              544  LOAD_ATTR                msgbox

 L. 512       546  LOAD_STR                 'Apply 3D-CNN'

 L. 513       548  LOAD_STR                 'Non-positive batch size'
              550  CALL_METHOD_3         3  '3 positional arguments'
              552  POP_TOP          

 L. 514       554  LOAD_CONST               None
              556  RETURN_VALUE     
            558_0  COME_FROM           518  '518'

 L. 516       558  LOAD_GLOBAL              len
              560  LOAD_FAST                'self'
              562  LOAD_ATTR                ldtsave
              564  LOAD_METHOD              text
              566  CALL_METHOD_0         0  '0 positional arguments'
              568  CALL_FUNCTION_1       1  '1 positional argument'
              570  LOAD_CONST               1
              572  COMPARE_OP               <
          574_576  POP_JUMP_IF_FALSE   614  'to 614'

 L. 517       578  LOAD_GLOBAL              vis_msg
              580  LOAD_ATTR                print
              582  LOAD_STR                 'ERROR in ApplyMl3DCnn4Pred: No name specified'
              584  LOAD_STR                 'error'
              586  LOAD_CONST               ('type',)
              588  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              590  POP_TOP          

 L. 518       592  LOAD_GLOBAL              QtWidgets
              594  LOAD_ATTR                QMessageBox
              596  LOAD_METHOD              critical
              598  LOAD_FAST                'self'
              600  LOAD_ATTR                msgbox

 L. 519       602  LOAD_STR                 'Apply 3D-CNN'

 L. 520       604  LOAD_STR                 'No name specified'
              606  CALL_METHOD_3         3  '3 positional arguments'
              608  POP_TOP          

 L. 521       610  LOAD_CONST               None
              612  RETURN_VALUE     
            614_0  COME_FROM           574  '574'

 L. 522       614  LOAD_FAST                'self'
              616  LOAD_ATTR                ldtsave
              618  LOAD_METHOD              text
              620  CALL_METHOD_0         0  '0 positional arguments'
              622  LOAD_FAST                'self'
              624  LOAD_ATTR                seisdata
              626  LOAD_METHOD              keys
              628  CALL_METHOD_0         0  '0 positional arguments'
              630  COMPARE_OP               in
          632_634  POP_JUMP_IF_FALSE   720  'to 720'
              636  LOAD_FAST                'self'
              638  LOAD_METHOD              checkSeisData
              640  LOAD_FAST                'self'
              642  LOAD_ATTR                ldtsave
              644  LOAD_METHOD              text
              646  CALL_METHOD_0         0  '0 positional arguments'
              648  CALL_METHOD_1         1  '1 positional argument'
          650_652  POP_JUMP_IF_FALSE   720  'to 720'

 L. 523       654  LOAD_GLOBAL              QtWidgets
              656  LOAD_ATTR                QMessageBox
              658  LOAD_METHOD              question
              660  LOAD_FAST                'self'
              662  LOAD_ATTR                msgbox
              664  LOAD_STR                 'Apply 3D-CNN'

 L. 524       666  LOAD_FAST                'self'
              668  LOAD_ATTR                ldtsave
              670  LOAD_METHOD              text
              672  CALL_METHOD_0         0  '0 positional arguments'
              674  LOAD_STR                 ' already exists. Overwrite?'
              676  BINARY_ADD       

 L. 525       678  LOAD_GLOBAL              QtWidgets
              680  LOAD_ATTR                QMessageBox
              682  LOAD_ATTR                Yes
              684  LOAD_GLOBAL              QtWidgets
              686  LOAD_ATTR                QMessageBox
              688  LOAD_ATTR                No
              690  BINARY_OR        

 L. 526       692  LOAD_GLOBAL              QtWidgets
              694  LOAD_ATTR                QMessageBox
              696  LOAD_ATTR                No
              698  CALL_METHOD_5         5  '5 positional arguments'
              700  STORE_FAST               'reply'

 L. 528       702  LOAD_FAST                'reply'
              704  LOAD_GLOBAL              QtWidgets
              706  LOAD_ATTR                QMessageBox
              708  LOAD_ATTR                No
              710  COMPARE_OP               ==
          712_714  POP_JUMP_IF_FALSE   720  'to 720'

 L. 529       716  LOAD_CONST               None
              718  RETURN_VALUE     
            720_0  COME_FROM           712  '712'
            720_1  COME_FROM           650  '650'
            720_2  COME_FROM           632  '632'

 L. 531       720  LOAD_CONST               2
              722  LOAD_GLOBAL              int
              724  LOAD_FAST                '_video_height_old'
              726  LOAD_CONST               2
              728  BINARY_TRUE_DIVIDE
              730  CALL_FUNCTION_1       1  '1 positional argument'
              732  BINARY_MULTIPLY  
              734  LOAD_CONST               1
              736  BINARY_ADD       
              738  STORE_FAST               '_video_height_old'

 L. 532       740  LOAD_CONST               2
              742  LOAD_GLOBAL              int
              744  LOAD_FAST                '_video_width_old'
              746  LOAD_CONST               2
              748  BINARY_TRUE_DIVIDE
              750  CALL_FUNCTION_1       1  '1 positional argument'
              752  BINARY_MULTIPLY  
              754  LOAD_CONST               1
              756  BINARY_ADD       
              758  STORE_FAST               '_video_width_old'

 L. 533       760  LOAD_CONST               2
              762  LOAD_GLOBAL              int
              764  LOAD_FAST                '_video_depth_old'
              766  LOAD_CONST               2
              768  BINARY_TRUE_DIVIDE
              770  CALL_FUNCTION_1       1  '1 positional argument'
              772  BINARY_MULTIPLY  
              774  LOAD_CONST               1
              776  BINARY_ADD       
              778  STORE_FAST               '_video_depth_old'

 L. 535       780  LOAD_GLOBAL              np
              782  LOAD_METHOD              shape
              784  LOAD_FAST                'self'
              786  LOAD_ATTR                seisdata
              788  LOAD_FAST                '_featurelist'
              790  LOAD_CONST               0
              792  BINARY_SUBSCR    
              794  BINARY_SUBSCR    
              796  CALL_METHOD_1         1  '1 positional argument'
              798  LOAD_CONST               0
              800  BINARY_SUBSCR    
              802  STORE_FAST               '_nsample'

 L. 537       804  LOAD_GLOBAL              int
              806  LOAD_GLOBAL              np
              808  LOAD_METHOD              ceil
              810  LOAD_FAST                '_nsample'
              812  LOAD_FAST                '_batch'
              814  BINARY_TRUE_DIVIDE
              816  CALL_METHOD_1         1  '1 positional argument'
              818  CALL_FUNCTION_1       1  '1 positional argument'
              820  STORE_FAST               '_nloop'

 L. 540       822  LOAD_GLOBAL              QtWidgets
              824  LOAD_METHOD              QProgressDialog
              826  CALL_METHOD_0         0  '0 positional arguments'
              828  STORE_FAST               '_pgsdlg'

 L. 541       830  LOAD_GLOBAL              QtGui
              832  LOAD_METHOD              QIcon
              834  CALL_METHOD_0         0  '0 positional arguments'
              836  STORE_FAST               'icon'

 L. 542       838  LOAD_FAST                'icon'
              840  LOAD_METHOD              addPixmap
              842  LOAD_GLOBAL              QtGui
              844  LOAD_METHOD              QPixmap
              846  LOAD_GLOBAL              os
              848  LOAD_ATTR                path
              850  LOAD_METHOD              join
              852  LOAD_FAST                'self'
              854  LOAD_ATTR                iconpath
              856  LOAD_STR                 'icons/apply.png'
              858  CALL_METHOD_2         2  '2 positional arguments'
              860  CALL_METHOD_1         1  '1 positional argument'

 L. 543       862  LOAD_GLOBAL              QtGui
              864  LOAD_ATTR                QIcon
              866  LOAD_ATTR                Normal
              868  LOAD_GLOBAL              QtGui
              870  LOAD_ATTR                QIcon
              872  LOAD_ATTR                Off
              874  CALL_METHOD_3         3  '3 positional arguments'
              876  POP_TOP          

 L. 544       878  LOAD_FAST                '_pgsdlg'
              880  LOAD_METHOD              setWindowIcon
              882  LOAD_FAST                'icon'
              884  CALL_METHOD_1         1  '1 positional argument'
              886  POP_TOP          

 L. 545       888  LOAD_FAST                '_pgsdlg'
              890  LOAD_METHOD              setWindowTitle
              892  LOAD_STR                 'Apply 3D-CNN'
              894  CALL_METHOD_1         1  '1 positional argument'
              896  POP_TOP          

 L. 546       898  LOAD_FAST                '_pgsdlg'
              900  LOAD_METHOD              setCancelButton
              902  LOAD_CONST               None
              904  CALL_METHOD_1         1  '1 positional argument'
              906  POP_TOP          

 L. 547       908  LOAD_FAST                '_pgsdlg'
              910  LOAD_METHOD              setWindowFlags
              912  LOAD_GLOBAL              QtCore
              914  LOAD_ATTR                Qt
              916  LOAD_ATTR                WindowStaysOnTopHint
              918  CALL_METHOD_1         1  '1 positional argument'
              920  POP_TOP          

 L. 548       922  LOAD_FAST                '_pgsdlg'
              924  LOAD_METHOD              forceShow
              926  CALL_METHOD_0         0  '0 positional arguments'
              928  POP_TOP          

 L. 549       930  LOAD_FAST                '_pgsdlg'
              932  LOAD_METHOD              setFixedWidth
              934  LOAD_CONST               400
              936  CALL_METHOD_1         1  '1 positional argument'
              938  POP_TOP          

 L. 550       940  LOAD_FAST                '_pgsdlg'
              942  LOAD_METHOD              setMaximum
              944  LOAD_FAST                '_nloop'
              946  CALL_METHOD_1         1  '1 positional argument'
              948  POP_TOP          

 L. 552       950  LOAD_GLOBAL              int
              952  LOAD_FAST                '_video_depth_old'
              954  LOAD_CONST               2
              956  BINARY_TRUE_DIVIDE
              958  CALL_FUNCTION_1       1  '1 positional argument'
              960  STORE_FAST               '_wdinl'

 L. 553       962  LOAD_GLOBAL              int
              964  LOAD_FAST                '_video_width_old'
              966  LOAD_CONST               2
              968  BINARY_TRUE_DIVIDE
              970  CALL_FUNCTION_1       1  '1 positional argument'
              972  STORE_FAST               '_wdxl'

 L. 554       974  LOAD_GLOBAL              int
              976  LOAD_FAST                '_video_height_old'
              978  LOAD_CONST               2
              980  BINARY_TRUE_DIVIDE
              982  CALL_FUNCTION_1       1  '1 positional argument'
              984  STORE_FAST               '_wdz'

 L. 556       986  LOAD_GLOBAL              seis_ays
              988  LOAD_METHOD              convertSeisInfoTo2DMat
              990  LOAD_FAST                'self'
              992  LOAD_ATTR                survinfo
              994  CALL_METHOD_1         1  '1 positional argument'
              996  STORE_FAST               '_seisdata'

 L. 558       998  LOAD_GLOBAL              np
             1000  LOAD_METHOD              zeros
             1002  LOAD_FAST                '_nsample'
             1004  LOAD_CONST               1
             1006  BUILD_LIST_2          2 
             1008  CALL_METHOD_1         1  '1 positional argument'
             1010  STORE_FAST               '_result'

 L. 559      1012  LOAD_CONST               0
             1014  STORE_FAST               'idxstart'

 L. 560  1016_1018  SETUP_LOOP         1354  'to 1354'
             1020  LOAD_GLOBAL              range
             1022  LOAD_FAST                '_nloop'
             1024  CALL_FUNCTION_1       1  '1 positional argument'
             1026  GET_ITER         
         1028_1030  FOR_ITER           1352  'to 1352'
             1032  STORE_FAST               'i'

 L. 562      1034  LOAD_GLOBAL              QtCore
             1036  LOAD_ATTR                QCoreApplication
             1038  LOAD_METHOD              instance
             1040  CALL_METHOD_0         0  '0 positional arguments'
             1042  LOAD_METHOD              processEvents
             1044  CALL_METHOD_0         0  '0 positional arguments'
             1046  POP_TOP          

 L. 564      1048  LOAD_GLOBAL              sys
             1050  LOAD_ATTR                stdout
             1052  LOAD_METHOD              write

 L. 565      1054  LOAD_STR                 '\r>>> Apply 3D-CNN, proceeding %.1f%% '
             1056  LOAD_GLOBAL              float
             1058  LOAD_FAST                'i'
             1060  CALL_FUNCTION_1       1  '1 positional argument'
             1062  LOAD_GLOBAL              float
             1064  LOAD_FAST                '_nloop'
             1066  CALL_FUNCTION_1       1  '1 positional argument'
             1068  BINARY_TRUE_DIVIDE
             1070  LOAD_CONST               100.0
             1072  BINARY_MULTIPLY  
             1074  BINARY_MODULO    
             1076  CALL_METHOD_1         1  '1 positional argument'
             1078  POP_TOP          

 L. 566      1080  LOAD_GLOBAL              sys
             1082  LOAD_ATTR                stdout
             1084  LOAD_METHOD              flush
             1086  CALL_METHOD_0         0  '0 positional arguments'
             1088  POP_TOP          

 L. 568      1090  LOAD_FAST                'idxstart'
             1092  LOAD_FAST                '_batch'
             1094  BINARY_ADD       
             1096  STORE_FAST               'idxend'

 L. 569      1098  LOAD_FAST                'idxend'
             1100  LOAD_FAST                '_nsample'
             1102  COMPARE_OP               >
         1104_1106  POP_JUMP_IF_FALSE  1112  'to 1112'

 L. 570      1108  LOAD_FAST                '_nsample'
             1110  STORE_FAST               'idxend'
           1112_0  COME_FROM          1104  '1104'

 L. 571      1112  LOAD_GLOBAL              np
             1114  LOAD_METHOD              linspace
             1116  LOAD_FAST                'idxstart'
             1118  LOAD_FAST                'idxend'
             1120  LOAD_CONST               1
             1122  BINARY_SUBTRACT  
             1124  LOAD_FAST                'idxend'
             1126  LOAD_FAST                'idxstart'
             1128  BINARY_SUBTRACT  
             1130  CALL_METHOD_3         3  '3 positional arguments'
             1132  LOAD_METHOD              astype
             1134  LOAD_GLOBAL              int
             1136  CALL_METHOD_1         1  '1 positional argument'
             1138  STORE_FAST               'idxlist'

 L. 572      1140  LOAD_FAST                'idxend'
             1142  STORE_FAST               'idxstart'

 L. 574      1144  LOAD_FAST                '_seisdata'
             1146  LOAD_FAST                'idxlist'
             1148  LOAD_CONST               0
             1150  LOAD_CONST               3
             1152  BUILD_SLICE_2         2 
             1154  BUILD_TUPLE_2         2 
             1156  BINARY_SUBSCR    
             1158  STORE_FAST               '_targetdata'

 L. 576      1160  BUILD_MAP_0           0 
             1162  STORE_FAST               '_dict'

 L. 577      1164  SETUP_LOOP         1298  'to 1298'
             1166  LOAD_FAST                '_featurelist'
             1168  GET_ITER         
           1170_0  COME_FROM          1256  '1256'
             1170  FOR_ITER           1296  'to 1296'
             1172  STORE_FAST               'f'

 L. 578      1174  LOAD_FAST                'self'
             1176  LOAD_ATTR                seisdata
             1178  LOAD_FAST                'f'
             1180  BINARY_SUBSCR    
             1182  STORE_FAST               '_data'

 L. 579      1184  LOAD_GLOBAL              seis_ays
             1186  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1188  LOAD_FAST                '_data'
             1190  LOAD_FAST                '_targetdata'
             1192  LOAD_FAST                'self'
             1194  LOAD_ATTR                survinfo

 L. 580      1196  LOAD_FAST                '_wdinl'
             1198  LOAD_FAST                '_wdxl'
             1200  LOAD_FAST                '_wdz'

 L. 581      1202  LOAD_CONST               False
             1204  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1206  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1208  LOAD_CONST               None
             1210  LOAD_CONST               None
             1212  BUILD_SLICE_2         2 
             1214  LOAD_CONST               3
             1216  LOAD_CONST               None
             1218  BUILD_SLICE_2         2 
             1220  BUILD_TUPLE_2         2 
             1222  BINARY_SUBSCR    
             1224  LOAD_FAST                '_dict'
             1226  LOAD_FAST                'f'
             1228  STORE_SUBSCR     

 L. 582      1230  LOAD_FAST                '_video_height_new'
             1232  LOAD_FAST                '_video_height_old'
             1234  COMPARE_OP               !=
         1236_1238  POP_JUMP_IF_TRUE   1260  'to 1260'

 L. 583      1240  LOAD_FAST                '_video_width_new'
             1242  LOAD_FAST                '_video_width_old'
             1244  COMPARE_OP               !=
         1246_1248  POP_JUMP_IF_TRUE   1260  'to 1260'

 L. 584      1250  LOAD_FAST                '_video_depth_new'
             1252  LOAD_FAST                '_video_depth_old'
             1254  COMPARE_OP               !=
         1256_1258  POP_JUMP_IF_FALSE  1170  'to 1170'
           1260_0  COME_FROM          1246  '1246'
           1260_1  COME_FROM          1236  '1236'

 L. 585      1260  LOAD_GLOBAL              basic_video
             1262  LOAD_ATTR                changeVideoSize
             1264  LOAD_FAST                '_dict'
             1266  LOAD_FAST                'f'
             1268  BINARY_SUBSCR    

 L. 586      1270  LOAD_FAST                '_video_height_old'

 L. 587      1272  LOAD_FAST                '_video_width_old'

 L. 588      1274  LOAD_FAST                '_video_depth_old'

 L. 589      1276  LOAD_FAST                '_video_height_new'

 L. 590      1278  LOAD_FAST                '_video_width_new'

 L. 591      1280  LOAD_FAST                '_video_depth_new'
             1282  LOAD_CONST               ('video_height', 'video_width', 'video_depth', 'video_height_new', 'video_width_new', 'video_depth_new')
             1284  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1286  LOAD_FAST                '_dict'
             1288  LOAD_FAST                'f'
             1290  STORE_SUBSCR     
         1292_1294  JUMP_BACK          1170  'to 1170'
             1296  POP_BLOCK        
           1298_0  COME_FROM_LOOP     1164  '1164'

 L. 593      1298  LOAD_GLOBAL              ml_cnn3d
             1300  LOAD_ATTR                predictionFrom3DCNNClassifier
             1302  LOAD_FAST                '_dict'

 L. 594      1304  LOAD_FAST                'self'
             1306  LOAD_ATTR                modelpath

 L. 595      1308  LOAD_FAST                'self'
             1310  LOAD_ATTR                modelname

 L. 596      1312  LOAD_FAST                '_batch'

 L. 597      1314  LOAD_CONST               True
             1316  LOAD_CONST               ('cnn3dpath', 'cnn3dname', 'batchsize', 'verbose')
             1318  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1320  LOAD_FAST                '_result'
             1322  LOAD_FAST                'idxlist'
             1324  LOAD_CONST               0
             1326  LOAD_CONST               1
             1328  BUILD_SLICE_2         2 
             1330  BUILD_TUPLE_2         2 
             1332  STORE_SUBSCR     

 L. 600      1334  LOAD_FAST                '_pgsdlg'
             1336  LOAD_METHOD              setValue
             1338  LOAD_FAST                'i'
             1340  LOAD_CONST               1
             1342  BINARY_ADD       
             1344  CALL_METHOD_1         1  '1 positional argument'
             1346  POP_TOP          
         1348_1350  JUMP_BACK          1028  'to 1028'
             1352  POP_BLOCK        
           1354_0  COME_FROM_LOOP     1016  '1016'

 L. 602      1354  LOAD_GLOBAL              print
             1356  LOAD_STR                 'Done'
             1358  CALL_FUNCTION_1       1  '1 positional argument'
             1360  POP_TOP          

 L. 603      1362  LOAD_GLOBAL              np
             1364  LOAD_METHOD              transpose
             1366  LOAD_GLOBAL              np
             1368  LOAD_METHOD              reshape
             1370  LOAD_FAST                '_result'

 L. 604      1372  LOAD_FAST                'self'
             1374  LOAD_ATTR                survinfo
             1376  LOAD_STR                 'ILNum'
             1378  BINARY_SUBSCR    
             1380  LOAD_FAST                'self'
             1382  LOAD_ATTR                survinfo
             1384  LOAD_STR                 'XLNum'
             1386  BINARY_SUBSCR    

 L. 605      1388  LOAD_FAST                'self'
             1390  LOAD_ATTR                survinfo
             1392  LOAD_STR                 'ZNum'
             1394  BINARY_SUBSCR    
             1396  BUILD_LIST_3          3 
             1398  CALL_METHOD_2         2  '2 positional arguments'

 L. 606      1400  LOAD_CONST               2
             1402  LOAD_CONST               1
             1404  LOAD_CONST               0
             1406  BUILD_LIST_3          3 
             1408  CALL_METHOD_2         2  '2 positional arguments'
             1410  LOAD_FAST                'self'
             1412  LOAD_ATTR                seisdata
             1414  LOAD_FAST                'self'
             1416  LOAD_ATTR                ldtsave
             1418  LOAD_METHOD              text
             1420  CALL_METHOD_0         0  '0 positional arguments'
             1422  STORE_SUBSCR     

 L. 608      1424  LOAD_GLOBAL              QtWidgets
             1426  LOAD_ATTR                QMessageBox
             1428  LOAD_METHOD              information
             1430  LOAD_FAST                'self'
             1432  LOAD_ATTR                msgbox

 L. 609      1434  LOAD_STR                 'Apply 3D-CNN'

 L. 610      1436  LOAD_STR                 'CNN applied successfully'
             1438  CALL_METHOD_3         3  '3 positional arguments'
             1440  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 1438

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
    ApplyMl3DCnn4Pred = QtWidgets.QWidget()
    gui = applyml3dcnn4pred()
    gui.setupGUI(ApplyMl3DCnn4Pred)
    ApplyMl3DCnn4Pred.show()
    sys.exit(app.exec_())