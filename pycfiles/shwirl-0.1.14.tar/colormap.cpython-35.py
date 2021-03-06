# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/color/colormap.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 38759 bytes
from __future__ import division
import inspect, numpy as np
from .color_array import ColorArray
from ..ext.six import string_types
from ..ext.cubehelix import cubehelix
from ..ext.husl import husl_to_rgb

def _vector_or_scalar(x, type='row'):
    """Convert an object to either a scalar or a row or column vector."""
    if isinstance(x, (list, tuple)):
        x = np.array(x)
    if isinstance(x, np.ndarray):
        assert x.ndim == 1
        if type == 'column':
            x = x[:, None]
    return x


def _vector(x, type='row'):
    """Convert an object to a row or column vector."""
    if isinstance(x, (list, tuple)):
        x = np.array(x, dtype=np.float32)
    else:
        if not isinstance(x, np.ndarray):
            x = np.array([x], dtype=np.float32)
        if not x.ndim == 1:
            raise AssertionError
    if type == 'column':
        x = x[:, None]
    return x


def _find_controls(x, controls=None, clip=None):
    x_controls = np.clip(np.searchsorted(controls, x) - 1, 0, clip)
    return x_controls.astype(np.int32)


def _normalize(x, cmin=None, cmax=None, clip=True):
    """Normalize an array from the range [cmin, cmax] to [0,1],
    with optional clipping."""
    if not isinstance(x, np.ndarray):
        x = np.array(x)
    if cmin is None:
        cmin = x.min()
    if cmax is None:
        cmax = x.max()
    if cmin == cmax:
        return 0.5 * np.ones(x.shape)
    else:
        cmin, cmax = float(cmin), float(cmax)
        y = (x - cmin) * 1.0 / (cmax - cmin)
        if clip:
            y = np.clip(y, 0.0, 1.0)
        return y


def _mix_simple(a, b, x):
    """Mix b (with proportion x) with a."""
    x = np.clip(x, 0.0, 1.0)
    return (1.0 - x) * a + x * b


def _interpolate_multi(colors, x, controls):
    x = x.ravel()
    n = len(colors)
    x_step = _find_controls(x, controls, n - 2)
    controls_length = np.diff(controls).astype(np.float32)
    controls_length[controls_length == 0.0] = 1.0
    _to_clip = x - controls[x_step]
    _to_clip /= controls_length[x_step]
    x_rel = np.clip(_to_clip, 0.0, 1.0)
    return (colors[x_step],
     colors[(x_step + 1)],
     x_rel[:, None])


def mix(colors, x, controls=None):
    a, b, x_rel = _interpolate_multi(colors, x, controls)
    return _mix_simple(a, b, x_rel)


def smoothstep(edge0, edge1, x):
    """ performs smooth Hermite interpolation
        between 0 and 1 when edge0 < x < edge1.  """
    x = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return x * x * (3 - 2 * x)


def step(colors, x, controls=None):
    x = x.ravel()
    assert (
     controls[0], controls[(-1)]) == (0.0, 1.0)
    ncolors = len(colors)
    assert ncolors == len(controls) - 1
    assert ncolors >= 2
    x_step = _find_controls(x, controls, ncolors - 1)
    return colors[(x_step, ...)]


def _glsl_mix(controls=None):
    """Generate a GLSL template function from a given interpolation patterns
    and control points."""
    assert (
     controls[0], controls[(-1)]) == (0.0, 1.0)
    ncolors = len(controls)
    assert ncolors >= 2
    if ncolors == 2:
        s = '    return mix($color_0, $color_1, t);\n'
    else:
        s = ''
        for i in range(ncolors - 1):
            if i == 0:
                ifs = 'if (t < %.6f)' % controls[(i + 1)]
            else:
                if i == ncolors - 2:
                    ifs = 'else'
                else:
                    ifs = 'else if (t < %.6f)' % controls[(i + 1)]
            adj_t = '(t - %s) / %s' % (controls[i],
             controls[(i + 1)] - controls[i])
            s += '%s {\n    return mix($color_%d, $color_%d, %s);\n} ' % (
             ifs, i, i + 1, adj_t)

    return 'vec4 colormap(float t) {\n%s\n}' % s


def _glsl_step(controls=None):
    assert (controls[0], controls[(-1)]) == (0.0, 1.0)
    ncolors = len(controls) - 1
    assert ncolors >= 2
    s = ''
    for i in range(ncolors - 1):
        if i == 0:
            ifs = 'if (t < %.6f)' % controls[(i + 1)]
        else:
            if i == ncolors - 2:
                ifs = 'else'
            else:
                ifs = 'else if (t < %.6f)' % controls[(i + 1)]
        s += '%s {\n    return $color_%d;\n} ' % (ifs, i)

    return 'vec4 colormap(float t) {\n%s\n}' % s


