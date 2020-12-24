# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/modules/svg.py
# Compiled at: 2019-07-01 17:38:15
# Size of source mod 2**32: 16734 bytes
"""
@author: hugo

Module to write raw svg commands in slides
"""
from beampy import document
from beampy.functions import getsvgwidth, getsvgheight
from beampy.modules.core import beampy_module, group
from beampy.geometry import convert_unit
import logging, tempfile, os

class svg(beampy_module):
    __doc__ = '\n    Insert svg content.\n\n    Parameters\n    ----------\n\n    svg_content : string\n        Svg elements to add written in svg syntax without svg document tag\n        "<svg xmlns...>"\n\n    x : int or float or {\'center\', \'auto\'} or str, optional\n        Horizontal position for the svg (the default is 0). See\n        positioning system of Beampy.\n\n    y : int or float or {\'center\', \'auto\'} or str, optional\n        Vertical position for the svg (the default is 0). See positioning\n        system of Beampy.\n\n    '

    def __init__(self, svg_content, **kwargs):
        self.type = 'svg'
        self.inkscape_size = True
        self.load_args(kwargs)
        self.content = svg_content
        self.register()

    def render(self):
        """
            The render of an svg part
        """
        if self.inkscape_size:
            logging.debug('Run inkscape to get svg size')
            tmpsvg = '<svg xmlns="http://www.w3.org/2000/svg" version="1.2" baseProfile="tiny" xmlns:xlink="http://www.w3.org/1999/xlink">'
            if self.out_svgdefs is not None:
                tmpsvg += '<defs>%s</defs>' % ' '.join(self.out_svgdefs)
            tmpsvg += ' %s</svg>' % self.content
            with tempfile.NamedTemporaryFile(mode='w', prefix='beampytmp', suffix='.svg') as (f):
                f.write(tmpsvg)
                f.file.flush()
                svg_width = getsvgwidth(f.name)
                svg_height = getsvgheight(f.name)
        else:
            svg_width = convert_unit(self.width.value)
            svg_height = convert_unit(self.height.value)
        self.update_size(svg_width, svg_height)
        self.svgout = self.content
        self.rendered = True


class rectangle(svg):
    __doc__ = '\n    Insert an svg rectangle.\n\n    Parameters\n    ----------\n\n    x : int or float or {\'center\', \'auto\'} or str, optional\n        Horizontal position for the rectangle (the default is \'center\'). See\n        positioning system of Beampy.\n\n    y : int or float or {\'center\', \'auto\'} or str, optional\n        Vertical position for the rectangle (the default theme sets this to\n        \'auto\'). See positioning system of Beampy.\n\n    height : string, optional\n         Height of the rectangle (the default theme sets this to \'10px\').\n         The value is given as string with a unit accepted by svg syntax.\n\n    width : string, optional\n         Width of the rectangle (the default theme sets this to\n         :py:mod:`document._width`). The value is given as string with a unit\n         accepted by svg syntax.\n\n    color : string, optional\n        Color filling the rectangle (the default theme sets this to\n        THEME[\'title\'][\'color\']). The color is given either as HTML hex value\n        "#ffffff" or as svg colornames "blank".\n\n    linewidth : string, optional\n        Rectangle edge line width (the default theme sets this to \'2px\'). The\n        value is given as string followed by an unit accepted by svg syntax.\n\n    edgecolor : string, optional\n        Color of the rectangle edge (the default theme sets this to\n        THEME[\'text\'][\'color\']). The color is given either as HTML hex value\n        "#ffffff" or as svg colornames "blank".\n\n    opacity: float, optional\n        Opacity of the rectangle (the default theme sets this to 1). The\n        value ranges between 0 (transparent) and 1 (solid).\n\n    rx: int, optional\n        The number of pixels for the rounding the rectangle corners in\n        x direction (The default theme sets this value to 0). \n\n    ry: int, optional\n        The number of pixels for the rounding the rectangle corners in\n        y direction (The default theme sets this value to 0). \n    \n    svgfilter: string or None, optional\n        Set the id of the svg filter (\'#name\') to apply to the\n        rectangle (default value is None, which means no\n        filter). Filter definitaion should be added to slide.svgdefout\n        list.\n\n    svgclip: string or None, optional\n       Set the id of the clip object (\'#name\') to apply on the\n       rectangle (the default value is None, which means no clip to\n       apply). Clip definition should be added to slide.svgdefout\n       list.\n\n    '

    def __init__(self, **kwargs):
        self.type = 'svg'
        self.check_args_from_theme(kwargs)
        if self.svgclip is not None or self.svgfilter is not None:
            self.inkscape_size = True
        else:
            self.inkscape_size = False
        beampy_svg_kword = {'color':'fill', 
         'linewidth':'stroke-width', 
         'opacity':'opacity', 
         'edgecolor':'stroke'}
        self.style = ''
        for kw in beampy_svg_kword:
            if hasattr(self, kw):
                self.style += '%s:%s;' % (beampy_svg_kword[kw], getattr(self, kw))

        self.dxdy = int(convert_unit(self.linewidth) / 2)
        self.content = '\'<rect x="{dx}" y="{dy}" rx="{rx}" ry="{ry}"\n        width="{width}" height="{height}" style="{style}" {filter}\n        {clip}/>'
        self.svgdefs = []
        self.svgdefsargs = []
        self.register()

    def pre_render(self):
        if self.svgfilter is None:
            self.svgfilter = ''
        else:
            self.svgfilter = 'filter="url({id})"'.format(id=(self.svgfilter))
        if self.svgclip is None:
            self.svgclip = ''
        else:
            self.svgclip = 'clip-path="url({id})"'.format(id=(self.svgclip))
        self.content = self.content.format(width=(self.width - self.dxdy * 2), height=(self.height - self.dxdy * 2),
          dx=(self.dxdy),
          dy=(self.dxdy),
          rx=(self.rx),
          ry=(self.ry),
          style=(self.style),
          filter=(self.svgfilter),
          clip=(self.svgclip))


