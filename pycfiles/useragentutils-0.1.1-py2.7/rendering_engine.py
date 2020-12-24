# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/useragentutils/rendering_engine.py
# Compiled at: 2012-12-17 16:45:23
from utilities import Enum, EnumValue

class RenderingEngine(Enum):

    def __init__(self, name):
        self.name = name

    TRIDENT = EnumValue('Trident')
    WORD = EnumValue('Microsoft Office Word')
    GECKO = EnumValue('Gecko')
    WEBKIT = EnumValue('WebKit')
    PRESTO = EnumValue('Presto')
    MOZILLA = EnumValue('Mozilla')
    KHTML = EnumValue('KHTML')
    OTHER = EnumValue('Other')