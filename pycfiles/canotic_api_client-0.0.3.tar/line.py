# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/canossa/line.py
# Compiled at: 2014-04-25 02:25:23
from cell import Cell
_LINE_TYPE_DHLT = 3
_LINE_TYPE_DHLB = 4
_LINE_TYPE_SWL = 5
_LINE_TYPE_DWL = 6

class SupportsDoubleSizedTrait:
    """ For DECDWL/DECDHL support
    """
    _type = _LINE_TYPE_SWL

    def set_swl(self):
        """
        >>> line = Line(5)
        >>> line.set_swl()
        >>> line.type() == _LINE_TYPE_SWL
        True
        """
        self._type = _LINE_TYPE_SWL
        self.dirty = True

    def set_dwl(self):
        """
        >>> line = Line(5)
        >>> line.set_dwl()
        >>> line.type() == _LINE_TYPE_DWL
        True
        """
        self._type = _LINE_TYPE_DWL
        self.dirty = True

    def set_dhlt(self):
        """
        >>> line = Line(5)
        >>> line.set_dhlt()
        >>> line.type() == _LINE_TYPE_DHLT
        True
        """
        self._type = _LINE_TYPE_DHLT
        self.dirty = True

    def set_dhlb(self):
        """
        >>> line = Line(5)
        >>> line.set_dhlb()
        >>> line.type() == _LINE_TYPE_DHLB
        True
        """
        self._type = _LINE_TYPE_DHLB
        self.dirty = True

    def is_normal(self):
        return self._type == _LINE_TYPE_SWL

    def type(self):
        """
        >>> line = Line(5)
        >>> line.type() == _LINE_TYPE_SWL
        True
        """
        return self._type


class SupportsWideTrait:
    """ provides pad method. it makes the cell at specified position contain '\x00'. """

    def pad(self, pos):
        cell = self.cells[pos]
        cell.pad()


class SupportsCombiningTrait:
    """ provides combine method. it combines specified character to the cell at specified position. """

    def combine(self, value, pos):
        """
        >>> from attribute import Attribute
        >>> line = Line(5)
        >>> attr = Attribute()
        >>> line.clear(attr._attrvalue)
        >>> line.write(0x40, 1, attr)
        >>> line.combine(0x300, 2)
        """
        self.cells[max(0, pos - 1)].combine(value)


class Line(SupportsDoubleSizedTrait, SupportsWideTrait, SupportsCombiningTrait):

    def __init__(self, width):
        """
        >>> line = Line(10)
        >>> len(line.cells)
        10
        >>> line.dirty
        True
        """
        self.cells = [ Cell() for cell in xrange(0, width) ]
        self.dirty = True

    def length(self):
        """
        >>> line = Line(19)
        >>> line.length()
        19
        """
        return len(self.cells)

    def resize(self, col):
        """
        >>> line = Line(14)
        >>> line.length()
        14
        >>> line.resize(9)
        >>> line.length()
        9
        >>> line.resize(0)
        >>> line.length()
        0
        >>> line.resize(20)
        >>> line.length()
        20
        """
        width = len(self.cells)
        if col < width:
            self.cells = self.cells[:col]
        elif col > width:
            self.cells += [ Cell() for cell in xrange(0, col - width) ]
        self.dirty = True

    def clear(self, attrvalue):
        """
        >>> from attribute import Attribute
        >>> line = Line(5)
        >>> line.clear(Attribute()._attrvalue)
        >>> print line
        <ESC>[0m<SP><SP><SP><SP><SP>
        """
        if not self.dirty:
            self.dirty = True
        self.set_swl()
        for cell in self.cells:
            cell.clear(attrvalue)

    def write(self, value, pos, attr):
        """
        >>> from attribute import Attribute
        >>> line = Line(5)
        >>> attr = Attribute()
        >>> line.clear(attr._attrvalue)
        >>> line.write(0x40, 0, attr)
        >>> print line
        <ESC>[0m@<SP><SP><SP><SP>
        >>> line.write(0x50, 0, attr)
        >>> print line
        <ESC>[0mP<SP><SP><SP><SP>
        >>> line.write(0x3042, 1, attr)
        """
        if not self.dirty:
            self.dirty = True
        self.cells[pos].write(value, attr)

    def drawrange(self, s, left, right, cursor, lazy=False):
        """
        >>> line = Line(5)
        >>> import StringIO
        >>> s = StringIO.StringIO()
        >>> from cursor import Cursor
        >>> line.drawrange(s, 3, 5, Cursor())
        >>> result = s.getvalue().replace("\x1b", "<ESC>")
        >>> result = result.replace(" ", "<SP>")
        >>> print result
        <ESC>[0m<SP><SP>
        """
        cells = self.cells
        attr = cursor.attr
        attr.draw(s)
        c = None
        if left > 0:
            cell = cells[(left - 1)]
            c = cell.get()
            if c is None:
                if False and lazy:
                    s.write(' ')
                    left += 1
                else:
                    s.write('\x08')
        for cell in cells[left:right]:
            c = cell.get()
            if c is not None:
                if not attr.equals(cell.attr):
                    cell.attr.draw(s, attr)
                    attr.copyfrom(cell.attr)
                s.write(c)

        if not lazy:
            if c is None:
                for cell in cells[right:]:
                    c = cell.get()
                    if c is not None:
                        if not attr.equals(cell.attr):
                            cell.attr.draw(s, attr)
                            attr.copyfrom(cell.attr)
                        s.write(c)
                        break

        return

    def drawall(self, s, cursor):
        self.dirty = False
        cells = self.cells
        s.write('\x1b#%d' % self._type)
        attr = cursor.attr
        attr.draw(s)
        c = None
        for cell in cells:
            c = cell.get()
            if c is not None:
                if not attr.equals(cell.attr):
                    cell.attr.draw(s, attr)
                    attr.copyfrom(cell.attr)
                s.write(c)

        if c is None:
            for cell in cells[right:]:
                c = cell.get()
                if c is not None:
                    if not attr.equals(cell.attr):
                        cell.attr.draw(s, attr)
                        attr.copyfrom(cell.attr)
                    s.write(c)
                    break

        return

    def __str__(self):
        """
        >>> line = Line(5)
        >>> print line
        <ESC>[0m<SP><SP><SP><SP><SP>
        """
        import StringIO, codecs, locale
        from cursor import Cursor
        (language, encoding) = locale.getdefaultlocale()
        cursor = Cursor()
        s = codecs.getwriter(encoding)(StringIO.StringIO())
        self.drawrange(s, 0, len(self.cells), cursor)
        result = s.getvalue().replace('\x1b', '<ESC>')
        result = result.replace(' ', '<SP>')
        result = result.replace('\x00', '<NUL>')
        return result


def test():
    """
    >>> from attribute import Attribute
    >>> line = Line(10)
    >>> attr = Attribute()
    >>> print line
    <ESC>[0m<SP><SP><SP><SP><SP><SP><SP><SP><SP><SP>
    >>> line.clear(attr._attrvalue)
    >>> print line
    <ESC>[0m<SP><SP><SP><SP><SP><SP><SP><SP><SP><SP>
    >>> line.write(0x40, 0, attr)
    >>> line.write(0x50, 0, attr)
    >>> print line
    <ESC>[0mP<SP><SP><SP><SP><SP><SP><SP><SP><SP>
    >>> line.write(0x40, 1, attr)
    >>> print line
    <ESC>[0mP@<SP><SP><SP><SP><SP><SP><SP><SP>
    >>> line.pad(2)
    >>> line.write(0x3042, 3, attr)
    """
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    test()