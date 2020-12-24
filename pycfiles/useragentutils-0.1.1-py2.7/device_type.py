# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/useragentutils/device_type.py
# Compiled at: 2013-01-06 02:01:24
from utilities import Enum, EnumValue

class DeviceType(Enum):

    def __init__(self, name):
        self.name = name

    COMPUTER = EnumValue('Computer')
    MOBILE = EnumValue('Mobile')
    TABLET = EnumValue('Tablet')
    GAME_CONSOLE = EnumValue('Game console')
    DMR = EnumValue('Digital media receiver')
    UNKNOWN = EnumValue('Unknown')