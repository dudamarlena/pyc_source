# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\mainGuisaxs.py
# Compiled at: 2019-01-14 09:30:28
"""
mainGuisaxs a new GUI made with qt
author : Olivier Tache
(C) CEA 2012
"""
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import codecs, unidecode, sys

def my_excepthook(type, value, tback):
    """
    enabled pyqt5 application to catch the exception without 
    crashing
    """
    sys.__excepthook__(type, value, tback)


import unicodedata
VER = 2
if sys.version_info.major >= 3:
    VER = 3
from pySAXS.guisaxs.qt import genericFormDialog
from functools import partial
from pySAXS.tools import isNumeric
from pySAXS.guisaxs.qt import QtMatplotlib
from pySAXS.guisaxs.qt import dlgClipQRange
from pySAXS.guisaxs.qt import dlgConcatenate
from pySAXS.guisaxs.qt import dlgCalculator
from pySAXS.guisaxs.qt import dlgAbsoluteI
from pySAXS.guisaxs.qt import dlgInfoDataset
try:
    from pySAXS.guisaxs.qt import pluginFAI
except:
    pass

from pySAXS.guisaxs.qt import dlgModel
from pySAXS.guisaxs.qt import dlgTextView
from pySAXS.guisaxs.qt import dlgAbsorption
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import colors
import matplotlib.font_manager as font_manager
from pySAXS.guisaxs import pySaxsColors
import os
from os import path
import pySAXS, itertools, numpy
from scipy import stats
from pySAXS.guisaxs.dataset import *
from pySAXS.tools import filetools
from pySAXS.tools import DetectPeaks
import unicodedata, pySAXS.LS.SAXSparametersXML as SAXSparameters
from pySAXS.models import listOfModels
import pySAXS.models
from pySAXS.filefilters import fileimport
from pySAXS.guisaxs.qt import preferences
from time import sleep
import time
from pySAXS.guisaxs.qt import pluginMCSAS
typefile_list = fileimport.import_list()
typefile = fileimport.import_dict()
SPLASHSCREEN_TEMPO = 0.0
DEBUG_MODE = True

