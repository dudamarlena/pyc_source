# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/sqlfire/ServerLiveConfigurations.py
# Compiled at: 2012-11-02 07:59:23
from vas.shared.Collection import Collection
from vas.shared.LiveConfiguration import LiveConfiguration

class ServerLiveConfigurations(Collection):
    """Used to enumerate a server instance's live configuration

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(ServerLiveConfigurations, self).__init__(client, location, 'live-configurations', ServerLiveConfiguration)


class ServerLiveConfiguration(LiveConfiguration):
    """A live configuration file in a server instance

    :ivar str                                           content:                The configuration's content
    :ivar `vas.sqlfire.ServerInstances.ServerInstance`  instance:               The instance that owns the configuration
    :ivar str                                           path:                   The configuration's path
    :ivar list                                          node_configurations:    The configuration's node configurations
    :ivar `vas.shared.Security.Security`                security:               The resource's security
    :ivar int                                           size:                   The configuration's size
    """

    def __init__(self, client, location):
        super(ServerLiveConfiguration, self).__init__(client, location, 'server-group-instance', ServerInstance, ServerNodeLiveConfiguration)


from vas.sqlfire.ServerInstances import ServerInstance
from vas.sqlfire.ServerNodeLiveConfigurations import ServerNodeLiveConfiguration