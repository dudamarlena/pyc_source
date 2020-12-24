# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/.virtualenvs/temp3/lib/python3.4/site-packages/colordiffs/ansiformat.py
# Compiled at: 2015-06-12 22:56:34
# Size of source mod 2**32: 323 bytes
from pygments.console import codes, dark_colors, light_colors, esc

def patch_codes():
    dark_bg = [s + '_bg' for s in dark_colors]
    light_bg = [s + '_bg' for s in light_colors]
    x = 40
    for d, l in zip(dark_bg, light_bg):
        codes[d] = esc + '%im' % x
        codes[l] = esc + '%i;01m' % x
        x += 1