# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/widgets/larch/mback_norm.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 9778 bytes
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
from silx.gui import qt
from silx.gui.plot import LegendSelector
import est.core.process.larch.mback_norm
from orangecontrib.est.process import _ProcessForOrangeMixIn
from orangecontrib.est.process import ProcessRunnable
from est.core.types import XASObject
from est.gui.XasObjectViewer import XasObjectViewer, ViewType
from est.gui.XasObjectViewer import _plot_norm, _plot_mback_mu
from est.gui.larch.mback import _MBackParameters
from orangecontrib.est.progress import QProgress
from orangecontrib.est.utils import Converter
from orangecontrib.est.widgets.container import _ParameterWindowContainer
_logger = logging.getLogger(__file__)
_USE_THREAD = False

class Mback_normWindow(qt.QMainWindow):

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        mapKeys = [
         'mu', 'mback_mu', 'norm']
        self.xasObjViewer = XasObjectViewer(mapKeys=mapKeys)
        self.xasObjViewer._spectrumViews[0]._plot.getXAxis().setLabel('Energy (eV)')
        self.setCentralWidget(self.xasObjViewer)
        self._parametersWindow = _ParameterWindowContainer(parent=self, parametersWindow=_MBackParameters)
        dockWidget = qt.QDockWidget(parent=self)
        dockWidget.setWidget(self._parametersWindow)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, dockWidget)
        dockWidget.setAllowedAreas(qt.Qt.RightDockWidgetArea | qt.Qt.LeftDockWidgetArea)
        dockWidget.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)
        self.legendDockWidget = LegendSelector.LegendsDockWidget(parent=self, plot=(self.xasObjViewer._spectrumViews[0]._plot))
        self.legendDockWidget.setAllowedAreas(qt.Qt.RightDockWidgetArea | qt.Qt.LeftDockWidgetArea)
        self.legendDockWidget.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self.legendDockWidget)
        self.addDockWidget(qt.Qt.RightDockWidgetArea, self.xasObjViewer._mapView.keySelectionDocker)
        for ope in (_plot_mback_mu, _plot_norm):
            self.xasObjViewer._spectrumViews[0].addCurveOperation(ope)

        self.setWindowFlags(qt.Qt.Widget)
        self.xasObjViewer.viewTypeChanged.connect(self._updateLegendView)
        self._updateLegendView()

    def _updateLegendView(self):
        index, viewType = self.xasObjViewer.getViewType()
        self.legendDockWidget.setVisible(viewType is ViewType.spectrum)
        self.xasObjViewer._mapView.keySelectionDocker.setVisible(viewType is ViewType.map)

    def getNCurves(self):
        return len(self.xasObjViewer._spectrumViews[0]._plot.getAllCurves())


class Mback_normOW(_ProcessForOrangeMixIn, OWWidget):
    __doc__ = '\n    Widget used for signal extraction\n    '
    name = 'mback norm'
    id = 'orange.widgets.xas.larch.mback.Mback_normOW'
    description = "simplified version of MBACK to Match mu(E) data for tabulated f''(E) for normalization"
    icon = 'icons/mbacknorm.svg'
    priority = 6
    category = 'esrfWidgets'
    keywords = ['spectroscopy', 'mback_norm']
    want_main_area = True
    resizing_enabled = True
    process_function = est.core.process.larch.mback_norm.Larch_mback_norm
    _larchSettings = Setting(dict())

    class Inputs:
        xas_obj = Input('xas_obj', XASObject, default=True)
        data_table = Input('Data', Orange.data.Table)

    class Outputs:
        res_xas_obj = Output('xas_obj', XASObject)

    def __init__(self):
        super().__init__()
        self._latest_xas_obj = None
        self._window = Mback_normWindow(parent=self)
        layout = gui.vBox(self.mainArea, 'mback_norm').layout()
        layout.addWidget(self._window)
        self._window.xasObjViewer.setWindowTitle('spectra')
        if self._larchSettings != dict():
            self._window._parametersWindow.setParameters(self._larchSettings)
        self._window._parametersWindow.sigChanged.connect(self._updateProcess)
        if _USE_THREAD is False:
            self._advancement = QProgress('mback_norm')
            self._advancement.sigProgress.connect(self._setProgressValue)

    def _updateProcess(self):
        self._update_settings()
        if self._latest_xas_obj:
            self.process(self._latest_xas_obj)

    def _update_settings(self):
        self._larchSettings = self._window._parametersWindow.getParameters()

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
        if _USE_THREAD is True:
            process_obj = QLarch_mback_norm()
            process_obj._advancement.sigProgress.connect(self._setProgressValue)
            process_obj.setProperties({'_larchSettings': self._window._parametersWindow.getParameters()})
            thread = self.getProcessingThread()
            thread.init(process_obj=process_obj, xas_obj=(self._latest_xas_obj))
            self._callback_finish = functools.partial(self._endProcess, self._latest_xas_obj)
            thread.finished.connect(self._callback_finish)
            thread.start(priority=(qt.QThread.LowPriority))
        else:
            self._advancement.setAdvancement(0)
            self._advancement.setMaxSpectrum(self._latest_xas_obj.n_spectrum)
            process_obj = est.core.process.larch.mback_norm.Larch_mback_norm()
            process_obj.advancement = self._advancement
            process_obj.setProperties({'_larchSettings': self._window._parametersWindow.getParameters()})
            process_obj.addCallback(qt.QApplication.instance().processEvents)
            process_obj.addCallback(self._advancement.increaseAdvancement)
            process_obj.process(self._latest_xas_obj)
            self._callback_finish = None
            self._endProcess(self._latest_xas_obj)


class QLarch_mback_norm(est.core.process.larch.mback_norm.Larch_mback_norm):
    __doc__ = '\n    Normalization able to give advancement using qt.Signal and QThreadPool\n    '

    def __init__(self):
        est.core.process.larch.mback_norm.Larch_mback_norm.__init__(self)
        self._advancement = QProgress('mback_norm')

    def _pool_process(self, xas_obj):
        self.pool = qt.QThreadPool()
        self.pool.setMaxThreadCount(5)
        for spectrum in xas_obj.spectra:
            runnable = ProcessRunnable(fct=(est.core.process.larch.mback_norm.process_spectr_mback_norm), spectrum=spectrum,
              configuration=(xas_obj.configuration),
              callback=(self._advancement.increaseAdvancement))
            self.pool.start(runnable)

        self.pool.waitForDone()