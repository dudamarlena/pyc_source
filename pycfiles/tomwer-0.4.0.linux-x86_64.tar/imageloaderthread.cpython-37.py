# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/synctools/imageloaderthread.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 6174 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '02/06/2017'
from silx.gui import qt
import numpy, logging, os
import silx.io.utils as silx_get_data
from tomwer.core.utils import ftseriesutils
import tomwer.resources
from tomwer.core.log import TomwerLogger
logger = TomwerLogger(__name__)

class ImageLoaderThread(qt.QThread):
    __doc__ = 'Thread used to load an image'
    IMG_NOT_FOUND = numpy.load(tomwer.resources._resource_filename(('%s.%s' % ('imageNotFound',
                                                                               'npy')), default_directory=(os.path.join('gui', 'icons'))))

    def __init__(self, url):
        super(qt.QThread, self).__init__()
        self.data = None
        self.url = url

    def getData(self):
        if hasattr(self, 'data'):
            return self.data
        return

    def run(self):
        if os.path.exists(self.url.file_path()):
            if os.path.isfile(self.url.file_path()):
                if self.url.file_path().lower().endswith('.vol.info') or self.url.file_path().lower().endswith('.vol'):
                    self.data = self._loadVol()
            else:
                try:
                    self.data = silx_get_data(self.url)
                except:
                    logger.warning('file %s not longer exists or is empty' % self.url)
                    self.data = None

        else:
            logger.warning('file %s not longer exists or is empty' % self.url)
            self.data = self.IMG_NOT_FOUND

    def _loadVol(self):
        if self.url.file_path().lower().endswith('.vol.info'):
            infoFile = self.url.file_path()
            rawFile = self.url.file_path().replace('.vol.info', '.vol')
        else:
            assert self.url.file_path().lower().endswith('.vol')
            rawFile = self.url.file_path()
            infoFile = self.url.file_path().replace('.vol', '.vol.info')
        if not os.path.exists(rawFile):
            data = None
            mess = "Can't find raw data file %s associated with %s" % (rawFile, infoFile)
            logger.warning(mess)
        else:
            if not os.path.exists(infoFile):
                mess = "Can't find info file %s associated with %s" % (infoFile, rawFile)
                logger.warning(mess)
                data = None
            else:
                shape = ftseriesutils._getShapeForVolFile(infoFile)
        if None in shape:
            logger.warning('Fail to retrieve data shape for %s.' % infoFile)
            data = None
        else:
            try:
                numpy.zeros(shape)
            except MemoryError:
                data = None
                logger.warning('Raw file %s is to large for being readed %s' % rawFile)
            else:
                data = numpy.fromfile(rawFile, dtype=(numpy.float32), count=(-1),
                  sep='')
                try:
                    data = data.reshape(shape)
                except ValueError:
                    logger.warning('unable to fix shape for raw file %s. Look for information in %s' % (
                     rawFile, infoFile))
                    try:
                        sqr = int(numpy.sqrt(len(data)))
                        shape = (1, sqr, sqr)
                        data = data.reshape(shape)
                    except ValueError:
                        logger.info('deduction of shape size for %s failed' % rawFile)
                        data = None
                    else:
                        logger.warning('try deducing shape size for %s might be an incorrect interpretation' % rawFile)

                if self.url.data_slice() is None:
                    return data
                return data[self.url.data_slice()]