# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/gui/XasObjectViewer.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 25532 bytes
"""Tools to visualize spectra"""
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '04/07/2019'
from est.core.types import XASObject, Spectrum
from silx.gui import qt
from silx.gui.plot import Plot1D
from silx.gui.plot.StackView import StackViewMainWindow
from silx.utils.enum import Enum
from silx.gui.widgets.FrameBrowser import HorizontalSliderWithBrowser
from est.gui import icons
import silx.gui as silx_icons
from silx.gui.colors import Colormap
import numpy, silx, logging
_logger = logging.getLogger(__name__)
silx_version = silx.version.split('.')
if int(silx_version[0]) == 0:
    if not int(silx_version[1]) <= 11:
        silx_plot_has_baseline_feature = True
else:
    silx_plot_has_baseline_feature = False
    _logger.warning('a more recent of silx is required to display mean spectrum (0.12)')

class ViewType(Enum):
    map = (0, )
    spectrum = (1, )


class _SpectrumViewAction(qt.QAction):

    def __init__(self, parent=None, iView=0):
        qt.QAction.__init__(self, 'spectrum view', parent=parent)
        if not iView in (0, 1):
            raise AssertionError
        else:
            self._iView = iView
            if iView == 0:
                icon = 'item-1dim'
            else:
                if iView == 1:
                    icon = 'item-1dim-black'
                else:
                    raise NotImplementedError('Only two spectrum views are maanged')
        spectrum_icon = icons.getQIcon(icon)
        self.setIcon(spectrum_icon)
        self.setCheckable(True)


class _MapViewAction(qt.QAction):

    def __init__(self, parent=None):
        qt.QAction.__init__(self, 'map view', parent=parent)
        map_icon = silx_icons.getQIcon('image')
        self.setIcon(map_icon)
        self.setCheckable(True)


class XasObjectViewer(qt.QMainWindow):
    __doc__ = 'Viewer dedicated to view a XAS object\n\n    :param QObject parent: Qt parent\n    :param list mapKeys: list of str keys to propose for the map display\n    :param list spectrumsPlots: list of keys if several spectrum plot should be\n                                proposed.\n    '
    viewTypeChanged = qt.Signal()

    def __init__(self, parent=None, mapKeys=None, spectrumPlots=None):
        qt.QMainWindow.__init__(self, parent)
        self.setWindowFlags(qt.Qt.Widget)
        self._mainWidget = qt.QWidget(parent=self)
        self._mainWidget.setLayout(qt.QVBoxLayout())
        self.setCentralWidget(self._mainWidget)
        self._mapView = MapViewer(parent=self, keys=mapKeys)
        self._mainWidget.layout().addWidget(self._mapView)
        self._spectrumViews = []
        if spectrumPlots is not None:
            spectrum_views_ = spectrumPlots
        else:
            spectrum_views_ = ('', )
        for spectrumPlot in range(len(spectrum_views_)):
            spectrumView = SpectrumViewer(parent=self)
            self._mainWidget.layout().addWidget(spectrumView)
            self._spectrumViews.append(spectrumView)

        toolbar = qt.QToolBar('')
        toolbar.setIconSize(qt.QSize(32, 32))
        self._spectrumViewActions = []
        self.view_actions = qt.QActionGroup(self)
        for iSpectrumView, tooltip in enumerate(spectrum_views_):
            spectrumViewAction = _SpectrumViewAction(parent=None, iView=iSpectrumView)
            self.view_actions.addAction(spectrumViewAction)
            self._spectrumViewActions.append(spectrumViewAction)
            spectrumViewAction.setToolTip(tooltip)
            toolbar.addAction(spectrumViewAction)

        self._mapViewAction = _MapViewAction()
        toolbar.addAction(self._mapViewAction)
        self.view_actions.addAction(self._mapViewAction)
        self.addToolBar(qt.Qt.LeftToolBarArea, toolbar)
        toolbar.setMovable(False)
        self._mapViewAction.triggered.connect(self._updateView)
        for spectrumAction in self._spectrumViewActions:
            spectrumAction.triggered.connect(self._updateView)

        self._spectrumViewActions[0].setChecked(True)
        self._updateView()

    def _updateView(self, *arg, **kwargs):
        index, view_type = self.getViewType()
        self._mapView.setVisible(view_type is ViewType.map)
        for iView, spectrumView in enumerate(self._spectrumViews):
            spectrumView.setVisible(view_type is ViewType.spectrum and iView == index)

        self.viewTypeChanged.emit()

    def getViewType(self):
        if self._mapViewAction.isChecked():
            return (
             None, ViewType.map)
        for spectrumViewAction in self._spectrumViewActions:
            if spectrumViewAction.isChecked():
                return (
                 spectrumViewAction._iView, ViewType.spectrum)

        return (None, None)

    def setXASObj(self, xas_obj):
        self._mapView.clear()
        self._mapView.setXasObject(xas_obj)
        for spectrumView in self._spectrumViews:
            spectrumView.clear()
            spectrumView.setXasObject(xas_obj)


