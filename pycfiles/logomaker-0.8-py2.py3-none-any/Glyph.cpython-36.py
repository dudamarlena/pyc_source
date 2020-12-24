# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../logomaker/src/Glyph.py
# Compiled at: 2019-05-09 13:28:52
# Size of source mod 2**32: 14731 bytes
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D, Bbox
from matplotlib.font_manager import FontManager, FontProperties
from matplotlib.colors import to_rgb
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from logomaker.src.error_handling import check, handle_errors
from logomaker.src.colors import get_rgb
import numpy as np
font_manager = FontManager()
VALID_FONT_WEIGHT_STRINGS = [
 'ultralight', 'light', 'normal', 'regular', 'book',
 'medium', 'roman', 'semibold', 'demibold', 'demi',
 'bold', 'heavy', 'extra bold', 'black']

def list_font_names():
    """
    Returns a list of valid font_name options for use in Glyph or
    Logo constructors.

    parameters
    ----------
    None.

    returns
    -------
    fontnames: (list)
        List of valid font_name names. This will vary from system to system.

    """
    fontnames_dict = dict([(f.name, f.fname) for f in font_manager.ttflist])
    fontnames = list(fontnames_dict.keys())
    fontnames.append('sans')
    fontnames.sort()
    return fontnames


class Glyph:
    __doc__ = '\n    A Glyph represents a character, drawn on a specified axes at a specified\n    position, rendered using specified styling such as color and font_name.\n\n    attributes\n    ----------\n\n    p: (number)\n        x-coordinate value on which to center the Glyph.\n\n    c: (str)\n        The character represented by the Glyph.\n\n    floor: (number)\n        y-coordinate value where the bottom of the Glyph extends to.\n        Must be < ceiling.\n\n    ceiling: (number)\n        y-coordinate value where the top of the Glyph extends to.\n        Must be > floor.\n\n    ax: (matplotlib Axes object)\n        The axes object on which to draw the Glyph.\n\n    width: (number > 0)\n        x-coordinate span of the Glyph.\n\n    vpad: (number in [0,1])\n        Amount of whitespace to leave within the Glyph bounding box above\n        and below the actual Glyph. Specifically, in a glyph with\n        height h = ceiling-floor, a margin of size h*vpad/2 will be left blank\n        both above and below the rendered character.\n\n    font_name: (str)\n        The name of the font to use when rendering the Glyph. This is\n        the value passed as the \'family\' parameter when calling the\n        matplotlib.font_manager.FontProperties constructor.\n\n    font_weight: (str or number)\n        The font weight to use when rendering the Glyph. Specifically, this is\n        the value passed as the \'weight\' parameter in the\n        matplotlib.font_manager.FontProperties constructor.\n        From matplotlib documentation: "weight: A numeric\n        value in the range 0-1000 or one of \'ultralight\', \'light\',\n        \'normal\', \'regular\', \'book\', \'medium\', \'roman\', \'semibold\',\n        \'demibold\', \'demi\', \'bold\', \'heavy\', \'extra bold\', \'black\'."\n\n    color: (matplotlib color)\n        Color to use for Glyph face.\n\n    edgecolor: (matplotlib color)\n        Color to use for Glyph edge.\n\n    edgewidth: (number >= 0)\n        Width of Glyph edge.\n\n    dont_stretch_more_than: (str)\n        This parameter limits the amount that a character will be\n        horizontally stretched when rendering the Glyph. Specifying a\n        wide character such as \'W\' corresponds to less potential stretching,\n        while specifying a narrow character such as \'.\' corresponds to more\n        stretching.\n\n    flip: (bool)\n        If True, the Glyph will be rendered upside down.\n\n    mirror: (bool)\n        If True, a mirror image of the Glyph will be rendered.\n\n    zorder: (number)\n        Placement of Glyph within the z-stack of ax.\n\n    alpha: (number in [0,1])\n        Opacity of the rendered Glyph.\n\n    figsize: ([float, float]):\n        The default figure size for the rendered glyph; only used if ax is\n        not supplied by the user.\n    '

    @handle_errors
    def __init__(self, p, c, floor, ceiling, ax=None, width=0.95, vpad=0.0, font_name='sans', font_weight='bold', color='gray', edgecolor='black', edgewidth=0.0, dont_stretch_more_than='E', flip=False, mirror=False, zorder=None, alpha=1, figsize=(1, 1)):
        self.p = p
        self.c = c
        self.floor = floor
        self.ceiling = ceiling
        self.ax = ax
        self.width = width
        self.vpad = vpad
        self.flip = flip
        self.mirror = mirror
        self.zorder = zorder
        self.dont_stretch_more_than = dont_stretch_more_than
        self.alpha = alpha
        self.color = color
        self.edgecolor = edgecolor
        self.edgewidth = edgewidth
        self.font_name = font_name
        self.font_weight = font_weight
        self.figsize = figsize
        self._input_checks()
        if self.ax is None:
            fig, ax = plt.subplots(1, 1, figsize=(self.figsize))
            self.ax = ax
        self._make_patch()

    def set_attributes(self, **kwargs):
        """
        Safe way to set the attributes of a Glyph object

        parameters
        ----------
        **kwargs:
            Attributes and their values.
        """
        if self.patch is not None:
            if self.patch.axes is not None:
                self.patch.remove()
        for key, value in kwargs.items():
            if key in ('color', 'edgecolor'):
                value = to_rgb(value)
            self.__dict__[key] = value

        self._make_patch()

    def draw(self):
        """
        Draws Glyph given current parameters.

        parameters
        ----------
        None.

        returns
        -------
        None.
        """
        if self.patch is not None:
            self.ax.add_patch(self.patch)

    def _make_patch(self):
        """
        Returns an appropriately scaled patch object corresponding to
        the Glyph.
        """
        height = self.ceiling - self.floor
        if height == 0.0:
            self.patch = None
            return
        char_xmin = self.p - self.width / 2.0
        char_ymin = self.floor + self.vpad * height / 2.0
        char_width = self.width
        char_height = height - self.vpad * height
        bbox = Bbox.from_bounds(char_xmin, char_ymin, char_width, char_height)
        font_properties = FontProperties(family=(self.font_name), weight=(self.font_weight))
        tmp_path = TextPath((0, 0), (self.c), size=1, prop=font_properties)
        msc_path = TextPath((0, 0), (self.dont_stretch_more_than), size=1, prop=font_properties)
        if self.flip:
            transformation = Affine2D().scale(sx=1, sy=(-1))
            tmp_path = transformation.transform_path(tmp_path)
        if self.mirror:
            transformation = Affine2D().scale(sx=(-1), sy=1)
            tmp_path = transformation.transform_path(tmp_path)
        tmp_bbox = tmp_path.get_extents()
        msc_bbox = msc_path.get_extents()
        hstretch_tmp = bbox.width / tmp_bbox.width
        hstretch_msc = bbox.width / msc_bbox.width
        hstretch = min(hstretch_tmp, hstretch_msc)
        char_width = hstretch * tmp_bbox.width
        char_shift = (bbox.width - char_width) / 2.0
        vstretch = bbox.height / tmp_bbox.height
        transformation = Affine2D().translate(tx=(-tmp_bbox.xmin),
          ty=(-tmp_bbox.ymin)).scale(sx=hstretch,
          sy=vstretch).translate(tx=(bbox.xmin + char_shift),
          ty=(bbox.ymin))
        char_path = transformation.transform_path(tmp_path)
        self.patch = PathPatch(char_path, facecolor=(self.color),
          zorder=(self.zorder),
          alpha=(self.alpha),
          edgecolor=(self.edgecolor),
          linewidth=(self.edgewidth))
        self.ax.add_patch(self.patch)

    def _input_checks(self):
        """
        check input parameters in the Logo constructor for correctness
        """
        check(isinstance(int(self.p), (float, int)), 'type(p) = %s must be a number' % type(self.p))
        check(isinstance(self.c, str), 'type(c) = %s; must be of type str ' % type(self.c))
        check(isinstance(self.floor, (float, int)), 'type(floor) = %s must be a number' % type(self.floor))
        self.floor = float(self.floor)
        check(isinstance(self.ceiling, (float, int)), 'type(ceiling) = %s must be a number' % type(self.ceiling))
        self.ceiling = float(self.ceiling)
        check(self.floor <= self.ceiling, 'must have floor <= ceiling. Currently, floor=%f, ceiling=%f' % (
         self.floor, self.ceiling))
        check(self.ax is None or isinstance(self.ax, Axes), 'ax must be either a matplotlib Axes object or None.')
        check(isinstance(self.width, (float, int)), 'type(width) = %s; must be of type float or int ' % type(self.width))
        check(self.width >= 0, 'width = %d must be >= 0 ' % self.width)
        check(isinstance(self.vpad, (float, int)), 'type(vpad) = %s; must be of type float or int ' % type(self.vpad))
        check(self.vpad >= 0, 'vpad = %d must be >= 0 ' % self.vpad)
        check(isinstance(self.font_name, str), 'type(font_name) = %s must be of type str' % type(self.font_name))
        check(isinstance(self.font_weight, (str, int)), 'type(font_weight) = %s should either be a string or an int' % type(self.font_weight))
        if isinstance(self.font_weight, str):
            check(self.font_weight in VALID_FONT_WEIGHT_STRINGS, 'font_weight must be one of %s' % VALID_FONT_WEIGHT_STRINGS)
        else:
            if isinstance(self.font_weight, int):
                check(0 <= self.font_weight <= 1000, 'font_weight must be in range [0,1000]')
        self.color = get_rgb(self.color)
        self.edgecolor = get_rgb(self.edgecolor)
        check(isinstance(self.edgewidth, (float, int)), 'type(edgewidth) = %s must be a number' % type(self.edgewidth))
        self.edgewidth = float(self.edgewidth)
        check(self.edgewidth >= 0, ' edgewidth must be >= 0; is %f' % self.edgewidth)
        check(isinstance(self.dont_stretch_more_than, str), 'type(dont_stretch_more_than) = %s; must be of type str ' % type(self.dont_stretch_more_than))
        check(len(self.dont_stretch_more_than) == 1, 'dont_stretch_more_than must have length 1; currently len(dont_stretch_more_than)=%d' % len(self.dont_stretch_more_than))
        check(isinstance(self.flip, (bool, np.bool_)), 'type(flip) = %s; must be of type bool ' % type(self.flip))
        self.flip = bool(self.flip)
        check(isinstance(self.mirror, (bool, np.bool_)), 'type(mirror) = %s; must be of type bool ' % type(self.mirror))
        self.mirror = bool(self.mirror)
        if self.zorder is not None:
            check(isinstance(self.zorder, (float, int)), 'type(zorder) = %s; must be of type float or int ' % type(self.zorder))
        check(isinstance(self.alpha, (float, int)), 'type(alpha) = %s must be a float or int' % type(self.alpha))
        self.alpha = float(self.alpha)
        check(0 <= self.alpha <= 1.0, 'alpha must be between 0.0 and 1.0 (inclusive)')