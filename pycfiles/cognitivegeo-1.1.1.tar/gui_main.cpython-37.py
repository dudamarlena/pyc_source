# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:/Users/HDi/Google Drive/ProgramCodes/Released/PyPI/cognitivegeo\cognitivegeo\src\gui\gui_main.py
# Compiled at: 2020-01-05 11:35:40
# Size of source mod 2**32: 101199 bytes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np, os, sys, shutil, webbrowser
sys.path.append(os.path.dirname(__file__)[:-4][:-4][:-13])
import cognitivegeo.src.seismic.analysis as seis_ays
import cognitivegeo.src.psseismic.analysis as psseis_ays
import cognitivegeo.src.pointset.analysis as point_ays
import cognitivegeo.src.core.settings as core_set
import cognitivegeo.src.vis.messager as vis_msg
import cognitivegeo.src.gui.importsurveymanual as gui_importsurveymanual
import cognitivegeo.src.gui.importsurveysegy as gui_importsurveysegy
import cognitivegeo.src.gui.importseissegy as gui_importseissegy
import cognitivegeo.src.gui.importseisimageset as gui_importseisimageset
import cognitivegeo.src.gui.importpsseissegy as gui_importpsseissegy
import cognitivegeo.src.gui.importpsseisimageset as gui_importpsseisimageset
import cognitivegeo.src.gui.importpointsetfile as gui_importpointsetfile
import cognitivegeo.src.gui.exportsurvey as gui_exportsurvey
import cognitivegeo.src.gui.exportseissegy as gui_exportseissegy
import cognitivegeo.src.gui.exportseisnpy as gui_exportseisnpy
import cognitivegeo.src.gui.exportseisimageset as gui_exportseisimageset
import cognitivegeo.src.gui.exportpsseisnpy as gui_exportpsseisnpy
import cognitivegeo.src.gui.exportpointsetfile as gui_exportpointsetfile
import cognitivegeo.src.gui.exportpointsetnpy as gui_exportpointsetnpy
import cognitivegeo.src.gui.managesurvey as gui_managesurvey
import cognitivegeo.src.gui.manageseis as gui_manageseis
import cognitivegeo.src.gui.managepsseis as gui_managepsseis
import cognitivegeo.src.gui.managepointset as gui_managepointset
import cognitivegeo.src.gui.convertseis2pointset as gui_convertseis2pointset
import cognitivegeo.src.gui.convertpointset2seis as gui_convertpointset2seis
import cognitivegeo.src.gui.convertseis2psseis as gui_convertseis2psseis
import cognitivegeo.src.gui.convertpsseis2seis as gui_convertpsseis2seis
import cognitivegeo.src.gui.calcmathattribsingle as gui_calcmathattribsingle
import cognitivegeo.src.gui.calcmathattribmultiple as gui_calcmathattribmultiple
import cognitivegeo.src.gui.calcinstanattrib as gui_calcinstanattrib
import cognitivegeo.src.gui.plotviscanvas as gui_plotviscanvas
import cognitivegeo.src.gui.plotvis1dseisz as gui_plotvis1dseisz
import cognitivegeo.src.gui.plotvis1dseisfreq as gui_plotvis1dseisfreq
import cognitivegeo.src.gui.plotvis2dseisinl as gui_plotvis2dseisinl
import cognitivegeo.src.gui.plotvis2dseisxl as gui_plotvis2dseisxl
import cognitivegeo.src.gui.plotvis2dseisz as gui_plotvis2dseisz
import cognitivegeo.src.gui.plotvis2dpsseisshot as gui_plotvis2dpsseisshot
import cognitivegeo.src.gui.plotvis2dpointsetcrossplt as gui_plotvis2dpointsetcrossplt
import cognitivegeo.src.gui.plotvis3dseisinlxlz as gui_plotvis3dseisinlxlz
import cognitivegeo.src.gui.settingsgui as gui_settingsgui
import cognitivegeo.src.gui.settingsgeneral as gui_settingsgeneral
import cognitivegeo.src.gui.settingsvisual as gui_settingsvisual
import cognitivegeo.src.gui.settingsviewer as gui_settingsviewer
import cognitivegeo.src.gui.about as gui_about
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
__all__ = [
 'start']

