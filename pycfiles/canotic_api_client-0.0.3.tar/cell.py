# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/canossa/cell.py
# Compiled at: 2014-04-25 02:25:23
from attribute import Attribute

class Cell:
    r"""
    >>> from attribute import Attribute
    >>> cell = Cell()
    >>> attr = Attribute()
    >>> cell.get()
    u' '
    >>> cell.write(0x34, attr)
    >>> cell.get()
    u'4'
    >>> cell.clear(attr._attrvalue)
    >>> cell.get()
    u' '
    >>> cell.write(0x3042, attr)
    >>> cell.get()
    u'\u3042'
    >>> cell.pad()
    >>> cell.get()
    >>> cell.write(0x09a4, attr)
    >>> cell.get()
    u'\u09a4'
    >>> cell.combine(0x20DE)
    >>> cell.get()
    u'\u09a4\u20de'
    >>> cell.combine(0x20DD)
    >>> cell.get()
    u'\u09a4\u20de\u20dd'
    >>> cell.combine(0x0308)
    >>> cell.get()
    u'\u09a4\u20de\u20dd\u0308'
    """
    _value = None
    _combine = None

    def __init__(self):
        self._value = 32
        self.attr = Attribute()

    def write(self, value, attr):
        self._value = value
        self.attr.copyfrom(attr)

    def pad(self):
        self._value = None
        return

    def combine(self, value):
        if self._combine:
            self._combine += unichr(value)
        else:
            self._combine = unichr(value)

    def get(self):
        c = self._value
        if c is None:
            return
        if c < 65536:
            result = unichr(c)
        else:
            c -= 65536
            c1 = (c >> 10) + 55296
            c2 = (c & 1023) + 56320
            result = unichr(c1) + unichr(c2)
        if self._combine is None:
            return result
        return result + self._combine

    def clear(self, attrvalue):
        self._value = 32
        self._combine = None
        self.attr.setvalue(attrvalue)
        return


def test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()