# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/external_resource.py
# Compiled at: 2013-04-04 15:36:36
"""For resources fetched from location specified by URLs."""
from muntjac.service.file_type_resolver import FileTypeResolver
from muntjac.terminal.resource import IResource

class ExternalResource(IResource):
    """C{ExternalResource} implements source for resources fetched
    from location specified by URLs. The resources are fetched directly by
    the client terminal and are not fetched trough the terminal adapter.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, sourceURL, mimeType=None):
        """Creates a new download component for downloading directly from
        given URL.

        @param sourceURL:
                   the source URL.
        @param mimeType:
                   the MIME Type
        """
        self._sourceURL = None
        self._mimeType = None
        if mimeType is None:
            if sourceURL is None:
                raise RuntimeError('Source must be non-null')
            self._sourceURL = sourceURL
        else:
            ExternalResource.__init__(self, sourceURL)
            self._mimeType = mimeType
        return

    def getURL(self):
        """Gets the URL of the external resource.

        @return: the URL of the external resource.
        """
        return self._sourceURL

    def getMIMEType(self):
        """Gets the MIME type of the resource.

        @see: L{muntjac.terminal.resource.IResource.getMIMEType}
        """
        if self._mimeType is None:
            self._mimeType = FileTypeResolver.getMIMEType(self.getURL())
        return self._mimeType

    def setMIMEType(self, mimeType):
        """Sets the MIME type of the resource."""
        self._mimeType = mimeType