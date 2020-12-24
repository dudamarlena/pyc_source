# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/archive/gz.py
# Compiled at: 2019-12-19 10:46:04
# Size of source mod 2**32: 1911 bytes
__doc__ = 'PyAMS_file.archive.gz module\n\nGZip files extraction module.\n'
import gzip
from io import BytesIO
from pyams_file.archive.tar import TarArchiveExtractor
from pyams_file.file import get_magic_content_type
from pyams_file.interfaces.archive import IArchiveExtractor
from pyams_utils.registry import utility_config
__docformat__ = 'restructuredtext'

@utility_config(name='application/x-gzip', provides=IArchiveExtractor)
class GZipArchiveExtractor:
    """GZipArchiveExtractor"""
    data = None
    gzip_file = None

    def initialize(self, data):
        """Initialize extractor"""
        if isinstance(data, tuple):
            data = data[0]
        if not hasattr(data, 'read'):
            data = BytesIO(data)
        self.data = data
        self.gzip_file = gzip.GzipFile(fileobj=data, mode='r')

    def get_contents(self):
        """Extract archive contents"""
        gzip_data = self.gzip_file.read(4096)
        mime_type = get_magic_content_type(gzip_data)
        if mime_type == 'application/x-tar':
            tar = TarArchiveExtractor()
            tar.initialize(self.data, mode='r:gz')
            for element in tar.get_contents():
                yield element

        else:
            next_data = self.gzip_file.read()
            while next_data:
                gzip_data += next_data
                next_data = self.gzip_file.read()

            yield (
             gzip_data, '')