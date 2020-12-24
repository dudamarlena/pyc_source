# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\widgets\volumeviewers.py
# Compiled at: 2018-08-27 17:21:07
__author__ = 'Ronald J Pandolfi'
__copyright__ = 'Copyright 2016, CAMERA, LBL, ALS'
__credits__ = ['Ronald J Pandolfi', 'Dinesh Kumar', 'Singanallur Venkatakrishnan', 'Luis Luque', 'Alexander Hexemer']
__license__ = ''
__version__ = '1.2.1'
__maintainer__ = 'Ronald J Pandolfi'
__email__ = 'ronpandolfi@lbl.gov'
__status__ = 'Beta'
import os, imageio, numpy as np, pyqtgraph as pg
from PySide import QtCore, QtGui
from vispy import scene
from vispy.color import Colormap
from pipeline import loader
from xicam.widgets.customwidgets import histDialogButton

class VolumeViewer(QtGui.QWidget):
    sigImageChanged = QtCore.Signal()

    def __init__(self, path=None, data=None, *args, **kwargs):
        super(VolumeViewer, self).__init__()
        self.levels = [
         0, 1]
        ly = QtGui.QHBoxLayout()
        ly.setContentsMargins(0, 0, 0, 0)
        ly.setSpacing(0)
        self.volumeRenderWidget = VolumeRenderWidget()
        ly.addWidget(self.volumeRenderWidget.native)
        self.HistogramLUTWidget = None
        self.HistogramLUTWidget = pg.HistogramLUTWidget(image=self, parent=self)
        self.HistogramLUTWidget.setMaximumWidth(self.HistogramLUTWidget.minimumWidth() + 15)
        self.HistogramLUTWidget.setMinimumWidth(self.HistogramLUTWidget.minimumWidth() + 15)
        v = QtGui.QVBoxLayout()
        v.addWidget(self.HistogramLUTWidget)
        self.setButton = histDialogButton('Set', parent=self)
        self.setButton.setMaximumWidth(self.HistogramLUTWidget.minimumWidth() + 15)
        self.setButton.setMinimumWidth(self.HistogramLUTWidget.minimumWidth() + 15)
        self.setButton.connectToHistWidget(self.HistogramLUTWidget)
        v.addWidget(self.setButton)
        ly.addLayout(v)
        self.xregion = SliceWidget(parent=self)
        self.yregion = SliceWidget(parent=self)
        self.zregion = SliceWidget(parent=self)
        self.xregion.item.region.setRegion([0, 1000])
        self.yregion.item.region.setRegion([0, 1000])
        self.zregion.item.region.setRegion([0, 1000])
        self.xregion.sigSliceChanged.connect(self.setVolume)
        self.yregion.sigSliceChanged.connect(self.setVolume)
        self.zregion.sigSliceChanged.connect(self.setVolume)
        ly.addWidget(self.xregion)
        ly.addWidget(self.yregion)
        ly.addWidget(self.zregion)
        self.setLayout(ly)
        return

    @property
    def vol(self):
        return self.volumeRenderWidget.vol

    def getSlice(self):
        xslice = self.xregion.getSlice()
        yslice = self.yregion.getSlice()
        zslice = self.zregion.getSlice()
        return (xslice, yslice, zslice)

    def setVolume(self, vol=None, path=None, slicevol=True):
        if slicevol:
            sliceobj = self.getSlice()
            print 'Got slice', sliceobj
        else:
            sliceobj = 3 * (slice(0, None),)
        if vol is not None:
            vol = np.nan_to_num(vol)
        self.volumeRenderWidget.setVolume(vol, path, sliceobj)
        self.volumeRenderWidget.update()
        if vol is not None or path is not None:
            self.sigImageChanged.emit()
            for i, region in enumerate([self.xregion, self.yregion, self.zregion]):
                try:
                    region.item.region.setRegion([0, vol.shape[i]])
                except RuntimeError as e:
                    print e.message

        return

    def moveGradientTick(self, idx, pos):
        tick = self.HistogramLUTWidget.item.gradient.listTicks()[idx][0]
        tick.setPos(pos, 0)
        tick.view().tickMoved(tick, QtCore.QPoint(pos * self.HistogramLUTWidget.item.gradient.length, 0))
        tick.sigMoving.emit(tick)
        tick.sigMoved.emit(tick)
        tick.view().tickMoveFinished(tick)

    def setLevels(self, levels, update=True):
        self.levels = levels
        self.setLookupTable()
        if self.HistogramLUTWidget:
            self.HistogramLUTWidget.region.setRegion(levels)
        if update:
            self.volumeRenderWidget.update()

    def setLookupTable(self, lut=None, update=True):
        try:
            table = self.HistogramLUTWidget.item.gradient.colorMap().color / 256.0
            pos = self.HistogramLUTWidget.item.gradient.colorMap().pos
            table[:, 3] = pos
            table = np.vstack([np.array([[0, 0, 0, 0]]), table, np.array([[1, 1, 1, 1]])])
            pos = np.hstack([[0], pos * (self.levels[1] - self.levels[0]) + self.levels[0], [1]])
            self.volumeRenderWidget.volume.cmap = Colormap(table, controls=pos)
        except AttributeError as ex:
            print ex

    def getHistogram(self, bins='auto', step='auto', targetImageSize=100, targetHistogramSize=500, **kwds):
        """Returns x and y arrays containing the histogram values for the current image.
        For an explanation of the return format, see numpy.histogram().

        The *step* argument causes pixels to be skipped when computing the histogram to save time.
        If *step* is 'auto', then a step is chosen such that the analyzed data has
        dimensions roughly *targetImageSize* for each axis.

        The *bins* argument and any extra keyword arguments are passed to
        np.histogram(). If *bins* is 'auto', then a bin number is automatically
        chosen based on the image characteristics:

        * Integer images will have approximately *targetHistogramSize* bins,
          with each bin having an integer width.
        * All other types will have *targetHistogramSize* bins.

        This method is also used when automatically computing levels.
        """
        if self.vol is None:
            return (None, None)
        else:
            if step == 'auto':
                step = (
                 int(np.ceil(float(self.vol.shape[0]) / targetImageSize)),
                 int(np.ceil(float(self.vol.shape[1]) / targetImageSize)))
            if np.isscalar(step):
                step = (
                 step, step)
            stepData = self.vol[::step[0], ::step[1]]
            if bins == 'auto':
                if stepData.dtype.kind in 'ui':
                    mn = stepData.min()
                    mx = stepData.max()
                    step = np.ceil((mx - mn) / 500.0)
                    bins = np.arange(mn, mx + 1.01 * step, step, dtype=np.int)
                    if len(bins) == 0:
                        bins = [
                         mn, mx]
                else:
                    bins = 500
            kwds['bins'] = bins
            hist = np.histogram(stepData, **kwds)
            return (
             hist[1][:-1], hist[0])

    def writevideo(self, fps=25):
        writer = imageio.save('foo.mp4', fps=25)
        self.volumeRenderWidget.events.draw.connect(lambda e: writer.append_data(self.render()))
        self.volumeRenderWidget.events.close.connect(lambda e: writer.close())


