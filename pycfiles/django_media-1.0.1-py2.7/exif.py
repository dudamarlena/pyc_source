# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/media/exif.py
# Compiled at: 2012-04-05 17:30:57
from PIL import Image
from PIL.ExifTags import TAGS

def show_exif(file):
    """
    Return a dictionary of decoded exif data.

    Thanks to Mike Driscoll: http://is.gd/0EkUar
    """
    exif = {}
    try:
        image = Image.open(file)
        raw = image._getexif()
        for tag, value in raw.items():
            decoded = TAGS.get(tag, tag)
            exif[decoded] = value

    except:
        pass

    return exif