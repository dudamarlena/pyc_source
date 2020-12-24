# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/colors.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 274 bytes
from . import deprecated
if deprecated.allowed():
    from ..colors import *
    from ..colors import arithmetic, classic, closest_colors, conversions, gamma, juce, legacy_palette, make, names, palettes, printer, wheel