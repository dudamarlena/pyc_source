# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/colors/legacy_palette.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 763 bytes
from . import make

def pop_legacy_palette(kwds, *color_defaults):
    """
    Older animations in BPA and other areas use all sorts of different names for
    what we are now representing with palettes.

    This function mutates a kwds dictionary to remove these legacy fields and
    extract a palette from it, which it returns.
 """
    palette = kwds.pop('palette', None)
    if palette:
        legacy = [k for k, _ in color_defaults if k in kwds]
        if legacy:
            raise ValueError('Cannot set palette and ' + ', '.join(legacy))
        return palette
    else:
        values = [kwds.pop(k, v) for k, v in color_defaults]
        if values:
            if color_defaults[0][0] in ('colors', 'palette'):
                values = values[0]
        return make.colors(values or None)