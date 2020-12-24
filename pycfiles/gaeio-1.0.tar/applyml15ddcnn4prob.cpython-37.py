# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\applyml15ddcnn4prob.py
# Compiled at: 2019-12-15 20:31:46
# Size of source mod 2**32: 39168 bytes
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

class applyml15ddcnn4prob(object):
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

    def setupGUI(self, ApplyMl15DDcnn4Prob):
        ApplyMl15DDcnn4Prob.setObjectName('ApplyMl15DDcnn4Prob')
        ApplyMl15DDcnn4Prob.setFixedSize(810, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ApplyMl15DDcnn4Prob.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ApplyMl15DDcnn4Prob)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ApplyMl15DDcnn4Prob)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ApplyMl15DDcnn4Prob)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(ApplyMl15DDcnn4Prob)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 230, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 230, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(ApplyMl15DDcnn4Prob)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 230, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 270, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(ApplyMl15DDcnn4Prob)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 270, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 230, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(ApplyMl15DDcnn4Prob)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(ApplyMl15DDcnn4Prob)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ApplyMl15DDcnn4Prob)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ApplyMl15DDcnn4Prob)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ApplyMl15DDcnn4Prob)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 190))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(ApplyMl15DDcnn4Prob)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(ApplyMl15DDcnn4Prob)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 190))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 350, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 350, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ApplyMl15DDcnn4Prob)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 350, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 390, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ApplyMl15DDcnn4Prob)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 390, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 350, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 350, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ApplyMl15DDcnn4Prob)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 350, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 390, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ApplyMl15DDcnn4Prob)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 390, 40, 30))
        self.lblpara = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 320, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ApplyMl15DDcnn4Prob)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblsave = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ApplyMl15DDcnn4Prob)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(150, 390, 100, 30))
        self.lbltarget = QtWidgets.QLabel(ApplyMl15DDcnn4Prob)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(250, 350, 50, 30))
        self.lwgtarget = QtWidgets.QListWidget(ApplyMl15DDcnn4Prob)
        self.lwgtarget.setObjectName('lwgtarget')
        self.lwgtarget.setGeometry(QtCore.QRect(300, 350, 90, 70))
        self.lwgtarget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.btnapply = QtWidgets.QPushButton(ApplyMl15DDcnn4Prob)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(320, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ApplyMl15DDcnn4Prob)
        self.msgbox.setObjectName('msgbox')
        _center_x = ApplyMl15DDcnn4Prob.geometry().center().x()
        _center_y = ApplyMl15DDcnn4Prob.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ApplyMl15DDcnn4Prob)
        QtCore.QMetaObject.connectSlotsByName(ApplyMl15DDcnn4Prob)

    def retranslateGUI(self, ApplyMl15DDcnn4Prob):
        self.dialog = ApplyMl15DDcnn4Prob
        _translate = QtCore.QCoreApplication.translate
        ApplyMl15DDcnn4Prob.setWindowTitle(_translate('ApplyMl15DDcnn4Prob', 'Apply 1.5D-DCNN for probability'))
        self.lblfrom.setText(_translate('ApplyMl15DDcnn4Prob', 'Select network:'))
        self.ldtfrom.setText(_translate('ApplyMl15DDcnn4Prob', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ApplyMl15DDcnn4Prob', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ApplyMl15DDcnn4Prob', 'Training features:'))
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblornt.setText(_translate('ApplyMl15DDcnn4Prob', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.cbbornt.currentIndexChanged.connect(self.changeCbbOrnt)
        self.lbloldsize.setText(_translate('ApplyMl15DDcnn4Prob', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('ApplyMl15DDcnn4Prob', 'height='))
        self.ldtoldheight.setText(_translate('ApplyMl15DDcnn4Prob', ''))
        self.ldtoldheight.setEnabled(False)
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('ApplyMl15DDcnn4Prob', 'width='))
        self.ldtoldwidth.setText(_translate('ApplyMl15DDcnn4Prob', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('ApplyMl15DDcnn4Prob', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('ApplyMl15DDcnn4Prob', 'height='))
        self.ldtnewheight.setText(_translate('ApplyMl15DDcnn4Prob', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('ApplyMl15DDcnn4Prob', 'width='))
        self.ldtnewwidth.setText(_translate('ApplyMl15DDcnn4Prob', ''))
        self.ldtnewwidth.setEnabled(False)
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('ApplyMl15DDcnn4Prob', 'Pre-trained DCNN architecture:'))
        self.btnviewnetwork.setText(_translate('ApplyMl15DDcnn4Prob', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('ApplyMl15DDcnn4Prob', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ApplyMl15DDcnn4Prob', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('ApplyMl15DDcnn4Prob', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('ApplyMl15DDcnn4Prob', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('ApplyMl15DDcnn4Prob', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ApplyMl15DDcnn4Prob', 'height='))
        self.ldtmaskheight.setText(_translate('ApplyMl15DDcnn4Prob', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ApplyMl15DDcnn4Prob', 'width='))
        self.ldtmaskwidth.setText(_translate('ApplyMl15DDcnn4Prob', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ApplyMl15DDcnn4Prob', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ApplyMl15DDcnn4Prob', 'height='))
        self.ldtpoolheight.setText(_translate('ApplyMl15DDcnn4Prob', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ApplyMl15DDcnn4Prob', 'width='))
        self.ldtpoolwidth.setText(_translate('ApplyMl15DDcnn4Prob', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ApplyMl15DDcnn4Prob', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ApplyMl15DDcnn4Prob', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ApplyMl15DDcnn4Prob', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('ApplyMl15DDcnn4Prob', 'Output prefix='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ApplyMl15DDcnn4Prob', 'dcnn_prob_'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltarget.setText(_translate('ApplyMl15DWdcnn4Prob', 'Target ='))
        self.btnapply.setText(_translate('ApplyMl15DDcnn4Prob', 'Apply 1.5D-DCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnApplyMl15DDcnn4Prob)

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

    def clickBtnApplyMl15DDcnn4Prob--- This code section failed: ---

 L. 471         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 473         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 474        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in ApplyMl15DDcnn4Prob: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 475        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 476        44  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 477        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 478        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 480        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              check15DDCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 481        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in ApplyMl15DDcnn4Prob: No pre-DCNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 482        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 483       100  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 484       102  LOAD_STR                 'No pre-DCNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 485       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 487       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 488       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 489       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in ApplyMl15DDcnn4Prob: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    

 L. 490       152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 491       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 492       170  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 493       172  LOAD_STR                 "Feature '"
              174  LOAD_FAST                'f'
              176  BINARY_ADD       
              178  LOAD_STR                 "' not found in seismic data"
              180  BINARY_ADD       
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L. 494       186  LOAD_CONST               None
              188  RETURN_VALUE     
              190  JUMP_BACK           124  'to 124'
              192  POP_BLOCK        
            194_0  COME_FROM_LOOP      112  '112'

 L. 496       194  LOAD_FAST                'self'
              196  LOAD_ATTR                modelinfo
              198  LOAD_STR                 'feature_list'
              200  BINARY_SUBSCR    
              202  STORE_FAST               '_features'

 L. 497       204  LOAD_GLOBAL              basic_data
              206  LOAD_METHOD              str2int
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                ldtoldheight
              212  LOAD_METHOD              text
              214  CALL_METHOD_0         0  '0 positional arguments'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  STORE_FAST               '_image_height'

 L. 498       220  LOAD_GLOBAL              basic_data
              222  LOAD_METHOD              str2int
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                ldtoldwidth
              228  LOAD_METHOD              text
              230  CALL_METHOD_0         0  '0 positional arguments'
              232  CALL_METHOD_1         1  '1 positional argument'
              234  STORE_FAST               '_image_width'

 L. 499       236  LOAD_GLOBAL              basic_data
              238  LOAD_METHOD              str2int
              240  LOAD_FAST                'self'
              242  LOAD_ATTR                ldtnewheight
              244  LOAD_METHOD              text
              246  CALL_METHOD_0         0  '0 positional arguments'
              248  CALL_METHOD_1         1  '1 positional argument'
              250  STORE_FAST               '_image_height_new'

 L. 500       252  LOAD_GLOBAL              basic_data
              254  LOAD_METHOD              str2int
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                ldtnewwidth
              260  LOAD_METHOD              text
              262  CALL_METHOD_0         0  '0 positional arguments'
              264  CALL_METHOD_1         1  '1 positional argument'
              266  STORE_FAST               '_image_width_new'

 L. 501       268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               False
              272  COMPARE_OP               is
          274_276  POP_JUMP_IF_TRUE    308  'to 308'
              278  LOAD_FAST                '_image_width'
              280  LOAD_CONST               False
              282  COMPARE_OP               is
          284_286  POP_JUMP_IF_TRUE    308  'to 308'

 L. 502       288  LOAD_FAST                '_image_height_new'
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

 L. 503       308  LOAD_GLOBAL              vis_msg
              310  LOAD_ATTR                print
              312  LOAD_STR                 'ERROR in ApplyMl15DDcnn4Prob: Non-integer feature size'
              314  LOAD_STR                 'error'
              316  LOAD_CONST               ('type',)
              318  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              320  POP_TOP          

 L. 504       322  LOAD_GLOBAL              QtWidgets
              324  LOAD_ATTR                QMessageBox
              326  LOAD_METHOD              critical
              328  LOAD_FAST                'self'
              330  LOAD_ATTR                msgbox

 L. 505       332  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 506       334  LOAD_STR                 'Non-integer feature size'
              336  CALL_METHOD_3         3  '3 positional arguments'
              338  POP_TOP          

 L. 507       340  LOAD_CONST               None
              342  RETURN_VALUE     
            344_0  COME_FROM           304  '304'

 L. 508       344  LOAD_FAST                '_image_height'
              346  LOAD_CONST               2
              348  COMPARE_OP               <
          350_352  POP_JUMP_IF_TRUE    384  'to 384'
              354  LOAD_FAST                '_image_width'
              356  LOAD_CONST               2
              358  COMPARE_OP               <
          360_362  POP_JUMP_IF_TRUE    384  'to 384'

 L. 509       364  LOAD_FAST                '_image_height_new'
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

 L. 510       384  LOAD_GLOBAL              vis_msg
              386  LOAD_ATTR                print
              388  LOAD_STR                 'ERROR in ApplyMl15DDcnn4Prob: Features are not 2D'
              390  LOAD_STR                 'error'
              392  LOAD_CONST               ('type',)
              394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              396  POP_TOP          

 L. 511       398  LOAD_GLOBAL              QtWidgets
              400  LOAD_ATTR                QMessageBox
              402  LOAD_METHOD              critical
              404  LOAD_FAST                'self'
              406  LOAD_ATTR                msgbox

 L. 512       408  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 513       410  LOAD_STR                 'Features are not 2D'
              412  CALL_METHOD_3         3  '3 positional arguments'
              414  POP_TOP          

 L. 514       416  LOAD_CONST               None
              418  RETURN_VALUE     
            420_0  COME_FROM           380  '380'

 L. 516       420  LOAD_GLOBAL              basic_data
              422  LOAD_METHOD              str2int
              424  LOAD_FAST                'self'
              426  LOAD_ATTR                ldtbatchsize
              428  LOAD_METHOD              text
              430  CALL_METHOD_0         0  '0 positional arguments'
              432  CALL_METHOD_1         1  '1 positional argument'
              434  STORE_FAST               '_batch'

 L. 517       436  LOAD_FAST                '_batch'
              438  LOAD_CONST               False
              440  COMPARE_OP               is
          442_444  POP_JUMP_IF_TRUE    456  'to 456'
              446  LOAD_FAST                '_batch'
              448  LOAD_CONST               1
              450  COMPARE_OP               <
          452_454  POP_JUMP_IF_FALSE   492  'to 492'
            456_0  COME_FROM           442  '442'

 L. 518       456  LOAD_GLOBAL              vis_msg
              458  LOAD_ATTR                print
              460  LOAD_STR                 'ERROR in ApplyMl15DDcnn4Prob: Non-positive batch size'
              462  LOAD_STR                 'error'
              464  LOAD_CONST               ('type',)
              466  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              468  POP_TOP          

 L. 519       470  LOAD_GLOBAL              QtWidgets
              472  LOAD_ATTR                QMessageBox
              474  LOAD_METHOD              critical
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                msgbox

 L. 520       480  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 521       482  LOAD_STR                 'Non-positive batch size'
              484  CALL_METHOD_3         3  '3 positional arguments'
              486  POP_TOP          

 L. 522       488  LOAD_CONST               None
              490  RETURN_VALUE     
            492_0  COME_FROM           452  '452'

 L. 524       492  LOAD_GLOBAL              len
              494  LOAD_FAST                'self'
              496  LOAD_ATTR                ldtsave
              498  LOAD_METHOD              text
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  CALL_FUNCTION_1       1  '1 positional argument'
              504  LOAD_CONST               1
              506  COMPARE_OP               <
          508_510  POP_JUMP_IF_FALSE   548  'to 548'

 L. 525       512  LOAD_GLOBAL              vis_msg
              514  LOAD_ATTR                print
              516  LOAD_STR                 'ERROR in ApplyMl15DDcnn4Prob: No prefix specified'
              518  LOAD_STR                 'error'
              520  LOAD_CONST               ('type',)
              522  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              524  POP_TOP          

 L. 526       526  LOAD_GLOBAL              QtWidgets
              528  LOAD_ATTR                QMessageBox
              530  LOAD_METHOD              critical
              532  LOAD_FAST                'self'
              534  LOAD_ATTR                msgbox

 L. 527       536  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 528       538  LOAD_STR                 'No prefix specified'
              540  CALL_METHOD_3         3  '3 positional arguments'
              542  POP_TOP          

 L. 529       544  LOAD_CONST               None
              546  RETURN_VALUE     
            548_0  COME_FROM           508  '508'

 L. 531       548  LOAD_GLOBAL              len
              550  LOAD_FAST                'self'
              552  LOAD_ATTR                lwgtarget
              554  LOAD_METHOD              selectedItems
              556  CALL_METHOD_0         0  '0 positional arguments'
              558  CALL_FUNCTION_1       1  '1 positional argument'
              560  LOAD_CONST               1
              562  COMPARE_OP               <
          564_566  POP_JUMP_IF_FALSE   604  'to 604'

 L. 532       568  LOAD_GLOBAL              vis_msg
              570  LOAD_ATTR                print
              572  LOAD_STR                 'ERROR in ApplyMl15DDcnn4Prob: No target class specified'
              574  LOAD_STR                 'error'
              576  LOAD_CONST               ('type',)
              578  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              580  POP_TOP          

 L. 533       582  LOAD_GLOBAL              QtWidgets
              584  LOAD_ATTR                QMessageBox
              586  LOAD_METHOD              critical
              588  LOAD_FAST                'self'
              590  LOAD_ATTR                msgbox

 L. 534       592  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 535       594  LOAD_STR                 'No target class specified'
              596  CALL_METHOD_3         3  '3 positional arguments'
              598  POP_TOP          

 L. 536       600  LOAD_CONST               None
              602  RETURN_VALUE     
            604_0  COME_FROM           564  '564'

 L. 537       604  LOAD_LISTCOMP            '<code_object <listcomp>>'
              606  LOAD_STR                 'applyml15ddcnn4prob.clickBtnApplyMl15DDcnn4Prob.<locals>.<listcomp>'
              608  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              610  LOAD_FAST                'self'
              612  LOAD_ATTR                lwgtarget
              614  LOAD_METHOD              selectedItems
              616  CALL_METHOD_0         0  '0 positional arguments'
              618  GET_ITER         
              620  CALL_FUNCTION_1       1  '1 positional argument'
              622  STORE_FAST               '_classlist'

 L. 538       624  SETUP_LOOP          778  'to 778'
              626  LOAD_FAST                '_classlist'
              628  GET_ITER         
            630_0  COME_FROM           766  '766'
            630_1  COME_FROM           686  '686'
            630_2  COME_FROM           660  '660'
              630  FOR_ITER            776  'to 776'
              632  STORE_FAST               '_class'

 L. 539       634  LOAD_FAST                'self'
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

 L. 540       664  LOAD_FAST                'self'
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

 L. 541       690  LOAD_GLOBAL              QtWidgets
              692  LOAD_ATTR                QMessageBox
              694  LOAD_METHOD              question
              696  LOAD_FAST                'self'
              698  LOAD_ATTR                msgbox
              700  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 542       702  LOAD_FAST                'self'
              704  LOAD_ATTR                ldtsave
              706  LOAD_METHOD              text
              708  CALL_METHOD_0         0  '0 positional arguments'
              710  LOAD_STR                 ' already exists. Overwrite?'
              712  BINARY_ADD       

 L. 543       714  LOAD_GLOBAL              QtWidgets
              716  LOAD_ATTR                QMessageBox
              718  LOAD_ATTR                Yes
              720  LOAD_GLOBAL              QtWidgets
              722  LOAD_ATTR                QMessageBox
              724  LOAD_ATTR                No
              726  BINARY_OR        

 L. 544       728  LOAD_GLOBAL              QtWidgets
              730  LOAD_ATTR                QMessageBox
              732  LOAD_ATTR                No
              734  CALL_METHOD_5         5  '5 positional arguments'
              736  STORE_FAST               'reply'

 L. 545       738  LOAD_FAST                'reply'
              740  LOAD_GLOBAL              QtWidgets
              742  LOAD_ATTR                QMessageBox
              744  LOAD_ATTR                No
              746  COMPARE_OP               ==
          748_750  POP_JUMP_IF_FALSE   756  'to 756'

 L. 546       752  LOAD_CONST               None
              754  RETURN_VALUE     
            756_0  COME_FROM           748  '748'

 L. 547       756  LOAD_FAST                'reply'
              758  LOAD_GLOBAL              QtWidgets
              760  LOAD_ATTR                QMessageBox
              762  LOAD_ATTR                Yes
              764  COMPARE_OP               ==
          766_768  POP_JUMP_IF_FALSE   630  'to 630'

 L. 548       770  BREAK_LOOP       
          772_774  JUMP_BACK           630  'to 630'
              776  POP_BLOCK        
            778_0  COME_FROM_LOOP      624  '624'

 L. 550       778  LOAD_FAST                'self'
              780  LOAD_ATTR                survinfo
              782  STORE_FAST               '_seisinfo'

 L. 552       784  LOAD_CONST               0
              786  STORE_FAST               '_wdinl'

 L. 553       788  LOAD_CONST               0
              790  STORE_FAST               '_wdxl'

 L. 554       792  LOAD_CONST               0
              794  STORE_FAST               '_wdz'

 L. 555       796  LOAD_FAST                'self'
              798  LOAD_ATTR                cbbornt
              800  LOAD_METHOD              currentIndex
              802  CALL_METHOD_0         0  '0 positional arguments'
              804  LOAD_CONST               0
              806  COMPARE_OP               ==
          808_810  POP_JUMP_IF_FALSE   824  'to 824'

 L. 556       812  LOAD_GLOBAL              int
              814  LOAD_FAST                '_image_width'
              816  LOAD_CONST               2
              818  BINARY_TRUE_DIVIDE
              820  CALL_FUNCTION_1       1  '1 positional argument'
              822  STORE_FAST               '_wdxl'
            824_0  COME_FROM           808  '808'

 L. 557       824  LOAD_FAST                'self'
              826  LOAD_ATTR                cbbornt
              828  LOAD_METHOD              currentIndex
              830  CALL_METHOD_0         0  '0 positional arguments'
              832  LOAD_CONST               1
              834  COMPARE_OP               ==
          836_838  POP_JUMP_IF_FALSE   852  'to 852'

 L. 558       840  LOAD_GLOBAL              int
              842  LOAD_FAST                '_image_width'
              844  LOAD_CONST               2
              846  BINARY_TRUE_DIVIDE
              848  CALL_FUNCTION_1       1  '1 positional argument'
              850  STORE_FAST               '_wdinl'
            852_0  COME_FROM           836  '836'

 L. 559       852  LOAD_FAST                'self'
              854  LOAD_ATTR                cbbornt
              856  LOAD_METHOD              currentIndex
              858  CALL_METHOD_0         0  '0 positional arguments'
              860  LOAD_CONST               2
              862  COMPARE_OP               ==
          864_866  POP_JUMP_IF_FALSE   880  'to 880'

 L. 560       868  LOAD_GLOBAL              int
              870  LOAD_FAST                '_image_width'
              872  LOAD_CONST               2
              874  BINARY_TRUE_DIVIDE
              876  CALL_FUNCTION_1       1  '1 positional argument'
              878  STORE_FAST               '_wdinl'
            880_0  COME_FROM           864  '864'

 L. 561       880  BUILD_MAP_0           0 
              882  STORE_FAST               '_seisdict'

 L. 562       884  LOAD_FAST                'self'
              886  LOAD_ATTR                cbbornt
              888  LOAD_METHOD              currentIndex
              890  CALL_METHOD_0         0  '0 positional arguments'
              892  LOAD_CONST               0
              894  COMPARE_OP               ==
          896_898  POP_JUMP_IF_TRUE    916  'to 916'
              900  LOAD_FAST                'self'
              902  LOAD_ATTR                cbbornt
              904  LOAD_METHOD              currentIndex
              906  CALL_METHOD_0         0  '0 positional arguments'
              908  LOAD_CONST               1
              910  COMPARE_OP               ==
          912_914  POP_JUMP_IF_FALSE  1024  'to 1024'
            916_0  COME_FROM           896  '896'

 L. 563       916  LOAD_GLOBAL              np
              918  LOAD_METHOD              arange
              920  LOAD_CONST               0
              922  LOAD_FAST                '_seisinfo'
              924  LOAD_STR                 'ILNum'
              926  BINARY_SUBSCR    
              928  LOAD_FAST                '_seisinfo'
              930  LOAD_STR                 'XLNum'
              932  BINARY_SUBSCR    
              934  BINARY_MULTIPLY  
              936  CALL_METHOD_2         2  '2 positional arguments'
              938  STORE_FAST               '_all_sample'

 L. 564       940  LOAD_GLOBAL              np
              942  LOAD_METHOD              reshape
              944  LOAD_FAST                '_seisinfo'
              946  LOAD_STR                 'ILRange'
              948  BINARY_SUBSCR    
              950  LOAD_FAST                '_all_sample'
              952  LOAD_FAST                '_seisinfo'
              954  LOAD_STR                 'XLNum'
              956  BINARY_SUBSCR    
              958  BINARY_TRUE_DIVIDE
              960  LOAD_METHOD              astype
              962  LOAD_GLOBAL              int
              964  CALL_METHOD_1         1  '1 positional argument'
              966  BINARY_SUBSCR    

 L. 565       968  LOAD_CONST               -1
              970  LOAD_CONST               1
              972  BUILD_LIST_2          2 
              974  CALL_METHOD_2         2  '2 positional arguments'
              976  LOAD_FAST                '_seisdict'
              978  LOAD_STR                 'Inline'
              980  STORE_SUBSCR     

 L. 566       982  LOAD_GLOBAL              np
              984  LOAD_METHOD              reshape
              986  LOAD_FAST                '_seisinfo'
              988  LOAD_STR                 'XLRange'
              990  BINARY_SUBSCR    
              992  LOAD_FAST                '_all_sample'
              994  LOAD_FAST                '_seisinfo'
              996  LOAD_STR                 'XLNum'
              998  BINARY_SUBSCR    
             1000  BINARY_MODULO    
             1002  LOAD_METHOD              astype
             1004  LOAD_GLOBAL              int
             1006  CALL_METHOD_1         1  '1 positional argument'
             1008  BINARY_SUBSCR    

 L. 567      1010  LOAD_CONST               -1
             1012  LOAD_CONST               1
             1014  BUILD_LIST_2          2 
             1016  CALL_METHOD_2         2  '2 positional arguments'
             1018  LOAD_FAST                '_seisdict'
             1020  LOAD_STR                 'Crossline'
             1022  STORE_SUBSCR     
           1024_0  COME_FROM           912  '912'

 L. 568      1024  LOAD_FAST                'self'
             1026  LOAD_ATTR                cbbornt
             1028  LOAD_METHOD              currentIndex
             1030  CALL_METHOD_0         0  '0 positional arguments'
             1032  LOAD_CONST               2
             1034  COMPARE_OP               ==
         1036_1038  POP_JUMP_IF_FALSE  1148  'to 1148'

 L. 569      1040  LOAD_GLOBAL              np
             1042  LOAD_METHOD              arange
             1044  LOAD_CONST               0
             1046  LOAD_FAST                '_seisinfo'
             1048  LOAD_STR                 'ILNum'
             1050  BINARY_SUBSCR    
             1052  LOAD_FAST                '_seisinfo'
             1054  LOAD_STR                 'ZNum'
             1056  BINARY_SUBSCR    
             1058  BINARY_MULTIPLY  
             1060  CALL_METHOD_2         2  '2 positional arguments'
             1062  STORE_FAST               '_all_sample'

 L. 570      1064  LOAD_GLOBAL              np
             1066  LOAD_METHOD              reshape
             1068  LOAD_FAST                '_seisinfo'
             1070  LOAD_STR                 'ILRange'
             1072  BINARY_SUBSCR    
             1074  LOAD_FAST                '_all_sample'
             1076  LOAD_FAST                '_seisinfo'
             1078  LOAD_STR                 'ZNum'
             1080  BINARY_SUBSCR    
             1082  BINARY_TRUE_DIVIDE
             1084  LOAD_METHOD              astype
             1086  LOAD_GLOBAL              int
             1088  CALL_METHOD_1         1  '1 positional argument'
             1090  BINARY_SUBSCR    

 L. 571      1092  LOAD_CONST               -1
             1094  LOAD_CONST               1
             1096  BUILD_LIST_2          2 
             1098  CALL_METHOD_2         2  '2 positional arguments'
             1100  LOAD_FAST                '_seisdict'
             1102  LOAD_STR                 'Inline'
             1104  STORE_SUBSCR     

 L. 572      1106  LOAD_GLOBAL              np
             1108  LOAD_METHOD              reshape
             1110  LOAD_FAST                '_seisinfo'
             1112  LOAD_STR                 'ZRange'
             1114  BINARY_SUBSCR    
             1116  LOAD_FAST                '_all_sample'
             1118  LOAD_FAST                '_seisinfo'
             1120  LOAD_STR                 'ZNum'
             1122  BINARY_SUBSCR    
             1124  BINARY_MODULO    
             1126  LOAD_METHOD              astype
             1128  LOAD_GLOBAL              int
             1130  CALL_METHOD_1         1  '1 positional argument'
             1132  BINARY_SUBSCR    

 L. 573      1134  LOAD_CONST               -1
             1136  LOAD_CONST               1
             1138  BUILD_LIST_2          2 
             1140  CALL_METHOD_2         2  '2 positional arguments'
             1142  LOAD_FAST                '_seisdict'
             1144  LOAD_STR                 'Z'
             1146  STORE_SUBSCR     
           1148_0  COME_FROM          1036  '1036'

 L. 587      1148  LOAD_GLOBAL              basic_mdt
             1150  LOAD_METHOD              maxDictConstantRow
             1152  LOAD_FAST                '_seisdict'
             1154  CALL_METHOD_1         1  '1 positional argument'
             1156  STORE_FAST               '_nsample'

 L. 589      1158  LOAD_GLOBAL              int
             1160  LOAD_GLOBAL              np
             1162  LOAD_METHOD              ceil
             1164  LOAD_FAST                '_nsample'
             1166  LOAD_FAST                '_batch'
             1168  BINARY_TRUE_DIVIDE
             1170  CALL_METHOD_1         1  '1 positional argument'
             1172  CALL_FUNCTION_1       1  '1 positional argument'
             1174  STORE_FAST               '_nloop'

 L. 592      1176  LOAD_GLOBAL              QtWidgets
             1178  LOAD_METHOD              QProgressDialog
             1180  CALL_METHOD_0         0  '0 positional arguments'
             1182  STORE_FAST               '_pgsdlg'

 L. 593      1184  LOAD_GLOBAL              QtGui
             1186  LOAD_METHOD              QIcon
             1188  CALL_METHOD_0         0  '0 positional arguments'
             1190  STORE_FAST               'icon'

 L. 594      1192  LOAD_FAST                'icon'
             1194  LOAD_METHOD              addPixmap
             1196  LOAD_GLOBAL              QtGui
             1198  LOAD_METHOD              QPixmap
             1200  LOAD_GLOBAL              os
             1202  LOAD_ATTR                path
             1204  LOAD_METHOD              join
             1206  LOAD_FAST                'self'
             1208  LOAD_ATTR                iconpath
             1210  LOAD_STR                 'icons/check.png'
             1212  CALL_METHOD_2         2  '2 positional arguments'
             1214  CALL_METHOD_1         1  '1 positional argument'

 L. 595      1216  LOAD_GLOBAL              QtGui
             1218  LOAD_ATTR                QIcon
             1220  LOAD_ATTR                Normal
             1222  LOAD_GLOBAL              QtGui
             1224  LOAD_ATTR                QIcon
             1226  LOAD_ATTR                Off
             1228  CALL_METHOD_3         3  '3 positional arguments'
             1230  POP_TOP          

 L. 596      1232  LOAD_FAST                '_pgsdlg'
             1234  LOAD_METHOD              setWindowIcon
             1236  LOAD_FAST                'icon'
             1238  CALL_METHOD_1         1  '1 positional argument'
             1240  POP_TOP          

 L. 597      1242  LOAD_FAST                '_pgsdlg'
             1244  LOAD_METHOD              setWindowTitle
             1246  LOAD_STR                 'Apply 1.5D-DCNN'
             1248  CALL_METHOD_1         1  '1 positional argument'
             1250  POP_TOP          

 L. 598      1252  LOAD_FAST                '_pgsdlg'
             1254  LOAD_METHOD              setCancelButton
             1256  LOAD_CONST               None
             1258  CALL_METHOD_1         1  '1 positional argument'
             1260  POP_TOP          

 L. 599      1262  LOAD_FAST                '_pgsdlg'
             1264  LOAD_METHOD              setWindowFlags
             1266  LOAD_GLOBAL              QtCore
             1268  LOAD_ATTR                Qt
             1270  LOAD_ATTR                WindowStaysOnTopHint
             1272  CALL_METHOD_1         1  '1 positional argument'
             1274  POP_TOP          

 L. 600      1276  LOAD_FAST                '_pgsdlg'
             1278  LOAD_METHOD              forceShow
             1280  CALL_METHOD_0         0  '0 positional arguments'
             1282  POP_TOP          

 L. 601      1284  LOAD_FAST                '_pgsdlg'
             1286  LOAD_METHOD              setFixedWidth
             1288  LOAD_CONST               400
             1290  CALL_METHOD_1         1  '1 positional argument'
             1292  POP_TOP          

 L. 602      1294  LOAD_FAST                '_pgsdlg'
             1296  LOAD_METHOD              setMaximum
             1298  LOAD_FAST                '_nloop'
             1300  CALL_METHOD_1         1  '1 positional argument'
             1302  POP_TOP          

 L. 604      1304  LOAD_GLOBAL              np
             1306  LOAD_METHOD              zeros
             1308  LOAD_FAST                '_nsample'
             1310  LOAD_GLOBAL              len
             1312  LOAD_FAST                '_classlist'
             1314  CALL_FUNCTION_1       1  '1 positional argument'
             1316  LOAD_FAST                '_image_height'
             1318  BUILD_LIST_3          3 
             1320  CALL_METHOD_1         1  '1 positional argument'
             1322  STORE_FAST               '_result'

 L. 605      1324  LOAD_CONST               0
             1326  STORE_FAST               'idxstart'

 L. 606  1328_1330  SETUP_LOOP         1948  'to 1948'
             1332  LOAD_GLOBAL              range
             1334  LOAD_FAST                '_nloop'
             1336  CALL_FUNCTION_1       1  '1 positional argument'
             1338  GET_ITER         
         1340_1342  FOR_ITER           1946  'to 1946'
             1344  STORE_FAST               'i'

 L. 608      1346  LOAD_GLOBAL              QtCore
             1348  LOAD_ATTR                QCoreApplication
             1350  LOAD_METHOD              instance
             1352  CALL_METHOD_0         0  '0 positional arguments'
             1354  LOAD_METHOD              processEvents
             1356  CALL_METHOD_0         0  '0 positional arguments'
             1358  POP_TOP          

 L. 610      1360  LOAD_GLOBAL              sys
             1362  LOAD_ATTR                stdout
             1364  LOAD_METHOD              write

 L. 611      1366  LOAD_STR                 '\r>>> Apply 1.5D-DCNN, proceeding %.1f%% '
             1368  LOAD_GLOBAL              float
             1370  LOAD_FAST                'i'
             1372  CALL_FUNCTION_1       1  '1 positional argument'
             1374  LOAD_GLOBAL              float
             1376  LOAD_FAST                '_nloop'
             1378  CALL_FUNCTION_1       1  '1 positional argument'
             1380  BINARY_TRUE_DIVIDE
             1382  LOAD_CONST               100.0
             1384  BINARY_MULTIPLY  
             1386  BINARY_MODULO    
             1388  CALL_METHOD_1         1  '1 positional argument'
             1390  POP_TOP          

 L. 612      1392  LOAD_GLOBAL              sys
             1394  LOAD_ATTR                stdout
             1396  LOAD_METHOD              flush
             1398  CALL_METHOD_0         0  '0 positional arguments'
             1400  POP_TOP          

 L. 614      1402  LOAD_FAST                'idxstart'
             1404  LOAD_FAST                '_batch'
             1406  BINARY_ADD       
             1408  STORE_FAST               'idxend'

 L. 615      1410  LOAD_FAST                'idxend'
             1412  LOAD_FAST                '_nsample'
             1414  COMPARE_OP               >
         1416_1418  POP_JUMP_IF_FALSE  1424  'to 1424'

 L. 616      1420  LOAD_FAST                '_nsample'
             1422  STORE_FAST               'idxend'
           1424_0  COME_FROM          1416  '1416'

 L. 617      1424  LOAD_GLOBAL              np
             1426  LOAD_METHOD              linspace
             1428  LOAD_FAST                'idxstart'
             1430  LOAD_FAST                'idxend'
             1432  LOAD_CONST               1
             1434  BINARY_SUBTRACT  
             1436  LOAD_FAST                'idxend'
             1438  LOAD_FAST                'idxstart'
             1440  BINARY_SUBTRACT  
             1442  CALL_METHOD_3         3  '3 positional arguments'
             1444  LOAD_METHOD              astype
             1446  LOAD_GLOBAL              int
             1448  CALL_METHOD_1         1  '1 positional argument'
             1450  STORE_FAST               'idxlist'

 L. 618      1452  LOAD_FAST                'idxend'
             1454  STORE_FAST               'idxstart'

 L. 619      1456  LOAD_GLOBAL              basic_mdt
             1458  LOAD_METHOD              retrieveDictByIndex
             1460  LOAD_FAST                '_seisdict'
             1462  LOAD_FAST                'idxlist'
             1464  CALL_METHOD_2         2  '2 positional arguments'
             1466  STORE_FAST               '_dict'

 L. 621      1468  LOAD_FAST                '_dict'
             1470  LOAD_STR                 'Inline'
             1472  BINARY_SUBSCR    
             1474  STORE_FAST               '_targetdata'

 L. 622      1476  LOAD_FAST                'self'
             1478  LOAD_ATTR                cbbornt
             1480  LOAD_METHOD              currentIndex
             1482  CALL_METHOD_0         0  '0 positional arguments'
             1484  LOAD_CONST               0
             1486  COMPARE_OP               ==
         1488_1490  POP_JUMP_IF_TRUE   1508  'to 1508'
             1492  LOAD_FAST                'self'
             1494  LOAD_ATTR                cbbornt
             1496  LOAD_METHOD              currentIndex
             1498  CALL_METHOD_0         0  '0 positional arguments'
             1500  LOAD_CONST               1
             1502  COMPARE_OP               ==
         1504_1506  POP_JUMP_IF_FALSE  1612  'to 1612'
           1508_0  COME_FROM          1488  '1488'

 L. 623      1508  LOAD_GLOBAL              np
             1510  LOAD_ATTR                concatenate
             1512  LOAD_FAST                '_targetdata'
             1514  LOAD_FAST                '_dict'
             1516  LOAD_STR                 'Crossline'
             1518  BINARY_SUBSCR    
             1520  BUILD_TUPLE_2         2 
             1522  LOAD_CONST               1
             1524  LOAD_CONST               ('axis',)
             1526  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1528  STORE_FAST               '_targetdata'

 L. 624      1530  SETUP_LOOP         1612  'to 1612'
             1532  LOAD_FAST                '_features'
             1534  GET_ITER         
             1536  FOR_ITER           1610  'to 1610'
             1538  STORE_FAST               'f'

 L. 625      1540  LOAD_FAST                'self'
             1542  LOAD_ATTR                seisdata
             1544  LOAD_FAST                'f'
             1546  BINARY_SUBSCR    
             1548  STORE_FAST               '_data'

 L. 626      1550  LOAD_GLOBAL              seis_ays
             1552  LOAD_ATTR                retrieveSeisZTraceFrom3DMat
             1554  LOAD_FAST                '_data'
             1556  LOAD_FAST                '_targetdata'

 L. 627      1558  LOAD_FAST                'self'
             1560  LOAD_ATTR                survinfo

 L. 628      1562  LOAD_FAST                '_wdinl'
             1564  LOAD_FAST                '_wdxl'

 L. 629      1566  LOAD_CONST               False
             1568  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'verbose')
             1570  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1572  STORE_FAST               '_data'

 L. 630      1574  LOAD_FAST                '_data'
             1576  LOAD_CONST               None
             1578  LOAD_CONST               None
             1580  BUILD_SLICE_2         2 
             1582  LOAD_CONST               2
             1584  LOAD_CONST               2
             1586  LOAD_FAST                '_image_height'
             1588  LOAD_FAST                '_image_width'
             1590  BINARY_MULTIPLY  
             1592  BINARY_ADD       
             1594  BUILD_SLICE_2         2 
             1596  BUILD_TUPLE_2         2 
             1598  BINARY_SUBSCR    
             1600  LOAD_FAST                '_dict'
             1602  LOAD_FAST                'f'
             1604  STORE_SUBSCR     
         1606_1608  JUMP_BACK          1536  'to 1536'
             1610  POP_BLOCK        
           1612_0  COME_FROM_LOOP     1530  '1530'
           1612_1  COME_FROM          1504  '1504'

 L. 631      1612  LOAD_FAST                'self'
             1614  LOAD_ATTR                cbbornt
             1616  LOAD_METHOD              currentIndex
             1618  CALL_METHOD_0         0  '0 positional arguments'
             1620  LOAD_CONST               2
             1622  COMPARE_OP               ==
         1624_1626  POP_JUMP_IF_FALSE  1732  'to 1732'

 L. 632      1628  LOAD_GLOBAL              np
             1630  LOAD_ATTR                concatenate
             1632  LOAD_FAST                '_targetdata'
             1634  LOAD_FAST                '_dict'
             1636  LOAD_STR                 'Z'
             1638  BINARY_SUBSCR    
             1640  BUILD_TUPLE_2         2 
             1642  LOAD_CONST               1
             1644  LOAD_CONST               ('axis',)
             1646  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1648  STORE_FAST               '_targetdata'

 L. 633      1650  SETUP_LOOP         1732  'to 1732'
             1652  LOAD_FAST                '_features'
             1654  GET_ITER         
             1656  FOR_ITER           1730  'to 1730'
             1658  STORE_FAST               'f'

 L. 634      1660  LOAD_FAST                'self'
             1662  LOAD_ATTR                seisdata
             1664  LOAD_FAST                'f'
             1666  BINARY_SUBSCR    
             1668  STORE_FAST               '_data'

 L. 635      1670  LOAD_GLOBAL              seis_ays
             1672  LOAD_ATTR                retrieveSeisXLTraceFrom3DMat
             1674  LOAD_FAST                '_data'
             1676  LOAD_FAST                '_targetdata'

 L. 636      1678  LOAD_FAST                'self'
             1680  LOAD_ATTR                survinfo

 L. 637      1682  LOAD_FAST                '_wdinl'
             1684  LOAD_FAST                '_wdz'

 L. 638      1686  LOAD_CONST               False
             1688  LOAD_CONST               ('seisinfo', 'wdinl', 'wdz', 'verbose')
             1690  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1692  STORE_FAST               '_data'

 L. 639      1694  LOAD_FAST                '_data'
             1696  LOAD_CONST               None
             1698  LOAD_CONST               None
             1700  BUILD_SLICE_2         2 
             1702  LOAD_CONST               2
             1704  LOAD_CONST               2
             1706  LOAD_FAST                '_image_height'
             1708  LOAD_FAST                '_image_width'
             1710  BINARY_MULTIPLY  
             1712  BINARY_ADD       
             1714  BUILD_SLICE_2         2 
             1716  BUILD_TUPLE_2         2 
             1718  BINARY_SUBSCR    
             1720  LOAD_FAST                '_dict'
             1722  LOAD_FAST                'f'
             1724  STORE_SUBSCR     
         1726_1728  JUMP_BACK          1656  'to 1656'
             1730  POP_BLOCK        
           1732_0  COME_FROM_LOOP     1650  '1650'
           1732_1  COME_FROM          1624  '1624'

 L. 640      1732  LOAD_FAST                '_image_height_new'
             1734  LOAD_FAST                '_image_height'
             1736  COMPARE_OP               !=
         1738_1740  POP_JUMP_IF_TRUE   1752  'to 1752'
             1742  LOAD_FAST                '_image_width_new'
             1744  LOAD_FAST                '_image_width'
             1746  COMPARE_OP               !=
         1748_1750  POP_JUMP_IF_FALSE  1796  'to 1796'
           1752_0  COME_FROM          1738  '1738'

 L. 641      1752  SETUP_LOOP         1796  'to 1796'
             1754  LOAD_FAST                '_features'
             1756  GET_ITER         
             1758  FOR_ITER           1794  'to 1794'
             1760  STORE_FAST               'f'

 L. 642      1762  LOAD_GLOBAL              basic_image
             1764  LOAD_ATTR                changeImageSize
             1766  LOAD_FAST                '_dict'
             1768  LOAD_FAST                'f'
             1770  BINARY_SUBSCR    

 L. 643      1772  LOAD_FAST                '_image_height'

 L. 644      1774  LOAD_FAST                '_image_width'

 L. 645      1776  LOAD_FAST                '_image_height_new'

 L. 646      1778  LOAD_FAST                '_image_width_new'
             1780  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1782  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1784  LOAD_FAST                '_dict'
             1786  LOAD_FAST                'f'
             1788  STORE_SUBSCR     
         1790_1792  JUMP_BACK          1758  'to 1758'
             1794  POP_BLOCK        
           1796_0  COME_FROM_LOOP     1752  '1752'
           1796_1  COME_FROM          1748  '1748'

 L. 649      1796  LOAD_GLOBAL              ml_dcnn15d
             1798  LOAD_ATTR                probabilityFrom15DDCNNSegmentor
             1800  LOAD_FAST                '_dict'

 L. 650      1802  LOAD_FAST                '_image_height_new'

 L. 651      1804  LOAD_FAST                '_image_width_new'

 L. 652      1806  LOAD_FAST                'self'
             1808  LOAD_ATTR                modelpath

 L. 653      1810  LOAD_FAST                'self'
             1812  LOAD_ATTR                modelname

 L. 654      1814  LOAD_FAST                '_classlist'

 L. 655      1816  LOAD_FAST                '_batch'
             1818  LOAD_CONST               False
             1820  LOAD_CONST               ('imageheight', 'imagewidth', 'dcnnpath', 'dcnnname', 'targetlist', 'batchsize', 'verbose')
             1822  CALL_FUNCTION_KW_8     8  '8 total positional and keyword args'
             1824  STORE_FAST               '_rst'

 L. 657      1826  LOAD_FAST                '_image_height_new'
             1828  LOAD_FAST                '_image_height'
             1830  COMPARE_OP               !=
         1832_1834  POP_JUMP_IF_FALSE  1888  'to 1888'

 L. 658      1836  LOAD_GLOBAL              np
             1838  LOAD_METHOD              reshape
             1840  LOAD_FAST                '_rst'
             1842  LOAD_GLOBAL              np
             1844  LOAD_METHOD              shape
             1846  LOAD_FAST                '_rst'
             1848  CALL_METHOD_1         1  '1 positional argument'
             1850  LOAD_CONST               0
             1852  BINARY_SUBSCR    
             1854  LOAD_GLOBAL              len
             1856  LOAD_FAST                '_classlist'
             1858  CALL_FUNCTION_1       1  '1 positional argument'
             1860  BINARY_MULTIPLY  
             1862  LOAD_FAST                '_image_height_new'
             1864  BUILD_LIST_2          2 
             1866  CALL_METHOD_2         2  '2 positional arguments'
             1868  STORE_FAST               '_rst'

 L. 659      1870  LOAD_GLOBAL              basic_curve
             1872  LOAD_ATTR                changeCurveSize
             1874  LOAD_FAST                '_rst'

 L. 660      1876  LOAD_FAST                '_image_height_new'

 L. 661      1878  LOAD_FAST                '_image_height'
             1880  LOAD_STR                 'linear'
             1882  LOAD_CONST               ('length', 'length_new', 'kind')
             1884  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1886  STORE_FAST               '_rst'
           1888_0  COME_FROM          1832  '1832'

 L. 662      1888  LOAD_GLOBAL              np
             1890  LOAD_METHOD              reshape
             1892  LOAD_FAST                '_rst'
             1894  LOAD_CONST               -1
             1896  LOAD_GLOBAL              len
             1898  LOAD_FAST                '_classlist'
             1900  CALL_FUNCTION_1       1  '1 positional argument'
             1902  LOAD_FAST                '_image_height'
             1904  BUILD_LIST_3          3 
             1906  CALL_METHOD_2         2  '2 positional arguments'
             1908  LOAD_FAST                '_result'
             1910  LOAD_FAST                'idxlist'
             1912  LOAD_CONST               None
             1914  LOAD_CONST               None
             1916  BUILD_SLICE_2         2 
             1918  LOAD_CONST               None
             1920  LOAD_CONST               None
             1922  BUILD_SLICE_2         2 
             1924  BUILD_TUPLE_3         3 
             1926  STORE_SUBSCR     

 L. 665      1928  LOAD_FAST                '_pgsdlg'
             1930  LOAD_METHOD              setValue
             1932  LOAD_FAST                'i'
             1934  LOAD_CONST               1
             1936  BINARY_ADD       
             1938  CALL_METHOD_1         1  '1 positional argument'
             1940  POP_TOP          
         1942_1944  JUMP_BACK          1340  'to 1340'
             1946  POP_BLOCK        
           1948_0  COME_FROM_LOOP     1328  '1328'

 L. 667      1948  LOAD_GLOBAL              print
             1950  LOAD_STR                 'Done'
             1952  CALL_FUNCTION_1       1  '1 positional argument'
             1954  POP_TOP          

 L. 669      1956  SETUP_LOOP         2188  'to 2188'
             1958  LOAD_GLOBAL              range
             1960  LOAD_GLOBAL              len
             1962  LOAD_FAST                '_classlist'
             1964  CALL_FUNCTION_1       1  '1 positional argument'
             1966  CALL_FUNCTION_1       1  '1 positional argument'
             1968  GET_ITER         
             1970  FOR_ITER           2186  'to 2186'
             1972  STORE_FAST               'i'

 L. 670      1974  LOAD_FAST                'self'
             1976  LOAD_ATTR                cbbornt
             1978  LOAD_METHOD              currentIndex
             1980  CALL_METHOD_0         0  '0 positional arguments'
             1982  LOAD_CONST               0
             1984  COMPARE_OP               ==
         1986_1988  POP_JUMP_IF_TRUE   2006  'to 2006'
             1990  LOAD_FAST                'self'
             1992  LOAD_ATTR                cbbornt
             1994  LOAD_METHOD              currentIndex
             1996  CALL_METHOD_0         0  '0 positional arguments'
             1998  LOAD_CONST               1
             2000  COMPARE_OP               ==
         2002_2004  POP_JUMP_IF_FALSE  2072  'to 2072'
           2006_0  COME_FROM          1986  '1986'

 L. 671      2006  LOAD_GLOBAL              np
             2008  LOAD_METHOD              reshape
             2010  LOAD_FAST                '_result'
             2012  LOAD_CONST               None
             2014  LOAD_CONST               None
             2016  BUILD_SLICE_2         2 
             2018  LOAD_FAST                'i'
             2020  LOAD_CONST               None
             2022  LOAD_CONST               None
             2024  BUILD_SLICE_2         2 
             2026  BUILD_TUPLE_3         3 
             2028  BINARY_SUBSCR    
             2030  LOAD_FAST                '_seisinfo'
             2032  LOAD_STR                 'ILNum'
             2034  BINARY_SUBSCR    
             2036  LOAD_FAST                '_seisinfo'
             2038  LOAD_STR                 'XLNum'
             2040  BINARY_SUBSCR    
             2042  LOAD_FAST                '_seisinfo'
             2044  LOAD_STR                 'ZNum'
             2046  BINARY_SUBSCR    
             2048  BUILD_LIST_3          3 
             2050  CALL_METHOD_2         2  '2 positional arguments'
             2052  STORE_FAST               '_rst'

 L. 672      2054  LOAD_GLOBAL              np
             2056  LOAD_METHOD              transpose
             2058  LOAD_FAST                '_rst'
             2060  LOAD_CONST               2
             2062  LOAD_CONST               1
             2064  LOAD_CONST               0
             2066  BUILD_LIST_3          3 
             2068  CALL_METHOD_2         2  '2 positional arguments'
             2070  STORE_FAST               '_rst'
           2072_0  COME_FROM          2002  '2002'

 L. 673      2072  LOAD_FAST                'self'
             2074  LOAD_ATTR                cbbornt
             2076  LOAD_METHOD              currentIndex
             2078  CALL_METHOD_0         0  '0 positional arguments'
             2080  LOAD_CONST               2
             2082  COMPARE_OP               ==
         2084_2086  POP_JUMP_IF_FALSE  2154  'to 2154'

 L. 674      2088  LOAD_GLOBAL              np
             2090  LOAD_METHOD              reshape
             2092  LOAD_FAST                '_result'
             2094  LOAD_CONST               None
             2096  LOAD_CONST               None
             2098  BUILD_SLICE_2         2 
             2100  LOAD_FAST                'i'
             2102  LOAD_CONST               None
             2104  LOAD_CONST               None
             2106  BUILD_SLICE_2         2 
             2108  BUILD_TUPLE_3         3 
             2110  BINARY_SUBSCR    
             2112  LOAD_FAST                '_seisinfo'
             2114  LOAD_STR                 'ILNum'
             2116  BINARY_SUBSCR    
             2118  LOAD_FAST                '_seisinfo'
             2120  LOAD_STR                 'ZNum'
             2122  BINARY_SUBSCR    
             2124  LOAD_FAST                '_seisinfo'
             2126  LOAD_STR                 'XLNum'
             2128  BINARY_SUBSCR    
             2130  BUILD_LIST_3          3 
             2132  CALL_METHOD_2         2  '2 positional arguments'
             2134  STORE_FAST               '_rst'

 L. 675      2136  LOAD_GLOBAL              np
             2138  LOAD_METHOD              transpose
             2140  LOAD_FAST                '_rst'
             2142  LOAD_CONST               1
             2144  LOAD_CONST               2
             2146  LOAD_CONST               0
             2148  BUILD_LIST_3          3 
             2150  CALL_METHOD_2         2  '2 positional arguments'
             2152  STORE_FAST               '_rst'
           2154_0  COME_FROM          2084  '2084'

 L. 677      2154  LOAD_FAST                '_rst'
             2156  LOAD_FAST                'self'
             2158  LOAD_ATTR                seisdata
             2160  LOAD_FAST                'self'
             2162  LOAD_ATTR                ldtsave
             2164  LOAD_METHOD              text
             2166  CALL_METHOD_0         0  '0 positional arguments'
             2168  LOAD_GLOBAL              str
             2170  LOAD_FAST                '_classlist'
             2172  LOAD_FAST                'i'
             2174  BINARY_SUBSCR    
             2176  CALL_FUNCTION_1       1  '1 positional argument'
             2178  BINARY_ADD       
             2180  STORE_SUBSCR     
         2182_2184  JUMP_BACK          1970  'to 1970'
             2186  POP_BLOCK        
           2188_0  COME_FROM_LOOP     1956  '1956'

 L. 679      2188  LOAD_GLOBAL              QtWidgets
             2190  LOAD_ATTR                QMessageBox
             2192  LOAD_METHOD              information
             2194  LOAD_FAST                'self'
             2196  LOAD_ATTR                msgbox

 L. 680      2198  LOAD_STR                 'Apply 1.5D-DCNN'

 L. 681      2200  LOAD_STR                 'DCNN applied successfully'
             2202  CALL_METHOD_3         3  '3 positional arguments'
             2204  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 2202

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
    ApplyMl15DDcnn4Prob = QtWidgets.QWidget()
    gui = applyml15ddcnn4prob()
    gui.setupGUI(ApplyMl15DDcnn4Prob)
    ApplyMl15DDcnn4Prob.show()
    sys.exit(app.exec_())