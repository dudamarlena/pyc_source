# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ggplot/scales/scale_color_brewer.py
# Compiled at: 2016-07-31 11:30:58
from __future__ import absolute_import, division, print_function, unicode_literals
from .scale import scale
from copy import deepcopy
import brewer2mpl

def _number_to_palette(ctype, n):
    n -= 1
    palettes = sorted(brewer2mpl.COLOR_MAPS[ctype].keys())
    if n < len(palettes):
        return palettes[n]


def _handle_shorthand(text):
    abbrevs = {b'seq': b'Sequential', 
       b'qual': b'Qualitative', 
       b'div': b'Diverging'}
    text = abbrevs.get(text, text)
    text = text.title()
    return text


class scale_color_brewer(scale):
    """
    Use ColorBrewer (http://colorbrewer2.org/) style colors
    
    Parameters
    ----------
    type: string
        One of seq (sequential), div (diverging) or qual (qualitative)
    palette: string
        If a string, will use that named palette. If a number, will index into
        the list of palettes of appropriate type

    Examples
    --------
    >>> from ggplot import *
    >>> p = ggplot(aes(x='carat', y='price', colour='clarity'), data=diamonds)
    >>> p += geom_point()
    >>> print(p + scale_color_brewer(palette=4))
    >>> print(p + scale_color_brewer(type='diverging'))
    >>> print(p + scale_color_brewer(type='div'))
    >>> print(p + scale_color_brewer(type='seq'))
    >>> print(p + scale_color_brewer(type='seq', palette='Blues'))
    """
    VALID_SCALES = [
     b'type', b'palette']

    def __radd__(self, gg):
        if self.type:
            ctype = self.type
        else:
            ctype = b'Sequential'
        ctype = _handle_shorthand(ctype)
        if self.palette:
            palette = self.palette
        else:
            palette = _number_to_palette(ctype, 1)
        if isinstance(palette, int):
            palette = _number_to_palette(ctype, palette)
        try:
            color_col = gg._aes.data.get(b'color', gg._aes.data.get(b'fill'))
            n_colors = max(gg.data[color_col].nunique(), 3)
        except:
            n_colors = 3

        bmap = brewer2mpl.get_map(palette, ctype, n_colors)
        gg.manual_color_list = bmap.hex_colors
        return gg