# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/imagefromfile.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 5750 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '06/08/2018'
import functools, logging, os
from silx.gui import qt
from silx.io.url import DataUrl
from tomwer.core.utils import ftseriesutils
from tomwer.synctools.imageloaderthread import ImageLoaderThread
logger = logging.getLogger(__name__)

class _Image(qt.QObject):

    def __init__(self, data):
        qt.QObject.__init__(self)
        self.data = data


class ImageFromFile(_Image):
    __doc__ = '\n    Define an Image with a status\n    '
    LOADING_STATUS = {'loading':0,  'loaded':1,  'not loaded':2}
    sigLoaded = qt.Signal(str)

    def __init__(self, _file=None, index=None, data=None, _load=False, url=None):
        _Image.__init__(self, data)
        if url is not None:
            if not (_file is None and index is None):
                raise AssertionError
            self.url = url
        else:
            if not isinstance(_file, str):
                raise AssertionError
            elif _file.lower().endswith('.edf'):
                scheme = 'fabio'
            else:
                scheme = 'silx'
            self.url = DataUrl(file_path=_file, data_slice=index, scheme=scheme)
        self._status = 'not loaded' if data is None else 'loaded'
        self.url_path = self.url.path()
        if _load is True:
            self.load()

    def load(self, sync=False):
        """
        Load the data contained in the url.

        :param sync: if True: then wait for the image to be loaded for giving
            back hand
        """
        if self._status == 'loaded' and self.data is not None:
            self.sigLoaded.emit(self.url.path())
        else:
            if self._status == 'loading':
                logger.debug('%s is already loading' % self.url.path())
            else:
                self._status = 'loading'
                self.loaderThread = ImageLoaderThread(url=(self.url))
                callback = functools.partial(self._setData, self.url_path, self.loaderThread.getData)
                self.loaderThread.finished.connect(callback)
                self.loaderThread.start()
                if sync is False:
                    self.loaderThread.wait()

    def _setData(self, url_path, dataGetter):
        self.data = dataGetter()
        if self.data is not None:
            if self.data.ndim != 2:
                if self.data.shape[0] == 1:
                    self.data = self.data.reshape(self.data.shape[1:])
                else:
                    if self.data.shape[(-1)] == 1:
                        self.data = self.data.reshape(self.data.shape[0:-1])
        self._status = 'loaded'
        self.sigLoaded.emit(url_path)

    def isLoaded(self):
        return self._status == 'loaded'


class FileWithImage(object):
    __doc__ = 'Definition of file which can contain multiple images'

    def __init__(self, _file):
        self.file = _file

    def getImages(self, _load):
        """

        :param bool _load: if True then launch the load of the image
        :return: the list of images contained in the given file.
        """
        if self.file.endswith('.vol'):
            return self._dealWithVolFile(self.file, _load)
        if self.file.lower().endswith('.edf'):
            return [
             ImageFromFile(self.file)]
        logger.error('only deal with .edf and .vol extension')
        return []

    def _dealWithVolFile(self, _file, _load):
        _imagesFiles = []
        volInfoFile = _file.replace('.vol', '.vol.info')
        if not os.path.exists(volInfoFile):
            mess = "Can't find description file %s associated with raw data file %s " % (
             volInfoFile, _file)
            logger.warning(mess)
        else:
            shape = ftseriesutils._getShapeForVolFile(volInfoFile)
            if shape is not None:
                for zSlice in range(shape[0]):
                    if _file.lower().endswith('.edf'):
                        scheme = 'fabio'
                    else:
                        scheme = 'tomwer'
                    _imagesFiles.append(ImageFromFile(url=DataUrl(file_path=_file, data_slice=(
                     zSlice,),
                      scheme=scheme),
                      _load=_load))

            return _imagesFiles