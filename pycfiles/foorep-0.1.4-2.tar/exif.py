# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jbn/s/code/foorep/foorep/plugins/exif.py
# Compiled at: 2012-12-14 06:53:09
from foorep import Plugin

class Exif(Plugin):

    def analyze(self, path):
        try:
            import pyexiv2
        except ImportError:
            return

        try:
            exif = pyexiv2.ImageMetadata(path)
            exif.read()
            self.tags = exif.exif_keys
        except IOError:
            return

        if self.tags:
            result = {'type': 'exif', 'value': {}}
            for tag in exif.exif_keys:
                result['value'][tag.replace('.', '_')] = exif[tag].human_value

        else:
            result = None
        return result