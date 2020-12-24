# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\extractml2ddcnn.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 36915 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.image as basic_image
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.dcnnsegmentor as ml_dcnn
import cognitivegeo.src.gui.viewml2ddcnn as gui_viewml2ddcnn
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class extractml2ddcnn(object):
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

    def setupGUI(self, ExtractMl2DDcnn):
        ExtractMl2DDcnn.setObjectName('ExtractMl2DDcnn')
        ExtractMl2DDcnn.setFixedSize(810, 480)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/retrieve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ExtractMl2DDcnn.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ExtractMl2DDcnn)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ExtractMl2DDcnn)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ExtractMl2DDcnn)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(ExtractMl2DDcnn)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 230, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 230, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(ExtractMl2DDcnn)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 230, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 270, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(ExtractMl2DDcnn)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 270, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 230, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(ExtractMl2DDcnn)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(ExtractMl2DDcnn)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ExtractMl2DDcnn)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ExtractMl2DDcnn)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ExtractMl2DDcnn)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 190))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(ExtractMl2DDcnn)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(ExtractMl2DDcnn)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 190))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 350, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 350, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ExtractMl2DDcnn)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 350, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 390, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ExtractMl2DDcnn)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 390, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 350, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 350, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ExtractMl2DDcnn)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 350, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 390, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ExtractMl2DDcnn)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 390, 40, 30))
        self.lblpara = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 320, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ExtractMl2DDcnn)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lbltype = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lbltype.setObjectName('lbltype')
        self.lbltype.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.cbbtype = QtWidgets.QComboBox(ExtractMl2DDcnn)
        self.cbbtype.setObjectName('cbbtype')
        self.cbbtype.setGeometry(QtCore.QRect(150, 390, 240, 30))
        self.lblsave = QtWidgets.QLabel(ExtractMl2DDcnn)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 430, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExtractMl2DDcnn)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(150, 430, 100, 30))
        self.btnapply = QtWidgets.QPushButton(ExtractMl2DDcnn)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 430, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/retrieve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ExtractMl2DDcnn)
        self.msgbox.setObjectName('msgbox')
        _center_x = ExtractMl2DDcnn.geometry().center().x()
        _center_y = ExtractMl2DDcnn.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ExtractMl2DDcnn)
        QtCore.QMetaObject.connectSlotsByName(ExtractMl2DDcnn)

    def retranslateGUI(self, ExtractMl2DDcnn):
        self.dialog = ExtractMl2DDcnn
        _translate = QtCore.QCoreApplication.translate
        ExtractMl2DDcnn.setWindowTitle(_translate('ExtractMl2DDcnn', 'Extract 2D-DCNN'))
        self.lblfrom.setText(_translate('ExtractMl2DDcnn', 'Select network:'))
        self.ldtfrom.setText(_translate('ExtractMl2DDcnn', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ExtractMl2DDcnn', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ExtractMl2DDcnn', 'Training features:'))
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblornt.setText(_translate('ExtractMl2DDcnn', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.cbbornt.currentIndexChanged.connect(self.changeCbbOrnt)
        self.lbloldsize.setText(_translate('ExtractMl2DDcnn', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('ExtractMl2DDcnn', 'height='))
        self.ldtoldheight.setText(_translate('ExtractMl2DDcnn', '0'))
        self.ldtoldheight.setEnabled(False)
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('ExtractMl2DDcnn', 'width='))
        self.ldtoldwidth.setText(_translate('ExtractMl2DDcnn', '0'))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtoldwidth.setEnabled(False)
        self.lblnewsize.setText(_translate('ExtractMl2DDcnn', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('ExtractMl2DDcnn', 'height='))
        self.ldtnewheight.setText(_translate('ExtractMl2DDcnn', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('ExtractMl2DDcnn', 'width='))
        self.ldtnewwidth.setText(_translate('ExtractMl2DDcnn', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('ExtractMl2DDcnn', 'Pre-trained DCNN architecture:'))
        self.btnviewnetwork.setText(_translate('ExtractMl2DDcnn', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('ExtractMl2DDcnn', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ExtractMl2DDcnn', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('ExtractMl2DDcnn', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('ExtractMl2DDcnn', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('ExtractMl2DDcnn', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ExtractMl2DDcnn', 'height='))
        self.ldtmaskheight.setText(_translate('ExtractMl2DDcnn', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ExtractMl2DDcnn', 'width='))
        self.ldtmaskwidth.setText(_translate('ExtractMl2DDcnn', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ExtractMl2DDcnn', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ExtractMl2DDcnn', 'height='))
        self.ldtpoolheight.setText(_translate('ExtractMl2DDcnn', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ExtractMl2DDcnn', 'width='))
        self.ldtpoolwidth.setText(_translate('ExtractMl2DDcnn', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ExtractMl2DDcnn', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ExtractMl2DDcnn', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ExtractMl2DDcnn', '5'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltype.setText(_translate('ExtractMl2DCnn', 'Target layer='))
        self.lbltype.setAlignment(QtCore.Qt.AlignRight)
        self.lblsave.setText(_translate('ExtractMl2DCnn', 'Output prefix='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ExtractMl2DCnn', 'dcnn_feature_'))
        self.btnapply.setText(_translate('ExtractMl2DDcnn', 'Extract 2D-DCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnExtractMl2DDcnn)

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
            self.btnviewnetwork.setEnabled(False)
            self.ldtnconvblock.setText('')
            self.ldtn1x1layer.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')
            self.cbbtype.clear()

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

    def clickBtnExtractMl2DDcnn--- This code section failed: ---

 L. 477         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 479         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 480        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in ExtractMl2DDcnn: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 481        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 482        44  LOAD_STR                 'Extract 2D-DCNN'

 L. 483        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 484        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 486        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkDCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 487        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in ExtractMl2DDcnn: No pre-DCNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 488        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 489       100  LOAD_STR                 'Extract 2D-DCNN'

 L. 490       102  LOAD_STR                 'No pre-DCNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 491       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 493       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 494       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 495       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in ExtractMl2DDcnn: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    

 L. 496       152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 497       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 498       170  LOAD_STR                 'Extract 2D-DCNN'

 L. 499       172  LOAD_STR                 "Feature '"
              174  LOAD_FAST                'f'
              176  BINARY_ADD       
              178  LOAD_STR                 "' not found in seismic data"
              180  BINARY_ADD       
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L. 500       186  LOAD_CONST               None
              188  RETURN_VALUE     
              190  JUMP_BACK           124  'to 124'
              192  POP_BLOCK        
            194_0  COME_FROM_LOOP      112  '112'

 L. 502       194  LOAD_FAST                'self'
              196  LOAD_ATTR                modelinfo
              198  LOAD_STR                 'feature_list'
              200  BINARY_SUBSCR    
              202  STORE_FAST               '_features'

 L. 504       204  LOAD_GLOBAL              basic_data
              206  LOAD_METHOD              str2int
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                ldtoldheight
              212  LOAD_METHOD              text
              214  CALL_METHOD_0         0  '0 positional arguments'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  STORE_FAST               '_image_height'

 L. 505       220  LOAD_GLOBAL              basic_data
              222  LOAD_METHOD              str2int
              224  LOAD_FAST                'self'
              226  LOAD_ATTR                ldtoldwidth
              228  LOAD_METHOD              text
              230  CALL_METHOD_0         0  '0 positional arguments'
              232  CALL_METHOD_1         1  '1 positional argument'
              234  STORE_FAST               '_image_width'

 L. 506       236  LOAD_GLOBAL              basic_data
              238  LOAD_METHOD              str2int
              240  LOAD_FAST                'self'
              242  LOAD_ATTR                ldtnewheight
              244  LOAD_METHOD              text
              246  CALL_METHOD_0         0  '0 positional arguments'
              248  CALL_METHOD_1         1  '1 positional argument'
              250  STORE_FAST               '_image_height_new'

 L. 507       252  LOAD_GLOBAL              basic_data
              254  LOAD_METHOD              str2int
              256  LOAD_FAST                'self'
              258  LOAD_ATTR                ldtnewwidth
              260  LOAD_METHOD              text
              262  CALL_METHOD_0         0  '0 positional arguments'
              264  CALL_METHOD_1         1  '1 positional argument'
              266  STORE_FAST               '_image_width_new'

 L. 508       268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               False
              272  COMPARE_OP               is
          274_276  POP_JUMP_IF_TRUE    308  'to 308'
              278  LOAD_FAST                '_image_width'
              280  LOAD_CONST               False
              282  COMPARE_OP               is
          284_286  POP_JUMP_IF_TRUE    308  'to 308'

 L. 509       288  LOAD_FAST                '_image_height_new'
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

 L. 510       308  LOAD_GLOBAL              vis_msg
              310  LOAD_ATTR                print
              312  LOAD_STR                 'ERROR in ExtractMl2DDcnn: Non-integer feature size'
              314  LOAD_STR                 'error'
              316  LOAD_CONST               ('type',)
              318  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              320  POP_TOP          

 L. 511       322  LOAD_GLOBAL              QtWidgets
              324  LOAD_ATTR                QMessageBox
              326  LOAD_METHOD              critical
              328  LOAD_FAST                'self'
              330  LOAD_ATTR                msgbox

 L. 512       332  LOAD_STR                 'Extract 2D-DCNN'

 L. 513       334  LOAD_STR                 'Non-integer feature size'
              336  CALL_METHOD_3         3  '3 positional arguments'
              338  POP_TOP          

 L. 514       340  LOAD_CONST               None
              342  RETURN_VALUE     
            344_0  COME_FROM           304  '304'

 L. 515       344  LOAD_FAST                '_image_height'
              346  LOAD_CONST               2
              348  COMPARE_OP               <
          350_352  POP_JUMP_IF_TRUE    384  'to 384'
              354  LOAD_FAST                '_image_width'
              356  LOAD_CONST               2
              358  COMPARE_OP               <
          360_362  POP_JUMP_IF_TRUE    384  'to 384'

 L. 516       364  LOAD_FAST                '_image_height_new'
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

 L. 517       384  LOAD_GLOBAL              vis_msg
              386  LOAD_ATTR                print
              388  LOAD_STR                 'ERROR in ExtractMl2DDcnn: Features are not 2D'
              390  LOAD_STR                 'error'
              392  LOAD_CONST               ('type',)
              394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              396  POP_TOP          

 L. 518       398  LOAD_GLOBAL              QtWidgets
              400  LOAD_ATTR                QMessageBox
              402  LOAD_METHOD              critical
              404  LOAD_FAST                'self'
              406  LOAD_ATTR                msgbox

 L. 519       408  LOAD_STR                 'Extract 2D-DCNN'

 L. 520       410  LOAD_STR                 'Features are not 2D'
              412  CALL_METHOD_3         3  '3 positional arguments'
              414  POP_TOP          

 L. 521       416  LOAD_CONST               None
              418  RETURN_VALUE     
            420_0  COME_FROM           380  '380'

 L. 523       420  LOAD_GLOBAL              basic_data
              422  LOAD_METHOD              str2int
              424  LOAD_FAST                'self'
              426  LOAD_ATTR                ldtbatchsize
              428  LOAD_METHOD              text
              430  CALL_METHOD_0         0  '0 positional arguments'
              432  CALL_METHOD_1         1  '1 positional argument'
              434  STORE_FAST               '_batch'

 L. 524       436  LOAD_FAST                '_batch'
              438  LOAD_CONST               False
              440  COMPARE_OP               is
          442_444  POP_JUMP_IF_TRUE    456  'to 456'
              446  LOAD_FAST                '_batch'
              448  LOAD_CONST               1
              450  COMPARE_OP               <
          452_454  POP_JUMP_IF_FALSE   492  'to 492'
            456_0  COME_FROM           442  '442'

 L. 525       456  LOAD_GLOBAL              vis_msg
              458  LOAD_ATTR                print
              460  LOAD_STR                 'ERROR in ExtractMl2DDcnn: Non-positive batch size'
              462  LOAD_STR                 'error'
              464  LOAD_CONST               ('type',)
              466  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              468  POP_TOP          

 L. 526       470  LOAD_GLOBAL              QtWidgets
              472  LOAD_ATTR                QMessageBox
              474  LOAD_METHOD              critical
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                msgbox

 L. 527       480  LOAD_STR                 'Extract 2D-DCNN'

 L. 528       482  LOAD_STR                 'Non-postive batch size'
              484  CALL_METHOD_3         3  '3 positional arguments'
              486  POP_TOP          

 L. 529       488  LOAD_CONST               None
              490  RETURN_VALUE     
            492_0  COME_FROM           452  '452'

 L. 531       492  LOAD_GLOBAL              len
              494  LOAD_FAST                'self'
              496  LOAD_ATTR                ldtsave
              498  LOAD_METHOD              text
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  CALL_FUNCTION_1       1  '1 positional argument'
              504  LOAD_CONST               1
              506  COMPARE_OP               <
          508_510  POP_JUMP_IF_FALSE   548  'to 548'

 L. 532       512  LOAD_GLOBAL              vis_msg
              514  LOAD_ATTR                print
              516  LOAD_STR                 'ERROR in ExtractMl2DDcnn: No prefix specified'
              518  LOAD_STR                 'error'
              520  LOAD_CONST               ('type',)
              522  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              524  POP_TOP          

 L. 533       526  LOAD_GLOBAL              QtWidgets
              528  LOAD_ATTR                QMessageBox
              530  LOAD_METHOD              critical
              532  LOAD_FAST                'self'
              534  LOAD_ATTR                msgbox

 L. 534       536  LOAD_STR                 'Extract 2D-DCNN'

 L. 535       538  LOAD_STR                 'No prefix specified'
              540  CALL_METHOD_3         3  '3 positional arguments'
              542  POP_TOP          

 L. 536       544  LOAD_CONST               None
              546  RETURN_VALUE     
            548_0  COME_FROM           508  '508'

 L. 537       548  LOAD_FAST                'self'
              550  LOAD_ATTR                ldtsave
              552  LOAD_METHOD              text
              554  CALL_METHOD_0         0  '0 positional arguments'
              556  LOAD_STR                 '1'
              558  BINARY_ADD       
              560  LOAD_FAST                'self'
              562  LOAD_ATTR                seisdata
              564  LOAD_METHOD              keys
              566  CALL_METHOD_0         0  '0 positional arguments'
              568  COMPARE_OP               in
          570_572  POP_JUMP_IF_FALSE   666  'to 666'

 L. 538       574  LOAD_FAST                'self'
              576  LOAD_METHOD              checkSeisData
              578  LOAD_FAST                'self'
              580  LOAD_ATTR                ldtsave
              582  LOAD_METHOD              text
              584  CALL_METHOD_0         0  '0 positional arguments'
              586  LOAD_STR                 '1'
              588  BINARY_ADD       
              590  CALL_METHOD_1         1  '1 positional argument'
          592_594  POP_JUMP_IF_FALSE   666  'to 666'

 L. 539       596  LOAD_GLOBAL              QtWidgets
              598  LOAD_ATTR                QMessageBox
              600  LOAD_METHOD              question
              602  LOAD_FAST                'self'
              604  LOAD_ATTR                msgbox
              606  LOAD_STR                 'Extract 2D-DCNN'

 L. 540       608  LOAD_STR                 'Prefix '
              610  LOAD_FAST                'self'
              612  LOAD_ATTR                ldtsave
              614  LOAD_METHOD              text
              616  CALL_METHOD_0         0  '0 positional arguments'
              618  BINARY_ADD       
              620  LOAD_STR                 ' already exists. Overwrite?'
              622  BINARY_ADD       

 L. 541       624  LOAD_GLOBAL              QtWidgets
              626  LOAD_ATTR                QMessageBox
              628  LOAD_ATTR                Yes
              630  LOAD_GLOBAL              QtWidgets
              632  LOAD_ATTR                QMessageBox
              634  LOAD_ATTR                No
              636  BINARY_OR        

 L. 542       638  LOAD_GLOBAL              QtWidgets
              640  LOAD_ATTR                QMessageBox
              642  LOAD_ATTR                No
              644  CALL_METHOD_5         5  '5 positional arguments'
              646  STORE_FAST               'reply'

 L. 544       648  LOAD_FAST                'reply'
              650  LOAD_GLOBAL              QtWidgets
              652  LOAD_ATTR                QMessageBox
              654  LOAD_ATTR                No
              656  COMPARE_OP               ==
          658_660  POP_JUMP_IF_FALSE   666  'to 666'

 L. 545       662  LOAD_CONST               None
              664  RETURN_VALUE     
            666_0  COME_FROM           658  '658'
            666_1  COME_FROM           592  '592'
            666_2  COME_FROM           570  '570'

 L. 547       666  LOAD_FAST                'self'
              668  LOAD_ATTR                survinfo
              670  STORE_FAST               '_seisinfo'

 L. 549       672  LOAD_CONST               0
              674  STORE_FAST               '_nsample'

 L. 550       676  LOAD_FAST                'self'
              678  LOAD_ATTR                cbbornt
              680  LOAD_METHOD              currentIndex
              682  CALL_METHOD_0         0  '0 positional arguments'
              684  LOAD_CONST               0
              686  COMPARE_OP               ==
          688_690  POP_JUMP_IF_FALSE   700  'to 700'

 L. 551       692  LOAD_FAST                '_seisinfo'
              694  LOAD_STR                 'ILNum'
              696  BINARY_SUBSCR    
              698  STORE_FAST               '_nsample'
            700_0  COME_FROM           688  '688'

 L. 552       700  LOAD_FAST                'self'
              702  LOAD_ATTR                cbbornt
              704  LOAD_METHOD              currentIndex
              706  CALL_METHOD_0         0  '0 positional arguments'
              708  LOAD_CONST               1
              710  COMPARE_OP               ==
          712_714  POP_JUMP_IF_FALSE   724  'to 724'

 L. 553       716  LOAD_FAST                '_seisinfo'
              718  LOAD_STR                 'XLNum'
              720  BINARY_SUBSCR    
              722  STORE_FAST               '_nsample'
            724_0  COME_FROM           712  '712'

 L. 554       724  LOAD_FAST                'self'
              726  LOAD_ATTR                cbbornt
              728  LOAD_METHOD              currentIndex
              730  CALL_METHOD_0         0  '0 positional arguments'
              732  LOAD_CONST               2
              734  COMPARE_OP               ==
          736_738  POP_JUMP_IF_FALSE   748  'to 748'

 L. 555       740  LOAD_FAST                '_seisinfo'
              742  LOAD_STR                 'ZNum'
              744  BINARY_SUBSCR    
              746  STORE_FAST               '_nsample'
            748_0  COME_FROM           736  '736'

 L. 557       748  LOAD_GLOBAL              int
              750  LOAD_GLOBAL              np
              752  LOAD_METHOD              ceil
              754  LOAD_FAST                '_nsample'
              756  LOAD_FAST                '_batch'
              758  BINARY_TRUE_DIVIDE
              760  CALL_METHOD_1         1  '1 positional argument'
              762  CALL_FUNCTION_1       1  '1 positional argument'
              764  STORE_FAST               '_nloop'

 L. 560       766  LOAD_GLOBAL              QtWidgets
              768  LOAD_METHOD              QProgressDialog
              770  CALL_METHOD_0         0  '0 positional arguments'
              772  STORE_FAST               '_pgsdlg'

 L. 561       774  LOAD_GLOBAL              QtGui
              776  LOAD_METHOD              QIcon
              778  CALL_METHOD_0         0  '0 positional arguments'
              780  STORE_FAST               'icon'

 L. 562       782  LOAD_FAST                'icon'
              784  LOAD_METHOD              addPixmap
              786  LOAD_GLOBAL              QtGui
              788  LOAD_METHOD              QPixmap
              790  LOAD_GLOBAL              os
              792  LOAD_ATTR                path
              794  LOAD_METHOD              join
              796  LOAD_FAST                'self'
              798  LOAD_ATTR                iconpath
              800  LOAD_STR                 'icons/check.png'
              802  CALL_METHOD_2         2  '2 positional arguments'
              804  CALL_METHOD_1         1  '1 positional argument'

 L. 563       806  LOAD_GLOBAL              QtGui
              808  LOAD_ATTR                QIcon
              810  LOAD_ATTR                Normal
              812  LOAD_GLOBAL              QtGui
              814  LOAD_ATTR                QIcon
              816  LOAD_ATTR                Off
              818  CALL_METHOD_3         3  '3 positional arguments'
              820  POP_TOP          

 L. 564       822  LOAD_FAST                '_pgsdlg'
              824  LOAD_METHOD              setWindowIcon
              826  LOAD_FAST                'icon'
              828  CALL_METHOD_1         1  '1 positional argument'
              830  POP_TOP          

 L. 565       832  LOAD_FAST                '_pgsdlg'
              834  LOAD_METHOD              setWindowTitle
              836  LOAD_STR                 'Extract 2D-DCNN'
              838  CALL_METHOD_1         1  '1 positional argument'
              840  POP_TOP          

 L. 566       842  LOAD_FAST                '_pgsdlg'
              844  LOAD_METHOD              setCancelButton
              846  LOAD_CONST               None
              848  CALL_METHOD_1         1  '1 positional argument'
              850  POP_TOP          

 L. 567       852  LOAD_FAST                '_pgsdlg'
              854  LOAD_METHOD              setWindowFlags
              856  LOAD_GLOBAL              QtCore
              858  LOAD_ATTR                Qt
              860  LOAD_ATTR                WindowStaysOnTopHint
              862  CALL_METHOD_1         1  '1 positional argument'
              864  POP_TOP          

 L. 568       866  LOAD_FAST                '_pgsdlg'
              868  LOAD_METHOD              forceShow
              870  CALL_METHOD_0         0  '0 positional arguments'
              872  POP_TOP          

 L. 569       874  LOAD_FAST                '_pgsdlg'
              876  LOAD_METHOD              setFixedWidth
              878  LOAD_CONST               400
              880  CALL_METHOD_1         1  '1 positional argument'
              882  POP_TOP          

 L. 570       884  LOAD_FAST                '_pgsdlg'
              886  LOAD_METHOD              setMaximum
              888  LOAD_FAST                '_nloop'
              890  CALL_METHOD_1         1  '1 positional argument'
              892  POP_TOP          

 L. 572       894  LOAD_FAST                'self'
              896  LOAD_ATTR                modelinfo
              898  LOAD_STR                 'number_conv_block'
              900  BINARY_SUBSCR    
              902  STORE_FAST               '_nblock'

 L. 573       904  LOAD_FAST                'self'
              906  LOAD_ATTR                modelinfo
              908  LOAD_STR                 'number_conv_layer'
              910  BINARY_SUBSCR    
              912  STORE_FAST               '_nlayer'

 L. 574       914  LOAD_FAST                'self'
              916  LOAD_ATTR                modelinfo
              918  LOAD_STR                 'number_conv_feature'
              920  BINARY_SUBSCR    
              922  STORE_FAST               '_nfeature'

 L. 576       924  LOAD_FAST                'self'
              926  LOAD_ATTR                cbbtype
              928  LOAD_METHOD              currentIndex
              930  CALL_METHOD_0         0  '0 positional arguments'
              932  STORE_FAST               '_featureidx'

 L. 577       934  LOAD_CONST               0
              936  STORE_FAST               '_blockidx'

 L. 578       938  LOAD_CONST               0
              940  STORE_FAST               '_layeridx'

 L. 579       942  SETUP_LOOP         1018  'to 1018'
              944  LOAD_GLOBAL              range
              946  LOAD_FAST                '_nblock'
              948  CALL_FUNCTION_1       1  '1 positional argument'
              950  GET_ITER         
            952_0  COME_FROM           982  '982'
              952  FOR_ITER           1016  'to 1016'
              954  STORE_FAST               'i'

 L. 580       956  LOAD_GLOBAL              sum
              958  LOAD_FAST                '_nlayer'
              960  LOAD_CONST               0
              962  LOAD_FAST                'i'
              964  LOAD_CONST               1
              966  BINARY_ADD       
              968  BUILD_SLICE_2         2 
              970  BINARY_SUBSCR    
              972  CALL_FUNCTION_1       1  '1 positional argument'
              974  LOAD_FAST                '_featureidx'
              976  LOAD_CONST               1
              978  BINARY_ADD       
              980  COMPARE_OP               >=
          982_984  POP_JUMP_IF_FALSE   952  'to 952'

 L. 581       986  LOAD_FAST                'i'
              988  STORE_FAST               '_blockidx'

 L. 582       990  LOAD_FAST                '_featureidx'
              992  LOAD_GLOBAL              sum
              994  LOAD_FAST                '_nlayer'
              996  LOAD_CONST               0
              998  LOAD_FAST                'i'
             1000  BUILD_SLICE_2         2 
             1002  BINARY_SUBSCR    
             1004  CALL_FUNCTION_1       1  '1 positional argument'
             1006  BINARY_SUBTRACT  
             1008  STORE_FAST               '_layeridx'

 L. 583      1010  BREAK_LOOP       
         1012_1014  JUMP_BACK           952  'to 952'
             1016  POP_BLOCK        
           1018_0  COME_FROM_LOOP      942  '942'

 L. 585      1018  LOAD_FAST                '_nfeature'
             1020  LOAD_FAST                '_blockidx'
             1022  BINARY_SUBSCR    
             1024  STORE_FAST               '_nfeature'

 L. 586      1026  LOAD_GLOBAL              np
             1028  LOAD_METHOD              zeros
             1030  LOAD_FAST                '_nsample'
             1032  LOAD_FAST                '_nfeature'
             1034  LOAD_FAST                '_image_height'
             1036  LOAD_FAST                '_image_width'
             1038  BINARY_MULTIPLY  
             1040  BUILD_LIST_3          3 
             1042  CALL_METHOD_1         1  '1 positional argument'
             1044  STORE_FAST               '_result'

 L. 587      1046  LOAD_CONST               0
             1048  STORE_FAST               'idxstart'

 L. 588  1050_1052  SETUP_LOOP         1784  'to 1784'
             1054  LOAD_GLOBAL              range
             1056  LOAD_FAST                '_nloop'
             1058  CALL_FUNCTION_1       1  '1 positional argument'
             1060  GET_ITER         
         1062_1064  FOR_ITER           1782  'to 1782'
             1066  STORE_FAST               'i'

 L. 590      1068  LOAD_GLOBAL              QtCore
             1070  LOAD_ATTR                QCoreApplication
             1072  LOAD_METHOD              instance
             1074  CALL_METHOD_0         0  '0 positional arguments'
             1076  LOAD_METHOD              processEvents
             1078  CALL_METHOD_0         0  '0 positional arguments'
             1080  POP_TOP          

 L. 592      1082  LOAD_GLOBAL              sys
             1084  LOAD_ATTR                stdout
             1086  LOAD_METHOD              write

 L. 593      1088  LOAD_STR                 '\r>>> Extract 2D-DCNN, proceeding %.1f%% '
             1090  LOAD_GLOBAL              float
             1092  LOAD_FAST                'i'
             1094  CALL_FUNCTION_1       1  '1 positional argument'
             1096  LOAD_GLOBAL              float
             1098  LOAD_FAST                '_nloop'
             1100  CALL_FUNCTION_1       1  '1 positional argument'
             1102  BINARY_TRUE_DIVIDE
             1104  LOAD_CONST               100.0
             1106  BINARY_MULTIPLY  
             1108  BINARY_MODULO    
             1110  CALL_METHOD_1         1  '1 positional argument'
             1112  POP_TOP          

 L. 594      1114  LOAD_GLOBAL              sys
             1116  LOAD_ATTR                stdout
             1118  LOAD_METHOD              flush
             1120  CALL_METHOD_0         0  '0 positional arguments'
             1122  POP_TOP          

 L. 596      1124  LOAD_FAST                'idxstart'
             1126  LOAD_FAST                '_batch'
             1128  BINARY_ADD       
             1130  STORE_FAST               'idxend'

 L. 597      1132  LOAD_FAST                'idxend'
             1134  LOAD_FAST                '_nsample'
             1136  COMPARE_OP               >
         1138_1140  POP_JUMP_IF_FALSE  1146  'to 1146'

 L. 598      1142  LOAD_FAST                '_nsample'
             1144  STORE_FAST               'idxend'
           1146_0  COME_FROM          1138  '1138'

 L. 599      1146  LOAD_GLOBAL              np
             1148  LOAD_METHOD              linspace
             1150  LOAD_FAST                'idxstart'
             1152  LOAD_FAST                'idxend'
             1154  LOAD_CONST               1
             1156  BINARY_SUBTRACT  
             1158  LOAD_FAST                'idxend'
             1160  LOAD_FAST                'idxstart'
             1162  BINARY_SUBTRACT  
             1164  CALL_METHOD_3         3  '3 positional arguments'
             1166  LOAD_METHOD              astype
             1168  LOAD_GLOBAL              int
             1170  CALL_METHOD_1         1  '1 positional argument'
             1172  STORE_FAST               'idxlist'

 L. 600      1174  LOAD_FAST                'idxend'
             1176  STORE_FAST               'idxstart'

 L. 602      1178  BUILD_MAP_0           0 
             1180  STORE_FAST               '_dict'

 L. 603  1182_1184  SETUP_LOOP         1482  'to 1482'
             1186  LOAD_FAST                '_features'
             1188  GET_ITER         
           1190_0  COME_FROM          1404  '1404'
         1190_1192  FOR_ITER           1480  'to 1480'
             1194  STORE_FAST               'f'

 L. 604      1196  LOAD_FAST                'self'
             1198  LOAD_ATTR                seisdata
             1200  LOAD_FAST                'f'
             1202  BINARY_SUBSCR    
             1204  STORE_FAST               '_data'

 L. 605      1206  LOAD_GLOBAL              np
             1208  LOAD_METHOD              transpose
             1210  LOAD_FAST                '_data'
             1212  LOAD_CONST               2
             1214  LOAD_CONST               1
             1216  LOAD_CONST               0
             1218  BUILD_LIST_3          3 
             1220  CALL_METHOD_2         2  '2 positional arguments'
             1222  STORE_FAST               '_data'

 L. 606      1224  LOAD_FAST                'self'
             1226  LOAD_ATTR                cbbornt
             1228  LOAD_METHOD              currentIndex
             1230  CALL_METHOD_0         0  '0 positional arguments'
             1232  LOAD_CONST               0
             1234  COMPARE_OP               ==
         1236_1238  POP_JUMP_IF_FALSE  1308  'to 1308'

 L. 607      1240  LOAD_FAST                '_data'
             1242  LOAD_FAST                'idxlist'
             1244  LOAD_CONST               None
             1246  LOAD_CONST               None
             1248  BUILD_SLICE_2         2 
             1250  LOAD_CONST               None
             1252  LOAD_CONST               None
             1254  BUILD_SLICE_2         2 
             1256  BUILD_TUPLE_3         3 
             1258  BINARY_SUBSCR    
             1260  STORE_FAST               '_data'

 L. 608      1262  LOAD_GLOBAL              np
             1264  LOAD_METHOD              reshape
             1266  LOAD_GLOBAL              np
             1268  LOAD_METHOD              transpose
             1270  LOAD_FAST                '_data'
             1272  LOAD_CONST               0
             1274  LOAD_CONST               2
             1276  LOAD_CONST               1
             1278  BUILD_LIST_3          3 
             1280  CALL_METHOD_2         2  '2 positional arguments'

 L. 609      1282  LOAD_CONST               -1
             1284  LOAD_FAST                '_seisinfo'
             1286  LOAD_STR                 'XLNum'
             1288  BINARY_SUBSCR    
             1290  LOAD_FAST                '_seisinfo'
             1292  LOAD_STR                 'ZNum'
             1294  BINARY_SUBSCR    
             1296  BINARY_MULTIPLY  
             1298  BUILD_LIST_2          2 
             1300  CALL_METHOD_2         2  '2 positional arguments'
             1302  LOAD_FAST                '_dict'
             1304  LOAD_FAST                'f'
             1306  STORE_SUBSCR     
           1308_0  COME_FROM          1236  '1236'

 L. 610      1308  LOAD_FAST                'self'
             1310  LOAD_ATTR                cbbornt
             1312  LOAD_METHOD              currentIndex
             1314  CALL_METHOD_0         0  '0 positional arguments'
             1316  LOAD_CONST               1
             1318  COMPARE_OP               ==
         1320_1322  POP_JUMP_IF_FALSE  1392  'to 1392'

 L. 611      1324  LOAD_FAST                '_data'
             1326  LOAD_CONST               None
             1328  LOAD_CONST               None
             1330  BUILD_SLICE_2         2 
             1332  LOAD_FAST                'idxlist'
             1334  LOAD_CONST               None
             1336  LOAD_CONST               None
             1338  BUILD_SLICE_2         2 
             1340  BUILD_TUPLE_3         3 
             1342  BINARY_SUBSCR    
             1344  STORE_FAST               '_data'

 L. 612      1346  LOAD_GLOBAL              np
             1348  LOAD_METHOD              reshape
             1350  LOAD_GLOBAL              np
             1352  LOAD_METHOD              transpose
             1354  LOAD_FAST                '_data'
             1356  LOAD_CONST               1
             1358  LOAD_CONST               2
             1360  LOAD_CONST               0
             1362  BUILD_LIST_3          3 
             1364  CALL_METHOD_2         2  '2 positional arguments'

 L. 613      1366  LOAD_CONST               -1
             1368  LOAD_FAST                '_seisinfo'
             1370  LOAD_STR                 'ILNum'
             1372  BINARY_SUBSCR    
             1374  LOAD_FAST                '_seisinfo'
             1376  LOAD_STR                 'ZNum'
             1378  BINARY_SUBSCR    
             1380  BINARY_MULTIPLY  
             1382  BUILD_LIST_2          2 
             1384  CALL_METHOD_2         2  '2 positional arguments'
             1386  LOAD_FAST                '_dict'
             1388  LOAD_FAST                'f'
             1390  STORE_SUBSCR     
           1392_0  COME_FROM          1320  '1320'

 L. 614      1392  LOAD_FAST                'self'
             1394  LOAD_ATTR                cbbornt
             1396  LOAD_METHOD              currentIndex
             1398  CALL_METHOD_0         0  '0 positional arguments'
             1400  LOAD_CONST               2
             1402  COMPARE_OP               ==
         1404_1406  POP_JUMP_IF_FALSE  1190  'to 1190'

 L. 615      1408  LOAD_FAST                '_data'
             1410  LOAD_CONST               None
             1412  LOAD_CONST               None
             1414  BUILD_SLICE_2         2 
             1416  LOAD_CONST               None
             1418  LOAD_CONST               None
             1420  BUILD_SLICE_2         2 
             1422  LOAD_FAST                'idxlist'
             1424  BUILD_TUPLE_3         3 
             1426  BINARY_SUBSCR    
             1428  STORE_FAST               '_data'

 L. 616      1430  LOAD_GLOBAL              np
             1432  LOAD_METHOD              reshape
             1434  LOAD_GLOBAL              np
             1436  LOAD_METHOD              transpose
             1438  LOAD_FAST                '_data'
             1440  LOAD_CONST               2
             1442  LOAD_CONST               1
             1444  LOAD_CONST               0
             1446  BUILD_LIST_3          3 
             1448  CALL_METHOD_2         2  '2 positional arguments'

 L. 617      1450  LOAD_CONST               -1
             1452  LOAD_FAST                '_seisinfo'
             1454  LOAD_STR                 'ILNum'
             1456  BINARY_SUBSCR    
             1458  LOAD_FAST                '_seisinfo'
             1460  LOAD_STR                 'XLNum'
             1462  BINARY_SUBSCR    
             1464  BINARY_MULTIPLY  
             1466  BUILD_LIST_2          2 
             1468  CALL_METHOD_2         2  '2 positional arguments'
             1470  LOAD_FAST                '_dict'
             1472  LOAD_FAST                'f'
             1474  STORE_SUBSCR     
         1476_1478  JUMP_BACK          1190  'to 1190'
             1480  POP_BLOCK        
           1482_0  COME_FROM_LOOP     1182  '1182'

 L. 618      1482  LOAD_FAST                '_image_height_new'
             1484  LOAD_FAST                '_image_height'
             1486  COMPARE_OP               !=
         1488_1490  POP_JUMP_IF_TRUE   1502  'to 1502'
             1492  LOAD_FAST                '_image_width_new'
             1494  LOAD_FAST                '_image_width'
             1496  COMPARE_OP               !=
         1498_1500  POP_JUMP_IF_FALSE  1546  'to 1546'
           1502_0  COME_FROM          1488  '1488'

 L. 619      1502  SETUP_LOOP         1546  'to 1546'
             1504  LOAD_FAST                '_features'
             1506  GET_ITER         
             1508  FOR_ITER           1544  'to 1544'
             1510  STORE_FAST               'f'

 L. 620      1512  LOAD_GLOBAL              basic_image
             1514  LOAD_ATTR                changeImageSize
             1516  LOAD_FAST                '_dict'
             1518  LOAD_FAST                'f'
             1520  BINARY_SUBSCR    

 L. 621      1522  LOAD_FAST                '_image_height'

 L. 622      1524  LOAD_FAST                '_image_width'

 L. 623      1526  LOAD_FAST                '_image_height_new'

 L. 624      1528  LOAD_FAST                '_image_width_new'
             1530  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1532  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1534  LOAD_FAST                '_dict'
             1536  LOAD_FAST                'f'
             1538  STORE_SUBSCR     
         1540_1542  JUMP_BACK          1508  'to 1508'
             1544  POP_BLOCK        
           1546_0  COME_FROM_LOOP     1502  '1502'
           1546_1  COME_FROM          1498  '1498'

 L. 627      1546  LOAD_GLOBAL              ml_dcnn
             1548  LOAD_ATTR                extractDCNNConvFeature
             1550  LOAD_FAST                '_dict'

 L. 628      1552  LOAD_FAST                '_image_height_new'
             1554  LOAD_FAST                '_image_width_new'

 L. 629      1556  LOAD_FAST                'self'
             1558  LOAD_ATTR                modelpath

 L. 630      1560  LOAD_FAST                'self'
             1562  LOAD_ATTR                modelname

 L. 631      1564  LOAD_FAST                '_blockidx'

 L. 632      1566  LOAD_FAST                '_layeridx'
             1568  LOAD_STR                 'full'

 L. 633      1570  LOAD_FAST                '_batch'
             1572  LOAD_CONST               True
             1574  LOAD_CONST               ('imageheight', 'imagewidth', 'dcnnpath', 'dcnnname', 'blockidx', 'layeridx', 'location', 'batchsize', 'verbose')
             1576  CALL_FUNCTION_KW_10    10  '10 total positional and keyword args'
             1578  STORE_FAST               '_rst'

 L. 635      1580  LOAD_GLOBAL              np
             1582  LOAD_METHOD              shape
             1584  LOAD_FAST                '_rst'
             1586  CALL_METHOD_1         1  '1 positional argument'
             1588  LOAD_CONST               2
             1590  BINARY_SUBSCR    
             1592  STORE_FAST               '_feature_height'

 L. 636      1594  LOAD_GLOBAL              np
             1596  LOAD_METHOD              shape
             1598  LOAD_FAST                '_rst'
             1600  CALL_METHOD_1         1  '1 positional argument'
             1602  LOAD_CONST               3
             1604  BINARY_SUBSCR    
             1606  STORE_FAST               '_feature_width'

 L. 637      1608  LOAD_FAST                '_feature_height'
             1610  LOAD_FAST                '_image_height'
             1612  COMPARE_OP               !=
         1614_1616  POP_JUMP_IF_TRUE   1628  'to 1628'
             1618  LOAD_FAST                '_feature_width'
             1620  LOAD_FAST                '_image_width'
             1622  COMPARE_OP               !=
         1624_1626  POP_JUMP_IF_FALSE  1724  'to 1724'
           1628_0  COME_FROM          1614  '1614'

 L. 638      1628  LOAD_GLOBAL              np
             1630  LOAD_METHOD              reshape
             1632  LOAD_FAST                '_rst'
             1634  LOAD_GLOBAL              np
             1636  LOAD_METHOD              shape
             1638  LOAD_FAST                '_rst'
             1640  CALL_METHOD_1         1  '1 positional argument'
             1642  LOAD_CONST               0
             1644  BINARY_SUBSCR    
             1646  LOAD_FAST                '_nfeature'
             1648  BINARY_MULTIPLY  
             1650  LOAD_FAST                '_feature_height'
             1652  LOAD_FAST                '_feature_width'
             1654  BINARY_MULTIPLY  
             1656  BUILD_LIST_2          2 
             1658  CALL_METHOD_2         2  '2 positional arguments'
             1660  STORE_FAST               '_rst'

 L. 639      1662  LOAD_GLOBAL              basic_image
             1664  LOAD_ATTR                changeImageSize
             1666  LOAD_FAST                '_rst'

 L. 640      1668  LOAD_FAST                '_feature_height'

 L. 641      1670  LOAD_FAST                '_feature_width'

 L. 642      1672  LOAD_FAST                '_image_height'

 L. 643      1674  LOAD_FAST                '_image_width'
             1676  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1678  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1680  STORE_FAST               '_rst'

 L. 644      1682  LOAD_GLOBAL              np
             1684  LOAD_METHOD              reshape
             1686  LOAD_FAST                '_rst'
             1688  LOAD_CONST               -1
             1690  LOAD_FAST                '_nfeature'
             1692  LOAD_FAST                '_image_height'
             1694  LOAD_FAST                '_image_width'
             1696  BINARY_MULTIPLY  
             1698  BUILD_LIST_3          3 
             1700  CALL_METHOD_2         2  '2 positional arguments'
             1702  LOAD_FAST                '_result'
             1704  LOAD_FAST                'idxlist'
             1706  LOAD_CONST               None
             1708  LOAD_CONST               None
             1710  BUILD_SLICE_2         2 
             1712  LOAD_CONST               None
             1714  LOAD_CONST               None
             1716  BUILD_SLICE_2         2 
             1718  BUILD_TUPLE_3         3 
             1720  STORE_SUBSCR     
             1722  JUMP_FORWARD       1764  'to 1764'
           1724_0  COME_FROM          1624  '1624'

 L. 646      1724  LOAD_GLOBAL              np
             1726  LOAD_METHOD              reshape
             1728  LOAD_FAST                '_rst'
             1730  LOAD_CONST               -1
             1732  LOAD_FAST                '_nfeature'
             1734  LOAD_FAST                '_image_height'
             1736  LOAD_FAST                '_image_width'
             1738  BINARY_MULTIPLY  
             1740  BUILD_LIST_3          3 
             1742  CALL_METHOD_2         2  '2 positional arguments'
             1744  LOAD_FAST                '_result'
             1746  LOAD_FAST                'idxlist'
             1748  LOAD_CONST               None
             1750  LOAD_CONST               None
             1752  BUILD_SLICE_2         2 
             1754  LOAD_CONST               None
             1756  LOAD_CONST               None
             1758  BUILD_SLICE_2         2 
             1760  BUILD_TUPLE_3         3 
             1762  STORE_SUBSCR     
           1764_0  COME_FROM          1722  '1722'

 L. 649      1764  LOAD_FAST                '_pgsdlg'
             1766  LOAD_METHOD              setValue
             1768  LOAD_FAST                'i'
             1770  LOAD_CONST               1
             1772  BINARY_ADD       
             1774  CALL_METHOD_1         1  '1 positional argument'
             1776  POP_TOP          
         1778_1780  JUMP_BACK          1062  'to 1062'
             1782  POP_BLOCK        
           1784_0  COME_FROM_LOOP     1050  '1050'

 L. 651      1784  LOAD_GLOBAL              print
             1786  LOAD_STR                 'Done'
             1788  CALL_FUNCTION_1       1  '1 positional argument'
             1790  POP_TOP          

 L. 653      1792  LOAD_FAST                'self'
             1794  LOAD_ATTR                survinfo
             1796  STORE_FAST               '_info'

 L. 654      1798  LOAD_FAST                '_info'
             1800  LOAD_STR                 'ILNum'
             1802  BINARY_SUBSCR    
             1804  STORE_FAST               '_inlnum'

 L. 655      1806  LOAD_FAST                '_info'
             1808  LOAD_STR                 'XLNum'
             1810  BINARY_SUBSCR    
             1812  STORE_FAST               '_xlnum'

 L. 656      1814  LOAD_FAST                '_info'
             1816  LOAD_STR                 'ZNum'
             1818  BINARY_SUBSCR    
             1820  STORE_FAST               '_znum'

 L. 657      1822  SETUP_LOOP         2062  'to 2062'
             1824  LOAD_GLOBAL              range
             1826  LOAD_FAST                '_nfeature'
             1828  CALL_FUNCTION_1       1  '1 positional argument'
             1830  GET_ITER         
             1832  FOR_ITER           2060  'to 2060'
             1834  STORE_FAST               'i'

 L. 658      1836  LOAD_FAST                'self'
             1838  LOAD_ATTR                cbbornt
             1840  LOAD_METHOD              currentIndex
             1842  CALL_METHOD_0         0  '0 positional arguments'
             1844  LOAD_CONST               0
             1846  COMPARE_OP               ==
         1848_1850  POP_JUMP_IF_FALSE  1906  'to 1906'

 L. 659      1852  LOAD_GLOBAL              np
             1854  LOAD_METHOD              reshape
             1856  LOAD_FAST                '_result'
             1858  LOAD_CONST               None
             1860  LOAD_CONST               None
             1862  BUILD_SLICE_2         2 
             1864  LOAD_FAST                'i'
             1866  LOAD_CONST               None
             1868  LOAD_CONST               None
             1870  BUILD_SLICE_2         2 
             1872  BUILD_TUPLE_3         3 
             1874  BINARY_SUBSCR    
             1876  LOAD_CONST               -1
             1878  LOAD_FAST                '_znum'
             1880  LOAD_FAST                '_xlnum'
             1882  BUILD_LIST_3          3 
             1884  CALL_METHOD_2         2  '2 positional arguments'
             1886  STORE_FAST               '_rst'

 L. 660      1888  LOAD_GLOBAL              np
             1890  LOAD_METHOD              transpose
             1892  LOAD_FAST                '_rst'
             1894  LOAD_CONST               1
             1896  LOAD_CONST               2
             1898  LOAD_CONST               0
             1900  BUILD_LIST_3          3 
             1902  CALL_METHOD_2         2  '2 positional arguments'
             1904  STORE_FAST               '_rst'
           1906_0  COME_FROM          1848  '1848'

 L. 661      1906  LOAD_FAST                'self'
             1908  LOAD_ATTR                cbbornt
             1910  LOAD_METHOD              currentIndex
             1912  CALL_METHOD_0         0  '0 positional arguments'
             1914  LOAD_CONST               1
             1916  COMPARE_OP               ==
         1918_1920  POP_JUMP_IF_FALSE  1976  'to 1976'

 L. 662      1922  LOAD_GLOBAL              np
             1924  LOAD_METHOD              reshape
             1926  LOAD_FAST                '_result'
             1928  LOAD_CONST               None
             1930  LOAD_CONST               None
             1932  BUILD_SLICE_2         2 
             1934  LOAD_FAST                'i'
             1936  LOAD_CONST               None
             1938  LOAD_CONST               None
             1940  BUILD_SLICE_2         2 
             1942  BUILD_TUPLE_3         3 
             1944  BINARY_SUBSCR    
             1946  LOAD_CONST               -1
             1948  LOAD_FAST                '_znum'
             1950  LOAD_FAST                '_inlnum'
             1952  BUILD_LIST_3          3 
             1954  CALL_METHOD_2         2  '2 positional arguments'
             1956  STORE_FAST               '_rst'

 L. 663      1958  LOAD_GLOBAL              np
             1960  LOAD_METHOD              transpose
             1962  LOAD_FAST                '_rst'
             1964  LOAD_CONST               1
             1966  LOAD_CONST               0
             1968  LOAD_CONST               2
             1970  BUILD_LIST_3          3 
             1972  CALL_METHOD_2         2  '2 positional arguments'
             1974  STORE_FAST               '_rst'
           1976_0  COME_FROM          1918  '1918'

 L. 664      1976  LOAD_FAST                'self'
             1978  LOAD_ATTR                cbbornt
             1980  LOAD_METHOD              currentIndex
             1982  CALL_METHOD_0         0  '0 positional arguments'
             1984  LOAD_CONST               2
             1986  COMPARE_OP               ==
         1988_1990  POP_JUMP_IF_FALSE  2028  'to 2028'

 L. 665      1992  LOAD_GLOBAL              np
             1994  LOAD_METHOD              reshape
             1996  LOAD_FAST                '_result'
             1998  LOAD_CONST               None
             2000  LOAD_CONST               None
             2002  BUILD_SLICE_2         2 
             2004  LOAD_FAST                'i'
             2006  LOAD_CONST               None
             2008  LOAD_CONST               None
             2010  BUILD_SLICE_2         2 
             2012  BUILD_TUPLE_3         3 
             2014  BINARY_SUBSCR    
             2016  LOAD_CONST               -1
             2018  LOAD_FAST                '_xlnum'
             2020  LOAD_FAST                '_inlnum'
             2022  BUILD_LIST_3          3 
             2024  CALL_METHOD_2         2  '2 positional arguments'
             2026  STORE_FAST               '_rst'
           2028_0  COME_FROM          1988  '1988'

 L. 667      2028  LOAD_FAST                '_rst'
             2030  LOAD_FAST                'self'
             2032  LOAD_ATTR                seisdata
             2034  LOAD_FAST                'self'
             2036  LOAD_ATTR                ldtsave
             2038  LOAD_METHOD              text
             2040  CALL_METHOD_0         0  '0 positional arguments'
             2042  LOAD_GLOBAL              str
             2044  LOAD_FAST                'i'
             2046  LOAD_CONST               1
             2048  BINARY_ADD       
             2050  CALL_FUNCTION_1       1  '1 positional argument'
             2052  BINARY_ADD       
             2054  STORE_SUBSCR     
         2056_2058  JUMP_BACK          1832  'to 1832'
             2060  POP_BLOCK        
           2062_0  COME_FROM_LOOP     1822  '1822'

 L. 669      2062  LOAD_GLOBAL              QtWidgets
             2064  LOAD_ATTR                QMessageBox
             2066  LOAD_METHOD              information
             2068  LOAD_FAST                'self'
             2070  LOAD_ATTR                msgbox

 L. 670      2072  LOAD_STR                 'Extract 2D-DCNN'

 L. 671      2074  LOAD_GLOBAL              str
             2076  LOAD_FAST                '_nfeature'
             2078  CALL_FUNCTION_1       1  '1 positional argument'
             2080  LOAD_STR                 ' DCNN features extracted successfully'
             2082  BINARY_ADD       
             2084  CALL_METHOD_3         3  '3 positional arguments'
             2086  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 2084

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
    ExtractMl2DDcnn = QtWidgets.QWidget()
    gui = extractml2ddcnn()
    gui.setupGUI(ExtractMl2DDcnn)
    ExtractMl2DDcnn.show()
    sys.exit(app.exec_())