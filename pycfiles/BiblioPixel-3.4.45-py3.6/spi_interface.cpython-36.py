# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/types/spi_interface.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 424 bytes
import functools
from ...drivers.spi_interfaces import SPI_INTERFACES
USAGE = '\nA spi_interface is represented by a string.\n\nPossible values are ' + ', '.join(sorted(SPI_INTERFACES.__members__))

@functools.singledispatch
def make(c):
    raise ValueError("Don't understand type %s" % type(c), USAGE)


@make.register(SPI_INTERFACES)
def _(c):
    return c


@make.register(str)
def _(c):
    return SPI_INTERFACES[c]