# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/archive/bz2.py
# Compiled at: 2019-12-19 10:46:04
# Size of source mod 2**32: 2202 bytes
__doc__ = 'PyAMS_file.archive.bz2 module\n\nBzip2 extraction module.\n'
import bz2
from pyams_file.archive.tar import TarArchiveExtractor
from pyams_file.file import get_magic_content_type
from pyams_file.interfaces.archive import IArchiveExtractor
from pyams_utils.registry import utility_config
__docformat__ = 'restructuredtext'
CHUNK_SIZE = 4096

@utility_config(name='application/x-bzip2', provides=IArchiveExtractor)
class BZip2ArchiveExtractor:
    """BZip2ArchiveExtractor"""
    data = None
    bz2 = None

    def initialize(self, data):
        """Initialize extractor"""
        if isinstance(data, tuple):
            data = data[0]
        self.data = data
        self.bz2 = bz2.BZ2Decompressor()

    def get_contents(self):
        """Extract archive contents"""
        position = 0
        compressed = self.data[position:position + CHUNK_SIZE]
        decompressed = self.bz2.decompress(compressed)
        while not decompressed and position < len(self.data):
            compressed = self.data[position:position + CHUNK_SIZE]
            decompressed = self.bz2.decompress(compressed)
            position += CHUNK_SIZE

        mime_type = get_magic_content_type(decompressed[:CHUNK_SIZE])
        if mime_type == 'application/x-tar':
            tar = TarArchiveExtractor()
            tar.initialize(self.data, mode='r:bz2')
            for element in tar.get_contents():
                yield element

        else:
            while position < len(self.data):
                compressed = self.data[position:position + CHUNK_SIZE]
                decompressed += self.bz2.decompress(compressed)
                position += CHUNK_SIZE

            yield (
             decompressed, '')