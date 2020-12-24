# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\applyml15dwdcnn4pred.py
# Compiled at: 2019-12-15 20:31:46
# Size of source mod 2**32: 36764 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, numpy.matlib as npmat, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.basic.data import data as basic_data
from cognitivegeo.src.seismic.analysis import analysis as seis_ays
from cognitivegeo.src.basic.matdict import matdict as basic_mdt
from cognitivegeo.src.basic.curve import curve as basic_curve
from cognitivegeo.src.basic.image import image as basic_image
from cognitivegeo.src.vis.messager import messager as vis_msg
from cognitivegeo.src.ml.tfmodel import tfmodel as ml_tfm
from cognitivegeo.src.ml.wdcnnsegmentor15d import wdcnnsegmentor15d as ml_wdcnn15d
from cognitivegeo.src.gui.viewml2dwdcnn import viewml2dwdcnn as gui_viewml2dwdcnn
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class applyml15dwdcnn4pred(object):
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

    def setupGUI(self, ApplyMl15DWdcnn4Pred):
        ApplyMl15DWdcnn4Pred.setObjectName('ApplyMl15DWdcnn4Pred')
        ApplyMl15DWdcnn4Pred.setFixedSize(810, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ApplyMl15DWdcnn4Pred.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ApplyMl15DWdcnn4Pred)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ApplyMl15DWdcnn4Pred)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ApplyMl15DWdcnn4Pred)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(ApplyMl15DWdcnn4Pred)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 230, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 230, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(ApplyMl15DWdcnn4Pred)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 230, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 270, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(ApplyMl15DWdcnn4Pred)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 270, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 230, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(ApplyMl15DWdcnn4Pred)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(ApplyMl15DWdcnn4Pred)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ApplyMl15DWdcnn4Pred)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ApplyMl15DWdcnn4Pred)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ApplyMl15DWdcnn4Pred)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 190))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(ApplyMl15DWdcnn4Pred)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(ApplyMl15DWdcnn4Pred)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 190))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 350, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 350, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ApplyMl15DWdcnn4Pred)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 350, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 390, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ApplyMl15DWdcnn4Pred)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 390, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 350, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 350, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ApplyMl15DWdcnn4Pred)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 350, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 390, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ApplyMl15DWdcnn4Pred)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 390, 40, 30))
        self.lblpara = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 320, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ApplyMl15DWdcnn4Pred)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblsave = QtWidgets.QLabel(ApplyMl15DWdcnn4Pred)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ApplyMl15DWdcnn4Pred)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.btnapply = QtWidgets.QPushButton(ApplyMl15DWdcnn4Pred)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(320, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ApplyMl15DWdcnn4Pred)
        self.msgbox.setObjectName('msgbox')
        _center_x = ApplyMl15DWdcnn4Pred.geometry().center().x()
        _center_y = ApplyMl15DWdcnn4Pred.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ApplyMl15DWdcnn4Pred)
        QtCore.QMetaObject.connectSlotsByName(ApplyMl15DWdcnn4Pred)

    def retranslateGUI(self, ApplyMl15DWdcnn4Pred):
        self.dialog = ApplyMl15DWdcnn4Pred
        _translate = QtCore.QCoreApplication.translate
        ApplyMl15DWdcnn4Pred.setWindowTitle(_translate('ApplyMl15DWdcnn4Pred', 'Apply 1.5D-WDCNN for prediction'))
        self.lblfrom.setText(_translate('ApplyMl15DWdcnn4Pred', 'Select network:'))
        self.ldtfrom.setText(_translate('ApplyMl15DWdcnn4Pred', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ApplyMl15DWdcnn4Pred', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ApplyMl15DWdcnn4Pred', 'Training features:'))
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblornt.setText(_translate('ApplyMl15DWdcnn4Pred', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.cbbornt.currentIndexChanged.connect(self.changeCbbOrnt)
        self.lbloldsize.setText(_translate('ApplyMl15DWdcnn4Pred', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('ApplyMl15DWdcnn4Pred', 'height='))
        self.ldtoldheight.setText(_translate('ApplyMl15DWdcnn4Pred', ''))
        self.ldtoldheight.setEnabled(False)
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('ApplyMl15DWdcnn4Pred', 'width='))
        self.ldtoldwidth.setText(_translate('ApplyMl15DWdcnn4Pred', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('ApplyMl15DWdcnn4Pred', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('ApplyMl15DWdcnn4Pred', 'height='))
        self.ldtnewheight.setText(_translate('ApplyMl15DWdcnn4Pred', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('ApplyMl15DWdcnn4Pred', 'width='))
        self.ldtnewwidth.setText(_translate('ApplyMl15DWdcnn4Pred', ''))
        self.ldtnewwidth.setEnabled(False)
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('ApplyMl15DWdcnn4Pred', 'Pre-trained WDCNN architecture:'))
        self.btnviewnetwork.setText(_translate('ApplyMl15DWdcnn4Pred', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('ApplyMl15DWdcnn4Pred', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ApplyMl15DWdcnn4Pred', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('ApplyMl15DWdcnn4Pred', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('ApplyMl15DWdcnn4Pred', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('ApplyMl15DWdcnn4Pred', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ApplyMl15DWdcnn4Pred', 'height='))
        self.ldtmaskheight.setText(_translate('ApplyMl15DWdcnn4Pred', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ApplyMl15DWdcnn4Pred', 'width='))
        self.ldtmaskwidth.setText(_translate('ApplyMl15DWdcnn4Pred', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ApplyMl15DWdcnn4Pred', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ApplyMl15DWdcnn4Pred', 'height='))
        self.ldtpoolheight.setText(_translate('ApplyMl15DWdcnn4Pred', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ApplyMl15DWdcnn4Pred', 'width='))
        self.ldtpoolwidth.setText(_translate('ApplyMl15DWdcnn4Pred', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ApplyMl15DWdcnn4Pred', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ApplyMl15DWdcnn4Pred', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ApplyMl15DWdcnn4Pred', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('ApplyMl15DWdcnn4Pred', 'Output name='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ApplyMl15DWdcnn4Pred', 'wdcnn'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('ApplyMl15DWdcnn4Pred', 'Apply 1.5D-WDCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnApplyMl15DWdcnn4Pred)

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.check15DWDCNNModel(self.modelpath, self.modelname) is True:
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
            self.btnviewnetwork.setEnabled(True)
            self.ldtnconvblock.setText(str(self.modelinfo['number_conv_block']))
            self.ldtn1x1layer.setText(str(self.modelinfo['number_1x1_layer']))
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
            self.btnviewnetwork.setEnabled(False)
            self.ldtnconvblock.setText('')
            self.ldtn1x1layer.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')

    def clickBtnFrom(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select WDCNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def changeLwgFeature(self):
        _shape = [
         0, 0]
        if ml_tfm.check15DWDCNNModel(self.modelpath, self.modelname):
            _shape = self.getImageSize(self.lwgfeature.currentItem().text())
        _height = _shape[0]
        _width = _shape[1]
        self.ldtoldheight.setText(str(_height))

    def changeCbbOrnt(self):
        _shape = [
         0, 0]
        if ml_tfm.check15DWDCNNModel(self.modelpath, self.modelname):
            _shape = self.getImageSize(self.lwgfeature.currentItem().text())
        _height = _shape[0]
        _width = _shape[1]
        self.ldtoldheight.setText(str(_height))

    def changeLdtNconvblock(self):
        if ml_tfm.check15DWDCNNModel(self.modelpath, self.modelname) is True:
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
        if ml_tfm.check15DWDCNNModel(self.modelpath, self.modelname) is True:
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

    def clickBtnApplyMl15DWdcnn4Pred(self):
        self.refreshMsgBox()
        if self.checkSurvInfo() is False:
            vis_msg.print('ERROR in ApplyMl15DWdcnn4Pred: No seismic survey available', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Apply 1.5D-WDCNN', 'No seismic survey available')
            return
        if ml_tfm.check15DWDCNNModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in ApplyMl15DWdcnn4Pred: No pre-WDCNN network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Apply 1.5D-WDCNN', 'No pre-WDCNN network found')
            return
        for f in self.modelinfo['feature_list']:
            if self.checkSeisData(f) is False:
                vis_msg.print(("ERROR in ApplyMl15DWdcnn4Pred: Feature '%s' not found in seismic data" % f), type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Apply 1.5D-WDCNN', "Feature '" + f + "' not found in seismic data")
                return

        _features = self.modelinfo['feature_list']
        _image_height = basic_data.str2int(self.ldtoldheight.text())
        _image_width = basic_data.str2int(self.ldtoldwidth.text())
        _image_height_new = basic_data.str2int(self.ldtnewheight.text())
        _image_width_new = basic_data.str2int(self.ldtnewwidth.text())
        if _image_height is False or _image_width is False or _image_height_new is False or _image_width_new is False:
            vis_msg.print('ERROR in ApplyMl15DWdcnn4Pred: Non-integer feature size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Apply 1.5D-WDCNN', 'Non-integer feature size')
            return
        if _image_height < 2 or _image_width < 2 or _image_height_new < 2 or _image_width_new < 2:
            vis_msg.print('ERROR in ApplyMl15DWdcnn4Pred: Features are not 2D', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Apply 1.5D-WDCNN', 'Features are not 2D')
            return
        _batch = basic_data.str2int(self.ldtbatchsize.text())
        if _batch is False or _batch < 1:
            vis_msg.print('ERROR in ApplyMl15DWdcnn4Pred: Non-positive batch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Apply 1.5D-WDCNN', 'Non-positive batch size')
            return
        if len(self.ldtsave.text()) < 1:
            vis_msg.print('ApplyMl15DWdcnn4Pred: No name specified', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Apply 1.5D-WDCNN', 'No name specified')
            return
        if self.ldtsave.text() in self.seisdata.keys():
            if self.checkSeisData(self.ldtsave.text()):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Apply 1.5D-WDCNN', self.ldtsave.text() + ' already exists. Overwrite?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
        _seisinfo = self.survinfo
        _wdinl = 0
        _wdxl = 0
        _wdz = 0
        if self.cbbornt.currentIndex() == 0:
            _wdxl = int(_image_width / 2)
        if self.cbbornt.currentIndex() == 1:
            _wdinl = int(_image_width / 2)
        if self.cbbornt.currentIndex() == 2:
            _wdinl = int(_image_width / 2)
        _seisdict = {}
        if self.cbbornt.currentIndex() == 0 or self.cbbornt.currentIndex() == 1:
            _all_sample = np.arange(0, _seisinfo['ILNum'] * _seisinfo['XLNum'])
            _seisdict['Inline'] = np.reshape(_seisinfo['ILRange'][(_all_sample / _seisinfo['XLNum']).astype(int)], [
             -1, 1])
            _seisdict['Crossline'] = np.reshape(_seisinfo['XLRange'][(_all_sample % _seisinfo['XLNum']).astype(int)], [
             -1, 1])
        if self.cbbornt.currentIndex() == 2:
            _all_sample = np.arange(0, _seisinfo['ILNum'] * _seisinfo['ZNum'])
            _seisdict['Inline'] = np.reshape(_seisinfo['ILRange'][(_all_sample / _seisinfo['ZNum']).astype(int)], [
             -1, 1])
            _seisdict['Z'] = np.reshape(_seisinfo['ZRange'][(_all_sample % _seisinfo['ZNum']).astype(int)], [
             -1, 1])
        _nsample = basic_mdt.maxDictConstantRow(_seisdict)
        _nloop = int(np.ceil(_nsample / _batch))
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/check.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Apply 1.5D-WDCNN')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _pgsdlg.setMaximum(_nloop)
        _result = np.zeros([_nsample, _image_height])
        idxstart = 0
        for i in range(_nloop):
            QtCore.QCoreApplication.instance().processEvents()
            sys.stdout.write('\r>>> Apply 1.5D-WDCNN, proceeding %.1f%% ' % (float(i) / float(_nloop) * 100.0))
            sys.stdout.flush()
            idxend = idxstart + _batch
            if idxend > _nsample:
                idxend = _nsample
            idxlist = np.linspace(idxstart, idxend - 1, idxend - idxstart).astype(int)
            idxstart = idxend
            _dict = basic_mdt.retrieveDictByIndex(_seisdict, idxlist)
            _targetdata = _dict['Inline']
            if self.cbbornt.currentIndex() == 0 or self.cbbornt.currentIndex() == 1:
                _targetdata = np.concatenate((_targetdata, _dict['Crossline']), axis=1)
                for f in _features:
                    _data = self.seisdata[f]
                    _data = seis_ays.retrieveSeisZTraceFrom3DMat(_data, _targetdata, seisinfo=(self.survinfo),
                      wdinl=_wdinl,
                      wdxl=_wdxl,
                      verbose=False)
                    _dict[f] = _data[:, 2:2 + _image_height * _image_width]

            if self.cbbornt.currentIndex() == 2:
                _targetdata = np.concatenate((_targetdata, _dict['Z']), axis=1)
                for f in _features:
                    _data = self.seisdata[f]
                    _data = seis_ays.retrieveSeisXLTraceFrom3DMat(_data, _targetdata, seisinfo=(self.survinfo),
                      wdinl=_wdinl,
                      wdz=_wdz,
                      verbose=False)
                    _dict[f] = _data[:, 2:2 + _image_height * _image_width]

            if _image_height_new != _image_height or _image_width_new != _image_width:
                for f in _features:
                    _dict[f] = basic_image.changeImageSize((_dict[f]), image_height=_image_height,
                      image_width=_image_width,
                      image_height_new=_image_height_new,
                      image_width_new=_image_width_new)

            _rst = ml_wdcnn15d.predictionFrom15DWDCNNSegmentor(_dict, imageheight=_image_height_new,
              imagewidth=_image_width_new,
              wdcnnpath=(self.modelpath),
              wdcnnname=(self.modelname),
              batchsize=_batch,
              verbose=False)
            if _image_height_new != _image_height:
                _result[idxlist, :] = basic_curve.changeCurveSize(_rst, length=_image_height_new,
                  length_new=_image_height,
                  kind='linear')
            else:
                _result[idxlist, :] = _rst
            _pgsdlg.setValue(i + 1)

        print('Done')
        _result = np.round(_result).astype(int)
        if self.cbbornt.currentIndex() == 0 or self.cbbornt.currentIndex() == 1:
            _result = np.reshape(_result, [_seisinfo['ILNum'], _seisinfo['XLNum'], _seisinfo['ZNum']])
            _result = np.transpose(_result, [2, 1, 0])
        if self.cbbornt.currentIndex() == 2:
            _result = np.reshape(_result, [_seisinfo['ILNum'], _seisinfo['ZNum'], _seisinfo['XLNum']])
            _result = np.transpose(_result, [1, 2, 0])
        self.seisdata[self.ldtsave.text()] = _result
        QtWidgets.QMessageBox.information(self.msgbox, 'Apply 1.5D-WDCNN', 'WDCNN applied successfully')

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
        else:
            return True

    def checkSeisData(self, f):
        self.refreshMsgBox()
        return seis_ays.isSeis3DMatConsistentWithSeisInfo(self.seisdata[f], self.survinfo)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ApplyMl15DWdcnn4Pred = QtWidgets.QWidget()
    gui = applyml15dwdcnn4pred()
    gui.setupGUI(ApplyMl15DWdcnn4Pred)
    ApplyMl15DWdcnn4Pred.show()
    sys.exit(app.exec_())