class MapViewer(qt.QWidget):

    def __init__(self, parent=None, keys=None):
        """
        
        :param parent: 
        :param keys: volume keys to display for the xasObject (Mu,
        NormalizedMu...)
        """
        assert keys is not None
        self._xasObj = None
        qt.QWidget.__init__(self, parent=parent)
        self.setLayout(qt.QVBoxLayout())
        self._mainWindow = StackViewMainWindow(parent=parent)
        self.layout().addWidget(self._mainWindow)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0.0)
        self._mainWindow.setKeepDataAspectRatio(True)
        self._mainWindow.setColormap(Colormap(name='temperature'))
        self._keyWidget = qt.QWidget(parent=self)
        self._keyWidget.setLayout(qt.QHBoxLayout())
        self._keyComboBox = qt.QComboBox(parent=(self._keyWidget))
        for key in keys:
            self._keyComboBox.addItem(key)

        self._keyWidget.layout().addWidget(qt.QLabel('view: '))
        self._keyWidget.layout().addWidget(self._keyComboBox)
        self.keySelectionDocker = qt.QDockWidget(parent=self)
        self.keySelectionDocker.setContentsMargins(0, 0, 0, 0)
        self._keyWidget.layout().setContentsMargins(0, 0, 0, 0)
        self._keyWidget.layout().setSpacing(0.0)
        self.keySelectionDocker.setWidget(self._keyWidget)
        self.keySelectionDocker.setAllowedAreas(qt.Qt.TopDockWidgetArea)
        self.keySelectionDocker.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)
        self._keyComboBox.currentTextChanged.connect(self._updateView)

    def clear(self):
        self._mainWindow.clear()

    def getActiveKey(self):
        return self._keyComboBox.currentText()

    def setXasObject(self, xas_obj):
        self._xasObj = xas_obj
        self._updateView()

    def _updateView(self, *args, **kwargs):
        if self._xasObj is None:
            return
        spectra_volume = XASObject._spectra_volume(spectra=(self._xasObj.spectra), dim_1=(self._xasObj.dim1),
          dim_2=(self._xasObj.dim2),
          key=(self.getActiveKey()))
        self._mainWindow.setStack(spectra_volume)

    def getPlot(self):
        return self._mainWindow.getPlot()


class _ExtendedSliderWithBrowser(HorizontalSliderWithBrowser):

    def __init__(self, parent=None, name=None):
        HorizontalSliderWithBrowser.__init__(self, parent)
        self.layout().insertWidget(0, qt.QLabel(str(name + ':')))


class _CurveOperation(object):

    def __init__(self, x, y, legend, yaxis=None, linestyle=None, symbol=None, color=None, ylabel=None, baseline=None, alpha=1.0):
        self.x = x
        self.y = y
        self.legend = legend
        self.yaxis = yaxis
        self.linestyle = linestyle
        self.symbol = symbol
        self.color = color
        self.ylabel = ylabel
        self.baseline = baseline
        self.alpha = alpha


class _XMarkerOperation(object):

    def __init__(self, x, legend, color='blue'):
        self.x = x
        self.legend = legend
        self.color = color


