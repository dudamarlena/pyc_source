# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/ripl/image2exif.py
# Compiled at: 2017-03-01 09:16:28
# Size of source mod 2**32: 329 bytes
from PIL import Image, ExifTags

def get_exif(im):
    exif = im._getexif()
    result = {}
    for key, value in exif.items():
        result[ExifTags.TAGS.get(key, key)] = value

    return result


class Im2Exif:

    def interpret(self, msg, who=None):
        im = Image.open(msg)
        return get_exif(im)