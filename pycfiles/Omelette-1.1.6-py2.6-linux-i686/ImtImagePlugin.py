# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/ImtImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.2'
import string, re, Image, ImageFile
field = re.compile('([a-z]*) ([^ \\r\\n]*)')

class ImtImageFile(ImageFile.ImageFile):
    format = 'IMT'
    format_description = 'IM Tools'

    def _open(self):
        if '\n' not in self.fp.read(100):
            raise SyntaxError, 'not an IM file'
        self.fp.seek(0)
        xsize = ysize = 0
        while 1:
            s = self.fp.read(1)
            if not s:
                break
            if s == chr(12):
                self.tile = [
                 (
                  'raw', (0, 0) + self.size,
                  self.fp.tell(),
                  (
                   self.mode, 0, 1))]
                break
            else:
                s = s + self.fp.readline()
                if len(s) == 1 or len(s) > 100:
                    break
                if s[0] == '*':
                    continue
                m = field.match(s)
                if not m:
                    break
                (k, v) = m.group(1, 2)
                if k == 'width':
                    xsize = int(v)
                    self.size = (xsize, ysize)
                elif k == 'height':
                    ysize = int(v)
                    self.size = (xsize, ysize)
                elif k == 'pixel' and v == 'n8':
                    self.mode = 'L'


Image.register_open('IMT', ImtImageFile)