def _process_glsl_template(template, colors):
    """Replace $color_i by color #i in the GLSL template."""
    for i in range(len(colors) - 1, -1, -1):
        color = colors[i]
        assert len(color) == 4
        vec4_color = 'vec4(%.3f, %.3f, %.3f, %.3f)' % tuple(color)
        template = template.replace('$color_%d' % i, vec4_color)

    return template


class BaseColormap(object):
    __doc__ = 'Class representing a colormap:\n\n        t \\in [0, 1] --> rgba_color\n\n    Parameters\n    ----------\n    colors : list of lists, tuples, or ndarrays\n        The control colors used by the colormap (shape = (ncolors, 4)).\n\n    Notes\n    -----\n    Must be overriden. Child classes need to implement:\n\n    glsl_map : string\n        The GLSL function for the colormap. Use $color_0 to refer\n        to the first color in `colors`, and so on. These are vec4 vectors.\n    map(item) : function\n        Takes a (N, 1) vector of values in [0, 1], and returns a rgba array\n        of size (N, 4).\n\n    '
    colors = None
    glsl_map = None

    def __init__(self, colors=None):
        if colors is not None:
            self.colors = colors
        if not isinstance(self.colors, ColorArray):
            self.colors = ColorArray(self.colors)
        if len(self.colors) > 0:
            self.glsl_map = _process_glsl_template(self.glsl_map, self.colors.rgba)

    def map(self, item):
        """Return a rgba array for the requested items.

        This function must be overriden by child classes.

        This function doesn't need to implement argument checking on `item`.
        It can always assume that `item` is a (N, 1) array of values between
        0 and 1.

        Parameters
        ----------
        item : ndarray
            An array of values in [0,1].

        Returns
        -------
        rgba : ndarray
            An array with rgba values, with one color per item. The shape
            should be ``item.shape + (4,)``.

        Notes
        -----
        Users are expected to use a colormap with ``__getitem__()`` rather
        than ``map()`` (which implements a lower-level API).

        """
        raise NotImplementedError()

    def __getitem__(self, item):
        if isinstance(item, tuple):
            raise ValueError('ColorArray indexing is only allowed along the first dimension.')
        item = _vector(item, type='column')
        item = np.clip(item, 0.0, 1.0)
        colors = self.map(item)
        return ColorArray(colors)

    def __setitem__(self, item, value):
        raise RuntimeError('It is not possible to set items to BaseColormap instances.')

    def _repr_html_(self):
        n = 100
        html = '\n                <style>\n                    table.vispy_colormap {\n                        height: 30px;\n                        border: 0;\n                        margin: 0;\n                        padding: 0;\n                    }\n\n                    table.vispy_colormap td {\n                        width: 3px;\n                        border: 0;\n                        margin: 0;\n                        padding: 0;\n                    }\n                </style>\n                <table class="vispy_colormap">\n                ' + '\n'.join(['<td style="background-color: %s;"\n                                 title="%s"></td>' % (color, color) for color in self[np.linspace(0.0, 1.0, n)].hex]) + '\n                </table>\n                '
        return html


def _default_controls(ncolors):
    """Generate linearly spaced control points from a set of colors."""
    return np.linspace(0.0, 1.0, ncolors)


_interpolation_info = {'linear': {'ncontrols': lambda ncolors: ncolors, 
            'glsl_map': _glsl_mix, 
            'map': mix}, 
 
 'zero': {'ncontrols': lambda ncolors: ncolors + 1, 
          'glsl_map': _glsl_step, 
          'map': step}}

class Colormap(BaseColormap):
    __doc__ = "A colormap defining several control colors and an interpolation scheme.\n\n    Parameters\n    ----------\n    colors : list of colors | ColorArray\n        The list of control colors. If not a ``ColorArray``, a new\n        ``ColorArray`` instance is created from this list. See the\n        documentation of ``ColorArray``.\n    controls : array-like\n        The list of control points for the given colors. It should be\n        an increasing list of floating-point number between 0.0 and 1.0.\n        The first control point must be 0.0. The last control point must be\n        1.0. The number of control points depends on the interpolation scheme.\n    interpolation : str\n        The interpolation mode of the colormap. Default: 'linear'. Can also\n        be 'zero'.\n        If 'linear', ncontrols = ncolors (one color per control point).\n        If 'zero', ncontrols = ncolors+1 (one color per bin).\n\n    Examples\n    --------\n    Here is a basic example:\n\n        >>> from vispy.color import Colormap\n        >>> cm = Colormap(['r', 'g', 'b'])\n        >>> cm[0.], cm[0.5], cm[np.linspace(0., 1., 100)]\n\n    "

    def __init__(self, colors, controls=None, interpolation='linear'):
        self.interpolation = interpolation
        ncontrols = self._ncontrols(len(colors))
        if controls is None:
            controls = _default_controls(ncontrols)
        assert len(controls) == ncontrols
        self._controls = np.array(controls, dtype=np.float32)
        self.glsl_map = self._glsl_map_generator(self._controls)
        super(Colormap, self).__init__(colors)

    @property
    def interpolation(self):
        """The interpolation mode of the colormap"""
        return self._interpolation

    @interpolation.setter
    def interpolation(self, val):
        if val not in _interpolation_info:
            raise ValueError('The interpolation mode can only be one of: ' + ', '.join(sorted(_interpolation_info.keys())))
        info = _interpolation_info[val]
        self._glsl_map_generator = info['glsl_map']
        self._ncontrols = info['ncontrols']
        self._map_function = info['map']
        self._interpolation = val

    def map(self, x):
        """The Python mapping function from the [0,1] interval to a
        list of rgba colors

        Parameters
        ----------
        x : array-like
            The values to map.

        Returns
        -------
        colors : list
            List of rgba colors.
        """
        return self._map_function(self.colors.rgba, x, self._controls)


