# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\applyml2ddcnn4pred.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 35062 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.image as basic_image
import cognitivegeo.src.vis.messager as vis_msg
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.dcnnsegmentor as ml_dcnn
import cognitivegeo.src.gui.viewml2ddcnn as gui_viewml2ddcnn
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class applyml2ddcnn4pred(object):
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

    def setupGUI(self, ApplyMl2DDcnn4Pred):
        ApplyMl2DDcnn4Pred.setObjectName('ApplyMl2DDcnn4Pred')
        ApplyMl2DDcnn4Pred.setFixedSize(810, 490)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ApplyMl2DDcnn4Pred.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ApplyMl2DDcnn4Pred)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ApplyMl2DDcnn4Pred)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ApplyMl2DDcnn4Pred)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(ApplyMl2DDcnn4Pred)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 230, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 230, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(ApplyMl2DDcnn4Pred)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 230, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 270, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(ApplyMl2DDcnn4Pred)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 270, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 230, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(ApplyMl2DDcnn4Pred)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(ApplyMl2DDcnn4Pred)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ApplyMl2DDcnn4Pred)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ApplyMl2DDcnn4Pred)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ApplyMl2DDcnn4Pred)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 190))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(ApplyMl2DDcnn4Pred)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(ApplyMl2DDcnn4Pred)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 190))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 350, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 350, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ApplyMl2DDcnn4Pred)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 350, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 390, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ApplyMl2DDcnn4Pred)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 390, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 350, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 350, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ApplyMl2DDcnn4Pred)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 350, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 390, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ApplyMl2DDcnn4Pred)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 390, 40, 30))
        self.lblpara = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 320, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ApplyMl2DDcnn4Pred)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblsave = QtWidgets.QLabel(ApplyMl2DDcnn4Pred)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ApplyMl2DDcnn4Pred)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.btnapply = QtWidgets.QPushButton(ApplyMl2DDcnn4Pred)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(320, 440, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ApplyMl2DDcnn4Pred)
        self.msgbox.setObjectName('msgbox')
        _center_x = ApplyMl2DDcnn4Pred.geometry().center().x()
        _center_y = ApplyMl2DDcnn4Pred.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ApplyMl2DDcnn4Pred)
        QtCore.QMetaObject.connectSlotsByName(ApplyMl2DDcnn4Pred)

    def retranslateGUI(self, ApplyMl2DDcnn4Pred):
        self.dialog = ApplyMl2DDcnn4Pred
        _translate = QtCore.QCoreApplication.translate
        ApplyMl2DDcnn4Pred.setWindowTitle(_translate('ApplyMl2DDcnn4Pred', 'Apply 2D-DCNN for prediction'))
        self.lblfrom.setText(_translate('ApplyMl2DDcnn4Pred', 'Select network:'))
        self.ldtfrom.setText(_translate('ApplyMl2DDcnn4Pred', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ApplyMl2DDcnn4Pred', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ApplyMl2DDcnn4Pred', 'Training features:'))
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblornt.setText(_translate('ApplyMl2DDcnn4Pred', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.cbbornt.currentIndexChanged.connect(self.changeCbbOrnt)
        self.lbloldsize.setText(_translate('ApplyMl2DDcnn4Pred', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('ApplyMl2DDcnn4Pred', 'height='))
        self.ldtoldheight.setText(_translate('ApplyMl2DDcnn4Pred', '0'))
        self.ldtoldheight.setEnabled(False)
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('ApplyMl2DDcnn4Pred', 'width='))
        self.ldtoldwidth.setText(_translate('ApplyMl2DDcnn4Pred', '0'))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtoldwidth.setEnabled(False)
        self.lblnewsize.setText(_translate('ApplyMl2DDcnn4Pred', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('ApplyMl2DDcnn4Pred', 'height='))
        self.ldtnewheight.setText(_translate('ApplyMl2DDcnn4Pred', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('ApplyMl2DDcnn4Pred', 'width='))
        self.ldtnewwidth.setText(_translate('ApplyMl2DDcnn4Pred', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('ApplyMl2DDcnn4Pred', 'Pre-trained DCNN architecture:'))
        self.btnviewnetwork.setText(_translate('ApplyMl2DDcnn4Pred', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('ApplyMl2DDcnn4Pred', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ApplyMl2DDcnn4Pred', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('ApplyMl2DDcnn4Pred', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('ApplyMl2DDcnn4Pred', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('ApplyMl2DDcnn4Pred', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ApplyMl2DDcnn4Pred', 'height='))
        self.ldtmaskheight.setText(_translate('ApplyMl2DDcnn4Pred', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ApplyMl2DDcnn4Pred', 'width='))
        self.ldtmaskwidth.setText(_translate('ApplyMl2DDcnn4Pred', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ApplyMl2DDcnn4Pred', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ApplyMl2DDcnn4Pred', 'height='))
        self.ldtpoolheight.setText(_translate('ApplyMl2DDcnn4Pred', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ApplyMl2DDcnn4Pred', 'width='))
        self.ldtpoolwidth.setText(_translate('ApplyMl2DDcnn4Pred', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ApplyMl2DDcnn4Pred', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ApplyMl2DDcnn4Pred', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ApplyMl2DDcnn4Pred', '5'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('ApplyMl2DDcnn4Pred', 'Output name='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ApplyMl2DDcnn4Pred', 'dcnn'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('ApplyMl2DDcnn4Pred', 'Apply 2D-DCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnApplyMl2DDcnn4Pred)

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.checkDCNNModel(self.modelpath, self.modelname) is True:
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
        if ml_tfm.checkDCNNModel(self.modelpath, self.modelname):
            _shape = self.getImageSize(self.lwgfeature.currentItem().text())
        _height = _shape[0]
        _width = _shape[1]
        self.ldtoldheight.setText(str(_height))
        self.ldtoldwidth.setText(str(_width))

    def changeCbbOrnt(self):
        _shape = [
         0, 0]
        if ml_tfm.checkDCNNModel(self.modelpath, self.modelname):
            _shape = self.getImageSize(self.lwgfeature.currentItem().text())
        _height = _shape[0]
        _width = _shape[1]
        self.ldtoldheight.setText(str(_height))
        self.ldtoldwidth.setText(str(_width))

    def changeLdtNconvblock(self):
        if ml_tfm.checkDCNNModel(self.modelpath, self.modelname) is True:
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
        if ml_tfm.checkDCNNModel(self.modelpath, self.modelname) is True:
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

    def clickBtnApplyMl2DDcnn4Pred--- This code section failed: ---

 L. 455         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 457         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 458        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in ApplyMl2DDcnn4Pred: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 459        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 460        44  LOAD_STR                 'Apply 2D-DCNN'

 L. 461        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 462        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 464        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkDCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 465        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in ApplyMl2DDcnn4Pred: No pre-DCNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 466        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 467       100  LOAD_STR                 'Apply 2D-DCNN'

 L. 468       102  LOAD_STR                 'No pre-DCNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 469       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 471       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 472       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 473       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in ApplyMl2DDcnn4Pred: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    

 L. 474       152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 475       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 476       170  LOAD_STR                 'Apply 2D-DCNN'

 L. 477       172  LOAD_STR                 "Feature '"
              174  LOAD_FAST                'f'
              176  BINARY_ADD       
              178  LOAD_STR                 "' not found in seismic data"
              180  BINARY_ADD       
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L. 478       186  LOAD_CONST               None
              188  RETURN_VALUE     
              190  JUMP_BACK           124  'to 124'
              192  POP_BLOCK        
            194_0  COME_FROM_LOOP      112  '112'

 L. 480       194  LOAD_FAST                'self'
              196  LOAD_ATTR                modelinfo
              198  LOAD_STR                 'feature_list'
              200  BINARY_SUBSCR    
              202  STORE_FAST               '_features'

 L. 481       204  LOAD_GLOBAL              basic_data
              206  LOAD_METHOD              str2int
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                ldtoldheight
              212  LOAD_METHOD              text
              214  CALL_METHOD_0         0  '0 positional arguments'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  STORE_FAST               '_image_height'

 L. 482       220  LOAD_GLOBAL              basic_data
              222  LOAD_METHOD              str2int
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                ldtoldwidth
              228  LOAD_METHOD              text
              230  CALL_METHOD_0         0  '0 positional arguments'
              232  CALL_METHOD_1         1  '1 positional argument'
              234  STORE_FAST               '_image_width'

 L. 483       236  LOAD_GLOBAL              basic_data
              238  LOAD_METHOD              str2int
              240  LOAD_FAST                'self'
              242  LOAD_ATTR                ldtnewheight
              244  LOAD_METHOD              text
              246  CALL_METHOD_0         0  '0 positional arguments'
              248  CALL_METHOD_1         1  '1 positional argument'
              250  STORE_FAST               '_image_height_new'

 L. 484       252  LOAD_GLOBAL              basic_data
              254  LOAD_METHOD              str2int
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                ldtnewwidth
              260  LOAD_METHOD              text
              262  CALL_METHOD_0         0  '0 positional arguments'
              264  CALL_METHOD_1         1  '1 positional argument'
              266  STORE_FAST               '_image_width_new'

 L. 485       268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               False
              272  COMPARE_OP               is
          274_276  POP_JUMP_IF_TRUE    308  'to 308'
              278  LOAD_FAST                '_image_width'
              280  LOAD_CONST               False
              282  COMPARE_OP               is
          284_286  POP_JUMP_IF_TRUE    308  'to 308'

 L. 486       288  LOAD_FAST                '_image_height_new'
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

 L. 487       308  LOAD_GLOBAL              vis_msg
              310  LOAD_ATTR                print
              312  LOAD_STR                 'ERROR in ApplyMl2DDcnn4Pred: Non-integer feature size'
              314  LOAD_STR                 'error'
              316  LOAD_CONST               ('type',)
              318  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              320  POP_TOP          

 L. 488       322  LOAD_GLOBAL              QtWidgets
              324  LOAD_ATTR                QMessageBox
              326  LOAD_METHOD              critical
              328  LOAD_FAST                'self'
              330  LOAD_ATTR                msgbox

 L. 489       332  LOAD_STR                 'Apply 2D-DCNN'

 L. 490       334  LOAD_STR                 'Non-integer feature size'
              336  CALL_METHOD_3         3  '3 positional arguments'
              338  POP_TOP          

 L. 491       340  LOAD_CONST               None
              342  RETURN_VALUE     
            344_0  COME_FROM           304  '304'

 L. 492       344  LOAD_FAST                '_image_height'
              346  LOAD_CONST               2
              348  COMPARE_OP               <
          350_352  POP_JUMP_IF_TRUE    384  'to 384'
              354  LOAD_FAST                '_image_width'
              356  LOAD_CONST               2
              358  COMPARE_OP               <
          360_362  POP_JUMP_IF_TRUE    384  'to 384'

 L. 493       364  LOAD_FAST                '_image_height_new'
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

 L. 494       384  LOAD_GLOBAL              vis_msg
              386  LOAD_ATTR                print
              388  LOAD_STR                 'ERROR in ApplyMl2DDcnn4Pred: Features are not 2D'
              390  LOAD_STR                 'error'
              392  LOAD_CONST               ('type',)
              394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              396  POP_TOP          

 L. 495       398  LOAD_GLOBAL              QtWidgets
              400  LOAD_ATTR                QMessageBox
              402  LOAD_METHOD              critical
              404  LOAD_FAST                'self'
              406  LOAD_ATTR                msgbox

 L. 496       408  LOAD_STR                 'Apply 2D-DCNN'

 L. 497       410  LOAD_STR                 'Features are not 2D'
              412  CALL_METHOD_3         3  '3 positional arguments'
              414  POP_TOP          

 L. 498       416  LOAD_CONST               None
              418  RETURN_VALUE     
            420_0  COME_FROM           380  '380'

 L. 500       420  LOAD_GLOBAL              basic_data
              422  LOAD_METHOD              str2int
              424  LOAD_FAST                'self'
              426  LOAD_ATTR                ldtbatchsize
              428  LOAD_METHOD              text
              430  CALL_METHOD_0         0  '0 positional arguments'
              432  CALL_METHOD_1         1  '1 positional argument'
              434  STORE_FAST               '_batch'

 L. 501       436  LOAD_FAST                '_batch'
              438  LOAD_CONST               False
              440  COMPARE_OP               is
          442_444  POP_JUMP_IF_TRUE    456  'to 456'
              446  LOAD_FAST                '_batch'
              448  LOAD_CONST               1
              450  COMPARE_OP               <
          452_454  POP_JUMP_IF_FALSE   492  'to 492'
            456_0  COME_FROM           442  '442'

 L. 502       456  LOAD_GLOBAL              vis_msg
              458  LOAD_ATTR                print
              460  LOAD_STR                 'ERROR in ApplyMl2DDcnn4Pred: Non-positive batch size'
              462  LOAD_STR                 'error'
              464  LOAD_CONST               ('type',)
              466  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              468  POP_TOP          

 L. 503       470  LOAD_GLOBAL              QtWidgets
              472  LOAD_ATTR                QMessageBox
              474  LOAD_METHOD              critical
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                msgbox

 L. 504       480  LOAD_STR                 'Apply 2D-DCNN'

 L. 505       482  LOAD_STR                 'Non-positive batch size'
              484  CALL_METHOD_3         3  '3 positional arguments'
              486  POP_TOP          

 L. 506       488  LOAD_CONST               None
              490  RETURN_VALUE     
            492_0  COME_FROM           452  '452'

 L. 508       492  LOAD_GLOBAL              len
              494  LOAD_FAST                'self'
              496  LOAD_ATTR                ldtsave
              498  LOAD_METHOD              text
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  CALL_FUNCTION_1       1  '1 positional argument'
              504  LOAD_CONST               1
              506  COMPARE_OP               <
          508_510  POP_JUMP_IF_FALSE   548  'to 548'

 L. 509       512  LOAD_GLOBAL              vis_msg
              514  LOAD_ATTR                print
              516  LOAD_STR                 'ERROR in ApplyMl2DDcnn4Pred: No name specified'
              518  LOAD_STR                 'error'
              520  LOAD_CONST               ('type',)
              522  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              524  POP_TOP          

 L. 510       526  LOAD_GLOBAL              QtWidgets
              528  LOAD_ATTR                QMessageBox
              530  LOAD_METHOD              critical
              532  LOAD_FAST                'self'
              534  LOAD_ATTR                msgbox

 L. 511       536  LOAD_STR                 'Apply 2D-DCNN'

 L. 512       538  LOAD_STR                 'No name specified'
              540  CALL_METHOD_3         3  '3 positional arguments'
              542  POP_TOP          

 L. 513       544  LOAD_CONST               None
              546  RETURN_VALUE     
            548_0  COME_FROM           508  '508'

 L. 514       548  LOAD_FAST                'self'
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

 L. 515       588  LOAD_GLOBAL              QtWidgets
              590  LOAD_ATTR                QMessageBox
              592  LOAD_METHOD              question
              594  LOAD_FAST                'self'
              596  LOAD_ATTR                msgbox
              598  LOAD_STR                 'Apply 2D-DCNN'

 L. 516       600  LOAD_FAST                'self'
              602  LOAD_ATTR                ldtsave
              604  LOAD_METHOD              text
              606  CALL_METHOD_0         0  '0 positional arguments'
              608  LOAD_STR                 ' already exists. Overwrite?'
              610  BINARY_ADD       

 L. 517       612  LOAD_GLOBAL              QtWidgets
              614  LOAD_ATTR                QMessageBox
              616  LOAD_ATTR                Yes
              618  LOAD_GLOBAL              QtWidgets
              620  LOAD_ATTR                QMessageBox
              622  LOAD_ATTR                No
              624  BINARY_OR        

 L. 518       626  LOAD_GLOBAL              QtWidgets
              628  LOAD_ATTR                QMessageBox
              630  LOAD_ATTR                No
              632  CALL_METHOD_5         5  '5 positional arguments'
              634  STORE_FAST               'reply'

 L. 520       636  LOAD_FAST                'reply'
              638  LOAD_GLOBAL              QtWidgets
              640  LOAD_ATTR                QMessageBox
              642  LOAD_ATTR                No
              644  COMPARE_OP               ==
          646_648  POP_JUMP_IF_FALSE   654  'to 654'

 L. 521       650  LOAD_CONST               None
              652  RETURN_VALUE     
            654_0  COME_FROM           646  '646'
            654_1  COME_FROM           584  '584'
            654_2  COME_FROM           566  '566'

 L. 523       654  LOAD_FAST                'self'
              656  LOAD_ATTR                survinfo
              658  STORE_FAST               '_seisinfo'

 L. 525       660  LOAD_CONST               0
              662  STORE_FAST               '_nsample'

 L. 526       664  LOAD_FAST                'self'
              666  LOAD_ATTR                cbbornt
              668  LOAD_METHOD              currentIndex
              670  CALL_METHOD_0         0  '0 positional arguments'
              672  LOAD_CONST               0
              674  COMPARE_OP               ==
          676_678  POP_JUMP_IF_FALSE   688  'to 688'

 L. 527       680  LOAD_FAST                '_seisinfo'
              682  LOAD_STR                 'ILNum'
              684  BINARY_SUBSCR    
              686  STORE_FAST               '_nsample'
            688_0  COME_FROM           676  '676'

 L. 528       688  LOAD_FAST                'self'
              690  LOAD_ATTR                cbbornt
              692  LOAD_METHOD              currentIndex
              694  CALL_METHOD_0         0  '0 positional arguments'
              696  LOAD_CONST               1
              698  COMPARE_OP               ==
          700_702  POP_JUMP_IF_FALSE   712  'to 712'

 L. 529       704  LOAD_FAST                '_seisinfo'
              706  LOAD_STR                 'XLNum'
              708  BINARY_SUBSCR    
              710  STORE_FAST               '_nsample'
            712_0  COME_FROM           700  '700'

 L. 530       712  LOAD_FAST                'self'
              714  LOAD_ATTR                cbbornt
              716  LOAD_METHOD              currentIndex
              718  CALL_METHOD_0         0  '0 positional arguments'
              720  LOAD_CONST               2
              722  COMPARE_OP               ==
          724_726  POP_JUMP_IF_FALSE   736  'to 736'

 L. 531       728  LOAD_FAST                '_seisinfo'
              730  LOAD_STR                 'ZNum'
              732  BINARY_SUBSCR    
              734  STORE_FAST               '_nsample'
            736_0  COME_FROM           724  '724'

 L. 533       736  LOAD_GLOBAL              int
              738  LOAD_GLOBAL              np
              740  LOAD_METHOD              ceil
              742  LOAD_FAST                '_nsample'
              744  LOAD_FAST                '_batch'
              746  BINARY_TRUE_DIVIDE
              748  CALL_METHOD_1         1  '1 positional argument'
              750  CALL_FUNCTION_1       1  '1 positional argument'
              752  STORE_FAST               '_nloop'

 L. 536       754  LOAD_GLOBAL              QtWidgets
              756  LOAD_METHOD              QProgressDialog
              758  CALL_METHOD_0         0  '0 positional arguments'
              760  STORE_FAST               '_pgsdlg'

 L. 537       762  LOAD_GLOBAL              QtGui
              764  LOAD_METHOD              QIcon
              766  CALL_METHOD_0         0  '0 positional arguments'
              768  STORE_FAST               'icon'

 L. 538       770  LOAD_FAST                'icon'
              772  LOAD_METHOD              addPixmap
              774  LOAD_GLOBAL              QtGui
              776  LOAD_METHOD              QPixmap
              778  LOAD_GLOBAL              os
              780  LOAD_ATTR                path
              782  LOAD_METHOD              join
              784  LOAD_FAST                'self'
              786  LOAD_ATTR                iconpath
              788  LOAD_STR                 'icons/check.png'
              790  CALL_METHOD_2         2  '2 positional arguments'
              792  CALL_METHOD_1         1  '1 positional argument'

 L. 539       794  LOAD_GLOBAL              QtGui
              796  LOAD_ATTR                QIcon
              798  LOAD_ATTR                Normal
              800  LOAD_GLOBAL              QtGui
              802  LOAD_ATTR                QIcon
              804  LOAD_ATTR                Off
              806  CALL_METHOD_3         3  '3 positional arguments'
              808  POP_TOP          

 L. 540       810  LOAD_FAST                '_pgsdlg'
              812  LOAD_METHOD              setWindowIcon
              814  LOAD_FAST                'icon'
              816  CALL_METHOD_1         1  '1 positional argument'
              818  POP_TOP          

 L. 541       820  LOAD_FAST                '_pgsdlg'
              822  LOAD_METHOD              setWindowTitle
              824  LOAD_STR                 'Apply 2D-DCNN'
              826  CALL_METHOD_1         1  '1 positional argument'
              828  POP_TOP          

 L. 542       830  LOAD_FAST                '_pgsdlg'
              832  LOAD_METHOD              setCancelButton
              834  LOAD_CONST               None
              836  CALL_METHOD_1         1  '1 positional argument'
              838  POP_TOP          

 L. 543       840  LOAD_FAST                '_pgsdlg'
              842  LOAD_METHOD              setWindowFlags
              844  LOAD_GLOBAL              QtCore
              846  LOAD_ATTR                Qt
              848  LOAD_ATTR                WindowStaysOnTopHint
              850  CALL_METHOD_1         1  '1 positional argument'
              852  POP_TOP          

 L. 544       854  LOAD_FAST                '_pgsdlg'
              856  LOAD_METHOD              forceShow
              858  CALL_METHOD_0         0  '0 positional arguments'
              860  POP_TOP          

 L. 545       862  LOAD_FAST                '_pgsdlg'
              864  LOAD_METHOD              setFixedWidth
              866  LOAD_CONST               400
              868  CALL_METHOD_1         1  '1 positional argument'
              870  POP_TOP          

 L. 546       872  LOAD_FAST                '_pgsdlg'
              874  LOAD_METHOD              setMaximum
              876  LOAD_FAST                '_nloop'
              878  CALL_METHOD_1         1  '1 positional argument'
              880  POP_TOP          

 L. 548       882  LOAD_GLOBAL              np
              884  LOAD_METHOD              zeros
              886  LOAD_FAST                '_nsample'
              888  LOAD_FAST                '_image_height'
              890  LOAD_FAST                '_image_width'
              892  BINARY_MULTIPLY  
              894  BUILD_LIST_2          2 
              896  CALL_METHOD_1         1  '1 positional argument'
              898  STORE_FAST               '_result'

 L. 549       900  LOAD_CONST               0
              902  STORE_FAST               'idxstart'

 L. 550   904_906  SETUP_LOOP         1520  'to 1520'
              908  LOAD_GLOBAL              range
              910  LOAD_FAST                '_nloop'
              912  CALL_FUNCTION_1       1  '1 positional argument'
              914  GET_ITER         
          916_918  FOR_ITER           1518  'to 1518'
              920  STORE_FAST               'i'

 L. 552       922  LOAD_GLOBAL              QtCore
              924  LOAD_ATTR                QCoreApplication
              926  LOAD_METHOD              instance
              928  CALL_METHOD_0         0  '0 positional arguments'
              930  LOAD_METHOD              processEvents
              932  CALL_METHOD_0         0  '0 positional arguments'
              934  POP_TOP          

 L. 554       936  LOAD_GLOBAL              sys
              938  LOAD_ATTR                stdout
              940  LOAD_METHOD              write

 L. 555       942  LOAD_STR                 '\r>>> Apply 2D-DCNN, proceeding %.1f%% '
              944  LOAD_GLOBAL              float
              946  LOAD_FAST                'i'
              948  CALL_FUNCTION_1       1  '1 positional argument'
              950  LOAD_GLOBAL              float
              952  LOAD_FAST                '_nloop'
              954  CALL_FUNCTION_1       1  '1 positional argument'
              956  BINARY_TRUE_DIVIDE
              958  LOAD_CONST               100.0
              960  BINARY_MULTIPLY  
              962  BINARY_MODULO    
              964  CALL_METHOD_1         1  '1 positional argument'
              966  POP_TOP          

 L. 556       968  LOAD_GLOBAL              sys
              970  LOAD_ATTR                stdout
              972  LOAD_METHOD              flush
              974  CALL_METHOD_0         0  '0 positional arguments'
              976  POP_TOP          

 L. 558       978  LOAD_FAST                'idxstart'
              980  LOAD_FAST                '_batch'
              982  BINARY_ADD       
              984  STORE_FAST               'idxend'

 L. 559       986  LOAD_FAST                'idxend'
              988  LOAD_FAST                '_nsample'
              990  COMPARE_OP               >
          992_994  POP_JUMP_IF_FALSE  1000  'to 1000'

 L. 560       996  LOAD_FAST                '_nsample'
              998  STORE_FAST               'idxend'
           1000_0  COME_FROM           992  '992'

 L. 561      1000  LOAD_GLOBAL              np
             1002  LOAD_METHOD              linspace
             1004  LOAD_FAST                'idxstart'
             1006  LOAD_FAST                'idxend'
             1008  LOAD_CONST               1
             1010  BINARY_SUBTRACT  
             1012  LOAD_FAST                'idxend'
             1014  LOAD_FAST                'idxstart'
             1016  BINARY_SUBTRACT  
             1018  CALL_METHOD_3         3  '3 positional arguments'
             1020  LOAD_METHOD              astype
             1022  LOAD_GLOBAL              int
             1024  CALL_METHOD_1         1  '1 positional argument'
             1026  STORE_FAST               'idxlist'

 L. 562      1028  LOAD_FAST                'idxend'
             1030  STORE_FAST               'idxstart'

 L. 564      1032  BUILD_MAP_0           0 
             1034  STORE_FAST               '_dict'

 L. 565  1036_1038  SETUP_LOOP         1336  'to 1336'
             1040  LOAD_FAST                '_features'
             1042  GET_ITER         
           1044_0  COME_FROM          1258  '1258'
         1044_1046  FOR_ITER           1334  'to 1334'
             1048  STORE_FAST               'f'

 L. 566      1050  LOAD_FAST                'self'
             1052  LOAD_ATTR                seisdata
             1054  LOAD_FAST                'f'
             1056  BINARY_SUBSCR    
             1058  STORE_FAST               '_data'

 L. 567      1060  LOAD_GLOBAL              np
             1062  LOAD_METHOD              transpose
             1064  LOAD_FAST                '_data'
             1066  LOAD_CONST               2
             1068  LOAD_CONST               1
             1070  LOAD_CONST               0
             1072  BUILD_LIST_3          3 
             1074  CALL_METHOD_2         2  '2 positional arguments'
             1076  STORE_FAST               '_data'

 L. 568      1078  LOAD_FAST                'self'
             1080  LOAD_ATTR                cbbornt
             1082  LOAD_METHOD              currentIndex
             1084  CALL_METHOD_0         0  '0 positional arguments'
             1086  LOAD_CONST               0
             1088  COMPARE_OP               ==
         1090_1092  POP_JUMP_IF_FALSE  1162  'to 1162'

 L. 569      1094  LOAD_FAST                '_data'
             1096  LOAD_FAST                'idxlist'
             1098  LOAD_CONST               None
             1100  LOAD_CONST               None
             1102  BUILD_SLICE_2         2 
             1104  LOAD_CONST               None
             1106  LOAD_CONST               None
             1108  BUILD_SLICE_2         2 
             1110  BUILD_TUPLE_3         3 
             1112  BINARY_SUBSCR    
             1114  STORE_FAST               '_data'

 L. 570      1116  LOAD_GLOBAL              np
             1118  LOAD_METHOD              reshape
             1120  LOAD_GLOBAL              np
             1122  LOAD_METHOD              transpose
             1124  LOAD_FAST                '_data'
             1126  LOAD_CONST               0
             1128  LOAD_CONST               2
             1130  LOAD_CONST               1
             1132  BUILD_LIST_3          3 
             1134  CALL_METHOD_2         2  '2 positional arguments'

 L. 571      1136  LOAD_CONST               -1
             1138  LOAD_FAST                '_seisinfo'
             1140  LOAD_STR                 'XLNum'
             1142  BINARY_SUBSCR    
             1144  LOAD_FAST                '_seisinfo'
             1146  LOAD_STR                 'ZNum'
             1148  BINARY_SUBSCR    
             1150  BINARY_MULTIPLY  
             1152  BUILD_LIST_2          2 
             1154  CALL_METHOD_2         2  '2 positional arguments'
             1156  LOAD_FAST                '_dict'
             1158  LOAD_FAST                'f'
             1160  STORE_SUBSCR     
           1162_0  COME_FROM          1090  '1090'

 L. 572      1162  LOAD_FAST                'self'
             1164  LOAD_ATTR                cbbornt
             1166  LOAD_METHOD              currentIndex
             1168  CALL_METHOD_0         0  '0 positional arguments'
             1170  LOAD_CONST               1
             1172  COMPARE_OP               ==
         1174_1176  POP_JUMP_IF_FALSE  1246  'to 1246'

 L. 573      1178  LOAD_FAST                '_data'
             1180  LOAD_CONST               None
             1182  LOAD_CONST               None
             1184  BUILD_SLICE_2         2 
             1186  LOAD_FAST                'idxlist'
             1188  LOAD_CONST               None
             1190  LOAD_CONST               None
             1192  BUILD_SLICE_2         2 
             1194  BUILD_TUPLE_3         3 
             1196  BINARY_SUBSCR    
             1198  STORE_FAST               '_data'

 L. 574      1200  LOAD_GLOBAL              np
             1202  LOAD_METHOD              reshape
             1204  LOAD_GLOBAL              np
             1206  LOAD_METHOD              transpose
             1208  LOAD_FAST                '_data'
             1210  LOAD_CONST               1
             1212  LOAD_CONST               2
             1214  LOAD_CONST               0
             1216  BUILD_LIST_3          3 
             1218  CALL_METHOD_2         2  '2 positional arguments'

 L. 575      1220  LOAD_CONST               -1
             1222  LOAD_FAST                '_seisinfo'
             1224  LOAD_STR                 'ILNum'
             1226  BINARY_SUBSCR    
             1228  LOAD_FAST                '_seisinfo'
             1230  LOAD_STR                 'ZNum'
             1232  BINARY_SUBSCR    
             1234  BINARY_MULTIPLY  
             1236  BUILD_LIST_2          2 
             1238  CALL_METHOD_2         2  '2 positional arguments'
             1240  LOAD_FAST                '_dict'
             1242  LOAD_FAST                'f'
             1244  STORE_SUBSCR     
           1246_0  COME_FROM          1174  '1174'

 L. 576      1246  LOAD_FAST                'self'
             1248  LOAD_ATTR                cbbornt
             1250  LOAD_METHOD              currentIndex
             1252  CALL_METHOD_0         0  '0 positional arguments'
             1254  LOAD_CONST               2
             1256  COMPARE_OP               ==
         1258_1260  POP_JUMP_IF_FALSE  1044  'to 1044'

 L. 577      1262  LOAD_FAST                '_data'
             1264  LOAD_CONST               None
             1266  LOAD_CONST               None
             1268  BUILD_SLICE_2         2 
             1270  LOAD_CONST               None
             1272  LOAD_CONST               None
             1274  BUILD_SLICE_2         2 
             1276  LOAD_FAST                'idxlist'
             1278  BUILD_TUPLE_3         3 
             1280  BINARY_SUBSCR    
             1282  STORE_FAST               '_data'

 L. 578      1284  LOAD_GLOBAL              np
             1286  LOAD_METHOD              reshape
             1288  LOAD_GLOBAL              np
             1290  LOAD_METHOD              transpose
             1292  LOAD_FAST                '_data'
             1294  LOAD_CONST               2
             1296  LOAD_CONST               1
             1298  LOAD_CONST               0
             1300  BUILD_LIST_3          3 
             1302  CALL_METHOD_2         2  '2 positional arguments'

 L. 579      1304  LOAD_CONST               -1
             1306  LOAD_FAST                '_seisinfo'
             1308  LOAD_STR                 'ILNum'
             1310  BINARY_SUBSCR    
             1312  LOAD_FAST                '_seisinfo'
             1314  LOAD_STR                 'XLNum'
             1316  BINARY_SUBSCR    
             1318  BINARY_MULTIPLY  
             1320  BUILD_LIST_2          2 
             1322  CALL_METHOD_2         2  '2 positional arguments'
             1324  LOAD_FAST                '_dict'
             1326  LOAD_FAST                'f'
             1328  STORE_SUBSCR     
         1330_1332  JUMP_BACK          1044  'to 1044'
             1334  POP_BLOCK        
           1336_0  COME_FROM_LOOP     1036  '1036'

 L. 581      1336  LOAD_FAST                '_image_height_new'
             1338  LOAD_FAST                '_image_height'
             1340  COMPARE_OP               !=
         1342_1344  POP_JUMP_IF_TRUE   1356  'to 1356'
             1346  LOAD_FAST                '_image_width_new'
             1348  LOAD_FAST                '_image_width'
             1350  COMPARE_OP               !=
         1352_1354  POP_JUMP_IF_FALSE  1400  'to 1400'
           1356_0  COME_FROM          1342  '1342'

 L. 582      1356  SETUP_LOOP         1400  'to 1400'
             1358  LOAD_FAST                '_features'
             1360  GET_ITER         
             1362  FOR_ITER           1398  'to 1398'
             1364  STORE_FAST               'f'

 L. 583      1366  LOAD_GLOBAL              basic_image
             1368  LOAD_ATTR                changeImageSize
             1370  LOAD_FAST                '_dict'
             1372  LOAD_FAST                'f'
             1374  BINARY_SUBSCR    

 L. 584      1376  LOAD_FAST                '_image_height'

 L. 585      1378  LOAD_FAST                '_image_width'

 L. 586      1380  LOAD_FAST                '_image_height_new'

 L. 587      1382  LOAD_FAST                '_image_width_new'
             1384  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1386  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1388  LOAD_FAST                '_dict'
             1390  LOAD_FAST                'f'
             1392  STORE_SUBSCR     
         1394_1396  JUMP_BACK          1362  'to 1362'
             1398  POP_BLOCK        
           1400_0  COME_FROM_LOOP     1356  '1356'
           1400_1  COME_FROM          1352  '1352'

 L. 589      1400  LOAD_GLOBAL              ml_dcnn
             1402  LOAD_ATTR                predictionFromDCNNSegmentor
             1404  LOAD_FAST                '_dict'

 L. 590      1406  LOAD_FAST                '_image_height_new'
             1408  LOAD_FAST                '_image_width_new'

 L. 591      1410  LOAD_FAST                'self'
             1412  LOAD_ATTR                modelpath

 L. 592      1414  LOAD_FAST                'self'
             1416  LOAD_ATTR                modelname

 L. 593      1418  LOAD_FAST                '_batch'
             1420  LOAD_CONST               True
             1422  LOAD_CONST               ('imageheight', 'imagewidth', 'dcnnpath', 'dcnnname', 'batchsize', 'verbose')
             1424  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1426  STORE_FAST               '_rst'

 L. 595      1428  LOAD_FAST                '_image_height_new'
             1430  LOAD_FAST                '_image_height'
             1432  COMPARE_OP               !=
         1434_1436  POP_JUMP_IF_TRUE   1448  'to 1448'
             1438  LOAD_FAST                '_image_width_new'
             1440  LOAD_FAST                '_image_width'
             1442  COMPARE_OP               !=
         1444_1446  POP_JUMP_IF_FALSE  1484  'to 1484'
           1448_0  COME_FROM          1434  '1434'

 L. 596      1448  LOAD_GLOBAL              basic_image
             1450  LOAD_ATTR                changeImageSize
             1452  LOAD_FAST                '_rst'

 L. 597      1454  LOAD_FAST                '_image_height_new'

 L. 598      1456  LOAD_FAST                '_image_width_new'

 L. 599      1458  LOAD_FAST                '_image_height'

 L. 600      1460  LOAD_FAST                '_image_width'
             1462  LOAD_STR                 'linear'
             1464  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             1466  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1468  LOAD_FAST                '_result'
             1470  LOAD_FAST                'idxlist'
             1472  LOAD_CONST               None
             1474  LOAD_CONST               None
             1476  BUILD_SLICE_2         2 
             1478  BUILD_TUPLE_2         2 
             1480  STORE_SUBSCR     
             1482  JUMP_FORWARD       1500  'to 1500'
           1484_0  COME_FROM          1444  '1444'

 L. 603      1484  LOAD_FAST                '_rst'
             1486  LOAD_FAST                '_result'
             1488  LOAD_FAST                'idxlist'
             1490  LOAD_CONST               None
             1492  LOAD_CONST               None
             1494  BUILD_SLICE_2         2 
             1496  BUILD_TUPLE_2         2 
             1498  STORE_SUBSCR     
           1500_0  COME_FROM          1482  '1482'

 L. 606      1500  LOAD_FAST                '_pgsdlg'
             1502  LOAD_METHOD              setValue
             1504  LOAD_FAST                'i'
             1506  LOAD_CONST               1
             1508  BINARY_ADD       
             1510  CALL_METHOD_1         1  '1 positional argument'
             1512  POP_TOP          
         1514_1516  JUMP_BACK           916  'to 916'
             1518  POP_BLOCK        
           1520_0  COME_FROM_LOOP      904  '904'

 L. 608      1520  LOAD_GLOBAL              print
             1522  LOAD_STR                 'Done'
             1524  CALL_FUNCTION_1       1  '1 positional argument'
             1526  POP_TOP          

 L. 610      1528  LOAD_GLOBAL              np
             1530  LOAD_METHOD              round
             1532  LOAD_FAST                '_result'
             1534  CALL_METHOD_1         1  '1 positional argument'
             1536  LOAD_METHOD              astype
             1538  LOAD_GLOBAL              int
             1540  CALL_METHOD_1         1  '1 positional argument'
             1542  STORE_FAST               '_result'

 L. 612      1544  LOAD_FAST                'self'
             1546  LOAD_ATTR                survinfo
             1548  STORE_FAST               '_info'

 L. 613      1550  LOAD_FAST                '_info'
             1552  LOAD_STR                 'ILNum'
             1554  BINARY_SUBSCR    
             1556  STORE_FAST               '_inlnum'

 L. 614      1558  LOAD_FAST                '_info'
             1560  LOAD_STR                 'XLNum'
             1562  BINARY_SUBSCR    
             1564  STORE_FAST               '_xlnum'

 L. 615      1566  LOAD_FAST                '_info'
             1568  LOAD_STR                 'ZNum'
             1570  BINARY_SUBSCR    
             1572  STORE_FAST               '_znum'

 L. 616      1574  LOAD_FAST                'self'
             1576  LOAD_ATTR                cbbornt
             1578  LOAD_METHOD              currentIndex
             1580  CALL_METHOD_0         0  '0 positional arguments'
             1582  LOAD_CONST               0
             1584  COMPARE_OP               ==
         1586_1588  POP_JUMP_IF_FALSE  1626  'to 1626'

 L. 617      1590  LOAD_GLOBAL              np
             1592  LOAD_METHOD              reshape
             1594  LOAD_FAST                '_result'
             1596  LOAD_CONST               -1
             1598  LOAD_FAST                '_znum'
             1600  LOAD_FAST                '_xlnum'
             1602  BUILD_LIST_3          3 
             1604  CALL_METHOD_2         2  '2 positional arguments'
             1606  STORE_FAST               '_result'

 L. 618      1608  LOAD_GLOBAL              np
             1610  LOAD_METHOD              transpose
             1612  LOAD_FAST                '_result'
             1614  LOAD_CONST               1
             1616  LOAD_CONST               2
             1618  LOAD_CONST               0
             1620  BUILD_LIST_3          3 
             1622  CALL_METHOD_2         2  '2 positional arguments'
             1624  STORE_FAST               '_result'
           1626_0  COME_FROM          1586  '1586'

 L. 619      1626  LOAD_FAST                'self'
             1628  LOAD_ATTR                cbbornt
             1630  LOAD_METHOD              currentIndex
             1632  CALL_METHOD_0         0  '0 positional arguments'
             1634  LOAD_CONST               1
             1636  COMPARE_OP               ==
         1638_1640  POP_JUMP_IF_FALSE  1678  'to 1678'

 L. 620      1642  LOAD_GLOBAL              np
             1644  LOAD_METHOD              reshape
             1646  LOAD_FAST                '_result'
             1648  LOAD_CONST               -1
             1650  LOAD_FAST                '_znum'
             1652  LOAD_FAST                '_inlnum'
             1654  BUILD_LIST_3          3 
             1656  CALL_METHOD_2         2  '2 positional arguments'
             1658  STORE_FAST               '_result'

 L. 621      1660  LOAD_GLOBAL              np
             1662  LOAD_METHOD              transpose
             1664  LOAD_FAST                '_result'
             1666  LOAD_CONST               1
             1668  LOAD_CONST               0
             1670  LOAD_CONST               2
             1672  BUILD_LIST_3          3 
             1674  CALL_METHOD_2         2  '2 positional arguments'
             1676  STORE_FAST               '_result'
           1678_0  COME_FROM          1638  '1638'

 L. 622      1678  LOAD_FAST                'self'
             1680  LOAD_ATTR                cbbornt
             1682  LOAD_METHOD              currentIndex
             1684  CALL_METHOD_0         0  '0 positional arguments'
             1686  LOAD_CONST               2
             1688  COMPARE_OP               ==
         1690_1692  POP_JUMP_IF_FALSE  1712  'to 1712'

 L. 623      1694  LOAD_GLOBAL              np
             1696  LOAD_METHOD              reshape
             1698  LOAD_FAST                '_result'
             1700  LOAD_CONST               -1
             1702  LOAD_FAST                '_xlnum'
             1704  LOAD_FAST                '_inlnum'
             1706  BUILD_LIST_3          3 
             1708  CALL_METHOD_2         2  '2 positional arguments'
             1710  STORE_FAST               '_result'
           1712_0  COME_FROM          1690  '1690'

 L. 625      1712  LOAD_FAST                '_result'
             1714  LOAD_FAST                'self'
             1716  LOAD_ATTR                seisdata
             1718  LOAD_FAST                'self'
             1720  LOAD_ATTR                ldtsave
             1722  LOAD_METHOD              text
             1724  CALL_METHOD_0         0  '0 positional arguments'
             1726  STORE_SUBSCR     

 L. 627      1728  LOAD_GLOBAL              QtWidgets
             1730  LOAD_ATTR                QMessageBox
             1732  LOAD_METHOD              information
             1734  LOAD_FAST                'self'
             1736  LOAD_ATTR                msgbox

 L. 628      1738  LOAD_STR                 'Apply 2D-DCNN'

 L. 629      1740  LOAD_STR                 'DCNN applied successfully'
             1742  CALL_METHOD_3         3  '3 positional arguments'
             1744  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 1742

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
    ApplyMl2DDcnn4Pred = QtWidgets.QWidget()
    gui = applyml2ddcnn4pred()
    gui.setupGUI(ApplyMl2DDcnn4Pred)
    ApplyMl2DDcnn4Pred.show()
    sys.exit(app.exec_())