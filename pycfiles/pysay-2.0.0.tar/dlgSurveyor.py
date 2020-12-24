# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\dlgSurveyor.py
# Compiled at: 2019-10-29 06:22:59
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from fileinput import filename
from pyFAI import azimuthalIntegrator
from pySAXS.guisaxs import dataset
from pySAXS.guisaxs.qt import preferences
from pySAXS.guisaxs.qt import QtMatplotlib
from pySAXS.guisaxs.qt import dlgAbsoluteI
from pySAXS.guisaxs.qt import dlgAutomaticFit
import matplotlib.colors as colors
from pySAXS.tools import FAIsaxs
from pySAXS.tools import filetools
import os, sys
from scipy import ndimage
if sys.version_info.major >= 3:
    import configparser
else:
    import ConfigParser as configparser
from pySAXS.guisaxs.qt.dlgAbsoluteI import dlgAbsolute
from matplotlib.patches import Circle
from PyQt5 import QtTest
AUTOMATIC_FIT = False

def my_excepthook(type, value, tback):
    sys.__excepthook__(type, value, tback)


sys.excepthook = my_excepthook
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.patches as patches
from time import *
import fabio, numpy, os.path, pyFAI, sys, threading, glob, fnmatch, pySAXS
from pySAXS.LS import SAXSparametersXML
from pySAXS.guisaxs.qt import dlgQtFAITest
ICON_PATH = pySAXS.__path__[0] + os.sep + 'guisaxs' + os.sep + 'images' + os.sep
HEADER = [
 'name', 'x', 'z', 'exposure', 'Trans. Flux', 'Incid. Flux']
FROM_EDF = ['Comment', 'x', 'z', 'count_time', 'pilroi0', 'pilai1']
FROM_RPT = ['filename', 'samplex', 'samplez', 'exposure', 'transmitted flux']
IMAGE_TYPE = [
 '*.edf*', '*.TIFF*']

class SurveyorDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, parameterfile=None, outputdir=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'dlgSurveyor.ui', self)
        self.setWindowTitle('Continuous Radial averaging tool for pySAXS')
        if parent is not None:
            self.setWindowIcon(parent.windowIcon())
        self.parent = parent
        self.plotapp = None
        self.printout = None
        self.whereZ = False
        self.workingdirectory = None
        self.fai = None
        self.mad = None
        self.lastDatas = None
        self.plt = self.ui.matplotlibwidget.figure
        self.plt.patch.set_facecolor('White')
        self.canvas = FigureCanvas(self.plt)
        self.axes = self.plt.add_subplot(111)
        self.clbar = None
        self.plt.tight_layout()
        self.ui.paramFileButton.clicked.connect(self.OnClickparamFileButton)
        self.ui.changeDirButton.clicked.connect(self.OnClickchangeDirButton)
        self.ui.plotChkBox.clicked.connect(self.OnClickPlotCheckBox)
        self.ui.btnExtUpdate.clicked.connect(self.updateListInit)
        self.ui.tableWidget.cellClicked[(int, int)].connect(self.cellClicked)
        self.ui.tableWidget.cellDoubleClicked[(int, int)].connect(self.cellDoubleClicked)
        self.ui.btnDisplaySelected.clicked.connect(self.btnDisplayClicked)
        self.ui.btnZApply.clicked.connect(self.btnZApplyClicked)
        self.ui.btnReset.clicked.connect(self.btnZResetClicked)
        self.ui.btnDisplayAV.clicked.connect(self.btnDisplayAVClicked)
        self.ui.btnProcessSelection.clicked.connect(self.btnProcessSelectionClicked)
        self.ui.btnProcessALL.clicked.connect(self.btnProcessALLClicked)
        self.ui.paramViewButton.clicked.connect(self.OnClickparamViewButton)
        self.ui.btnCenterOfMass.clicked.connect(self.OnClickCenterOfMassButton)
        self.ui.btnExportList.clicked.connect(self.OnClickExportList)
        self.ui.navi_toolbar = NavigationToolbar(self.ui.matplotlibwidget, self)
        self.ui.verticalLayout_2.insertWidget(0, self.ui.navi_toolbar)
        l = self.ui.navi_toolbar.actions()
        l = self.ui.navi_toolbar.actions()
        for i in l:
            if i.text() == 'Pan':
                panAction = i
            if i.text() == 'Customize':
                customizeAction = i
            if i.text() == 'Subplots':
                subplotAction = i

        self.ui.navi_toolbar.removeAction(customizeAction)
        self.ui.navi_toolbar.removeAction(subplotAction)
        self.AutoscaleAction = QtWidgets.QAction('Autoscale', self)
        self.AutoscaleAction.triggered.connect(self.OnAutoscale)
        self.ui.navi_toolbar.addAction(self.AutoscaleAction)
        self.FixScaleAction = QtWidgets.QAction(QtGui.QIcon(ICON_PATH + 'magnet.png'), 'Fix Scale', self)
        self.FixScaleAction.setCheckable(True)
        self.FixScaleAction.setChecked(False)
        self.FixScaleAction.triggered.connect(self.OnButtonFixScale)
        self.ui.navi_toolbar.addAction(self.FixScaleAction)
        self.SelectedFile = None
        self.ui.labelSelectedFIle.setText('')
        self.ui.btnDisplaySelected.setEnabled(False)
        self.ui.btnDisplayAV.setEnabled(False)
        self.ui.radioButton_lin.setChecked(True)
        self.ui.radioButton_lin.toggled.connect(lambda : self.btnStateLinLog(self.radioButton_lin))
        self.DISPLAY_LOG = False
        self.EXPORT_LIST = []
        self.ui.chkDisplayBeam.clicked.connect(self.OnClickDisplayBeam)
        self.ui.chkDisplayCircles.clicked.connect(self.btnDisplayClicked)
        self.ui.btnBeamApply.clicked.connect(self.OnClickButtonBeam)
        self.ui.btnTransferParams.clicked.connect(self.OnClickButtonTransferParams)
        self.ui.edit_Q.textChanged.connect(self.btnDisplayClicked)
        self.ui.edit_dd.textChanged.connect(self.btnDisplayClicked)
        self.ui.chkDisplayMaskFile.clicked.connect(self.btnDisplayClicked)
        if AUTOMATIC_FIT:
            self.ui.btnAutomaticFit.setEnabled(True)
            self.automaticFitApp = dlgAutomaticFit.dlgAutomaticFit(parent)
            self.ui.btnAutomaticFit.clicked.connect(self.btnDisplayAutomaticFitClicked)
            self.ui.btnPAF.setEnabled(True)
            self.ui.btnPAF.clicked.connect(self.btnProcessALLClicked)
        self.ui.btnCheckSolvent.clicked.connect(self.btnCheckSolventClicked)
        if self.parent is None:
            self.ui.chkSubSolvent.setEnabled(False)
            self.ui.btnCheckSolvent.setEnabled(False)
        else:
            if self.parent.referencedata is not None:
                self.ui.solventEdit.setText(str(self.parent.referencedata))
            self.parameterfile = parameterfile
            try:
                if self.parameterfile is not None and self.parameterfile != '':
                    self.ui.paramTxt.setText(str(parameterfile))
            except:
                pass

            self.pref = preferences.prefs()
            if parent is not None:
                self.printout = parent.printTXT
                self.workingdirectory = parent.workingdirectory
                self.pref = self.parent.pref
                try:
                    if self.pref.fileExist():
                        self.pref.read()
                        dr = self.pref.get('defaultdirectory', section='guisaxs qt')
                        if dr is not None:
                            self.workingdirectory = dr
                            self.ui.DirTxt.setText(str(self.workingdirectory))
                        pf = self.pref.get('parameterfile', section='pyFAI')
                        if pf is not None:
                            self.parameterfile = pf
                            self.ui.paramTxt.setText(str(self.parameterfile))
                            try:
                                self.OnClickButtonTransferParams()
                            except:
                                print 'problem when trying to read parameters'

                        ext = self.pref.get('fileextension', section='pyFAI')
                        if ext is not None:
                            self.ui.extensionTxt.setText(ext)
                    else:
                        self.pref.save()
                except:
                    print 'couldnt reach working directory '
                    return

            else:
                self.workingdirectory = 'Y:/2017/2017-08-24-OT'
                self.ui.DirTxt.setText(self.workingdirectory)
            self.imageToolWindow = None
            self.updateListInit()
            self.fp = str(self.ui.DirTxt.text())
            txt = ''
            for i in IMAGE_TYPE:
                txt += i + ' '

        self.ui.extensionTxt.setText(txt)
        self._fileSysWatcher = QtCore.QFileSystemWatcher()
        if self.fp != '':
            if os.path.isdir(self.fp):
                self._fileSysWatcher.addPath(self.fp)
                self._fileSysWatcher.directoryChanged.connect(self.slotDirChanged)
        return

    @QtCore.pyqtSlot('QString')
    def slotDirChanged(self, path):
        self.updateListInit()

    def OnClickparamFileButton(self):
        """
        Allow to select a parameter file
        """
        fd = QtWidgets.QFileDialog(self)
        filename = fd.getOpenFileName(directory=self.workingdirectory)[0]
        self.ui.paramTxt.setText(filename)
        self.radialPrepare()

    def OnClickSTARTButton(self):
        """
        Used when start button is clicked
        """
        print 'start'
        self.ui.progressBar.setRange(0, 0)
        self.radialPrepare()
        self.ui.STOPButton.setEnabled(True)
        self.ui.STARTButton.setDisabled(True)
        if self.ui.refreshTimeTxt.text() == '':
            t = 30
        else:
            t = float(self.ui.refreshTimeTxt.text())
        self.t = Intervallometre(t, self.updateList, self)
        self.t.start()

    def OnClickSTOPButton(self):
        """
        Used when stop button is clicked
        """
        print 'stop'
        self.ui.progressBar.setRange(0, 1)
        self.ui.STARTButton.setEnabled(True)
        self.ui.STOPButton.setDisabled(True)
        self.t.stop()

    def OnClickchangeDirButton(self):
        """
        Allow to select a directory
        """
        dir = QtWidgets.QFileDialog.getExistingDirectory(directory=self.workingdirectory)
        if dir == '':
            return
        if not os.path.isdir(dir):
            return
        self.ui.DirTxt.setText(dir)
        self.workingdirectory = dir
        self.updateListInit()
        try:
            self.pref.set('defaultdirectory', self.workingdirectory, section='guisaxs qt')
            self.pref.save()
        except:
            pass

        l = self._fileSysWatcher.directories()
        if len(l) > 0:
            self._fileSysWatcher.removePaths(l)
        self._fileSysWatcher.addPath(dir)
        l = self._fileSysWatcher.directories()

    def cellClicked(self, row, col):
        self.SelectedFile = str(self.ui.tableWidget.item(row, 0).text())
        self.ui.labelSelectedFIle.setText(self.workingdirectory + os.sep + self.SelectedFile)
        self.ui.btnDisplaySelected.setEnabled(True)
        self.ui.btnDisplayAV.setEnabled(True)

    def cellDoubleClicked(self, row, col):
        self.SelectedFile = str(self.ui.tableWidget.item(row, 0).text())
        self.ui.labelSelectedFIle.setText(self.workingdirectory + os.sep + self.SelectedFile)
        self.ui.btnDisplaySelected.setEnabled(True)
        self.ui.btnDisplayAV.setEnabled(True)
        self.btnDisplayClicked()

    def btnDisplayClicked(self):
        """
        display the image
        """
        self.axes.cla()
        if self.SelectedFile is None:
            return
        else:
            try:
                self.img = fabio.open(self.workingdirectory + os.sep + self.SelectedFile)
            except:
                print 'pySAXS : unable to open imagefile : ' + self.workingdirectory + os.sep + self.SelectedFile
                return

            D = self.img.data
            xmax, ymax = numpy.shape(D)
            extent = (0, xmax, 0, ymax)
            if self.whereZ:
                zmin = float(self.ui.edtZmin.text())
                zmax = float(self.ui.edtZmax.text())
                D = numpy.where(D <= zmin, zmin, D)
                D = numpy.where(D > zmax, zmax, D)
            else:
                self.ui.edtZmin.setText(str(D.min()))
                self.ui.edtZmax.setText(str(D.max()))
            norm = colors.LogNorm(vmin=D.min(), vmax=D.max())
            if self.DISPLAY_LOG:
                zmin = float(self.ui.edtZmin.text())
                if zmin <= 0:
                    zmin = 1
                    self.ui.edtZmin.setText('1')
                zmax = float(self.ui.edtZmax.text())
                D = numpy.where(D <= zmin, zmin, D)
                D = numpy.where(D > zmax, zmax, D)
                norm = colors.LogNorm(vmin=D.min(), vmax=D.max())
                if self.ui.chkDisplayMaskFile.isChecked() and self.mad is not None:
                    imgplot = self.axes.imshow(numpy.logical_not(self.mad) * D, cmap='jet', norm=norm)
                else:
                    imgplot = self.axes.imshow(D, cmap='jet', norm=norm)
            else:
                if self.ui.chkDisplayMaskFile.isChecked() and self.mad is not None:
                    imgplot = self.axes.imshow(numpy.logical_not(self.mad) * D, cmap='jet')
                else:
                    imgplot = self.axes.imshow(D, cmap='jet')
                if self.FixScaleAction.isChecked():
                    self.axes.set_xlim((self.xlim_min, self.xlim_max))
                    self.axes.set_ylim((self.ylim_min, self.ylim_max))
                if self.clbar is None:
                    self.clbar = self.plt.colorbar(imgplot, shrink=0.5)
                else:
                    try:
                        self.clbar.remove()
                    except:
                        pass

                self.clbar = self.plt.colorbar(imgplot, shrink=0.5)
            if self.ui.chkDisplayBeam.isChecked():
                BeamX = float(self.ui.edtBeamX.text())
                BeamY = float(self.ui.edtBeamY.text())
                xmax, ymax = numpy.shape(D)
                x1, y1 = [
                 BeamX, 0], [BeamX, ymax]
                x2, y2 = [0, BeamY], [xmax, BeamY]
                rect = patches.Rectangle((0, 0), BeamX, BeamY, linewidth=1, edgecolor='r', facecolor='none')
                rect2 = patches.Rectangle((BeamX, BeamY), xmax, ymax, linewidth=1, edgecolor='r', facecolor='none')
                self.axes.add_patch(rect)
                self.axes.add_patch(rect2)
            if self.ui.chkDisplayCircles.isChecked():
                try:
                    Q = float(self.ui.edit_Q.text())
                    lam = float(self.ui.edit_wavelength.text())
                    L = float(self.ui.edit_dd.text())
                    pixelSize = float(self.ui.edit_pixelsize.text())
                    sizemax = max(xmax, ymax)
                    theta = numpy.arcsin(Q * lam / (4 * numpy.pi)) * 2
                    ellipse_height = 2 * L * numpy.tan(theta) / pixelSize
                    for ccNumber in range(0, int(sizemax * 2 / ellipse_height) + 1):
                        CC = Circle((BeamX, BeamY), ccNumber * ellipse_height / 2, color='white', linewidth=1, linestyle='--', fill=False)
                        self.axes.add_patch(CC)

                except:
                    pass

            self.ui.matplotlibwidget.draw()
            return

    def btnDisplayAVClicked(self):
        if self.SelectedFile is None:
            return
        else:
            self.radialAverage(self.workingdirectory + os.sep + self.SelectedFile)
            return

    def OnAutoscale(self):
        sh = self.img.data.shape
        plt = self.ui.matplotlibwidget
        plt.axes.set_ylim((sh[0], 0))
        plt.axes.set_xlim((0, sh[1]))
        self.xlim_min, self.xlim_max = plt.axes.get_xlim()
        self.ylim_min, self.ylim_max = plt.axes.get_ylim()
        plt.draw()

    def OnButtonFixScale(self):
        plt = self.ui.matplotlibwidget
        self.xlim_min, self.xlim_max = plt.axes.get_xlim()
        self.ylim_min, self.ylim_max = plt.axes.get_ylim()

    def btnZApplyClicked(self):
        try:
            self.zmin = float(self.ui.edtZmin.text())
            zmax = float(self.ui.edtZmax.text())
            self.whereZ = True
            self.btnDisplayClicked()
        except:
            pass

    def btnZResetClicked(self):
        self.whereZ = False
        self.btnDisplayClicked()

    def btnStateLinLog(self, b):
        if b.text() == 'lin':
            if b.isChecked() == True:
                self.DISPLAY_LOG = False
            else:
                self.DISPLAY_LOG = True
                if float(self.ui.edtZmin.text()) <= 0:
                    self.ui.edtZmin.setText('1')
        self.whereZ = True
        self.btnDisplayClicked()

    def OnClickGetBeamXY(self):
        """
        try to get Beam X Y from parameter file
        """
        if self.ui.paramTxt.text() == '':
            QtWidgets.QMessageBox.information(self, 'pySAXS', 'Parameter file is not specified', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return
        else:
            filename = self.ui.paramTxt.text()
            if not os.path.exists(filename):
                self.printTXT(filename + ' does not exist')
                QtWidgets.QMessageBox.information(self, 'pySAXS', str(filename) + ' does not exist', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
                return
            if self.fai is None:
                self.radialPrepare()
            self.fai.setGeometry(filename)
            self.ui.edtBeamY.setText(str(self.fai._xmldirectory['user.centery']))
            self.ui.edtBeamX.setText(str(self.fai._xmldirectory['user.centerx']))
            self.OnClickButtonBeam()
            return

    def OnClickButtonTransferParams(self):
        if self.ui.paramTxt.text() == '':
            QtWidgets.QMessageBox.information(self, 'pySAXS', 'Parameter file is not specified', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return
        else:
            filename = self.ui.paramTxt.text()
            if not os.path.exists(filename):
                self.printTXT(filename + ' does not exist')
                QtWidgets.QMessageBox.information(self, 'pySAXS', str(filename) + ' does not exist', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
                return
            if self.fai is None:
                self.radialPrepare()
            self.fai.setGeometry(filename)
            self.ui.edtBeamY.setText(str(self.fai._xmldirectory['user.centery']))
            self.ui.edtBeamX.setText(str(self.fai._xmldirectory['user.centerx']))
            self.OnClickButtonBeam()
            self.ui.edit_pixelsize.setText(str('%6.5f' % self.fai._xmldirectory['user.PixelSize']))
            self.ui.edit_wavelength.setText(str('%6.5f' % self.fai._xmldirectory['user.wavelength']))
            self.ui.edit_dd.setText(str(self.fai._xmldirectory['user.DetectorDistance']))
            self.ui.edit_maskfile.setText(str(self.fai._xmldirectory['user.MaskImageName']))
            return

    def OnClickButtonBeam(self):
        self.ui.chkDisplayBeam.setChecked(True)
        self.btnDisplayClicked()

    def updateList(self):
        """
        Update the list
        """
        print 'refresh'
        self.ext = str(self.ui.extensionTxt.text())
        if self.ext == '':
            self.ext = '*.*'
        self.fp = str(self.ui.DirTxt.text())
        listoffile = self.getList(self.fp, self.ext)
        files = sorted(listoffile, reverse=True)
        self.ui.tableWidget.setColumnCount(4)
        self.ui.tableWidget.setRowCount(len(listoffile))
        headerNames = ['File', 'date', 'processed', 'new']
        self.ui.tableWidget.setHorizontalHeaderLabels(headerNames)
        self.ui.tableWidget.setColumnWidth(0, 220)
        self.ui.tableWidget.setColumnWidth(1, 150)
        self.ui.tableWidget.setColumnWidth(2, 70)
        self.ui.tableWidget.setColumnWidth(3, 50)
        i = 0
        for name in files:
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(listoffile[name][0])))
            self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(listoffile[name][1])))
            self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(str(listoffile[name][2])))
            self.ui.tableWidget.setRowHeight(i, 20)
            if not listoffile[name][1]:
                try:
                    self.radialAverage(self.fp + os.sep + name)
                except:
                    print (
                     'unable to average on file :', name)

            i += 1

        self.listoffileVerif = glob.glob(os.path.join(self.fp, self.ext))
        self.listoffileVerif = listoffile
        if len(listoffile) > 0:
            self.cellClicked(0, 0)
            self.btnDisplayClicked()
        else:
            self.SelectedFile = None
            self.ui.labelSelectedFIle.setText('')
            self.ui.btnDisplaySelected.setEnabled(False)
            self.ui.btnDisplayAV.setEnabled(False)
        return

    def updateListInit(self):
        """
        Update the initial List WITHOUT treatment 
        """
        self.fp = str(self.ui.DirTxt.text())
        try:
            listoffile, files = self.getList(self.fp)
        except:
            listoffile = {}
            files = []

        self.ui.tableWidget.setRowCount(len(listoffile))
        headerNames = ['File', 'date', 'processed', 'new']
        headerNames += HEADER
        self.EXPORT_LIST = [headerNames]
        self.ui.tableWidget.setColumnCount(len(headerNames))
        self.ui.tableWidget.setHorizontalHeaderLabels(headerNames)
        self.ui.tableWidget.setColumnWidth(0, 220)
        self.ui.tableWidget.setColumnWidth(1, 150)
        self.ui.tableWidget.setColumnWidth(2, 70)
        self.ui.tableWidget.setColumnWidth(3, 50)
        i = 0
        ll = []
        iconTrue = QtGui.QIcon(ICON_PATH + 'check-mark-small.png')
        iconFalse = QtGui.QIcon(ICON_PATH + 'error-icon-small.png')
        iconNew = QtGui.QIcon(ICON_PATH + 'new.png')
        for name in files:
            ll = [
             name] + listoffile[name]
            self.ui.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(name))
            self.ui.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(listoffile[name][0])))
            if listoffile[name][1]:
                self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(iconTrue, ''))
            else:
                self.ui.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(iconFalse, ''))
            if listoffile[name][2]:
                self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(iconNew, ''))
            else:
                self.ui.tableWidget.setItem(i, 3, QtWidgets.QTableWidgetItem(iconTrue, ''))
            self.ui.tableWidget.setRowHeight(i, 20)
            if HEADER is not None:
                infos = self.getInformationFromImage(name)
                for j in range(len(infos)):
                    self.ui.tableWidget.setItem(i, 4 + j, QtWidgets.QTableWidgetItem(infos[j]))

                ll += infos
            i += 1
            self.EXPORT_LIST.append(ll)

        self.listoffileVerif = listoffile
        if len(listoffile) > 0:
            if self.ui.chkAutomaticDisplayFirst.isChecked():
                self.cellClicked(0, 0)
                self.btnDisplayClicked()
            if self.ui.chkAutomaticAV.isChecked():
                self.cellClicked(0, 0)
                self.btnDisplayClicked()
                self.btnDisplayAVClicked()
        else:
            self.SelectedFile = None
            self.ui.labelSelectedFIle.setText('')
            self.ui.btnDisplaySelected.setEnabled(False)
            self.ui.btnDisplayAV.setEnabled(False)
        return

    def getfiles(self, dirpath):
        a = [ s for s in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath, s))
            ]
        a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
        return a

    def getList(self, fp):
        listoffile = []
        if self.fp == '':
            return []
        for file in os.listdir(self.fp):
            for ext in IMAGE_TYPE:
                if fnmatch.fnmatch(file, ext):
                    listoffile.append(os.path.abspath(self.fp) + os.sep + file)

        files = {}
        ttdict = {}
        for name in listoffile:
            fich = filetools.getFilename(name)
            dt = filetools.getModifiedDate(name)
            newfn = filetools.getFilenameOnly(name)
            tt = os.path.getmtime(os.path.join(self.fp, name))
            ttdict[tt] = fich
            ficTiff = newfn
            newfn += '.rgr'
            if filetools.fileExist(newfn):
                proc = True
                new = False
            else:
                proc = False
                new = True
            files[fich] = [
             dt, proc, new, tt]

        ttsorted = sorted(ttdict, reverse=True)
        filessorted = []
        for i in ttsorted:
            filessorted.append(ttdict[i])

        return (
         files, filessorted)

    def printTXT(self, txt='', par=''):
        """
        for printing messages
        """
        if self.printout == None:
            print str(txt) + str(par)
        else:
            self.printout(txt, par)
        return

    def radialPrepare(self):
        self.fai = FAIsaxs.FAIsaxs()
        filename = self.ui.paramTxt.text()
        if not os.path.exists(filename):
            self.printTXT(filename + ' does not exist')
            return
        else:
            outputdir = self.ui.DirTxt.text()
            self.fai.setGeometry(filename)
            try:
                self.mad = self.fai.getIJMask()
            except:
                self.mad = None

            maskfilename = self.fai.getMaskFilename()
            return

    def radialAverage(self, imageFilename, plotRefresh=True):
        if self.fai is None:
            self.radialPrepare()
        t0 = time()
        im, q, i, s, newname = self.fai.integratePySaxs(imageFilename, self.mad, self.printTXT)
        self.fai.saveGeometry(imageFilename)
        if im is None:
            return
        else:
            self.OnClickPlotCheckBox()
            if self.parent is None:
                self.plotapp.addData(q, i, label=imageFilename)
                self.plotapp.replot()
            else:
                myname = filetools.getFilename(imageFilename)
                if 'Comment' in im.header:
                    comment = im.header['Comment']
                    if comment != '':
                        myname += '-' + comment
                self.parent.data_dict[myname] = dataset.dataset(myname, q, i, imageFilename, error=s, type='saxs', image='Image')
                if plotRefresh:
                    self.parent.redrawTheList()
                if plotRefresh:
                    if self.ui.plotChkBox.isChecked():
                        self.parent.Replot()
                if self.ui.chkAutomaticAbsolute.isChecked():
                    param = dlgAbsoluteI.getTheParameters(myname, self.parent, self.workingdirectory)
                    if param is not None:
                        param.calculate_All()
                        if self.ui.chkSubSolvent.isChecked():
                            referencedata = self.parent.referencedata
                        else:
                            referencedata = None
                        try:
                            thickness = float(self.ui.thicknessEdit.text())
                        except:
                            thickness = None

                        try:
                            background_by_s = float(self.ui.backgdEdit.text())
                        except:
                            background_by_s = None

                        newname_scaled = dlgAbsoluteI.OnScalingSAXSApply(self.parent, dataname=myname, parameters=param.parameters, referencedata=referencedata, thickness=thickness, background_by_s=background_by_s)
                        self.parent.data_dict[myname].parameters = param
                        self.parent.data_dict[myname].checked = False
                        myname = newname_scaled
                    else:
                        print 'not found'
                    if plotRefresh:
                        self.parent.redrawTheList()
                        self.parent.Replot()
                self.lastDatas = myname
                if plotRefresh:
                    if self.ui.chkAutomaticSaving.isChecked():
                        if self.parent.DatasetFilename != '':
                            self.parent.OnFileSave()
            return

    def btnProcessALLClicked(self):
        st = self.ui.chkAutomaticAV.isChecked()
        self.ui.chkAutomaticAV.setChecked(False)
        if AUTOMATIC_FIT:
            self.automaticFitApp.clearResult()
        n = self.ui.tableWidget.rowCount()
        self.ui.progressBar.setMaximum(n)
        for row in range(0, n):
            name = str(self.ui.tableWidget.item(row, 0).text())
            name = self.workingdirectory + os.sep + name
            self.radialAverage(name, plotRefresh=False)
            self.ui.progressBar.setValue(row)
            if AUTOMATIC_FIT:
                self.btnDisplayAutomaticFitClicked()
                QtTest.QTest.qWait(500)

        self.radialAverage(name, plotRefresh=True)
        self.ui.progressBar.setValue(0)
        self.ui.chkAutomaticAV.setChecked(st)

    def btnProcessSelectionClicked(self):
        st = self.ui.chkAutomaticAV.isChecked()
        self.ui.chkAutomaticAV.setChecked(False)
        if AUTOMATIC_FIT:
            self.automaticFitApp.clearResult()
        n = self.ui.tableWidget.rowCount()
        self.ui.progressBar.setMaximum(n)
        for item in self.ui.tableWidget.selectedIndexes():
            row = item.row()
            name = str(self.ui.tableWidget.item(row, 0).text())
            name = self.workingdirectory + os.sep + name
            self.radialAverage(name, plotRefresh=False)
            if AUTOMATIC_FIT:
                self.btnDisplayAutomaticFitClicked()
                QtTest.QTest.qWait(500)

        self.radialAverage(name, plotRefresh=True)
        self.ui.progressBar.setValue(0)
        self.ui.chkAutomaticAV.setChecked(st)

    def OnClickPlotCheckBox(self):
        if self.parent is None:
            if self.ui.plotChkBox.isChecked():
                self.plotapp = QtMatplotlib.QtMatplotlib()
                self.plotapp.show()
            else:
                self.plotapp.close()
        return

    def OnClickDisplayBeam(self):
        """
        user clicked on display beam
        """
        self.btnDisplayClicked()

    def OnClickparamViewButton(self):
        filename = str(self.ui.paramTxt.text())
        if filename is not None and filename != '':
            self.dlgFAI = dlgQtFAITest.FAIDialogTest(self.parent, filename, None)
            self.dlgFAI.show()
        return

    def getInformationFromImage(self, filename):
        """
        get the information from image
        (header if EDF, or rpt file if TIFF)
        """
        d = self.ui.DirTxt.text()
        filename = self.workingdirectory + os.sep + filename
        try:
            im = fabio.open(filename)
        except:
            return []

        l = []
        EXTE = filetools.getExtension(filename).lower()
        if EXTE == 'edf':
            for n in FROM_EDF:
                try:
                    l.append(str(im.header[n]))
                except:
                    l.append('?')

        else:
            rpt = configparser.ConfigParser()
            txt = '?'
            filenameRPT = filetools.getFilenameOnly(filename) + '.rpt'
            if not filetools.fileExist(filenameRPT):
                return []
            test = rpt.read(filenameRPT)
            if len(test) == 0:
                print (
                 'error when reading file :', filenameRPT)
                return []
            l = []
            for n in FROM_RPT:
                try:
                    l.append(str(rpt.get('acquisition', n)))
                except:
                    l.append('?')

        return l

    def OnClickCenterOfMassButton(self):
        """
        calculate the center of mass
        """
        plt = self.ui.matplotlibwidget
        xlim_min, xlim_max = plt.axes.get_xlim()
        ylim_max, ylim_min = plt.axes.get_ylim()
        im = self.img.data[int(ylim_min):int(ylim_max), int(xlim_min):int(xlim_max)]
        CenterOM = ndimage.measurements.center_of_mass(im)
        self.ui.chkDisplayBeam.setChecked(True)
        self.ui.edtBeamX.setText('%6.2f' % (CenterOM[1] + xlim_min))
        self.ui.edtBeamY.setText('%6.2f' % (CenterOM[0] + ylim_min))
        self.btnDisplayClicked()

    def OnClickExportList(self):
        """
        export the list
        """
        fd = QtWidgets.QFileDialog(self)
        filename, ext = fd.getSaveFileName(self, 'export list', directory=self.workingdirectory, filter='Text files(*.txt);;All files (*.*)')
        if filename:
            f = open(filename, 'w')
            for row in self.EXPORT_LIST:
                tt = ''
                for n in row:
                    tt += str(n) + '\t'

                print tt
                f.write(tt + '\n')

            f.close()

    def btnDisplayAutomaticFitClicked(self):
        self.automaticFitApp.tryFitThis(self.lastDatas)

    def btnCheckSolventClicked(self):
        if self.parent.referencedata is not None:
            self.ui.solventEdit.setText(str(self.parent.referencedata))
        return

    def closeEvent(self, event):
        """
        when window is closed
        """
        l = self._fileSysWatcher.directories()
        self._fileSysWatcher.removePaths(l)
        if self.parent is not None:
            self.pref.set('parameterfile', section='pyFAI', value=str(self.ui.paramTxt.text()))
            self.pref.set('defaultdirectory', section='guisaxs qt', value=str(self.ui.DirTxt.text()))
            self.pref.set('fileextension', section='pyFAI', value=str(self.ui.extensionTxt.text()))
            self.pref.save()
        try:
            self.t.stop()
        except:
            pass

        return


class Intervallometre(threading.Thread):

    def __init__(self, duree, fonction, parent=None):
        threading.Thread.__init__(self)
        self.duree = duree
        self.fonction = fonction
        self.parent = parent
        self.encore = True

    def run(self):
        print 'start'
        while self.encore:
            self.parent.updateList()
            self.slip(self.duree)

    def stop(self):
        self.encore = False

    def slip(self, t, intt=1.0):
        if t < intt:
            sleep(t)
            return
        t0 = time()
        while t - (time() - t0) > intt:
            if self.encore:
                sleep(intt)
            else:
                return

        sleep(t - (time() - t0))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = SurveyorDialog()
    myapp.show()
    sys.exit(app.exec_())