# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\viewml2dwcae.py
# Compiled at: 2019-12-16 00:14:22
# Size of source mod 2**32: 26031 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.plotmllearncurve as gui_plotmllearncurve
import cognitivegeo.src.gui.plotml2dwcaeconvmask as gui_plotml2dwcaeconvmask
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class viewml2dwcae(object):
    rootpath = ''
    linestyle = core_set.Visual['Line']
    maskstyle = core_set.Visual['Image']
    fontstyle = core_set.Visual['Font']
    iconpath = os.path.dirname(__file__)
    dialog = None
    modelpath = ''
    modelname = ''
    modelinfo = None

    def setupGUI(self, ViewMl2DWcae):
        ViewMl2DWcae.setObjectName('ViewMl2DWcae')
        ViewMl2DWcae.setFixedSize(810, 510)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ViewMl2DWcae.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ViewMl2DWcae)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ViewMl2DWcae)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ViewMl2DWcae)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lblpatchsize = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblpatchsize.setObjectName('lblpatchsize')
        self.lblpatchsize.setGeometry(QtCore.QRect(10, 180, 80, 60))
        self.lblpatchheight = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblpatchheight.setObjectName('lblpatchheight')
        self.lblpatchheight.setGeometry(QtCore.QRect(100, 180, 50, 30))
        self.ldtpatchheight = QtWidgets.QLineEdit(ViewMl2DWcae)
        self.ldtpatchheight.setObjectName('ldtpatchheight')
        self.ldtpatchheight.setGeometry(QtCore.QRect(150, 180, 40, 30))
        self.lblpatchwidth = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblpatchwidth.setObjectName('lblpatchwidth')
        self.lblpatchwidth.setGeometry(QtCore.QRect(200, 180, 50, 30))
        self.ldtpatchwidth = QtWidgets.QLineEdit(ViewMl2DWcae)
        self.ldtpatchwidth.setObjectName('ldtpatchwidth')
        self.ldtpatchwidth.setGeometry(QtCore.QRect(250, 180, 40, 30))
        self.lbltarget = QtWidgets.QLabel(ViewMl2DWcae)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 230, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(ViewMl2DWcae)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 230, 280, 30))
        self.lblweight = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblweight.setObjectName('lblweight')
        self.lblweight.setGeometry(QtCore.QRect(10, 280, 100, 30))
        self.cbbweight = QtWidgets.QComboBox(ViewMl2DWcae)
        self.cbbweight.setObjectName('cbbweight')
        self.cbbweight.setGeometry(QtCore.QRect(110, 280, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.lblnconvblock = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ViewMl2DWcae)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ViewMl2DWcae)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 160))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(ViewMl2DWcae)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(ViewMl2DWcae)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(ViewMl2DWcae)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 140, 180, 160))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 320, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ViewMl2DWcae)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 360, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ViewMl2DWcae)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 320, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ViewMl2DWcae)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 360, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ViewMl2DWcae)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 360, 40, 30))
        self.lblpara = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 330, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 370, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(ViewMl2DWcae)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 370, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(ViewMl2DWcae)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 370, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ViewMl2DWcae)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 370, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(ViewMl2DWcae)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 410, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(ViewMl2DWcae)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 410, 40, 30))
        self.lbldropout = QtWidgets.QLabel(ViewMl2DWcae)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 410, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(ViewMl2DWcae)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 410, 40, 30))
        self.btnviewlc = QtWidgets.QPushButton(ViewMl2DWcae)
        self.btnviewlc.setObjectName('btnviewlc')
        self.btnviewlc.setGeometry(QtCore.QRect(80, 460, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/matrix.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewlc.setIcon(icon)
        self.btnplotlc = QtWidgets.QPushButton(ViewMl2DWcae)
        self.btnplotlc.setObjectName('btnplotlc')
        self.btnplotlc.setGeometry(QtCore.QRect(320, 460, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/plotcurve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnplotlc.setIcon(icon)
        self.btnplotmask = QtWidgets.QPushButton(ViewMl2DWcae)
        self.btnplotmask.setObjectName('btnplotmask')
        self.btnplotmask.setGeometry(QtCore.QRect(560, 460, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/mask.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnplotmask.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ViewMl2DWcae)
        self.msgbox.setObjectName('msgbox')
        _center_x = ViewMl2DWcae.geometry().center().x()
        _center_y = ViewMl2DWcae.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ViewMl2DWcae)
        QtCore.QMetaObject.connectSlotsByName(ViewMl2DWcae)

    def retranslateGUI(self, ViewMl2DWcae):
        self.dialog = ViewMl2DWcae
        _translate = QtCore.QCoreApplication.translate
        ViewMl2DWcae.setWindowTitle(_translate('ViewMl2DWcae', 'View 2D-WCAE'))
        self.lblfrom.setText(_translate('ViewMl2DWcae', 'Select network:'))
        self.ldtfrom.setText(_translate('ViewMl2DWcae', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ViewMl2DWcae', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ViewMl2DWcae', 'Training features:'))
        self.lblpatchsize.setText(_translate('ViewMl2DWcae', 'Image size:'))
        self.lblpatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpatchheight.setText(_translate('ViewMl2DWcae', 'height='))
        self.ldtpatchheight.setText(_translate('ViewMl2DWcae', ''))
        self.ldtpatchheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtpatchheight.setEnabled(False)
        self.lblpatchwidth.setText(_translate('ViewMl2DWcae', 'width='))
        self.ldtpatchwidth.setText(_translate('ViewMl2DWcae', ''))
        self.ldtpatchwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtpatchwidth.setEnabled(False)
        self.lbltarget.setText(_translate('ViewMl2DWcae', 'Training target:'))
        self.lblweight.setText(_translate('ViewMl2DWcae', 'Training weight:'))
        self.lblnetwork.setText(_translate('ViewMl2DWcae', 'Pre-trained WCAE architecture:'))
        self.lblnconvblock.setText(_translate('ViewMl2DWcae', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ViewMl2DWcae', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lbln1x1layer.setText(_translate('ViewMl2DWcae', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('ViewMl2DWcae', ''))
        self.ldtn1x1layer.setEnabled(False)
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.lblmasksize.setText(_translate('ViewMl2DWcae', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ViewMl2DWcae', 'height='))
        self.ldtmaskheight.setText(_translate('ViewMl2DWcae', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ViewMl2DWcae', 'width='))
        self.ldtmaskwidth.setText(_translate('ViewMl2DWcae', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ViewMl2DWcae', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ViewMl2DWcae', 'height='))
        self.ldtpoolheight.setText(_translate('ViewMl2DWcae', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ViewMl2DWcae', 'width='))
        self.ldtpoolwidth.setText(_translate('ViewMl2DWcae', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ViewMl2DWcae', 'Pre-training parameters:'))
        self.lblnepoch.setText(_translate('ViewMl2DWcae', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('ViewMl2DWcae', ''))
        self.ldtnepoch.setEnabled(False)
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('ViewMl2DWcae', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ViewMl2DWcae', ''))
        self.ldtbatchsize.setEnabled(False)
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('ViewMl2DWcae', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('ViewMl2DWcae', ''))
        self.ldtlearnrate.setEnabled(False)
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('ViewMl2DWcae', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('ViewMl2DWcae', ''))
        self.ldtdropout.setEnabled(False)
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.btnviewlc.setText(_translate('ViewMl2DWcae', 'View Learning Matrix'))
        self.btnviewlc.clicked.connect(self.clickBtnViewLc)
        self.btnplotlc.setText(_translate('ViewMl2DWcae', 'Plot Learning Curve'))
        self.btnplotlc.setDefault(True)
        self.btnplotlc.clicked.connect(self.clickBtnPlotLc)
        self.btnplotmask.setText(_translate('ViewMl2DWcae', 'Plot Conv. Masks'))
        self.btnplotmask.clicked.connect(self.clickBtnPlotMask)

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.checkWCAEModel(self.modelpath, self.modelname) is True:
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
            self.ldtpatchheight.setText(str(_height))
            self.ldtpatchwidth.setText(str(_width))
            self.cbbtarget.clear()
            self.cbbtarget.addItem(self.modelinfo['target'])
            self.cbbweight.clear()
            self.cbbweight.addItem(self.modelinfo['weight'])
            self.ldtnconvblock.setText(str(self.modelinfo['number_conv_block']))
            self.ldtn1x1layer.setText(str(self.modelinfo['number_1x1_layer']))
            self.ldtmaskheight.setText(str(self.modelinfo['patch_size'][0]))
            self.ldtmaskwidth.setText(str(self.modelinfo['patch_size'][1]))
            self.ldtpoolheight.setText(str(self.modelinfo['pool_size'][0]))
            self.ldtpoolwidth.setText(str(self.modelinfo['pool_size'][1]))
            self.ldtnepoch.setText(str(self.modelinfo['number_epoch']))
            self.ldtbatchsize.setText(str(self.modelinfo['batch_size']))
            self.ldtlearnrate.setText(str(self.modelinfo['learning_rate']))
            self.ldtdropout.setText(str(self.modelinfo['dropout_prob']))
        else:
            self.modelpath = ''
            self.modelname = ''
            self.modelinfo = None
            self.lwgfeature.clear()
            self.ldtpatchheight.setText('')
            self.ldtpatchwidth.setText('')
            self.cbbtarget.clear()
            self.cbbweight.clear()
            self.ldtnconvblock.setText('')
            self.ldtn1x1layer.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')
            self.ldtnepoch.setText('')
            self.ldtbatchsize.setText('')
            self.ldtlearnrate.setText('')
            self.ldtdropout.setText('')

    def clickBtnFrom(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select WCAE Network', (self.rootpath), filter='Tensorflow network files (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def changeLdtNconvblock(self):
        if ml_tfm.checkWCAEModel(self.modelpath, self.modelname) is True:
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
        if ml_tfm.checkWCAEModel(self.modelpath, self.modelname) is True:
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

    def clickBtnViewLc(self):
        self.refreshMsgBox()
        if ml_tfm.checkWCAEModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in ViewMl2DWcae: No WCAE network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'View 2D-WCAE', 'No WCAE network found')
            return
        _viewmllearnmat = QtWidgets.QDialog()
        _gui = gui_viewmllearnmat()
        _gui.learnmat = self.modelinfo['learning_curve']
        _gui.linestyle = self.linestyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewmllearnmat)
        _viewmllearnmat.exec()
        _viewmllearnmat.show()

    def clickBtnPlotLc(self):
        self.refreshMsgBox()
        if ml_tfm.checkWCAEModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in ViewMl2DWcae: No WCAE network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'View 2D-WCAE', 'No WCAE network found')
            return
        _plotmllearncurve = QtWidgets.QDialog()
        _gui = gui_plotmllearncurve()
        _gui.learnmat = self.modelinfo['learning_curve']
        _gui.linestyle = self.linestyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_plotmllearncurve)
        _plotmllearncurve.exec()
        _plotmllearncurve.show()

    def clickBtnPlotMask(self):
        self.refreshMsgBox()
        if ml_tfm.checkWCAEModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in ViewMl2DWcae: No WCAE network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'View 2D-WCAE', 'No WCAE network found')
            return
        _plotmlcaeconvmask = QtWidgets.QDialog()
        _gui = gui_plotml2dwcaeconvmask()
        _gui.modelpath = self.modelpath
        _gui.modelname = self.modelname
        _gui.maskstyle = self.maskstyle
        _gui.setupGUI(_plotmlcaeconvmask)
        _plotmlcaeconvmask.exec()
        _plotmlcaeconvmask.show()

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ViewMl2DWcae = QtWidgets.QWidget()
    gui = viewml2dwcae()
    gui.setupGUI(ViewMl2DWcae)
    ViewMl2DWcae.show()
    sys.exit(app.exec_())