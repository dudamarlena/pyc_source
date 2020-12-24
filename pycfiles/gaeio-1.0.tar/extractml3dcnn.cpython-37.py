# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\extractml3dcnn.py
# Compiled at: 2019-12-16 00:14:21
# Size of source mod 2**32: 36194 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.video as basic_video
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.cnnclassifier3d as ml_cnn3d
import cognitivegeo.src.gui.viewml3dcnn as gui_viewml3dcnn
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class extractml3dcnn(object):
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

    def setupGUI(self, ExtractMl3DCnn):
        ExtractMl3DCnn.setObjectName('ExtractMl3DCnn')
        ExtractMl3DCnn.setFixedSize(800, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/retrieve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ExtractMl3DCnn.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ExtractMl3DCnn)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ExtractMl3DCnn)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lbloldsize = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 180, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 180, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 180, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 220, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 220, 40, 30))
        self.lblolddepth = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblolddepth.setObjectName('lblolddepth')
        self.lblolddepth.setGeometry(QtCore.QRect(100, 260, 50, 30))
        self.ldtolddepth = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtolddepth.setObjectName('ldtolddepth')
        self.ldtolddepth.setGeometry(QtCore.QRect(150, 260, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 180, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 180, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 180, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 220, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 220, 40, 30))
        self.lblnewdepth = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblnewdepth.setObjectName('lblnewdepth')
        self.lblnewdepth.setGeometry(QtCore.QRect(300, 260, 50, 30))
        self.ldtnewdepth = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtnewdepth.setObjectName('ldtnewdepth')
        self.ldtnewdepth.setGeometry(QtCore.QRect(350, 260, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ExtractMl3DCnn)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ExtractMl3DCnn)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 130))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(ExtractMl3DCnn)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 140, 180, 130))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblmaskdepth = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblmaskdepth.setObjectName('lblmaskdepth')
        self.lblmaskdepth.setGeometry(QtCore.QRect(500, 360, 50, 30))
        self.ldtmaskdepth = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtmaskdepth.setObjectName('ldtmaskdepth')
        self.ldtmaskdepth.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.lblpooldepth = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblpooldepth.setObjectName('lblpooldepth')
        self.lblpooldepth.setGeometry(QtCore.QRect(700, 360, 50, 30))
        self.ldtpooldepth = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtpooldepth.setObjectName('ldtpooldepth')
        self.ldtpooldepth.setGeometry(QtCore.QRect(750, 360, 40, 30))
        self.lblpara = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lbltype = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lbltype.setObjectName('lbltype')
        self.lbltype.setGeometry(QtCore.QRect(10, 400, 130, 30))
        self.cbbtype = QtWidgets.QComboBox(ExtractMl3DCnn)
        self.cbbtype.setObjectName('cbbtype')
        self.cbbtype.setGeometry(QtCore.QRect(150, 400, 240, 30))
        self.lblsave = QtWidgets.QLabel(ExtractMl3DCnn)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExtractMl3DCnn)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(150, 440, 100, 30))
        self.btnapply = QtWidgets.QPushButton(ExtractMl3DCnn)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/retrieve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ExtractMl3DCnn)
        self.msgbox.setObjectName('msgbox')
        _center_x = ExtractMl3DCnn.geometry().center().x()
        _center_y = ExtractMl3DCnn.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ExtractMl3DCnn)
        QtCore.QMetaObject.connectSlotsByName(ExtractMl3DCnn)

    def retranslateGUI(self, ExtractMl3DCnn):
        self.dialog = ExtractMl3DCnn
        _translate = QtCore.QCoreApplication.translate
        ExtractMl3DCnn.setWindowTitle(_translate('ExtractMl3DCnn', 'Extract 3D-CNN'))
        self.lblfrom.setText(_translate('ExtractMl3DCnn', 'Select network:'))
        self.ldtfrom.setText(_translate('ExtractMl3DCnn', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ExtractMl3DCnn', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ExtractMl3DCnn', 'Training features:'))
        self.lbloldsize.setText(_translate('ExtractMl3DCnn', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('ExtractMl3DCnn', 'height=\ntime/depth'))
        self.ldtoldheight.setText(_translate('ExtractMl3DCnn', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('ExtractMl3DCnn', 'width=\ncrossline'))
        self.ldtoldwidth.setText(_translate('ExtractMl3DCnn', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblolddepth.setText(_translate('ExtractMl3DCnn', 'depth=\ninline'))
        self.ldtolddepth.setText(_translate('ExtractMl3DCnn', ''))
        self.ldtolddepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('ExtractMl3DCnn', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('ExtractMl3DCnn', 'height='))
        self.ldtnewheight.setText(_translate('ExtractMl3DCnn', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewheight.setEnabled(False)
        self.lblnewwidth.setText(_translate('ExtractMl3DCnn', 'width='))
        self.ldtnewwidth.setText(_translate('ExtractMl3DCnn', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnewwidth.setEnabled(False)
        self.lblnewdepth.setText(_translate('ExtractMl3DCnn', 'depth='))
        self.ldtnewdepth.setText(_translate('ExtractMl3DCnn', ''))
        self.ldtnewdepth.setEnabled(False)
        self.ldtnewdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('ExtractMl3DCnn', 'Pre-trained CNN architecture:'))
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
        self.lblmasksize.setText(_translate('ExtractMl3DCnn', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ExtractMl3DCnn', 'height='))
        self.ldtmaskheight.setText(_translate('ExtractMl3DCnn', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ExtractMl3DCnn', 'width='))
        self.ldtmaskwidth.setText(_translate('ExtractMl3DCnn', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskdepth.setText(_translate('ExtractMl3DCnn', 'depth='))
        self.ldtmaskdepth.setText(_translate('ExtractMl3DCnn', ''))
        self.ldtmaskdepth.setEnabled(False)
        self.ldtmaskdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ExtractMl3DCnn', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ExtractMl3DCnn', 'height='))
        self.ldtpoolheight.setText(_translate('ExtractMl3DCnn', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ExtractMl3DCnn', 'width='))
        self.ldtpoolwidth.setText(_translate('ExtractMl3DCnn', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpooldepth.setText(_translate('ExtractMl3DCnn', 'depth='))
        self.ldtpooldepth.setText(_translate('ExtractMl3DCnn', ''))
        self.ldtpooldepth.setEnabled(False)
        self.ldtpooldepth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ExtractMl3DCnn', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ExtractMl3DCnn', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ExtractMl3DCnn', '5000'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltype.setText(_translate('ExtractMl3DCnn', 'Target layer='))
        self.lbltype.setAlignment(QtCore.Qt.AlignRight)
        self.lblsave.setText(_translate('ExtractMl3DCnn', 'Output prefix='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ExtractMl3DCnn', 'feature_'))
        self.btnapply.setText(_translate('ExtractMl3DCnn', 'Extract 3D-CNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnExtractMl3DCnn)

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
            self.cbbtype.clear()

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

    def clickBtnExtractMl3DCnn--- This code section failed: ---

 L. 484         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 486         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 487        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in ExtractMl3DCnn: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 488        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 489        44  LOAD_STR                 'Extract 3D-CNN'

 L. 490        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 491        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 493        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              check3DCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 494        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in ExtractMl3DCnn: No CNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 495        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 496       100  LOAD_STR                 'Extract 3D-CNN'

 L. 497       102  LOAD_STR                 'No CNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 498       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 499       112  LOAD_FAST                'self'
              114  LOAD_ATTR                modelinfo
              116  LOAD_STR                 'feature_list'
              118  BINARY_SUBSCR    
              120  STORE_FAST               '_featurelist'

 L. 500       122  SETUP_LOOP          198  'to 198'
              124  LOAD_FAST                '_featurelist'
              126  GET_ITER         
            128_0  COME_FROM           144  '144'
              128  FOR_ITER            196  'to 196'
              130  STORE_FAST               'f'

 L. 501       132  LOAD_FAST                'self'
              134  LOAD_METHOD              checkSeisData
              136  LOAD_FAST                'f'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_CONST               False
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   128  'to 128'

 L. 502       146  LOAD_GLOBAL              vis_msg
              148  LOAD_ATTR                print
              150  LOAD_STR                 "ERROR in ExtractMl3DCnn: Feature '%s' not found in seismic data"
              152  LOAD_FAST                'f'
              154  BINARY_MODULO    

 L. 503       156  LOAD_STR                 'error'
              158  LOAD_CONST               ('type',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  POP_TOP          

 L. 504       164  LOAD_GLOBAL              QtWidgets
              166  LOAD_ATTR                QMessageBox
              168  LOAD_METHOD              critical
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                msgbox

 L. 505       174  LOAD_STR                 'Extract 3D-CNN'

 L. 506       176  LOAD_STR                 "Feature '"
              178  LOAD_FAST                'f'
              180  BINARY_ADD       
              182  LOAD_STR                 "' not found in seismic data"
              184  BINARY_ADD       
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 507       190  LOAD_CONST               None
              192  RETURN_VALUE     
              194  JUMP_BACK           128  'to 128'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      122  '122'

 L. 509       198  LOAD_GLOBAL              basic_data
              200  LOAD_METHOD              str2int
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                ldtoldheight
              206  LOAD_METHOD              text
              208  CALL_METHOD_0         0  '0 positional arguments'
              210  CALL_METHOD_1         1  '1 positional argument'
              212  STORE_FAST               '_video_height_old'

 L. 510       214  LOAD_GLOBAL              basic_data
              216  LOAD_METHOD              str2int
              218  LOAD_FAST                'self'
              220  LOAD_ATTR                ldtoldwidth
              222  LOAD_METHOD              text
              224  CALL_METHOD_0         0  '0 positional arguments'
              226  CALL_METHOD_1         1  '1 positional argument'
              228  STORE_FAST               '_video_width_old'

 L. 511       230  LOAD_GLOBAL              basic_data
              232  LOAD_METHOD              str2int
              234  LOAD_FAST                'self'
              236  LOAD_ATTR                ldtolddepth
              238  LOAD_METHOD              text
              240  CALL_METHOD_0         0  '0 positional arguments'
              242  CALL_METHOD_1         1  '1 positional argument'
              244  STORE_FAST               '_video_depth_old'

 L. 512       246  LOAD_GLOBAL              basic_data
              248  LOAD_METHOD              str2int
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                ldtnewheight
              254  LOAD_METHOD              text
              256  CALL_METHOD_0         0  '0 positional arguments'
              258  CALL_METHOD_1         1  '1 positional argument'
              260  STORE_FAST               '_video_height_new'

 L. 513       262  LOAD_GLOBAL              basic_data
              264  LOAD_METHOD              str2int
              266  LOAD_FAST                'self'
              268  LOAD_ATTR                ldtnewwidth
              270  LOAD_METHOD              text
              272  CALL_METHOD_0         0  '0 positional arguments'
              274  CALL_METHOD_1         1  '1 positional argument'
              276  STORE_FAST               '_video_width_new'

 L. 514       278  LOAD_GLOBAL              basic_data
              280  LOAD_METHOD              str2int
              282  LOAD_FAST                'self'
              284  LOAD_ATTR                ldtnewdepth
              286  LOAD_METHOD              text
              288  CALL_METHOD_0         0  '0 positional arguments'
              290  CALL_METHOD_1         1  '1 positional argument'
              292  STORE_FAST               '_video_depth_new'

 L. 515       294  LOAD_FAST                '_video_height_old'
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

 L. 516       324  LOAD_FAST                '_video_height_new'
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

 L. 517       354  LOAD_GLOBAL              vis_msg
              356  LOAD_ATTR                print
              358  LOAD_STR                 'ERROR in ExtractMl3DCnn: Non-integer feature size'
              360  LOAD_STR                 'error'
              362  LOAD_CONST               ('type',)
              364  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              366  POP_TOP          

 L. 518       368  LOAD_GLOBAL              QtWidgets
              370  LOAD_ATTR                QMessageBox
              372  LOAD_METHOD              critical
              374  LOAD_FAST                'self'
              376  LOAD_ATTR                msgbox

 L. 519       378  LOAD_STR                 'Extract 3D-CNN'

 L. 520       380  LOAD_STR                 'Non-integer feature size'
              382  CALL_METHOD_3         3  '3 positional arguments'
              384  POP_TOP          

 L. 521       386  LOAD_CONST               None
              388  RETURN_VALUE     
            390_0  COME_FROM           350  '350'

 L. 522       390  LOAD_FAST                '_video_height_old'
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

 L. 523       420  LOAD_FAST                '_video_height_new'
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

 L. 524       450  LOAD_GLOBAL              vis_msg
              452  LOAD_ATTR                print
              454  LOAD_STR                 'ERROR in ExtractMl2DCnn: Features are not 3D '
              456  LOAD_STR                 'error'
              458  LOAD_CONST               ('type',)
              460  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              462  POP_TOP          

 L. 525       464  LOAD_GLOBAL              QtWidgets
              466  LOAD_ATTR                QMessageBox
              468  LOAD_METHOD              critical
              470  LOAD_FAST                'self'
              472  LOAD_ATTR                msgbox

 L. 526       474  LOAD_STR                 'Extract 2D-CNN'

 L. 527       476  LOAD_STR                 'Features are not 3D '
              478  CALL_METHOD_3         3  '3 positional arguments'
              480  POP_TOP          

 L. 528       482  LOAD_CONST               None
              484  RETURN_VALUE     
            486_0  COME_FROM           446  '446'

 L. 530       486  LOAD_GLOBAL              basic_data
              488  LOAD_METHOD              str2int
              490  LOAD_FAST                'self'
              492  LOAD_ATTR                ldtbatchsize
              494  LOAD_METHOD              text
              496  CALL_METHOD_0         0  '0 positional arguments'
              498  CALL_METHOD_1         1  '1 positional argument'
              500  STORE_FAST               '_batch'

 L. 531       502  LOAD_FAST                '_batch'
              504  LOAD_CONST               False
              506  COMPARE_OP               is
          508_510  POP_JUMP_IF_TRUE    522  'to 522'
              512  LOAD_FAST                '_batch'
              514  LOAD_CONST               1
              516  COMPARE_OP               <
          518_520  POP_JUMP_IF_FALSE   558  'to 558'
            522_0  COME_FROM           508  '508'

 L. 532       522  LOAD_GLOBAL              vis_msg
              524  LOAD_ATTR                print
              526  LOAD_STR                 'ERROR in ExtractMl3DCnn: Non-positive batch size'
              528  LOAD_STR                 'error'
              530  LOAD_CONST               ('type',)
              532  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              534  POP_TOP          

 L. 533       536  LOAD_GLOBAL              QtWidgets
              538  LOAD_ATTR                QMessageBox
              540  LOAD_METHOD              critical
              542  LOAD_FAST                'self'
              544  LOAD_ATTR                msgbox

 L. 534       546  LOAD_STR                 'Extract 3D-CNN'

 L. 535       548  LOAD_STR                 'Non-positive batch size'
              550  CALL_METHOD_3         3  '3 positional arguments'
              552  POP_TOP          

 L. 536       554  LOAD_CONST               None
              556  RETURN_VALUE     
            558_0  COME_FROM           518  '518'

 L. 538       558  LOAD_GLOBAL              len
              560  LOAD_FAST                'self'
              562  LOAD_ATTR                ldtsave
              564  LOAD_METHOD              text
              566  CALL_METHOD_0         0  '0 positional arguments'
              568  CALL_FUNCTION_1       1  '1 positional argument'
              570  LOAD_CONST               1
              572  COMPARE_OP               <
          574_576  POP_JUMP_IF_FALSE   614  'to 614'

 L. 539       578  LOAD_GLOBAL              vis_msg
              580  LOAD_ATTR                print
              582  LOAD_STR                 'ERROR in ExtractMl3DCnn: No prefix specified'
              584  LOAD_STR                 'error'
              586  LOAD_CONST               ('type',)
              588  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              590  POP_TOP          

 L. 540       592  LOAD_GLOBAL              QtWidgets
              594  LOAD_ATTR                QMessageBox
              596  LOAD_METHOD              critical
              598  LOAD_FAST                'self'
              600  LOAD_ATTR                msgbox

 L. 541       602  LOAD_STR                 'Extract 3D-CNN'

 L. 542       604  LOAD_STR                 'No prefix specified'
              606  CALL_METHOD_3         3  '3 positional arguments'
              608  POP_TOP          

 L. 543       610  LOAD_CONST               None
              612  RETURN_VALUE     
            614_0  COME_FROM           574  '574'

 L. 544       614  LOAD_FAST                'self'
              616  LOAD_ATTR                ldtsave
              618  LOAD_METHOD              text
              620  CALL_METHOD_0         0  '0 positional arguments'
              622  LOAD_STR                 '1'
              624  BINARY_ADD       
              626  LOAD_FAST                'self'
              628  LOAD_ATTR                seisdata
              630  LOAD_METHOD              keys
              632  CALL_METHOD_0         0  '0 positional arguments'
              634  COMPARE_OP               in
          636_638  POP_JUMP_IF_FALSE   732  'to 732'

 L. 545       640  LOAD_FAST                'self'
              642  LOAD_METHOD              checkSeisData
              644  LOAD_FAST                'self'
              646  LOAD_ATTR                ldtsave
              648  LOAD_METHOD              text
              650  CALL_METHOD_0         0  '0 positional arguments'
              652  LOAD_STR                 '1'
              654  BINARY_ADD       
              656  CALL_METHOD_1         1  '1 positional argument'
          658_660  POP_JUMP_IF_FALSE   732  'to 732'

 L. 546       662  LOAD_GLOBAL              QtWidgets
              664  LOAD_ATTR                QMessageBox
              666  LOAD_METHOD              question
              668  LOAD_FAST                'self'
              670  LOAD_ATTR                msgbox
              672  LOAD_STR                 'Extract 3D-CNN'

 L. 547       674  LOAD_STR                 'Prefix '
              676  LOAD_FAST                'self'
              678  LOAD_ATTR                ldtsave
              680  LOAD_METHOD              text
              682  CALL_METHOD_0         0  '0 positional arguments'
              684  BINARY_ADD       
              686  LOAD_STR                 ' already exists. Overwrite?'
              688  BINARY_ADD       

 L. 548       690  LOAD_GLOBAL              QtWidgets
              692  LOAD_ATTR                QMessageBox
              694  LOAD_ATTR                Yes
              696  LOAD_GLOBAL              QtWidgets
              698  LOAD_ATTR                QMessageBox
              700  LOAD_ATTR                No
              702  BINARY_OR        

 L. 549       704  LOAD_GLOBAL              QtWidgets
              706  LOAD_ATTR                QMessageBox
              708  LOAD_ATTR                No
              710  CALL_METHOD_5         5  '5 positional arguments'
              712  STORE_FAST               'reply'

 L. 551       714  LOAD_FAST                'reply'
              716  LOAD_GLOBAL              QtWidgets
              718  LOAD_ATTR                QMessageBox
              720  LOAD_ATTR                No
              722  COMPARE_OP               ==
          724_726  POP_JUMP_IF_FALSE   732  'to 732'

 L. 552       728  LOAD_CONST               None
              730  RETURN_VALUE     
            732_0  COME_FROM           724  '724'
            732_1  COME_FROM           658  '658'
            732_2  COME_FROM           636  '636'

 L. 554       732  LOAD_CONST               2
              734  LOAD_GLOBAL              int
              736  LOAD_FAST                '_video_height_old'
              738  LOAD_CONST               2
              740  BINARY_TRUE_DIVIDE
              742  CALL_FUNCTION_1       1  '1 positional argument'
              744  BINARY_MULTIPLY  
              746  LOAD_CONST               1
              748  BINARY_ADD       
              750  STORE_FAST               '_video_height_old'

 L. 555       752  LOAD_CONST               2
              754  LOAD_GLOBAL              int
              756  LOAD_FAST                '_video_width_old'
              758  LOAD_CONST               2
              760  BINARY_TRUE_DIVIDE
              762  CALL_FUNCTION_1       1  '1 positional argument'
              764  BINARY_MULTIPLY  
              766  LOAD_CONST               1
              768  BINARY_ADD       
              770  STORE_FAST               '_video_width_old'

 L. 556       772  LOAD_CONST               2
              774  LOAD_GLOBAL              int
              776  LOAD_FAST                '_video_depth_old'
              778  LOAD_CONST               2
              780  BINARY_TRUE_DIVIDE
              782  CALL_FUNCTION_1       1  '1 positional argument'
              784  BINARY_MULTIPLY  
              786  LOAD_CONST               1
              788  BINARY_ADD       
              790  STORE_FAST               '_video_depth_old'

 L. 558       792  LOAD_GLOBAL              np
              794  LOAD_METHOD              shape
              796  LOAD_FAST                'self'
              798  LOAD_ATTR                seisdata
              800  LOAD_FAST                '_featurelist'
              802  LOAD_CONST               0
              804  BINARY_SUBSCR    
              806  BINARY_SUBSCR    
              808  CALL_METHOD_1         1  '1 positional argument'
              810  LOAD_CONST               0
              812  BINARY_SUBSCR    
              814  STORE_FAST               '_nsample'

 L. 560       816  LOAD_GLOBAL              int
              818  LOAD_GLOBAL              np
              820  LOAD_METHOD              ceil
              822  LOAD_FAST                '_nsample'
              824  LOAD_FAST                '_batch'
              826  BINARY_TRUE_DIVIDE
              828  CALL_METHOD_1         1  '1 positional argument'
              830  CALL_FUNCTION_1       1  '1 positional argument'
              832  STORE_FAST               '_nloop'

 L. 563       834  LOAD_GLOBAL              QtWidgets
              836  LOAD_METHOD              QProgressDialog
              838  CALL_METHOD_0         0  '0 positional arguments'
              840  STORE_FAST               '_pgsdlg'

 L. 564       842  LOAD_GLOBAL              QtGui
              844  LOAD_METHOD              QIcon
              846  CALL_METHOD_0         0  '0 positional arguments'
              848  STORE_FAST               'icon'

 L. 565       850  LOAD_FAST                'icon'
              852  LOAD_METHOD              addPixmap
              854  LOAD_GLOBAL              QtGui
              856  LOAD_METHOD              QPixmap
              858  LOAD_GLOBAL              os
              860  LOAD_ATTR                path
              862  LOAD_METHOD              join
              864  LOAD_FAST                'self'
              866  LOAD_ATTR                iconpath
              868  LOAD_STR                 'icons/retrieve.png'
              870  CALL_METHOD_2         2  '2 positional arguments'
              872  CALL_METHOD_1         1  '1 positional argument'

 L. 566       874  LOAD_GLOBAL              QtGui
              876  LOAD_ATTR                QIcon
              878  LOAD_ATTR                Normal
              880  LOAD_GLOBAL              QtGui
              882  LOAD_ATTR                QIcon
              884  LOAD_ATTR                Off
              886  CALL_METHOD_3         3  '3 positional arguments'
              888  POP_TOP          

 L. 567       890  LOAD_FAST                '_pgsdlg'
              892  LOAD_METHOD              setWindowIcon
              894  LOAD_FAST                'icon'
              896  CALL_METHOD_1         1  '1 positional argument'
              898  POP_TOP          

 L. 568       900  LOAD_FAST                '_pgsdlg'
              902  LOAD_METHOD              setWindowTitle
              904  LOAD_STR                 'Extract 3D-CNN'
              906  CALL_METHOD_1         1  '1 positional argument'
              908  POP_TOP          

 L. 569       910  LOAD_FAST                '_pgsdlg'
              912  LOAD_METHOD              setCancelButton
              914  LOAD_CONST               None
              916  CALL_METHOD_1         1  '1 positional argument'
              918  POP_TOP          

 L. 570       920  LOAD_FAST                '_pgsdlg'
              922  LOAD_METHOD              setWindowFlags
              924  LOAD_GLOBAL              QtCore
              926  LOAD_ATTR                Qt
              928  LOAD_ATTR                WindowStaysOnTopHint
              930  CALL_METHOD_1         1  '1 positional argument'
              932  POP_TOP          

 L. 571       934  LOAD_FAST                '_pgsdlg'
              936  LOAD_METHOD              forceShow
              938  CALL_METHOD_0         0  '0 positional arguments'
              940  POP_TOP          

 L. 572       942  LOAD_FAST                '_pgsdlg'
              944  LOAD_METHOD              setFixedWidth
              946  LOAD_CONST               400
              948  CALL_METHOD_1         1  '1 positional argument'
              950  POP_TOP          

 L. 573       952  LOAD_FAST                '_pgsdlg'
              954  LOAD_METHOD              setMaximum
              956  LOAD_FAST                '_nloop'
              958  CALL_METHOD_1         1  '1 positional argument'
              960  POP_TOP          

 L. 575       962  LOAD_GLOBAL              int
              964  LOAD_FAST                '_video_depth_old'
              966  LOAD_CONST               2
              968  BINARY_TRUE_DIVIDE
              970  CALL_FUNCTION_1       1  '1 positional argument'
              972  STORE_FAST               '_wdinl'

 L. 576       974  LOAD_GLOBAL              int
              976  LOAD_FAST                '_video_width_old'
              978  LOAD_CONST               2
              980  BINARY_TRUE_DIVIDE
              982  CALL_FUNCTION_1       1  '1 positional argument'
              984  STORE_FAST               '_wdxl'

 L. 577       986  LOAD_GLOBAL              int
              988  LOAD_FAST                '_video_height_old'
              990  LOAD_CONST               2
              992  BINARY_TRUE_DIVIDE
              994  CALL_FUNCTION_1       1  '1 positional argument'
              996  STORE_FAST               '_wdz'

 L. 579       998  LOAD_GLOBAL              seis_ays
             1000  LOAD_METHOD              convertSeisInfoTo2DMat
             1002  LOAD_FAST                'self'
             1004  LOAD_ATTR                survinfo
             1006  CALL_METHOD_1         1  '1 positional argument'
             1008  STORE_FAST               '_seisdata'

 L. 581      1010  LOAD_GLOBAL              np
             1012  LOAD_METHOD              load
             1014  LOAD_GLOBAL              os
             1016  LOAD_ATTR                path
             1018  LOAD_METHOD              join
             1020  LOAD_FAST                'self'
             1022  LOAD_ATTR                modelpath
             1024  LOAD_FAST                'self'
             1026  LOAD_ATTR                modelname
             1028  LOAD_STR                 '_modelinfo.npy'
             1030  BINARY_ADD       
             1032  CALL_METHOD_2         2  '2 positional arguments'
             1034  CALL_METHOD_1         1  '1 positional argument'
             1036  LOAD_METHOD              item
             1038  CALL_METHOD_0         0  '0 positional arguments'
             1040  STORE_FAST               '_modelinfo'

 L. 582      1042  LOAD_FAST                '_modelinfo'
             1044  LOAD_STR                 'number_conv_block'
             1046  BINARY_SUBSCR    
             1048  STORE_FAST               '_nblock'

 L. 583      1050  LOAD_FAST                '_modelinfo'
             1052  LOAD_STR                 'number_conv_layer'
             1054  BINARY_SUBSCR    
             1056  STORE_FAST               '_nlayer'

 L. 584      1058  LOAD_FAST                '_modelinfo'
             1060  LOAD_STR                 'number_conv_feature'
             1062  BINARY_SUBSCR    
             1064  STORE_FAST               '_nfeature'

 L. 586      1066  LOAD_FAST                'self'
             1068  LOAD_ATTR                cbbtype
             1070  LOAD_METHOD              currentIndex
             1072  CALL_METHOD_0         0  '0 positional arguments'
             1074  STORE_FAST               '_featureidx'

 L. 587      1076  LOAD_CONST               0
             1078  STORE_FAST               '_blockidx'

 L. 588      1080  LOAD_CONST               0
             1082  STORE_FAST               '_layeridx'

 L. 589      1084  SETUP_LOOP         1160  'to 1160'
             1086  LOAD_GLOBAL              range
             1088  LOAD_FAST                '_nblock'
             1090  CALL_FUNCTION_1       1  '1 positional argument'
             1092  GET_ITER         
           1094_0  COME_FROM          1124  '1124'
             1094  FOR_ITER           1158  'to 1158'
             1096  STORE_FAST               'i'

 L. 590      1098  LOAD_GLOBAL              sum
             1100  LOAD_FAST                '_nlayer'
             1102  LOAD_CONST               0
             1104  LOAD_FAST                'i'
             1106  LOAD_CONST               1
             1108  BINARY_ADD       
             1110  BUILD_SLICE_2         2 
             1112  BINARY_SUBSCR    
             1114  CALL_FUNCTION_1       1  '1 positional argument'
             1116  LOAD_FAST                '_featureidx'
             1118  LOAD_CONST               1
             1120  BINARY_ADD       
             1122  COMPARE_OP               >=
         1124_1126  POP_JUMP_IF_FALSE  1094  'to 1094'

 L. 591      1128  LOAD_FAST                'i'
             1130  STORE_FAST               '_blockidx'

 L. 592      1132  LOAD_FAST                '_featureidx'
             1134  LOAD_GLOBAL              sum
             1136  LOAD_FAST                '_nlayer'
             1138  LOAD_CONST               0
             1140  LOAD_FAST                'i'
             1142  BUILD_SLICE_2         2 
             1144  BINARY_SUBSCR    
             1146  CALL_FUNCTION_1       1  '1 positional argument'
             1148  BINARY_SUBTRACT  
             1150  STORE_FAST               '_layeridx'

 L. 593      1152  BREAK_LOOP       
         1154_1156  JUMP_BACK          1094  'to 1094'
             1158  POP_BLOCK        
           1160_0  COME_FROM_LOOP     1084  '1084'

 L. 595      1160  LOAD_FAST                '_nfeature'
             1162  LOAD_FAST                '_blockidx'
             1164  BINARY_SUBSCR    
             1166  STORE_FAST               '_nfeature'

 L. 596      1168  LOAD_GLOBAL              np
             1170  LOAD_METHOD              zeros
             1172  LOAD_FAST                '_nsample'
             1174  LOAD_FAST                '_nfeature'
             1176  BUILD_LIST_2          2 
             1178  CALL_METHOD_1         1  '1 positional argument'
             1180  STORE_FAST               '_result'

 L. 597      1182  LOAD_CONST               0
             1184  STORE_FAST               'idxstart'

 L. 598  1186_1188  SETUP_LOOP         1540  'to 1540'
             1190  LOAD_GLOBAL              range
             1192  LOAD_FAST                '_nloop'
             1194  CALL_FUNCTION_1       1  '1 positional argument'
             1196  GET_ITER         
         1198_1200  FOR_ITER           1538  'to 1538'
             1202  STORE_FAST               'i'

 L. 600      1204  LOAD_GLOBAL              QtCore
             1206  LOAD_ATTR                QCoreApplication
             1208  LOAD_METHOD              instance
             1210  CALL_METHOD_0         0  '0 positional arguments'
             1212  LOAD_METHOD              processEvents
             1214  CALL_METHOD_0         0  '0 positional arguments'
             1216  POP_TOP          

 L. 602      1218  LOAD_GLOBAL              sys
             1220  LOAD_ATTR                stdout
             1222  LOAD_METHOD              write

 L. 603      1224  LOAD_STR                 '\r>>> Extract 3D-CNN, proceeding %.1f%% '
             1226  LOAD_GLOBAL              float
             1228  LOAD_FAST                'i'
             1230  CALL_FUNCTION_1       1  '1 positional argument'
             1232  LOAD_GLOBAL              float
             1234  LOAD_FAST                '_nloop'
             1236  CALL_FUNCTION_1       1  '1 positional argument'
             1238  BINARY_TRUE_DIVIDE
             1240  LOAD_CONST               100.0
             1242  BINARY_MULTIPLY  
             1244  BINARY_MODULO    
             1246  CALL_METHOD_1         1  '1 positional argument'
             1248  POP_TOP          

 L. 604      1250  LOAD_GLOBAL              sys
             1252  LOAD_ATTR                stdout
             1254  LOAD_METHOD              flush
             1256  CALL_METHOD_0         0  '0 positional arguments'
             1258  POP_TOP          

 L. 606      1260  LOAD_FAST                'idxstart'
             1262  LOAD_FAST                '_batch'
             1264  BINARY_ADD       
             1266  STORE_FAST               'idxend'

 L. 607      1268  LOAD_FAST                'idxend'
             1270  LOAD_FAST                '_nsample'
             1272  COMPARE_OP               >
         1274_1276  POP_JUMP_IF_FALSE  1282  'to 1282'

 L. 608      1278  LOAD_FAST                '_nsample'
             1280  STORE_FAST               'idxend'
           1282_0  COME_FROM          1274  '1274'

 L. 609      1282  LOAD_GLOBAL              np
             1284  LOAD_METHOD              linspace
             1286  LOAD_FAST                'idxstart'
             1288  LOAD_FAST                'idxend'
             1290  LOAD_CONST               1
             1292  BINARY_SUBTRACT  
             1294  LOAD_FAST                'idxend'
             1296  LOAD_FAST                'idxstart'
             1298  BINARY_SUBTRACT  
             1300  CALL_METHOD_3         3  '3 positional arguments'
             1302  LOAD_METHOD              astype
             1304  LOAD_GLOBAL              int
             1306  CALL_METHOD_1         1  '1 positional argument'
             1308  STORE_FAST               'idxlist'

 L. 610      1310  LOAD_FAST                'idxend'
             1312  STORE_FAST               'idxstart'

 L. 611      1314  LOAD_GLOBAL              basic_mdt
             1316  LOAD_METHOD              retrieveDictByIndex
             1318  LOAD_FAST                'self'
             1320  LOAD_ATTR                seisdata
             1322  LOAD_FAST                'idxlist'
             1324  CALL_METHOD_2         2  '2 positional arguments'
             1326  STORE_FAST               '_dict'

 L. 613      1328  LOAD_FAST                '_seisdata'
             1330  LOAD_FAST                'idxlist'
             1332  LOAD_CONST               0
             1334  LOAD_CONST               3
             1336  BUILD_SLICE_2         2 
             1338  BUILD_TUPLE_2         2 
             1340  BINARY_SUBSCR    
             1342  STORE_FAST               '_targetdata'

 L. 615      1344  BUILD_MAP_0           0 
             1346  STORE_FAST               '_dict'

 L. 616      1348  SETUP_LOOP         1482  'to 1482'
             1350  LOAD_FAST                '_featurelist'
             1352  GET_ITER         
           1354_0  COME_FROM          1440  '1440'
             1354  FOR_ITER           1480  'to 1480'
             1356  STORE_FAST               'f'

 L. 617      1358  LOAD_FAST                'self'
             1360  LOAD_ATTR                seisdata
             1362  LOAD_FAST                'f'
             1364  BINARY_SUBSCR    
             1366  STORE_FAST               '_data'

 L. 618      1368  LOAD_GLOBAL              seis_ays
             1370  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1372  LOAD_FAST                '_data'
             1374  LOAD_FAST                '_targetdata'
             1376  LOAD_FAST                'self'
             1378  LOAD_ATTR                survinfo

 L. 619      1380  LOAD_FAST                '_wdinl'
             1382  LOAD_FAST                '_wdxl'
             1384  LOAD_FAST                '_wdz'

 L. 620      1386  LOAD_CONST               False
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

 L. 621      1414  LOAD_FAST                '_video_height_new'
             1416  LOAD_FAST                '_video_height_old'
             1418  COMPARE_OP               !=
         1420_1422  POP_JUMP_IF_TRUE   1444  'to 1444'

 L. 622      1424  LOAD_FAST                '_video_width_new'
             1426  LOAD_FAST                '_video_width_old'
             1428  COMPARE_OP               !=
         1430_1432  POP_JUMP_IF_TRUE   1444  'to 1444'

 L. 623      1434  LOAD_FAST                '_video_depth_new'
             1436  LOAD_FAST                '_video_depth_old'
             1438  COMPARE_OP               !=
         1440_1442  POP_JUMP_IF_FALSE  1354  'to 1354'
           1444_0  COME_FROM          1430  '1430'
           1444_1  COME_FROM          1420  '1420'

 L. 624      1444  LOAD_GLOBAL              basic_video
             1446  LOAD_ATTR                changeVideoSize
             1448  LOAD_FAST                '_dict'
             1450  LOAD_FAST                'f'
             1452  BINARY_SUBSCR    

 L. 625      1454  LOAD_FAST                '_video_height_old'

 L. 626      1456  LOAD_FAST                '_video_width_old'

 L. 627      1458  LOAD_FAST                '_video_depth_old'

 L. 628      1460  LOAD_FAST                '_video_height_new'

 L. 629      1462  LOAD_FAST                '_video_width_new'

 L. 630      1464  LOAD_FAST                '_video_depth_new'
             1466  LOAD_CONST               ('video_height', 'video_width', 'video_depth', 'video_height_new', 'video_width_new', 'video_depth_new')
             1468  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1470  LOAD_FAST                '_dict'
             1472  LOAD_FAST                'f'
             1474  STORE_SUBSCR     
         1476_1478  JUMP_BACK          1354  'to 1354'
             1480  POP_BLOCK        
           1482_0  COME_FROM_LOOP     1348  '1348'

 L. 632      1482  LOAD_GLOBAL              ml_cnn3d
             1484  LOAD_ATTR                extract3DCNNConvFeature
             1486  LOAD_FAST                '_dict'

 L. 633      1488  LOAD_FAST                'self'
             1490  LOAD_ATTR                modelpath

 L. 634      1492  LOAD_FAST                'self'
             1494  LOAD_ATTR                modelname

 L. 635      1496  LOAD_FAST                '_blockidx'

 L. 636      1498  LOAD_FAST                '_layeridx'

 L. 637      1500  LOAD_CONST               True
             1502  LOAD_CONST               ('cnn3dpath', 'cnn3dname', 'blockidx', 'layeridx', 'verbose')
             1504  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1506  LOAD_FAST                '_result'
             1508  LOAD_FAST                'idxlist'
             1510  LOAD_CONST               0
             1512  LOAD_FAST                '_nfeature'
             1514  BUILD_SLICE_2         2 
             1516  BUILD_TUPLE_2         2 
             1518  STORE_SUBSCR     

 L. 639      1520  LOAD_FAST                '_pgsdlg'
             1522  LOAD_METHOD              setValue
             1524  LOAD_FAST                'i'
             1526  LOAD_CONST               1
             1528  BINARY_ADD       
             1530  CALL_METHOD_1         1  '1 positional argument'
             1532  POP_TOP          
         1534_1536  JUMP_BACK          1198  'to 1198'
             1538  POP_BLOCK        
           1540_0  COME_FROM_LOOP     1186  '1186'

 L. 641      1540  LOAD_GLOBAL              print
             1542  LOAD_STR                 'Done'
             1544  CALL_FUNCTION_1       1  '1 positional argument'
             1546  POP_TOP          

 L. 642      1548  SETUP_LOOP         1662  'to 1662'
             1550  LOAD_GLOBAL              range
             1552  LOAD_FAST                '_nfeature'
             1554  CALL_FUNCTION_1       1  '1 positional argument'
             1556  GET_ITER         
             1558  FOR_ITER           1660  'to 1660'
             1560  STORE_FAST               'i'

 L. 643      1562  LOAD_GLOBAL              np
             1564  LOAD_METHOD              transpose
             1566  LOAD_GLOBAL              np
             1568  LOAD_METHOD              reshape
             1570  LOAD_FAST                '_result'
             1572  LOAD_CONST               None
             1574  LOAD_CONST               None
             1576  BUILD_SLICE_2         2 
             1578  LOAD_FAST                'i'
             1580  LOAD_FAST                'i'
             1582  LOAD_CONST               1
             1584  BINARY_ADD       
             1586  BUILD_SLICE_2         2 
             1588  BUILD_TUPLE_2         2 
             1590  BINARY_SUBSCR    

 L. 644      1592  LOAD_FAST                'self'
             1594  LOAD_ATTR                survinfo
             1596  LOAD_STR                 'ILNum'
             1598  BINARY_SUBSCR    

 L. 645      1600  LOAD_FAST                'self'
             1602  LOAD_ATTR                survinfo
             1604  LOAD_STR                 'XLNum'
             1606  BINARY_SUBSCR    

 L. 646      1608  LOAD_FAST                'self'
             1610  LOAD_ATTR                survinfo
             1612  LOAD_STR                 'ZNum'
             1614  BINARY_SUBSCR    
             1616  BUILD_LIST_3          3 
             1618  CALL_METHOD_2         2  '2 positional arguments'

 L. 647      1620  LOAD_CONST               2
             1622  LOAD_CONST               1
             1624  LOAD_CONST               0
             1626  BUILD_LIST_3          3 
             1628  CALL_METHOD_2         2  '2 positional arguments'
             1630  LOAD_FAST                'self'
             1632  LOAD_ATTR                seisdata
             1634  LOAD_FAST                'self'
             1636  LOAD_ATTR                ldtsave
             1638  LOAD_METHOD              text
             1640  CALL_METHOD_0         0  '0 positional arguments'
             1642  LOAD_GLOBAL              str
             1644  LOAD_FAST                'i'
             1646  LOAD_CONST               1
             1648  BINARY_ADD       
             1650  CALL_FUNCTION_1       1  '1 positional argument'
             1652  BINARY_ADD       
             1654  STORE_SUBSCR     
         1656_1658  JUMP_BACK          1558  'to 1558'
             1660  POP_BLOCK        
           1662_0  COME_FROM_LOOP     1548  '1548'

 L. 649      1662  LOAD_GLOBAL              QtWidgets
             1664  LOAD_ATTR                QMessageBox
             1666  LOAD_METHOD              information
             1668  LOAD_FAST                'self'
             1670  LOAD_ATTR                msgbox

 L. 650      1672  LOAD_STR                 'Extract 3D-CNN'

 L. 651      1674  LOAD_GLOBAL              str
             1676  LOAD_FAST                '_nfeature'
             1678  CALL_FUNCTION_1       1  '1 positional argument'
             1680  LOAD_STR                 ' CNN features extracted successfully'
             1682  BINARY_ADD       
             1684  CALL_METHOD_3         3  '3 positional arguments'
             1686  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 1684

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
    ExtractMl3DCnn = QtWidgets.QWidget()
    gui = extractml3dcnn()
    gui.setupGUI(ExtractMl3DCnn)
    ExtractMl3DCnn.show()
    sys.exit(app.exec_())