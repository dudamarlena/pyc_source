# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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