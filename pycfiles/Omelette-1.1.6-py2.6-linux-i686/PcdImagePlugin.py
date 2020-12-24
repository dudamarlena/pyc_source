# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/PcdImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.1'
import Image, ImageFile

class PcdImageFile(ImageFile.ImageFile):
    format = 'PCD'
    format_description = 'Kodak PhotoCD'

    def _open(self):
        self.fp.seek(2048)
        s = self.fp.read(2048)
        if s[:4] != 'PCD_':
            raise SyntaxError, 'not a PCD file'
        orientation = ord(s[1538]) & 3
        if orientation == 1:
            self.tile_post_rotate = 90
        elif orientation == 3:
            self.tile_post_rotate = -90
        self.mode = 'RGB'
        self.size = (768, 512)
        self.tile = [('pcd', (0, 0) + self.size, 196608, None)]
        return

    def draft(self, mode, size):
        if len(self.tile) != 1:
            return
        (d, e, o, a) = self.tile[0]
        if size:
            scale = max(self.size[0] / size[0], self.size[1] / size[1])
            for (s, o) in [(4, 0), (2, 0), (1, 196608)]:
                if scale >= s:
                    break

        self.tile = [
         (
          d, e, o, a)]
        return self


Image.register_open('PCD', PcdImageFile)
Image.register_extension('PCD', '.pcd')