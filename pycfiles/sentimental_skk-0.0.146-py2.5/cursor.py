# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/canossa/canossa/cursor.py
# Compiled at: 2014-04-25 02:25:23
from attribute import Attribute

class Cursor:
    col = 0
    row = 0
    dirty = True
    attr = None
    _backup = None

    def __init__(self, y=0, x=0, attr=Attribute()):
        self.col = x
        self.row = y
        self.dirty = True
        self.attr = attr
        self._backup = None
        return

    def clear(self):
        self.col = 0
        self.row = 0
        self.dirty = True
        self.attr.clear()

    def save(self):
        self._backup = Cursor(self.row, self.col, self.attr.clone())

    def restore(self):
        if self._backup:
            self.col = self._backup.col
            self.row = self._backup.row
            self.attr = self._backup.attr
            self._backup = None
        return

    def draw(self, s):
        s.write('\x1b[%d;%dH' % (self.row + 1, self.col + 1))
        self.dirty = False

    def setyx(self, y, x):
        self.row = y
        self.col = x

    def getyx(self):
        return (
         self.row, self.col)

    def __str__(self):
        import StringIO
        s = StringIO.StringIO()
        self.draw(s)
        return s.getvalue().replace('\x1b', '<ESC>')


def test():
    """
    >>> cursor = Cursor()
    >>> print cursor
    <ESC>[1;1H
    >>> cursor.clear()
    >>> print cursor
    <ESC>[1;1H
    >>> cursor.setyx(10, 20)
    >>> print cursor
    <ESC>[11;21H
    >>> print cursor.getyx()
    (10, 20)
    >>> cursor.save()
    >>> cursor.setyx(24, 15)
    >>> print cursor
    <ESC>[25;16H
    >>> cursor.clear()
    >>> print cursor
    <ESC>[1;1H
    >>> cursor.restore()
    >>> print cursor
    <ESC>[11;21H
    """
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()