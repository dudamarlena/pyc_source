# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mpl_aea/aea.py
# Compiled at: 2017-04-14 21:04:55
""" 
    Native matplotlib support of frequently used 2d projections,
    for looking up to the sky.

    This file is initially developed as part of skymapper by Peter Melchior
    based on the example in matplotlib.

    It is later adopted by me (Yu Feng), and I will maintain a copy in
    imaginglss for easier access, also because I do plan to clean up
    the function signatures and variable naming (breaking compatibility with
    old skymapper code).

    The current version adds the ability to generate equal area histograms
    on HealPix pixels.

    It does not depend on healpy, there is a minimal python implementation of 
    healpix at the end of the file; imported in the javascript/lua style.
    
    The intention is one day we will submit a PR of this to matplotlib.

    What does not work:
        
        1. Panning.
        2. Color bar is sometimes in the wrong place
        3. Label locations are poorly calculated.

    What does work:
        Evertying else.

    Author: Yu Feng 
            Peter Melchior

"""
from __future__ import unicode_literals
import matplotlib
from matplotlib.axes import Axes
from matplotlib.patches import Polygon
from matplotlib.path import Path
from matplotlib.ticker import NullLocator, Formatter, FixedLocator, MaxNLocator
from matplotlib.transforms import Affine2D, BboxTransformTo, Transform, blended_transform_factory, Bbox, IdentityTransform
import matplotlib.spines as mspines, matplotlib.axis as maxis, numpy as np
from . import healpix
from .collections import HealpixQuadCollection, HealpixTriCollection, HealpixHistogram
__author__ = b'Yu Feng'
__email__ = b'rainwoodman@gmail.com'

class SkymapperTransform(Transform):
    input_dims = 2
    output_dims = 2
    is_separable = False

    def __init__(self, **kwargs):
        self.dec0 = 0
        self.ra0 = 180
        self.dec1 = -60
        self.dec2 = 30
        Transform.__init__(self, **kwargs)
        self._update()

    def _update(self):
        pass

    def set_center(self, center):
        ra0, dec0 = center
        self.ra0 = ra0
        self.dec0 = dec0
        self._update()

    def set_dec1(self, dec1):
        self.dec1 = dec1
        self._update()

    def set_dec2(self, dec2):
        self.dec2 = dec2
        self._update()

    def vertices_into_view(self, v):
        v = v.copy()
        diff = v[(Ellipsis, 0)] - v[(Ellipsis, 0, 0)][:, None]
        v00 = v[(Ellipsis, 0, 0)] - self.ra0
        while (v00 > 180).any():
            v00[(v00 > 180)] -= 360

        while (v00 < -180).any():
            v00[(v00 < -180)] += 360

        v00 += self.ra0
        v[(Ellipsis, 0)] = v00[:, None] + diff
        return v