class mainwindow(object):
    projname = 'New project'
    projpath = ''
    survinfo = {}
    seisdata = {}
    psseisdata = {}
    pointsetdata = {}
    settings = core_set.Settings
    iconpath = os.path.dirname(__file__)
    dialog = None

    def setupGUI(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.setFixedSize(900, 560)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/logo.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName('menubar')
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 50))
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName('statusbar')
        self.toolbarleft = QtWidgets.QToolBar(MainWindow)
        self.toolbarleft.setObjectName('toolbarleft')
        self.toolbarleft.setGeometry(QtCore.QRect(0, 75, 50, 425))
        self.toolbarright = QtWidgets.QToolBar(MainWindow)
        self.toolbarright.setObjectName('toolbarright')
        self.toolbarright.setGeometry(QtCore.QRect(850, 75, 50, 425))
        self.toolbartop = QtWidgets.QToolBar(MainWindow)
        self.toolbartop.setObjectName('toolbartop')
        self.toolbartop.setGeometry(QtCore.QRect(0, 25, 900, 50))
        self.toolbarbottom = QtWidgets.QToolBar(MainWindow)
        self.toolbarbottom.setObjectName('toolbarbottom')
        self.toolbarbottom.setGeometry(QtCore.QRect(0, 500, 900, 50))
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName('menufile')
        self.menumanage = QtWidgets.QMenu(self.menubar)
        self.menumanage.setObjectName('menumanage')
        self.menutool = QtWidgets.QMenu(self.menubar)
        self.menutool.setObjectName('menutool')
        self.menuvis = QtWidgets.QMenu(self.menubar)
        self.menuvis.setObjectName('menuvis')
        self.menuutil = QtWidgets.QMenu(self.menubar)
        self.menuutil.setObjectName('menuutil')
        self.menuhelp = QtWidgets.QMenu(self.menubar)
        self.menuhelp.setObjectName('menuhelp')
        MainWindow.setMenuBar(self.menubar)
        MainWindow.setStatusBar(self.statusbar)
        self.actionnewproject = QtWidgets.QAction(MainWindow)
        self.actionnewproject.setObjectName('actionnewproject')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/new.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionnewproject.setIcon(icon)
        self.actionopenproject = QtWidgets.QAction(MainWindow)
        self.actionopenproject.setObjectName('actionopenproject')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/folder.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionopenproject.setIcon(icon)
        self.actionsaveproject = QtWidgets.QAction(MainWindow)
        self.actionsaveproject.setObjectName('actionsaveproject')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/disk.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionsaveproject.setIcon(icon)
        self.actionsaveasproject = QtWidgets.QAction(MainWindow)
        self.actionsaveasproject.setObjectName('actionsaveasproject')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/diskwithpen.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionsaveasproject.setIcon(icon)
        self.menuimport = QtWidgets.QMenu(self.menufile)
        self.menuimport.setObjectName('menuimport')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/import.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuimport.setIcon(icon)
        self.menuimportsurvey = QtWidgets.QMenu(self.menuimport)
        self.menuimportsurvey.setObjectName('menuimportsurvey')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/survey.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuimportsurvey.setIcon(icon)
        self.actionimportsurveymanual = QtWidgets.QAction(MainWindow)
        self.actionimportsurveymanual.setObjectName('actionimportsurveymanual')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/supervised.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionimportsurveymanual.setIcon(icon)
        self.actionimportsurveysegy = QtWidgets.QAction(MainWindow)
        self.actionimportsurveysegy.setObjectName('actionimportsurveysegy')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/segy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionimportsurveysegy.setIcon(icon)
        self.actionimportsurveynpy = QtWidgets.QAction(MainWindow)
        self.actionimportsurveynpy.setObjectName('actionimportsurveynpy')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/numpy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionimportsurveynpy.setIcon(icon)
        self.menuimportseis = QtWidgets.QMenu(self.menuimport)
        self.menuimportseis.setObjectName('menuimportseis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/seismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuimportseis.setIcon(icon)
        self.actionimportseissegy = QtWidgets.QAction(MainWindow)
        self.actionimportseissegy.setObjectName('actionimportseissegy')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/segy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionimportseissegy.setIcon(icon)
        self.actionimportseisnpy = QtWidgets.QAction(MainWindow)
        self.actionimportseisnpy.setObjectName('actionimportseisnpy')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/numpy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionimportseisnpy.setIcon(icon)
        self.actionimportseisimageset = QtWidgets.QAction(MainWindow)
        self.actionimportseisimageset.setObjectName('actionimportseisimageset')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/image.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionimportseisimageset.setIcon(icon)
        self.menuimportpsseis = QtWidgets.QMenu(self.menuimport)
        self.menuimportpsseis.setObjectName('menuimportpsseis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/psseismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuimportpsseis.setIcon(icon)
        self.actionimportpsseissegy = QtWidgets.QAction(MainWindow)
        self.actionimportpsseissegy.setObjectName('actionimportpsseissegy')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/segy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionimportpsseissegy.setIcon(icon)
        self.actionimportpsseisnpy = QtWidgets.QAction(MainWindow)
        self.actionimportpsseisnpy.setObjectName('actionimportpsseisnpy')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/numpy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionimportpsseisnpy.setIcon(icon)
        self.actionimportpsseisimageset = QtWidgets.QAction(MainWindow)
        self.actionimportpsseisimageset.setObjectName('actionimportpsseisimageset')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/image.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionimportpsseisimageset.setIcon(icon)
        self.menuimportpointset = QtWidgets.QMenu(self.menuimport)
        self.menuimportpointset.setObjectName('menuimportpointset')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/point.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuimportpointset.setIcon(icon)
        self.actionimportpointsetfile = QtWidgets.QAction(MainWindow)
        self.actionimportpointsetfile.setObjectName('actionimportpointsetfile')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/copy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionimportpointsetfile.setIcon(icon)
        self.actionimportpointsetnpy = QtWidgets.QAction(MainWindow)
        self.actionimportpointsetnpy.setObjectName('actionimportpointsetnpy')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/numpy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionimportpointsetnpy.setIcon(icon)
        self.menuexport = QtWidgets.QMenu(self.menufile)
        self.menuexport.setObjectName('menuexport')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/export.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuexport.setIcon(icon)
        self.actionexportsurvey = QtWidgets.QAction(MainWindow)
        self.actionexportsurvey.setObjectName('actionexportsurvey')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/survey.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionexportsurvey.setIcon(icon)
        self.menuexportseis = QtWidgets.QMenu(self.menuexport)
        self.menuexportseis.setObjectName('menuexportseis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/seismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuexportseis.setIcon(icon)
        self.actionexportseissegy = QtWidgets.QAction(MainWindow)
        self.actionexportseissegy.setObjectName('actionexportseissegy')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/segy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionexportseissegy.setIcon(icon)
        self.actionexportseisnpy = QtWidgets.QAction(MainWindow)
        self.actionexportseisnpy.setObjectName('actionexportseisnpy')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/numpy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionexportseisnpy.setIcon(icon)
        self.actionexportseisimageset = QtWidgets.QAction(MainWindow)
        self.actionexportseisimageset.setObjectName('actionexportseisimageset')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/image.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionexportseisimageset.setIcon(icon)
        self.menuexportpsseis = QtWidgets.QMenu(self.menuexport)
        self.menuexportpsseis.setObjectName('menuexportpsseis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/psseismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuexportpsseis.setIcon(icon)
        self.actionexportpsseisnpy = QtWidgets.QAction(MainWindow)
        self.actionexportpsseisnpy.setObjectName('actionexportpsseisnpy')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/numpy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionexportpsseisnpy.setIcon(icon)
        self.menuexportpointset = QtWidgets.QMenu(self.menuimport)
        self.menuexportpointset.setObjectName('menuexportpointset')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/point.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuexportpointset.setIcon(icon)
        self.actionexportpointsetfile = QtWidgets.QAction(MainWindow)
        self.actionexportpointsetfile.setObjectName('actionexportpointsetfile')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/copy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionexportpointsetfile.setIcon(icon)
        self.actionexportpointsetnpy = QtWidgets.QAction(MainWindow)
        self.actionexportpointsetnpy.setObjectName('actionexportpointsetnpy')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/numpy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionexportpointsetnpy.setIcon(icon)
        self.actionquit = QtWidgets.QAction(MainWindow)
        self.actionquit.setObjectName('actionquit')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/close.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionquit.setIcon(icon)
        self.actionmanagesurvey = QtWidgets.QAction(MainWindow)
        self.actionmanagesurvey.setObjectName('actionmanagesurvey')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/survey.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionmanagesurvey.setIcon(icon)
        self.actionmanageseis = QtWidgets.QAction(MainWindow)
        self.actionmanageseis.setObjectName('actionmanageseis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/seismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionmanageseis.setIcon(icon)
        self.actionmanagepsseis = QtWidgets.QAction(MainWindow)
        self.actionmanagepsseis.setObjectName('actionmanagepsseis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/psseismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionmanagepsseis.setIcon(icon)
        self.actionmanagepointset = QtWidgets.QAction(MainWindow)
        self.actionmanagepointset.setObjectName('actionmanagepointset')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/point.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionmanagepointset.setIcon(icon)
        self.menudataconversion = QtWidgets.QMenu(self.menutool)
        self.menudataconversion.setObjectName('menudataconversion')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/exchange.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menudataconversion.setIcon(icon)
        self.actionconvertseis2pointset = QtWidgets.QAction(MainWindow)
        self.actionconvertseis2pointset.setObjectName('actionconvertseis2pointset')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/seismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionconvertseis2pointset.setIcon(icon)
        self.actionconvertpointset2seis = QtWidgets.QAction(MainWindow)
        self.actionconvertpointset2seis.setObjectName('actionconvertpointset2seis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/point.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionconvertpointset2seis.setIcon(icon)
        self.actionconvertseis2psseis = QtWidgets.QAction(MainWindow)
        self.actionconvertseis2psseis.setObjectName('actionconvertseis2psseis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/seismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionconvertseis2psseis.setIcon(icon)
        self.actionconvertpsseis2seis = QtWidgets.QAction(MainWindow)
        self.actionconvertpsseis2seis.setObjectName('actionconvertpsseis2seis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/psseismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionconvertpsseis2seis.setIcon(icon)
        self.menuattribengine = QtWidgets.QMenu(self.menutool)
        self.menuattribengine.setObjectName('menuattribengine')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/attribute.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuattribengine.setIcon(icon)
        self.menumathattrib = QtWidgets.QMenu(self.menuattribengine)
        self.menumathattrib.setObjectName('menumathattrib')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/math.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menumathattrib.setIcon(icon)
        self.actioncalcmathattribsingle = QtWidgets.QAction(MainWindow)
        self.actioncalcmathattribsingle.setObjectName('actioncalcmathattribsingle')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/file.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actioncalcmathattribsingle.setIcon(icon)
        self.actioncalcmathattribmultiple = QtWidgets.QAction(MainWindow)
        self.actioncalcmathattribmultiple.setObjectName('actioncalcmathattribmultiple')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/copy.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actioncalcmathattribmultiple.setIcon(icon)
        self.actioncalcinstanattrib = QtWidgets.QAction(MainWindow)
        self.actioncalcinstanattrib.setObjectName('actioncalcinstanattrib')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/hilbert.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actioncalcinstanattrib.setIcon(icon)
        self.actionplotviscanvas = QtWidgets.QAction(MainWindow)
        self.actionplotviscanvas.setObjectName('actionplotviscanvas')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/canvas.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionplotviscanvas.setIcon(icon)
        self.menu1dwindow = QtWidgets.QMenu(self.menuvis)
        self.menu1dwindow.setObjectName('menu1dwindow')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/vis1d.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu1dwindow.setIcon(icon)
        self.menu1dwindowseis = QtWidgets.QMenu(self.menu1dwindow)
        self.menu1dwindowseis.setObjectName('menu1dwindowseis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/seismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu1dwindowseis.setIcon(icon)
        self.actionplotvis1dseisz = QtWidgets.QAction(MainWindow)
        self.actionplotvis1dseisz.setObjectName('actionplotvis1dseisz')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/waveform.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionplotvis1dseisz.setIcon(icon)
        self.actionplotvis1dseisfreq = QtWidgets.QAction(MainWindow)
        self.actionplotvis1dseisfreq.setObjectName('actionplotvis1dseisfreq')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/plotcurve.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionplotvis1dseisfreq.setIcon(icon)
        self.menu2dwindow = QtWidgets.QMenu(self.menuvis)
        self.menu2dwindow.setObjectName('menu2dwindow')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/vis2d.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu2dwindow.setIcon(icon)
        self.menu2dwindowseis = QtWidgets.QMenu(self.menu2dwindow)
        self.menu2dwindowseis.setObjectName('menu2dwindowseis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/seismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu2dwindowseis.setIcon(icon)
        self.actionplotvis2dseisinl = QtWidgets.QAction(MainWindow)
        self.actionplotvis2dseisinl.setObjectName('actionplotvis2dseisinl')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/visinl.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionplotvis2dseisinl.setIcon(icon)
        self.actionplotvis2dseisxl = QtWidgets.QAction(MainWindow)
        self.actionplotvis2dseisxl.setObjectName('actionplotvis2dseisxl')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/visxl.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionplotvis2dseisxl.setIcon(icon)
        self.actionplotvis2dseisz = QtWidgets.QAction(MainWindow)
        self.actionplotvis2dseisz.setObjectName('actionplotvis2dseisz')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/visz.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionplotvis2dseisz.setIcon(icon)
        self.menu2dwindowpsseis = QtWidgets.QMenu(self.menu2dwindow)
        self.menu2dwindowpsseis.setObjectName('menu2dwindowpsseis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/psseismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu2dwindowpsseis.setIcon(icon)
        self.actionplotvis2dpsseisshot = QtWidgets.QAction(MainWindow)
        self.actionplotvis2dpsseisshot.setObjectName('actionplotvis2dpsseisshot')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/gather.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionplotvis2dpsseisshot.setIcon(icon)
        self.menu2dwindowpointset = QtWidgets.QMenu(self.menu2dwindow)
        self.menu2dwindowpointset.setObjectName('menu2dwindowpointset')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/point.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu2dwindowpointset.setIcon(icon)
        self.actionplotvis2dpointsetcrossplt = QtWidgets.QAction(MainWindow)
        self.actionplotvis2dpointsetcrossplt.setObjectName('actionplotvis2dpointsetcrossplt')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/plotpoint.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionplotvis2dpointsetcrossplt.setIcon(icon)
        self.menu3dwindow = QtWidgets.QMenu(self.menuvis)
        self.menu3dwindow.setObjectName('menu3dwindow')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/vis3d.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu3dwindow.setIcon(icon)
        self.menu3dwindowseis = QtWidgets.QMenu(self.menu3dwindow)
        self.menu3dwindowseis.setObjectName('menu3dwindowseis')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/seismic.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menu3dwindowseis.setIcon(icon)
        self.actionplotvis3dseisinlxlz = QtWidgets.QAction(MainWindow)
        self.actionplotvis3dseisinlxlz.setObjectName('actionplotvis3dseisinlxlz')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/box.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionplotvis3dseisinlxlz.setIcon(icon)
        self.menusettings = QtWidgets.QMenu(self.menuutil)
        self.menusettings.setObjectName('menusettings')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menusettings.setIcon(icon)
        self.actionsettingsgui = QtWidgets.QAction(MainWindow)
        self.actionsettingsgui.setObjectName('actionsettingsgui')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/logo.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionsettingsgui.setIcon(icon)
        self.actionsettingsgeneral = QtWidgets.QAction(MainWindow)
        self.actionsettingsgeneral.setObjectName('actionsettingsgeneral')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/settings.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionsettingsgeneral.setIcon(icon)
        self.actionsettingsvisual = QtWidgets.QAction(MainWindow)
        self.actionsettingsvisual.setObjectName('actionsettingsvisual')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/image.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionsettingsvisual.setIcon(icon)
        self.actionsettingsviewer = QtWidgets.QAction(MainWindow)
        self.actionsettingsviewer.setObjectName('actionsettingsviewer')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/dice.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionsettingsviewer.setIcon(icon)
        self.actionmanual = QtWidgets.QAction(MainWindow)
        self.actionmanual.setObjectName('actionmanual')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/manual.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionmanual.setIcon(icon)
        self.actionsupport = QtWidgets.QAction(MainWindow)
        self.actionsupport.setObjectName('actionsupport')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/support.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionsupport.setIcon(icon)
        self.actionabout = QtWidgets.QAction(MainWindow)
        self.actionabout.setObjectName('actionabout')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/about.png')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionabout.setIcon(icon)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menumanage.menuAction())
        self.menubar.addAction(self.menutool.menuAction())
        self.menubar.addAction(self.menuvis.menuAction())
        self.menubar.addAction(self.menuutil.menuAction())
        self.menubar.addAction(self.menuhelp.menuAction())
        self.menufile.addAction(self.actionnewproject)
        self.menufile.addAction(self.actionopenproject)
        self.menufile.addAction(self.actionsaveproject)
        self.menufile.addAction(self.actionsaveasproject)
        self.menufile.addSeparator()
        self.menufile.addAction(self.menuimport.menuAction())
        self.menuimport.addAction(self.menuimportsurvey.menuAction())
        self.menuimportsurvey.addAction(self.actionimportsurveymanual)
        self.menuimportsurvey.addAction(self.actionimportsurveysegy)
        self.menuimportsurvey.addAction(self.actionimportsurveynpy)
        self.menuimport.addSeparator()
        self.menuimport.addAction(self.menuimportseis.menuAction())
        self.menuimportseis.addAction(self.actionimportseissegy)
        self.menuimportseis.addAction(self.actionimportseisnpy)
        self.menuimportseis.addAction(self.actionimportseisimageset)
        self.menuimport.addAction(self.menuimportpsseis.menuAction())
        self.menuimportpsseis.addAction(self.actionimportpsseissegy)
        self.menuimportpsseis.addAction(self.actionimportpsseisnpy)
        self.menuimportpsseis.addAction(self.actionimportpsseisimageset)
        self.menuimport.addSeparator()
        self.menuimport.addAction(self.menuimportpointset.menuAction())
        self.menuimportpointset.addAction(self.actionimportpointsetfile)
        self.menuimportpointset.addAction(self.actionimportpointsetnpy)
        self.menufile.addAction(self.menuexport.menuAction())
        self.menuexport.addAction(self.actionexportsurvey)
        self.menuexport.addSeparator()
        self.menuexport.addAction(self.menuexportseis.menuAction())
        self.menuexportseis.addAction(self.actionexportseissegy)
        self.menuexportseis.addAction(self.actionexportseisnpy)
        self.menuexportseis.addAction(self.actionexportseisimageset)
        self.menuexport.addAction(self.menuexportpsseis.menuAction())
        self.menuexportpsseis.addAction(self.actionexportpsseisnpy)
        self.menuexport.addSeparator()
        self.menuexport.addAction(self.menuexportpointset.menuAction())
        self.menuexportpointset.addAction(self.actionexportpointsetfile)
        self.menuexportpointset.addAction(self.actionexportpointsetnpy)
        self.menufile.addSeparator()
        self.menufile.addAction(self.actionquit)
        self.menumanage.addAction(self.actionmanagesurvey)
        self.menumanage.addSeparator()
        self.menumanage.addAction(self.actionmanageseis)
        self.menumanage.addAction(self.actionmanagepsseis)
        self.menumanage.addAction(self.actionmanagepointset)
        self.menutool.addAction(self.menudataconversion.menuAction())
        self.menudataconversion.addAction(self.actionconvertseis2pointset)
        self.menudataconversion.addAction(self.actionconvertpointset2seis)
        self.menudataconversion.addSeparator()
        self.menudataconversion.addAction(self.actionconvertseis2psseis)
        self.menudataconversion.addAction(self.actionconvertpsseis2seis)
        self.menutool.addSeparator()
        self.menutool.addAction(self.menuattribengine.menuAction())
        self.menuattribengine.addAction(self.menumathattrib.menuAction())
        self.menumathattrib.addAction(self.actioncalcmathattribsingle)
        self.menumathattrib.addAction(self.actioncalcmathattribmultiple)
        self.menuattribengine.addAction(self.actioncalcinstanattrib)
        self.menuvis.addAction(self.actionplotviscanvas)
        self.menuvis.addSeparator()
        self.menuvis.addAction(self.menu1dwindow.menuAction())
        self.menuvis.addSeparator()
        self.menuvis.addAction(self.menu2dwindow.menuAction())
        self.menuvis.addSeparator()
        self.menuvis.addAction(self.menu3dwindow.menuAction())
        self.menu1dwindow.addAction(self.menu1dwindowseis.menuAction())
        self.menu1dwindowseis.addAction(self.actionplotvis1dseisz)
        self.menu1dwindowseis.addAction(self.actionplotvis1dseisfreq)
        self.menu2dwindow.addAction(self.menu2dwindowseis.menuAction())
        self.menu2dwindowseis.addAction(self.actionplotvis2dseisinl)
        self.menu2dwindowseis.addAction(self.actionplotvis2dseisxl)
        self.menu2dwindowseis.addAction(self.actionplotvis2dseisz)
        self.menu2dwindow.addAction(self.menu2dwindowpsseis.menuAction())
        self.menu2dwindowpsseis.addAction(self.actionplotvis2dpsseisshot)
        self.menu2dwindow.addAction(self.menu2dwindowpointset.menuAction())
        self.menu2dwindowpointset.addAction(self.actionplotvis2dpointsetcrossplt)
        self.menu3dwindow.addAction(self.menu3dwindowseis.menuAction())
        self.menu3dwindowseis.addAction(self.actionplotvis3dseisinlxlz)
        self.menuutil.addAction(self.menusettings.menuAction())
        self.menusettings.addAction(self.actionsettingsgui)
        self.menusettings.addAction(self.actionsettingsgeneral)
        self.menusettings.addAction(self.actionsettingsvisual)
        self.menusettings.addAction(self.actionsettingsviewer)
        self.menuhelp.addAction(self.actionmanual)
        self.menuhelp.addAction(self.actionsupport)
        self.menuhelp.addSeparator()
        self.menuhelp.addAction(self.actionabout)
        self.toolbarleft.setOrientation(QtCore.Qt.Vertical)
        self.toolbarleft.addAction(self.menuimport.menuAction())
        self.toolbarleft.addSeparator()
        self.toolbarleft.addAction(self.menuexport.menuAction())
        self.toolbarright.setOrientation(QtCore.Qt.Vertical)
        self.toolbarright.addAction(self.menudataconversion.menuAction())
        self.toolbarright.addSeparator()
        self.toolbarright.addAction(self.menuattribengine.menuAction())
        self.toolbartop.addAction(self.actionmanagesurvey)
        self.toolbartop.addSeparator()
        self.toolbartop.addAction(self.actionmanageseis)
        self.toolbartop.addAction(self.actionmanagepsseis)
        self.toolbartop.addAction(self.actionmanagepointset)
        self.toolbarbottom.addAction(self.actionplotviscanvas)
        self.toolbarbottom.addSeparator()
        self.toolbarbottom.addAction(self.actionplotvis1dseisz)
        self.toolbarbottom.addSeparator()
        self.toolbarbottom.addAction(self.actionplotvis2dpointsetcrossplt)
        self.msgbox = QtWidgets.QMessageBox(MainWindow)
        self.msgbox.setObjectName('msgbox')
        _center_x = MainWindow.geometry().center().x()
        _center_y = MainWindow.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))
        self.bkimage = QtWidgets.QLabel(MainWindow)
        self.bkimage.setObjectName('bkimage')
        self.bkimage.setGeometry(QtCore.QRect(100, 130, 700, 300))
        self.retranslateGUI(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateGUI(self, MainWindow):
        self.dialog = MainWindow
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate('MainWindow', 'CognitiveGeo <' + self.projname + '>'))
        self.menufile.setTitle(_translate('MainWindow', '&File'))
        self.menumanage.setTitle(_translate('MainWindow', 'Manage'))
        self.menutool.setTitle(_translate('MainWindow', 'Toolbox'))
        self.menuvis.setTitle(_translate('MainWindow', 'Visualization'))
        self.menuutil.setTitle(_translate('MainWindow', 'Utilities'))
        self.menuhelp.setTitle(_translate('MainWindow', '&Help'))
        self.actionnewproject.setText(_translate('MainWindow', 'New Project'))
        self.actionopenproject.setText(_translate('MainWindow', 'Open Project'))
        self.actionsaveproject.setText(_translate('MainWindow', 'Save Project'))
        self.actionsaveasproject.setText(_translate('MainWindow', 'Save Project as'))
        self.menuimport.setTitle(_translate('MainWindow', 'Import'))
        self.menuimportsurvey.setTitle(_translate('MainWindow', 'Survey'))
        self.actionimportsurveymanual.setText(_translate('MainWindow', 'Create'))
        self.actionimportsurveysegy.setText(_translate('MainWindow', 'SEG-Y'))
        self.actionimportsurveynpy.setText(_translate('MainWindow', 'NumPy'))
        self.menuimportseis.setTitle(_translate('MainWindow', 'Seismic'))
        self.actionimportseissegy.setText(_translate('MainWindow', 'SEG-Y'))
        self.actionimportseisnpy.setText(_translate('MainWindow', 'NumPy'))
        self.actionimportseisnpy.setToolTip('Import Seismic from NumPy')
        self.actionimportseisimageset.setText(_translate('MainWindow', 'ImageSet'))
        self.menuimportpsseis.setTitle(_translate('MainWindow', 'Pre-stack Seismic'))
        self.actionimportpsseissegy.setText(_translate('MainWindow', 'SEG-Y'))
        self.actionimportpsseisnpy.setText(_translate('MainWindow', 'NumPy'))
        self.actionimportpsseisimageset.setText(_translate('MainWindow', 'ImageSet'))
        self.menuimportpointset.setTitle(_translate('MainWindow', 'PointSet'))
        self.actionimportpointsetfile.setText(_translate('MainWindow', 'Ascii File'))
        self.actionimportpointsetnpy.setText(_translate('MainWindow', 'NumPy'))
        self.menuexport.setTitle(_translate('MainWindow', 'Export'))
        self.actionexportsurvey.setText(_translate('MainWindow', 'Survey'))
        self.menuexportseis.setTitle(_translate('MainWindow', 'Seismic'))
        self.actionexportseissegy.setText(_translate('MainWindow', 'SEG-Y'))
        self.actionexportseisnpy.setText(_translate('MainWindow', 'NumPy'))
        self.actionexportseisimageset.setText(_translate('MainWindow', 'ImageSet'))
        self.menuexportpsseis.setTitle(_translate('MainWindow', 'Pre-stack Seismic'))
        self.actionexportpsseisnpy.setText(_translate('MainWindow', 'NumPy'))
        self.menuexportpointset.setTitle(_translate('MainWindow', 'PointSet'))
        self.actionexportpointsetfile.setText(_translate('MainWindow', 'Ascii File'))
        self.actionexportpointsetnpy.setText(_translate('MainWindow', 'NumPy'))
        self.actionquit.setText(_translate('MainWindow', 'Quit'))
        self.actionnewproject.setShortcut(QtGui.QKeySequence('Ctrl+N'))
        self.actionopenproject.setShortcut(QtGui.QKeySequence('Ctrl+O'))
        self.actionsaveproject.setShortcut(QtGui.QKeySequence('Ctrl+S'))
        self.actionimportseisnpy.setShortcut(QtGui.QKeySequence('Ctrl+M'))
        self.actionimportpsseisnpy.setShortcut(QtGui.QKeySequence('Ctrl+G'))
        self.actionimportpointsetnpy.setShortcut(QtGui.QKeySequence('Ctrl+P'))
        self.actionquit.setShortcut(QtGui.QKeySequence('Ctrl+Q'))
        self.actionmanagesurvey.setText(_translate('MainWindow', 'Survey'))
        self.actionmanagesurvey.setToolTip('Manage Seismic Survey')
        self.actionmanageseis.setText(_translate('MainWindow', 'Seismic'))
        self.actionmanageseis.setToolTip('Manage Seismic')
        self.actionmanagepsseis.setText(_translate('MainWindow', 'Pre-stack Seismic'))
        self.actionmanagepsseis.setToolTip('Manage Pre-stack Seismic')
        self.actionmanagepointset.setText(_translate('MainWindow', 'PointSet'))
        self.actionmanagepointset.setToolTip('Manage PointSets')
        self.actionmanagesurvey.setShortcut(QtGui.QKeySequence('Shift+V'))
        self.actionmanageseis.setShortcut(QtGui.QKeySequence('Shift+M'))
        self.actionmanagepsseis.setShortcut(QtGui.QKeySequence('Shift+G'))
        self.actionmanagepointset.setShortcut(QtGui.QKeySequence('Shift+P'))
        self.menudataconversion.setTitle(_translate('MainWindow', 'Data conversion'))
        self.actionconvertseis2pointset.setText(_translate('MainWindow', 'Seismic --> PointSet'))
        self.actionconvertpointset2seis.setText(_translate('MainWindow', 'PointSet --> Seismic'))
        self.actionconvertseis2psseis.setText(_translate('MainWindow', 'Seismic --> Pre-stack'))
        self.actionconvertpsseis2seis.setText(_translate('MainWindow', 'Pre-stack --> Seismic'))
        self.menuattribengine.setTitle(_translate('MainWindow', 'Seismic attribute'))
        self.menumathattrib.setTitle(_translate('MainWindow', 'Mathematical'))
        self.actioncalcmathattribsingle.setText(_translate('MainWindow', 'from Single property'))
        self.actioncalcmathattribmultiple.setText(_translate('MainWindow', 'between Multiple properties'))
        self.actioncalcinstanattrib.setText(_translate('MainWindow', 'Instantaneous'))
        self.actionplotviscanvas.setText(_translate('MainWindow', 'Canvas'))
        self.menu1dwindow.setTitle(_translate('MainWindow', '1D window'))
        self.menu1dwindowseis.setTitle(_translate('MainWindow', 'Seismic'))
        self.actionplotvis1dseisz.setText(_translate('MainWindow', 'Waveform'))
        self.actionplotvis1dseisz.setToolTip('1D Window: Seismic Waveform')
        self.actionplotvis1dseisfreq.setText(_translate('MainWindow', 'Spectrum'))
        self.actionplotvis1dseisfreq.setToolTip('1D Window: Seismic Spectrum')
        self.menu2dwindow.setTitle(_translate('MainWindow', '2D window'))
        self.menu2dwindowseis.setTitle(_translate('MainWindow', 'Seismic'))
        self.actionplotvis2dseisinl.setText(_translate('MainWindow', 'Inline'))
        self.actionplotvis2dseisinl.setToolTip('2D Window: Seismic Inline')
        self.actionplotvis2dseisxl.setText(_translate('MainWindow', 'Crossline'))
        self.actionplotvis2dseisxl.setToolTip('2D Window: Seismic Crossline')
        self.actionplotvis2dseisz.setText(_translate('MainWindow', 'Time/depth'))
        self.actionplotvis2dseisz.setToolTip('2D Window: Seismic Time/depth')
        self.menu2dwindowpsseis.setTitle(_translate('MainWindow', 'Pre-stack Seismic'))
        self.actionplotvis2dpsseisshot.setText(_translate('MainWindow', 'Gather'))
        self.actionplotvis2dpsseisshot.setToolTip('2D Window: Pre-stack Gather')
        self.menu2dwindowpointset.setTitle(_translate('MainWindow', 'PointSet'))
        self.actionplotvis2dpointsetcrossplt.setText(_translate('MainWindow', 'Cross-plot'))
        self.actionplotvis2dpointsetcrossplt.setToolTip('2D Window: PointSet Cross-plot')
        self.menu3dwindow.setTitle(_translate('MainWindow', '3D window'))
        self.menu3dwindowseis.setTitle(_translate('MainWindow', 'Seismic'))
        self.actionplotvis3dseisinlxlz.setText(_translate('MainWindow', 'IL/XL/Z'))
        self.actionplotviscanvas.setShortcut(QtGui.QKeySequence('Alt+C'))
        self.actionplotvis1dseisz.setShortcut(QtGui.QKeySequence('Alt+W'))
        self.actionplotvis1dseisfreq.setShortcut(QtGui.QKeySequence('Alt+Q'))
        self.actionplotvis2dseisinl.setShortcut(QtGui.QKeySequence('Alt+I'))
        self.actionplotvis2dseisxl.setShortcut(QtGui.QKeySequence('Alt+X'))
        self.actionplotvis2dseisz.setShortcut(QtGui.QKeySequence('Alt+Z'))
        self.actionplotvis2dpsseisshot.setShortcut(QtGui.QKeySequence('Alt+G'))
        self.actionplotvis2dpointsetcrossplt.setShortcut(QtGui.QKeySequence('Alt+P'))
        self.actionplotvis3dseisinlxlz.setShortcut(QtGui.QKeySequence('Alt+M'))
        self.menusettings.setTitle(_translate('MainWindow', 'Settings'))
        self.actionsettingsgui.setText(_translate('MainWindow', 'Interface'))
        self.actionsettingsgeneral.setText(_translate('MainWindow', 'General'))
        self.actionsettingsvisual.setText(_translate('MainWindow', 'Visual'))
        self.actionsettingsviewer.setText(_translate('MainWindow', 'Viewer'))
        self.actionsettingsgui.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F8))
        self.actionsettingsgeneral.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F9))
        self.actionsettingsvisual.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F10))
        self.actionsettingsviewer.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F11))
        self.actionmanual.setText(_translate('MainWindow', 'Manual'))
        self.actionsupport.setText(_translate('MainWindow', 'Online support'))
        self.actionabout.setText(_translate('MainWindow', 'About'))
        self.actionmanual.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F1))
        self.toolbarleft.setVisible(self.settings['Gui']['Toolbar']['Left'])
        self.toolbarright.setVisible(self.settings['Gui']['Toolbar']['Right'])
        self.toolbartop.setVisible(self.settings['Gui']['Toolbar']['Top'])
        self.toolbarbottom.setVisible(self.settings['Gui']['Toolbar']['Bottom'])
        self.actionnewproject.triggered.connect(self.doNewProject)
        self.actionopenproject.triggered.connect(self.doOpenProject)
        self.actionsaveproject.triggered.connect(self.doSaveProject)
        self.actionsaveasproject.triggered.connect(self.doSaveasProject)
        self.actionimportsurveymanual.triggered.connect(self.doImportSurveyManual)
        self.actionimportsurveysegy.triggered.connect(self.doImportSurveySegy)
        self.actionimportsurveynpy.triggered.connect(self.doImportSurveyNpy)
        self.actionimportseissegy.triggered.connect(self.doImportSeisSegy)
        self.actionimportseisnpy.triggered.connect(self.doImportSeisNpy)
        self.actionimportseisimageset.triggered.connect(self.doImportSeisImageSet)
        self.actionimportpsseissegy.triggered.connect(self.doImportPsSeisSegy)
        self.actionimportpsseisnpy.triggered.connect(self.doImportPsSeisNpy)
        self.actionimportpsseisimageset.triggered.connect(self.doImportPsSeisImageSet)
        self.actionimportpointsetfile.triggered.connect(self.doImportPointSetFile)
        self.actionimportpointsetnpy.triggered.connect(self.doImportPointSetNpy)
        self.actionexportsurvey.triggered.connect(self.doExportSurvey)
        self.actionexportseissegy.triggered.connect(self.doExportSeisSegy)
        self.actionexportseisnpy.triggered.connect(self.doExportSeisNpy)
        self.actionexportseisimageset.triggered.connect(self.doExportSeisImageSet)
        self.actionexportpsseisnpy.triggered.connect(self.doExportPsSeisNpy)
        self.actionexportpointsetfile.triggered.connect(self.doExportPointSetFile)
        self.actionexportpointsetnpy.triggered.connect(self.doExportPointSetNpy)
        self.actionquit.triggered.connect(self.doQuit)
        self.actionmanagesurvey.triggered.connect(self.doManageSurvey)
        self.actionmanageseis.triggered.connect(self.doManageSeis)
        self.actionmanagepsseis.triggered.connect(self.doManagePsSeis)
        self.actionmanagepointset.triggered.connect(self.doManagePointSet)
        self.actionconvertseis2pointset.triggered.connect(self.doConvertSeis2PointSet)
        self.actionconvertpointset2seis.triggered.connect(self.doConvertPointSet2Seis)
        self.actionconvertseis2psseis.triggered.connect(self.doConvertSeis2PsSeis)
        self.actionconvertpsseis2seis.triggered.connect(self.doConvertPsSeis2Seis)
        self.actioncalcmathattribsingle.triggered.connect(self.doCalcMathAttribSingle)
        self.actioncalcmathattribmultiple.triggered.connect(self.doCalcMathAttribMultiple)
        self.actioncalcinstanattrib.triggered.connect(self.doCalcInstanAttrib)
        self.actionplotviscanvas.triggered.connect(self.doPlotVisCanvas)
        self.actionplotvis1dseisz.triggered.connect(self.doPlotVis1DSeisZ)
        self.actionplotvis1dseisfreq.triggered.connect(self.doPlotVis1DSeisFreq)
        self.actionplotvis2dseisinl.triggered.connect(self.doPlotVis2DSeisInl)
        self.actionplotvis2dseisxl.triggered.connect(self.doPlotVis2DSeisXl)
        self.actionplotvis2dseisz.triggered.connect(self.doPlotVis2DSeisZ)
        self.actionplotvis2dpsseisshot.triggered.connect(self.doPlotVis2DPsSeisShot)
        self.actionplotvis2dpointsetcrossplt.triggered.connect(self.doPlotVis2DPointSetCrossplt)
        self.actionplotvis3dseisinlxlz.triggered.connect(self.doPlotVis3DSeisInlXlZ)
        self.actionsettingsgui.triggered.connect(self.doSettingsGUI)
        self.actionsettingsgeneral.triggered.connect(self.doSettingsGeneral)
        self.actionsettingsvisual.triggered.connect(self.doSettingsVisual)
        self.actionsettingsviewer.triggered.connect(self.doSettingsViewer)
        self.actionmanual.triggered.connect(self.doManual)
        self.actionsupport.triggered.connect(self.doSupport)
        self.actionabout.triggered.connect(self.doAbout)
        self.bkimage.setPixmap(QtGui.QPixmap(os.path.join(self.iconpath, 'icons/background.png')).scaled(700, 300, QtCore.Qt.KeepAspectRatio))
        self.bkimage.setAlignment(QtCore.Qt.AlignCenter)

    def doNewProject(self):
        self.projname = 'New project'
        self.projpath = ''
        self.survinfo = {}
        self.seisdata = {}
        self.psseisdata = {}
        self.pointsetdata = {}
        self.settings = core_set.Settings
        self.dialog.setWindowTitle('CognitiveGeo <' + self.projname + '>')
        self.setSettings(self.settings)

    def doOpenProject(self):
        self.refreshMsgBox()
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Project NumPy', (self.settings['General']['RootPath']), filter='Project Numpy files (*.proj.npy);; All files (*.*)')
        self.projpath = os.path.split(_file[0])[0]
        _projname = os.path.basename(_file[0])
        self.projname = _projname.replace('.proj.npy', '')
        if os.path.exists(os.path.join(self.projpath, self.projname + '.proj.npy')) is False or os.path.exists(os.path.join(self.projpath, self.projname + '.proj.data')) is False:
            vis_msg.print('doOpenProj: No Project selected', type='error')
            return
        print('doOpenProj: Import Project: ' + os.path.join(self.projpath, self.projname + 'proj.npy'))
        try:
            _proj = np.load((os.path.join(self.projpath, self.projname + '.proj.npy')), allow_pickle=True).item()
        except ValueError:
            vis_msg.print('doOpenProj: Non-dictionary Project NumPy selected', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Open Project', 'Non-dictionary Project NumPy selected')
            return
        else:
            if 'survinfo' in _proj.keys():
                self.survinfo = _proj['survinfo']
                if os.path.exists(os.path.join(self.projpath, self.projname + '.proj.data/Survey/' + 'survey' + '.srv.npy')):
                    try:
                        _survinfo = np.load(os.path.join(self.projpath, self.projname + '.proj.data/Survey/' + 'survey' + '.srv.npy')).item()
                    except ValueError:
                        _survinfo = {}

                    if checkSurvInfo(_survinfo):
                        self.survinfo = _survinfo
                    else:
                        self.survinfo = {}
                if 'survinfo' in _proj.keys():
                    if 'seisdata' in _proj.keys():
                        self.seisdata = {}
                        for key in _proj['seisdata'].keys():
                            if os.path.exists(os.path.join(self.projpath, self.projname + '.proj.data/Seismic/' + key + '.seis.npy')):
                                try:
                                    _seisdata = np.load(os.path.join(self.projpath, self.projname + '.proj.data/Seismic/' + key + '.seis.npy'))
                                except ValueError:
                                    _seisdata = []

                                if checkSeisData(_seisdata, self.survinfo):
                                    self.seisdata[key] = _seisdata

                    else:
                        self.seisdata = {}
                    if 'psseisdata' in _proj.keys():
                        self.psseisdata = {}
                        for key in _proj['psseisdata'].keys():
                            _psseisdata = {}
                            for shot in _proj['psseisdata'][key].keys():
                                _psseisdata[shot] = {}
                                _psseisdata[shot]['ShotInfo'] = _proj['psseisdata'][key][shot]['ShotInfo']
                                if os.path.exists(os.path.join(self.projpath, self.projname + '.proj.data/PsSeismic/' + key + '_shot_' + shot + '.psseis.npy')):
                                    try:
                                        _psseisdata[shot]['ShotData'] = np.load(os.path.join(self.projpath, self.projname + '.proj.data/PsSeismic/' + key + '_shot_' + shot + '.psseis.npy'))
                                    except ValueError:
                                        _psseisdata[shot] = {}

                            if checkPsSeisData(_psseisdata):
                                self.psseisdata[key] = _psseisdata

                else:
                    self.psseisdata = {}
                if 'pointsetdata' in _proj.keys():
                    self.pointsetdata = {}
                    for key in _proj['pointsetdata'].keys():
                        if os.path.exists(os.path.join(self.projpath, self.projname + '.proj.data/PointSet/' + key + '.pts.npy')):
                            try:
                                _pointsetdata = np.load((os.path.join(self.projpath, self.projname + '.proj.data/PointSet/' + key + '.pts.npy')),
                                  allow_pickle=True).item()
                            except ValueError:
                                _pointsetdata = {}

                            if checkPointData(_pointsetdata):
                                self.pointsetdata[key] = _pointsetdata

            else:
                self.pointsetdata = {}
            if 'settings' in _proj.keys() and os.path.exists(os.path.join(self.projpath, self.projname + '.proj.data/Settings/' + 'settings' + '.npy')):
                try:
                    _settings = np.load(os.path.join(self.projpath, self.projname + '.proj.data/Settings/' + 'settings' + '.npy')).item()
                except ValueError:
                    _settings = {}

                if checkSettings(_settings):
                    self.settings = _settings
            self.dialog.setWindowTitle('CognitiveGeo <' + self.projname + '>')
            self.settings['General']['RootPath'] = self.projpath
            self.setSettings(self.settings)
            QtWidgets.QMessageBox.information(self.msgbox, 'Open Project', 'Project ' + self.projname + ' loaded successfully')

    def doSaveProject(self):
        self.refreshMsgBox()
        if len(self.projpath) > 1:
            saveProject(survinfo=(self.survinfo), seisdata=(self.seisdata), psseisdata=(self.psseisdata),
              pointsetdata=(self.pointsetdata),
              settings=(self.settings),
              savepath=(self.projpath),
              savename=(self.projname))
            QtWidgets.QMessageBox.information(self.msgbox, 'Save Project', 'Project ' + self.projname + ' saved successfully')
        else:
            self.doSaveasProject()

    def doSaveasProject(self):
        self.refreshMsgBox()
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getSaveFileName(None, 'Select Project NumPy', (self.settings['General']['RootPath']), filter='Project NumPy files (*.proj.npy);; All files (*.*)')
        if len(_file[0]) > 0:
            self.projpath = os.path.split(_file[0])[0]
            _name = os.path.split(_file[0])[1]
            self.projname = _name.replace('.proj.npy', '')
            self.dialog.setWindowTitle('CognitiveGeo <' + self.projname + '>')
            self.settings['General']['RootPath'] = self.projpath
            saveProject(survinfo=(self.survinfo), seisdata=(self.seisdata), psseisdata=(self.psseisdata),
              pointsetdata=(self.pointsetdata),
              settings=(self.settings),
              savepath=(self.projpath),
              savename=(self.projname))
            QtWidgets.QMessageBox.information(self.msgbox, 'Save Project', 'Project ' + self.projname + ' saved successfully')

    def doImportSurveyManual(self):
        _importsurvey = QtWidgets.QDialog()
        _gui = gui_importsurveymanual()
        _gui.survinfo = self.survinfo
        _gui.setupGUI(_importsurvey)
        _importsurvey.exec_()
        self.survinfo = _gui.survinfo
        _importsurvey.show()

    def doImportSurveySegy(self):
        _importsurvey = QtWidgets.QDialog()
        _gui = gui_importsurveysegy()
        _gui.survinfo = self.survinfo
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importsurvey)
        _importsurvey.exec_()
        self.survinfo = _gui.survinfo
        _importsurvey.show()

    def doImportSurveyNpy(self):
        self.refreshMsgBox()
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Survey NumPy', (self.settings['General']['RootPath']), filter='Survey Numpy files (*.srv.npy);; All files (*.*)')
        if os.path.exists(_file[0]) is False:
            vis_msg.print('ImportSurveyNpy: No NumPy selected for import', type='error')
            return
        print('ImportSurveyNpy: Import Survey Numpy: ' + _file[0])
        try:
            _survinfo = np.load(_file[0]).item()
            if checkSurvInfo(_survinfo) is False:
                vis_msg.print('ImportSurveyNpy: No survey NumPy selected for import', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Import NumPy', 'No NumPy selected for import')
                return
            self.survinfo = _survinfo
        except ValueError:
            vis_msg.print('ImportSurveyNpy: Numpy dictionary expected', type='error')
            QtWidgets.QMessageBox.critical(self.msgbox, 'Import NumPy', 'Numpy dictionary expected')
            return
        else:
            QtWidgets.QMessageBox.information(self.msgbox, 'Import Survey NumPy', 'Survey imported successfully')

    def doImportSeisSegy(self):
        _importsegy = QtWidgets.QDialog()
        _gui = gui_importseissegy()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importsegy)
        _importsegy.exec_()
        self.survinfo = _gui.survinfo
        self.seisdata = _gui.seisdata
        _importsegy.show()

    def doImportSeisNpy(self):
        self.refreshMsgBox()
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Seismic NumPy', (self.settings['General']['RootPath']), filter='Seismic NumPy files (*.seis.npy);; All files (*.*)')
        if os.path.exists(_file[0]) is False:
            vis_msg.print('ImportSeisNpy: No NumPy selected for import', type='error')
            return
        print('ImportSeisNpy: Import Seismic Numpy: ' + _file[0])
        try:
            _npydata = np.load(_file[0]).item()
            if 'SeisInfo' not in _npydata.keys() or seis_ays.checkSeisInfo(_npydata['SeisInfo']) is False:
                vis_msg.print('ImportSeisNpy: NumPy dictionary contains no information about seismic survey', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Import Seismic NumPy', 'NumPy dictionary contains no inforamtion about seismic')
                return
            _survinfo = _npydata['SeisInfo']
            _seisdata = {}
            for key in _npydata.keys():
                if checkSeisData(_npydata[key], _survinfo):
                    _seisdata[key] = _npydata[key]

        except ValueError:
            _npydata = np.load((_file[0]), allow_pickle=True)
            _filename = os.path.basename(_file[0]).replace('.seis.npy', '')
            if np.ndim(_npydata) <= 1 or np.ndim(_npydata) >= 4:
                vis_msg.print('ImportSeisNpy: NumPy matrix shall be 2D or 3D', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Import Seismic NumPy', 'NumPy matrix shall be 2D or 3D')
                return
            if np.ndim(_npydata) == 2:
                if np.shape(_npydata)[1] < 4:
                    vis_msg.print('ImportSeisNpy: 2D NumPy matrix shall contain at least 4 columns', type='error')
                    QtWidgets.QMessageBox.critical(self.msgbox, 'Import Seismic NumPy', '2D NumPy matrix shall contain at least 4 columns')
                    return
                _survinfo = seis_ays.getSeisInfoFrom2DMat(_npydata)
                _npydata = np.transpose(np.reshape(_npydata[:, 3:4], [_survinfo['ILNum'],
                 _survinfo['XLNum'],
                 _survinfo['ZNum']]), [2, 1, 0])
            if np.ndim(_npydata) == 3:
                if checkSurvInfo(self.survinfo) and self.survinfo['ZNum'] == np.shape(_npydata)[0] and self.survinfo['XLNum'] == np.shape(_npydata)[1] and self.survinfo['ILNum'] == np.shape(_npydata)[2]:
                    _survinfo = self.survinfo
                else:
                    _survinfo = seis_ays.createSeisInfoFrom3DMat(_npydata)
                _npydata = _npydata
            _seisdata = {}
            if checkSeisData(_npydata, _survinfo):
                _seisdata[_filename] = _npydata

        if _survinfo['ZStep'] >= 0:
            reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Seismic Numpy', 'Warning: positive z wii be reversed. Continue?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                return
            _survinfo['ZStart'] = -_survinfo['ZStart']
            _survinfo['ZStep'] = -_survinfo['ZStep']
            _survinfo['ZEnd'] = -_survinfo['ZEnd']
            _survinfo['ZRange'] = -_survinfo['ZRange']
        if checkSurvInfo(_survinfo):
            self.survinfo = _survinfo
        for key in _seisdata.keys():
            if key in self.seisdata.keys():
                if checkSeisData(self.seisdata[key], self.survinfo):
                    reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Seismic NumPy', key + ' already exists. Overwrite?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                    if reply == QtWidgets.QMessageBox.No:
                        return
            self.seisdata[key] = _seisdata[key]

        QtWidgets.QMessageBox.information(self.msgbox, 'Import Seismic NumPy', 'NumPy imported successfully')

    def doImportSeisImageSet(self):
        _importimage = QtWidgets.QDialog()
        _gui = gui_importseisimageset()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importimage)
        _importimage.exec_()
        self.seisdata = _gui.seisdata
        self.survinfo = _gui.survinfo
        _importimage.show()

    def doImportPsSeisSegy(self):
        _importsegy = QtWidgets.QDialog()
        _gui = gui_importpsseissegy()
        _gui.psseisdata = self.psseisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importsegy)
        _importsegy.exec_()
        self.psseisdata = _gui.psseisdata
        _importsegy.show()

    def doImportPsSeisNpy(self):
        self.refreshMsgBox()
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select Pre-stack Seismic NumPy', (self.settings['General']['RootPath']), filter='Pre-stack Seismic NumPy files (*.psseis.npy);; All files (*.*)')
        if os.path.exists(_file[0]) is False:
            vis_msg.print('doImportPsSeisNpy: No NumPy selected for import', type='error')
            return
        print('doImportPsSeisNpy: Import Numpy: ' + _file[0])
        try:
            _psseisdata = np.load(_file[0]).item()
        except ValueError:
            _npydata = np.load(_file[0])
            if np.ndim(_npydata) == 2:
                _npydata = np.expand_dims(_npydata, axis=2)
            _psseisdata = {}
            _filename = os.path.basename(_file[0]).replace('.psseis.npy', '')
            _psseisdata[_filename] = {}
            _psseisdata[_filename]['0'] = {}
            _psseisdata[_filename]['0']['ShotData'] = _npydata
            _psseisdata[_filename]['0']['ShotInfo'] = psseis_ays.createShotInfo(_npydata)

        for key in _psseisdata.keys():
            if key in self.psseisdata.keys():
                if checkPsSeisData(self.psseisdata[key]):
                    reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import Pre-stack Seismic NumPy', key + ' already exists. Overwrite?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                    if reply == QtWidgets.QMessageBox.No:
                        return
            self.psseisdata[key] = _psseisdata[key]

        QtWidgets.QMessageBox.information(self.msgbox, 'Import Pre-stack Seismic NumPy', 'NumPy imported successfully')

    def doImportPsSeisImageSet(self):
        _importimage = QtWidgets.QDialog()
        _gui = gui_importpsseisimageset()
        _gui.psseisdata = self.psseisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importimage)
        _importimage.exec_()
        self.psseisdata = _gui.psseisdata
        _importimage.show()

    def doImportPointSetFile(self):
        _importpoint = QtWidgets.QDialog()
        _gui = gui_importpointsetfile()
        _gui.pointsetdata = self.pointsetdata.copy()
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_importpoint)
        _importpoint.exec()
        self.pointsetdata = _gui.pointsetdata.copy()
        _importpoint.show()

    def doImportPointSetNpy(self):
        self.refreshMsgBox()
        _dialog = QtWidgets.QFileDialog()
        _file = _dialog.getOpenFileName(None, 'Select PointSet NumPy', (self.settings['General']['RootPath']), filter='PointSet NumPy files (*.pts.npy);; All files (*.*)')
        if os.path.exists(_file[0]) is False:
            vis_msg.print('ImportPointSetNpy: No NumPy selected for import', type='error')
            return
        print('ImportPointSetNpy: Import Numpy: ' + _file[0])
        try:
            _pointsetdata = np.load(_file[0]).item()
        except ValueError:
            _npydata = np.load(_file[0])
            if np.ndim(_npydata) != 2:
                vis_msg.print('ImportPointSetNpy: NumPy matrix shall be 2D', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Import PointSet NumPy', 'NumPy matrix shall be 2D')
                return
            _ncol = np.shape(_npydata)[1]
            if _ncol < 3:
                vis_msg.print('ImportPointSetNpy: 2D NumPy matrix shall contain at least 3 columns', type='error')
                QtWidgets.QMessageBox.critical(self.msgbox, 'Import PointSet NumPy', '2D NumPy matrix shall contain at least 3 columns')
                return
            _pointsetdata = {}
            _filename = os.path.basename(_file[0]).replace('.pts.npy', '')
            _pointsetdata[_filename] = {}
            _pointsetdata[_filename]['Inline'] = _npydata[:, 0:1]
            _pointsetdata[_filename]['Crossline'] = _npydata[:, 1:2]
            _pointsetdata[_filename]['Z'] = _npydata[:, 2:3]
            for _i in range(_ncol - 3):
                _pointsetdata[_filename]['property_' + str(_i + 1)] = _npydata[:, _i + 3:_i + 4]

        for key in _pointsetdata.keys():
            if key in self.pointsetdata.keys():
                if checkPointData(_pointsetdata[key]):
                    reply = QtWidgets.QMessageBox.question(self.msgbox, 'Import PointSet NumPy', key + ' already exists. Overwrite?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                    if reply == QtWidgets.QMessageBox.No:
                        return
            self.pointsetdata[key] = _pointsetdata[key]

        QtWidgets.QMessageBox.information(self.msgbox, 'Import PointSet NumPy', 'NumPy imported successfully')

    def doExportSurvey(self):
        _exportsurvey = QtWidgets.QDialog()
        _gui = gui_exportsurvey()
        _gui.survinfo = self.survinfo
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportsurvey)
        _exportsurvey.exec_()
        _exportsurvey.show()

    def doExportSeisSegy(self):
        _exportsegy = QtWidgets.QDialog()
        _gui = gui_exportseissegy()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportsegy)
        _exportsegy.exec_()
        _exportsegy.show()

    def doExportSeisNpy(self):
        _exportnpy = QtWidgets.QDialog()
        _gui = gui_exportseisnpy()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportnpy)
        _exportnpy.exec_()
        _exportnpy.show()

    def doExportSeisImageSet(self):
        _exportimage = QtWidgets.QDialog()
        _gui = gui_exportseisimageset()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportimage)
        _exportimage.exec_()
        _exportimage.show()

    def doExportPsSeisNpy(self):
        _exportnpy = QtWidgets.QDialog()
        _gui = gui_exportpsseisnpy()
        _gui.psseisdata = self.psseisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportnpy)
        _exportnpy.exec_()
        _exportnpy.show()

    def doExportPointSetFile(self):
        _exportfile = QtWidgets.QDialog()
        _gui = gui_exportpointsetfile()
        _gui.pointsetdata = self.pointsetdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportfile)
        _exportfile.exec_()
        _exportfile.show()

    def doExportPointSetNpy(self):
        _exportnpy = QtWidgets.QDialog()
        _gui = gui_exportpointsetnpy()
        _gui.pointsetdata = self.pointsetdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_exportnpy)
        _exportnpy.exec_()
        _exportnpy.show()

    def doQuit(self):
        self.refreshMsgBox()
        reply = QtWidgets.QMessageBox.question(self.msgbox, 'CognitiveGeo', 'Are you sure to quit CognitiveGeo?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            return

    def doManageSurvey(self):
        _managesurvey = QtWidgets.QDialog()
        _gui = gui_managesurvey()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.setupGUI(_managesurvey)
        _managesurvey.exec()
        self.survinfo = _gui.survinfo
        self.seisdata = _gui.seisdata
        _managesurvey.show()

    def doManageSeis(self):
        _manageseis = QtWidgets.QDialog()
        _gui = gui_manageseis()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_manageseis)
        _manageseis.exec()
        self.seisdata = _gui.seisdata
        self.survinfo = _gui.survinfo
        _manageseis.show()

    def doManagePsSeis(self):
        _managepsseis = QtWidgets.QDialog()
        _gui = gui_managepsseis()
        _gui.psseisdata = self.psseisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_managepsseis)
        _managepsseis.exec()
        self.psseisdata = _gui.psseisdata
        _managepsseis.show()

    def doManagePointSet(self):
        _managepoint = QtWidgets.QDialog()
        _gui = gui_managepointset()
        _gui.pointsetdata = self.pointsetdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.linestyle = self.settings['Visual']['Line']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_managepoint)
        _managepoint.exec()
        self.pointsetdata = _gui.pointsetdata
        _managepoint.show()

    def doConvertSeis2PointSet(self):
        _convert = QtWidgets.QDialog()
        _gui = gui_convertseis2pointset()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.pointsetdata = self.pointsetdata
        _gui.setupGUI(_convert)
        _convert.exec()
        self.pointsetdata = _gui.pointsetdata
        _convert.show()

    def doConvertPointSet2Seis(self):
        _convert = QtWidgets.QDialog()
        _gui = gui_convertpointset2seis()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.pointsetdata = self.pointsetdata
        _gui.setupGUI(_convert)
        _convert.exec()
        self.seisdata = _gui.seisdata
        _convert.show()

    def doConvertSeis2PsSeis(self):
        _convert = QtWidgets.QDialog()
        _gui = gui_convertseis2psseis()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.psseisdata = self.psseisdata
        _gui.setupGUI(_convert)
        _convert.exec()
        self.psseisdata = _gui.psseisdata
        _convert.show()

    def doConvertPsSeis2Seis(self):
        _convert = QtWidgets.QDialog()
        _gui = gui_convertpsseis2seis()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.psseisdata = self.psseisdata
        _gui.setupGUI(_convert)
        _convert.exec()
        self.survinfo = _gui.survinfo
        self.seisdata = _gui.seisdata
        _convert.show()

    def doCalcMathAttribSingle(self):
        _attrib = QtWidgets.QDialog()
        _gui = gui_calcmathattribsingle()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_attrib)
        _attrib.exec()
        self.seisdata = _gui.seisdata
        _attrib.show()

    def doCalcMathAttribMultiple(self):
        _attrib = QtWidgets.QDialog()
        _gui = gui_calcmathattribmultiple()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_attrib)
        _attrib.exec()
        self.seisdata = _gui.seisdata
        _attrib.show()

    def doCalcInstanAttrib(self):
        _attrib = QtWidgets.QDialog()
        _gui = gui_calcinstanattrib()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_attrib)
        _attrib.exec()
        self.seisdata = _gui.seisdata
        _attrib.show()

    def doPlotVisCanvas(self):
        _plot = QtWidgets.QDialog()
        _gui = gui_plotviscanvas()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.settings = self.settings
        _gui.setupGUI(_plot)
        _plot.exec()
        _plot.show()

    def doPlotVis1DSeisZ(self):
        _plot1dz = QtWidgets.QDialog()
        _gui = gui_plotvis1dseisz()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.linestyle = self.settings['Visual']['Line']
        _gui.playerconfiginl = self.settings['Viewer']['Player']
        _gui.playerconfigxl = {}
        _gui.playerconfigxl['First'] = 'G'
        _gui.playerconfigxl['Previous'] = 'H'
        _gui.playerconfigxl['Backward'] = 'E'
        _gui.playerconfigxl['Pause'] = 'P'
        _gui.playerconfigxl['Forward'] = 'R'
        _gui.playerconfigxl['Next'] = 'J'
        _gui.playerconfigxl['Last'] = 'K'
        _gui.playerconfigxl['Interval'] = _gui.playerconfiginl['Interval']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot1dz)
        _plot1dz.exec()
        _plot1dz.show()

    def doPlotVis1DSeisFreq(self):
        _plot1d = QtWidgets.QDialog()
        _gui = gui_plotvis1dseisfreq()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.linestyle = self.settings['Visual']['Line']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot1d)
        _plot1d.exec()
        _plot1d.show()

    def doPlotVis2DSeisInl(self):
        _plot2dinl = QtWidgets.QDialog()
        _gui = gui_plotvis2dseisinl()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.playerconfig = self.settings['Viewer']['Player']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot2dinl)
        _plot2dinl.exec()
        _plot2dinl.show()

    def doPlotVis2DSeisXl(self):
        _plot2dxl = QtWidgets.QDialog()
        _gui = gui_plotvis2dseisxl()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.playerconfig = self.settings['Viewer']['Player']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot2dxl)
        _plot2dxl.exec()
        _plot2dxl.show()

    def doPlotVis2DSeisZ(self):
        _plot2dz = QtWidgets.QDialog()
        _gui = gui_plotvis2dseisz()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.playerconfig = self.settings['Viewer']['Player']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot2dz)
        _plot2dz.exec()
        _plot2dz.show()

    def doPlotVis2DPsSeisShot(self):
        _plot2d = QtWidgets.QDialog()
        _gui = gui_plotvis2dpsseisshot()
        _gui.psseisdata = self.psseisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.playerconfig = self.settings['Viewer']['Player']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot2d)
        _plot2d.exec()
        _plot2d.show()

    def doPlotVis2DPointSetCrossplt(self):
        _cplt = QtWidgets.QDialog()
        _gui = gui_plotvis2dpointsetcrossplt()
        _gui.pointsetdata = self.pointsetdata
        _gui.linestyle = self.settings['Visual']['Line']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_cplt)
        _cplt.exec()
        _cplt.show()

    def doPlotVis3DSeisInlXlZ(self):
        _plot3d = QtWidgets.QDialog()
        _gui = gui_plotvis3dseisinlxlz()
        _gui.survinfo = self.survinfo
        _gui.seisdata = self.seisdata
        _gui.plotstyle = self.settings['Visual']['Image']
        _gui.viewerconfig = self.settings['Viewer']['Viewer3D']['ViewFrom']
        _gui.viewerconfig['Home'] = self.settings['Viewer']['Viewer3D']['GoHome']
        _gui.playerconfiginl = self.settings['Viewer']['Player']
        _gui.playerconfigxl = {}
        _gui.playerconfigxl['First'] = 'G'
        _gui.playerconfigxl['Previous'] = 'H'
        _gui.playerconfigxl['Backward'] = 'E'
        _gui.playerconfigxl['Pause'] = 'P'
        _gui.playerconfigxl['Forward'] = 'R'
        _gui.playerconfigxl['Next'] = 'J'
        _gui.playerconfigxl['Last'] = 'K'
        _gui.playerconfigxl['Interval'] = _gui.playerconfiginl['Interval']
        _gui.playerconfigz = {}
        _gui.playerconfigz['First'] = 'C'
        _gui.playerconfigz['Previous'] = 'V'
        _gui.playerconfigz['Backward'] = 'T'
        _gui.playerconfigz['Pause'] = 'P'
        _gui.playerconfigz['Forward'] = 'Y'
        _gui.playerconfigz['Next'] = 'B'
        _gui.playerconfigz['Last'] = 'N'
        _gui.playerconfigz['Interval'] = _gui.playerconfiginl['Interval']
        _gui.fontstyle = self.settings['Visual']['Font']
        _gui.setupGUI(_plot3d)
        _plot3d.exec()
        _plot3d.show()

    def doSettingsGUI(self):
        _settings = QtWidgets.QDialog()
        _gui = gui_settingsgui()
        _gui.mainwindow = self
        _gui.settings = self.settings['Gui']
        _gui.setupGUI(_settings)
        _settings.exec()
        self.settings['Gui'] = _gui.settings
        _settings.show()

    def doSettingsGeneral(self):
        _settings = QtWidgets.QDialog()
        _gui = gui_settingsgeneral()
        _gui.settings = self.settings['General']
        _gui.setupGUI(_settings)
        _settings.exec()
        self.settings['General'] = _gui.settings
        _settings.show()

    def doSettingsVisual(self):
        _settings = QtWidgets.QDialog()
        _gui = gui_settingsvisual()
        _gui.settings = self.settings['Visual']
        _gui.setupGUI(_settings)
        _settings.exec()
        self.settings['Visual'] = _gui.settings
        _settings.show()

    def doSettingsViewer(self):
        _settings = QtWidgets.QDialog()
        _gui = gui_settingsviewer()
        _gui.settings = self.settings['Viewer']
        _gui.setupGUI(_settings)
        _settings.exec()
        self.settings['Viewer'] = _gui.settings
        _settings.show()

    def doManual(self):
        self.refreshMsgBox()
        webbrowser.open('https://geopyteam.wixsite.com/cognitivegeo/manual')

    def doSupport(self):
        webbrowser.open('https://geopyteam.wixsite.com/cognitivegeo/support')

    def doAbout(self):
        _about = QtWidgets.QDialog()
        _gui = gui_about()
        _gui.rootpath = self.settings['General']['RootPath']
        _gui.setupGUI(_about)
        _about.exec()
        _about.show()

    def setSettings(self, settings):
        _dialog = QtWidgets.QDialog()
        _gui = gui_settingsgui()
        _gui.mainwindow = self
        _gui.settings = settings['Gui']
        _gui.setupGUI(_dialog)
        _gui = gui_settingsgeneral()
        _gui.settings = settings['General']
        _gui.setupGUI(_dialog)
        _gui = gui_settingsvisual()
        _gui.settings = settings['Visual']
        _gui.setupGUI(_dialog)
        _gui = gui_settingsviewer()
        _gui.settings = settings['Viewer']
        _gui.setupGUI(_dialog)

    def refreshMsgBox(self):
        _center_x = self.dialog.geometry().center().x()
        _center_y = self.dialog.geometry().center().y()
        self.msgbox.setGeometry(QtCore.QRect(_center_x - 150, _center_y - 50, 300, 100))