class SpectrumViewer(qt.QMainWindow):

    def __init__(self, parent=None):
        self._curveOperations = []
        qt.QMainWindow.__init__(self, parent)
        self.xas_obj = None
        self._plot = Plot1D(parent=self)
        self.setCentralWidget(self._plot)
        dockWidget = qt.QDockWidget(parent=self)
        frameBrowsers = qt.QWidget(parent=self)
        frameBrowsers.setLayout(qt.QVBoxLayout())
        frameBrowsers.layout().setContentsMargins(0, 0, 0, 0)
        self._dim1FrameBrowser = _ExtendedSliderWithBrowser(parent=self, name='dim 1')
        frameBrowsers.layout().addWidget(self._dim1FrameBrowser)
        self._dim2FrameBrowser = _ExtendedSliderWithBrowser(parent=self, name='dim 2')
        frameBrowsers.layout().addWidget(self._dim2FrameBrowser)
        dockWidget.setWidget(frameBrowsers)
        self.addDockWidget(qt.Qt.BottomDockWidgetArea, dockWidget)
        dockWidget.setAllowedAreas(qt.Qt.BottomDockWidgetArea)
        dockWidget.setFeatures(qt.QDockWidget.NoDockWidgetFeatures)
        self._dim1FrameBrowser.valueChanged.connect(self._updateSpectrumDisplayed)
        self._dim2FrameBrowser.valueChanged.connect(self._updateSpectrumDisplayed)

    def addCurveOperation(self, callbacks):
        """register an curve to display from Xasobject keys, and a legend

        :param callbacks: callback to call when displaying a specific curve
        :type: Union[list,tuple,function]
        """
        if isinstance(callbacks, (list, tuple)):
            for callback in callbacks:
                self.addCurveOperation(callback)

        else:
            self._curveOperations.append(callbacks)

    def clearCurveOperations(self):
        """Remove all defined curve operation"""
        self._curveOperations.clear()

    def setXasObject(self, xas_obj):
        self.xas_obj = xas_obj
        assert self.xas_obj.dim1 >= 0
        assert self.xas_obj.dim2 >= 0
        self._dim1FrameBrowser.setRange(0, self.xas_obj.dim1 - 1)
        self._dim2FrameBrowser.setRange(0, self.xas_obj.dim2 - 1)

    def _updateSpectrumDisplayed(self, *args, **kwargs):
        if self.xas_obj is None:
            return
        dim1_index = self._dim1FrameBrowser.value()
        dim2_index = self._dim2FrameBrowser.value()
        if dim1_index < 0 or dim2_index < 0:
            return
        assert dim1_index >= 0
        assert dim2_index >= 0
        spectrum = self.xas_obj.getSpectrum(dim1_index, dim2_index)
        for operation in self._curveOperations:
            curves = [
             operation(spectrum)]
            if silx_plot_has_baseline_feature is True:
                new_curves_op = operation((self.xas_obj), index=dim1_index)
                if new_curves_op is not None:
                    curves += new_curves_op
            for res in curves:
                if res is not None and res.x is not None:
                    if isinstance(res, _CurveOperation):
                        kwargs = {'x':res.x,  'y':res.y, 
                         'legend':res.legend, 
                         'yaxis':res.yaxis, 
                         'linestyle':res.linestyle, 
                         'symbol':res.symbol, 
                         'color':res.color, 
                         'ylabel':res.ylabel}
                        if silx_plot_has_baseline_feature:
                            kwargs['baseline'] = (
                             res.baseline,)
                        curve = (self._plot.addCurve)(**kwargs)
                        curve = self._plot.getCurve(curve)
                        curve.setAlpha(res.alpha)
                    elif isinstance(res, _XMarkerOperation):
                        self._plot.addXMarker(x=(res.x), color=(res.color),
                          legend=(res.legend))
                    else:
                        raise TypeError('this type of operation is not recognized', type(res))

    def clear(self):
        self._plot.clear()
        self._dim1FrameBrowser.setMaximum(-1)
        self._dim2FrameBrowser.setMaximum(-1)


COLOR_MEAN = 'black'
COLOR_STD = 'grey'

def _plot_norm(obj, **kwargs):
    if isinstance(obj, XASObject):
        assert 'index' in kwargs
        index_dim1 = kwargs['index']
        spectra = XASObject._spectra_volume((obj.spectra), 'normalized_mu',
          (obj.dim1),
          (obj.dim2),
          relative_to='energy')
        spectra = spectra[:, index_dim1, :]
        mean = numpy.mean(spectra, axis=1)
        std = numpy.std(spectra, axis=1)
        return (
         _CurveOperation(x=(obj.energy), y=mean, color=COLOR_MEAN, legend='mean norm', alpha=0.5),
         _CurveOperation(x=(obj.energy), y=(mean + std), baseline=(mean - std), color=COLOR_STD, legend='std norm',
           alpha=0.5))
    if isinstance(obj, Spectrum):
        assert obj.normalized_mu is not None
        if obj.normalized_mu is None:
            _logger.error('norm has not been computed yet')
            return
        assert len(obj.energy) == len(obj.normalized_mu)
        return _CurveOperation(x=(obj.energy), y=(obj.normalized_mu), legend='norm', color='black')


