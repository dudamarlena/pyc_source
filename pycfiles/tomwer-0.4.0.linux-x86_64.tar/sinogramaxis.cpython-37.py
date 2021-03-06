# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/axis/sinogramaxis.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 15996 bytes
"""
contains gui relative to axis calculation using sinogram
"""
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '14/10/2019'
from silx.gui import qt
from tomwer.core.process.reconstruction.axis.params import AxisCalculationInput
from tomwer.core.process.reconstruction.axis.mode import AxisMode
from tomwer.gui.utils.buttons import PadlockButton
from tomwer.synctools.axis import QAxisRP
from tomwer.core.scan.scanbase import TomoBase
from silx.gui.plot import Plot2D
import logging
_logger = logging.getLogger(__file__)

class SinogramAxisWindow(qt.QMainWindow):
    __doc__ = '\n    Main window for axis calculation from sinogram\n    '
    sigComputationRequested = qt.Signal()
    sigApply = qt.Signal()
    sigAxisEditionLocked = qt.Signal(bool)
    sigSinoLoadStarted = qt.Signal()
    sigSinoLoadEnded = qt.Signal()
    _MARKER_NAME = 'cor'
    _MARKER_COLOR = '#ebc634'

    def __init__(self, axis, parent=None):
        qt.QMainWindow.__init__(self, parent)
        self._scan = None
        if isinstance(axis, QAxisRP):
            self._axis_params = axis
        else:
            raise TypeError('axis should be an instance of QAxisRP')
        self._plot = Plot2D(parent=self)
        self._plot.getDefaultColormap().setVRange(None, None)
        self._plot.setAxesDisplayed(False)
        self._dockOpt = qt.QDockWidget(parent=self)
        self._options = _SinogramOpts(parent=self, axis_params=axis)
        self._dockOpt.setWidget(self._options)
        self.setCentralWidget(self._plot)
        self._dockOpt.setFeatures(qt.QDockWidget.DockWidgetMovable)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self._dockOpt)
        self._loadingThread = _LoadSinoThread()
        self._options.sigComputationRequested.connect(self._computationRequested)
        self._options.sigAxisEditionLocked.connect(self._editionLocked)
        self._options.sigApply.connect(self._applyRequested)
        self._options._lockBut.toggled.connect(self.setLocked)
        self._options._applyBut.pressed.connect(self._validated)
        self._options.sigPositionChanged.connect(self._updateCORMarker)
        self._loadingThread.finished.connect(self._sinogram_loaded)
        self.setPosition = self._options.setPosition

    def setReconsParams(self, axis):
        self._axis_params = axis

    def setScan(self, scan):
        self._scan = scan
        self._options.setScan(self._scan)

    def _updatePlot(self, sinogram):
        self._plot.addImage(data=sinogram)
        self._plot.replot()

    def _computationRequested(self):
        if self._loadingThread.isRunning():
            _logger.warning('a center of rotation is already into processing,please wait until it ends')
            return
        if self._scan is None:
            return
        self._scan.axis_params.use_sinogram = True
        self._axis_params.sinogram_line = self._options.getRadioLine()
        self._axis_params.sinogram_subsampling = self._options.getSubsampling()
        self._axis_params.calculation_input_type = self._options.getCalulationInputType()
        self._scan.axis_params.sinogram_line = self._axis_params.sinogram_line
        self._scan.axis_params.sinogram_subsampling = self._axis_params.sinogram_subsampling
        self._scan.axis_params.calculation_input_type = self._axis_params.calculation_input_type
        self._options.setEnabled(False)
        self.sigSinoLoadStarted.emit()
        self._loadingThread.init(scan=(self._scan), line=(self._options.getRadioLine()),
          subsampling=(int(self._options.getSubsampling())))
        self._loadingThread.start()

    def _editionLocked(self, locked):
        self.sigAxisEditionLocked.emit(locked)

    def _applyRequested(self):
        self.sigApply.emit()

    def _sinogram_loaded(self):
        """callback when the sinogram is loaded"""
        sinogram = self._scan.get_sinogram(line=(self._scan.axis_params.sinogram_line), subsampling=(self._scan.axis_params.sinogram_subsampling))
        self._updatePlot(sinogram=sinogram)
        self.sigSinoLoadEnded.emit()
        self.sigComputationRequested.emit()
        self._options.setEnabled(True)

    def setLocked(self, locked):
        if self._axis_params.mode not in (AxisMode.manual, AxisMode.read):
            self._axis_params.mode = AxisMode.manual
        self._options.setLocked(locked)

    def _validated(self):
        """callback when the validate button is activated"""
        self.sigApply.emit()

    def _updateCORMarker(self, value):
        if value is None:
            try:
                self._plot.removeMarker(self._MARKER_NAME)
            except:
                pass

        else:
            img = self._plot.getActiveImage(just_legend=False)
            if img:
                value = value + img.getData().shape[1] // 2
            self._plot.addXMarker(value, legend=(self._MARKER_NAME),
              color=(self._MARKER_COLOR),
              text='center')


