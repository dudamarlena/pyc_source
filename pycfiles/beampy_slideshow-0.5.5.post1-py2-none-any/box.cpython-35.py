# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/libperso/beampy/modules/box.py
# Compiled at: 2019-04-18 16:13:22
# Size of source mod 2**32: 8945 bytes
"""
Beampy module to create a boxed group 
"""
from beampy.document import document
from beampy.functions import set_curentslide, set_lastslide
from beampy.modules.core import group
from beampy.modules.text import text
from beampy.modules.svg import rectangle
from beampy.geometry import center
import logging

class box(group):
    __doc__ = "\n    Draw a box around a group.\n\n    Parameters\n    ----------\n\n    title : str or None, optional\n        The title of the box (the default value is None, which implies\n        no title).\n\n    x : int or float or {'center', 'auto'} or str, optional\n        Horizontal position for the group (the default is 'center'). See\n        positioning system of Beampy.\n\n    y : int or float or {'center', 'auto'} or str, optional\n        Vertical position for the group (the default is 'auto'). See\n        positioning system of Beampy.\n\n    width : int or float or None, optional\n        Width of the group (the default is None, which implies that the width\n        is computed to fit the group contents width).\n\n    height : int or float or None, optional\n        Height of the group (the default is None). When height is None the\n        height is computed to fit the group contents height.\n\n    perentid : str or None, optional\n        Beampy id of the parent group (the default is None). This parentid is\n        given automatically by Beampy render.\n\n    rounded : int, optional\n        The number of pixel for rounded borders (the default value is\n        10).\n\n    linewidth : int, optional\n        The linewidth of the border in pt (the default value is 1).\n\n    color : svg color name as string, optional\n        The color of the contour line of the box (the default value is\n        'red').\n\n    head_height : int or None, optional\n        The height in pixel of the background under the title (the\n        default is None, which implies that height is computed from\n        title height + 10px of margins). You need to adjust this value\n        for multi-lines titles.\n\n    shadow : boolean, optional\n        Draw a shadow under the box (the default value is False, which\n        means no shadow).\n\n    background_color : svg color name as string, optional\n        The color of the background of the box (the default values is\n        'white').\n\n    title_color : svg color name as string, optional\n        The color of the title (the default value is 'white').\n\n    title_align : {'left','right','center'}, optional\n        The horizontal alignment of the title (the default value is\n        'left').\n\n    title_xoffset : int, optional\n        The horizontal offset in pixel from the box border of the\n        title (the default value is 10).\n\n    auto_height_margin : int, optional\n        The vertical margin in pixel (top and bottom) to use when box height is not specified \n        (the default theme sets this value to 15).\n\n    "

    def __init__(self, title=None, x='center', y='auto', width=None, height=None, parentid=None, **kwargs):
        self.title = title
        self.check_args_from_theme(kwargs)
        super(box, self).__init__(x=x, y=y, width=width, height=height, parentid=parentid, opengroup=False)
        self.bp_title = None
        if self.title is not None:
            self.build_title()
            self.yoffset = self.head_height

    def build_title(self):
        self.title_xpos = self.title_xoffset
        self.title_ypos = 5
        self.bp_title = text(self.title, x=self.title_xpos, y=self.title_ypos, color=self.title_color, width=self.width - 20)
        if self.head_height is None:
            self.head_height = (self.bp_title.height + 10).value

    def build_background(self):
        if self.shadow:
            self.svg_shadow = '#drop-shadow'
        else:
            self.svg_shadow = None
        self.main_svg = rectangle(width=self.width, height=self.height, rx=self.rounded, ry=self.rounded, edgecolor=self.color, linewidth=self.linewidth, color=self.background_color, svgfilter=self.svg_shadow, x=self.center + center(0), y=self.center + center(0))
        if self.svg_shadow is not None:
            self.main_svg.add_svgdef('\n            <filter id="drop-shadow"> <feGaussianBlur in="SourceAlpha"\n            stdDeviation="3"/> <feOffset dx="4" dy="4" result="offsetblur"/>\n            <feMerge> <feMergeNode/> <feMergeNode in="SourceGraphic"/> </feMerge>\n            </filter>\n            ')
        if self.bp_title is not None:
            clipid = '#boxborder_{id}'.format(id=self.id)
            self.title_svg = rectangle(width=self.width, height=self.head_height, color=self.color, edgecolor=self.color, linewidth=self.linewidth, svgclip=clipid, x='-%ipx' % (self.linewidth / 2), y='-%ipx' % (self.linewidth / 2))
            self.title_svg.rounded = self.rounded
            self.title_svg.add_svgdef('\n            <clipPath id="boxborder_%s">\n            <rect width="{width}" height="{clipheight}" \n            rx="{rounded}" ry="{rounded}" stroke="{color}" \n            stroke-width="{linewidth}"/>\n            </clipPath>\n            ' % self.id, ['width', 'clipheight', 'rounded',
             'color', 'linewidth'])
            self.title_svg.clipheight = self.head_height * 2

    def pre_render(self):
        set_curentslide(self.slide_id)
        if self.init_height is None:
            for eid in self.elementsid:
                elem = document._slides[self.slide_id].contents[eid]
                if elem.height.value is None:
                    elem.height.run_render()
                if elem.width.value is None:
                    elem.width.run_render()

            self.compute_group_size()
            self.update_size(self.width, self.height + self.yoffset + 2 * self.auto_height_margin)
            for eid in self.elementsid:
                document._slides[self.slide_id].contents[eid].positionner.y['final'] += self.yoffset + self.auto_height_margin

        else:
            for eid in self.elementsid:
                elemp = document._slides[self.slide_id].contents[eid].positionner
                if elemp.y['align'] not in ('auto', 'center') and elemp.y['reference'] != 'relative':
                    document._slides[self.slide_id].contents[eid].positionner.y['shift'] += self.yoffset

        with self:
            self.build_background()
        self.propagate_layers()
        self.main_svg.first()
        if self.bp_title is not None:
            self.title_svg.above(self.main_svg)
            logging.debug('set layer to box title to %s ' % str(self.layers))
            self.bp_title.layers = self.layers
            title_xpos = self.left + self.title_xoffset
            if self.title_align == 'center':
                title_xpos = self.left + (self.title_svg.width - self.bp_title.width) / 2
            if self.title_align == 'right':
                title_xpos = self.right - (self.bp_title.width + self.title_xpos)
            self.bp_title.positionner.update_y(self.top + 5)
            self.bp_title.positionner.update_x(title_xpos)
        set_lastslide()