def _plot_norm_area(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    else:
        hasattr(obj, 'norm_area') or _logger.error('norm_area has not been computed yet')
        return
    assert len(obj.energy) == len(obj.norm_area)
    return _CurveOperation(x=(obj.energy), y=(obj.norm_area), legend='norm_area',
      color='orange')


def _plot_mback_mu(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    else:
        hasattr(obj, 'mback_mu') or _logger.error('mback_mu has not been computed yet')
        return
    return _CurveOperation(x=(obj.energy), y=(obj.mback_mu), legend='mback_mu',
      color='orange')


def _plot_pre_edge(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    if obj.pre_edge is None:
        _logger.error('pre_edge has not been computed yet')
        return
    assert len(obj.energy) == len(obj.pre_edge)
    return _CurveOperation(x=(obj.energy), y=(obj.pre_edge), legend='pre edge',
      color='green')


def _plot_post_edge(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    if obj.post_edge is None:
        _logger.error('post_edge has not been computed yet')
        return
    assert len(obj.energy) == len(obj.post_edge)
    return _CurveOperation(x=(obj.energy), y=(obj.post_edge), legend='post edge',
      color='black')


def _plot_edge(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    else:
        hasattr(obj, 'e0') or _logger.error('e0 has not been computed yet')
        return
    return _XMarkerOperation(x=(obj.e0), legend='edge', color='yellow')


def _plot_raw(obj, **kwargs):
    if isinstance(obj, Spectrum):
        if obj.mu is None:
            _logger.error('mu not existing')
            return
        return _CurveOperation(x=(obj.energy), y=(obj.mu), legend='mu',
          color='red')
    if isinstance(obj, XASObject):
        assert 'index' in kwargs
        index_dim1 = kwargs['index']
        spectra = XASObject._spectra_volume((obj.spectra), 'normalized_mu',
          (obj.dim1),
          (obj.dim2),
          relative_to='energy')
        spectra = spectra[:, index_dim1, :]
        mean = numpy.mean(spectra, axis=1)
        std = numpy.std(spectra, axis=1)
        return (
         _CurveOperation(x=(obj.energy), y=mean, color=COLOR_MEAN, legend='mean mu', alpha=0.5),
         _CurveOperation(x=(obj.energy), y=(mean + std), baseline=(mean - std), color=COLOR_STD, legend='mu std',
           alpha=0.5))
    raise ValueError('input type is not manged')


def _plot_fpp(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    else:
        hasattr(obj, 'fpp') or _logger.error('fpp has not been computed yet')
        return
    return _CurveOperation(x=(obj.energy), y=(obj.fpp), legend='fpp', color='blue')


def _plot_f2(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    else:
        hasattr(obj, 'f2') or _logger.error('f2 has not been computed yet')
        return
    return _CurveOperation(x=(obj.energy), y=(obj.f2), legend='f2', color='orange')


def _plot_chir_mag(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    else:
        if not hasattr(obj, 'r'):
            _logger.error('r not computed, unable to display it')
            return
        hasattr(obj, 'chir_mag') or _logger.error('chir_mag not computed, unable to display it')
        return
    return _CurveOperation(x=(obj.r), y=(obj.chir_mag), legend='chi k (mag)')


def _plot_chir_re(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    else:
        if not hasattr(obj, 'r'):
            _logger.error('r not computed, unable to display it')
            return
        hasattr(obj, 'chir_re') or _logger.error('chir_re not computed, unable to display it')
        return
    return _CurveOperation(x=(obj.r), y=(obj.chir_re), legend='chi k (real)')


def _plot_chir_imag(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    else:
        if not hasattr(obj, 'r'):
            _logger.error('r not computed, unable to display it')
            return
        hasattr(obj, 'chir_im') or _logger.error('chir_im not computed, unable to display it')
        return
    return _CurveOperation(x=(obj.r), y=(obj.chir_im), legend='chi k (imag)')


def _plot_spectrum(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    return _CurveOperation(x=(obj.energy), y=(obj.mu), legend='spectrum', yaxis=None,
      color='blue')


def _plot_bkg(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    else:
        hasattr(obj, 'bkg') or _logger.error('missing bkg parameter, unable to compute bkg plot')
        return
    return _CurveOperation(x=(obj.energy), y=(obj.bkg), legend='bkg', yaxis=None,
      color='red')


def _plot_knots(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    else:
        hasattr(obj, 'autobk_details') or _logger.error('missing bkg parameter, unable to compute bkg plot')
        return
    return _CurveOperation(x=(obj.autobk_details.knots_e), y=(obj.autobk_details.knots_y),
      legend='knots',
      yaxis=None,
      color='green',
      linestyle='',
      symbol='o')


def _exafs_signal_plot(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    missing_keys = obj.get_missing_keys(('EXAFSKValues', 'EXAFSSignal'))
    if missing_keys:
        _logger.error('missing keys:', missing_keys, 'unable to compute exafs signal plot')
        return
    k = obj['EXAFSKValues']
    if 'KMin' not in obj:
        obj['KMin'] = k.min()
    if 'KMax' not in obj:
        obj['KMax'] = k.max()
    idx = (obj['EXAFSKValues'] >= obj['KMin']) & (obj['EXAFSKValues'] <= obj['KMax'])
    x = obj['EXAFSKValues'][idx]
    y = obj['EXAFSSignal'][idx]
    return _CurveOperation(x=x, y=y, legend='EXAFSSignal')


def _exafs_postedge_plot(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    missing_keys = obj.get_missing_keys(('EXAFSKValues', 'PostEdgeB'))
    if missing_keys:
        _logger.error('missing keys:', missing_keys, 'unable to compute exafs postedge plot')
        return
    k = obj['EXAFSKValues']
    if 'KMin' not in obj:
        obj['KMin'] = k.min()
    if 'KMax' not in obj:
        obj['KMax'] = k.max()
    idx = (obj['EXAFSKValues'] >= obj['KMin']) & (obj['EXAFSKValues'] <= obj['KMax'])
    x = obj['EXAFSKValues'][idx]
    y = obj['PostEdgeB'][idx]
    return _CurveOperation(x=x, y=y, legend='PostEdge')


def _exafs_knots_plot(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    missing_keys = obj.get_missing_keys(('KnotsX', 'KnotsY'))
    if missing_keys:
        _logger.error('missing keys:', missing_keys, 'unable to compute exafs knot plot')
        return
    x = obj['KnotsX']
    y = obj['KnotsY']
    return _CurveOperation(x=x, y=y, legend='Knots', linestyle='', symbol='o')


def _normalized_exafs(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    else:
        assert isinstance(obj, Spectrum)
        missing_keys = obj.get_missing_keys(('EXAFSKValues', 'EXAFSNormalized'))
        if missing_keys:
            _logger.error('missing keys:', missing_keys, 'unable to compute normalized EXAFS')
            return
            if obj['KWeight']:
                if obj['KWeight'] == 1:
                    ylabel = 'EXAFS Signal * k'
                else:
                    ylabel = 'EXAFS Signal * k^%d' % obj['KWeight']
        else:
            ylabel = 'EXAFS Signal'
    idx = (obj['EXAFSKValues'] >= obj['KMin']) & (obj['EXAFSKValues'] <= obj['KMax'])
    return _CurveOperation(x=(obj['EXAFSKValues'][idx]), y=(obj['EXAFSNormalized'][idx]),
      legend='Normalized EXAFS',
      ylabel=ylabel)


def _ft_window_plot(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    missing_keys = obj.ft.get_missing_keys(('K', 'WindowWeight'))
    if missing_keys:
        _logger.error('missing keys:', missing_keys, 'unable to compute normalized EXAFS')
        return
    return _CurveOperation(x=(obj.ft['K']), y=(obj.ft['WindowWeight']),
      legend='FT Window',
      yaxis='right',
      color='red')


def _ft_intensity_plot(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    missing_keys = obj.ft.get_missing_keys(('FTRadius', 'FTIntensity'))
    if missing_keys:
        _logger.error('missing keys:', missing_keys, 'unable to compute spectrum plot')
        return
    return _CurveOperation(x=(obj.ft['FTRadius']), y=(obj.ft['FTIntensity']),
      legend='FT Intensity')


def _ft_imaginary_plot(obj, **kwargs):
    if not isinstance(obj, Spectrum):
        return
    missing_keys = obj.ft.get_missing_keys(('FTRadius', 'FTImaginary'))
    if missing_keys:
        _logger.error('missing keys:', missing_keys, 'unable to compute spectrum plot')
        return
    return _CurveOperation(x=(obj.ft['FTRadius']), y=(obj.ft['FTImaginary']),
      legend='FT Imaginary',
      color='red')