class CubeHelixColormap(Colormap):

    def __init__(self, start=0.5, rot=1, gamma=1.0, reverse=True, nlev=32, minSat=1.2, maxSat=1.2, minLight=0.0, maxLight=1.0, **kwargs):
        """Cube helix colormap

        A full implementation of Dave Green's "cubehelix" for Matplotlib.
        Based on the FORTRAN 77 code provided in
        D.A. Green, 2011, BASI, 39, 289.

        http://adsabs.harvard.edu/abs/2011arXiv1108.5083G

        User can adjust all parameters of the cubehelix algorithm.
        This enables much greater flexibility in choosing color maps, while
        always ensuring the color map scales in intensity from black
        to white. A few simple examples:

        Default color map settings produce the standard "cubehelix".

        Create color map in only blues by setting rot=0 and start=0.

        Create reverse (white to black) backwards through the rainbow once
        by setting rot=1 and reverse=True.

        Parameters
        ----------
        start : scalar, optional
            Sets the starting position in the color space. 0=blue, 1=red,
            2=green. Defaults to 0.5.
        rot : scalar, optional
            The number of rotations through the rainbow. Can be positive
            or negative, indicating direction of rainbow. Negative values
            correspond to Blue->Red direction. Defaults to -1.5
        gamma : scalar, optional
            The gamma correction for intensity. Defaults to 1.0
        reverse : boolean, optional
            Set to True to reverse the color map. Will go from black to
            white. Good for density plots where shade~density. Defaults to
            False
        nlev : scalar, optional
            Defines the number of discrete levels to render colors at.
            Defaults to 32.
        sat : scalar, optional
            The saturation intensity factor. Defaults to 1.2
            NOTE: this was formerly known as "hue" parameter
        minSat : scalar, optional
            Sets the minimum-level saturation. Defaults to 1.2
        maxSat : scalar, optional
            Sets the maximum-level saturation. Defaults to 1.2
        startHue : scalar, optional
            Sets the starting color, ranging from [0, 360], as in
            D3 version by @mbostock
            NOTE: overrides values in start parameter
        endHue : scalar, optional
            Sets the ending color, ranging from [0, 360], as in
            D3 version by @mbostock
            NOTE: overrides values in rot parameter
        minLight : scalar, optional
            Sets the minimum lightness value. Defaults to 0.
        maxLight : scalar, optional
            Sets the maximum lightness value. Defaults to 1.
        """
        super(CubeHelixColormap, self).__init__(cubehelix(start=start, rot=rot, gamma=gamma, reverse=reverse, nlev=nlev, minSat=minSat, maxSat=maxSat, minLight=minLight, maxLight=maxLight, **kwargs))


class _Fire(BaseColormap):
    colors = [
     (1.0, 1.0, 1.0, 1.0),
     (1.0, 1.0, 0.0, 1.0),
     (1.0, 0.0, 0.0, 1.0)]
    glsl_map = '\n    vec4 fire(float t) {\n        return mix(mix($color_0, $color_1, t),\n                   mix($color_1, $color_2, t*t), t);\n    }\n    '

    def map(self, t):
        a, b, d = self.colors.rgba
        c = _mix_simple(a, b, t)
        e = _mix_simple(b, d, t ** 2)
        return _mix_simple(c, e, t)


class _Grays(BaseColormap):
    glsl_map = '\n    vec4 grays(float t) {\n        return vec4(t, t, t, 1.0);\n    }\n    '

    def map(self, t):
        if isinstance(t, np.ndarray):
            return np.hstack([t, t, t, np.ones(t.shape)]).astype(np.float32)
        else:
            return np.array([t, t, t, 1.0], dtype=np.float32)


