# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/gemfire/CacheServerNodeLiveConfigurations.py
# Compiled at: 2012-11-01 11:35:36
from vas.shared.Collection import Collection
from vas.shared.NodeConfiguration import NodeConfiguration

class CacheServerNodeLiveConfigurations(Collection):
    """Used to enumerate a cache server node instance's live configuration

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(CacheServerNodeLiveConfigurations, self).__init__(client, location, 'node-live-configurations', CacheServerNodeLiveConfiguration)


class CacheServerNodeLiveConfiguration(NodeConfiguration):
    """A live configuration file in a cache server node instance

    :ivar str                                                               content:    The configuration's content
    :ivar `vas.gemfire.CacheServerLiveConfigurations.CacheServerLiveConfiguration`  group_configuration:    The node configuration's
                                                                                                            group configuration
    :ivar `vas.gemfire.CacheServerNodeInstances.CacheServerNodeInstance`    instance:   The instance the owns the
                                                                                        configuration
    :ivar str                                                               path:       The configuration's path
    :ivar `vas.shared.Security.Security`                                    security:   The resource's security
    :var int                                                                size:       The configuration's size
    """

    def __init__(self, client, location):
        super(CacheServerNodeLiveConfiguration, self).__init__(client, location, 'cache-server-node-instance', CacheServerNodeInstance, CacheServerLiveConfiguration)


from vas.gemfire.CacheServerLiveConfigurations import CacheServerLiveConfiguration
from vas.gemfire.CacheServerNodeInstances import CacheServerNodeInstance