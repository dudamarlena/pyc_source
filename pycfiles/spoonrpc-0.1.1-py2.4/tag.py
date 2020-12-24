# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/spoon/ber/tag.py
# Compiled at: 2006-11-19 22:32:38
from common import BERException, inflate_long, deflate_long
from common import UNIVERSAL, APPLICATION, CONTEXT, PRIVATE
_class_name = {UNIVERSAL: 'UNIVERSAL', APPLICATION: 'APPLICATION', CONTEXT: 'CONTEXT', PRIVATE: 'PRIVATE'}

class Tag(object):
    """
    Representation of the header of an ASN.1 object.  This includes the
    class (universal, application, context, or private), the type tag (any
    integer), and size.
    """
    __module__ = __name__

    def __init__(self, tag_class=0, tag=UNIVERSAL, size=None, container=False, _bytes_read=0):
        self._tag_class = tag_class
        self._tag = tag
        self._size = size
        self._container = container
        self._bytes_read = _bytes_read

    def __repr__(self):
        return '<ASN.1 Tag(%s, %d, size=%r, container=%r)>' % (_class_name[self._tag_class], self._tag, self._size, self._container)

    def __cmp__(self, other):
        if not isinstance(other, Tag):
            raise ValueError('not comparable with %r', other)
        x = cmp(self._tag_class, other._tag_class)
        if x != 0:
            return x
        x = cmp(self._container, other._container)
        if x != 0:
            return x
        return cmp(self._tag, other._tag)

    def __hash__(self):
        n = self._tag_class
        n *= 37
        if self._container:
            n += 1
        n *= 37
        n += self._tag
        return n

    tag_class = property(lambda self: self._tag_class, None, None)
    tag = property(lambda self: self._tag, None, None)
    size = property(lambda self: self._size, None, None)
    container = property(lambda self: self._container, None, None)

    def is_terminator(self):
        """
        Return C{True} if this tag is the special type used to terminate
        indefinite-length sequences (type 0, length 0).
        """
        return self._tag_class == UNIVERSAL and not self._container and self._tag == 0 and self._size == 0

    @staticmethod
    def make_terminator():
        """
        Return a tag that can be used to terminate indefinite-length sequences.
        """
        return Tag(Tag.UNIVERSAL, False, 0, 0)

    @staticmethod
    def from_tag(t, size=None):
        return Tag(t._tag_class, t._tag, size, t._container)

    @staticmethod
    def from_stream(fd):
        tag = fd.read(1)
        if len(tag) == 0:
            return
        bytes_read = 1
        tag = ord(tag)
        tag_class = tag >> 6
        if tag & 32:
            tag_container = True
        else:
            tag_container = False
        tag &= 31
        if tag == 31:
            tag = 0
            while True:
                t = fd.read(1)
                if len(t) == 0:
                    raise BERException('abrupt end of tag field')
                bytes_read += 1
                t = ord(t)
                tag = tag << 7 | t & 127
                if not t & 128:
                    break

        size = fd.read(1)
        if len(size) == 0:
            raise BERException('expected size field')
        bytes_read += 1
        size = ord(size)
        if size == 128:
            size = None
            if not tag_container:
                raise BERException('indefinite-length tags must refer to sequences')
        elif size & 128:
            size &= 127
            x = fd.read(size)
            if len(x) != size:
                raise BERException('truncated size field')
            bytes_read += size
            size = inflate_long(x, True)
        return Tag(tag_class, tag, size, container=tag_container, _bytes_read=bytes_read)

    def __len__(self):
        if self._bytes_read > 0:
            return self._bytes_read
        n = 2
        if self.tag > 30:
            t = self.tag
            while t > 0:
                n += 1
                t >>= 7

        if self.size > 127:
            n += len(deflate_long(self.size))
        return n

    def write(self, fd):
        high_bits = self._tag_class << 6
        if self._container:
            high_bits |= 32
        if self._tag <= 30:
            fd.write(chr(self._tag | high_bits))
        elif self._tag <= 127:
            fd.write(chr(high_bits | 31))
            fd.write(chr(self._tag))
        else:
            fd.write(chr(high_bits | 31))
            tag = self._tag
            tagstr = chr(tag & 127)
            tag >>= 7
            while tag > 0:
                tagstr = chr(128 | tag & 127) + tagstr
                tag >>= 7

            fd.write(tagstr)
        if self._size is None:
            fd.write(chr(128))
        elif self._size > 127:
            lenstr = deflate_long(self._size)
            fd.write(chr(128 | len(lenstr)))
            fd.write(lenstr)
        else:
            fd.write(chr(self._size))
        return