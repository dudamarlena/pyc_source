# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/archive/zip.py
# Compiled at: 2014-01-22 11:28:00
from cStringIO import StringIO
import zipfile
from ztfy.file.interfaces import IArchiveExtractor
from zope.component import queryUtility
from zope.interface import implements
from ztfy.extfile import getMagicContentType

class ZipArchiveExtractor(object):
    """ZIP file format archive extractor"""
    implements(IArchiveExtractor)

    def initialize(self, data, mode='r'):
        if isinstance(data, tuple):
            data = data[0]
        self.zip_data = zipfile.ZipFile(StringIO(data), mode=mode)

    def getContents(self):
        members = self.zip_data.infolist()
        for member in members:
            filename = member.filename
            content = self.zip_data.read(filename)
            mime_type = getMagicContentType(content[:4096])
            extractor = queryUtility(IArchiveExtractor, name=mime_type)
            if extractor is not None:
                extractor.initialize(content)
                for element in extractor.getContents():
                    yield element

            else:
                yield (
                 content, filename)

        return