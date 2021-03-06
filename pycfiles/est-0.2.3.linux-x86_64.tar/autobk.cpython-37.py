# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/orangecontrib/est/widgets/larch/autobk.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 9763 bytes
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
import est.core.process.larch.autobk
from orangecontrib.est.process import _ProcessForOrangeMixIn
from orangecontrib.est.process import ProcessRunnable
from est.core.types import XASObject
from est.gui.XasObjectViewer import XasObjectViewer, ViewType
from est.gui.XasObjectViewer import _plot_bkg, _plot_spectrum, _plot_knots
from est.gui.larch.autobk import _AutobkParameters
from orangecontrib.est.progress import QProgress
from orangecontrib.est.utils import Converter
from orangecontrib.est.widgets.container import _ParameterWindowContainer
_logger = logging.getLogger(__file__)
_USE_THREAD = False

class AutobkWindow(qt.QMainWindow):

    def __init__(self, parent=None):
        qt.QMainWindow.__init__(self, parent)
        mapKeys = [
         'mu', 'bkg', 'chie', 'k', 'chi', 'e0']
        self.xasObjViewer = XasObjectViewer(mapKeys=mapKeys)
        self.xasObjViewer._spectrumViews[0]._plot.getXAxis().setLabel('Energy (eV)')
        self.xasObjViewer._spectrumViews[0]._plot.getYAxis().setLabel('Absorption (a.u.)')
        self.setCentralWidget(self.xasObjViewer)
        self._parametersWindow = _ParameterWindowContainer(parent=self, parametersWindow=_AutobkParameters)
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
        for ope in (_plot_bkg, _plot_spectrum, _plot_knots):
            self.xasObjViewer._spectrumViews[0].addCurveOperation(ope)

        self.setWindowFlags(qt.Qt.Widget)
        self.xasObjViewer.viewTypeChanged.connect(self._updateLegendView)
        self._updateLegendView()

    def getNCurves(self):
        return len(self.xasObjViewer._spectrumViews[0]._plot.getAllCurves())

    def _updateLegendView(self):
        index, viewType = self.xasObjViewer.getViewType()
        self.legendDockWidget.setVisible(viewType is ViewType.spectrum)
        self.xasObjViewer._mapView.keySelectionDocker.setVisible(viewType is ViewType.map)


class AutobkOW(_ProcessForOrangeMixIn, OWWidget):
    __doc__ = '\n    Widget used for signal extraction\n    '
    name = 'autobk'
    id = 'orange.widgets.xas.larch.autobk'
    description = 'background removal'
    icon = 'icons/autobk.png'
    priority = 1
    category = 'esrfWidgets'
    keywords = ['spectroscopy', 'autobk', 'background']
    want_main_area = True
    resizing_enabled = True
    process_function = est.core.process.larch.autobk.Larch_autobk
    _settings = Setting(dict())

    class Inputs:
        xas_obj = Input('xas_obj', XASObject, default=True)
        data_table = Input('Data', Orange.data.Table)

    class Outputs:
        res_xas_obj = Output('xas_obj', XASObject)

    def __init__(self):
        super().__init__()
        self._latest_xas_obj = None
        self._window = AutobkWindow(parent=self)
        layout = gui.vBox(self.mainArea, 'autobk').layout()
        layout.addWidget(self._window)
        self._window.xasObjViewer.setWindowTitle('spectra')
        if self._settings != dict():
            self._window._parametersWindow.setParameters(self._settings)
        self._window._parametersWindow.sigChanged.connect(self._updateProcess)
        if _USE_THREAD is False:
            self._advancement = QProgress('autobk')
            self._advancement.sigProgress.connect(self._setProgressValue)

    def _updateProcess(self):
        """Update settings keeping current xas obj"""
        self._update_settings()
        if self._latest_xas_obj:
            self.process(self._latest_xas_obj)

    def _update_settings(self):
        self._settings = self._window._parametersWindow.getParameters()

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
            process_obj = QLarch_autobk()
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
            process_obj = est.core.process.larch.autobk.Larch_autobk()
            process_obj.advancement = self._advancement
            process_obj.setProperties({'_larchSettings': self._window._parametersWindow.getParameters()})
            process_obj.addCallback(qt.QApplication.instance().processEvents)
            process_obj.addCallback(self._advancement.increaseAdvancement)
            process_obj.process(self._latest_xas_obj)
            self._callback_finish = None
            self._endProcess(self._latest_xas_obj)


class QLarch_autobk(est.core.process.larch.autobk.Larch_autobk):
    __doc__ = '\n    Normalization able to give advancement using qt.Signal and QThreadPool\n    '

    def __init__(self):
        est.core.process.larch.autobk.Larch_autobk.__init__(self)
        self._advancement = QProgress('autobk')

    def _pool_process(self, xas_obj):
        self.pool = qt.QThreadPool()
        self.pool.setMaxThreadCount(5)
        for spectrum in xas_obj.spectra:
            runnable = ProcessRunnable(fct=(est.core.process.larch.autobk.process_spectr_autobk), spectrum=spectrum,
              configuration=(xas_obj.configuration),
              callback=(self._advancement.increaseAdvancement))
            self.pool.start(runnable)

        self.pool.waitForDone()