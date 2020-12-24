# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/jpeg2kimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 5016 bytes
"""
FabIO class for dealing with JPEG 2000 images.
"""
from __future__ import with_statement, print_function, division
__authors__ = [
 'Valentin Valls']
__date__ = '19/08/2019'
__license__ = 'MIT'
__copyright__ = 'European Synchrotron Radiation Facility, Grenoble, France'
__status__ = 'stable'
import logging
logger = logging.getLogger(__name__)
try:
    import PIL
except ImportError:
    PIL = None

try:
    import glymur
except ImportError:
    glymur = None

from .fabioimage import FabioImage
from .fabioutils import OrderedDict
from .utils import pilutils

class Jpeg2KImage(FabioImage):
    __doc__ = '\n    Images in JPEG 2000 format.\n\n    It uses PIL or glymur libraries.\n    '
    DESCRIPTION = 'JPEG 2000 format'
    DEFAULT_EXTENSIONS = [
     'jp2', 'jpx', 'j2k', 'jpf', 'jpg2']
    _need_a_seek_to_read = True

    def __init__(self, *args, **kwds):
        """ Tifimage constructor adds an nbits member attribute """
        self.nbits = None
        FabioImage.__init__(self, *args, **kwds)
        self.lib = ''
        self._decoders = OrderedDict()
        if PIL is not None:
            self._decoders['PIL'] = self._readWithPil
        if glymur is not None:
            self._decoders['glymur'] = self._readWithGlymur

    def _readWithPil(self, filename, infile):
        """Read data using PIL"""
        pilimage = PIL.Image.open(infile)
        data = pilutils.get_numpy_array(pilimage)
        self.data = data
        if pilimage and pilimage.info:
            for k, v in pilimage.info.items():
                self.header[k] = v

    def _loadGlymurImage(self, filename, infile):
        """
        Hack to use Glymur with Python file object

        This code was tested with all release 0.8.x
        """
        if glymur.__version__.startswith('0.7.'):
            image = glymur.Jp2k(filename=filename)
        else:
            if glymur.__version__.startswith('0.8.'):
                image = glymur.Jp2k(filename=filename, shape=(1, 1))
            else:
                raise IOError('Glymur version %s is not supported' % glymur.__version__)
        infile.seek(0, 2)
        length = infile.tell()
        infile.seek(0)
        image.length = length
        image._shape = None
        image._codec_format = glymur.lib.openjp2.CODEC_JP2
        image.box = image.parse_superbox(infile)
        try:
            image._validate()
        except Exception:
            logger.debug('Backtrace', exc_info=True)
            raise IOError('File %s is not a valid format' % filename)

        return image

    def _readWithGlymur(self, filename, infile):
        """Read data using Glymur"""
        image = self._loadGlymurImage(filename, infile)
        self.data = image.read()

    def read(self, filename, frame=None):
        infile = self._open(filename, 'rb')
        self.data = None
        for name, read in self._decoders.items():
            try:
                infile.seek(0)
                read(filename, infile)
                self.lib = name
                break
            except IOError as e:
                self.data = None
                self.header = OrderedDict()
                logger.debug('Error while using %s library: %s' % (name, e), exc_info=True)

        if self.data is None:
            infile.seek(0)
            raise IOError('No decoder available for the file %s.' % filename)
        self.resetvals()
        return self


jpeg2kimage = Jpeg2KImage