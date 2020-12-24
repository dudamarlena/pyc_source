# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/useragentutils/manufacturer.py
# Compiled at: 2012-12-17 16:57:38
from utilities import Enum, EnumValue

class Manufacturer(Enum):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    OTHER = EnumValue(1, 'Other')
    MICROSOFT = EnumValue(2, 'Microsoft Corporation')
    APPLE = EnumValue(3, 'Apple Inc.')
    SUN = EnumValue(4, 'Sun Microsystems, Inc.')
    SYMBIAN = EnumValue(5, 'Symbian Ltd.')
    NOKIA = EnumValue(6, 'Nokia Corporation')
    BLACKBERRY = EnumValue(7, 'Research In Motion Limited')
    HP = EnumValue(8, 'Hewlet Packard')
    SONY_ERICSSON = EnumValue(9, 'Sony Ericsson Mobile Communications AB')
    SAMSUNG = EnumValue(20, 'Samsung Electronics')
    SONY = EnumValue(10, 'Sony Computer Entertainment, Inc.')
    NINTENDO = EnumValue(11, 'Nintendo')
    OPERA = EnumValue(12, 'Opera Software ASA')
    MOZILLA = EnumValue(13, 'Mozilla Foundation')
    GOOGLE = EnumValue(15, 'Google Inc.')
    COMPUSERVE = EnumValue(16, 'CompuServe Interactive Services, Inc.')
    YAHOO = EnumValue(17, 'Yahoo Inc.')
    AOL = EnumValue(18, 'AOL LLC.')
    MMC = EnumValue(19, 'Mail.com Media Corporation')
    AMAZON = EnumValue(20, 'Amazon.com, Inc.')
    ROKU = EnumValue(21, 'Roku, Inc.')