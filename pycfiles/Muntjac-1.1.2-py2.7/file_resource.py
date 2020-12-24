# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/file_resource.py
# Compiled at: 2013-04-04 15:36:36
"""File or directory resources on the local filesystem."""
from os.path import getsize, basename
from muntjac.service.file_type_resolver import FileTypeResolver
from muntjac.terminal.application_resource import IApplicationResource
from muntjac.terminal.download_stream import DownloadStream
from muntjac.terminal.terminal import IErrorEvent

class FileResource(IApplicationResource):
    """C{FileResources} are files or directories on local filesystem. The
    files and directories are served through URI:s to the client terminal
    and thus must be registered to an URI context before they can be used.
    The resource is automatically registered to the application when it is
    created.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, sourceFile, application):
        """Creates a new file resource for providing given file for
        client terminals.
        """
        self._bufferSize = 0
        self._sourceFile = None
        self._application = None
        self._cacheTime = DownloadStream.DEFAULT_CACHETIME
        self._application = application
        self.setSourceFile(sourceFile)
        application.addResource(self)
        return

    def getStream(self):
        """Gets the resource as stream.

        @see: L{IApplicationResource.getStream}
        """
        try:
            ds = DownloadStream(file(self._sourceFile, 'rb'), self.getMIMEType(), self.getFilename())
            length = str(getsize(self._sourceFile))
            ds.setParameter('Content-Length', length)
            ds.setCacheTime(self._cacheTime)
            return ds
        except IOError:

            class Error(IErrorEvent):

                def getThrowable(self):
                    return self.e

            self.getApplication().getErrorHandler().terminalError(Error())
            return

        return

    def getSourceFile(self):
        """Gets the source file.

        @return: the source File.
        """
        return self._sourceFile

    def setSourceFile(self, sourceFile):
        """Sets the source file.

        @param sourceFile:
                   the source file to set.
        """
        self._sourceFile = sourceFile

    def getApplication(self):
        """@see: L{IApplicationResource.getApplication}"""
        return self._application

    def getFilename(self):
        """@see: L{IApplicationResource.getFilename}"""
        return basename(self._sourceFile)

    def getMIMEType(self):
        """@see: L{IResource.getMIMEType}"""
        return FileTypeResolver.getMIMEType(self._sourceFile)

    def getCacheTime(self):
        """Gets the length of cache expiration time. This gives the adapter
        the possibility cache streams sent to the client. The caching may be
        made in adapter or at the client if the client supports caching.
        Default is C{DownloadStream.DEFAULT_CACHETIME}.

        @return: Cache time in milliseconds.
        """
        return self._cacheTime

    def setCacheTime(self, cacheTime):
        """Sets the length of cache expiration time. This gives the adapter
        the possibility cache streams sent to the client. The caching may be
        made in adapter or at the client if the client supports caching. Zero
        or negavive value disbales the caching of this stream.

        @param cacheTime:
                   the cache time in milliseconds.
        """
        self._cacheTime = cacheTime

    def getBufferSize(self):
        return self._bufferSize

    def setBufferSize(self, bufferSize):
        """Sets the size of the download buffer used for this resource.

        @param bufferSize:
                   the size of the buffer in bytes.
        """
        self._bufferSize = bufferSize