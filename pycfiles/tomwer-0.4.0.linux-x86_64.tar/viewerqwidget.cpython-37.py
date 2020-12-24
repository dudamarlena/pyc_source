# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/viewerqwidget.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 14374 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '24/01/2017'
from silx.gui import qt
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.scan.scanbase import TomoBase
from tomwer.gui import stackplot
import os, logging
logger = logging.getLogger(__name__)

class ScanWidget(qt.QWidget):
    __doc__ = '\n    Widget to display all scan information\n\n    :param parent: the qt parent of the widget\n    :param canLoadOtherScan: can we load an other scan\n    '

    def __init__(self, parent=None, canLoadOtherScan=False):
        qt.QWidget.__init__(self, parent)
        self.ftseriereconstruction = None
        self.canLoadOtherScan = canLoadOtherScan
        self._ScanWidget__loadGUI()

    def __loadGUI(self):
        """Function loading the GUI. Not done on the constructor to avoid memory
        charge
        """
        layout = qt.QVBoxLayout()
        self._folderSelection = self._ScanWidget__createFolderSelection()
        self._folderSelection.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        layout.addWidget(self._folderSelection)
        self.stackImageViewerTab = qt.QTabWidget(self)
        self.stackImageViewerTab.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)
        layout.addWidget(self.stackImageViewerTab)
        self.setLayout(layout)
        self.stackImageViewerTab.setLayout(qt.QVBoxLayout())
        self.stackImageViewerTab.layout().setContentsMargins(0, 0, 0, 0)
        self._stackImageViewerScan = stackplot._QImageFileStackPlot(self)
        self.stackImageViewerTab.addTab(self._stackImageViewerScan, 'Reconstruction')
        self._stackImageViewerRadio = stackplot._QImageFileStackPlot(self)
        self.stackImageViewerTab.addTab(self._stackImageViewerRadio, 'Radios')
        self.loaded = True

    def __createFolderSelection(self):
        layoutScanId = qt.QHBoxLayout()
        widget = qt.QWidget(self)
        widget.setLayout(layoutScanId)
        self.folderName = qt.QLineEdit(widget)
        layoutScanId.addWidget(self.folderName)
        self.button = qt.QPushButton('Select folder', parent=widget)
        self._rootFolderSelection = None
        layoutScanId.addWidget(self.button)
        self.button.clicked.connect(self._getFolder)
        self.folderName.textChanged.connect(self._loadNewSerie)
        if not self.canLoadOtherScan:
            self.button.hide()
            self.folderName.setEnabled(False)
        return widget

    def setRootFolderSelection(self, path):
        """Set the path open when selection a folder to be diaplyed

        :param str path: root path to be open when asking for a new folder
        """
        self._rootFolderSelection = path

    def getCurrentScanFolder(self):
        """Return the folder we want to scan"""
        return self.folderName.text()

    def _loadNewSerie(self, seriePath):
        """
        Load a new serie from the given path

        :param str seriePath: the path to the folder containing the serie
        """
        if os.path.isdir(seriePath):
            self.updateData(ScanFactory.create_scan_object(seriePath))

    def updateData(self, ftseriereconstruction):
        """
        Update the current ftSerieReconstruction displayed

        :param FtserieReconstruction ftseriereconstruction: the new serie to be
        displayed
        """
        if ftseriereconstruction is None or ftseriereconstruction.path is None:
            return
        assert type(ftseriereconstruction.path) is str
        self.ftseriereconstruction = ftseriereconstruction
        self.ftseriereconstruction.updateDataset()
        self.loaded = False
        self.folderName.setText(ftseriereconstruction.path)
        self._stackImageViewerRadio.setImages(self.ftseriereconstruction.projections)
        self._stackImageViewerScan.setImages(self.ftseriereconstruction.reconstructions)

    def _getFolder(self):
        """
        Call back when the user want to change the folder to validate
        """
        defaultDirectory = self._rootFolderSelection or os.getcwd()
        currentSettedFolder = self.getCurrentScanFolder()
        if currentSettedFolder is not None:
            if os.path.isdir(currentSettedFolder):
                defaultDirectory = currentSettedFolder
        dialog = qt.QFileDialog(self, directory=defaultDirectory)
        dialog.setFileMode(qt.QFileDialog.DirectoryOnly)
        if not dialog.exec_():
            dialog.close()
            return
        self.folderName.setText(dialog.selectedFiles()[0])

    def clear(self):
        self.ftseriereconstruction = None
        self.loaded = False
        self.folderName.setText('')
        self._stackImageViewerRadio.clear()
        self._stackImageViewerScan.clear()

    def showActiveImage(self):
        self._stackImageViewerRadio.updateActiveImage()
        self._stackImageViewerScan.updateActiveImage()


