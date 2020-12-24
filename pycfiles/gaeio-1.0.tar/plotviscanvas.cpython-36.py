# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\HDi\Google Drive\ProgramCodes\PythonCodes\cognitivegeo\src\gui\plotviscanvas.py
# Compiled at: 2020-03-23 13:32:09
# Size of source mod 2**32: 53951 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys, numpy as np, vispy.io as vispy_io
from vispy import scene
from vispy.color import Colormap
from functools import partial
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
from cognitivegeo.src.basic.data import data as basic_data
from cognitivegeo.src.basic.matdict import matdict as basic_mdt
from cognitivegeo.src.core.settings import settings as core_set
from cognitivegeo.src.seismic.analysis import analysis as seis_ays
from cognitivegeo.src.pointset.analysis import analysis as pointset_ays
from cognitivegeo.src.vis.colormap import colormap as vis_cmap
from cognitivegeo.src.gui.manageseis import manageseis as gui_manageseis
from cognitivegeo.src.gui.configseisvis import configseisvis as gui_configseisvis
from cognitivegeo.src.gui.managepointset import managepointset as gui_managepointset
from cognitivegeo.src.gui.configpointsetvis import configpointsetvis as gui_configpointsetvis
from cognitivegeo.src.vis.messager import messager as vis_msg
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class plotviscanvas(object):
    survinfo = {}
    seisdata = {}
    pointsetdata = {}
    settings = core_set.Settings
    iconpath = os.path.dirname(__file__)
    dialog = None
    canvas = None
    view = None
    canvasproperties = {}
    canvascomponents = {}
    seisvisconfig = {}
    pointsetvisconfig = {}

    def setupGUI(self, PlotVisCanvas):
        PlotVisCanvas.setObjectName('PlotVisCanvas')
        PlotVisCanvas.setFixedSize(1400, 960)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/canvas.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PlotVisCanvas.setWindowIcon(icon)
        self.lblseisicon = QtWidgets.QLabel(PlotVisCanvas)
        self.lblseisicon.setObjectName('lblseisicon')
        self.lblseisicon.setGeometry(QtCore.QRect(10, 10, 30, 30))
        self.lblseisicon.setPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/seismic.png')).scaled(30, 30, QtCore.Qt.KeepAspectRatio))
        self.lblseis = QtWidgets.QLabel(PlotVisCanvas)
        self.lblseis.setObjectName('lblseis')
        self.lblseis.setGeometry(QtCore.QRect(50, 10, 50, 30))
        self.btnconfigseisvis = QtWidgets.QPushButton(PlotVisCanvas)
        self.btnconfigseisvis.setObjectName('btnconfigseisvis')
        self.btnconfigseisvis.setGeometry(QtCore.QRect(100, 10, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigseisvis.setIcon(icon)
        self.btnmanageseis = QtWidgets.QPushButton(PlotVisCanvas)
        self.btnmanageseis.setObjectName('btnmanageseis')
        self.btnmanageseis.setGeometry(QtCore.QRect(140, 10, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnmanageseis.setIcon(icon)
        self.cbblistseis = QtWidgets.QComboBox(PlotVisCanvas)
        self.cbblistseis.setObjectName('cbblistseis')
        self.cbblistseis.setGeometry(QtCore.QRect(10, 50, 240, 30))
        self.btnaddseis2canvas = QtWidgets.QPushButton(PlotVisCanvas)
        self.btnaddseis2canvas.setObjectName('btnaddseis2canvas')
        self.btnaddseis2canvas.setGeometry(QtCore.QRect(260, 50, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/add.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnaddseis2canvas.setIcon(icon)
        self.twgseisoncanvas = QtWidgets.QTableWidget(PlotVisCanvas)
        self.twgseisoncanvas.setObjectName('twgseisoncanvas')
        self.twgseisoncanvas.setGeometry(QtCore.QRect(10, 90, 280, 300))
        self.twgseisoncanvas.setColumnCount(5)
        self.twgseisoncanvas.setRowCount(0)
        self.twgseisoncanvas.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgseisoncanvas.horizontalHeader().hide()
        self.twgseisoncanvas.verticalHeader().hide()
        self.twgseisoncanvas.setColumnWidth(0, 18)
        self.twgseisoncanvas.setColumnWidth(1, 108)
        self.twgseisoncanvas.setColumnWidth(2, 60)
        self.twgseisoncanvas.setColumnWidth(3, 60)
        self.twgseisoncanvas.setColumnWidth(4, 30)
        self.lblpointseticon = QtWidgets.QLabel(PlotVisCanvas)
        self.lblpointseticon.setObjectName('lblpointseticon')
        self.lblpointseticon.setGeometry(QtCore.QRect(10, 410, 30, 30))
        self.lblpointseticon.setPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/point.png')).scaled(30, 30, QtCore.Qt.KeepAspectRatio))
        self.lblpointset = QtWidgets.QLabel(PlotVisCanvas)
        self.lblpointset.setObjectName('lblpointset')
        self.lblpointset.setGeometry(QtCore.QRect(50, 410, 50, 30))
        self.btnconfigpointsetvis = QtWidgets.QPushButton(PlotVisCanvas)
        self.btnconfigpointsetvis.setObjectName('btnconfigpointsetvis')
        self.btnconfigpointsetvis.setGeometry(QtCore.QRect(100, 410, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/view.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnconfigpointsetvis.setIcon(icon)
        self.btnmanagepointset = QtWidgets.QPushButton(PlotVisCanvas)
        self.btnmanagepointset.setObjectName('btnmanagepointset')
        self.btnmanagepointset.setGeometry(QtCore.QRect(140, 410, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnmanagepointset.setIcon(icon)
        self.cbblistpointset = QtWidgets.QComboBox(PlotVisCanvas)
        self.cbblistpointset.setObjectName('cbblistpointset')
        self.cbblistpointset.setGeometry(QtCore.QRect(10, 450, 240, 30))
        self.btnaddpointset2canvas = QtWidgets.QPushButton(PlotVisCanvas)
        self.btnaddpointset2canvas.setObjectName('btnaddpointset2canvas')
        self.btnaddpointset2canvas.setGeometry(QtCore.QRect(260, 450, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/add.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnaddpointset2canvas.setIcon(icon)
        self.twgpointsetoncanvas = QtWidgets.QTableWidget(PlotVisCanvas)
        self.twgpointsetoncanvas.setObjectName('twgpointsetoncanvas')
        self.twgpointsetoncanvas.setGeometry(QtCore.QRect(10, 490, 280, 100))
        self.twgpointsetoncanvas.setColumnCount(4)
        self.twgpointsetoncanvas.setRowCount(0)
        self.twgpointsetoncanvas.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.twgpointsetoncanvas.horizontalHeader().hide()
        self.twgpointsetoncanvas.verticalHeader().hide()
        self.twgpointsetoncanvas.setColumnWidth(0, 18)
        self.twgpointsetoncanvas.setColumnWidth(1, 108)
        self.twgpointsetoncanvas.setColumnWidth(2, 120)
        self.twgpointsetoncanvas.setColumnWidth(3, 30)
        self.wgtcanvas = QtWidgets.QWidget(PlotVisCanvas)
        self.wgtcanvas.setObjectName('wdtcanvas')
        self.wgtcanvas.setGeometry(QtCore.QRect(300, 50, 1050, 900))
        self.btnsrvbox = QtWidgets.QPushButton(PlotVisCanvas)
        self.btnsrvbox.setObjectName('btnsrvbox')
        self.btnsrvbox.setGeometry(QtCore.QRect(1360, 50, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/box.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnsrvbox.setIcon(icon)
        self.btnxyzaxis = QtWidgets.QPushButton(PlotVisCanvas)
        self.btnxyzaxis.setObjectName('btnxyzaxis')
        self.btnxyzaxis.setGeometry(QtCore.QRect(1360, 90, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/xyz.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnxyzaxis.setIcon(icon)
        self.btnsnapshot = QtWidgets.QPushButton(PlotVisCanvas)
        self.btnsnapshot.setObjectName('btnsnapshot')
        self.btnsnapshot.setGeometry(QtCore.QRect(1360, 130, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/camera.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnsnapshot.setIcon(icon)
        self.btngohome = QtWidgets.QPushButton(PlotVisCanvas)
        self.btngohome.setObjectName('btngohome')
        self.btngohome.setGeometry(QtCore.QRect(300, 10, 30, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/home.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btngohome.setIcon(icon)
        self.cbbviewfrom = QtWidgets.QComboBox(PlotVisCanvas)
        self.cbbviewfrom.setObjectName('cbbviewfrom')
        self.cbbviewfrom.setGeometry(QtCore.QRect(340, 10, 90, 30))
        self.ldtzscale = QtWidgets.QLineEdit(PlotVisCanvas)
        self.ldtzscale.setObjectName('ldtzscale')
        self.ldtzscale.setGeometry(QtCore.QRect(440, 10, 60, 30))
        self.ldtzscale.setAlignment(QtCore.Qt.AlignCenter)
        self.msgbox = QtWidgets.QMessageBox(PlotVisCanvas)
        self.msgbox.setObjectName('msgbox')
        _center_x = PlotVisCanvas.geometry().center().x()
        _center_y = PlotVisCanvas.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.retranslateGUI(PlotVisCanvas)
        QtCore.QMetaObject.connectSlotsByName(PlotVisCanvas)

    def retranslateGUI(self, PlotVisCanvas):
        self.dialog = PlotVisCanvas
        _translate = QtCore.QCoreApplication.translate
        PlotVisCanvas.setWindowTitle(_translate('PlotVisCanvas', 'Canvas'))
        self.lblseis.setText(_translate('PlotVisCanvas', 'Seismic:'))
        self.btnconfigseisvis.setText(_translate('PlotVisCanvas', ''))
        self.btnconfigseisvis.setToolTip('Visualization')
        self.btnconfigseisvis.clicked.connect(self.clickBtnConfigSeisVis)
        self.btnmanageseis.setText(_translate('PlotVisCanvas', ''))
        self.btnmanageseis.setToolTip('Manage')
        self.btnmanageseis.clicked.connect(self.clickBtnManageSeis)
        self.cbblistseis.addItems(list(self.seisdata.keys()))
        self.btnaddseis2canvas.setText(_translate('PlotVisCanvas', ''))
        self.btnaddseis2canvas.setToolTip('Add to canvas')
        self.btnaddseis2canvas.clicked.connect(self.clickBtnAddSeis2Canvas)
        self.lblpointset.setText(_translate('PlotVisCanvas', 'PointSet:'))
        self.btnconfigpointsetvis.setText(_translate('PlotVisCanvas', ''))
        self.btnconfigpointsetvis.setToolTip('Visualization')
        self.btnconfigpointsetvis.clicked.connect(self.clickBtnConfigPointSetVis)
        self.btnmanagepointset.setText(_translate('PlotVisCanvas', ''))
        self.btnmanagepointset.setToolTip('Manage')
        self.btnmanagepointset.clicked.connect(self.clickBtnManagePointSet)
        self.cbblistpointset.addItems(list(self.pointsetdata.keys()))
        self.btnaddpointset2canvas.setText(_translate('PlotVisCanvas', ''))
        self.btnaddpointset2canvas.setToolTip('Add to canvas')
        self.btnaddpointset2canvas.clicked.connect(self.clickBtnAddPointSet2Canvas)
        self.canvas = scene.SceneCanvas(keys='interactive', title='Canvas', bgcolor=[0.5, 0.5, 0.5], size=(1050,
                                                                                                           900),
          app='pyqt5',
          parent=(self.wgtcanvas))
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.TurntableCamera(elevation=30, azimuth=135)
        self.btnsrvbox.setText(_translate('PlotVisCanvas', ''))
        self.btnsrvbox.setToolTip('Survey box')
        self.btnsrvbox.setDefault(False)
        self.btnsrvbox.clicked.connect(self.clickBtnSrvBox)
        self.btnxyzaxis.setText(_translate('PlotVisCanvas', ''))
        self.btnxyzaxis.setToolTip('XYZ axis')
        self.btnxyzaxis.setDefault(False)
        self.btnxyzaxis.clicked.connect(self.clickBtnXYZAxis)
        self.btnsnapshot.setText(_translate('PlotVisCanvas', ''))
        self.btnsnapshot.setToolTip('Snapshot')
        self.btnsnapshot.setDefault(False)
        self.btnsnapshot.clicked.connect(self.clickBtnSnapshot)
        self.btngohome.setText(_translate('PlotVisCanvas', ''))
        self.btngohome.setDefault(True)
        self.btngohome.setToolTip('Home view')
        self.btngohome.clicked.connect(self.clickBtnGoHome)
        self.cbbviewfrom.addItems(['Inline', 'Crossline', 'Top'])
        self.cbbviewfrom.setItemIcon(0, QtGui.QIcon(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/visinl.png')).scaled(30, 30)))
        self.cbbviewfrom.setItemIcon(1, QtGui.QIcon(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/visxl.png')).scaled(30, 30)))
        self.cbbviewfrom.setItemIcon(2, QtGui.QIcon(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/visz.png')).scaled(30, 30)))
        self.cbbviewfrom.setCurrentIndex(0)
        self.cbbviewfrom.currentIndexChanged.connect(self.changeCbbViewFrom)
        self.ldtzscale.setText(_translate('PlotVisCanvas', '1.0'))
        self.ldtzscale.textChanged.connect(self.changeLdtZScale)
        self.initSeisVis()
        self.initPointSetVis()
        self.initCanvas()

    def initSeisVis(self):
        self.seisvisconfig = {}
        if len(self.seisdata.keys()) > 0:
            for seis in self.seisdata.keys():
                if self.checkSeisData(seis):
                    self.seisvisconfig[seis] = {}
                    self.seisvisconfig[seis]['Colormap'] = self.settings['Visual']['Image']['Colormap']
                    self.seisvisconfig[seis]['Flip'] = False
                    self.seisvisconfig[seis]['Opacity'] = '100%'
                    self.seisvisconfig[seis]['Interpolation'] = self.settings['Visual']['Image']['Interpolation']
                    self.seisvisconfig[seis]['Maximum'] = np.max(self.seisdata[seis])
                    self.seisvisconfig[seis]['Minimum'] = np.min(self.seisdata[seis])

    def initPointSetVis(self):
        self.pointsetvisconfig = {}
        if len(self.pointsetdata.keys()) > 0:
            for point in self.pointsetdata.keys():
                if self.checkPointSetData(point):
                    self.pointsetvisconfig[point] = {}
                    self.pointsetvisconfig[point]['Marker'] = '+'
                    self.pointsetvisconfig[point]['Color'] = self.settings['Visual']['Line']['Color']
                    self.pointsetvisconfig[point]['Size'] = self.settings['Visual']['Line']['MarkerSize']

    def initCanvas(self):
        self.canvasproperties['Seismic'] = []
        self.canvascomponents['Seismic'] = []
        self.canvasproperties['PointSet'] = []
        self.canvascomponents['PointSet'] = []
        self.canvasproperties['Survey_Box'] = False
        self.canvascomponents['Survey_Box'] = []
        self.canvasproperties['XYZ_Axis'] = False
        self.canvascomponents['XYZ_Axis'] = None
        self.canvasproperties['Z_Scale'] = 1.0
        self.canvascomponents['Survey_Box'] = self.createSrvBox()
        if len(self.canvascomponents['Survey_Box']) == 12:
            for _i in self.canvascomponents['Survey_Box']:
                _i.parent = self.view.scene

            self.canvasproperties['Survey_Box'] = True
        self.canvascomponents['XYZ_Axis'] = self.createXYZAxis()
        if self.canvascomponents['XYZ_Axis'] is not None:
            self.canvascomponents['XYZ_Axis'].parent = self.view.scene
            self.canvasproperties['XYZ_Axis'] = True
        _zscale = basic_data.str2float(self.ldtzscale.text())
        if _zscale is not False and _zscale > 0.0:
            self.canvasproperties['Z_Scale'] = _zscale
        self.setCameraRange()
        self.canvas.show()

    def clickBtnConfigSeisVis(self):
        _config = QtWidgets.QDialog()
        _gui = gui_configseisvis()
        _gui.seisvisconfig = self.seisvisconfig
        _gui.setupGUI(_config)
        _config.exec()
        self.seisvisconfig = _gui.seisvisconfig
        _config.show()
        for _i in range(len(self.canvascomponents['Seismic'])):
            self.canvascomponents['Seismic'][_i].parent = None
            _vis = self.createVisualSeis(self.canvasproperties['Seismic'][_i]['Name'], self.canvasproperties['Seismic'][_i]['Orientation'], self.canvasproperties['Seismic'][_i]['Number'])
            if self.canvasproperties['Seismic'][_i]['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['Seismic'][_i] = _vis

    def clickBtnManageSeis(self):
        _manage = QtWidgets.QDialog()
        _gui = gui_manageseis()
        _gui.pointsetdata = self.pointsetdata
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_manage)
        _manage.exec()
        self.seisdata = _gui.seisdata
        self.survinfo = _gui.survinfo
        _manage.show()
        self.cbblistseis.clear()
        self.cbblistseis.addItems(list(self.seisdata.keys()))
        _config = {}
        if len(self.seisdata.keys()) > 0:
            for _seis in self.seisdata.keys():
                if self.checkSeisData(_seis):
                    _config[_seis] = {}
                    if _seis in self.seisvisconfig.keys():
                        _config[_seis] = self.seisvisconfig[_seis]
                    else:
                        _config[_seis]['Colormap'] = self.settings['Visual']['Image']['Colormap']
                        _config[_seis]['Flip'] = False
                        _config[_seis]['Opacity'] = '100%'
                        _config[_seis]['Interpolation'] = self.settings['Visual']['Image']['Interpolation']
                        _config[_seis]['Maximum'] = np.max(self.seisdata[_seis])
                        _config[_seis]['Minimum'] = np.min(self.seisdata[_seis])

        self.seisvisconfig = _config
        _idx_pop = []
        for _idx in range(len(self.canvasproperties['Seismic'])):
            if self.canvasproperties['Seismic'][_idx]['Name'] not in self.seisdata.keys():
                _idx_pop.append(_idx)

        for _idx in range(len(_idx_pop)):
            self.canvasproperties['Seismic'].pop(_idx_pop[_idx] - _idx)
            self.canvascomponents['Seismic'][(_idx_pop[_idx] - _idx)].parent = None
            self.canvascomponents['Seismic'].pop(_idx_pop[_idx] - _idx)

        self.updateTwgSeisOnCanvas()

    def clickBtnAddSeis2Canvas(self):
        if len(self.seisdata.keys()) > 0 and self.checkSeisData(list(self.seisdata.keys())[self.cbblistseis.currentIndex()]):
            _seis = {}
            _seis['Visible'] = False
            _seis['Name'] = list(self.seisdata.keys())[self.cbblistseis.currentIndex()]
            _seis['Orientation'] = 'Inline'
            _seis['Number'] = self.survinfo['ILStart']
            _seis['Remove'] = False
            self.canvasproperties['Seismic'].append(_seis)
            _nseis = len(self.canvasproperties['Seismic'])
            self.twgseisoncanvas.setRowCount(_nseis)
            _item = QtWidgets.QCheckBox()
            _item.setChecked(_seis['Visible'])
            _item.stateChanged.connect(partial((self.changeCbxVisSeisOnCanvas), idx=(_nseis - 1)))
            self.twgseisoncanvas.setCellWidget(_nseis - 1, 0, _item)
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_seis['Name'])
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgseisoncanvas.setItem(_nseis - 1, 1, _item)
            _item = QtWidgets.QComboBox()
            _item.addItems(['Inline', 'Xline', 'Z'])
            _item.setCurrentIndex(list.index(['Inline', 'Crossline', 'Z'], _seis['Orientation']))
            _item.currentIndexChanged.connect(partial((self.changeCbbOrtSeisOnCanvas), idx=(_nseis - 1)))
            self.twgseisoncanvas.setCellWidget(_nseis - 1, 2, _item)
            _item = QtWidgets.QComboBox()
            _slices = []
            if _seis['Orientation'] == 'Inline':
                _slices = [str(_no) for _no in self.survinfo['ILRange']]
            if _seis['Orientation'] == 'Crossline':
                _slices = [str(_no) for _no in self.survinfo['XLRange']]
            if _seis['Orientation'] == 'Z':
                _slices = [str(_no) for _no in self.survinfo['ZRange']]
            _item.addItems(_slices)
            _item.setCurrentIndex(list.index(_slices, str(_seis['Number'])))
            _item.currentIndexChanged.connect(partial((self.changeCbbNoSeisOnCanvas), idx=(_nseis - 1)))
            self.twgseisoncanvas.setCellWidget(_nseis - 1, 3, _item)
            _item = QtWidgets.QPushButton()
            _icon = QtGui.QIcon()
            _icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/no.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            _item.setIcon(_icon)
            _item.clicked.connect(partial((self.clickBtnRmSeisOnCanvas), idx=(_nseis - 1)))
            self.twgseisoncanvas.setCellWidget(_nseis - 1, 4, _item)
            _vis = self.createVisualSeis(_seis['Name'], _seis['Orientation'], _seis['Number'])
            if _seis['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['Seismic'].append(_vis)

    def changeCbxVisSeisOnCanvas(self, idx):
        if idx < len(self.canvasproperties['Seismic']):
            self.canvasproperties['Seismic'][idx]['Visible'] = self.twgseisoncanvas.cellWidget(idx, 0).isChecked()
            if self.twgseisoncanvas.cellWidget(idx, 0).isChecked():
                self.canvascomponents['Seismic'][idx].parent = self.view.scene
            else:
                self.canvascomponents['Seismic'][idx].parent = None

    def changeCbbOrtSeisOnCanvas(self, idx):
        if idx < len(self.canvasproperties['Seismic']):
            self.twgseisoncanvas.cellWidget(idx, 3).clear()
            _ort = ''
            _no = 0
            if self.twgseisoncanvas.cellWidget(idx, 2).currentIndex() == 0:
                self.twgseisoncanvas.cellWidget(idx, 3).addItems([str(_no) for _no in self.survinfo['ILRange']])
                self.twgseisoncanvas.cellWidget(idx, 3).setCurrentIndex(0)
                _ort = 'Inline'
                _no = self.survinfo['ILRange'][0]
            if self.twgseisoncanvas.cellWidget(idx, 2).currentIndex() == 1:
                self.twgseisoncanvas.cellWidget(idx, 3).addItems([str(_no) for _no in self.survinfo['XLRange']])
                self.twgseisoncanvas.cellWidget(idx, 3).setCurrentIndex(0)
                _ort = 'Crossline'
                _no = self.survinfo['XLRange'][0]
            if self.twgseisoncanvas.cellWidget(idx, 2).currentIndex() == 2:
                self.twgseisoncanvas.cellWidget(idx, 3).addItems([str(_no) for _no in self.survinfo['ZRange']])
                self.twgseisoncanvas.cellWidget(idx, 3).setCurrentIndex(0)
                _ort = 'Z'
                _no = self.survinfo['ZRange'][0]
            self.canvasproperties['Seismic'][idx]['Orientation'] = _ort
            self.canvasproperties['Seismic'][idx]['Number'] = _no
            self.canvascomponents['Seismic'][idx].parent = None
            _vis = self.createVisualSeis(self.canvasproperties['Seismic'][idx]['Name'], _ort, _no)
            if self.canvasproperties['Seismic'][idx]['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['Seismic'][idx] = _vis

    def changeCbbNoSeisOnCanvas(self, idx):
        if idx < len(self.canvasproperties['Seismic']):
            _no = 0
            _ort = ''
            if self.twgseisoncanvas.cellWidget(idx, 2).currentIndex() == 0:
                _ort = 'Inline'
                _no = self.survinfo['ILRange'][self.twgseisoncanvas.cellWidget(idx, 3).currentIndex()]
            if self.twgseisoncanvas.cellWidget(idx, 2).currentIndex() == 1:
                _ort = 'Crossline'
                _no = self.survinfo['XLRange'][self.twgseisoncanvas.cellWidget(idx, 3).currentIndex()]
            if self.twgseisoncanvas.cellWidget(idx, 2).currentIndex() == 2:
                _ort = 'Z'
                _no = self.survinfo['ZRange'][self.twgseisoncanvas.cellWidget(idx, 3).currentIndex()]
            self.canvasproperties['Seismic'][idx]['Number'] = _no
            self.canvascomponents['Seismic'][idx].parent = None
            _vis = self.createVisualSeis(self.canvasproperties['Seismic'][idx]['Name'], _ort, _no)
            if self.canvasproperties['Seismic'][idx]['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['Seismic'][idx] = _vis

    def clickBtnRmSeisOnCanvas(self, idx):
        if idx < len(self.canvasproperties['Seismic']):
            self.canvasproperties['Seismic'].pop(idx)
            self.canvascomponents['Seismic'][idx].parent = None
            self.canvascomponents['Seismic'].pop(idx)
            self.updateTwgSeisOnCanvas()

    def updateTwgSeisOnCanvas(self):
        self.twgseisoncanvas.clear()
        _seis = self.canvasproperties['Seismic']
        self.twgseisoncanvas.setRowCount(len(_seis))
        for _i in range(len(_seis)):
            _item = QtWidgets.QCheckBox()
            _item.setChecked(_seis[_i]['Visible'])
            _item.stateChanged.connect(partial((self.changeCbxVisSeisOnCanvas), idx=_i))
            self.twgseisoncanvas.setCellWidget(_i, 0, _item)
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_seis[_i]['Name'])
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgseisoncanvas.setItem(_i, 1, _item)
            _item = QtWidgets.QComboBox()
            _item.addItems(['Inline', 'Xline', 'Z'])
            _item.setCurrentIndex(list.index(['Inline', 'Crossline', 'Z'], _seis[_i]['Orientation']))
            _item.currentIndexChanged.connect(partial((self.changeCbbOrtSeisOnCanvas), idx=_i))
            self.twgseisoncanvas.setCellWidget(_i, 2, _item)
            _item = QtWidgets.QComboBox()
            _slices = []
            if _seis[_i]['Orientation'] == 'Inline':
                _slices = [str(_no) for _no in self.survinfo['ILRange']]
            if _seis[_i]['Orientation'] == 'Crossline':
                _slices = [str(_no) for _no in self.survinfo['XLRange']]
            if _seis[_i]['Orientation'] == 'Z':
                _slices = [str(_no) for _no in self.survinfo['ZRange']]
            _item.addItems(_slices)
            _item.setCurrentIndex(list.index(_slices, str(_seis[_i]['Number'])))
            _item.currentIndexChanged.connect(partial((self.changeCbbNoSeisOnCanvas), idx=_i))
            self.twgseisoncanvas.setCellWidget(_i, 3, _item)
            _item = QtWidgets.QPushButton()
            _icon = QtGui.QIcon()
            _icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/no.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            _item.setIcon(_icon)
            _item.clicked.connect(partial((self.clickBtnRmSeisOnCanvas), idx=_i))
            self.twgseisoncanvas.setCellWidget(_i, 4, _item)

    def clickBtnConfigPointSetVis(self):
        _config = QtWidgets.QDialog()
        _gui = gui_configpointsetvis()
        _gui.pointsetvisconfig = self.pointsetvisconfig
        _gui.setupGUI(_config)
        _config.exec()
        self.pointsetvisconfig = _gui.pointsetvisconfig
        _config.show()
        for _i in range(len(self.canvascomponents['PointSet'])):
            self.canvascomponents['PointSet'][_i].parent = None
            _vis = self.createVisualPointSet(self.canvasproperties['PointSet'][_i]['Name'])
            if self.canvasproperties['PointSet'][_i]['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['PointSet'][_i] = _vis

    def clickBtnManagePointSet(self):
        _manage = QtWidgets.QDialog()
        _gui = gui_managepointset()
        _gui.pointsetdata = self.pointsetdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.linestyle = self.settings['Visual']['Line']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_manage)
        _manage.exec()
        self.pointsetdata = _gui.pointsetdata
        _manage.show()
        self.cbblistpointset.clear()
        self.cbblistpointset.addItems(list(self.pointsetdata.keys()))
        _config = {}
        if len(self.pointsetdata.keys()) > 0:
            for _point in self.pointsetdata.keys():
                if self.checkPointSetData(_point):
                    _config[_point] = {}
                    if _point in self.pointsetvisconfig.keys():
                        _config[_point] = self.pointsetvisconfig[_point]
                    else:
                        _config[_point]['Marker'] = '+'
                        _config[_point]['Color'] = self.settings['Visual']['Line']['Color']
                        _config[_point]['Size'] = self.settings['Visual']['Line']['MarkerSize']

        self.pointsetvisconfig = _config
        _idx_pop = []
        for _idx in range(len(self.canvasproperties['PointSet'])):
            if self.canvasproperties['PointSet'][_idx]['Name'] not in self.pointsetdata.keys():
                _idx_pop.append(_idx)

        for _idx in range(len(_idx_pop)):
            self.canvasproperties['PointSet'].pop(_idx_pop[_idx] - _idx)
            self.canvascomponents['PointSet'][(_idx_pop[_idx] - _idx)].parent = None
            self.canvascomponents['PointSet'].pop(_idx_pop[_idx] - _idx)

        self.updateTwgPointSetOnCanvas()

    def clickBtnAddPointSet2Canvas(self):
        if len(self.pointsetdata.keys()) > 0 and self.checkPointSetData(list(self.pointsetdata.keys())[self.cbblistpointset.currentIndex()]):
            _point = {}
            _point['Visible'] = False
            _point['Name'] = list(self.pointsetdata.keys())[self.cbblistpointset.currentIndex()]
            _point['Property'] = 'Z'
            _point['Remove'] = False
            self.canvasproperties['PointSet'].append(_point)
            _npoint = len(self.canvasproperties['PointSet'])
            self.twgpointsetoncanvas.setRowCount(_npoint)
            _item = QtWidgets.QCheckBox()
            _item.setChecked(_point['Visible'])
            _item.stateChanged.connect(partial((self.changeCbxVisPointSetOnCanvas), idx=(_npoint - 1)))
            self.twgpointsetoncanvas.setCellWidget(_npoint - 1, 0, _item)
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_point['Name'])
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgpointsetoncanvas.setItem(_npoint - 1, 1, _item)
            _item = QtWidgets.QComboBox()
            _item.addItems(list(self.pointsetdata[_point['Name']].keys()))
            _item.setCurrentIndex(list.index(list(self.pointsetdata[_point['Name']].keys()), 'Z'))
            _item.setEnabled(False)
            _item.currentIndexChanged.connect(partial((self.changeCbbPropPointSetOnCanvas), idx=(_npoint - 1)))
            self.twgpointsetoncanvas.setCellWidget(_npoint - 1, 2, _item)
            _item = QtWidgets.QPushButton()
            _icon = QtGui.QIcon()
            _icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/no.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            _item.setIcon(_icon)
            _item.clicked.connect(partial((self.clickBtnRmPointSetOnCanvas), idx=(_npoint - 1)))
            self.twgpointsetoncanvas.setCellWidget(_npoint - 1, 3, _item)
            _vis = self.createVisualPointSet(_point['Name'])
            if _point['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['PointSet'].append(_vis)

    def changeCbxVisPointSetOnCanvas(self, idx):
        if idx < len(self.canvasproperties['PointSet']):
            self.canvasproperties['PointSet'][idx]['Visible'] = self.twgpointsetoncanvas.cellWidget(idx, 0).isChecked()
            if self.twgpointsetoncanvas.cellWidget(idx, 0).isChecked():
                self.canvascomponents['PointSet'][idx].parent = self.view.scene
            else:
                self.canvascomponents['PointSet'][idx].parent = None

    def changeCbbPropPointSetOnCanvas(self, idx):
        print('Not used yet')

    def clickBtnRmPointSetOnCanvas(self, idx):
        if idx < len(self.canvasproperties['PointSet']):
            self.canvasproperties['PointSet'].pop(idx)
            self.canvascomponents['PointSet'][idx].parent = None
            self.canvascomponents['PointSet'].pop(idx)
            self.updateTwgPointSetOnCanvas()

    def updateTwgPointSetOnCanvas(self):
        self.twgpointsetoncanvas.clear()
        _point = self.canvasproperties['PointSet']
        self.twgpointsetoncanvas.setRowCount(len(_point))
        for _i in range(len(_point)):
            _item = QtWidgets.QCheckBox()
            _item.setChecked(_point[_i]['Visible'])
            _item.stateChanged.connect(partial((self.changeCbxVisPointSetOnCanvas), idx=_i))
            self.twgpointsetoncanvas.setCellWidget(_i, 0, _item)
            _item = QtWidgets.QTableWidgetItem()
            _item.setText(_point[_i]['Name'])
            _item.setTextAlignment(QtCore.Qt.AlignCenter)
            _item.setFlags(QtCore.Qt.ItemIsEditable)
            self.twgpointsetoncanvas.setItem(_i, 1, _item)
            _item = QtWidgets.QComboBox()
            _item.addItems(list(self.pointsetdata[_point[_i]['Name']].keys()))
            _item.setCurrentIndex(list.index(list(self.pointsetdata[_point[_i]['Name']].keys()), _point[_i]['Property']))
            _item.setEnabled(False)
            _item.currentIndexChanged.connect(partial((self.changeCbbPropPointSetOnCanvas), idx=_i))
            self.twgpointsetoncanvas.setCellWidget(_i, 2, _item)
            _item = QtWidgets.QPushButton()
            _icon = QtGui.QIcon()
            _icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/no.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            _item.setIcon(_icon)
            _item.clicked.connect(partial((self.clickBtnRmPointSetOnCanvas), idx=_i))
            self.twgpointsetoncanvas.setCellWidget(_i, 3, _item)

    def clickBtnSrvBox(self):
        if len(self.canvascomponents['Survey_Box']) == 12:
            if self.canvasproperties['Survey_Box'] is True:
                for _i in self.canvascomponents['Survey_Box']:
                    _i.parent = None

                self.canvasproperties['Survey_Box'] = False
            else:
                for _i in self.canvascomponents['Survey_Box']:
                    _i.parent = self.view.scene

                self.canvasproperties['Survey_Box'] = True

    def clickBtnXYZAxis(self):
        if self.canvascomponents['XYZ_Axis'] is not None:
            if self.canvasproperties['XYZ_Axis'] is True:
                self.canvascomponents['XYZ_Axis'].parent = None
                self.canvasproperties['XYZ_Axis'] = False
            else:
                self.canvascomponents['XYZ_Axis'].parent = self.view.scene
                self.canvasproperties['XYZ_Axis'] = True

    def clickBtnSnapshot(self):
        res = self.canvas.render()[:, :, 0:3]
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Save canvas', (self.settings['General']['RootPath']), filter='Portable Network Graphic file (PNG) (*.PNG);;All files (*.*)')
        if len(_file[0]) > 0:
            vispy_io.write_png(_file[0], res)

    def clickBtnGoHome(self):
        self.setCameraRange()
        self.view.camera.elevation = 30
        self.view.camera.azimuth = 135

    def changeCbbViewFrom(self):
        if self.cbbviewfrom.currentIndex() == 0:
            self.view.camera.elevation = 0
            self.view.camera.azimuth = 0
        else:
            if self.cbbviewfrom.currentIndex() == 1:
                self.view.camera.elevation = 0
                self.view.camera.azimuth = 90
            if self.cbbviewfrom.currentIndex() == 2:
                self.view.camera.elevation = 90
                self.view.camera.azimuth = 0

    def changeLdtZScale(self):
        _zscale = basic_data.str2float(self.ldtzscale.text())
        if _zscale is not False:
            if _zscale > 0.0:
                self.canvasproperties['Z_Scale'] = _zscale
        for _i in range(len(self.canvascomponents['Seismic'])):
            self.canvascomponents['Seismic'][_i].parent = None
            _vis = self.createVisualSeis(self.canvasproperties['Seismic'][_i]['Name'], self.canvasproperties['Seismic'][_i]['Orientation'], self.canvasproperties['Seismic'][_i]['Number'])
            if self.canvasproperties['Seismic'][_i]['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['Seismic'][_i] = _vis

        for _i in range(len(self.canvascomponents['PointSet'])):
            self.canvascomponents['PointSet'][_i].parent = None
            _vis = self.createVisualPointSet(self.canvasproperties['PointSet'][_i]['Name'])
            if self.canvasproperties['PointSet'][_i]['Visible']:
                _vis.parent = self.view.scene
            self.canvascomponents['PointSet'][_i] = _vis

        _srvbox = self.createSrvBox()
        if len(_srvbox) == 12:
            for _i in self.canvascomponents['Survey_Box']:
                _i.parent = None

            self.canvascomponents['Survey_Box'] = _srvbox
            for _i in self.canvascomponents['Survey_Box']:
                if self.canvasproperties['Survey_Box'] is True:
                    _i.parent = self.view.scene
                else:
                    _i.parent = None

        _xyzaxis = self.createXYZAxis()
        if _xyzaxis is not None:
            self.canvascomponents['XYZ_Axis'].parent = None
            self.canvascomponents['XYZ_Axis'] = _xyzaxis
            if self.canvasproperties['XYZ_Axis'] is True:
                self.canvascomponents['XYZ_Axis'].parent = self.view.scene
            else:
                self.canvascomponents['XYZ_Axis'].parent = None
        self.setCameraRange()

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))

    def createVisualSeis(self, seis, ort, no):
        if self.checkSurvInfo() is False:
            return
        else:
            if seis not in self.seisdata.keys():
                return
            else:
                if ort != 'Inline':
                    if ort != 'Crossline':
                        if ort != 'Z':
                            return
                        else:
                            _xlstart = self.survinfo['XLStart']
                            _xlend = self.survinfo['XLEnd']
                            _zstart = self.survinfo['ZStart'] * self.canvasproperties['Z_Scale']
                            _zend = self.survinfo['ZEnd'] * self.canvasproperties['Z_Scale']
                            _inlstart = self.survinfo['ILStart']
                            _inlend = self.survinfo['ILEnd']
                            _inlstep = self.survinfo['ILStep']
                            _inlnum = self.survinfo['ILNum']
                            if _inlnum == 1:
                                _inlstep = 1
                            _xlstep = self.survinfo['XLStep']
                            _xlnum = self.survinfo['XLNum']
                            if _xlnum == 1:
                                _xlstep = 1
                            _zstep = self.survinfo['ZStep'] * self.canvasproperties['Z_Scale']
                            _znum = self.survinfo['ZNum']
                            if _znum == 1:
                                _zstep = 1
                        if ort == 'Z':
                            no = no * self.canvasproperties['Z_Scale']
                    else:
                        if no < _inlstart:
                            if no > _inlend:
                                if no < _xlstart:
                                    if no > _xlend:
                                        if no > _zstart:
                                            if no < _zend:
                                                return
                    _data = np.zeros([2, 2])
                    _cmp = vis_cmap.makeColorMap(cmapname=(self.seisvisconfig[seis]['Colormap']), flip=(self.seisvisconfig[seis]['Flip']),
                      opacity=(self.seisvisconfig[seis]['Opacity']))
                    _cmp = Colormap(_cmp.colors)
                    _interp = self.seisvisconfig[seis]['Interpolation'].lower()
                    if _interp is None or _interp == 'None' or _interp == 'none':
                        _interp = 'nearest'
                else:
                    _vis = scene.visuals.Image(_data, parent=None, cmap=_cmp, clim=(
                     self.seisvisconfig[seis]['Minimum'], self.seisvisconfig[seis]['Maximum']),
                      interpolation=_interp)
                    _tr = scene.transforms.MatrixTransform()
                    if ort == 'Inline':
                        _idx = np.round((no - _inlstart) / _inlstep).astype(np.int32)
                        _data = self.seisdata[seis][:, :, _idx]
                        _tr.scale((abs(_xlstep), abs(_zstep)))
                        _tr.rotate(-90, (1, 0, 0))
                        _tr.translate((_xlstart, no, _zstart))
                        _tr.translate((-0.5 * _xlstep, 0, -0.5 * _zstep))
                    if ort == 'Crossline':
                        _idx = np.round((no - _xlstart) / _xlstep).astype(np.int32)
                        _data = self.seisdata[seis][:, _idx, :]
                        _tr.scale((abs(_inlstep), abs(_zstep)))
                        _tr.rotate(-90, (1, 0, 0))
                        _tr.rotate(90, (0, 0, 1))
                        _tr.translate((no, _inlstart, _zstart))
                        _tr.translate((0, -0.5 * _inlstep, -0.5 * _zstep))
                if ort == 'Z':
                    _idx = np.round((no - _zstart) / _zstep).astype(np.int32)
                    _data = self.seisdata[seis][_idx, :, :]
                    _tr.scale((abs(_inlstep), abs(_xlstep)))
                    _tr.rotate(90, (0, 0, 1))
                    _tr.rotate(180, (0, 1, 0))
                    _tr.translate((_xlstart, _inlstart, no))
                    _tr.translate((-0.5 * _xlstep, -0.5 * _inlstep, 0))
            _vis.set_data(_data)
            _vis.transform = _tr
            return _vis

    def createVisualPointSet(self, point):
        if self.checkSurvInfo() is False:
            return
        else:
            if point not in self.pointsetdata.keys():
                return
            _data = basic_mdt.exportMatDict(self.pointsetdata[point], ['Inline', 'Crossline', 'Z'])
            _data[:, 2] *= self.canvasproperties['Z_Scale']
            _vis = scene.visuals.Markers()
            _vis.set_data(_data, size=(self.pointsetvisconfig[point]['Size']),
              face_color=(self.pointsetvisconfig[point]['Color'].lower()),
              edge_color=None,
              symbol=(self.pointsetvisconfig[point]['Marker']),
              scaling=False)
            return _vis

    def createSrvBox(self):
        _srvlines = []
        if self.checkSurvInfo():
            _xlstart = self.survinfo['XLStart']
            _xlend = self.survinfo['XLEnd']
            _zstart = self.survinfo['ZStart'] * self.canvasproperties['Z_Scale']
            _zend = self.survinfo['ZEnd'] * self.canvasproperties['Z_Scale']
            _inlstart = self.survinfo['ILStart']
            _inlend = self.survinfo['ILEnd']
            _inlstep = self.survinfo['ILStep']
            _inlnum = self.survinfo['ILNum']
            if _inlnum == 1:
                _inlstep = 1
            _xlstep = self.survinfo['XLStep']
            _xlnum = self.survinfo['XLNum']
            if _xlnum == 1:
                _xlstep = 1
            _zstep = self.survinfo['ZStep'] * self.canvasproperties['Z_Scale']
            _znum = self.survinfo['ZNum']
            if _znum == 1:
                _zstep = 1
            for p in ([_xlstart - 0.5 * _xlstep, _inlstart - 0.5 * _inlstep, _zend + 0.5 * _zstep, _xlend + 0.5 * _xlstep, _inlstart - 0.5 * _inlstep, _zend + 0.5 * _zstep],
             [
              _xlstart - 0.5 * _xlstep, _inlstart - 0.5 * _inlstep, _zend + 0.5 * _zstep, _xlstart - 0.5 * _xlstep, _inlend + 0.5 * _inlstep, _zend + 0.5 * _zstep],
             [
              _xlstart - 0.5 * _xlstep, _inlstart - 0.5 * _inlstep, _zend + 0.5 * _zstep, _xlstart - 0.5 * _xlstep, _inlstart - 0.5 * _inlstep, _zstart - 0.5 * _zstep],
             [
              _xlstart - 0.5 * _xlstep, _inlend + 0.5 * _inlstep, _zstart - 0.5 * _zstep, _xlend + 0.5 * _xlstep, _inlend + 0.5 * _inlstep, _zstart - 0.5 * _zstep],
             [
              _xlend + 0.5 * _xlstep, _inlstart - 0.5 * _inlstep, _zstart - 0.5 * _zstep, _xlend + 0.5 * _xlstep, _inlend + 0.5 * _inlstep, _zstart - 0.5 * _zstep],
             [
              _xlend + 0.5 * _xlstep, _inlend + 0.5 * _inlstep, _zend + 0.5 * _zstep, _xlend + 0.5 * _xlstep, _inlend + 0.5 * _inlstep, _zstart - 0.5 * _zstep],
             [
              _xlend + 0.5 * _xlstep, _inlstart - 0.5 * _inlstep, _zend + 0.5 * _zstep, _xlend + 0.5 * _xlstep, _inlend + 0.5 * _inlstep, _zend + 0.5 * _zstep],
             [
              _xlstart - 0.5 * _xlstep, _inlend + 0.5 * _inlstep, _zend + 0.5 * _zstep, _xlend + 0.5 * _xlstep, _inlend + 0.5 * _inlstep, _zend + 0.5 * _zstep],
             [
              _xlstart - 0.5 * _xlstep, _inlend + 0.5 * _inlstep, _zend + 0.5 * _zstep, _xlstart - 0.5 * _xlstep, _inlend + 0.5 * _inlstep, _zstart - 0.5 * _zstep],
             [
              _xlstart - 0.5 * _xlstep, _inlstart - 0.5 * _inlstep, _zstart - 0.5 * _zstep, _xlstart - 0.5 * _xlstep, _inlend + 0.5 * _inlstep, _zstart - 0.5 * _zstep],
             [
              _xlend + 0.5 * _xlstep, _inlstart - 0.5 * _inlstep, _zend + 0.5 * _zstep, _xlend + 0.5 * _xlstep, _inlstart - 0.5 * _inlstep, _zstart - 0.5 * _zstep],
             [
              _xlstart - 0.5 * _xlstep, _inlstart - 0.5 * _inlstep, _zstart - 0.5 * _zstep, _xlend + 0.5 * _xlstep, _inlstart - 0.5 * _inlstep, _zstart - 0.5 * _zstep]):
                _line = scene.visuals.Line(pos=(np.array([[p[0], p[1], p[2]], [p[3], p[4], p[5]]])), color='black',
                  parent=None)
                _srvlines.append(_line)

        return _srvlines

    def createXYZAxis(self):
        _xyz = None
        if self.checkSurvInfo():
            _xlstart = self.survinfo['XLStart']
            _xlend = self.survinfo['XLEnd']
            _zstart = self.survinfo['ZStart'] * self.canvasproperties['Z_Scale']
            _zend = self.survinfo['ZEnd'] * self.canvasproperties['Z_Scale']
            _inlstart = self.survinfo['ILStart']
            _inlend = self.survinfo['ILEnd']
            _inlstep = self.survinfo['ILStep']
            _inlnum = self.survinfo['ILNum']
            if _inlnum == 1:
                _inlstep = 1
            _xlstep = self.survinfo['XLStep']
            _xlnum = self.survinfo['XLNum']
            if _xlnum == 1:
                _xlstep = 1
            _zstep = self.survinfo['ZStep'] * self.canvasproperties['Z_Scale']
            _znum = self.survinfo['ZNum']
            if _znum == 1:
                _zstep = 1
            _x0 = 0.5 * (_xlstart + _xlend)
            _y0 = 0.5 * (_inlstart + _inlend)
            _z0 = 0.5 * (_zstart + _zend)
            _len = np.max(np.abs(np.array([_xlstep, _inlstep, _zstep])))
            _xyz = scene.visuals.XYZAxis(parent=None, pos=(np.array([[_x0, _y0, _z0], [_x0 + _len, _y0, _z0],
             [
              _x0, _y0, _z0], [_x0, _y0 + _len, _z0],
             [
              _x0, _y0, _z0], [_x0, _y0, _z0 - _len]])))
        return _xyz

    def setCameraRange(self):
        if self.checkSurvInfo():
            _xlstart = self.survinfo['XLStart']
            _xlend = self.survinfo['XLEnd']
            _zstart = self.survinfo['ZStart'] * self.canvasproperties['Z_Scale']
            _zend = self.survinfo['ZEnd'] * self.canvasproperties['Z_Scale']
            _inlstart = self.survinfo['ILStart']
            _inlend = self.survinfo['ILEnd']
            self.view.camera.set_range((_xlstart, _xlend), (_inlstart, _inlend), (_zend, _zstart))

    def checkSurvInfo(self):
        self.refreshMsgBox()
        if seis_ays.checkSeisInfo(self.survinfo) is False:
            return False
        else:
            return True

    def checkSeisData(self, f):
        self.refreshMsgBox()
        return seis_ays.isSeis3DMatConsistentWithSeisInfo(self.seisdata[f], self.survinfo)

    def checkPointSetData(self, p):
        self.refreshMsgBox()
        return pointset_ays.checkPoint(self.pointsetdata[p])


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PlotVisCanvas = QtWidgets.QWidget()
    gui = plotviscanvas()
    gui.setupGUI(PlotVisCanvas)
    PlotVisCanvas.show()
    sys.exit(app.exec_())