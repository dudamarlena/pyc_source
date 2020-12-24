# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/field/new_seekable_field_set.py
# Compiled at: 2010-01-19 19:10:22
from hachoir_core.field import BasicFieldSet, GenericFieldSet, ParserError, createRawField
from hachoir_core.error import HACHOIR_ERRORS

def getgaps(start, length, blocks):
    """
    Example:
    >>> list(getgaps(0, 20, [(15,3), (6,2), (6,2), (1,2), (2,3), (11,2), (9,5)]))
    [(0, 1), (5, 1), (8, 1), (14, 1), (18, 2)]
    """
    blocks = sorted(blocks, key=lambda b: b[0])
    end = start + length
    for (s, l) in blocks:
        if s > start:
            yield (
             start, s - start)
            start = s
        if s + l > start:
            start = s + l

    if start < end:
        yield (
         start, end - start)


class NewRootSeekableFieldSet(GenericFieldSet):
    __module__ = __name__

    def seekBit(self, address, relative=True):
        if not relative:
            address -= self.absolute_address
        if address < 0:
            raise ParserError('Seek below field set start (%s.%s)' % divmod(address, 8))
        self._current_size = address
        return

    def seekByte(self, address, relative=True):
        return self.seekBit(address * 8, relative)

    def _fixLastField(self):
        """
        Try to fix last field when we know current field set size.
        Returns new added field if any, or None.
        """
        assert self._size is not None
        message = [
         'stop parser']
        self._field_generator = None
        while self._size < self._current_size:
            field = self._deleteField(len(self._fields) - 1)
            message.append('delete field %s' % field.path)

        assert self._current_size <= self._size
        blocks = [ (x.absolute_address, x.size) for x in self._fields ]
        fields = []
        for (start, length) in getgaps(self.absolute_address, self._size, blocks):
            self.seekBit(start, relative=False)
            field = createRawField(self, length, 'unparsed[]')
            self.setUniqueFieldName(field)
            self._fields.append(field.name, field)
            fields.append(field)
            message.append('found unparsed segment: start %s, length %s' % (start, length))

        self.seekBit(self._size, relative=False)
        message = (', ').join(message)
        if fields:
            self.warning('[Autofix] Fix parser error: ' + message)
        return fields

    def _stopFeeding(self):
        new_field = None
        if self._size is None:
            if self._parent:
                self._size = self._current_size
        new_field = self._fixLastField()
        self._field_generator = None
        return new_field


class NewSeekableFieldSet(NewRootSeekableFieldSet):
    __module__ = __name__

    def __init__(self, parent, name, description=None, size=None):
        assert issubclass(parent.__class__, BasicFieldSet)
        NewRootSeekableFieldSet.__init__(self, parent, name, parent.stream, description, size)