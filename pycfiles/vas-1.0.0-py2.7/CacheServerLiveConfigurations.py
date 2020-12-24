# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/gemfire/CacheServerLiveConfigurations.py
# Compiled at: 2012-11-01 11:35:36
from vas.shared.Collection import Collection
from vas.shared.LiveConfiguration import LiveConfiguration

class CacheServerLiveConfigurations(Collection):
    """Used to enumerate a cache server instance's live configuration

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(CacheServerLiveConfigurations, self).__init__(client, location, 'live-configurations', CacheServerLiveConfiguration)


class CacheServerLiveConfiguration(LiveConfiguration):
    """A live configuration file in a cache server instance

    :ivar str                                                       content:                The configuration's content
    :ivar `vas.gemfire.CacheServerInstances.CacheServerInstance`    instance:               The instance that owns the
                                                                                            configuration
    :ivar str                                                       path:                   The configuration's path
    :ivar list                                                      node_configurations:    The configuration's node
                                                                                            configurations
    :ivar `vas.shared.Security.Security`                            security:               The resource's security
    :ivar int                                                       size:                   The configuration's size
    """

    def __init__(self, client, location):
        super(CacheServerLiveConfiguration, self).__init__(client, location, 'cache-server-group-instance', CacheServerInstance, CacheServerNodeLiveConfiguration)


from vas.gemfire.CacheServerInstances import CacheServerInstance
from vas.gemfire.CacheServerNodeLiveConfigurations import CacheServerNodeLiveConfiguration