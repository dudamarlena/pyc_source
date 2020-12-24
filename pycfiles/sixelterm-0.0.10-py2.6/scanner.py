# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/sixelterm/scanner.py
# Compiled at: 2012-11-25 09:41:00
import tff, sixel
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

_MODE_NORMAL = 0
_MODE_PNG = 1
_MODE_JPEG = 2
_JPEG_SOI = b'\xff\xd8'
_JPEG_EOI = b'\xff\xd9'
_PNG_IEND = ''

class ImageAwareScanner(tff.Scanner):
    """ scan input stream and iterate characters """

    def __init__(self):
        self.__imagebuffer = StringIO()
        self.__mode = _MODE_NORMAL
        self.__writer = sixel.SixelWriter()

    def __writeimage(self, value):
        self.__imagebuffer.write(value)

    def __convert(self):
        try:
            data = self.__imagebuffer.getvalue()
            self.__writer.draw(StringIO(data))
        except:
            self.__data += 'cannot identify image file\n'

        self.__imagebuffer = StringIO()

    def assign(self, value, termenc):
        self.__termenc = termenc
        if self.__mode == _MODE_PNG:
            pos = value.find(b'IEND\xaeB`\x82')
            if pos != -1:
                pos += len(b'IEND\xaeB`\x82')
                self.__mode = _MODE_NORMAL
                self.__data = value[pos:]
                self.__writeimage(value[:pos])
                self.__convert()
            else:
                self.__writeimage(value)
        elif self.__mode == _MODE_JPEG:
            pos = value.find(_JPEG_EOI)
            if pos != -1:
                pos += len(_JPEG_EOI)
                if pos != len(value) and (value[pos] == '\x00' or value[pos] == b'\xff'):
                    self.__writeimage(value)
                else:
                    self.__mode = _MODE_NORMAL
                    self.__data = value[pos:]
                    self.__writeimage(value[:pos])
                    self.__convert()
            else:
                self.__writeimage(value)
        else:
            pos = value.find(b'\x89PNG')
            if pos != -1:
                self.__mode = _MODE_PNG
                self.__cr = False
                self.__data = value[:pos]
                self.__writeimage(value[pos:])
                return
            pos = value.find(_JPEG_SOI)
            if pos != -1:
                self.__mode = _MODE_JPEG
                self.__cr = False
                self.__data = value[:pos]
                self.__writeimage(value[pos:])
                return
            self.__data = value

    def __iter__(self):
        if self.__mode == _MODE_NORMAL:
            for x in unicode(self.__data, self.__termenc, 'ignore'):
                yield ord(x)