# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/field/byte_field.py
# Compiled at: 2009-09-07 17:44:28
"""
Very basic field: raw content with a size in byte. Use this class for
unknown content.
"""
from hachoir_core.field import Field, FieldError
from hachoir_core.tools import makePrintable
from hachoir_core.bits import str2hex
from hachoir_core import config
MAX_LENGTH = 2 ** 64

class RawBytes(Field):
    """
    Byte vector of unknown content

    @see: L{Bytes}
    """
    __module__ = __name__
    static_size = staticmethod(lambda *args, **kw: args[1] * 8)

    def __init__(self, parent, name, length, description='Raw data'):
        assert issubclass(parent.__class__, Field)
        if not 0 < length <= MAX_LENGTH:
            raise FieldError('Invalid RawBytes length (%s)!' % length)
        Field.__init__(self, parent, name, length * 8, description)
        self._display = None
        return

    def _createDisplay(self, human):
        max_bytes = config.max_byte_length
        if type(self._getValue) is type(lambda : None):
            display = self.value[:max_bytes]
        else:
            if self._display is None:
                address = self.absolute_address
                length = min(self._size / 8, max_bytes)
                self._display = self._parent.stream.readBytes(address, length)
            display = self._display
        truncated = 8 * len(display) < self._size
        if human:
            if truncated:
                display += '(...)'
            return makePrintable(display, 'latin-1', quote='"', to_unicode=True)
        else:
            display = str2hex(display, format='\\x%02x')
            if truncated:
                return '"%s(...)"' % display
            else:
                return '"%s"' % display
        return

    def createDisplay(self):
        return self._createDisplay(True)

    def createRawDisplay(self):
        return self._createDisplay(False)

    def hasValue(self):
        return True

    def createValue(self):
        assert self._size % 8 == 0
        if self._display:
            self._display = None
        return self._parent.stream.readBytes(self.absolute_address, self._size / 8)


class Bytes(RawBytes):
    """
    Byte vector: can be used for magic number or GUID/UUID for example.

    @see: L{RawBytes}
    """
    __module__ = __name__