class _Ice(BaseColormap):
    glsl_map = '\n    vec4 ice(float t) {\n        return vec4(t, t, 1.0, 1.0);\n    }\n    '

    def map(self, t):
        if isinstance(t, np.ndarray):
            return np.hstack([t, t, np.ones(t.shape),
             np.ones(t.shape)]).astype(np.float32)
        else:
            return np.array([t, t, 1.0, 1.0], dtype=np.float32)


class _Hot(BaseColormap):
    colors = [
     (0.0, 0.33, 0.66, 1.0),
     (0.33, 0.66, 1.0, 1.0)]
    glsl_map = '\n    vec4 hot(float t) {\n        return vec4(smoothstep($color_0.rgb, $color_1.rgb, vec3(t, t, t)),\n                    1.0);\n    }\n    '

    def map(self, t):
        rgba = self.colors.rgba
        smoothed = smoothstep(rgba[0, :3], rgba[1, :3], t)
        return np.hstack((smoothed, np.ones((len(t), 1))))


class _Winter(BaseColormap):
    colors = [
     (0.0, 0.0, 1.0, 1.0),
     (0.0, 1.0, 0.5, 1.0)]
    glsl_map = '\n    vec4 winter(float t) {\n        return mix($color_0, $color_1, sqrt(t));\n    }\n    '

    def map(self, t):
        return _mix_simple(self.colors.rgba[0], self.colors.rgba[1], np.sqrt(t))


class _SingleHue(Colormap):
    __doc__ = 'A colormap which is solely defined by the given hue and value.\n\n    Given the color hue and value, this color map increases the saturation\n    of a color. The start color is almost white but still contains a hint of\n    the given color, and at the end the color is fully saturated.\n\n    Parameters\n    ----------\n    hue : scalar, optional\n        The hue refers to a "true" color, without any shading or tinting.\n        Must be in the range [0, 360]. Defaults to 200 (blue).\n    saturation_range : array-like, optional\n        The saturation represents how "pure" a color is. Less saturation means\n        more white light mixed in the color. A fully saturated color means\n        the pure color defined by the hue. No saturation means completely\n        white. This colormap changes the saturation, and with this parameter\n        you can specify the lower and upper bound. Default is [0.2, 0.8].\n    value : scalar, optional\n        The value defines the "brightness" of a color: a value of 0.0 means\n        completely black while a value of 1.0 means the color defined by the\n        hue without shading. Must be in the range [0, 1.0]. The default value\n        is 1.0.\n\n    Notes\n    -----\n    For more information about the hue values see the `wikipedia page`_.\n\n    .. _wikipedia page: https://en.wikipedia.org/wiki/Hue\n    '

    def __init__(self, hue=200, saturation_range=[0.1, 0.8], value=1.0):
        colors = ColorArray([
         (
          hue, saturation_range[0], value),
         (
          hue, saturation_range[1], value)], color_space='hsv')
        super(_SingleHue, self).__init__(colors)


class _HSL(Colormap):
    __doc__ = "A colormap which is defined by n evenly spaced points in\n    a circular color space.\n\n    This means that we change the hue value while keeping the\n    saturation and value constant.\n\n    Parameters\n    ---------\n    n_colors : int, optional\n        The number of colors to generate.\n    hue_start : int, optional\n        The hue start value. Must be in the range [0, 360], the default is 0.\n    saturation : float, optional\n        The saturation component of the colors to generate. The default is\n        fully saturated (1.0). Must be in the range [0, 1.0].\n    value : float, optional\n        The value (brightness) component of the colors to generate. Must\n        be in the range [0, 1.0], and the default is 1.0\n    controls : array-like, optional\n        The list of control points for the colors to generate. It should be\n        an increasing list of floating-point number between 0.0 and 1.0.\n        The first control point must be 0.0. The last control point must be\n        1.0. The number of control points depends on the interpolation scheme.\n    interpolation : str, optional\n        The interpolation mode of the colormap. Default: 'linear'. Can also\n        be 'zero'.\n        If 'linear', ncontrols = ncolors (one color per control point).\n        If 'zero', ncontrols = ncolors+1 (one color per bin).\n    "

    def __init__(self, ncolors=6, hue_start=0, saturation=1.0, value=1.0, controls=None, interpolation='linear'):
        hues = np.linspace(0, 360, ncolors + 1)[:-1]
        hues += hue_start
        hues %= 360
        colors = ColorArray([(hue, saturation, value) for hue in hues], color_space='hsv')
        super(_HSL, self).__init__(colors, controls=controls, interpolation=interpolation)