class qt_mainwindow(QtWidgets.QMainWindow):

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, 'CognitiveGeo', 'Are you sure to quit CognitiveGeo?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            event.ignore()


def checkSurvInfo(survinfo):
    return seis_ays.checkSeisInfo(survinfo)


def checkSeisData(seisdata, survinfo={}):
    return seis_ays.isSeis3DMatConsistentWithSeisInfo(seisdata, survinfo)


def checkPsSeisData(psseisdata):
    return psseis_ays.checkPsSeis(psseisdata)


def checkPointData(pointsetdata):
    return point_ays.checkPoint(pointsetdata)


def checkSettings--- This code section failed: ---

 L.1948         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'setting'
                4  LOAD_METHOD              keys
                6  CALL_METHOD_0         0  '0 positional arguments'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  LOAD_CONST               1
               12  COMPARE_OP               <
               14  POP_JUMP_IF_FALSE    20  'to 20'

 L.1949        16  LOAD_CONST               False
               18  RETURN_VALUE     
             20_0  COME_FROM            14  '14'

 L.1950        20  LOAD_STR                 'Gui'
               22  LOAD_FAST                'setting'
               24  LOAD_METHOD              keys
               26  CALL_METHOD_0         0  '0 positional arguments'
               28  COMPARE_OP               not-in
               30  POP_JUMP_IF_TRUE     68  'to 68'

 L.1951        32  LOAD_STR                 'General'
               34  LOAD_FAST                'setting'
               36  LOAD_METHOD              keys
               38  CALL_METHOD_0         0  '0 positional arguments'
               40  COMPARE_OP               not-in
               42  POP_JUMP_IF_TRUE     68  'to 68'

 L.1952        44  LOAD_STR                 'Visual'
               46  LOAD_FAST                'setting'
               48  LOAD_METHOD              keys
               50  CALL_METHOD_0         0  '0 positional arguments'
               52  COMPARE_OP               not-in
               54  POP_JUMP_IF_TRUE     68  'to 68'

 L.1953        56  LOAD_STR                 'Viewer'
               58  LOAD_FAST                'setting'
               60  LOAD_METHOD              keys
               62  CALL_METHOD_0         0  '0 positional arguments'
               64  COMPARE_OP               not-in
               66  POP_JUMP_IF_FALSE    72  'to 72'
             68_0  COME_FROM            54  '54'
             68_1  COME_FROM            42  '42'
             68_2  COME_FROM            30  '30'

 L.1954        68  LOAD_CONST               False
               70  RETURN_VALUE     
             72_0  COME_FROM            66  '66'

 L.1955        72  LOAD_GLOBAL              core_set
               74  LOAD_ATTR                checkSettings
               76  LOAD_FAST                'setting'
               78  LOAD_STR                 'Gui'
               80  BINARY_SUBSCR    
               82  LOAD_FAST                'setting'
               84  LOAD_STR                 'General'
               86  BINARY_SUBSCR    

 L.1956        88  LOAD_FAST                'setting'
               90  LOAD_STR                 'Visual'
               92  BINARY_SUBSCR    
               94  LOAD_FAST                'setting'
               96  LOAD_STR                 'Viewer'
               98  BINARY_SUBSCR    
              100  LOAD_CONST               ('gui', 'general', 'visual', 'viewer')
              102  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              104  LOAD_CONST               False
              106  COMPARE_OP               is
              108  POP_JUMP_IF_FALSE   114  'to 114'

 L.1957       110  LOAD_CONST               False
              112  RETURN_VALUE     
            114_0  COME_FROM           108  '108'

 L.1959       114  LOAD_CONST               True
              116  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 116


