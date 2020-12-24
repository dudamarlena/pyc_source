# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/colors/palettes.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 2464 bytes
import copy
from .make import colors_no_palette as _colors
from . import conversions

def get(name=None):
    """
    Return a named Palette, or None if no such name exists.

    If ``name`` is omitted, the default value is used.
    """
    if name is None or name == 'default':
        return _DEFAULT_PALETTE
    if isinstance(name, str):
        return PROJECT_PALETTES.get(name) or BUILT_IN_PALETTES.get(name)


PROJECT_PALETTES = {}
BUILT_IN_PALETTES = {'rainbow':_colors(conversions.HUE_RAINBOW), 
 'raw':_colors(conversions.HUE_RAW), 
 'spectrum':_colors(conversions.HUE_SPECTRUM), 
 'three_sixty':_colors(conversions.HUE_360), 
 'flag':_colors('red, white, blue'), 
 'checker':_colors('white, black', serpentine=True), 
 'primary':_colors('red, green, blue'), 
 'secondary':_colors('yellow, magenta, cyan'), 
 'eight':_colors('black, red, yellow, green, cyan, blue, magenta, white'), 
 'van_gogh':_colors('gold, teal, spring green 3, ivory black'), 
 'trendy':_colors('medium aquamarine, orange red, chocolate 1, gainsboro'), 
 'muted':_colors('navajo white 3, ivory 3, white smoke, ivory black'), 
 'bold':_colors('black, dodger blue 4, hot pink 4, orange red 3'), 
 'clean':_colors('light cyan 2, dark gray, brown 1, snow 2'), 
 'warm':_colors('snow 3, dark grey, indian red 4, burly wood 3'), 
 'sharp':_colors('sea green 3, ivory black, burly wood 2, gray'), 
 'pastel':_colors('azure 3, eggshell, sienna 2, goldenrod'), 
 'tints':_colors('plum 4, dark grey, antique white 2, linen'), 
 'splash':_colors('steel blue 3, gainsboro, gold, tan 2'), 
 'energy':_colors('magenta, yellow, cyan, beige')}

def set_default(palette):
    global _DEFAULT_PALETTE
    p = get(palette)
    if not p:
        raise ValueError("Don't understand default %s" % palette)
    _DEFAULT_PALETTE = p


set_default('rainbow')