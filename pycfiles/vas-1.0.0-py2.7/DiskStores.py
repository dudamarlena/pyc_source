# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/gemfire/DiskStores.py
# Compiled at: 2012-11-01 11:37:44
from datetime import datetime
from vas.shared.Deletable import Deletable
from vas.shared.MutableCollection import MutableCollection
from vas.shared.Resource import Resource
from vas.util.LinkUtils import LinkUtils

class DiskStores(MutableCollection):
    """Provides access to a cache server node instance's disk stores

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(DiskStores, self).__init__(client, location, 'disk-stores', DiskStore)


class DiskStore(Resource, Deletable):
    """A disk store in a cache server node instance

    :ivar str                                                               content:        The disk store's content
    :ivar `vas.gemfire.CacheServerNodeInstances.CacheServerNodeInstance`    instance:       The disk store's cache
                                                                                            server node instance
    :ivar `datetime.datetime`                                               last_modified:  The last modified stamp of
                                                                                            the disk store
    :ivar str                                                               name:           the name of the disk store
    :ivar `vas.shared.Security.Security`                                    security:       The resource's security
    :ivar int                                                               size:           The size of the disk store

    """
    __instance = None

    @property
    def content(self):
        return self._client.get(self.__content_location)

    @property
    def instance(self):
        self.__instance = self.__instance or CacheServerNodeInstance(self._client, self.__instance_location)
        return self.__instance

    @property
    def last_modified(self):
        return self.__last_modified

    @property
    def name(self):
        return self.__name

    @property
    def size(self):
        return self.__size

    def __init__(self, client, location):
        super(DiskStore, self).__init__(client, location)
        self.__name = self._details['name']
        self.__instance_location = LinkUtils.get_link_href(self._details, 'cache-server-node-instance')
        self.__content_location = LinkUtils.get_link_href(self._details, 'content')

    def reload(self):
        """Reloads the disk store's details from the server"""
        super(DiskStore, self).reload()
        self.__last_modified = datetime.utcfromtimestamp(self._details['last-modified'])
        self.__size = self._details['size']

    def __str__(self):
        return ('<{} name={} size={} last_modified={}>').format(self.__class__.__name__, self.__name, self.__size, self.__last_modified)


from vas.gemfire.CacheServerNodeInstances import CacheServerNodeInstance