class line(svg):
    __doc__ = '\n    Insert an svg line.\n\n    Parameters\n    ----------\n\n    x2 : int or float or str\n        End horizontal coordinate of the line. The value is passed to unit\n        converted of Beampy which translate it to pixel.\n\n    y2 : int or float or str\n        End vertical coordinate of the line. The value is passed to unit\n        converted of Beampy which translate it to pixel.\n\n    x : int or float or {\'center\', \'auto\'} or str, optional\n        Horizontal position for the line (the default theme sets this to\n        \'center\'). See positioning system of Beampy.\n\n    y : int or float or {\'center\', \'auto\'} or str, optional\n        Vertical position for the line (the default theme sets this to\n        \'auto\'). See positioning system of Beampy.\n\n    linewidth : string, optional\n        Line width (the default theme sets this to \'2px\'). The value is given\n        as string followed by an unit accepted by svg syntax.\n\n    color : string, optional\n        Line color (the default theme sets this to THEME[\'title\'][\'color\']).\n        The color is given either as HTML hex value "#ffffff" or as svg\n        colornames "blank".\n\n    opacity: float, optional\n        Opacity of the rectangle (the default theme sets this to 1). The\n        value ranges between 0 (transparent) and 1 (solid).\n\n    '

    def __init__(self, x2, y2, **kwargs):
        self.type = 'svg'
        self.inkscape_size = True
        self.check_args_from_theme(kwargs)
        self.x2 = x2
        self.y2 = y2
        self.x2 = convert_unit(self.x2)
        self.y2 = convert_unit(self.y2)
        self.args['x2'] = self.x2
        self.args['y2'] = self.y2
        beampy_svg_kword = {'color':'stroke', 
         'linewidth':'stroke-width', 
         'opacity':'opacity'}
        self.style = ''
        for kw in beampy_svg_kword:
            if hasattr(self, kw):
                self.style += '%s:%s;' % (beampy_svg_kword[kw], getattr(self, kw))

        self.content = '<line x1="0" y1="0" x2="{x2}px" y2="{y2}px" style="{style}"/>'
        self.svgdefs = []
        self.svgdefsargs = []
        self.register()

    def pre_render(self):
        self.content = self.content.format(x2=(self.x2), y2=(self.y2),
          style=(self.style))


def hline(y, **kwargs):
    """
    Create an horizontal line at a given horizontal position.
    Accept all arguments of :py:mod:`beampy.line`
    
    Parameters
    ----------

    y : int or float or {'center', 'auto'} or str
        Vertical position for the line (the default theme sets this to
        'auto'). See positioning system of Beampy.

    See Also
    --------

    :py:mod:`beampy.line`

    """
    if isinstance(y, str):
        y = convert_unit(y)
        y = '%spx' % y
    return line(x=0, y=y, x2='%spx' % document._width, y2=0, **kwargs)


def vline(x, **kwargs):
    """
    Create an horizontal line at a given vertical position.
    Accept all arguments of :py:mod:`beampy.line`

    Parameters
    ----------

    x : int or float or {'center', 'auto'} or str
        Horizontal position for the line (the default theme sets this to
        'auto'). See positioning system of Beampy.

    See Also
    --------

    :py:mod:`beampy.line`

    """
    if isinstance(x, str):
        x = convert_unit(x)
        x = '%spx' % x
    return line(x=x, y=0, y2='%spx' % document._height, x2=0, **kwargs)


