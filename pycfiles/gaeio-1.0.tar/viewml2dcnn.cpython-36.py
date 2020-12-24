# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\viewml2dcnn.py
# Compiled at: 2019-12-16 00:14:23
# Size of source mod 2**32: 25325 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.ml.tfmodel import tfmodel as ml_tfm
from cognitivegeo.src.gui.viewmllearnmat import viewmllearnmat as gui_viewmllearnmat
from cognitivegeo.src.gui.plotmllearncurve import plotmllearncurve as gui_plotmllearncurve
from cognitivegeo.src.gui.plotml2dcnnconvmask import plotml2dcnnconvmask as gui_plotml2dcnnconvmask
from cognitivegeo.src.vis.messager import messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class viewml2dcnn(object):
    rootpath = ''
    linestyle = core_set.Visual['Line']
    maskstyle = core_set.Visual['Image']
    fontstyle = core_set.Visual['Font']
    iconpath = os.path.dirname(__file__)
    dialog = None
    modelpath = ''
    modelname = ''
    modelinfo = None

    def setupGUI(self, ViewMl2DCnn):
        ViewMl2DCnn.setObjectName('ViewMl2DCnn')
        ViewMl2DCnn.setFixedSize(800, 470)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ViewMl2DCnn.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ViewMl2DCnn)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ViewMl2DCnn)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblattrib = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblattrib.setObjectName('lblattrib')
        self.lblattrib.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgattrib = QtWidgets.QListWidget(ViewMl2DCnn)
        self.lwgattrib.setObjectName('lwgattrib')
        self.lwgattrib.setGeometry(QtCore.QRect(110, 60, 280, 110))
        self.lwgattrib.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.lblpatchsize = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblpatchsize.setObjectName('lblpatchsize')
        self.lblpatchsize.setGeometry(QtCore.QRect(10, 180, 80, 60))
        self.lblpatchheight = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblpatchheight.setObjectName('lblpatchheight')
        self.lblpatchheight.setGeometry(QtCore.QRect(100, 180, 50, 30))
        self.ldtpatchheight = QtWidgets.QLineEdit(ViewMl2DCnn)
        self.ldtpatchheight.setObjectName('ldtpatchheight')
        self.ldtpatchheight.setGeometry(QtCore.QRect(150, 180, 40, 30))
        self.lblpatchwidth = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblpatchwidth.setObjectName('lblpatchwidth')
        self.lblpatchwidth.setGeometry(QtCore.QRect(200, 180, 50, 30))
        self.ldtpatchwidth = QtWidgets.QLineEdit(ViewMl2DCnn)
        self.ldtpatchwidth.setObjectName('ldtpatchwidth')
        self.ldtpatchwidth.setGeometry(QtCore.QRect(250, 180, 40, 30))
        self.lbllabel = QtWidgets.QLabel(ViewMl2DCnn)
        self.lbllabel.setObjectName('lbllabele')
        self.lbllabel.setGeometry(QtCore.QRect(10, 230, 100, 30))
        self.cbblabel = QtWidgets.QComboBox(ViewMl2DCnn)
        self.cbblabel.setObjectName('cbblabel')
        self.cbblabel.setGeometry(QtCore.QRect(110, 230, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.lblnconvblock = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(ViewMl2DCnn)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(ViewMl2DCnn)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 140, 180, 130))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblock.verticalHeader().hide()
        self.lblnfclayer = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblnfclayer.setObjectName('lblnfclayer')
        self.lblnfclayer.setGeometry(QtCore.QRect(610, 100, 130, 30))
        self.ldtnfclayer = QtWidgets.QLineEdit(ViewMl2DCnn)
        self.ldtnfclayer.setObjectName('ldtnfclayer')
        self.ldtnfclayer.setGeometry(QtCore.QRect(750, 100, 40, 30))
        self.twgnfclayer = QtWidgets.QTableWidget(ViewMl2DCnn)
        self.twgnfclayer.setObjectName('twgnfclayer')
        self.twgnfclayer.setGeometry(QtCore.QRect(610, 140, 180, 130))
        self.twgnfclayer.setColumnCount(2)
        self.twgnfclayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnfclayer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 280, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 280, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(ViewMl2DCnn)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 280, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 320, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(ViewMl2DCnn)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 320, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 280, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 280, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(ViewMl2DCnn)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 280, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 320, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(ViewMl2DCnn)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 320, 40, 30))
        self.lblpara = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 280, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 320, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(ViewMl2DCnn)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 320, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 320, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ViewMl2DCnn)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 320, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(ViewMl2DCnn)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 360, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(ViewMl2DCnn)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 360, 40, 30))
        self.lblfcdropout = QtWidgets.QLabel(ViewMl2DCnn)
        self.lblfcdropout.setObjectName('lblfcdropout')
        self.lblfcdropout.setGeometry(QtCore.QRect(210, 360, 130, 30))
        self.ldtfcdropout = QtWidgets.QLineEdit(ViewMl2DCnn)
        self.ldtfcdropout.setObjectName('ldtfcdropout')
        self.ldtfcdropout.setGeometry(QtCore.QRect(350, 360, 40, 30))
        self.btnviewlc = QtWidgets.QPushButton(ViewMl2DCnn)
        self.btnviewlc.setObjectName('btnviewlc')
        self.btnviewlc.setGeometry(QtCore.QRect(80, 420, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/matrix.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewlc.setIcon(icon)
        self.btnplotlc = QtWidgets.QPushButton(ViewMl2DCnn)
        self.btnplotlc.setObjectName('btnplotlc')
        self.btnplotlc.setGeometry(QtCore.QRect(320, 420, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/plotcurve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnplotlc.setIcon(icon)
        self.btnplotmask = QtWidgets.QPushButton(ViewMl2DCnn)
        self.btnplotmask.setObjectName('btnplotmask')
        self.btnplotmask.setGeometry(QtCore.QRect(560, 420, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/mask.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnplotmask.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ViewMl2DCnn)
        self.msgbox.setObjectName('msgbox')
        _center_x = ViewMl2DCnn.geometry().center().x()
        _center_y = ViewMl2DCnn.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ViewMl2DCnn)
        QtCore.QMetaObject.connectSlotsByName(ViewMl2DCnn)

    def retranslateGUI(self, ViewMl2DCnn):
        self.dialog = ViewMl2DCnn
        _translate = QtCore.QCoreApplication.translate
        ViewMl2DCnn.setWindowTitle(_translate('ViewMl2DCnn', 'View 2D-CNN'))
        self.lblfrom.setText(_translate('ViewMl2DCnn', 'Select network:'))
        self.ldtfrom.setText(_translate('ViewMl2DCnn', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ViewMl2DCnn', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblattrib.setText(_translate('ViewMl2DCnn', 'Feature channel:'))
        self.lblpatchsize.setText(_translate('ViewMl2DCnn', 'Patch size:'))
        self.lblpatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpatchheight.setText(_translate('ViewMl2DCnn', 'height='))
        self.ldtpatchheight.setText(_translate('ViewMl2DCnn', ''))
        self.ldtpatchheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtpatchheight.setEnabled(False)
        self.lblpatchwidth.setText(_translate('ViewMl2DCnn', 'width='))
        self.ldtpatchwidth.setText(_translate('ViewMl2DCnn', ''))
        self.ldtpatchwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtpatchwidth.setEnabled(False)
        self.lbllabel.setText(_translate('ViewMl2DCnn', 'Target label:'))
        self.lblnetwork.setText(_translate('ViewMl2DCnn', 'Pre-trained CNN architecture:'))
        self.lblnconvblock.setText(_translate('ViewMl2DCnn', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('ViewMl2DCnn', ''))
        self.ldtnconvblock.setEnabled(False)
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblnfclayer.setText(_translate('ViewMl2DCnn', 'No. of MLP layers:'))
        self.lblnfclayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnfclayer.setText(_translate('ViewMl2DCnn', ''))
        self.ldtnfclayer.setEnabled(False)
        self.ldtnfclayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnfclayer.textChanged.connect(self.changeLdtNfclayer)
        self.twgnfclayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblmasksize.setText(_translate('ViewMl2DCnn', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('ViewMl2DCnn', 'height='))
        self.ldtmaskheight.setText(_translate('ViewMl2DCnn', ''))
        self.ldtmaskheight.setEnabled(False)
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblmaskwidth.setText(_translate('ViewMl2DCnn', 'width='))
        self.ldtmaskwidth.setText(_translate('ViewMl2DCnn', ''))
        self.ldtmaskwidth.setEnabled(False)
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolsize.setText(_translate('ViewMl2DCnn', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('ViewMl2DCnn', 'height='))
        self.ldtpoolheight.setText(_translate('ViewMl2DCnn', ''))
        self.ldtpoolheight.setEnabled(False)
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('ViewMl2DCnn', 'width='))
        self.ldtpoolwidth.setText(_translate('ViewMl2DCnn', ''))
        self.ldtpoolwidth.setEnabled(False)
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('ViewMl2DCnn', 'Pre-training parameters:'))
        self.lblnepoch.setText(_translate('ViewMl2DCnn', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('ViewMl2DCnn', ''))
        self.ldtnepoch.setEnabled(False)
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('ViewMl2DCnn', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ViewMl2DCnn', ''))
        self.ldtbatchsize.setEnabled(False)
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('ViewMl2DCnn', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('ViewMl2DCnn', ''))
        self.ldtlearnrate.setEnabled(False)
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfcdropout.setText(_translate('ViewMl2DCnn', 'MLP dropout rate:'))
        self.lblfcdropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtfcdropout.setText(_translate('ViewMl2DCnn', ''))
        self.ldtfcdropout.setEnabled(False)
        self.ldtfcdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.btnviewlc.setText(_translate('ViewMl2DCnn', 'View Learning Matrix'))
        self.btnviewlc.clicked.connect(self.clickBtnViewLc)
        self.btnplotlc.setText(_translate('ViewMl2DCnn', 'Plot Learning Curve'))
        self.btnplotlc.setDefault(True)
        self.btnplotlc.clicked.connect(self.clickBtnPlotLc)
        self.btnplotmask.setText(_translate('ViewMl2DCnn', 'Plot Conv. Masks'))
        self.btnplotmask.clicked.connect(self.clickBtnPlotMask)

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.checkCNNModel(self.modelpath, self.modelname) is True:
            self.modelinfo = ml_tfm.getModelInfo(self.modelpath, self.modelname)
            self.lwgattrib.clear()
            _attriblist = self.modelinfo['feature_list']
            _firstattrib = None
            for f in _attriblist:
                item = QtWidgets.QListWidgetItem(self.lwgattrib)
                item.setText(f)
                self.lwgattrib.addItem(item)
                if _firstattrib is None:
                    _firstattrib = item

            self.lwgattrib.setCurrentItem(_firstattrib)
            _height = self.modelinfo['image_size'][0]
            _width = self.modelinfo['image_size'][1]
            self.ldtpatchheight.setText(str(_height))
            self.ldtpatchwidth.setText(str(_width))
            self.cbblabel.clear()
            self.cbblabel.addItem(self.modelinfo['target'])
            self.ldtnconvblock.setText(str(self.modelinfo['number_conv_block']))
            self.ldtnfclayer.setText(str(self.modelinfo['number_fc_layer']))
            self.ldtmaskheight.setText(str(self.modelinfo['patch_size'][0]))
            self.ldtmaskwidth.setText(str(self.modelinfo['patch_size'][1]))
            self.ldtpoolheight.setText(str(self.modelinfo['pool_size'][0]))
            self.ldtpoolwidth.setText(str(self.modelinfo['pool_size'][1]))
            self.ldtnepoch.setText(str(self.modelinfo['number_epoch']))
            self.ldtbatchsize.setText(str(self.modelinfo['batch_size']))
            self.ldtlearnrate.setText(str(self.modelinfo['learning_rate']))
            self.ldtfcdropout.setText(str(self.modelinfo['dropout_prob_fc_layer']))
        else:
            self.modelpath = ''
            self.modelname = ''
            self.modelinfo = None
            self.lwgattrib.clear()
            self.ldtpatchheight.setText('')
            self.ldtpatchwidth.setText('')
            self.cbblabel.clear()
            self.ldtnconvblock.setText('')
            self.ldtnfclayer.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')
            self.ldtnepoch.setText('')
            self.ldtbatchsize.setText('')
            self.ldtlearnrate.setText('')
            self.ldtfcdropout.setText('')

    def clickBtnFrom(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select CNN Network', (self.rootpath), filter='Tensorflow network files (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def changeLdtNconvblock(self):
        if ml_tfm.checkCNNModel(self.modelpath, self.modelname) is True:
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

    def changeLdtNfclayer(self):
        if ml_tfm.checkCNNModel(self.modelpath, self.modelname) is True:
            _nlayer = self.modelinfo['number_fc_layer']
            self.twgnfclayer.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnfclayer.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.modelinfo['number_fc_neuron'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnfclayer.setItem(_idx, 1, item)

        else:
            self.twgnfclayer.setRowCount(0)

    def clickBtnViewLc(self):
        self.refreshMsgBox()
        if ml_tfm.checkCNNModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in ViewMl2DCnn: No CNN network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'View 2D-CNN', 'No CNN network found')
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
        if ml_tfm.checkCNNModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in ViewMl2DCnn: No CNN network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'View 2D-CNN', 'No CNN network found')
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
        if ml_tfm.checkCNNModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in ViewMl2DCnn: No CNN network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'View 2D-CNN', 'No CNN network found')
            return
        _plotmlcnnconvmask = QtWidgets.QDialog()
        _gui = gui_plotml2dcnnconvmask()
        _gui.modelpath = self.modelpath
        _gui.modelname = self.modelname
        _gui.maskstyle = self.maskstyle
        _gui.setupGUI(_plotmlcnnconvmask)
        _plotmlcnnconvmask.exec()
        _plotmlcnnconvmask.show()

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ViewMl2DCnn = QtWidgets.QWidget()
    gui = viewml2dcnn()
    gui.setupGUI(ViewMl2DCnn)
    ViewMl2DCnn.show()
    sys.exit(app.exec_())