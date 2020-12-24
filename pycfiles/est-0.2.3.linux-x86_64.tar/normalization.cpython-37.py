# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/widgets/pymca/normalization.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 8744 bytes
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
import PyMca5.PyMcaGui.physics.xas.XASNormalizationParameters as XASNormalizationParameters
from silx.gui import qt
from silx.gui.plot import LegendSelector
from est.gui.XasObjectViewer import _plot_edge, _plot_norm, _plot_post_edge, _plot_pre_edge
import est.core.process.pymca.normalization
from orangecontrib.est.process import _ProcessForOrangeMixIn
from orangecontrib.est.process import ProcessRunnable
from est.core.types import XASObject
from est.gui.XasObjectViewer import XasObjectViewer, ViewType
from orangecontrib.est.progress import QProgress
from orangecontrib.est.utils import Converter
from ..container import _ParameterWindowContainer
_logger = logging.getLogger(__file__)

class NormalizationWindow(qt.QMainWindow):

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        mapKeys = [
         'mu', 'NormalizedMu', 'NormalizedSignal', 'NormalizedBackground']
        self.xasObjViewer = XasObjectViewer(mapKeys=mapKeys)
        self.xasObjViewer._spectrumViews[0]._plot.getXAxis().setLabel('Energy (eV)')
        self.xasObjViewer._spectrumViews[0]._plot.getYAxis().setLabel('Absorption (a.u.)')
        self.setCentralWidget(self.xasObjViewer)
        self._pymcaWindow = _ParameterWindowContainer(parent=self, parametersWindow=XASNormalizationParameters)
        dockWidget = qt.QDockWidget(parent=self)
        dockWidget.setWidget(self._pymcaWindow)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, dockWidget)
        dockWidget.setAllowedAreas(qt.Qt.RightDockWidgetArea | qt.Qt.LeftDockWidgetArea)
        dockWidget.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)
        self.legendDockWidget = LegendSelector.LegendsDockWidget(parent=self, plot=(self.xasObjViewer._spectrumViews[0]._plot))
        self.legendDockWidget.setAllowedAreas(qt.Qt.RightDockWidgetArea | qt.Qt.LeftDockWidgetArea)
        self.legendDockWidget.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self.legendDockWidget)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self.xasObjViewer._mapView.keySelectionDocker)
        for ope in (_plot_edge, _plot_norm, _plot_post_edge, _plot_pre_edge):
            self.xasObjViewer._spectrumViews[0].addCurveOperation(ope)

        self.setWindowFlags(qt.Qt.Widget)
        self.xasObjViewer.viewTypeChanged.connect(self._updateLegendView)
        self._updateLegendView()

    def getNCurves(self):
        return len(self.xasObjViewer._spectrumViews._plot.getAllCurves())

    def _updateLegendView(self):
        index, viewType = self.xasObjViewer.getViewType()
        self.legendDockWidget.setVisible(viewType is ViewType.spectrum)
        self.xasObjViewer._mapView.keySelectionDocker.setVisible(viewType is ViewType.map)


class NormalizationOW(_ProcessForOrangeMixIn, OWWidget):
    __doc__ = '\n    Widget used for signal extraction\n    '
    name = 'normalization'
    id = 'orange.widgets.xas.pymca.normalization'
    description = 'Progress spectra normalization'
    icon = 'icons/normalization.png'
    priority = 1
    category = 'esrfWidgets'
    keywords = ['spectroscopy', 'normalization']
    want_main_area = True
    resizing_enabled = True
    process_function = est.core.process.pymca.normalization.PyMca_normalization
    _pymcaSettings = Setting(dict())

    class Inputs:
        xas_obj = Input('xas_obj', XASObject, default=True)
        data_table = Input('Data', Orange.data.Table)

    class Outputs:
        res_xas_obj = Output('xas_obj', XASObject)

    def __init__(self):
        super().__init__()
        self._latest_xas_obj = None
        self._window = NormalizationWindow(parent=self)
        layout = gui.vBox(self.mainArea, 'normalization').layout()
        layout.addWidget(self._window)
        self._window.xasObjViewer.setWindowTitle('spectra')
        if self._pymcaSettings != dict():
            self._window._pymcaWindow.setParameters(self._pymcaSettings)
        _sig = self._window._pymcaWindow.sigChanged.connect(self._updateProcess)

    def _updateProcess(self):
        self._update_settings()
        if self._latest_xas_obj:
            self.process(self._latest_xas_obj)

    def _update_settings(self):
        self._pymcaSettings = self._window._pymcaWindow.getParameters()

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
        process_obj = QPyMca_normalization()
        process_obj._advancement.sigProgress.connect(self._setProgressValue)
        process_obj.setProperties({'_pymcaSettings': self._window._pymcaWindow.getParameters()})
        thread = self.getProcessingThread()
        thread.init(process_obj=process_obj, xas_obj=(self._latest_xas_obj))
        self._callback_finish = functools.partial(self._endProcess, self._latest_xas_obj)
        thread.finished.connect(self._callback_finish)
        thread.start(priority=(qt.QThread.LowPriority))


class QPyMca_normalization(est.core.process.pymca.normalization.PyMca_normalization):
    __doc__ = '\n    Normalization able to give advancement using qt.Signal and QThreadPool\n    '

    def __init__(self):
        est.core.process.pymca.normalization.PyMca_normalization.__init__(self)
        self._advancement = QProgress('normalization')

    def _pool_process(self, xas_obj):
        self.pool = qt.QThreadPool()
        self.pool.setMaxThreadCount(5)
        for spectrum in xas_obj.spectra:
            runnable = ProcessRunnable(fct=(est.core.process.pymca.normalization.process_spectr_norm), spectrum=spectrum,
              configuration=(xas_obj.configuration),
              callback=(self._advancement.increaseAdvancement))
            self.pool.start(runnable)

        self.pool.waitForDone()