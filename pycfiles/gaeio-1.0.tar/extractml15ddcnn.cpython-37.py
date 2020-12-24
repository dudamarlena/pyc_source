# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\extractml15ddcnn.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 36985 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.image as basic_image
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.dcnnsegmentor15d as ml_dcnn15d
import cognitivegeo.src.gui.viewml15ddcnn as gui_viewml15ddcnn
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class extractml15ddcnn(object):
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

    def setupGUI(self, ExtractMl15DDcnn):
        ExtractMl15DDcnn.setObjectName('ExtractMl15DDcnn')
        ExtractMl15DDcnn.setFixedSize(810, 480)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/retrieve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ExtractMl15DDcnn.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ExtractMl15DDcnn)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ExtractMl15DDcnn)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ExtractMl15DDcnn)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(ExtractMl15DDcnn)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 230, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 230, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(ExtractMl15DDcnn)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 230, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 270, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(ExtractMl15DDcnn)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 270, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 230, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(ExtractMl15DDcnn)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(ExtractMl15DDcnn)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ExtractMl15DDcnn)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ExtractMl15DDcnn)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ExtractMl15DDcnn)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 190))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(ExtractMl15DDcnn)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(ExtractMl15DDcnn)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 190))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 350, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 350, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ExtractMl15DDcnn)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 350, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 390, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ExtractMl15DDcnn)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 390, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 350, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 350, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ExtractMl15DDcnn)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 350, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 390, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ExtractMl15DDcnn)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 390, 40, 30))
        self.lblpara = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 320, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ExtractMl15DDcnn)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lbltype = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lbltype.setObjectName('lbltype')
        self.lbltype.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.cbbtype = QtWidgets.QComboBox(ExtractMl15DDcnn)
        self.cbbtype.setObjectName('cbbtype')
        self.cbbtype.setGeometry(QtCore.QRect(150, 390, 240, 30))
        self.lblsave = QtWidgets.QLabel(ExtractMl15DDcnn)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 430, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ExtractMl15DDcnn)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(150, 430, 100, 30))
        self.btnapply = QtWidgets.QPushButton(ExtractMl15DDcnn)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(520, 430, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/retrieve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ExtractMl15DDcnn)
        self.msgbox.setObjectName('msgbox')
        _center_x = ExtractMl15DDcnn.geometry().center().x()
        _center_y = ExtractMl15DDcnn.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ExtractMl15DDcnn)
        QtCore.QMetaObject.connectSlotsByName(ExtractMl15DDcnn)

    def retranslateGUI(self, ExtractMl15DDcnn):
        self.dialog = ExtractMl15DDcnn
        _translate = QtCore.QCoreApplication.translate
        ExtractMl15DDcnn.setWindowTitle(_translate('ExtractMl15DDcnn', 'Extract 1.5D-DCNN'))
        self.lblfrom.setText(_translate('ExtractMl15DDcnn', 'Select network:'))
        self.ldtfrom.setText(_translate('ExtractMl15DDcnn', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ExtractMl15DDcnn', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ExtractMl15DDcnn', 'Training features:'))
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblornt.setText(_translate('ExtractMl15DDcnn', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.cbbornt.currentIndexChanged.connect(self.changeCbbOrnt)
        self.lbloldsize.setText(_translate('ExtractMl15DDcnn', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('ExtractMl15DDcnn', 'height='))
        self.ldtoldheight.setText(_translate('ExtractMl15DDcnn', '0'))
        self.ldtoldheight.setEnabled(False)
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('ExtractMl15DDcnn', 'width='))
        self.ldtoldwidth.setText(_translate('ExtractMl15DDcnn', '0'))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtoldwidth.setEnabled(False)
        self.lblnewsize.setText(_translate('ExtractMl15DDcnn', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('ExtractMl15DDcnn', 'height='))
        self.ldtnewheight.setText(_translate('ExtractMl15DDcnn', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('ExtractMl15DDcnn', 'width='))
        self.ldtnewwidth.setText(_translate('ExtractMl15DDcnn', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnetwork.setText(_translate('ExtractMl15DDcnn', 'Pre-trained DCNN architecture:'))
        self.btnviewnetwork.setText(_translate('ExtractMl15DDcnn', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('ExtractMl15DDcnn', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ExtractMl15DDcnn', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('ExtractMl15DDcnn', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('ExtractMl15DDcnn', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('ExtractMl15DDcnn', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ExtractMl15DDcnn', 'height='))
        self.ldtmaskheight.setText(_translate('ExtractMl15DDcnn', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ExtractMl15DDcnn', 'width='))
        self.ldtmaskwidth.setText(_translate('ExtractMl15DDcnn', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ExtractMl15DDcnn', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ExtractMl15DDcnn', 'height='))
        self.ldtpoolheight.setText(_translate('ExtractMl15DDcnn', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ExtractMl15DDcnn', 'width='))
        self.ldtpoolwidth.setText(_translate('ExtractMl15DDcnn', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ExtractMl15DDcnn', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ExtractMl15DDcnn', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ExtractMl15DDcnn', '5'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltype.setText(_translate('ExtractMl2DCnn', 'Target layer='))
        self.lbltype.setAlignment(QtCore.Qt.AlignRight)
        self.lblsave.setText(_translate('ExtractMl2DCnn', 'Output prefix='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ExtractMl2DCnn', 'dcnn15d_feature_'))
        self.btnapply.setText(_translate('ExtractMl15DDcnn', 'Extract 1.5D-DCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnExtractMl15DDcnn)

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
        if ml_tfm.check15DDCNNModel(self.modelpath, self.modelname):
            _shape = self.getImageSize(self.lwgfeature.currentItem().text())
        _height = _shape[0]
        _width = _shape[1]
        self.ldtoldheight.setText(str(_height))
        self.ldtoldwidth.setText(str(_width))

    def changeCbbOrnt(self):
        _shape = [
         0, 0]
        if ml_tfm.check15DDCNNModel(self.modelpath, self.modelname):
            _shape = self.getImageSize(self.lwgfeature.currentItem().text())
        _height = _shape[0]
        _width = _shape[1]
        self.ldtoldheight.setText(str(_height))
        self.ldtoldwidth.setText(str(_width))

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
        _viewmldcnn = QtWidgets.QDialog()
        _gui = gui_viewml15ddcnn()
        _gui.linestyle = self.linestyle
        _gui.maskstyle = self.maskstyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewmldcnn)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewmldcnn.exec()
        _viewmldcnn.show()

    def clickBtnExtractMl15DDcnn--- This code section failed: ---

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
               24  LOAD_STR                 'ERROR in ExtractMl15DDcnn: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 481        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 482        44  LOAD_STR                 'Extract 1.5D-DCNN'

 L. 483        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 484        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 486        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              check15DDCNNModel
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
               80  LOAD_STR                 'ERROR in ExtractMl15DDcnn: No pre-DCNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 488        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 489       100  LOAD_STR                 'Extract 1.5D-DCNN'

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
              146  LOAD_STR                 "ERROR in ExtractMl15DDcnn: Feature '%s' not found in seismic data"
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

 L. 498       170  LOAD_STR                 'Extract 1.5D-DCNN'

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
              312  LOAD_STR                 'ERROR in ExtractMl15DDcnn: Non-integer feature size'
              314  LOAD_STR                 'error'
              316  LOAD_CONST               ('type',)
              318  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              320  POP_TOP          

 L. 511       322  LOAD_GLOBAL              QtWidgets
              324  LOAD_ATTR                QMessageBox
              326  LOAD_METHOD              critical
              328  LOAD_FAST                'self'
              330  LOAD_ATTR                msgbox

 L. 512       332  LOAD_STR                 'Extract 1.5D-DCNN'

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
              388  LOAD_STR                 'ERROR in ExtractMl15DDcnn: Features are not 2D'
              390  LOAD_STR                 'error'
              392  LOAD_CONST               ('type',)
              394  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              396  POP_TOP          

 L. 518       398  LOAD_GLOBAL              QtWidgets
              400  LOAD_ATTR                QMessageBox
              402  LOAD_METHOD              critical
              404  LOAD_FAST                'self'
              406  LOAD_ATTR                msgbox

 L. 519       408  LOAD_STR                 'Extract 1.5D-DCNN'

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
              460  LOAD_STR                 'ERROR in ExtractMl15DDcnn: Non-positive batch size'
              462  LOAD_STR                 'error'
              464  LOAD_CONST               ('type',)
              466  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              468  POP_TOP          

 L. 526       470  LOAD_GLOBAL              QtWidgets
              472  LOAD_ATTR                QMessageBox
              474  LOAD_METHOD              critical
              476  LOAD_FAST                'self'
              478  LOAD_ATTR                msgbox

 L. 527       480  LOAD_STR                 'Extract 1.5D-DCNN'

 L. 528       482  LOAD_STR                 'Non-positive batch size'
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
              516  LOAD_STR                 'ERROR in ExtractMl15DDcnn: No prefix specified'
              518  LOAD_STR                 'error'
              520  LOAD_CONST               ('type',)
              522  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              524  POP_TOP          

 L. 533       526  LOAD_GLOBAL              QtWidgets
              528  LOAD_ATTR                QMessageBox
              530  LOAD_METHOD              critical
              532  LOAD_FAST                'self'
              534  LOAD_ATTR                msgbox

 L. 534       536  LOAD_STR                 'Extract 1.5D-DCNN'

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
              606  LOAD_STR                 'Extract 1.5D-DCNN'

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

 L. 547       666  LOAD_GLOBAL              print
              668  LOAD_STR                 'ExtractMl15DDcnn: Step 1 - Reformat images'
              670  CALL_FUNCTION_1       1  '1 positional argument'
              672  POP_TOP          

 L. 548       674  BUILD_MAP_0           0 
              676  STORE_FAST               '_seisdict'

 L. 549       678  SETUP_LOOP          708  'to 708'
              680  LOAD_FAST                '_features'
              682  GET_ITER         
              684  FOR_ITER            706  'to 706'
              686  STORE_FAST               'f'

 L. 550       688  LOAD_FAST                'self'
              690  LOAD_METHOD              reformatImage
              692  LOAD_FAST                'f'
              694  CALL_METHOD_1         1  '1 positional argument'
              696  LOAD_FAST                '_seisdict'
              698  LOAD_FAST                'f'
              700  STORE_SUBSCR     
          702_704  JUMP_BACK           684  'to 684'
              706  POP_BLOCK        
            708_0  COME_FROM_LOOP      678  '678'

 L. 551       708  LOAD_GLOBAL              print
              710  LOAD_STR                 'ExtractMl15DDcnn: Step 2 - Interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 552       712  LOAD_FAST                '_image_height'
              714  LOAD_FAST                '_image_width'
              716  LOAD_FAST                '_image_height_new'
              718  LOAD_FAST                '_image_width_new'
              720  BUILD_TUPLE_4         4 
              722  BINARY_MODULO    
              724  CALL_FUNCTION_1       1  '1 positional argument'
              726  POP_TOP          

 L. 555       728  LOAD_FAST                '_image_height_new'
              730  LOAD_FAST                '_image_height'
              732  COMPARE_OP               !=
          734_736  POP_JUMP_IF_TRUE    748  'to 748'
              738  LOAD_FAST                '_image_width_new'
              740  LOAD_FAST                '_image_width'
              742  COMPARE_OP               !=
          744_746  POP_JUMP_IF_FALSE   792  'to 792'
            748_0  COME_FROM           734  '734'

 L. 556       748  SETUP_LOOP          792  'to 792'
              750  LOAD_FAST                '_features'
              752  GET_ITER         
              754  FOR_ITER            790  'to 790'
              756  STORE_FAST               'f'

 L. 557       758  LOAD_GLOBAL              basic_image
              760  LOAD_ATTR                changeImageSize
              762  LOAD_FAST                '_seisdict'
              764  LOAD_FAST                'f'
              766  BINARY_SUBSCR    

 L. 558       768  LOAD_FAST                '_image_height'

 L. 559       770  LOAD_FAST                '_image_width'

 L. 560       772  LOAD_FAST                '_image_height_new'

 L. 561       774  LOAD_FAST                '_image_width_new'
              776  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
              778  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              780  LOAD_FAST                '_seisdict'
              782  LOAD_FAST                'f'
              784  STORE_SUBSCR     
          786_788  JUMP_BACK           754  'to 754'
              790  POP_BLOCK        
            792_0  COME_FROM_LOOP      748  '748'
            792_1  COME_FROM           744  '744'

 L. 563       792  LOAD_GLOBAL              print
              794  LOAD_STR                 'ExtractMl15DDcnn: Step 3 - Extract'
              796  CALL_FUNCTION_1       1  '1 positional argument'
              798  POP_TOP          

 L. 564       800  LOAD_GLOBAL              np
              802  LOAD_METHOD              shape
              804  LOAD_FAST                '_seisdict'
              806  LOAD_FAST                '_features'
              808  LOAD_CONST               0
              810  BINARY_SUBSCR    
              812  BINARY_SUBSCR    
              814  CALL_METHOD_1         1  '1 positional argument'
              816  LOAD_CONST               0
              818  BINARY_SUBSCR    
              820  STORE_FAST               '_nsample'

 L. 566       822  LOAD_GLOBAL              int
              824  LOAD_GLOBAL              np
              826  LOAD_METHOD              ceil
              828  LOAD_FAST                '_nsample'
              830  LOAD_FAST                '_batch'
              832  BINARY_TRUE_DIVIDE
              834  CALL_METHOD_1         1  '1 positional argument'
              836  CALL_FUNCTION_1       1  '1 positional argument'
              838  STORE_FAST               '_nloop'

 L. 569       840  LOAD_GLOBAL              QtWidgets
              842  LOAD_METHOD              QProgressDialog
              844  CALL_METHOD_0         0  '0 positional arguments'
              846  STORE_FAST               '_pgsdlg'

 L. 570       848  LOAD_GLOBAL              QtGui
              850  LOAD_METHOD              QIcon
              852  CALL_METHOD_0         0  '0 positional arguments'
              854  STORE_FAST               'icon'

 L. 571       856  LOAD_FAST                'icon'
              858  LOAD_METHOD              addPixmap
              860  LOAD_GLOBAL              QtGui
              862  LOAD_METHOD              QPixmap
              864  LOAD_GLOBAL              os
              866  LOAD_ATTR                path
              868  LOAD_METHOD              join
              870  LOAD_FAST                'self'
              872  LOAD_ATTR                iconpath
              874  LOAD_STR                 'icons/check.png'
              876  CALL_METHOD_2         2  '2 positional arguments'
              878  CALL_METHOD_1         1  '1 positional argument'

 L. 572       880  LOAD_GLOBAL              QtGui
              882  LOAD_ATTR                QIcon
              884  LOAD_ATTR                Normal
              886  LOAD_GLOBAL              QtGui
              888  LOAD_ATTR                QIcon
              890  LOAD_ATTR                Off
              892  CALL_METHOD_3         3  '3 positional arguments'
              894  POP_TOP          

 L. 573       896  LOAD_FAST                '_pgsdlg'
              898  LOAD_METHOD              setWindowIcon
              900  LOAD_FAST                'icon'
              902  CALL_METHOD_1         1  '1 positional argument'
              904  POP_TOP          

 L. 574       906  LOAD_FAST                '_pgsdlg'
              908  LOAD_METHOD              setWindowTitle
              910  LOAD_STR                 'Extract 1.5D-DCNN'
              912  CALL_METHOD_1         1  '1 positional argument'
              914  POP_TOP          

 L. 575       916  LOAD_FAST                '_pgsdlg'
              918  LOAD_METHOD              setCancelButton
              920  LOAD_CONST               None
              922  CALL_METHOD_1         1  '1 positional argument'
              924  POP_TOP          

 L. 576       926  LOAD_FAST                '_pgsdlg'
              928  LOAD_METHOD              setWindowFlags
              930  LOAD_GLOBAL              QtCore
              932  LOAD_ATTR                Qt
              934  LOAD_ATTR                WindowStaysOnTopHint
              936  CALL_METHOD_1         1  '1 positional argument'
              938  POP_TOP          

 L. 577       940  LOAD_FAST                '_pgsdlg'
              942  LOAD_METHOD              forceShow
              944  CALL_METHOD_0         0  '0 positional arguments'
              946  POP_TOP          

 L. 578       948  LOAD_FAST                '_pgsdlg'
              950  LOAD_METHOD              setFixedWidth
              952  LOAD_CONST               400
              954  CALL_METHOD_1         1  '1 positional argument'
              956  POP_TOP          

 L. 579       958  LOAD_FAST                '_pgsdlg'
              960  LOAD_METHOD              setMaximum
              962  LOAD_FAST                '_nloop'
              964  CALL_METHOD_1         1  '1 positional argument'
              966  POP_TOP          

 L. 581       968  LOAD_FAST                'self'
              970  LOAD_ATTR                modelinfo
              972  LOAD_STR                 'number_conv_block'
              974  BINARY_SUBSCR    
              976  STORE_FAST               '_nblock'

 L. 582       978  LOAD_FAST                'self'
              980  LOAD_ATTR                modelinfo
              982  LOAD_STR                 'number_conv_layer'
              984  BINARY_SUBSCR    
              986  STORE_FAST               '_nlayer'

 L. 583       988  LOAD_FAST                'self'
              990  LOAD_ATTR                modelinfo
              992  LOAD_STR                 'number_conv_feature'
              994  BINARY_SUBSCR    
              996  STORE_FAST               '_nfeature'

 L. 585       998  LOAD_FAST                'self'
             1000  LOAD_ATTR                cbbtype
             1002  LOAD_METHOD              currentIndex
             1004  CALL_METHOD_0         0  '0 positional arguments'
             1006  STORE_FAST               '_featureidx'

 L. 586      1008  LOAD_CONST               0
             1010  STORE_FAST               '_blockidx'

 L. 587      1012  LOAD_CONST               0
             1014  STORE_FAST               '_layeridx'

 L. 588      1016  SETUP_LOOP         1092  'to 1092'
             1018  LOAD_GLOBAL              range
             1020  LOAD_FAST                '_nblock'
             1022  CALL_FUNCTION_1       1  '1 positional argument'
             1024  GET_ITER         
           1026_0  COME_FROM          1056  '1056'
             1026  FOR_ITER           1090  'to 1090'
             1028  STORE_FAST               'i'

 L. 589      1030  LOAD_GLOBAL              sum
             1032  LOAD_FAST                '_nlayer'
             1034  LOAD_CONST               0
             1036  LOAD_FAST                'i'
             1038  LOAD_CONST               1
             1040  BINARY_ADD       
             1042  BUILD_SLICE_2         2 
             1044  BINARY_SUBSCR    
             1046  CALL_FUNCTION_1       1  '1 positional argument'
             1048  LOAD_FAST                '_featureidx'
             1050  LOAD_CONST               1
             1052  BINARY_ADD       
             1054  COMPARE_OP               >=
         1056_1058  POP_JUMP_IF_FALSE  1026  'to 1026'

 L. 590      1060  LOAD_FAST                'i'
             1062  STORE_FAST               '_blockidx'

 L. 591      1064  LOAD_FAST                '_featureidx'
             1066  LOAD_GLOBAL              sum
             1068  LOAD_FAST                '_nlayer'
             1070  LOAD_CONST               0
             1072  LOAD_FAST                'i'
             1074  BUILD_SLICE_2         2 
             1076  BINARY_SUBSCR    
             1078  CALL_FUNCTION_1       1  '1 positional argument'
             1080  BINARY_SUBTRACT  
             1082  STORE_FAST               '_layeridx'

 L. 592      1084  BREAK_LOOP       
         1086_1088  JUMP_BACK          1026  'to 1026'
             1090  POP_BLOCK        
           1092_0  COME_FROM_LOOP     1016  '1016'

 L. 594      1092  LOAD_FAST                '_nfeature'
             1094  LOAD_FAST                '_blockidx'
             1096  BINARY_SUBSCR    
             1098  STORE_FAST               '_nfeature'

 L. 595      1100  LOAD_GLOBAL              np
             1102  LOAD_METHOD              zeros
             1104  LOAD_FAST                '_nsample'
             1106  LOAD_FAST                '_nfeature'
             1108  LOAD_FAST                '_image_height'
             1110  LOAD_FAST                '_image_width'
             1112  BINARY_MULTIPLY  
             1114  BUILD_LIST_3          3 
             1116  CALL_METHOD_1         1  '1 positional argument'
             1118  STORE_FAST               '_result'

 L. 596      1120  LOAD_CONST               0
             1122  STORE_FAST               'idxstart'

 L. 597  1124_1126  SETUP_LOOP         1502  'to 1502'
             1128  LOAD_GLOBAL              range
             1130  LOAD_FAST                '_nloop'
             1132  CALL_FUNCTION_1       1  '1 positional argument'
             1134  GET_ITER         
         1136_1138  FOR_ITER           1500  'to 1500'
             1140  STORE_FAST               'i'

 L. 599      1142  LOAD_GLOBAL              QtCore
             1144  LOAD_ATTR                QCoreApplication
             1146  LOAD_METHOD              instance
             1148  CALL_METHOD_0         0  '0 positional arguments'
             1150  LOAD_METHOD              processEvents
             1152  CALL_METHOD_0         0  '0 positional arguments'
             1154  POP_TOP          

 L. 601      1156  LOAD_GLOBAL              sys
             1158  LOAD_ATTR                stdout
             1160  LOAD_METHOD              write

 L. 602      1162  LOAD_STR                 '\r>>> Extract 1.5D-DCNN, proceeding %.1f%% '
             1164  LOAD_GLOBAL              float
             1166  LOAD_FAST                'i'
             1168  CALL_FUNCTION_1       1  '1 positional argument'
             1170  LOAD_GLOBAL              float
             1172  LOAD_FAST                '_nloop'
             1174  CALL_FUNCTION_1       1  '1 positional argument'
             1176  BINARY_TRUE_DIVIDE
             1178  LOAD_CONST               100.0
             1180  BINARY_MULTIPLY  
             1182  BINARY_MODULO    
             1184  CALL_METHOD_1         1  '1 positional argument'
             1186  POP_TOP          

 L. 603      1188  LOAD_GLOBAL              sys
             1190  LOAD_ATTR                stdout
             1192  LOAD_METHOD              flush
             1194  CALL_METHOD_0         0  '0 positional arguments'
             1196  POP_TOP          

 L. 605      1198  LOAD_FAST                'idxstart'
             1200  LOAD_FAST                '_batch'
             1202  BINARY_ADD       
             1204  STORE_FAST               'idxend'

 L. 606      1206  LOAD_FAST                'idxend'
             1208  LOAD_FAST                '_nsample'
             1210  COMPARE_OP               >
         1212_1214  POP_JUMP_IF_FALSE  1220  'to 1220'

 L. 607      1216  LOAD_FAST                '_nsample'
             1218  STORE_FAST               'idxend'
           1220_0  COME_FROM          1212  '1212'

 L. 608      1220  LOAD_GLOBAL              np
             1222  LOAD_METHOD              linspace
             1224  LOAD_FAST                'idxstart'
             1226  LOAD_FAST                'idxend'
             1228  LOAD_CONST               1
             1230  BINARY_SUBTRACT  
             1232  LOAD_FAST                'idxend'
             1234  LOAD_FAST                'idxstart'
             1236  BINARY_SUBTRACT  
             1238  CALL_METHOD_3         3  '3 positional arguments'
             1240  LOAD_METHOD              astype
             1242  LOAD_GLOBAL              int
             1244  CALL_METHOD_1         1  '1 positional argument'
             1246  STORE_FAST               'idxlist'

 L. 609      1248  LOAD_FAST                'idxend'
             1250  STORE_FAST               'idxstart'

 L. 610      1252  LOAD_GLOBAL              basic_mdt
             1254  LOAD_METHOD              retrieveDictByIndex
             1256  LOAD_FAST                '_seisdict'
             1258  LOAD_FAST                'idxlist'
             1260  CALL_METHOD_2         2  '2 positional arguments'
             1262  STORE_FAST               '_dict'

 L. 611      1264  LOAD_GLOBAL              ml_dcnn15d
             1266  LOAD_ATTR                extract15DDCNNConvFeature
             1268  LOAD_FAST                '_dict'

 L. 612      1270  LOAD_FAST                '_image_height_new'
             1272  LOAD_FAST                '_image_width_new'

 L. 613      1274  LOAD_FAST                'self'
             1276  LOAD_ATTR                modelpath

 L. 614      1278  LOAD_FAST                'self'
             1280  LOAD_ATTR                modelname

 L. 615      1282  LOAD_FAST                '_blockidx'

 L. 616      1284  LOAD_FAST                '_layeridx'
             1286  LOAD_STR                 'full'

 L. 617      1288  LOAD_CONST               1
             1290  LOAD_CONST               True
             1292  LOAD_CONST               ('imageheight', 'imagewidth', 'dcnnpath', 'dcnnname', 'blockidx', 'layeridx', 'location', 'batchsize', 'verbose')
             1294  CALL_FUNCTION_KW_10    10  '10 total positional and keyword args'
             1296  STORE_FAST               '_rst'

 L. 620      1298  LOAD_GLOBAL              np
             1300  LOAD_METHOD              shape
             1302  LOAD_FAST                '_rst'
             1304  CALL_METHOD_1         1  '1 positional argument'
             1306  LOAD_CONST               2
             1308  BINARY_SUBSCR    
             1310  STORE_FAST               '_feature_height'

 L. 621      1312  LOAD_GLOBAL              np
             1314  LOAD_METHOD              shape
             1316  LOAD_FAST                '_rst'
             1318  CALL_METHOD_1         1  '1 positional argument'
             1320  LOAD_CONST               3
             1322  BINARY_SUBSCR    
             1324  STORE_FAST               '_feature_width'

 L. 622      1326  LOAD_FAST                '_feature_height'
             1328  LOAD_FAST                '_image_height'
             1330  COMPARE_OP               !=
         1332_1334  POP_JUMP_IF_TRUE   1346  'to 1346'
             1336  LOAD_FAST                '_feature_width'
             1338  LOAD_FAST                '_image_width'
             1340  COMPARE_OP               !=
         1342_1344  POP_JUMP_IF_FALSE  1442  'to 1442'
           1346_0  COME_FROM          1332  '1332'

 L. 623      1346  LOAD_GLOBAL              np
             1348  LOAD_METHOD              reshape
             1350  LOAD_FAST                '_rst'
             1352  LOAD_GLOBAL              np
             1354  LOAD_METHOD              shape
             1356  LOAD_FAST                '_rst'
             1358  CALL_METHOD_1         1  '1 positional argument'
             1360  LOAD_CONST               0
             1362  BINARY_SUBSCR    
             1364  LOAD_FAST                '_nfeature'
             1366  BINARY_MULTIPLY  
             1368  LOAD_FAST                '_feature_height'
             1370  LOAD_FAST                '_feature_width'
             1372  BINARY_MULTIPLY  
             1374  BUILD_LIST_2          2 
             1376  CALL_METHOD_2         2  '2 positional arguments'
             1378  STORE_FAST               '_rst'

 L. 624      1380  LOAD_GLOBAL              basic_image
             1382  LOAD_ATTR                changeImageSize
             1384  LOAD_FAST                '_rst'

 L. 625      1386  LOAD_FAST                '_feature_height'

 L. 626      1388  LOAD_FAST                '_feature_width'

 L. 627      1390  LOAD_FAST                '_image_height'

 L. 628      1392  LOAD_FAST                '_image_width'
             1394  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1396  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1398  STORE_FAST               '_rst'

 L. 629      1400  LOAD_GLOBAL              np
             1402  LOAD_METHOD              reshape
             1404  LOAD_FAST                '_rst'
             1406  LOAD_CONST               -1
             1408  LOAD_FAST                '_nfeature'
             1410  LOAD_FAST                '_image_height'
             1412  LOAD_FAST                '_image_width'
             1414  BINARY_MULTIPLY  
             1416  BUILD_LIST_3          3 
             1418  CALL_METHOD_2         2  '2 positional arguments'
             1420  LOAD_FAST                '_result'
             1422  LOAD_FAST                'idxlist'
             1424  LOAD_CONST               None
             1426  LOAD_CONST               None
             1428  BUILD_SLICE_2         2 
             1430  LOAD_CONST               None
             1432  LOAD_CONST               None
             1434  BUILD_SLICE_2         2 
             1436  BUILD_TUPLE_3         3 
             1438  STORE_SUBSCR     
             1440  JUMP_FORWARD       1482  'to 1482'
           1442_0  COME_FROM          1342  '1342'

 L. 631      1442  LOAD_GLOBAL              np
             1444  LOAD_METHOD              reshape
             1446  LOAD_FAST                '_rst'
             1448  LOAD_CONST               -1
             1450  LOAD_FAST                '_nfeature'
             1452  LOAD_FAST                '_image_height'
             1454  LOAD_FAST                '_image_width'
             1456  BINARY_MULTIPLY  
             1458  BUILD_LIST_3          3 
             1460  CALL_METHOD_2         2  '2 positional arguments'
             1462  LOAD_FAST                '_result'
             1464  LOAD_FAST                'idxlist'
             1466  LOAD_CONST               None
             1468  LOAD_CONST               None
             1470  BUILD_SLICE_2         2 
             1472  LOAD_CONST               None
             1474  LOAD_CONST               None
             1476  BUILD_SLICE_2         2 
             1478  BUILD_TUPLE_3         3 
             1480  STORE_SUBSCR     
           1482_0  COME_FROM          1440  '1440'

 L. 634      1482  LOAD_FAST                '_pgsdlg'
             1484  LOAD_METHOD              setValue
             1486  LOAD_FAST                'i'
             1488  LOAD_CONST               1
             1490  BINARY_ADD       
             1492  CALL_METHOD_1         1  '1 positional argument'
             1494  POP_TOP          
         1496_1498  JUMP_BACK          1136  'to 1136'
             1500  POP_BLOCK        
           1502_0  COME_FROM_LOOP     1124  '1124'

 L. 636      1502  LOAD_GLOBAL              print
             1504  LOAD_STR                 'Done'
             1506  CALL_FUNCTION_1       1  '1 positional argument'
             1508  POP_TOP          

 L. 638      1510  LOAD_FAST                'self'
             1512  LOAD_ATTR                survinfo
             1514  STORE_FAST               '_info'

 L. 639      1516  LOAD_FAST                '_info'
             1518  LOAD_STR                 'ILNum'
             1520  BINARY_SUBSCR    
             1522  STORE_FAST               '_inlnum'

 L. 640      1524  LOAD_FAST                '_info'
             1526  LOAD_STR                 'XLNum'
             1528  BINARY_SUBSCR    
             1530  STORE_FAST               '_xlnum'

 L. 641      1532  LOAD_FAST                '_info'
             1534  LOAD_STR                 'ZNum'
             1536  BINARY_SUBSCR    
             1538  STORE_FAST               '_znum'

 L. 642      1540  SETUP_LOOP         1780  'to 1780'
             1542  LOAD_GLOBAL              range
             1544  LOAD_FAST                '_nfeature'
             1546  CALL_FUNCTION_1       1  '1 positional argument'
             1548  GET_ITER         
             1550  FOR_ITER           1778  'to 1778'
             1552  STORE_FAST               'i'

 L. 643      1554  LOAD_FAST                'self'
             1556  LOAD_ATTR                cbbornt
             1558  LOAD_METHOD              currentIndex
             1560  CALL_METHOD_0         0  '0 positional arguments'
             1562  LOAD_CONST               0
             1564  COMPARE_OP               ==
         1566_1568  POP_JUMP_IF_FALSE  1624  'to 1624'

 L. 644      1570  LOAD_GLOBAL              np
             1572  LOAD_METHOD              reshape
             1574  LOAD_FAST                '_result'
             1576  LOAD_CONST               None
             1578  LOAD_CONST               None
             1580  BUILD_SLICE_2         2 
             1582  LOAD_FAST                'i'
             1584  LOAD_CONST               None
             1586  LOAD_CONST               None
             1588  BUILD_SLICE_2         2 
             1590  BUILD_TUPLE_3         3 
             1592  BINARY_SUBSCR    
             1594  LOAD_CONST               -1
             1596  LOAD_FAST                '_znum'
             1598  LOAD_FAST                '_xlnum'
             1600  BUILD_LIST_3          3 
             1602  CALL_METHOD_2         2  '2 positional arguments'
             1604  STORE_FAST               '_rst'

 L. 645      1606  LOAD_GLOBAL              np
             1608  LOAD_METHOD              transpose
             1610  LOAD_FAST                '_rst'
             1612  LOAD_CONST               1
             1614  LOAD_CONST               2
             1616  LOAD_CONST               0
             1618  BUILD_LIST_3          3 
             1620  CALL_METHOD_2         2  '2 positional arguments'
             1622  STORE_FAST               '_rst'
           1624_0  COME_FROM          1566  '1566'

 L. 646      1624  LOAD_FAST                'self'
             1626  LOAD_ATTR                cbbornt
             1628  LOAD_METHOD              currentIndex
             1630  CALL_METHOD_0         0  '0 positional arguments'
             1632  LOAD_CONST               1
             1634  COMPARE_OP               ==
         1636_1638  POP_JUMP_IF_FALSE  1694  'to 1694'

 L. 647      1640  LOAD_GLOBAL              np
             1642  LOAD_METHOD              reshape
             1644  LOAD_FAST                '_result'
             1646  LOAD_CONST               None
             1648  LOAD_CONST               None
             1650  BUILD_SLICE_2         2 
             1652  LOAD_FAST                'i'
             1654  LOAD_CONST               None
             1656  LOAD_CONST               None
             1658  BUILD_SLICE_2         2 
             1660  BUILD_TUPLE_3         3 
             1662  BINARY_SUBSCR    
             1664  LOAD_CONST               -1
             1666  LOAD_FAST                '_znum'
             1668  LOAD_FAST                '_inlnum'
             1670  BUILD_LIST_3          3 
             1672  CALL_METHOD_2         2  '2 positional arguments'
             1674  STORE_FAST               '_rst'

 L. 648      1676  LOAD_GLOBAL              np
             1678  LOAD_METHOD              transpose
             1680  LOAD_FAST                '_rst'
             1682  LOAD_CONST               1
             1684  LOAD_CONST               0
             1686  LOAD_CONST               2
             1688  BUILD_LIST_3          3 
             1690  CALL_METHOD_2         2  '2 positional arguments'
             1692  STORE_FAST               '_rst'
           1694_0  COME_FROM          1636  '1636'

 L. 649      1694  LOAD_FAST                'self'
             1696  LOAD_ATTR                cbbornt
             1698  LOAD_METHOD              currentIndex
             1700  CALL_METHOD_0         0  '0 positional arguments'
             1702  LOAD_CONST               2
             1704  COMPARE_OP               ==
         1706_1708  POP_JUMP_IF_FALSE  1746  'to 1746'

 L. 650      1710  LOAD_GLOBAL              np
             1712  LOAD_METHOD              reshape
             1714  LOAD_FAST                '_result'
             1716  LOAD_CONST               None
             1718  LOAD_CONST               None
             1720  BUILD_SLICE_2         2 
             1722  LOAD_FAST                'i'
             1724  LOAD_CONST               None
             1726  LOAD_CONST               None
             1728  BUILD_SLICE_2         2 
             1730  BUILD_TUPLE_3         3 
             1732  BINARY_SUBSCR    
             1734  LOAD_CONST               -1
             1736  LOAD_FAST                '_xlnum'
             1738  LOAD_FAST                '_inlnum'
             1740  BUILD_LIST_3          3 
             1742  CALL_METHOD_2         2  '2 positional arguments'
             1744  STORE_FAST               '_rst'
           1746_0  COME_FROM          1706  '1706'

 L. 652      1746  LOAD_FAST                '_rst'
             1748  LOAD_FAST                'self'
             1750  LOAD_ATTR                seisdata
             1752  LOAD_FAST                'self'
             1754  LOAD_ATTR                ldtsave
             1756  LOAD_METHOD              text
             1758  CALL_METHOD_0         0  '0 positional arguments'
             1760  LOAD_GLOBAL              str
             1762  LOAD_FAST                'i'
             1764  LOAD_CONST               1
             1766  BINARY_ADD       
             1768  CALL_FUNCTION_1       1  '1 positional argument'
             1770  BINARY_ADD       
             1772  STORE_SUBSCR     
         1774_1776  JUMP_BACK          1550  'to 1550'
             1778  POP_BLOCK        
           1780_0  COME_FROM_LOOP     1540  '1540'

 L. 654      1780  LOAD_GLOBAL              QtWidgets
             1782  LOAD_ATTR                QMessageBox
             1784  LOAD_METHOD              information
             1786  LOAD_FAST                'self'
             1788  LOAD_ATTR                msgbox

 L. 655      1790  LOAD_STR                 'Extract 1.5D-DCNN'

 L. 656      1792  LOAD_GLOBAL              str
             1794  LOAD_FAST                '_nfeature'
             1796  CALL_FUNCTION_1       1  '1 positional argument'
             1798  LOAD_STR                 ' DCNN features extracted successfully'
             1800  BINARY_ADD       
             1802  CALL_METHOD_3         3  '3 positional arguments'
             1804  POP_TOP          

Parse error at or near `CALL_METHOD_3' instruction at offset 1802

    def reformatImage(self, feature):
        _info = self.survinfo
        _inlnum = _info['ILNum']
        _xlnum = _info['XLNum']
        _znum = _info['ZNum']
        _data = self.seisdata[feature]
        _data = np.transpose(_data, [2, 1, 0])
        if self.cbbornt.currentIndex() == 0:
            _data = np.reshape(np.transpose(_data, [0, 2, 1]), [_inlnum, -1])
        if self.cbbornt.currentIndex() == 1:
            _data = np.reshape(np.transpose(_data, [1, 2, 0]), [_xlnum, -1])
        if self.cbbornt.currentIndex() == 2:
            _data = np.reshape(np.transpose(_data, [2, 1, 0]), [_znum, -1])
        return _data

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
    ExtractMl15DDcnn = QtWidgets.QWidget()
    gui = extractml15ddcnn()
    gui.setupGUI(ExtractMl15DDcnn)
    ExtractMl15DDcnn.show()
    sys.exit(app.exec_())