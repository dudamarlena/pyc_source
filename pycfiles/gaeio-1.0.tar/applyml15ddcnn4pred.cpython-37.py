# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\applyml15ddcnn4pred.py
# Compiled at: 2019-12-15 20:31:46
# Size of source mod 2**32: 36602 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import numpy.matlib as npmat
import os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.curve as basic_curve
import cognitivegeo.src.basic.image as basic_image
import cognitivegeo.src.vis.messager as vis_msg
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.dcnnsegmentor15d as ml_dcnn15d
import cognitivegeo.src.gui.viewml2ddcnn as gui_viewml2ddcnn
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class applyml15ddcnn4pred(object):
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

    def setupGUI(self, ApplyMl15DDcnn4Pred):
        ApplyMl15DDcnn4Pred.setObjectName('ApplyMl15DDcnn4Pred')
        ApplyMl15DDcnn4Pred.setFixedSize(810, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ApplyMl15DDcnn4Pred.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ApplyMl15DDcnn4Pred)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ApplyMl15DDcnn4Pred)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ApplyMl15DDcnn4Pred)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(ApplyMl15DDcnn4Pred)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 230, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 230, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(ApplyMl15DDcnn4Pred)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 230, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 270, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(ApplyMl15DDcnn4Pred)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 270, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 230, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(ApplyMl15DDcnn4Pred)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(ApplyMl15DDcnn4Pred)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ApplyMl15DDcnn4Pred)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ApplyMl15DDcnn4Pred)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ApplyMl15DDcnn4Pred)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 190))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(ApplyMl15DDcnn4Pred)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(ApplyMl15DDcnn4Pred)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 190))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 350, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 350, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ApplyMl15DDcnn4Pred)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 350, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 390, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ApplyMl15DDcnn4Pred)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 390, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 350, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 350, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ApplyMl15DDcnn4Pred)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 350, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 390, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ApplyMl15DDcnn4Pred)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 390, 40, 30))
        self.lblpara = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 320, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ApplyMl15DDcnn4Pred)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblsave = QtWidgets.QLabel(ApplyMl15DDcnn4Pred)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ApplyMl15DDcnn4Pred)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.btnapply = QtWidgets.QPushButton(ApplyMl15DDcnn4Pred)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(320, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ApplyMl15DDcnn4Pred)
        self.msgbox.setObjectName('msgbox')
        _center_x = ApplyMl15DDcnn4Pred.geometry().center().x()
        _center_y = ApplyMl15DDcnn4Pred.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ApplyMl15DDcnn4Pred)
        QtCore.QMetaObject.connectSlotsByName(ApplyMl15DDcnn4Pred)

    def retranslateGUI(self, ApplyMl15DDcnn4Pred):
        self.dialog = ApplyMl15DDcnn4Pred
        _translate = QtCore.QCoreApplication.translate
        ApplyMl15DDcnn4Pred.setWindowTitle(_translate('ApplyMl15DDcnn4Pred', 'Apply 1.5D-DCNN for prediction'))
        self.lblfrom.setText(_translate('ApplyMl15DDcnn4Pred', 'Select network:'))
        self.ldtfrom.setText(_translate('ApplyMl15DDcnn4Pred', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ApplyMl15DDcnn4Pred', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ApplyMl15DDcnn4Pred', 'Training features:'))
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblornt.setText(_translate('ApplyMl15DDcnn4Pred', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.cbbornt.currentIndexChanged.connect(self.changeCbbOrnt)
        self.lbloldsize.setText(_translate('ApplyMl15DDcnn4Pred', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('ApplyMl15DDcnn4Pred', 'height='))
        self.ldtoldheight.setText(_translate('ApplyMl15DDcnn4Pred', ''))
        self.ldtoldheight.setEnabled(False)
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('ApplyMl15DDcnn4Pred', 'width='))
        self.ldtoldwidth.setText(_translate('ApplyMl15DDcnn4Pred', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('ApplyMl15DDcnn4Pred', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('ApplyMl15DDcnn4Pred', 'height='))
        self.ldtnewheight.setText(_translate('ApplyMl15DDcnn4Pred', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('ApplyMl15DDcnn4Pred', 'width='))
        self.ldtnewwidth.setText(_translate('ApplyMl15DDcnn4Pred', ''))
        self.ldtnewwidth.setEnabled(False)
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('ApplyMl15DDcnn4Pred', 'Pre-trained DCNN architecture:'))
        self.btnviewnetwork.setText(_translate('ApplyMl15DDcnn4Pred', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('ApplyMl15DDcnn4Pred', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ApplyMl15DDcnn4Pred', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('ApplyMl15DDcnn4Pred', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('ApplyMl15DDcnn4Pred', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('ApplyMl15DDcnn4Pred', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ApplyMl15DDcnn4Pred', 'height='))
        self.ldtmaskheight.setText(_translate('ApplyMl15DDcnn4Pred', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ApplyMl15DDcnn4Pred', 'width='))
        self.ldtmaskwidth.setText(_translate('ApplyMl15DDcnn4Pred', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ApplyMl15DDcnn4Pred', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ApplyMl15DDcnn4Pred', 'height='))
        self.ldtpoolheight.setText(_translate('ApplyMl15DDcnn4Pred', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ApplyMl15DDcnn4Pred', 'width='))
        self.ldtpoolwidth.setText(_translate('ApplyMl15DDcnn4Pred', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ApplyMl15DDcnn4Pred', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ApplyMl15DDcnn4Pred', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ApplyMl15DDcnn4Pred', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('ApplyMl15DDcnn4Pred', 'Output name='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ApplyMl15DDcnn4Pred', 'dcnn'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('ApplyMl15DDcnn4Pred', 'Apply 1.5D-DCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnApplyMl15DDcnn4Pred)

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.check15DDCNNModel(self.modelpath, self.modelname) is True:
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
        _file = _dialog.getOpenFileName(None, 'Select DCNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def changeLwgFeature(self):
        _shape = [
         0, 0]
        if ml_tfm.check15DDCNNModel(self.modelpath, self.modelname):
            _shape = self.getImageSize(self.lwgfeature.currentItem().text())
        _height = _shape[0]
        _width = _shape[1]
        self.ldtoldheight.setText(str(_height))

    def changeCbbOrnt(self):
        _shape = [
         0, 0]
        if ml_tfm.check15DDCNNModel(self.modelpath, self.modelname):
            _shape = self.getImageSize(self.lwgfeature.currentItem().text())
        _height = _shape[0]
        _width = _shape[1]
        self.ldtoldheight.setText(str(_height))

    def changeLdtNconvblock(self):
        if ml_tfm.check15DDCNNModel(self.modelpath, self.modelname) is True:
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
        if ml_tfm.check15DDCNNModel(self.modelpath, self.modelname) is True:
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
        _viewmlcnn = QtWidgets.QDialog()
        _gui = gui_viewml2ddcnn()
        _gui.linestyle = self.linestyle
        _gui.maskstyle = self.maskstyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewmlcnn)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewmlcnn.exec()
        _viewmlcnn.show()

    def clickBtnApplyMl15DDcnn4Pred--- This code section failed: ---

 L. 458         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 460         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 461        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in ApplyMl15DDcnn4Pred: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 462        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 463        44  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 464        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 465        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 467        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              check15DDCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 468        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in ApplyMl15DDcnn4Pred: No pre-DCNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 469        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 470       100  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 471       102  LOAD_STR                 'No pre-DCNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 472       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 474       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 475       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 476       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in ApplyMl15DDcnn4Pred: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    
              152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 477       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 478       170  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 479       172  LOAD_STR                 "Feature '"
              174  LOAD_FAST                'f'
              176  BINARY_ADD       
              178  LOAD_STR                 "' not found in seismic data"
              180  BINARY_ADD       
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L. 480       186  LOAD_CONST               None
              188  RETURN_VALUE     
              190  JUMP_BACK           124  'to 124'
              192  POP_BLOCK        
            194_0  COME_FROM_LOOP      112  '112'

 L. 482       194  LOAD_FAST                'self'
              196  LOAD_ATTR                modelinfo
              198  LOAD_STR                 'feature_list'
              200  BINARY_SUBSCR    
              202  STORE_FAST               '_features'

 L. 483       204  LOAD_GLOBAL              basic_data
              206  LOAD_METHOD              str2int
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                ldtoldheight
              212  LOAD_METHOD              text
              214  CALL_METHOD_0         0  '0 positional arguments'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  STORE_FAST               '_image_height'

 L. 484       220  LOAD_GLOBAL              basic_data
              222  LOAD_METHOD              str2int
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                ldtoldwidth
              228  LOAD_METHOD              text
              230  CALL_METHOD_0         0  '0 positional arguments'
              232  CALL_METHOD_1         1  '1 positional argument'
              234  STORE_FAST               '_image_width'

 L. 485       236  LOAD_GLOBAL              basic_data
              238  LOAD_METHOD              str2int
              240  LOAD_FAST                'self'
              242  LOAD_ATTR                ldtnewheight
              244  LOAD_METHOD              text
              246  CALL_METHOD_0         0  '0 positional arguments'
              248  CALL_METHOD_1         1  '1 positional argument'
              250  STORE_FAST               '_image_height_new'

 L. 486       252  LOAD_GLOBAL              basic_data
              254  LOAD_METHOD              str2int
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                ldtnewwidth
              260  LOAD_METHOD              text
              262  CALL_METHOD_0         0  '0 positional arguments'
              264  CALL_METHOD_1         1  '1 positional argument'
              266  STORE_FAST               '_image_width_new'

 L. 487       268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               False
              272  COMPARE_OP               is
          274_276  POP_JUMP_IF_TRUE    308  'to 308'
              278  LOAD_FAST                '_image_width'
              280  LOAD_CONST               False
              282  COMPARE_OP               is
          284_286  POP_JUMP_IF_TRUE    308  'to 308'

 L. 488       288  LOAD_FAST                '_image_height_new'
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

 L. 489       308  LOAD_GLOBAL              vis_msg
              310  LOAD_ATTR                print
              312  LOAD_STR                 'ERROR in ApplyMl15DDcnn4Pred: Non-integer feature size'
              314  LOAD_STR                 'error'
              316  LOAD_CONST               ('type',)
              318  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              320  POP_TOP          

 L. 490       322  LOAD_GLOBAL              QtWidgets
              324  LOAD_ATTR                QMessageBox
              326  LOAD_METHOD              critical
              328  LOAD_FAST                'self'
              330  LOAD_ATTR                msgbox

 L. 491       332  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 492       334  LOAD_STR                 'Non-integer feature size'
              336  CALL_METHOD_3         3  '3 positional arguments'
              338  POP_TOP          

 L. 493       340  LOAD_CONST               None
              342  RETURN_VALUE     
            344_0  COME_FROM           304  '304'

 L. 494       344  LOAD_FAST                '_image_height'
              346  LOAD_CONST               2
              348  COMPARE_OP               <
          350_352  POP_JUMP_IF_TRUE    384  'to 384'
              354  LOAD_FAST                '_image_width'
              356  LOAD_CONST               2
              358  COMPARE_OP               <
          360_362  POP_JUMP_IF_TRUE    384  'to 384'

 L. 495       364  LOAD_FAST                '_image_height_new'
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

 L. 496       384  LOAD_GLOBAL              vis_msg
              386  LOAD_ATTR                print
              388  LOAD_STR                 'ERROR in ApplyMl15DDcnn4Pred: Features are not 2D'
              390  LOAD_STR                 'error'
              392  LOAD_CONST               ('type',)
              394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              396  POP_TOP          

 L. 497       398  LOAD_GLOBAL              QtWidgets
              400  LOAD_ATTR                QMessageBox
              402  LOAD_METHOD              critical
              404  LOAD_FAST                'self'
              406  LOAD_ATTR                msgbox

 L. 498       408  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 499       410  LOAD_STR                 'Features are not 2D'
              412  CALL_METHOD_3         3  '3 positional arguments'
              414  POP_TOP          

 L. 500       416  LOAD_CONST               None
              418  RETURN_VALUE     
            420_0  COME_FROM           380  '380'

 L. 502       420  LOAD_GLOBAL              basic_data
              422  LOAD_METHOD              str2int
              424  LOAD_FAST                'self'
              426  LOAD_ATTR                ldtbatchsize
              428  LOAD_METHOD              text
              430  CALL_METHOD_0         0  '0 positional arguments'
              432  CALL_METHOD_1         1  '1 positional argument'
              434  STORE_FAST               '_batch'

 L. 503       436  LOAD_FAST                '_batch'
              438  LOAD_CONST               False
              440  COMPARE_OP               is
          442_444  POP_JUMP_IF_TRUE    456  'to 456'
              446  LOAD_FAST                '_batch'
              448  LOAD_CONST               1
              450  COMPARE_OP               <
          452_454  POP_JUMP_IF_FALSE   492  'to 492'
            456_0  COME_FROM           442  '442'

 L. 504       456  LOAD_GLOBAL              vis_msg
              458  LOAD_ATTR                print
              460  LOAD_STR                 'ERROR in ApplyMl15DDcnn4Pred: Non-positive batch size'
              462  LOAD_STR                 'error'
              464  LOAD_CONST               ('type',)
              466  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              468  POP_TOP          

 L. 505       470  LOAD_GLOBAL              QtWidgets
              472  LOAD_ATTR                QMessageBox
              474  LOAD_METHOD              critical
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                msgbox

 L. 506       480  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 507       482  LOAD_STR                 'Non-positive batch size'
              484  CALL_METHOD_3         3  '3 positional arguments'
              486  POP_TOP          

 L. 508       488  LOAD_CONST               None
              490  RETURN_VALUE     
            492_0  COME_FROM           452  '452'

 L. 510       492  LOAD_GLOBAL              len
              494  LOAD_FAST                'self'
              496  LOAD_ATTR                ldtsave
              498  LOAD_METHOD              text
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  CALL_FUNCTION_1       1  '1 positional argument'
              504  LOAD_CONST               1
              506  COMPARE_OP               <
          508_510  POP_JUMP_IF_FALSE   548  'to 548'

 L. 511       512  LOAD_GLOBAL              vis_msg
              514  LOAD_ATTR                print
              516  LOAD_STR                 'ERROR in ApplyMl15DDcnn4Pred: No name specified'
              518  LOAD_STR                 'error'
              520  LOAD_CONST               ('type',)
              522  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              524  POP_TOP          

 L. 512       526  LOAD_GLOBAL              QtWidgets
              528  LOAD_ATTR                QMessageBox
              530  LOAD_METHOD              critical
              532  LOAD_FAST                'self'
              534  LOAD_ATTR                msgbox

 L. 513       536  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 514       538  LOAD_STR                 'No name specified'
              540  CALL_METHOD_3         3  '3 positional arguments'
              542  POP_TOP          

 L. 515       544  LOAD_CONST               None
              546  RETURN_VALUE     
            548_0  COME_FROM           508  '508'

 L. 516       548  LOAD_FAST                'self'
              550  LOAD_ATTR                ldtsave
              552  LOAD_METHOD              text
              554  CALL_METHOD_0         0  '0 positional arguments'
              556  LOAD_FAST                'self'
              558  LOAD_ATTR                seisdata
              560  LOAD_METHOD              keys
              562  CALL_METHOD_0         0  '0 positional arguments'
              564  COMPARE_OP               in
          566_568  POP_JUMP_IF_FALSE   654  'to 654'
              570  LOAD_FAST                'self'
              572  LOAD_METHOD              checkSeisData
              574  LOAD_FAST                'self'
              576  LOAD_ATTR                ldtsave
              578  LOAD_METHOD              text
              580  CALL_METHOD_0         0  '0 positional arguments'
              582  CALL_METHOD_1         1  '1 positional argument'
          584_586  POP_JUMP_IF_FALSE   654  'to 654'

 L. 517       588  LOAD_GLOBAL              QtWidgets
              590  LOAD_ATTR                QMessageBox
              592  LOAD_METHOD              question
              594  LOAD_FAST                'self'
              596  LOAD_ATTR                msgbox
              598  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 518       600  LOAD_FAST                'self'
              602  LOAD_ATTR                ldtsave
              604  LOAD_METHOD              text
              606  CALL_METHOD_0         0  '0 positional arguments'
              608  LOAD_STR                 ' already exists. Overwrite?'
              610  BINARY_ADD       

 L. 519       612  LOAD_GLOBAL              QtWidgets
              614  LOAD_ATTR                QMessageBox
              616  LOAD_ATTR                Yes
              618  LOAD_GLOBAL              QtWidgets
              620  LOAD_ATTR                QMessageBox
              622  LOAD_ATTR                No
              624  BINARY_OR        

 L. 520       626  LOAD_GLOBAL              QtWidgets
              628  LOAD_ATTR                QMessageBox
              630  LOAD_ATTR                No
              632  CALL_METHOD_5         5  '5 positional arguments'
              634  STORE_FAST               'reply'

 L. 522       636  LOAD_FAST                'reply'
              638  LOAD_GLOBAL              QtWidgets
              640  LOAD_ATTR                QMessageBox
              642  LOAD_ATTR                No
              644  COMPARE_OP               ==
          646_648  POP_JUMP_IF_FALSE   654  'to 654'

 L. 523       650  LOAD_CONST               None
              652  RETURN_VALUE     
            654_0  COME_FROM           646  '646'
            654_1  COME_FROM           584  '584'
            654_2  COME_FROM           566  '566'

 L. 525       654  LOAD_FAST                'self'
              656  LOAD_ATTR                survinfo
              658  STORE_FAST               '_seisinfo'

 L. 527       660  LOAD_CONST               0
              662  STORE_FAST               '_wdinl'

 L. 528       664  LOAD_CONST               0
              666  STORE_FAST               '_wdxl'

 L. 529       668  LOAD_CONST               0
              670  STORE_FAST               '_wdz'

 L. 530       672  LOAD_FAST                'self'
              674  LOAD_ATTR                cbbornt
              676  LOAD_METHOD              currentIndex
              678  CALL_METHOD_0         0  '0 positional arguments'
              680  LOAD_CONST               0
              682  COMPARE_OP               ==
          684_686  POP_JUMP_IF_FALSE   700  'to 700'

 L. 531       688  LOAD_GLOBAL              int
              690  LOAD_FAST                '_image_width'
              692  LOAD_CONST               2
              694  BINARY_TRUE_DIVIDE
              696  CALL_FUNCTION_1       1  '1 positional argument'
              698  STORE_FAST               '_wdxl'
            700_0  COME_FROM           684  '684'

 L. 532       700  LOAD_FAST                'self'
              702  LOAD_ATTR                cbbornt
              704  LOAD_METHOD              currentIndex
              706  CALL_METHOD_0         0  '0 positional arguments'
              708  LOAD_CONST               1
              710  COMPARE_OP               ==
          712_714  POP_JUMP_IF_FALSE   728  'to 728'

 L. 533       716  LOAD_GLOBAL              int
              718  LOAD_FAST                '_image_width'
              720  LOAD_CONST               2
              722  BINARY_TRUE_DIVIDE
              724  CALL_FUNCTION_1       1  '1 positional argument'
              726  STORE_FAST               '_wdinl'
            728_0  COME_FROM           712  '712'

 L. 534       728  LOAD_FAST                'self'
              730  LOAD_ATTR                cbbornt
              732  LOAD_METHOD              currentIndex
              734  CALL_METHOD_0         0  '0 positional arguments'
              736  LOAD_CONST               2
              738  COMPARE_OP               ==
          740_742  POP_JUMP_IF_FALSE   756  'to 756'

 L. 535       744  LOAD_GLOBAL              int
              746  LOAD_FAST                '_image_width'
              748  LOAD_CONST               2
              750  BINARY_TRUE_DIVIDE
              752  CALL_FUNCTION_1       1  '1 positional argument'
              754  STORE_FAST               '_wdinl'
            756_0  COME_FROM           740  '740'

 L. 536       756  BUILD_MAP_0           0 
              758  STORE_FAST               '_seisdict'

 L. 537       760  LOAD_FAST                'self'
              762  LOAD_ATTR                cbbornt
              764  LOAD_METHOD              currentIndex
              766  CALL_METHOD_0         0  '0 positional arguments'
              768  LOAD_CONST               0
              770  COMPARE_OP               ==
          772_774  POP_JUMP_IF_TRUE    792  'to 792'
              776  LOAD_FAST                'self'
              778  LOAD_ATTR                cbbornt
              780  LOAD_METHOD              currentIndex
              782  CALL_METHOD_0         0  '0 positional arguments'
              784  LOAD_CONST               1
              786  COMPARE_OP               ==
          788_790  POP_JUMP_IF_FALSE   900  'to 900'
            792_0  COME_FROM           772  '772'

 L. 538       792  LOAD_GLOBAL              np
              794  LOAD_METHOD              arange
              796  LOAD_CONST               0
              798  LOAD_FAST                '_seisinfo'
              800  LOAD_STR                 'ILNum'
              802  BINARY_SUBSCR    
              804  LOAD_FAST                '_seisinfo'
              806  LOAD_STR                 'XLNum'
              808  BINARY_SUBSCR    
              810  BINARY_MULTIPLY  
              812  CALL_METHOD_2         2  '2 positional arguments'
              814  STORE_FAST               '_all_sample'

 L. 539       816  LOAD_GLOBAL              np
              818  LOAD_METHOD              reshape
              820  LOAD_FAST                '_seisinfo'
              822  LOAD_STR                 'ILRange'
              824  BINARY_SUBSCR    
              826  LOAD_FAST                '_all_sample'
              828  LOAD_FAST                '_seisinfo'
              830  LOAD_STR                 'XLNum'
              832  BINARY_SUBSCR    
              834  BINARY_TRUE_DIVIDE
              836  LOAD_METHOD              astype
              838  LOAD_GLOBAL              int
              840  CALL_METHOD_1         1  '1 positional argument'
              842  BINARY_SUBSCR    

 L. 540       844  LOAD_CONST               -1
              846  LOAD_CONST               1
              848  BUILD_LIST_2          2 
              850  CALL_METHOD_2         2  '2 positional arguments'
              852  LOAD_FAST                '_seisdict'
              854  LOAD_STR                 'Inline'
              856  STORE_SUBSCR     

 L. 541       858  LOAD_GLOBAL              np
              860  LOAD_METHOD              reshape
              862  LOAD_FAST                '_seisinfo'
              864  LOAD_STR                 'XLRange'
              866  BINARY_SUBSCR    
              868  LOAD_FAST                '_all_sample'
              870  LOAD_FAST                '_seisinfo'
              872  LOAD_STR                 'XLNum'
              874  BINARY_SUBSCR    
              876  BINARY_MODULO    
              878  LOAD_METHOD              astype
              880  LOAD_GLOBAL              int
              882  CALL_METHOD_1         1  '1 positional argument'
              884  BINARY_SUBSCR    

 L. 542       886  LOAD_CONST               -1
              888  LOAD_CONST               1
              890  BUILD_LIST_2          2 
              892  CALL_METHOD_2         2  '2 positional arguments'
              894  LOAD_FAST                '_seisdict'
              896  LOAD_STR                 'Crossline'
              898  STORE_SUBSCR     
            900_0  COME_FROM           788  '788'

 L. 543       900  LOAD_FAST                'self'
              902  LOAD_ATTR                cbbornt
              904  LOAD_METHOD              currentIndex
              906  CALL_METHOD_0         0  '0 positional arguments'
              908  LOAD_CONST               2
              910  COMPARE_OP               ==
          912_914  POP_JUMP_IF_FALSE  1024  'to 1024'

 L. 544       916  LOAD_GLOBAL              np
              918  LOAD_METHOD              arange
              920  LOAD_CONST               0
              922  LOAD_FAST                '_seisinfo'
              924  LOAD_STR                 'ILNum'
              926  BINARY_SUBSCR    
              928  LOAD_FAST                '_seisinfo'
              930  LOAD_STR                 'ZNum'
              932  BINARY_SUBSCR    
              934  BINARY_MULTIPLY  
              936  CALL_METHOD_2         2  '2 positional arguments'
              938  STORE_FAST               '_all_sample'

 L. 545       940  LOAD_GLOBAL              np
              942  LOAD_METHOD              reshape
              944  LOAD_FAST                '_seisinfo'
              946  LOAD_STR                 'ILRange'
              948  BINARY_SUBSCR    
              950  LOAD_FAST                '_all_sample'
              952  LOAD_FAST                '_seisinfo'
              954  LOAD_STR                 'ZNum'
              956  BINARY_SUBSCR    
              958  BINARY_TRUE_DIVIDE
              960  LOAD_METHOD              astype
              962  LOAD_GLOBAL              int
              964  CALL_METHOD_1         1  '1 positional argument'
              966  BINARY_SUBSCR    

 L. 546       968  LOAD_CONST               -1
              970  LOAD_CONST               1
              972  BUILD_LIST_2          2 
              974  CALL_METHOD_2         2  '2 positional arguments'
              976  LOAD_FAST                '_seisdict'
              978  LOAD_STR                 'Inline'
              980  STORE_SUBSCR     

 L. 547       982  LOAD_GLOBAL              np
              984  LOAD_METHOD              reshape
              986  LOAD_FAST                '_seisinfo'
              988  LOAD_STR                 'ZRange'
              990  BINARY_SUBSCR    
              992  LOAD_FAST                '_all_sample'
              994  LOAD_FAST                '_seisinfo'
              996  LOAD_STR                 'ZNum'
              998  BINARY_SUBSCR    
             1000  BINARY_MODULO    
             1002  LOAD_METHOD              astype
             1004  LOAD_GLOBAL              int
             1006  CALL_METHOD_1         1  '1 positional argument'
             1008  BINARY_SUBSCR    

 L. 548      1010  LOAD_CONST               -1
             1012  LOAD_CONST               1
             1014  BUILD_LIST_2          2 
             1016  CALL_METHOD_2         2  '2 positional arguments'
             1018  LOAD_FAST                '_seisdict'
             1020  LOAD_STR                 'Z'
             1022  STORE_SUBSCR     
           1024_0  COME_FROM           912  '912'

 L. 550      1024  LOAD_GLOBAL              basic_mdt
             1026  LOAD_METHOD              maxDictConstantRow
             1028  LOAD_FAST                '_seisdict'
             1030  CALL_METHOD_1         1  '1 positional argument'
             1032  STORE_FAST               '_nsample'

 L. 552      1034  LOAD_GLOBAL              int
             1036  LOAD_GLOBAL              np
             1038  LOAD_METHOD              ceil
             1040  LOAD_FAST                '_nsample'
             1042  LOAD_FAST                '_batch'
             1044  BINARY_TRUE_DIVIDE
             1046  CALL_METHOD_1         1  '1 positional argument'
             1048  CALL_FUNCTION_1       1  '1 positional argument'
             1050  STORE_FAST               '_nloop'

 L. 555      1052  LOAD_GLOBAL              QtWidgets
             1054  LOAD_METHOD              QProgressDialog
             1056  CALL_METHOD_0         0  '0 positional arguments'
             1058  STORE_FAST               '_pgsdlg'

 L. 556      1060  LOAD_GLOBAL              QtGui
             1062  LOAD_METHOD              QIcon
             1064  CALL_METHOD_0         0  '0 positional arguments'
             1066  STORE_FAST               'icon'

 L. 557      1068  LOAD_FAST                'icon'
             1070  LOAD_METHOD              addPixmap
             1072  LOAD_GLOBAL              QtGui
             1074  LOAD_METHOD              QPixmap
             1076  LOAD_GLOBAL              os
             1078  LOAD_ATTR                path
             1080  LOAD_METHOD              join
             1082  LOAD_FAST                'self'
             1084  LOAD_ATTR                iconpath
             1086  LOAD_STR                 'icons/check.png'
             1088  CALL_METHOD_2         2  '2 positional arguments'
             1090  CALL_METHOD_1         1  '1 positional argument'

 L. 558      1092  LOAD_GLOBAL              QtGui
             1094  LOAD_ATTR                QIcon
             1096  LOAD_ATTR                Normal
             1098  LOAD_GLOBAL              QtGui
             1100  LOAD_ATTR                QIcon
             1102  LOAD_ATTR                Off
             1104  CALL_METHOD_3         3  '3 positional arguments'
             1106  POP_TOP          

 L. 559      1108  LOAD_FAST                '_pgsdlg'
             1110  LOAD_METHOD              setWindowIcon
             1112  LOAD_FAST                'icon'
             1114  CALL_METHOD_1         1  '1 positional argument'
             1116  POP_TOP          

 L. 560      1118  LOAD_FAST                '_pgsdlg'
             1120  LOAD_METHOD              setWindowTitle
             1122  LOAD_STR                 'Apply 1.5D-DCNN'
             1124  CALL_METHOD_1         1  '1 positional argument'
             1126  POP_TOP          

 L. 561      1128  LOAD_FAST                '_pgsdlg'
             1130  LOAD_METHOD              setCancelButton
             1132  LOAD_CONST               None
             1134  CALL_METHOD_1         1  '1 positional argument'
             1136  POP_TOP          

 L. 562      1138  LOAD_FAST                '_pgsdlg'
             1140  LOAD_METHOD              setWindowFlags
             1142  LOAD_GLOBAL              QtCore
             1144  LOAD_ATTR                Qt
             1146  LOAD_ATTR                WindowStaysOnTopHint
             1148  CALL_METHOD_1         1  '1 positional argument'
             1150  POP_TOP          

 L. 563      1152  LOAD_FAST                '_pgsdlg'
             1154  LOAD_METHOD              forceShow
             1156  CALL_METHOD_0         0  '0 positional arguments'
             1158  POP_TOP          

 L. 564      1160  LOAD_FAST                '_pgsdlg'
             1162  LOAD_METHOD              setFixedWidth
             1164  LOAD_CONST               400
             1166  CALL_METHOD_1         1  '1 positional argument'
             1168  POP_TOP          

 L. 565      1170  LOAD_FAST                '_pgsdlg'
             1172  LOAD_METHOD              setMaximum
             1174  LOAD_FAST                '_nloop'
             1176  CALL_METHOD_1         1  '1 positional argument'
             1178  POP_TOP          

 L. 567      1180  LOAD_GLOBAL              np
             1182  LOAD_METHOD              zeros
             1184  LOAD_FAST                '_nsample'
             1186  LOAD_FAST                '_image_height'
             1188  BUILD_LIST_2          2 
             1190  CALL_METHOD_1         1  '1 positional argument'
             1192  STORE_FAST               '_result'

 L. 568      1194  LOAD_CONST               0
             1196  STORE_FAST               'idxstart'

 L. 569  1198_1200  SETUP_LOOP         1772  'to 1772'
             1202  LOAD_GLOBAL              range
             1204  LOAD_FAST                '_nloop'
             1206  CALL_FUNCTION_1       1  '1 positional argument'
             1208  GET_ITER         
         1210_1212  FOR_ITER           1770  'to 1770'
             1214  STORE_FAST               'i'

 L. 571      1216  LOAD_GLOBAL              QtCore
             1218  LOAD_ATTR                QCoreApplication
             1220  LOAD_METHOD              instance
             1222  CALL_METHOD_0         0  '0 positional arguments'
             1224  LOAD_METHOD              processEvents
             1226  CALL_METHOD_0         0  '0 positional arguments'
             1228  POP_TOP          

 L. 573      1230  LOAD_GLOBAL              sys
             1232  LOAD_ATTR                stdout
             1234  LOAD_METHOD              write

 L. 574      1236  LOAD_STR                 '\r>>> Apply 1.5D-DCNN, proceeding %.1f%% '
             1238  LOAD_GLOBAL              float
             1240  LOAD_FAST                'i'
             1242  CALL_FUNCTION_1       1  '1 positional argument'
             1244  LOAD_GLOBAL              float
             1246  LOAD_FAST                '_nloop'
             1248  CALL_FUNCTION_1       1  '1 positional argument'
             1250  BINARY_TRUE_DIVIDE
             1252  LOAD_CONST               100.0
             1254  BINARY_MULTIPLY  
             1256  BINARY_MODULO    
             1258  CALL_METHOD_1         1  '1 positional argument'
             1260  POP_TOP          

 L. 575      1262  LOAD_GLOBAL              sys
             1264  LOAD_ATTR                stdout
             1266  LOAD_METHOD              flush
             1268  CALL_METHOD_0         0  '0 positional arguments'
             1270  POP_TOP          

 L. 577      1272  LOAD_FAST                'idxstart'
             1274  LOAD_FAST                '_batch'
             1276  BINARY_ADD       
             1278  STORE_FAST               'idxend'

 L. 578      1280  LOAD_FAST                'idxend'
             1282  LOAD_FAST                '_nsample'
             1284  COMPARE_OP               >
         1286_1288  POP_JUMP_IF_FALSE  1294  'to 1294'

 L. 579      1290  LOAD_FAST                '_nsample'
             1292  STORE_FAST               'idxend'
           1294_0  COME_FROM          1286  '1286'

 L. 580      1294  LOAD_GLOBAL              np
             1296  LOAD_METHOD              linspace
             1298  LOAD_FAST                'idxstart'
             1300  LOAD_FAST                'idxend'
             1302  LOAD_CONST               1
             1304  BINARY_SUBTRACT  
             1306  LOAD_FAST                'idxend'
             1308  LOAD_FAST                'idxstart'
             1310  BINARY_SUBTRACT  
             1312  CALL_METHOD_3         3  '3 positional arguments'
             1314  LOAD_METHOD              astype
             1316  LOAD_GLOBAL              int
             1318  CALL_METHOD_1         1  '1 positional argument'
             1320  STORE_FAST               'idxlist'

 L. 581      1322  LOAD_FAST                'idxend'
             1324  STORE_FAST               'idxstart'

 L. 582      1326  LOAD_GLOBAL              basic_mdt
             1328  LOAD_METHOD              retrieveDictByIndex
             1330  LOAD_FAST                '_seisdict'
             1332  LOAD_FAST                'idxlist'
             1334  CALL_METHOD_2         2  '2 positional arguments'
             1336  STORE_FAST               '_dict'

 L. 584      1338  LOAD_FAST                '_dict'
             1340  LOAD_STR                 'Inline'
             1342  BINARY_SUBSCR    
             1344  STORE_FAST               '_targetdata'

 L. 585      1346  LOAD_FAST                'self'
             1348  LOAD_ATTR                cbbornt
             1350  LOAD_METHOD              currentIndex
             1352  CALL_METHOD_0         0  '0 positional arguments'
             1354  LOAD_CONST               0
             1356  COMPARE_OP               ==
         1358_1360  POP_JUMP_IF_TRUE   1378  'to 1378'
             1362  LOAD_FAST                'self'
             1364  LOAD_ATTR                cbbornt
             1366  LOAD_METHOD              currentIndex
             1368  CALL_METHOD_0         0  '0 positional arguments'
             1370  LOAD_CONST               1
             1372  COMPARE_OP               ==
         1374_1376  POP_JUMP_IF_FALSE  1482  'to 1482'
           1378_0  COME_FROM          1358  '1358'

 L. 586      1378  LOAD_GLOBAL              np
             1380  LOAD_ATTR                concatenate
             1382  LOAD_FAST                '_targetdata'
             1384  LOAD_FAST                '_dict'
             1386  LOAD_STR                 'Crossline'
             1388  BINARY_SUBSCR    
             1390  BUILD_TUPLE_2         2 
             1392  LOAD_CONST               1
             1394  LOAD_CONST               ('axis',)
             1396  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1398  STORE_FAST               '_targetdata'

 L. 587      1400  SETUP_LOOP         1482  'to 1482'
             1402  LOAD_FAST                '_features'
             1404  GET_ITER         
             1406  FOR_ITER           1480  'to 1480'
             1408  STORE_FAST               'f'

 L. 588      1410  LOAD_FAST                'self'
             1412  LOAD_ATTR                seisdata
             1414  LOAD_FAST                'f'
             1416  BINARY_SUBSCR    
             1418  STORE_FAST               '_data'

 L. 589      1420  LOAD_GLOBAL              seis_ays
             1422  LOAD_ATTR                retrieveSeisZTraceFrom3DMat
             1424  LOAD_FAST                '_data'
             1426  LOAD_FAST                '_targetdata'

 L. 590      1428  LOAD_FAST                'self'
             1430  LOAD_ATTR                survinfo

 L. 591      1432  LOAD_FAST                '_wdinl'
             1434  LOAD_FAST                '_wdxl'

 L. 592      1436  LOAD_CONST               False
             1438  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'verbose')
             1440  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1442  STORE_FAST               '_data'

 L. 593      1444  LOAD_FAST                '_data'
             1446  LOAD_CONST               None
             1448  LOAD_CONST               None
             1450  BUILD_SLICE_2         2 
             1452  LOAD_CONST               2
             1454  LOAD_CONST               2
             1456  LOAD_FAST                '_image_height'
             1458  LOAD_FAST                '_image_width'
             1460  BINARY_MULTIPLY  
             1462  BINARY_ADD       
             1464  BUILD_SLICE_2         2 
             1466  BUILD_TUPLE_2         2 
             1468  BINARY_SUBSCR    
             1470  LOAD_FAST                '_dict'
             1472  LOAD_FAST                'f'
             1474  STORE_SUBSCR     
         1476_1478  JUMP_BACK          1406  'to 1406'
             1480  POP_BLOCK        
           1482_0  COME_FROM_LOOP     1400  '1400'
           1482_1  COME_FROM          1374  '1374'

 L. 594      1482  LOAD_FAST                'self'
             1484  LOAD_ATTR                cbbornt
             1486  LOAD_METHOD              currentIndex
             1488  CALL_METHOD_0         0  '0 positional arguments'
             1490  LOAD_CONST               2
             1492  COMPARE_OP               ==
         1494_1496  POP_JUMP_IF_FALSE  1602  'to 1602'

 L. 595      1498  LOAD_GLOBAL              np
             1500  LOAD_ATTR                concatenate
             1502  LOAD_FAST                '_targetdata'
             1504  LOAD_FAST                '_dict'
             1506  LOAD_STR                 'Z'
             1508  BINARY_SUBSCR    
             1510  BUILD_TUPLE_2         2 
             1512  LOAD_CONST               1
             1514  LOAD_CONST               ('axis',)
             1516  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1518  STORE_FAST               '_targetdata'

 L. 596      1520  SETUP_LOOP         1602  'to 1602'
             1522  LOAD_FAST                '_features'
             1524  GET_ITER         
             1526  FOR_ITER           1600  'to 1600'
             1528  STORE_FAST               'f'

 L. 597      1530  LOAD_FAST                'self'
             1532  LOAD_ATTR                seisdata
             1534  LOAD_FAST                'f'
             1536  BINARY_SUBSCR    
             1538  STORE_FAST               '_data'

 L. 598      1540  LOAD_GLOBAL              seis_ays
             1542  LOAD_ATTR                retrieveSeisXLTraceFrom3DMat
             1544  LOAD_FAST                '_data'
             1546  LOAD_FAST                '_targetdata'

 L. 599      1548  LOAD_FAST                'self'
             1550  LOAD_ATTR                survinfo

 L. 600      1552  LOAD_FAST                '_wdinl'
             1554  LOAD_FAST                '_wdz'

 L. 601      1556  LOAD_CONST               False
             1558  LOAD_CONST               ('seisinfo', 'wdinl', 'wdz', 'verbose')
             1560  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1562  STORE_FAST               '_data'

 L. 602      1564  LOAD_FAST                '_data'
             1566  LOAD_CONST               None
             1568  LOAD_CONST               None
             1570  BUILD_SLICE_2         2 
             1572  LOAD_CONST               2
             1574  LOAD_CONST               2
             1576  LOAD_FAST                '_image_height'
             1578  LOAD_FAST                '_image_width'
             1580  BINARY_MULTIPLY  
             1582  BINARY_ADD       
             1584  BUILD_SLICE_2         2 
             1586  BUILD_TUPLE_2         2 
             1588  BINARY_SUBSCR    
             1590  LOAD_FAST                '_dict'
             1592  LOAD_FAST                'f'
             1594  STORE_SUBSCR     
         1596_1598  JUMP_BACK          1526  'to 1526'
             1600  POP_BLOCK        
           1602_0  COME_FROM_LOOP     1520  '1520'
           1602_1  COME_FROM          1494  '1494'

 L. 603      1602  LOAD_FAST                '_image_height_new'
             1604  LOAD_FAST                '_image_height'
             1606  COMPARE_OP               !=
         1608_1610  POP_JUMP_IF_TRUE   1622  'to 1622'
             1612  LOAD_FAST                '_image_width_new'
             1614  LOAD_FAST                '_image_width'
             1616  COMPARE_OP               !=
         1618_1620  POP_JUMP_IF_FALSE  1666  'to 1666'
           1622_0  COME_FROM          1608  '1608'

 L. 604      1622  SETUP_LOOP         1666  'to 1666'
             1624  LOAD_FAST                '_features'
             1626  GET_ITER         
             1628  FOR_ITER           1664  'to 1664'
             1630  STORE_FAST               'f'

 L. 605      1632  LOAD_GLOBAL              basic_image
             1634  LOAD_ATTR                changeImageSize
             1636  LOAD_FAST                '_dict'
             1638  LOAD_FAST                'f'
             1640  BINARY_SUBSCR    

 L. 606      1642  LOAD_FAST                '_image_height'

 L. 607      1644  LOAD_FAST                '_image_width'

 L. 608      1646  LOAD_FAST                '_image_height_new'

 L. 609      1648  LOAD_FAST                '_image_width_new'
             1650  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1652  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1654  LOAD_FAST                '_dict'
             1656  LOAD_FAST                'f'
             1658  STORE_SUBSCR     
         1660_1662  JUMP_BACK          1628  'to 1628'
             1664  POP_BLOCK        
           1666_0  COME_FROM_LOOP     1622  '1622'
           1666_1  COME_FROM          1618  '1618'

 L. 612      1666  LOAD_GLOBAL              ml_dcnn15d
             1668  LOAD_ATTR                predictionFrom15DDCNNSegmentor
             1670  LOAD_FAST                '_dict'

 L. 613      1672  LOAD_FAST                '_image_height_new'

 L. 614      1674  LOAD_FAST                '_image_width_new'

 L. 615      1676  LOAD_FAST                'self'
             1678  LOAD_ATTR                modelpath

 L. 616      1680  LOAD_FAST                'self'
             1682  LOAD_ATTR                modelname

 L. 617      1684  LOAD_FAST                '_batch'
             1686  LOAD_CONST               False
             1688  LOAD_CONST               ('imageheight', 'imagewidth', 'dcnnpath', 'dcnnname', 'batchsize', 'verbose')
             1690  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1692  STORE_FAST               '_rst'

 L. 619      1694  LOAD_FAST                '_image_height_new'
             1696  LOAD_FAST                '_image_height'
             1698  COMPARE_OP               !=
         1700_1702  POP_JUMP_IF_FALSE  1736  'to 1736'

 L. 620      1704  LOAD_GLOBAL              basic_curve
             1706  LOAD_ATTR                changeCurveSize
             1708  LOAD_FAST                '_rst'

 L. 621      1710  LOAD_FAST                '_image_height_new'

 L. 622      1712  LOAD_FAST                '_image_height'
             1714  LOAD_STR                 'linear'
             1716  LOAD_CONST               ('length', 'length_new', 'kind')
             1718  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1720  LOAD_FAST                '_result'
             1722  LOAD_FAST                'idxlist'
             1724  LOAD_CONST               None
             1726  LOAD_CONST               None
             1728  BUILD_SLICE_2         2 
             1730  BUILD_TUPLE_2         2 
             1732  STORE_SUBSCR     
             1734  JUMP_FORWARD       1752  'to 1752'
           1736_0  COME_FROM          1700  '1700'

 L. 625      1736  LOAD_FAST                '_rst'
             1738  LOAD_FAST                '_result'
             1740  LOAD_FAST                'idxlist'
             1742  LOAD_CONST               None
             1744  LOAD_CONST               None
             1746  BUILD_SLICE_2         2 
             1748  BUILD_TUPLE_2         2 
             1750  STORE_SUBSCR     
           1752_0  COME_FROM          1734  '1734'

 L. 628      1752  LOAD_FAST                '_pgsdlg'
             1754  LOAD_METHOD              setValue
             1756  LOAD_FAST                'i'
             1758  LOAD_CONST               1
             1760  BINARY_ADD       
             1762  CALL_METHOD_1         1  '1 positional argument'
             1764  POP_TOP          
         1766_1768  JUMP_BACK          1210  'to 1210'
             1770  POP_BLOCK        
           1772_0  COME_FROM_LOOP     1198  '1198'

 L. 630      1772  LOAD_GLOBAL              print
             1774  LOAD_STR                 'Done'
             1776  CALL_FUNCTION_1       1  '1 positional argument'
             1778  POP_TOP          

 L. 632      1780  LOAD_GLOBAL              np
             1782  LOAD_METHOD              round
             1784  LOAD_FAST                '_result'
             1786  CALL_METHOD_1         1  '1 positional argument'
             1788  LOAD_METHOD              astype
             1790  LOAD_GLOBAL              int
             1792  CALL_METHOD_1         1  '1 positional argument'
             1794  STORE_FAST               '_result'

 L. 634      1796  LOAD_FAST                'self'
             1798  LOAD_ATTR                cbbornt
             1800  LOAD_METHOD              currentIndex
             1802  CALL_METHOD_0         0  '0 positional arguments'
             1804  LOAD_CONST               0
             1806  COMPARE_OP               ==
         1808_1810  POP_JUMP_IF_TRUE   1828  'to 1828'
             1812  LOAD_FAST                'self'
             1814  LOAD_ATTR                cbbornt
             1816  LOAD_METHOD              currentIndex
             1818  CALL_METHOD_0         0  '0 positional arguments'
             1820  LOAD_CONST               1
             1822  COMPARE_OP               ==
         1824_1826  POP_JUMP_IF_FALSE  1876  'to 1876'
           1828_0  COME_FROM          1808  '1808'

 L. 635      1828  LOAD_GLOBAL              np
             1830  LOAD_METHOD              reshape
             1832  LOAD_FAST                '_result'
             1834  LOAD_FAST                '_seisinfo'
             1836  LOAD_STR                 'ILNum'
             1838  BINARY_SUBSCR    
             1840  LOAD_FAST                '_seisinfo'
             1842  LOAD_STR                 'XLNum'
             1844  BINARY_SUBSCR    
             1846  LOAD_FAST                '_seisinfo'
             1848  LOAD_STR                 'ZNum'
             1850  BINARY_SUBSCR    
             1852  BUILD_LIST_3          3 
             1854  CALL_METHOD_2         2  '2 positional arguments'
             1856  STORE_FAST               '_result'

 L. 636      1858  LOAD_GLOBAL              np
             1860  LOAD_METHOD              transpose
             1862  LOAD_FAST                '_result'
             1864  LOAD_CONST               2
             1866  LOAD_CONST               1
             1868  LOAD_CONST               0
             1870  BUILD_LIST_3          3 
             1872  CALL_METHOD_2         2  '2 positional arguments'
             1874  STORE_FAST               '_result'
           1876_0  COME_FROM          1824  '1824'

 L. 637      1876  LOAD_FAST                'self'
             1878  LOAD_ATTR                cbbornt
             1880  LOAD_METHOD              currentIndex
             1882  CALL_METHOD_0         0  '0 positional arguments'
             1884  LOAD_CONST               2
             1886  COMPARE_OP               ==
         1888_1890  POP_JUMP_IF_FALSE  1940  'to 1940'

 L. 638      1892  LOAD_GLOBAL              np
             1894  LOAD_METHOD              reshape
             1896  LOAD_FAST                '_result'
             1898  LOAD_FAST                '_seisinfo'
             1900  LOAD_STR                 'ILNum'
             1902  BINARY_SUBSCR    
             1904  LOAD_FAST                '_seisinfo'
             1906  LOAD_STR                 'ZNum'
             1908  BINARY_SUBSCR    
             1910  LOAD_FAST                '_seisinfo'
             1912  LOAD_STR                 'XLNum'
             1914  BINARY_SUBSCR    
             1916  BUILD_LIST_3          3 
             1918  CALL_METHOD_2         2  '2 positional arguments'
             1920  STORE_FAST               '_result'

 L. 639      1922  LOAD_GLOBAL              np
             1924  LOAD_METHOD              transpose
             1926  LOAD_FAST                '_result'
             1928  LOAD_CONST               1
             1930  LOAD_CONST               2
             1932  LOAD_CONST               0
             1934  BUILD_LIST_3          3 
             1936  CALL_METHOD_2         2  '2 positional arguments'
             1938  STORE_FAST               '_result'
           1940_0  COME_FROM          1888  '1888'

 L. 641      1940  LOAD_FAST                '_result'
             1942  LOAD_FAST                'self'
             1944  LOAD_ATTR                seisdata
             1946  LOAD_FAST                'self'
             1948  LOAD_ATTR                ldtsave
             1950  LOAD_METHOD              text
             1952  CALL_METHOD_0         0  '0 positional arguments'
             1954  STORE_SUBSCR     

 L. 643      1956  LOAD_GLOBAL              QtWidgets
             1958  LOAD_ATTR                QMessageBox
             1960  LOAD_METHOD              information
             1962  LOAD_FAST                'self'
             1964  LOAD_ATTR                msgbox

 L. 644      1966  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 645      1968  LOAD_STR                 'DCNN applied successfully'
             1970  CALL_METHOD_3         3  '3 positional arguments'
             1972  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 1970

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
    ApplyMl15DDcnn4Pred = QtWidgets.QWidget()
    gui = applyml15ddcnn4pred()
    gui.setupGUI(ApplyMl15DDcnn4Pred)
    ApplyMl15DDcnn4Pred.show()
    sys.exit(app.exec_())