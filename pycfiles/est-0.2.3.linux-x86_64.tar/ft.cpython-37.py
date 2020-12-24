# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/widgets/pymca/ft.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 9429 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/07/2019'
import functools, logging
from Orange.widgets import gui
from Orange.widgets.settings import Setting
from Orange.widgets.widget import OWWidget
from Orange.widgets.widget import Input, Output
import Orange.data
import PyMca5.PyMcaGui.physics.xas.XASFourierTransformParameters as XASFourierTransformParameters
from silx.gui import qt
from silx.gui.plot import LegendSelector
import est.core.process.pymca.ft
from orangecontrib.est.process import _ProcessForOrangeMixIn, ProcessRunnable
from est.core.types import XASObject
from est.gui.XasObjectViewer import XasObjectViewer, ViewType
from est.gui.XasObjectViewer import _normalized_exafs, _ft_window_plot
from est.gui.XasObjectViewer import _ft_intensity_plot, _ft_imaginary_plot
from orangecontrib.est.progress import QProgress
from orangecontrib.est.utils import Converter
from ..container import _ParameterWindowContainer
_logger = logging.getLogger(__file__)

class FTWindow(qt.QMainWindow):

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        self.xasObjViewer = XasObjectViewer(mapKeys=['Mu'], spectrumPlots=('FTWindow',
                                                                           'FTIntensity'))
        self.xasObjViewer._spectrumViews[0]._plot.getXAxis().setLabel('K')
        self.xasObjViewer._spectrumViews[1]._plot.getXAxis().setLabel('R (Angstrom)')
        self.xasObjViewer._spectrumViews[1]._plot.getYAxis().setLabel('Arbitrary Units')
        self.setCentralWidget(self.xasObjViewer)
        self._pymcaWindow = _ParameterWindowContainer(parent=self, parametersWindow=XASFourierTransformParameters)
        dockWidget = qt.QDockWidget(parent=self)
        dockWidget.setWidget(self._pymcaWindow)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, dockWidget)
        dockWidget.setAllowedAreas(qt.Qt.RightDockWidgetArea | qt.Qt.LeftDockWidgetArea)
        dockWidget.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)
        self.legendDockWidget1 = LegendSelector.LegendsDockWidget(parent=self, plot=(self.xasObjViewer._spectrumViews[0]._plot))
        self.legendDockWidget1.setAllowedAreas(qt.Qt.RightDockWidgetArea | qt.Qt.LeftDockWidgetArea)
        self.legendDockWidget1.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self.legendDockWidget1)
        self.legendDockWidget2 = LegendSelector.LegendsDockWidget(parent=self, plot=(self.xasObjViewer._spectrumViews[1]._plot))
        self.legendDockWidget2.setAllowedAreas(qt.Qt.RightDockWidgetArea | qt.Qt.LeftDockWidgetArea)
        self.legendDockWidget2.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self.legendDockWidget2)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self.xasObjViewer._mapView.keySelectionDocker)
        for ope in (_normalized_exafs, _ft_window_plot):
            self.xasObjViewer._spectrumViews[0].addCurveOperation(ope)

        for ope in (_ft_intensity_plot, _ft_imaginary_plot):
            self.xasObjViewer._spectrumViews[1].addCurveOperation(ope)

        self.setWindowFlags(qt.Qt.Widget)
        self.xasObjViewer.viewTypeChanged.connect(self._updateLegendView)
        self._updateLegendView()

    def getNCurves(self):
        return len(self.plot.getAllCurves())

    def _updateLegendView(self):
        index, viewType = self.xasObjViewer.getViewType()
        self.legendDockWidget1.setVisible(viewType is ViewType.spectrum and index == 0)
        self.legendDockWidget2.setVisible(viewType is ViewType.spectrum and index == 1)
        self.xasObjViewer._mapView.keySelectionDocker.setVisible(viewType is ViewType.map)


class FTOW(_ProcessForOrangeMixIn, OWWidget):
    __doc__ = '\n    Widget used for signal extraction\n    '
    name = 'fourier transform'
    id = 'orange.widgets.pymca.xas.ft'
    description = 'Progress fourier transform'
    icon = 'icons/ft.png'
    priority = 4
    category = 'esrfWidgets'
    keywords = ['spectroscopy', 'signal', 'fourier', 'transform', 'fourier transform']
    want_main_area = True
    resizing_enabled = True
    process_function = est.core.process.pymca.ft.PyMca_ft
    _pymcaSettings = Setting(dict())

    class Inputs:
        xas_obj = Input('xas_obj', XASObject, default=True)
        data_table = Input('Data', Orange.data.Table)

    class Outputs:
        res_xas_obj = Output('xas_obj', XASObject)

    def __init__(self):
        super().__init__()
        self._latest_xas_obj = None
        self._window = FTWindow(parent=self)
        layout = gui.vBox(self.mainArea, 'fourier transform').layout()
        layout.addWidget(self._window)
        self._progress = gui.ProgressBar(self, 100)
        if self._pymcaSettings != dict():
            self._window._pymcaWindow.setParameters(self._pymcaSettings)
        self._window._pymcaWindow.sigChanged.connect(self._updateProcess)

    def _updateProcess(self, *arv, **kwargs):
        self._update_settings()
        if self._latest_xas_obj:
            self.process(xas_obj=(self._latest_xas_obj))

    @Inputs.data_table
    def processFrmDataTable(self, data_table):
        if data_table is None:
            return
        self.process(Converter.toXASObject(data_table=data_table))

    @Inputs.xas_obj
    def process(self, xas_obj):
        if xas_obj is None:
            return
        if not self._canProcess():
            _logger.warning('There is some processing on going already, willnot process the new dataset')
        self._latest_xas_obj = xas_obj.copy(create_h5_file=True)
        self._startProcess()
        process_obj = QPyMca_ft()
        process_obj._advancement.sigProgress.connect(self._setProgressValue)
        process_obj.setProperties({'_pymcaSettings': self._window._pymcaWindow.getParameters()})
        thread = self.getProcessingThread()
        thread.init(process_obj=process_obj, xas_obj=(self._latest_xas_obj))
        self._callback_finish = functools.partial(self._endProcess, self._latest_xas_obj)
        thread.finished.connect(self._callback_finish)
        thread.start(priority=(qt.QThread.LowPriority))

    def _update_settings(self):
        self._pymcaSettings = self._window._pymcaWindow.getParameters()

    def _setProgressValue(self, value):
        self._progress.widget.progressBarSet(value)


class QPyMca_ft(est.core.process.pymca.ft.PyMca_ft):
    __doc__ = '\n    Normalization able to give advancement using qt.Signal and QThreadPool\n    '

    def __init__(self):
        est.core.process.pymca.ft.PyMca_ft.__init__(self)
        self._advancement = QProgress('normalization')

    def _pool_process(self, xas_obj):
        self.pool = qt.QThreadPool()
        self.pool.setMaxThreadCount(5)
        for spectrum in xas_obj.spectra:
            runnable = ProcessRunnable(fct=(est.core.process.pymca.ft.process_spectr_ft), spectrum=spectrum,
              configuration=(xas_obj.configuration),
              callback=(self._advancement.increaseAdvancement))
            self.pool.start(runnable)

        self.pool.waitForDone()