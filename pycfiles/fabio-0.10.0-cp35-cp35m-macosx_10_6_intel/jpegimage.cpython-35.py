# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/jpegimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 3410 bytes
"""
FabIO class for dealing with JPEG images.
"""
from __future__ import with_statement, print_function, division
__authors__ = [
 'Valentin Valls']
__date__ = '04/03/2019'
__license__ = 'MIT'
__copyright__ = 'European Synchrotron Radiation Facility, Grenoble, France'
__status__ = 'stable'
import logging
logger = logging.getLogger(__name__)
try:
    from PIL import Image
except ImportError:
    Image = None

from .fabioimage import FabioImage
from .utils import pilutils
JPEG_RESERVED_HEADER_KEYS = [
 'jfif',
 'jfif_version',
 'jfif_density',
 'jfif_unit',
 'dpi',
 'adobe',
 'adobe_transform',
 'progression',
 'icc_profile',
 'exif',
 'quality',
 'optimize',
 'progressive',
 'dpi',
 'exif',
 'subsampling',
 'qtables']

class JpegImage(FabioImage):
    __doc__ = '\n    Images in JPEG format using PIL\n    '
    DESCRIPTION = 'JPEG format'
    DEFAULT_EXTENSIONS = [
     'jpg', 'jpeg']
    RESERVED_HEADER_KEYS = JPEG_RESERVED_HEADER_KEYS
    _need_a_seek_to_read = True

    def __init__(self, *args, **kwds):
        """ Tifimage constructor adds an nbits member attribute """
        self.nbits = None
        FabioImage.__init__(self, *args, **kwds)

    def _readWithPil(self, filename, infile):
        try:
            infile.seek(0)
            pilimage = Image.open(infile)
        except Exception:
            pilimage = None
            infile.seek(0)
            raise IOError('Error in opening %s with PIL' % filename)

        data = pilutils.get_numpy_array(pilimage)
        self.data = data
        if pilimage and pilimage.info:
            for k, v in pilimage.info.items():
                self.header[k] = v

    def read(self, filename, frame=None):
        infile = self._open(filename, 'rb')
        self.data = None
        if Image is not None:
            self._readWithPil(filename, infile)
        if self.data is None:
            infile.seek(0)
            raise IOError('Error in opening %s.' % filename)
        self.resetvals()
        return self


jpegimage = JpegImage