class ScanWidgetValidation(ScanWidget):
    __doc__ = '\n    This is the same as ScanWidget but include a widget button which will\n    emit signals such as validated, canceled...\n\n    :param parent: the qt parent of the widget\n    :param canLoadOtherScan: can we load an other scan\n    '

    def __init__(self, parent=None, canLoadOtherScan=False):
        ScanWidget.__init__(self, parent=parent,
          canLoadOtherScan=canLoadOtherScan)
        self.validationWidget = ValidationWidget(parent=self, ftseriereconstruction=(self.ftseriereconstruction))
        self.validationWidget.setVisible(not canLoadOtherScan)
        self.validationWidget.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        self.layout().addWidget(self.validationWidget)

    def updateData(self, ftseriereconstruction):
        ScanWidget.updateData(self, ftseriereconstruction)
        if ftseriereconstruction is not None:
            self.validationWidget.ftseriereconstruction = ftseriereconstruction


class ValidationWidget(qt.QGroupBox):
    __doc__ = '\n    Class containing all the validation buttons\n    and sending signals when they are pushed\n\n    :param QObject parent: the parent of the QTabWidget\n    :param :class:`.FtserieReconstruction`: the scan to display\n    '
    sigValidateScan = qt.Signal(str)
    sigCancelScan = qt.Signal(str)
    sigRedoAcquisitionScan = qt.Signal(TomoBase)
    sigChangeReconstructionParametersScan = qt.Signal(TomoBase)

    def __init__(self, ftseriereconstruction, parent=None):
        qt.QGroupBox.__init__(self, title='Validate manually', parent=parent)
        self.setCheckable(True)
        self.ftseriereconstruction = ftseriereconstruction
        layout = qt.QGridLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.validateButton = qt.QPushButton('Validate')
        style = qt.QApplication.style()
        self.validateButton.setIcon(style.standardIcon(qt.QStyle.SP_DialogApplyButton))
        self.validateButton.pressed.connect(self._ValidationWidget__validated)
        layout.addWidget(self.validateButton, 0, 2)
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        layout.addWidget(spacer, 0, 1)
        self.cancelButton = qt.QPushButton('Cancel')
        self.cancelButton.setIcon(style.standardIcon(qt.QStyle.SP_DialogCancelButton))
        self.cancelButton.pressed.connect(self._ValidationWidget__canceled)
        layout.addWidget(self.cancelButton, 0, 0)
        self.changeReconsParamButton = qt.QPushButton('Change reconstruction parameters')
        self.changeReconsParamButton.setIcon(style.standardIcon(qt.QStyle.SP_FileDialogContentsView))
        self.changeReconsParamButton.pressed.connect(self._ValidationWidget__updateReconstructionParameters)
        layout.addWidget(self.changeReconsParamButton, 2, 0)

    def setEnabled(self, b):
        self.validateButton.setEnabled(b)
        self.cancelButton.setEnabled(b)
        self.changeReconsParamButton.setEnabled(b)

    def __validated(self):
        """Callback when the validate button is pushed"""
        self.sigValidateScan.emit('')

    def __canceled(self):
        """Callback when the cancel button is pushed"""
        if self.ftseriereconstruction is not None:
            self.setEnabled(False)
            self.sigCancelScan.emit(self.ftseriereconstruction.path)

    def __redoacquisition(self):
        """Callback when the redo acquisition button is pushed"""
        if self.ftseriereconstruction is not None:
            self.setEnabled(False)
            self.sigRedoAcquisitionScan.emit(self.ftseriereconstruction)

    def __updateReconstructionParameters(self):
        """Callback when the change reconstruction button is pushed"""
        if self.ftseriereconstruction is not None:
            self.setEnabled(False)
            self.sigChangeReconstructionParametersScan.emit(self.ftseriereconstruction)


