# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sqlpython/imagedetect.py
# Compiled at: 2012-05-26 21:28:24


def is_jpg(data):
    """True if data is the first 11 bytes of a JPEG file."""
    return data[:4] == b'\xff\xd8\xff\xe0' and data[6:11] == 'JFIF\x00'


def is_png(data):
    """True if data is the first 8 bytes of a PNG file."""
    return data[:8] == b'\x89PNG\r\n\x1a\n'


def is_tiff(data):
    """True if data is the first 4 bytes of a TIFF file."""
    return data[:4] == 'MM\x00*' or data[:4] == 'II*\x00'


def is_gif(data):
    """True if data is the first 4 bytes of a GIF file."""
    return data[:4] == 'GIF8'


def extension_from_data(data):
    """Returns extension (like '.jpg') from first 11 bytes of image data.

    An empty string is returned if no match is found."""
    if is_jpg(data):
        return '.jpg'
    if is_png(data):
        return '.png'
    if is_tiff(data):
        return '.tif'
    if is_gif(data):
        return '.gif'
    return ''


def extension_from_file(path):
    """Returns extension (like '.jpg') based on content of image file at path.

    An empty string is returned if no match is found."""
    f = file(path, 'r')
    ext = extension_from_data(f.read(11))
    f.close()
    return ext