class VolumeVisual(scene.visuals.Volume):

    def set_data(self, vol, clim=None):
        """ Set the volume data.

        Parameters
        ----------
        vol : ndarray
            The 3D volume.
        clim : tuple | None
            Colormap limits to use. None will use the min and max values.
        """
        if not isinstance(vol, np.ndarray):
            raise ValueError('Volume visual needs a numpy array.')
        if not (vol.ndim == 3 or vol.ndim == 4 and vol.shape[(-1)] <= 4):
            raise ValueError('Volume visual needs a 3D image.')
        if clim is not None:
            clim = np.array(clim, float)
            if not (clim.ndim == 1 and clim.size == 2):
                raise ValueError('clim must be a 2-element array-like')
            self._clim = tuple(clim)
        self._clim = (
         vol.min(), vol.max())
        vol = np.array(vol, dtype='float32', copy=False)
        vol -= self._clim[0]
        vol *= 1.0 / (self._clim[1] - self._clim[0])
        self._tex.set_data(vol)
        self._program['u_shape'] = (vol.shape[2], vol.shape[1], vol.shape[0])
        self._vol_shape = vol.shape[:3]
        if self._index_buffer is None:
            self._create_vertex_data()
        return


class SliceWidget(pg.HistogramLUTWidget):
    sigSliceChanged = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(SliceWidget, self).__init__(*args, **kwargs)
        self.item.paint = lambda *x: None
        self.item.vb.deleteLater()
        self.item.gradient.gradRect.hide()
        self.item.gradient.allowAdd = False
        self.setMinimumWidth(70)
        self.setMaximumWidth(70)
        self.item.sigLookupTableChanged.connect(self.ticksChanged)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

    def sizeHint(self):
        return QtCore.QSize(70, 200)

    def ticksChanged(self, LUT):
        self.sigSliceChanged.emit()

    def getSlice(self):
        bounds = sorted(self.item.gradient.ticks.values())
        bounds = (bounds[0] * self.item.region.getRegion()[1], bounds[1] * self.item.region.getRegion()[1])
        return slice(*bounds)