class _HUSL(Colormap):
    __doc__ = 'A colormap which is defined by n evenly spaced points in\n    the HUSL hue space.\n\n    Parameters\n    ---------\n    n_colors : int, optional\n        The number of colors to generate.\n    hue_start : int, optional\n        The hue start value. Must be in the range [0, 360], the default is 0.\n    saturation : float, optional\n        The saturation component of the colors to generate. The default is\n        fully saturated (1.0). Must be in the range [0, 1.0].\n    value : float, optional\n        The value component of the colors to generate or "brightness". Must\n        be in the range [0, 1.0], and the default is 0.7.\n    controls : array-like, optional\n        The list of control points for the colors to generate. It should be\n        an increasing list of floating-point number between 0.0 and 1.0.\n        The first control point must be 0.0. The last control point must be\n        1.0. The number of control points depends on the interpolation scheme.\n    interpolation : str, optional\n        The interpolation mode of the colormap. Default: \'linear\'. Can also\n        be \'zero\'.\n        If \'linear\', ncontrols = ncolors (one color per control point).\n        If \'zero\', ncontrols = ncolors+1 (one color per bin).\n\n    Notes\n    -----\n    For more information about HUSL colors see http://husl-colors.org\n    '

    def __init__(self, ncolors=6, hue_start=0, saturation=1.0, value=0.7, controls=None, interpolation='linear'):
        hues = np.linspace(0, 360, ncolors + 1)[:-1]
        hues += hue_start
        hues %= 360
        saturation *= 99
        value *= 99
        colors = ColorArray([husl_to_rgb(hue, saturation, value) for hue in hues])
        super(_HUSL, self).__init__(colors, controls=controls, interpolation=interpolation)


class _Diverging(Colormap):

    def __init__(self, h_pos=20, h_neg=250, saturation=1.0, value=0.7, center='light'):
        saturation *= 99
        value *= 99
        start = husl_to_rgb(h_neg, saturation, value)
        mid = (0.133, 0.133, 0.133) if center == 'dark' else (0.92, 0.92, 0.92)
        end = husl_to_rgb(h_pos, saturation, value)
        colors = ColorArray([start, mid, end])
        super(_Diverging, self).__init__(colors)


