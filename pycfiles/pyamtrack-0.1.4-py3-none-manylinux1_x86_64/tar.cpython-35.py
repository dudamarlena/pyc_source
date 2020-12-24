# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/archive/tar.py
# Compiled at: 2019-12-19 10:46:04
# Size of source mod 2**32: 1961 bytes
__doc__ = 'PyAMS_file.archive.tar module\n\nTAR files extraction module.\n'
import tarfile
from io import BytesIO
from pyams_file.file import get_magic_content_type
from pyams_file.interfaces.archive import IArchiveExtractor
from pyams_utils.registry import query_utility, utility_config
__docformat__ = 'restructuredtext'

@utility_config(name='application/x-tar', provides=IArchiveExtractor)
class TarArchiveExtractor:
    """TarArchiveExtractor"""
    tar = None

    def initialize(self, data, mode='r'):
        """Initialize extractor"""
        if isinstance(data, tuple):
            data = data[0]
        if not hasattr(data, 'read'):
            data = BytesIO(data)
        self.tar = tarfile.open(fileobj=data, mode=mode)

    def get_contents(self):
        """Extract archive contents"""
        members = self.tar.getmembers()
        for member in members:
            filename = member.name
            content = self.tar.extractfile(member)
            if content is not None:
                content = content.read()
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