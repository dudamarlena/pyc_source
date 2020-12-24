# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/orangecontrib/tomwer/widgets/control/DataValidatorOW.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 13951 bytes
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '01/12/2016'
import logging, os
from silx.gui import qt
from Orange.widgets import widget, gui
from Orange.widgets.widget import Output, Input
from tomwer.core.process.scanvalidator import ScanValidator, logger as SVLogger
from tomwer.core.scan.scanbase import TomoBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.gui.qfolderdialog import QScanDialog
from tomwer.gui.viewerqwidget import ImageStackViewerValidator
from tomwer.gui.utils.waiterthread import QWaiterThread
from tomwer.web.client import OWClient
logger = logging.getLogger(__name__)
WAIT_TIME_MEM_REL = 20

class DataValidatorOW(widget.OWWidget, ScanValidator):
    name = 'data validator'
    id = 'orange.widgets.tomwer.scanvalidator'
    description = 'Widget displaying results of a reconstruction and asking to\n    the user if he want to validate or not the reconstruction. User can also ask\n    for some modification on the reconstruction parameters'
    icon = 'icons/validator.png'
    priority = 23
    category = 'esrfWidgets'
    keywords = ['tomography', 'file', 'tomwer', 'acquisition', 'validation']
    want_main_area = True
    resizing_enabled = True
    compress_signal = False
    _warnValManualShow = False
    _NB_SCAN_BF_WARN = 10
    scanready = qt.Signal(str)
    assert len(ScanValidator.inputs) == 1

    class Inputs:
        data_in = Input(name=(ScanValidator.inputs[0].name), type=(ScanValidator.inputs[0].type),
          doc=(ScanValidator.inputs[0].doc))

    assert len(ScanValidator.outputs) == 2

    class Outputs:
        assert ScanValidator.outputs[0].name == 'change recons params'
        recons_param_changed = Output(name=(ScanValidator.outputs[0].name), type=(ScanValidator.outputs[0].type),
          doc=(ScanValidator.outputs[0].doc))
        data_out = Output(name=(ScanValidator.outputs[1].name), type=(ScanValidator.outputs[1].type),
          doc=(ScanValidator.outputs[1].doc))

    def __init__(self, parent=None, ftserie=None, memReleaserWaitLoop=WAIT_TIME_MEM_REL):
        """a simple viewer of image stack

        :param parent: the parent widget
        :param ftserie: an ftserie to validate
        """
        widget.OWWidget.__init__(self, parent)
        ScanValidator.__init__(self, memoryReleaser=(QWaiterThread(memReleaserWaitLoop)))
        OWClient.__init__(self, (logger, SVLogger))
        self._buildGUI(ftserie)

    def _buildGUI(self, ftserie):
        self.tabsWidget = {}
        self._scanWidgetLayout = gui.hBox(self.mainArea, self.name).layout()
        self._scanWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = ImageStackViewerValidator(self)
        self._scanWidgetLayout.addWidget(self.widget)
        lateralWidget = qt.QWidget(parent=self)
        lateralWidget.setLayout(qt.QVBoxLayout())
        lateralWidget.layout().setContentsMargins(0, 0, 0, 0)
        sliderWidget = qt.QWidget(parent=lateralWidget)
        sliderWidget.setLayout(qt.QHBoxLayout())
        self._qslider = qt.QSlider((qt.Qt.Vertical), parent=sliderWidget)
        self._qslider.valueChanged.connect(self.updateStackView)
        sliderWidget.layout().addWidget(self._qslider)
        sliderWidget.layout().addWidget(_VerticalLabel('stack of received scan', parent=sliderWidget,
          revert=True))
        lateralWidget.layout().addWidget(sliderWidget)
        self._addSlideButton = qt.QPushButton('Add scan', parent=lateralWidget)
        self._addSlideButton.pressed.connect(self._addScanCallBack)
        lateralWidget.layout().addWidget(self._addSlideButton)
        self._scanWidgetLayout.addWidget(lateralWidget)
        self.addScan(ftserie)
        self._connectValidationWidget()

    def _connectValidationWidget(self):
        validationWidget = self.widget.validationWidget
        validationWidget.sigValidateScan.connect(self._validateCurrentScan)
        validationWidget.sigCancelScan.connect(self._cancelCurrentScan)
        validationWidget.sigChangeReconstructionParametersScan.connect(self._changeReconsParamCurrentScan)
        validationWidget.toggled.connect(self.setManualValidation)

    def getValidationWidget(self, tab):
        return self.widget.validationWidget

    @Inputs.data_in
    def addScan(self, scan):
        if scan is None:
            return
        else:
            assert isinstance(scan, TomoBase)
            ScanValidator.addScan(self, scan)
            self.updateStackView()
            if scan.path in self._scansToValidate:
                self.setActiveScan(self._scansToValidate[scan.path])
            if self._warnValManualShow is False and len(self._scansToValidate) >= self._NB_SCAN_BF_WARN:
                mess = 'Please note that the scanValidator is actually storing %s scan(s). \nScan need to be validated manually in order to continue the workflow processing. \nyou can either validate scan manually or uncheck the `validate manually` check box.' % self._NB_SCAN_BF_WARN
                mess = qt.QMessageBox(parent=self, icon=(qt.QMessageBox.Information), text=mess)
                mess.setModal(False)
                mess.show()
                self._warnValManualShow = True
        if self.isValidationManual():
            self.show()
            self.activateWindow()
            self.raise_()

    def updateStackView(self):
        """
        Update the stack view.
         If active is given then this will be the new active value of the stack
        """
        currentDisplayed = self.getCurrentScanID()
        if currentDisplayed is None:
            if len(self._scansToValidate) > 0:
                currentDisplayed = list(self._scansToValidate.keys())[0]
        self._qslider.setRange(0, len(self._scansToValidate) - 1)
        self.setActiveScan(currentDisplayed)

    def setActiveScan(self, scan):
        if scan is None:
            return
        _scanID = scan
        if isinstance(_scanID, TomoBase):
            _scanID = scan.path
        self.widget.clear()
        if _scanID is None or _scanID not in self._scansToValidate:
            return
        self.widget.updateData(self._scansToValidate[_scanID])
        self.widget.validationWidget.setEnabled(True)
        index = list(self._scansToValidate.keys()).index(_scanID)
        self._qslider.valueChanged.disconnect(self.updateStackView)
        self._qslider.setValue(index)
        self._qslider.valueChanged.connect(self.updateStackView)

    def getCurrentScanID(self):
        """

        :return: the scan currently displayed on the viewer
        :rtype: str
        """
        index = self._qslider.value()
        if index >= len(self._scansToValidate):
            return
        return list(self._scansToValidate.keys())[index]

    def getCurrentScan(self):
        """

        :return: the scan currently displayed on the viewer
        :rtype: :class:`.TomoBase`
        """
        scanID = self.getCurrentScanID()
        if scanID:
            return self._scansToValidate[scanID]

    def _validateCurrentScan(self):
        """This will validate the ftserie currently displayed

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate. Execution order in this case is
            not insured.
        """
        current_scan = self.getCurrentScan()
        if current_scan:
            assert isinstance(current_scan, TomoBase)
            ScanValidator._validateScan(self, current_scan)
            self.updateStackView()
        if self.getCurrentScan() is None:
            self.hide()

    def _cancelCurrentScan(self):
        """This will cancel the ftserie currently displayed

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate. Execution order in this case is
            not insured.
        """
        current_scan = self.getCurrentScan()
        if current_scan:
            self._cancelScan(current_scan)
            self.updateStackView()

    def _changeReconsParamCurrentScan(self):
        """This will emit a signal to request am acquisition for the current
        ftSerieReconstruction

        :warning: this will cancel the currently displayed reconstruction.
            But if we are validating a stack of ftserie make sure this is the
            correct one you want to validate. Execution order in this case is
            not insured.
        """
        current_scan = self.getCurrentScan()
        if current_scan:
            ScanValidator._changeReconsParam(self, current_scan)
            self.updateStackView()

    def _addScanCallBack(self):
        dialog = QScanDialog(self, multiSelection=True)
        if not dialog.exec_():
            dialog.close()
            return
        foldersSelected = dialog.filesSelected()
        for folder in foldersSelected:
            assert os.path.isdir(folder)
            try:
                scan = ScanFactory.create_scan_object(scan_path=folder)
            except Exception as e:
                try:
                    logger.error('cannot create instance of TomoBase from', folder, 'Error is', e)
                finally:
                    e = None
                    del e

            else:
                self.addScan(scan=scan)

        if len(dialog.filesSelected()) > 0:
            activeScan = dialog.filesSelected()[(-1)]
            self.setActiveScan(activeScan)

    def _validateStack(self):
        ScanValidator._validateStack(self)
        self.updateStackView()

    def _sendScanReady(self, scan):
        assert isinstance(scan, TomoBase)
        self.widget.clear()
        self.Outputs.data_out.send(scan)
        self.scanready.emit(scan.path)

    def _sendScanCanceledAt(self, scan):
        assert isinstance(scan, TomoBase)
        self.widget.clear()

    def _sendUpdateReconsParam(self, ftserie):
        self.widget.clear()
        self.Outputs.recons_param_changed.send(ftserie)


class _VerticalLabel(qt.QLabel):
    __doc__ = 'Display vertically the given text\n    '

    def __init__(self, text, parent=None, revert=False):
        """

        :param text: the legend
        :param parent: the Qt parent if any
        """
        qt.QLabel.__init__(self, text, parent)
        self.revert = revert
        self.setLayout(qt.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

    def paintEvent(self, event):
        painter = qt.QPainter(self)
        painter.setFont(self.font())
        painter.translate(0, self.rect().height())
        painter.rotate(90)
        if self.revert:
            newRect = qt.QRect(-self.rect().height(), -self.rect().width(), self.rect().height(), self.rect().width())
        painter.drawText(newRect, qt.Qt.AlignHCenter, self.text())
        fm = qt.QFontMetrics(self.font())
        preferedHeight = fm.width(self.text())
        preferedWidth = fm.height()
        self.setFixedWidth(preferedWidth)
        self.setMinimumHeight(preferedHeight)