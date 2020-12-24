# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\applymlmlp4pred.py
# Compiled at: 2019-12-15 21:49:30
# Size of source mod 2**32: 27195 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.basic.data import data as basic_data
from cognitivegeo.src.seismic.analysis import analysis as seis_ays
from cognitivegeo.src.vis.messager import messager as vis_msg
from cognitivegeo.src.ml.tfmodel import tfmodel as ml_tfm
from cognitivegeo.src.ml.fnnclassifier import fnnclassifier as ml_fnn
from cognitivegeo.src.gui.viewmlmlp import viewmlmlp as gui_viewmlmlp
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class applymlmlp4pred(object):
    survinfo = {}
    seisdata = {}
    rootpath = ''
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    iconpath = os.path.dirname(__file__)
    dialog = None
    modelpath = ''
    modelname = ''
    modelinfo = None

    def setupGUI(self, ApplyMlMlp4Pred):
        ApplyMlMlp4Pred.setObjectName('ApplyMlMlp4Pred')
        ApplyMlMlp4Pred.setFixedSize(810, 470)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ApplyMlMlp4Pred.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ApplyMlMlp4Pred)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ApplyMlMlp4Pred)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 160))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lblpatchsize = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblpatchsize.setObjectName('lblpatchsize')
        self.lblpatchsize.setGeometry(QtCore.QRect(10, 230, 80, 30))
        self.lblpatchheight = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblpatchheight.setObjectName('lblpatchheight')
        self.lblpatchheight.setGeometry(QtCore.QRect(110, 230, 50, 30))
        self.ldtpatchheight = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtpatchheight.setObjectName('ldtpatchheight')
        self.ldtpatchheight.setGeometry(QtCore.QRect(160, 230, 40, 30))
        self.lblpatchwidth = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblpatchwidth.setObjectName('lblpatchwidth')
        self.lblpatchwidth.setGeometry(QtCore.QRect(205, 230, 50, 30))
        self.ldtpatchwidth = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtpatchwidth.setObjectName('ldtpatchwidth')
        self.ldtpatchwidth.setGeometry(QtCore.QRect(255, 230, 40, 30))
        self.lblpatchdepth = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblpatchdepth.setObjectName('lblpatchdepth')
        self.lblpatchdepth.setGeometry(QtCore.QRect(300, 230, 50, 30))
        self.ldtpatchdepth = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtpatchdepth.setObjectName('ldtpatchdepth')
        self.ldtpatchdepth.setGeometry(QtCore.QRect(350, 230, 40, 30))
        self.lblold = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblold.setObjectName('lblold')
        self.lblold.setGeometry(QtCore.QRect(50, 270, 60, 30))
        self.lbloldlength = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lbloldlength.setObjectName('lbloldlength')
        self.lbloldlength.setGeometry(QtCore.QRect(110, 270, 50, 30))
        self.ldtoldlength = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtoldlength.setObjectName('ldtoldlength')
        self.ldtoldlength.setGeometry(QtCore.QRect(160, 270, 40, 30))
        self.lbloldtotal = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lbloldtotal.setObjectName('lbloldtotal')
        self.lbloldtotal.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldtoldtotal = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtoldtotal.setObjectName('ldtoldtotal')
        self.ldtoldtotal.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lblnew = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblnew.setObjectName('lblnew')
        self.lblnew.setGeometry(QtCore.QRect(50, 310, 60, 30))
        self.lblnewlength = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblnewlength.setObjectName('lblnewlength')
        self.lblnewlength.setGeometry(QtCore.QRect(110, 310, 50, 30))
        self.ldtnewlength = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtnewlength.setObjectName('ldtnewlength')
        self.ldtnewlength.setGeometry(QtCore.QRect(160, 310, 40, 30))
        self.lblnewtotal = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblnewtotal.setObjectName('lblnewtotal')
        self.lblnewtotal.setGeometry(QtCore.QRect(300, 310, 50, 30))
        self.ldtnewtotal = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtnewtotal.setObjectName('ldtnewtotal')
        self.ldtnewtotal.setGeometry(QtCore.QRect(350, 310, 40, 30))
        self.lblnetwork = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.btnviewnetwork = QtWidgets.QPushButton(ApplyMlMlp4Pred)
        self.btnviewnetwork.setObjectName('btnviewnetwork')
        self.btnviewnetwork.setGeometry(QtCore.QRect(710, 60, 80, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewnetwork.setIcon(icon)
        self.lblnlayer = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblnlayer.setObjectName('lblnlayer')
        self.lblnlayer.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnlayer = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtnlayer.setObjectName('ldtnlayer')
        self.ldtnlayer.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnlayer = QtWidgets.QTableWidget(ApplyMlMlp4Pred)
        self.twgnlayer.setObjectName('twgnlayer')
        self.twgnlayer.setGeometry(QtCore.QRect(610, 100, 180, 160))
        self.twgnlayer.setColumnCount(2)
        self.twgnlayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnlayer.verticalHeader().hide()
        self.lblpara = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(410, 270, 100, 30))
        self.lblbatchsize = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(410, 310, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(550, 310, 40, 30))
        self.lblsave = QtWidgets.QLabel(ApplyMlMlp4Pred)
        self.lblsave.setObjectName('lblsave')
        self.lblsave.setGeometry(QtCore.QRect(410, 360, 130, 30))
        self.ldtsave = QtWidgets.QLineEdit(ApplyMlMlp4Pred)
        self.ldtsave.setObjectName('ldtsave')
        self.ldtsave.setGeometry(QtCore.QRect(550, 360, 40, 30))
        self.btnapply = QtWidgets.QPushButton(ApplyMlMlp4Pred)
        self.btnapply.setObjectName('btnapply')
        self.btnapply.setGeometry(QtCore.QRect(320, 410, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnapply.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ApplyMlMlp4Pred)
        self.msgbox.setObjectName('msgbox')
        _center_x = ApplyMlMlp4Pred.geometry().center().x()
        _center_y = ApplyMlMlp4Pred.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ApplyMlMlp4Pred)
        QtCore.QMetaObject.connectSlotsByName(ApplyMlMlp4Pred)

    def retranslateGUI(self, ApplyMlMlp4Pred):
        self.dialog = ApplyMlMlp4Pred
        _translate = QtCore.QCoreApplication.translate
        ApplyMlMlp4Pred.setWindowTitle(_translate('ApplyMlMlp4Pred', 'Apply MLP for prediction'))
        self.lblfrom.setText(_translate('ApplyMlMlp4Pred', 'Select network:'))
        self.ldtfrom.setText(_translate('ApplyMlMlp4Pred', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ApplyMlMlp4Pred', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ApplyMlMlp4Pred', 'Training features:'))
        self.lblpatchsize.setText(_translate('ApplyMlMlp4Pred', 'Patch\nsize:'))
        self.lblpatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.lblpatchheight.setText(_translate('ApplyMlMlp4Pred', 'height=\ntime/depth'))
        self.ldtpatchheight.setText(_translate('ApplyMlMlp4Pred', '1'))
        self.ldtpatchheight.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpatchwidth.setText(_translate('ApplyMlMlp4Pred', 'width=\ncrossline'))
        self.ldtpatchwidth.setText(_translate('ApplyMlMlp4Pred', '1'))
        self.ldtpatchwidth.setAlignment(QtCore.Qt.AlignCenter)
        self.lblpatchdepth.setText(_translate('ApplyMlMlp4Pred', 'depth=\ninline'))
        self.ldtpatchdepth.setText(_translate('ApplyMlMlp4Pred', '1'))
        self.ldtpatchdepth.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtpatchheight.textChanged.connect(self.changeLdtPatchSize)
        self.ldtpatchwidth.textChanged.connect(self.changeLdtPatchSize)
        self.ldtpatchdepth.textChanged.connect(self.changeLdtPatchSize)
        self.lblold.setText(_translate('ApplyMlMlp4Pred', 'available:'))
        self.lbloldlength.setText(_translate('ApplyMlMlp4Pred', 'length ='))
        self.ldtoldlength.setText(_translate('ApplyMlMlp4Pred', ''))
        self.ldtoldlength.setEnabled(False)
        self.ldtoldlength.setAlignment(QtCore.Qt.AlignCenter)
        self.lbloldtotal.setText(_translate('ApplyMlMlp4Pred', 'total ='))
        self.ldtoldtotal.setText(_translate('ApplyMlMlp4Pred', ''))
        self.ldtoldtotal.setEnabled(False)
        self.ldtoldtotal.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnew.setText(_translate('ApplyMlMlp4Pred', 'expected:'))
        self.lblnewlength.setText(_translate('ApplyMlMlp4Pred', 'length ='))
        self.ldtnewlength.setText(_translate('ApplyMlMlp4Pred', ''))
        self.ldtnewlength.setEnabled(False)
        self.ldtnewlength.setAlignment(QtCore.Qt.AlignCenter)
        self.lblnewtotal.setText(_translate('ApplyMlMlp4Pred', 'total ='))
        self.ldtnewtotal.setText(_translate('ApplyMlMlp4Pred', ''))
        self.ldtnewtotal.setEnabled(False)
        self.ldtnewtotal.setAlignment(QtCore.Qt.AlignCenter)
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblnetwork.setText(_translate('ApplyMlMlp4Pred', 'Pre-trained MLP architecture:'))
        self.btnviewnetwork.setText(_translate('ApplyMlMlp4Pred', 'View'))
        self.btnviewnetwork.setEnabled(False)
        self.btnviewnetwork.clicked.connect(self.clickBtnViewNetwork)
        self.lblnlayer.setText(_translate('ApplyMlMlp4Pred', 'No. of MLP layers:'))
        self.lblnlayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnlayer.setText(_translate('ApplyMlMlp4Pred', ''))
        self.ldtnlayer.setEnabled(False)
        self.ldtnlayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnlayer.textChanged.connect(self.changeLdtNlayer)
        self.twgnlayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblpara.setText(_translate('ApplyMlMlp4Pred', 'Key parameters:'))
        self.lblbatchsize.setText(_translate('ApplyMlMlp4Pred', 'Batch size='))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ApplyMlMlp4Pred', '10000'))
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lblsave.setText(_translate('ApplyMlMlp4Pred', 'Output name='))
        self.lblsave.setAlignment(QtCore.Qt.AlignRight)
        self.ldtsave.setText(_translate('ApplyMlMlp4Pred', 'mlp'))
        self.ldtsave.setAlignment(QtCore.Qt.AlignCenter)
        self.btnapply.setText(_translate('ApplyMlMlp4Pred', 'Apply MLP'))
        self.btnapply.setDefault(True)
        self.btnapply.clicked.connect(self.clickBtnApplyMlMlp4Pred)

    def clickBtnFrom(self):
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select MLP Network', (self.rootpath), filter='Tensorflow network files (*.meta);; All files (*.*)')
        if len(_file[0]) > 0:
            self.ldtfrom.setText(_file[0])

    def changeLdtFrom(self):
        self.refreshMsgBox()
        if os.path.exists(self.ldtfrom.text()):
            self.modelpath = os.path.dirname(self.ldtfrom.text())
            self.modelname = os.path.splitext(os.path.basename(self.ldtfrom.text()))[0]
        else:
            self.modelpath = ''
            self.modelname = ''
        if ml_tfm.checkFNNModel(self.modelpath, self.modelname) is True:
            self.modelinfo = ml_tfm.getModelInfo(self.modelpath, self.modelname)
            self.lwgfeature.clear()
            _featurelist = self.modelinfo['feature_list']
            _firstfeature = None
            for f in _featurelist:
                item = QtWidgets.QListWidgetItem(self.lwgfeature)
                item.setText(f)
                self.lwgfeature.addItem(item)
                if _firstfeature is None:
                    _firstfeature = item

            self.lwgfeature.setCurrentItem(_firstfeature)
            _len = self.getFeatureLength(_firstfeature.text())
            self.ldtoldlength.setText(str(_len))
            _len = self.modelinfo['feature_length'][0]
            self.ldtnewlength.setText(str(_len))
            _len = self.getTotalFeatureLength(_featurelist)
            self.ldtoldtotal.setText(str(_len))
            self.ldtnewtotal.setText(str(self.modelinfo['number_feature']))
            self.btnviewnetwork.setEnabled(True)
            self.ldtnlayer.setText(str(self.modelinfo['number_layer']))
        else:
            self.modelpath = ''
            self.modelname = ''
            self.modelinfo = None
            self.lwgfeature.clear()
            self.ldtoldlength.setText('')
            self.ldtoldtotal.setText('')
            self.ldtnewlength.setText('')
            self.ldtnewtotal.setText('')
            self.btnviewnetwork.setEnabled(False)
            self.ldtnlayer.setText('')

    def changeLwgFeature(self):
        if ml_tfm.checkFNNModel(self.modelpath, self.modelname):
            _len = self.getFeatureLength(self.lwgfeature.currentItem().text())
            self.ldtoldlength.setText(str(_len))
            _len = self.modelinfo['feature_length'][self.lwgfeature.currentIndex().row()]
            self.ldtnewlength.setText(str(_len))

    def changeLdtPatchSize(self):
        if ml_tfm.checkFNNModel(self.modelpath, self.modelname):
            _len = self.getFeatureLength(self.lwgfeature.currentItem().text())
            self.ldtoldlength.setText(str(_len))
            _len = self.getTotalFeatureLength(self.modelinfo['feature_list'])
            self.ldtoldtotal.setText(str(_len))

    def changeLdtNlayer(self):
        if ml_tfm.checkFNNModel(self.modelpath, self.modelname) is True:
            _nlayer = self.modelinfo['number_layer']
            self.twgnlayer.setRowCount(_nlayer)
            for _idx in range(_nlayer):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(_idx + 1))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnlayer.setItem(_idx, 0, item)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.modelinfo['number_neuron'][_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.ItemIsEditable)
                self.twgnlayer.setItem(_idx, 1, item)

        else:
            self.twgnlayer.setRowCount(0)

    def clickBtnViewNetwork(self):
        _viewmlmlp = QtWidgets.QDialog()
        _gui = gui_viewmlmlp()
        _gui.linestyle = self.linestyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_viewmlmlp)
        _gui.ldtfrom.setText(self.ldtfrom.text())
        _viewmlmlp.exec()
        _viewmlmlp.show()

    def clickBtnApplyMlMlp4Pred(self):
        self.refreshMsgBox()
        if self.checkSurvInfo() is False:
            vis_msg.print('ERROR in ApplyMlMlp4Pred: No seismic survey available', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Apply MLP', 'No seismic survey available')
            return
        if ml_tfm.checkFNNModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in ApplyMlMlp4Pred: No MLP network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Apply MLP', 'No MLP network found')
            return
        _featurelist = self.modelinfo['feature_list']
        for f in _featurelist:
            if self.checkSeisData(f) is False:
                vis_msg.print(("ERROR in ApplyMlMlp4Pred: Feature '%s' not found in seismic data" % f), type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Apply MLP', "Feature '" + f + "' not found in seismic data")
                return

        if self.ldtoldlength.text() != self.ldtnewlength.text() or self.ldtoldtotal.text() != self.ldtnewtotal.text():
            vis_msg.print('ERROR in ApplyMlMlp4Pred: Feature length not match', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Apply MLP', 'Feature length not match')
            return
        _patch_height = basic_data.str2int(self.ldtpatchheight.text())
        _patch_width = basic_data.str2int(self.ldtpatchwidth.text())
        _patch_depth = basic_data.str2int(self.ldtpatchdepth.text())
        if _patch_height is False or _patch_width is False or _patch_depth is False or _patch_height < 1 or _patch_width < 1 or _patch_depth < 1:
            vis_msg.print('ERROR in ApplyMlMlp4Pred: Non-positive feature size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Apply MLP', 'Non-positive feature size')
            return
        _batch = basic_data.str2int(self.ldtbatchsize.text())
        if _batch is False or _batch < 1:
            vis_msg.print('ERROR in ApplyMlMlp4Pred: Non-positive batch size', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Apply MLP', 'Non-positive batch size')
            return
        if len(self.ldtsave.text()) < 1:
            vis_msg.print('ERROR in ApplyMlMlp4Pred: No name specified', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Apply MLP', 'No name specified')
            return
        if self.ldtsave.text() in self.seisdata.keys():
            if self.checkSeisData(self.ldtsave.text()):
                reply = QtWidgets.QMessageBox.question(self.msgbox, 'Apply MLP', self.ldtsave.text() + ' already exists. Overwrite?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    return
        _patch_height = 2 * int(_patch_height / 2) + 1
        _patch_width = 2 * int(_patch_width / 2) + 1
        _patch_depth = 2 * int(_patch_depth / 2) + 1
        _nsample = np.shape(self.seisdata[_featurelist[0]])[0]
        _nloop = int(np.ceil(_nsample / _batch))
        _pgsdlg = QtWidgets.QProgressDialog()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/apply.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        _pgsdlg.setWindowIcon(icon)
        _pgsdlg.setWindowTitle('Apply MLP')
        _pgsdlg.setCancelButton(None)
        _pgsdlg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        _pgsdlg.forceShow()
        _pgsdlg.setFixedWidth(400)
        _pgsdlg.setMaximum(_nloop)
        _wdinl = int(_patch_depth / 2)
        _wdxl = int(_patch_width / 2)
        _wdz = int(_patch_height / 2)
        _seisdata = seis_ays.convertSeisInfoTo2DMat(self.survinfo)
        _result = np.zeros([_nsample, 1])
        idxstart = 0
        for i in range(_nloop):
            QtCore.QCoreApplication.instance().processEvents()
            sys.stdout.write('\r>>> Apply MLP, proceeding %.1f%% ' % (float(i) / float(_nloop) * 100.0))
            sys.stdout.flush()
            idxend = idxstart + _batch
            if idxend > _nsample:
                idxend = _nsample
            idxlist = np.linspace(idxstart, idxend - 1, idxend - idxstart).astype(int)
            idxstart = idxend
            _targetdata = _seisdata[idxlist, 0:3]
            _dict = {}
            for f in _featurelist:
                _data = self.seisdata[f]
                _dict[f] = seis_ays.retrieveSeisWindowFrom3DMat(_data, _targetdata, seisinfo=(self.survinfo), wdinl=_wdinl,
                  wdxl=_wdxl,
                  wdz=_wdz,
                  verbose=False)[:, 3:]

            _result[idxlist, 0:1] = ml_fnn.predictionFromFNNClassifier(_dict, fnnpath=(self.modelpath),
              fnnname=(self.modelname),
              batchsize=_batch,
              verbose=True)
            _pgsdlg.setValue(i + 1)

        print('Done')
        self.seisdata[self.ldtsave.text()] = np.transpose(np.reshape(_result, [
         self.survinfo['ILNum'], self.survinfo['XLNum'],
         self.survinfo['ZNum']]), [
         2, 1, 0])
        QtWidgets.QMessageBox.information(self.msgbox, 'Apply MLP', 'MLP applied successfully')

    def getTotalFeatureLength(self, featurelist):
        _len = 0
        for f in featurelist:
            if self.checkSurvInfo() and f in self.seisdata.keys() and self.checkSeisData(f):
                _len = _len + self.getFeatureLength(f)

        return _len

    def getFeatureLength(self, feature):
        _len = 0
        if self.checkSurvInfo():
            if feature in self.seisdata.keys():
                if self.checkSeisData(feature):
                    _dims = np.shape(self.seisdata[feature])[1:]
                    _len = 1
                    for i in _dims:
                        _len = _len * i

        _len = _len * basic_data.str2int(self.ldtpatchheight.text()) * basic_data.str2int(self.ldtpatchwidth.text()) * basic_data.str2int(self.ldtpatchdepth.text())
        return _len

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))

    def checkSurvInfo(self):
        self.refreshMsgBox()
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            return False
        else:
            return True

    def checkSeisData(self, f):
        self.refreshMsgBox()
        return seis_ays.isSeis3DMatConsistentWithSeisInfo(self.seisdata[f], self.survinfo)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ApplyMlMlp4Pred = QtWidgets.QWidget()
    gui = applymlmlp4pred()
    gui.setupGUI(ApplyMlMlp4Pred)
    ApplyMlMlp4Pred.show()
    sys.exit(app.exec_())