_viridis_data = [
 [
  0.267004, 0.004874, 0.329415],
 [
  0.26851, 0.009605, 0.335427],
 [
  0.269944, 0.014625, 0.341379],
 [
  0.271305, 0.019942, 0.347269],
 [
  0.272594, 0.025563, 0.353093],
 [
  0.273809, 0.031497, 0.358853],
 [
  0.274952, 0.037752, 0.364543],
 [
  0.276022, 0.044167, 0.370164],
 [
  0.277018, 0.050344, 0.375715],
 [
  0.277941, 0.056324, 0.381191],
 [
  0.278791, 0.062145, 0.386592],
 [
  0.279566, 0.067836, 0.391917],
 [
  0.280267, 0.073417, 0.397163],
 [
  0.280894, 0.078907, 0.402329],
 [
  0.281446, 0.08432, 0.407414],
 [
  0.281924, 0.089666, 0.412415],
 [
  0.282327, 0.094955, 0.417331],
 [
  0.282656, 0.100196, 0.42216],
 [
  0.28291, 0.105393, 0.426902],
 [
  0.283091, 0.110553, 0.431554],
 [
  0.283197, 0.11568, 0.436115],
 [
  0.283229, 0.120777, 0.440584],
 [
  0.283187, 0.125848, 0.44496],
 [
  0.283072, 0.130895, 0.449241],
 [
  0.282884, 0.13592, 0.453427],
 [
  0.282623, 0.140926, 0.457517],
 [
  0.28229, 0.145912, 0.46151],
 [
  0.281887, 0.150881, 0.465405],
 [
  0.281412, 0.155834, 0.469201],
 [
  0.280868, 0.160771, 0.472899],
 [
  0.280255, 0.165693, 0.476498],
 [
  0.279574, 0.170599, 0.479997],
 [
  0.278826, 0.17549, 0.483397],
 [
  0.278012, 0.180367, 0.486697],
 [
  0.277134, 0.185228, 0.489898],
 [
  0.276194, 0.190074, 0.493001],
 [
  0.275191, 0.194905, 0.496005],
 [
  0.274128, 0.199721, 0.498911],
 [
  0.273006, 0.20452, 0.501721],
 [
  0.271828, 0.209303, 0.504434],
 [
  0.270595, 0.214069, 0.507052],
 [
  0.269308, 0.218818, 0.509577],
 [
  0.267968, 0.223549, 0.512008],
 [
  0.26658, 0.228262, 0.514349],
 [
  0.265145, 0.232956, 0.516599],
 [
  0.263663, 0.237631, 0.518762],
 [
  0.262138, 0.242286, 0.520837],
 [
  0.260571, 0.246922, 0.522828],
 [
  0.258965, 0.251537, 0.524736],
 [
  0.257322, 0.25613, 0.526563],
 [
  0.255645, 0.260703, 0.528312],
 [
  0.253935, 0.265254, 0.529983],
 [
  0.252194, 0.269783, 0.531579],
 [
  0.250425, 0.27429, 0.533103],
 [
  0.248629, 0.278775, 0.534556],
 [
  0.246811, 0.283237, 0.535941],
 [
  0.244972, 0.287675, 0.53726],
 [
  0.243113, 0.292092, 0.538516],
 [
  0.241237, 0.296485, 0.539709],
 [
  0.239346, 0.300855, 0.540844],
 [
  0.237441, 0.305202, 0.541921],
 [
  0.235526, 0.309527, 0.542944],
 [
  0.233603, 0.313828, 0.543914],
 [
  0.231674, 0.318106, 0.544834],
 [
  0.229739, 0.322361, 0.545706],
 [
  0.227802, 0.326594, 0.546532],
 [
  0.225863, 0.330805, 0.547314],
 [
  0.223925, 0.334994, 0.548053],
 [
  0.221989, 0.339161, 0.548752],
 [
  0.220057, 0.343307, 0.549413],
 [
  0.21813, 0.347432, 0.550038],
 [
  0.21621, 0.351535, 0.550627],
 [
  0.214298, 0.355619, 0.551184],
 [
  0.212395, 0.359683, 0.55171],
 [
  0.210503, 0.363727, 0.552206],
 [
  0.208623, 0.367752, 0.552675],
 [
  0.206756, 0.371758, 0.553117],
 [
  0.204903, 0.375746, 0.553533],
 [
  0.203063, 0.379716, 0.553925],
 [
  0.201239, 0.38367, 0.554294],
 [
  0.19943, 0.387607, 0.554642],
 [
  0.197636, 0.391528, 0.554969],
 [
  0.19586, 0.395433, 0.555276],
 [
  0.1941, 0.399323, 0.555565],
 [
  0.192357, 0.403199, 0.555836],
 [
  0.190631, 0.407061, 0.556089],
 [
  0.188923, 0.41091, 0.556326],
 [
  0.187231, 0.414746, 0.556547],
 [
  0.185556, 0.41857, 0.556753],
 [
  0.183898, 0.422383, 0.556944],
 [
  0.182256, 0.426184, 0.55712],
 [
  0.180629, 0.429975, 0.557282],
 [
  0.179019, 0.433756, 0.55743],
 [
  0.177423, 0.437527, 0.557565],
 [
  0.175841, 0.44129, 0.557685],
 [
  0.174274, 0.445044, 0.557792],
 [
  0.172719, 0.448791, 0.557885],
 [
  0.171176, 0.45253, 0.557965],
 [
  0.169646, 0.456262, 0.55803],
 [
  0.168126, 0.459988, 0.558082],
 [
  0.166617, 0.463708, 0.558119],
 [
  0.165117, 0.467423, 0.558141],
 [
  0.163625, 0.471133, 0.558148],
 [
  0.162142, 0.474838, 0.55814],
 [
  0.160665, 0.47854, 0.558115],
 [
  0.159194, 0.482237, 0.558073],
 [
  0.157729, 0.485932, 0.558013],
 [
  0.15627, 0.489624, 0.557936],
 [
  0.154815, 0.493313, 0.55784],
 [
  0.153364, 0.497, 0.557724],
 [
  0.151918, 0.500685, 0.557587],
 [
  0.150476, 0.504369, 0.55743],
 [
  0.149039, 0.508051, 0.55725],
 [
  0.147607, 0.511733, 0.557049],
 [
  0.14618, 0.515413, 0.556823],
 [
  0.144759, 0.519093, 0.556572],
 [
  0.143343, 0.522773, 0.556295],
 [
  0.141935, 0.526453, 0.555991],
 [
  0.140536, 0.530132, 0.555659],
 [
  0.139147, 0.533812, 0.555298],
 [
  0.13777, 0.537492, 0.554906],
 [
  0.136408, 0.541173, 0.554483],
 [
  0.135066, 0.544853, 0.554029],
 [
  0.133743, 0.548535, 0.553541],
 [
  0.132444, 0.552216, 0.553018],
 [
  0.131172, 0.555899, 0.552459],
 [
  0.129933, 0.559582, 0.551864],
 [
  0.128729, 0.563265, 0.551229],
 [
  0.127568, 0.566949, 0.550556],
 [
  0.126453, 0.570633, 0.549841],
 [
  0.125394, 0.574318, 0.549086],
 [
  0.124395, 0.578002, 0.548287],
 [
  0.123463, 0.581687, 0.547445],
 [
  0.122606, 0.585371, 0.546557],
 [
  0.121831, 0.589055, 0.545623],
 [
  0.121148, 0.592739, 0.544641],
 [
  0.120565, 0.596422, 0.543611],
 [
  0.120092, 0.600104, 0.54253],
 [
  0.119738, 0.603785, 0.5414],
 [
  0.119512, 0.607464, 0.540218],
 [
  0.119423, 0.611141, 0.538982],
 [
  0.119483, 0.614817, 0.537692],
 [
  0.119699, 0.61849, 0.536347],
 [
  0.120081, 0.622161, 0.534946],
 [
  0.120638, 0.625828, 0.533488],
 [
  0.12138, 0.629492, 0.531973],
 [
  0.122312, 0.633153, 0.530398],
 [
  0.123444, 0.636809, 0.528763],
 [
  0.12478, 0.640461, 0.527068],
 [
  0.126326, 0.644107, 0.525311],
 [
  0.128087, 0.647749, 0.523491],
 [
  0.130067, 0.651384, 0.521608],
 [
  0.132268, 0.655014, 0.519661],
 [
  0.134692, 0.658636, 0.517649],
 [
  0.137339, 0.662252, 0.515571],
 [
  0.14021, 0.665859, 0.513427],
 [
  0.143303, 0.669459, 0.511215],
 [
  0.146616, 0.67305, 0.508936],
 [
  0.150148, 0.676631, 0.506589],
 [
  0.153894, 0.680203, 0.504172],
 [
  0.157851, 0.683765, 0.501686],
 [
  0.162016, 0.687316, 0.499129],
 [
  0.166383, 0.690856, 0.496502],
 [
  0.170948, 0.694384, 0.493803],
 [
  0.175707, 0.6979, 0.491033],
 [
  0.180653, 0.701402, 0.488189],
 [
  0.185783, 0.704891, 0.485273],
 [
  0.19109, 0.708366, 0.482284],
 [
  0.196571, 0.711827, 0.479221],
 [
  0.202219, 0.715272, 0.476084],
 [
  0.20803, 0.718701, 0.472873],
 [
  0.214, 0.722114, 0.469588],
 [
  0.220124, 0.725509, 0.466226],
 [
  0.226397, 0.728888, 0.462789],
 [
  0.232815, 0.732247, 0.459277],
 [
  0.239374, 0.735588, 0.455688],
 [
  0.24607, 0.73891, 0.452024],
 [
  0.252899, 0.742211, 0.448284],
 [
  0.259857, 0.745492, 0.444467],
 [
  0.266941, 0.748751, 0.440573],
 [
  0.274149, 0.751988, 0.436601],
 [
  0.281477, 0.755203, 0.432552],
 [
  0.288921, 0.758394, 0.428426],
 [
  0.296479, 0.761561, 0.424223],
 [
  0.304148, 0.764704, 0.419943],
 [
  0.311925, 0.767822, 0.415586],
 [
  0.319809, 0.770914, 0.411152],
 [
  0.327796, 0.77398, 0.40664],
 [
  0.335885, 0.777018, 0.402049],
 [
  0.344074, 0.780029, 0.397381],
 [
  0.35236, 0.783011, 0.392636],
 [
  0.360741, 0.785964, 0.387814],
 [
  0.369214, 0.788888, 0.382914],
 [
  0.377779, 0.791781, 0.377939],
 [
  0.386433, 0.794644, 0.372886],
 [
  0.395174, 0.797475, 0.367757],
 [
  0.404001, 0.800275, 0.362552],
 [
  0.412913, 0.803041, 0.357269],
 [
  0.421908, 0.805774, 0.35191],
 [
  0.430983, 0.808473, 0.346476],
 [
  0.440137, 0.811138, 0.340967],
 [
  0.449368, 0.813768, 0.335384],
 [
  0.458674, 0.816363, 0.329727],
 [
  0.468053, 0.818921, 0.323998],
 [
  0.477504, 0.821444, 0.318195],
 [
  0.487026, 0.823929, 0.312321],
 [
  0.496615, 0.826376, 0.306377],
 [
  0.506271, 0.828786, 0.300362],
 [
  0.515992, 0.831158, 0.294279],
 [
  0.525776, 0.833491, 0.288127],
 [
  0.535621, 0.835785, 0.281908],
 [
  0.545524, 0.838039, 0.275626],
 [
  0.555484, 0.840254, 0.269281],
 [
  0.565498, 0.84243, 0.262877],
 [
  0.575563, 0.844566, 0.256415],
 [
  0.585678, 0.846661, 0.249897],
 [
  0.595839, 0.848717, 0.243329],
 [
  0.606045, 0.850733, 0.236712],
 [
  0.616293, 0.852709, 0.230052],
 [
  0.626579, 0.854645, 0.223353],
 [
  0.636902, 0.856542, 0.21662],
 [
  0.647257, 0.8584, 0.209861],
 [
  0.657642, 0.860219, 0.203082],
 [
  0.668054, 0.861999, 0.196293],
 [
  0.678489, 0.863742, 0.189503],
 [
  0.688944, 0.865448, 0.182725],
 [
  0.699415, 0.867117, 0.175971],
 [
  0.709898, 0.868751, 0.169257],
 [
  0.720391, 0.87035, 0.162603],
 [
  0.730889, 0.871916, 0.156029],
 [
  0.741388, 0.873449, 0.149561],
 [
  0.751884, 0.874951, 0.143228],
 [
  0.762373, 0.876424, 0.137064],
 [
  0.772852, 0.877868, 0.131109],
 [
  0.783315, 0.879285, 0.125405],
 [
  0.79376, 0.880678, 0.120005],
 [
  0.804182, 0.882046, 0.114965],
 [
  0.814576, 0.883393, 0.110347],
 [
  0.82494, 0.88472, 0.106217],
 [
  0.83527, 0.886029, 0.102646],
 [
  0.845561, 0.887322, 0.099702],
 [
  0.85581, 0.888601, 0.097452],
 [
  0.866013, 0.889868, 0.095953],
 [
  0.876168, 0.891125, 0.09525],
 [
  0.886271, 0.892374, 0.095374],
 [
  0.89632, 0.893616, 0.096335],
 [
  0.906311, 0.894855, 0.098125],
 [
  0.916242, 0.896091, 0.100717],
 [
  0.926106, 0.89733, 0.104071],
 [
  0.935904, 0.89857, 0.108131],
 [
  0.945636, 0.899815, 0.112838],
 [
  0.9553, 0.901065, 0.118128],
 [
  0.964894, 0.902323, 0.123941],
 [
  0.974417, 0.90359, 0.130215],
 [
  0.983868, 0.904867, 0.136897],
 [
  0.993248, 0.906157, 0.143936]]
