# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/field/character.py
# Compiled at: 2009-09-07 17:44:28
"""
Character field class: a 8-bit character
"""
from hachoir_core.field import Bits
from hachoir_core.endian import BIG_ENDIAN
from hachoir_core.tools import makePrintable

class Character(Bits):
    """
    A 8-bit character using ASCII charset for display attribute.
    """
    __module__ = __name__
    static_size = 8

    def __init__(self, parent, name, description=None):
        Bits.__init__(self, parent, name, 8, description=description)

    def createValue(self):
        return chr(self._parent.stream.readBits(self.absolute_address, 8, BIG_ENDIAN))

    def createRawDisplay(self):
        return unicode(Bits.createValue(self))

    def createDisplay(self):
        return makePrintable(self.value, 'ASCII', quote="'", to_unicode=True)