# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/core/files/images.py
# Compiled at: 2019-02-14 00:35:17
"""
Utility functions for handling images.

Requires Pillow as you might imagine.
"""
import struct, zlib
from django.core.files import File

class ImageFile(File):
    """
    A mixin for use alongside django.core.files.base.File, which provides
    additional features for dealing with images.
    """

    @property
    def width(self):
        return self._get_image_dimensions()[0]

    @property
    def height(self):
        return self._get_image_dimensions()[1]

    def _get_image_dimensions(self):
        if not hasattr(self, '_dimensions_cache'):
            close = self.closed
            self.open()
            self._dimensions_cache = get_image_dimensions(self, close=close)
        return self._dimensions_cache


def get_image_dimensions(file_or_path, close=False):
    """
    Returns the (width, height) of an image, given an open file or a path.  Set
    'close' to True to close the file at the end if it is initially in an open
    state.
    """
    from PIL import ImageFile as PillowImageFile
    p = PillowImageFile.Parser()
    if hasattr(file_or_path, 'read'):
        file = file_or_path
        file_pos = file.tell()
        file.seek(0)
    else:
        file = open(file_or_path, 'rb')
        close = True
    try:
        chunk_size = 1024
        while 1:
            data = file.read(chunk_size)
            if not data:
                break
            try:
                p.feed(data)
            except zlib.error as e:
                if e.args[0].startswith('Error -5'):
                    pass
                else:
                    raise
            except struct.error:
                pass

            if p.image:
                return p.image.size
            chunk_size *= 2

        return (None, None)
    finally:
        if close:
            file.close()
        else:
            file.seek(file_pos)

    return