_colormaps = dict(autumn=Colormap([(1.0, 0.0, 0.0, 1.0), (1.0, 1.0, 0.0, 1.0)]), blues=Colormap([(1.0, 1.0, 1.0, 1.0), (0.0, 0.0, 1.0, 1.0)]), cool=Colormap([(0.0, 1.0, 1.0, 1.0), (1.0, 0.0, 1.0, 1.0)]), greens=Colormap([(1.0, 1.0, 1.0, 1.0), (0.0, 1.0, 0.0, 1.0)]), reds=Colormap([(1.0, 1.0, 1.0, 1.0), (1.0, 0.0, 0.0, 1.0)]), blue_red=Colormap([(0.0, 0.0, 1.0, 1.0), (0.0, 0.0, 0.85, 1.0), (0.0, 0.0, 0.65, 1.0), (0.0, 0.0, 0.35, 1.0),
 (0.0, 0.25, 0.0, 1.0),
 (0.35, 0.0, 0.0, 1.0), (0.65, 0.0, 0.0, 1.0), (0.85, 0.0, 0.0, 1.0), (1.0, 0.0, 0.0, 1.0)]), spring=Colormap([(1.0, 0.0, 1.0, 1.0), (1.0, 1.0, 0.0, 1.0)]), summer=Colormap([(0.0, 0.5, 0.4, 1.0), (1.0, 1.0, 0.4, 1.0)]), fire=_Fire(), grays=_Grays(), hot=_Hot(), ice=_Ice(), winter=_Winter(), light_blues=_SingleHue(), orange=_SingleHue(hue=35), coolwarm=Colormap(ColorArray([
 (226, 0.59, 0.92), (222, 0.44, 0.99), (218, 0.26, 0.97),
 (30, 0.01, 0.87),
 (20, 0.3, 0.96), (15, 0.5, 0.95), (8, 0.66, 0.86)], color_space='hsv')), BlueRed=Colormap(ColorArray([
 (240, 1.0, 1.0), (232, 0.7, 0.99), (228, 0.3, 0.97),
 (18, 0.3, 0.97), (8, 0.7, 0.99), (0, 1.0, 1.0)], color_space='hsv')), PuGr=_Diverging(145, 280, 0.85, 0.3), GrBu=_Diverging(255, 133, 0.75, 0.6), GrBu_d=_Diverging(255, 133, 0.75, 0.6, 'dark'), RdBu=_Diverging(220, 20, 0.75, 0.5), BuRd=_Diverging(20, 220, 1, 0.25), cubehelix=CubeHelixColormap, single_hue=_SingleHue, hsl=_HSL, husl=_HUSL, diverging=_Diverging)

def get_colormap(name, *args, **kwargs):
    """Obtain a colormap

    Some colormaps can have additional configuration parameters. Refer to
    their corresponding documentation for more information.

    Parameters
    ----------
    name : str | Colormap
        Colormap name. Can also be a Colormap for pass-through.

    Examples
    --------

        >>> get_colormap('autumn')
        >>> get_colormap('single_hue', hue=10)
    """
    if isinstance(name, BaseColormap):
        cmap = name
    else:
        if not isinstance(name, string_types):
            raise TypeError('colormap must be a Colormap or string name')
        if name not in _colormaps:
            raise KeyError('colormap name %s not found' % name)
        cmap = _colormaps[name]
    if inspect.isclass(cmap):
        cmap = cmap(*args, **kwargs)
    return cmap


def get_colormaps():
    """Return the list of colormap names."""
    return _colormaps.copy()