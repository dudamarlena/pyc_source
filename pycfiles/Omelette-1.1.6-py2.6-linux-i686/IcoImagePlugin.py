# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/IcoImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.1'
import string, Image, BmpImagePlugin

def i16(c):
    return ord(c[0]) + (ord(c[1]) << 8)


def i32(c):
    return ord(c[0]) + (ord(c[1]) << 8) + (ord(c[2]) << 16) + (ord(c[3]) << 24)


def _accept(prefix):
    return prefix[:4] == '\x00\x00\x01\x00'


class IcoImageFile(BmpImagePlugin.BmpImageFile):
    format = 'ICO'
    format_description = 'Windows Icon'

    def _open(self):
        s = self.fp.read(6)
        if not _accept(s):
            raise SyntaxError, 'not an ICO file'
        m = ''
        for i in range(i16(s[4:])):
            s = self.fp.read(16)
            if not m:
                m = s
            elif ord(s[0]) > ord(m[0]) and ord(s[1]) > ord(m[1]):
                m = s

        self._bitmap(i32(m[12:]))
        self.size = (
         self.size[0], self.size[1] / 2)
        (d, e, o, a) = self.tile[0]
        self.tile[0] = (d, (0, 0) + self.size, o, a)


Image.register_open('ICO', IcoImageFile, _accept)
Image.register_extension('ICO', '.ico')