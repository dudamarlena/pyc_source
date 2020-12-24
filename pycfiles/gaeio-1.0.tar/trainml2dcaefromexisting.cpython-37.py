# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml2dcaefromexisting.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 53603 bytes
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
import cognitivegeo.src.ml.caereconstructor as ml_cae
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml2dcaefromexisting(object):
    survinfo = {}
    seisdata = {}
    pointsetdata = {}
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    rootpath = ''
    iconpath = os.path.dirname(__file__)
    dialog = None
    featurelist = list()
    traindataconfig = {}
    traindataconfig['TrainPointSet'] = []
    traindataconfig['RotateFeature_Enabled'] = True
    traindataconfig['RotateFeature_Checked'] = False
    traindataconfig['RemoveInvariantFeature_Enabled'] = True
    traindataconfig['RemoveInvariantFeature_Checked'] = False

    def setupGUI(self, TrainMl2DCaeFromExisting):
        TrainMl2DCaeFromExisting.setObjectName('TrainMl2DCaeFromExisting')
        TrainMl2DCaeFromExisting.setFixedSize(800, 630)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl2DCaeFromExisting.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl2DCaeFromExisting)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl2DCaeFromExisting)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl2DCaeFromExisting)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblexisting = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblexisting.setObjectName('lblexisting')
        self.lblexisting.setGeometry(QtCore.QRect(410, 50, 100, 30))
        self.ldtexisting = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtexisting.setObjectName('ldtexisting')
        self.ldtexisting.setGeometry(QtCore.QRect(510, 50, 210, 30))
        self.btnexisting = QtWidgets.QPushButton(TrainMl2DCaeFromExisting)
        self.btnexisting.setObjectName('btnexisting')
        self.btnexisting.setGeometry(QtCore.QRect(730, 50, 60, 30))
        self.lblnconvblockexisting = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblnconvblockexisting.setObjectName('lblnconvblockexisting')
        self.lblnconvblockexisting.setGeometry(QtCore.QRect(410, 90, 130, 30))
        self.ldtnconvblockexisting = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtnconvblockexisting.setObjectName('ldtnconvblockexisting')
        self.ldtnconvblockexisting.setGeometry(QtCore.QRect(550, 90, 40, 30))
        self.twgnconvblockexisting = QtWidgets.QTableWidget(TrainMl2DCaeFromExisting)
        self.twgnconvblockexisting.setObjectName('twgnconvblockexisting')
        self.twgnconvblockexisting.setGeometry(QtCore.QRect(610, 90, 180, 150))
        self.twgnconvblockexisting.setColumnCount(3)
        self.twgnconvblockexisting.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblockexisting.verticalHeader().hide()
        self.lblblockid = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblblockid.setObjectName('lblblockid')
        self.lblblockid.setGeometry(QtCore.QRect(410, 130, 130, 30))
        self.cbbblockid = QtWidgets.QComboBox(TrainMl2DCaeFromExisting)
        self.cbbblockid.setObjectName('cbbblockid')
        self.cbbblockid.setGeometry(QtCore.QRect(550, 130, 40, 30))
        self.lbllayerid = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lbllayerid.setObjectName('lbllayerid')
        self.lbllayerid.setGeometry(QtCore.QRect(410, 170, 130, 30))
        self.cbblayerid = QtWidgets.QComboBox(TrainMl2DCaeFromExisting)
        self.cbblayerid.setObjectName('cbblayerid')
        self.cbblayerid.setGeometry(QtCore.QRect(550, 170, 40, 30))
        self.lbltrainable = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lbltrainable.setObjectName('lbltrainable')
        self.lbltrainable.setGeometry(QtCore.QRect(410, 210, 130, 30))
        self.cbbtrainable = QtWidgets.QComboBox(TrainMl2DCaeFromExisting)
        self.cbbtrainable.setObjectName('cbbtrainable')
        self.cbbtrainable.setGeometry(QtCore.QRect(550, 210, 40, 30))
        self.lblappend = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblappend.setObjectName('lblappend')
        self.lblappend.setGeometry(QtCore.QRect(410, 250, 200, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 290, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 290, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl2DCaeFromExisting)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 330, 180, 200))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 290, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 290, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(TrainMl2DCaeFromExisting)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 330, 180, 200))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 540, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 540, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 540, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 580, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 580, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 540, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 540, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 540, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 580, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 580, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl2DCaeFromExisting)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 310, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 350, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.lbldropout = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 390, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 390, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl2DCaeFromExisting)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl2DCaeFromExisting)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 440, 180, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl2DCaeFromExisting)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 440, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl2DCaeFromExisting)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(120, 580, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl2DCaeFromExisting)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl2DCaeFromExisting.geometry().center().x()
        _center_y = TrainMl2DCaeFromExisting.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl2DCaeFromExisting)
        QtCore.QMetaObject.connectSlotsByName(TrainMl2DCaeFromExisting)

    def retranslateGUI(self, TrainMl2DCaeFromExisting):
        self.dialog = TrainMl2DCaeFromExisting
        _translate = QtCore.QCoreApplication.translate
        TrainMl2DCaeFromExisting.setWindowTitle(_translate('TrainMl2DCaeFromExisting', 'Train 2D-CAE from pre-trained'))
        self.lblfeature.setText(_translate('TrainMl2DCaeFromExisting', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl2DCaeFromExisting', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl2DCaeFromExisting', 'Select target:'))
        self.btnconfigtraindata.setText(_translate('TrainMl2DDcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('TrainMl2DCaeFromExisting', 'Original\nimage\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl2DCaeFromExisting', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl2DCaeFromExisting', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl2DCaeFromExisting', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl2DCaeFromExisting', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl2DCaeFromExisting', 'Interpolated\nimage\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl2DCaeFromExisting', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl2DCaeFromExisting', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl2DCaeFromExisting', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl2DCaeFromExisting', '32'))
        self.ldtnewwidth.setAlignment(QtCore.Qt.AlignCenter)
        if self.checkSurvInfo():
            self.featurelist.clear()
            self.lwgfeature.clear()
            self.cbbtarget.clear()
            _firstfeature = None
            for i in sorted(self.seisdata.keys()):
                if self.checkSeisData(i):
                    self.featurelist.append(i)
                    item = QtWidgets.QListWidgetItem(self.lwgfeature)
                    item.setText(_translate('TrainMl2DCaeFromExisting', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl2DCaeFromExisting', 'Specify CAE architecture:'))
        self.lblexisting.setText(_translate('TrainMl2DCaeFromExisting', 'Select pre-trained:'))
        self.ldtexisting.setText(_translate('TrainMl2DCaeFromExisting', ''))
        self.ldtexisting.textChanged.connect(self.changeLdtExisting)
        self.btnexisting.setText(_translate('TrainMl2DCaeFromExisting', 'Browse'))
        self.btnexisting.clicked.connect(self.clickBtnExisting)
        self.lblnconvblockexisting.setText(_translate('TrainMl2DCaeFromExisting', 'Available conv. blocks:'))
        self.lblnconvblockexisting.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblockexisting.setText(_translate('TrainMl2DCaeFromExisting', ''))
        self.ldtnconvblockexisting.setEnabled(False)
        self.ldtnconvblockexisting.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblockexisting.textChanged.connect(self.changeLdtNconvblockExisting)
        self.twgnconvblockexisting.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblblockid.setText(_translate('TrainMl2DCaeFromExisting', 'Select conv. block ID:'))
        self.lblblockid.setAlignment(QtCore.Qt.AlignRight)
        self.cbbblockid.currentIndexChanged.connect(self.changeCbbBlockid)
        self.lbllayerid.setText(_translate('TrainMl2DCaeFromExisting', 'Select conv. layer ID:'))
        self.lbllayerid.setAlignment(QtCore.Qt.AlignRight)
        self.lbltrainable.setText(_translate('TrainMl2DCaeFromExisting', 'Is trainable?:'))
        self.lbltrainable.setAlignment(QtCore.Qt.AlignRight)
        self.cbbtrainable.addItems(['Yes', 'No'])
        self.lblappend.setText(_translate('TrainMl2DCaeFromExisting', 'Append more blocks & layers:'))
        self.lblnconvblock.setText(_translate('TrainMl2DCaeFromExisting', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl2DCaeFromExisting', '2'))
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

        self.lbln1x1layer.setText(_translate('TrainMl2DCaeFromExisting', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('TrainMl2DCaeFromExisting', '2'))
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.twgn1x1layer.setRowCount(2)
        for _idx in range(int(self.ldtn1x1layer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl2DCaeFromExisting', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgn1x1layer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgn1x1layer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl2DCaeFromExisting', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl2DCaeFromExisting', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl2DCaeFromExisting', ''))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskheight.setEnabled(False)
        self.lblmaskwidth.setText(_translate('TrainMl2DCaeFromExisting', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl2DCaeFromExisting', ''))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskwidth.setEnabled(False)
        self.lblpoolsize.setText(_translate('TrainMl2DCaeFromExisting', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl2DCaeFromExisting', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl2DCaeFromExisting', ''))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl2DCaeFromExisting', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl2DCaeFromExisting', ''))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('TrainMl2DCaeFromExisting', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl2DCaeFromExisting', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl2DCaeFromExisting', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl2DCaeFromExisting', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl2DCaeFromExisting', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl2DCaeFromExisting', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl2DCaeFromExisting', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('TrainMl2DCaeFromExisting', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('TrainMl2DCaeFromExisting', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl2DCaeFromExisting', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl2DCaeFromExisting', ''))
        self.btnsave.setText(_translate('TrainMl2DCaeFromExisting', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl2DCaeFromExisting', 'Train 2D-CAE'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl2DCaeFromExisting)

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

    def clickBtnTrainMl2DCaeFromExisting--- This code section failed: ---

 L. 597         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 599         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 600        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 601        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 602        50  LOAD_STR                 'Train 2D-CAE'

 L. 603        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 604        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 606        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_image_height'

 L. 607        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_image_width'

 L. 608        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtnewheight
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_image_height_new'

 L. 609       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewwidth
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_image_width_new'

 L. 610       126  LOAD_FAST                '_image_height'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'
              134  LOAD_FAST                '_image_width'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_TRUE    158  'to 158'

 L. 611       142  LOAD_FAST                '_image_height_new'
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

 L. 612       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 613       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 614       182  LOAD_STR                 'Train 2D-CAE'

 L. 615       184  LOAD_STR                 'Non-integer feature size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 616       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 617       194  LOAD_FAST                '_image_height'
              196  LOAD_CONST               2
              198  COMPARE_OP               <
              200  POP_JUMP_IF_TRUE    228  'to 228'
              202  LOAD_FAST                '_image_width'
              204  LOAD_CONST               2
              206  COMPARE_OP               <
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 618       210  LOAD_FAST                '_image_height_new'
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

 L. 619       228  LOAD_GLOBAL              vis_msg
              230  LOAD_ATTR                print
              232  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 620       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 621       252  LOAD_STR                 'Train 2D-CAE'

 L. 622       254  LOAD_STR                 'Features are not 2D'
              256  CALL_METHOD_3         3  '3 positional arguments'
              258  POP_TOP          

 L. 623       260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           224  '224'

 L. 625       264  LOAD_CONST               2
              266  LOAD_GLOBAL              int
              268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               2
              272  BINARY_TRUE_DIVIDE
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  BINARY_MULTIPLY  
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  STORE_FAST               '_image_height'

 L. 626       284  LOAD_CONST               2
              286  LOAD_GLOBAL              int
              288  LOAD_FAST                '_image_width'
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BINARY_MULTIPLY  
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               '_image_width'

 L. 628       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                lwgfeature
              308  LOAD_METHOD              selectedItems
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               '_features'

 L. 629       314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainml2dcaefromexisting.clickBtnTrainMl2DCaeFromExisting.<locals>.<listcomp>'
              318  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              320  LOAD_FAST                '_features'
              322  GET_ITER         
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               '_features'

 L. 630       328  LOAD_DEREF               'self'
              330  LOAD_ATTR                featurelist
              332  LOAD_DEREF               'self'
              334  LOAD_ATTR                cbbtarget
              336  LOAD_METHOD              currentIndex
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  BINARY_SUBSCR    
              342  STORE_FAST               '_target'

 L. 632       344  LOAD_GLOBAL              len
              346  LOAD_DEREF               'self'
              348  LOAD_ATTR                ldtexisting
              350  LOAD_METHOD              text
              352  CALL_METHOD_0         0  '0 positional arguments'
              354  CALL_FUNCTION_1       1  '1 positional argument'
              356  LOAD_CONST               1
              358  COMPARE_OP               <
          360_362  POP_JUMP_IF_FALSE   400  'to 400'

 L. 633       364  LOAD_GLOBAL              vis_msg
              366  LOAD_ATTR                print
              368  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: No name specified for pre-trained network'

 L. 634       370  LOAD_STR                 'error'
              372  LOAD_CONST               ('type',)
              374  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              376  POP_TOP          

 L. 635       378  LOAD_GLOBAL              QtWidgets
              380  LOAD_ATTR                QMessageBox
              382  LOAD_METHOD              critical
              384  LOAD_DEREF               'self'
              386  LOAD_ATTR                msgbox

 L. 636       388  LOAD_STR                 'Train 2D-CAE'

 L. 637       390  LOAD_STR                 'No name specified for pre-trained network'
              392  CALL_METHOD_3         3  '3 positional arguments'
              394  POP_TOP          

 L. 638       396  LOAD_CONST               None
              398  RETURN_VALUE     
            400_0  COME_FROM           360  '360'

 L. 639       400  LOAD_GLOBAL              os
              402  LOAD_ATTR                path
              404  LOAD_METHOD              dirname
              406  LOAD_DEREF               'self'
              408  LOAD_ATTR                ldtexisting
              410  LOAD_METHOD              text
              412  CALL_METHOD_0         0  '0 positional arguments'
              414  CALL_METHOD_1         1  '1 positional argument'
              416  STORE_FAST               '_precnnpath'

 L. 640       418  LOAD_GLOBAL              os
              420  LOAD_ATTR                path
              422  LOAD_METHOD              splitext
              424  LOAD_GLOBAL              os
              426  LOAD_ATTR                path
              428  LOAD_METHOD              basename
              430  LOAD_DEREF               'self'
              432  LOAD_ATTR                ldtexisting
              434  LOAD_METHOD              text
              436  CALL_METHOD_0         0  '0 positional arguments'
              438  CALL_METHOD_1         1  '1 positional argument'
              440  CALL_METHOD_1         1  '1 positional argument'
              442  LOAD_CONST               0
              444  BINARY_SUBSCR    
              446  STORE_FAST               '_precnnname'

 L. 641       448  LOAD_DEREF               'self'
              450  LOAD_ATTR                cbbblockid
              452  LOAD_METHOD              currentIndex
              454  CALL_METHOD_0         0  '0 positional arguments'
              456  STORE_FAST               '_blockidx'

 L. 642       458  LOAD_DEREF               'self'
              460  LOAD_ATTR                cbblayerid
              462  LOAD_METHOD              currentIndex
              464  CALL_METHOD_0         0  '0 positional arguments'
              466  STORE_FAST               '_layeridx'

 L. 643       468  LOAD_CONST               True
              470  STORE_FAST               '_trainable'

 L. 644       472  LOAD_DEREF               'self'
              474  LOAD_ATTR                cbbtrainable
              476  LOAD_METHOD              currentIndex
              478  CALL_METHOD_0         0  '0 positional arguments'
              480  LOAD_CONST               0
              482  COMPARE_OP               !=
          484_486  POP_JUMP_IF_FALSE   492  'to 492'

 L. 645       488  LOAD_CONST               False
              490  STORE_FAST               '_trainable'
            492_0  COME_FROM           484  '484'

 L. 647       492  LOAD_GLOBAL              ml_tfm
              494  LOAD_METHOD              getConvModelNChannel
              496  LOAD_FAST                '_precnnpath'
              498  LOAD_FAST                '_precnnname'
              500  CALL_METHOD_2         2  '2 positional arguments'
              502  LOAD_GLOBAL              len
              504  LOAD_FAST                '_features'
              506  CALL_FUNCTION_1       1  '1 positional argument'
              508  COMPARE_OP               !=
          510_512  POP_JUMP_IF_FALSE   550  'to 550'

 L. 648       514  LOAD_GLOBAL              vis_msg
              516  LOAD_ATTR                print
              518  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Feature channel number not match with pre-trained network'

 L. 649       520  LOAD_STR                 'error'
              522  LOAD_CONST               ('type',)
              524  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              526  POP_TOP          

 L. 650       528  LOAD_GLOBAL              QtWidgets
              530  LOAD_ATTR                QMessageBox
              532  LOAD_METHOD              critical
              534  LOAD_DEREF               'self'
              536  LOAD_ATTR                msgbox

 L. 651       538  LOAD_STR                 'Train 2D-CAE'

 L. 652       540  LOAD_STR                 'Feature channel number not match with pre-trained network'
              542  CALL_METHOD_3         3  '3 positional arguments'
              544  POP_TOP          

 L. 653       546  LOAD_CONST               None
              548  RETURN_VALUE     
            550_0  COME_FROM           510  '510'

 L. 655       550  LOAD_GLOBAL              basic_data
              552  LOAD_METHOD              str2int
              554  LOAD_DEREF               'self'
              556  LOAD_ATTR                ldtnconvblock
              558  LOAD_METHOD              text
              560  CALL_METHOD_0         0  '0 positional arguments'
              562  CALL_METHOD_1         1  '1 positional argument'
              564  STORE_FAST               '_nconvblock'

 L. 656       566  LOAD_CLOSURE             'self'
              568  BUILD_TUPLE_1         1 
              570  LOAD_LISTCOMP            '<code_object <listcomp>>'
              572  LOAD_STR                 'trainml2dcaefromexisting.clickBtnTrainMl2DCaeFromExisting.<locals>.<listcomp>'
              574  MAKE_FUNCTION_8          'closure'
              576  LOAD_GLOBAL              range
              578  LOAD_FAST                '_nconvblock'
              580  CALL_FUNCTION_1       1  '1 positional argument'
              582  GET_ITER         
              584  CALL_FUNCTION_1       1  '1 positional argument'
              586  STORE_FAST               '_nconvlayer'

 L. 657       588  LOAD_CLOSURE             'self'
              590  BUILD_TUPLE_1         1 
              592  LOAD_LISTCOMP            '<code_object <listcomp>>'
              594  LOAD_STR                 'trainml2dcaefromexisting.clickBtnTrainMl2DCaeFromExisting.<locals>.<listcomp>'
              596  MAKE_FUNCTION_8          'closure'
              598  LOAD_GLOBAL              range
              600  LOAD_FAST                '_nconvblock'
              602  CALL_FUNCTION_1       1  '1 positional argument'
              604  GET_ITER         
              606  CALL_FUNCTION_1       1  '1 positional argument'
              608  STORE_FAST               '_nconvfeature'

 L. 658       610  LOAD_GLOBAL              basic_data
              612  LOAD_METHOD              str2int
              614  LOAD_DEREF               'self'
              616  LOAD_ATTR                ldtn1x1layer
              618  LOAD_METHOD              text
              620  CALL_METHOD_0         0  '0 positional arguments'
              622  CALL_METHOD_1         1  '1 positional argument'
              624  STORE_FAST               '_n1x1layer'

 L. 659       626  LOAD_CLOSURE             'self'
              628  BUILD_TUPLE_1         1 
              630  LOAD_LISTCOMP            '<code_object <listcomp>>'
              632  LOAD_STR                 'trainml2dcaefromexisting.clickBtnTrainMl2DCaeFromExisting.<locals>.<listcomp>'
              634  MAKE_FUNCTION_8          'closure'
              636  LOAD_GLOBAL              range
              638  LOAD_FAST                '_n1x1layer'
              640  CALL_FUNCTION_1       1  '1 positional argument'
              642  GET_ITER         
              644  CALL_FUNCTION_1       1  '1 positional argument'
              646  STORE_FAST               '_n1x1feature'

 L. 660       648  LOAD_GLOBAL              basic_data
              650  LOAD_METHOD              str2int
              652  LOAD_DEREF               'self'
              654  LOAD_ATTR                ldtmaskheight
              656  LOAD_METHOD              text
              658  CALL_METHOD_0         0  '0 positional arguments'
              660  CALL_METHOD_1         1  '1 positional argument'
              662  STORE_FAST               '_patch_height'

 L. 661       664  LOAD_GLOBAL              basic_data
              666  LOAD_METHOD              str2int
              668  LOAD_DEREF               'self'
              670  LOAD_ATTR                ldtmaskwidth
              672  LOAD_METHOD              text
              674  CALL_METHOD_0         0  '0 positional arguments'
              676  CALL_METHOD_1         1  '1 positional argument'
              678  STORE_FAST               '_patch_width'

 L. 662       680  LOAD_GLOBAL              basic_data
              682  LOAD_METHOD              str2int
              684  LOAD_DEREF               'self'
              686  LOAD_ATTR                ldtpoolheight
              688  LOAD_METHOD              text
              690  CALL_METHOD_0         0  '0 positional arguments'
              692  CALL_METHOD_1         1  '1 positional argument'
              694  STORE_FAST               '_pool_height'

 L. 663       696  LOAD_GLOBAL              basic_data
              698  LOAD_METHOD              str2int
              700  LOAD_DEREF               'self'
              702  LOAD_ATTR                ldtpoolwidth
              704  LOAD_METHOD              text
              706  CALL_METHOD_0         0  '0 positional arguments'
              708  CALL_METHOD_1         1  '1 positional argument'
              710  STORE_FAST               '_pool_width'

 L. 664       712  LOAD_GLOBAL              basic_data
              714  LOAD_METHOD              str2int
              716  LOAD_DEREF               'self'
              718  LOAD_ATTR                ldtnepoch
              720  LOAD_METHOD              text
              722  CALL_METHOD_0         0  '0 positional arguments'
              724  CALL_METHOD_1         1  '1 positional argument'
              726  STORE_FAST               '_nepoch'

 L. 665       728  LOAD_GLOBAL              basic_data
              730  LOAD_METHOD              str2int
              732  LOAD_DEREF               'self'
              734  LOAD_ATTR                ldtbatchsize
              736  LOAD_METHOD              text
              738  CALL_METHOD_0         0  '0 positional arguments'
              740  CALL_METHOD_1         1  '1 positional argument'
              742  STORE_FAST               '_batchsize'

 L. 666       744  LOAD_GLOBAL              basic_data
              746  LOAD_METHOD              str2float
              748  LOAD_DEREF               'self'
              750  LOAD_ATTR                ldtlearnrate
              752  LOAD_METHOD              text
              754  CALL_METHOD_0         0  '0 positional arguments'
              756  CALL_METHOD_1         1  '1 positional argument'
              758  STORE_FAST               '_learning_rate'

 L. 667       760  LOAD_GLOBAL              basic_data
              762  LOAD_METHOD              str2float
              764  LOAD_DEREF               'self'
              766  LOAD_ATTR                ldtdropout
              768  LOAD_METHOD              text
              770  CALL_METHOD_0         0  '0 positional arguments'
              772  CALL_METHOD_1         1  '1 positional argument'
              774  STORE_FAST               '_dropout_prob'

 L. 668       776  LOAD_FAST                '_nconvblock'
              778  LOAD_CONST               False
              780  COMPARE_OP               is
          782_784  POP_JUMP_IF_TRUE    796  'to 796'
              786  LOAD_FAST                '_nconvblock'
              788  LOAD_CONST               0
              790  COMPARE_OP               <=
          792_794  POP_JUMP_IF_FALSE   832  'to 832'
            796_0  COME_FROM           782  '782'

 L. 669       796  LOAD_GLOBAL              vis_msg
              798  LOAD_ATTR                print
              800  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Non-positive convolutional block number'

 L. 670       802  LOAD_STR                 'error'
              804  LOAD_CONST               ('type',)
              806  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              808  POP_TOP          

 L. 671       810  LOAD_GLOBAL              QtWidgets
              812  LOAD_ATTR                QMessageBox
              814  LOAD_METHOD              critical
              816  LOAD_DEREF               'self'
              818  LOAD_ATTR                msgbox

 L. 672       820  LOAD_STR                 'Train 2D-CAE'

 L. 673       822  LOAD_STR                 'Non-positive convolutional block number'
              824  CALL_METHOD_3         3  '3 positional arguments'
              826  POP_TOP          

 L. 674       828  LOAD_CONST               None
              830  RETURN_VALUE     
            832_0  COME_FROM           792  '792'

 L. 675       832  SETUP_LOOP          904  'to 904'
              834  LOAD_FAST                '_nconvlayer'
              836  GET_ITER         
            838_0  COME_FROM           858  '858'
              838  FOR_ITER            902  'to 902'
              840  STORE_FAST               '_i'

 L. 676       842  LOAD_FAST                '_i'
              844  LOAD_CONST               False
              846  COMPARE_OP               is
          848_850  POP_JUMP_IF_TRUE    862  'to 862'
              852  LOAD_FAST                '_i'
              854  LOAD_CONST               1
              856  COMPARE_OP               <
          858_860  POP_JUMP_IF_FALSE   838  'to 838'
            862_0  COME_FROM           848  '848'

 L. 677       862  LOAD_GLOBAL              vis_msg
              864  LOAD_ATTR                print
              866  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Non-positive convolutional layer number'

 L. 678       868  LOAD_STR                 'error'
              870  LOAD_CONST               ('type',)
              872  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              874  POP_TOP          

 L. 679       876  LOAD_GLOBAL              QtWidgets
              878  LOAD_ATTR                QMessageBox
              880  LOAD_METHOD              critical
              882  LOAD_DEREF               'self'
              884  LOAD_ATTR                msgbox

 L. 680       886  LOAD_STR                 'Train 2D-CAE'

 L. 681       888  LOAD_STR                 'Non-positive convolutional layer number'
              890  CALL_METHOD_3         3  '3 positional arguments'
              892  POP_TOP          

 L. 682       894  LOAD_CONST               None
              896  RETURN_VALUE     
          898_900  JUMP_BACK           838  'to 838'
              902  POP_BLOCK        
            904_0  COME_FROM_LOOP      832  '832'

 L. 683       904  SETUP_LOOP          976  'to 976'
              906  LOAD_FAST                '_nconvfeature'
              908  GET_ITER         
            910_0  COME_FROM           930  '930'
              910  FOR_ITER            974  'to 974'
              912  STORE_FAST               '_i'

 L. 684       914  LOAD_FAST                '_i'
              916  LOAD_CONST               False
              918  COMPARE_OP               is
          920_922  POP_JUMP_IF_TRUE    934  'to 934'
              924  LOAD_FAST                '_i'
              926  LOAD_CONST               1
              928  COMPARE_OP               <
          930_932  POP_JUMP_IF_FALSE   910  'to 910'
            934_0  COME_FROM           920  '920'

 L. 685       934  LOAD_GLOBAL              vis_msg
              936  LOAD_ATTR                print
              938  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Non-positive convolutional feature number'

 L. 686       940  LOAD_STR                 'error'
              942  LOAD_CONST               ('type',)
              944  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              946  POP_TOP          

 L. 687       948  LOAD_GLOBAL              QtWidgets
              950  LOAD_ATTR                QMessageBox
              952  LOAD_METHOD              critical
              954  LOAD_DEREF               'self'
              956  LOAD_ATTR                msgbox

 L. 688       958  LOAD_STR                 'Train 2D-CAE'

 L. 689       960  LOAD_STR                 'Non-positive convolutional feature number'
              962  CALL_METHOD_3         3  '3 positional arguments'
              964  POP_TOP          

 L. 690       966  LOAD_CONST               None
              968  RETURN_VALUE     
          970_972  JUMP_BACK           910  'to 910'
              974  POP_BLOCK        
            976_0  COME_FROM_LOOP      904  '904'

 L. 691       976  LOAD_FAST                '_n1x1layer'
              978  LOAD_CONST               False
              980  COMPARE_OP               is
          982_984  POP_JUMP_IF_TRUE    996  'to 996'
              986  LOAD_FAST                '_n1x1layer'
              988  LOAD_CONST               0
              990  COMPARE_OP               <=
          992_994  POP_JUMP_IF_FALSE  1032  'to 1032'
            996_0  COME_FROM           982  '982'

 L. 692       996  LOAD_GLOBAL              vis_msg
              998  LOAD_ATTR                print
             1000  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Non-positive 1x1 convolutional layer number'

 L. 693      1002  LOAD_STR                 'error'
             1004  LOAD_CONST               ('type',)
             1006  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1008  POP_TOP          

 L. 694      1010  LOAD_GLOBAL              QtWidgets
             1012  LOAD_ATTR                QMessageBox
             1014  LOAD_METHOD              critical
             1016  LOAD_DEREF               'self'
             1018  LOAD_ATTR                msgbox

 L. 695      1020  LOAD_STR                 'Train 2D-CAE'

 L. 696      1022  LOAD_STR                 'Non-positive 1x1 convolutional layer number'
             1024  CALL_METHOD_3         3  '3 positional arguments'
             1026  POP_TOP          

 L. 697      1028  LOAD_CONST               None
             1030  RETURN_VALUE     
           1032_0  COME_FROM           992  '992'

 L. 698      1032  SETUP_LOOP         1104  'to 1104'
             1034  LOAD_FAST                '_n1x1feature'
             1036  GET_ITER         
           1038_0  COME_FROM          1058  '1058'
             1038  FOR_ITER           1102  'to 1102'
             1040  STORE_FAST               '_i'

 L. 699      1042  LOAD_FAST                '_i'
             1044  LOAD_CONST               False
             1046  COMPARE_OP               is
         1048_1050  POP_JUMP_IF_TRUE   1062  'to 1062'
             1052  LOAD_FAST                '_i'
             1054  LOAD_CONST               1
             1056  COMPARE_OP               <
         1058_1060  POP_JUMP_IF_FALSE  1038  'to 1038'
           1062_0  COME_FROM          1048  '1048'

 L. 700      1062  LOAD_GLOBAL              vis_msg
             1064  LOAD_ATTR                print
             1066  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Non-positive 1x1 convolutional feature number'

 L. 701      1068  LOAD_STR                 'error'
             1070  LOAD_CONST               ('type',)
             1072  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1074  POP_TOP          

 L. 702      1076  LOAD_GLOBAL              QtWidgets
             1078  LOAD_ATTR                QMessageBox
             1080  LOAD_METHOD              critical
             1082  LOAD_DEREF               'self'
             1084  LOAD_ATTR                msgbox

 L. 703      1086  LOAD_STR                 'Train 2D-CAE'

 L. 704      1088  LOAD_STR                 'Non-positive 1x1 convolutional feature number'
             1090  CALL_METHOD_3         3  '3 positional arguments'
             1092  POP_TOP          

 L. 705      1094  LOAD_CONST               None
             1096  RETURN_VALUE     
         1098_1100  JUMP_BACK          1038  'to 1038'
             1102  POP_BLOCK        
           1104_0  COME_FROM_LOOP     1032  '1032'

 L. 706      1104  LOAD_FAST                '_patch_height'
             1106  LOAD_CONST               False
             1108  COMPARE_OP               is
         1110_1112  POP_JUMP_IF_TRUE   1144  'to 1144'
             1114  LOAD_FAST                '_patch_width'
             1116  LOAD_CONST               False
             1118  COMPARE_OP               is
         1120_1122  POP_JUMP_IF_TRUE   1144  'to 1144'

 L. 707      1124  LOAD_FAST                '_patch_height'
             1126  LOAD_CONST               1
             1128  COMPARE_OP               <
         1130_1132  POP_JUMP_IF_TRUE   1144  'to 1144'
             1134  LOAD_FAST                '_patch_width'
             1136  LOAD_CONST               1
             1138  COMPARE_OP               <
         1140_1142  POP_JUMP_IF_FALSE  1180  'to 1180'
           1144_0  COME_FROM          1130  '1130'
           1144_1  COME_FROM          1120  '1120'
           1144_2  COME_FROM          1110  '1110'

 L. 708      1144  LOAD_GLOBAL              vis_msg
             1146  LOAD_ATTR                print
             1148  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Non-positive convolutional patch size'

 L. 709      1150  LOAD_STR                 'error'
             1152  LOAD_CONST               ('type',)
             1154  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1156  POP_TOP          

 L. 710      1158  LOAD_GLOBAL              QtWidgets
             1160  LOAD_ATTR                QMessageBox
             1162  LOAD_METHOD              critical
             1164  LOAD_DEREF               'self'
             1166  LOAD_ATTR                msgbox

 L. 711      1168  LOAD_STR                 'Train 2D-CAE'

 L. 712      1170  LOAD_STR                 'Non-positive convolutional patch size'
             1172  CALL_METHOD_3         3  '3 positional arguments'
             1174  POP_TOP          

 L. 713      1176  LOAD_CONST               None
             1178  RETURN_VALUE     
           1180_0  COME_FROM          1140  '1140'

 L. 714      1180  LOAD_FAST                '_pool_height'
             1182  LOAD_CONST               False
             1184  COMPARE_OP               is
         1186_1188  POP_JUMP_IF_TRUE   1220  'to 1220'
             1190  LOAD_FAST                '_pool_width'
             1192  LOAD_CONST               False
             1194  COMPARE_OP               is
         1196_1198  POP_JUMP_IF_TRUE   1220  'to 1220'

 L. 715      1200  LOAD_FAST                '_pool_height'
             1202  LOAD_CONST               1
             1204  COMPARE_OP               <
         1206_1208  POP_JUMP_IF_TRUE   1220  'to 1220'
             1210  LOAD_FAST                '_pool_width'
             1212  LOAD_CONST               1
             1214  COMPARE_OP               <
         1216_1218  POP_JUMP_IF_FALSE  1256  'to 1256'
           1220_0  COME_FROM          1206  '1206'
           1220_1  COME_FROM          1196  '1196'
           1220_2  COME_FROM          1186  '1186'

 L. 716      1220  LOAD_GLOBAL              vis_msg
             1222  LOAD_ATTR                print
             1224  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Non-positive pooling size'
             1226  LOAD_STR                 'error'
             1228  LOAD_CONST               ('type',)
             1230  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1232  POP_TOP          

 L. 717      1234  LOAD_GLOBAL              QtWidgets
             1236  LOAD_ATTR                QMessageBox
             1238  LOAD_METHOD              critical
             1240  LOAD_DEREF               'self'
             1242  LOAD_ATTR                msgbox

 L. 718      1244  LOAD_STR                 'Train 2D-CAE'

 L. 719      1246  LOAD_STR                 'Non-positive pooling size'
             1248  CALL_METHOD_3         3  '3 positional arguments'
             1250  POP_TOP          

 L. 720      1252  LOAD_CONST               None
             1254  RETURN_VALUE     
           1256_0  COME_FROM          1216  '1216'

 L. 721      1256  LOAD_FAST                '_nepoch'
             1258  LOAD_CONST               False
             1260  COMPARE_OP               is
         1262_1264  POP_JUMP_IF_TRUE   1276  'to 1276'
             1266  LOAD_FAST                '_nepoch'
             1268  LOAD_CONST               0
             1270  COMPARE_OP               <=
         1272_1274  POP_JUMP_IF_FALSE  1312  'to 1312'
           1276_0  COME_FROM          1262  '1262'

 L. 722      1276  LOAD_GLOBAL              vis_msg
             1278  LOAD_ATTR                print
             1280  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Non-positive epoch number'
             1282  LOAD_STR                 'error'
             1284  LOAD_CONST               ('type',)
             1286  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1288  POP_TOP          

 L. 723      1290  LOAD_GLOBAL              QtWidgets
             1292  LOAD_ATTR                QMessageBox
             1294  LOAD_METHOD              critical
             1296  LOAD_DEREF               'self'
             1298  LOAD_ATTR                msgbox

 L. 724      1300  LOAD_STR                 'Train 2D-CAE'

 L. 725      1302  LOAD_STR                 'Non-positive epoch number'
             1304  CALL_METHOD_3         3  '3 positional arguments'
             1306  POP_TOP          

 L. 726      1308  LOAD_CONST               None
             1310  RETURN_VALUE     
           1312_0  COME_FROM          1272  '1272'

 L. 727      1312  LOAD_FAST                '_batchsize'
             1314  LOAD_CONST               False
             1316  COMPARE_OP               is
         1318_1320  POP_JUMP_IF_TRUE   1332  'to 1332'
             1322  LOAD_FAST                '_batchsize'
             1324  LOAD_CONST               0
             1326  COMPARE_OP               <=
         1328_1330  POP_JUMP_IF_FALSE  1368  'to 1368'
           1332_0  COME_FROM          1318  '1318'

 L. 728      1332  LOAD_GLOBAL              vis_msg
             1334  LOAD_ATTR                print
             1336  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Non-positive batch size'
             1338  LOAD_STR                 'error'
             1340  LOAD_CONST               ('type',)
             1342  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1344  POP_TOP          

 L. 729      1346  LOAD_GLOBAL              QtWidgets
             1348  LOAD_ATTR                QMessageBox
             1350  LOAD_METHOD              critical
             1352  LOAD_DEREF               'self'
             1354  LOAD_ATTR                msgbox

 L. 730      1356  LOAD_STR                 'Train 2D-CAE'

 L. 731      1358  LOAD_STR                 'Non-positive batch size'
             1360  CALL_METHOD_3         3  '3 positional arguments'
             1362  POP_TOP          

 L. 732      1364  LOAD_CONST               None
             1366  RETURN_VALUE     
           1368_0  COME_FROM          1328  '1328'

 L. 733      1368  LOAD_FAST                '_learning_rate'
             1370  LOAD_CONST               False
             1372  COMPARE_OP               is
         1374_1376  POP_JUMP_IF_TRUE   1388  'to 1388'
             1378  LOAD_FAST                '_learning_rate'
             1380  LOAD_CONST               0
             1382  COMPARE_OP               <=
         1384_1386  POP_JUMP_IF_FALSE  1424  'to 1424'
           1388_0  COME_FROM          1374  '1374'

 L. 734      1388  LOAD_GLOBAL              vis_msg
             1390  LOAD_ATTR                print
             1392  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Non-positive learning rate'
             1394  LOAD_STR                 'error'
             1396  LOAD_CONST               ('type',)
             1398  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1400  POP_TOP          

 L. 735      1402  LOAD_GLOBAL              QtWidgets
             1404  LOAD_ATTR                QMessageBox
             1406  LOAD_METHOD              critical
             1408  LOAD_DEREF               'self'
             1410  LOAD_ATTR                msgbox

 L. 736      1412  LOAD_STR                 'Train 2D-CAE'

 L. 737      1414  LOAD_STR                 'Non-positive learning rate'
             1416  CALL_METHOD_3         3  '3 positional arguments'
             1418  POP_TOP          

 L. 738      1420  LOAD_CONST               None
             1422  RETURN_VALUE     
           1424_0  COME_FROM          1384  '1384'

 L. 739      1424  LOAD_FAST                '_dropout_prob'
             1426  LOAD_CONST               False
             1428  COMPARE_OP               is
         1430_1432  POP_JUMP_IF_TRUE   1444  'to 1444'
             1434  LOAD_FAST                '_dropout_prob'
             1436  LOAD_CONST               0
             1438  COMPARE_OP               <=
         1440_1442  POP_JUMP_IF_FALSE  1480  'to 1480'
           1444_0  COME_FROM          1430  '1430'

 L. 740      1444  LOAD_GLOBAL              vis_msg
             1446  LOAD_ATTR                print
             1448  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: Negative dropout rate'
             1450  LOAD_STR                 'error'
             1452  LOAD_CONST               ('type',)
             1454  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1456  POP_TOP          

 L. 741      1458  LOAD_GLOBAL              QtWidgets
             1460  LOAD_ATTR                QMessageBox
             1462  LOAD_METHOD              critical
             1464  LOAD_DEREF               'self'
             1466  LOAD_ATTR                msgbox

 L. 742      1468  LOAD_STR                 'Train 2D-CAE'

 L. 743      1470  LOAD_STR                 'Negative dropout rate'
             1472  CALL_METHOD_3         3  '3 positional arguments'
             1474  POP_TOP          

 L. 744      1476  LOAD_CONST               None
             1478  RETURN_VALUE     
           1480_0  COME_FROM          1440  '1440'

 L. 746      1480  LOAD_GLOBAL              len
             1482  LOAD_DEREF               'self'
             1484  LOAD_ATTR                ldtsave
             1486  LOAD_METHOD              text
             1488  CALL_METHOD_0         0  '0 positional arguments'
             1490  CALL_FUNCTION_1       1  '1 positional argument'
             1492  LOAD_CONST               1
             1494  COMPARE_OP               <
         1496_1498  POP_JUMP_IF_FALSE  1536  'to 1536'

 L. 747      1500  LOAD_GLOBAL              vis_msg
             1502  LOAD_ATTR                print
             1504  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: No name specified for CAE network'
             1506  LOAD_STR                 'error'
             1508  LOAD_CONST               ('type',)
             1510  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1512  POP_TOP          

 L. 748      1514  LOAD_GLOBAL              QtWidgets
             1516  LOAD_ATTR                QMessageBox
             1518  LOAD_METHOD              critical
             1520  LOAD_DEREF               'self'
             1522  LOAD_ATTR                msgbox

 L. 749      1524  LOAD_STR                 'Train 2D-CAE'

 L. 750      1526  LOAD_STR                 'No name specified for CAE network'
             1528  CALL_METHOD_3         3  '3 positional arguments'
             1530  POP_TOP          

 L. 751      1532  LOAD_CONST               None
             1534  RETURN_VALUE     
           1536_0  COME_FROM          1496  '1496'

 L. 752      1536  LOAD_GLOBAL              os
             1538  LOAD_ATTR                path
             1540  LOAD_METHOD              dirname
             1542  LOAD_DEREF               'self'
             1544  LOAD_ATTR                ldtsave
             1546  LOAD_METHOD              text
             1548  CALL_METHOD_0         0  '0 positional arguments'
             1550  CALL_METHOD_1         1  '1 positional argument'
             1552  STORE_FAST               '_savepath'

 L. 753      1554  LOAD_GLOBAL              os
             1556  LOAD_ATTR                path
             1558  LOAD_METHOD              splitext
             1560  LOAD_GLOBAL              os
             1562  LOAD_ATTR                path
             1564  LOAD_METHOD              basename
             1566  LOAD_DEREF               'self'
             1568  LOAD_ATTR                ldtsave
             1570  LOAD_METHOD              text
             1572  CALL_METHOD_0         0  '0 positional arguments'
             1574  CALL_METHOD_1         1  '1 positional argument'
             1576  CALL_METHOD_1         1  '1 positional argument'
             1578  LOAD_CONST               0
             1580  BINARY_SUBSCR    
             1582  STORE_FAST               '_savename'

 L. 755      1584  LOAD_CONST               0
             1586  STORE_FAST               '_wdinl'

 L. 756      1588  LOAD_CONST               0
             1590  STORE_FAST               '_wdxl'

 L. 757      1592  LOAD_CONST               0
             1594  STORE_FAST               '_wdz'

 L. 758      1596  LOAD_DEREF               'self'
             1598  LOAD_ATTR                cbbornt
             1600  LOAD_METHOD              currentIndex
             1602  CALL_METHOD_0         0  '0 positional arguments'
             1604  LOAD_CONST               0
             1606  COMPARE_OP               ==
         1608_1610  POP_JUMP_IF_FALSE  1636  'to 1636'

 L. 759      1612  LOAD_GLOBAL              int
             1614  LOAD_FAST                '_image_width'
             1616  LOAD_CONST               2
             1618  BINARY_TRUE_DIVIDE
             1620  CALL_FUNCTION_1       1  '1 positional argument'
             1622  STORE_FAST               '_wdxl'

 L. 760      1624  LOAD_GLOBAL              int
             1626  LOAD_FAST                '_image_height'
             1628  LOAD_CONST               2
             1630  BINARY_TRUE_DIVIDE
             1632  CALL_FUNCTION_1       1  '1 positional argument'
             1634  STORE_FAST               '_wdz'
           1636_0  COME_FROM          1608  '1608'

 L. 761      1636  LOAD_DEREF               'self'
             1638  LOAD_ATTR                cbbornt
             1640  LOAD_METHOD              currentIndex
             1642  CALL_METHOD_0         0  '0 positional arguments'
             1644  LOAD_CONST               1
             1646  COMPARE_OP               ==
         1648_1650  POP_JUMP_IF_FALSE  1676  'to 1676'

 L. 762      1652  LOAD_GLOBAL              int
             1654  LOAD_FAST                '_image_width'
             1656  LOAD_CONST               2
             1658  BINARY_TRUE_DIVIDE
             1660  CALL_FUNCTION_1       1  '1 positional argument'
             1662  STORE_FAST               '_wdinl'

 L. 763      1664  LOAD_GLOBAL              int
             1666  LOAD_FAST                '_image_height'
             1668  LOAD_CONST               2
             1670  BINARY_TRUE_DIVIDE
             1672  CALL_FUNCTION_1       1  '1 positional argument'
             1674  STORE_FAST               '_wdz'
           1676_0  COME_FROM          1648  '1648'

 L. 764      1676  LOAD_DEREF               'self'
             1678  LOAD_ATTR                cbbornt
             1680  LOAD_METHOD              currentIndex
             1682  CALL_METHOD_0         0  '0 positional arguments'
             1684  LOAD_CONST               2
             1686  COMPARE_OP               ==
         1688_1690  POP_JUMP_IF_FALSE  1716  'to 1716'

 L. 765      1692  LOAD_GLOBAL              int
             1694  LOAD_FAST                '_image_width'
             1696  LOAD_CONST               2
             1698  BINARY_TRUE_DIVIDE
             1700  CALL_FUNCTION_1       1  '1 positional argument'
             1702  STORE_FAST               '_wdinl'

 L. 766      1704  LOAD_GLOBAL              int
             1706  LOAD_FAST                '_image_height'
             1708  LOAD_CONST               2
             1710  BINARY_TRUE_DIVIDE
             1712  CALL_FUNCTION_1       1  '1 positional argument'
             1714  STORE_FAST               '_wdxl'
           1716_0  COME_FROM          1688  '1688'

 L. 768      1716  LOAD_DEREF               'self'
             1718  LOAD_ATTR                survinfo
             1720  STORE_FAST               '_seisinfo'

 L. 770      1722  LOAD_GLOBAL              print
             1724  LOAD_STR                 'TrainMl2DCaeFromExisting: Step 1 - Step 1 - Get training samples:'
             1726  CALL_FUNCTION_1       1  '1 positional argument'
             1728  POP_TOP          

 L. 771      1730  LOAD_DEREF               'self'
             1732  LOAD_ATTR                traindataconfig
             1734  LOAD_STR                 'TrainPointSet'
             1736  BINARY_SUBSCR    
             1738  STORE_FAST               '_trainpoint'

 L. 772      1740  LOAD_GLOBAL              np
             1742  LOAD_METHOD              zeros
             1744  LOAD_CONST               0
             1746  LOAD_CONST               3
             1748  BUILD_LIST_2          2 
             1750  CALL_METHOD_1         1  '1 positional argument'
             1752  STORE_FAST               '_traindata'

 L. 773      1754  SETUP_LOOP         1830  'to 1830'
             1756  LOAD_FAST                '_trainpoint'
             1758  GET_ITER         
           1760_0  COME_FROM          1778  '1778'
             1760  FOR_ITER           1828  'to 1828'
             1762  STORE_FAST               '_p'

 L. 774      1764  LOAD_GLOBAL              point_ays
             1766  LOAD_METHOD              checkPoint
             1768  LOAD_DEREF               'self'
             1770  LOAD_ATTR                pointsetdata
             1772  LOAD_FAST                '_p'
             1774  BINARY_SUBSCR    
             1776  CALL_METHOD_1         1  '1 positional argument'
         1778_1780  POP_JUMP_IF_FALSE  1760  'to 1760'

 L. 775      1782  LOAD_GLOBAL              basic_mdt
             1784  LOAD_METHOD              exportMatDict
             1786  LOAD_DEREF               'self'
             1788  LOAD_ATTR                pointsetdata
             1790  LOAD_FAST                '_p'
             1792  BINARY_SUBSCR    
             1794  LOAD_STR                 'Inline'
             1796  LOAD_STR                 'Crossline'
             1798  LOAD_STR                 'Z'
             1800  BUILD_LIST_3          3 
             1802  CALL_METHOD_2         2  '2 positional arguments'
             1804  STORE_FAST               '_pt'

 L. 776      1806  LOAD_GLOBAL              np
             1808  LOAD_ATTR                concatenate
             1810  LOAD_FAST                '_traindata'
             1812  LOAD_FAST                '_pt'
             1814  BUILD_TUPLE_2         2 
             1816  LOAD_CONST               0
             1818  LOAD_CONST               ('axis',)
             1820  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1822  STORE_FAST               '_traindata'
         1824_1826  JUMP_BACK          1760  'to 1760'
             1828  POP_BLOCK        
           1830_0  COME_FROM_LOOP     1754  '1754'

 L. 777      1830  LOAD_GLOBAL              seis_ays
             1832  LOAD_ATTR                removeOutofSurveySample
             1834  LOAD_FAST                '_traindata'

 L. 778      1836  LOAD_FAST                '_seisinfo'
             1838  LOAD_STR                 'ILStart'
             1840  BINARY_SUBSCR    
             1842  LOAD_FAST                '_wdinl'
             1844  LOAD_FAST                '_seisinfo'
             1846  LOAD_STR                 'ILStep'
             1848  BINARY_SUBSCR    
             1850  BINARY_MULTIPLY  
             1852  BINARY_ADD       

 L. 779      1854  LOAD_FAST                '_seisinfo'
             1856  LOAD_STR                 'ILEnd'
             1858  BINARY_SUBSCR    
             1860  LOAD_FAST                '_wdinl'
             1862  LOAD_FAST                '_seisinfo'
             1864  LOAD_STR                 'ILStep'
             1866  BINARY_SUBSCR    
             1868  BINARY_MULTIPLY  
             1870  BINARY_SUBTRACT  

 L. 780      1872  LOAD_FAST                '_seisinfo'
             1874  LOAD_STR                 'XLStart'
             1876  BINARY_SUBSCR    
             1878  LOAD_FAST                '_wdxl'
             1880  LOAD_FAST                '_seisinfo'
             1882  LOAD_STR                 'XLStep'
             1884  BINARY_SUBSCR    
             1886  BINARY_MULTIPLY  
             1888  BINARY_ADD       

 L. 781      1890  LOAD_FAST                '_seisinfo'
             1892  LOAD_STR                 'XLEnd'
             1894  BINARY_SUBSCR    
             1896  LOAD_FAST                '_wdxl'
             1898  LOAD_FAST                '_seisinfo'
             1900  LOAD_STR                 'XLStep'
             1902  BINARY_SUBSCR    
             1904  BINARY_MULTIPLY  
             1906  BINARY_SUBTRACT  

 L. 782      1908  LOAD_FAST                '_seisinfo'
             1910  LOAD_STR                 'ZStart'
             1912  BINARY_SUBSCR    
             1914  LOAD_FAST                '_wdz'
             1916  LOAD_FAST                '_seisinfo'
             1918  LOAD_STR                 'ZStep'
             1920  BINARY_SUBSCR    
             1922  BINARY_MULTIPLY  
             1924  BINARY_ADD       

 L. 783      1926  LOAD_FAST                '_seisinfo'
             1928  LOAD_STR                 'ZEnd'
             1930  BINARY_SUBSCR    
             1932  LOAD_FAST                '_wdz'
             1934  LOAD_FAST                '_seisinfo'
             1936  LOAD_STR                 'ZStep'
             1938  BINARY_SUBSCR    
             1940  BINARY_MULTIPLY  
             1942  BINARY_SUBTRACT  
             1944  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1946  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1948  STORE_FAST               '_traindata'

 L. 786      1950  LOAD_GLOBAL              np
             1952  LOAD_METHOD              shape
             1954  LOAD_FAST                '_traindata'
             1956  CALL_METHOD_1         1  '1 positional argument'
             1958  LOAD_CONST               0
             1960  BINARY_SUBSCR    
             1962  LOAD_CONST               0
             1964  COMPARE_OP               <=
         1966_1968  POP_JUMP_IF_FALSE  2006  'to 2006'

 L. 787      1970  LOAD_GLOBAL              vis_msg
             1972  LOAD_ATTR                print
             1974  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: No training sample found'
             1976  LOAD_STR                 'error'
             1978  LOAD_CONST               ('type',)
             1980  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1982  POP_TOP          

 L. 788      1984  LOAD_GLOBAL              QtWidgets
             1986  LOAD_ATTR                QMessageBox
             1988  LOAD_METHOD              critical
             1990  LOAD_DEREF               'self'
             1992  LOAD_ATTR                msgbox

 L. 789      1994  LOAD_STR                 'Train 2D-CAE'

 L. 790      1996  LOAD_STR                 'No training sample found'
             1998  CALL_METHOD_3         3  '3 positional arguments'
             2000  POP_TOP          

 L. 791      2002  LOAD_CONST               None
             2004  RETURN_VALUE     
           2006_0  COME_FROM          1966  '1966'

 L. 794      2006  LOAD_GLOBAL              print
             2008  LOAD_STR                 'TrainMl2DCaeFromExisting: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 795      2010  LOAD_FAST                '_image_height'
             2012  LOAD_FAST                '_image_width'
             2014  LOAD_FAST                '_image_height_new'
             2016  LOAD_FAST                '_image_width_new'
             2018  BUILD_TUPLE_4         4 
             2020  BINARY_MODULO    
             2022  CALL_FUNCTION_1       1  '1 positional argument'
             2024  POP_TOP          

 L. 796      2026  BUILD_MAP_0           0 
             2028  STORE_FAST               '_traindict'

 L. 797      2030  SETUP_LOOP         2102  'to 2102'
             2032  LOAD_FAST                '_features'
             2034  GET_ITER         
             2036  FOR_ITER           2100  'to 2100'
             2038  STORE_FAST               'f'

 L. 798      2040  LOAD_DEREF               'self'
             2042  LOAD_ATTR                seisdata
             2044  LOAD_FAST                'f'
             2046  BINARY_SUBSCR    
             2048  STORE_FAST               '_seisdata'

 L. 799      2050  LOAD_GLOBAL              seis_ays
             2052  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2054  LOAD_FAST                '_seisdata'
             2056  LOAD_FAST                '_traindata'
             2058  LOAD_DEREF               'self'
             2060  LOAD_ATTR                survinfo

 L. 800      2062  LOAD_FAST                '_wdinl'
             2064  LOAD_FAST                '_wdxl'
             2066  LOAD_FAST                '_wdz'

 L. 801      2068  LOAD_CONST               False
             2070  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2072  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2074  LOAD_CONST               None
             2076  LOAD_CONST               None
             2078  BUILD_SLICE_2         2 
             2080  LOAD_CONST               3
             2082  LOAD_CONST               None
             2084  BUILD_SLICE_2         2 
             2086  BUILD_TUPLE_2         2 
             2088  BINARY_SUBSCR    
             2090  LOAD_FAST                '_traindict'
             2092  LOAD_FAST                'f'
             2094  STORE_SUBSCR     
         2096_2098  JUMP_BACK          2036  'to 2036'
             2100  POP_BLOCK        
           2102_0  COME_FROM_LOOP     2030  '2030'

 L. 802      2102  LOAD_FAST                '_target'
             2104  LOAD_FAST                '_features'
             2106  COMPARE_OP               not-in
         2108_2110  POP_JUMP_IF_FALSE  2168  'to 2168'

 L. 803      2112  LOAD_DEREF               'self'
             2114  LOAD_ATTR                seisdata
             2116  LOAD_FAST                '_target'
             2118  BINARY_SUBSCR    
             2120  STORE_FAST               '_seisdata'

 L. 804      2122  LOAD_GLOBAL              seis_ays
             2124  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2126  LOAD_FAST                '_seisdata'
             2128  LOAD_FAST                '_traindata'
             2130  LOAD_DEREF               'self'
             2132  LOAD_ATTR                survinfo

 L. 805      2134  LOAD_FAST                '_wdinl'
             2136  LOAD_FAST                '_wdxl'
             2138  LOAD_FAST                '_wdz'

 L. 806      2140  LOAD_CONST               False
             2142  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2144  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2146  LOAD_CONST               None
             2148  LOAD_CONST               None
             2150  BUILD_SLICE_2         2 
             2152  LOAD_CONST               3
             2154  LOAD_CONST               None
             2156  BUILD_SLICE_2         2 
             2158  BUILD_TUPLE_2         2 
             2160  BINARY_SUBSCR    
             2162  LOAD_FAST                '_traindict'
             2164  LOAD_FAST                '_target'
             2166  STORE_SUBSCR     
           2168_0  COME_FROM          2108  '2108'

 L. 807      2168  LOAD_DEREF               'self'
             2170  LOAD_ATTR                traindataconfig
             2172  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2174  BINARY_SUBSCR    
         2176_2178  POP_JUMP_IF_FALSE  2260  'to 2260'

 L. 808      2180  SETUP_LOOP         2260  'to 2260'
             2182  LOAD_FAST                '_features'
             2184  GET_ITER         
           2186_0  COME_FROM          2214  '2214'
             2186  FOR_ITER           2258  'to 2258'
             2188  STORE_FAST               'f'

 L. 809      2190  LOAD_GLOBAL              ml_aug
             2192  LOAD_METHOD              removeInvariantFeature
             2194  LOAD_FAST                '_traindict'
             2196  LOAD_FAST                'f'
             2198  CALL_METHOD_2         2  '2 positional arguments'
             2200  STORE_FAST               '_traindict'

 L. 810      2202  LOAD_GLOBAL              basic_mdt
             2204  LOAD_METHOD              maxDictConstantRow
             2206  LOAD_FAST                '_traindict'
             2208  CALL_METHOD_1         1  '1 positional argument'
             2210  LOAD_CONST               0
             2212  COMPARE_OP               <=
         2214_2216  POP_JUMP_IF_FALSE  2186  'to 2186'

 L. 811      2218  LOAD_GLOBAL              vis_msg
             2220  LOAD_ATTR                print
             2222  LOAD_STR                 'ERROR in TrainMl2DCaeFromExisting: No training sample found'
             2224  LOAD_STR                 'error'
             2226  LOAD_CONST               ('type',)
             2228  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2230  POP_TOP          

 L. 812      2232  LOAD_GLOBAL              QtWidgets
             2234  LOAD_ATTR                QMessageBox
             2236  LOAD_METHOD              critical
             2238  LOAD_DEREF               'self'
             2240  LOAD_ATTR                msgbox

 L. 813      2242  LOAD_STR                 'Train 2D-CAE'

 L. 814      2244  LOAD_STR                 'No training sample found'
             2246  CALL_METHOD_3         3  '3 positional arguments'
             2248  POP_TOP          

 L. 815      2250  LOAD_CONST               None
             2252  RETURN_VALUE     
         2254_2256  JUMP_BACK          2186  'to 2186'
             2258  POP_BLOCK        
           2260_0  COME_FROM_LOOP     2180  '2180'
           2260_1  COME_FROM          2176  '2176'

 L. 816      2260  LOAD_FAST                '_image_height_new'
             2262  LOAD_FAST                '_image_height'
             2264  COMPARE_OP               !=
         2266_2268  POP_JUMP_IF_TRUE   2280  'to 2280'
             2270  LOAD_FAST                '_image_width_new'
             2272  LOAD_FAST                '_image_width'
             2274  COMPARE_OP               !=
         2276_2278  POP_JUMP_IF_FALSE  2364  'to 2364'
           2280_0  COME_FROM          2266  '2266'

 L. 817      2280  SETUP_LOOP         2324  'to 2324'
             2282  LOAD_FAST                '_features'
             2284  GET_ITER         
             2286  FOR_ITER           2322  'to 2322'
             2288  STORE_FAST               'f'

 L. 818      2290  LOAD_GLOBAL              basic_image
             2292  LOAD_ATTR                changeImageSize
             2294  LOAD_FAST                '_traindict'
             2296  LOAD_FAST                'f'
             2298  BINARY_SUBSCR    

 L. 819      2300  LOAD_FAST                '_image_height'

 L. 820      2302  LOAD_FAST                '_image_width'

 L. 821      2304  LOAD_FAST                '_image_height_new'

 L. 822      2306  LOAD_FAST                '_image_width_new'
             2308  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2310  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2312  LOAD_FAST                '_traindict'
             2314  LOAD_FAST                'f'
             2316  STORE_SUBSCR     
         2318_2320  JUMP_BACK          2286  'to 2286'
             2322  POP_BLOCK        
           2324_0  COME_FROM_LOOP     2280  '2280'

 L. 823      2324  LOAD_FAST                '_target'
             2326  LOAD_FAST                '_features'
             2328  COMPARE_OP               not-in
         2330_2332  POP_JUMP_IF_FALSE  2364  'to 2364'

 L. 824      2334  LOAD_GLOBAL              basic_image
             2336  LOAD_ATTR                changeImageSize
             2338  LOAD_FAST                '_traindict'
             2340  LOAD_FAST                '_target'
             2342  BINARY_SUBSCR    

 L. 825      2344  LOAD_FAST                '_image_height'

 L. 826      2346  LOAD_FAST                '_image_width'

 L. 827      2348  LOAD_FAST                '_image_height_new'

 L. 828      2350  LOAD_FAST                '_image_width_new'
             2352  LOAD_STR                 'linear'
             2354  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2356  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2358  LOAD_FAST                '_traindict'
             2360  LOAD_FAST                '_target'
             2362  STORE_SUBSCR     
           2364_0  COME_FROM          2330  '2330'
           2364_1  COME_FROM          2276  '2276'

 L. 829      2364  LOAD_DEREF               'self'
             2366  LOAD_ATTR                traindataconfig
             2368  LOAD_STR                 'RotateFeature_Checked'
             2370  BINARY_SUBSCR    
             2372  LOAD_CONST               True
             2374  COMPARE_OP               is
         2376_2378  POP_JUMP_IF_FALSE  2518  'to 2518'

 L. 830      2380  SETUP_LOOP         2452  'to 2452'
             2382  LOAD_FAST                '_features'
             2384  GET_ITER         
             2386  FOR_ITER           2450  'to 2450'
             2388  STORE_FAST               'f'

 L. 831      2390  LOAD_FAST                '_image_height_new'
             2392  LOAD_FAST                '_image_width_new'
             2394  COMPARE_OP               ==
         2396_2398  POP_JUMP_IF_FALSE  2424  'to 2424'

 L. 832      2400  LOAD_GLOBAL              ml_aug
             2402  LOAD_METHOD              rotateImage6Way
             2404  LOAD_FAST                '_traindict'
             2406  LOAD_FAST                'f'
             2408  BINARY_SUBSCR    
             2410  LOAD_FAST                '_image_height_new'
             2412  LOAD_FAST                '_image_width_new'
             2414  CALL_METHOD_3         3  '3 positional arguments'
             2416  LOAD_FAST                '_traindict'
             2418  LOAD_FAST                'f'
             2420  STORE_SUBSCR     
             2422  JUMP_BACK          2386  'to 2386'
           2424_0  COME_FROM          2396  '2396'

 L. 834      2424  LOAD_GLOBAL              ml_aug
             2426  LOAD_METHOD              rotateImage4Way
             2428  LOAD_FAST                '_traindict'
             2430  LOAD_FAST                'f'
             2432  BINARY_SUBSCR    
             2434  LOAD_FAST                '_image_height_new'
             2436  LOAD_FAST                '_image_width_new'
             2438  CALL_METHOD_3         3  '3 positional arguments'
             2440  LOAD_FAST                '_traindict'
             2442  LOAD_FAST                'f'
             2444  STORE_SUBSCR     
         2446_2448  JUMP_BACK          2386  'to 2386'
             2450  POP_BLOCK        
           2452_0  COME_FROM_LOOP     2380  '2380'

 L. 835      2452  LOAD_FAST                '_target'
             2454  LOAD_FAST                '_features'
             2456  COMPARE_OP               not-in
         2458_2460  POP_JUMP_IF_FALSE  2518  'to 2518'

 L. 836      2462  LOAD_FAST                '_image_height_new'
             2464  LOAD_FAST                '_image_width_new'
             2466  COMPARE_OP               ==
         2468_2470  POP_JUMP_IF_FALSE  2496  'to 2496'

 L. 838      2472  LOAD_GLOBAL              ml_aug
             2474  LOAD_METHOD              rotateImage6Way
             2476  LOAD_FAST                '_traindict'
             2478  LOAD_FAST                '_target'
             2480  BINARY_SUBSCR    
             2482  LOAD_FAST                '_image_height_new'
             2484  LOAD_FAST                '_image_width_new'
             2486  CALL_METHOD_3         3  '3 positional arguments'
             2488  LOAD_FAST                '_traindict'
             2490  LOAD_FAST                '_target'
             2492  STORE_SUBSCR     
             2494  JUMP_FORWARD       2518  'to 2518'
           2496_0  COME_FROM          2468  '2468'

 L. 841      2496  LOAD_GLOBAL              ml_aug
             2498  LOAD_METHOD              rotateImage4Way
             2500  LOAD_FAST                '_traindict'
             2502  LOAD_FAST                '_target'
             2504  BINARY_SUBSCR    
             2506  LOAD_FAST                '_image_height_new'
             2508  LOAD_FAST                '_image_width_new'
             2510  CALL_METHOD_3         3  '3 positional arguments'
             2512  LOAD_FAST                '_traindict'
             2514  LOAD_FAST                '_target'
             2516  STORE_SUBSCR     
           2518_0  COME_FROM          2494  '2494'
           2518_1  COME_FROM          2458  '2458'
           2518_2  COME_FROM          2376  '2376'

 L. 844      2518  LOAD_GLOBAL              print
             2520  LOAD_STR                 'TrainMl2DCaeFromExisting: A total of %d valid training samples'
             2522  LOAD_GLOBAL              basic_mdt
             2524  LOAD_METHOD              maxDictConstantRow

 L. 845      2526  LOAD_FAST                '_traindict'
             2528  CALL_METHOD_1         1  '1 positional argument'
             2530  BINARY_MODULO    
             2532  CALL_FUNCTION_1       1  '1 positional argument'
             2534  POP_TOP          

 L. 847      2536  LOAD_GLOBAL              print
             2538  LOAD_STR                 'TrainMl2DCaeFromExisting: Step 3 - Start training'
             2540  CALL_FUNCTION_1       1  '1 positional argument'
             2542  POP_TOP          

 L. 849      2544  LOAD_GLOBAL              QtWidgets
             2546  LOAD_METHOD              QProgressDialog
             2548  CALL_METHOD_0         0  '0 positional arguments'
             2550  STORE_FAST               '_pgsdlg'

 L. 850      2552  LOAD_GLOBAL              QtGui
             2554  LOAD_METHOD              QIcon
             2556  CALL_METHOD_0         0  '0 positional arguments'
             2558  STORE_FAST               'icon'

 L. 851      2560  LOAD_FAST                'icon'
             2562  LOAD_METHOD              addPixmap
             2564  LOAD_GLOBAL              QtGui
             2566  LOAD_METHOD              QPixmap
             2568  LOAD_GLOBAL              os
             2570  LOAD_ATTR                path
             2572  LOAD_METHOD              join
             2574  LOAD_DEREF               'self'
             2576  LOAD_ATTR                iconpath
             2578  LOAD_STR                 'icons/new.png'
             2580  CALL_METHOD_2         2  '2 positional arguments'
             2582  CALL_METHOD_1         1  '1 positional argument'

 L. 852      2584  LOAD_GLOBAL              QtGui
             2586  LOAD_ATTR                QIcon
             2588  LOAD_ATTR                Normal
             2590  LOAD_GLOBAL              QtGui
             2592  LOAD_ATTR                QIcon
             2594  LOAD_ATTR                Off
             2596  CALL_METHOD_3         3  '3 positional arguments'
             2598  POP_TOP          

 L. 853      2600  LOAD_FAST                '_pgsdlg'
             2602  LOAD_METHOD              setWindowIcon
             2604  LOAD_FAST                'icon'
             2606  CALL_METHOD_1         1  '1 positional argument'
             2608  POP_TOP          

 L. 854      2610  LOAD_FAST                '_pgsdlg'
             2612  LOAD_METHOD              setWindowTitle
             2614  LOAD_STR                 'Train 2D-CAE'
             2616  CALL_METHOD_1         1  '1 positional argument'
             2618  POP_TOP          

 L. 855      2620  LOAD_FAST                '_pgsdlg'
             2622  LOAD_METHOD              setCancelButton
             2624  LOAD_CONST               None
             2626  CALL_METHOD_1         1  '1 positional argument'
             2628  POP_TOP          

 L. 856      2630  LOAD_FAST                '_pgsdlg'
             2632  LOAD_METHOD              setWindowFlags
             2634  LOAD_GLOBAL              QtCore
             2636  LOAD_ATTR                Qt
             2638  LOAD_ATTR                WindowStaysOnTopHint
             2640  CALL_METHOD_1         1  '1 positional argument'
             2642  POP_TOP          

 L. 857      2644  LOAD_FAST                '_pgsdlg'
             2646  LOAD_METHOD              forceShow
             2648  CALL_METHOD_0         0  '0 positional arguments'
             2650  POP_TOP          

 L. 858      2652  LOAD_FAST                '_pgsdlg'
             2654  LOAD_METHOD              setFixedWidth
             2656  LOAD_CONST               400
             2658  CALL_METHOD_1         1  '1 positional argument'
             2660  POP_TOP          

 L. 859      2662  LOAD_GLOBAL              ml_cae
             2664  LOAD_ATTR                createCAEReconstructorFromExisting
             2666  LOAD_FAST                '_traindict'

 L. 860      2668  LOAD_FAST                '_image_height_new'
             2670  LOAD_FAST                '_image_width_new'

 L. 861      2672  LOAD_FAST                '_features'
             2674  LOAD_FAST                '_target'

 L. 862      2676  LOAD_FAST                '_nepoch'
             2678  LOAD_FAST                '_batchsize'

 L. 863      2680  LOAD_FAST                '_nconvblock'
             2682  LOAD_FAST                '_nconvfeature'

 L. 864      2684  LOAD_FAST                '_nconvlayer'

 L. 865      2686  LOAD_FAST                '_n1x1layer'
             2688  LOAD_FAST                '_n1x1feature'

 L. 866      2690  LOAD_FAST                '_pool_height'
             2692  LOAD_FAST                '_pool_width'

 L. 867      2694  LOAD_FAST                '_learning_rate'

 L. 868      2696  LOAD_FAST                '_dropout_prob'

 L. 869      2698  LOAD_CONST               True

 L. 870      2700  LOAD_FAST                '_savepath'
             2702  LOAD_FAST                '_savename'

 L. 871      2704  LOAD_FAST                '_pgsdlg'

 L. 872      2706  LOAD_FAST                '_precnnpath'

 L. 873      2708  LOAD_FAST                '_precnnname'

 L. 874      2710  LOAD_FAST                '_blockidx'
             2712  LOAD_FAST                '_layeridx'

 L. 875      2714  LOAD_FAST                '_trainable'
             2716  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'nepoch', 'batchsize', 'nconvblock', 'nconvfeature', 'nconvlayer', 'n1x1layer', 'n1x1feature', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprob', 'save2disk', 'savepath', 'savename', 'qpgsdlg', 'precnnpath', 'precnnname', 'blockidx', 'layeridx', 'trainable')
             2718  CALL_FUNCTION_KW_25    25  '25 total positional and keyword args'
             2720  STORE_FAST               '_caelog'

 L. 878      2722  LOAD_GLOBAL              QtWidgets
             2724  LOAD_ATTR                QMessageBox
             2726  LOAD_METHOD              information
             2728  LOAD_DEREF               'self'
             2730  LOAD_ATTR                msgbox

 L. 879      2732  LOAD_STR                 'Train 2D-CAE'

 L. 880      2734  LOAD_STR                 'CAE trained successfully'
             2736  CALL_METHOD_3         3  '3 positional arguments'
             2738  POP_TOP          

 L. 882      2740  LOAD_GLOBAL              QtWidgets
             2742  LOAD_ATTR                QMessageBox
             2744  LOAD_METHOD              question
             2746  LOAD_DEREF               'self'
             2748  LOAD_ATTR                msgbox
             2750  LOAD_STR                 'Train 2D-CAE'
             2752  LOAD_STR                 'View learning matrix?'

 L. 883      2754  LOAD_GLOBAL              QtWidgets
             2756  LOAD_ATTR                QMessageBox
             2758  LOAD_ATTR                Yes
             2760  LOAD_GLOBAL              QtWidgets
             2762  LOAD_ATTR                QMessageBox
             2764  LOAD_ATTR                No
             2766  BINARY_OR        

 L. 884      2768  LOAD_GLOBAL              QtWidgets
             2770  LOAD_ATTR                QMessageBox
             2772  LOAD_ATTR                Yes
             2774  CALL_METHOD_5         5  '5 positional arguments'
             2776  STORE_FAST               'reply'

 L. 886      2778  LOAD_FAST                'reply'
             2780  LOAD_GLOBAL              QtWidgets
             2782  LOAD_ATTR                QMessageBox
             2784  LOAD_ATTR                Yes
             2786  COMPARE_OP               ==
         2788_2790  POP_JUMP_IF_FALSE  2858  'to 2858'

 L. 887      2792  LOAD_GLOBAL              QtWidgets
             2794  LOAD_METHOD              QDialog
             2796  CALL_METHOD_0         0  '0 positional arguments'
             2798  STORE_FAST               '_viewmllearnmat'

 L. 888      2800  LOAD_GLOBAL              gui_viewmllearnmat
             2802  CALL_FUNCTION_0       0  '0 positional arguments'
             2804  STORE_FAST               '_gui'

 L. 889      2806  LOAD_FAST                '_caelog'
             2808  LOAD_STR                 'learning_curve'
             2810  BINARY_SUBSCR    
             2812  LOAD_FAST                '_gui'
             2814  STORE_ATTR               learnmat

 L. 890      2816  LOAD_DEREF               'self'
             2818  LOAD_ATTR                linestyle
             2820  LOAD_FAST                '_gui'
             2822  STORE_ATTR               linestyle

 L. 891      2824  LOAD_DEREF               'self'
             2826  LOAD_ATTR                fontstyle
             2828  LOAD_FAST                '_gui'
             2830  STORE_ATTR               fontstyle

 L. 892      2832  LOAD_FAST                '_gui'
             2834  LOAD_METHOD              setupGUI
             2836  LOAD_FAST                '_viewmllearnmat'
             2838  CALL_METHOD_1         1  '1 positional argument'
             2840  POP_TOP          

 L. 893      2842  LOAD_FAST                '_viewmllearnmat'
             2844  LOAD_METHOD              exec
             2846  CALL_METHOD_0         0  '0 positional arguments'
             2848  POP_TOP          

 L. 894      2850  LOAD_FAST                '_viewmllearnmat'
             2852  LOAD_METHOD              show
             2854  CALL_METHOD_0         0  '0 positional arguments'
             2856  POP_TOP          
           2858_0  COME_FROM          2788  '2788'

Parse error at or near `POP_TOP' instruction at offset 2856

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
    TrainMl2DCaeFromExisting = QtWidgets.QWidget()
    gui = trainml2dcaefromexisting()
    gui.setupGUI(TrainMl2DCaeFromExisting)
    TrainMl2DCaeFromExisting.show()
    sys.exit(app.exec_())