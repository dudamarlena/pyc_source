# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/spi_interfaces.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 117 bytes
from enum import IntEnum

class SPI_INTERFACES(IntEnum):
    FILE = 0
    PYDEV = 1
    PERIPHERY = 2
    DUMMY = 3