class SkymapperAxes(Axes):
    """
    A base class for a Skymapper axes that takes in ra0, dec0, dec1, dec2.

    The base class takes care of clipping and interpolating with matplotlib.

    Subclass and override class method get_projection_class.

    """
    name = None

    @classmethod
    def get_projection_class(kls):
        raise NotImplementedError(b'Must implement this in subclass')

    def __init__(self, *args, **kwargs):
        self.ra0 = None
        self.dec0 = None
        self.dec1 = None
        self.dec2 = None
        Axes.__init__(self, *args, **kwargs)
        self.cla()
        return

    def _init_axis(self):
        self.xaxis = maxis.XAxis(self)
        self.spines[b'bottom'].register_axis(self.xaxis)
        self.spines[b'top'].register_axis(self.xaxis)
        self.yaxis = maxis.YAxis(self)
        self.spines[b'left'].register_axis(self.yaxis)
        self.spines[b'right'].register_axis(self.yaxis)
        self.yaxis.set_tick_params(pad=-12)
        self.xaxis.set_tick_params(pad=-12)
        self._update_transScale()

    def cla(self):
        """
        Override to set up some reasonable defaults.
        """
        Axes.cla(self)
        self.patch.set_transform(self.transClip)
        self.xaxis.set_minor_locator(NullLocator())
        self.yaxis.set_minor_locator(NullLocator())
        self.xaxis.set_major_locator(MaxNLocator(5, prune=b'both'))
        self.yaxis.set_major_locator(MaxNLocator(5, prune=b'both'))
        self.xaxis.set_ticks_position(b'none')
        self.yaxis.set_ticks_position(b'none')
        self.set_center(None, None)
        self._tight = True
        self._xmargin = 0
        self._ymargin = 0
        return

    def _set_lim_and_transforms(self):
        """
        This is called once when the plot is created to set up all the
        transforms for the data, text and grids.
        """
        self.transProjection = self.get_projection_class()()
        self.transProjection.set_center((180, 0))
        self.transProjection.set_dec1(-65)
        self.transProjection.set_dec2(80)
        self.transAffine = Affine2D()
        self.transAxes = BboxTransformTo(self.bbox)
        self.transData = self.transProjection + self.transAffine + self.transAxes
        self.transClip = self.transProjection + self.transAffine + self.transAxes
        self._xaxis_pretransform = Affine2D().scale(1.0, 180).translate(0.0, -90)
        self._xaxis_transform = self._xaxis_pretransform + self.transData
        self._xaxis_text1_transform = self._xaxis_pretransform + self.transData
        self._xaxis_text2_transform = self._xaxis_pretransform + self.transData
        self._yaxis_stretch = Affine2D().scale(360, 1.0).translate(0.0, 0.0)
        self._yaxis_stretch1 = Affine2D().scale(360, 1.0).translate(0.0, 0.0)
        self._yaxis_stretch2 = Affine2D().scale(360, 1.0).translate(0.0, 0.0)
        self._yaxis_transform = self._yaxis_stretch + self.transData
        self._yaxis_text1_transform = self._yaxis_stretch1 + self.transData
        self._yaxis_text2_transform = self._yaxis_stretch2 + self.transData

    def _update_affine(self):
        if self.ra0 is None:
            x0, x1 = self.viewLim.intervalx
            ra0 = 0.5 * (x0 + x1)
        else:
            ra0 = self.ra0
        if self.dec0 is None:
            y0, y1 = self.viewLim.intervaly
            dec0 = 0.5 * (y0 + y1)
        else:
            dec0 = self.dec0
        if self.dec1 is None:
            y0, y1 = self.viewLim.intervaly
            dec1 = -max(abs(y0), abs(y1)) * 11.0 / 12
        else:
            dec1 = self.dec1
        if self.dec2 is None:
            y0, y1 = self.viewLim.intervaly
            dec2 = -dec1
        else:
            dec2 = self.dec2
        self.transProjection.set_center((ra0, dec0))
        self.transProjection.set_dec1(dec1)
        self.transProjection.set_dec2(dec2)
        self._yaxis_stretch.clear().scale(self.viewLim.width, 1.0).translate(self.viewLim.x0, 0)
        self._yaxis_stretch1.clear().scale(self.viewLim.width, 1.0).translate(self.viewLim.x0 - 0.0 * self.viewLim.width, 0)
        self._yaxis_stretch2.clear().scale(self.viewLim.width, 1.0).translate(self.viewLim.x0 + 0.0 * self.viewLim.width, 0)
        self._xaxis_pretransform.clear().scale(1.0, self.viewLim.height).translate(0.0, self.viewLim.y0)
        corners_data = np.array([[self.viewLim.x0, self.viewLim.y0],
         [
          ra0, self.viewLim.y0],
         [
          self.viewLim.x1, self.viewLim.y0],
         [
          self.viewLim.x1, self.viewLim.y1],
         [
          self.viewLim.x0, self.viewLim.y1]])
        corners = self.transProjection.transform_non_affine(corners_data)
        x0 = corners[0][0]
        x1 = corners[2][0]
        if x0 == x1:
            x1 = -x0
        y0 = corners[1][1]
        y1 = max([corners[3][1], corners[4][1]])
        xscale = x1 - x0
        yscale = y1 - y0
        self.transAffine.clear().translate(-(x0 + x1) * 0.5, -(y0 + y1) * 0.5).scale(0.95 / xscale, 0.95 / yscale).translate(0.5, 0.5)
        path = Path(corners_data)
        self.patch.set_xy(path.vertices)
        return

    def get_xaxis_transform(self, which=b'grid'):
        """
        Override this method to provide a transformation for the
        x-axis grid and ticks.
        """
        assert which in ('tick1', 'tick2', 'grid')
        return self._xaxis_transform

    def get_xaxis_text1_transform(self, pixelPad):
        """
        Override this method to provide a transformation for the
        x-axis tick labels.

        Returns a tuple of the form (transform, valign, halign)
        """
        return (
         self._xaxis_text1_transform + Affine2D().translate(0.0, pixelPad), b'center', b'center')

    def get_xaxis_text2_transform(self, pixelPad):
        """
        Override this method to provide a transformation for the
        secondary x-axis tick labels.

        Returns a tuple of the form (transform, valign, halign)
        """
        return (
         self._xaxis_text2_transform + Affine2D().translate(0.0, pixelPad), b'center', b'center')

    def get_yaxis_transform(self, which=b'grid'):
        """
        Override this method to provide a transformation for the
        y-axis grid and ticks.
        """
        assert which in ('tick1', 'tick2', 'grid')
        return self._yaxis_transform

    def get_yaxis_text1_transform(self, pixelPad):
        """
        Override this method to provide a transformation for the
        y-axis tick labels.

        Returns a tuple of the form (transform, valign, halign)
        """
        return (
         self._yaxis_text1_transform + Affine2D().translate(pixelPad, 0.0), b'center', b'center')

    def get_yaxis_text2_transform(self, pixelPad):
        """
        Override this method to provide a transformation for the
        secondary y-axis tick labels.

        Returns a tuple of the form (transform, valign, halign)
        """
        return (
         self._yaxis_text2_transform + Affine2D().translate(pixelPad, 0.0), b'center', b'center')

    def _gen_axes_patch(self):
        """
        ClipPath.

        Initially set to a size of 2 box in transAxes.

        After xlim and ylim are set, this will be changed to the actual
        region in transData.

        For unclear reason the very initial clip path is always applied
        to the grid. Therefore we set size to 2.0 to avoid bad clipping.
        """
        return Polygon([(0, 0), (0, 0), (0, 0), (0, 0)], fill=False)

    def _gen_axes_spines(self):
        d = {b'left': mspines.Spine.linear_spine(self, spine_type=b'left'), 
           b'right': mspines.Spine.linear_spine(self, spine_type=b'right'), 
           b'top': mspines.Spine.linear_spine(self, spine_type=b'top'), 
           b'bottom': mspines.Spine.linear_spine(self, spine_type=b'bottom')}
        d[b'left'].set_position(('axes', 0))
        d[b'right'].set_position(('axes', 1))
        d[b'top'].set_position(('axes', 0))
        d[b'bottom'].set_position(('axes', 1))
        return d

    def set_xscale(self, *args, **kwargs):
        if args[0] != b'linear':
            raise NotImplementedError
        Axes.set_xscale(self, *args, **kwargs)

    def set_yscale(self, *args, **kwargs):
        if args[0] != b'linear':
            raise NotImplementedError
        Axes.set_yscale(self, *args, **kwargs)

    def set_center(self, ra0, dec0):
        """ Set the center of ra """
        self.ra0 = ra0
        self.dec0 = dec0
        self._update_affine()

    def set_parallels(self, dec1, dec2):
        """ Set the parallels """
        self.dec1 = dec1
        self.dec2 = dec2
        self._update_affine()

    def set_xlim(self, *args, **kwargs):
        Axes.set_xlim(self, *args, **kwargs)
        x0, x1 = self.viewLim.intervalx
        if self.ra0 is not None:
            if not x0 <= self.transProjection.ra0 or not x1 > self.transProjection.ra0:
                raise ValueError(b'The given limit in RA does not enclose ra0')
        self._update_affine()
        return

    def set_ylim(self, *args, **kwargs):
        Axes.set_ylim(self, *args, **kwargs)
        self._update_affine()

    def _histmap(self, show, ra, dec, weights=None, nside=32, perarea=False, mean=False, range=None, **kwargs):
        r = healpix.histogrammap(ra, dec, weights, nside, perarea=perarea, range=range)
        if weights is not None:
            w, N = r
        else:
            w = r
        if mean:
            mask = N != 0
            w[mask] /= N[mask]
        else:
            mask = w > 0
        return (
         w, mask, show(w, mask, nest=False, **kwargs))

    def histmap(self, ra, dec, weights=None, nside=None, perarea=False, mean=False, range=None, **kwargs):
        """ Making a histogram with healpix for variables located at RA, DEC.

            Parameters
            ----------
            ra, dec : angular positions
            weights : the weight at the position
            nside : band width of the healpix map. None for automatically decided.
            perarea : normalized to per unit area
            mean : use the average per pixel instead of sum per pixel.
            range : filter ra dec to ((ra0, dec0), (ra1, dec1))
            cmap : color map
            vmin, vmax : min and max.

        """
        vmin = kwargs.pop(b'vmin', None)
        vmax = kwargs.pop(b'vmax', None)
        defaults = dict(rasterized=True, alpha=1.0, linewidth=0)
        defaults.update(kwargs)
        coll = HealpixHistogram(ra, dec, weights, nside, perarea, mean, range, transform=self.transData, **defaults)
        coll.set_clim(vmin=vmin, vmax=vmax)
        self.add_collection(coll)
        self._sci(coll)
        self.autoscale_view(tight=True)
        return coll

    def histcontour(self, ra, dec, weights=None, nside=32, perarea=False, mean=False, range=None, **kwargs):
        return self._histmap(self.mapcontour, ra, dec, weights, nside, perarea, mean, range, **kwargs)

    def histcontourf(self, ra, dec, weights=None, nside=32, perarea=False, mean=False, range=None, **kwargs):
        kwargs[b'filled'] = True
        return self._histmap(self.mapcontour, ra, dec, weights, nside, perarea, mean, range, **kwargs)

    def mapshow(self, map, mask=None, nest=False, shading=b'smooth', **kwargs):
        """ Display a healpix map """
        vmin = kwargs.pop(b'vmin', None)
        vmax = kwargs.pop(b'vmax', None)
        defaults = dict(rasterized=True, alpha=1.0, linewidth=0)
        defaults.update(kwargs)
        if mask is None:
            mask = map == map
        if shading == b'flat':
            coll = HealpixQuadCollection(map, mask, transform=self.transData, **defaults)
        elif shading == b'smooth':
            coll = HealpixTriCollection(map, mask, transform=self.transData, **defaults)
        coll.set_clim(vmin=vmin, vmax=vmax)
        self.add_collection(coll)
        self._sci(coll)
        self.autoscale_view(tight=True)
        return coll

    def mapcontour(self, map, mask=None, nest=False, **kwargs):
        """ Display a healpix map as coutours. This is approximate. """
        if mask is None:
            mask = map == map
        ra, dec = healpix.pix2radec(healpix.npix2nside(len(map)), mask.nonzero()[0])
        filled = kwargs.pop(b'filled', False)
        if filled:
            im = self.tricontourf(ra, dec, map[mask], **kwargs)
        else:
            im = self.tricontour(ra, dec, map[mask], **kwargs)
        self._sci(im)
        self.autoscale_view(tight=True)
        return im

    def format_coord(self, lon, lat):
        """
        Override this method to change how the values are displayed in
        the status bar.

        In this case, we want them to be displayed in degrees N/S/E/W.
        """
        lon = lon
        lat = lat
        if lat >= 0.0:
            ns = b'N'
        else:
            ns = b'S'
        if lon >= 0.0:
            ew = b'E'
        else:
            ew = b'W'
        return b'%f°%s, %f°%s' % (abs(lat), ns, abs(lon), ew)

    class DegreeFormatter(Formatter):
        """
        This is a custom formatter that converts the native unit of
        radians into (truncated) degrees and adds a degree symbol.
        """

        def __init__(self, round_to=1.0):
            self._round_to = round_to

        def __call__(self, x, pos=None):
            degrees = round(x / self._round_to) * self._round_to
            return b'%d°' % degrees

    def set_meridian_grid(self, degrees):
        """
        Set the number of degrees between each meridian grid.

        It provides a more convenient interface to set the ticking than set_xticks would.
        """
        x0, x1 = self.get_xlim()
        number = abs((x1 - x0) / degrees) + 1
        self.xaxis.set_major_locator(FixedLocator(np.linspace(x0, x1, number, True)[1:-1]))
        self.xaxis.set_major_formatter(self.DegreeFormatter(degrees))

    def set_parallel_grid(self, degrees):
        """
        Set the number of degrees between each meridian grid.

        It provides a more convenient interface than set_yticks would.
        """
        y0, y1 = self.get_ylim()
        number = (y1 - y0) / degrees + 1
        self.yaxis.set_major_locator(FixedLocator(np.linspace(y0, y1, number, True)[1:-1]))
        self.yaxis.set_major_formatter(self.DegreeFormatter(degrees))

    def _in_axes(self, mouseevent):
        if hasattr(self._pan_trans):
            return True
        else:
            return Axes._in_axes(self, mouseevent)

    def can_zoom(self):
        """
        Return True if this axes support the zoom box
        """
        return True

    def start_pan(self, x, y, button):
        self._pan_trans = self.transAxes.inverted() + blended_transform_factory(self._yaxis_stretch, self._xaxis_pretransform)

    def end_pan(self):
        delattr(self, b'_pan_trans')

    def drag_pan(self, button, key, x, y):
        pan1 = self._pan_trans.transform([(x, y)])[0]
        self.set_ra0(360 - pan1[0])
        self.set_dec0(pan1[1])
        self._update_affine()


