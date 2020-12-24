# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/field/sub_file.py
# Compiled at: 2009-09-07 17:44:28
from hachoir_core.field import Bytes
from hachoir_core.tools import makePrintable, humanFilesize
from hachoir_core.stream import InputIOStream

class SubFile(Bytes):
    """
    File stored in another file
    """
    __module__ = __name__

    def __init__(self, parent, name, length, description=None, parser=None, filename=None, mime_type=None, parser_class=None):
        if filename:
            if not isinstance(filename, unicode):
                filename = makePrintable(filename, 'ISO-8859-1')
            if not description:
                description = 'File "%s" (%s)' % (filename, humanFilesize(length))
        Bytes.__init__(self, parent, name, length, description)

        def createInputStream(cis, **args):
            tags = args.setdefault('tags', [])
            if parser_class:
                tags.append(('class', parser_class))
            if parser is not None:
                tags.append(('id', parser.PARSER_TAGS['id']))
            if mime_type:
                tags.append(('mime', mime_type))
            if filename:
                tags.append(('filename', filename))
            return cis(**args)

        self.setSubIStream(createInputStream)


class CompressedStream:
    __module__ = __name__
    offset = 0

    def __init__(self, stream, decompressor):
        self.stream = stream
        self.decompressor = decompressor(stream)
        self._buffer = ''

    def read(self, size):
        d = self._buffer
        data = [d[:size]]
        size -= len(d)
        if size > 0:
            d = self.decompressor(size)
            data.append(d[:size])
            size -= len(d)
            while size > 0:
                n = 4096
                if self.stream.size:
                    n = min(self.stream.size - self.offset, n)
                    if not n:
                        break
                d = self.stream.read(self.offset, n)[1]
                self.offset += 8 * len(d)
                d = self.decompressor(size, d)
                data.append(d[:size])
                size -= len(d)

        self._buffer = d[size + len(d):]
        return ('').join(data)


def CompressedField(field, decompressor):

    def createInputStream(cis, source=None, **args):
        if field._parent:
            stream = cis(source=source)
            args.setdefault('tags', []).extend(stream.tags)
        else:
            stream = field.stream
        input = CompressedStream(stream, decompressor)
        if source is None:
            source = "Compressed source: '%s' (offset=%s)" % (stream.source, field.absolute_address)
        return InputIOStream(input, source=source, **args)

    field.setSubIStream(createInputStream)
    return field