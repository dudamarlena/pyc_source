# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\viewmlmlp.py
# Compiled at: 2019-12-16 00:14:23
# Size of source mod 2**32: 17061 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.ml.tfmodel as ml_tfm
import cognitivegeo.src.gui.viewmllearnmat as gui_viewmllearnmat
import cognitivegeo.src.gui.plotmllearncurve as gui_plotmllearncurve
import cognitivegeo.src.vis.messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class viewmlmlp(object):
    rootpath = ''
    linestyle = core_set.Visual['Line']
    fontstyle = core_set.Visual['Font']
    iconpath = os.path.dirname(__file__)
    dialog = None
    modelpath = ''
    modelname = ''
    modelinfo = None

    def setupGUI(self, ViewMlMlp):
        ViewMlMlp.setObjectName('ViewMlMlp')
        ViewMlMlp.setFixedSize(810, 410)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ViewMlMlp.setWindowIcon(icon)
        self.lblfrom = QtWidgets.QLabel(ViewMlMlp)
        self.lblfrom.setObjectName('lblfrom')
        self.lblfrom.setGeometry(QtCore.QRect(10, 10, 100, 30))
        self.ldtfrom = QtWidgets.QLineEdit(ViewMlMlp)
        self.ldtfrom.setObjectName('ldtfrom')
        self.ldtfrom.setGeometry(QtCore.QRect(110, 10, 210, 30))
        self.btnfrom = QtWidgets.QPushButton(ViewMlMlp)
        self.btnfrom.setObjectName('btnfrom')
        self.btnfrom.setGeometry(QtCore.QRect(330, 10, 60, 30))
        self.lblfeature = QtWidgets.QLabel(ViewMlMlp)
        self.lblfeature.setObjectName('lblfeature')
        self.lblfeature.setGeometry(QtCore.QRect(10, 60, 100, 30))
        self.lwgfeature = QtWidgets.QListWidget(ViewMlMlp)
        self.lwgfeature.setObjectName('lwgfeature')
        self.lwgfeature.setGeometry(QtCore.QRect(110, 60, 280, 200))
        self.lwgfeature.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lbllength = QtWidgets.QLabel(ViewMlMlp)
        self.lbllength.setObjectName('lbllength')
        self.lbllength.setGeometry(QtCore.QRect(110, 270, 50, 30))
        self.ldtlength = QtWidgets.QLineEdit(ViewMlMlp)
        self.ldtlength.setObjectName('ldtlength')
        self.ldtlength.setGeometry(QtCore.QRect(160, 270, 40, 30))
        self.lbltotal = QtWidgets.QLabel(ViewMlMlp)
        self.lbltotal.setObjectName('lbltotal')
        self.lbltotal.setGeometry(QtCore.QRect(300, 270, 50, 30))
        self.ldttotal = QtWidgets.QLineEdit(ViewMlMlp)
        self.ldttotal.setObjectName('ldttotal')
        self.ldttotal.setGeometry(QtCore.QRect(350, 270, 40, 30))
        self.lbltarget = QtWidgets.QLabel(ViewMlMlp)
        self.lbltarget.setObjectName('lbltarget')
        self.lbltarget.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.cbbtarget = QtWidgets.QComboBox(ViewMlMlp)
        self.cbbtarget.setObjectName('cbbtarget')
        self.cbbtarget.setGeometry(QtCore.QRect(110, 310, 280, 30))
        self.lblnetwork = QtWidgets.QLabel(ViewMlMlp)
        self.lblnetwork.setObjectName('lblnetwork')
        self.lblnetwork.setGeometry(QtCore.QRect(410, 60, 190, 30))
        self.lblnlayer = QtWidgets.QLabel(ViewMlMlp)
        self.lblnlayer.setObjectName('lblnlayer')
        self.lblnlayer.setGeometry(QtCore.QRect(410, 100, 130, 30))
        self.ldtnlayer = QtWidgets.QLineEdit(ViewMlMlp)
        self.ldtnlayer.setObjectName('ldtnlayer')
        self.ldtnlayer.setGeometry(QtCore.QRect(550, 100, 40, 30))
        self.twgnlayer = QtWidgets.QTableWidget(ViewMlMlp)
        self.twgnlayer.setObjectName('twgnlayer')
        self.twgnlayer.setGeometry(QtCore.QRect(610, 100, 180, 240))
        self.twgnlayer.setColumnCount(2)
        self.twgnlayer.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgnlayer.verticalHeader().hide()
        self.lblpara = QtWidgets.QLabel(ViewMlMlp)
        self.lblpara.setObjectName('lblpara')
        self.lblpara.setGeometry(QtCore.QRect(410, 150, 190, 30))
        self.lblnepoch = QtWidgets.QLabel(ViewMlMlp)
        self.lblnepoch.setObjectName('lblnepoch')
        self.lblnepoch.setGeometry(QtCore.QRect(410, 190, 130, 30))
        self.ldtnepoch = QtWidgets.QLineEdit(ViewMlMlp)
        self.ldtnepoch.setObjectName('ldtnepoch')
        self.ldtnepoch.setGeometry(QtCore.QRect(550, 190, 40, 30))
        self.lblbatchsize = QtWidgets.QLabel(ViewMlMlp)
        self.lblbatchsize.setObjectName('lblbatchsize')
        self.lblbatchsize.setGeometry(QtCore.QRect(410, 230, 130, 30))
        self.ldtbatchsize = QtWidgets.QLineEdit(ViewMlMlp)
        self.ldtbatchsize.setObjectName('ldtbatchsize')
        self.ldtbatchsize.setGeometry(QtCore.QRect(550, 230, 40, 30))
        self.lbllearnrate = QtWidgets.QLabel(ViewMlMlp)
        self.lbllearnrate.setObjectName('lbllearnrate')
        self.lbllearnrate.setGeometry(QtCore.QRect(410, 270, 130, 30))
        self.ldtlearnrate = QtWidgets.QLineEdit(ViewMlMlp)
        self.ldtlearnrate.setObjectName('ldtlearnrate')
        self.ldtlearnrate.setGeometry(QtCore.QRect(550, 270, 40, 30))
        self.lblfcdropout = QtWidgets.QLabel(ViewMlMlp)
        self.lblfcdropout.setObjectName('lblfcdropout')
        self.lblfcdropout.setGeometry(QtCore.QRect(410, 310, 130, 30))
        self.ldtfcdropout = QtWidgets.QLineEdit(ViewMlMlp)
        self.ldtfcdropout.setObjectName('ldtfcdropout')
        self.ldtfcdropout.setGeometry(QtCore.QRect(550, 310, 40, 30))
        self.btnviewlc = QtWidgets.QPushButton(ViewMlMlp)
        self.btnviewlc.setObjectName('btnviewlc')
        self.btnviewlc.setGeometry(QtCore.QRect(220, 360, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/matrix.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnviewlc.setIcon(icon)
        self.btnplotlc = QtWidgets.QPushButton(ViewMlMlp)
        self.btnplotlc.setObjectName('btnplotlc')
        self.btnplotlc.setGeometry(QtCore.QRect(430, 360, 160, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/plotcurve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnplotlc.setIcon(icon)
        self.msgbox = QtWidgets.QMessageBox(ViewMlMlp)
        self.msgbox.setObjectName('msgbox')
        _center_x = ViewMlMlp.geometry().center().x()
        _center_y = ViewMlMlp.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(ViewMlMlp)
        QtCore.QMetaObject.connectSlotsByName(ViewMlMlp)

    def retranslateGUI(self, ViewMlMlp):
        self.dialog = ViewMlMlp
        _translate = QtCore.QCoreApplication.translate
        ViewMlMlp.setWindowTitle(_translate('ViewMlMlp', 'View MLP'))
        self.lblfrom.setText(_translate('ViewMlMlp', 'Select network:'))
        self.ldtfrom.setText(_translate('ViewMlMlp', ''))
        self.ldtfrom.textChanged.connect(self.changeLdtFrom)
        self.btnfrom.setText(_translate('ViewMlMlp', 'Browse'))
        self.btnfrom.clicked.connect(self.clickBtnFrom)
        self.lblfeature.setText(_translate('ViewMlMlp', 'Training features:'))
        self.lbllength.setText(_translate('ViewMlMlp', 'length ='))
        self.ldtlength.setText(_translate('ViewMlMlp', ''))
        self.ldtlength.setEnabled(False)
        self.ldtlength.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltotal.setText(_translate('ViewMlMlp', 'total ='))
        self.ldttotal.setText(_translate('ViewMlMlp', ''))
        self.ldttotal.setEnabled(False)
        self.ldttotal.setAlignment(QtCore.Qt.AlignCenter)
        self.lbltarget.setText(_translate('ViewMlMlp', 'Training target:'))
        self.lwgfeature.itemSelectionChanged.connect(self.changeLwgFeature)
        self.lblnetwork.setText(_translate('ViewMlMlp', 'Pre-trained MLP architecture:'))
        self.lblnlayer.setText(_translate('ViewMlMlp', 'No. of MLP layers:'))
        self.lblnlayer.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnlayer.setText(_translate('ViewMlMlp', ''))
        self.ldtnlayer.setEnabled(False)
        self.ldtnlayer.setAlignment(QtCore.Qt.AlignCenter)
        self.ldtnlayer.textChanged.connect(self.changeLdtNlayer)
        self.twgnlayer.setHorizontalHeaderLabels(['MLP ID', 'No. of neuron'])
        self.lblpara.setText(_translate('ViewMlMlp', 'Pre-training parameters:'))
        self.lblnepoch.setText(_translate('ViewMlMlp', 'No. of epochs:'))
        self.lblnepoch.setAlignment(QtCore.Qt.AlignRight)
        self.ldtnepoch.setText(_translate('ViewMlMlp', ''))
        self.ldtnepoch.setEnabled(False)
        self.ldtnepoch.setAlignment(QtCore.Qt.AlignCenter)
        self.lblbatchsize.setText(_translate('ViewMlMlp', 'Batch size:'))
        self.lblbatchsize.setAlignment(QtCore.Qt.AlignRight)
        self.ldtbatchsize.setText(_translate('ViewMlMlp', ''))
        self.ldtbatchsize.setEnabled(False)
        self.ldtbatchsize.setAlignment(QtCore.Qt.AlignCenter)
        self.lbllearnrate.setText(_translate('ViewMlMlp', 'Learning rate:'))
        self.lbllearnrate.setAlignment(QtCore.Qt.AlignRight)
        self.ldtlearnrate.setText(_translate('ViewMlMlp', ''))
        self.ldtlearnrate.setEnabled(False)
        self.ldtlearnrate.setAlignment(QtCore.Qt.AlignCenter)
        self.lblfcdropout.setText(_translate('ViewMlMlp', 'MLP dropout rate:'))
        self.lblfcdropout.setAlignment(QtCore.Qt.AlignRight)
        self.ldtfcdropout.setText(_translate('ViewMlMlp', ''))
        self.ldtfcdropout.setEnabled(False)
        self.ldtfcdropout.setAlignment(QtCore.Qt.AlignCenter)
        self.btnviewlc.setText(_translate('ViewMlMlp', 'View Learning Matrix'))
        self.btnviewlc.clicked.connect(self.clickBtnViewLc)
        self.btnplotlc.setText(_translate('ViewMlMlp', 'Plot Learning Curve'))
        self.btnplotlc.clicked.connect(self.clickBtnPlotLc)
        self.btnplotlc.setDefault(True)

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
            _len = self.modelinfo['feature_length'][0]
            self.ldtlength.setText(str(_len))
            self.ldttotal.setText(str(self.modelinfo['number_feature']))
            self.cbbtarget.clear()
            self.cbbtarget.addItem(self.modelinfo['target'])
            self.ldtnlayer.setText(str(self.modelinfo['number_layer']))
            self.ldtnepoch.setText(str(self.modelinfo['number_epoch']))
            self.ldtbatchsize.setText(str(self.modelinfo['batch_size']))
            self.ldtlearnrate.setText(str(self.modelinfo['learning_rate']))
            self.ldtfcdropout.setText(str(self.modelinfo['dropout_prob_fc_layer']))
        else:
            self.modelpath = ''
            self.modelname = ''
            self.modelinfo = None
            self.lwgfeature.clear()
            self.ldtlength.setText('')
            self.ldttotal.setText('')
            self.cbbtarget.clear()
            self.ldtnlayer.setText('')
            self.ldtnepoch.setText('')
            self.ldtbatchsize.setText('')
            self.ldtlearnrate.setText('')
            self.ldtfcdropout.setText('')

    def changeLwgFeature(self):
        if ml_tfm.checkFNNModel(self.modelpath, self.modelname):
            _len = self.modelinfo['feature_length'][self.lwgfeature.currentIndex().row()]
            self.ldtlength.setText(str(_len))

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

    def clickBtnViewLc(self):
        self.refreshMsgBox()
        if ml_tfm.checkFNNModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in ViewMlMlp: No MLP network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'View MLP', 'No MLP network found')
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
        if ml_tfm.checkFNNModel(self.modelpath, self.modelname) is False:
            vis_msg.print('ERROR in ViewMlMlp: No MLP network found', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'View MLP', 'No MLP network found')
            return
        _plotmllearncurve = QtWidgets.QDialog()
        _gui = gui_plotmllearncurve()
        _gui.learnmat = self.modelinfo['learning_curve']
        _gui.linestyle = self.linestyle
        _gui.fontstyle = self.fontstyle
        _gui.setupGUI(_plotmllearncurve)
        _plotmllearncurve.exec()
        _plotmllearncurve.show()

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ViewMlMlp = QtWidgets.QWidget()
    gui = viewmlmlp()
    gui.setupGUI(ViewMlMlp)
    ViewMlMlp.show()
    sys.exit(app.exec_())