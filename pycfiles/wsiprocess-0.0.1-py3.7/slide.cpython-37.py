# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/wsiprocess/slide.py
# Compiled at: 2019-11-28 08:31:06
# Size of source mod 2**32: 820 bytes
import pyvips
from pathlib import Path

class Slide:

    def __init__(self, path):
        self.slide = pyvips.Image.new_from_file(path)
        self.filestem = Path(path).stem
        self.wsi_width = self.slide.width
        self.wsi_height = self.slide.height
        try:
            self.magnification = self.slide.get('openslide.objective-power')
        except:
            self.magnification = None

        self.set_properties()

    def export_thumbnail(self, save_to, size=500):
        thumb = self.get_thumbnail(size)
        thumb.pngsave('{}/thumb.png'.format(save_to))

    def get_thumbnail(self, size=500):
        return self.slide.thumbnail_image(size, height=size)

    def set_properties(self):
        for field in self.slide.get_fields():
            setattr(self, field, self.slide.get(field))