class ImageStackViewerValidator(ScanWidgetValidation):
    __doc__ = '\n    Widget to visualize a stack of image\n\n    :param QObject parent: the parent of the QTabWidget\n    :param :class:`.FtserieReconstruction`: the scan to display\n    '
    _sizeHint = qt.QSize(600, 600)

    def __init__(self, parent=None, ftseries=None):
        ScanWidgetValidation.__init__(self, parent)
        self._scanWidgetLayout = qt.QVBoxLayout()
        self.layout().setContentsMargins(0, 0, 0, 0)
        if ftseries is not None:
            self.addScan(ftseries)

    def addScan(self, ftseriereconstruction):
        """function called for showing infomration about a new reconstruction

        :param FtserieReconstruction ftseriereconstruction:
            contains all information about the reconstruciton (scan path,
            reconstruction path ... )
        """
        if type(ftseriereconstruction) is not TomoBase:
            raise RuntimeError("Update error can't manage a type different than                                 FtserieReconstruction")
        assert ftseriereconstruction is not None
        assert ftseriereconstruction.path is not None
        logger.info('Scan validator received %s to be validated' % ftseriereconstruction.path)
        self.lastReconstructionReceived = ftseriereconstruction
        self._updateData(self.lastReconstructionReceived)

    def updateFromPath(self, path):
        """Show the reconstruction from a path"""
        if not os.path.isdir(path):
            raise RuntimeError('givem path %s is not a directory' % path)
        self.addScan(ScanFactory.create_scan_object(path))

    def __updateScanTabsID(self):
        if hasattr(self, 'lastReconstructionReceived'):
            if self.lastReconstructionReceived is not None:
                self.updateData(self.lastReconstructionReceived)
                assert self.OTHER_TAB in self.tabsWidget
                if self.lastReconstructionReceived.path is not None:
                    self.setRootFolderSelection(os.path.dirname(self.lastReconstructionReceived.path))

    def sizeHint(self):
        """Return a reasonable default size for usage in :class:`PlotWindow`"""
        return self._sizeHint


def setUp():
    import fabio.edfimage, tempfile, numpy
    folder = tempfile.mkdtemp()
    basename = os.path.basename(folder)
    for i in range(20):
        f = tempfile.mkstemp(prefix=basename, suffix=(str('_' + str(i) + '.edf')), dir=folder)
        data = numpy.array(numpy.random.random(40000))
        data.shape = (200, 200)
        edf_writer = fabio.edfimage.EdfImage(data=data, header={'tata': 'toto'})
        edf_writer.write(f[1])

    for i in range(5):
        f = tempfile.mkstemp(prefix=basename, suffix=(str('_slice_' + str(i) + '.edf')), dir=folder)
        data = numpy.zeros((200, 200))
        data[::i + 2, ::i + 2] = 1.0
        edf_writer = fabio.edfimage.EdfImage(data=data, header={'tata': 'toto'})
        edf_writer.write(f[1])

    f = tempfile.mkstemp(prefix=basename, suffix=(str('_slice_' + str(6) + '.edf')), dir=folder)
    data = numpy.zeros((200, 200))
    data[50:150, 50:150] = 1.0
    edf_writer = fabio.edfimage.EdfImage(data=data, header={'tata': 'toto'})
    edf_writer.write(f[1])
    return folder