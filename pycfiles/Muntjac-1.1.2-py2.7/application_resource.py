# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/application_resource.py
# Compiled at: 2013-04-04 15:36:36
"""Interface implemented by classes wishing to provide application
resources."""
from muntjac.terminal.resource import IResource

class IApplicationResource(IResource):
    """This interface must be implemented by classes wishing to provide
    Application resources.

    C{IApplicationResource} are a set of named resources (pictures, sounds,
    etc) associated with some specific application. Having named application
    resources provides a convenient method for having inter-theme common
    resources for an application.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    DEFAULT_CACHETIME = 86400000

    def getStream(self):
        """Gets resource as stream."""
        raise NotImplementedError

    def getApplication(self):
        """Gets the application of the resource."""
        raise NotImplementedError

    def getFilename(self):
        """Gets the virtual filename for this resource.

        @return: the file name associated to this resource.
        """
        raise NotImplementedError

    def getCacheTime(self):
        """Gets the length of cache expiration time.

        This gives the adapter the possibility cache streams sent to the
        client. The caching may be made in adapter or at the client if the
        client supports caching. Default is C{DEFAULT_CACHETIME}.

        @return: Cache time in milliseconds
        """
        raise NotImplementedError

    def getBufferSize(self):
        """Gets the size of the download buffer used for this resource.

        If the buffer size is 0, the buffer size is decided by the terminal
        adapter. The default value is 0.

        @return: the size of the buffer in bytes.
        """
        raise NotImplementedError