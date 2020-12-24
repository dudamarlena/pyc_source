# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/archive/gz.py
# Compiled at: 2014-01-22 11:27:39
from cStringIO import StringIO
import gzip
from ztfy.file.interfaces import IArchiveExtractor
from zope.interface import implements
from ztfy.extfile import getMagicContentType
from ztfy.file.archive.tar import TarArchiveExtractor

class GZipArchiveExtractor(object):
    """GZip file format archive extractor"""
    implements(IArchiveExtractor)

    def initialize(self, data):
        if isinstance(data, tuple):
            data = data[0]
        self.data = data
        self.gzip_file = gzip.GzipFile(fileobj=StringIO(data), mode='r')

    def getContents(self):
        gzip_data = self.gzip_file.read(4096)
        mime_type = getMagicContentType(gzip_data)
        if mime_type == 'application/x-tar':
            tar = TarArchiveExtractor()
            tar.initialize(self.data, mode='r:gz')
            for element in tar.getContents():
                yield element

        else:
            next_data = self.gzip_file.read()
            while next_data:
                gzip_data += next_data
                next_data = self.gzip_file.read()

            yield (
             gzip_data, '')