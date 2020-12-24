# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/stacks.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 7098 bytes
"""Some widget construction to check if a sample moved"""
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '19/03/2018'
from silx.gui import qt
from tomwer.gui.stackplot import _QImageFileStackPlot
from tomwer.core.scan.edfscan import EDFTomoScan
from collections import OrderedDict
from tomwer.gui.qfolderdialog import QScanDialog
from tomwer.core.scan.scanbase import TomoBase
import os

class _ImageStack(qt.QMainWindow):
    __doc__ = '\n    This widget will make copy or virtual link to all received *slice* files\n    in order to group them all in one place and be able to browse those\n    (using the image stack of view in orange or a third software as silx view)\n\n    Options are:\n       - copy files or create sym link (set to sym link)\n       - overwrite if existing (set to False)\n\n    Behavior:\n        When the process receives a new data path ([scanPath]/[scan]) and if\n        no output folder has been defined manually them it will try to create\n        the folder [scanPath]/slices if not existing in order to redirect\n        the slices files.\n        If fails will ask for a directory.\n        If the output folder is already existing then move directly to the\n        copy.\n    '

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)
        self._scans = set()
        self._viewer = _QImageFileStackPlot(parent=self)
        self._viewer.addFolderName(True)
        self.setCentralWidget(self._viewer)
        self._viewer.getControlWidget().hide()
        self._dockWidgetMenu = qt.QDockWidget(parent=self)
        self._dockWidgetMenu.layout().setContentsMargins(0, 0, 0, 0)
        self._dockWidgetMenu.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self._dockWidgetMenu.setWidget(self._viewer.getControlWidget())
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, self._dockWidgetMenu)
        toolbar = qt.QToolBar()
        self.addToolBar(qt.Qt.RightToolBarArea, toolbar)
        self._clearAction = _ClearAction(parent=toolbar)
        toolbar.addAction(self._clearAction)
        self._clearAction.triggered.connect(self.clear)
        self._addAction = _AddAction(parent=toolbar)
        toolbar.addAction(self._addAction)
        self._addAction.triggered.connect(self._addNewFolder)
        self.setLoadingMode = self._viewer.setLoadingMode
        self.setForceSync = self._viewer.setForceSync
        self.setLoadingMode('lazy loading')

    def addLeafScan(self, scanID):
        if isinstance(scanID, TomoBase):
            self._scans.add(scanID.path)
        else:
            assert type(scanID) is str
            self._scans.add(scanID)
        self._update()

    def _addNewFolder(self):
        dialog = QScanDialog(self, multiSelection=True)
        if not dialog.exec_():
            dialog.close()
            return
        for folder in dialog.filesSelected():
            assert os.path.isdir(folder)
            self.addLeafScan(folder)

    def removeLeafScan(self, scanID):
        self._scans.remove(scanID)
        self._update()

    def extractImages(self):
        """
        Parse all self._scans and find the images to be displayed on the widget

        :return: images to display for each scan
        :rtype: dict
        """
        raise NotImplementedError('Base class')

    def _update(self):
        all_images = self.extractImages()
        all_images = OrderedDict(sorted(all_images.items()))
        ordered_imgs = []
        for scan in all_images:
            try:
                oScanSlices = OrderedDict(sorted(all_images[scan].items()))
                for slice in oScanSlices:
                    ordered_imgs.append(all_images[scan][slice])

            except TypeError:
                ordered_imgs = ordered_imgs + list(all_images[scan].values())

        self._viewer.setImages(ordered_imgs)

    def clear(self):
        self._scans = set()
        self._viewer.clear()


class _ClearAction(qt.QAction):

    def __init__(self, parent):
        style = qt.QApplication.instance().style()
        icon = style.standardIcon(qt.QStyle.SP_DialogResetButton)
        qt.QAction.__init__(self, icon, 'Clear', parent)


class _AddAction(qt.QAction):

    def __init__(self, parent):
        style = qt.QApplication.instance().style()
        icon = style.standardIcon(qt.QStyle.SP_DirIcon)
        qt.QAction.__init__(self, icon, 'Add', parent)


class SliceStack(_ImageStack):
    __doc__ = '\n    Widget displaying all slices contained in a list of acquisition folder\n    '

    def extractImages(self):
        """
        Parse all self._scans and find the images to be displayed on the widget

        :return: images to display for each scan
        :rtype: dict
        """
        slices = {}
        for scan in self._scans:
            imgs = EDFTomoScan.getReconstructionsPaths(scan, withIndex=True)
            if len(imgs) > 0:
                slices[scan] = imgs

        return slices


class RadioStack(_ImageStack):
    __doc__ = '\n    Widget displaying all radio contained in a list of acquisition folder\n    '

    def extractImages(self):
        """
        Parse all self._scans and find the images to be displayed on the widget

        :return: images to display for each scan
        :rtype: dict
        """
        slices = {}
        for scan in self._scans:
            imgs = EDFTomoScan.getRadioPaths(scan)
            if len(imgs) > 0:
                slices[scan] = imgs

        return slices