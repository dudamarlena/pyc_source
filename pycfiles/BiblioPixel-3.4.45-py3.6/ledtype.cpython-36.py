# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/types/ledtype.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 378 bytes
import functools
from ...drivers.ledtype import LEDTYPE
USAGE = '\nAn LEDTYPE is represented by a string.\n\nPossible LEDTYPEs are ' + ', '.join(LEDTYPE.__members__)

@functools.singledispatch
def make(c):
    raise ValueError("Don't understand type %s" % type(c), USAGE)


@make.register(LEDTYPE)
def _(c):
    return c


@make.register(str)
def _(c):
    return LEDTYPE[c]