def grid(dx, dy, **kwargs):
    """
    Create a grid with a given spacing.

    Parameters
    ----------

    Accept all arguments of :py:mod:`beampy.line`

    See Also
    --------

    :py:mod:`beampy.line`

    """
    assert dx > 0
    assert dy > 0
    with group(x=0, y=0, width=(document._width), height=(document._height)) as (g):
        cur_x = 0
        while cur_x <= document._height:
            hline(('%spx' % cur_x), **kwargs)
            cur_x += dx

        cur_y = 0
        while cur_y <= document._width:
            vline(('%spx' % cur_y), **kwargs)
            cur_y += dy

    return g


class grid_new(svg):
    __doc__ = '\n    Create a grid with a given spacing.\n\n    Parameters\n    ----------\n\n    dx : int\n        Horizontal spacing for the grid. The unit used is pixel.\n\n    dy : int\n        Vertical spacing for the grid. The unit used is pixel.\n\n    linewidth : string, optional\n        Line width (the default theme sets this to \'2px\'). The value is given\n        as string followed by an unit accepted by svg syntax.\n\n    color : string, optional\n        Line color (the default theme sets this to THEME[\'title\'][\'color\']).\n        The color is given either as HTML hex value "#ffffff" or as svg\n        colornames "blank".\n\n    opacity: float, optional\n        Opacity of the rectangle (the default theme sets this to 1). The\n        value ranges between 0 (transparent) and 1 (solid).\n\n    '

    def __init__(self, dx, dy, **kwargs):
        self.type = 'svg'
        self.inkscape_size = True
        self.check_args_from_theme(kwargs)
        self.dx = dx
        self.dy = dy
        self.dx = convert_unit(self.dx)
        self.dy = convert_unit(self.dy)
        self.args['dx'] = self.dx
        self.args['dy'] = self.dy
        beampy_svg_kword = {'color':'stroke', 
         'linewidth':'stroke-width', 
         'opacity':'opacity'}
        self.style = ''
        for kw in beampy_svg_kword:
            if hasattr(self, kw):
                self.style += '%s:%s;' % (beampy_svg_kword[kw], getattr(self, kw))

        curslide = document._slides[self.slide_id]
        base_hline = '<line id="{id}" x1="0" y1="0" x2="{x2}px" y2="{y2}px" style="{style}"/>'
        self.content = base_hline
        self.content = self.content.format(x2=(curslide.curwidth), y2=0, style=(self.style),
          id='hlineXX')


class circle(svg):
    __doc__ = '\n    Insert an svg circle.\n\n    Parameters\n    ----------\n\n    x : int or float or {\'center\', \'auto\'} or str, optional\n        Horizontal position for the rectangle (the default is \'center\'). See\n        positioning system of Beampy.\n\n    y : int or float or {\'center\', \'auto\'} or str, optional\n        Vertical position for the rectangle (the default theme sets this to\n        \'auto\'). See positioning system of Beampy.\n\n    r : int or float or string, optional\n         radius of the circle (the default theme sets this to 3 for \'3px\').\n         When the value is given as string it accepts a unit allow by svg syntax.\n         ("em" | "ex" | "px" | "in" | "cm" | "mm" | "pt" | "pc" | "%")\n    \n    color : string, optional\n        Color filling the circle (the default theme sets this to\n        THEME[\'title\'][\'color\']). The color is given either as HTML hex value\n        "#ffffff" or as svg colornames "blank".\n\n    linewidth : string, optional\n        Circle edge line width (the default theme sets this to \'1px\'). The\n        value is given as string followed by an unit accepted by svg syntax.\n\n    edgecolor : string, optional\n        Color of the circle edge (the default theme sets this to\n        THEME[\'title\'][\'color\']). The color is given either as HTML hex value\n        "#ffffff" or as svg colornames "blank".\n\n    opacity: float, optional\n        Opacity of the circle (the default theme sets this to 1). The\n        value ranges between 0 (transparent) and 1 (solid).\n\n    '

    def __init__(self, **kwargs):
        self.type = 'svg'
        self.inkscape_size = False
        self.check_args_from_theme(kwargs)
        beampy_svg_kword = {'color':'fill', 
         'linewidth':'stroke-width', 
         'opacity':'opacity', 
         'edgecolor':'stroke'}
        self.style = ''
        for kw in beampy_svg_kword:
            if hasattr(self, kw):
                self.style += '%s:%s;' % (beampy_svg_kword[kw], getattr(self, kw))

        self.cx = convert_unit(self.r) + int(convert_unit(self.linewidth) / 2)
        self.cy = convert_unit(self.r) + int(convert_unit(self.linewidth) / 2)
        self.content = '<circle cx="{cx}" cy="{cy}" r="{r}" style="{style}" />'
        self.svgdefs = []
        self.svgdefsargs = []
        self.register()

    def pre_render(self):
        self.content = self.content.format(r=(self.r), cx=(self.cx), cy=(self.cy), style=(self.style))
        self.width = convert_unit(self.r) * 2 + convert_unit(self.linewidth)
        self.height = convert_unit(self.r) * 2 + convert_unit(self.linewidth)
        self.update_size(self.width, self.height)