def saveProject(survinfo={}, seisdata={}, psseisdata={}, pointsetdata={}, settings={}, savepath='', savename='gpy'):
    _proj = {}
    _proj['survinfo'] = survinfo
    _proj['seisdata'] = {}
    _proj['psseisdata'] = {}
    _proj['pointsetdata'] = {}
    _proj['settings'] = settings
    if os.path.exists(os.path.join(savepath, savename + '.proj.data')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data'))
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/Survey')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data/Survey'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data/Survey'))
    np.save(os.path.join(savepath, savename + '.proj.data/Survey/' + 'survey' + '.srv.npy'), survinfo)
    if os.path.exists(os.path.join(savepath, savename + '.proj.data/Seismic')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data/Seismic'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data/Seismic'))
    for key in seisdata.keys():
        _proj['seisdata'][key] = {}
        np.save(os.path.join(savepath, savename + '.proj.data/Seismic/' + key + '.seis.npy'), seisdata[key])

    if os.path.exists(os.path.join(savepath, savename + '.proj.data/PsSeismic')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data/PsSeismic'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data/PsSeismic'))
    for key in psseisdata.keys():
        _proj['psseisdata'][key] = {}
        for shot in psseisdata[key].keys():
            _proj['psseisdata'][key][shot] = {}
            _proj['psseisdata'][key][shot]['ShotInfo'] = psseisdata[key][shot]['ShotInfo']
            np.save(os.path.join(savepath, savename + '.proj.data/PsSeismic/' + key + '_shot_' + shot + '.psseis.npy'), psseisdata[key][shot]['ShotData'])

    if os.path.exists(os.path.join(savepath, savename + '.proj.data/PointSet')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data/PointSet'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data/PointSet'))
    for key in pointsetdata.keys():
        _proj['pointsetdata'][key] = {}
        _proj['pointsetdata'][key] = {}
        np.save(os.path.join(savepath, savename + '.proj.data/PointSet/' + key + '.pts.npy'), pointsetdata[key])

    if os.path.exists(os.path.join(savepath, savename + '.proj.data/Settings')) is True:
        shutil.rmtree(os.path.join(savepath, savename + '.proj.data/Settings'))
    os.mkdir(os.path.join(savepath, savename + '.proj.data/Settings'))
    np.save(os.path.join(savepath, savename + '.proj.data/Settings/' + 'settings' + '.npy'), settings)
    np.save(os.path.join(savepath, savename + '.proj.npy'), _proj)


def start(startpath=os.path.dirname(__file__)[:-8]):
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = qt_mainwindow()
    gui = mainwindow()
    gui.settings['General']['RootPath'] = startpath
    gui.setupGUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start()