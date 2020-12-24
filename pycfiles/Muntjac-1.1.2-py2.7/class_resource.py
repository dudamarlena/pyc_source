# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/class_resource.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.service.file_type_resolver import FileTypeResolver
from muntjac.terminal.application_resource import IApplicationResource
from muntjac.terminal.download_stream import DownloadStream

class ClassResource(IApplicationResource):
    """C{ClassResource} is a named resource accessed with the
    class loader.

    This can be used to access resources such as icons, files, etc.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, *args):
        """Creates a new application resource instance. The resource id is
        relative to the location of the application class.

        @param args: tuple of the form
            - (resourceName, application)
              1. the Unique identifier of the resource within the application
              2. the application this resource will be added to
            - (associatedClass, resourceName, application)
              1. the class of the which the resource is associated.
              2. the Unique identifier of the resource within the application
              3. the application this resource will be added to
        """
        self._bufferSize = 0
        self._cacheTime = self.DEFAULT_CACHETIME
        self._associatedClass = None
        self._resourceName = None
        self._application = None
        nargs = len(args)
        if nargs == 2:
            resourceName, application = args
            self._associatedClass = application.__class__
            self._resourceName = resourceName
            self._application = application
            if resourceName is None:
                raise ValueError
            application.addResource(self)
        elif nargs == 3:
            associatedClass, resourceName, application = args
            self._associatedClass = associatedClass
            self._resourceName = resourceName
            self._application = application
            if resourceName is None or associatedClass is None:
                raise ValueError
            application.addResource(self)
        else:
            raise ValueError, 'invalid number of arguments'
        return

    def getMIMEType(self):
        """Gets the MIME type of this resource.

        @see: L{muntjac.terminal.resource.IResource.getMIMEType}
        """
        return FileTypeResolver.getMIMEType(self._resourceName)

    def getApplication(self):
        """Gets the application of this resource.

        @see: L{IApplicationResource.getApplication}
        """
        return self._application

    def getFilename(self):
        """Gets the virtual filename for this resource.

        @return: the file name associated to this resource.
        @see: L{IApplicationResource.getFilename}
        """
        index = 0
        idx = self._resourceName.find('/', index)
        while idx > 0 and idx + 1 < len(self._resourceName):
            index = idx + 1
            idx = self._resourceName.find('/', index)

        return self._resourceName[index:]

    def getStream(self):
        """Gets resource as stream.

        @see: L{IApplicationResource.getStream}
        """
        ds = DownloadStream(self._associatedClass.getResourceAsStream(self._resourceName), self.getMIMEType(), self.getFilename())
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

        This gives the adapter the possibility cache streams sent to the
        client. The caching may be made in adapter or at the client if the
        client supports caching. Zero or negative value disables the caching
        of this stream.

        @param cacheTime:
                   the cache time in milliseconds.
        """
        self._cacheTime = cacheTime