scene.visuals.Volume = VolumeVisual

class VolumeRenderWidget(scene.SceneCanvas):

    def __init__(self, vol=None, path=None, size=(800, 600), show=False):
        super(VolumeRenderWidget, self).__init__(keys='interactive', size=size, show=show)
        self.measure_fps()
        self.view = self.central_widget.add_view()
        self.vol = None
        self.setVolume(vol, path)
        self.volume = None
        fov = 60.0
        self.cam1 = scene.cameras.FlyCamera(parent=self.view.scene, fov=fov, name='Fly')
        self.cam2 = scene.cameras.TurntableCamera(parent=self.view.scene, fov=fov, name='Turntable')
        self.cam3 = scene.cameras.ArcballCamera(parent=self.view.scene, fov=fov, name='Arcball')
        self.view.camera = self.cam2
        return

    def setVolume(self, vol=None, path=None, sliceobj=None):
        if path is not None and vol is None:
            if '*' in path:
                vol = loader.loadimageseries(path)
            elif os.path.splitext(path)[(-1)] == '.npy':
                vol = loader.loadimage(path)
            else:
                vol = loader.loadtiffstack(path)
        elif vol is None:
            vol = self.vol
        if vol is None:
            return
        else:
            self.vol = vol
            if slice is not None:

                def intify(a):
                    if a is not None:
                        return int(a)
                    else:
                        return

                sliceobj = [ slice(intify(s.start), intify(s.stop), intify(s.step)) for s in sliceobj ]
                slicevol = self.vol[sliceobj]
            else:
                slicevol = self.vol
            emulate_texture = False
            if self.volume is None:
                self.volume = scene.visuals.Volume(slicevol, parent=self.view.scene, emulate_texture=emulate_texture)
                self.volume.method = 'translucent'
            else:
                self.volume.set_data(slicevol)
                self.volume._create_vertex_data()
            scale = 3 * (2.0 / self.vol.shape[1],)
            translate = map(lambda x: -scale[0] * x / 2, reversed(vol.shape))
            self.volume.transform = scene.STTransform(translate=translate, scale=scale)
            return

    def on_key_press(self, event):
        if event.text == '1':
            cam_toggle = {self.cam1: self.cam2, self.cam2: self.cam3, self.cam3: self.cam1}
            self.view.camera = cam_toggle.get(self.view.camera, self.cam2)
            print self.view.camera.name + ' camera'
        elif event.text == '2':
            pass
        elif event.text == '3':
            pass
        elif event.text == '4':
            pass
        elif event.text == '0':
            self.cam1.set_range()
            self.cam3.set_range()
        elif event.text != '' and event.text in '[]':
            s = -0.025 if event.text == '[' else 0.025
            self.volume.threshold += s
            th = self.volume.threshold
            print 'Isosurface threshold: %0.3f' % th