# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/artpacker/saver/jpeg.py
# Compiled at: 2012-05-29 14:37:01
import ImageFile
from artpacker.saver import Saver

class JPEGSaver(Saver):

    def __init__(self, output_path, filename_prefix, progressive=False, quality=85):
        Saver.__init__(self, 'jpg', output_path, filename_prefix)
        self.progressive = progressive
        self.quality = quality
        self.output_path = output_path

    def save_file(self, image, filename):
        ImageFile.MAXBLOCK = image.size[0] * image.size[1]
        image.save(filename, 'JPEG', quality=self.quality, optimize=True, progressive=self.progressive)