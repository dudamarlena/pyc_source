# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/betsee/util/path/guifiletype.py
# Compiled at: 2019-08-01 01:03:54
# Size of source mod 2**32: 1926 bytes
"""
:mod:`PySide2`-based filetype functionality.
"""
from PySide2.QtGui import QImageReader
from betse.util.type.decorator.decmemo import func_cached
from betse.util.type.types import SetType

@func_cached
def get_image_read_filetypes() -> SetType:
    """
    Set of all image filetypes readable by the low-level :class:`QImageReader`
    utility class internally required by all high-level image classes (e.g.,
    :class:`PySide2.QtGui.QImage`, :class:`PySide2.QtGui.QPicture`).

    For generality, these filetypes are *not* prefixed by a ``.`` delimiter.

    Examples
    ----------
        >>> from betsee.util.path import guifiletype
        >>> guifiletype.get_image_read_filetypes()
        ... {'bmp',
        ...  'cur',
        ...  'gif',
        ...  'ico',
        ...  'jpeg',
        ...  'jpg',
        ...  'pbm',
        ...  'pgm',
        ...  'png',
        ...  'ppm',
        ...  'svg',
        ...  'svgz',
        ...  'xbm',
        ...  'xpm'}
    """
    from betsee.util.type.text import guistr
    return {guistr.decode_qbytearray_ascii(image_filetype_qbytearray) for image_filetype_qbytearray in QImageReader.supportedImageFormats()}