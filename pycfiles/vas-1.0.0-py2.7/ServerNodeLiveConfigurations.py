# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/sqlfire/ServerNodeLiveConfigurations.py
# Compiled at: 2012-11-02 07:59:23
from vas.shared.Collection import Collection
from vas.shared.NodeConfiguration import NodeConfiguration

class ServerNodeLiveConfigurations(Collection):
    """Used to enumerate a server node instance's live configuration

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(ServerNodeLiveConfigurations, self).__init__(client, location, 'node-live-configurations', ServerNodeLiveConfiguration)


class ServerNodeLiveConfiguration(NodeConfiguration):
    """A live configuration file in a server node instance

    :ivar str                                                   content:    The configuration's content
    :ivar `vas.sqlfire.ServerLiveConfigurations.ServerLiveConfiguration`    group_configuration:    The node configuration's
                                                                                                    group configuration
    :ivar `vas.sqlfire.ServerNodeInstances.ServerNodeInstance`  instance:   The instance the owns the configuration
    :ivar str                                                   path:       The configuration's path
    :ivar `vas.shared.Security.Security`                        security:   The resource's security
    :var int                                                    size:       The configuration's size
    """

    def __init__(self, client, location):
        super(ServerNodeLiveConfiguration, self).__init__(client, location, 'server-node-instance', ServerNodeInstance, ServerLiveConfiguration)


from vas.sqlfire.ServerLiveConfigurations import ServerLiveConfiguration
from vas.sqlfire.ServerNodeInstances import ServerNodeInstance