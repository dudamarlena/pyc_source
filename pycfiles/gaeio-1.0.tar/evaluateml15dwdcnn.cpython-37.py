# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\evaluateml15dwdcnn.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 38331 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.curve as basic_curve
import cognitivegeo.src.basic.image as basic_image
import cognitivegeo.src.vis.messager as vis_msg
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.wdcnnsegmentor15d as ml_wdcnn15d
import cognitivegeo.src.gui.viewml2dwdcnn as gui_viewml2dwdcnn
import cognitivegeo.src.gui.viewmlconfmat as gui_viewmlconfmat
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class evaluateml15dwdcnn(object):
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

    def setupGUI(self, EvaluateMl15DWdcnn):
        EvaluateMl15DWdcnn.setObjectName('EvaluateMl15DWdcnn')
        EvaluateMl15DWdcnn.setFixedSize(810, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/check.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EvaluateMl15DWdcnn.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(EvaluateMl15DWdcnn)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(EvaluateMl15DWdcnn)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(EvaluateMl15DWdcnn)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(EvaluateMl15DWdcnn)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 230, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 230, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(EvaluateMl15DWdcnn)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 230, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 270, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(EvaluateMl15DWdcnn)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 270, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 230, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(EvaluateMl15DWdcnn)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(EvaluateMl15DWdcnn)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lbltarget = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 320, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(EvaluateMl15DWdcnn)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 320, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(EvaluateMl15DWdcnn)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(EvaluateMl15DWdcnn)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(EvaluateMl15DWdcnn)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 210))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(EvaluateMl15DWdcnn)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(EvaluateMl15DWdcnn)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 210))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 360, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 360, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(EvaluateMl15DWdcnn)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 400, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(EvaluateMl15DWdcnn)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 400, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 360, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 360, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(EvaluateMl15DWdcnn)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 360, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 400, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(EvaluateMl15DWdcnn)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 400, 40, 30))
        self.lblpara = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 370, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(EvaluateMl15DWdcnn)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 400, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(EvaluateMl15DWdcnn)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 400, 40, 30))
        self.btnapply = QtWidgets.QPushButton(EvaluateMl15DWdcnn)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(320, 450, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/check.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(EvaluateMl15DWdcnn)
        self.msgbox.setObjectName('msgbox')
        _center_x = EvaluateMl15DWdcnn.geometry().center().x()
        _center_y = EvaluateMl15DWdcnn.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(EvaluateMl15DWdcnn)
        QtCore.QMetaObject.connectSlotsByName(EvaluateMl15DWdcnn)

    def retranslateGUI(self, EvaluateMl15DWdcnn):
        self.dialog = EvaluateMl15DWdcnn
        _translate = QtCore.QCoreApplication.translate
        EvaluateMl15DWdcnn.setWindowTitle(_translate('EvaluateMl15DWdcnn', 'Evaluate 1.5D-WDCNN'))
        self.lblfrom.setText(_translate('EvaluateMl15DWdcnn', 'Select network:'))
        self.ldtfrom.setText(_translate('EvaluateMl15DWdcnn', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('EvaluateMl15DWdcnn', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('EvaluateMl15DWdcnn', 'Training features:'))
        self.lblornt.setText(_translate('EvaluateMl15DWdcnn', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('EvaluateMl15DWdcnn', 'Training target:'))
        self.lbloldsize.setText(_translate('EvaluateMl15DWdcnn', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('EvaluateMl15DWdcnn', 'height='))
        self.ldtoldheight.setText(_translate('EvaluateMl15DWdcnn', ''))
        self.ldtoldheight.setEnabled(False)
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('EvaluateMl15DWdcnn', 'width='))
        self.ldtoldwidth.setText(_translate('EvaluateMl15DWdcnn', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('EvaluateMl15DWdcnn', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('EvaluateMl15DWdcnn', 'height='))
        self.ldtnewheight.setText(_translate('EvaluateMl15DWdcnn', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('EvaluateMl15DWdcnn', 'width='))
        self.ldtnewwidth.setText(_translate('EvaluateMl15DWdcnn', ''))
        self.ldtnewwidth.setEnabled(False)
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.cbbornt.currentIndexChanged.connect(self.changeCbbOrnt)
        self.lblnetwork.setText(_translate('EvaluateMl15DWdcnn', 'Pre-trained WDCNN architecture:'))
        self.btnviewnetwork.setText(_translate('EvaluateMl15DWdcnn', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('EvaluateMl15DWdcnn', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('EvaluateMl15DWdcnn', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('EvaluateMl15DWdcnn', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('EvaluateMl15DWdcnn', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('EvaluateMl15DWdcnn', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('EvaluateMl15DWdcnn', 'height='))
        self.ldtmaskheight.setText(_translate('EvaluateMl15DWdcnn', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('EvaluateMl15DWdcnn', 'width='))
        self.ldtmaskwidth.setText(_translate('EvaluateMl15DWdcnn', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('EvaluateMl15DWdcnn', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('EvaluateMl15DWdcnn', 'height='))
        self.ldtpoolheight.setText(_translate('EvaluateMl15DWdcnn', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('EvaluateMl15DWdcnn', 'width='))
        self.ldtpoolwidth.setText(_translate('EvaluateMl15DWdcnn', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('EvaluateMl15DWdcnn', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('EvaluateMl15DWdcnn', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('EvaluateMl15DWdcnn', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('EvaluateMl15DWdcnn', 'Evaluate 1.5D-DCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnEvaluateMl15DWdcnn)

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
            self.cbbtarget.clear()
            self.cbbtarget.addItem(self.modelinfo['target'])
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
            self.cbbtarget.clear()
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

    def clickBtnEvaluateMl15DWdcnn--- This code section failed: ---

 L. 457         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 459         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 460        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in EvaluateMl15DWdcnn: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 461        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 462        44  LOAD_STR                 'Evaluate 1.5D-WDCNN'

 L. 463        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 464        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 466        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              check15DWDCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 467        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in EvaluateMl15DWdcnn: No pre-WDCNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 468        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 469       100  LOAD_STR                 'Evaluate 1.5D-WDCNN'

 L. 470       102  LOAD_STR                 'No pre-WDCNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 471       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 473       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 474       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 475       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in EvaluateMl15DWdcnn: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    

 L. 476       152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 477       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 478       170  LOAD_STR                 'Evaluate 1.5D-WDCNN'

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
              198  LOAD_STR                 'target'
              200  BINARY_SUBSCR    
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                seisdata
              206  LOAD_METHOD              keys
              208  CALL_METHOD_0         0  '0 positional arguments'
              210  COMPARE_OP               not-in
          212_214  POP_JUMP_IF_FALSE   276  'to 276'

 L. 483       216  LOAD_GLOBAL              vis_msg
              218  LOAD_ATTR                print
              220  LOAD_STR                 "ERROR in EvaluateMl15DWdcnn: Target key '%s' not found in seismic data"

 L. 484       222  LOAD_FAST                'self'
              224  LOAD_ATTR                modelinfo
              226  LOAD_STR                 'target'
              228  BINARY_SUBSCR    
              230  BINARY_MODULO    
              232  LOAD_STR                 'error'
              234  LOAD_CONST               ('type',)
              236  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              238  POP_TOP          

 L. 485       240  LOAD_GLOBAL              QtWidgets
              242  LOAD_ATTR                QMessageBox
              244  LOAD_METHOD              critical
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                msgbox

 L. 486       250  LOAD_STR                 'Evaluate 1.5D-WDCNN'

 L. 487       252  LOAD_STR                 "Target key '"
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                modelinfo
              258  LOAD_STR                 'target'
              260  BINARY_SUBSCR    
              262  BINARY_ADD       
              264  LOAD_STR                 ' not found in seismic data'
              266  BINARY_ADD       
              268  CALL_METHOD_3         3  '3 positional arguments'
              270  POP_TOP          

 L. 488       272  LOAD_CONST               None
              274  RETURN_VALUE     
            276_0  COME_FROM           212  '212'

 L. 490       276  LOAD_FAST                'self'
              278  LOAD_ATTR                modelinfo
              280  LOAD_STR                 'feature_list'
              282  BINARY_SUBSCR    
              284  STORE_FAST               '_features'

 L. 491       286  LOAD_FAST                'self'
              288  LOAD_ATTR                modelinfo
              290  LOAD_STR                 'target'
              292  BINARY_SUBSCR    
              294  STORE_FAST               '_target'

 L. 492       296  LOAD_FAST                'self'
              298  LOAD_ATTR                modelinfo
              300  LOAD_STR                 'number_class'
              302  BINARY_SUBSCR    
              304  STORE_FAST               '_nclass'

 L. 494       306  LOAD_GLOBAL              basic_data
              308  LOAD_METHOD              str2int
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                ldtoldheight
              314  LOAD_METHOD              text
              316  CALL_METHOD_0         0  '0 positional arguments'
              318  CALL_METHOD_1         1  '1 positional argument'
              320  STORE_FAST               '_image_height'

 L. 495       322  LOAD_GLOBAL              basic_data
              324  LOAD_METHOD              str2int
              326  LOAD_FAST                'self'
              328  LOAD_ATTR                ldtoldwidth
              330  LOAD_METHOD              text
              332  CALL_METHOD_0         0  '0 positional arguments'
              334  CALL_METHOD_1         1  '1 positional argument'
              336  STORE_FAST               '_image_width'

 L. 496       338  LOAD_GLOBAL              basic_data
              340  LOAD_METHOD              str2int
              342  LOAD_FAST                'self'
              344  LOAD_ATTR                ldtnewheight
              346  LOAD_METHOD              text
              348  CALL_METHOD_0         0  '0 positional arguments'
              350  CALL_METHOD_1         1  '1 positional argument'
              352  STORE_FAST               '_image_height_new'

 L. 497       354  LOAD_GLOBAL              basic_data
              356  LOAD_METHOD              str2int
              358  LOAD_FAST                'self'
              360  LOAD_ATTR                ldtnewwidth
              362  LOAD_METHOD              text
              364  CALL_METHOD_0         0  '0 positional arguments'
              366  CALL_METHOD_1         1  '1 positional argument'
              368  STORE_FAST               '_image_width_new'

 L. 498       370  LOAD_FAST                '_image_height'
              372  LOAD_CONST               False
              374  COMPARE_OP               is
          376_378  POP_JUMP_IF_TRUE    410  'to 410'
              380  LOAD_FAST                '_image_width'
              382  LOAD_CONST               False
              384  COMPARE_OP               is
          386_388  POP_JUMP_IF_TRUE    410  'to 410'

 L. 499       390  LOAD_FAST                '_image_height_new'
              392  LOAD_CONST               False
              394  COMPARE_OP               is
          396_398  POP_JUMP_IF_TRUE    410  'to 410'
              400  LOAD_FAST                '_image_width_new'
              402  LOAD_CONST               False
              404  COMPARE_OP               is
          406_408  POP_JUMP_IF_FALSE   446  'to 446'
            410_0  COME_FROM           396  '396'
            410_1  COME_FROM           386  '386'
            410_2  COME_FROM           376  '376'

 L. 500       410  LOAD_GLOBAL              vis_msg
              412  LOAD_ATTR                print
              414  LOAD_STR                 'ERROR in EvaluateMl15DWdcnn: Non-integer feature size'
              416  LOAD_STR                 'error'
              418  LOAD_CONST               ('type',)
              420  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              422  POP_TOP          

 L. 501       424  LOAD_GLOBAL              QtWidgets
              426  LOAD_ATTR                QMessageBox
              428  LOAD_METHOD              critical
              430  LOAD_FAST                'self'
              432  LOAD_ATTR                msgbox

 L. 502       434  LOAD_STR                 'Evaluate 1.5D-WDCNN'

 L. 503       436  LOAD_STR                 'Non-integer feature size'
              438  CALL_METHOD_3         3  '3 positional arguments'
              440  POP_TOP          

 L. 504       442  LOAD_CONST               None
              444  RETURN_VALUE     
            446_0  COME_FROM           406  '406'

 L. 505       446  LOAD_FAST                '_image_height'
              448  LOAD_CONST               2
              450  COMPARE_OP               <
          452_454  POP_JUMP_IF_TRUE    486  'to 486'
              456  LOAD_FAST                '_image_width'
              458  LOAD_CONST               2
              460  COMPARE_OP               <
          462_464  POP_JUMP_IF_TRUE    486  'to 486'

 L. 506       466  LOAD_FAST                '_image_height_new'
              468  LOAD_CONST               2
              470  COMPARE_OP               <
          472_474  POP_JUMP_IF_TRUE    486  'to 486'
              476  LOAD_FAST                '_image_width_new'
              478  LOAD_CONST               2
              480  COMPARE_OP               <
          482_484  POP_JUMP_IF_FALSE   522  'to 522'
            486_0  COME_FROM           472  '472'
            486_1  COME_FROM           462  '462'
            486_2  COME_FROM           452  '452'

 L. 507       486  LOAD_GLOBAL              vis_msg
              488  LOAD_ATTR                print
              490  LOAD_STR                 'ERROR in EvaluateMl15DWdcnn: Features are not 2D'
              492  LOAD_STR                 'error'
              494  LOAD_CONST               ('type',)
              496  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              498  POP_TOP          

 L. 508       500  LOAD_GLOBAL              QtWidgets
              502  LOAD_ATTR                QMessageBox
              504  LOAD_METHOD              critical
              506  LOAD_FAST                'self'
              508  LOAD_ATTR                msgbox

 L. 509       510  LOAD_STR                 'Evaluate 1.5D-WDCNN'

 L. 510       512  LOAD_STR                 'Features are not 2D'
              514  CALL_METHOD_3         3  '3 positional arguments'
              516  POP_TOP          

 L. 511       518  LOAD_CONST               None
              520  RETURN_VALUE     
            522_0  COME_FROM           482  '482'

 L. 513       522  LOAD_GLOBAL              basic_data
              524  LOAD_METHOD              str2int
              526  LOAD_FAST                'self'
              528  LOAD_ATTR                ldtbatchsize
              530  LOAD_METHOD              text
              532  CALL_METHOD_0         0  '0 positional arguments'
              534  CALL_METHOD_1         1  '1 positional argument'
              536  STORE_FAST               '_batch'

 L. 514       538  LOAD_FAST                '_batch'
              540  LOAD_CONST               False
              542  COMPARE_OP               is
          544_546  POP_JUMP_IF_TRUE    558  'to 558'
              548  LOAD_FAST                '_batch'
              550  LOAD_CONST               1
              552  COMPARE_OP               <
          554_556  POP_JUMP_IF_FALSE   594  'to 594'
            558_0  COME_FROM           544  '544'

 L. 515       558  LOAD_GLOBAL              vis_msg
              560  LOAD_ATTR                print
              562  LOAD_STR                 'ERROR in EvaluateMl15DWdcnn: Non-positive batch size'
              564  LOAD_STR                 'error'
              566  LOAD_CONST               ('type',)
              568  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              570  POP_TOP          

 L. 516       572  LOAD_GLOBAL              QtWidgets
              574  LOAD_ATTR                QMessageBox
              576  LOAD_METHOD              critical
              578  LOAD_FAST                'self'
              580  LOAD_ATTR                msgbox

 L. 517       582  LOAD_STR                 'Evaluate 1.5D-WDCNN'

 L. 518       584  LOAD_STR                 'Non-positive batch size'
              586  CALL_METHOD_3         3  '3 positional arguments'
              588  POP_TOP          

 L. 519       590  LOAD_CONST               None
              592  RETURN_VALUE     
            594_0  COME_FROM           554  '554'

 L. 521       594  LOAD_FAST                'self'
              596  LOAD_ATTR                survinfo
              598  STORE_FAST               '_seisinfo'

 L. 523       600  LOAD_CONST               0
              602  STORE_FAST               '_wdinl'

 L. 524       604  LOAD_CONST               0
              606  STORE_FAST               '_wdxl'

 L. 525       608  LOAD_CONST               0
              610  STORE_FAST               '_wdz'

 L. 526       612  LOAD_FAST                'self'
              614  LOAD_ATTR                cbbornt
              616  LOAD_METHOD              currentIndex
              618  CALL_METHOD_0         0  '0 positional arguments'
              620  LOAD_CONST               0
              622  COMPARE_OP               ==
          624_626  POP_JUMP_IF_FALSE   640  'to 640'

 L. 527       628  LOAD_GLOBAL              int
              630  LOAD_FAST                '_image_width'
              632  LOAD_CONST               2
              634  BINARY_TRUE_DIVIDE
              636  CALL_FUNCTION_1       1  '1 positional argument'
              638  STORE_FAST               '_wdxl'
            640_0  COME_FROM           624  '624'

 L. 528       640  LOAD_FAST                'self'
              642  LOAD_ATTR                cbbornt
              644  LOAD_METHOD              currentIndex
              646  CALL_METHOD_0         0  '0 positional arguments'
              648  LOAD_CONST               1
              650  COMPARE_OP               ==
          652_654  POP_JUMP_IF_FALSE   668  'to 668'

 L. 529       656  LOAD_GLOBAL              int
              658  LOAD_FAST                '_image_width'
              660  LOAD_CONST               2
              662  BINARY_TRUE_DIVIDE
              664  CALL_FUNCTION_1       1  '1 positional argument'
              666  STORE_FAST               '_wdinl'
            668_0  COME_FROM           652  '652'

 L. 530       668  LOAD_FAST                'self'
              670  LOAD_ATTR                cbbornt
              672  LOAD_METHOD              currentIndex
              674  CALL_METHOD_0         0  '0 positional arguments'
              676  LOAD_CONST               2
              678  COMPARE_OP               ==
          680_682  POP_JUMP_IF_FALSE   696  'to 696'

 L. 531       684  LOAD_GLOBAL              int
              686  LOAD_FAST                '_image_width'
              688  LOAD_CONST               2
              690  BINARY_TRUE_DIVIDE
              692  CALL_FUNCTION_1       1  '1 positional argument'
              694  STORE_FAST               '_wdinl'
            696_0  COME_FROM           680  '680'

 L. 532       696  BUILD_MAP_0           0 
              698  STORE_FAST               '_seisdict'

 L. 533       700  LOAD_FAST                'self'
              702  LOAD_ATTR                cbbornt
              704  LOAD_METHOD              currentIndex
              706  CALL_METHOD_0         0  '0 positional arguments'
              708  LOAD_CONST               0
              710  COMPARE_OP               ==
          712_714  POP_JUMP_IF_TRUE    732  'to 732'
              716  LOAD_FAST                'self'
              718  LOAD_ATTR                cbbornt
              720  LOAD_METHOD              currentIndex
              722  CALL_METHOD_0         0  '0 positional arguments'
              724  LOAD_CONST               1
              726  COMPARE_OP               ==
          728_730  POP_JUMP_IF_FALSE   978  'to 978'
            732_0  COME_FROM           712  '712'

 L. 534       732  LOAD_GLOBAL              np
              734  LOAD_METHOD              arange
              736  LOAD_CONST               0
              738  LOAD_FAST                '_seisinfo'
              740  LOAD_STR                 'ILNum'
              742  BINARY_SUBSCR    
              744  LOAD_FAST                '_seisinfo'
              746  LOAD_STR                 'XLNum'
              748  BINARY_SUBSCR    
              750  BINARY_MULTIPLY  
              752  CALL_METHOD_2         2  '2 positional arguments'
              754  STORE_FAST               '_all_sample'

 L. 535       756  LOAD_GLOBAL              np
              758  LOAD_METHOD              reshape
              760  LOAD_FAST                '_seisinfo'
              762  LOAD_STR                 'ILRange'
              764  BINARY_SUBSCR    
              766  LOAD_FAST                '_all_sample'
              768  LOAD_FAST                '_seisinfo'
              770  LOAD_STR                 'XLNum'
              772  BINARY_SUBSCR    
              774  BINARY_TRUE_DIVIDE
              776  LOAD_METHOD              astype
              778  LOAD_GLOBAL              int
              780  CALL_METHOD_1         1  '1 positional argument'
              782  BINARY_SUBSCR    

 L. 536       784  LOAD_CONST               -1
              786  LOAD_CONST               1
              788  BUILD_LIST_2          2 
              790  CALL_METHOD_2         2  '2 positional arguments'
              792  STORE_FAST               '_inls'

 L. 537       794  LOAD_GLOBAL              np
              796  LOAD_METHOD              reshape
              798  LOAD_FAST                '_seisinfo'
              800  LOAD_STR                 'XLRange'
              802  BINARY_SUBSCR    
              804  LOAD_FAST                '_all_sample'
              806  LOAD_FAST                '_seisinfo'
              808  LOAD_STR                 'XLNum'
              810  BINARY_SUBSCR    
              812  BINARY_MODULO    
              814  LOAD_METHOD              astype
              816  LOAD_GLOBAL              int
              818  CALL_METHOD_1         1  '1 positional argument'
              820  BINARY_SUBSCR    

 L. 538       822  LOAD_CONST               -1
              824  LOAD_CONST               1
              826  BUILD_LIST_2          2 
              828  CALL_METHOD_2         2  '2 positional arguments'
              830  STORE_FAST               '_xls'

 L. 539       832  LOAD_GLOBAL              seis_ays
              834  LOAD_ATTR                removeOutofSurveyZTrace
              836  LOAD_GLOBAL              np
              838  LOAD_ATTR                concatenate
              840  LOAD_FAST                '_inls'
              842  LOAD_FAST                '_xls'
              844  BUILD_TUPLE_2         2 
              846  LOAD_CONST               1
              848  LOAD_CONST               ('axis',)
              850  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 540       852  LOAD_FAST                '_seisinfo'
              854  LOAD_STR                 'ILStart'
              856  BINARY_SUBSCR    
              858  LOAD_FAST                '_wdinl'
              860  LOAD_FAST                '_seisinfo'
              862  LOAD_STR                 'ILStep'
              864  BINARY_SUBSCR    
              866  BINARY_MULTIPLY  
              868  BINARY_ADD       

 L. 541       870  LOAD_FAST                '_seisinfo'
              872  LOAD_STR                 'ILEnd'
              874  BINARY_SUBSCR    
              876  LOAD_FAST                '_wdinl'
              878  LOAD_FAST                '_seisinfo'
              880  LOAD_STR                 'ILStep'
              882  BINARY_SUBSCR    
              884  BINARY_MULTIPLY  
              886  BINARY_SUBTRACT  

 L. 542       888  LOAD_FAST                '_seisinfo'
              890  LOAD_STR                 'XLStart'
              892  BINARY_SUBSCR    
              894  LOAD_FAST                '_wdxl'
              896  LOAD_FAST                '_seisinfo'
              898  LOAD_STR                 'XLStep'
              900  BINARY_SUBSCR    
              902  BINARY_MULTIPLY  
              904  BINARY_ADD       

 L. 543       906  LOAD_FAST                '_seisinfo'
              908  LOAD_STR                 'XLEnd'
              910  BINARY_SUBSCR    
              912  LOAD_FAST                '_wdxl'
              914  LOAD_FAST                '_seisinfo'
              916  LOAD_STR                 'XLStep'
              918  BINARY_SUBSCR    
              920  BINARY_MULTIPLY  
              922  BINARY_SUBTRACT  
              924  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend')
              926  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              928  STORE_FAST               '_traces'

 L. 544       930  LOAD_FAST                '_traces'
              932  LOAD_CONST               None
              934  LOAD_CONST               None
              936  BUILD_SLICE_2         2 
              938  LOAD_CONST               0
              940  LOAD_CONST               1
              942  BUILD_SLICE_2         2 
              944  BUILD_TUPLE_2         2 
              946  BINARY_SUBSCR    
              948  LOAD_FAST                '_seisdict'
              950  LOAD_STR                 'Inline'
              952  STORE_SUBSCR     

 L. 545       954  LOAD_FAST                '_traces'
              956  LOAD_CONST               None
              958  LOAD_CONST               None
              960  BUILD_SLICE_2         2 
              962  LOAD_CONST               1
              964  LOAD_CONST               2
              966  BUILD_SLICE_2         2 
              968  BUILD_TUPLE_2         2 
              970  BINARY_SUBSCR    
              972  LOAD_FAST                '_seisdict'
              974  LOAD_STR                 'Crossline'
              976  STORE_SUBSCR     
            978_0  COME_FROM           728  '728'

 L. 546       978  LOAD_FAST                'self'
              980  LOAD_ATTR                cbbornt
              982  LOAD_METHOD              currentIndex
              984  CALL_METHOD_0         0  '0 positional arguments'
              986  LOAD_CONST               2
              988  COMPARE_OP               ==
          990_992  POP_JUMP_IF_FALSE  1240  'to 1240'

 L. 547       994  LOAD_GLOBAL              np
              996  LOAD_METHOD              arange
              998  LOAD_CONST               0
             1000  LOAD_FAST                '_seisinfo'
             1002  LOAD_STR                 'ILNum'
             1004  BINARY_SUBSCR    
             1006  LOAD_FAST                '_seisinfo'
             1008  LOAD_STR                 'ZNum'
             1010  BINARY_SUBSCR    
             1012  BINARY_MULTIPLY  
             1014  CALL_METHOD_2         2  '2 positional arguments'
             1016  STORE_FAST               '_all_sample'

 L. 548      1018  LOAD_GLOBAL              np
             1020  LOAD_METHOD              reshape
             1022  LOAD_FAST                '_seisinfo'
             1024  LOAD_STR                 'ILRange'
             1026  BINARY_SUBSCR    
             1028  LOAD_FAST                '_all_sample'
             1030  LOAD_FAST                '_seisinfo'
             1032  LOAD_STR                 'ZNum'
             1034  BINARY_SUBSCR    
             1036  BINARY_TRUE_DIVIDE
             1038  LOAD_METHOD              astype
             1040  LOAD_GLOBAL              int
             1042  CALL_METHOD_1         1  '1 positional argument'
             1044  BINARY_SUBSCR    

 L. 549      1046  LOAD_CONST               -1
             1048  LOAD_CONST               1
             1050  BUILD_LIST_2          2 
             1052  CALL_METHOD_2         2  '2 positional arguments'
             1054  STORE_FAST               '_inls'

 L. 550      1056  LOAD_GLOBAL              np
             1058  LOAD_METHOD              reshape
             1060  LOAD_FAST                '_seisinfo'
             1062  LOAD_STR                 'ZRange'
             1064  BINARY_SUBSCR    
             1066  LOAD_FAST                '_all_sample'
             1068  LOAD_FAST                '_seisinfo'
             1070  LOAD_STR                 'ZNum'
             1072  BINARY_SUBSCR    
             1074  BINARY_MODULO    
             1076  LOAD_METHOD              astype
             1078  LOAD_GLOBAL              int
             1080  CALL_METHOD_1         1  '1 positional argument'
             1082  BINARY_SUBSCR    

 L. 551      1084  LOAD_CONST               -1
             1086  LOAD_CONST               1
             1088  BUILD_LIST_2          2 
             1090  CALL_METHOD_2         2  '2 positional arguments'
             1092  STORE_FAST               '_zs'

 L. 552      1094  LOAD_GLOBAL              seis_ays
             1096  LOAD_ATTR                removeOutofSurveyXLTrace
             1098  LOAD_GLOBAL              np
             1100  LOAD_ATTR                concatenate
             1102  LOAD_FAST                '_inls'
             1104  LOAD_FAST                '_zs'
             1106  BUILD_TUPLE_2         2 
             1108  LOAD_CONST               1
             1110  LOAD_CONST               ('axis',)
             1112  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 553      1114  LOAD_FAST                '_seisinfo'
             1116  LOAD_STR                 'ILStart'
             1118  BINARY_SUBSCR    
             1120  LOAD_FAST                '_wdinl'
             1122  LOAD_FAST                '_seisinfo'
             1124  LOAD_STR                 'ILStep'
             1126  BINARY_SUBSCR    
             1128  BINARY_MULTIPLY  
             1130  BINARY_ADD       

 L. 554      1132  LOAD_FAST                '_seisinfo'
             1134  LOAD_STR                 'ILEnd'
             1136  BINARY_SUBSCR    
             1138  LOAD_FAST                '_wdinl'
             1140  LOAD_FAST                '_seisinfo'
             1142  LOAD_STR                 'ILStep'
             1144  BINARY_SUBSCR    
             1146  BINARY_MULTIPLY  
             1148  BINARY_SUBTRACT  

 L. 555      1150  LOAD_FAST                '_seisinfo'
             1152  LOAD_STR                 'ZStart'
             1154  BINARY_SUBSCR    
             1156  LOAD_FAST                '_wdz'
             1158  LOAD_FAST                '_seisinfo'
             1160  LOAD_STR                 'ZStep'
             1162  BINARY_SUBSCR    
             1164  BINARY_MULTIPLY  
             1166  BINARY_ADD       

 L. 556      1168  LOAD_FAST                '_seisinfo'
             1170  LOAD_STR                 'ZEnd'
             1172  BINARY_SUBSCR    
             1174  LOAD_FAST                '_wdz'
             1176  LOAD_FAST                '_seisinfo'
             1178  LOAD_STR                 'ZStep'
             1180  BINARY_SUBSCR    
             1182  BINARY_MULTIPLY  
             1184  BINARY_SUBTRACT  
             1186  LOAD_CONST               ('inlstart', 'inlend', 'zstart', 'zend')
             1188  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1190  STORE_FAST               '_traces'

 L. 557      1192  LOAD_FAST                '_traces'
             1194  LOAD_CONST               None
             1196  LOAD_CONST               None
             1198  BUILD_SLICE_2         2 
             1200  LOAD_CONST               0
             1202  LOAD_CONST               1
             1204  BUILD_SLICE_2         2 
             1206  BUILD_TUPLE_2         2 
             1208  BINARY_SUBSCR    
             1210  LOAD_FAST                '_seisdict'
             1212  LOAD_STR                 'Inline'
             1214  STORE_SUBSCR     

 L. 558      1216  LOAD_FAST                '_traces'
             1218  LOAD_CONST               None
             1220  LOAD_CONST               None
             1222  BUILD_SLICE_2         2 
             1224  LOAD_CONST               1
             1226  LOAD_CONST               2
             1228  BUILD_SLICE_2         2 
             1230  BUILD_TUPLE_2         2 
             1232  BINARY_SUBSCR    
             1234  LOAD_FAST                '_seisdict'
             1236  LOAD_STR                 'Z'
             1238  STORE_SUBSCR     
           1240_0  COME_FROM           990  '990'

 L. 560      1240  LOAD_GLOBAL              basic_mdt
             1242  LOAD_METHOD              maxDictConstantRow
             1244  LOAD_FAST                '_seisdict'
             1246  CALL_METHOD_1         1  '1 positional argument'
             1248  STORE_FAST               '_nsample'

 L. 562      1250  LOAD_GLOBAL              int
             1252  LOAD_GLOBAL              np
             1254  LOAD_METHOD              ceil
             1256  LOAD_FAST                '_nsample'
             1258  LOAD_FAST                '_batch'
             1260  BINARY_TRUE_DIVIDE
             1262  CALL_METHOD_1         1  '1 positional argument'
             1264  CALL_FUNCTION_1       1  '1 positional argument'
             1266  STORE_FAST               '_nloop'

 L. 565      1268  LOAD_GLOBAL              QtWidgets
             1270  LOAD_METHOD              QProgressDialog
             1272  CALL_METHOD_0         0  '0 positional arguments'
             1274  STORE_FAST               '_pgsdlg'

 L. 566      1276  LOAD_GLOBAL              QtGui
             1278  LOAD_METHOD              QIcon
             1280  CALL_METHOD_0         0  '0 positional arguments'
             1282  STORE_FAST               'icon'

 L. 567      1284  LOAD_FAST                'icon'
             1286  LOAD_METHOD              addPixmap
             1288  LOAD_GLOBAL              QtGui
             1290  LOAD_METHOD              QPixmap
             1292  LOAD_GLOBAL              os
             1294  LOAD_ATTR                path
             1296  LOAD_METHOD              join
             1298  LOAD_FAST                'self'
             1300  LOAD_ATTR                iconpath
             1302  LOAD_STR                 'icons/check.png'
             1304  CALL_METHOD_2         2  '2 positional arguments'
             1306  CALL_METHOD_1         1  '1 positional argument'

 L. 568      1308  LOAD_GLOBAL              QtGui
             1310  LOAD_ATTR                QIcon
             1312  LOAD_ATTR                Normal
             1314  LOAD_GLOBAL              QtGui
             1316  LOAD_ATTR                QIcon
             1318  LOAD_ATTR                Off
             1320  CALL_METHOD_3         3  '3 positional arguments'
             1322  POP_TOP          

 L. 569      1324  LOAD_FAST                '_pgsdlg'
             1326  LOAD_METHOD              setWindowIcon
             1328  LOAD_FAST                'icon'
             1330  CALL_METHOD_1         1  '1 positional argument'
             1332  POP_TOP          

 L. 570      1334  LOAD_FAST                '_pgsdlg'
             1336  LOAD_METHOD              setWindowTitle
             1338  LOAD_STR                 'Evaluate 1.5D-DCNN'
             1340  CALL_METHOD_1         1  '1 positional argument'
             1342  POP_TOP          

 L. 571      1344  LOAD_FAST                '_pgsdlg'
             1346  LOAD_METHOD              setCancelButton
             1348  LOAD_CONST               None
             1350  CALL_METHOD_1         1  '1 positional argument'
             1352  POP_TOP          

 L. 572      1354  LOAD_FAST                '_pgsdlg'
             1356  LOAD_METHOD              setWindowFlags
             1358  LOAD_GLOBAL              QtCore
             1360  LOAD_ATTR                Qt
             1362  LOAD_ATTR                WindowStaysOnTopHint
             1364  CALL_METHOD_1         1  '1 positional argument'
             1366  POP_TOP          

 L. 573      1368  LOAD_FAST                '_pgsdlg'
             1370  LOAD_METHOD              forceShow
             1372  CALL_METHOD_0         0  '0 positional arguments'
             1374  POP_TOP          

 L. 574      1376  LOAD_FAST                '_pgsdlg'
             1378  LOAD_METHOD              setFixedWidth
             1380  LOAD_CONST               400
             1382  CALL_METHOD_1         1  '1 positional argument'
             1384  POP_TOP          

 L. 575      1386  LOAD_FAST                '_pgsdlg'
             1388  LOAD_METHOD              setMaximum
             1390  LOAD_FAST                '_nloop'
             1392  CALL_METHOD_1         1  '1 positional argument'
             1394  POP_TOP          

 L. 577      1396  LOAD_GLOBAL              np
             1398  LOAD_METHOD              zeros
             1400  LOAD_FAST                '_nclass'
             1402  LOAD_CONST               1
             1404  BINARY_ADD       
             1406  LOAD_FAST                '_nclass'
             1408  LOAD_CONST               1
             1410  BINARY_ADD       
             1412  BUILD_LIST_2          2 
             1414  CALL_METHOD_1         1  '1 positional argument'
             1416  STORE_FAST               '_result'

 L. 578      1418  LOAD_CONST               0
             1420  STORE_FAST               'idxstart'

 L. 579  1422_1424  SETUP_LOOP         2144  'to 2144'
             1426  LOAD_GLOBAL              range
             1428  LOAD_FAST                '_nloop'
             1430  CALL_FUNCTION_1       1  '1 positional argument'
             1432  GET_ITER         
         1434_1436  FOR_ITER           2142  'to 2142'
             1438  STORE_FAST               'i'

 L. 581      1440  LOAD_GLOBAL              QtCore
             1442  LOAD_ATTR                QCoreApplication
             1444  LOAD_METHOD              instance
             1446  CALL_METHOD_0         0  '0 positional arguments'
             1448  LOAD_METHOD              processEvents
             1450  CALL_METHOD_0         0  '0 positional arguments'
             1452  POP_TOP          

 L. 583      1454  LOAD_GLOBAL              sys
             1456  LOAD_ATTR                stdout
             1458  LOAD_METHOD              write

 L. 584      1460  LOAD_STR                 '\r>>> Evaluate 1.5D-WDCNN, proceeding %.1f%% '
             1462  LOAD_GLOBAL              float
             1464  LOAD_FAST                'i'
             1466  CALL_FUNCTION_1       1  '1 positional argument'
             1468  LOAD_GLOBAL              float
             1470  LOAD_FAST                '_nloop'
             1472  CALL_FUNCTION_1       1  '1 positional argument'
             1474  BINARY_TRUE_DIVIDE
             1476  LOAD_CONST               100.0
             1478  BINARY_MULTIPLY  
             1480  BINARY_MODULO    
             1482  CALL_METHOD_1         1  '1 positional argument'
             1484  POP_TOP          

 L. 585      1486  LOAD_GLOBAL              sys
             1488  LOAD_ATTR                stdout
             1490  LOAD_METHOD              flush
             1492  CALL_METHOD_0         0  '0 positional arguments'
             1494  POP_TOP          

 L. 587      1496  LOAD_FAST                'idxstart'
             1498  LOAD_FAST                '_batch'
             1500  BINARY_ADD       
             1502  STORE_FAST               'idxend'

 L. 588      1504  LOAD_FAST                'idxend'
             1506  LOAD_FAST                '_nsample'
             1508  COMPARE_OP               >
         1510_1512  POP_JUMP_IF_FALSE  1518  'to 1518'

 L. 589      1514  LOAD_FAST                '_nsample'
             1516  STORE_FAST               'idxend'
           1518_0  COME_FROM          1510  '1510'

 L. 590      1518  LOAD_GLOBAL              np
             1520  LOAD_METHOD              linspace
             1522  LOAD_FAST                'idxstart'
             1524  LOAD_FAST                'idxend'
             1526  LOAD_CONST               1
             1528  BINARY_SUBTRACT  
             1530  LOAD_FAST                'idxend'
             1532  LOAD_FAST                'idxstart'
             1534  BINARY_SUBTRACT  
             1536  CALL_METHOD_3         3  '3 positional arguments'
             1538  LOAD_METHOD              astype
             1540  LOAD_GLOBAL              int
             1542  CALL_METHOD_1         1  '1 positional argument'
             1544  STORE_FAST               'idxlist'

 L. 591      1546  LOAD_FAST                'idxend'
             1548  STORE_FAST               'idxstart'

 L. 592      1550  LOAD_GLOBAL              basic_mdt
             1552  LOAD_METHOD              retrieveDictByIndex
             1554  LOAD_FAST                '_seisdict'
             1556  LOAD_FAST                'idxlist'
             1558  CALL_METHOD_2         2  '2 positional arguments'
             1560  STORE_FAST               '_dict'

 L. 594      1562  LOAD_FAST                '_dict'
             1564  LOAD_STR                 'Inline'
             1566  BINARY_SUBSCR    
             1568  STORE_FAST               '_targetdata'

 L. 595      1570  LOAD_FAST                'self'
             1572  LOAD_ATTR                cbbornt
             1574  LOAD_METHOD              currentIndex
             1576  CALL_METHOD_0         0  '0 positional arguments'
             1578  LOAD_CONST               0
             1580  COMPARE_OP               ==
         1582_1584  POP_JUMP_IF_TRUE   1602  'to 1602'
             1586  LOAD_FAST                'self'
             1588  LOAD_ATTR                cbbornt
             1590  LOAD_METHOD              currentIndex
             1592  CALL_METHOD_0         0  '0 positional arguments'
             1594  LOAD_CONST               1
             1596  COMPARE_OP               ==
         1598_1600  POP_JUMP_IF_FALSE  1782  'to 1782'
           1602_0  COME_FROM          1582  '1582'

 L. 596      1602  LOAD_GLOBAL              np
             1604  LOAD_ATTR                concatenate
             1606  LOAD_FAST                '_targetdata'
             1608  LOAD_FAST                '_dict'
             1610  LOAD_STR                 'Crossline'
             1612  BINARY_SUBSCR    
             1614  BUILD_TUPLE_2         2 
             1616  LOAD_CONST               1
             1618  LOAD_CONST               ('axis',)
             1620  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1622  STORE_FAST               '_targetdata'

 L. 597      1624  SETUP_LOOP         1706  'to 1706'
             1626  LOAD_FAST                '_features'
             1628  GET_ITER         
             1630  FOR_ITER           1704  'to 1704'
             1632  STORE_FAST               'f'

 L. 598      1634  LOAD_FAST                'self'
             1636  LOAD_ATTR                seisdata
             1638  LOAD_FAST                'f'
             1640  BINARY_SUBSCR    
             1642  STORE_FAST               '_data'

 L. 599      1644  LOAD_GLOBAL              seis_ays
             1646  LOAD_ATTR                retrieveSeisZTraceFrom3DMat
             1648  LOAD_FAST                '_data'
             1650  LOAD_FAST                '_targetdata'

 L. 600      1652  LOAD_FAST                'self'
             1654  LOAD_ATTR                survinfo

 L. 601      1656  LOAD_FAST                '_wdinl'
             1658  LOAD_FAST                '_wdxl'

 L. 602      1660  LOAD_CONST               False
             1662  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'verbose')
             1664  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1666  STORE_FAST               '_data'

 L. 603      1668  LOAD_FAST                '_data'
             1670  LOAD_CONST               None
             1672  LOAD_CONST               None
             1674  BUILD_SLICE_2         2 
             1676  LOAD_CONST               2
             1678  LOAD_CONST               2
             1680  LOAD_FAST                '_image_height'
             1682  LOAD_FAST                '_image_width'
             1684  BINARY_MULTIPLY  
             1686  BINARY_ADD       
             1688  BUILD_SLICE_2         2 
             1690  BUILD_TUPLE_2         2 
             1692  BINARY_SUBSCR    
             1694  LOAD_FAST                '_dict'
             1696  LOAD_FAST                'f'
             1698  STORE_SUBSCR     
         1700_1702  JUMP_BACK          1630  'to 1630'
             1704  POP_BLOCK        
           1706_0  COME_FROM_LOOP     1624  '1624'

 L. 604      1706  LOAD_FAST                '_target'
             1708  LOAD_FAST                '_features'
             1710  COMPARE_OP               not-in
         1712_1714  POP_JUMP_IF_FALSE  1782  'to 1782'

 L. 605      1716  LOAD_FAST                'self'
             1718  LOAD_ATTR                seisdata
             1720  LOAD_FAST                '_target'
             1722  BINARY_SUBSCR    
             1724  STORE_FAST               '_data'

 L. 606      1726  LOAD_GLOBAL              seis_ays
             1728  LOAD_ATTR                retrieveSeisZTraceFrom3DMat
             1730  LOAD_FAST                '_data'
             1732  LOAD_FAST                '_targetdata'

 L. 607      1734  LOAD_FAST                'self'
             1736  LOAD_ATTR                survinfo

 L. 608      1738  LOAD_CONST               0
             1740  LOAD_CONST               0

 L. 609      1742  LOAD_CONST               False
             1744  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'verbose')
             1746  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1748  STORE_FAST               '_data'

 L. 610      1750  LOAD_FAST                '_data'
             1752  LOAD_CONST               None
             1754  LOAD_CONST               None
             1756  BUILD_SLICE_2         2 
             1758  LOAD_CONST               2
             1760  LOAD_CONST               2
             1762  LOAD_FAST                '_image_height'
             1764  LOAD_FAST                '_image_width'
             1766  BINARY_MULTIPLY  
             1768  BINARY_ADD       
             1770  BUILD_SLICE_2         2 
             1772  BUILD_TUPLE_2         2 
             1774  BINARY_SUBSCR    
             1776  LOAD_FAST                '_dict'
             1778  LOAD_FAST                '_target'
             1780  STORE_SUBSCR     
           1782_0  COME_FROM          1712  '1712'
           1782_1  COME_FROM          1598  '1598'

 L. 611      1782  LOAD_FAST                'self'
             1784  LOAD_ATTR                cbbornt
             1786  LOAD_METHOD              currentIndex
             1788  CALL_METHOD_0         0  '0 positional arguments'
             1790  LOAD_CONST               2
             1792  COMPARE_OP               ==
         1794_1796  POP_JUMP_IF_FALSE  1974  'to 1974'

 L. 612      1798  LOAD_GLOBAL              np
             1800  LOAD_ATTR                concatenate
             1802  LOAD_FAST                '_targetdata'
             1804  LOAD_FAST                '_dict'
             1806  LOAD_STR                 'Z'
             1808  BINARY_SUBSCR    
             1810  BUILD_TUPLE_2         2 
             1812  LOAD_CONST               1
             1814  LOAD_CONST               ('axis',)
             1816  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1818  STORE_FAST               '_targetdata'

 L. 613      1820  SETUP_LOOP         1902  'to 1902'
             1822  LOAD_FAST                '_features'
             1824  GET_ITER         
             1826  FOR_ITER           1900  'to 1900'
             1828  STORE_FAST               'f'

 L. 614      1830  LOAD_FAST                'self'
             1832  LOAD_ATTR                seisdata
             1834  LOAD_FAST                'f'
             1836  BINARY_SUBSCR    
             1838  STORE_FAST               '_data'

 L. 615      1840  LOAD_GLOBAL              seis_ays
             1842  LOAD_ATTR                retrieveSeisXLTraceFrom3DMat
             1844  LOAD_FAST                '_data'
             1846  LOAD_FAST                '_targetdata'

 L. 616      1848  LOAD_FAST                'self'
             1850  LOAD_ATTR                survinfo

 L. 617      1852  LOAD_FAST                '_wdinl'
             1854  LOAD_FAST                '_wdz'

 L. 618      1856  LOAD_CONST               False
             1858  LOAD_CONST               ('seisinfo', 'wdinl', 'wdz', 'verbose')
             1860  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1862  STORE_FAST               '_data'

 L. 619      1864  LOAD_FAST                '_data'
             1866  LOAD_CONST               None
             1868  LOAD_CONST               None
             1870  BUILD_SLICE_2         2 
             1872  LOAD_CONST               2
             1874  LOAD_CONST               2
             1876  LOAD_FAST                '_image_height'
             1878  LOAD_FAST                '_image_width'
             1880  BINARY_MULTIPLY  
             1882  BINARY_ADD       
             1884  BUILD_SLICE_2         2 
             1886  BUILD_TUPLE_2         2 
             1888  BINARY_SUBSCR    
             1890  LOAD_FAST                '_dict'
             1892  LOAD_FAST                'f'
             1894  STORE_SUBSCR     
         1896_1898  JUMP_BACK          1826  'to 1826'
             1900  POP_BLOCK        
           1902_0  COME_FROM_LOOP     1820  '1820'

 L. 620      1902  LOAD_FAST                '_target'
             1904  LOAD_FAST                '_features'
             1906  COMPARE_OP               not-in
         1908_1910  POP_JUMP_IF_FALSE  1974  'to 1974'

 L. 621      1912  LOAD_FAST                'self'
             1914  LOAD_ATTR                seisdata
             1916  LOAD_FAST                '_target'
             1918  BINARY_SUBSCR    
             1920  STORE_FAST               '_data'

 L. 622      1922  LOAD_GLOBAL              seis_ays
             1924  LOAD_ATTR                retrieveSeisXLTraceFrom3DMat
             1926  LOAD_FAST                '_data'
             1928  LOAD_FAST                '_targetdata'

 L. 623      1930  LOAD_FAST                'self'
             1932  LOAD_ATTR                survinfo

 L. 624      1934  LOAD_CONST               0
             1936  LOAD_CONST               0

 L. 625      1938  LOAD_CONST               False
             1940  LOAD_CONST               ('seisinfo', 'wdinl', 'wdz', 'verbose')
             1942  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1944  STORE_FAST               '_data'

 L. 626      1946  LOAD_FAST                '_data'
             1948  LOAD_CONST               None
             1950  LOAD_CONST               None
             1952  BUILD_SLICE_2         2 
             1954  LOAD_CONST               2
             1956  LOAD_CONST               2
             1958  LOAD_FAST                '_image_height'
             1960  BINARY_ADD       
             1962  BUILD_SLICE_2         2 
             1964  BUILD_TUPLE_2         2 
             1966  BINARY_SUBSCR    
             1968  LOAD_FAST                '_dict'
             1970  LOAD_FAST                '_target'
             1972  STORE_SUBSCR     
           1974_0  COME_FROM          1908  '1908'
           1974_1  COME_FROM          1794  '1794'

 L. 627      1974  LOAD_FAST                '_image_height_new'
             1976  LOAD_FAST                '_image_height'
             1978  COMPARE_OP               !=
         1980_1982  POP_JUMP_IF_TRUE   1994  'to 1994'
             1984  LOAD_FAST                '_image_width_new'
             1986  LOAD_FAST                '_image_width'
             1988  COMPARE_OP               !=
         1990_1992  POP_JUMP_IF_FALSE  2038  'to 2038'
           1994_0  COME_FROM          1980  '1980'

 L. 628      1994  SETUP_LOOP         2038  'to 2038'
             1996  LOAD_FAST                '_features'
             1998  GET_ITER         
             2000  FOR_ITER           2036  'to 2036'
             2002  STORE_FAST               'f'

 L. 629      2004  LOAD_GLOBAL              basic_image
             2006  LOAD_ATTR                changeImageSize
             2008  LOAD_FAST                '_dict'
             2010  LOAD_FAST                'f'
             2012  BINARY_SUBSCR    

 L. 630      2014  LOAD_FAST                '_image_height'

 L. 631      2016  LOAD_FAST                '_image_width'

 L. 632      2018  LOAD_FAST                '_image_height_new'

 L. 633      2020  LOAD_FAST                '_image_width_new'
             2022  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2024  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2026  LOAD_FAST                '_dict'
             2028  LOAD_FAST                'f'
             2030  STORE_SUBSCR     
         2032_2034  JUMP_BACK          2000  'to 2000'
             2036  POP_BLOCK        
           2038_0  COME_FROM_LOOP     1994  '1994'
           2038_1  COME_FROM          1990  '1990'

 L. 635      2038  LOAD_FAST                '_image_height_new'
             2040  LOAD_FAST                '_image_height'
             2042  COMPARE_OP               !=
         2044_2046  POP_JUMP_IF_FALSE  2084  'to 2084'
             2048  LOAD_FAST                '_target'
             2050  LOAD_FAST                '_features'
             2052  COMPARE_OP               not-in
         2054_2056  POP_JUMP_IF_FALSE  2084  'to 2084'

 L. 636      2058  LOAD_GLOBAL              basic_curve
             2060  LOAD_ATTR                changeCurveSize
             2062  LOAD_FAST                '_dict'
             2064  LOAD_FAST                '_target'
             2066  BINARY_SUBSCR    

 L. 637      2068  LOAD_FAST                '_image_height'

 L. 638      2070  LOAD_FAST                '_image_height_new'
             2072  LOAD_STR                 'linear'
             2074  LOAD_CONST               ('length', 'length_new', 'kind')
             2076  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2078  LOAD_FAST                '_dict'
             2080  LOAD_FAST                '_target'
             2082  STORE_SUBSCR     
           2084_0  COME_FROM          2054  '2054'
           2084_1  COME_FROM          2044  '2044'

 L. 640      2084  LOAD_GLOBAL              ml_wdcnn15d
             2086  LOAD_ATTR                evaluate15DWDCNNSegmentor
             2088  LOAD_FAST                '_dict'

 L. 641      2090  LOAD_FAST                '_image_height_new'

 L. 642      2092  LOAD_FAST                '_image_width_new'

 L. 643      2094  LOAD_FAST                'self'
             2096  LOAD_ATTR                modelpath

 L. 644      2098  LOAD_FAST                'self'
             2100  LOAD_ATTR                modelname

 L. 645      2102  LOAD_FAST                '_batch'
             2104  LOAD_CONST               False
             2106  LOAD_CONST               ('imageheight', 'imagewidth', 'wdcnnpath', 'wdcnnname', 'batchsize', 'verbose')
             2108  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2110  STORE_FAST               '_confmatrix'

 L. 648      2112  LOAD_FAST                '_result'
             2114  LOAD_FAST                '_confmatrix'
             2116  LOAD_STR                 'confusion_matrix'
             2118  BINARY_SUBSCR    
             2120  BINARY_ADD       
             2122  STORE_FAST               '_result'

 L. 650      2124  LOAD_FAST                '_pgsdlg'
             2126  LOAD_METHOD              setValue
             2128  LOAD_FAST                'i'
             2130  LOAD_CONST               1
             2132  BINARY_ADD       
             2134  CALL_METHOD_1         1  '1 positional argument'
             2136  POP_TOP          
         2138_2140  JUMP_BACK          1434  'to 1434'
             2142  POP_BLOCK        
           2144_0  COME_FROM_LOOP     1422  '1422'

 L. 652      2144  LOAD_GLOBAL              print
             2146  LOAD_STR                 'Done'
             2148  CALL_FUNCTION_1       1  '1 positional argument'
             2150  POP_TOP          

 L. 654      2152  LOAD_FAST                '_result'
             2154  LOAD_CONST               0
             2156  LOAD_CONST               1
             2158  LOAD_CONST               None
             2160  BUILD_SLICE_2         2 
             2162  BUILD_TUPLE_2         2 
             2164  BINARY_SUBSCR    
             2166  LOAD_FAST                '_nloop'
             2168  BINARY_TRUE_DIVIDE
             2170  LOAD_FAST                '_result'
             2172  LOAD_CONST               0
             2174  LOAD_CONST               1
             2176  LOAD_CONST               None
             2178  BUILD_SLICE_2         2 
             2180  BUILD_TUPLE_2         2 
             2182  STORE_SUBSCR     

 L. 655      2184  LOAD_FAST                '_result'
             2186  LOAD_CONST               1
             2188  LOAD_CONST               None
             2190  BUILD_SLICE_2         2 
             2192  LOAD_CONST               0
             2194  BUILD_TUPLE_2         2 
             2196  BINARY_SUBSCR    
             2198  LOAD_FAST                '_nloop'
             2200  BINARY_TRUE_DIVIDE
             2202  LOAD_FAST                '_result'
             2204  LOAD_CONST               1
             2206  LOAD_CONST               None
             2208  BUILD_SLICE_2         2 
             2210  LOAD_CONST               0
             2212  BUILD_TUPLE_2         2 
             2214  STORE_SUBSCR     

 L. 656      2216  LOAD_GLOBAL              print
             2218  LOAD_FAST                '_result'
             2220  CALL_FUNCTION_1       1  '1 positional argument'
             2222  POP_TOP          

 L. 661      2224  LOAD_GLOBAL              QtWidgets
             2226  LOAD_METHOD              QDialog
             2228  CALL_METHOD_0         0  '0 positional arguments'
             2230  STORE_FAST               '_viewmlconfmat'

 L. 662      2232  LOAD_GLOBAL              gui_viewmlconfmat
             2234  CALL_FUNCTION_0       0  '0 positional arguments'
             2236  STORE_FAST               '_gui'

 L. 663      2238  LOAD_FAST                '_result'
             2240  LOAD_FAST                '_gui'
             2242  STORE_ATTR               confmat

 L. 664      2244  LOAD_FAST                '_gui'
             2246  LOAD_METHOD              setupGUI
             2248  LOAD_FAST                '_viewmlconfmat'
             2250  CALL_METHOD_1         1  '1 positional argument'
             2252  POP_TOP          

 L. 665      2254  LOAD_FAST                '_viewmlconfmat'
             2256  LOAD_METHOD              exec
             2258  CALL_METHOD_0         0  '0 positional arguments'
             2260  POP_TOP          

 L. 666      2262  LOAD_FAST                '_viewmlconfmat'
             2264  LOAD_METHOD              show
             2266  CALL_METHOD_0         0  '0 positional arguments'
             2268  POP_TOP          

Parse error at or near `CALL_METHOD_0' instruction at offset 2266

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
    EvaluateMl15DWdcnn = QtWidgets.QWidget()
    gui = evaluateml15dwdcnn()
    gui.setupGUI(EvaluateMl15DWdcnn)
    EvaluateMl15DWdcnn.show()
    sys.exit(app.exec_())