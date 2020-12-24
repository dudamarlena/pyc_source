# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/PIL/MicImagePlugin.py
# Compiled at: 2007-09-25 20:00:35
__version__ = '0.1'
import string, Image, TiffImagePlugin
from OleFileIO import *

def _accept(prefix):
    return prefix[:8] == MAGIC


class MicImageFile(TiffImagePlugin.TiffImageFile):
    format = 'MIC'
    format_description = 'Microsoft Image Composer'

    def _open(self):
        try:
            self.ole = OleFileIO(self.fp)
        except IOError:
            raise SyntaxError, 'not an MIC file; invalid OLE file'

        self.images = []
        for file in self.ole.listdir():
            if file[1:] and file[0][-4:] == '.ACI' and file[1] == 'Image':
                self.images.append(file)

        if not self.images:
            raise SyntaxError, 'not an MIC file; no image entries'
        self.__fp = self.fp
        self.frame = 0
        if len(self.images) > 1:
            self.category = Image.CONTAINER
        self.seek(0)

    def seek(self, frame):
        try:
            filename = self.images[frame]
        except IndexError:
            raise EOFError, 'no such frame'

        self.fp = self.ole.openstream(filename)
        TiffImagePlugin.TiffImageFile._open(self)
        self.frame = frame

    def tell(self):
        return self.frame


Image.register_open('MIC', MicImageFile, _accept)
Image.register_extension('MIC', '.mic')