class _LoadSinoThread(qt.QThread):

    def init(self, scan, line, subsampling):
        self._scan = scan
        self._line = line
        self._subsampling = subsampling

    def run(self):
        self._scan.axis_params.use_sinogram = True
        self._scan.axis_params.sinogram_line = self._line
        self._scan.axis_params.sinogram_subsampling = self._subsampling
        try:
            self._scan.get_sinogram(line=(self._line), subsampling=(self._subsampling))
        except ValueError as e:
            try:
                _logger.error(e)
            finally:
                e = None
                del e


class _SinogramOpts(qt.QWidget):
    __doc__ = '\n    Add axis calculation options for sinogram\n    '
    sigComputationRequested = qt.Signal()
    sigApply = qt.Signal()
    sigAxisEditionLocked = qt.Signal(bool)
    sigPositionChanged = qt.Signal(object)

    def __init__(self, parent, axis_params):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QVBoxLayout())
        self._axis = axis_params
        self._scan = None
        self._dataModeWidget = qt.QWidget(parent=self)
        self._dataModeWidget.setLayout(qt.QHBoxLayout())
        self._dataModeWidget.layout().addWidget(qt.QLabel('Data mode', parent=(self._dataModeWidget)))
        self._qcbDataMode = qt.QComboBox(parent=self)
        for input_type in AxisCalculationInput:
            if input_type == AxisCalculationInput.transmission_pag:
                continue
            else:
                self._qcbDataMode.addItem(input_type.name(), input_type)

        self._dataModeWidget.layout().addWidget(self._qcbDataMode)
        self.layout().addWidget(self._dataModeWidget)
        self._lineSelWidget = qt.QWidget(parent=self)
        self._lineSelWidget.setLayout(qt.QHBoxLayout())
        self._lineSelWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._lineSB = qt.QSpinBox(parent=self)
        self._lineSelWidget.layout().addWidget(qt.QLabel('radio line', self))
        self._lineSelWidget.layout().addWidget(self._lineSB)
        self.layout().addWidget(self._lineSelWidget)
        self._subsamplingWidget = qt.QWidget(parent=self)
        self._subsamplingWidget.setLayout(qt.QHBoxLayout())
        self._subsamplingWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._subsamplingSB = qt.QSpinBox(parent=self)
        self._subsamplingSB.setMinimum(1)
        self._subsamplingSB.setValue(4)
        self._subsamplingSB.setMaximum(16)
        self._subsamplingWidget.layout().addWidget(qt.QLabel('subsampling', self))
        self._subsamplingWidget.setToolTip('if you like you can only take a subsample of the sinogram to speed up process')
        self._subsamplingWidget.layout().addWidget(self._subsamplingSB)
        self.layout().addWidget(self._subsamplingWidget)
        spacer = qt.QWidget(self)
        spacer.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Expanding)
        self.layout().addWidget(spacer)
        self._positionWidget = qt.QWidget(parent=self)
        self._positionWidget.setLayout(qt.QHBoxLayout())
        self._positionWidget.layout().setContentsMargins(0, 0, 0, 0)
        centerLabel = qt.QLabel('center:', parent=self)
        centerLabel.setSizePolicy(qt.QSizePolicy.Minimum, qt.QSizePolicy.Minimum)
        font = centerLabel.font()
        font.setBold(True)
        centerLabel.setFont(font)
        self._positionWidget.layout().addWidget(centerLabel)
        self._positionLabel = qt.QLabel('', parent=self)
        self._positionLabel.setAlignment(qt.Qt.AlignLeft)
        self._positionLabel.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        palette = self._positionLabel.palette()
        palette.setColor(qt.QPalette.WindowText, qt.QColor(qt.Qt.red))
        self._positionLabel.setPalette(palette)
        self._positionWidget.layout().addWidget(self._positionLabel)
        if axis_params is not None:
            if axis_params.value is not None:
                self._positionLabel.setText(str(axis_params.value))
        else:
            self.layout().addWidget(self._positionWidget)
            self._buttons = qt.QWidget(parent=self)
            self._buttons.setLayout(qt.QHBoxLayout())
            self._lockBut = PadlockButton(parent=self)
            self._buttons.layout().addWidget(self._lockBut)
            spacer = qt.QWidget(self)
            spacer.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
            self._buttons.layout().addWidget(spacer)
            self._lockLabel = qt.QLabel('lock axis position', parent=self)
            self._buttons.layout().addWidget(self._lockLabel)
            self._computeBut = qt.QPushButton('compute', parent=self)
            self._buttons.layout().addWidget(self._computeBut)
            style = qt.QApplication.style()
            applyIcon = style.standardIcon(qt.QStyle.SP_DialogApplyButton)
            self._applyBut = qt.QPushButton(applyIcon, 'validate', parent=self)
            self._buttons.layout().addWidget(self._applyBut)
            self.layout().addWidget(self._buttons)
            if self._axis.sinogram_line is None:
                self._axis.sinogram_line = 0
            else:
                self._lineSB.setValue(self._axis.sinogram_line)
        self._subsamplingSB.setValue(self._axis.sinogram_subsampling)
        self._computeBut.pressed.connect(self._needComputation)
        self._qcbDataMode.currentIndexChanged.connect(self._updateInputType)

    def _needComputation(self, *arg, **kwargs):
        """callback when the radio line changed"""
        if self._scan is not None:
            self.sigComputationRequested.emit()

    def getRadioLine(self):
        return self._lineSB.value()

    def getSubsampling(self):
        return self._subsamplingSB.value()

    def setScan(self, scan):
        """
        set the gui for this scan

        :param TomoBase scan:
        """
        if scan is None:
            return
        assert isinstance(scan, TomoBase)
        if self._scan is not None:
            self._scan.axis_params.sigChanged.disconnect(self._updatePosition)
        self.blockSignals(True)
        n_line = scan.get_dim_2()
        if n_line is None:
            n_line = 0
        self._lineSB.setMaximum(n_line)
        if scan.axis_params.sinogram_line is not None:
            self._lineSB.setValue(scan.axis_params.sinogram_line)
        else:
            if self._lineSB.value() == 0:
                self._lineSB.setValue(n_line // 2)
            else:
                position = scan.axis_params.value
                if position is None:
                    self.setPosition(0.0)
                else:
                    self.setPosition(position)
            self._scan = scan
            self._scan.axis_params.sigChanged.connect(self._updatePosition)
            self.blockSignals(False)

    def _updatePosition(self):
        if self._scan:
            if self._scan.axis_params:
                axis = self._scan.axis_params
                if axis.value is None:
                    value = '?'
                else:
                    value = axis.value
                self.setPosition(value=value)

    def setPosition(self, value):
        if isinstance(value, float):
            conver = '%.4f' % value
            self.sigPositionChanged.emit(value)
        else:
            conver = value
            try:
                try:
                    value_ = float(value)
                except ValueError:
                    value_ = None

            finally:
                self.sigPositionChanged.emit(value_)

        self._positionLabel.setText(conver)

    def _updateInputType(self):
        self._axis.calculation_input_type = self.getCalulationInputType()

    def getCalulationInputType(self, *arg, **kwargs):
        return AxisCalculationInput.from_value(self._qcbDataMode.currentText())

    def setLocked(self, locked):
        self._dataModeWidget.setEnabled(not locked)
        self._qcbDataMode.setEnabled(not locked)
        self._dataModeWidget.setEnabled(not locked)
        self._lineSelWidget.setEnabled(not locked)
        self._lineSB.setEnabled(not locked)
        self._subsamplingWidget.setEnabled(not locked)
        self._lockBut.setChecked(locked)
        self.sigAxisEditionLocked.emit(locked)