class mainGuisaxs(QtWidgets.QMainWindow):

    def __init__(self, parent=None, splashScreen=None):
        QtWidgets.QWidget.__init__(self, parent)
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = uic.loadUi(pySAXS.UI_PATH + 'mainGuisaxs.ui', self)
        self.setWindowTitle('pySAXS')
        self.icon = QtGui.QIcon(pySAXS.ICON_PATH + 'pySaxs.png')
        self.setWindowIcon(self.icon)
        self.DatasetFilename = ''
        self.workingdirectory = ''
        self.referencedata = None
        self.referenceValue = None
        self.backgrounddata = None
        self.referencedataSubtract = True
        self.setAcceptDrops(True)
        self.pastedModel = None
        self.colors = pySaxsColors.pySaxsColors()
        if splashScreen is not None:
            splashScreen.showMessage('Loading preferences...', color=QtCore.Qt.white, alignment=QtCore.Qt.AlignBottom)
            sleep(SPLASHSCREEN_TEMPO)
        self.pref = preferences.prefs()
        if self.pref.fileExist():
            self.pref.read()
            dr = self.pref.get('defaultdirectory')
            if dr is not None:
                self.workingdirectory = dr
        else:
            self.pref.save()
        rec = self.pref.getRecentFiles()
        for name in rec:
            name = name.strip('\'"')
            action = self.ui.menuRecents.addAction(name)
            item = name
            action.triggered.connect(partial(self.OnRecentFile, item))

        self.ui.menuFile.addAction(self.ui.menuRecents.menuAction())
        if splashScreen is not None:
            splashScreen.showMessage('Loading menus...', color=QtCore.Qt.white, alignment=QtCore.Qt.AlignBottom)
            sleep(SPLASHSCREEN_TEMPO)
        self.ui.actionOpen.triggered.connect(self.OnFileOpen)
        self.ui.actionOpen_Dataset.triggered.connect(self.OnFileOpenDataset)
        self.ui.actionAppend_Dataset.triggered.connect(self.OnFileAppendDataset)
        self.ui.actionSave.triggered.connect(self.OnFileSave)
        self.ui.actionSave.setShortcut('Ctrl+S')
        self.ui.actionSave_As.triggered.connect(self.OnFileSaveAs)
        self.ui.actionExport.triggered.connect(self.OnFileExport)
        self.ui.actionReset_datas.triggered.connect(self.OnFileResetDatas)
        self.ui.actionGenerate_treatment_file.triggered.connect(self.OnFileGenerateABS)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionSelect_All.triggered.connect(self.OnEditSelectAll)
        self.ui.actionUnselect_All.triggered.connect(self.OnEditUnselectAll)
        self.ui.actionSelect_Only_Parents.triggered.connect(self.OnEditSelectParents)
        self.ui.actionSelect_Only_Childs.triggered.connect(self.OnEditSelectChilds)
        self.ui.actionRefresh_from_file.triggered.connect(self.OnEditRefresh)
        self.ui.actionRename.triggered.connect(self.OnEditRename)
        self.ui.actionRemove.triggered.connect(self.OnEditRemove)
        self.ui.actionRemove.setShortcut('Delete')
        self.ui.actionRemove_selected.triggered.connect(self.OnEditRemoveSelected)
        self.ui.actionRemove_UNselected.triggered.connect(self.OnEditRemoveUNSelected)
        self.ui.actionDuplicate.triggered.connect(self.OnEditDuplicate)
        self.ui.actionDuplicate_without_links.triggered.connect(self.OnEditDuplicateWLinks)
        self.ui.actionClip_Q_range.triggered.connect(self.OnEditClipQRange)
        self.ui.actionScale_Q_range.triggered.connect(self.OnEditScaleQ)
        self.ui.actionConcatenate.triggered.connect(self.OnEditConcatenate)
        self.ui.actionDerivate.triggered.connect(self.OnEditDerivate)
        self.ui.actionFind_peaks.triggered.connect(self.OnEditFindPeaks)
        self.ui.actionSmooth.triggered.connect(self.OnEditSmooth)
        self.ui.actionCalculator.triggered.connect(self.OnEditCalculator)
        self.ui.actionStatistics.triggered.connect(self.OnEditStat)
        self.ui.actionGenerate_Noise.triggered.connect(self.OnEditGenerateNoise)
        self.ui.actionAddReferenceValue.triggered.connect(self.OnEditAddReference)
        self.ui.actionRemove_dependencies.triggered.connect(self.OnEditRemoveDependencies)
        self.ui.actionChange_color.triggered.connect(self.OnEditChangeColor)
        self.ui.actionSet_as_reference.triggered.connect(self.OnEditSetAsReference)
        self.ui.actionSet_as_Background.triggered.connect(self.OnEditSetAsBackground)
        self.ui.actionCalculate_Resolution_function.triggered.connect(self.NotYetImplemented)
        self.ui.actionInvariant.triggered.connect(self.NotYetImplemented)
        self.ui.actionX_ray_absorption.triggered.connect(self.OnToolsAbsorption)
        self.ui.actionChanges.triggered.connect(self.OnHelpChanges)
        self.ui.actionLicence.triggered.connect(self.OnHelpLicense)
        self.ui.actionAbout.triggered.connect(self.OnHelpAbout)
        self.ui.actionInfo.triggered.connect(self.OnInfoDataset)
        self.ui.treeWidget.itemClicked.connect(self.OnItemChanged)
        self.ui.treeWidget.itemDoubleClicked.connect(self.OnItemDoubleClicked)
        self.ui.treeWidget.setHeaderLabels(['Datas'])
        self.ui.treeWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.treeWidget.customContextMenuRequested.connect(self.popup)
        self.data_dict = {}
        self.createFilters()
        if splashScreen is not None:
            splashScreen.showMessage('Loading plot windows...', color=QtCore.Qt.white, alignment=QtCore.Qt.AlignBottom)
            sleep(SPLASHSCREEN_TEMPO)
        self.move(QtCore.QPoint(100, 100))
        self.createPlotframe()
        self.printTXT('<b>--- Welcome to GuiSAXS in QT ---</b>')
        if splashScreen is not None:
            splashScreen.showMessage('Loading plugins...', color=QtCore.Qt.white, alignment=QtCore.Qt.AlignBottom)
            sleep(SPLASHSCREEN_TEMPO)
        p = path.dirname(pySAXS.__file__)
        p += os.sep + 'guisaxs' + os.sep + 'qt'
        pl = self.plugins_list(p)
        base = 'pySAXS.guisaxs.qt.'
        submenuDict = {}
        toolbarListPluginsActions = []
        for name in pl:
            try:
                m = self.my_import(base + name)
                cl = m.classlist
                for c in cl:
                    try:
                        o = getattr(m, c)
                        sub = o.subMenu
                        item = o
                        if sub not in submenuDict:
                            itemSub = QtWidgets.QMenu(self.ui.menuData_Treatment)
                            itemSub.setObjectName(sub)
                            itemSub.setTitle(sub)
                            if o.icon is not None:
                                icon1 = QtGui.QIcon()
                                icon1.addPixmap(QtGui.QPixmap(pySAXS.ICON_PATH + o.icon), QtGui.QIcon.Normal, QtGui.QIcon.On)
                                itemSub.setIcon(icon1)
                            submenuDict[sub] = itemSub
                        itemSub = submenuDict[sub]
                        action = itemSub.addAction(o.subMenuText)
                        if o.icon is not None:
                            icon1 = QtGui.QIcon()
                            icon1.addPixmap(QtGui.QPixmap(pySAXS.ICON_PATH + o.icon), QtGui.QIcon.Normal, QtGui.QIcon.On)
                            action.setIcon(icon1)
                        self.ui.menuData_Treatment.addAction(itemSub.menuAction())
                        action.triggered.connect(partial(self.callPlugin, o))
                        if o.toolbar:
                            toolbarListPluginsActions.append(action)
                    except:
                        print (
                         'Unexpected error :', sys.exc_info()[0])
                        print ('module : ', c, ' module will not be available')

            except:
                print (
                 'Unexpected error:', sys.exc_info()[0])
                print ('module : ', name, ' module will not be available')

        if splashScreen is not None:
            splashScreen.showMessage('Loading models...', color=QtCore.Qt.white, alignment=QtCore.Qt.AlignBottom)
            sleep(SPLASHSCREEN_TEMPO)
        menuModels = QtWidgets.QMenu(self.ui.menuFit)
        menuModels.setTitle('Models')
        menuModels.setObjectName('Models')
        iconModel = QtGui.QIcon()
        iconModel.addPixmap(QtGui.QPixmap(pySAXS.ICON_PATH + 'model.png'), QtGui.QIcon.Normal, QtGui.QIcon.On)
        menuModels.setIcon(iconModel)
        modelsDict = listOfModels.listOfModels()
        dd = list(modelsDict.items())
        dd = self.sortDictByKey(modelsDict)
        self.modelsDictId = {}
        for id in range(len(dd)):
            self.modelsDictId[id] = dd[id]
            action = menuModels.addAction(dd[id][0])
            action.setIcon(iconModel)
            item = dd[id][1]
            action.triggered.connect(partial(self.callModel, item))

        self.ui.menuFit.addAction(menuModels.menuAction())
        self.ui.menuFit.addSeparator()
        self.actionCopyModel = self.ui.menuFit.addAction('Copy model')
        self.actionCopyModel.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'clipboard-paste.png'))
        self.actionCopyModel.setEnabled(False)
        self.actionCopyModel.triggered.connect(self.OnFitCopyModel)
        self.actionPasteModel = self.ui.menuFit.addAction('Paste model')
        self.actionPasteModel.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'arrow-curve-270-left.png'))
        self.actionPasteModel.setEnabled(False)
        self.actionPasteModel.triggered.connect(self.OnFitPasteModel)
        if splashScreen is not None:
            splashScreen.showMessage('Loading documentation...', color=QtCore.Qt.white, alignment=QtCore.Qt.AlignBottom)
            sleep(SPLASHSCREEN_TEMPO)
        self.docs = self.getListOfDocs()
        i = 0
        for name in self.docs:
            action = self.ui.menuDocuments.addAction(path.basename(name))
            item = name
            action.triggered.connect(partial(self.OnOpenDocument, item))

        self.ui.actionX_ray_absorption.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'table.png'))
        self.ui.actionFind_peaks.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'fit.png'))
        self.ui.actionSelect_All.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'ui-check-box-mix.png'))
        self.ui.actionUnselect_All.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'ui-check-box-uncheck.png'))
        self.ui.actionSelect_Only_Parents.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'node-select.png'))
        self.ui.actionSelect_Only_Childs.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'node-select-child.png'))
        self.ui.actionRename.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'document-rename.png'))
        self.ui.actionRemove.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'editdelete.png'))
        self.ui.actionDuplicate.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'editcopy.png'))
        self.ui.actionDuplicate_without_links.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'blue-document-copy.png'))
        self.ui.actionClip_Q_range.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'scissors'))
        self.ui.actionScale_Q_range.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'slide-resize-actual.png'))
        self.ui.actionConcatenate.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'plus-button.png'))
        self.ui.actionDerivate.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'hide.png'))
        self.ui.actionSmooth.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'chart-down.png'))
        self.ui.actionFind_Peaks.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'fit.png'))
        self.ui.actionInterpolate.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'chart-down-color.png'))
        self.ui.actionCalculator.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'calculator.png'))
        self.ui.actionStatistics.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'edit-mathematics.png'))
        self.ui.actionGenerate_Noise.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'megaphone.png'))
        self.ui.actionRefresh_from_file.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'reload.png'))
        self.ui.actionAddReferenceValue.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'arrow.png'))
        self.ui.actionSet_as_reference.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'water.png'))
        self.ui.actionSet_as_Background.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'wall.png'))
        self.ui.actionRemove_dependencies.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'node-delete.png'))
        self.ui.actionChange_color.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'color.png'))
        self.ui.actionReset_datas.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'counter-reset.png'))
        self.ui.actionRemove_selected.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'document--minus.png'))
        self.ui.actionGenerate_treatment_file.setIcon(QtGui.QIcon(pySAXS.ICON_PATH + 'blue-documents-stack.png'))
        self.ui.toolBar.addAction(self.ui.actionOpen)
        toolbarListActions = [self.ui.actionOpen, self.ui.actionSave, None, self.ui.actionCalculator, self.ui.actionChange_color,
         self.ui.actionSet_as_reference, self.ui.actionSet_as_Background, None]
        toolbarListActions.extend(toolbarListPluginsActions)
        for act in toolbarListActions:
            if act is not None:
                self.ui.toolBar.addAction(act)
            else:
                self.ui.toolBar.addSeparator()

        self.ui.show()
        return

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            print e.key()

    def callPlugin(self, obj, val):
        print val
        label = self.getCurrentSelectedItem()
        child = obj(self, label)
        if DEBUG_MODE:
            child.execute()
        else:
            try:
                child.execute()
            except:
                print (
                 'Unexpected error in :' + obj.menu, sys.exc_info()[0])

    def callModel(self, modelname, val):
        label = self.getCurrentSelectedItem()
        M = getattr(pySAXS.models, modelname)()
        if M.WarningForCalculationTime:
            ret = QtWidgets.QMessageBox.question(self, 'pySAXS', 'Computation time can be high for this model. Continue ?', buttons=QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if ret != QtWidgets.QMessageBox.Yes:
                return
        self.openModel(M, label)

    def openModel(self, M, label, openDialog=True):
        if label is None:
            data_selected_for_model = M.name
            self.data_dict[data_selected_for_model] = dataset(data_selected_for_model, M.q, M.getIntensity(), '', True, M, type='model')
            if openDialog:
                self.childmodel = dlgModel.dlgModel(self, data_selected_for_model, type='model')
        else:
            data_selected_for_model = label
            new_dataname = data_selected_for_model + '-' + M.name + ' model'
            q = self.data_dict[data_selected_for_model].q
            M.q = q
            i = M.getIntensity()
            filename = self.data_dict[data_selected_for_model].filename
            self.data_dict[new_dataname] = dataset(new_dataname, copy(q), copy(i), filename, True, M, parent=[
             data_selected_for_model], rawdata_ref=data_selected_for_model, type='model')
            if openDialog:
                self.childmodel = dlgModel.dlgModel(self, new_dataname, type='data')
        self.redrawTheList()
        self.Replot()
        if openDialog:
            self.childmodel.show()
        return

    def sortDictByKey(self, d):
        """
        return list of couple sorted by key
        """
        l = []
        for key in sorted(d.keys()):
            l.append((key, d[key]))

        return l

    def popup(self, pos):
        """
        display the Edit menu on popup
        """
        menu = self.ui.menuEdit
        action = menu.exec_(self.mapToGlobal(pos))

    def closeEvent(self, event):
        """
        when window is closed
        """
        try:
            self.plotframe.close()
        except:
            pass

    def createPlotframe(self):
        """
        create the plotframe
        """
        spacex = 25
        spacey = +30
        self.plotframe = QtMatplotlib.QtMatplotlib(self)
        x = self.width() + self.x() + spacex
        y = self.y() + spacey
        self.plotframe.move(x, y)
        self.plotframe.resize(self.width() * 1.5, self.height())
        self.plotframe.setWindowTitle('Guisaxs Plot')
        self.plotframe.setScaleLabels('$q(\\AA^{-1})$', 'I', size=10)
        self.plotframe.setAxesFormat(QtMatplotlib.LOGLOG, changeMenu=True)
        self.plotframe.show()

    def OnPlotframeClosed(self):
        """
        when plotframe is closed
        """
        self.plotframe = None
        return

    def createFilters(self):
        """
        create file filters
        """
        self.filterList = ''
        self.filterDict = {}
        for k in typefile_list:
            filterName = typefile[k][0] + ' (' + typefile[k][1] + ')'
            self.filterList += filterName + ';;'
            self.filterDict[filterName] = k

    def OnRecentFile(self, name):
        """
        user clicked on recent file
        """
        print (
         'open', name)
        if name is None:
            return
        else:
            if name is False:
                return
            extension = filetools.getExtension(name)
            if extension != 'xml':
                for type in typefile_list:
                    if typefile[type][1] == extension:
                        self.OnFileOpen(false, [name], type)
                        return

                self.printTXT("Don't know the type of :", name)
                self.OnFileOpen(False, [name])
            else:
                if len(self.data_dict) > 0:
                    reply = QtWidgets.QMessageBox.question(self, 'pySAXS error', 'There is already an open dataset. Do you want to overwrite ?', QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
                    if reply == QtWidgets.QMessageBox.No:
                        return
                self.OnFileOpenDataset(filename=name)
            return

    def OnFileOpen(self, bool=False, filenames=None, file_type=None):
        """
        Load datas
        """
        if filenames is None:
            print 'call the dialog box'
            fd = QtWidgets.QFileDialog(self)
            filenames, filter = fd.getOpenFileNames(filter=self.filterList, initialFilter='*.*', directory=self.workingdirectory)
            if len(filenames) <= 0:
                return
            file_type = self.filterDict[str(filter)]
        ext = filetools.getExtension(str(filenames[0]))
        if filetools.getExtension(str(filenames[0])) == 'xml':
            self.printTXT('opening Dataset', str(filenames[0]))
            self.OnFileOpenDataset(filename=str(filenames[0]))
            return
        else:
            for datafilename in filenames:
                self.printTXT('opening ' + datafilename)
                datafilename = str(datafilename)
                self.ReadFile(datafilename, file_type)

            self.setWorkingDirectory(datafilename)
            self.redrawTheList()
            self.Replot()
            return

    def OnFileOpenDataset(self, bool=False, filename=None):
        """
        open the data set
        """
        if len(self.data_dict) > 0:
            reply = QtWidgets.QMessageBox.question(self, 'pySAXS error', 'There is already an open dataset. Do you want to overwrite ?', QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
            if reply == QtWidgets.QMessageBox.No:
                return
        if filename is None:
            fd = QtWidgets.QFileDialog(self)
            wc = 'dataset  xml file (*.xml);;dataset file(*.dst)'
            filenames, filter = fd.getOpenFileNames(filter=wc, initialFilter='*.dst', directory=self.workingdirectory)
            if len(filenames) <= 0:
                return
            filename = str(filenames[0])
        ext = filetools.getExtension(filename)
        if str(ext).find('dst') >= 0:
            self.data_dict = getDataDictRaw(filename)
            for name in self.data_dict:
                self.data_dict[name].parent = None
                self.data_dict[name].color = None
                self.data_dict[name].image = None

        else:
            self.data_dict = getDataDictFromXMLFile(filename)
        colors = pySaxsColors.pySaxsColors()
        l = []
        for name in self.data_dict:
            l.append(name)
            if self.data_dict[name].type == 'reference':
                self.referencedata = name
                self.printTXT('reference datas are ', name)
            if self.data_dict[name].type == 'background':
                self.backgrounddata = name
                self.printTXT('background datas are ', name)

        l.sort()
        i = 0
        for name in l:
            if self.data_dict[name].color is None:
                col = colors.getColor(i)
                self.data_dict[name].color = col
                i += 1

        self.setWorkingDirectory(filename)
        self.redrawTheList()
        self.Replot()
        self.setWindowTitle(filename)
        self.DatasetFilename = filename
        self.printTXT('open dataset : ', filename)
        return

    def OnFileAppendDataset(self):
        """
        append a data set
        """
        fd = QtWidgets.QFileDialog(self)
        wc = 'dataset  xml file (*.xml);;dataset file(*.dst)'
        filenames, filter = fd.getOpenFileNames(filter=wc, initialFilter='*.dst', directory=self.workingdirectory)
        filename = str(filenames[0])
        self.setWorkingDirectory(filename)
        if len(filenames) <= 0:
            return
        else:
            ext = filetools.getExtension(filename)
            if str(filter).find('dst') >= 0:
                new_data_dict = getDataDictRaw(filename)
                for name in self.data_dict:
                    new_data_dict[name].parent = None

            else:
                new_data_dict = getDataDictFromXMLFile(filename)
            for name in new_data_dict:
                if name in self.data_dict:
                    newname = name + ' ' + self.giveMeANewName()
                    self.printTXT(name + ' dataset already exist, renamed as ' + newname)
                    new_data_dict[name].name = newname
                    self.data_dict[newname] = new_data_dict[name]
                else:
                    self.data_dict[name] = new_data_dict[name]

            self.redrawTheList()
            self.Replot()
            self.printTXT('open dataset : ', filename)
            return

    def OnFileSave(self):
        """
        save the dataset in the same file
        """
        if self.DatasetFilename == '':
            if len(self.data_dict) > 0:
                self.OnFileSaveAs()
            return
        filename = self.DatasetFilename
        saveDataDictOnXMLFile(filename, self.data_dict)
        self.DatasetFilename = filename
        self.setWindowTitle(filename)
        self.printTXT('datas saved in file ' + filename + ' at ' + time.strftime('%d %B %Y %H:%M:%S'))

    def OnFileSaveAs(self):
        """
        save the checked datas
        """
        fd = QtWidgets.QFileDialog(self)
        wc = 'dataset  xml file (*.xml)'
        filename = fd.getSaveFileName(filter=wc, directory=self.workingdirectory)[0]
        filename = str(filename)
        self.setWorkingDirectory(filename)
        if filename != '':
            if filetools.fileExist(filename):
                reply = QtWidgets.QMessageBox.question(self, 'pySAXS Question', 'File exist. Do you want to replace ?', QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
                if reply == QtWidgets.QMessageBox.No:
                    self.printTXT('file ' + str(filename) + ' exist. Datas were NOT replaced')
                    return
            if filename[-3:] != 'xml':
                filename += '.xml'
            saveDataDictOnXMLFile(filename, self.data_dict)
            self.setWindowTitle(filename)
            self.DatasetFilename = filename
            self.printTXT('datas saved in file ' + filename)

    def OnFileExport(self):
        """
        save the checked datas in txt
        """
        fd = QtWidgets.QFileDialog(self)
        wc = 'txt file (*.txt)'
        filename = fd.getSaveFileName(filter=wc, directory=self.workingdirectory)[0]
        filename = str(filename)
        self.setWorkingDirectory(filename)
        if filename != '':
            if filetools.fileExist(filename):
                reply = QtWidgets.QMessageBox.question(self, 'pySAXS Question', 'File exist. Do you want to replace ?', QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
                if reply == QtWidgets.QMessageBox.No:
                    self.printTXT('file ' + str(filename) + ' exist. Datas were NOT replaced')
                    return
            self.SaveAsTXT(filename)

    def SaveAsTXT(self, filename):
        """
        save the checked datas
        """
        self.printTXT('-------------------')
        self.printTXT('Saving data as txt in ' + filename)
        l = self.ListOfDatasChecked()
        print l
        l.sort()
        print l
        f = open(filename, mode='w')
        header1 = '#'
        header2 = '#'
        nrows = 0
        for name in l:
            self.printTXT(name)
            header1 += name + '\t\t'
            header2 += 'q\t i\t'
            if self.data_dict[name].error is not None:
                header1 += '\t'
                header2 += 'error\t'
            if len(self.data_dict[name].q) > nrows:
                nrows = len(self.data_dict[name].q)

        header1 += '\n'
        header2 += '\n'
        f.write(header1)
        f.write(header2)
        self.printTXT(str(nrows) + ' rows will be saved')
        for n in range(nrows):
            dat = ''
            for name in l:
                if n < len(self.data_dict[name].q):
                    dat += str(self.data_dict[name].q[n]) + '\t'
                    dat += str(self.data_dict[name].i[n]) + '\t'
                    if self.data_dict[name].error is not None:
                        dat += str(self.data_dict[name].error[n]) + '\t'
                else:
                    dat += '\t\t'
                    if self.data_dict[name].error is not None:
                        dat += '\t'

            dat += '\n'
            f.write(dat)

        self.printTXT('data are saved')
        self.printTXT('-------------------')
        f.close()
        return

    def OnFileResetDatas(self):
        """
        clear the datas
        """
        self.setWindowTitle('pySAXS')
        self.DatasetFilename = ''
        self.data_dict.clear()
        self.redrawTheList()
        self.Replot()

    def OnFileGenerateABS(self):
        """
        generate for each selected datas an ABS file containing all the data treatment
        """
        self.printTXT('-------------------')
        self.printTXT('Saving ABS data treatment ')
        l = self.ListOfDatasChecked()
        for name in l:
            if self.data_dict[name].abs is not None:
                print self.data_dict[name].abs
                self.data_dict[name].abs.saveABS(self.data_dict[name].filename)

        return

    def OnEditSelectAll(self):
        """
        when the user want to select all
        """
        for label in self.data_dict:
            self.data_dict[label].checked = True

        self.redrawTheList()
        self.Replot()

    def OnEditUnselectAll(self):
        """
        when the user want to select all
        """
        for label in self.data_dict:
            self.data_dict[label].checked = False

        self.redrawTheList()
        self.Replot()

    def OnEditSelectParents(self):
        """
        when the user want to select only parents
        """
        for label in self.data_dict:
            if self.data_dict[label].parent is None:
                self.data_dict[label].checked = True
            else:
                self.data_dict[label].checked = False

        self.redrawTheList()
        self.Replot()
        return

    def OnEditSelectChilds(self):
        """
        when the user want to select only parents
        """
        for label in self.data_dict:
            if self.data_dict[label].parent is None:
                self.data_dict[label].checked = False
            else:
                self.data_dict[label].checked = True

        self.redrawTheList()
        self.Replot()
        return

    def OnEditRefresh(self):
        """
        refresh data from file (is exist)
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            filename = self.data_dict[label].filename
            type = self.data_dict[label].type
            if type != None:
                self.printTXT('refresh ' + filename)
                self.ReadFile(filename, type)
                self.Replot()
            else:
                self.printTXT('type of data unknown -> not possible to refresh datas ')
            return

    def OnEditRename(self):
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            newlabel, ok = QtWidgets.QInputDialog.getText(self, 'pySAXS', 'Enter the new name:', text=label)
            newlabel = str(newlabel)
            if ok:
                newlabel = self.cleanString(newlabel)
                if newlabel in self.data_dict:
                    reply = QtWidgets.QMessageBox.question(self, 'pySAXS Question', 'There is already a data set with this name ! Replace ?', QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
                    if reply == QtWidgets.QMessageBox.No:
                        return
                self.printTXT('Rename  ' + label + ' into : ', newlabel)
                self.data_dict[newlabel] = self.data_dict[label]
                self.data_dict[newlabel].name = newlabel
                self.data_dict.pop(label)
                self.redrawTheList()
                self.Replot()
            return

    def OnEditRemove(self):
        """
        remove a data set
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            reply = QtWidgets.QMessageBox.question(self, 'pySAXS Question', 'Are you sure you want to remove this data set : ' + label + ' ?', QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
            if reply == QtWidgets.QMessageBox.Yes:
                self.printTXT('removing ', label)
                self.data_dict.pop(label)
                self.redrawTheList()
                self.Replot()
            return

    def OnEditRemoveSelected(self):
        """
        remove selected datas
        """
        listofdata = self.ListOfDatasChecked()
        if len(listofdata) <= 0:
            self.noDataErrorMessage()
            return
        reply = QtWidgets.QMessageBox.question(self, 'pySAXS Question', 'Are you sure you want to remove this datas ?', QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            for label in listofdata:
                self.printTXT('removing ', label)
                self.data_dict.pop(label)

            self.redrawTheList()
            self.Replot()

    def OnEditRemoveUNSelected(self):
        """
        remove UNselected datas
        """
        listofdata = self.ListOfDatasUNChecked()
        if len(listofdata) <= 0:
            self.noDataErrorMessage()
            return
        reply = QtWidgets.QMessageBox.question(self, 'pySAXS Question', 'Are you sure you want to remove this datas ?', QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            for label in listofdata:
                self.printTXT('removing ', label)
                self.data_dict.pop(label)

            self.redrawTheList()
            self.Replot()

    def OnEditDuplicate(self):
        """
        duplicate a data set
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            newlabel, ok = QtWidgets.QInputDialog.getText(self, 'pySAXS', 'Enter the new name:', text=label)
            newlabel = str(newlabel)
            if ok:
                self.printTXT('duplicate dataset : ' + label + ' to ' + newlabel)
                if newlabel in self.data_dict:
                    reply = QtWidgets.QMessageBox.warning(self, 'pySAXS Error', 'There is already a data set with this name !')
                    return
                self.data_dict[newlabel] = self.data_dict[label]._deepcopy()
                self.data_dict[newlabel].name = newlabel
                self.redrawTheList()
                self.Replot()
            return

    def OnEditDuplicateWLinks(self):
        """
        duplicate a data set without links
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            newlabel, ok = QtWidgets.QInputDialog.getText(self, 'pySAXS', 'Enter the new name:')
            newlabel = str(newlabel)
            if ok:
                self.printTXT('duplicate dataset : ' + label + ' to ' + newlabel)
                if newlabel in self.data_dict:
                    reply = QtWidgets.QMessageBox.warning(self, 'pySAXS Error', 'There is already a data set with this name !')
                    return
                self.data_dict[newlabel] = self.data_dict[label]._deepcopy()
                self.data_dict[newlabel].parent = None
                self.data_dict[newlabel].name = newlabel
                self.redrawTheList()
                self.Replot()
            return

    def OnEditClipQRange(self):
        """
        clip q range
        """
        listofdata = self.ListOfDatasChecked()
        if len(listofdata) == 0:
            QtWidgets.QMessageBox.information(self, 'pySAXS', 'No data are selected', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return
        else:
            dataset_name = listofdata[0]
            datas = self.data_dict[dataset_name]
            qmin = datas.q.min()
            qmax = datas.q.max()
            nbpoints = len(datas.q)
            dlg = genericFormDialog.genericFormDialog(title='Clip q range', comment=str(listofdata), names=[
             'qmin', 'qmax'], values=[
             qmin, qmax])
            dlg.exec_()
            if dlg.result is not None:
                qmin, qmax = dlg.getResult()
            else:
                return
            for dataset_name in listofdata:
                q = numpy.array(self.data_dict[dataset_name].q)
                i = numpy.array(self.data_dict[dataset_name].i)
                error = self.data_dict[dataset_name].error
                if self.data_dict[dataset_name].error is not None:
                    error = numpy.repeat(error, q >= qmin)
                i = numpy.repeat(i, q >= qmin)
                q = numpy.repeat(q, q >= qmin)
                if self.data_dict[dataset_name].error is not None:
                    error = numpy.repeat(error, q <= qmax)
                i = numpy.repeat(i, q <= qmax)
                q = numpy.repeat(q, q <= qmax)
                self.data_dict[dataset_name].q = q
                self.data_dict[dataset_name].i = i
                self.data_dict[dataset_name].error = error
                self.Replot()
                self.printTXT(dataset_name, ' clipped')

            return

    def OnEditScaleQ(self):
        """
        user want to scale q with a formula
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            formula, ok = QtWidgets.QInputDialog.getText(self, 'Formula for q scaling :', 'specify a formula for q scaling', text='1*q')
            formula = str(formula)
            newdataset = label + ' scaled with ' + str(formula)
            q = self.data_dict[label].q
            i = self.data_dict[label].i
            try:
                qout = eval(formula, {'q': q})
            except:
                self.printTXT('error on evaluation of ' + formula)
                return

            qout = numpy.array(qout)
            self.data_dict[newdataset] = dataset(newdataset, qout, i, parent=[label])
            self.redrawTheList()
            self.Replot()
            return

    def OnEditConcatenate(self):
        """
        user want to concatenate different dataset
        """
        listofdata = self.ListOfDatasChecked()
        if len(listofdata) <= 0:
            self.noDataErrorMessage()
        newdatasetname = listofdata[0] + ' new'
        dlg = dlgConcatenate.dlgConcatenate(self, newdatasetname)
        dlg.exec_()

    def OnEditSmooth(self):
        """
        user want to smooth dataset
        ref http://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            pp, ok = QtWidgets.QInputDialog.getText(self, 'pySAXS Smooth parameter :', 'Smooth parameter:')
            if ok:
                if not isNumeric.isNumeric(pp):
                    self.printTXT('value : ' + str(pp) + ' is not a valid numeric')
                    return
                pp = float(str(pp))
                newdatasetname = label + ' smooth'
                self.data_dict[newdatasetname] = self.data_dict[label]._deepcopy()
                self.data_dict[newdatasetname].parent = [label]
                self.data_dict[newdatasetname].name = newdatasetname
                q = self.data_dict[newdatasetname].q
                i = self.data_dict[newdatasetname].i
                tck = interpolate.splrep(q, i, s=pp)
                ysmooth = interpolate.splev(q, tck, der=0)
                self.data_dict[newdatasetname].i = ysmooth
                self.redrawTheList()
                self.Replot()
            return

    def OnEditCalculator(self):
        """
        show the calculator dialog box
        """
        listofdata = self.ListOfDatasChecked()
        if len(listofdata) == 0:
            QtWidgets.QMessageBox.information(self, 'pySAXS', 'No data are selected', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return
        else:
            newdataset = self.giveMeANewName()
            dlg = dlgCalculator.dlgCalculator(self, listofdata, newdataset)
            dlg.exec_()
            return

    def OnEditRemoveDependencies(self):
        """
        remove all dependencies on datasets
        """
        label = self.getCurrentSelectedItem()
        selectedDatas = self.ListOfDatasChecked()
        for name in selectedDatas:
            self.data_dict[name].parent = None
            self.data_dict[name].child = None
            self.data_dict[name].parentformula = None
            self.data_dict[name].variableDict = None

        self.redrawTheList()
        self.Replot()
        return

    def OnEditChangeColor(self):
        """
        user want to change the color
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            initial = self.data_dict[label].color
            if initial is None:
                initial = '#ffffff'
            col = QtWidgets.QColorDialog.getColor(QtGui.QColor(initial))
            self.data_dict[label].color = str(col.name())
            self.Replot()
            return

    def OnEditStat(self):
        """
        user want statistical information
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            q = self.data_dict[label].q
            i = self.data_dict[label].i
            info = ''
            info += 'Statistical information for ' + label + ' : \n'
            info += 'Number of points : ' + str(len(q)) + '\n'
            info += 'x min : ' + str(q[0]) + ', x max : ' + str(q[(len(q) - 1)]) + '\n'
            info += 'y min : ' + str(min(i)) + ' at ' + str(q[numpy.argmin(i)]) + ', y max : ' + str(max(i)) + ' at ' + str(q[numpy.argmax(i)]) + '\n'
            info += 'Mean of y : ' + str(numpy.mean(i)) + ' with standard deviation : ' + str(numpy.std(i)) + '\n'
            dlg = QtWidgets.QMessageBox.information(self, 'pySAXS', info, buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)
            return

    def OnEditGenerateNoise(self):
        """
        user want generate a noise from the data
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            num, ok = QtWidgets.QInputDialog.getDouble(self, 'Noise generator :', 'specify a percent of random noise around the data value', decimals=10)
            if ok:
                percent = float(num)
            else:
                return
            percent = int(percent) / 100.0
            newdataset = label + ' noised with ' + str(percent * 100) + '%'
            q = self.data_dict[label].q
            i = self.data_dict[label].i
            randomarray = numpy.random.rand(len(i)) * 2 - 1
            i = i + i * percent * randomarray
            self.data_dict[newdataset] = dataset(newdataset, q, i, label, type='calculated', parent=[label])
            self.redrawTheList()
            self.Replot()
            return

    def OnEditAddReference(self):
        """
        user want to add a reference value
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            value = 1.0
            num, ok = QtWidgets.QInputDialog.getText(self, 'Add a reference value :', 'specify a value')
            if ok:
                value = float(num)
            else:
                return
            newdataset = 'reference ' + str(value)
            q = self.data_dict[label].q
            ilist = [value] * len(q)
            i = numpy.array(ilist)
            self.data_dict[newdataset] = dataset(newdataset, q, i, label, type='referenceVal')
            self.redrawTheList()
            self.Replot()
            return

    def OnEditSetAsReference(self):
        """
        user want to set a reference 
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            self.data_dict[label].type = 'reference'
            self.referencedata = label
            self.printTXT('reference datas are ', label)
            self.redrawTheList()
            return

    def OnEditSetAsBackground(self):
        """
        user want to set a background 
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            print (
             'set as background : ', label)
            self.data_dict[label].type = 'background'
            self.backgrounddata = label
            self.printTXT('background datas are ', label)
            self.redrawTheList()
            return

    def OnFitPasteModel(self):
        """
        paste model on all checked data set
        """
        if self.pastedModel is None:
            print "we should'nt have this"
            return
        else:
            label = self.getCurrentSelectedItem()
            if label is None:
                self.noDataErrorMessage()
                return
            self.openModel(self.pastedModel._deepcopy(), label, openDialog=False)
            print self.pastedModel
            self.printTXT('model ' + self.pastedModel.Description + ' pasted')
            self.redrawTheList()
            return

    def OnFitCopyModel(self):
        item = self.ui.treeWidget.currentItem()
        if item is None:
            return
        else:
            if not item.isSelected():
                return
            itemParent = item.parent()
            labelParent = str(itemParent.text(0))
            print labelParent
            if self.data_dict[labelParent].model is not None:
                self.OnCopyModel(self.data_dict[labelParent].model)
            return

    def OnCopyModel(self, model):
        """
        get a copy of a model
        """
        self.printTXT('Copy of model : ', model.Description)
        self.pastedModel = model
        self.actionPasteModel.setEnabled(True)

    def OnInfoDataset(self):
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            data = self.data_dict[label]
            child = dlgInfoDataset.dlgInfoDataset(data)
            return

    def redrawTheList(self):
        """
        redraw the listbox
        """
        l = []
        for name in self.data_dict:
            l.append(name)

        l.sort()
        self.ui.treeWidget.clear()
        self.ui.treeWidget.setHeaderLabels(['Datas'])
        treedict = {}
        for name in l:
            item = QtWidgets.QTreeWidgetItem([name])
            item.label = name
            item.internalType = 'data'
            treedict[name] = item
            if self.data_dict[name].checked:
                item.setCheckState(0, QtCore.Qt.Checked)
                item.setBackground(0, QtGui.QColor('#FFEFD5'))
                if self.data_dict[name].color is not None:
                    item.setForeground(0, QtGui.QColor(self.data_dict[name].color))
            else:
                item.setCheckState(0, QtCore.Qt.Unchecked)
                item.setBackground(0, QtCore.Qt.white)
                if self.data_dict[name].color is not None:
                    item.setForeground(0, QtGui.QColor(self.data_dict[name].color))
            if name == self.referencedata:
                item.setBackground(0, QtGui.QColor('#FFB6C1'))
            if name == self.backgrounddata:
                item.setBackground(0, QtGui.QColor('#C3AEAE'))

        for name, item in list(treedict.items()):
            parent = self.data_dict[name].parent
            if parent is not None:
                pere = parent[0]
                if pere in treedict:
                    treedict[pere].addChild(item)
                    treedict[pere].setExpanded(True)
                    item.setExpanded(True)
                    item.setIcon(0, QtGui.QIcon(pySAXS.ICON_PATH + 'arrow_join.png'))
                    self.ui.treeWidget.expandItem(item)
                else:
                    self.ui.treeWidget.addTopLevelItem(item)
            else:
                item.setExpanded(True)
                self.ui.treeWidget.addTopLevelItem(item)
            if self.data_dict[name].parameters is not None:
                lbl = 'Scaling parameters'
                item = QtWidgets.QTreeWidgetItem([lbl])
                item.label = lbl
                item.internalType = 'parameters'
                item.setIcon(0, QtGui.QIcon(pySAXS.ICON_PATH + 'chart_params.png'))
                treedict[name].addChild(item)
                treedict[name].setExpanded(True)
                item.setExpanded(True)
                self.ui.treeWidget.expandItem(item)
            if self.data_dict[name].model is not None:
                lbl = 'Model :' + self.data_dict[name].model.name
                item = QtWidgets.QTreeWidgetItem([lbl])
                item.label = lbl
                item.internalType = 'model'
                item.setIcon(0, QtGui.QIcon(pySAXS.ICON_PATH + 'fit.png'))
                treedict[name].addChild(item)
                treedict[name].setExpanded(True)
                item.setExpanded(True)
                self.ui.treeWidget.expandItem(item)

        self.ui.treeWidget.expandAll()
        self.ui.treeWidget.sortByColumn(0, 0)
        return

    def ReadFile(self, datafilename, file_type=None):
        """
        read file depending of type of file
        """
        name = filetools.getFilename(datafilename)
        f = fileimport.fileImport(file_type)
        q, i, err = f.read(datafilename)
        name = self.cleanString(name)
        self.data_dict[name] = dataset(name, q, i, datafilename, type=type, error=err)
        self.data_dict[name].color = self.colors.getColor()

    def OnItemChanged(self, item, column):
        """
        what's happen when the user chek a box
        """
        label = str(item.text(0))
        if item.internalType == 'model':
            self.actionCopyModel.setEnabled(True)
        else:
            self.actionCopyModel.setEnabled(False)
        if item.internalType != 'data':
            return
        else:
            state = item.checkState(0)
            if self.data_dict[label].checked == state:
                return
            self.ui.treeWidget.setCurrentItem(item)
            if state:
                self.data_dict[label].checked = True
                item.setBackground(0, QtGui.QColor('#FFEFD5'))
                if self.data_dict[label].color is not None:
                    item.setForeground(0, QtGui.QColor(self.data_dict[label].color))
            else:
                self.data_dict[label].checked = False
                item.setBackground(0, QtCore.Qt.white)
            self.Replot()
            if self.DatasetFilename != '':
                self.setWindowTitle('*' + self.DatasetFilename)
            return

    def OnItemDoubleClicked(self, item, column):
        """
        user double clicked on item
        """
        label = str(item.text(0))
        if item.internalType == 'parameters':
            itemParent = item.parent()
            labelParent = str(itemParent.text(0))
            self.childSaxs = dlgAbsoluteI.dlgAbsolute(self, saxsparameters=self.data_dict[labelParent].parameters, datasetname=labelParent, printout=self.printTXT, referencedata=self.referencedata, backgrounddata=self.backgrounddata)
            self.childSaxs.show()
            return
        if item.internalType == 'model':
            itemParent = item.parent()
            labelParent = str(itemParent.text(0))
            self.childmodel = dlgModel.dlgModel(self, labelParent, type='data')
            self.childmodel.show()
            return

    def Replot(self):
        l = self.ListOfDatasChecked()
        if len(l) == 0:
            return
        else:
            for name in l:
                if hasattr(self.data_dict[name], 'parent'):
                    if self.data_dict[name].parent != None:
                        r = self.data_dict[name]._evaluateFromParent(self.data_dict)
                        if r != '' and r is not None:
                            self.printTXT(r)

            i = 0
            if self.plotframe is None:
                self.createPlotframe()
            try:
                self.plotframe.clearData()
            except:
                self.createPlotframe()
                print 'DeadObjectError'

            l = []
            for name in self.data_dict:
                l.append(name)
                l.sort()

            for name in l:
                qexp = self.data_dict[name].q
                iexp = self.data_dict[name].i
                if self.data_dict[name].checked:
                    if self.data_dict[name].color != None:
                        col = self.data_dict[name].color
                    else:
                        col = self.colors.getColor()
                        self.data_dict[name].color = col
                    isModel = self.data_dict[name].model is not None
                    if self.data_dict[name].error is not None:
                        self.plotframe.addData(qexp, iexp, self.data_dict[name].name, id=i, error=self.data_dict[name].error, color=col, model=isModel)
                    else:
                        self.plotframe.addData(qexp, iexp, self.data_dict[name].name, id=i, color=col, model=isModel)
                i = i + 1

            self.plotframe.replot()
            return

    def ListOfDatasChecked(self):
        """
        check if there are data checked
        return list of dataset checked
        """
        keylist = list(self.data_dict.keys())
        keylist.sort()
        l = []
        for name in keylist:
            if self.data_dict[name].checked:
                l.append(name)

        return l

    def ListOfDatasUNChecked(self):
        """
        check if there are data checked
        return list of dataset UNchecked
        """
        keylist = list(self.data_dict.keys())
        keylist.sort()
        l = []
        for name in keylist:
            if not self.data_dict[name].checked:
                l.append(name)

        return l

    def ImportData(self, datafilename, lineskip=0, delimiter='\t', usecols=None, type=None, name=None, errorcol=2, skiprows=0):
        """
        extract data from file
        no more used (8/2015)
        """
        if name == None:
            name = filetools.getFilename(datafilename)
        data = numpy.loadtxt(datafilename, comments='#', skiprows=skiprows, usecols=usecols)
        data = numpy.transpose(numpy.array(data))
        q = data[0]
        i = data[1]
        isnotNan = numpy.where(~numpy.isnan(i))
        q = q[isnotNan]
        i = i[isnotNan]
        if len(data) > errorcol:
            err = data[errorcol]
            err = err[isnotNan]
        else:
            err = None
        name = self.cleanString(name)
        self.data_dict[name] = dataset(name, q, i, datafilename, type=type)
        if errorcol is not None and err is not None:
            self.data_dict[name].error = err
        self.data_dict[name].color = self.colors.getColor()
        return

    def cleanString(self, s):
        """Removes all accents from the string"""
        return unidecode.unidecode(s)

    def printTXT(self, txt='', par=''):
        """
        print on comment ctrl
        """
        self.ui.multitxt.append(str(txt) + str(par))

    def getCurrentSelectedItem(self):
        """
        return the current item selected
        if no item is selected return None
        """
        item = self.ui.treeWidget.currentItem()
        if item is None:
            return
        else:
            if not item.isSelected():
                return
            label = str(item.text(0))
            if label not in self.data_dict:
                return
            return label

    def noDataErrorMessage(self):
        QtWidgets.QMessageBox.information(self, 'pySAXS', 'No datas are selected', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)

    def OnEditFindPeaks(self):
        """
        find peaks
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            i = self.data_dict[label].i
            q = self.data_dict[label].q
            newq = None
            newi = None
            pp = 20
            print 'fp'
            dlg = genericFormDialog.genericFormDialog(title='Find peaks', comment='parameters', names=[
             'Window for scan', 'Peaks height from the background (in percent)'], values=[
             pp, 100.0])
            dlg.exec_()
            print 'exit fp'
            if dlg.result is not None:
                pp, percent = dlg.getResult()
            else:
                return
            founds, newq, newi = DetectPeaks.findPeaks(q, i, pp, percent, self)
            n = len(founds)
            if n > 0:
                for res in founds:
                    self.printTXT('found peak at q=' + str(res[2]) + '\t i=' + str(res[0]) + '\t fwhm=' + str(res[1]))
                    self.plotframe.annotate(res[2], res[0], 'peak at q=' + str(res[2]) + ' i=' + str(res[0]) + '  fwhm=' + str(res[1]))

                self.data_dict[label + ' peaks'] = dataset(label + ' peaks', numpy.array(newq), numpy.array(newi), comment=label + ' peaks', type='calculated', parent=[label])
            self.printTXT(str(n) + ' peaks found ---------')
            self.redrawTheList()
            return

    def OnEditDerivate(self):
        """
        user want to derivate dataset
        """
        label = self.getCurrentSelectedItem()
        if label is None:
            self.noDataErrorMessage()
            return
        else:
            newdatasetname = label + ' derivate'
            self.data_dict[newdatasetname] = self.data_dict[label]._deepcopy()
            self.data_dict[newdatasetname].name = newdatasetname
            q = self.data_dict[newdatasetname].q
            i = self.data_dict[newdatasetname].i
            tck = interpolate.splrep(q, i, s=0)
            yder = interpolate.splev(q, tck, der=1)
            self.data_dict[newdatasetname].i = yder
            self.data_dict[newdatasetname].parent = [label]
            self.redrawTheList()
            self.Replot()
            return

    def NotYetImplemented(self):
        QtWidgets.QMessageBox.information(self, 'PySAXS', 'Not yet implemented', buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.NoButton)

    def giveMeANewName(self):
        """
        return a new name for a data set
        """
        newname = 'newdata'
        i = 0
        while newname in self.data_dict:
            newname = 'newdata' + str(i)
            i += 1

        return newname

    def plugins_list(self, plugins_dirs):
        """ List all python modules in specified plugins folders """
        l = []
        for path in plugins_dirs.split(os.pathsep):
            for filename in os.listdir(path):
                name, ext = os.path.splitext(filename)
                if ext.endswith('.py') and name.startswith('plugin'):
                    if name != 'plugin':
                        l.append(name)

        return l

    def my_import(self, name):
        m = __import__(name)
        for n in name.split('.')[1:]:
            m = getattr(m, n)

        return m

    def setWorkingDirectory(self, filename):
        self.workingdirectory = os.path.dirname(filename)
        self.pref.set('defaultdirectory', self.workingdirectory)
        if self.pref.addRecentFile(filename):
            self.pref.save()
            action = self.ui.menuRecents.addAction(filename)
            item = filename
            action.triggered.connect(partial(self.OnRecentFile, item))
            self.ui.menuFile.addAction(self.ui.menuRecents.menuAction())

    def getWorkingDirectory(self):
        return self.workingdirectory

    def getListOfDocs(self):
        p = path.dirname(pySAXS.__file__)
        l = filetools.listFiles(p + os.sep + 'doc', '*.*')
        return l

    def OnOpenDocument(self, name, val):
        """
        start the default application for the doc file
        """
        if os.name == 'nt':
            os.startfile('%s' % name)
        elif os.name == 'posix':
            os.system('/usr/bin/xdg-open %s' % name)

    def OnHelpChanges(self):
        """
        start the changes dlg
        """
        file = pySAXS.__path__[0] + os.sep + 'CHANGELOG.txt'
        child = dlgTextView.ViewMessage(file, 'Changes ' + pySAXS.__version__ + pySAXS.__subversion__, parent=self)
        child.exec_()

    def OnHelpAbout(self):
        """
        start the about dlg
        """
        splash = showSplash()
        file = pySAXS.__path__[0] + os.sep + 'ABOUT.txt'
        child = dlgTextView.ViewMessage(file, 'About ' + pySAXS.__version__ + pySAXS.__subversion__, parent=self)
        child.exec_()

    def OnHelpLicense(self):
        """
        start the about dlg
        """
        file = pySAXS.__path__[0] + os.sep + 'LICENSE.txt'
        child = dlgTextView.ViewMessage(file, 'License', parent=self)
        child.exec_()

    def OnToolsAbsorption(self):
        """
        start the absorption tool with XRlib
        """
        dlg = dlgAbsorption.dlgAbsorption(self, printout=self.printTXT)
        dlg.exec_()

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            filenames = []
            url = QtCore.QUrl()
            for url in mimeData.urls():
                f = str(url.path())[1:]
                filenames.append(f)

            self.OnFileOpen(filenames=filenames)


def showSplash():
    splash_file = pySAXS.__path__[0] + os.sep + 'guisaxs' + os.sep + 'images' + os.sep + 'splash.png'
    splash_pix = QtGui.QPixmap(splash_file)
    splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash_font = splash.font()
    splash_font.setPixelSize(20)
    splash.setFont(splash_font)
    splash.setMask(splash_pix.mask())
    messg = 'version : ' + pySAXS.__version__ + pySAXS.__subversion__
    messg += '   Python : ' + str(sys.version.split()[0])
    splash.showMessage(messg, color=QtCore.Qt.white, alignment=QtCore.Qt.AlignBottom)
    splash.show()
    return splash


def main():
    from pySAXS.guisaxs.qt.mainGuisaxs import showSplash
    app = QtWidgets.QApplication(sys.argv)
    splash = showSplash()
    app.processEvents()
    from pySAXS.guisaxs.qt import mainGuisaxs
    myapp = mainGuisaxs.mainGuisaxs(splashScreen=splash)
    myapp.show()
    splash.destroy()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()