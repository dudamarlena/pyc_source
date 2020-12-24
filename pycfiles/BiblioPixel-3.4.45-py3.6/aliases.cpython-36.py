# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/aliases.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 1085 bytes
import operator, os, re
from ..util import log
ALIAS_MARKERS = '@$'
SEPARATORS = re.compile('([./#]|[^./#]+)')
PROJECT_ALIASES = {}
BUILTIN_ALIASES = {'apa102':'bibliopixel.drivers.SPI.APA102.APA102', 
 'lpd8806':'bibliopixel.drivers.SPI.LPD8806.LPD8806', 
 'pi_ws281x':'bibliopixel.drivers.PiWS281X.PiWS281X', 
 'serial':'bibliopixel.drivers.serial.Serial', 
 'sk9822':'bibliopixel.drivers.SPI.APA102.APA102', 
 'spi':'bibliopixel.drivers.SPI.SPI', 
 'ws2801':'bibliopixel.drivers.SPI.WS2801.WS2801', 
 'ws281x':'bibliopixel.drivers.SPI.WS281X.WS281X', 
 'bpa':'BiblioPixelAnimations'}

def get_alias(alias):
    return PROJECT_ALIASES.get(alias) or BUILTIN_ALIASES.get(alias)


def resolve(typename, aliases=None):
    aliases = aliases or {}

    def get(s):
        return aliases.get(s) or get_alias(s) or s

    def get_all(typename):
        for part in SEPARATORS.split(typename):
            is_alias = part and part[0] in ALIAS_MARKERS
            yield get(part[1:]) if is_alias else part

    return ''.join(get_all(get(typename)))