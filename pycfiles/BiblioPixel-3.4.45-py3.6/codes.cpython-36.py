# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/drivers/serial/codes.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 739 bytes
from enum import IntEnum
from ..ledtype import LEDTYPE

class CMDTYPE(IntEnum):
    SETUP_DATA = 1
    PIXEL_DATA = 2
    BRIGHTNESS = 3
    GETID = 4
    SETID = 5
    GETVER = 6
    SYNC = 7


SPIChipsets = [
 LEDTYPE.LPD8806,
 LEDTYPE.WS2801,
 LEDTYPE.SM16716,
 LEDTYPE.APA102,
 LEDTYPE.P9813]
BufferChipsets = {LEDTYPE.APA102: lambda num: int(num / 64.0) + 1}