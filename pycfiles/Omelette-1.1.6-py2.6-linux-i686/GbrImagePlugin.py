# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/GbrImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
import Image, ImageFile

def i32(c):
    return ord(c[3]) + (ord(c[2]) << 8) + (ord(c[1]) << 16) + (ord(c[0]) << 24)


def _accept(prefix):
    return i32(prefix) >= 20 and i32(prefix[4:8]) == 1


class GbrImageFile(ImageFile.ImageFile):
    format = 'GBR'
    format_description = 'GIMP brush file'

    def _open(self):
        header_size = i32(self.fp.read(4))
        version = i32(self.fp.read(4))
        if header_size < 20 or version != 1:
            raise SyntaxError, 'not a GIMP brush'
        width = i32(self.fp.read(4))
        height = i32(self.fp.read(4))
        bytes = i32(self.fp.read(4))
        if width <= 0 or height <= 0 or bytes != 1:
            raise SyntaxError, 'not a GIMP brush'
        comment = self.fp.read(header_size - 20)[:-1]
        self.mode = 'L'
        self.size = (width, height)
        self.info['comment'] = comment
        self.data = self.fp.read(width * height)

    def load(self):
        if not self.data:
            return
        self.im = Image.core.new(self.mode, self.size)
        self.im.fromstring(self.data)
        self.data = ''


Image.register_open('GBR', GbrImageFile, _accept)
Image.register_extension('GBR', '.gbr')