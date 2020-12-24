# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/GimpPaletteFile.py
# Compiled at: 2007-09-25 20:00:35
import re, string

class GimpPaletteFile:
    rawmode = 'RGB'

    def __init__(self, fp):
        self.palette = map(lambda i: chr(i) * 3, range(256))
        if fp.readline()[:12] != 'GIMP Palette':
            raise SyntaxError, 'not a GIMP palette file'
        i = 0
        while i <= 255:
            s = fp.readline()
            if not s:
                break
            if re.match('\\w+:|#', s):
                continue
            if len(s) > 100:
                raise SyntaxError, 'bad palette file'
            v = tuple(map(int, string.split(s)[:3]))
            if len(v) != 3:
                raise ValueError, 'bad palette entry'
            if 0 <= i <= 255:
                self.palette[i] = chr(v[0]) + chr(v[1]) + chr(v[2])
            i = i + 1

        self.palette = string.join(self.palette, '')

    def getpalette(self):
        return (
         self.palette, self.rawmode)