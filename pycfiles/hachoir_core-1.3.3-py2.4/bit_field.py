# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/field/bit_field.py
# Compiled at: 2009-09-07 17:44:28
"""
Bit sized classes:
- Bit: Single bit, value is False or True ;
- Bits: Integer with a size in bits ;
- RawBits: unknown content with a size in bits.
"""
from hachoir_core.field import Field
from hachoir_core.i18n import _
from hachoir_core import config

class RawBits(Field):
    """
    Unknown content with a size in bits.
    """
    __module__ = __name__
    static_size = staticmethod(lambda *args, **kw: args[1])

    def __init__(self, parent, name, size, description=None):
        """
        Constructor: see L{Field.__init__} for parameter description
        """
        Field.__init__(self, parent, name, size, description)

    def hasValue(self):
        return True

    def createValue(self):
        return self._parent.stream.readBits(self.absolute_address, self._size, self._parent.endian)

    def createDisplay(self):
        if self._size < config.max_bit_length:
            return unicode(self.value)
        else:
            return _('<%s size=%u>' % (self.__class__.__name__, self._size))

    createRawDisplay = createDisplay


class Bits(RawBits):
    """
    Positive integer with a size in bits

    @see: L{Bit}
    @see: L{RawBits}
    """
    __module__ = __name__


class Bit(RawBits):
    """
    Single bit: value can be False or True, and size is exactly one bit.

    @see: L{Bits}
    """
    __module__ = __name__
    static_size = 1

    def __init__(self, parent, name, description=None):
        """
        Constructor: see L{Field.__init__} for parameter description
        """
        RawBits.__init__(self, parent, name, 1, description=description)

    def createValue(self):
        return 1 == self._parent.stream.readBits(self.absolute_address, 1, self._parent.endian)

    def createRawDisplay(self):
        return unicode(int(self.value))