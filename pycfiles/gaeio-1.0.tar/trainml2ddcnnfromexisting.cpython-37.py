# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\trainml2ddcnnfromexisting.py
# Compiled at: 2020-01-05 11:47:48
# Size of source mod 2**32: 54362 bytes
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
import cognitivegeo.src.ml.dcnnsegmentor as ml_dcnn
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.configmltraindata as gui_configmltraindata
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class trainml2ddcnnfromexisting(object):
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

    def setupGUI(self, TrainMl2DDcnnFromExisting):
        TrainMl2DDcnnFromExisting.setObjectName('TrainMl2DDcnnFromExisting')
        TrainMl2DDcnnFromExisting.setFixedSize(800, 630)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        TrainMl2DDcnnFromExisting.setWindowIcon(icon)
        self.lblfeature = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(TrainMl2DDcnnFromExisting)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 10, 280, 110))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lblornt = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblornt.setObjectName('lblornt')
        self.lblornt.setGeometry(QtCore.QRect(30, 130, 80, 30))
        self.cbbornt = QtWidgets.QComboBox(TrainMl2DDcnnFromExisting)
        self.cbbornt.setObjectName('cbbornt')
        self.cbbornt.setGeometry(QtCore.QRect(110, 130, 280, 30))
        self.lbloldsize = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lbloldsize.setObjectName('lbloldsize')
        self.lbloldsize.setGeometry(QtCore.QRect(10, 170, 80, 60))
        self.lbloldheight = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lbloldheight.setObjectName('lbloldheight')
        self.lbloldheight.setGeometry(QtCore.QRect(100, 170, 50, 30))
        self.ldtoldheight = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtoldheight.setObjectName('ldtoldheight')
        self.ldtoldheight.setGeometry(QtCore.QRect(150, 170, 40, 30))
        self.lbloldwidth = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lbloldwidth.setObjectName('lbloldwidth')
        self.lbloldwidth.setGeometry(QtCore.QRect(100, 210, 50, 30))
        self.ldtoldwidth = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtoldwidth.setObjectName('ldtoldwidth')
        self.ldtoldwidth.setGeometry(QtCore.QRect(150, 210, 40, 30))
        self.lblnewsize = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblnewsize.setObjectName('lblnewsize')
        self.lblnewsize.setGeometry(QtCore.QRect(210, 170, 80, 60))
        self.lblnewheight = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblnewheight.setObjectName('lblnewheight')
        self.lblnewheight.setGeometry(QtCore.QRect(300, 170, 50, 30))
        self.ldtnewheight = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtnewheight.setObjectName('ldtnewheight')
        self.ldtnewheight.setGeometry(QtCore.QRect(350, 170, 40, 30))
        self.lblnewwidth = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblnewwidth.setObjectName('lblnewwidth')
        self.lblnewwidth.setGeometry(QtCore.QRect(300, 210, 50, 30))
        self.ldtnewwidth = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtnewwidth.setObjectName('ldtnewwidth')
        self.ldtnewwidth.setGeometry(QtCore.QRect(350, 210, 40, 30))
        self.lbltarget = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 260, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(TrainMl2DDcnnFromExisting)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 260, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 10, 190, 30))
        self.lblexisting = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblexisting.setObjectName('lblexisting')
        self.lblexisting.setGeometry(QtCore.QRect(410, 50, 100, 30))
        self.ldtexisting = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtexisting.setObjectName('ldtexisting')
        self.ldtexisting.setGeometry(QtCore.QRect(510, 50, 210, 30))
        self.btnexisting = QtWidgets.QPushButton(TrainMl2DDcnnFromExisting)
        self.btnexisting.setObjectName('btnexisting')
        self.btnexisting.setGeometry(QtCore.QRect(730, 50, 60, 30))
        self.lblnconvblockexisting = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblnconvblockexisting.setObjectName('lblnconvblockexisting')
        self.lblnconvblockexisting.setGeometry(QtCore.QRect(410, 90, 130, 30))
        self.ldtnconvblockexisting = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtnconvblockexisting.setObjectName('ldtnconvblockexisting')
        self.ldtnconvblockexisting.setGeometry(QtCore.QRect(550, 90, 40, 30))
        self.twgnconvblockexisting = QtWidgets.QTableWidget(TrainMl2DDcnnFromExisting)
        self.twgnconvblockexisting.setObjectName('twgnconvblockexisting')
        self.twgnconvblockexisting.setGeometry(QtCore.QRect(610, 90, 180, 150))
        self.twgnconvblockexisting.setColumnCount(3)
        self.twgnconvblockexisting.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnconvblockexisting.verticalHeader().hide()
        self.lblblockid = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblblockid.setObjectName('lblblockid')
        self.lblblockid.setGeometry(QtCore.QRect(410, 130, 130, 30))
        self.cbbblockid = QtWidgets.QComboBox(TrainMl2DDcnnFromExisting)
        self.cbbblockid.setObjectName('cbbblockid')
        self.cbbblockid.setGeometry(QtCore.QRect(550, 130, 40, 30))
        self.lbllayerid = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lbllayerid.setObjectName('lbllayerid')
        self.lbllayerid.setGeometry(QtCore.QRect(410, 170, 130, 30))
        self.cbblayerid = QtWidgets.QComboBox(TrainMl2DDcnnFromExisting)
        self.cbblayerid.setObjectName('cbblayerid')
        self.cbblayerid.setGeometry(QtCore.QRect(550, 170, 40, 30))
        self.lbltrainable = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lbltrainable.setObjectName('lbltrainable')
        self.lbltrainable.setGeometry(QtCore.QRect(410, 210, 130, 30))
        self.cbbtrainable = QtWidgets.QComboBox(TrainMl2DDcnnFromExisting)
        self.cbbtrainable.setObjectName('cbbtrainable')
        self.cbbtrainable.setGeometry(QtCore.QRect(550, 210, 40, 30))
        self.lblappend = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblappend.setObjectName('lblappend')
        self.lblappend.setGeometry(QtCore.QRect(410, 250, 200, 30))
        self.lblnconvblock = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblnconvblock.setObjectName('lblnconvblock')
        self.lblnconvblock.setGeometry(QtCore.QRect(410, 290, 130, 30))
        self.ldtnconvblock = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtnconvblock.setObjectName('ldtnconvblock')
        self.ldtnconvblock.setGeometry(QtCore.QRect(550, 290, 40, 30))
        self.twgnconvblock = QtWidgets.QTableWidget(TrainMl2DDcnnFromExisting)
        self.twgnconvblock.setObjectName('twgnconvblock')
        self.twgnconvblock.setGeometry(QtCore.QRect(410, 330, 180, 200))
        self.twgnconvblock.setColumnCount(3)
        self.twgnconvblock.verticalHeader().hide()
        self.lbln1x1layer = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lbln1x1layer.setObjectName('lbln1x1layer')
        self.lbln1x1layer.setGeometry(QtCore.QRect(610, 290, 130, 30))
        self.ldtn1x1layer = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtn1x1layer.setObjectName('ldtn1x1layer')
        self.ldtn1x1layer.setGeometry(QtCore.QRect(750, 290, 40, 30))
        self.twgn1x1layer = QtWidgets.QTableWidget(TrainMl2DDcnnFromExisting)
        self.twgn1x1layer.setObjectName('twgn1x1layer')
        self.twgn1x1layer.setGeometry(QtCore.QRect(610, 330, 180, 200))
        self.twgn1x1layer.setColumnCount(2)
        self.twgn1x1layer.verticalHeader().hide()
        self.lblmasksize = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblmasksize.setObjectName('lblmasksize')
        self.lblmasksize.setGeometry(QtCore.QRect(410, 540, 80, 60))
        self.lblmaskheight = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblmaskheight.setObjectName('lblmaskheight')
        self.lblmaskheight.setGeometry(QtCore.QRect(500, 540, 50, 30))
        self.ldtmaskheight = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtmaskheight.setObjectName('ldtmaskheight')
        self.ldtmaskheight.setGeometry(QtCore.QRect(550, 540, 40, 30))
        self.lblmaskwidth = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblmaskwidth.setObjectName('lblmaskwidth')
        self.lblmaskwidth.setGeometry(QtCore.QRect(500, 580, 50, 30))
        self.ldtmaskwidth = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtmaskwidth.setObjectName('ldtmaskwidth')
        self.ldtmaskwidth.setGeometry(QtCore.QRect(550, 580, 40, 30))
        self.lblpoolsize = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblpoolsize.setObjectName('lblpoolsize')
        self.lblpoolsize.setGeometry(QtCore.QRect(610, 540, 80, 60))
        self.lblpoolheight = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblpoolheight.setObjectName('lblpoolheight')
        self.lblpoolheight.setGeometry(QtCore.QRect(700, 540, 50, 30))
        self.ldtpoolheight = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtpoolheight.setObjectName('ldtpoolheight')
        self.ldtpoolheight.setGeometry(QtCore.QRect(750, 540, 40, 30))
        self.lblpoolwidth = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblpoolwidth.setObjectName('lblpoolwidth')
        self.lblpoolwidth.setGeometry(QtCore.QRect(700, 580, 50, 30))
        self.ldtpoolwidth = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtpoolwidth.setObjectName('ldtpoolwidth')
        self.ldtpoolwidth.setGeometry(QtCore.QRect(750, 580, 40, 30))
        self.btnconfigtraindata = QtWidgets.QPushButton(TrainMl2DDcnnFromExisting)
        self.btnconfigtraindata.setObjectName('btnconfigtraindata')
        self.btnconfigtraindata.setGeometry(QtCore.QRect(230, 310, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigtraindata.setIcon(icon)
        self.lblpara = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(10, 310, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(10, 350, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(150, 350, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(210, 350, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(350, 350, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(10, 390, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(150, 390, 40, 30))
        self.lbldropout = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lbldropout.setObjectName('lbldropout')
        self.lbldropout.setGeometry(QtCore.QRect(210, 390, 130, 30))
        self.ldtdropout = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtdropout.setObjectName('ldtdropout')
        self.ldtdropout.setGeometry(QtCore.QRect(350, 390, 40, 30))
        self.lblsave = QtWidgets.QLabel(TrainMl2DDcnnFromExisting)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(10, 440, 120, 30))
        self.ldtsave = QtWidgets.QLineEdit(TrainMl2DDcnnFromExisting)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(140, 440, 180, 30))
        self.btnsave = QtWidgets.QPushButton(TrainMl2DDcnnFromExisting)
        self.btnsave.setObjectName('btnsave')
        self.btnsave.setGeometry(QtCore.QRect(330, 440, 60, 30))
        self.btnapply = QtWidgets.QPushButton(TrainMl2DDcnnFromExisting)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(120, 580, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(TrainMl2DDcnnFromExisting)
        self.msgbox.setObjectName('msgbox')
        _center_x = TrainMl2DDcnnFromExisting.geometry().center().x()
        _center_y = TrainMl2DDcnnFromExisting.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(TrainMl2DDcnnFromExisting)
        QtCore.QMetaObject.connectSlotsByName(TrainMl2DDcnnFromExisting)

    def retranslateGUI(self, TrainMl2DDcnnFromExisting):
        self.dialog = TrainMl2DDcnnFromExisting
        _translate = QtCore.QCoreApplication.translate
        TrainMl2DDcnnFromExisting.setWindowTitle(_translate('TrainMl2DDcnnFromExisting', 'Train 2D-DCNN from pre-trained'))
        self.lblfeature.setText(_translate('TrainMl2DDcnnFromExisting', 'Select features:'))
        self.lblornt.setText(_translate('TrainMl2DDcnnFromExisting', 'Orientation:'))
        self.cbbornt.addItems(['Inline (height = Time/depth & width = Crossline)',
         'Crossline (height = Time/depth & width = Inline)',
         'Time/depth (height = Crossline & width = Inline)'])
        self.cbbornt.setItemIcon(0, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(1, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visinl.png')))
        self.cbbornt.setItemIcon(2, QtGui.QIcon(os.path.join(self.iconpath, 'icons/visz.png')))
        self.lbltarget.setText(_translate('TrainMl2DDcnnFromExisting', 'Select target:'))
        self.btnconfigtraindata.setText(_translate('TrainMl2DDcnnFromScratch', 'Configure training data'))
        self.btnconfigtraindata.clicked.connect(self.clickBtnConfigTrainData)
        self.lbloldsize.setText(_translate('TrainMl2DDcnnFromExisting', 'Original\nimage\nsize:'))
        self.lbloldsize.setAlignment(QtCore.Qt.AlignRight)
        self.lbloldheight.setText(_translate('TrainMl2DDcnnFromExisting', 'height='))
        self.ldtoldheight.setText(_translate('TrainMl2DDcnnFromExisting', ''))
        self.ldtoldheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldwidth.setText(_translate('TrainMl2DDcnnFromExisting', 'width='))
        self.ldtoldwidth.setText(_translate('TrainMl2DDcnnFromExisting', ''))
        self.ldtoldwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewsize.setText(_translate('TrainMl2DDcnnFromExisting', 'Interpolated\nimage\nsize:'))
        self.lblnewsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblnewheight.setText(_translate('TrainMl2DDcnnFromExisting', 'height='))
        self.ldtnewheight.setText(_translate('TrainMl2DDcnnFromExisting', '32'))
        self.ldtnewheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewwidth.setText(_translate('TrainMl2DDcnnFromExisting', 'width='))
        self.ldtnewwidth.setText(_translate('TrainMl2DDcnnFromExisting', '32'))
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
                    item.setText(_translate('TrainMl2DDcnnFromExisting', i))
                    self.lwgfeature.addItem(item)
                    if _firstfeature is None:
                        _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            self.cbbtarget.addItems(self.featurelist)
        self.lblnetwork.setText(_translate('TrainMl2DDcnnFromExisting', 'Specify DCNN architecture:'))
        self.lblexisting.setText(_translate('TrainMl2DDcnnFromExisting', 'Select pre-trained:'))
        self.ldtexisting.setText(_translate('TrainMl2DDcnnFromExisting', ''))
        self.ldtexisting.textChanged.connect(self.changeLdtExisting)
        self.btnexisting.setText(_translate('TrainMl2DDcnnFromExisting', 'Browse'))
        self.btnexisting.clicked.connect(self.clickBtnExisting)
        self.lblnconvblockexisting.setText(_translate('TrainMl2DDcnnFromExisting', 'Available conv. blocks:'))
        self.lblnconvblockexisting.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblockexisting.setText(_translate('TrainMl2DDcnnFromExisting', ''))
        self.ldtnconvblockexisting.setEnabled(False)
        self.ldtnconvblockexisting.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnconvblockexisting.textChanged.connect(self.changeLdtNconvblockExisting)
        self.twgnconvblockexisting.setHorizontalHeaderLabels(['Block ID', 'No. of layers', 'No. of features'])
        self.lblblockid.setText(_translate('TrainMl2DDcnnFromExisting', 'Select conv. block ID:'))
        self.lblblockid.setAlignment(QtCore.Qt.AlignRight)
        self.cbbblockid.currentIndexChanged.connect(self.changeCbbBlockid)
        self.lbllayerid.setText(_translate('TrainMl2DDcnnFromExisting', 'Select conv. layer ID:'))
        self.lbllayerid.setAlignment(QtCore.Qt.AlignRight)
        self.lbltrainable.setText(_translate('TrainMl2DDcnnFromExisting', 'Is trainable?:'))
        self.lbltrainable.setAlignment(QtCore.Qt.AlignRight)
        self.cbbtrainable.addItems(['Yes', 'No'])
        self.lblappend.setText(_translate('TrainMl2DDcnnFromExisting', 'Append more blocks & layers:'))
        self.lblnconvblock.setText(_translate('TrainMl2DDcnnFromExisting', 'No. of conv. blocks:'))
        self.lblnconvblock.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnconvblock.setText(_translate('TrainMl2DDcnnFromExisting', '2'))
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

        self.lbln1x1layer.setText(_translate('TrainMl2DDcnnFromExisting', 'No. of 1x1 layers:'))
        self.lbln1x1layer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtn1x1layer.setText(_translate('TrainMl2DDcnnFromExisting', '2'))
        self.ldtn1x1layer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtn1x1layer.textChanged.connect(self.changeLdtN1x1layer)
        self.twgn1x1layer.setHorizontalHeaderLabels(['Layer ID', 'No. of features'])
        self.twgn1x1layer.setRowCount(2)
        for _idx in range(int(self.ldtn1x1layer.text())):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate('TrainMl2DDcnnFromExisting', str(_idx + 1)))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgn1x1layer.setItem(_idx, 0, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(1024))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.twgn1x1layer.setItem(_idx, 1, item)

        self.lblmasksize.setText(_translate('TrainMl2DDcnnFromExisting', 'Convolution\nmask\nsize:'))
        self.lblmasksize.setAlignment(QtCore.Qt.AlignRight)
        self.lblmaskheight.setText(_translate('TrainMl2DDcnnFromExisting', 'height='))
        self.ldtmaskheight.setText(_translate('TrainMl2DDcnnFromExisting', ''))
        self.ldtmaskheight.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskheight.setEnabled(False)
        self.lblmaskwidth.setText(_translate('TrainMl2DDcnnFromExisting', 'width='))
        self.ldtmaskwidth.setText(_translate('TrainMl2DDcnnFromExisting', ''))
        self.ldtmaskwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtmaskwidth.setEnabled(False)
        self.lblpoolsize.setText(_translate('TrainMl2DDcnnFromExisting', 'Maximum\npooling\nsize:'))
        self.lblpoolsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpoolheight.setText(_translate('TrainMl2DDcnnFromExisting', 'height='))
        self.ldtpoolheight.setText(_translate('TrainMl2DDcnnFromExisting', ''))
        self.ldtpoolheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpoolwidth.setText(_translate('TrainMl2DDcnnFromExisting', 'width='))
        self.ldtpoolwidth.setText(_translate('TrainMl2DDcnnFromExisting', ''))
        self.ldtpoolwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpara.setText(_translate('TrainMl2DDcnnFromExisting', 'Specify training parameters:'))
        self.lblnepoch.setText(_translate('TrainMl2DDcnnFromExisting', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('TrainMl2DDcnnFromExisting', '100'))
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('TrainMl2DDcnnFromExisting', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('TrainMl2DDcnnFromExisting', '50'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('TrainMl2DDcnnFromExisting', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('TrainMl2DDcnnFromExisting', '1e-4'))
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lbldropout.setText(_translate('TrainMl2DDcnnFromExisting', 'Dropout rate:'))
        self.lbldropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtdropout.setText(_translate('TrainMl2DDcnnFromExisting', '0.1'))
        self.ldtdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('TrainMl2DDcnnFromExisting', 'Save network to:'))
        self.ldtsave.setText(_translate('TrainMl2DDcnnFromExisting', ''))
        self.btnsave.setText(_translate('TrainMl2DDcnnFromExisting', 'Browse'))
        self.btnsave.clicked.connect(self.clickBtnSave)
        self.btnapply.setText(_translate('TrainMl2DDcnnFromExisting', 'Train 2D-DCNN'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnTrainMl2DDcnnFromExisting)

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

    def clickBtnTrainMl2DDcnnFromExisting--- This code section failed: ---

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
               30  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: No feature selected for training'
               32  LOAD_STR                 'error'
               34  LOAD_CONST               ('type',)
               36  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               38  POP_TOP          

 L. 601        40  LOAD_GLOBAL              QtWidgets
               42  LOAD_ATTR                QMessageBox
               44  LOAD_METHOD              critical
               46  LOAD_DEREF               'self'
               48  LOAD_ATTR                msgbox

 L. 602        50  LOAD_STR                 'Train 2D-DCNN'

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
              162  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Non-integer feature size'
              164  LOAD_STR                 'error'
              166  LOAD_CONST               ('type',)
              168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              170  POP_TOP          

 L. 613       172  LOAD_GLOBAL              QtWidgets
              174  LOAD_ATTR                QMessageBox
              176  LOAD_METHOD              critical
              178  LOAD_DEREF               'self'
              180  LOAD_ATTR                msgbox

 L. 614       182  LOAD_STR                 'Train 2D-DCNN'

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
              232  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Features are not 2D'
              234  LOAD_STR                 'error'
              236  LOAD_CONST               ('type',)
              238  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              240  POP_TOP          

 L. 620       242  LOAD_GLOBAL              QtWidgets
              244  LOAD_ATTR                QMessageBox
              246  LOAD_METHOD              critical
              248  LOAD_DEREF               'self'
              250  LOAD_ATTR                msgbox

 L. 621       252  LOAD_STR                 'Train 2D-DCNN'

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
              316  LOAD_STR                 'trainml2ddcnnfromexisting.clickBtnTrainMl2DDcnnFromExisting.<locals>.<listcomp>'
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

 L. 632       344  LOAD_FAST                '_target'
              346  LOAD_FAST                '_features'
              348  COMPARE_OP               in
          350_352  POP_JUMP_IF_FALSE   390  'to 390'

 L. 633       354  LOAD_GLOBAL              vis_msg
              356  LOAD_ATTR                print
              358  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Target also used as features'
              360  LOAD_STR                 'error'
              362  LOAD_CONST               ('type',)
              364  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              366  POP_TOP          

 L. 634       368  LOAD_GLOBAL              QtWidgets
              370  LOAD_ATTR                QMessageBox
              372  LOAD_METHOD              critical
              374  LOAD_DEREF               'self'
              376  LOAD_ATTR                msgbox

 L. 635       378  LOAD_STR                 'Train 2D-DCNN'

 L. 636       380  LOAD_STR                 'Target also used as features'
              382  CALL_METHOD_3         3  '3 positional arguments'
              384  POP_TOP          

 L. 637       386  LOAD_CONST               None
              388  RETURN_VALUE     
            390_0  COME_FROM           350  '350'

 L. 639       390  LOAD_GLOBAL              len
              392  LOAD_DEREF               'self'
              394  LOAD_ATTR                ldtexisting
              396  LOAD_METHOD              text
              398  CALL_METHOD_0         0  '0 positional arguments'
              400  CALL_FUNCTION_1       1  '1 positional argument'
              402  LOAD_CONST               1
              404  COMPARE_OP               <
          406_408  POP_JUMP_IF_FALSE   446  'to 446'

 L. 640       410  LOAD_GLOBAL              vis_msg
              412  LOAD_ATTR                print
              414  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: No name specified for pre-trained network'

 L. 641       416  LOAD_STR                 'error'
              418  LOAD_CONST               ('type',)
              420  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              422  POP_TOP          

 L. 642       424  LOAD_GLOBAL              QtWidgets
              426  LOAD_ATTR                QMessageBox
              428  LOAD_METHOD              critical
              430  LOAD_DEREF               'self'
              432  LOAD_ATTR                msgbox

 L. 643       434  LOAD_STR                 'Train 2D-DCNN'

 L. 644       436  LOAD_STR                 'No name specified for pre-trained network'
              438  CALL_METHOD_3         3  '3 positional arguments'
              440  POP_TOP          

 L. 645       442  LOAD_CONST               None
              444  RETURN_VALUE     
            446_0  COME_FROM           406  '406'

 L. 646       446  LOAD_GLOBAL              os
              448  LOAD_ATTR                path
              450  LOAD_METHOD              dirname
              452  LOAD_DEREF               'self'
              454  LOAD_ATTR                ldtexisting
              456  LOAD_METHOD              text
              458  CALL_METHOD_0         0  '0 positional arguments'
              460  CALL_METHOD_1         1  '1 positional argument'
              462  STORE_FAST               '_precnnpath'

 L. 647       464  LOAD_GLOBAL              os
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

 L. 648       494  LOAD_DEREF               'self'
              496  LOAD_ATTR                cbbblockid
              498  LOAD_METHOD              currentIndex
              500  CALL_METHOD_0         0  '0 positional arguments'
              502  STORE_FAST               '_blockidx'

 L. 649       504  LOAD_DEREF               'self'
              506  LOAD_ATTR                cbblayerid
              508  LOAD_METHOD              currentIndex
              510  CALL_METHOD_0         0  '0 positional arguments'
              512  STORE_FAST               '_layeridx'

 L. 650       514  LOAD_CONST               True
              516  STORE_FAST               '_trainable'

 L. 651       518  LOAD_DEREF               'self'
              520  LOAD_ATTR                cbbtrainable
              522  LOAD_METHOD              currentIndex
              524  CALL_METHOD_0         0  '0 positional arguments'
              526  LOAD_CONST               0
              528  COMPARE_OP               !=
          530_532  POP_JUMP_IF_FALSE   538  'to 538'

 L. 652       534  LOAD_CONST               False
              536  STORE_FAST               '_trainable'
            538_0  COME_FROM           530  '530'

 L. 654       538  LOAD_GLOBAL              ml_tfm
              540  LOAD_METHOD              getConvModelNChannel
              542  LOAD_FAST                '_precnnpath'
              544  LOAD_FAST                '_precnnname'
              546  CALL_METHOD_2         2  '2 positional arguments'
              548  LOAD_GLOBAL              len
              550  LOAD_FAST                '_features'
              552  CALL_FUNCTION_1       1  '1 positional argument'
              554  COMPARE_OP               !=
          556_558  POP_JUMP_IF_FALSE   596  'to 596'

 L. 655       560  LOAD_GLOBAL              vis_msg
              562  LOAD_ATTR                print
              564  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Feature channel number not match with pre-trained network'

 L. 656       566  LOAD_STR                 'error'
              568  LOAD_CONST               ('type',)
              570  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              572  POP_TOP          

 L. 657       574  LOAD_GLOBAL              QtWidgets
              576  LOAD_ATTR                QMessageBox
              578  LOAD_METHOD              critical
              580  LOAD_DEREF               'self'
              582  LOAD_ATTR                msgbox

 L. 658       584  LOAD_STR                 'Train 2D-DCNN'

 L. 659       586  LOAD_STR                 'Feature channel number not match with pre-trained network'
              588  CALL_METHOD_3         3  '3 positional arguments'
              590  POP_TOP          

 L. 660       592  LOAD_CONST               None
              594  RETURN_VALUE     
            596_0  COME_FROM           556  '556'

 L. 662       596  LOAD_GLOBAL              basic_data
              598  LOAD_METHOD              str2int
              600  LOAD_DEREF               'self'
              602  LOAD_ATTR                ldtnconvblock
              604  LOAD_METHOD              text
              606  CALL_METHOD_0         0  '0 positional arguments'
              608  CALL_METHOD_1         1  '1 positional argument'
              610  STORE_FAST               '_nconvblock'

 L. 663       612  LOAD_CLOSURE             'self'
              614  BUILD_TUPLE_1         1 
              616  LOAD_LISTCOMP            '<code_object <listcomp>>'
              618  LOAD_STR                 'trainml2ddcnnfromexisting.clickBtnTrainMl2DDcnnFromExisting.<locals>.<listcomp>'
              620  MAKE_FUNCTION_8          'closure'
              622  LOAD_GLOBAL              range
              624  LOAD_FAST                '_nconvblock'
              626  CALL_FUNCTION_1       1  '1 positional argument'
              628  GET_ITER         
              630  CALL_FUNCTION_1       1  '1 positional argument'
              632  STORE_FAST               '_nconvlayer'

 L. 664       634  LOAD_CLOSURE             'self'
              636  BUILD_TUPLE_1         1 
              638  LOAD_LISTCOMP            '<code_object <listcomp>>'
              640  LOAD_STR                 'trainml2ddcnnfromexisting.clickBtnTrainMl2DDcnnFromExisting.<locals>.<listcomp>'
              642  MAKE_FUNCTION_8          'closure'
              644  LOAD_GLOBAL              range
              646  LOAD_FAST                '_nconvblock'
              648  CALL_FUNCTION_1       1  '1 positional argument'
              650  GET_ITER         
              652  CALL_FUNCTION_1       1  '1 positional argument'
              654  STORE_FAST               '_nconvfeature'

 L. 665       656  LOAD_GLOBAL              basic_data
              658  LOAD_METHOD              str2int
              660  LOAD_DEREF               'self'
              662  LOAD_ATTR                ldtn1x1layer
              664  LOAD_METHOD              text
              666  CALL_METHOD_0         0  '0 positional arguments'
              668  CALL_METHOD_1         1  '1 positional argument'
              670  STORE_FAST               '_n1x1layer'

 L. 666       672  LOAD_CLOSURE             'self'
              674  BUILD_TUPLE_1         1 
              676  LOAD_LISTCOMP            '<code_object <listcomp>>'
              678  LOAD_STR                 'trainml2ddcnnfromexisting.clickBtnTrainMl2DDcnnFromExisting.<locals>.<listcomp>'
              680  MAKE_FUNCTION_8          'closure'
              682  LOAD_GLOBAL              range
              684  LOAD_FAST                '_n1x1layer'
              686  CALL_FUNCTION_1       1  '1 positional argument'
              688  GET_ITER         
              690  CALL_FUNCTION_1       1  '1 positional argument'
              692  STORE_FAST               '_n1x1feature'

 L. 667       694  LOAD_GLOBAL              basic_data
              696  LOAD_METHOD              str2int
              698  LOAD_DEREF               'self'
              700  LOAD_ATTR                ldtmaskheight
              702  LOAD_METHOD              text
              704  CALL_METHOD_0         0  '0 positional arguments'
              706  CALL_METHOD_1         1  '1 positional argument'
              708  STORE_FAST               '_patch_height'

 L. 668       710  LOAD_GLOBAL              basic_data
              712  LOAD_METHOD              str2int
              714  LOAD_DEREF               'self'
              716  LOAD_ATTR                ldtmaskwidth
              718  LOAD_METHOD              text
              720  CALL_METHOD_0         0  '0 positional arguments'
              722  CALL_METHOD_1         1  '1 positional argument'
              724  STORE_FAST               '_patch_width'

 L. 669       726  LOAD_GLOBAL              basic_data
              728  LOAD_METHOD              str2int
              730  LOAD_DEREF               'self'
              732  LOAD_ATTR                ldtpoolheight
              734  LOAD_METHOD              text
              736  CALL_METHOD_0         0  '0 positional arguments'
              738  CALL_METHOD_1         1  '1 positional argument'
              740  STORE_FAST               '_pool_height'

 L. 670       742  LOAD_GLOBAL              basic_data
              744  LOAD_METHOD              str2int
              746  LOAD_DEREF               'self'
              748  LOAD_ATTR                ldtpoolwidth
              750  LOAD_METHOD              text
              752  CALL_METHOD_0         0  '0 positional arguments'
              754  CALL_METHOD_1         1  '1 positional argument'
              756  STORE_FAST               '_pool_width'

 L. 671       758  LOAD_GLOBAL              basic_data
              760  LOAD_METHOD              str2int
              762  LOAD_DEREF               'self'
              764  LOAD_ATTR                ldtnepoch
              766  LOAD_METHOD              text
              768  CALL_METHOD_0         0  '0 positional arguments'
              770  CALL_METHOD_1         1  '1 positional argument'
              772  STORE_FAST               '_nepoch'

 L. 672       774  LOAD_GLOBAL              basic_data
              776  LOAD_METHOD              str2int
              778  LOAD_DEREF               'self'
              780  LOAD_ATTR                ldtbatchsize
              782  LOAD_METHOD              text
              784  CALL_METHOD_0         0  '0 positional arguments'
              786  CALL_METHOD_1         1  '1 positional argument'
              788  STORE_FAST               '_batchsize'

 L. 673       790  LOAD_GLOBAL              basic_data
              792  LOAD_METHOD              str2float
              794  LOAD_DEREF               'self'
              796  LOAD_ATTR                ldtlearnrate
              798  LOAD_METHOD              text
              800  CALL_METHOD_0         0  '0 positional arguments'
              802  CALL_METHOD_1         1  '1 positional argument'
              804  STORE_FAST               '_learning_rate'

 L. 674       806  LOAD_GLOBAL              basic_data
              808  LOAD_METHOD              str2float
              810  LOAD_DEREF               'self'
              812  LOAD_ATTR                ldtdropout
              814  LOAD_METHOD              text
              816  CALL_METHOD_0         0  '0 positional arguments'
              818  CALL_METHOD_1         1  '1 positional argument'
              820  STORE_FAST               '_dropout_prob'

 L. 675       822  LOAD_FAST                '_nconvblock'
              824  LOAD_CONST               False
              826  COMPARE_OP               is
          828_830  POP_JUMP_IF_TRUE    842  'to 842'
              832  LOAD_FAST                '_nconvblock'
              834  LOAD_CONST               0
              836  COMPARE_OP               <=
          838_840  POP_JUMP_IF_FALSE   878  'to 878'
            842_0  COME_FROM           828  '828'

 L. 676       842  LOAD_GLOBAL              vis_msg
              844  LOAD_ATTR                print
              846  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Non-positive convolutional block number'

 L. 677       848  LOAD_STR                 'error'
              850  LOAD_CONST               ('type',)
              852  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              854  POP_TOP          

 L. 678       856  LOAD_GLOBAL              QtWidgets
              858  LOAD_ATTR                QMessageBox
              860  LOAD_METHOD              critical
              862  LOAD_DEREF               'self'
              864  LOAD_ATTR                msgbox

 L. 679       866  LOAD_STR                 'Train 2D-DCNN'

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
              912  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Non-positive convolutional layer number'

 L. 685       914  LOAD_STR                 'error'
              916  LOAD_CONST               ('type',)
              918  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              920  POP_TOP          

 L. 686       922  LOAD_GLOBAL              QtWidgets
              924  LOAD_ATTR                QMessageBox
              926  LOAD_METHOD              critical
              928  LOAD_DEREF               'self'
              930  LOAD_ATTR                msgbox

 L. 687       932  LOAD_STR                 'Train 2D-DCNN'

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
              984  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Non-positive convolutional feature number'

 L. 693       986  LOAD_STR                 'error'
              988  LOAD_CONST               ('type',)
              990  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              992  POP_TOP          

 L. 694       994  LOAD_GLOBAL              QtWidgets
              996  LOAD_ATTR                QMessageBox
              998  LOAD_METHOD              critical
             1000  LOAD_DEREF               'self'
             1002  LOAD_ATTR                msgbox

 L. 695      1004  LOAD_STR                 'Train 2D-DCNN'

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
             1046  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Non-positive 1x1 convolutional layer number'

 L. 700      1048  LOAD_STR                 'error'
             1050  LOAD_CONST               ('type',)
             1052  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1054  POP_TOP          

 L. 701      1056  LOAD_GLOBAL              QtWidgets
             1058  LOAD_ATTR                QMessageBox
             1060  LOAD_METHOD              critical
             1062  LOAD_DEREF               'self'
             1064  LOAD_ATTR                msgbox

 L. 702      1066  LOAD_STR                 'Train 2D-DCNN'

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
             1112  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Non-positive 1x1 convolutional feature number'

 L. 708      1114  LOAD_STR                 'error'
             1116  LOAD_CONST               ('type',)
             1118  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1120  POP_TOP          

 L. 709      1122  LOAD_GLOBAL              QtWidgets
             1124  LOAD_ATTR                QMessageBox
             1126  LOAD_METHOD              critical
             1128  LOAD_DEREF               'self'
             1130  LOAD_ATTR                msgbox

 L. 710      1132  LOAD_STR                 'Train 2D-DCNN'

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
             1194  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Non-positive convolutional patch size'

 L. 716      1196  LOAD_STR                 'error'
             1198  LOAD_CONST               ('type',)
             1200  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1202  POP_TOP          

 L. 717      1204  LOAD_GLOBAL              QtWidgets
             1206  LOAD_ATTR                QMessageBox
             1208  LOAD_METHOD              critical
             1210  LOAD_DEREF               'self'
             1212  LOAD_ATTR                msgbox

 L. 718      1214  LOAD_STR                 'Train 2D-DCNN'

 L. 719      1216  LOAD_STR                 'Non-positive convolutional patch size'
             1218  CALL_METHOD_3         3  '3 positional arguments'
             1220  POP_TOP          

 L. 720      1222  LOAD_CONST               None
             1224  RETURN_VALUE     
           1226_0  COME_FROM          1186  '1186'

 L. 721      1226  LOAD_FAST                '_pool_height'
             1228  LOAD_CONST               False
             1230  COMPARE_OP               is
         1232_1234  POP_JUMP_IF_TRUE   1266  'to 1266'
             1236  LOAD_FAST                '_pool_width'
             1238  LOAD_CONST               False
             1240  COMPARE_OP               is
         1242_1244  POP_JUMP_IF_TRUE   1266  'to 1266'

 L. 722      1246  LOAD_FAST                '_pool_height'
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

 L. 723      1266  LOAD_GLOBAL              vis_msg
             1268  LOAD_ATTR                print
             1270  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Non-positive pooling size'
             1272  LOAD_STR                 'error'
             1274  LOAD_CONST               ('type',)
             1276  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1278  POP_TOP          

 L. 724      1280  LOAD_GLOBAL              QtWidgets
             1282  LOAD_ATTR                QMessageBox
             1284  LOAD_METHOD              critical
             1286  LOAD_DEREF               'self'
             1288  LOAD_ATTR                msgbox

 L. 725      1290  LOAD_STR                 'Train 2D-DCNN'

 L. 726      1292  LOAD_STR                 'Non-positive pooling size'
             1294  CALL_METHOD_3         3  '3 positional arguments'
             1296  POP_TOP          

 L. 727      1298  LOAD_CONST               None
             1300  RETURN_VALUE     
           1302_0  COME_FROM          1262  '1262'

 L. 728      1302  LOAD_FAST                '_nepoch'
             1304  LOAD_CONST               False
             1306  COMPARE_OP               is
         1308_1310  POP_JUMP_IF_TRUE   1322  'to 1322'
             1312  LOAD_FAST                '_nepoch'
             1314  LOAD_CONST               0
             1316  COMPARE_OP               <=
         1318_1320  POP_JUMP_IF_FALSE  1358  'to 1358'
           1322_0  COME_FROM          1308  '1308'

 L. 729      1322  LOAD_GLOBAL              vis_msg
             1324  LOAD_ATTR                print
             1326  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Non-positive epoch number'
             1328  LOAD_STR                 'error'
             1330  LOAD_CONST               ('type',)
             1332  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1334  POP_TOP          

 L. 730      1336  LOAD_GLOBAL              QtWidgets
             1338  LOAD_ATTR                QMessageBox
             1340  LOAD_METHOD              critical
             1342  LOAD_DEREF               'self'
             1344  LOAD_ATTR                msgbox

 L. 731      1346  LOAD_STR                 'Train 2D-DCNN'

 L. 732      1348  LOAD_STR                 'Non-positive epoch number'
             1350  CALL_METHOD_3         3  '3 positional arguments'
             1352  POP_TOP          

 L. 733      1354  LOAD_CONST               None
             1356  RETURN_VALUE     
           1358_0  COME_FROM          1318  '1318'

 L. 734      1358  LOAD_FAST                '_batchsize'
             1360  LOAD_CONST               False
             1362  COMPARE_OP               is
         1364_1366  POP_JUMP_IF_TRUE   1378  'to 1378'
             1368  LOAD_FAST                '_batchsize'
             1370  LOAD_CONST               0
             1372  COMPARE_OP               <=
         1374_1376  POP_JUMP_IF_FALSE  1414  'to 1414'
           1378_0  COME_FROM          1364  '1364'

 L. 735      1378  LOAD_GLOBAL              vis_msg
             1380  LOAD_ATTR                print
             1382  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Non-positive batch size'
             1384  LOAD_STR                 'error'
             1386  LOAD_CONST               ('type',)
             1388  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1390  POP_TOP          

 L. 736      1392  LOAD_GLOBAL              QtWidgets
             1394  LOAD_ATTR                QMessageBox
             1396  LOAD_METHOD              critical
             1398  LOAD_DEREF               'self'
             1400  LOAD_ATTR                msgbox

 L. 737      1402  LOAD_STR                 'Train 2D-DCNN'

 L. 738      1404  LOAD_STR                 'Non-positive batch size'
             1406  CALL_METHOD_3         3  '3 positional arguments'
             1408  POP_TOP          

 L. 739      1410  LOAD_CONST               None
             1412  RETURN_VALUE     
           1414_0  COME_FROM          1374  '1374'

 L. 740      1414  LOAD_FAST                '_learning_rate'
             1416  LOAD_CONST               False
             1418  COMPARE_OP               is
         1420_1422  POP_JUMP_IF_TRUE   1434  'to 1434'
             1424  LOAD_FAST                '_learning_rate'
             1426  LOAD_CONST               0
             1428  COMPARE_OP               <=
         1430_1432  POP_JUMP_IF_FALSE  1470  'to 1470'
           1434_0  COME_FROM          1420  '1420'

 L. 741      1434  LOAD_GLOBAL              vis_msg
             1436  LOAD_ATTR                print
             1438  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Non-positive learning rate'
             1440  LOAD_STR                 'error'
             1442  LOAD_CONST               ('type',)
             1444  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1446  POP_TOP          

 L. 742      1448  LOAD_GLOBAL              QtWidgets
             1450  LOAD_ATTR                QMessageBox
             1452  LOAD_METHOD              critical
             1454  LOAD_DEREF               'self'
             1456  LOAD_ATTR                msgbox

 L. 743      1458  LOAD_STR                 'Train 2D-DCNN'

 L. 744      1460  LOAD_STR                 'Non-positive learning rate'
             1462  CALL_METHOD_3         3  '3 positional arguments'
             1464  POP_TOP          

 L. 745      1466  LOAD_CONST               None
             1468  RETURN_VALUE     
           1470_0  COME_FROM          1430  '1430'

 L. 746      1470  LOAD_FAST                '_dropout_prob'
             1472  LOAD_CONST               False
             1474  COMPARE_OP               is
         1476_1478  POP_JUMP_IF_TRUE   1490  'to 1490'
             1480  LOAD_FAST                '_dropout_prob'
             1482  LOAD_CONST               0
             1484  COMPARE_OP               <=
         1486_1488  POP_JUMP_IF_FALSE  1526  'to 1526'
           1490_0  COME_FROM          1476  '1476'

 L. 747      1490  LOAD_GLOBAL              vis_msg
             1492  LOAD_ATTR                print
             1494  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: Negative dropout rate'
             1496  LOAD_STR                 'error'
             1498  LOAD_CONST               ('type',)
             1500  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1502  POP_TOP          

 L. 748      1504  LOAD_GLOBAL              QtWidgets
             1506  LOAD_ATTR                QMessageBox
             1508  LOAD_METHOD              critical
             1510  LOAD_DEREF               'self'
             1512  LOAD_ATTR                msgbox

 L. 749      1514  LOAD_STR                 'Train 2D-DCNN'

 L. 750      1516  LOAD_STR                 'Negative dropout rate'
             1518  CALL_METHOD_3         3  '3 positional arguments'
             1520  POP_TOP          

 L. 751      1522  LOAD_CONST               None
             1524  RETURN_VALUE     
           1526_0  COME_FROM          1486  '1486'

 L. 753      1526  LOAD_GLOBAL              len
             1528  LOAD_DEREF               'self'
             1530  LOAD_ATTR                ldtsave
             1532  LOAD_METHOD              text
             1534  CALL_METHOD_0         0  '0 positional arguments'
             1536  CALL_FUNCTION_1       1  '1 positional argument'
             1538  LOAD_CONST               1
             1540  COMPARE_OP               <
         1542_1544  POP_JUMP_IF_FALSE  1582  'to 1582'

 L. 754      1546  LOAD_GLOBAL              vis_msg
             1548  LOAD_ATTR                print
             1550  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: No name specified for DCNN network'
             1552  LOAD_STR                 'error'
             1554  LOAD_CONST               ('type',)
             1556  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1558  POP_TOP          

 L. 755      1560  LOAD_GLOBAL              QtWidgets
             1562  LOAD_ATTR                QMessageBox
             1564  LOAD_METHOD              critical
             1566  LOAD_DEREF               'self'
             1568  LOAD_ATTR                msgbox

 L. 756      1570  LOAD_STR                 'Train 2D-DCNN'

 L. 757      1572  LOAD_STR                 'No name specified for DCNN network'
             1574  CALL_METHOD_3         3  '3 positional arguments'
             1576  POP_TOP          

 L. 758      1578  LOAD_CONST               None
             1580  RETURN_VALUE     
           1582_0  COME_FROM          1542  '1542'

 L. 759      1582  LOAD_GLOBAL              os
             1584  LOAD_ATTR                path
             1586  LOAD_METHOD              dirname
             1588  LOAD_DEREF               'self'
             1590  LOAD_ATTR                ldtsave
             1592  LOAD_METHOD              text
             1594  CALL_METHOD_0         0  '0 positional arguments'
             1596  CALL_METHOD_1         1  '1 positional argument'
             1598  STORE_FAST               '_savepath'

 L. 760      1600  LOAD_GLOBAL              os
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

 L. 762      1630  LOAD_CONST               0
             1632  STORE_FAST               '_wdinl'

 L. 763      1634  LOAD_CONST               0
             1636  STORE_FAST               '_wdxl'

 L. 764      1638  LOAD_CONST               0
             1640  STORE_FAST               '_wdz'

 L. 765      1642  LOAD_DEREF               'self'
             1644  LOAD_ATTR                cbbornt
             1646  LOAD_METHOD              currentIndex
             1648  CALL_METHOD_0         0  '0 positional arguments'
             1650  LOAD_CONST               0
             1652  COMPARE_OP               ==
         1654_1656  POP_JUMP_IF_FALSE  1682  'to 1682'

 L. 766      1658  LOAD_GLOBAL              int
             1660  LOAD_FAST                '_image_width'
             1662  LOAD_CONST               2
             1664  BINARY_TRUE_DIVIDE
             1666  CALL_FUNCTION_1       1  '1 positional argument'
             1668  STORE_FAST               '_wdxl'

 L. 767      1670  LOAD_GLOBAL              int
             1672  LOAD_FAST                '_image_height'
             1674  LOAD_CONST               2
             1676  BINARY_TRUE_DIVIDE
             1678  CALL_FUNCTION_1       1  '1 positional argument'
             1680  STORE_FAST               '_wdz'
           1682_0  COME_FROM          1654  '1654'

 L. 768      1682  LOAD_DEREF               'self'
             1684  LOAD_ATTR                cbbornt
             1686  LOAD_METHOD              currentIndex
             1688  CALL_METHOD_0         0  '0 positional arguments'
             1690  LOAD_CONST               1
             1692  COMPARE_OP               ==
         1694_1696  POP_JUMP_IF_FALSE  1722  'to 1722'

 L. 769      1698  LOAD_GLOBAL              int
             1700  LOAD_FAST                '_image_width'
             1702  LOAD_CONST               2
             1704  BINARY_TRUE_DIVIDE
             1706  CALL_FUNCTION_1       1  '1 positional argument'
             1708  STORE_FAST               '_wdinl'

 L. 770      1710  LOAD_GLOBAL              int
             1712  LOAD_FAST                '_image_height'
             1714  LOAD_CONST               2
             1716  BINARY_TRUE_DIVIDE
             1718  CALL_FUNCTION_1       1  '1 positional argument'
             1720  STORE_FAST               '_wdz'
           1722_0  COME_FROM          1694  '1694'

 L. 771      1722  LOAD_DEREF               'self'
             1724  LOAD_ATTR                cbbornt
             1726  LOAD_METHOD              currentIndex
             1728  CALL_METHOD_0         0  '0 positional arguments'
             1730  LOAD_CONST               2
             1732  COMPARE_OP               ==
         1734_1736  POP_JUMP_IF_FALSE  1762  'to 1762'

 L. 772      1738  LOAD_GLOBAL              int
             1740  LOAD_FAST                '_image_width'
             1742  LOAD_CONST               2
             1744  BINARY_TRUE_DIVIDE
             1746  CALL_FUNCTION_1       1  '1 positional argument'
             1748  STORE_FAST               '_wdinl'

 L. 773      1750  LOAD_GLOBAL              int
             1752  LOAD_FAST                '_image_height'
             1754  LOAD_CONST               2
             1756  BINARY_TRUE_DIVIDE
             1758  CALL_FUNCTION_1       1  '1 positional argument'
             1760  STORE_FAST               '_wdxl'
           1762_0  COME_FROM          1734  '1734'

 L. 775      1762  LOAD_DEREF               'self'
             1764  LOAD_ATTR                survinfo
             1766  STORE_FAST               '_seisinfo'

 L. 777      1768  LOAD_GLOBAL              print
             1770  LOAD_STR                 'TrainMl2DDcnnFromExisting: Step 1 - Step 1 - Get training samples:'
             1772  CALL_FUNCTION_1       1  '1 positional argument'
             1774  POP_TOP          

 L. 778      1776  LOAD_DEREF               'self'
             1778  LOAD_ATTR                traindataconfig
             1780  LOAD_STR                 'TrainPointSet'
             1782  BINARY_SUBSCR    
             1784  STORE_FAST               '_trainpoint'

 L. 779      1786  LOAD_GLOBAL              np
             1788  LOAD_METHOD              zeros
             1790  LOAD_CONST               0
             1792  LOAD_CONST               3
             1794  BUILD_LIST_2          2 
             1796  CALL_METHOD_1         1  '1 positional argument'
             1798  STORE_FAST               '_traindata'

 L. 780      1800  SETUP_LOOP         1876  'to 1876'
             1802  LOAD_FAST                '_trainpoint'
             1804  GET_ITER         
           1806_0  COME_FROM          1824  '1824'
             1806  FOR_ITER           1874  'to 1874'
             1808  STORE_FAST               '_p'

 L. 781      1810  LOAD_GLOBAL              point_ays
             1812  LOAD_METHOD              checkPoint
             1814  LOAD_DEREF               'self'
             1816  LOAD_ATTR                pointsetdata
             1818  LOAD_FAST                '_p'
             1820  BINARY_SUBSCR    
             1822  CALL_METHOD_1         1  '1 positional argument'
         1824_1826  POP_JUMP_IF_FALSE  1806  'to 1806'

 L. 782      1828  LOAD_GLOBAL              basic_mdt
             1830  LOAD_METHOD              exportMatDict
             1832  LOAD_DEREF               'self'
             1834  LOAD_ATTR                pointsetdata
             1836  LOAD_FAST                '_p'
             1838  BINARY_SUBSCR    
             1840  LOAD_STR                 'Inline'
             1842  LOAD_STR                 'Crossline'
             1844  LOAD_STR                 'Z'
             1846  BUILD_LIST_3          3 
             1848  CALL_METHOD_2         2  '2 positional arguments'
             1850  STORE_FAST               '_pt'

 L. 783      1852  LOAD_GLOBAL              np
             1854  LOAD_ATTR                concatenate
             1856  LOAD_FAST                '_traindata'
             1858  LOAD_FAST                '_pt'
             1860  BUILD_TUPLE_2         2 
             1862  LOAD_CONST               0
             1864  LOAD_CONST               ('axis',)
             1866  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1868  STORE_FAST               '_traindata'
         1870_1872  JUMP_BACK          1806  'to 1806'
             1874  POP_BLOCK        
           1876_0  COME_FROM_LOOP     1800  '1800'

 L. 784      1876  LOAD_GLOBAL              seis_ays
             1878  LOAD_ATTR                removeOutofSurveySample
             1880  LOAD_FAST                '_traindata'

 L. 785      1882  LOAD_FAST                '_seisinfo'
             1884  LOAD_STR                 'ILStart'
             1886  BINARY_SUBSCR    
             1888  LOAD_FAST                '_wdinl'
             1890  LOAD_FAST                '_seisinfo'
             1892  LOAD_STR                 'ILStep'
             1894  BINARY_SUBSCR    
             1896  BINARY_MULTIPLY  
             1898  BINARY_ADD       

 L. 786      1900  LOAD_FAST                '_seisinfo'
             1902  LOAD_STR                 'ILEnd'
             1904  BINARY_SUBSCR    
             1906  LOAD_FAST                '_wdinl'
             1908  LOAD_FAST                '_seisinfo'
             1910  LOAD_STR                 'ILStep'
             1912  BINARY_SUBSCR    
             1914  BINARY_MULTIPLY  
             1916  BINARY_SUBTRACT  

 L. 787      1918  LOAD_FAST                '_seisinfo'
             1920  LOAD_STR                 'XLStart'
             1922  BINARY_SUBSCR    
             1924  LOAD_FAST                '_wdxl'
             1926  LOAD_FAST                '_seisinfo'
             1928  LOAD_STR                 'XLStep'
             1930  BINARY_SUBSCR    
             1932  BINARY_MULTIPLY  
             1934  BINARY_ADD       

 L. 788      1936  LOAD_FAST                '_seisinfo'
             1938  LOAD_STR                 'XLEnd'
             1940  BINARY_SUBSCR    
             1942  LOAD_FAST                '_wdxl'
             1944  LOAD_FAST                '_seisinfo'
             1946  LOAD_STR                 'XLStep'
             1948  BINARY_SUBSCR    
             1950  BINARY_MULTIPLY  
             1952  BINARY_SUBTRACT  

 L. 789      1954  LOAD_FAST                '_seisinfo'
             1956  LOAD_STR                 'ZStart'
             1958  BINARY_SUBSCR    
             1960  LOAD_FAST                '_wdz'
             1962  LOAD_FAST                '_seisinfo'
             1964  LOAD_STR                 'ZStep'
             1966  BINARY_SUBSCR    
             1968  BINARY_MULTIPLY  
             1970  BINARY_ADD       

 L. 790      1972  LOAD_FAST                '_seisinfo'
             1974  LOAD_STR                 'ZEnd'
             1976  BINARY_SUBSCR    
             1978  LOAD_FAST                '_wdz'
             1980  LOAD_FAST                '_seisinfo'
             1982  LOAD_STR                 'ZStep'
             1984  BINARY_SUBSCR    
             1986  BINARY_MULTIPLY  
             1988  BINARY_SUBTRACT  
             1990  LOAD_CONST               ('inlstart', 'inlend', 'xlstart', 'xlend', 'zstart', 'zend')
             1992  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             1994  STORE_FAST               '_traindata'

 L. 793      1996  LOAD_GLOBAL              np
             1998  LOAD_METHOD              shape
             2000  LOAD_FAST                '_traindata'
             2002  CALL_METHOD_1         1  '1 positional argument'
             2004  LOAD_CONST               0
             2006  BINARY_SUBSCR    
             2008  LOAD_CONST               0
             2010  COMPARE_OP               <=
         2012_2014  POP_JUMP_IF_FALSE  2052  'to 2052'

 L. 794      2016  LOAD_GLOBAL              vis_msg
             2018  LOAD_ATTR                print
             2020  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: No training sample found'
             2022  LOAD_STR                 'error'
             2024  LOAD_CONST               ('type',)
             2026  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2028  POP_TOP          

 L. 795      2030  LOAD_GLOBAL              QtWidgets
             2032  LOAD_ATTR                QMessageBox
             2034  LOAD_METHOD              critical
             2036  LOAD_DEREF               'self'
             2038  LOAD_ATTR                msgbox

 L. 796      2040  LOAD_STR                 'Train 2D-DCNN'

 L. 797      2042  LOAD_STR                 'No training sample found'
             2044  CALL_METHOD_3         3  '3 positional arguments'
             2046  POP_TOP          

 L. 798      2048  LOAD_CONST               None
             2050  RETURN_VALUE     
           2052_0  COME_FROM          2012  '2012'

 L. 801      2052  LOAD_GLOBAL              print
             2054  LOAD_STR                 'TrainMl2DDcnnFromExisting: Step 2 - Retrieve and interpolate images if necessary: (%d, %d) --> (%d, %d)'

 L. 802      2056  LOAD_FAST                '_image_height'
             2058  LOAD_FAST                '_image_width'
             2060  LOAD_FAST                '_image_height_new'
             2062  LOAD_FAST                '_image_width_new'
             2064  BUILD_TUPLE_4         4 
             2066  BINARY_MODULO    
             2068  CALL_FUNCTION_1       1  '1 positional argument'
             2070  POP_TOP          

 L. 803      2072  BUILD_MAP_0           0 
             2074  STORE_FAST               '_traindict'

 L. 804      2076  SETUP_LOOP         2148  'to 2148'
             2078  LOAD_FAST                '_features'
             2080  GET_ITER         
             2082  FOR_ITER           2146  'to 2146'
             2084  STORE_FAST               'f'

 L. 805      2086  LOAD_DEREF               'self'
             2088  LOAD_ATTR                seisdata
             2090  LOAD_FAST                'f'
             2092  BINARY_SUBSCR    
             2094  STORE_FAST               '_seisdata'

 L. 806      2096  LOAD_GLOBAL              seis_ays
             2098  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2100  LOAD_FAST                '_seisdata'
             2102  LOAD_FAST                '_traindata'
             2104  LOAD_DEREF               'self'
             2106  LOAD_ATTR                survinfo

 L. 807      2108  LOAD_FAST                '_wdinl'
             2110  LOAD_FAST                '_wdxl'
             2112  LOAD_FAST                '_wdz'

 L. 808      2114  LOAD_CONST               False
             2116  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2118  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2120  LOAD_CONST               None
             2122  LOAD_CONST               None
             2124  BUILD_SLICE_2         2 
             2126  LOAD_CONST               3
             2128  LOAD_CONST               None
             2130  BUILD_SLICE_2         2 
             2132  BUILD_TUPLE_2         2 
             2134  BINARY_SUBSCR    
             2136  LOAD_FAST                '_traindict'
             2138  LOAD_FAST                'f'
             2140  STORE_SUBSCR     
         2142_2144  JUMP_BACK          2082  'to 2082'
             2146  POP_BLOCK        
           2148_0  COME_FROM_LOOP     2076  '2076'

 L. 809      2148  LOAD_FAST                '_target'
             2150  LOAD_FAST                '_features'
             2152  COMPARE_OP               not-in
         2154_2156  POP_JUMP_IF_FALSE  2214  'to 2214'

 L. 810      2158  LOAD_DEREF               'self'
             2160  LOAD_ATTR                seisdata
             2162  LOAD_FAST                '_target'
             2164  BINARY_SUBSCR    
             2166  STORE_FAST               '_seisdata'

 L. 811      2168  LOAD_GLOBAL              seis_ays
             2170  LOAD_ATTR                retrieveSeisWindowFrom3DMat
             2172  LOAD_FAST                '_seisdata'
             2174  LOAD_FAST                '_traindata'
             2176  LOAD_DEREF               'self'
             2178  LOAD_ATTR                survinfo

 L. 812      2180  LOAD_FAST                '_wdinl'

 L. 813      2182  LOAD_FAST                '_wdxl'

 L. 814      2184  LOAD_FAST                '_wdz'

 L. 815      2186  LOAD_CONST               False
             2188  LOAD_CONST               ('seisinfo', 'wdinl', 'wdxl', 'wdz', 'verbose')
             2190  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
             2192  LOAD_CONST               None
             2194  LOAD_CONST               None
             2196  BUILD_SLICE_2         2 
             2198  LOAD_CONST               3
             2200  LOAD_CONST               None
             2202  BUILD_SLICE_2         2 
             2204  BUILD_TUPLE_2         2 
             2206  BINARY_SUBSCR    
             2208  LOAD_FAST                '_traindict'
             2210  LOAD_FAST                '_target'
             2212  STORE_SUBSCR     
           2214_0  COME_FROM          2154  '2154'

 L. 817      2214  LOAD_DEREF               'self'
             2216  LOAD_ATTR                traindataconfig
             2218  LOAD_STR                 'RemoveInvariantFeature_Checked'
             2220  BINARY_SUBSCR    
         2222_2224  POP_JUMP_IF_FALSE  2306  'to 2306'

 L. 818      2226  SETUP_LOOP         2306  'to 2306'
             2228  LOAD_FAST                '_features'
             2230  GET_ITER         
           2232_0  COME_FROM          2260  '2260'
             2232  FOR_ITER           2304  'to 2304'
             2234  STORE_FAST               'f'

 L. 819      2236  LOAD_GLOBAL              ml_aug
             2238  LOAD_METHOD              removeInvariantFeature
             2240  LOAD_FAST                '_traindict'
             2242  LOAD_FAST                'f'
             2244  CALL_METHOD_2         2  '2 positional arguments'
             2246  STORE_FAST               '_traindict'

 L. 820      2248  LOAD_GLOBAL              basic_mdt
             2250  LOAD_METHOD              maxDictConstantRow
             2252  LOAD_FAST                '_traindict'
             2254  CALL_METHOD_1         1  '1 positional argument'
             2256  LOAD_CONST               0
             2258  COMPARE_OP               <=
         2260_2262  POP_JUMP_IF_FALSE  2232  'to 2232'

 L. 821      2264  LOAD_GLOBAL              vis_msg
             2266  LOAD_ATTR                print
             2268  LOAD_STR                 'ERROR in TrainMl2DDcnnFromExisting: No training sample found'
             2270  LOAD_STR                 'error'
             2272  LOAD_CONST               ('type',)
             2274  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2276  POP_TOP          

 L. 822      2278  LOAD_GLOBAL              QtWidgets
             2280  LOAD_ATTR                QMessageBox
             2282  LOAD_METHOD              critical
             2284  LOAD_DEREF               'self'
             2286  LOAD_ATTR                msgbox

 L. 823      2288  LOAD_STR                 'Train 2D-DCNN'

 L. 824      2290  LOAD_STR                 'No training sample found'
             2292  CALL_METHOD_3         3  '3 positional arguments'
             2294  POP_TOP          

 L. 825      2296  LOAD_CONST               None
             2298  RETURN_VALUE     
         2300_2302  JUMP_BACK          2232  'to 2232'
             2304  POP_BLOCK        
           2306_0  COME_FROM_LOOP     2226  '2226'
           2306_1  COME_FROM          2222  '2222'

 L. 826      2306  LOAD_FAST                '_image_height_new'
             2308  LOAD_FAST                '_image_height'
             2310  COMPARE_OP               !=
         2312_2314  POP_JUMP_IF_TRUE   2326  'to 2326'
             2316  LOAD_FAST                '_image_width_new'
             2318  LOAD_FAST                '_image_width'
             2320  COMPARE_OP               !=
         2322_2324  POP_JUMP_IF_FALSE  2410  'to 2410'
           2326_0  COME_FROM          2312  '2312'

 L. 827      2326  SETUP_LOOP         2370  'to 2370'
             2328  LOAD_FAST                '_features'
             2330  GET_ITER         
             2332  FOR_ITER           2368  'to 2368'
             2334  STORE_FAST               'f'

 L. 828      2336  LOAD_GLOBAL              basic_image
             2338  LOAD_ATTR                changeImageSize
             2340  LOAD_FAST                '_traindict'
             2342  LOAD_FAST                'f'
             2344  BINARY_SUBSCR    

 L. 829      2346  LOAD_FAST                '_image_height'

 L. 830      2348  LOAD_FAST                '_image_width'

 L. 831      2350  LOAD_FAST                '_image_height_new'

 L. 832      2352  LOAD_FAST                '_image_width_new'
             2354  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new')
             2356  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             2358  LOAD_FAST                '_traindict'
             2360  LOAD_FAST                'f'
             2362  STORE_SUBSCR     
         2364_2366  JUMP_BACK          2332  'to 2332'
             2368  POP_BLOCK        
           2370_0  COME_FROM_LOOP     2326  '2326'

 L. 833      2370  LOAD_FAST                '_target'
             2372  LOAD_FAST                '_features'
             2374  COMPARE_OP               not-in
         2376_2378  POP_JUMP_IF_FALSE  2410  'to 2410'

 L. 834      2380  LOAD_GLOBAL              basic_image
             2382  LOAD_ATTR                changeImageSize
             2384  LOAD_FAST                '_traindict'
             2386  LOAD_FAST                '_target'
             2388  BINARY_SUBSCR    

 L. 835      2390  LOAD_FAST                '_image_height'

 L. 836      2392  LOAD_FAST                '_image_width'

 L. 837      2394  LOAD_FAST                '_image_height_new'

 L. 838      2396  LOAD_FAST                '_image_width_new'
             2398  LOAD_STR                 'linear'
             2400  LOAD_CONST               ('image_height', 'image_width', 'image_height_new', 'image_width_new', 'kind')
             2402  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             2404  LOAD_FAST                '_traindict'
             2406  LOAD_FAST                '_target'
             2408  STORE_SUBSCR     
           2410_0  COME_FROM          2376  '2376'
           2410_1  COME_FROM          2322  '2322'

 L. 839      2410  LOAD_DEREF               'self'
             2412  LOAD_ATTR                traindataconfig
             2414  LOAD_STR                 'RotateFeature_Checked'
             2416  BINARY_SUBSCR    
             2418  LOAD_CONST               True
             2420  COMPARE_OP               is
         2422_2424  POP_JUMP_IF_FALSE  2564  'to 2564'

 L. 840      2426  SETUP_LOOP         2498  'to 2498'
             2428  LOAD_FAST                '_features'
             2430  GET_ITER         
             2432  FOR_ITER           2496  'to 2496'
             2434  STORE_FAST               'f'

 L. 841      2436  LOAD_FAST                '_image_height_new'
             2438  LOAD_FAST                '_image_width_new'
             2440  COMPARE_OP               ==
         2442_2444  POP_JUMP_IF_FALSE  2470  'to 2470'

 L. 842      2446  LOAD_GLOBAL              ml_aug
             2448  LOAD_METHOD              rotateImage6Way
             2450  LOAD_FAST                '_traindict'
             2452  LOAD_FAST                'f'
             2454  BINARY_SUBSCR    
             2456  LOAD_FAST                '_image_height_new'
             2458  LOAD_FAST                '_image_width_new'
             2460  CALL_METHOD_3         3  '3 positional arguments'
             2462  LOAD_FAST                '_traindict'
             2464  LOAD_FAST                'f'
             2466  STORE_SUBSCR     
             2468  JUMP_BACK          2432  'to 2432'
           2470_0  COME_FROM          2442  '2442'

 L. 844      2470  LOAD_GLOBAL              ml_aug
             2472  LOAD_METHOD              rotateImage4Way
             2474  LOAD_FAST                '_traindict'
             2476  LOAD_FAST                'f'
             2478  BINARY_SUBSCR    
             2480  LOAD_FAST                '_image_height_new'
             2482  LOAD_FAST                '_image_width_new'
             2484  CALL_METHOD_3         3  '3 positional arguments'
             2486  LOAD_FAST                '_traindict'
             2488  LOAD_FAST                'f'
             2490  STORE_SUBSCR     
         2492_2494  JUMP_BACK          2432  'to 2432'
             2496  POP_BLOCK        
           2498_0  COME_FROM_LOOP     2426  '2426'

 L. 845      2498  LOAD_FAST                '_target'
             2500  LOAD_FAST                '_features'
             2502  COMPARE_OP               not-in
         2504_2506  POP_JUMP_IF_FALSE  2564  'to 2564'

 L. 846      2508  LOAD_FAST                '_image_height_new'
             2510  LOAD_FAST                '_image_width_new'
             2512  COMPARE_OP               ==
         2514_2516  POP_JUMP_IF_FALSE  2542  'to 2542'

 L. 848      2518  LOAD_GLOBAL              ml_aug
             2520  LOAD_METHOD              rotateImage6Way
             2522  LOAD_FAST                '_traindict'
             2524  LOAD_FAST                '_target'
             2526  BINARY_SUBSCR    
             2528  LOAD_FAST                '_image_height_new'
             2530  LOAD_FAST                '_image_width_new'
             2532  CALL_METHOD_3         3  '3 positional arguments'
             2534  LOAD_FAST                '_traindict'
             2536  LOAD_FAST                '_target'
             2538  STORE_SUBSCR     
             2540  JUMP_FORWARD       2564  'to 2564'
           2542_0  COME_FROM          2514  '2514'

 L. 851      2542  LOAD_GLOBAL              ml_aug
             2544  LOAD_METHOD              rotateImage4Way
             2546  LOAD_FAST                '_traindict'
             2548  LOAD_FAST                '_target'
             2550  BINARY_SUBSCR    
             2552  LOAD_FAST                '_image_height_new'
             2554  LOAD_FAST                '_image_width_new'
             2556  CALL_METHOD_3         3  '3 positional arguments'
             2558  LOAD_FAST                '_traindict'
             2560  LOAD_FAST                '_target'
             2562  STORE_SUBSCR     
           2564_0  COME_FROM          2540  '2540'
           2564_1  COME_FROM          2504  '2504'
           2564_2  COME_FROM          2422  '2422'

 L. 853      2564  LOAD_GLOBAL              np
             2566  LOAD_METHOD              round
             2568  LOAD_FAST                '_traindict'
             2570  LOAD_FAST                '_target'
             2572  BINARY_SUBSCR    
             2574  CALL_METHOD_1         1  '1 positional argument'
             2576  LOAD_METHOD              astype
             2578  LOAD_GLOBAL              int
             2580  CALL_METHOD_1         1  '1 positional argument'
             2582  LOAD_FAST                '_traindict'
             2584  LOAD_FAST                '_target'
             2586  STORE_SUBSCR     

 L. 855      2588  LOAD_GLOBAL              print
             2590  LOAD_STR                 'TrainMl2DDcnnFromExisting: A total of %d valid training samples'
             2592  LOAD_GLOBAL              basic_mdt
             2594  LOAD_METHOD              maxDictConstantRow

 L. 856      2596  LOAD_FAST                '_traindict'
             2598  CALL_METHOD_1         1  '1 positional argument'
             2600  BINARY_MODULO    
             2602  CALL_FUNCTION_1       1  '1 positional argument'
             2604  POP_TOP          

 L. 858      2606  LOAD_GLOBAL              print
             2608  LOAD_STR                 'TrainMl2DDcnnFromExisting: Step 3 - Start training'
             2610  CALL_FUNCTION_1       1  '1 positional argument'
             2612  POP_TOP          

 L. 860      2614  LOAD_GLOBAL              QtWidgets
             2616  LOAD_METHOD              QProgressDialog
             2618  CALL_METHOD_0         0  '0 positional arguments'
             2620  STORE_FAST               '_pgsdlg'

 L. 861      2622  LOAD_GLOBAL              QtGui
             2624  LOAD_METHOD              QIcon
             2626  CALL_METHOD_0         0  '0 positional arguments'
             2628  STORE_FAST               'icon'

 L. 862      2630  LOAD_FAST                'icon'
             2632  LOAD_METHOD              addPixmap
             2634  LOAD_GLOBAL              QtGui
             2636  LOAD_METHOD              QPixmap
             2638  LOAD_GLOBAL              os
             2640  LOAD_ATTR                path
             2642  LOAD_METHOD              join
             2644  LOAD_DEREF               'self'
             2646  LOAD_ATTR                iconpath
             2648  LOAD_STR                 'icons/new.png'
             2650  CALL_METHOD_2         2  '2 positional arguments'
             2652  CALL_METHOD_1         1  '1 positional argument'

 L. 863      2654  LOAD_GLOBAL              QtGui
             2656  LOAD_ATTR                QIcon
             2658  LOAD_ATTR                Normal
             2660  LOAD_GLOBAL              QtGui
             2662  LOAD_ATTR                QIcon
             2664  LOAD_ATTR                Off
             2666  CALL_METHOD_3         3  '3 positional arguments'
             2668  POP_TOP          

 L. 864      2670  LOAD_FAST                '_pgsdlg'
             2672  LOAD_METHOD              setWindowIcon
             2674  LOAD_FAST                'icon'
             2676  CALL_METHOD_1         1  '1 positional argument'
             2678  POP_TOP          

 L. 865      2680  LOAD_FAST                '_pgsdlg'
             2682  LOAD_METHOD              setWindowTitle
             2684  LOAD_STR                 'Train 2D-DCNN'
             2686  CALL_METHOD_1         1  '1 positional argument'
             2688  POP_TOP          

 L. 866      2690  LOAD_FAST                '_pgsdlg'
             2692  LOAD_METHOD              setCancelButton
             2694  LOAD_CONST               None
             2696  CALL_METHOD_1         1  '1 positional argument'
             2698  POP_TOP          

 L. 867      2700  LOAD_FAST                '_pgsdlg'
             2702  LOAD_METHOD              setWindowFlags
             2704  LOAD_GLOBAL              QtCore
             2706  LOAD_ATTR                Qt
             2708  LOAD_ATTR                WindowStaysOnTopHint
             2710  CALL_METHOD_1         1  '1 positional argument'
             2712  POP_TOP          

 L. 868      2714  LOAD_FAST                '_pgsdlg'
             2716  LOAD_METHOD              forceShow
             2718  CALL_METHOD_0         0  '0 positional arguments'
             2720  POP_TOP          

 L. 869      2722  LOAD_FAST                '_pgsdlg'
             2724  LOAD_METHOD              setFixedWidth
             2726  LOAD_CONST               400
             2728  CALL_METHOD_1         1  '1 positional argument'
             2730  POP_TOP          

 L. 870      2732  LOAD_GLOBAL              ml_dcnn
             2734  LOAD_ATTR                createDCNNSegmentorFromExisting
             2736  LOAD_FAST                '_traindict'

 L. 871      2738  LOAD_FAST                '_image_height_new'
             2740  LOAD_FAST                '_image_width_new'

 L. 872      2742  LOAD_FAST                '_features'
             2744  LOAD_FAST                '_target'

 L. 873      2746  LOAD_FAST                '_nepoch'
             2748  LOAD_FAST                '_batchsize'

 L. 874      2750  LOAD_FAST                '_nconvblock'
             2752  LOAD_FAST                '_nconvfeature'

 L. 875      2754  LOAD_FAST                '_nconvlayer'

 L. 876      2756  LOAD_FAST                '_n1x1layer'
             2758  LOAD_FAST                '_n1x1feature'

 L. 877      2760  LOAD_FAST                '_pool_height'
             2762  LOAD_FAST                '_pool_width'

 L. 878      2764  LOAD_FAST                '_learning_rate'

 L. 879      2766  LOAD_FAST                '_dropout_prob'

 L. 880      2768  LOAD_CONST               True

 L. 881      2770  LOAD_FAST                '_savepath'
             2772  LOAD_FAST                '_savename'

 L. 882      2774  LOAD_FAST                '_pgsdlg'

 L. 883      2776  LOAD_FAST                '_precnnpath'

 L. 884      2778  LOAD_FAST                '_precnnname'

 L. 885      2780  LOAD_FAST                '_blockidx'
             2782  LOAD_FAST                '_layeridx'

 L. 886      2784  LOAD_FAST                '_trainable'
             2786  LOAD_CONST               ('imageheight', 'imagewidth', 'features', 'target', 'nepoch', 'batchsize', 'nconvblock', 'nconvfeature', 'nconvlayer', 'n1x1layer', 'n1x1feature', 'poolheight', 'poolwidth', 'learningrate', 'dropoutprob', 'save2disk', 'savepath', 'savename', 'qpgsdlg', 'precnnpath', 'precnnname', 'blockidx', 'layeridx', 'trainable')
             2788  CALL_FUNCTION_KW_25    25  '25 total positional and keyword args'
             2790  STORE_FAST               '_dcnnlog'

 L. 889      2792  LOAD_GLOBAL              QtWidgets
             2794  LOAD_ATTR                QMessageBox
             2796  LOAD_METHOD              information
             2798  LOAD_DEREF               'self'
             2800  LOAD_ATTR                msgbox

 L. 890      2802  LOAD_STR                 'Train 2D-DCNN'

 L. 891      2804  LOAD_STR                 'DCNN trained successfully'
             2806  CALL_METHOD_3         3  '3 positional arguments'
             2808  POP_TOP          

 L. 893      2810  LOAD_GLOBAL              QtWidgets
             2812  LOAD_ATTR                QMessageBox
             2814  LOAD_METHOD              question
             2816  LOAD_DEREF               'self'
             2818  LOAD_ATTR                msgbox
             2820  LOAD_STR                 'Train 2D-DCNN'
             2822  LOAD_STR                 'View learning matrix?'

 L. 894      2824  LOAD_GLOBAL              QtWidgets
             2826  LOAD_ATTR                QMessageBox
             2828  LOAD_ATTR                Yes
             2830  LOAD_GLOBAL              QtWidgets
             2832  LOAD_ATTR                QMessageBox
             2834  LOAD_ATTR                No
             2836  BINARY_OR        

 L. 895      2838  LOAD_GLOBAL              QtWidgets
             2840  LOAD_ATTR                QMessageBox
             2842  LOAD_ATTR                Yes
             2844  CALL_METHOD_5         5  '5 positional arguments'
             2846  STORE_FAST               'reply'

 L. 897      2848  LOAD_FAST                'reply'
             2850  LOAD_GLOBAL              QtWidgets
             2852  LOAD_ATTR                QMessageBox
             2854  LOAD_ATTR                Yes
             2856  COMPARE_OP               ==
         2858_2860  POP_JUMP_IF_FALSE  2928  'to 2928'

 L. 898      2862  LOAD_GLOBAL              QtWidgets
             2864  LOAD_METHOD              QDialog
             2866  CALL_METHOD_0         0  '0 positional arguments'
             2868  STORE_FAST               '_viewmllearnmat'

 L. 899      2870  LOAD_GLOBAL              gui_viewmllearnmat
             2872  CALL_FUNCTION_0       0  '0 positional arguments'
             2874  STORE_FAST               '_gui'

 L. 900      2876  LOAD_FAST                '_dcnnlog'
             2878  LOAD_STR                 'learning_curve'
             2880  BINARY_SUBSCR    
             2882  LOAD_FAST                '_gui'
             2884  STORE_ATTR               learnmat

 L. 901      2886  LOAD_DEREF               'self'
             2888  LOAD_ATTR                linestyle
             2890  LOAD_FAST                '_gui'
             2892  STORE_ATTR               linestyle

 L. 902      2894  LOAD_DEREF               'self'
             2896  LOAD_ATTR                fontstyle
             2898  LOAD_FAST                '_gui'
             2900  STORE_ATTR               fontstyle

 L. 903      2902  LOAD_FAST                '_gui'
             2904  LOAD_METHOD              setupGUI
             2906  LOAD_FAST                '_viewmllearnmat'
             2908  CALL_METHOD_1         1  '1 positional argument'
             2910  POP_TOP          

 L. 904      2912  LOAD_FAST                '_viewmllearnmat'
             2914  LOAD_METHOD              exec
             2916  CALL_METHOD_0         0  '0 positional arguments'
             2918  POP_TOP          

 L. 905      2920  LOAD_FAST                '_viewmllearnmat'
             2922  LOAD_METHOD              show
             2924  CALL_METHOD_0         0  '0 positional arguments'
             2926  POP_TOP          
           2928_0  COME_FROM          2858  '2858'

Parse error at or near `POP_TOP' instruction at offset 2926

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
    TrainMl2DDcnnFromExisting = QtWidgets.QWidget()
    gui = trainml2ddcnnfromexisting()
    gui.setupGUI(TrainMl2DDcnnFromExisting)
    TrainMl2DDcnnFromExisting.show()
    sys.exit(app.exec_())