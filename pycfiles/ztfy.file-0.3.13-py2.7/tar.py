# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/file/archive/tar.py
# Compiled at: 2014-01-22 11:27:50
from cStringIO import StringIO
import tarfile
from ztfy.file.interfaces import IArchiveExtractor
from zope.component import queryUtility
from zope.interface import implements
from ztfy.extfile import getMagicContentType

class TarArchiveExtractor(object):
    """TAR file format archive extractor"""
    implements(IArchiveExtractor)

    def initialize(self, data, mode='r'):
        if isinstance(data, tuple):
            data = data[0]
        self.tar = tarfile.open(fileobj=StringIO(data), mode=mode)

    def getContents(self):
        members = self.tar.getmembers()
        for member in members:
            filename = member.name
            content = self.tar.extractfile(member)
            if content is not None:
                content = content.read()
            if not content:
                continue
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