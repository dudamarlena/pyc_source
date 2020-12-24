# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/gemfire/CacheServerNodeInstances.py
# Compiled at: 2012-11-01 11:35:36
from vas.shared.NodeInstances import NodeInstances, NodeInstance
from vas.util.LinkUtils import LinkUtils

class CacheServerNodeInstances(NodeInstances):
    """Used to enumerate cache server instances on an individual node

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(CacheServerNodeInstances, self).__init__(client, location, 'cache-server-node-instances', CacheServerNodeInstance)


class CacheServerNodeInstance(NodeInstance):
    """A cache server node instance

    :ivar `vas.gemfire.DiskStores.DiskStores`                       disk_stores:    The instance's disk stores
    :ivar `vas.gemfire.CacheServerInstances.CacheServerInstance`    group_instance: The node instance's group instance
    :ivar `vas.gemfire.CacheServerLiveConfigurations.CacheServerLiveConfigurations` live_configurations:    The node instance's
                                                                                                            live configuration
    :ivar `vas.gemfire.CacheServerLogs.CacheServerLogs`             logs:           The instance's logs
    :ivar str                                                       name:           The instance's name
    :ivar `vas.gemfire.Nodes.Nodes`                                 node:           The node that contains this instance
    :ivar `vas.shared.Security.Security`                            security:       The resource's security
    :ivar str                                                       state:          Retrieves the state of the resource
                                                                                    from the server. Will be one of:

                                                                                    * ``STARTING``
                                                                                    * ``STARTED``
                                                                                    * ``STOPPING``
                                                                                    * ``STOPPED``
    :ivar `vas.gemfire.Statistics.Statistics`                       statistics:     The instance's statistics
    """
    __disk_stores = None
    __statistics = None

    @property
    def disk_stores(self):
        self.__disk_stores = self.__disk_stores or DiskStores(self._client, self.__disk_stores_location)
        return self.__disk_stores

    @property
    def statistics(self):
        self.__statistics = self.__statistics or Statistics(self._client, self.__statistics_location)
        return self.__statistics

    def __init__(self, client, location):
        super(CacheServerNodeInstance, self).__init__(client, location, Node, CacheServerLogs, CacheServerInstance, 'cache-server-group-instance', CacheServerNodeLiveConfigurations)
        self.__disk_stores_location = LinkUtils.get_link_href(self._details, 'disk-stores')
        self.__state_location = LinkUtils.get_link_href(self._details, 'state')
        self.__statistics_location = LinkUtils.get_link_href(self._details, 'statistics')

    def start(self, rebalance=None):
        """Starts the resource

        :param bool rebalance:  Whether to rebalance the cache server instance on start
        """
        payload = {'status': 'STARTED'}
        if rebalance is not None:
            payload['rebalance'] = rebalance
        self._client.post(self.__state_location, payload)
        return


from vas.gemfire.CacheServerInstances import CacheServerInstance
from vas.gemfire.CacheServerLogs import CacheServerLogs
from vas.gemfire.CacheServerNodeLiveConfigurations import CacheServerNodeLiveConfigurations
from vas.gemfire.DiskStores import DiskStores
from vas.gemfire.Nodes import Node
from vas.gemfire.Statistics import Statistics