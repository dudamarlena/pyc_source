# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml2dwcaefromexisting.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 57081 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.pointset.analysis as point_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.image as basic_image
import cognitivegeo.src.ml.augmentation as ml_aug
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.wcaereconstructor as ml_wcae
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml2dwcaefromexisting(object):
    survinfo = {}
    seisdata = {}
    pointsetdata = {}
    rootpath = ''
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    iconpath = os.path.dirname(__file__)
    dialog = None
    featurelist = list()
    traindataconfig = {}
    traindataconfig['TrainPointSet'] = []
    traindataconfig['RotateFeature_Enabled'] = True
    traindataconfig['RotateFeature_Checked'] = False
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False
    traindataconfig['RemoveZeroWeight_Enabled'] = True
    traindataconfig['RemoveZeroWeight_Checked'] = False

    def setupGUI(self, TrainMl2DWcaeFromExisting):
        TrainMl2DWcaeFromExisting.setObjectName('TrainMl2DWcaeFromExisting')
        TrainMl2DWcaeFromExisting.setFixedSize(800, 630)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl2DWcaeFromExisting.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl2DWcaeFromExisting)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl2DWcaeFromExisting)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl2DWcaeFromExisting)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblweight = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblweight.setObjectName('lblweight')
        self.lblweight.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.cbbweight = QtWidgets.QComboBox(TrainMl2DWcaeFromExisting)
        self.cbbweight.setObjectName('cbbweight')
        self.cbbweight.setGeometry(QtCore.QRect(110, 310, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblexisting = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblexisting.setObjectName('lblexisting')
        self.lblexisting.setGeometry(QtCore.QRect(410, 50, 100, 30))
        self.ldtexisting = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtexisting.setObjectName('ldtexisting')
        self.ldtexisting.setGeometry(QtCore.QRect(510, 50, 210, 30))
        self.btnexisting = QtWidgets.QPushButton(TrainMl2DWcaeFromExisting)
        self.btnexisting.setObjectName('btnexisting')
        self.btnexisting.setGeometry(QtCore.QRect(730, 50, 60, 30))
        self.lblnconvblockexisting = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblnconvblockexisting.setObjectName('lblnconvblockexisting')
        self.lblnconvblockexisting.setGeometry(QtCore.QRect(410, 90, 130, 30))
        self.ldtnconvblockexisting = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtnconvblockexisting.setObjectName('ldtnconvblockexisting')
        self.ldtnconvblockexisting.setGeometry(QtCore.QRect(550, 90, 40, 30))
        self.twgnconvblockexisting = QtWidgets.QTableWidget(TrainMl2DWcaeFromExisting)
        self.twgnconvblockexisting.setObjectName('twgnconvblockexisting')
        self.twgnconvblockexisting.setGeometry(QtCore.QRect(610, 90, 180, 150))
        self.twgnconvblockexisting.setColumnCount(3)
        self.twgnconvblockexisting.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblockexisting.verticalHeader().hide()
        self.lblblockid = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblblockid.setObjectName('lblblockid')
        self.lblblockid.setGeometry(QtCore.QRect(410, 130, 130, 30))
        self.cbbblockid = QtWidgets.QComboBox(TrainMl2DWcaeFromExisting)
        self.cbbblockid.setObjectName('cbbblockid')
        self.cbbblockid.setGeometry(QtCore.QRect(550, 130, 40, 30))
        self.lbllayerid = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lbllayerid.setObjectName('lbllayerid')
        self.lbllayerid.setGeometry(QtCore.QRect(410, 170, 130, 30))
        self.cbblayerid = QtWidgets.QComboBox(TrainMl2DWcaeFromExisting)
        self.cbblayerid.setObjectName('cbblayerid')
        self.cbblayerid.setGeometry(QtCore.QRect(550, 170, 40, 30))
        self.lbltrainable = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lbltrainable.setObjectName('lbltrainable')
        self.lbltrainable.setGeometry(QtCore.QRect(410, 210, 130, 30))
        self.cbbtrainable = QtWidgets.QComboBox(TrainMl2DWcaeFromExisting)
        self.cbbtrainable.setObjectName('cbbtrainable')
        self.cbbtrainable.setGeometry(QtCore.QRect(550, 210, 40, 30))
        self.lblappend = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblappend.setObjectName('lblappend')
        self.lblappend.setGeometry(QtCore.QRect(410, 250, 200, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 290, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 290, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl2DWcaeFromExisting)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 330, 180, 200))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 290, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 290, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(TrainMl2DWcaeFromExisting)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 330, 180, 200))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 540, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 540, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 540, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 580, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 580, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 540, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 540, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 540, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 580, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 580, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl2DWcaeFromExisting)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 360, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 360, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 400, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 400, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 400, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 400, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 440, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 440, 40, 30))
        self.lbldropout = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 440, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 440, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl2DWcaeFromExisting)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 490, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl2DWcaeFromExisting)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 490, 180, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl2DWcaeFromExisting)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 490, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl2DWcaeFromExisting)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(120, 580, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl2DWcaeFromExisting)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl2DWcaeFromExisting.geometry().center().x()
        _center_y = TrainMl2DWcaeFromExisting.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl2DWcaeFromExisting)
        QtCore.QMetaObject.connectSlotsByName(TrainMl2DWcaeFromExisting)

    def retranslateGUI(self, TrainMl2DWcaeFromExisting):
        self.dialog = TrainMl2DWcaeFromExisting
        _translate = QtCore.QCoreApplication.translate
        TrainMl2DWcaeFromExisting.setWindowTitle(_translate('TrainMl2DWcaeFromExisting', 'Train 2D-WCAE from pre-trained'))
        self.lblfeature.setText(_translate('TrainMl2DWcaeFromExisting', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl2DWcaeFromExisting', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl2DWcaeFromExisting', 'Select target:'))
        self.lblweight.setText(_translate('TrainMl2DWcaeFromExisting', 'Select weight:'))
        self.btnconfigtraindata.setText(_translate('TrainMl2DDcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('TrainMl2DWcaeFromExisting', 'Original\nimage\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl2DWcaeFromExisting', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl2DWcaeFromExisting', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl2DWcaeFromExisting', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl2DWcaeFromExisting', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl2DWcaeFromExisting', 'Interpolated\nimage\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl2DWcaeFromExisting', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl2DWcaeFromExisting', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl2DWcaeFromExisting', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl2DWcaeFromExisting', '32'))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        if self.checkSurvInfo():
            self.featurelist.clear()
            self.lwgfeature.clear()
            self.cbbtarget.clear()
            self.cbbweight.clear()
            _firstfeature = None
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    self.featurelist.append(i)
                    item = QtWidgets.QListWidgetItem(self.lwgfeature)
                    item.setText(_translate('TrainMl2DWcaeFromExisting', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
            self.cbbweight.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl2DWcaeFromExisting', 'Specify CAE architecture:'))
        self.lblexisting.setText(_translate('TrainMl2DWcaeFromExisting', 'Select pre-trained:'))
        self.ldtexisting.setText(_translate('TrainMl2DWcaeFromExisting', ''))
        self.ldtexisting.textChanged.connect(self.changeLdtExisting)
        self.btnexisting.setText(_translate('TrainMl2DWcaeFromExisting', 'Browse'))
        self.btnexisting.clicked.connect(self.clickBtnExisting)
        self.lblnconvblockexisting.setText(_translate('TrainMl2DWcaeFromExisting', 'Available conv. blocks:'))
        self.lblnconvblockexisting.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblockexisting.setText(_translate('TrainMl2DWcaeFromExisting', ''))
        self.ldtnconvblockexisting.setEnabled(False)
        self.ldtnconvblockexisting.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblockexisting.textChanged.connect(self.changeLdtNconvblockExisting)
        self.twgnconvblockexisting.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblblockid.setText(_translate('TrainMl2DWcaeFromExisting', 'Select conv. block ID:'))
        self.lblblockid.setAlignment(QtCore.Qt.AlignRight)
        self.cbbblockid.currentIndexChanged.connect(self.changeCbbBlockid)
        self.lbllayerid.setText(_translate('TrainMl2DWcaeFromExisting', 'Select conv. layer ID:'))
        self.lbllayerid.setAlignment(QtCore.Qt.AlignRight)
        self.lbltrainable.setText(_translate('TrainMl2DWcaeFromExisting', 'Is trainable?:'))
        self.lbltrainable.setAlignment(QtCore.Qt.AlignRight)
        self.cbbtrainable.addItems(['Yes', 'No'])
        self.lblappend.setText(_translate('TrainMl2DWcaeFromExisting', 'Append more blocks & layers:'))
        self.lblnconvblock.setText(_translate('TrainMl2DWcaeFromExisting', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl2DWcaeFromExisting', '2'))
        self.ldtnconvblock.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblock.textChanged.connect(self.changeLdtNconvblock)
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.twgnconvblock.setRowCount(2)
        for _idx in range(int(self.ldtnconvblock.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(_idx + 1))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgnconvblock.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(2))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgnconvblock.setItem(_idx, 1, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(int(np.power(2, _idx) * 32)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgnconvblock.setItem(_idx, 2, item)

        self.lbln1x1layer.setText(_translate('TrainMl2DWcaeFromExisting', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('TrainMl2DWcaeFromExisting', '2'))
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.twgn1x1layer.setRowCount(2)
        for _idx in range(int(self.ldtn1x1layer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl2DWcaeFromExisting', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgn1x1layer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgn1x1layer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl2DWcaeFromExisting', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl2DWcaeFromExisting', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl2DWcaeFromExisting', ''))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskheight.setEnabled(False)
        self.lblmaskwidth.setText(_translate('TrainMl2DWcaeFromExisting', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl2DWcaeFromExisting', ''))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskwidth.setEnabled(False)
        self.lblpoolsize.setText(_translate('TrainMl2DWcaeFromExisting', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl2DWcaeFromExisting', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl2DWcaeFromExisting', ''))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl2DWcaeFromExisting', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl2DWcaeFromExisting', ''))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('TrainMl2DWcaeFromExisting', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl2DWcaeFromExisting', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl2DWcaeFromExisting', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl2DWcaeFromExisting', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl2DWcaeFromExisting', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl2DWcaeFromExisting', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl2DWcaeFromExisting', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('TrainMl2DWcaeFromExisting', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('TrainMl2DWcaeFromExisting', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl2DWcaeFromExisting', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl2DWcaeFromExisting', ''))
        self.btnsave.setText(_translate('TrainMl2DWcaeFromExisting', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl2DWcaeFromExisting', 'Train 2D-CAE'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl2DWcaeFromExisting)

    def changeLdtExisting(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtexisting.text()):
            _modelpath = os.path.dirname(self.ldtexisting.text())
            _modelname = os.path.splitext(os.path.basename(self.ldtexisting.text()))[0]
        else:
            _modelpath = ''
            _modelname = ''
        if ml_tfm.isConvModel(_modelpath, _modelname) is True:
            _modelinfo = ml_tfm.getModelInfo(_modelpath, _modelname)
            self.ldtnconvblockexisting.setText(str(_modelinfo['number_conv_block']))
            self.ldtmaskheight.setText(str(_modelinfo['patch_size'][0]))
            self.ldtmaskwidth.setText(str(_modelinfo['patch_size'][1]))
            self.ldtpoolheight.setText(str(_modelinfo['pool_size'][0]))
            self.ldtpoolwidth.setText(str(_modelinfo['pool_size'][1]))
        else:
            self.ldtnconvblockexisting.setText('')
            self.ldtmaskheight.setText('')
            self.ldtmaskwidth.setText('')
            self.ldtpoolheight.setText('')
            self.ldtpoolwidth.setText('')

    def clickBtnExisting(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select pre-trained Network', (self.rootpath), filter='Tensorflow network files (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtexisting.setText(_file[0])

    def changeLdtNconvblockExisting(self):
        if os.path.exists(self.ldtexisting.text()):
            _modelpath = os.path.dirname(self.ldtexisting.text())
            _modelname = os.path.splitext(os.path.basename(self.ldtexisting.text()))[0]
        else:
            _modelpath = ''
            _modelname = ''
        if ml_tfm.isConvModel(_modelpath, _modelname) is True:
            _modelinfo = ml_tfm.getModelInfo(_modelpath, _modelname)
            _nlayer = _modelinfo['number_conv_block']
            self.twgnconvblockexisting.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblockexisting.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_modelinfo['number_conv_layer'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblockexisting.setItem(_idx, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_modelinfo['number_conv_feature'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblockexisting.setItem(_idx, 2, item)

            self.cbbblockid.clear()
            self.cbbblockid.addItems([str(_i + 1) for _i in range(_nlayer)])
        else:
            self.twgnconvblockexisting.setRowCount(0)
            self.cbbblockid.clear()

    def changeCbbBlockid(self):
        if os.path.exists(self.ldtexisting.text()):
            _modelpath = os.path.dirname(self.ldtexisting.text())
            _modelname = os.path.splitext(os.path.basename(self.ldtexisting.text()))[0]
        else:
            _modelpath = ''
            _modelname = ''
        if ml_tfm.isConvModel(_modelpath, _modelname) is True:
            _modelinfo = ml_tfm.getModelInfo(_modelpath, _modelname)
            _blockid = self.cbbblockid.currentIndex()
            self.cbblayerid.clear()
            self.cbblayerid.addItems([str(_i + 1) for _i in range(_modelinfo['number_conv_layer'][_blockid])])
        else:
            self.cbblayerid.clear()

    def changeLdtNconvblock(self):
        if len(self.ldtnconvblock.text()) > 0:
            _nlayer = int(self.ldtnconvblock.text())
            self.twgnconvblock.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnconvblock.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(2))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgnconvblock.setItem(_idx, 1, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(int(np.power(2, _idx) * 32)))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgnconvblock.setItem(_idx, 2, item)

        else:
            self.twgnconvblock.setRowCount(0)

    def changeLdtN1x1layer(self):
        if len(self.ldtn1x1layer.text()) > 0:
            _nlayer = int(self.ldtn1x1layer.text())
            self.twgn1x1layer.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgn1x1layer.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(1024))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.twgn1x1layer.setItem(_idx, 1, item)

        else:
            self.twgn1x1layer.setRowCount(0)

    def clickBtnSave(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Save CAE Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtsave.setText(_file[0])

    def clickBtnConfigTrainData(self):
        _configtraindata = QtWidgets.QDialog()
        _gui = gui_configmltraindata()
        _gui.mltraindataconfig = self.traindataconfig
        _gui.pointsetlist = sorted(self.pointsetdata.keys())
        _gui.setupGUI(_configtraindata)
        _configtraindata.exec()
        self.traindataconfig = _gui.mltraindataconfig
        _configtraindata.show()

    def clickBtnTrainMl2DWcaeFromExisting--- This code section failed: ---

 L. 608         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 610         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 611        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('tyep',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 612        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 613        50  LOAD_STR                 'Train 2D-WCAE'

 L. 614        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 615        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 617        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_image_height'

 L. 618        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_image_width'

 L. 619        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtnewheight
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_image_height_new'

 L. 620       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewwidth
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_image_width_new'

 L. 621       126  LOAD_FAST                '_image_height'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'
              134  LOAD_FAST                '_image_width'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_TRUE    158  'to 158'

 L. 622       142  LOAD_FAST                '_image_height_new'
              144  LOAD_CONST               False
              146  COMPARE_OP               is
              148  POP_JUMP_IF_TRUE    158  'to 158'
              150  LOAD_FAST                '_image_width_new'
              152  LOAD_CONST               False
              154  COMPARE_OP               is
              156  POP_JUMP_IF_FALSE   194  'to 194'
            158_0  COME_FROM           148  '148'
            158_1  COME_FROM           140  '140'
            158_2  COME_FROM           132  '132'

 L. 623       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 624       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 625       182  LOAD_STR                 'Train 2D-WCAE'

 L. 626       184  LOAD_STR                 'Non-integer feature size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 627       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 628       194  LOAD_FAST                '_image_height'
              196  LOAD_CONST               2
              198  COMPARE_OP               <
              200  POP_JUMP_IF_TRUE    228  'to 228'
              202  LOAD_FAST                '_image_width'
              204  LOAD_CONST               2
              206  COMPARE_OP               <
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 629       210  LOAD_FAST                '_image_height_new'
              212  LOAD_CONST               2
              214  COMPARE_OP               <
              216  POP_JUMP_IF_TRUE    228  'to 228'
              218  LOAD_FAST                '_image_width_new'
              220  LOAD_CONST               2
              222  COMPARE_OP               <
          224_226  POP_JUMP_IF_FALSE   264  'to 264'
            228_0  COME_FROM           216  '216'
            228_1  COME_FROM           208  '208'
            228_2  COME_FROM           200  '200'

 L. 630       228  LOAD_GLOBAL              vis_msg
              230  LOAD_ATTR                print
              232  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 631       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 632       252  LOAD_STR                 'Train 2D-WCAE'

 L. 633       254  LOAD_STR                 'Features are not 2D'
              256  CALL_METHOD_3         3  '3 positional arguments'
              258  POP_TOP          

 L. 634       260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           224  '224'

 L. 636       264  LOAD_CONST               2
              266  LOAD_GLOBAL              int
              268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               2
              272  BINARY_TRUE_DIVIDE
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  BINARY_MULTIPLY  
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  STORE_FAST               '_image_height'

 L. 637       284  LOAD_CONST               2
              286  LOAD_GLOBAL              int
              288  LOAD_FAST                '_image_width'
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BINARY_MULTIPLY  
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               '_image_width'

 L. 639       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                lwgfeature
              308  LOAD_METHOD              selectedItems
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               '_features'

 L. 640       314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainml2dwcaefromexisting.clickBtnTrainMl2DWcaeFromExisting.<locals>.<listcomp>'
              318  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              320  LOAD_FAST                '_features'
              322  GET_ITER         
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               '_features'

 L. 641       328  LOAD_DEREF               'self'
              330  LOAD_ATTR                featurelist
              332  LOAD_DEREF               'self'
              334  LOAD_ATTR                cbbtarget
              336  LOAD_METHOD              currentIndex
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  BINARY_SUBSCR    
              342  STORE_FAST               '_target'

 L. 642       344  LOAD_DEREF               'self'
              346  LOAD_ATTR                featurelist
              348  LOAD_DEREF               'self'
              350  LOAD_ATTR                cbbweight
              352  LOAD_METHOD              currentIndex
              354  CALL_METHOD_0         0  '0 positional arguments'
              356  BINARY_SUBSCR    
              358  STORE_FAST               '_weight'

 L. 644       360  LOAD_GLOBAL              len
              362  LOAD_DEREF               'self'
              364  LOAD_ATTR                ldtexisting
              366  LOAD_METHOD              text
              368  CALL_METHOD_0         0  '0 positional arguments'
              370  CALL_FUNCTION_1       1  '1 positional argument'
              372  LOAD_CONST               1
              374  COMPARE_OP               <
          376_378  POP_JUMP_IF_FALSE   416  'to 416'

 L. 645       380  LOAD_GLOBAL              vis_msg
              382  LOAD_ATTR                print
              384  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: No name specified for pre-trained network'

 L. 646       386  LOAD_STR                 'error'
              388  LOAD_CONST               ('type',)
              390  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              392  POP_TOP          

 L. 647       394  LOAD_GLOBAL              QtWidgets
              396  LOAD_ATTR                QMessageBox
              398  LOAD_METHOD              critical
              400  LOAD_DEREF               'self'
              402  LOAD_ATTR                msgbox

 L. 648       404  LOAD_STR                 'Train 2D-WCAE'

 L. 649       406  LOAD_STR                 'No name specified for pre-trained network'
              408  CALL_METHOD_3         3  '3 positional arguments'
              410  POP_TOP          

 L. 650       412  LOAD_CONST               None
              414  RETURN_VALUE     
            416_0  COME_FROM           376  '376'

 L. 651       416  LOAD_GLOBAL              os
              418  LOAD_ATTR                path
              420  LOAD_METHOD              dirname
              422  LOAD_DEREF               'self'
              424  LOAD_ATTR                ldtexisting
              426  LOAD_METHOD              text
              428  CALL_METHOD_0         0  '0 positional arguments'
              430  CALL_METHOD_1         1  '1 positional argument'
              432  STORE_FAST               '_precnnpath'

 L. 652       434  LOAD_GLOBAL              os
              436  LOAD_ATTR                path
              438  LOAD_METHOD              splitext
              440  LOAD_GLOBAL              os
              442  LOAD_ATTR                path
              444  LOAD_METHOD              basename
              446  LOAD_DEREF               'self'
              448  LOAD_ATTR                ldtexisting
              450  LOAD_METHOD              text
              452  CALL_METHOD_0         0  '0 positional arguments'
              454  CALL_METHOD_1         1  '1 positional argument'
              456  CALL_METHOD_1         1  '1 positional argument'
              458  LOAD_CONST               0
              460  BINARY_SUBSCR    
              462  STORE_FAST               '_precnnname'

 L. 653       464  LOAD_DEREF               'self'
              466  LOAD_ATTR                cbbblockid
              468  LOAD_METHOD              currentIndex
              470  CALL_METHOD_0         0  '0 positional arguments'
              472  STORE_FAST               '_blockidx'

 L. 654       474  LOAD_DEREF               'self'
              476  LOAD_ATTR                cbblayerid
              478  LOAD_METHOD              currentIndex
              480  CALL_METHOD_0         0  '0 positional arguments'
              482  STORE_FAST               '_layeridx'

 L. 655       484  LOAD_CONST               True
              486  STORE_FAST               '_trainable'

 L. 656       488  LOAD_DEREF               'self'
              490  LOAD_ATTR                cbbtrainable
              492  LOAD_METHOD              currentIndex
              494  CALL_METHOD_0         0  '0 positional arguments'
              496  LOAD_CONST               0
              498  COMPARE_OP               !=
          500_502  POP_JUMP_IF_FALSE   508  'to 508'

 L. 657       504  LOAD_CONST               False
              506  STORE_FAST               '_trainable'
            508_0  COME_FROM           500  '500'

 L. 659       508  LOAD_GLOBAL              ml_tfm
              510  LOAD_METHOD              getConvModelNChannel
              512  LOAD_FAST                '_precnnpath'
              514  LOAD_FAST                '_precnnname'
              516  CALL_METHOD_2         2  '2 positional arguments'
              518  LOAD_GLOBAL              len
              520  LOAD_FAST                '_features'
              522  CALL_FUNCTION_1       1  '1 positional argument'
              524  COMPARE_OP               !=
          526_528  POP_JUMP_IF_FALSE   566  'to 566'

 L. 660       530  LOAD_GLOBAL              vis_msg
              532  LOAD_ATTR                print
              534  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Feature channel number not match with pre-trained network'

 L. 661       536  LOAD_STR                 'error'
              538  LOAD_CONST               ('type',)
              540  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              542  POP_TOP          

 L. 662       544  LOAD_GLOBAL              QtWidgets
              546  LOAD_ATTR                QMessageBox
              548  LOAD_METHOD              critical
              550  LOAD_DEREF               'self'
              552  LOAD_ATTR                msgbox

 L. 663       554  LOAD_STR                 'Train 2D-WCAE'

 L. 664       556  LOAD_STR                 'Feature channel number not match with pre-trained network'
              558  CALL_METHOD_3         3  '3 positional arguments'
              560  POP_TOP          

 L. 665       562  LOAD_CONST               None
              564  RETURN_VALUE     
            566_0  COME_FROM           526  '526'

 L. 667       566  LOAD_GLOBAL              basic_data
              568  LOAD_METHOD              str2int
              570  LOAD_DEREF               'self'
              572  LOAD_ATTR                ldtnconvblock
              574  LOAD_METHOD              text
              576  CALL_METHOD_0         0  '0 positional arguments'
              578  CALL_METHOD_1         1  '1 positional argument'
              580  STORE_FAST               '_nconvblock'

 L. 668       582  LOAD_CLOSURE             'self'
              584  BUILD_TUPLE_1         1 
              586  LOAD_LISTCOMP            '<code_object <listcomp>>'
              588  LOAD_STR                 'trainml2dwcaefromexisting.clickBtnTrainMl2DWcaeFromExisting.<locals>.<listcomp>'
              590  MAKE_FUNCTION_8          'closure'
              592  LOAD_GLOBAL              range
              594  LOAD_FAST                '_nconvblock'
              596  CALL_FUNCTION_1       1  '1 positional argument'
              598  GET_ITER         
              600  CALL_FUNCTION_1       1  '1 positional argument'
              602  STORE_FAST               '_nconvlayer'

 L. 669       604  LOAD_CLOSURE             'self'
              606  BUILD_TUPLE_1         1 
              608  LOAD_LISTCOMP            '<code_object <listcomp>>'
              610  LOAD_STR                 'trainml2dwcaefromexisting.clickBtnTrainMl2DWcaeFromExisting.<locals>.<listcomp>'
              612  MAKE_FUNCTION_8          'closure'
              614  LOAD_GLOBAL              range
              616  LOAD_FAST                '_nconvblock'
              618  CALL_FUNCTION_1       1  '1 positional argument'
              620  GET_ITER         
              622  CALL_FUNCTION_1       1  '1 positional argument'
              624  STORE_FAST               '_nconvfeature'

 L. 670       626  LOAD_GLOBAL              basic_data
              628  LOAD_METHOD              str2int
              630  LOAD_DEREF               'self'
              632  LOAD_ATTR                ldtn1x1layer
              634  LOAD_METHOD              text
              636  CALL_METHOD_0         0  '0 positional arguments'
              638  CALL_METHOD_1         1  '1 positional argument'
              640  STORE_FAST               '_n1x1layer'

 L. 671       642  LOAD_CLOSURE             'self'
              644  BUILD_TUPLE_1         1 
              646  LOAD_LISTCOMP            '<code_object <listcomp>>'
              648  LOAD_STR                 'trainml2dwcaefromexisting.clickBtnTrainMl2DWcaeFromExisting.<locals>.<listcomp>'
              650  MAKE_FUNCTION_8          'closure'
              652  LOAD_GLOBAL              range
              654  LOAD_FAST                '_n1x1layer'
              656  CALL_FUNCTION_1       1  '1 positional argument'
              658  GET_ITER         
              660  CALL_FUNCTION_1       1  '1 positional argument'
              662  STORE_FAST               '_n1x1feature'

 L. 672       664  LOAD_GLOBAL              basic_data
              666  LOAD_METHOD              str2int
              668  LOAD_DEREF               'self'
              670  LOAD_ATTR                ldtmaskheight
              672  LOAD_METHOD              text
              674  CALL_METHOD_0         0  '0 positional arguments'
              676  CALL_METHOD_1         1  '1 positional argument'
              678  STORE_FAST               '_patch_height'

 L. 673       680  LOAD_GLOBAL              basic_data
              682  LOAD_METHOD              str2int
              684  LOAD_DEREF               'self'
              686  LOAD_ATTR                ldtmaskwidth
              688  LOAD_METHOD              text
              690  CALL_METHOD_0         0  '0 positional arguments'
              692  CALL_METHOD_1         1  '1 positional argument'
              694  STORE_FAST               '_patch_width'

 L. 674       696  LOAD_GLOBAL              basic_data
              698  LOAD_METHOD              str2int
              700  LOAD_DEREF               'self'
              702  LOAD_ATTR                ldtpoolheight
              704  LOAD_METHOD              text
              706  CALL_METHOD_0         0  '0 positional arguments'
              708  CALL_METHOD_1         1  '1 positional argument'
              710  STORE_FAST               '_pool_height'

 L. 675       712  LOAD_GLOBAL              basic_data
              714  LOAD_METHOD              str2int
              716  LOAD_DEREF               'self'
              718  LOAD_ATTR                ldtpoolwidth
              720  LOAD_METHOD              text
              722  CALL_METHOD_0         0  '0 positional arguments'
              724  CALL_METHOD_1         1  '1 positional argument'
              726  STORE_FAST               '_pool_width'

 L. 676       728  LOAD_GLOBAL              basic_data
              730  LOAD_METHOD              str2int
              732  LOAD_DEREF               'self'
              734  LOAD_ATTR                ldtnepoch
              736  LOAD_METHOD              text
              738  CALL_METHOD_0         0  '0 positional arguments'
              740  CALL_METHOD_1         1  '1 positional argument'
              742  STORE_FAST               '_nepoch'

 L. 677       744  LOAD_GLOBAL              basic_data
              746  LOAD_METHOD              str2int
              748  LOAD_DEREF               'self'
              750  LOAD_ATTR                ldtbatchsize
              752  LOAD_METHOD              text
              754  CALL_METHOD_0         0  '0 positional arguments'
              756  CALL_METHOD_1         1  '1 positional argument'
              758  STORE_FAST               '_batchsize'

 L. 678       760  LOAD_GLOBAL              basic_data
              762  LOAD_METHOD              str2float
              764  LOAD_DEREF               'self'
              766  LOAD_ATTR                ldtlearnrate
              768  LOAD_METHOD              text
              770  CALL_METHOD_0         0  '0 positional arguments'
              772  CALL_METHOD_1         1  '1 positional argument'
              774  STORE_FAST               '_learning_rate'

 L. 679       776  LOAD_GLOBAL              basic_data
              778  LOAD_METHOD              str2float
              780  LOAD_DEREF               'self'
              782  LOAD_ATTR                ldtdropout
              784  LOAD_METHOD              text
              786  CALL_METHOD_0         0  '0 positional arguments'
              788  CALL_METHOD_1         1  '1 positional argument'
              790  STORE_FAST               '_dropout_prob'

 L. 680       792  LOAD_FAST                '_nconvblock'
              794  LOAD_CONST               False
              796  COMPARE_OP               is
          798_800  POP_JUMP_IF_TRUE    812  'to 812'
              802  LOAD_FAST                '_nconvblock'
              804  LOAD_CONST               0
              806  COMPARE_OP               <=
          808_810  POP_JUMP_IF_FALSE   848  'to 848'
            812_0  COME_FROM           798  '798'

 L. 681       812  LOAD_GLOBAL              vis_msg
              814  LOAD_ATTR                print
              816  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Non-positive convolutional block number'

 L. 682       818  LOAD_STR                 'error'
              820  LOAD_CONST               ('type',)
              822  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              824  POP_TOP          

 L. 683       826  LOAD_GLOBAL              QtWidgets
              828  LOAD_ATTR                QMessageBox
              830  LOAD_METHOD              critical
              832  LOAD_DEREF               'self'
              834  LOAD_ATTR                msgbox

 L. 684       836  LOAD_STR                 'Train 2D-WCAE'

 L. 685       838  LOAD_STR                 'Non-positive convolutional block number'
              840  CALL_METHOD_3         3  '3 positional arguments'
              842  POP_TOP          

 L. 686       844  LOAD_CONST               None
              846  RETURN_VALUE     
            848_0  COME_FROM           808  '808'

 L. 687       848  SETUP_LOOP          920  'to 920'
              850  LOAD_FAST                '_nconvlayer'
              852  GET_ITER         
            854_0  COME_FROM           874  '874'
              854  FOR_ITER            918  'to 918'
              856  STORE_FAST               '_i'

 L. 688       858  LOAD_FAST                '_i'
              860  LOAD_CONST               False
              862  COMPARE_OP               is
          864_866  POP_JUMP_IF_TRUE    878  'to 878'
              868  LOAD_FAST                '_i'
              870  LOAD_CONST               1
              872  COMPARE_OP               <
          874_876  POP_JUMP_IF_FALSE   854  'to 854'
            878_0  COME_FROM           864  '864'

 L. 689       878  LOAD_GLOBAL              vis_msg
              880  LOAD_ATTR                print
              882  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Non-positive convolutional layer number'

 L. 690       884  LOAD_STR                 'error'
              886  LOAD_CONST               ('type',)
              888  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              890  POP_TOP          

 L. 691       892  LOAD_GLOBAL              QtWidgets
              894  LOAD_ATTR                QMessageBox
              896  LOAD_METHOD              critical
              898  LOAD_DEREF               'self'
              900  LOAD_ATTR                msgbox

 L. 692       902  LOAD_STR                 'Train 2D-WCAE'

 L. 693       904  LOAD_STR                 'Non-positive convolutional layer number'
              906  CALL_METHOD_3         3  '3 positional arguments'
              908  POP_TOP          

 L. 694       910  LOAD_CONST               None
              912  RETURN_VALUE     
          914_916  JUMP_BACK           854  'to 854'
              918  POP_BLOCK        
            920_0  COME_FROM_LOOP      848  '848'

 L. 695       920  SETUP_LOOP          992  'to 992'
              922  LOAD_FAST                '_nconvfeature'
              924  GET_ITER         
            926_0  COME_FROM           946  '946'
              926  FOR_ITER            990  'to 990'
              928  STORE_FAST               '_i'

 L. 696       930  LOAD_FAST                '_i'
              932  LOAD_CONST               False
              934  COMPARE_OP               is
          936_938  POP_JUMP_IF_TRUE    950  'to 950'
              940  LOAD_FAST                '_i'
              942  LOAD_CONST               1
              944  COMPARE_OP               <
          946_948  POP_JUMP_IF_FALSE   926  'to 926'
            950_0  COME_FROM           936  '936'

 L. 697       950  LOAD_GLOBAL              vis_msg
              952  LOAD_ATTR                print
              954  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Non-positive convolutional feature number'

 L. 698       956  LOAD_STR                 'error'
              958  LOAD_CONST               ('type',)
              960  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              962  POP_TOP          

 L. 699       964  LOAD_GLOBAL              QtWidgets
              966  LOAD_ATTR                QMessageBox
              968  LOAD_METHOD              critical
              970  LOAD_DEREF               'self'
              972  LOAD_ATTR                msgbox

 L. 700       974  LOAD_STR                 'Train 2D-WCAE'

 L. 701       976  LOAD_STR                 'Non-positive convolutional feature number'
              978  CALL_METHOD_3         3  '3 positional arguments'
              980  POP_TOP          

 L. 702       982  LOAD_CONST               None
              984  RETURN_VALUE     
          986_988  JUMP_BACK           926  'to 926'
              990  POP_BLOCK        
            992_0  COME_FROM_LOOP      920  '920'

 L. 703       992  LOAD_FAST                '_n1x1layer'
              994  LOAD_CONST               False
              996  COMPARE_OP               is
         998_1000  POP_JUMP_IF_TRUE   1012  'to 1012'
             1002  LOAD_FAST                '_n1x1layer'
             1004  LOAD_CONST               0
             1006  COMPARE_OP               <=
         1008_1010  POP_JUMP_IF_FALSE  1048  'to 1048'
           1012_0  COME_FROM           998  '998'

 L. 704      1012  LOAD_GLOBAL              vis_msg
             1014  LOAD_ATTR                print
             1016  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Non-positive 1x1 convolutional layer number'

 L. 705      1018  LOAD_STR                 'error'
             1020  LOAD_CONST               ('type',)
             1022  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1024  POP_TOP          

 L. 706      1026  LOAD_GLOBAL              QtWidgets
             1028  LOAD_ATTR                QMessageBox
             1030  LOAD_METHOD              critical
             1032  LOAD_DEREF               'self'
             1034  LOAD_ATTR                msgbox

 L. 707      1036  LOAD_STR                 'Train 2D-WCAE'

 L. 708      1038  LOAD_STR                 'Non-positive 1x1 convolutional layer number'
             1040  CALL_METHOD_3         3  '3 positional arguments'
             1042  POP_TOP          

 L. 709      1044  LOAD_CONST               None
             1046  RETURN_VALUE     
           1048_0  COME_FROM          1008  '1008'

 L. 710      1048  SETUP_LOOP         1120  'to 1120'
             1050  LOAD_FAST                '_n1x1feature'
             1052  GET_ITER         
           1054_0  COME_FROM          1074  '1074'
             1054  FOR_ITER           1118  'to 1118'
             1056  STORE_FAST               '_i'

 L. 711      1058  LOAD_FAST                '_i'
             1060  LOAD_CONST               False
             1062  COMPARE_OP               is
         1064_1066  POP_JUMP_IF_TRUE   1078  'to 1078'
             1068  LOAD_FAST                '_i'
             1070  LOAD_CONST               1
             1072  COMPARE_OP               <
         1074_1076  POP_JUMP_IF_FALSE  1054  'to 1054'
           1078_0  COME_FROM          1064  '1064'

 L. 712      1078  LOAD_GLOBAL              vis_msg
             1080  LOAD_ATTR                print
             1082  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Non-positive 1x1 convolutional feature number'

 L. 713      1084  LOAD_STR                 'error'
             1086  LOAD_CONST               ('type',)
             1088  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1090  POP_TOP          

 L. 714      1092  LOAD_GLOBAL              QtWidgets
             1094  LOAD_ATTR                QMessageBox
             1096  LOAD_METHOD              critical
             1098  LOAD_DEREF               'self'
             1100  LOAD_ATTR                msgbox

 L. 715      1102  LOAD_STR                 'Train 2D-WCAE'

 L. 716      1104  LOAD_STR                 'Non-positive 1x1 convolutional feature number'
             1106  CALL_METHOD_3         3  '3 positional arguments'
             1108  POP_TOP          

 L. 717      1110  LOAD_CONST               None
             1112  RETURN_VALUE     
         1114_1116  JUMP_BACK          1054  'to 1054'
             1118  POP_BLOCK        
           1120_0  COME_FROM_LOOP     1048  '1048'

 L. 718      1120  LOAD_FAST                '_patch_height'
             1122  LOAD_CONST               False
             1124  COMPARE_OP               is
         1126_1128  POP_JUMP_IF_TRUE   1160  'to 1160'
             1130  LOAD_FAST                '_patch_width'
             1132  LOAD_CONST               False
             1134  COMPARE_OP               is
         1136_1138  POP_JUMP_IF_TRUE   1160  'to 1160'

 L. 719      1140  LOAD_FAST                '_patch_height'
             1142  LOAD_CONST               1
             1144  COMPARE_OP               <
         1146_1148  POP_JUMP_IF_TRUE   1160  'to 1160'
             1150  LOAD_FAST                '_patch_width'
             1152  LOAD_CONST               1
             1154  COMPARE_OP               <
         1156_1158  POP_JUMP_IF_FALSE  1196  'to 1196'
           1160_0  COME_FROM          1146  '1146'
           1160_1  COME_FROM          1136  '1136'
           1160_2  COME_FROM          1126  '1126'

 L. 720      1160  LOAD_GLOBAL              vis_msg
             1162  LOAD_ATTR                print
             1164  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Non-positive convolutional patch size'

 L. 721      1166  LOAD_STR                 'error'
             1168  LOAD_CONST               ('type',)
             1170  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1172  POP_TOP          

 L. 722      1174  LOAD_GLOBAL              QtWidgets
             1176  LOAD_ATTR                QMessageBox
             1178  LOAD_METHOD              critical
             1180  LOAD_DEREF               'self'
             1182  LOAD_ATTR                msgbox

 L. 723      1184  LOAD_STR                 'Train 2D-WCAE'

 L. 724      1186  LOAD_STR                 'Non-positive convolutional patch size'
             1188  CALL_METHOD_3         3  '3 positional arguments'
             1190  POP_TOP          

 L. 725      1192  LOAD_CONST               None
             1194  RETURN_VALUE     
           1196_0  COME_FROM          1156  '1156'

 L. 726      1196  LOAD_FAST                '_pool_height'
             1198  LOAD_CONST               False
             1200  COMPARE_OP               is
         1202_1204  POP_JUMP_IF_TRUE   1236  'to 1236'
             1206  LOAD_FAST                '_pool_width'
             1208  LOAD_CONST               False
             1210  COMPARE_OP               is
         1212_1214  POP_JUMP_IF_TRUE   1236  'to 1236'

 L. 727      1216  LOAD_FAST                '_pool_height'
             1218  LOAD_CONST               1
             1220  COMPARE_OP               <
         1222_1224  POP_JUMP_IF_TRUE   1236  'to 1236'
             1226  LOAD_FAST                '_pool_width'
             1228  LOAD_CONST               1
             1230  COMPARE_OP               <
         1232_1234  POP_JUMP_IF_FALSE  1272  'to 1272'
           1236_0  COME_FROM          1222  '1222'
           1236_1  COME_FROM          1212  '1212'
           1236_2  COME_FROM          1202  '1202'

 L. 728      1236  LOAD_GLOBAL              vis_msg
             1238  LOAD_ATTR                print
             1240  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Non-positive pooling size'
             1242  LOAD_STR                 'error'
             1244  LOAD_CONST               ('type',)
             1246  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1248  POP_TOP          

 L. 729      1250  LOAD_GLOBAL              QtWidgets
             1252  LOAD_ATTR                QMessageBox
             1254  LOAD_METHOD              critical
             1256  LOAD_DEREF               'self'
             1258  LOAD_ATTR                msgbox

 L. 730      1260  LOAD_STR                 'Train 2D-WCAE'

 L. 731      1262  LOAD_STR                 'Non-positive pooling size'
             1264  CALL_METHOD_3         3  '3 positional arguments'
             1266  POP_TOP          

 L. 732      1268  LOAD_CONST               None
             1270  RETURN_VALUE     
           1272_0  COME_FROM          1232  '1232'

 L. 733      1272  LOAD_FAST                '_nepoch'
             1274  LOAD_CONST               False
             1276  COMPARE_OP               is
         1278_1280  POP_JUMP_IF_TRUE   1292  'to 1292'
             1282  LOAD_FAST                '_nepoch'
             1284  LOAD_CONST               0
             1286  COMPARE_OP               <=
         1288_1290  POP_JUMP_IF_FALSE  1328  'to 1328'
           1292_0  COME_FROM          1278  '1278'

 L. 734      1292  LOAD_GLOBAL              vis_msg
             1294  LOAD_ATTR                print
             1296  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Non-positive epoch number'
             1298  LOAD_STR                 'error'
             1300  LOAD_CONST               ('type',)
             1302  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1304  POP_TOP          

 L. 735      1306  LOAD_GLOBAL              QtWidgets
             1308  LOAD_ATTR                QMessageBox
             1310  LOAD_METHOD              critical
             1312  LOAD_DEREF               'self'
             1314  LOAD_ATTR                msgbox

 L. 736      1316  LOAD_STR                 'Train 2D-WCAE'

 L. 737      1318  LOAD_STR                 'Non-positive epoch number'
             1320  CALL_METHOD_3         3  '3 positional arguments'
             1322  POP_TOP          

 L. 738      1324  LOAD_CONST               None
             1326  RETURN_VALUE     
           1328_0  COME_FROM          1288  '1288'

 L. 739      1328  LOAD_FAST                '_batchsize'
             1330  LOAD_CONST               False
             1332  COMPARE_OP               is
         1334_1336  POP_JUMP_IF_TRUE   1348  'to 1348'
             1338  LOAD_FAST                '_batchsize'
             1340  LOAD_CONST               0
             1342  COMPARE_OP               <=
         1344_1346  POP_JUMP_IF_FALSE  1384  'to 1384'
           1348_0  COME_FROM          1334  '1334'

 L. 740      1348  LOAD_GLOBAL              vis_msg
             1350  LOAD_ATTR                print
             1352  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Non-positive batch size'
             1354  LOAD_STR                 'error'
             1356  LOAD_CONST               ('type',)
             1358  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1360  POP_TOP          

 L. 741      1362  LOAD_GLOBAL              QtWidgets
             1364  LOAD_ATTR                QMessageBox
             1366  LOAD_METHOD              critical
             1368  LOAD_DEREF               'self'
             1370  LOAD_ATTR                msgbox

 L. 742      1372  LOAD_STR                 'Train 2D-WCAE'

 L. 743      1374  LOAD_STR                 'Non-positive batch size'
             1376  CALL_METHOD_3         3  '3 positional arguments'
             1378  POP_TOP          

 L. 744      1380  LOAD_CONST               None
             1382  RETURN_VALUE     
           1384_0  COME_FROM          1344  '1344'

 L. 745      1384  LOAD_FAST                '_learning_rate'
             1386  LOAD_CONST               False
             1388  COMPARE_OP               is
         1390_1392  POP_JUMP_IF_TRUE   1404  'to 1404'
             1394  LOAD_FAST                '_learning_rate'
             1396  LOAD_CONST               0
             1398  COMPARE_OP               <=
         1400_1402  POP_JUMP_IF_FALSE  1440  'to 1440'
           1404_0  COME_FROM          1390  '1390'

 L. 746      1404  LOAD_GLOBAL              vis_msg
             1406  LOAD_ATTR                print
             1408  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Non-positive learning rate'
             1410  LOAD_STR                 'error'
             1412  LOAD_CONST               ('type',)
             1414  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1416  POP_TOP          

 L. 747      1418  LOAD_GLOBAL              QtWidgets
             1420  LOAD_ATTR                QMessageBox
             1422  LOAD_METHOD              critical
             1424  LOAD_DEREF               'self'
             1426  LOAD_ATTR                msgbox

 L. 748      1428  LOAD_STR                 'Train 2D-WCAE'

 L. 749      1430  LOAD_STR                 'Non-positive learning rate'
             1432  CALL_METHOD_3         3  '3 positional arguments'
             1434  POP_TOP          

 L. 750      1436  LOAD_CONST               None
             1438  RETURN_VALUE     
           1440_0  COME_FROM          1400  '1400'

 L. 751      1440  LOAD_FAST                '_dropout_prob'
             1442  LOAD_CONST               False
             1444  COMPARE_OP               is
         1446_1448  POP_JUMP_IF_TRUE   1460  'to 1460'
             1450  LOAD_FAST                '_dropout_prob'
             1452  LOAD_CONST               0
             1454  COMPARE_OP               <=
         1456_1458  POP_JUMP_IF_FALSE  1496  'to 1496'
           1460_0  COME_FROM          1446  '1446'

 L. 752      1460  LOAD_GLOBAL              vis_msg
             1462  LOAD_ATTR                print
             1464  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: Negative dropout rate'
             1466  LOAD_STR                 'error'
             1468  LOAD_CONST               ('type',)
             1470  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1472  POP_TOP          

 L. 753      1474  LOAD_GLOBAL              QtWidgets
             1476  LOAD_ATTR                QMessageBox
             1478  LOAD_METHOD              critical
             1480  LOAD_DEREF               'self'
             1482  LOAD_ATTR                msgbox

 L. 754      1484  LOAD_STR                 'Train 2D-WCAE'

 L. 755      1486  LOAD_STR                 'Negative dropout rate'
             1488  CALL_METHOD_3         3  '3 positional arguments'
             1490  POP_TOP          

 L. 756      1492  LOAD_CONST               None
             1494  RETURN_VALUE     
           1496_0  COME_FROM          1456  '1456'

 L. 758      1496  LOAD_GLOBAL              len
             1498  LOAD_DEREF               'self'
             1500  LOAD_ATTR                ldtsave
             1502  LOAD_METHOD              text
             1504  CALL_METHOD_0         0  '0 positional arguments'
             1506  CALL_FUNCTION_1       1  '1 positional argument'
             1508  LOAD_CONST               1
             1510  COMPARE_OP               <
         1512_1514  POP_JUMP_IF_FALSE  1552  'to 1552'

 L. 759      1516  LOAD_GLOBAL              vis_msg
             1518  LOAD_ATTR                print
             1520  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: No name specified for CAE network'

 L. 760      1522  LOAD_STR                 'error'
             1524  LOAD_CONST               ('type',)
             1526  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1528  POP_TOP          

 L. 761      1530  LOAD_GLOBAL              QtWidgets
             1532  LOAD_ATTR                QMessageBox
             1534  LOAD_METHOD              critical
             1536  LOAD_DEREF               'self'
             1538  LOAD_ATTR                msgbox

 L. 762      1540  LOAD_STR                 'Train 2D-WCAE'

 L. 763      1542  LOAD_STR                 'No name specified for CAE network'
             1544  CALL_METHOD_3         3  '3 positional arguments'
             1546  POP_TOP          

 L. 764      1548  LOAD_CONST               None
             1550  RETURN_VALUE     
           1552_0  COME_FROM          1512  '1512'

 L. 765      1552  LOAD_GLOBAL              os
             1554  LOAD_ATTR                path
             1556  LOAD_METHOD              dirname
             1558  LOAD_DEREF               'self'
             1560  LOAD_ATTR                ldtsave
             1562  LOAD_METHOD              text
             1564  CALL_METHOD_0         0  '0 positional arguments'
             1566  CALL_METHOD_1         1  '1 positional argument'
             1568  STORE_FAST               '_savepath'

 L. 766      1570  LOAD_GLOBAL              os
             1572  LOAD_ATTR                path
             1574  LOAD_METHOD              splitext
             1576  LOAD_GLOBAL              os
             1578  LOAD_ATTR                path
             1580  LOAD_METHOD              basename
             1582  LOAD_DEREF               'self'
             1584  LOAD_ATTR                ldtsave
             1586  LOAD_METHOD              text
             1588  CALL_METHOD_0         0  '0 positional arguments'
             1590  CALL_METHOD_1         1  '1 positional argument'
             1592  CALL_METHOD_1         1  '1 positional argument'
             1594  LOAD_CONST               0
             1596  BINARY_SUBSCR    
             1598  STORE_FAST               '_savename'

 L. 768      1600  LOAD_CONST               0
             1602  STORE_FAST               '_wdinl'

 L. 769      1604  LOAD_CONST               0
             1606  STORE_FAST               '_wdxl'

 L. 770      1608  LOAD_CONST               0
             1610  STORE_FAST               '_wdz'

 L. 771      1612  LOAD_DEREF               'self'
             1614  LOAD_ATTR                cbbornt
             1616  LOAD_METHOD              currentIndex
             1618  CALL_METHOD_0         0  '0 positional arguments'
             1620  LOAD_CONST               0
             1622  COMPARE_OP               ==
         1624_1626  POP_JUMP_IF_FALSE  1652  'to 1652'

 L. 772      1628  LOAD_GLOBAL              int
             1630  LOAD_FAST                '_image_width'
             1632  LOAD_CONST               2
             1634  BINARY_TRUE_DIVIDE
             1636  CALL_FUNCTION_1       1  '1 positional argument'
             1638  STORE_FAST               '_wdxl'

 L. 773      1640  LOAD_GLOBAL              int
             1642  LOAD_FAST                '_image_height'
             1644  LOAD_CONST               2
             1646  BINARY_TRUE_DIVIDE
             1648  CALL_FUNCTION_1       1  '1 positional argument'
             1650  STORE_FAST               '_wdz'
           1652_0  COME_FROM          1624  '1624'

 L. 774      1652  LOAD_DEREF               'self'
             1654  LOAD_ATTR                cbbornt
             1656  LOAD_METHOD              currentIndex
             1658  CALL_METHOD_0         0  '0 positional arguments'
             1660  LOAD_CONST               1
             1662  COMPARE_OP               ==
         1664_1666  POP_JUMP_IF_FALSE  1692  'to 1692'

 L. 775      1668  LOAD_GLOBAL              int
             1670  LOAD_FAST                '_image_width'
             1672  LOAD_CONST               2
             1674  BINARY_TRUE_DIVIDE
             1676  CALL_FUNCTION_1       1  '1 positional argument'
             1678  STORE_FAST               '_wdinl'

 L. 776      1680  LOAD_GLOBAL              int
             1682  LOAD_FAST                '_image_height'
             1684  LOAD_CONST               2
             1686  BINARY_TRUE_DIVIDE
             1688  CALL_FUNCTION_1       1  '1 positional argument'
             1690  STORE_FAST               '_wdz'
           1692_0  COME_FROM          1664  '1664'

 L. 777      1692  LOAD_DEREF               'self'
             1694  LOAD_ATTR                cbbornt
             1696  LOAD_METHOD              currentIndex
             1698  CALL_METHOD_0         0  '0 positional arguments'
             1700  LOAD_CONST               2
             1702  COMPARE_OP               ==
         1704_1706  POP_JUMP_IF_FALSE  1732  'to 1732'

 L. 778      1708  LOAD_GLOBAL              int
             1710  LOAD_FAST                '_image_width'
             1712  LOAD_CONST               2
             1714  BINARY_TRUE_DIVIDE
             1716  CALL_FUNCTION_1       1  '1 positional argument'
             1718  STORE_FAST               '_wdinl'

 L. 779      1720  LOAD_GLOBAL              int
             1722  LOAD_FAST                '_image_height'
             1724  LOAD_CONST               2
             1726  BINARY_TRUE_DIVIDE
             1728  CALL_FUNCTION_1       1  '1 positional argument'
             1730  STORE_FAST               '_wdxl'
           1732_0  COME_FROM          1704  '1704'

 L. 781      1732  LOAD_DEREF               'self'
             1734  LOAD_ATTR                survinfo
             1736  STORE_FAST               '_seisinfo'

 L. 783      1738  LOAD_GLOBAL              print
             1740  LOAD_STR                 'TrainMl2DWcaeFromExisting: Step 1 - Step 1 - Get training samples:'
             1742  CALL_FUNCTION_1       1  '1 positional argument'
             1744  POP_TOP          

 L. 784      1746  LOAD_DEREF               'self'
             1748  LOAD_ATTR                traindataconfig
             1750  LOAD_STR                 'TrainPointSet'
             1752  BINARY_SUBSCR    
             1754  STORE_FAST               '_trainpoint'

 L. 785      1756  LOAD_GLOBAL              np
             1758  LOAD_METHOD              zeros
             1760  LOAD_CONST               0
             1762  LOAD_CONST               3
             1764  BUILD_LIST_2          2 
             1766  CALL_METHOD_1         1  '1 positional argument'
             1768  STORE_FAST               '_traindata'

 L. 786      1770  SETUP_LOOP         1846  'to 1846'
             1772  LOAD_FAST                '_trainpoint'
             1774  GET_ITER         
           1776_0  COME_FROM          1794  '1794'
             1776  FOR_ITER           1844  'to 1844'
             1778  STORE_FAST               '_p'

 L. 787      1780  LOAD_GLOBAL              point_ays
             1782  LOAD_METHOD              checkPoint
             1784  LOAD_DEREF               'self'
             1786  LOAD_ATTR                pointsetdata
             1788  LOAD_FAST                '_p'
             1790  BINARY_SUBSCR    
             1792  CALL_METHOD_1         1  '1 positional argument'
         1794_1796  POP_JUMP_IF_FALSE  1776  'to 1776'

 L. 788      1798  LOAD_GLOBAL              basic_mdt
             1800  LOAD_METHOD              exportMatDict
             1802  LOAD_DEREF               'self'
             1804  LOAD_ATTR                pointsetdata
             1806  LOAD_FAST                '_p'
             1808  BINARY_SUBSCR    
             1810  LOAD_STR                 'Inline'
             1812  LOAD_STR                 'Crossline'
             1814  LOAD_STR                 'Z'
             1816  BUILD_LIST_3          3 
             1818  CALL_METHOD_2         2  '2 positional arguments'
             1820  STORE_FAST               '_pt'

 L. 789      1822  LOAD_GLOBAL              np
             1824  LOAD_ATTR                concatenate
             1826  LOAD_FAST                '_traindata'
             1828  LOAD_FAST                '_pt'
             1830  BUILD_TUPLE_2         2 
             1832  LOAD_CONST               0
             1834  LOAD_CONST               ('axis',)
             1836  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1838  STORE_FAST               '_traindata'
         1840_1842  JUMP_BACK          1776  'to 1776'
             1844  POP_BLOCK        
           1846_0  COME_FROM_LOOP     1770  '1770'

 L. 790      1846  LOAD_GLOBAL              seis_ays
             1848  LOAD_ATTR                removeOutofSurveySample
             1850  LOAD_FAST                '_traindata'

 L. 791      1852  LOAD_FAST                '_seisinfo'
             1854  LOAD_STR                 'ILStart'
             1856  BINARY_SUBSCR    
             1858  LOAD_FAST                '_wdinl'
             1860  LOAD_FAST                '_seisinfo'
             1862  LOAD_STR                 'ILStep'
             1864  BINARY_SUBSCR    
             1866  BINARY_MULTIPLY  
             1868  BINARY_ADD       

 L. 792      1870  LOAD_FAST                '_seisinfo'
             1872  LOAD_STR                 'ILEnd'
             1874  BINARY_SUBSCR    
             1876  LOAD_FAST                '_wdinl'
             1878  LOAD_FAST                '_seisinfo'
             1880  LOAD_STR                 'ILStep'
             1882  BINARY_SUBSCR    
             1884  BINARY_MULTIPLY  
             1886  BINARY_SUBTRACT  

 L. 793      1888  LOAD_FAST                '_seisinfo'
             1890  LOAD_STR                 'XLStart'
             1892  BINARY_SUBSCR    
             1894  LOAD_FAST                '_wdxl'
             1896  LOAD_FAST                '_seisinfo'
             1898  LOAD_STR                 'XLStep'
             1900  BINARY_SUBSCR    
             1902  BINARY_MULTIPLY  
             1904  BINARY_ADD       

 L. 794      1906  LOAD_FAST                '_seisinfo'
             1908  LOAD_STR                 'XLEnd'
             1910  BINARY_SUBSCR    
             1912  LOAD_FAST                '_wdxl'
             1914  LOAD_FAST                '_seisinfo'
             1916  LOAD_STR                 'XLStep'
             1918  BINARY_SUBSCR    
             1920  BINARY_MULTIPLY  
             1922  BINARY_SUBTRACT  

 L. 795      1924  LOAD_FAST                '_seisinfo'
             1926  LOAD_STR                 'ZStart'
             1928  BINARY_SUBSCR    
             1930  LOAD_FAST                '_wdz'
             1932  LOAD_FAST                '_seisinfo'
             1934  LOAD_STR                 'ZStep'
             1936  BINARY_SUBSCR    
             1938  BINARY_MULTIPLY  
             1940  BINARY_ADD       

 L. 796      1942  LOAD_FAST                '_seisinfo'
             1944  LOAD_STR                 'ZEnd'
             1946  BINARY_SUBSCR    
             1948  LOAD_FAST                '_wdz'
             1950  LOAD_FAST                '_seisinfo'
             1952  LOAD_STR                 'ZStep'
             1954  BINARY_SUBSCR    
             1956  BINARY_MULTIPLY  
             1958  BINARY_SUBTRACT  
             1960  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1962  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1964  STORE_FAST               '_traindata'

 L. 799      1966  LOAD_GLOBAL              np
             1968  LOAD_METHOD              shape
             1970  LOAD_FAST                '_traindata'
             1972  CALL_METHOD_1         1  '1 positional argument'
             1974  LOAD_CONST               0
             1976  BINARY_SUBSCR    
             1978  LOAD_CONST               0
             1980  COMPARE_OP               <=
         1982_1984  POP_JUMP_IF_FALSE  2022  'to 2022'

 L. 800      1986  LOAD_GLOBAL              vis_msg
             1988  LOAD_ATTR                print
             1990  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: No training sample found'
             1992  LOAD_STR                 'error'
             1994  LOAD_CONST               ('type',)
             1996  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1998  POP_TOP          

 L. 801      2000  LOAD_GLOBAL              QtWidgets
             2002  LOAD_ATTR                QMessageBox
             2004  LOAD_METHOD              critical
             2006  LOAD_DEREF               'self'
             2008  LOAD_ATTR                msgbox

 L. 802      2010  LOAD_STR                 'Train 2D-WCAE'

 L. 803      2012  LOAD_STR                 'No training sample found'
             2014  CALL_METHOD_3         3  '3 positional arguments'
             2016  POP_TOP          

 L. 804      2018  LOAD_CONST               None
             2020  RETURN_VALUE     
           2022_0  COME_FROM          1982  '1982'

 L. 807      2022  LOAD_GLOBAL              print
             2024  LOAD_STR                 'TrainMl2DWcaeFromExisting: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 808      2026  LOAD_FAST                '_image_height'
             2028  LOAD_FAST                '_image_width'
             2030  LOAD_FAST                '_image_height_new'
             2032  LOAD_FAST                '_image_width_new'
             2034  BUILD_TUPLE_4         4 
             2036  BINARY_MODULO    
             2038  CALL_FUNCTION_1       1  '1 positional argument'
             2040  POP_TOP          

 L. 809      2042  BUILD_MAP_0           0 
             2044  STORE_FAST               '_traindict'

 L. 810      2046  SETUP_LOOP         2118  'to 2118'
             2048  LOAD_FAST                '_features'
             2050  GET_ITER         
             2052  FOR_ITER           2116  'to 2116'
             2054  STORE_FAST               'f'

 L. 811      2056  LOAD_DEREF               'self'
             2058  LOAD_ATTR                seisdata
             2060  LOAD_FAST                'f'
             2062  BINARY_SUBSCR    
             2064  STORE_FAST               '_seisdata'

 L. 812      2066  LOAD_GLOBAL              seis_ays
             2068  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2070  LOAD_FAST                '_seisdata'
             2072  LOAD_FAST                '_traindata'
             2074  LOAD_DEREF               'self'
             2076  LOAD_ATTR                survinfo

 L. 813      2078  LOAD_FAST                '_wdinl'
             2080  LOAD_FAST                '_wdxl'
             2082  LOAD_FAST                '_wdz'

 L. 814      2084  LOAD_CONST               False
             2086  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2088  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2090  LOAD_CONST               None
             2092  LOAD_CONST               None
             2094  BUILD_SLICE_2         2 
             2096  LOAD_CONST               3
             2098  LOAD_CONST               None
             2100  BUILD_SLICE_2         2 
             2102  BUILD_TUPLE_2         2 
             2104  BINARY_SUBSCR    
             2106  LOAD_FAST                '_traindict'
             2108  LOAD_FAST                'f'
             2110  STORE_SUBSCR     
         2112_2114  JUMP_BACK          2052  'to 2052'
             2116  POP_BLOCK        
           2118_0  COME_FROM_LOOP     2046  '2046'

 L. 815      2118  LOAD_FAST                '_target'
             2120  LOAD_FAST                '_features'
             2122  COMPARE_OP               not-in
         2124_2126  POP_JUMP_IF_FALSE  2184  'to 2184'

 L. 816      2128  LOAD_DEREF               'self'
             2130  LOAD_ATTR                seisdata
             2132  LOAD_FAST                '_target'
             2134  BINARY_SUBSCR    
             2136  STORE_FAST               '_seisdata'

 L. 817      2138  LOAD_GLOBAL              seis_ays
             2140  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2142  LOAD_FAST                '_seisdata'
             2144  LOAD_FAST                '_traindata'
             2146  LOAD_DEREF               'self'
             2148  LOAD_ATTR                survinfo

 L. 818      2150  LOAD_FAST                '_wdinl'
             2152  LOAD_FAST                '_wdxl'
             2154  LOAD_FAST                '_wdz'

 L. 819      2156  LOAD_CONST               False
             2158  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2160  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2162  LOAD_CONST               None
             2164  LOAD_CONST               None
             2166  BUILD_SLICE_2         2 
             2168  LOAD_CONST               3
             2170  LOAD_CONST               None
             2172  BUILD_SLICE_2         2 
             2174  BUILD_TUPLE_2         2 
             2176  BINARY_SUBSCR    
             2178  LOAD_FAST                '_traindict'
             2180  LOAD_FAST                '_target'
             2182  STORE_SUBSCR     
           2184_0  COME_FROM          2124  '2124'

 L. 820      2184  LOAD_FAST                '_weight'
             2186  LOAD_FAST                '_features'
             2188  COMPARE_OP               not-in
         2190_2192  POP_JUMP_IF_FALSE  2260  'to 2260'
             2194  LOAD_FAST                '_weight'
             2196  LOAD_FAST                '_target'
             2198  COMPARE_OP               !=
         2200_2202  POP_JUMP_IF_FALSE  2260  'to 2260'

 L. 821      2204  LOAD_DEREF               'self'
             2206  LOAD_ATTR                seisdata
             2208  LOAD_FAST                '_weight'
             2210  BINARY_SUBSCR    
             2212  STORE_FAST               '_seisdata'

 L. 822      2214  LOAD_GLOBAL              seis_ays
             2216  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2218  LOAD_FAST                '_seisdata'
             2220  LOAD_FAST                '_traindata'
             2222  LOAD_DEREF               'self'
             2224  LOAD_ATTR                survinfo

 L. 823      2226  LOAD_FAST                '_wdinl'
             2228  LOAD_FAST                '_wdxl'
             2230  LOAD_FAST                '_wdz'

 L. 824      2232  LOAD_CONST               False
             2234  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2236  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2238  LOAD_CONST               None
             2240  LOAD_CONST               None
             2242  BUILD_SLICE_2         2 
             2244  LOAD_CONST               3
             2246  LOAD_CONST               None
             2248  BUILD_SLICE_2         2 
             2250  BUILD_TUPLE_2         2 
             2252  BINARY_SUBSCR    
             2254  LOAD_FAST                '_traindict'
             2256  LOAD_FAST                '_weight'
             2258  STORE_SUBSCR     
           2260_0  COME_FROM          2200  '2200'
           2260_1  COME_FROM          2190  '2190'

 L. 825      2260  LOAD_DEREF               'self'
             2262  LOAD_ATTR                traindataconfig
             2264  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2266  BINARY_SUBSCR    
         2268_2270  POP_JUMP_IF_FALSE  2352  'to 2352'

 L. 826      2272  SETUP_LOOP         2352  'to 2352'
             2274  LOAD_FAST                '_features'
             2276  GET_ITER         
           2278_0  COME_FROM          2306  '2306'
             2278  FOR_ITER           2350  'to 2350'
             2280  STORE_FAST               'f'

 L. 827      2282  LOAD_GLOBAL              ml_aug
             2284  LOAD_METHOD              removeInvariantFeature
             2286  LOAD_FAST                '_traindict'
             2288  LOAD_FAST                'f'
             2290  CALL_METHOD_2         2  '2 positional arguments'
             2292  STORE_FAST               '_traindict'

 L. 828      2294  LOAD_GLOBAL              basic_mdt
             2296  LOAD_METHOD              maxDictConstantRow
             2298  LOAD_FAST                '_traindict'
             2300  CALL_METHOD_1         1  '1 positional argument'
             2302  LOAD_CONST               0
             2304  COMPARE_OP               <=
         2306_2308  POP_JUMP_IF_FALSE  2278  'to 2278'

 L. 829      2310  LOAD_GLOBAL              vis_msg
             2312  LOAD_ATTR                print
             2314  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: No training sample found'

 L. 830      2316  LOAD_STR                 'error'
             2318  LOAD_CONST               ('type',)
             2320  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2322  POP_TOP          

 L. 831      2324  LOAD_GLOBAL              QtWidgets
             2326  LOAD_ATTR                QMessageBox
             2328  LOAD_METHOD              critical
             2330  LOAD_DEREF               'self'
             2332  LOAD_ATTR                msgbox

 L. 832      2334  LOAD_STR                 'Train 2D-CAE'

 L. 833      2336  LOAD_STR                 'No training sample found'
             2338  CALL_METHOD_3         3  '3 positional arguments'
             2340  POP_TOP          

 L. 834      2342  LOAD_CONST               None
             2344  RETURN_VALUE     
         2346_2348  JUMP_BACK          2278  'to 2278'
             2350  POP_BLOCK        
           2352_0  COME_FROM_LOOP     2272  '2272'
           2352_1  COME_FROM          2268  '2268'

 L. 835      2352  LOAD_DEREF               'self'
             2354  LOAD_ATTR                traindataconfig
             2356  LOAD_STR                 'RemoveZeroWeight_Checked'
             2358  BINARY_SUBSCR    
         2360_2362  POP_JUMP_IF_FALSE  2428  'to 2428'

 L. 836      2364  LOAD_GLOBAL              ml_aug
             2366  LOAD_METHOD              removeZeroWeight
             2368  LOAD_FAST                '_traindict'
             2370  LOAD_FAST                '_weight'
             2372  CALL_METHOD_2         2  '2 positional arguments'
             2374  STORE_FAST               '_traindict'

 L. 837      2376  LOAD_GLOBAL              basic_mdt
             2378  LOAD_METHOD              maxDictConstantRow
             2380  LOAD_FAST                '_traindict'
             2382  CALL_METHOD_1         1  '1 positional argument'
             2384  LOAD_CONST               0
             2386  COMPARE_OP               <=
         2388_2390  POP_JUMP_IF_FALSE  2428  'to 2428'

 L. 838      2392  LOAD_GLOBAL              vis_msg
             2394  LOAD_ATTR                print
             2396  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: No training sample found'

 L. 839      2398  LOAD_STR                 'error'
             2400  LOAD_CONST               ('type',)
             2402  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2404  POP_TOP          

 L. 840      2406  LOAD_GLOBAL              QtWidgets
             2408  LOAD_ATTR                QMessageBox
             2410  LOAD_METHOD              critical
             2412  LOAD_DEREF               'self'
             2414  LOAD_ATTR                msgbox

 L. 841      2416  LOAD_STR                 'Train 2D-CAE'

 L. 842      2418  LOAD_STR                 'No training sample found'
             2420  CALL_METHOD_3         3  '3 positional arguments'
             2422  POP_TOP          

 L. 843      2424  LOAD_CONST               None
             2426  RETURN_VALUE     
           2428_0  COME_FROM          2388  '2388'
           2428_1  COME_FROM          2360  '2360'

 L. 845      2428  LOAD_GLOBAL              np
             2430  LOAD_METHOD              shape
             2432  LOAD_FAST                '_traindict'
             2434  LOAD_FAST                '_target'
             2436  BINARY_SUBSCR    
             2438  CALL_METHOD_1         1  '1 positional argument'
             2440  LOAD_CONST               0
             2442  BINARY_SUBSCR    
             2444  LOAD_CONST               0
             2446  COMPARE_OP               <=
         2448_2450  POP_JUMP_IF_FALSE  2488  'to 2488'

 L. 846      2452  LOAD_GLOBAL              vis_msg
             2454  LOAD_ATTR                print
             2456  LOAD_STR                 'ERROR in TrainMl2DWcaeFromExisting: No training sample found'

 L. 847      2458  LOAD_STR                 'error'
             2460  LOAD_CONST               ('type',)
             2462  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2464  POP_TOP          

 L. 848      2466  LOAD_GLOBAL              QtWidgets
             2468  LOAD_ATTR                QMessageBox
             2470  LOAD_METHOD              critical
             2472  LOAD_DEREF               'self'
             2474  LOAD_ATTR                msgbox

 L. 849      2476  LOAD_STR                 'Train 2D-WCAE'

 L. 850      2478  LOAD_STR                 'No training sample found'
             2480  CALL_METHOD_3         3  '3 positional arguments'
             2482  POP_TOP          

 L. 851      2484  LOAD_CONST               None
             2486  RETURN_VALUE     
           2488_0  COME_FROM          2448  '2448'

 L. 853      2488  LOAD_FAST                '_image_height_new'
             2490  LOAD_FAST                '_image_height'
             2492  COMPARE_OP               !=
         2494_2496  POP_JUMP_IF_TRUE   2508  'to 2508'
             2498  LOAD_FAST                '_image_width_new'
             2500  LOAD_FAST                '_image_width'
             2502  COMPARE_OP               !=
         2504_2506  POP_JUMP_IF_FALSE  2642  'to 2642'
           2508_0  COME_FROM          2494  '2494'

 L. 854      2508  SETUP_LOOP         2552  'to 2552'
             2510  LOAD_FAST                '_features'
             2512  GET_ITER         
             2514  FOR_ITER           2550  'to 2550'
             2516  STORE_FAST               'f'

 L. 855      2518  LOAD_GLOBAL              basic_image
             2520  LOAD_ATTR                changeImageSize
             2522  LOAD_FAST                '_traindict'
             2524  LOAD_FAST                'f'
             2526  BINARY_SUBSCR    

 L. 856      2528  LOAD_FAST                '_image_height'

 L. 857      2530  LOAD_FAST                '_image_width'

 L. 858      2532  LOAD_FAST                '_image_height_new'

 L. 859      2534  LOAD_FAST                '_image_width_new'
             2536  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2538  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2540  LOAD_FAST                '_traindict'
             2542  LOAD_FAST                'f'
             2544  STORE_SUBSCR     
         2546_2548  JUMP_BACK          2514  'to 2514'
             2550  POP_BLOCK        
           2552_0  COME_FROM_LOOP     2508  '2508'

 L. 860      2552  LOAD_FAST                '_target'
             2554  LOAD_FAST                '_features'
             2556  COMPARE_OP               not-in
         2558_2560  POP_JUMP_IF_FALSE  2592  'to 2592'

 L. 861      2562  LOAD_GLOBAL              basic_image
             2564  LOAD_ATTR                changeImageSize
             2566  LOAD_FAST                '_traindict'
             2568  LOAD_FAST                '_target'
             2570  BINARY_SUBSCR    

 L. 862      2572  LOAD_FAST                '_image_height'

 L. 863      2574  LOAD_FAST                '_image_width'

 L. 864      2576  LOAD_FAST                '_image_height_new'

 L. 865      2578  LOAD_FAST                '_image_width_new'
             2580  LOAD_STR                 'linear'
             2582  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2584  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2586  LOAD_FAST                '_traindict'
             2588  LOAD_FAST                '_target'
             2590  STORE_SUBSCR     
           2592_0  COME_FROM          2558  '2558'

 L. 866      2592  LOAD_FAST                '_weight'
             2594  LOAD_FAST                '_features'
             2596  COMPARE_OP               not-in
         2598_2600  POP_JUMP_IF_FALSE  2642  'to 2642'
             2602  LOAD_FAST                '_weight'
             2604  LOAD_FAST                '_target'
             2606  COMPARE_OP               !=
         2608_2610  POP_JUMP_IF_FALSE  2642  'to 2642'

 L. 867      2612  LOAD_GLOBAL              basic_image
             2614  LOAD_ATTR                changeImageSize
             2616  LOAD_FAST                '_traindict'
             2618  LOAD_FAST                '_weight'
             2620  BINARY_SUBSCR    

 L. 868      2622  LOAD_FAST                '_image_height'

 L. 869      2624  LOAD_FAST                '_image_width'

 L. 870      2626  LOAD_FAST                '_image_height_new'

 L. 871      2628  LOAD_FAST                '_image_width_new'
             2630  LOAD_STR                 'linear'
             2632  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2634  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2636  LOAD_FAST                '_traindict'
             2638  LOAD_FAST                '_weight'
             2640  STORE_SUBSCR     
           2642_0  COME_FROM          2608  '2608'
           2642_1  COME_FROM          2598  '2598'
           2642_2  COME_FROM          2504  '2504'

 L. 872      2642  LOAD_DEREF               'self'
             2644  LOAD_ATTR                traindataconfig
             2646  LOAD_STR                 'RotateFeature_Checked'
             2648  BINARY_SUBSCR    
             2650  LOAD_CONST               True
             2652  COMPARE_OP               is
         2654_2656  POP_JUMP_IF_FALSE  2872  'to 2872'

 L. 873      2658  SETUP_LOOP         2730  'to 2730'
             2660  LOAD_FAST                '_features'
             2662  GET_ITER         
             2664  FOR_ITER           2728  'to 2728'
             2666  STORE_FAST               'f'

 L. 874      2668  LOAD_FAST                '_image_height_new'
             2670  LOAD_FAST                '_image_width_new'
             2672  COMPARE_OP               ==
         2674_2676  POP_JUMP_IF_FALSE  2702  'to 2702'

 L. 875      2678  LOAD_GLOBAL              ml_aug
             2680  LOAD_METHOD              rotateImage6Way
             2682  LOAD_FAST                '_traindict'
             2684  LOAD_FAST                'f'
             2686  BINARY_SUBSCR    
             2688  LOAD_FAST                '_image_height_new'
             2690  LOAD_FAST                '_image_width_new'
             2692  CALL_METHOD_3         3  '3 positional arguments'
             2694  LOAD_FAST                '_traindict'
             2696  LOAD_FAST                'f'
             2698  STORE_SUBSCR     
             2700  JUMP_BACK          2664  'to 2664'
           2702_0  COME_FROM          2674  '2674'

 L. 877      2702  LOAD_GLOBAL              ml_aug
             2704  LOAD_METHOD              rotateImage4Way
             2706  LOAD_FAST                '_traindict'
             2708  LOAD_FAST                'f'
             2710  BINARY_SUBSCR    
             2712  LOAD_FAST                '_image_height_new'
             2714  LOAD_FAST                '_image_width_new'
             2716  CALL_METHOD_3         3  '3 positional arguments'
             2718  LOAD_FAST                '_traindict'
             2720  LOAD_FAST                'f'
             2722  STORE_SUBSCR     
         2724_2726  JUMP_BACK          2664  'to 2664'
             2728  POP_BLOCK        
           2730_0  COME_FROM_LOOP     2658  '2658'

 L. 878      2730  LOAD_FAST                '_target'
             2732  LOAD_FAST                '_features'
             2734  COMPARE_OP               not-in
         2736_2738  POP_JUMP_IF_FALSE  2796  'to 2796'

 L. 879      2740  LOAD_FAST                '_image_height_new'
             2742  LOAD_FAST                '_image_width_new'
             2744  COMPARE_OP               ==
         2746_2748  POP_JUMP_IF_FALSE  2774  'to 2774'

 L. 881      2750  LOAD_GLOBAL              ml_aug
             2752  LOAD_METHOD              rotateImage6Way
             2754  LOAD_FAST                '_traindict'
             2756  LOAD_FAST                '_target'
             2758  BINARY_SUBSCR    
             2760  LOAD_FAST                '_image_height_new'
             2762  LOAD_FAST                '_image_width_new'
             2764  CALL_METHOD_3         3  '3 positional arguments'
             2766  LOAD_FAST                '_traindict'
             2768  LOAD_FAST                '_target'
             2770  STORE_SUBSCR     
             2772  JUMP_FORWARD       2796  'to 2796'
           2774_0  COME_FROM          2746  '2746'

 L. 884      2774  LOAD_GLOBAL              ml_aug
             2776  LOAD_METHOD              rotateImage4Way
             2778  LOAD_FAST                '_traindict'
             2780  LOAD_FAST                '_target'
             2782  BINARY_SUBSCR    
             2784  LOAD_FAST                '_image_height_new'
             2786  LOAD_FAST                '_image_width_new'
             2788  CALL_METHOD_3         3  '3 positional arguments'
             2790  LOAD_FAST                '_traindict'
             2792  LOAD_FAST                '_target'
             2794  STORE_SUBSCR     
           2796_0  COME_FROM          2772  '2772'
           2796_1  COME_FROM          2736  '2736'

 L. 885      2796  LOAD_FAST                '_weight'
             2798  LOAD_FAST                '_features'
             2800  COMPARE_OP               not-in
         2802_2804  POP_JUMP_IF_FALSE  2872  'to 2872'
             2806  LOAD_FAST                '_weight'
             2808  LOAD_FAST                '_target'
             2810  COMPARE_OP               !=
         2812_2814  POP_JUMP_IF_FALSE  2872  'to 2872'

 L. 886      2816  LOAD_FAST                '_image_height_new'
             2818  LOAD_FAST                '_image_width_new'
             2820  COMPARE_OP               ==
         2822_2824  POP_JUMP_IF_FALSE  2850  'to 2850'

 L. 888      2826  LOAD_GLOBAL              ml_aug
             2828  LOAD_METHOD              rotateImage6Way
             2830  LOAD_FAST                '_traindict'
             2832  LOAD_FAST                '_weight'
             2834  BINARY_SUBSCR    
             2836  LOAD_FAST                '_image_height_new'
             2838  LOAD_FAST                '_image_width_new'
             2840  CALL_METHOD_3         3  '3 positional arguments'
             2842  LOAD_FAST                '_traindict'
             2844  LOAD_FAST                '_weight'
             2846  STORE_SUBSCR     
             2848  JUMP_FORWARD       2872  'to 2872'
           2850_0  COME_FROM          2822  '2822'

 L. 891      2850  LOAD_GLOBAL              ml_aug
             2852  LOAD_METHOD              rotateImage4Way
             2854  LOAD_FAST                '_traindict'
             2856  LOAD_FAST                '_weight'
             2858  BINARY_SUBSCR    
             2860  LOAD_FAST                '_image_height_new'
             2862  LOAD_FAST                '_image_width_new'
             2864  CALL_METHOD_3         3  '3 positional arguments'
             2866  LOAD_FAST                '_traindict'
             2868  LOAD_FAST                '_weight'
             2870  STORE_SUBSCR     
           2872_0  COME_FROM          2848  '2848'
           2872_1  COME_FROM          2812  '2812'
           2872_2  COME_FROM          2802  '2802'
           2872_3  COME_FROM          2654  '2654'

 L. 894      2872  LOAD_GLOBAL              print
             2874  LOAD_STR                 'TrainMl2DWcaeFromExisting: A total of %d valid training samples'
             2876  LOAD_GLOBAL              basic_mdt
             2878  LOAD_METHOD              maxDictConstantRow

 L. 895      2880  LOAD_FAST                '_traindict'
             2882  CALL_METHOD_1         1  '1 positional argument'
             2884  BINARY_MODULO    
             2886  CALL_FUNCTION_1       1  '1 positional argument'
             2888  POP_TOP          

 L. 897      2890  LOAD_GLOBAL              print
             2892  LOAD_STR                 'TrainMl2DWcaeFromExisting: Step 3 - Start training'
             2894  CALL_FUNCTION_1       1  '1 positional argument'
             2896  POP_TOP          

 L. 899      2898  LOAD_GLOBAL              QtWidgets
             2900  LOAD_METHOD              QProgressDialog
             2902  CALL_METHOD_0         0  '0 positional arguments'
             2904  STORE_FAST               '_pgsdlg'

 L. 900      2906  LOAD_GLOBAL              QtGui
             2908  LOAD_METHOD              QIcon
             2910  CALL_METHOD_0         0  '0 positional arguments'
             2912  STORE_FAST               'icon'

 L. 901      2914  LOAD_FAST                'icon'
             2916  LOAD_METHOD              addPixmap
             2918  LOAD_GLOBAL              QtGui
             2920  LOAD_METHOD              QPixmap
             2922  LOAD_GLOBAL              os
             2924  LOAD_ATTR                path
             2926  LOAD_METHOD              join
             2928  LOAD_DEREF               'self'
             2930  LOAD_ATTR                iconpath
             2932  LOAD_STR                 'icons/new.png'
             2934  CALL_METHOD_2         2  '2 positional arguments'
             2936  CALL_METHOD_1         1  '1 positional argument'

 L. 902      2938  LOAD_GLOBAL              QtGui
             2940  LOAD_ATTR                QIcon
             2942  LOAD_ATTR                Normal
             2944  LOAD_GLOBAL              QtGui
             2946  LOAD_ATTR                QIcon
             2948  LOAD_ATTR                Off
             2950  CALL_METHOD_3         3  '3 positional arguments'
             2952  POP_TOP          

 L. 903      2954  LOAD_FAST                '_pgsdlg'
             2956  LOAD_METHOD              setWindowIcon
             2958  LOAD_FAST                'icon'
             2960  CALL_METHOD_1         1  '1 positional argument'
             2962  POP_TOP          

 L. 904      2964  LOAD_FAST                '_pgsdlg'
             2966  LOAD_METHOD              setWindowTitle
             2968  LOAD_STR                 'Train 2D-CAE'
             2970  CALL_METHOD_1         1  '1 positional argument'
             2972  POP_TOP          

 L. 905      2974  LOAD_FAST                '_pgsdlg'
             2976  LOAD_METHOD              setCancelButton
             2978  LOAD_CONST               None
             2980  CALL_METHOD_1         1  '1 positional argument'
             2982  POP_TOP          

 L. 906      2984  LOAD_FAST                '_pgsdlg'
             2986  LOAD_METHOD              setWindowFlags
             2988  LOAD_GLOBAL              QtCore
             2990  LOAD_ATTR                Qt
             2992  LOAD_ATTR                WindowStaysOnTopHint
             2994  CALL_METHOD_1         1  '1 positional argument'
             2996  POP_TOP          

 L. 907      2998  LOAD_FAST                '_pgsdlg'
             3000  LOAD_METHOD              forceShow
             3002  CALL_METHOD_0         0  '0 positional arguments'
             3004  POP_TOP          

 L. 908      3006  LOAD_FAST                '_pgsdlg'
             3008  LOAD_METHOD              setFixedWidth
             3010  LOAD_CONST               400
             3012  CALL_METHOD_1         1  '1 positional argument'
             3014  POP_TOP          

 L. 909      3016  LOAD_GLOBAL              ml_wcae
             3018  LOAD_ATTR                createWCAEReconstructorFromExisting
             3020  LOAD_FAST                '_traindict'

 L. 910      3022  LOAD_FAST                '_image_height_new'
             3024  LOAD_FAST                '_image_width_new'

 L. 911      3026  LOAD_FAST                '_features'
             3028  LOAD_FAST                '_target'
             3030  LOAD_FAST                '_weight'

 L. 912      3032  LOAD_FAST                '_nepoch'
             3034  LOAD_FAST                '_batchsize'

 L. 913      3036  LOAD_FAST                '_nconvblock'
             3038  LOAD_FAST                '_nconvfeature'

 L. 914      3040  LOAD_FAST                '_nconvlayer'

 L. 915      3042  LOAD_FAST                '_n1x1layer'
             3044  LOAD_FAST                '_n1x1feature'

 L. 916      3046  LOAD_FAST                '_pool_height'
             3048  LOAD_FAST                '_pool_width'

 L. 917      3050  LOAD_FAST                '_learning_rate'

 L. 918      3052  LOAD_FAST                '_dropout_prob'

 L. 919      3054  LOAD_CONST               True

 L. 920      3056  LOAD_FAST                '_savepath'
             3058  LOAD_FAST                '_savename'

 L. 921      3060  LOAD_FAST                '_pgsdlg'

 L. 922      3062  LOAD_FAST                '_precnnpath'

 L. 923      3064  LOAD_FAST                '_precnnname'

 L. 924      3066  LOAD_FAST                '_blockidx'
             3068  LOAD_FAST                '_layeridx'

 L. 925      3070  LOAD_FAST                '_trainable'
             3072  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'weight', 'nepoch', 'batchsize', 'nconvblock', 'nconvfeature', 'nconvlayer', 'n1x1layer', 'n1x1feature', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprob', 'save2disk', 'savepath', 'savename', 'qpgsdlg', 'precnnpath', 'precnnname', 'blockidx', 'layeridx', 'trainable')
             3074  CALL_FUNCTION_KW_26    26  '26 total positional and keyword args'
             3076  STORE_FAST               '_caelog'

 L. 928      3078  LOAD_GLOBAL              QtWidgets
             3080  LOAD_ATTR                QMessageBox
             3082  LOAD_METHOD              information
             3084  LOAD_DEREF               'self'
             3086  LOAD_ATTR                msgbox

 L. 929      3088  LOAD_STR                 'Train 2D-WCAE'

 L. 930      3090  LOAD_STR                 'WCAE trained successfully'
             3092  CALL_METHOD_3         3  '3 positional arguments'
             3094  POP_TOP          

 L. 932      3096  LOAD_GLOBAL              QtWidgets
             3098  LOAD_ATTR                QMessageBox
             3100  LOAD_METHOD              question
             3102  LOAD_DEREF               'self'
             3104  LOAD_ATTR                msgbox
             3106  LOAD_STR                 'Train 2D-WCAE'
             3108  LOAD_STR                 'View learning matrix?'

 L. 933      3110  LOAD_GLOBAL              QtWidgets
             3112  LOAD_ATTR                QMessageBox
             3114  LOAD_ATTR                Yes
             3116  LOAD_GLOBAL              QtWidgets
             3118  LOAD_ATTR                QMessageBox
             3120  LOAD_ATTR                No
             3122  BINARY_OR        

 L. 934      3124  LOAD_GLOBAL              QtWidgets
             3126  LOAD_ATTR                QMessageBox
             3128  LOAD_ATTR                Yes
             3130  CALL_METHOD_5         5  '5 positional arguments'
             3132  STORE_FAST               'reply'

 L. 936      3134  LOAD_FAST                'reply'
             3136  LOAD_GLOBAL              QtWidgets
             3138  LOAD_ATTR                QMessageBox
             3140  LOAD_ATTR                Yes
             3142  COMPARE_OP               ==
         3144_3146  POP_JUMP_IF_FALSE  3214  'to 3214'

 L. 937      3148  LOAD_GLOBAL              QtWidgets
             3150  LOAD_METHOD              QDialog
             3152  CALL_METHOD_0         0  '0 positional arguments'
             3154  STORE_FAST               '_viewmllearnmat'

 L. 938      3156  LOAD_GLOBAL              gui_viewmllearnmat
             3158  CALL_FUNCTION_0       0  '0 positional arguments'
             3160  STORE_FAST               '_gui'

 L. 939      3162  LOAD_FAST                '_caelog'
             3164  LOAD_STR                 'learning_curve'
             3166  BINARY_SUBSCR    
             3168  LOAD_FAST                '_gui'
             3170  STORE_ATTR               learnmat

 L. 940      3172  LOAD_DEREF               'self'
             3174  LOAD_ATTR                linestyle
             3176  LOAD_FAST                '_gui'
             3178  STORE_ATTR               linestyle

 L. 941      3180  LOAD_DEREF               'self'
             3182  LOAD_ATTR                fontstyle
             3184  LOAD_FAST                '_gui'
             3186  STORE_ATTR               fontstyle

 L. 942      3188  LOAD_FAST                '_gui'
             3190  LOAD_METHOD              setupGUI
             3192  LOAD_FAST                '_viewmllearnmat'
             3194  CALL_METHOD_1         1  '1 positional argument'
             3196  POP_TOP          

 L. 943      3198  LOAD_FAST                '_viewmllearnmat'
             3200  LOAD_METHOD              exec
             3202  CALL_METHOD_0         0  '0 positional arguments'
             3204  POP_TOP          

 L. 944      3206  LOAD_FAST                '_viewmllearnmat'
             3208  LOAD_METHOD              show
             3210  CALL_METHOD_0         0  '0 positional arguments'
             3212  POP_TOP          
           3214_0  COME_FROM          3144  '3144'

Parse error at or near `POP_TOP' instruction at offset 3212

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
    TrainMl2DWcaeFromExisting = QtWidgets.QWidget()
    gui = trainml2dwcaefromexisting()
    gui.setupGUI(TrainMl2DWcaeFromExisting)
    TrainMl2DWcaeFromExisting.show()
    sys.exit(app.exec_())