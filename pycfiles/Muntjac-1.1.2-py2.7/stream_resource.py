# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/stream_resource.py
# Compiled at: 2013-04-04 15:36:36
"""A resource provided to the client directly by the application."""
from muntjac.service.file_type_resolver import FileTypeResolver
from muntjac.terminal.application_resource import IApplicationResource
from muntjac.terminal.download_stream import DownloadStream

class StreamResource(IApplicationResource):
    """C{StreamResource} is a resource provided to the client
    directly by the application. The strean resource is fetched from URI
    that is most often in the context of the application or window. The
    resource is automatically registered to window in creation.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, streamSource, filename, application):
        """Creates a new stream resource for downloading from stream.

        @param streamSource:
                   the source Stream.
        @param filename:
                   the name of the file.
        @param application:
                   the Application object.
        """
        self._streamSource = None
        self._MIMEType = None
        self._filename = None
        self._application = application
        self._bufferSize = 0
        self._cacheTime = self.DEFAULT_CACHETIME
        self.setFilename(filename)
        self.setStreamSource(streamSource)
        application.addResource(self)
        return

    def getMIMEType(self):
        """@see: IResource.getMIMEType"""
        if self._MIMEType is not None:
            return self._MIMEType
        else:
            return FileTypeResolver.getMIMEType(self._filename)

    def setMIMEType(self, MIMEType):
        """Sets the mime type of the resource.

        @param MIMEType:
                   the MIME type to be set.
        """
        self._MIMEType = MIMEType

    def getStreamSource(self):
        """Returns the source for this C{StreamResource}.
        StreamSource is queried when the resource is about to be streamed
        to the client.

        @return: Source of the StreamResource.
        """
        return self._streamSource

    def setStreamSource(self, streamSource):
        """Sets the source for this C{StreamResource}.
        C{StreamSource} is queried when the resource is
        about to be streamed to the client.

        @param streamSource:
                   the source to set.
        """
        self._streamSource = streamSource

    def getFilename(self):
        """Gets the filename.

        @return: the filename.
        """
        return self._filename

    def setFilename(self, filename):
        """Sets the filename.

        @param filename:
                   the filename to set.
        """
        self._filename = filename

    def getApplication(self):
        """@see: L{IApplicationResource.getApplication}"""
        return self._application

    def getStream(self):
        """@see: L{IApplicationResource.getStream}"""
        ss = self.getStreamSource()
        if ss is None:
            return
        else:
            ds = DownloadStream(ss.getStream(), self.getMIMEType(), self.getFilename())
            ds.setBufferSize(self.getBufferSize())
            ds.setCacheTime(self._cacheTime)
            return ds

    def getBufferSize(self):
        return self._bufferSize

    def setBufferSize(self, bufferSize):
        """Sets the size of the download buffer used for this resource.

        @param bufferSize:
                   the size of the buffer in bytes.
        """
        self._bufferSize = bufferSize

    def getCacheTime(self):
        return self._cacheTime

    def setCacheTime(self, cacheTime):
        """Sets the length of cache expiration time.

        This gives the adapter the possibility cache streams sent to
        the client. The caching may be made in adapter or at the client
        if the client supports caching. Zero or negative value disables
        the caching of this stream.

        @param cacheTime:
                   the cache time in milliseconds.
        """
        self._cacheTime = cacheTime


class IStreamSource(object):
    """Interface implemented by the source of a StreamResource.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def getStream(self):
        """Returns new input stream that is used for reading the resource."""
        pass