class AlbersEqualAreaAxes(SkymapperAxes):
    """
    A custom class for the Albers Equal Area projection.

    https://en.wikipedia.org/wiki/Albers_projection
    """
    name = b'ast.aea'

    @classmethod
    def get_projection_class(kls):
        return kls.AlbersEqualAreaTransform

    class AlbersEqualAreaTransform(SkymapperTransform):
        """
        The base Hammer transform.
        """

        def __init__(self, **kwargs):
            SkymapperTransform.__init__(self, **kwargs)

        def _update(self):
            self.n = 0.5 * (np.sin(np.radians(self.dec1)) + np.sin(np.radians(self.dec2)))
            self.C = np.cos(np.radians(self.dec1)) ** 2 + 2 * self.n * np.sin(np.radians(self.dec1))
            self.rho0 = self.__rho__(self.dec0)

        def __rho__(self, dec):
            if self.n == 0:
                return np.sqrt(self.C - 2 * self.n * np.sin(np.radians(dec)))
            else:
                return np.sqrt(self.C - 2 * self.n * np.sin(np.radians(dec))) / self.n

        def transform_non_affine(self, ll):
            """
            Override the transform_non_affine method to implement the custom
            transform.

            The input and output are Nx2 numpy arrays.
            """
            ra = ll[:, 0]
            dec = ll[:, 1]
            ra0 = self.ra0
            ra_ = np.radians(ra - ra0)
            if self.n == 0:
                rt = np.array([
                 self.rho0 * ra_,
                 -self.rho0 * np.sin(np.radians(self.dec0) - np.sin(np.radians(dec)))]).T
            else:
                theta = self.n * ra_
                rho = self.__rho__(dec)
                rt = np.array([
                 rho * np.sin(theta),
                 self.rho0 - rho * np.cos(theta)]).T
            return rt

        def transform_path_non_affine(self, path):
            ra0 = self.ra0
            path = path.cleaned(curves=False)
            v = path.vertices
            diff = v[:, 0] - v[(0, 0)]
            v00 = v[0][0] - ra0
            while v00 > 180:
                v00 -= 360

            while v00 < -180:
                v00 += 360

            v00 += ra0
            v[:, 0] = v00 + diff
            nonstop = path.codes > 0
            path = Path(v[nonstop], path.codes[nonstop])
            isteps = int(path._interpolation_steps * 1.5)
            if isteps < 10:
                isteps = 10
            while True:
                ipath = path.interpolated(isteps)
                tiv = self.transform(ipath.vertices)
                itv = Path(self.transform(path.vertices)).interpolated(isteps).vertices
                if np.mean(np.abs(tiv - itv)) < 0.01:
                    break
                if isteps > 20:
                    break
                isteps = int(isteps * 1.5)

            return Path(tiv, ipath.codes)

        transform_path_non_affine.__doc__ = Transform.transform_path_non_affine.__doc__
        if matplotlib.__version__ < b'1.2':
            transform = transform_non_affine
            transform_path = transform_path_non_affine
            transform_path.__doc__ = Transform.transform_path.__doc__

        def inverted(self):
            return AlbersEqualAreaAxes.InvertedAlbersEqualAreaTransform(self)

        inverted.__doc__ = Transform.inverted.__doc__

    class InvertedAlbersEqualAreaTransform(Transform):
        """ Inverted transform.

            This will always only give values in the prime ra0-180 ~ ra0+180 range, I believe.
            So it is inherently broken. I wonder when matplotlib actually calls this function,
            given that interactive is disabled.
        """
        input_dims = 2
        output_dims = 2
        is_separable = False

        def __init__(self, inverted, **kwargs):
            Transform.__init__(self, **kwargs)
            self.inverted = inverted

        def transform_non_affine(self, xy):
            x = xy[:, 0]
            y = xy[:, 1]
            inverted = self.inverted
            rho = np.sqrt(x ** 2 + (inverted.rho0 - y) ** 2)
            if inverted.n == 0:
                rt = np.degrees([
                 np.radians(inverted.ra0) + x / inverted.rho0,
                 np.arcsin(y / inverted.rho0 + np.sin(np.radians(inverted.dec0)))]).T
                return rt
            elif inverted.n > 0:
                theta = np.degrees(np.arctan2(x, inverted.rho0 - y))
            else:
                theta = np.degrees(np.arctan2(-x, -(inverted.rho0 - y)))
            return np.degrees([np.radians(inverted.ra0) + theta / inverted.n,
             np.arcsin((inverted.C - (rho * inverted.n) ** 2) / (2 * inverted.n))]).T
            transform_non_affine.__doc__ = Transform.transform_non_affine.__doc__

        if matplotlib.__version__ < b'1.2':
            transform = transform_non_affine

        def inverted(self):
            return self.inverted

        inverted.__doc__ = Transform.inverted.__doc__