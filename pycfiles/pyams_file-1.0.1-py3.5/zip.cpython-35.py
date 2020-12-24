# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/archive/zip.py
# Compiled at: 2019-12-20 07:09:55
# Size of source mod 2**32: 1930 bytes
"""PyAMS_file.archive.zip module

ZIP files extraction module.
"""
import zipfile
from io import BytesIO
from pyams_file.file import get_magic_content_type
from pyams_file.interfaces.archive import IArchiveExtractor
from pyams_utils.registry import query_utility, utility_config
__docformat__ = 'restructuredtext'

@utility_config(name='application/zip', provides=IArchiveExtractor)
class ZipArchiveExtractor:
    __doc__ = 'ZIP file format archive extractor'
    zip_data = None

    def initialize(self, data, mode='r'):
        """Initialize extractor"""
        if isinstance(data, tuple):
            data = data[0]
        if not hasattr(data, 'read'):
            data = BytesIO(data)
        self.zip_data = zipfile.ZipFile(data, mode=mode)

    def get_contents(self):
        """Extract archive contents"""
        members = self.zip_data.infolist()
        for member in members:
            filename = member.filename
            content = self.zip_data.read(filename)
            if not content:
                pass
            else:
                mime_type = get_magic_content_type(content[:4096])
                extractor = query_utility(IArchiveExtractor, name=mime_type)
                if extractor is not None:
                    extractor.initialize(content)
                    for element in extractor.get_contents():
                        yield element

                else:
                    yield (
                     content, filename)