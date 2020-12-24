# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/archive/bz2.py
# Compiled at: 2014-01-22 11:27:30
import bz2
from ztfy.file.interfaces import IArchiveExtractor
from zope.interface import implements
from ztfy.extfile import getMagicContentType
from ztfy.file.archive.tar import TarArchiveExtractor
CHUNK_SIZE = 4096

class BZip2ArchiveExtractor(object):
    """BZip2 file format archive extractor"""
    implements(IArchiveExtractor)

    def initialize(self, data):
        if isinstance(data, tuple):
            data = data[0]
        self.data = data
        self.bz2 = bz2.BZ2Decompressor()

    def getContents(self):
        position = 0
        compressed = self.data[position:position + CHUNK_SIZE]
        decompressed = self.bz2.decompress(compressed)
        while not decompressed and position < len(self.data):
            compressed = self.data[position:position + CHUNK_SIZE]
            decompressed = self.bz2.decompress(compressed)
            position += CHUNK_SIZE

        mime_type = getMagicContentType(decompressed[:CHUNK_SIZE])
        if mime_type == 'application/x-tar':
            tar = TarArchiveExtractor()
            tar.initialize(self.data, mode='r:bz2')
            for element in tar.getContents():
                yield element

        else:
            while position < len(self.data):
                compressed = self.data[position:position + CHUNK_SIZE]
                decompressed += self.bz2.decompress(compressed)
                position += CHUNK_SIZE

            yield (
             decompressed, '')