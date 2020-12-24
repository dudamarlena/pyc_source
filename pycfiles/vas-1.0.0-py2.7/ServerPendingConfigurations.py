# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/sqlfire/ServerPendingConfigurations.py
# Compiled at: 2012-11-02 07:59:23
from vas.shared.PendingConfigurations import PendingConfigurations, PendingConfiguration

class ServerPendingConfigurations(PendingConfigurations):
    """Used to enumerate a server instance's pending configuration

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(ServerPendingConfigurations, self).__init__(client, location, ServerPendingConfiguration)


class ServerPendingConfiguration(PendingConfiguration):
    """A server configuration file that is pending

    :ivar str                                           content:    The configuration's content
    :ivar `vas.sqlfire.ServerInstances.ServerInstance`  instance:   The instance that owns the configuration
    :ivar str                                           path:       The configuration's path
    :ivar `vas.shared.Security.Security`                security:   The resource's security
    :ivar int                                           size:       The configuration's size
    """

    def __init__(self, client, location):
        super(ServerPendingConfiguration, self).__init__(client, location, 'server-group-instance', ServerInstance)


from vas.sqlfire.ServerInstances import ServerInstance