# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/gemfire/Statistics.py
# Compiled at: 2012-11-01 11:37:44
from datetime import datetime
from vas.shared.Deletable import Deletable
from vas.shared.MutableCollection import MutableCollection
from vas.shared.Resource import Resource
from vas.util.LinkUtils import LinkUtils

class Statistics(MutableCollection):
    """Used to enumerate and delete a cache server's statistics

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(Statistics, self).__init__(client, location, 'statistics', Statistic)


class Statistic(Resource, Deletable):
    """A statistic of a cache server

    :ivar str                                                               content:        The statistic's content
    :ivar `vas.gemfire.CacheServerNodeInstances.CacheServerNodeInstance`    instance:       The statistic's cache server
                                                                                            node instance
    :ivar `datetime.datetime`                                               last_modified:  The last modified stamp of
                                                                                            the statistic
    :ivar str                                                               path:           the path of the statistic
    :ivar `vas.shared.Security.Security`                                    security:       The resource's security
    :ivar int                                                               size:           The size of the statistic
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
    def path(self):
        return self.__path

    @property
    def size(self):
        return self.__size

    def __init__(self, client, location):
        super(Statistic, self).__init__(client, location)
        self.__path = self._details['path']
        self.__instance_location = LinkUtils.get_link_href(self._details, 'cache-server-node-instance')
        self.__content_location = LinkUtils.get_link_href(self._details, 'content')

    def reload(self):
        super(Statistic, self).reload()
        self.__last_modified = datetime.utcfromtimestamp(self._details['last-modified'])
        self.__size = self._details['size']

    def __str__(self):
        return ('<{} path={} size={} last_modified={}>').format(self.__class__.__name__, self.__path, self.__size, self.__last_modified)


from vas.gemfire.CacheServerNodeInstances import CacheServerNodeInstance