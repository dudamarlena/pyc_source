# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\evaluateml3dcnn.py
# Compiled at: 2019-12-15 21:49:29
# Size of source mod 2**32: 35417 bytes
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
import cognitivegeo.src.gui.viewmlconfmat as gui_viewmlconfmat
import cognitivegeo.src.gui.viewml3dcnn as gui_viewml3dcnn
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

    def clickBtnEvaluateMl3DCnn--- This code section failed: ---

 L. 464         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 466         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 467        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in EvaluateMl3DCnn: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 468        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 469        44  LOAD_STR                 'Evaluate 3D-CNN'

 L. 470        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 471        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 473        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              check3DCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 474        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in EvaluateMl3DCnn: No CNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 475        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 476       100  LOAD_STR                 'Evaluate 3D-CNN'

 L. 477       102  LOAD_STR                 'No CNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 478       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 480       112  LOAD_FAST                'self'
              114  LOAD_ATTR                modelinfo
              116  LOAD_STR                 'feature_list'
              118  BINARY_SUBSCR    
              120  STORE_FAST               '_featurelist'

 L. 481       122  SETUP_LOOP          198  'to 198'
              124  LOAD_FAST                '_featurelist'
              126  GET_ITER         
            128_0  COME_FROM           144  '144'
              128  FOR_ITER            196  'to 196'
              130  STORE_FAST               'f'

 L. 482       132  LOAD_FAST                'self'
              134  LOAD_METHOD              checkSeisData
              136  LOAD_FAST                'f'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  LOAD_CONST               False
              142  COMPARE_OP               is
              144  POP_JUMP_IF_FALSE   128  'to 128'

 L. 483       146  LOAD_GLOBAL              vis_msg
              148  LOAD_ATTR                print
              150  LOAD_STR                 "ERROR in EvaluateMl3DCnn: Feature '%s' not found in seismic data"
              152  LOAD_FAST                'f'
              154  BINARY_MODULO    

 L. 484       156  LOAD_STR                 'error'
              158  LOAD_CONST               ('type',)
              160  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              162  POP_TOP          

 L. 485       164  LOAD_GLOBAL              QtWidgets
              166  LOAD_ATTR                QMessageBox
              168  LOAD_METHOD              critical
              170  LOAD_FAST                'self'
              172  LOAD_ATTR                msgbox

 L. 486       174  LOAD_STR                 'Evaluate 3D-CNN'

 L. 487       176  LOAD_STR                 "Feature '"
              178  LOAD_FAST                'f'
              180  BINARY_ADD       
              182  LOAD_STR                 "' not found in seismic data"
              184  BINARY_ADD       
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 488       190  LOAD_CONST               None
              192  RETURN_VALUE     
              194  JUMP_BACK           128  'to 128'
              196  POP_BLOCK        
            198_0  COME_FROM_LOOP      122  '122'

 L. 490       198  LOAD_FAST                'self'
              200  LOAD_ATTR                modelinfo
              202  LOAD_STR                 'target'
              204  BINARY_SUBSCR    
              206  LOAD_FAST                'self'
              208  LOAD_ATTR                seisdata
              210  LOAD_METHOD              keys
              212  CALL_METHOD_0         0  '0 positional arguments'
              214  COMPARE_OP               not-in
          216_218  POP_JUMP_IF_FALSE   280  'to 280'

 L. 491       220  LOAD_GLOBAL              vis_msg
              222  LOAD_ATTR                print
              224  LOAD_STR                 "ERROR in EvauluateMlCnn: Target label '%s' not found in seismic data"

 L. 492       226  LOAD_FAST                'self'
              228  LOAD_ATTR                modelinfo
              230  LOAD_STR                 'target'
              232  BINARY_SUBSCR    
              234  BINARY_MODULO    
              236  LOAD_STR                 'error'
              238  LOAD_CONST               ('type',)
              240  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              242  POP_TOP          

 L. 493       244  LOAD_GLOBAL              QtWidgets
              246  LOAD_ATTR                QMessageBox
              248  LOAD_METHOD              critical
              250  LOAD_FAST                'self'
              252  LOAD_ATTR                msgbox

 L. 494       254  LOAD_STR                 'Evaluate 3D-CNN'

 L. 495       256  LOAD_STR                 "Target label '"
              258  LOAD_FAST                'self'
              260  LOAD_ATTR                modelinfo
              262  LOAD_STR                 'target'
              264  BINARY_SUBSCR    
              266  BINARY_ADD       
              268  LOAD_STR                 "' not found in seismic data"
              270  BINARY_ADD       
              272  CALL_METHOD_3         3  '3 positional arguments'
              274  POP_TOP          

 L. 496       276  LOAD_CONST               None
              278  RETURN_VALUE     
            280_0  COME_FROM           216  '216'

 L. 498       280  LOAD_GLOBAL              basic_data
              282  LOAD_METHOD              str2int
              284  LOAD_FAST                'self'
              286  LOAD_ATTR                ldtoldheight
              288  LOAD_METHOD              text
              290  CALL_METHOD_0         0  '0 positional arguments'
              292  CALL_METHOD_1         1  '1 positional argument'
              294  STORE_FAST               '_video_height_old'

 L. 499       296  LOAD_GLOBAL              basic_data
              298  LOAD_METHOD              str2int
              300  LOAD_FAST                'self'
              302  LOAD_ATTR                ldtoldwidth
              304  LOAD_METHOD              text
              306  CALL_METHOD_0         0  '0 positional arguments'
              308  CALL_METHOD_1         1  '1 positional argument'
              310  STORE_FAST               '_video_width_old'

 L. 500       312  LOAD_GLOBAL              basic_data
              314  LOAD_METHOD              str2int
              316  LOAD_FAST                'self'
              318  LOAD_ATTR                ldtolddepth
              320  LOAD_METHOD              text
              322  CALL_METHOD_0         0  '0 positional arguments'
              324  CALL_METHOD_1         1  '1 positional argument'
              326  STORE_FAST               '_video_depth_old'

 L. 501       328  LOAD_GLOBAL              basic_data
              330  LOAD_METHOD              str2int
              332  LOAD_FAST                'self'
              334  LOAD_ATTR                ldtnewheight
              336  LOAD_METHOD              text
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  CALL_METHOD_1         1  '1 positional argument'
              342  STORE_FAST               '_video_height_new'

 L. 502       344  LOAD_GLOBAL              basic_data
              346  LOAD_METHOD              str2int
              348  LOAD_FAST                'self'
              350  LOAD_ATTR                ldtnewwidth
              352  LOAD_METHOD              text
              354  CALL_METHOD_0         0  '0 positional arguments'
              356  CALL_METHOD_1         1  '1 positional argument'
              358  STORE_FAST               '_video_width_new'

 L. 503       360  LOAD_GLOBAL              basic_data
              362  LOAD_METHOD              str2int
              364  LOAD_FAST                'self'
              366  LOAD_ATTR                ldtnewdepth
              368  LOAD_METHOD              text
              370  CALL_METHOD_0         0  '0 positional arguments'
              372  CALL_METHOD_1         1  '1 positional argument'
              374  STORE_FAST               '_video_depth_new'

 L. 504       376  LOAD_FAST                '_video_height_old'
              378  LOAD_CONST               False
              380  COMPARE_OP               is
          382_384  POP_JUMP_IF_TRUE    436  'to 436'
              386  LOAD_FAST                '_video_width_old'
              388  LOAD_CONST               False
              390  COMPARE_OP               is
          392_394  POP_JUMP_IF_TRUE    436  'to 436'
              396  LOAD_FAST                '_video_depth_old'
              398  LOAD_CONST               False
              400  COMPARE_OP               is
          402_404  POP_JUMP_IF_TRUE    436  'to 436'

 L. 505       406  LOAD_FAST                '_video_height_new'
              408  LOAD_CONST               False
              410  COMPARE_OP               is
          412_414  POP_JUMP_IF_TRUE    436  'to 436'
              416  LOAD_FAST                '_video_width_new'
              418  LOAD_CONST               False
              420  COMPARE_OP               is
          422_424  POP_JUMP_IF_TRUE    436  'to 436'
              426  LOAD_FAST                '_video_depth_new'
              428  LOAD_CONST               False
              430  COMPARE_OP               is
          432_434  POP_JUMP_IF_FALSE   472  'to 472'
            436_0  COME_FROM           422  '422'
            436_1  COME_FROM           412  '412'
            436_2  COME_FROM           402  '402'
            436_3  COME_FROM           392  '392'
            436_4  COME_FROM           382  '382'

 L. 506       436  LOAD_GLOBAL              vis_msg
              438  LOAD_ATTR                print
              440  LOAD_STR                 'ERROR in EvaluateMl3DCnn: Non-integer feature size'
              442  LOAD_STR                 'error'
              444  LOAD_CONST               ('type',)
              446  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              448  POP_TOP          

 L. 507       450  LOAD_GLOBAL              QtWidgets
              452  LOAD_ATTR                QMessageBox
              454  LOAD_METHOD              critical
              456  LOAD_FAST                'self'
              458  LOAD_ATTR                msgbox

 L. 508       460  LOAD_STR                 'Evaluate 3D-CNN'

 L. 509       462  LOAD_STR                 'Non-integer feature size'
              464  CALL_METHOD_3         3  '3 positional arguments'
              466  POP_TOP          

 L. 510       468  LOAD_CONST               None
              470  RETURN_VALUE     
            472_0  COME_FROM           432  '432'

 L. 511       472  LOAD_FAST                '_video_height_old'
              474  LOAD_CONST               2
              476  COMPARE_OP               <
          478_480  POP_JUMP_IF_TRUE    532  'to 532'
              482  LOAD_FAST                '_video_width_old'
              484  LOAD_CONST               2
              486  COMPARE_OP               <
          488_490  POP_JUMP_IF_TRUE    532  'to 532'
              492  LOAD_FAST                '_video_depth_old'
              494  LOAD_CONST               2
              496  COMPARE_OP               <
          498_500  POP_JUMP_IF_TRUE    532  'to 532'

 L. 512       502  LOAD_FAST                '_video_height_new'
              504  LOAD_CONST               2
              506  COMPARE_OP               <
          508_510  POP_JUMP_IF_TRUE    532  'to 532'
              512  LOAD_FAST                '_video_width_new'
              514  LOAD_CONST               2
              516  COMPARE_OP               <
          518_520  POP_JUMP_IF_TRUE    532  'to 532'
              522  LOAD_FAST                '_video_depth_new'
              524  LOAD_CONST               2
              526  COMPARE_OP               <
          528_530  POP_JUMP_IF_FALSE   568  'to 568'
            532_0  COME_FROM           518  '518'
            532_1  COME_FROM           508  '508'
            532_2  COME_FROM           498  '498'
            532_3  COME_FROM           488  '488'
            532_4  COME_FROM           478  '478'

 L. 513       532  LOAD_GLOBAL              vis_msg
              534  LOAD_ATTR                print
              536  LOAD_STR                 'ERROR in EvaluateMl2DCnn: Features are not 3D '
              538  LOAD_STR                 'error'
              540  LOAD_CONST               ('type',)
              542  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              544  POP_TOP          

 L. 514       546  LOAD_GLOBAL              QtWidgets
              548  LOAD_ATTR                QMessageBox
              550  LOAD_METHOD              critical
              552  LOAD_FAST                'self'
              554  LOAD_ATTR                msgbox

 L. 515       556  LOAD_STR                 'Evaluate 2D-CNN'

 L. 516       558  LOAD_STR                 'Features are not 3D '
              560  CALL_METHOD_3         3  '3 positional arguments'
              562  POP_TOP          

 L. 517       564  LOAD_CONST               None
              566  RETURN_VALUE     
            568_0  COME_FROM           528  '528'

 L. 519       568  LOAD_GLOBAL              basic_data
              570  LOAD_METHOD              str2int
              572  LOAD_FAST                'self'
              574  LOAD_ATTR                ldtbatchsize
              576  LOAD_METHOD              text
              578  CALL_METHOD_0         0  '0 positional arguments'
              580  CALL_METHOD_1         1  '1 positional argument'
              582  STORE_FAST               '_batch'

 L. 520       584  LOAD_FAST                '_batch'
              586  LOAD_CONST               False
              588  COMPARE_OP               is
          590_592  POP_JUMP_IF_TRUE    604  'to 604'
              594  LOAD_FAST                '_batch'
              596  LOAD_CONST               1
              598  COMPARE_OP               <
          600_602  POP_JUMP_IF_FALSE   640  'to 640'
            604_0  COME_FROM           590  '590'

 L. 521       604  LOAD_GLOBAL              vis_msg
              606  LOAD_ATTR                print
              608  LOAD_STR                 'ERROR in EvaluateMl3DCnn: Non-positive batch size'
              610  LOAD_STR                 'error'
              612  LOAD_CONST               ('type',)
              614  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              616  POP_TOP          

 L. 522       618  LOAD_GLOBAL              QtWidgets
              620  LOAD_ATTR                QMessageBox
              622  LOAD_METHOD              critical
              624  LOAD_FAST                'self'
              626  LOAD_ATTR                msgbox

 L. 523       628  LOAD_STR                 'Evaluate 3D-CNN'

 L. 524       630  LOAD_STR                 'Non-positive batch size'
              632  CALL_METHOD_3         3  '3 positional arguments'
              634  POP_TOP          

 L. 525       636  LOAD_CONST               None
              638  RETURN_VALUE     
            640_0  COME_FROM           600  '600'

 L. 527       640  LOAD_CONST               2
              642  LOAD_GLOBAL              int
              644  LOAD_FAST                '_video_height_old'
              646  LOAD_CONST               2
              648  BINARY_TRUE_DIVIDE
              650  CALL_FUNCTION_1       1  '1 positional argument'
              652  BINARY_MULTIPLY  
              654  LOAD_CONST               1
              656  BINARY_ADD       
              658  STORE_FAST               '_video_height_old'

 L. 528       660  LOAD_CONST               2
              662  LOAD_GLOBAL              int
              664  LOAD_FAST                '_video_width_old'
              666  LOAD_CONST               2
              668  BINARY_TRUE_DIVIDE
              670  CALL_FUNCTION_1       1  '1 positional argument'
              672  BINARY_MULTIPLY  
              674  LOAD_CONST               1
              676  BINARY_ADD       
              678  STORE_FAST               '_video_width_old'

 L. 529       680  LOAD_CONST               2
              682  LOAD_GLOBAL              int
              684  LOAD_FAST                '_video_depth_old'
              686  LOAD_CONST               2
              688  BINARY_TRUE_DIVIDE
              690  CALL_FUNCTION_1       1  '1 positional argument'
              692  BINARY_MULTIPLY  
              694  LOAD_CONST               1
              696  BINARY_ADD       
              698  STORE_FAST               '_video_depth_old'

 L. 531       700  LOAD_FAST                'self'
              702  LOAD_ATTR                modelinfo
              704  LOAD_STR                 'number_label'
              706  BINARY_SUBSCR    
              708  STORE_FAST               '_nlabel'

 L. 532       710  LOAD_FAST                'self'
              712  LOAD_ATTR                modelinfo
              714  LOAD_STR                 'target'
              716  BINARY_SUBSCR    
              718  STORE_FAST               '_target'

 L. 534       720  LOAD_GLOBAL              int
              722  LOAD_FAST                '_video_depth_old'
              724  LOAD_CONST               2
              726  BINARY_TRUE_DIVIDE
              728  CALL_FUNCTION_1       1  '1 positional argument'
              730  STORE_FAST               '_wdinl'

 L. 535       732  LOAD_GLOBAL              int
              734  LOAD_FAST                '_video_width_old'
              736  LOAD_CONST               2
              738  BINARY_TRUE_DIVIDE
              740  CALL_FUNCTION_1       1  '1 positional argument'
              742  STORE_FAST               '_wdxl'

 L. 536       744  LOAD_GLOBAL              int
              746  LOAD_FAST                '_video_height_old'
              748  LOAD_CONST               2
              750  BINARY_TRUE_DIVIDE
              752  CALL_FUNCTION_1       1  '1 positional argument'
              754  STORE_FAST               '_wdz'

 L. 538       756  LOAD_FAST                'self'
              758  LOAD_ATTR                survinfo
              760  STORE_FAST               '_seisinfo'

 L. 540       762  LOAD_GLOBAL              seis_ays
              764  LOAD_ATTR                removeOutofSurveySample
              766  LOAD_GLOBAL              seis_ays
              768  LOAD_METHOD              convertSeisInfoTo2DMat
              770  LOAD_FAST                'self'
              772  LOAD_ATTR                survinfo
              774  CALL_METHOD_1         1  '1 positional argument'

 L. 541       776  LOAD_FAST                '_seisinfo'
              778  LOAD_STR                 'ILStart'
              780  BINARY_SUBSCR    
              782  LOAD_FAST                '_wdinl'
              784  LOAD_FAST                '_seisinfo'
              786  LOAD_STR                 'ILStep'
              788  BINARY_SUBSCR    
              790  BINARY_MULTIPLY  
              792  BINARY_ADD       

 L. 542       794  LOAD_FAST                '_seisinfo'
              796  LOAD_STR                 'ILEnd'
              798  BINARY_SUBSCR    
              800  LOAD_FAST                '_wdinl'
              802  LOAD_FAST                '_seisinfo'
              804  LOAD_STR                 'ILStep'
              806  BINARY_SUBSCR    
              808  BINARY_MULTIPLY  
              810  BINARY_SUBTRACT  

 L. 543       812  LOAD_FAST                '_seisinfo'
              814  LOAD_STR                 'XLStart'
              816  BINARY_SUBSCR    
              818  LOAD_FAST                '_wdxl'
              820  LOAD_FAST                '_seisinfo'
              822  LOAD_STR                 'XLStep'
              824  BINARY_SUBSCR    
              826  BINARY_MULTIPLY  
              828  BINARY_ADD       

 L. 544       830  LOAD_FAST                '_seisinfo'
              832  LOAD_STR                 'XLEnd'
              834  BINARY_SUBSCR    
              836  LOAD_FAST                '_wdxl'
              838  LOAD_FAST                '_seisinfo'
              840  LOAD_STR                 'XLStep'
              842  BINARY_SUBSCR    
              844  BINARY_MULTIPLY  
              846  BINARY_SUBTRACT  

 L. 545       848  LOAD_FAST                '_seisinfo'
              850  LOAD_STR                 'ZStart'
              852  BINARY_SUBSCR    
              854  LOAD_FAST                '_wdz'
              856  LOAD_FAST                '_seisinfo'
              858  LOAD_STR                 'ZStep'
              860  BINARY_SUBSCR    
              862  BINARY_MULTIPLY  
              864  BINARY_ADD       

 L. 546       866  LOAD_FAST                '_seisinfo'
              868  LOAD_STR                 'ZEnd'
              870  BINARY_SUBSCR    
              872  LOAD_FAST                '_wdz'
              874  LOAD_FAST                '_seisinfo'
              876  LOAD_STR                 'ZStep'
              878  BINARY_SUBSCR    
              880  BINARY_MULTIPLY  
              882  BINARY_SUBTRACT  
              884  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
              886  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              888  STORE_FAST               '_data'

 L. 548       890  BUILD_MAP_0           0 
              892  STORE_FAST               '_seisdict'

 L. 549       894  LOAD_FAST                '_data'
              896  LOAD_CONST               None
              898  LOAD_CONST               None
              900  BUILD_SLICE_2         2 
              902  LOAD_CONST               0
              904  LOAD_CONST               1
              906  BUILD_SLICE_2         2 
              908  BUILD_TUPLE_2         2 
              910  BINARY_SUBSCR    
              912  LOAD_FAST                '_seisdict'
              914  LOAD_STR                 'Inline'
              916  STORE_SUBSCR     

 L. 550       918  LOAD_FAST                '_data'
              920  LOAD_CONST               None
              922  LOAD_CONST               None
              924  BUILD_SLICE_2         2 
              926  LOAD_CONST               1
              928  LOAD_CONST               2
              930  BUILD_SLICE_2         2 
              932  BUILD_TUPLE_2         2 
              934  BINARY_SUBSCR    
              936  LOAD_FAST                '_seisdict'
              938  LOAD_STR                 'Crossline'
              940  STORE_SUBSCR     

 L. 551       942  LOAD_FAST                '_data'
              944  LOAD_CONST               None
              946  LOAD_CONST               None
              948  BUILD_SLICE_2         2 
              950  LOAD_CONST               2
              952  LOAD_CONST               3
              954  BUILD_SLICE_2         2 
              956  BUILD_TUPLE_2         2 
              958  BINARY_SUBSCR    
              960  LOAD_FAST                '_seisdict'
              962  LOAD_STR                 'Z'
              964  STORE_SUBSCR     

 L. 553       966  LOAD_GLOBAL              basic_mdt
              968  LOAD_METHOD              maxDictConstantRow
              970  LOAD_FAST                '_seisdict'
              972  CALL_METHOD_1         1  '1 positional argument'
              974  STORE_FAST               '_nsample'

 L. 555       976  LOAD_GLOBAL              int
              978  LOAD_GLOBAL              np
              980  LOAD_METHOD              ceil
              982  LOAD_FAST                '_nsample'
              984  LOAD_FAST                '_batch'
              986  BINARY_TRUE_DIVIDE
              988  CALL_METHOD_1         1  '1 positional argument'
              990  CALL_FUNCTION_1       1  '1 positional argument'
              992  STORE_FAST               '_nloop'

 L. 558       994  LOAD_GLOBAL              QtWidgets
              996  LOAD_METHOD              QProgressDialog
              998  CALL_METHOD_0         0  '0 positional arguments'
             1000  STORE_FAST               '_pgsdlg'

 L. 559      1002  LOAD_GLOBAL              QtGui
             1004  LOAD_METHOD              QIcon
             1006  CALL_METHOD_0         0  '0 positional arguments'
             1008  STORE_FAST               'icon'

 L. 560      1010  LOAD_FAST                'icon'
             1012  LOAD_METHOD              addPixmap
             1014  LOAD_GLOBAL              QtGui
             1016  LOAD_METHOD              QPixmap
             1018  LOAD_GLOBAL              os
             1020  LOAD_ATTR                path
             1022  LOAD_METHOD              join
             1024  LOAD_FAST                'self'
             1026  LOAD_ATTR                iconpath
             1028  LOAD_STR                 'icons/check.png'
             1030  CALL_METHOD_2         2  '2 positional arguments'
             1032  CALL_METHOD_1         1  '1 positional argument'

 L. 561      1034  LOAD_GLOBAL              QtGui
             1036  LOAD_ATTR                QIcon
             1038  LOAD_ATTR                Normal
             1040  LOAD_GLOBAL              QtGui
             1042  LOAD_ATTR                QIcon
             1044  LOAD_ATTR                Off
             1046  CALL_METHOD_3         3  '3 positional arguments'
             1048  POP_TOP          

 L. 562      1050  LOAD_FAST                '_pgsdlg'
             1052  LOAD_METHOD              setWindowIcon
             1054  LOAD_FAST                'icon'
             1056  CALL_METHOD_1         1  '1 positional argument'
             1058  POP_TOP          

 L. 563      1060  LOAD_FAST                '_pgsdlg'
             1062  LOAD_METHOD              setWindowTitle
             1064  LOAD_STR                 'Evaluate 3D-CNN'
             1066  CALL_METHOD_1         1  '1 positional argument'
             1068  POP_TOP          

 L. 564      1070  LOAD_FAST                '_pgsdlg'
             1072  LOAD_METHOD              setCancelButton
             1074  LOAD_CONST               None
             1076  CALL_METHOD_1         1  '1 positional argument'
             1078  POP_TOP          

 L. 565      1080  LOAD_FAST                '_pgsdlg'
             1082  LOAD_METHOD              setWindowFlags
             1084  LOAD_GLOBAL              QtCore
             1086  LOAD_ATTR                Qt
             1088  LOAD_ATTR                WindowStaysOnTopHint
             1090  CALL_METHOD_1         1  '1 positional argument'
             1092  POP_TOP          

 L. 566      1094  LOAD_FAST                '_pgsdlg'
             1096  LOAD_METHOD              forceShow
             1098  CALL_METHOD_0         0  '0 positional arguments'
             1100  POP_TOP          

 L. 567      1102  LOAD_FAST                '_pgsdlg'
             1104  LOAD_METHOD              setFixedWidth
             1106  LOAD_CONST               400
             1108  CALL_METHOD_1         1  '1 positional argument'
             1110  POP_TOP          

 L. 568      1112  LOAD_FAST                '_pgsdlg'
             1114  LOAD_METHOD              setMaximum
             1116  LOAD_FAST                '_nloop'
             1118  CALL_METHOD_1         1  '1 positional argument'
             1120  POP_TOP          

 L. 570      1122  LOAD_GLOBAL              np
             1124  LOAD_METHOD              zeros
             1126  LOAD_FAST                '_nlabel'
             1128  LOAD_CONST               1
             1130  BINARY_ADD       
             1132  LOAD_FAST                '_nlabel'
             1134  LOAD_CONST               1
             1136  BINARY_ADD       
             1138  BUILD_LIST_2          2 
             1140  CALL_METHOD_1         1  '1 positional argument'
             1142  STORE_FAST               '_result'

 L. 571      1144  LOAD_CONST               0
             1146  STORE_FAST               'idxstart'

 L. 572  1148_1150  SETUP_LOOP         1616  'to 1616'
             1152  LOAD_GLOBAL              range
             1154  LOAD_FAST                '_nloop'
             1156  CALL_FUNCTION_1       1  '1 positional argument'
             1158  GET_ITER         
         1160_1162  FOR_ITER           1614  'to 1614'
             1164  STORE_FAST               'i'

 L. 574      1166  LOAD_GLOBAL              sys
             1168  LOAD_ATTR                stdout
             1170  LOAD_METHOD              write

 L. 575      1172  LOAD_STR                 '\r>>> Evaluate 3D-CNN, proceeding %.1f%% '
             1174  LOAD_GLOBAL              float
             1176  LOAD_FAST                'i'
             1178  LOAD_CONST               1
             1180  BINARY_ADD       
             1182  CALL_FUNCTION_1       1  '1 positional argument'
             1184  LOAD_GLOBAL              float
             1186  LOAD_FAST                '_nloop'
             1188  CALL_FUNCTION_1       1  '1 positional argument'
             1190  BINARY_TRUE_DIVIDE
             1192  LOAD_CONST               100.0
             1194  BINARY_MULTIPLY  
             1196  BINARY_MODULO    
             1198  CALL_METHOD_1         1  '1 positional argument'
             1200  POP_TOP          

 L. 576      1202  LOAD_GLOBAL              sys
             1204  LOAD_ATTR                stdout
             1206  LOAD_METHOD              flush
             1208  CALL_METHOD_0         0  '0 positional arguments'
             1210  POP_TOP          

 L. 578      1212  LOAD_GLOBAL              QtCore
             1214  LOAD_ATTR                QCoreApplication
             1216  LOAD_METHOD              instance
             1218  CALL_METHOD_0         0  '0 positional arguments'
             1220  LOAD_METHOD              processEvents
             1222  CALL_METHOD_0         0  '0 positional arguments'
             1224  POP_TOP          

 L. 580      1226  LOAD_FAST                'idxstart'
             1228  LOAD_FAST                '_batch'
             1230  BINARY_ADD       
             1232  STORE_FAST               'idxend'

 L. 581      1234  LOAD_FAST                'idxend'
             1236  LOAD_FAST                '_nsample'
             1238  COMPARE_OP               >
         1240_1242  POP_JUMP_IF_FALSE  1248  'to 1248'

 L. 582      1244  LOAD_FAST                '_nsample'
             1246  STORE_FAST               'idxend'
           1248_0  COME_FROM          1240  '1240'

 L. 583      1248  LOAD_GLOBAL              np
             1250  LOAD_METHOD              linspace
             1252  LOAD_FAST                'idxstart'
             1254  LOAD_FAST                'idxend'
             1256  LOAD_CONST               1
             1258  BINARY_SUBTRACT  
             1260  LOAD_FAST                'idxend'
             1262  LOAD_FAST                'idxstart'
             1264  BINARY_SUBTRACT  
             1266  CALL_METHOD_3         3  '3 positional arguments'
             1268  LOAD_METHOD              astype
             1270  LOAD_GLOBAL              int
             1272  CALL_METHOD_1         1  '1 positional argument'
             1274  STORE_FAST               'idxlist'

 L. 584      1276  LOAD_FAST                'idxend'
             1278  STORE_FAST               'idxstart'

 L. 585      1280  LOAD_GLOBAL              basic_mdt
             1282  LOAD_METHOD              retrieveDictByIndex
             1284  LOAD_FAST                '_seisdict'
             1286  LOAD_FAST                'idxlist'
             1288  CALL_METHOD_2         2  '2 positional arguments'
             1290  STORE_FAST               '_dict'

 L. 587      1292  LOAD_FAST                '_dict'
             1294  LOAD_STR                 'Inline'
             1296  BINARY_SUBSCR    
             1298  STORE_FAST               '_targetdata'

 L. 588      1300  LOAD_GLOBAL              np
             1302  LOAD_ATTR                concatenate
             1304  LOAD_FAST                '_targetdata'
             1306  LOAD_FAST                '_dict'
             1308  LOAD_STR                 'Crossline'
             1310  BINARY_SUBSCR    
             1312  BUILD_TUPLE_2         2 
             1314  LOAD_CONST               1
             1316  LOAD_CONST               ('axis',)
             1318  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1320  STORE_FAST               '_targetdata'

 L. 589      1322  LOAD_GLOBAL              np
             1324  LOAD_ATTR                concatenate
             1326  LOAD_FAST                '_targetdata'
             1328  LOAD_FAST                '_dict'
             1330  LOAD_STR                 'Z'
             1332  BINARY_SUBSCR    
             1334  BUILD_TUPLE_2         2 
             1336  LOAD_CONST               1
             1338  LOAD_CONST               ('axis',)
             1340  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1342  STORE_FAST               '_targetdata'

 L. 590      1344  SETUP_LOOP         1478  'to 1478'
             1346  LOAD_FAST                '_featurelist'
             1348  GET_ITER         
           1350_0  COME_FROM          1436  '1436'
             1350  FOR_ITER           1476  'to 1476'
             1352  STORE_FAST               'f'

 L. 591      1354  LOAD_FAST                'self'
             1356  LOAD_ATTR                seisdata
             1358  LOAD_FAST                'f'
             1360  BINARY_SUBSCR    
             1362  STORE_FAST               '_data'

 L. 592      1364  LOAD_GLOBAL              seis_ays
             1366  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             1368  LOAD_FAST                '_data'
             1370  LOAD_FAST                '_targetdata'
             1372  LOAD_FAST                'self'
             1374  LOAD_ATTR                survinfo

 L. 593      1376  LOAD_FAST                '_wdinl'
             1378  LOAD_FAST                '_wdxl'
             1380  LOAD_FAST                '_wdz'

 L. 594      1382  LOAD_CONST               False
             1384  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             1386  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1388  LOAD_CONST               None
             1390  LOAD_CONST               None
             1392  BUILD_SLICE_2         2 
             1394  LOAD_CONST               3
             1396  LOAD_CONST               None
             1398  BUILD_SLICE_2         2 
             1400  BUILD_TUPLE_2         2 
             1402  BINARY_SUBSCR    
             1404  LOAD_FAST                '_dict'
             1406  LOAD_FAST                'f'
             1408  STORE_SUBSCR     

 L. 595      1410  LOAD_FAST                '_video_height_new'
             1412  LOAD_FAST                '_video_height_old'
             1414  COMPARE_OP               !=
         1416_1418  POP_JUMP_IF_TRUE   1440  'to 1440'

 L. 596      1420  LOAD_FAST                '_video_width_new'
             1422  LOAD_FAST                '_video_width_old'
             1424  COMPARE_OP               !=
         1426_1428  POP_JUMP_IF_TRUE   1440  'to 1440'

 L. 597      1430  LOAD_FAST                '_video_depth_new'
             1432  LOAD_FAST                '_video_depth_old'
             1434  COMPARE_OP               !=
         1436_1438  POP_JUMP_IF_FALSE  1350  'to 1350'
           1440_0  COME_FROM          1426  '1426'
           1440_1  COME_FROM          1416  '1416'

 L. 598      1440  LOAD_GLOBAL              basic_video
             1442  LOAD_ATTR                changeVideoSize
             1444  LOAD_FAST                '_dict'
             1446  LOAD_FAST                'f'
             1448  BINARY_SUBSCR    

 L. 599      1450  LOAD_FAST                '_video_height_old'

 L. 600      1452  LOAD_FAST                '_video_width_old'

 L. 601      1454  LOAD_FAST                '_video_depth_old'

 L. 602      1456  LOAD_FAST                '_video_height_new'

 L. 603      1458  LOAD_FAST                '_video_width_new'

 L. 604      1460  LOAD_FAST                '_video_depth_new'
             1462  LOAD_CONST               ('video_height', 'video_width', 'video_depth', 'video_height_new', 'video_width_new', 'video_depth_new')
             1464  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1466  LOAD_FAST                '_dict'
             1468  LOAD_FAST                'f'
             1470  STORE_SUBSCR     
         1472_1474  JUMP_BACK          1350  'to 1350'
             1476  POP_BLOCK        
           1478_0  COME_FROM_LOOP     1344  '1344'

 L. 606      1478  LOAD_FAST                '_target'
             1480  LOAD_FAST                '_featurelist'
             1482  COMPARE_OP               not-in
         1484_1486  POP_JUMP_IF_FALSE  1538  'to 1538'

 L. 607      1488  LOAD_FAST                'self'
             1490  LOAD_ATTR                seisdata
             1492  LOAD_FAST                '_target'
             1494  BINARY_SUBSCR    
             1496  STORE_FAST               '_data'

 L. 608      1498  LOAD_GLOBAL              seis_ays
             1500  LOAD_ATTR                retrieveSeisSampleFrom3DMat
             1502  LOAD_FAST                '_data'
             1504  LOAD_FAST                '_targetdata'

 L. 609      1506  LOAD_FAST                'self'
             1508  LOAD_ATTR                survinfo

 L. 610      1510  LOAD_CONST               False
             1512  LOAD_CONST               ('seisinfo', 'verbose')
             1514  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1516  LOAD_CONST               None
             1518  LOAD_CONST               None
             1520  BUILD_SLICE_2         2 
             1522  LOAD_CONST               3
             1524  LOAD_CONST               None
             1526  BUILD_SLICE_2         2 
             1528  BUILD_TUPLE_2         2 
             1530  BINARY_SUBSCR    
             1532  LOAD_FAST                '_dict'
             1534  LOAD_FAST                '_target'
             1536  STORE_SUBSCR     
           1538_0  COME_FROM          1484  '1484'

 L. 611      1538  LOAD_GLOBAL              np
             1540  LOAD_METHOD              round
             1542  LOAD_FAST                '_dict'
             1544  LOAD_FAST                '_target'
             1546  BINARY_SUBSCR    
             1548  CALL_METHOD_1         1  '1 positional argument'
             1550  LOAD_METHOD              astype
             1552  LOAD_GLOBAL              int
             1554  CALL_METHOD_1         1  '1 positional argument'
             1556  LOAD_FAST                '_dict'
             1558  LOAD_FAST                '_target'
             1560  STORE_SUBSCR     

 L. 613      1562  LOAD_GLOBAL              ml_cnn3d
             1564  LOAD_ATTR                evaluate3DCNNClassifier
             1566  LOAD_FAST                '_dict'

 L. 614      1568  LOAD_FAST                'self'
             1570  LOAD_ATTR                modelpath

 L. 615      1572  LOAD_FAST                'self'
             1574  LOAD_ATTR                modelname

 L. 616      1576  LOAD_CONST               True
             1578  LOAD_CONST               ('cnn3dpath', 'cnn3dname', 'verbose')
             1580  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1582  STORE_FAST               '_confmatrix'

 L. 617      1584  LOAD_FAST                '_result'
             1586  LOAD_FAST                '_confmatrix'
             1588  LOAD_STR                 'confusion_matrix'
             1590  BINARY_SUBSCR    
             1592  BINARY_ADD       
             1594  STORE_FAST               '_result'

 L. 619      1596  LOAD_FAST                '_pgsdlg'
             1598  LOAD_METHOD              setValue
             1600  LOAD_FAST                'i'
             1602  LOAD_CONST               1
             1604  BINARY_ADD       
             1606  CALL_METHOD_1         1  '1 positional argument'
             1608  POP_TOP          
         1610_1612  JUMP_BACK          1160  'to 1160'
             1614  POP_BLOCK        
           1616_0  COME_FROM_LOOP     1148  '1148'

 L. 621      1616  LOAD_GLOBAL              print
             1618  LOAD_STR                 'Done'
             1620  CALL_FUNCTION_1       1  '1 positional argument'
             1622  POP_TOP          

 L. 623      1624  LOAD_FAST                '_result'
             1626  LOAD_CONST               0
             1628  LOAD_CONST               1
             1630  LOAD_CONST               None
             1632  BUILD_SLICE_2         2 
             1634  BUILD_TUPLE_2         2 
             1636  BINARY_SUBSCR    
             1638  LOAD_FAST                '_nloop'
             1640  BINARY_TRUE_DIVIDE
             1642  LOAD_FAST                '_result'
             1644  LOAD_CONST               0
             1646  LOAD_CONST               1
             1648  LOAD_CONST               None
             1650  BUILD_SLICE_2         2 
             1652  BUILD_TUPLE_2         2 
             1654  STORE_SUBSCR     

 L. 624      1656  LOAD_FAST                '_result'
             1658  LOAD_CONST               1
             1660  LOAD_CONST               None
             1662  BUILD_SLICE_2         2 
             1664  LOAD_CONST               0
             1666  BUILD_TUPLE_2         2 
             1668  BINARY_SUBSCR    
             1670  LOAD_FAST                '_nloop'
             1672  BINARY_TRUE_DIVIDE
             1674  LOAD_FAST                '_result'
             1676  LOAD_CONST               1
             1678  LOAD_CONST               None
             1680  BUILD_SLICE_2         2 
             1682  LOAD_CONST               0
             1684  BUILD_TUPLE_2         2 
             1686  STORE_SUBSCR     

 L. 625      1688  LOAD_GLOBAL              print
             1690  LOAD_FAST                '_result'
             1692  CALL_FUNCTION_1       1  '1 positional argument'
             1694  POP_TOP          

 L. 630      1696  LOAD_GLOBAL              QtWidgets
             1698  LOAD_METHOD              QDialog
             1700  CALL_METHOD_0         0  '0 positional arguments'
             1702  STORE_FAST               '_viewmlconfmat'

 L. 631      1704  LOAD_GLOBAL              gui_viewmlconfmat
             1706  CALL_FUNCTION_0       0  '0 positional arguments'
             1708  STORE_FAST               '_gui'

 L. 632      1710  LOAD_FAST                '_result'
             1712  LOAD_FAST                '_gui'
             1714  STORE_ATTR               confmat

 L. 633      1716  LOAD_FAST                '_gui'
             1718  LOAD_METHOD              setupGUI
             1720  LOAD_FAST                '_viewmlconfmat'
             1722  CALL_METHOD_1         1  '1 positional argument'
             1724  POP_TOP          

 L. 634      1726  LOAD_FAST                '_viewmlconfmat'
             1728  LOAD_METHOD              exec
             1730  CALL_METHOD_0         0  '0 positional arguments'
             1732  POP_TOP          

 L. 635      1734  LOAD_FAST                '_viewmlconfmat'
             1736  LOAD_METHOD              show
             1738  CALL_METHOD_0         0  '0 positional arguments'
             1740  POP_TOP          

Parse error at or near `CALL_METHOD_0' instruction at offset 1738

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
    EvaluateMl3DCnn = QtWidgets.QWidget()
    gui = evaluateml3dcnn()
    gui.setupGUI(EvaluateMl3DCnn)
    EvaluateMl3DCnn.show()
    sys.exit(app.exec_())