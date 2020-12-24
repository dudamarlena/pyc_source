# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/WmfImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.2'
import Image, ImageFile
_handler = None

def register_handler(handler):
    global _handler
    _handler = handler


def word(c, o=0):
    return ord(c[o]) + (ord(c[(o + 1)]) << 8)


def short(c, o=0):
    v = ord(c[o]) + (ord(c[(o + 1)]) << 8)
    if v >= 32768:
        v = v - 65536
    return v


def dword(c, o=0):
    return ord(c[o]) + (ord(c[(o + 1)]) << 8) + (ord(c[(o + 2)]) << 16) + (ord(c[(o + 3)]) << 24)


def long(c, o=0):
    return dword(c, o)


def _accept(prefix):
    return prefix[:6] == b'\xd7\xcd\xc6\x9a\x00\x00' or prefix[:4] == '\x01\x00\x00\x00'


class WmfStubImageFile(ImageFile.StubImageFile):
    format = 'WMF'
    format_description = 'Windows Metafile'

    def _open(self):
        s = self.fp.read(80)
        if s[:6] == b'\xd7\xcd\xc6\x9a\x00\x00':
            inch = word(s, 14)
            x0 = short(s, 6)
            y0 = short(s, 8)
            x1 = short(s, 10)
            y1 = short(s, 12)
            size = (
             (x1 - x0) * 72 / inch, (y1 - y0) * 72 / inch)
            self.info['wmf_bbox'] = (
             x0, y0, x1, y1)
            self.info['dpi'] = 72
            if s[22:26] != '\x01\x00\t\x00':
                raise SyntaxError('Unsupported WMF file format')
        elif long(s) == 1 and s[40:44] == ' EMF':
            x0 = long(s, 8)
            y0 = long(s, 12)
            x1 = long(s, 16)
            y1 = long(s, 20)
            frame = (
             long(s, 24), long(s, 28), long(s, 32), long(s, 36))
            size = (
             x1 - x0, y1 - y0)
            xdpi = 2540 * (x1 - y0) / (frame[2] - frame[0])
            ydpi = 2540 * (y1 - y0) / (frame[3] - frame[1])
            self.info['wmf_bbox'] = (
             x0, y0, x1, y1)
            if xdpi == ydpi:
                self.info['dpi'] = xdpi
            else:
                self.info['dpi'] = (
                 xdpi, ydpi)
        else:
            raise SyntaxError('Unsupported file format')
        self.mode = 'RGB'
        self.size = size
        loader = self._load()
        if loader:
            loader.open(self)

    def _load(self):
        return _handler


def _save(im, fp, filename):
    if _handler is None or not hasattr('_handler', 'save'):
        raise IOError('WMF save handler not installed')
    _handler.save(im, fp, filename)
    return


Image.register_open(WmfStubImageFile.format, WmfStubImageFile, _accept)
Image.register_save(WmfStubImageFile.format, _save)
Image.register_extension(WmfStubImageFile.format, '.wmf')
Image.register_extension(WmfStubImageFile.format, '.emf')