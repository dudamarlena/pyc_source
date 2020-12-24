# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\evaluateml2dwdcnn.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 35453 bytes
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
import cognitivegeo.src.gui.viewmlconfmat as gui_viewmlconfmat
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class evaluateml2dwdcnn(object):
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

    def setupGUI(self, EvaluateMl2DWdcnn):
        EvaluateMl2DWdcnn.setObjectName('EvaluateMl2DWdcnn')
        EvaluateMl2DWdcnn.setFixedSize(810, 500)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/check.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        EvaluateMl2DWdcnn.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(EvaluateMl2DWdcnn)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(EvaluateMl2DWdcnn)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(EvaluateMl2DWdcnn)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 180, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(EvaluateMl2DWdcnn)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 180, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 230, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 230, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(EvaluateMl2DWdcnn)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 230, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 270, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(EvaluateMl2DWdcnn)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 270, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 230, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(EvaluateMl2DWdcnn)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(EvaluateMl2DWdcnn)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lbltarget = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lbltarget.setObjectName('lbltargete')
        self.lbltarget.setGeometry(QtCore.QRect(10, 320, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(EvaluateMl2DWdcnn)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 320, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(EvaluateMl2DWdcnn)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnconvblock = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(EvaluateMl2DWdcnn)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(EvaluateMl2DWdcnn)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 210))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(EvaluateMl2DWdcnn)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(EvaluateMl2DWdcnn)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 210))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 360, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 360, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(EvaluateMl2DWdcnn)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 400, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(EvaluateMl2DWdcnn)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 400, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 360, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 360, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(EvaluateMl2DWdcnn)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 360, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 400, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(EvaluateMl2DWdcnn)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 400, 40, 30))
        self.lblpara = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 370, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(EvaluateMl2DWdcnn)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(10, 400, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(EvaluateMl2DWdcnn)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(150, 400, 40, 30))
        self.btnapply = QtWidgets.QPushButton(EvaluateMl2DWdcnn)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(320, 450, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/check.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(EvaluateMl2DWdcnn)
        self.msgbox.setObjectName('msgbox')
        _center_x = EvaluateMl2DWdcnn.geometry().center().x()
        _center_y = EvaluateMl2DWdcnn.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(EvaluateMl2DWdcnn)
        QtCore.QMetaObject.connectSlotsByName(EvaluateMl2DWdcnn)

    def retranslateGUI(self, EvaluateMl2DWdcnn):
        self.dialog = EvaluateMl2DWdcnn
        _translate = QtCore.QCoreApplication.translate
        EvaluateMl2DWdcnn.setWindowTitle(_translate('EvaluateMl2DWdcnn', 'Evaluate 2D-WDCNN'))
        self.lblfrom.setText(_translate('EvaluateMl2DWdcnn', 'Select network:'))
        self.ldtfrom.setText(_translate('EvaluateMl2DWdcnn', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('EvaluateMl2DWdcnn', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('EvaluateMl2DWdcnn', 'Training features:'))
        self.lblornt.setText(_translate('EvaluateMl2DWdcnn', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('EvaluateMl2DWdcnn', 'Training target:'))
        self.lbloldsize.setText(_translate('EvaluateMl2DWdcnn', 'Original\npatch\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('EvaluateMl2DWdcnn', 'height='))
        self.ldtoldheight.setText(_translate('EvaluateMl2DWdcnn', '0'))
        self.ldtoldheight.setEnabled(False)
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('EvaluateMl2DWdcnn', 'width='))
        self.ldtoldwidth.setText(_translate('EvaluateMl2DWdcnn', '0'))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtoldwidth.setEnabled(False)
        self.lblnewsize.setText(_translate('EvaluateMl2DWdcnn', 'Interpolated\npatch\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('EvaluateMl2DWdcnn', 'height='))
        self.ldtnewheight.setText(_translate('EvaluateMl2DWdcnn', ''))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('EvaluateMl2DWdcnn', 'width='))
        self.ldtnewwidth.setText(_translate('EvaluateMl2DWdcnn', ''))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.cbbornt.currentIndexChanged.connect(self.changeCbbOrnt)
        self.lblnetwork.setText(_translate('EvaluateMl2DWdcnn', 'Pre-trained WDCNN architecture:'))
        self.btnviewnetwork.setText(_translate('EvaluateMl2DWdcnn', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnconvblock.setText(_translate('EvaluateMl2DWdcnn', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('EvaluateMl2DWdcnn', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('EvaluateMl2DWdcnn', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('EvaluateMl2DWdcnn', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('EvaluateMl2DWdcnn', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('EvaluateMl2DWdcnn', 'height='))
        self.ldtmaskheight.setText(_translate('EvaluateMl2DWdcnn', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('EvaluateMl2DWdcnn', 'width='))
        self.ldtmaskwidth.setText(_translate('EvaluateMl2DWdcnn', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('EvaluateMl2DWdcnn', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('EvaluateMl2DWdcnn', 'height='))
        self.ldtpoolheight.setText(_translate('EvaluateMl2DWdcnn', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('EvaluateMl2DWdcnn', 'width='))
        self.ldtpoolwidth.setText(_translate('EvaluateMl2DWdcnn', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('EvaluateMl2DWdcnn', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('EvaluateMl2DWdcnn', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('EvaluateMl2DWdcnn', '5'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('EvaluateMl2DWdcnn', 'Evaluate 2D-WDCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnEvaluateMl2DWdcnn)

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

    def clickBtnEvaluateMl2DWdcnn--- This code section failed: ---

 L. 456         0  LOAD_FAST                'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 458         8  LOAD_FAST                'self'
               10  LOAD_METHOD              checkSurvInfo
               12  CALL_METHOD_0         0  '0 positional arguments'
               14  LOAD_CONST               False
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    56  'to 56'

 L. 459        20  LOAD_GLOBAL              vis_msg
               22  LOAD_ATTR                print
               24  LOAD_STR                 'ERROR in EvaluateMl2DWdcnn: No seismic survey available'
               26  LOAD_STR                 'error'
               28  LOAD_CONST               ('type',)
               30  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               32  POP_TOP          

 L. 460        34  LOAD_GLOBAL              QtWidgets
               36  LOAD_ATTR                QMessageBox
               38  LOAD_METHOD              critical
               40  LOAD_FAST                'self'
               42  LOAD_ATTR                msgbox

 L. 461        44  LOAD_STR                 'Evaluate 2D-WDCNN'

 L. 462        46  LOAD_STR                 'No seismic survey available'
               48  CALL_METHOD_3         3  '3 positional arguments'
               50  POP_TOP          

 L. 463        52  LOAD_CONST               None
               54  RETURN_VALUE     
             56_0  COME_FROM            18  '18'

 L. 465        56  LOAD_GLOBAL              ml_tfm
               58  LOAD_METHOD              checkWDCNNModel
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                modelpath
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                modelname
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  LOAD_CONST               False
               72  COMPARE_OP               is
               74  POP_JUMP_IF_FALSE   112  'to 112'

 L. 466        76  LOAD_GLOBAL              vis_msg
               78  LOAD_ATTR                print
               80  LOAD_STR                 'ERROR in EvaluateMl2DWdcnn: No pre-WDCNN network found'
               82  LOAD_STR                 'error'
               84  LOAD_CONST               ('type',)
               86  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               88  POP_TOP          

 L. 467        90  LOAD_GLOBAL              QtWidgets
               92  LOAD_ATTR                QMessageBox
               94  LOAD_METHOD              critical
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                msgbox

 L. 468       100  LOAD_STR                 'Evaluate 2D-WDCNN'

 L. 469       102  LOAD_STR                 'No pre-WDCNN network found'
              104  CALL_METHOD_3         3  '3 positional arguments'
              106  POP_TOP          

 L. 470       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            74  '74'

 L. 472       112  SETUP_LOOP          194  'to 194'
              114  LOAD_FAST                'self'
              116  LOAD_ATTR                modelinfo
              118  LOAD_STR                 'feature_list'
              120  BINARY_SUBSCR    
              122  GET_ITER         
            124_0  COME_FROM           140  '140'
              124  FOR_ITER            192  'to 192'
              126  STORE_FAST               'f'

 L. 473       128  LOAD_FAST                'self'
              130  LOAD_METHOD              checkSeisData
              132  LOAD_FAST                'f'
              134  CALL_METHOD_1         1  '1 positional argument'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_FALSE   124  'to 124'

 L. 474       142  LOAD_GLOBAL              vis_msg
              144  LOAD_ATTR                print
              146  LOAD_STR                 "ERROR in EvaluateMl2DWdcnn: Feature '%s' not found in seismic data"
              148  LOAD_FAST                'f'
              150  BINARY_MODULO    

 L. 475       152  LOAD_STR                 'error'
              154  LOAD_CONST               ('type',)
              156  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              158  POP_TOP          

 L. 476       160  LOAD_GLOBAL              QtWidgets
              162  LOAD_ATTR                QMessageBox
              164  LOAD_METHOD              critical
              166  LOAD_FAST                'self'
              168  LOAD_ATTR                msgbox

 L. 477       170  LOAD_STR                 'Evaluate 2D-WDCNN'

 L. 478       172  LOAD_STR                 "Feature '"
              174  LOAD_FAST                'f'
              176  BINARY_ADD       
              178  LOAD_STR                 "' not found in seismic data"
              180  BINARY_ADD       
              182  CALL_METHOD_3         3  '3 positional arguments'
              184  POP_TOP          

 L. 479       186  LOAD_CONST               None
              188  RETURN_VALUE     
              190  JUMP_BACK           124  'to 124'
              192  POP_BLOCK        
            194_0  COME_FROM_LOOP      112  '112'

 L. 480       194  LOAD_FAST                'self'
              196  LOAD_ATTR                modelinfo
              198  LOAD_STR                 'target'
              200  BINARY_SUBSCR    
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                seisdata
              206  LOAD_METHOD              keys
              208  CALL_METHOD_0         0  '0 positional arguments'
              210  COMPARE_OP               not-in
          212_214  POP_JUMP_IF_FALSE   276  'to 276'

 L. 481       216  LOAD_GLOBAL              vis_msg
              218  LOAD_ATTR                print
              220  LOAD_STR                 "ERROR in EvaluateMl2DWdcnn: Target key '%s' not found in seismic data"

 L. 482       222  LOAD_FAST                'self'
              224  LOAD_ATTR                modelinfo
              226  LOAD_STR                 'target'
              228  BINARY_SUBSCR    
              230  BINARY_MODULO    
              232  LOAD_STR                 'error'
              234  LOAD_CONST               ('type',)
              236  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              238  POP_TOP          

 L. 483       240  LOAD_GLOBAL              QtWidgets
              242  LOAD_ATTR                QMessageBox
              244  LOAD_METHOD              critical
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                msgbox

 L. 484       250  LOAD_STR                 'Evaluate 2D-WDCNN'

 L. 485       252  LOAD_STR                 "Target key '"
              254  LOAD_FAST                'self'
              256  LOAD_ATTR                modelinfo
              258  LOAD_STR                 'target'
              260  BINARY_SUBSCR    
              262  BINARY_ADD       
              264  LOAD_STR                 ' not found in seismic data'
              266  BINARY_ADD       
              268  CALL_METHOD_3         3  '3 positional arguments'
              270  POP_TOP          

 L. 486       272  LOAD_CONST               None
              274  RETURN_VALUE     
            276_0  COME_FROM           212  '212'

 L. 488       276  LOAD_FAST                'self'
              278  LOAD_ATTR                modelinfo
              280  LOAD_STR                 'feature_list'
              282  BINARY_SUBSCR    
              284  STORE_FAST               '_features'

 L. 489       286  LOAD_FAST                'self'
              288  LOAD_ATTR                modelinfo
              290  LOAD_STR                 'target'
              292  BINARY_SUBSCR    
              294  STORE_FAST               '_target'

 L. 490       296  LOAD_FAST                'self'
              298  LOAD_ATTR                modelinfo
              300  LOAD_STR                 'number_class'
              302  BINARY_SUBSCR    
              304  STORE_FAST               '_nclass'

 L. 492       306  LOAD_GLOBAL              basic_data
              308  LOAD_METHOD              str2int
              310  LOAD_FAST                'self'
              312  LOAD_ATTR                ldtoldheight
              314  LOAD_METHOD              text
              316  CALL_METHOD_0         0  '0 positional arguments'
              318  CALL_METHOD_1         1  '1 positional argument'
              320  STORE_FAST               '_image_height'

 L. 493       322  LOAD_GLOBAL              basic_data
              324  LOAD_METHOD              str2int
              326  LOAD_FAST                'self'
              328  LOAD_ATTR                ldtoldwidth
              330  LOAD_METHOD              text
              332  CALL_METHOD_0         0  '0 positional arguments'
              334  CALL_METHOD_1         1  '1 positional argument'
              336  STORE_FAST               '_image_width'

 L. 494       338  LOAD_GLOBAL              basic_data
              340  LOAD_METHOD              str2int
              342  LOAD_FAST                'self'
              344  LOAD_ATTR                ldtnewheight
              346  LOAD_METHOD              text
              348  CALL_METHOD_0         0  '0 positional arguments'
              350  CALL_METHOD_1         1  '1 positional argument'
              352  STORE_FAST               '_image_height_new'

 L. 495       354  LOAD_GLOBAL              basic_data
              356  LOAD_METHOD              str2int
              358  LOAD_FAST                'self'
              360  LOAD_ATTR                ldtnewwidth
              362  LOAD_METHOD              text
              364  CALL_METHOD_0         0  '0 positional arguments'
              366  CALL_METHOD_1         1  '1 positional argument'
              368  STORE_FAST               '_image_width_new'

 L. 496       370  LOAD_FAST                '_image_height'
              372  LOAD_CONST               False
              374  COMPARE_OP               is
          376_378  POP_JUMP_IF_TRUE    410  'to 410'
              380  LOAD_FAST                '_image_width'
              382  LOAD_CONST               False
              384  COMPARE_OP               is
          386_388  POP_JUMP_IF_TRUE    410  'to 410'

 L. 497       390  LOAD_FAST                '_image_height_new'
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

 L. 498       410  LOAD_GLOBAL              vis_msg
              412  LOAD_ATTR                print
              414  LOAD_STR                 'ERROR in EvaluateMl2DWdcnn: Non-integer feature size'
              416  LOAD_STR                 'error'
              418  LOAD_CONST               ('type',)
              420  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              422  POP_TOP          

 L. 499       424  LOAD_GLOBAL              QtWidgets
              426  LOAD_ATTR                QMessageBox
              428  LOAD_METHOD              critical
              430  LOAD_FAST                'self'
              432  LOAD_ATTR                msgbox

 L. 500       434  LOAD_STR                 'Evaluate 2D-WDCNN'

 L. 501       436  LOAD_STR                 'Non-integer feature size'
              438  CALL_METHOD_3         3  '3 positional arguments'
              440  POP_TOP          

 L. 502       442  LOAD_CONST               None
              444  RETURN_VALUE     
            446_0  COME_FROM           406  '406'

 L. 503       446  LOAD_FAST                '_image_height'
              448  LOAD_CONST               2
              450  COMPARE_OP               <
          452_454  POP_JUMP_IF_TRUE    486  'to 486'
              456  LOAD_FAST                '_image_width'
              458  LOAD_CONST               2
              460  COMPARE_OP               <
          462_464  POP_JUMP_IF_TRUE    486  'to 486'

 L. 504       466  LOAD_FAST                '_image_height_new'
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

 L. 505       486  LOAD_GLOBAL              vis_msg
              488  LOAD_ATTR                print
              490  LOAD_STR                 'ERROR in EvaluateMl2DWdcnn: Features are not 2D'
              492  LOAD_STR                 'error'
              494  LOAD_CONST               ('type',)
              496  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              498  POP_TOP          

 L. 506       500  LOAD_GLOBAL              QtWidgets
              502  LOAD_ATTR                QMessageBox
              504  LOAD_METHOD              critical
              506  LOAD_FAST                'self'
              508  LOAD_ATTR                msgbox

 L. 507       510  LOAD_STR                 'Evaluate 2D-WDCNN'

 L. 508       512  LOAD_STR                 'Features are not 2D'
              514  CALL_METHOD_3         3  '3 positional arguments'
              516  POP_TOP          

 L. 509       518  LOAD_CONST               None
              520  RETURN_VALUE     
            522_0  COME_FROM           482  '482'

 L. 511       522  LOAD_GLOBAL              basic_data
              524  LOAD_METHOD              str2int
              526  LOAD_FAST                'self'
              528  LOAD_ATTR                ldtbatchsize
              530  LOAD_METHOD              text
              532  CALL_METHOD_0         0  '0 positional arguments'
              534  CALL_METHOD_1         1  '1 positional argument'
              536  STORE_FAST               '_batch'

 L. 512       538  LOAD_FAST                '_batch'
              540  LOAD_CONST               False
              542  COMPARE_OP               is
          544_546  POP_JUMP_IF_TRUE    558  'to 558'
              548  LOAD_FAST                '_batch'
              550  LOAD_CONST               1
              552  COMPARE_OP               <
          554_556  POP_JUMP_IF_FALSE   594  'to 594'
            558_0  COME_FROM           544  '544'

 L. 513       558  LOAD_GLOBAL              vis_msg
              560  LOAD_ATTR                print
              562  LOAD_STR                 'ERROR in EvaluateMl2DWdcnn: Non-positive batch size'
              564  LOAD_STR                 'error'
              566  LOAD_CONST               ('type',)
              568  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              570  POP_TOP          

 L. 514       572  LOAD_GLOBAL              QtWidgets
              574  LOAD_ATTR                QMessageBox
              576  LOAD_METHOD              critical
              578  LOAD_FAST                'self'
              580  LOAD_ATTR                msgbox

 L. 515       582  LOAD_STR                 'Evaluate 2D-WDCNN'

 L. 516       584  LOAD_STR                 'Non-positive batch size'
              586  CALL_METHOD_3         3  '3 positional arguments'
              588  POP_TOP          

 L. 517       590  LOAD_CONST               None
              592  RETURN_VALUE     
            594_0  COME_FROM           554  '554'

 L. 519       594  LOAD_FAST                'self'
              596  LOAD_ATTR                survinfo
              598  STORE_FAST               '_seisinfo'

 L. 521       600  LOAD_CONST               0
              602  STORE_FAST               '_nsample'

 L. 522       604  LOAD_FAST                'self'
              606  LOAD_ATTR                cbbornt
              608  LOAD_METHOD              currentIndex
              610  CALL_METHOD_0         0  '0 positional arguments'
              612  LOAD_CONST               0
              614  COMPARE_OP               ==
          616_618  POP_JUMP_IF_FALSE   628  'to 628'

 L. 523       620  LOAD_FAST                '_seisinfo'
              622  LOAD_STR                 'ILNum'
              624  BINARY_SUBSCR    
              626  STORE_FAST               '_nsample'
            628_0  COME_FROM           616  '616'

 L. 524       628  LOAD_FAST                'self'
              630  LOAD_ATTR                cbbornt
              632  LOAD_METHOD              currentIndex
              634  CALL_METHOD_0         0  '0 positional arguments'
              636  LOAD_CONST               1
              638  COMPARE_OP               ==
          640_642  POP_JUMP_IF_FALSE   652  'to 652'

 L. 525       644  LOAD_FAST                '_seisinfo'
              646  LOAD_STR                 'XLNum'
              648  BINARY_SUBSCR    
              650  STORE_FAST               '_nsample'
            652_0  COME_FROM           640  '640'

 L. 526       652  LOAD_FAST                'self'
              654  LOAD_ATTR                cbbornt
              656  LOAD_METHOD              currentIndex
              658  CALL_METHOD_0         0  '0 positional arguments'
              660  LOAD_CONST               2
              662  COMPARE_OP               ==
          664_666  POP_JUMP_IF_FALSE   676  'to 676'

 L. 527       668  LOAD_FAST                '_seisinfo'
              670  LOAD_STR                 'ZNum'
              672  BINARY_SUBSCR    
              674  STORE_FAST               '_nsample'
            676_0  COME_FROM           664  '664'

 L. 529       676  LOAD_GLOBAL              int
              678  LOAD_GLOBAL              np
              680  LOAD_METHOD              ceil
              682  LOAD_FAST                '_nsample'
              684  LOAD_FAST                '_batch'
              686  BINARY_TRUE_DIVIDE
              688  CALL_METHOD_1         1  '1 positional argument'
              690  CALL_FUNCTION_1       1  '1 positional argument'
              692  STORE_FAST               '_nloop'

 L. 532       694  LOAD_GLOBAL              QtWidgets
              696  LOAD_METHOD              QProgressDialog
              698  CALL_METHOD_0         0  '0 positional arguments'
              700  STORE_FAST               '_pgsdlg'

 L. 533       702  LOAD_GLOBAL              QtGui
              704  LOAD_METHOD              QIcon
              706  CALL_METHOD_0         0  '0 positional arguments'
              708  STORE_FAST               'icon'

 L. 534       710  LOAD_FAST                'icon'
              712  LOAD_METHOD              addPixmap
              714  LOAD_GLOBAL              QtGui
              716  LOAD_METHOD              QPixmap
              718  LOAD_GLOBAL              os
              720  LOAD_ATTR                path
              722  LOAD_METHOD              join
              724  LOAD_FAST                'self'
              726  LOAD_ATTR                iconpath
              728  LOAD_STR                 'icons/check.png'
              730  CALL_METHOD_2         2  '2 positional arguments'
              732  CALL_METHOD_1         1  '1 positional argument'

 L. 535       734  LOAD_GLOBAL              QtGui
              736  LOAD_ATTR                QIcon
              738  LOAD_ATTR                Normal
              740  LOAD_GLOBAL              QtGui
              742  LOAD_ATTR                QIcon
              744  LOAD_ATTR                Off
              746  CALL_METHOD_3         3  '3 positional arguments'
              748  POP_TOP          

 L. 536       750  LOAD_FAST                '_pgsdlg'
              752  LOAD_METHOD              setWindowIcon
              754  LOAD_FAST                'icon'
              756  CALL_METHOD_1         1  '1 positional argument'
              758  POP_TOP          

 L. 537       760  LOAD_FAST                '_pgsdlg'
              762  LOAD_METHOD              setWindowTitle
              764  LOAD_STR                 'Evaluate 2D-DCNN'
              766  CALL_METHOD_1         1  '1 positional argument'
              768  POP_TOP          

 L. 538       770  LOAD_FAST                '_pgsdlg'
              772  LOAD_METHOD              setCancelButton
              774  LOAD_CONST               None
              776  CALL_METHOD_1         1  '1 positional argument'
              778  POP_TOP          

 L. 539       780  LOAD_FAST                '_pgsdlg'
              782  LOAD_METHOD              setWindowFlags
              784  LOAD_GLOBAL              QtCore
              786  LOAD_ATTR                Qt
              788  LOAD_ATTR                WindowStaysOnTopHint
              790  CALL_METHOD_1         1  '1 positional argument'
              792  POP_TOP          

 L. 540       794  LOAD_FAST                '_pgsdlg'
              796  LOAD_METHOD              forceShow
              798  CALL_METHOD_0         0  '0 positional arguments'
              800  POP_TOP          

 L. 541       802  LOAD_FAST                '_pgsdlg'
              804  LOAD_METHOD              setFixedWidth
              806  LOAD_CONST               400
              808  CALL_METHOD_1         1  '1 positional argument'
              810  POP_TOP          

 L. 542       812  LOAD_FAST                '_pgsdlg'
              814  LOAD_METHOD              setMaximum
              816  LOAD_FAST                '_nloop'
              818  CALL_METHOD_1         1  '1 positional argument'
              820  POP_TOP          

 L. 544       822  LOAD_GLOBAL              np
              824  LOAD_METHOD              zeros
              826  LOAD_FAST                '_nclass'
              828  LOAD_CONST               1
              830  BINARY_ADD       
              832  LOAD_FAST                '_nclass'
              834  LOAD_CONST               1
              836  BINARY_ADD       
              838  BUILD_LIST_2          2 
              840  CALL_METHOD_1         1  '1 positional argument'
              842  STORE_FAST               '_result'

 L. 545       844  LOAD_CONST               0
              846  STORE_FAST               'idxstart'

 L. 546   848_850  SETUP_LOOP         1756  'to 1756'
              852  LOAD_GLOBAL              range
              854  LOAD_FAST                '_nloop'
              856  CALL_FUNCTION_1       1  '1 positional argument'
              858  GET_ITER         
          860_862  FOR_ITER           1754  'to 1754'
              864  STORE_FAST               'i'

 L. 548       866  LOAD_GLOBAL              QtCore
              868  LOAD_ATTR                QCoreApplication
              870  LOAD_METHOD              instance
              872  CALL_METHOD_0         0  '0 positional arguments'
              874  LOAD_METHOD              processEvents
              876  CALL_METHOD_0         0  '0 positional arguments'
              878  POP_TOP          

 L. 550       880  LOAD_GLOBAL              sys
              882  LOAD_ATTR                stdout
              884  LOAD_METHOD              write

 L. 551       886  LOAD_STR                 '\r>>> Evaluate 2D-WDCNN, proceeding %.1f%% '
              888  LOAD_GLOBAL              float
              890  LOAD_FAST                'i'
              892  CALL_FUNCTION_1       1  '1 positional argument'
              894  LOAD_GLOBAL              float
              896  LOAD_FAST                '_nloop'
              898  CALL_FUNCTION_1       1  '1 positional argument'
              900  BINARY_TRUE_DIVIDE
              902  LOAD_CONST               100.0
              904  BINARY_MULTIPLY  
              906  BINARY_MODULO    
              908  CALL_METHOD_1         1  '1 positional argument'
              910  POP_TOP          

 L. 552       912  LOAD_GLOBAL              sys
              914  LOAD_ATTR                stdout
              916  LOAD_METHOD              flush
              918  CALL_METHOD_0         0  '0 positional arguments'
              920  POP_TOP          

 L. 554       922  LOAD_FAST                'idxstart'
              924  LOAD_FAST                '_batch'
              926  BINARY_ADD       
              928  STORE_FAST               'idxend'

 L. 555       930  LOAD_FAST                'idxend'
              932  LOAD_FAST                '_nsample'
              934  COMPARE_OP               >
          936_938  POP_JUMP_IF_FALSE   944  'to 944'

 L. 556       940  LOAD_FAST                '_nsample'
              942  STORE_FAST               'idxend'
            944_0  COME_FROM           936  '936'

 L. 557       944  LOAD_GLOBAL              np
              946  LOAD_METHOD              linspace
              948  LOAD_FAST                'idxstart'
              950  LOAD_FAST                'idxend'
              952  LOAD_CONST               1
              954  BINARY_SUBTRACT  
              956  LOAD_FAST                'idxend'
              958  LOAD_FAST                'idxstart'
              960  BINARY_SUBTRACT  
              962  CALL_METHOD_3         3  '3 positional arguments'
              964  LOAD_METHOD              astype
              966  LOAD_GLOBAL              int
              968  CALL_METHOD_1         1  '1 positional argument'
              970  STORE_FAST               'idxlist'

 L. 558       972  LOAD_FAST                'idxend'
              974  STORE_FAST               'idxstart'

 L. 560       976  BUILD_MAP_0           0 
              978  STORE_FAST               '_dict'

 L. 561   980_982  SETUP_LOOP         1280  'to 1280'
              984  LOAD_FAST                '_features'
              986  GET_ITER         
            988_0  COME_FROM          1202  '1202'
          988_990  FOR_ITER           1278  'to 1278'
              992  STORE_FAST               'f'

 L. 562       994  LOAD_FAST                'self'
              996  LOAD_ATTR                seisdata
              998  LOAD_FAST                'f'
             1000  BINARY_SUBSCR    
             1002  STORE_FAST               '_data'

 L. 563      1004  LOAD_GLOBAL              np
             1006  LOAD_METHOD              transpose
             1008  LOAD_FAST                '_data'
             1010  LOAD_CONST               2
             1012  LOAD_CONST               1
             1014  LOAD_CONST               0
             1016  BUILD_LIST_3          3 
             1018  CALL_METHOD_2         2  '2 positional arguments'
             1020  STORE_FAST               '_data'

 L. 564      1022  LOAD_FAST                'self'
             1024  LOAD_ATTR                cbbornt
             1026  LOAD_METHOD              currentIndex
             1028  CALL_METHOD_0         0  '0 positional arguments'
             1030  LOAD_CONST               0
             1032  COMPARE_OP               ==
         1034_1036  POP_JUMP_IF_FALSE  1106  'to 1106'

 L. 565      1038  LOAD_FAST                '_data'
             1040  LOAD_FAST                'idxlist'
             1042  LOAD_CONST               None
             1044  LOAD_CONST               None
             1046  BUILD_SLICE_2         2 
             1048  LOAD_CONST               None
             1050  LOAD_CONST               None
             1052  BUILD_SLICE_2         2 
             1054  BUILD_TUPLE_3         3 
             1056  BINARY_SUBSCR    
             1058  STORE_FAST               '_data'

 L. 566      1060  LOAD_GLOBAL              np
             1062  LOAD_METHOD              reshape
             1064  LOAD_GLOBAL              np
             1066  LOAD_METHOD              transpose
             1068  LOAD_FAST                '_data'
             1070  LOAD_CONST               0
             1072  LOAD_CONST               2
             1074  LOAD_CONST               1
             1076  BUILD_LIST_3          3 
             1078  CALL_METHOD_2         2  '2 positional arguments'

 L. 567      1080  LOAD_CONST               -1
             1082  LOAD_FAST                '_seisinfo'
             1084  LOAD_STR                 'XLNum'
             1086  BINARY_SUBSCR    
             1088  LOAD_FAST                '_seisinfo'
             1090  LOAD_STR                 'ZNum'
             1092  BINARY_SUBSCR    
             1094  BINARY_MULTIPLY  
             1096  BUILD_LIST_2          2 
             1098  CALL_METHOD_2         2  '2 positional arguments'
             1100  LOAD_FAST                '_dict'
             1102  LOAD_FAST                'f'
             1104  STORE_SUBSCR     
           1106_0  COME_FROM          1034  '1034'

 L. 568      1106  LOAD_FAST                'self'
             1108  LOAD_ATTR                cbbornt
             1110  LOAD_METHOD              currentIndex
             1112  CALL_METHOD_0         0  '0 positional arguments'
             1114  LOAD_CONST               1
             1116  COMPARE_OP               ==
         1118_1120  POP_JUMP_IF_FALSE  1190  'to 1190'

 L. 569      1122  LOAD_FAST                '_data'
             1124  LOAD_CONST               None
             1126  LOAD_CONST               None
             1128  BUILD_SLICE_2         2 
             1130  LOAD_FAST                'idxlist'
             1132  LOAD_CONST               None
             1134  LOAD_CONST               None
             1136  BUILD_SLICE_2         2 
             1138  BUILD_TUPLE_3         3 
             1140  BINARY_SUBSCR    
             1142  STORE_FAST               '_data'

 L. 570      1144  LOAD_GLOBAL              np
             1146  LOAD_METHOD              reshape
             1148  LOAD_GLOBAL              np
             1150  LOAD_METHOD              transpose
             1152  LOAD_FAST                '_data'
             1154  LOAD_CONST               1
             1156  LOAD_CONST               2
             1158  LOAD_CONST               0
             1160  BUILD_LIST_3          3 
             1162  CALL_METHOD_2         2  '2 positional arguments'

 L. 571      1164  LOAD_CONST               -1
             1166  LOAD_FAST                '_seisinfo'
             1168  LOAD_STR                 'ILNum'
             1170  BINARY_SUBSCR    
             1172  LOAD_FAST                '_seisinfo'
             1174  LOAD_STR                 'ZNum'
             1176  BINARY_SUBSCR    
             1178  BINARY_MULTIPLY  
             1180  BUILD_LIST_2          2 
             1182  CALL_METHOD_2         2  '2 positional arguments'
             1184  LOAD_FAST                '_dict'
             1186  LOAD_FAST                'f'
             1188  STORE_SUBSCR     
           1190_0  COME_FROM          1118  '1118'

 L. 572      1190  LOAD_FAST                'self'
             1192  LOAD_ATTR                cbbornt
             1194  LOAD_METHOD              currentIndex
             1196  CALL_METHOD_0         0  '0 positional arguments'
             1198  LOAD_CONST               2
             1200  COMPARE_OP               ==
         1202_1204  POP_JUMP_IF_FALSE   988  'to 988'

 L. 573      1206  LOAD_FAST                '_data'
             1208  LOAD_CONST               None
             1210  LOAD_CONST               None
             1212  BUILD_SLICE_2         2 
             1214  LOAD_CONST               None
             1216  LOAD_CONST               None
             1218  BUILD_SLICE_2         2 
             1220  LOAD_FAST                'idxlist'
             1222  BUILD_TUPLE_3         3 
             1224  BINARY_SUBSCR    
             1226  STORE_FAST               '_data'

 L. 574      1228  LOAD_GLOBAL              np
             1230  LOAD_METHOD              reshape
             1232  LOAD_GLOBAL              np
             1234  LOAD_METHOD              transpose
             1236  LOAD_FAST                '_data'
             1238  LOAD_CONST               2
             1240  LOAD_CONST               1
             1242  LOAD_CONST               0
             1244  BUILD_LIST_3          3 
             1246  CALL_METHOD_2         2  '2 positional arguments'

 L. 575      1248  LOAD_CONST               -1
             1250  LOAD_FAST                '_seisinfo'
             1252  LOAD_STR                 'ILNum'
             1254  BINARY_SUBSCR    
             1256  LOAD_FAST                '_seisinfo'
             1258  LOAD_STR                 'XLNum'
             1260  BINARY_SUBSCR    
             1262  BINARY_MULTIPLY  
             1264  BUILD_LIST_2          2 
             1266  CALL_METHOD_2         2  '2 positional arguments'
             1268  LOAD_FAST                '_dict'
             1270  LOAD_FAST                'f'
             1272  STORE_SUBSCR     
         1274_1276  JUMP_BACK           988  'to 988'
             1278  POP_BLOCK        
           1280_0  COME_FROM_LOOP      980  '980'

 L. 576      1280  LOAD_FAST                '_target'
             1282  LOAD_FAST                '_features'
             1284  COMPARE_OP               not-in
         1286_1288  POP_JUMP_IF_FALSE  1570  'to 1570'

 L. 577      1290  LOAD_FAST                'self'
             1292  LOAD_ATTR                seisdata
             1294  LOAD_FAST                '_target'
             1296  BINARY_SUBSCR    
             1298  STORE_FAST               '_data'

 L. 578      1300  LOAD_GLOBAL              np
             1302  LOAD_METHOD              transpose
             1304  LOAD_FAST                '_data'
             1306  LOAD_CONST               2
             1308  LOAD_CONST               1
             1310  LOAD_CONST               0
             1312  BUILD_LIST_3          3 
             1314  CALL_METHOD_2         2  '2 positional arguments'
             1316  STORE_FAST               '_data'

 L. 579      1318  LOAD_FAST                'self'
             1320  LOAD_ATTR                cbbornt
             1322  LOAD_METHOD              currentIndex
             1324  CALL_METHOD_0         0  '0 positional arguments'
             1326  LOAD_CONST               0
             1328  COMPARE_OP               ==
         1330_1332  POP_JUMP_IF_FALSE  1402  'to 1402'

 L. 580      1334  LOAD_FAST                '_data'
             1336  LOAD_FAST                'idxlist'
             1338  LOAD_CONST               None
             1340  LOAD_CONST               None
             1342  BUILD_SLICE_2         2 
             1344  LOAD_CONST               None
             1346  LOAD_CONST               None
             1348  BUILD_SLICE_2         2 
             1350  BUILD_TUPLE_3         3 
             1352  BINARY_SUBSCR    
             1354  STORE_FAST               '_data'

 L. 581      1356  LOAD_GLOBAL              np
             1358  LOAD_METHOD              reshape
             1360  LOAD_GLOBAL              np
             1362  LOAD_METHOD              transpose
             1364  LOAD_FAST                '_data'
             1366  LOAD_CONST               0
             1368  LOAD_CONST               2
             1370  LOAD_CONST               1
             1372  BUILD_LIST_3          3 
             1374  CALL_METHOD_2         2  '2 positional arguments'

 L. 582      1376  LOAD_CONST               -1
             1378  LOAD_FAST                '_seisinfo'
             1380  LOAD_STR                 'XLNum'
             1382  BINARY_SUBSCR    
             1384  LOAD_FAST                '_seisinfo'
             1386  LOAD_STR                 'ZNum'
             1388  BINARY_SUBSCR    
             1390  BINARY_MULTIPLY  
             1392  BUILD_LIST_2          2 
             1394  CALL_METHOD_2         2  '2 positional arguments'
             1396  LOAD_FAST                '_dict'
             1398  LOAD_FAST                '_target'
             1400  STORE_SUBSCR     
           1402_0  COME_FROM          1330  '1330'

 L. 583      1402  LOAD_FAST                'self'
             1404  LOAD_ATTR                cbbornt
             1406  LOAD_METHOD              currentIndex
             1408  CALL_METHOD_0         0  '0 positional arguments'
             1410  LOAD_CONST               1
             1412  COMPARE_OP               ==
         1414_1416  POP_JUMP_IF_FALSE  1486  'to 1486'

 L. 584      1418  LOAD_FAST                '_data'
             1420  LOAD_CONST               None
             1422  LOAD_CONST               None
             1424  BUILD_SLICE_2         2 
             1426  LOAD_FAST                'idxlist'
             1428  LOAD_CONST               None
             1430  LOAD_CONST               None
             1432  BUILD_SLICE_2         2 
             1434  BUILD_TUPLE_3         3 
             1436  BINARY_SUBSCR    
             1438  STORE_FAST               '_data'

 L. 585      1440  LOAD_GLOBAL              np
             1442  LOAD_METHOD              reshape
             1444  LOAD_GLOBAL              np
             1446  LOAD_METHOD              transpose
             1448  LOAD_FAST                '_data'
             1450  LOAD_CONST               1
             1452  LOAD_CONST               2
             1454  LOAD_CONST               0
             1456  BUILD_LIST_3          3 
             1458  CALL_METHOD_2         2  '2 positional arguments'

 L. 586      1460  LOAD_CONST               -1
             1462  LOAD_FAST                '_seisinfo'
             1464  LOAD_STR                 'ILNum'
             1466  BINARY_SUBSCR    
             1468  LOAD_FAST                '_seisinfo'
             1470  LOAD_STR                 'ZNum'
             1472  BINARY_SUBSCR    
             1474  BINARY_MULTIPLY  
             1476  BUILD_LIST_2          2 
             1478  CALL_METHOD_2         2  '2 positional arguments'
             1480  LOAD_FAST                '_dict'
             1482  LOAD_FAST                '_target'
             1484  STORE_SUBSCR     
           1486_0  COME_FROM          1414  '1414'

 L. 587      1486  LOAD_FAST                'self'
             1488  LOAD_ATTR                cbbornt
             1490  LOAD_METHOD              currentIndex
             1492  CALL_METHOD_0         0  '0 positional arguments'
             1494  LOAD_CONST               2
             1496  COMPARE_OP               ==
         1498_1500  POP_JUMP_IF_FALSE  1570  'to 1570'

 L. 588      1502  LOAD_FAST                '_data'
             1504  LOAD_CONST               None
             1506  LOAD_CONST               None
             1508  BUILD_SLICE_2         2 
             1510  LOAD_CONST               None
             1512  LOAD_CONST               None
             1514  BUILD_SLICE_2         2 
             1516  LOAD_FAST                'idxlist'
             1518  BUILD_TUPLE_3         3 
             1520  BINARY_SUBSCR    
             1522  STORE_FAST               '_data'

 L. 589      1524  LOAD_GLOBAL              np
             1526  LOAD_METHOD              reshape
             1528  LOAD_GLOBAL              np
             1530  LOAD_METHOD              transpose
             1532  LOAD_FAST                '_data'
             1534  LOAD_CONST               2
             1536  LOAD_CONST               1
             1538  LOAD_CONST               0
             1540  BUILD_LIST_3          3 
             1542  CALL_METHOD_2         2  '2 positional arguments'

 L. 590      1544  LOAD_CONST               -1
             1546  LOAD_FAST                '_seisinfo'
             1548  LOAD_STR                 'ILNum'
             1550  BINARY_SUBSCR    
             1552  LOAD_FAST                '_seisinfo'
             1554  LOAD_STR                 'XLNum'
             1556  BINARY_SUBSCR    
             1558  BINARY_MULTIPLY  
             1560  BUILD_LIST_2          2 
             1562  CALL_METHOD_2         2  '2 positional arguments'
             1564  LOAD_FAST                '_dict'
             1566  LOAD_FAST                '_target'
             1568  STORE_SUBSCR     
           1570_0  COME_FROM          1498  '1498'
           1570_1  COME_FROM          1286  '1286'

 L. 592      1570  LOAD_FAST                '_image_height_new'
             1572  LOAD_FAST                '_image_height'
             1574  COMPARE_OP               !=
         1576_1578  POP_JUMP_IF_TRUE   1590  'to 1590'
             1580  LOAD_FAST                '_image_width_new'
             1582  LOAD_FAST                '_image_width'
             1584  COMPARE_OP               !=
         1586_1588  POP_JUMP_IF_FALSE  1672  'to 1672'
           1590_0  COME_FROM          1576  '1576'

 L. 593      1590  SETUP_LOOP         1634  'to 1634'
             1592  LOAD_FAST                '_features'
             1594  GET_ITER         
             1596  FOR_ITER           1632  'to 1632'
             1598  STORE_FAST               'f'

 L. 594      1600  LOAD_GLOBAL              basic_image
             1602  LOAD_ATTR                changeImageSize
             1604  LOAD_FAST                '_dict'
             1606  LOAD_FAST                'f'
             1608  BINARY_SUBSCR    

 L. 595      1610  LOAD_FAST                '_image_height'

 L. 596      1612  LOAD_FAST                '_image_width'

 L. 597      1614  LOAD_FAST                '_image_height_new'

 L. 598      1616  LOAD_FAST                '_image_width_new'
             1618  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1620  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1622  LOAD_FAST                '_dict'
             1624  LOAD_FAST                'f'
             1626  STORE_SUBSCR     
         1628_1630  JUMP_BACK          1596  'to 1596'
             1632  POP_BLOCK        
           1634_0  COME_FROM_LOOP     1590  '1590'

 L. 600      1634  LOAD_FAST                '_target'
             1636  LOAD_FAST                '_features'
             1638  COMPARE_OP               not-in
         1640_1642  POP_JUMP_IF_FALSE  1672  'to 1672'

 L. 601      1644  LOAD_GLOBAL              basic_image
             1646  LOAD_ATTR                changeImageSize
             1648  LOAD_FAST                '_dict'
             1650  LOAD_FAST                '_target'
             1652  BINARY_SUBSCR    

 L. 602      1654  LOAD_FAST                '_image_height'

 L. 603      1656  LOAD_FAST                '_image_width'

 L. 604      1658  LOAD_FAST                '_image_height_new'

 L. 605      1660  LOAD_FAST                '_image_width_new'
             1662  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             1664  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1666  LOAD_FAST                '_dict'
             1668  LOAD_FAST                '_target'
             1670  STORE_SUBSCR     
           1672_0  COME_FROM          1640  '1640'
           1672_1  COME_FROM          1586  '1586'

 L. 607      1672  LOAD_GLOBAL              np
             1674  LOAD_METHOD              round
             1676  LOAD_FAST                '_dict'
             1678  LOAD_FAST                '_target'
             1680  BINARY_SUBSCR    
             1682  CALL_METHOD_1         1  '1 positional argument'
             1684  LOAD_METHOD              astype
             1686  LOAD_GLOBAL              int
             1688  CALL_METHOD_1         1  '1 positional argument'
             1690  LOAD_FAST                '_dict'
             1692  LOAD_FAST                '_target'
             1694  STORE_SUBSCR     

 L. 609      1696  LOAD_GLOBAL              ml_wdcnn
             1698  LOAD_ATTR                evaluateWDCNNSegmentor
             1700  LOAD_FAST                '_dict'

 L. 610      1702  LOAD_FAST                '_image_height_new'
             1704  LOAD_FAST                '_image_width_new'

 L. 611      1706  LOAD_FAST                'self'
             1708  LOAD_ATTR                modelpath

 L. 612      1710  LOAD_FAST                'self'
             1712  LOAD_ATTR                modelname

 L. 613      1714  LOAD_FAST                '_batch'
             1716  LOAD_CONST               True
             1718  LOAD_CONST               ('imageheight', 'imagewidth', 'wdcnnpath', 'wdcnnname', 'batchsize', 'verbose')
             1720  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1722  STORE_FAST               '_confmatrix'

 L. 615      1724  LOAD_FAST                '_result'
             1726  LOAD_FAST                '_confmatrix'
             1728  LOAD_STR                 'confusion_matrix'
             1730  BINARY_SUBSCR    
             1732  BINARY_ADD       
             1734  STORE_FAST               '_result'

 L. 617      1736  LOAD_FAST                '_pgsdlg'
             1738  LOAD_METHOD              setValue
             1740  LOAD_FAST                'i'
             1742  LOAD_CONST               1
             1744  BINARY_ADD       
             1746  CALL_METHOD_1         1  '1 positional argument'
             1748  POP_TOP          
         1750_1752  JUMP_BACK           860  'to 860'
             1754  POP_BLOCK        
           1756_0  COME_FROM_LOOP      848  '848'

 L. 619      1756  LOAD_GLOBAL              print
             1758  LOAD_STR                 'Done'
             1760  CALL_FUNCTION_1       1  '1 positional argument'
             1762  POP_TOP          

 L. 621      1764  LOAD_FAST                '_result'
             1766  LOAD_CONST               0
             1768  LOAD_CONST               1
             1770  LOAD_CONST               None
             1772  BUILD_SLICE_2         2 
             1774  BUILD_TUPLE_2         2 
             1776  BINARY_SUBSCR    
             1778  LOAD_FAST                '_nloop'
             1780  BINARY_TRUE_DIVIDE
             1782  LOAD_FAST                '_result'
             1784  LOAD_CONST               0
             1786  LOAD_CONST               1
             1788  LOAD_CONST               None
             1790  BUILD_SLICE_2         2 
             1792  BUILD_TUPLE_2         2 
             1794  STORE_SUBSCR     

 L. 622      1796  LOAD_FAST                '_result'
             1798  LOAD_CONST               1
             1800  LOAD_CONST               None
             1802  BUILD_SLICE_2         2 
             1804  LOAD_CONST               0
             1806  BUILD_TUPLE_2         2 
             1808  BINARY_SUBSCR    
             1810  LOAD_FAST                '_nloop'
             1812  BINARY_TRUE_DIVIDE
             1814  LOAD_FAST                '_result'
             1816  LOAD_CONST               1
             1818  LOAD_CONST               None
             1820  BUILD_SLICE_2         2 
             1822  LOAD_CONST               0
             1824  BUILD_TUPLE_2         2 
             1826  STORE_SUBSCR     

 L. 623      1828  LOAD_GLOBAL              print
             1830  LOAD_FAST                '_result'
             1832  CALL_FUNCTION_1       1  '1 positional argument'
             1834  POP_TOP          

 L. 628      1836  LOAD_GLOBAL              QtWidgets
             1838  LOAD_METHOD              QDialog
             1840  CALL_METHOD_0         0  '0 positional arguments'
             1842  STORE_FAST               '_viewmlconfmat'

 L. 629      1844  LOAD_GLOBAL              gui_viewmlconfmat
             1846  CALL_FUNCTION_0       0  '0 positional arguments'
             1848  STORE_FAST               '_gui'

 L. 630      1850  LOAD_FAST                '_result'
             1852  LOAD_FAST                '_gui'
             1854  STORE_ATTR               confmat

 L. 631      1856  LOAD_FAST                '_gui'
             1858  LOAD_METHOD              setupGUI
             1860  LOAD_FAST                '_viewmlconfmat'
             1862  CALL_METHOD_1         1  '1 positional argument'
             1864  POP_TOP          

 L. 632      1866  LOAD_FAST                '_viewmlconfmat'
             1868  LOAD_METHOD              exec
             1870  CALL_METHOD_0         0  '0 positional arguments'
             1872  POP_TOP          

 L. 633      1874  LOAD_FAST                '_viewmlconfmat'
             1876  LOAD_METHOD              show
             1878  CALL_METHOD_0         0  '0 positional arguments'
             1880  POP_TOP          

Parse error at or near `CALL_METHOD_0' instruction at offset 1878

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
    EvaluateMl2DWdcnn = QtWidgets.QWidget()
    gui = evaluateml2dwdcnn()
    gui.setupGUI(EvaluateMl2DWdcnn)
    EvaluateMl2DWdcnn.show()
    sys.exit(app.exec_())