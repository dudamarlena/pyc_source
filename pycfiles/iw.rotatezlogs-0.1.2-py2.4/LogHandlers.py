# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/rotatezlogs/LogHandlers.py
# Compiled at: 2008-07-29 13:25:24
"""Plugins for zLOG

$Id: LogHandlers.py 5746 2006-06-05 19:30:17Z glenfant $
"""
import os, logging
from logging.handlers import RotatingFileHandler as BaseHandler
import zipfile, gzip
try:
    import bz2
except ImportError, e:
    bz2 = None

from ZConfig.components.logger.handlers import FileHandlerFactory

class RotateFileHandler(BaseHandler):
    """A standard RotatingFileHandler with zLOG compatibility"""
    __module__ = __name__

    def __init__(self, path, max_bytes, backup_count, compression):
        """Built by the factory and nothing else..."""
        filename = os.path.abspath(path)
        BaseHandler.__init__(self, filename, mode='a', maxBytes=max_bytes, backupCount=backup_count)
        self.baseFilename = filename
        self.compressor = getCompressor(compression)

    def doRollover(self):
        """Overrides method from logging.handlers.RotatingFileHandler"""
        self.stream.close()
        if self.backupCount > 0:
            file_pattern = self.compressor.file_pattern
            for i in range(self.backupCount - 1, 0, -1):
                sfn = file_pattern % (self.baseFilename, i)
                dfn = file_pattern % (self.baseFilename, i + 1)
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)

            self.compressor.compress(self.baseFilename)
        self.stream = file(self.baseFilename, 'w')

    def reopen(self):
        """Mandatory for the factory but useless in our case"""
        self.close()
        self.stream = open(self.baseFilename, 'a')


class NoneCompressor(object):
    """Just rotating, no compression"""
    __module__ = __name__
    file_pattern = '%s.%d'

    def compress(self, filename):
        dfn = filename + '.1'
        if os.path.exists(dfn):
            os.remove(dfn)
        os.rename(filename, dfn)


class ZipCompressor(object):
    """Zip compression"""
    __module__ = __name__
    file_pattern = '%s.%d.zip'

    def compress(self, filename):
        dfn = filename + '.1.zip'
        if os.path.exists(dfn):
            os.remove(dfn)
        zf = zipfile.ZipFile(dfn, 'w', zipfile.ZIP_DEFLATED)
        zf.write(filename, os.path.basename(filename))
        zf.close()
        os.remove(filename)


class GzipCompressor(object):
    """Gzip compression"""
    __module__ = __name__
    file_pattern = '%s.%d.gz'

    def compress(self, filename):
        dfn = filename + '.1.gz'
        if os.path.exists(dfn):
            os.remove(dfn)
        zf = gzip.GzipFile(dfn, 'wb')
        zf.write(file(filename, 'rb').read())
        zf.close()
        os.remove(filename)


if bz2:

    class Bzip2Compressor(object):
        """Bzip2 compression"""
        __module__ = __name__
        file_pattern = '%s.%d.bz2'

        def compress(self, filename):
            dfn = filename + '.1.bz2'
            if os.path.exists(dfn):
                os.remove(dfn)
            zf = bz2.BZ2File(dfn, 'w')
            zf.write(file(filename, 'rb').read())
            zf.close()
            os.remove(filename)


else:
    Bzip2Compressor = NoneCompressor

def getCompressor(compression):
    """->compressor object"""
    compressors = {'none': NoneCompressor, 'zip': ZipCompressor, 'gzip': GzipCompressor, 'bzip2': Bzip2Compressor}
    klass = compressors.get(compression, NoneCompressor)
    return klass()


class RotateFileHandlerFactory(FileHandlerFactory):
    """Our factory referenced from the component.xml"""
    __module__ = __name__

    def create_loghandler(self):
        """Mandatory override"""
        return RotateFileHandler(self.section.path, self.section.max_bytes, self.section.backup_count, self.section.compression)