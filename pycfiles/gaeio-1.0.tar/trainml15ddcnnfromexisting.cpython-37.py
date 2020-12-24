# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml15ddcnnfromexisting.py
# Compiled at: 2020-01-05 11:47:49
# Size of source mod 2**32: 54333 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.pointset.analysis as point_ays
import cognitivegeo.src.basic.data as basic_data
import cognitivegeo.src.basic.matdict as basic_mdt
import cognitivegeo.src.basic.curve as basic_curve
import cognitivegeo.src.basic.image as basic_image
import cognitivegeo.src.ml.augmentation as ml_aug
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.ml.dcnnsegmentor15d as ml_dcnn15d
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml15ddcnnfromexisting(object):
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

    def setupGUI(self, TrainMl15DDcnnFromExisting):
        TrainMl15DDcnnFromExisting.setObjectName('TrainMl15DDcnnFromExisting')
        TrainMl15DDcnnFromExisting.setFixedSize(800, 630)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl15DDcnnFromExisting.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl15DDcnnFromExisting)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl15DDcnnFromExisting)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lbltarget.setObjectName('lbltargete')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl15DDcnnFromExisting)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblexisting = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblexisting.setObjectName('lblexisting')
        self.lblexisting.setGeometry(QtCore.QRect(410, 50, 100, 30))
        self.ldtexisting = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtexisting.setObjectName('ldtexisting')
        self.ldtexisting.setGeometry(QtCore.QRect(510, 50, 210, 30))
        self.btnexisting = QtWidgets.QPushButton(TrainMl15DDcnnFromExisting)
        self.btnexisting.setObjectName('btnexisting')
        self.btnexisting.setGeometry(QtCore.QRect(730, 50, 60, 30))
        self.lblnconvblockexisting = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblnconvblockexisting.setObjectName('lblnconvblockexisting')
        self.lblnconvblockexisting.setGeometry(QtCore.QRect(410, 90, 130, 30))
        self.ldtnconvblockexisting = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtnconvblockexisting.setObjectName('ldtnconvblockexisting')
        self.ldtnconvblockexisting.setGeometry(QtCore.QRect(550, 90, 40, 30))
        self.twgnconvblockexisting = QtWidgets.QTableWidget(TrainMl15DDcnnFromExisting)
        self.twgnconvblockexisting.setObjectName('twgnconvblockexisting')
        self.twgnconvblockexisting.setGeometry(QtCore.QRect(610, 90, 180, 150))
        self.twgnconvblockexisting.setColumnCount(3)
        self.twgnconvblockexisting.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblockexisting.verticalHeader().hide()
        self.lblblockid = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblblockid.setObjectName('lblblockid')
        self.lblblockid.setGeometry(QtCore.QRect(410, 130, 130, 30))
        self.cbbblockid = QtWidgets.QComboBox(TrainMl15DDcnnFromExisting)
        self.cbbblockid.setObjectName('cbbblockid')
        self.cbbblockid.setGeometry(QtCore.QRect(550, 130, 40, 30))
        self.lbllayerid = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lbllayerid.setObjectName('lbllayerid')
        self.lbllayerid.setGeometry(QtCore.QRect(410, 170, 130, 30))
        self.cbblayerid = QtWidgets.QComboBox(TrainMl15DDcnnFromExisting)
        self.cbblayerid.setObjectName('cbblayerid')
        self.cbblayerid.setGeometry(QtCore.QRect(550, 170, 40, 30))
        self.lbltrainable = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lbltrainable.setObjectName('lbltrainable')
        self.lbltrainable.setGeometry(QtCore.QRect(410, 210, 130, 30))
        self.cbbtrainable = QtWidgets.QComboBox(TrainMl15DDcnnFromExisting)
        self.cbbtrainable.setObjectName('cbbtrainable')
        self.cbbtrainable.setGeometry(QtCore.QRect(550, 210, 40, 30))
        self.lblappend = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblappend.setObjectName('lblappend')
        self.lblappend.setGeometry(QtCore.QRect(410, 250, 200, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 290, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 290, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl15DDcnnFromExisting)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 330, 180, 200))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 290, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 290, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(TrainMl15DDcnnFromExisting)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 330, 180, 200))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 540, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 540, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 540, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 580, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 580, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 540, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 540, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 540, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 580, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 580, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl15DDcnnFromExisting)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 310, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 350, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.lbldropout = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 390, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 390, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl15DDcnnFromExisting)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl15DDcnnFromExisting)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 440, 180, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl15DDcnnFromExisting)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 440, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl15DDcnnFromExisting)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(120, 580, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl15DDcnnFromExisting)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl15DDcnnFromExisting.geometry().center().x()
        _center_y = TrainMl15DDcnnFromExisting.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl15DDcnnFromExisting)
        QtCore.QMetaObject.connectSlotsByName(TrainMl15DDcnnFromExisting)

    def retranslateGUI(self, TrainMl15DDcnnFromExisting):
        self.dialog = TrainMl15DDcnnFromExisting
        _translate = QtCore.QCoreApplication.translate
        TrainMl15DDcnnFromExisting.setWindowTitle(_translate('TrainMl15DDcnnFromExisting', 'Train 1.5D-DCNN from pre-trained'))
        self.lblfeature.setText(_translate('TrainMl15DDcnnFromExisting', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl15DDcnnFromExisting', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl15DDcnnFromExisting', 'Select target:'))
        self.btnconfigtraindata.setText(_translate('TrainMl2DDcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('TrainMl15DDcnnFromExisting', 'Original\nimage\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl15DDcnnFromExisting', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl15DDcnnFromExisting', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl15DDcnnFromExisting', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl15DDcnnFromExisting', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl15DDcnnFromExisting', 'Interpolated\nimage\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl15DDcnnFromExisting', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl15DDcnnFromExisting', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl15DDcnnFromExisting', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl15DDcnnFromExisting', '32'))
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
                    item.setText(_translate('TrainMl15DDcnnFromExisting', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl15DDcnnFromExisting', 'Specify DCNN architecture:'))
        self.lblexisting.setText(_translate('TrainMl15DDcnnFromExisting', 'Select pre-trained:'))
        self.ldtexisting.setText(_translate('TrainMl15DDcnnFromExisting', ''))
        self.ldtexisting.textChanged.connect(self.changeLdtExisting)
        self.btnexisting.setText(_translate('TrainMl15DDcnnFromExisting', 'Browse'))
        self.btnexisting.clicked.connect(self.clickBtnExisting)
        self.lblnconvblockexisting.setText(_translate('TrainMl15DDcnnFromExisting', 'Available conv. blocks:'))
        self.lblnconvblockexisting.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblockexisting.setText(_translate('TrainMl15DDcnnFromExisting', ''))
        self.ldtnconvblockexisting.setEnabled(False)
        self.ldtnconvblockexisting.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblockexisting.textChanged.connect(self.changeLdtNconvblockExisting)
        self.twgnconvblockexisting.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblblockid.setText(_translate('TrainMl15DDcnnFromExisting', 'Select conv. block ID:'))
        self.lblblockid.setAlignment(QtCore.Qt.AlignRight)
        self.cbbblockid.currentIndexChanged.connect(self.changeCbbBlockid)
        self.lbllayerid.setText(_translate('TrainMl15DDcnnFromExisting', 'Select conv. layer ID:'))
        self.lbllayerid.setAlignment(QtCore.Qt.AlignRight)
        self.lbltrainable.setText(_translate('TrainMl15DDcnnFromExisting', 'Is trainable?:'))
        self.lbltrainable.setAlignment(QtCore.Qt.AlignRight)
        self.cbbtrainable.addItems(['Yes', 'No'])
        self.lblappend.setText(_translate('TrainMl15DDcnnFromExisting', 'Append more blocks & layers:'))
        self.lblnconvblock.setText(_translate('TrainMl15DDcnnFromExisting', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl15DDcnnFromExisting', '2'))
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

        self.lbln1x1layer.setText(_translate('TrainMl15DDcnnFromExisting', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('TrainMl15DDcnnFromExisting', '2'))
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.twgn1x1layer.setRowCount(2)
        for _idx in range(int(self.ldtn1x1layer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl15DDcnnFromExisting', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgn1x1layer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgn1x1layer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl15DDcnnFromExisting', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl15DDcnnFromExisting', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl15DDcnnFromExisting', ''))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskheight.setEnabled(False)
        self.lblmaskwidth.setText(_translate('TrainMl15DDcnnFromExisting', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl15DDcnnFromExisting', ''))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskwidth.setEnabled(False)
        self.lblpoolsize.setText(_translate('TrainMl15DDcnnFromExisting', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl15DDcnnFromExisting', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl15DDcnnFromExisting', ''))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl15DDcnnFromExisting', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl15DDcnnFromExisting', ''))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('TrainMl15DDcnnFromExisting', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl15DDcnnFromExisting', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl15DDcnnFromExisting', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl15DDcnnFromExisting', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl15DDcnnFromExisting', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl15DDcnnFromExisting', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl15DDcnnFromExisting', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('TrainMl15DDcnnFromExisting', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('TrainMl15DDcnnFromExisting', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl15DDcnnFromExisting', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl15DDcnnFromExisting', ''))
        self.btnsave.setText(_translate('TrainMl15DDcnnFromExisting', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl15DDcnnFromExisting', 'Train 1.5D-DCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl15DDcnnFromExisting)

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
        _file = _dialog.getSaveFileName(None, 'Save DCNN Network', (self.rootpath), filter='Tensorflow network file (*.meta);; All files (*.*)')
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

    def clickBtnTrainMl15DDcnnFromExisting--- This code section failed: ---

 L. 598         0  LOAD_DEREF               'self'
                2  LOAD_METHOD              refreshMsgBox
                4  CALL_METHOD_0         0  '0 positional arguments'
                6  POP_TOP          

 L. 600         8  LOAD_GLOBAL              len
               10  LOAD_DEREF               'self'
               12  LOAD_ATTR                lwgfeature
               14  LOAD_METHOD              selectedItems
               16  CALL_METHOD_0         0  '0 positional arguments'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  LOAD_CONST               1
               22  COMPARE_OP               <
               24  POP_JUMP_IF_FALSE    62  'to 62'

 L. 601        26  LOAD_GLOBAL              vis_msg
               28  LOAD_ATTR                print
               30  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 602        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 603        50  LOAD_STR                 'Train 1.5D-DCNN'

 L. 604        52  LOAD_STR                 'No feature selected for training'
               54  CALL_METHOD_3         3  '3 positional arguments'
               56  POP_TOP          

 L. 605        58  LOAD_CONST               None
               60  RETURN_VALUE     
             62_0  COME_FROM            24  '24'

 L. 607        62  LOAD_GLOBAL              basic_data
               64  LOAD_METHOD              str2int
               66  LOAD_DEREF               'self'
               68  LOAD_ATTR                ldtoldheight
               70  LOAD_METHOD              text
               72  CALL_METHOD_0         0  '0 positional arguments'
               74  CALL_METHOD_1         1  '1 positional argument'
               76  STORE_FAST               '_image_height'

 L. 608        78  LOAD_GLOBAL              basic_data
               80  LOAD_METHOD              str2int
               82  LOAD_DEREF               'self'
               84  LOAD_ATTR                ldtoldwidth
               86  LOAD_METHOD              text
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  CALL_METHOD_1         1  '1 positional argument'
               92  STORE_FAST               '_image_width'

 L. 609        94  LOAD_GLOBAL              basic_data
               96  LOAD_METHOD              str2int
               98  LOAD_DEREF               'self'
              100  LOAD_ATTR                ldtnewheight
              102  LOAD_METHOD              text
              104  CALL_METHOD_0         0  '0 positional arguments'
              106  CALL_METHOD_1         1  '1 positional argument'
              108  STORE_FAST               '_image_height_new'

 L. 610       110  LOAD_GLOBAL              basic_data
              112  LOAD_METHOD              str2int
              114  LOAD_DEREF               'self'
              116  LOAD_ATTR                ldtnewwidth
              118  LOAD_METHOD              text
              120  CALL_METHOD_0         0  '0 positional arguments'
              122  CALL_METHOD_1         1  '1 positional argument'
              124  STORE_FAST               '_image_width_new'

 L. 611       126  LOAD_FAST                '_image_height'
              128  LOAD_CONST               False
              130  COMPARE_OP               is
              132  POP_JUMP_IF_TRUE    158  'to 158'
              134  LOAD_FAST                '_image_width'
              136  LOAD_CONST               False
              138  COMPARE_OP               is
              140  POP_JUMP_IF_TRUE    158  'to 158'

 L. 612       142  LOAD_FAST                '_image_height_new'
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

 L. 613       158  LOAD_GLOBAL              vis_msg
              160  LOAD_ATTR                print
              162  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 614       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 615       182  LOAD_STR                 'Train 1.5D-DCNN'

 L. 616       184  LOAD_STR                 'Non-integer feature size'
              186  CALL_METHOD_3         3  '3 positional arguments'
              188  POP_TOP          

 L. 617       190  LOAD_CONST               None
              192  RETURN_VALUE     
            194_0  COME_FROM           156  '156'

 L. 618       194  LOAD_FAST                '_image_height'
              196  LOAD_CONST               2
              198  COMPARE_OP               <
              200  POP_JUMP_IF_TRUE    228  'to 228'
              202  LOAD_FAST                '_image_width'
              204  LOAD_CONST               2
              206  COMPARE_OP               <
              208  POP_JUMP_IF_TRUE    228  'to 228'

 L. 619       210  LOAD_FAST                '_image_height_new'
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

 L. 620       228  LOAD_GLOBAL              vis_msg
              230  LOAD_ATTR                print
              232  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 621       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 622       252  LOAD_STR                 'Train 1.5D-DCNN'

 L. 623       254  LOAD_STR                 'Features are not 2D'
              256  CALL_METHOD_3         3  '3 positional arguments'
              258  POP_TOP          

 L. 624       260  LOAD_CONST               None
              262  RETURN_VALUE     
            264_0  COME_FROM           224  '224'

 L. 626       264  LOAD_CONST               2
              266  LOAD_GLOBAL              int
              268  LOAD_FAST                '_image_height'
              270  LOAD_CONST               2
              272  BINARY_TRUE_DIVIDE
              274  CALL_FUNCTION_1       1  '1 positional argument'
              276  BINARY_MULTIPLY  
              278  LOAD_CONST               1
              280  BINARY_ADD       
              282  STORE_FAST               '_image_height'

 L. 627       284  LOAD_CONST               2
              286  LOAD_GLOBAL              int
              288  LOAD_FAST                '_image_width'
              290  LOAD_CONST               2
              292  BINARY_TRUE_DIVIDE
              294  CALL_FUNCTION_1       1  '1 positional argument'
              296  BINARY_MULTIPLY  
              298  LOAD_CONST               1
              300  BINARY_ADD       
              302  STORE_FAST               '_image_width'

 L. 629       304  LOAD_DEREF               'self'
              306  LOAD_ATTR                lwgfeature
              308  LOAD_METHOD              selectedItems
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               '_features'

 L. 630       314  LOAD_LISTCOMP            '<code_object <listcomp>>'
              316  LOAD_STR                 'trainml15ddcnnfromexisting.clickBtnTrainMl15DDcnnFromExisting.<locals>.<listcomp>'
              318  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              320  LOAD_FAST                '_features'
              322  GET_ITER         
              324  CALL_FUNCTION_1       1  '1 positional argument'
              326  STORE_FAST               '_features'

 L. 631       328  LOAD_DEREF               'self'
              330  LOAD_ATTR                featurelist
              332  LOAD_DEREF               'self'
              334  LOAD_ATTR                cbbtarget
              336  LOAD_METHOD              currentIndex
              338  CALL_METHOD_0         0  '0 positional arguments'
              340  BINARY_SUBSCR    
              342  STORE_FAST               '_target'

 L. 633       344  LOAD_FAST                '_target'
              346  LOAD_FAST                '_features'
              348  COMPARE_OP               in
          350_352  POP_JUMP_IF_FALSE   390  'to 390'

 L. 634       354  LOAD_GLOBAL              vis_msg
              356  LOAD_ATTR                print
              358  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Target also used as features'
              360  LOAD_STR                 'error'
              362  LOAD_CONST               ('type',)
              364  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              366  POP_TOP          

 L. 635       368  LOAD_GLOBAL              QtWidgets
              370  LOAD_ATTR                QMessageBox
              372  LOAD_METHOD              critical
              374  LOAD_DEREF               'self'
              376  LOAD_ATTR                msgbox

 L. 636       378  LOAD_STR                 'Train 1.5D-DCNN'

 L. 637       380  LOAD_STR                 'Target also used as features'
              382  CALL_METHOD_3         3  '3 positional arguments'
              384  POP_TOP          

 L. 638       386  LOAD_CONST               None
              388  RETURN_VALUE     
            390_0  COME_FROM           350  '350'

 L. 640       390  LOAD_GLOBAL              len
              392  LOAD_DEREF               'self'
              394  LOAD_ATTR                ldtexisting
              396  LOAD_METHOD              text
              398  CALL_METHOD_0         0  '0 positional arguments'
              400  CALL_FUNCTION_1       1  '1 positional argument'
              402  LOAD_CONST               1
              404  COMPARE_OP               <
          406_408  POP_JUMP_IF_FALSE   446  'to 446'

 L. 641       410  LOAD_GLOBAL              vis_msg
              412  LOAD_ATTR                print
              414  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: No name specified for pre-trained network'

 L. 642       416  LOAD_STR                 'error'
              418  LOAD_CONST               ('type',)
              420  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              422  POP_TOP          

 L. 643       424  LOAD_GLOBAL              QtWidgets
              426  LOAD_ATTR                QMessageBox
              428  LOAD_METHOD              critical
              430  LOAD_DEREF               'self'
              432  LOAD_ATTR                msgbox

 L. 644       434  LOAD_STR                 'Train 1.5D-DCNN'

 L. 645       436  LOAD_STR                 'No name specified for pre-trained network'
              438  CALL_METHOD_3         3  '3 positional arguments'
              440  POP_TOP          

 L. 646       442  LOAD_CONST               None
              444  RETURN_VALUE     
            446_0  COME_FROM           406  '406'

 L. 647       446  LOAD_GLOBAL              os
              448  LOAD_ATTR                path
              450  LOAD_METHOD              dirname
              452  LOAD_DEREF               'self'
              454  LOAD_ATTR                ldtexisting
              456  LOAD_METHOD              text
              458  CALL_METHOD_0         0  '0 positional arguments'
              460  CALL_METHOD_1         1  '1 positional argument'
              462  STORE_FAST               '_precnnpath'

 L. 648       464  LOAD_GLOBAL              os
              466  LOAD_ATTR                path
              468  LOAD_METHOD              splitext
              470  LOAD_GLOBAL              os
              472  LOAD_ATTR                path
              474  LOAD_METHOD              basename
              476  LOAD_DEREF               'self'
              478  LOAD_ATTR                ldtexisting
              480  LOAD_METHOD              text
              482  CALL_METHOD_0         0  '0 positional arguments'
              484  CALL_METHOD_1         1  '1 positional argument'
              486  CALL_METHOD_1         1  '1 positional argument'
              488  LOAD_CONST               0
              490  BINARY_SUBSCR    
              492  STORE_FAST               '_precnnname'

 L. 649       494  LOAD_DEREF               'self'
              496  LOAD_ATTR                cbbblockid
              498  LOAD_METHOD              currentIndex
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  STORE_FAST               '_blockidx'

 L. 650       504  LOAD_DEREF               'self'
              506  LOAD_ATTR                cbblayerid
              508  LOAD_METHOD              currentIndex
              510  CALL_METHOD_0         0  '0 positional arguments'
              512  STORE_FAST               '_layeridx'

 L. 651       514  LOAD_CONST               True
              516  STORE_FAST               '_trainable'

 L. 652       518  LOAD_DEREF               'self'
              520  LOAD_ATTR                cbbtrainable
              522  LOAD_METHOD              currentIndex
              524  CALL_METHOD_0         0  '0 positional arguments'
              526  LOAD_CONST               0
              528  COMPARE_OP               !=
          530_532  POP_JUMP_IF_FALSE   538  'to 538'

 L. 653       534  LOAD_CONST               False
              536  STORE_FAST               '_trainable'
            538_0  COME_FROM           530  '530'

 L. 655       538  LOAD_GLOBAL              ml_tfm
              540  LOAD_METHOD              getConvModelNChannel
              542  LOAD_FAST                '_precnnpath'
              544  LOAD_FAST                '_precnnname'
              546  CALL_METHOD_2         2  '2 positional arguments'
              548  LOAD_GLOBAL              len
              550  LOAD_FAST                '_features'
              552  CALL_FUNCTION_1       1  '1 positional argument'
              554  COMPARE_OP               !=
          556_558  POP_JUMP_IF_FALSE   596  'to 596'

 L. 656       560  LOAD_GLOBAL              vis_msg
              562  LOAD_ATTR                print
              564  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Feature channel number not match with pre-trained network'

 L. 657       566  LOAD_STR                 'error'
              568  LOAD_CONST               ('type',)
              570  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              572  POP_TOP          

 L. 658       574  LOAD_GLOBAL              QtWidgets
              576  LOAD_ATTR                QMessageBox
              578  LOAD_METHOD              critical
              580  LOAD_DEREF               'self'
              582  LOAD_ATTR                msgbox

 L. 659       584  LOAD_STR                 'Train 1.5D-DCNN'

 L. 660       586  LOAD_STR                 'Feature channel number not match with pre-trained network'
              588  CALL_METHOD_3         3  '3 positional arguments'
              590  POP_TOP          

 L. 661       592  LOAD_CONST               None
              594  RETURN_VALUE     
            596_0  COME_FROM           556  '556'

 L. 663       596  LOAD_GLOBAL              basic_data
              598  LOAD_METHOD              str2int
              600  LOAD_DEREF               'self'
              602  LOAD_ATTR                ldtnconvblock
              604  LOAD_METHOD              text
              606  CALL_METHOD_0         0  '0 positional arguments'
              608  CALL_METHOD_1         1  '1 positional argument'
              610  STORE_FAST               '_nconvblock'

 L. 664       612  LOAD_CLOSURE             'self'
              614  BUILD_TUPLE_1         1 
              616  LOAD_LISTCOMP            '<code_object <listcomp>>'
              618  LOAD_STR                 'trainml15ddcnnfromexisting.clickBtnTrainMl15DDcnnFromExisting.<locals>.<listcomp>'
              620  MAKE_FUNCTION_8          'closure'
              622  LOAD_GLOBAL              range
              624  LOAD_FAST                '_nconvblock'
              626  CALL_FUNCTION_1       1  '1 positional argument'
              628  GET_ITER         
              630  CALL_FUNCTION_1       1  '1 positional argument'
              632  STORE_FAST               '_nconvlayer'

 L. 665       634  LOAD_CLOSURE             'self'
              636  BUILD_TUPLE_1         1 
              638  LOAD_LISTCOMP            '<code_object <listcomp>>'
              640  LOAD_STR                 'trainml15ddcnnfromexisting.clickBtnTrainMl15DDcnnFromExisting.<locals>.<listcomp>'
              642  MAKE_FUNCTION_8          'closure'
              644  LOAD_GLOBAL              range
              646  LOAD_FAST                '_nconvblock'
              648  CALL_FUNCTION_1       1  '1 positional argument'
              650  GET_ITER         
              652  CALL_FUNCTION_1       1  '1 positional argument'
              654  STORE_FAST               '_nconvfeature'

 L. 666       656  LOAD_GLOBAL              basic_data
              658  LOAD_METHOD              str2int
              660  LOAD_DEREF               'self'
              662  LOAD_ATTR                ldtn1x1layer
              664  LOAD_METHOD              text
              666  CALL_METHOD_0         0  '0 positional arguments'
              668  CALL_METHOD_1         1  '1 positional argument'
              670  STORE_FAST               '_n1x1layer'

 L. 667       672  LOAD_CLOSURE             'self'
              674  BUILD_TUPLE_1         1 
              676  LOAD_LISTCOMP            '<code_object <listcomp>>'
              678  LOAD_STR                 'trainml15ddcnnfromexisting.clickBtnTrainMl15DDcnnFromExisting.<locals>.<listcomp>'
              680  MAKE_FUNCTION_8          'closure'
              682  LOAD_GLOBAL              range
              684  LOAD_FAST                '_n1x1layer'
              686  CALL_FUNCTION_1       1  '1 positional argument'
              688  GET_ITER         
              690  CALL_FUNCTION_1       1  '1 positional argument'
              692  STORE_FAST               '_n1x1feature'

 L. 668       694  LOAD_GLOBAL              basic_data
              696  LOAD_METHOD              str2int
              698  LOAD_DEREF               'self'
              700  LOAD_ATTR                ldtmaskheight
              702  LOAD_METHOD              text
              704  CALL_METHOD_0         0  '0 positional arguments'
              706  CALL_METHOD_1         1  '1 positional argument'
              708  STORE_FAST               '_patch_height'

 L. 669       710  LOAD_GLOBAL              basic_data
              712  LOAD_METHOD              str2int
              714  LOAD_DEREF               'self'
              716  LOAD_ATTR                ldtmaskwidth
              718  LOAD_METHOD              text
              720  CALL_METHOD_0         0  '0 positional arguments'
              722  CALL_METHOD_1         1  '1 positional argument'
              724  STORE_FAST               '_patch_width'

 L. 670       726  LOAD_GLOBAL              basic_data
              728  LOAD_METHOD              str2int
              730  LOAD_DEREF               'self'
              732  LOAD_ATTR                ldtpoolheight
              734  LOAD_METHOD              text
              736  CALL_METHOD_0         0  '0 positional arguments'
              738  CALL_METHOD_1         1  '1 positional argument'
              740  STORE_FAST               '_pool_height'

 L. 671       742  LOAD_GLOBAL              basic_data
              744  LOAD_METHOD              str2int
              746  LOAD_DEREF               'self'
              748  LOAD_ATTR                ldtpoolwidth
              750  LOAD_METHOD              text
              752  CALL_METHOD_0         0  '0 positional arguments'
              754  CALL_METHOD_1         1  '1 positional argument'
              756  STORE_FAST               '_pool_width'

 L. 672       758  LOAD_GLOBAL              basic_data
              760  LOAD_METHOD              str2int
              762  LOAD_DEREF               'self'
              764  LOAD_ATTR                ldtnepoch
              766  LOAD_METHOD              text
              768  CALL_METHOD_0         0  '0 positional arguments'
              770  CALL_METHOD_1         1  '1 positional argument'
              772  STORE_FAST               '_nepoch'

 L. 673       774  LOAD_GLOBAL              basic_data
              776  LOAD_METHOD              str2int
              778  LOAD_DEREF               'self'
              780  LOAD_ATTR                ldtbatchsize
              782  LOAD_METHOD              text
              784  CALL_METHOD_0         0  '0 positional arguments'
              786  CALL_METHOD_1         1  '1 positional argument'
              788  STORE_FAST               '_batchsize'

 L. 674       790  LOAD_GLOBAL              basic_data
              792  LOAD_METHOD              str2float
              794  LOAD_DEREF               'self'
              796  LOAD_ATTR                ldtlearnrate
              798  LOAD_METHOD              text
              800  CALL_METHOD_0         0  '0 positional arguments'
              802  CALL_METHOD_1         1  '1 positional argument'
              804  STORE_FAST               '_learning_rate'

 L. 675       806  LOAD_GLOBAL              basic_data
              808  LOAD_METHOD              str2float
              810  LOAD_DEREF               'self'
              812  LOAD_ATTR                ldtdropout
              814  LOAD_METHOD              text
              816  CALL_METHOD_0         0  '0 positional arguments'
              818  CALL_METHOD_1         1  '1 positional argument'
              820  STORE_FAST               '_dropout_prob'

 L. 676       822  LOAD_FAST                '_nconvblock'
              824  LOAD_CONST               False
              826  COMPARE_OP               is
          828_830  POP_JUMP_IF_TRUE    842  'to 842'
              832  LOAD_FAST                '_nconvblock'
              834  LOAD_CONST               0
              836  COMPARE_OP               <=
          838_840  POP_JUMP_IF_FALSE   878  'to 878'
            842_0  COME_FROM           828  '828'

 L. 677       842  LOAD_GLOBAL              vis_msg
              844  LOAD_ATTR                print
              846  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Non-positive convolutional block number'
              848  LOAD_STR                 'error'
              850  LOAD_CONST               ('type',)
              852  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              854  POP_TOP          

 L. 678       856  LOAD_GLOBAL              QtWidgets
              858  LOAD_ATTR                QMessageBox
              860  LOAD_METHOD              critical
              862  LOAD_DEREF               'self'
              864  LOAD_ATTR                msgbox

 L. 679       866  LOAD_STR                 'Train 1.5D-DCNN'

 L. 680       868  LOAD_STR                 'Non-positive convolutional block number'
              870  CALL_METHOD_3         3  '3 positional arguments'
              872  POP_TOP          

 L. 681       874  LOAD_CONST               None
              876  RETURN_VALUE     
            878_0  COME_FROM           838  '838'

 L. 682       878  SETUP_LOOP          950  'to 950'
              880  LOAD_FAST                '_nconvlayer'
              882  GET_ITER         
            884_0  COME_FROM           904  '904'
              884  FOR_ITER            948  'to 948'
              886  STORE_FAST               '_i'

 L. 683       888  LOAD_FAST                '_i'
              890  LOAD_CONST               False
              892  COMPARE_OP               is
          894_896  POP_JUMP_IF_TRUE    908  'to 908'
              898  LOAD_FAST                '_i'
              900  LOAD_CONST               1
              902  COMPARE_OP               <
          904_906  POP_JUMP_IF_FALSE   884  'to 884'
            908_0  COME_FROM           894  '894'

 L. 684       908  LOAD_GLOBAL              vis_msg
              910  LOAD_ATTR                print
              912  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Non-positive convolutional layer number'

 L. 685       914  LOAD_STR                 'error'
              916  LOAD_CONST               ('type',)
              918  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              920  POP_TOP          

 L. 686       922  LOAD_GLOBAL              QtWidgets
              924  LOAD_ATTR                QMessageBox
              926  LOAD_METHOD              critical
              928  LOAD_DEREF               'self'
              930  LOAD_ATTR                msgbox

 L. 687       932  LOAD_STR                 'Train 1.5D-DCNN'

 L. 688       934  LOAD_STR                 'Non-positive convolutional layer number'
              936  CALL_METHOD_3         3  '3 positional arguments'
              938  POP_TOP          

 L. 689       940  LOAD_CONST               None
              942  RETURN_VALUE     
          944_946  JUMP_BACK           884  'to 884'
              948  POP_BLOCK        
            950_0  COME_FROM_LOOP      878  '878'

 L. 690       950  SETUP_LOOP         1022  'to 1022'
              952  LOAD_FAST                '_nconvfeature'
              954  GET_ITER         
            956_0  COME_FROM           976  '976'
              956  FOR_ITER           1020  'to 1020'
              958  STORE_FAST               '_i'

 L. 691       960  LOAD_FAST                '_i'
              962  LOAD_CONST               False
              964  COMPARE_OP               is
          966_968  POP_JUMP_IF_TRUE    980  'to 980'
              970  LOAD_FAST                '_i'
              972  LOAD_CONST               1
              974  COMPARE_OP               <
          976_978  POP_JUMP_IF_FALSE   956  'to 956'
            980_0  COME_FROM           966  '966'

 L. 692       980  LOAD_GLOBAL              vis_msg
              982  LOAD_ATTR                print
              984  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Non-positive convolutional feature number'

 L. 693       986  LOAD_STR                 'error'
              988  LOAD_CONST               ('type',)
              990  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              992  POP_TOP          

 L. 694       994  LOAD_GLOBAL              QtWidgets
              996  LOAD_ATTR                QMessageBox
              998  LOAD_METHOD              critical
             1000  LOAD_DEREF               'self'
             1002  LOAD_ATTR                msgbox

 L. 695      1004  LOAD_STR                 'Train 1.5D-DCNN'

 L. 696      1006  LOAD_STR                 'Non-positive convolutional feature number'
             1008  CALL_METHOD_3         3  '3 positional arguments'
             1010  POP_TOP          

 L. 697      1012  LOAD_CONST               None
             1014  RETURN_VALUE     
         1016_1018  JUMP_BACK           956  'to 956'
             1020  POP_BLOCK        
           1022_0  COME_FROM_LOOP      950  '950'

 L. 698      1022  LOAD_FAST                '_n1x1layer'
             1024  LOAD_CONST               False
             1026  COMPARE_OP               is
         1028_1030  POP_JUMP_IF_TRUE   1042  'to 1042'
             1032  LOAD_FAST                '_n1x1layer'
             1034  LOAD_CONST               0
             1036  COMPARE_OP               <=
         1038_1040  POP_JUMP_IF_FALSE  1078  'to 1078'
           1042_0  COME_FROM          1028  '1028'

 L. 699      1042  LOAD_GLOBAL              vis_msg
             1044  LOAD_ATTR                print
             1046  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Non-positive 1x1 convolutional layer number'

 L. 700      1048  LOAD_STR                 'error'
             1050  LOAD_CONST               ('type',)
             1052  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1054  POP_TOP          

 L. 701      1056  LOAD_GLOBAL              QtWidgets
             1058  LOAD_ATTR                QMessageBox
             1060  LOAD_METHOD              critical
             1062  LOAD_DEREF               'self'
             1064  LOAD_ATTR                msgbox

 L. 702      1066  LOAD_STR                 'Train 1.5D-DCNN'

 L. 703      1068  LOAD_STR                 'Non-positive 1x1 convolutional layer number'
             1070  CALL_METHOD_3         3  '3 positional arguments'
             1072  POP_TOP          

 L. 704      1074  LOAD_CONST               None
             1076  RETURN_VALUE     
           1078_0  COME_FROM          1038  '1038'

 L. 705      1078  SETUP_LOOP         1150  'to 1150'
             1080  LOAD_FAST                '_n1x1feature'
             1082  GET_ITER         
           1084_0  COME_FROM          1104  '1104'
             1084  FOR_ITER           1148  'to 1148'
             1086  STORE_FAST               '_i'

 L. 706      1088  LOAD_FAST                '_i'
             1090  LOAD_CONST               False
             1092  COMPARE_OP               is
         1094_1096  POP_JUMP_IF_TRUE   1108  'to 1108'
             1098  LOAD_FAST                '_i'
             1100  LOAD_CONST               1
             1102  COMPARE_OP               <
         1104_1106  POP_JUMP_IF_FALSE  1084  'to 1084'
           1108_0  COME_FROM          1094  '1094'

 L. 707      1108  LOAD_GLOBAL              vis_msg
             1110  LOAD_ATTR                print
             1112  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Non-positive 1x1 convolutional feature number'

 L. 708      1114  LOAD_STR                 'error'
             1116  LOAD_CONST               ('type',)
             1118  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1120  POP_TOP          

 L. 709      1122  LOAD_GLOBAL              QtWidgets
             1124  LOAD_ATTR                QMessageBox
             1126  LOAD_METHOD              critical
             1128  LOAD_DEREF               'self'
             1130  LOAD_ATTR                msgbox

 L. 710      1132  LOAD_STR                 'Train 1.5D-DCNN'

 L. 711      1134  LOAD_STR                 'Non-positive 1x1 convolutional feature number'
             1136  CALL_METHOD_3         3  '3 positional arguments'
             1138  POP_TOP          

 L. 712      1140  LOAD_CONST               None
             1142  RETURN_VALUE     
         1144_1146  JUMP_BACK          1084  'to 1084'
             1148  POP_BLOCK        
           1150_0  COME_FROM_LOOP     1078  '1078'

 L. 713      1150  LOAD_FAST                '_patch_height'
             1152  LOAD_CONST               False
             1154  COMPARE_OP               is
         1156_1158  POP_JUMP_IF_TRUE   1190  'to 1190'
             1160  LOAD_FAST                '_patch_width'
             1162  LOAD_CONST               False
             1164  COMPARE_OP               is
         1166_1168  POP_JUMP_IF_TRUE   1190  'to 1190'

 L. 714      1170  LOAD_FAST                '_patch_height'
             1172  LOAD_CONST               1
             1174  COMPARE_OP               <
         1176_1178  POP_JUMP_IF_TRUE   1190  'to 1190'
             1180  LOAD_FAST                '_patch_width'
             1182  LOAD_CONST               1
             1184  COMPARE_OP               <
         1186_1188  POP_JUMP_IF_FALSE  1226  'to 1226'
           1190_0  COME_FROM          1176  '1176'
           1190_1  COME_FROM          1166  '1166'
           1190_2  COME_FROM          1156  '1156'

 L. 715      1190  LOAD_GLOBAL              vis_msg
             1192  LOAD_ATTR                print
             1194  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Non-positive convolutional patch size'
             1196  LOAD_STR                 'error'
             1198  LOAD_CONST               ('type',)
             1200  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1202  POP_TOP          

 L. 716      1204  LOAD_GLOBAL              QtWidgets
             1206  LOAD_ATTR                QMessageBox
             1208  LOAD_METHOD              critical
             1210  LOAD_DEREF               'self'
             1212  LOAD_ATTR                msgbox

 L. 717      1214  LOAD_STR                 'Train 1.5D-DCNN'

 L. 718      1216  LOAD_STR                 'Non-positive convolutional patch size'
             1218  CALL_METHOD_3         3  '3 positional arguments'
             1220  POP_TOP          

 L. 719      1222  LOAD_CONST               None
             1224  RETURN_VALUE     
           1226_0  COME_FROM          1186  '1186'

 L. 720      1226  LOAD_FAST                '_pool_height'
             1228  LOAD_CONST               False
             1230  COMPARE_OP               is
         1232_1234  POP_JUMP_IF_TRUE   1266  'to 1266'
             1236  LOAD_FAST                '_pool_width'
             1238  LOAD_CONST               False
             1240  COMPARE_OP               is
         1242_1244  POP_JUMP_IF_TRUE   1266  'to 1266'

 L. 721      1246  LOAD_FAST                '_pool_height'
             1248  LOAD_CONST               1
             1250  COMPARE_OP               <
         1252_1254  POP_JUMP_IF_TRUE   1266  'to 1266'
             1256  LOAD_FAST                '_pool_width'
             1258  LOAD_CONST               1
             1260  COMPARE_OP               <
         1262_1264  POP_JUMP_IF_FALSE  1302  'to 1302'
           1266_0  COME_FROM          1252  '1252'
           1266_1  COME_FROM          1242  '1242'
           1266_2  COME_FROM          1232  '1232'

 L. 722      1266  LOAD_GLOBAL              vis_msg
             1268  LOAD_ATTR                print
             1270  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Non-positive pooling size'
             1272  LOAD_STR                 'error'
             1274  LOAD_CONST               ('type',)
             1276  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1278  POP_TOP          

 L. 723      1280  LOAD_GLOBAL              QtWidgets
             1282  LOAD_ATTR                QMessageBox
             1284  LOAD_METHOD              critical
             1286  LOAD_DEREF               'self'
             1288  LOAD_ATTR                msgbox

 L. 724      1290  LOAD_STR                 'Train 1.5D-DCNN'

 L. 725      1292  LOAD_STR                 'Non-positive pooling size'
             1294  CALL_METHOD_3         3  '3 positional arguments'
             1296  POP_TOP          

 L. 726      1298  LOAD_CONST               None
             1300  RETURN_VALUE     
           1302_0  COME_FROM          1262  '1262'

 L. 727      1302  LOAD_FAST                '_nepoch'
             1304  LOAD_CONST               False
             1306  COMPARE_OP               is
         1308_1310  POP_JUMP_IF_TRUE   1322  'to 1322'
             1312  LOAD_FAST                '_nepoch'
             1314  LOAD_CONST               0
             1316  COMPARE_OP               <=
         1318_1320  POP_JUMP_IF_FALSE  1358  'to 1358'
           1322_0  COME_FROM          1308  '1308'

 L. 728      1322  LOAD_GLOBAL              vis_msg
             1324  LOAD_ATTR                print
             1326  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Non-positive epoch number'
             1328  LOAD_STR                 'error'
             1330  LOAD_CONST               ('type',)
             1332  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1334  POP_TOP          

 L. 729      1336  LOAD_GLOBAL              QtWidgets
             1338  LOAD_ATTR                QMessageBox
             1340  LOAD_METHOD              critical
             1342  LOAD_DEREF               'self'
             1344  LOAD_ATTR                msgbox

 L. 730      1346  LOAD_STR                 'Train 1.5D-DCNN'

 L. 731      1348  LOAD_STR                 'Non-positive epoch number'
             1350  CALL_METHOD_3         3  '3 positional arguments'
             1352  POP_TOP          

 L. 732      1354  LOAD_CONST               None
             1356  RETURN_VALUE     
           1358_0  COME_FROM          1318  '1318'

 L. 733      1358  LOAD_FAST                '_batchsize'
             1360  LOAD_CONST               False
             1362  COMPARE_OP               is
         1364_1366  POP_JUMP_IF_TRUE   1378  'to 1378'
             1368  LOAD_FAST                '_batchsize'
             1370  LOAD_CONST               0
             1372  COMPARE_OP               <=
         1374_1376  POP_JUMP_IF_FALSE  1414  'to 1414'
           1378_0  COME_FROM          1364  '1364'

 L. 734      1378  LOAD_GLOBAL              vis_msg
             1380  LOAD_ATTR                print
             1382  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Non-positive batch size'
             1384  LOAD_STR                 'error'
             1386  LOAD_CONST               ('type',)
             1388  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1390  POP_TOP          

 L. 735      1392  LOAD_GLOBAL              QtWidgets
             1394  LOAD_ATTR                QMessageBox
             1396  LOAD_METHOD              critical
             1398  LOAD_DEREF               'self'
             1400  LOAD_ATTR                msgbox

 L. 736      1402  LOAD_STR                 'Train 1.5D-DCNN'

 L. 737      1404  LOAD_STR                 'Non-positive batch size'
             1406  CALL_METHOD_3         3  '3 positional arguments'
             1408  POP_TOP          

 L. 738      1410  LOAD_CONST               None
             1412  RETURN_VALUE     
           1414_0  COME_FROM          1374  '1374'

 L. 739      1414  LOAD_FAST                '_learning_rate'
             1416  LOAD_CONST               False
             1418  COMPARE_OP               is
         1420_1422  POP_JUMP_IF_TRUE   1434  'to 1434'
             1424  LOAD_FAST                '_learning_rate'
             1426  LOAD_CONST               0
             1428  COMPARE_OP               <=
         1430_1432  POP_JUMP_IF_FALSE  1470  'to 1470'
           1434_0  COME_FROM          1420  '1420'

 L. 740      1434  LOAD_GLOBAL              vis_msg
             1436  LOAD_ATTR                print
             1438  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Non-positive learning rate'
             1440  LOAD_STR                 'error'
             1442  LOAD_CONST               ('type',)
             1444  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1446  POP_TOP          

 L. 741      1448  LOAD_GLOBAL              QtWidgets
             1450  LOAD_ATTR                QMessageBox
             1452  LOAD_METHOD              critical
             1454  LOAD_DEREF               'self'
             1456  LOAD_ATTR                msgbox

 L. 742      1458  LOAD_STR                 'Train 1.5D-DCNN'

 L. 743      1460  LOAD_STR                 'Non-positive learning rate'
             1462  CALL_METHOD_3         3  '3 positional arguments'
             1464  POP_TOP          

 L. 744      1466  LOAD_CONST               None
             1468  RETURN_VALUE     
           1470_0  COME_FROM          1430  '1430'

 L. 745      1470  LOAD_FAST                '_dropout_prob'
             1472  LOAD_CONST               False
             1474  COMPARE_OP               is
         1476_1478  POP_JUMP_IF_TRUE   1490  'to 1490'
             1480  LOAD_FAST                '_dropout_prob'
             1482  LOAD_CONST               0
             1484  COMPARE_OP               <=
         1486_1488  POP_JUMP_IF_FALSE  1526  'to 1526'
           1490_0  COME_FROM          1476  '1476'

 L. 746      1490  LOAD_GLOBAL              vis_msg
             1492  LOAD_ATTR                print
             1494  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: Negative dropout rate'
             1496  LOAD_STR                 'error'
             1498  LOAD_CONST               ('type',)
             1500  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1502  POP_TOP          

 L. 747      1504  LOAD_GLOBAL              QtWidgets
             1506  LOAD_ATTR                QMessageBox
             1508  LOAD_METHOD              critical
             1510  LOAD_DEREF               'self'
             1512  LOAD_ATTR                msgbox

 L. 748      1514  LOAD_STR                 'Train 1.5D-DCNN'

 L. 749      1516  LOAD_STR                 'Negative dropout rate'
             1518  CALL_METHOD_3         3  '3 positional arguments'
             1520  POP_TOP          

 L. 750      1522  LOAD_CONST               None
             1524  RETURN_VALUE     
           1526_0  COME_FROM          1486  '1486'

 L. 752      1526  LOAD_GLOBAL              len
             1528  LOAD_DEREF               'self'
             1530  LOAD_ATTR                ldtsave
             1532  LOAD_METHOD              text
             1534  CALL_METHOD_0         0  '0 positional arguments'
             1536  CALL_FUNCTION_1       1  '1 positional argument'
             1538  LOAD_CONST               1
             1540  COMPARE_OP               <
         1542_1544  POP_JUMP_IF_FALSE  1582  'to 1582'

 L. 753      1546  LOAD_GLOBAL              vis_msg
             1548  LOAD_ATTR                print
             1550  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: No name specified for DCNN network'
             1552  LOAD_STR                 'error'
             1554  LOAD_CONST               ('type',)
             1556  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1558  POP_TOP          

 L. 754      1560  LOAD_GLOBAL              QtWidgets
             1562  LOAD_ATTR                QMessageBox
             1564  LOAD_METHOD              critical
             1566  LOAD_DEREF               'self'
             1568  LOAD_ATTR                msgbox

 L. 755      1570  LOAD_STR                 'Train 1.5D-DCNN'

 L. 756      1572  LOAD_STR                 'No name specified for DCNN network'
             1574  CALL_METHOD_3         3  '3 positional arguments'
             1576  POP_TOP          

 L. 757      1578  LOAD_CONST               None
             1580  RETURN_VALUE     
           1582_0  COME_FROM          1542  '1542'

 L. 758      1582  LOAD_GLOBAL              os
             1584  LOAD_ATTR                path
             1586  LOAD_METHOD              dirname
             1588  LOAD_DEREF               'self'
             1590  LOAD_ATTR                ldtsave
             1592  LOAD_METHOD              text
             1594  CALL_METHOD_0         0  '0 positional arguments'
             1596  CALL_METHOD_1         1  '1 positional argument'
             1598  STORE_FAST               '_savepath'

 L. 759      1600  LOAD_GLOBAL              os
             1602  LOAD_ATTR                path
             1604  LOAD_METHOD              splitext
             1606  LOAD_GLOBAL              os
             1608  LOAD_ATTR                path
             1610  LOAD_METHOD              basename
             1612  LOAD_DEREF               'self'
             1614  LOAD_ATTR                ldtsave
             1616  LOAD_METHOD              text
             1618  CALL_METHOD_0         0  '0 positional arguments'
             1620  CALL_METHOD_1         1  '1 positional argument'
             1622  CALL_METHOD_1         1  '1 positional argument'
             1624  LOAD_CONST               0
             1626  BINARY_SUBSCR    
             1628  STORE_FAST               '_savename'

 L. 761      1630  LOAD_CONST               0
             1632  STORE_FAST               '_wdinl'

 L. 762      1634  LOAD_CONST               0
             1636  STORE_FAST               '_wdxl'

 L. 763      1638  LOAD_CONST               0
             1640  STORE_FAST               '_wdz'

 L. 764      1642  LOAD_CONST               0
             1644  STORE_FAST               '_wdinltarget'

 L. 765      1646  LOAD_CONST               0
             1648  STORE_FAST               '_wdxltarget'

 L. 766      1650  LOAD_CONST               0
             1652  STORE_FAST               '_wdztarget'

 L. 767      1654  LOAD_DEREF               'self'
             1656  LOAD_ATTR                cbbornt
             1658  LOAD_METHOD              currentIndex
             1660  CALL_METHOD_0         0  '0 positional arguments'
             1662  LOAD_CONST               0
             1664  COMPARE_OP               ==
         1666_1668  POP_JUMP_IF_FALSE  1706  'to 1706'

 L. 768      1670  LOAD_GLOBAL              int
             1672  LOAD_FAST                '_image_width'
             1674  LOAD_CONST               2
             1676  BINARY_TRUE_DIVIDE
             1678  CALL_FUNCTION_1       1  '1 positional argument'
             1680  STORE_FAST               '_wdxl'

 L. 769      1682  LOAD_GLOBAL              int
             1684  LOAD_FAST                '_image_height'
             1686  LOAD_CONST               2
             1688  BINARY_TRUE_DIVIDE
             1690  CALL_FUNCTION_1       1  '1 positional argument'
             1692  STORE_FAST               '_wdz'

 L. 770      1694  LOAD_GLOBAL              int
             1696  LOAD_FAST                '_image_height'
             1698  LOAD_CONST               2
             1700  BINARY_TRUE_DIVIDE
             1702  CALL_FUNCTION_1       1  '1 positional argument'
             1704  STORE_FAST               '_wdztarget'
           1706_0  COME_FROM          1666  '1666'

 L. 771      1706  LOAD_DEREF               'self'
             1708  LOAD_ATTR                cbbornt
             1710  LOAD_METHOD              currentIndex
             1712  CALL_METHOD_0         0  '0 positional arguments'
             1714  LOAD_CONST               1
             1716  COMPARE_OP               ==
         1718_1720  POP_JUMP_IF_FALSE  1758  'to 1758'

 L. 772      1722  LOAD_GLOBAL              int
             1724  LOAD_FAST                '_image_width'
             1726  LOAD_CONST               2
             1728  BINARY_TRUE_DIVIDE
             1730  CALL_FUNCTION_1       1  '1 positional argument'
             1732  STORE_FAST               '_wdinl'

 L. 773      1734  LOAD_GLOBAL              int
             1736  LOAD_FAST                '_image_height'
             1738  LOAD_CONST               2
             1740  BINARY_TRUE_DIVIDE
             1742  CALL_FUNCTION_1       1  '1 positional argument'
             1744  STORE_FAST               '_wdz'

 L. 774      1746  LOAD_GLOBAL              int
             1748  LOAD_FAST                '_image_height'
             1750  LOAD_CONST               2
             1752  BINARY_TRUE_DIVIDE
             1754  CALL_FUNCTION_1       1  '1 positional argument'
             1756  STORE_FAST               '_wdztarget'
           1758_0  COME_FROM          1718  '1718'

 L. 775      1758  LOAD_DEREF               'self'
             1760  LOAD_ATTR                cbbornt
             1762  LOAD_METHOD              currentIndex
             1764  CALL_METHOD_0         0  '0 positional arguments'
             1766  LOAD_CONST               2
             1768  COMPARE_OP               ==
         1770_1772  POP_JUMP_IF_FALSE  1810  'to 1810'

 L. 776      1774  LOAD_GLOBAL              int
             1776  LOAD_FAST                '_image_width'
             1778  LOAD_CONST               2
             1780  BINARY_TRUE_DIVIDE
             1782  CALL_FUNCTION_1       1  '1 positional argument'
             1784  STORE_FAST               '_wdinl'

 L. 777      1786  LOAD_GLOBAL              int
             1788  LOAD_FAST                '_image_height'
             1790  LOAD_CONST               2
             1792  BINARY_TRUE_DIVIDE
             1794  CALL_FUNCTION_1       1  '1 positional argument'
             1796  STORE_FAST               '_wdxl'

 L. 778      1798  LOAD_GLOBAL              int
             1800  LOAD_FAST                '_image_height'
             1802  LOAD_CONST               2
             1804  BINARY_TRUE_DIVIDE
             1806  CALL_FUNCTION_1       1  '1 positional argument'
             1808  STORE_FAST               '_wdxltarget'
           1810_0  COME_FROM          1770  '1770'

 L. 780      1810  LOAD_DEREF               'self'
             1812  LOAD_ATTR                survinfo
             1814  STORE_FAST               '_seisinfo'

 L. 782      1816  LOAD_GLOBAL              print
             1818  LOAD_STR                 'TrainMl15DDcnnFromExisting: Step 1 - Step 1 - Get training samples:'
             1820  CALL_FUNCTION_1       1  '1 positional argument'
             1822  POP_TOP          

 L. 783      1824  LOAD_DEREF               'self'
             1826  LOAD_ATTR                traindataconfig
             1828  LOAD_STR                 'TrainPointSet'
             1830  BINARY_SUBSCR    
             1832  STORE_FAST               '_trainpoint'

 L. 784      1834  LOAD_GLOBAL              np
             1836  LOAD_METHOD              zeros
             1838  LOAD_CONST               0
             1840  LOAD_CONST               3
             1842  BUILD_LIST_2          2 
             1844  CALL_METHOD_1         1  '1 positional argument'
             1846  STORE_FAST               '_traindata'

 L. 785      1848  SETUP_LOOP         1924  'to 1924'
             1850  LOAD_FAST                '_trainpoint'
             1852  GET_ITER         
           1854_0  COME_FROM          1872  '1872'
             1854  FOR_ITER           1922  'to 1922'
             1856  STORE_FAST               '_p'

 L. 786      1858  LOAD_GLOBAL              point_ays
             1860  LOAD_METHOD              checkPoint
             1862  LOAD_DEREF               'self'
             1864  LOAD_ATTR                pointsetdata
             1866  LOAD_FAST                '_p'
             1868  BINARY_SUBSCR    
             1870  CALL_METHOD_1         1  '1 positional argument'
         1872_1874  POP_JUMP_IF_FALSE  1854  'to 1854'

 L. 787      1876  LOAD_GLOBAL              basic_mdt
             1878  LOAD_METHOD              exportMatDict
             1880  LOAD_DEREF               'self'
             1882  LOAD_ATTR                pointsetdata
             1884  LOAD_FAST                '_p'
             1886  BINARY_SUBSCR    
             1888  LOAD_STR                 'Inline'
             1890  LOAD_STR                 'Crossline'
             1892  LOAD_STR                 'Z'
             1894  BUILD_LIST_3          3 
             1896  CALL_METHOD_2         2  '2 positional arguments'
             1898  STORE_FAST               '_pt'

 L. 788      1900  LOAD_GLOBAL              np
             1902  LOAD_ATTR                concatenate
             1904  LOAD_FAST                '_traindata'
             1906  LOAD_FAST                '_pt'
             1908  BUILD_TUPLE_2         2 
             1910  LOAD_CONST               0
             1912  LOAD_CONST               ('axis',)
             1914  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1916  STORE_FAST               '_traindata'
         1918_1920  JUMP_BACK          1854  'to 1854'
             1922  POP_BLOCK        
           1924_0  COME_FROM_LOOP     1848  '1848'

 L. 789      1924  LOAD_GLOBAL              seis_ays
             1926  LOAD_ATTR                removeOutofSurveySample
             1928  LOAD_FAST                '_traindata'

 L. 790      1930  LOAD_FAST                '_seisinfo'
             1932  LOAD_STR                 'ILStart'
             1934  BINARY_SUBSCR    
             1936  LOAD_FAST                '_wdinl'
             1938  LOAD_FAST                '_seisinfo'
             1940  LOAD_STR                 'ILStep'
             1942  BINARY_SUBSCR    
             1944  BINARY_MULTIPLY  
             1946  BINARY_ADD       

 L. 791      1948  LOAD_FAST                '_seisinfo'
             1950  LOAD_STR                 'ILEnd'
             1952  BINARY_SUBSCR    
             1954  LOAD_FAST                '_wdinl'
             1956  LOAD_FAST                '_seisinfo'
             1958  LOAD_STR                 'ILStep'
             1960  BINARY_SUBSCR    
             1962  BINARY_MULTIPLY  
             1964  BINARY_SUBTRACT  

 L. 792      1966  LOAD_FAST                '_seisinfo'
             1968  LOAD_STR                 'XLStart'
             1970  BINARY_SUBSCR    
             1972  LOAD_FAST                '_wdxl'
             1974  LOAD_FAST                '_seisinfo'
             1976  LOAD_STR                 'XLStep'
             1978  BINARY_SUBSCR    
             1980  BINARY_MULTIPLY  
             1982  BINARY_ADD       

 L. 793      1984  LOAD_FAST                '_seisinfo'
             1986  LOAD_STR                 'XLEnd'
             1988  BINARY_SUBSCR    
             1990  LOAD_FAST                '_wdxl'
             1992  LOAD_FAST                '_seisinfo'
             1994  LOAD_STR                 'XLStep'
             1996  BINARY_SUBSCR    
             1998  BINARY_MULTIPLY  
             2000  BINARY_SUBTRACT  

 L. 794      2002  LOAD_FAST                '_seisinfo'
             2004  LOAD_STR                 'ZStart'
             2006  BINARY_SUBSCR    
             2008  LOAD_FAST                '_wdz'
             2010  LOAD_FAST                '_seisinfo'
             2012  LOAD_STR                 'ZStep'
             2014  BINARY_SUBSCR    
             2016  BINARY_MULTIPLY  
             2018  BINARY_ADD       

 L. 795      2020  LOAD_FAST                '_seisinfo'
             2022  LOAD_STR                 'ZEnd'
             2024  BINARY_SUBSCR    
             2026  LOAD_FAST                '_wdz'
             2028  LOAD_FAST                '_seisinfo'
             2030  LOAD_STR                 'ZStep'
             2032  BINARY_SUBSCR    
             2034  BINARY_MULTIPLY  
             2036  BINARY_SUBTRACT  
             2038  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             2040  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2042  STORE_FAST               '_traindata'

 L. 798      2044  LOAD_GLOBAL              np
             2046  LOAD_METHOD              shape
             2048  LOAD_FAST                '_traindata'
             2050  CALL_METHOD_1         1  '1 positional argument'
             2052  LOAD_CONST               0
             2054  BINARY_SUBSCR    
             2056  LOAD_CONST               0
             2058  COMPARE_OP               <=
         2060_2062  POP_JUMP_IF_FALSE  2100  'to 2100'

 L. 799      2064  LOAD_GLOBAL              vis_msg
             2066  LOAD_ATTR                print
             2068  LOAD_STR                 'ERROR in TrainMl15DDcnnFromExisting: No training sample found'
             2070  LOAD_STR                 'error'
             2072  LOAD_CONST               ('type',)
             2074  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2076  POP_TOP          

 L. 800      2078  LOAD_GLOBAL              QtWidgets
             2080  LOAD_ATTR                QMessageBox
             2082  LOAD_METHOD              critical
             2084  LOAD_DEREF               'self'
             2086  LOAD_ATTR                msgbox

 L. 801      2088  LOAD_STR                 'Train 1.5D-DCNN'

 L. 802      2090  LOAD_STR                 'No training sample found'
             2092  CALL_METHOD_3         3  '3 positional arguments'
             2094  POP_TOP          

 L. 803      2096  LOAD_CONST               None
             2098  RETURN_VALUE     
           2100_0  COME_FROM          2060  '2060'

 L. 806      2100  LOAD_GLOBAL              print
             2102  LOAD_STR                 'TrainMl15DDcnnFromExisting: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 807      2104  LOAD_FAST                '_image_height'
             2106  LOAD_FAST                '_image_width'
             2108  LOAD_FAST                '_image_height_new'
             2110  LOAD_FAST                '_image_width_new'
             2112  BUILD_TUPLE_4         4 
             2114  BINARY_MODULO    
             2116  CALL_FUNCTION_1       1  '1 positional argument'
             2118  POP_TOP          

 L. 808      2120  BUILD_MAP_0           0 
             2122  STORE_FAST               '_traindict'

 L. 809      2124  SETUP_LOOP         2196  'to 2196'
             2126  LOAD_FAST                '_features'
             2128  GET_ITER         
             2130  FOR_ITER           2194  'to 2194'
             2132  STORE_FAST               'f'

 L. 810      2134  LOAD_DEREF               'self'
             2136  LOAD_ATTR                seisdata
             2138  LOAD_FAST                'f'
             2140  BINARY_SUBSCR    
             2142  STORE_FAST               '_seisdata'

 L. 811      2144  LOAD_GLOBAL              seis_ays
             2146  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2148  LOAD_FAST                '_seisdata'
             2150  LOAD_FAST                '_traindata'
             2152  LOAD_DEREF               'self'
             2154  LOAD_ATTR                survinfo

 L. 812      2156  LOAD_FAST                '_wdinl'
             2158  LOAD_FAST                '_wdxl'
             2160  LOAD_FAST                '_wdz'

 L. 813      2162  LOAD_CONST               False
             2164  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2166  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2168  LOAD_CONST               None
             2170  LOAD_CONST               None
             2172  BUILD_SLICE_2         2 
             2174  LOAD_CONST               3
             2176  LOAD_CONST               None
             2178  BUILD_SLICE_2         2 
             2180  BUILD_TUPLE_2         2 
             2182  BINARY_SUBSCR    
             2184  LOAD_FAST                '_traindict'
             2186  LOAD_FAST                'f'
             2188  STORE_SUBSCR     
         2190_2192  JUMP_BACK          2130  'to 2130'
             2194  POP_BLOCK        
           2196_0  COME_FROM_LOOP     2124  '2124'

 L. 814      2196  LOAD_FAST                '_target'
             2198  LOAD_FAST                '_features'
             2200  COMPARE_OP               not-in
         2202_2204  POP_JUMP_IF_FALSE  2262  'to 2262'

 L. 815      2206  LOAD_DEREF               'self'
             2208  LOAD_ATTR                seisdata
             2210  LOAD_FAST                '_target'
             2212  BINARY_SUBSCR    
             2214  STORE_FAST               '_seisdata'

 L. 816      2216  LOAD_GLOBAL              seis_ays
             2218  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2220  LOAD_FAST                '_seisdata'
             2222  LOAD_FAST                '_traindata'
             2224  LOAD_DEREF               'self'
             2226  LOAD_ATTR                survinfo

 L. 817      2228  LOAD_FAST                '_wdinltarget'

 L. 818      2230  LOAD_FAST                '_wdxltarget'

 L. 819      2232  LOAD_FAST                '_wdztarget'

 L. 820      2234  LOAD_CONST               False
             2236  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2238  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2240  LOAD_CONST               None
             2242  LOAD_CONST               None
             2244  BUILD_SLICE_2         2 
             2246  LOAD_CONST               3
             2248  LOAD_CONST               None
             2250  BUILD_SLICE_2         2 
             2252  BUILD_TUPLE_2         2 
             2254  BINARY_SUBSCR    
             2256  LOAD_FAST                '_traindict'
             2258  LOAD_FAST                '_target'
             2260  STORE_SUBSCR     
           2262_0  COME_FROM          2202  '2202'

 L. 822      2262  LOAD_DEREF               'self'
             2264  LOAD_ATTR                traindataconfig
             2266  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2268  BINARY_SUBSCR    
         2270_2272  POP_JUMP_IF_FALSE  2348  'to 2348'

 L. 823      2274  SETUP_LOOP         2348  'to 2348'
             2276  LOAD_FAST                '_features'
             2278  GET_ITER         
           2280_0  COME_FROM          2308  '2308'
             2280  FOR_ITER           2346  'to 2346'
             2282  STORE_FAST               'f'

 L. 824      2284  LOAD_GLOBAL              ml_aug
             2286  LOAD_METHOD              removeInvariantFeature
             2288  LOAD_FAST                '_traindict'
             2290  LOAD_FAST                'f'
             2292  CALL_METHOD_2         2  '2 positional arguments'
             2294  STORE_FAST               '_traindict'

 L. 825      2296  LOAD_GLOBAL              basic_mdt
             2298  LOAD_METHOD              maxDictConstantRow
             2300  LOAD_FAST                '_traindict'
             2302  CALL_METHOD_1         1  '1 positional argument'
             2304  LOAD_CONST               0
             2306  COMPARE_OP               <=
         2308_2310  POP_JUMP_IF_FALSE  2280  'to 2280'

 L. 826      2312  LOAD_GLOBAL              print
             2314  LOAD_STR                 'TrainMl15DDcnnFromExisting: No training sample found'
             2316  CALL_FUNCTION_1       1  '1 positional argument'
             2318  POP_TOP          

 L. 827      2320  LOAD_GLOBAL              QtWidgets
             2322  LOAD_ATTR                QMessageBox
             2324  LOAD_METHOD              critical
             2326  LOAD_DEREF               'self'
             2328  LOAD_ATTR                msgbox

 L. 828      2330  LOAD_STR                 'Train 1.5D-DCNN'

 L. 829      2332  LOAD_STR                 'No training sample found'
             2334  CALL_METHOD_3         3  '3 positional arguments'
             2336  POP_TOP          

 L. 830      2338  LOAD_CONST               None
             2340  RETURN_VALUE     
         2342_2344  JUMP_BACK          2280  'to 2280'
             2346  POP_BLOCK        
           2348_0  COME_FROM_LOOP     2274  '2274'
           2348_1  COME_FROM          2270  '2270'

 L. 831      2348  LOAD_FAST                '_image_height_new'
             2350  LOAD_FAST                '_image_height'
             2352  COMPARE_OP               !=
         2354_2356  POP_JUMP_IF_TRUE   2368  'to 2368'
             2358  LOAD_FAST                '_image_width_new'
             2360  LOAD_FAST                '_image_width'
             2362  COMPARE_OP               !=
         2364_2366  POP_JUMP_IF_FALSE  2412  'to 2412'
           2368_0  COME_FROM          2354  '2354'

 L. 832      2368  SETUP_LOOP         2412  'to 2412'
             2370  LOAD_FAST                '_features'
             2372  GET_ITER         
             2374  FOR_ITER           2410  'to 2410'
             2376  STORE_FAST               'f'

 L. 833      2378  LOAD_GLOBAL              basic_image
             2380  LOAD_ATTR                changeImageSize
             2382  LOAD_FAST                '_traindict'
             2384  LOAD_FAST                'f'
             2386  BINARY_SUBSCR    

 L. 834      2388  LOAD_FAST                '_image_height'

 L. 835      2390  LOAD_FAST                '_image_width'

 L. 836      2392  LOAD_FAST                '_image_height_new'

 L. 837      2394  LOAD_FAST                '_image_width_new'
             2396  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2398  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2400  LOAD_FAST                '_traindict'
             2402  LOAD_FAST                'f'
             2404  STORE_SUBSCR     
         2406_2408  JUMP_BACK          2374  'to 2374'
             2410  POP_BLOCK        
           2412_0  COME_FROM_LOOP     2368  '2368'
           2412_1  COME_FROM          2364  '2364'

 L. 838      2412  LOAD_FAST                '_image_height_new'
             2414  LOAD_FAST                '_image_height'
             2416  COMPARE_OP               !=
         2418_2420  POP_JUMP_IF_FALSE  2458  'to 2458'
             2422  LOAD_FAST                '_target'
             2424  LOAD_FAST                '_features'
             2426  COMPARE_OP               not-in
         2428_2430  POP_JUMP_IF_FALSE  2458  'to 2458'

 L. 839      2432  LOAD_GLOBAL              basic_curve
             2434  LOAD_ATTR                changeCurveSize
             2436  LOAD_FAST                '_traindict'
             2438  LOAD_FAST                '_target'
             2440  BINARY_SUBSCR    

 L. 840      2442  LOAD_FAST                '_image_height'

 L. 841      2444  LOAD_FAST                '_image_height_new'
             2446  LOAD_STR                 'linear'
             2448  LOAD_CONST               ('length', 'length_new', 'kind')
             2450  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2452  LOAD_FAST                '_traindict'
             2454  LOAD_FAST                '_target'
             2456  STORE_SUBSCR     
           2458_0  COME_FROM          2428  '2428'
           2458_1  COME_FROM          2418  '2418'

 L. 842      2458  LOAD_DEREF               'self'
             2460  LOAD_ATTR                traindataconfig
             2462  LOAD_STR                 'RotateFeature_Checked'
             2464  BINARY_SUBSCR    
             2466  LOAD_CONST               True
             2468  COMPARE_OP               is
         2470_2472  POP_JUMP_IF_FALSE  2544  'to 2544'

 L. 843      2474  SETUP_LOOP         2512  'to 2512'
             2476  LOAD_FAST                '_features'
             2478  GET_ITER         
             2480  FOR_ITER           2510  'to 2510'
             2482  STORE_FAST               'f'

 L. 844      2484  LOAD_GLOBAL              ml_aug
             2486  LOAD_METHOD              rotateImage4Way
             2488  LOAD_FAST                '_traindict'
             2490  LOAD_FAST                'f'
             2492  BINARY_SUBSCR    
             2494  LOAD_FAST                '_image_height_new'
             2496  LOAD_FAST                '_image_width_new'
             2498  CALL_METHOD_3         3  '3 positional arguments'
             2500  LOAD_FAST                '_traindict'
             2502  LOAD_FAST                'f'
             2504  STORE_SUBSCR     
         2506_2508  JUMP_BACK          2480  'to 2480'
             2510  POP_BLOCK        
           2512_0  COME_FROM_LOOP     2474  '2474'

 L. 845      2512  LOAD_FAST                '_target'
             2514  LOAD_FAST                '_features'
             2516  COMPARE_OP               not-in
         2518_2520  POP_JUMP_IF_FALSE  2544  'to 2544'

 L. 846      2522  LOAD_GLOBAL              ml_aug
             2524  LOAD_METHOD              rotateImage4Way
             2526  LOAD_FAST                '_traindict'
             2528  LOAD_FAST                '_target'
             2530  BINARY_SUBSCR    
             2532  LOAD_FAST                '_image_height_new'
             2534  LOAD_CONST               1
             2536  CALL_METHOD_3         3  '3 positional arguments'
             2538  LOAD_FAST                '_traindict'
             2540  LOAD_FAST                '_target'
             2542  STORE_SUBSCR     
           2544_0  COME_FROM          2518  '2518'
           2544_1  COME_FROM          2470  '2470'

 L. 848      2544  LOAD_GLOBAL              np
             2546  LOAD_METHOD              round
             2548  LOAD_FAST                '_traindict'
             2550  LOAD_FAST                '_target'
             2552  BINARY_SUBSCR    
             2554  CALL_METHOD_1         1  '1 positional argument'
             2556  LOAD_METHOD              astype
             2558  LOAD_GLOBAL              int
             2560  CALL_METHOD_1         1  '1 positional argument'
             2562  LOAD_FAST                '_traindict'
             2564  LOAD_FAST                '_target'
             2566  STORE_SUBSCR     

 L. 851      2568  LOAD_GLOBAL              print
             2570  LOAD_STR                 'TrainMl15DDcnnFromExisting: A total of %d valid training samples'
             2572  LOAD_GLOBAL              basic_mdt
             2574  LOAD_METHOD              maxDictConstantRow

 L. 852      2576  LOAD_FAST                '_traindict'
             2578  CALL_METHOD_1         1  '1 positional argument'
             2580  BINARY_MODULO    
             2582  CALL_FUNCTION_1       1  '1 positional argument'
             2584  POP_TOP          

 L. 854      2586  LOAD_GLOBAL              print
             2588  LOAD_STR                 'TrainMl15DDcnnFromExisting: Step 3 - Start training'
             2590  CALL_FUNCTION_1       1  '1 positional argument'
             2592  POP_TOP          

 L. 856      2594  LOAD_GLOBAL              QtWidgets
             2596  LOAD_METHOD              QProgressDialog
             2598  CALL_METHOD_0         0  '0 positional arguments'
             2600  STORE_FAST               '_pgsdlg'

 L. 857      2602  LOAD_GLOBAL              QtGui
             2604  LOAD_METHOD              QIcon
             2606  CALL_METHOD_0         0  '0 positional arguments'
             2608  STORE_FAST               'icon'

 L. 858      2610  LOAD_FAST                'icon'
             2612  LOAD_METHOD              addPixmap
             2614  LOAD_GLOBAL              QtGui
             2616  LOAD_METHOD              QPixmap
             2618  LOAD_GLOBAL              os
             2620  LOAD_ATTR                path
             2622  LOAD_METHOD              join
             2624  LOAD_DEREF               'self'
             2626  LOAD_ATTR                iconpath
             2628  LOAD_STR                 'icons/new.png'
             2630  CALL_METHOD_2         2  '2 positional arguments'
             2632  CALL_METHOD_1         1  '1 positional argument'

 L. 859      2634  LOAD_GLOBAL              QtGui
             2636  LOAD_ATTR                QIcon
             2638  LOAD_ATTR                Normal
             2640  LOAD_GLOBAL              QtGui
             2642  LOAD_ATTR                QIcon
             2644  LOAD_ATTR                Off
             2646  CALL_METHOD_3         3  '3 positional arguments'
             2648  POP_TOP          

 L. 860      2650  LOAD_FAST                '_pgsdlg'
             2652  LOAD_METHOD              setWindowIcon
             2654  LOAD_FAST                'icon'
             2656  CALL_METHOD_1         1  '1 positional argument'
             2658  POP_TOP          

 L. 861      2660  LOAD_FAST                '_pgsdlg'
             2662  LOAD_METHOD              setWindowTitle
             2664  LOAD_STR                 'Train 1.5D-DCNN'
             2666  CALL_METHOD_1         1  '1 positional argument'
             2668  POP_TOP          

 L. 862      2670  LOAD_FAST                '_pgsdlg'
             2672  LOAD_METHOD              setCancelButton
             2674  LOAD_CONST               None
             2676  CALL_METHOD_1         1  '1 positional argument'
             2678  POP_TOP          

 L. 863      2680  LOAD_FAST                '_pgsdlg'
             2682  LOAD_METHOD              setWindowFlags
             2684  LOAD_GLOBAL              QtCore
             2686  LOAD_ATTR                Qt
             2688  LOAD_ATTR                WindowStaysOnTopHint
             2690  CALL_METHOD_1         1  '1 positional argument'
             2692  POP_TOP          

 L. 864      2694  LOAD_FAST                '_pgsdlg'
             2696  LOAD_METHOD              forceShow
             2698  CALL_METHOD_0         0  '0 positional arguments'
             2700  POP_TOP          

 L. 865      2702  LOAD_FAST                '_pgsdlg'
             2704  LOAD_METHOD              setFixedWidth
             2706  LOAD_CONST               400
             2708  CALL_METHOD_1         1  '1 positional argument'
             2710  POP_TOP          

 L. 866      2712  LOAD_GLOBAL              ml_dcnn15d
             2714  LOAD_ATTR                create15DDCNNSegmentorFromExisting
             2716  LOAD_FAST                '_traindict'

 L. 867      2718  LOAD_FAST                '_image_height_new'

 L. 868      2720  LOAD_FAST                '_image_width_new'

 L. 869      2722  LOAD_FAST                '_features'
             2724  LOAD_FAST                '_target'

 L. 870      2726  LOAD_FAST                '_nepoch'
             2728  LOAD_FAST                '_batchsize'

 L. 871      2730  LOAD_FAST                '_nconvblock'
             2732  LOAD_FAST                '_nconvfeature'

 L. 872      2734  LOAD_FAST                '_nconvlayer'

 L. 873      2736  LOAD_FAST                '_n1x1layer'
             2738  LOAD_FAST                '_n1x1feature'

 L. 874      2740  LOAD_FAST                '_pool_height'
             2742  LOAD_FAST                '_pool_width'

 L. 875      2744  LOAD_FAST                '_learning_rate'

 L. 876      2746  LOAD_FAST                '_dropout_prob'

 L. 877      2748  LOAD_CONST               True

 L. 878      2750  LOAD_FAST                '_savepath'
             2752  LOAD_FAST                '_savename'

 L. 879      2754  LOAD_FAST                '_pgsdlg'

 L. 880      2756  LOAD_FAST                '_precnnpath'

 L. 881      2758  LOAD_FAST                '_precnnname'

 L. 882      2760  LOAD_FAST                '_blockidx'
             2762  LOAD_FAST                '_layeridx'

 L. 883      2764  LOAD_FAST                '_trainable'
             2766  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'nepoch', 'batchsize', 'nconvblock', 'nconvfeature', 'nconvlayer', 'n1x1layer', 'n1x1feature', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprob', 'save2disk', 'savepath', 'savename', 'qpgsdlg', 'precnnpath', 'precnnname', 'blockidx', 'layeridx', 'trainable')
             2768  CALL_FUNCTION_KW_25    25  '25 total positional and keyword args'
             2770  STORE_FAST               '_dcnnlog'

 L. 886      2772  LOAD_GLOBAL              QtWidgets
             2774  LOAD_ATTR                QMessageBox
             2776  LOAD_METHOD              information
             2778  LOAD_DEREF               'self'
             2780  LOAD_ATTR                msgbox

 L. 887      2782  LOAD_STR                 'Train 1.5D-DCNN'

 L. 888      2784  LOAD_STR                 'DCNN trained successfully'
             2786  CALL_METHOD_3         3  '3 positional arguments'
             2788  POP_TOP          

 L. 890      2790  LOAD_GLOBAL              QtWidgets
             2792  LOAD_ATTR                QMessageBox
             2794  LOAD_METHOD              question
             2796  LOAD_DEREF               'self'
             2798  LOAD_ATTR                msgbox
             2800  LOAD_STR                 'Train 1.5D-DCNN'
             2802  LOAD_STR                 'View learning matrix?'

 L. 891      2804  LOAD_GLOBAL              QtWidgets
             2806  LOAD_ATTR                QMessageBox
             2808  LOAD_ATTR                Yes
             2810  LOAD_GLOBAL              QtWidgets
             2812  LOAD_ATTR                QMessageBox
             2814  LOAD_ATTR                No
             2816  BINARY_OR        

 L. 892      2818  LOAD_GLOBAL              QtWidgets
             2820  LOAD_ATTR                QMessageBox
             2822  LOAD_ATTR                Yes
             2824  CALL_METHOD_5         5  '5 positional arguments'
             2826  STORE_FAST               'reply'

 L. 894      2828  LOAD_FAST                'reply'
             2830  LOAD_GLOBAL              QtWidgets
             2832  LOAD_ATTR                QMessageBox
             2834  LOAD_ATTR                Yes
             2836  COMPARE_OP               ==
         2838_2840  POP_JUMP_IF_FALSE  2908  'to 2908'

 L. 895      2842  LOAD_GLOBAL              QtWidgets
             2844  LOAD_METHOD              QDialog
             2846  CALL_METHOD_0         0  '0 positional arguments'
             2848  STORE_FAST               '_viewmllearnmat'

 L. 896      2850  LOAD_GLOBAL              gui_viewmllearnmat
             2852  CALL_FUNCTION_0       0  '0 positional arguments'
             2854  STORE_FAST               '_gui'

 L. 897      2856  LOAD_DEREF               'self'
             2858  LOAD_ATTR                linestyle
             2860  LOAD_FAST                '_gui'
             2862  STORE_ATTR               linestyle

 L. 898      2864  LOAD_DEREF               'self'
             2866  LOAD_ATTR                fontstyle
             2868  LOAD_FAST                '_gui'
             2870  STORE_ATTR               fontstyle

 L. 899      2872  LOAD_FAST                '_dcnnlog'
             2874  LOAD_STR                 'learning_curve'
             2876  BINARY_SUBSCR    
             2878  LOAD_FAST                '_gui'
             2880  STORE_ATTR               learnmat

 L. 900      2882  LOAD_FAST                '_gui'
             2884  LOAD_METHOD              setupGUI
             2886  LOAD_FAST                '_viewmllearnmat'
             2888  CALL_METHOD_1         1  '1 positional argument'
             2890  POP_TOP          

 L. 901      2892  LOAD_FAST                '_viewmllearnmat'
             2894  LOAD_METHOD              exec
             2896  CALL_METHOD_0         0  '0 positional arguments'
             2898  POP_TOP          

 L. 902      2900  LOAD_FAST                '_viewmllearnmat'
             2902  LOAD_METHOD              show
             2904  CALL_METHOD_0         0  '0 positional arguments'
             2906  POP_TOP          
           2908_0  COME_FROM          2838  '2838'

Parse error at or near `POP_TOP' instruction at offset 2906

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
    TrainMl15DDcnnFromExisting = QtWidgets.QWidget()
    gui = trainml15ddcnnfromexisting()
    gui.setupGUI(TrainMl15DDcnnFromExisting)
    TrainMl15DDcnnFromExisting.show()
    sys.exit(app.exec_())