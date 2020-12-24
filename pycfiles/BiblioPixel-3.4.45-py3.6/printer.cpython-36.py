# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/colors/printer.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 379 bytes
from ..util import log
from . import names

def printer(colors, use_hex=False):
    if not colors:
        return
    try:
        colors[0][0]
    except:
        assert len(colors) % 3 == 0
        colors = zip(*[iter(colors)] * 3)

    for i, color in enumerate(colors):
        log.printer('%2d:' % i, names.color_to_name(color, use_hex))