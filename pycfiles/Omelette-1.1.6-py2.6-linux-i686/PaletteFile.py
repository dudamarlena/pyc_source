# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/PaletteFile.py
# Compiled at: 2007-09-25 20:00:35
import string

class PaletteFile:
    rawmode = 'RGB'

    def __init__(self, fp):
        self.palette = map(lambda i: (i, i, i), range(256))
        while 1:
            s = fp.readline()
            if not s:
                break
            if len(s) > 100:
                raise SyntaxError, 'bad palette file'
            v = map(int, string.split(s))
            try:
                (i, r, g, b) = v
            except ValueError:
                (i, r) = v
                g = b = r

            if 0 <= i <= 255:
                self.palette[i] = chr(r) + chr(g) + chr(b)

        self.palette = string.join(self.palette, '')

    def getpalette(self):
        return (
         self.palette, self.rawmode)