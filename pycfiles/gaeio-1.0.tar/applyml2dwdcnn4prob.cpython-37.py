# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\applyml2dwdcnn4prob.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 36933 bytes
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
import cognitivegeo.src.ml.wdcnnsegmentor as ml_wdcnn
import cognitivegeo.src.gui.viewml2dwdcnn as gui_viewml2dwdcnn
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class applyml2dwdcnn4prob(object):
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

    def setupGUI(self, ApplyMl2DWdcnn4Prob):
        ApplyMl2DWdcnn4Prob.setObjectName('ApplyMl2DWdcnn4Prob')
        ApplyMl2DWdcnn4Prob.setFixedSize(810, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ApplyMl2DWdcnn4Prob.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ApplyMl2DWdcnn4Prob)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ApplyMl2DWdcnn4Prob)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ApplyMl2DWdcnn4Prob)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(ApplyMl2DWdcnn4Prob)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 230, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 230, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(ApplyMl2DWdcnn4Prob)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 230, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 270, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(ApplyMl2DWdcnn4Prob)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 270, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 230, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(ApplyMl2DWdcnn4Prob)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(ApplyMl2DWdcnn4Prob)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ApplyMl2DWdcnn4Prob)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ApplyMl2DWdcnn4Prob)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ApplyMl2DWdcnn4Prob)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 190))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(ApplyMl2DWdcnn4Prob)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(ApplyMl2DWdcnn4Prob)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 190))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 350, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 350, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ApplyMl2DWdcnn4Prob)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 350, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 390, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ApplyMl2DWdcnn4Prob)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 390, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 350, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 350, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ApplyMl2DWdcnn4Prob)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 350, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 390, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ApplyMl2DWdcnn4Prob)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 390, 40, 30))
        self.lblpara = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 320, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ApplyMl2DWdcnn4Prob)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblsave = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ApplyMl2DWdcnn4Prob)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(150, 390, 100, 30))
        self.lbltarget = QtWidgets.QLabel(ApplyMl2DWdcnn4Prob)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(250, 350, 50, 30))
        self.lwgtarget = QtWidgets.QListWidget(ApplyMl2DWdcnn4Prob)
        self.lwgtarget.setObjectName('lwgtarget')
        self.lwgtarget.setGeometry(QtCore.QRect(300, 350, 90, 70))
        self.lwgtarget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.btnapply = QtWidgets.QPushButton(ApplyMl2DWdcnn4Prob)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(320, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ApplyMl2DWdcnn4Prob)
        self.msgbox.setObjectName('msgbox')
        _center_x = ApplyMl2DWdcnn4Prob.geometry().center().x()
        _center_y = ApplyMl2DWdcnn4Prob.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ApplyMl2DWdcnn4Prob)
        QtCore.QMetaObject.connectSlotsByName(ApplyMl2DWdcnn4Prob)

    def retranslateGUI(self, ApplyMl2DWdcnn4Prob):
        self.dialog = ApplyMl2DWdcnn4Prob
        _translate = QtCore.QCoreApplication.translate
        ApplyMl2DWdcnn4Prob.setWindowTitle(_translate('ApplyMl2DWdcnn4Prob', 'Apply 2D-WDCNN for probabilities'))
        self.lblfrom.setText(_translate('ApplyMl2DWdcnn4Prob', 'Select network:'))
        self.ldtfrom.setText(_translate('ApplyMl2DWdcnn4Prob', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ApplyMl2DWdcnn4Prob', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ApplyMl2DWdcnn4Prob', 'Training features:'))
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblornt.setText(_translate('ApplyMl2DWdcnn4Prob', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.cbbornt.currentIndexChanged.connect(self.changeCbbOrnt)
        self.lbloldsize.setText(_translate('ApplyMl2DWdcnn4Prob', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('ApplyMl2DWdcnn4Prob', 'height='))
        self.ldtoldheight.setText(_translate('ApplyMl2DWdcnn4Prob', '0'))
        self.ldtoldheight.setEnabled(False)
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('ApplyMl2DWdcnn4Prob', 'width='))
        self.ldtoldwidth.setText(_translate('ApplyMl2DWdcnn4Prob', '0'))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtoldwidth.setEnabled(False)
        self.lblnewsize.setText(_translate('ApplyMl2DWdcnn4Prob', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('ApplyMl2DWdcnn4Prob', 'height='))
        self.ldtnewheight.setText(_translate('ApplyMl2DWdcnn4Prob', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('ApplyMl2DWdcnn4Prob', 'width='))
        self.ldtnewwidth.setText(_translate('ApplyMl2DWdcnn4Prob', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('ApplyMl2DWdcnn4Prob', 'Pre-trained WDCNN architecture:'))
        self.btnviewnetwork.setText(_translate('ApplyMl2DWdcnn4Prob', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('ApplyMl2DWdcnn4Prob', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ApplyMl2DWdcnn4Prob', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('ApplyMl2DWdcnn4Prob', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('ApplyMl2DWdcnn4Prob', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('ApplyMl2DWdcnn4Prob', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ApplyMl2DWdcnn4Prob', 'height='))
        self.ldtmaskheight.setText(_translate('ApplyMl2DWdcnn4Prob', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ApplyMl2DWdcnn4Prob', 'width='))
        self.ldtmaskwidth.setText(_translate('ApplyMl2DWdcnn4Prob', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ApplyMl2DWdcnn4Prob', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ApplyMl2DWdcnn4Prob', 'height='))
        self.ldtpoolheight.setText(_translate('ApplyMl2DWdcnn4Prob', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ApplyMl2DWdcnn4Prob', 'width='))
        self.ldtpoolwidth.setText(_translate('ApplyMl2DWdcnn4Prob', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ApplyMl2DWdcnn4Prob', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ApplyMl2DWdcnn4Prob', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ApplyMl2DWdcnn4Prob', '5'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('ApplyMl2DWdcnn4Prob', 'Output prefix='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ApplyMl2DWdcnn4Prob', 'wdcnn_prob_'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltarget.setText(_translate('ApplyMl2DWdcnn4Prob', 'Target ='))
        self.btnapply.setText(_translate('ApplyMl2DWdcnn4Prob', 'Apply 2D-WDCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnApplyMl2DWdcnn4Prob)

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.checkWDCNNModel(self.modelpath, self.modelname) is True:
            self.modelinfo = ml_tfm.getModelInfo(self.modelpath, self.modelname)
            self.lwgfeature.clear()
            _firstfeature = None
            for f in self.modelinfo['feature_list']:
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
            _shape = self.getImageSize(_firstfeature.text())
            _height = _shape[0]
            _width = _shape[1]
            self.ldtoldheight.setText(str(_height))
            self.ldtoldwidth.setText(str(_width))
            self.btnviewnetwork.setEnabled(True)
            self.ldtnconvblock.setText(str(self.modelinfo['number_conv_block']))
            self.ldtn1x1layer.setText(str(self.modelinfo['number_1x1_layer']))
            self.ldtmaskheight.setText(str(self.modelinfo['patch_size'][0]))
            self.ldtmaskwidth.setText(str(self.modelinfo['patch_size'][1]))
            self.ldtpoolheight.setText(str(self.modelinfo['pool_size'][0]))
            self.ldtpoolwidth.setText(str(self.modelinfo['pool_size'][1]))
            self.lwgtarget.clear()
            self.lwgtarget.addItems([str(_t) for _t in range(self.modelinfo['number_class'])])
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
            self.ldtn1x1layer.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')
            self.lwgtarget.clear()

    def clickBtnFrom(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select WDCNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def changeLwgFeature(self):
        _shape = [
         0, 0]
        if ml_tfm.checkWDCNNModel(self.modelpath, self.modelname):
            _shape = self.getImageSize(self.lwgfeature.currentItem().text())
        _height = _shape[0]
        _width = _shape[1]
        self.ldtoldheight.setText(str(_height))
        self.ldtoldwidth.setText(str(_width))

    def changeCbbOrnt(self):
        _shape = [
         0, 0]
        if ml_tfm.checkWDCNNModel(self.modelpath, self.modelname):
            _shape = self.getImageSize(self.lwgfeature.currentItem().text())
        _height = _shape[0]
        _width = _shape[1]
        self.ldtoldheight.setText(str(_height))
        self.ldtoldwidth.setText(str(_width))

    def changeLdtNconvblock(self):
        if ml_tfm.checkWDCNNModel(self.modelpath, self.modelname) is True:
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

    def changeLdtN1x1layer(self):
        if ml_tfm.checkWDCNNModel(self.modelpath, self.modelname) is True:
            _nlayer = self.modelinfo['number_1x1_layer']
            self.twgn1x1layer.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgn1x1layer.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.modelinfo['number_1x1_feature'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgn1x1layer.setItem(_idx, 1, item)

        else:
            self.twgn1x1layer.setRowCount(0)

    def clickBtnViewNetwork(self):
        _viewml = QtWidgets.QDialog()
        _gui = gui_viewml2dwdcnn()
        _gui.linestyle = self.linestyle
        _gui.maskstyle = self.maskstyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewml)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewml.exec()
        _viewml.show()

    def clickBtnApplyMl2DWdcnn4Prob--- This code section failed: ---

 L. 469         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 471         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 472        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in ApplyMl2DWdcnn4Prob: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 473        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 474        44  LOAD_STR                 'Apply 2D-WDCNN'

 L. 475        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 476        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 478        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkWDCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 479        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in ApplyMl2DWdcnn4Prob: No pre-WDCNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 480        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 481       100  LOAD_STR                 'Apply 2D-WDCNN'

 L. 482       102  LOAD_STR                 'No pre-WDCNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 483       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 485       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 486       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 487       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in ApplyMl2DWdcnn4Prob: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    

 L. 488       152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 489       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 490       170  LOAD_STR                 'Apply 2D-WDCNN'

 L. 491       172  LOAD_STR                 "Feature '"
              174  LOAD_FAST                'f'
              176  BINARY_ADD       
              178  LOAD_STR                 "' not found in seismic data"
              180  BINARY_ADD       
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L. 492       186  LOAD_CONST               None
              188  RETURN_VALUE     
              190  JUMP_BACK           124  'to 124'
              192  POP_BLOCK        
            194_0  COME_FROM_LOOP      112  '112'

 L. 494       194  LOAD_FAST                'self'
              196  LOAD_ATTR                modelinfo
              198  LOAD_STR                 'feature_list'
              200  BINARY_SUBSCR    
              202  STORE_FAST               '_features'

 L. 495       204  LOAD_GLOBAL              basic_data
              206  LOAD_METHOD              str2int
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                ldtoldheight
              212  LOAD_METHOD              text
              214  CALL_METHOD_0         0  '0 positional arguments'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  STORE_FAST               '_image_height'

 L. 496       220  LOAD_GLOBAL              basic_data
              222  LOAD_METHOD              str2int
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                ldtoldwidth
              228  LOAD_METHOD              text
              230  CALL_METHOD_0         0  '0 positional arguments'
              232  CALL_METHOD_1         1  '1 positional argument'
              234  STORE_FAST               '_image_width'

 L. 497       236  LOAD_GLOBAL              basic_data
              238  LOAD_METHOD              str2int
              240  LOAD_FAST                'self'
              242  LOAD_ATTR                ldtnewheight
              244  LOAD_METHOD              text
              246  CALL_METHOD_0         0  '0 positional arguments'
              248  CALL_METHOD_1         1  '1 positional argument'
              250  STORE_FAST               '_image_height_new'

 L. 498       252  LOAD_GLOBAL              basic_data
              254  LOAD_METHOD              str2int
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                ldtnewwidth
              260  LOAD_METHOD              text
              262  CALL_METHOD_0         0  '0 positional arguments'
              264  CALL_METHOD_1         1  '1 positional argument'
              266  STORE_FAST               '_image_width_new'

 L. 499       268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               False
              272  COMPARE_OP               is
          274_276  POP_JUMP_IF_TRUE    308  'to 308'
              278  LOAD_FAST                '_image_width'
              280  LOAD_CONST               False
              282  COMPARE_OP               is
          284_286  POP_JUMP_IF_TRUE    308  'to 308'

 L. 500       288  LOAD_FAST                '_image_height_new'
              290  LOAD_CONST               False
              292  COMPARE_OP               is
          294_296  POP_JUMP_IF_TRUE    308  'to 308'
              298  LOAD_FAST                '_image_width_new'
              300  LOAD_CONST               False
              302  COMPARE_OP               is
          304_306  POP_JUMP_IF_FALSE   344  'to 344'
            308_0  COME_FROM           294  '294'
            308_1  COME_FROM           284  '284'
            308_2  COME_FROM           274  '274'

 L. 501       308  LOAD_GLOBAL              vis_msg
              310  LOAD_ATTR                print
              312  LOAD_STR                 'ERROR in ApplyMl2DWdcnn4Prob: Non-integer feature size'
              314  LOAD_STR                 'error'
              316  LOAD_CONST               ('type',)
              318  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              320  POP_TOP          

 L. 502       322  LOAD_GLOBAL              QtWidgets
              324  LOAD_ATTR                QMessageBox
              326  LOAD_METHOD              critical
              328  LOAD_FAST                'self'
              330  LOAD_ATTR                msgbox

 L. 503       332  LOAD_STR                 'Apply 2D-WDCNN'

 L. 504       334  LOAD_STR                 'Non-integer feature size'
              336  CALL_METHOD_3         3  '3 positional arguments'
              338  POP_TOP          

 L. 505       340  LOAD_CONST               None
              342  RETURN_VALUE     
            344_0  COME_FROM           304  '304'

 L. 506       344  LOAD_FAST                '_image_height'
              346  LOAD_CONST               2
              348  COMPARE_OP               <
          350_352  POP_JUMP_IF_TRUE    384  'to 384'
              354  LOAD_FAST                '_image_width'
              356  LOAD_CONST               2
              358  COMPARE_OP               <
          360_362  POP_JUMP_IF_TRUE    384  'to 384'

 L. 507       364  LOAD_FAST                '_image_height_new'
              366  LOAD_CONST               2
              368  COMPARE_OP               <
          370_372  POP_JUMP_IF_TRUE    384  'to 384'
              374  LOAD_FAST                '_image_width_new'
              376  LOAD_CONST               2
              378  COMPARE_OP               <
          380_382  POP_JUMP_IF_FALSE   420  'to 420'
            384_0  COME_FROM           370  '370'
            384_1  COME_FROM           360  '360'
            384_2  COME_FROM           350  '350'

 L. 508       384  LOAD_GLOBAL              vis_msg
              386  LOAD_ATTR                print
              388  LOAD_STR                 'ERROR in ApplyMl2DWdcnn4Prob: Features are not 2D'
              390  LOAD_STR                 'error'
              392  LOAD_CONST               ('type',)
              394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              396  POP_TOP          

 L. 509       398  LOAD_GLOBAL              QtWidgets
              400  LOAD_ATTR                QMessageBox
              402  LOAD_METHOD              critical
              404  LOAD_FAST                'self'
              406  LOAD_ATTR                msgbox

 L. 510       408  LOAD_STR                 'Apply 2D-WDCNN'

 L. 511       410  LOAD_STR                 'Features are not 2D'
              412  CALL_METHOD_3         3  '3 positional arguments'
              414  POP_TOP          

 L. 512       416  LOAD_CONST               None
              418  RETURN_VALUE     
            420_0  COME_FROM           380  '380'

 L. 514       420  LOAD_GLOBAL              basic_data
              422  LOAD_METHOD              str2int
              424  LOAD_FAST                'self'
              426  LOAD_ATTR                ldtbatchsize
              428  LOAD_METHOD              text
              430  CALL_METHOD_0         0  '0 positional arguments'
              432  CALL_METHOD_1         1  '1 positional argument'
              434  STORE_FAST               '_batch'

 L. 515       436  LOAD_FAST                '_batch'
              438  LOAD_CONST               False
              440  COMPARE_OP               is
          442_444  POP_JUMP_IF_TRUE    456  'to 456'
              446  LOAD_FAST                '_batch'
              448  LOAD_CONST               1
              450  COMPARE_OP               <
          452_454  POP_JUMP_IF_FALSE   492  'to 492'
            456_0  COME_FROM           442  '442'

 L. 516       456  LOAD_GLOBAL              vis_msg
              458  LOAD_ATTR                print
              460  LOAD_STR                 'ERROR in ApplyMl2DWdcnn4Prob: Non-positive batch size'
              462  LOAD_STR                 'error'
              464  LOAD_CONST               ('type',)
              466  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              468  POP_TOP          

 L. 517       470  LOAD_GLOBAL              QtWidgets
              472  LOAD_ATTR                QMessageBox
              474  LOAD_METHOD              critical
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                msgbox

 L. 518       480  LOAD_STR                 'Apply 2D-WDCNN'

 L. 519       482  LOAD_STR                 'Non-positive batch size'
              484  CALL_METHOD_3         3  '3 positional arguments'
              486  POP_TOP          

 L. 520       488  LOAD_CONST               None
              490  RETURN_VALUE     
            492_0  COME_FROM           452  '452'

 L. 522       492  LOAD_GLOBAL              len
              494  LOAD_FAST                'self'
              496  LOAD_ATTR                ldtsave
              498  LOAD_METHOD              text
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  CALL_FUNCTION_1       1  '1 positional argument'
              504  LOAD_CONST               1
              506  COMPARE_OP               <
          508_510  POP_JUMP_IF_FALSE   548  'to 548'

 L. 523       512  LOAD_GLOBAL              vis_msg
              514  LOAD_ATTR                print
              516  LOAD_STR                 'ERROR in ApplyMl2DWdcnn4Prob: No prefix specified'
              518  LOAD_STR                 'error'
              520  LOAD_CONST               ('type',)
              522  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              524  POP_TOP          

 L. 524       526  LOAD_GLOBAL              QtWidgets
              528  LOAD_ATTR                QMessageBox
              530  LOAD_METHOD              critical
              532  LOAD_FAST                'self'
              534  LOAD_ATTR                msgbox

 L. 525       536  LOAD_STR                 'Apply 2D-WDCNN'

 L. 526       538  LOAD_STR                 'No prefix specified'
              540  CALL_METHOD_3         3  '3 positional arguments'
              542  POP_TOP          

 L. 527       544  LOAD_CONST               None
              546  RETURN_VALUE     
            548_0  COME_FROM           508  '508'

 L. 529       548  LOAD_GLOBAL              len
              550  LOAD_FAST                'self'
              552  LOAD_ATTR                lwgtarget
              554  LOAD_METHOD              selectedItems
              556  CALL_METHOD_0         0  '0 positional arguments'
              558  CALL_FUNCTION_1       1  '1 positional argument'
              560  LOAD_CONST               1
              562  COMPARE_OP               <
          564_566  POP_JUMP_IF_FALSE   604  'to 604'

 L. 530       568  LOAD_GLOBAL              vis_msg
              570  LOAD_ATTR                print
              572  LOAD_STR                 'ERROR in ApplyMl2DWdcnn4Prob: No target class specified'
              574  LOAD_STR                 'error'
              576  LOAD_CONST               ('type',)
              578  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              580  POP_TOP          

 L. 531       582  LOAD_GLOBAL              QtWidgets
              584  LOAD_ATTR                QMessageBox
              586  LOAD_METHOD              critical
              588  LOAD_FAST                'self'
              590  LOAD_ATTR                msgbox

 L. 532       592  LOAD_STR                 'Apply 2D-WDCNN'

 L. 533       594  LOAD_STR                 'No target class specified'
              596  CALL_METHOD_3         3  '3 positional arguments'
              598  POP_TOP          

 L. 534       600  LOAD_CONST               None
              602  RETURN_VALUE     
            604_0  COME_FROM           564  '564'

 L. 535       604  LOAD_LISTCOMP            '<code_object <listcomp>>'
              606  LOAD_STR                 'applyml2dwdcnn4prob.clickBtnApplyMl2DWdcnn4Prob.<locals>.<listcomp>'
              608  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              610  LOAD_FAST                'self'
              612  LOAD_ATTR                lwgtarget
              614  LOAD_METHOD              selectedItems
              616  CALL_METHOD_0         0  '0 positional arguments'
              618  GET_ITER         
              620  CALL_FUNCTION_1       1  '1 positional argument'
              622  STORE_FAST               '_classlist'

 L. 536       624  SETUP_LOOP          778  'to 778'
              626  LOAD_FAST                '_classlist'
              628  GET_ITER         
            630_0  COME_FROM           766  '766'
            630_1  COME_FROM           686  '686'
            630_2  COME_FROM           660  '660'
              630  FOR_ITER            776  'to 776'
              632  STORE_FAST               '_class'

 L. 537       634  LOAD_FAST                'self'
              636  LOAD_ATTR                ldtsave
              638  LOAD_METHOD              text
              640  CALL_METHOD_0         0  '0 positional arguments'
              642  LOAD_GLOBAL              str
              644  LOAD_FAST                '_class'
              646  CALL_FUNCTION_1       1  '1 positional argument'
              648  BINARY_ADD       
              650  LOAD_FAST                'self'
              652  LOAD_ATTR                seisdata
              654  LOAD_METHOD              keys
              656  CALL_METHOD_0         0  '0 positional arguments'
              658  COMPARE_OP               in
          660_662  POP_JUMP_IF_FALSE   630  'to 630'

 L. 538       664  LOAD_FAST                'self'
              666  LOAD_METHOD              checkSeisData
              668  LOAD_FAST                'self'
              670  LOAD_ATTR                ldtsave
              672  LOAD_METHOD              text
              674  CALL_METHOD_0         0  '0 positional arguments'
              676  LOAD_GLOBAL              str
              678  LOAD_FAST                '_class'
              680  CALL_FUNCTION_1       1  '1 positional argument'
              682  BINARY_ADD       
              684  CALL_METHOD_1         1  '1 positional argument'
          686_688  POP_JUMP_IF_FALSE   630  'to 630'

 L. 539       690  LOAD_GLOBAL              QtWidgets
              692  LOAD_ATTR                QMessageBox
              694  LOAD_METHOD              question
              696  LOAD_FAST                'self'
              698  LOAD_ATTR                msgbox
              700  LOAD_STR                 'Apply 2D-WDCNN'

 L. 540       702  LOAD_FAST                'self'
              704  LOAD_ATTR                ldtsave
              706  LOAD_METHOD              text
              708  CALL_METHOD_0         0  '0 positional arguments'
              710  LOAD_STR                 ' already exists. Overwrite?'
              712  BINARY_ADD       

 L. 541       714  LOAD_GLOBAL              QtWidgets
              716  LOAD_ATTR                QMessageBox
              718  LOAD_ATTR                Yes
              720  LOAD_GLOBAL              QtWidgets
              722  LOAD_ATTR                QMessageBox
              724  LOAD_ATTR                No
              726  BINARY_OR        

 L. 542       728  LOAD_GLOBAL              QtWidgets
              730  LOAD_ATTR                QMessageBox
              732  LOAD_ATTR                No
              734  CALL_METHOD_5         5  '5 positional arguments'
              736  STORE_FAST               'reply'

 L. 543       738  LOAD_FAST                'reply'
              740  LOAD_GLOBAL              QtWidgets
              742  LOAD_ATTR                QMessageBox
              744  LOAD_ATTR                No
              746  COMPARE_OP               ==
          748_750  POP_JUMP_IF_FALSE   756  'to 756'

 L. 544       752  LOAD_CONST               None
              754  RETURN_VALUE     
            756_0  COME_FROM           748  '748'

 L. 545       756  LOAD_FAST                'reply'
              758  LOAD_GLOBAL              QtWidgets
              760  LOAD_ATTR                QMessageBox
              762  LOAD_ATTR                Yes
              764  COMPARE_OP               ==
          766_768  POP_JUMP_IF_FALSE   630  'to 630'

 L. 546       770  BREAK_LOOP       
          772_774  JUMP_BACK           630  'to 630'
              776  POP_BLOCK        
            778_0  COME_FROM_LOOP      624  '624'

 L. 548       778  LOAD_FAST                'self'
              780  LOAD_ATTR                survinfo
              782  STORE_FAST               '_seisinfo'

 L. 550       784  LOAD_CONST               0
              786  STORE_FAST               '_nsample'

 L. 551       788  LOAD_FAST                'self'
              790  LOAD_ATTR                cbbornt
              792  LOAD_METHOD              currentIndex
              794  CALL_METHOD_0         0  '0 positional arguments'
              796  LOAD_CONST               0
              798  COMPARE_OP               ==
          800_802  POP_JUMP_IF_FALSE   812  'to 812'

 L. 552       804  LOAD_FAST                '_seisinfo'
              806  LOAD_STR                 'ILNum'
              808  BINARY_SUBSCR    
              810  STORE_FAST               '_nsample'
            812_0  COME_FROM           800  '800'

 L. 553       812  LOAD_FAST                'self'
              814  LOAD_ATTR                cbbornt
              816  LOAD_METHOD              currentIndex
              818  CALL_METHOD_0         0  '0 positional arguments'
              820  LOAD_CONST               1
              822  COMPARE_OP               ==
          824_826  POP_JUMP_IF_FALSE   836  'to 836'

 L. 554       828  LOAD_FAST                '_seisinfo'
              830  LOAD_STR                 'XLNum'
              832  BINARY_SUBSCR    
              834  STORE_FAST               '_nsample'
            836_0  COME_FROM           824  '824'

 L. 555       836  LOAD_FAST                'self'
              838  LOAD_ATTR                cbbornt
              840  LOAD_METHOD              currentIndex
              842  CALL_METHOD_0         0  '0 positional arguments'
              844  LOAD_CONST               2
              846  COMPARE_OP               ==
          848_850  POP_JUMP_IF_FALSE   860  'to 860'

 L. 556       852  LOAD_FAST                '_seisinfo'
              854  LOAD_STR                 'ZNum'
              856  BINARY_SUBSCR    
              858  STORE_FAST               '_nsample'
            860_0  COME_FROM           848  '848'

 L. 558       860  LOAD_GLOBAL              int
              862  LOAD_GLOBAL              np
              864  LOAD_METHOD              ceil
              866  LOAD_FAST                '_nsample'
              868  LOAD_FAST                '_batch'
              870  BINARY_TRUE_DIVIDE
              872  CALL_METHOD_1         1  '1 positional argument'
              874  CALL_FUNCTION_1       1  '1 positional argument'
              876  STORE_FAST               '_nloop'

 L. 561       878  LOAD_GLOBAL              QtWidgets
              880  LOAD_METHOD              QProgressDialog
              882  CALL_METHOD_0         0  '0 positional arguments'
              884  STORE_FAST               '_pgsdlg'

 L. 562       886  LOAD_GLOBAL              QtGui
              888  LOAD_METHOD              QIcon
              890  CALL_METHOD_0         0  '0 positional arguments'
              892  STORE_FAST               'icon'

 L. 563       894  LOAD_FAST                'icon'
              896  LOAD_METHOD              addPixmap
              898  LOAD_GLOBAL              QtGui
              900  LOAD_METHOD              QPixmap
              902  LOAD_GLOBAL              os
              904  LOAD_ATTR                path
              906  LOAD_METHOD              join
              908  LOAD_FAST                'self'
              910  LOAD_ATTR                iconpath
              912  LOAD_STR                 'icons/check.png'
              914  CALL_METHOD_2         2  '2 positional arguments'
              916  CALL_METHOD_1         1  '1 positional argument'

 L. 564       918  LOAD_GLOBAL              QtGui
              920  LOAD_ATTR                QIcon
              922  LOAD_ATTR                Normal
              924  LOAD_GLOBAL              QtGui
              926  LOAD_ATTR                QIcon
              928  LOAD_ATTR                Off
              930  CALL_METHOD_3         3  '3 positional arguments'
              932  POP_TOP          

 L. 565       934  LOAD_FAST                '_pgsdlg'
              936  LOAD_METHOD              setWindowIcon
              938  LOAD_FAST                'icon'
              940  CALL_METHOD_1         1  '1 positional argument'
              942  POP_TOP          

 L. 566       944  LOAD_FAST                '_pgsdlg'
              946  LOAD_METHOD              setWindowTitle
              948  LOAD_STR                 'Apply 2D-WDCNN'
              950  CALL_METHOD_1         1  '1 positional argument'
              952  POP_TOP          

 L. 567       954  LOAD_FAST                '_pgsdlg'
              956  LOAD_METHOD              setCancelButton
              958  LOAD_CONST               None
              960  CALL_METHOD_1         1  '1 positional argument'
              962  POP_TOP          

 L. 568       964  LOAD_FAST                '_pgsdlg'
              966  LOAD_METHOD              setWindowFlags
              968  LOAD_GLOBAL              QtCore
              970  LOAD_ATTR                Qt
              972  LOAD_ATTR                WindowStaysOnTopHint
              974  CALL_METHOD_1         1  '1 positional argument'
              976  POP_TOP          

 L. 569       978  LOAD_FAST                '_pgsdlg'
              980  LOAD_METHOD              forceShow
              982  CALL_METHOD_0         0  '0 positional arguments'
              984  POP_TOP          

 L. 570       986  LOAD_FAST                '_pgsdlg'
              988  LOAD_METHOD              setFixedWidth
              990  LOAD_CONST               400
              992  CALL_METHOD_1         1  '1 positional argument'
              994  POP_TOP          

 L. 571       996  LOAD_FAST                '_pgsdlg'
              998  LOAD_METHOD              setMaximum
             1000  LOAD_FAST                '_nloop'
             1002  CALL_METHOD_1         1  '1 positional argument'
             1004  POP_TOP          

 L. 573      1006  LOAD_GLOBAL              np
             1008  LOAD_METHOD              zeros
             1010  LOAD_FAST                '_nsample'
             1012  LOAD_GLOBAL              len
             1014  LOAD_FAST                '_classlist'
             1016  CALL_FUNCTION_1       1  '1 positional argument'
             1018  LOAD_FAST                '_image_height'
             1020  LOAD_FAST                '_image_width'
             1022  BINARY_MULTIPLY  
             1024  BUILD_LIST_3          3 
             1026  CALL_METHOD_1         1  '1 positional argument'
             1028  STORE_FAST               '_result'

 L. 574      1030  LOAD_CONST               0
             1032  STORE_FAST               'idxstart'

 L. 575  1034_1036  SETUP_LOOP         1704  'to 1704'
             1038  LOAD_GLOBAL              range
             1040  LOAD_FAST                '_nloop'
             1042  CALL_FUNCTION_1       1  '1 positional argument'
             1044  GET_ITER         
         1046_1048  FOR_ITER           1702  'to 1702'
             1050  STORE_FAST               'i'

 L. 577      1052  LOAD_GLOBAL              QtCore
             1054  LOAD_ATTR                QCoreApplication
             1056  LOAD_METHOD              instance
             1058  CALL_METHOD_0         0  '0 positional arguments'
             1060  LOAD_METHOD              processEvents
             1062  CALL_METHOD_0         0  '0 positional arguments'
             1064  POP_TOP          

 L. 579      1066  LOAD_GLOBAL              sys
             1068  LOAD_ATTR                stdout
             1070  LOAD_METHOD              write

 L. 580      1072  LOAD_STR                 '\r>>> Apply 2D-WDCNN, proceeding %.1f%% '
             1074  LOAD_GLOBAL              float
             1076  LOAD_FAST                'i'
             1078  CALL_FUNCTION_1       1  '1 positional argument'
             1080  LOAD_GLOBAL              float
             1082  LOAD_FAST                '_nloop'
             1084  CALL_FUNCTION_1       1  '1 positional argument'
             1086  BINARY_TRUE_DIVIDE
             1088  LOAD_CONST               100.0
             1090  BINARY_MULTIPLY  
             1092  BINARY_MODULO    
             1094  CALL_METHOD_1         1  '1 positional argument'
             1096  POP_TOP          

 L. 581      1098  LOAD_GLOBAL              sys
             1100  LOAD_ATTR                stdout
             1102  LOAD_METHOD              flush
             1104  CALL_METHOD_0         0  '0 positional arguments'
             1106  POP_TOP          

 L. 583      1108  LOAD_FAST                'idxstart'
             1110  LOAD_FAST                '_batch'
             1112  BINARY_ADD       
             1114  STORE_FAST               'idxend'

 L. 584      1116  LOAD_FAST                'idxend'
             1118  LOAD_FAST                '_nsample'
             1120  COMPARE_OP               >
         1122_1124  POP_JUMP_IF_FALSE  1130  'to 1130'

 L. 585      1126  LOAD_FAST                '_nsample'
             1128  STORE_FAST               'idxend'
           1130_0  COME_FROM          1122  '1122'

 L. 586      1130  LOAD_GLOBAL              np
             1132  LOAD_METHOD              linspace
             1134  LOAD_FAST                'idxstart'
             1136  LOAD_FAST                'idxend'
             1138  LOAD_CONST               1
             1140  BINARY_SUBTRACT  
             1142  LOAD_FAST                'idxend'
             1144  LOAD_FAST                'idxstart'
             1146  BINARY_SUBTRACT  
             1148  CALL_METHOD_3         3  '3 positional arguments'
             1150  LOAD_METHOD              astype
             1152  LOAD_GLOBAL              int
             1154  CALL_METHOD_1         1  '1 positional argument'
             1156  STORE_FAST               'idxlist'

 L. 587      1158  LOAD_FAST                'idxend'
             1160  STORE_FAST               'idxstart'

 L. 589      1162  BUILD_MAP_0           0 
             1164  STORE_FAST               '_dict'

 L. 590  1166_1168  SETUP_LOOP         1466  'to 1466'
             1170  LOAD_FAST                '_features'
             1172  GET_ITER         
           1174_0  COME_FROM          1388  '1388'
         1174_1176  FOR_ITER           1464  'to 1464'
             1178  STORE_FAST               'f'

 L. 591      1180  LOAD_FAST                'self'
             1182  LOAD_ATTR                seisdata
             1184  LOAD_FAST                'f'
             1186  BINARY_SUBSCR    
             1188  STORE_FAST               '_data'

 L. 592      1190  LOAD_GLOBAL              np
             1192  LOAD_METHOD              transpose
             1194  LOAD_FAST                '_data'
             1196  LOAD_CONST               2
             1198  LOAD_CONST               1
             1200  LOAD_CONST               0
             1202  BUILD_LIST_3          3 
             1204  CALL_METHOD_2         2  '2 positional arguments'
             1206  STORE_FAST               '_data'

 L. 593      1208  LOAD_FAST                'self'
             1210  LOAD_ATTR                cbbornt
             1212  LOAD_METHOD              currentIndex
             1214  CALL_METHOD_0         0  '0 positional arguments'
             1216  LOAD_CONST               0
             1218  COMPARE_OP               ==
         1220_1222  POP_JUMP_IF_FALSE  1292  'to 1292'

 L. 594      1224  LOAD_FAST                '_data'
             1226  LOAD_FAST                'idxlist'
             1228  LOAD_CONST               None
             1230  LOAD_CONST               None
             1232  BUILD_SLICE_2         2 
             1234  LOAD_CONST               None
             1236  LOAD_CONST               None
             1238  BUILD_SLICE_2         2 
             1240  BUILD_TUPLE_3         3 
             1242  BINARY_SUBSCR    
             1244  STORE_FAST               '_data'

 L. 595      1246  LOAD_GLOBAL              np
             1248  LOAD_METHOD              reshape
             1250  LOAD_GLOBAL              np
             1252  LOAD_METHOD              transpose
             1254  LOAD_FAST                '_data'
             1256  LOAD_CONST               0
             1258  LOAD_CONST               2
             1260  LOAD_CONST               1
             1262  BUILD_LIST_3          3 
             1264  CALL_METHOD_2         2  '2 positional arguments'

 L. 596      1266  LOAD_CONST               -1
             1268  LOAD_FAST                '_seisinfo'
             1270  LOAD_STR                 'XLNum'
             1272  BINARY_SUBSCR    
             1274  LOAD_FAST                '_seisinfo'
             1276  LOAD_STR                 'ZNum'
             1278  BINARY_SUBSCR    
             1280  BINARY_MULTIPLY  
             1282  BUILD_LIST_2          2 
             1284  CALL_METHOD_2         2  '2 positional arguments'
             1286  LOAD_FAST                '_dict'
             1288  LOAD_FAST                'f'
             1290  STORE_SUBSCR     
           1292_0  COME_FROM          1220  '1220'

 L. 597      1292  LOAD_FAST                'self'
             1294  LOAD_ATTR                cbbornt
             1296  LOAD_METHOD              currentIndex
             1298  CALL_METHOD_0         0  '0 positional arguments'
             1300  LOAD_CONST               1
             1302  COMPARE_OP               ==
         1304_1306  POP_JUMP_IF_FALSE  1376  'to 1376'

 L. 598      1308  LOAD_FAST                '_data'
             1310  LOAD_CONST               None
             1312  LOAD_CONST               None
             1314  BUILD_SLICE_2         2 
             1316  LOAD_FAST                'idxlist'
             1318  LOAD_CONST               None
             1320  LOAD_CONST               None
             1322  BUILD_SLICE_2         2 
             1324  BUILD_TUPLE_3         3 
             1326  BINARY_SUBSCR    
             1328  STORE_FAST               '_data'

 L. 599      1330  LOAD_GLOBAL              np
             1332  LOAD_METHOD              reshape
             1334  LOAD_GLOBAL              np
             1336  LOAD_METHOD              transpose
             1338  LOAD_FAST                '_data'
             1340  LOAD_CONST               1
             1342  LOAD_CONST               2
             1344  LOAD_CONST               0
             1346  BUILD_LIST_3          3 
             1348  CALL_METHOD_2         2  '2 positional arguments'

 L. 600      1350  LOAD_CONST               -1
             1352  LOAD_FAST                '_seisinfo'
             1354  LOAD_STR                 'ILNum'
             1356  BINARY_SUBSCR    
             1358  LOAD_FAST                '_seisinfo'
             1360  LOAD_STR                 'ZNum'
             1362  BINARY_SUBSCR    
             1364  BINARY_MULTIPLY  
             1366  BUILD_LIST_2          2 
             1368  CALL_METHOD_2         2  '2 positional arguments'
             1370  LOAD_FAST                '_dict'
             1372  LOAD_FAST                'f'
             1374  STORE_SUBSCR     
           1376_0  COME_FROM          1304  '1304'

 L. 601      1376  LOAD_FAST                'self'
             1378  LOAD_ATTR                cbbornt
             1380  LOAD_METHOD              currentIndex
             1382  CALL_METHOD_0         0  '0 positional arguments'
             1384  LOAD_CONST               2
             1386  COMPARE_OP               ==
         1388_1390  POP_JUMP_IF_FALSE  1174  'to 1174'

 L. 602      1392  LOAD_FAST                '_data'
             1394  LOAD_CONST               None
             1396  LOAD_CONST               None
             1398  BUILD_SLICE_2         2 
             1400  LOAD_CONST               None
             1402  LOAD_CONST               None
             1404  BUILD_SLICE_2         2 
             1406  LOAD_FAST                'idxlist'
             1408  BUILD_TUPLE_3         3 
             1410  BINARY_SUBSCR    
             1412  STORE_FAST               '_data'

 L. 603      1414  LOAD_GLOBAL              np
             1416  LOAD_METHOD              reshape
             1418  LOAD_GLOBAL              np
             1420  LOAD_METHOD              transpose
             1422  LOAD_FAST                '_data'
             1424  LOAD_CONST               2
             1426  LOAD_CONST               1
             1428  LOAD_CONST               0
             1430  BUILD_LIST_3          3 
             1432  CALL_METHOD_2         2  '2 positional arguments'

 L. 604      1434  LOAD_CONST               -1
             1436  LOAD_FAST                '_seisinfo'
             1438  LOAD_STR                 'ILNum'
             1440  BINARY_SUBSCR    
             1442  LOAD_FAST                '_seisinfo'
             1444  LOAD_STR                 'XLNum'
             1446  BINARY_SUBSCR    
             1448  BINARY_MULTIPLY  
             1450  BUILD_LIST_2          2 
             1452  CALL_METHOD_2         2  '2 positional arguments'
             1454  LOAD_FAST                '_dict'
             1456  LOAD_FAST                'f'
             1458  STORE_SUBSCR     
         1460_1462  JUMP_BACK          1174  'to 1174'
             1464  POP_BLOCK        
           1466_0  COME_FROM_LOOP     1166  '1166'

 L. 606      1466  LOAD_FAST                '_image_height_new'
             1468  LOAD_FAST                '_image_height'
             1470  COMPARE_OP               !=
         1472_1474  POP_JUMP_IF_TRUE   1486  'to 1486'
             1476  LOAD_FAST                '_image_width_new'
             1478  LOAD_FAST                '_image_width'
             1480  COMPARE_OP               !=
         1482_1484  POP_JUMP_IF_FALSE  1530  'to 1530'
           1486_0  COME_FROM          1472  '1472'

 L. 607      1486  SETUP_LOOP         1530  'to 1530'
             1488  LOAD_FAST                '_features'
             1490  GET_ITER         
             1492  FOR_ITER           1528  'to 1528'
             1494  STORE_FAST               'f'

 L. 608      1496  LOAD_GLOBAL              basic_image
             1498  LOAD_ATTR                changeImageSize
             1500  LOAD_FAST                '_dict'
             1502  LOAD_FAST                'f'
             1504  BINARY_SUBSCR    

 L. 609      1506  LOAD_FAST                '_image_height'

 L. 610      1508  LOAD_FAST                '_image_width'

 L. 611      1510  LOAD_FAST                '_image_height_new'

 L. 612      1512  LOAD_FAST                '_image_width_new'
             1514  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1516  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1518  LOAD_FAST                '_dict'
             1520  LOAD_FAST                'f'
             1522  STORE_SUBSCR     
         1524_1526  JUMP_BACK          1492  'to 1492'
             1528  POP_BLOCK        
           1530_0  COME_FROM_LOOP     1486  '1486'
           1530_1  COME_FROM          1482  '1482'

 L. 614      1530  LOAD_GLOBAL              ml_wdcnn
             1532  LOAD_ATTR                probabilityFromWDCNNSegmentor
             1534  LOAD_FAST                '_dict'

 L. 615      1536  LOAD_FAST                '_image_height_new'
             1538  LOAD_FAST                '_image_width_new'

 L. 616      1540  LOAD_FAST                'self'
             1542  LOAD_ATTR                modelpath

 L. 617      1544  LOAD_FAST                'self'
             1546  LOAD_ATTR                modelname

 L. 618      1548  LOAD_FAST                '_classlist'

 L. 619      1550  LOAD_FAST                '_batch'
             1552  LOAD_CONST               True
             1554  LOAD_CONST               ('imageheight', 'imagewidth', 'wdcnnpath', 'wdcnnname', 'targetlist', 'batchsize', 'verbose')
             1556  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
             1558  STORE_FAST               '_rst'

 L. 622      1560  LOAD_FAST                '_image_height_new'
             1562  LOAD_FAST                '_image_height'
             1564  COMPARE_OP               !=
         1566_1568  POP_JUMP_IF_TRUE   1580  'to 1580'
             1570  LOAD_FAST                '_image_width_new'
             1572  LOAD_FAST                '_image_width'
             1574  COMPARE_OP               !=
         1576_1578  POP_JUMP_IF_FALSE  1640  'to 1640'
           1580_0  COME_FROM          1566  '1566'

 L. 623      1580  LOAD_GLOBAL              np
             1582  LOAD_METHOD              reshape
             1584  LOAD_FAST                '_rst'
             1586  LOAD_GLOBAL              np
             1588  LOAD_METHOD              shape
             1590  LOAD_FAST                '_rst'
             1592  CALL_METHOD_1         1  '1 positional argument'
             1594  LOAD_CONST               0
             1596  BINARY_SUBSCR    
             1598  LOAD_GLOBAL              len
             1600  LOAD_FAST                '_classlist'
             1602  CALL_FUNCTION_1       1  '1 positional argument'
             1604  BINARY_MULTIPLY  
             1606  LOAD_FAST                '_image_height_new'
             1608  LOAD_FAST                '_image_width_new'
             1610  BINARY_MULTIPLY  
             1612  BUILD_LIST_2          2 
             1614  CALL_METHOD_2         2  '2 positional arguments'
             1616  STORE_FAST               '_rst'

 L. 624      1618  LOAD_GLOBAL              basic_image
             1620  LOAD_ATTR                changeImageSize
             1622  LOAD_FAST                '_rst'

 L. 625      1624  LOAD_FAST                '_image_height_new'

 L. 626      1626  LOAD_FAST                '_image_width_new'

 L. 627      1628  LOAD_FAST                '_image_height'

 L. 628      1630  LOAD_FAST                '_image_width'
             1632  LOAD_STR                 'linear'
             1634  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             1636  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1638  STORE_FAST               '_rst'
           1640_0  COME_FROM          1576  '1576'

 L. 630      1640  LOAD_GLOBAL              np
             1642  LOAD_METHOD              reshape
             1644  LOAD_FAST                '_rst'
             1646  LOAD_CONST               -1
             1648  LOAD_GLOBAL              len
             1650  LOAD_FAST                '_classlist'
             1652  CALL_FUNCTION_1       1  '1 positional argument'
             1654  LOAD_FAST                '_image_height'
             1656  LOAD_FAST                '_image_width'
             1658  BINARY_MULTIPLY  
             1660  BUILD_LIST_3          3 
             1662  CALL_METHOD_2         2  '2 positional arguments'
             1664  LOAD_FAST                '_result'
             1666  LOAD_FAST                'idxlist'
             1668  LOAD_CONST               None
             1670  LOAD_CONST               None
             1672  BUILD_SLICE_2         2 
             1674  LOAD_CONST               None
             1676  LOAD_CONST               None
             1678  BUILD_SLICE_2         2 
             1680  BUILD_TUPLE_3         3 
             1682  STORE_SUBSCR     

 L. 633      1684  LOAD_FAST                '_pgsdlg'
             1686  LOAD_METHOD              setValue
             1688  LOAD_FAST                'i'
             1690  LOAD_CONST               1
             1692  BINARY_ADD       
             1694  CALL_METHOD_1         1  '1 positional argument'
             1696  POP_TOP          
         1698_1700  JUMP_BACK          1046  'to 1046'
             1702  POP_BLOCK        
           1704_0  COME_FROM_LOOP     1034  '1034'

 L. 635      1704  LOAD_GLOBAL              print
             1706  LOAD_STR                 'Done'
             1708  CALL_FUNCTION_1       1  '1 positional argument'
             1710  POP_TOP          

 L. 637      1712  LOAD_FAST                'self'
             1714  LOAD_ATTR                survinfo
             1716  STORE_FAST               '_info'

 L. 638      1718  LOAD_FAST                '_info'
             1720  LOAD_STR                 'ILNum'
             1722  BINARY_SUBSCR    
             1724  STORE_FAST               '_inlnum'

 L. 639      1726  LOAD_FAST                '_info'
             1728  LOAD_STR                 'XLNum'
             1730  BINARY_SUBSCR    
             1732  STORE_FAST               '_xlnum'

 L. 640      1734  LOAD_FAST                '_info'
             1736  LOAD_STR                 'ZNum'
             1738  BINARY_SUBSCR    
             1740  STORE_FAST               '_znum'

 L. 641      1742  SETUP_LOOP         1986  'to 1986'
             1744  LOAD_GLOBAL              range
             1746  LOAD_GLOBAL              len
             1748  LOAD_FAST                '_classlist'
             1750  CALL_FUNCTION_1       1  '1 positional argument'
             1752  CALL_FUNCTION_1       1  '1 positional argument'
             1754  GET_ITER         
             1756  FOR_ITER           1984  'to 1984'
             1758  STORE_FAST               'i'

 L. 642      1760  LOAD_FAST                'self'
             1762  LOAD_ATTR                cbbornt
             1764  LOAD_METHOD              currentIndex
             1766  CALL_METHOD_0         0  '0 positional arguments'
             1768  LOAD_CONST               0
             1770  COMPARE_OP               ==
         1772_1774  POP_JUMP_IF_FALSE  1830  'to 1830'

 L. 643      1776  LOAD_GLOBAL              np
             1778  LOAD_METHOD              reshape
             1780  LOAD_FAST                '_result'
             1782  LOAD_CONST               None
             1784  LOAD_CONST               None
             1786  BUILD_SLICE_2         2 
             1788  LOAD_FAST                'i'
             1790  LOAD_CONST               None
             1792  LOAD_CONST               None
             1794  BUILD_SLICE_2         2 
             1796  BUILD_TUPLE_3         3 
             1798  BINARY_SUBSCR    
             1800  LOAD_CONST               -1
             1802  LOAD_FAST                '_znum'
             1804  LOAD_FAST                '_xlnum'
             1806  BUILD_LIST_3          3 
             1808  CALL_METHOD_2         2  '2 positional arguments'
             1810  STORE_FAST               '_rst'

 L. 644      1812  LOAD_GLOBAL              np
             1814  LOAD_METHOD              transpose
             1816  LOAD_FAST                '_rst'
             1818  LOAD_CONST               1
             1820  LOAD_CONST               2
             1822  LOAD_CONST               0
             1824  BUILD_LIST_3          3 
             1826  CALL_METHOD_2         2  '2 positional arguments'
             1828  STORE_FAST               '_rst'
           1830_0  COME_FROM          1772  '1772'

 L. 645      1830  LOAD_FAST                'self'
             1832  LOAD_ATTR                cbbornt
             1834  LOAD_METHOD              currentIndex
             1836  CALL_METHOD_0         0  '0 positional arguments'
             1838  LOAD_CONST               1
             1840  COMPARE_OP               ==
         1842_1844  POP_JUMP_IF_FALSE  1900  'to 1900'

 L. 646      1846  LOAD_GLOBAL              np
             1848  LOAD_METHOD              reshape
             1850  LOAD_FAST                '_result'
             1852  LOAD_CONST               None
             1854  LOAD_CONST               None
             1856  BUILD_SLICE_2         2 
             1858  LOAD_FAST                'i'
             1860  LOAD_CONST               None
             1862  LOAD_CONST               None
             1864  BUILD_SLICE_2         2 
             1866  BUILD_TUPLE_3         3 
             1868  BINARY_SUBSCR    
             1870  LOAD_CONST               -1
             1872  LOAD_FAST                '_znum'
             1874  LOAD_FAST                '_inlnum'
             1876  BUILD_LIST_3          3 
             1878  CALL_METHOD_2         2  '2 positional arguments'
             1880  STORE_FAST               '_rst'

 L. 647      1882  LOAD_GLOBAL              np
             1884  LOAD_METHOD              transpose
             1886  LOAD_FAST                '_rst'
             1888  LOAD_CONST               1
             1890  LOAD_CONST               0
             1892  LOAD_CONST               2
             1894  BUILD_LIST_3          3 
             1896  CALL_METHOD_2         2  '2 positional arguments'
             1898  STORE_FAST               '_rst'
           1900_0  COME_FROM          1842  '1842'

 L. 648      1900  LOAD_FAST                'self'
             1902  LOAD_ATTR                cbbornt
             1904  LOAD_METHOD              currentIndex
             1906  CALL_METHOD_0         0  '0 positional arguments'
             1908  LOAD_CONST               2
             1910  COMPARE_OP               ==
         1912_1914  POP_JUMP_IF_FALSE  1952  'to 1952'

 L. 649      1916  LOAD_GLOBAL              np
             1918  LOAD_METHOD              reshape
             1920  LOAD_FAST                '_result'
             1922  LOAD_CONST               None
             1924  LOAD_CONST               None
             1926  BUILD_SLICE_2         2 
             1928  LOAD_FAST                'i'
             1930  LOAD_CONST               None
             1932  LOAD_CONST               None
             1934  BUILD_SLICE_2         2 
             1936  BUILD_TUPLE_3         3 
             1938  BINARY_SUBSCR    
             1940  LOAD_CONST               -1
             1942  LOAD_FAST                '_xlnum'
             1944  LOAD_FAST                '_inlnum'
             1946  BUILD_LIST_3          3 
             1948  CALL_METHOD_2         2  '2 positional arguments'
             1950  STORE_FAST               '_rst'
           1952_0  COME_FROM          1912  '1912'

 L. 651      1952  LOAD_FAST                '_rst'
             1954  LOAD_FAST                'self'
             1956  LOAD_ATTR                seisdata
             1958  LOAD_FAST                'self'
             1960  LOAD_ATTR                ldtsave
             1962  LOAD_METHOD              text
             1964  CALL_METHOD_0         0  '0 positional arguments'
             1966  LOAD_GLOBAL              str
             1968  LOAD_FAST                '_classlist'
             1970  LOAD_FAST                'i'
             1972  BINARY_SUBSCR    
             1974  CALL_FUNCTION_1       1  '1 positional argument'
             1976  BINARY_ADD       
             1978  STORE_SUBSCR     
         1980_1982  JUMP_BACK          1756  'to 1756'
             1984  POP_BLOCK        
           1986_0  COME_FROM_LOOP     1742  '1742'

 L. 653      1986  LOAD_GLOBAL              QtWidgets
             1988  LOAD_ATTR                QMessageBox
             1990  LOAD_METHOD              information
             1992  LOAD_FAST                'self'
             1994  LOAD_ATTR                msgbox

 L. 654      1996  LOAD_STR                 'Apply 2D-WDCNN'

 L. 655      1998  LOAD_STR                 'WDCNN applied successfully'
             2000  CALL_METHOD_3         3  '3 positional arguments'
             2002  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 2000

    def getImageSize(self, feature):
        _shape = [
         0, 0]
        if self.checkSurvInfo():
            if feature in self.seisdata.keys():
                if self.checkSeisData(feature):
                    _info = self.survinfo
                    if self.cbbornt.currentIndex() == 0:
                        _shape = [
                         _info['ZNum'], _info['XLNum']]
                    if self.cbbornt.currentIndex() == 1:
                        _shape = [
                         _info['ZNum'], _info['ILNum']]
                    if self.cbbornt.currentIndex() == 2:
                        _shape = [
                         _info['XLNum'], _info['ILNum']]
        return _shape

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
    ApplyMl2DWdcnn4Prob = QtWidgets.QWidget()
    gui = applyml2dwdcnn4prob()
    gui.setupGUI(ApplyMl2DWdcnn4Prob)
    ApplyMl2DWdcnn4Prob.show()
    sys.exit(app.exec_())