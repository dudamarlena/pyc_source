# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/web_server/PendingConfigurations.py
# Compiled at: 2012-11-01 11:36:39
import vas.shared.PendingConfigurations

class PendingConfigurations(vas.shared.PendingConfigurations.PendingConfigurations):
    """Used to enumerate an instance's pending configuration

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(PendingConfigurations, self).__init__(client, location, PendingConfiguration)


class PendingConfiguration(vas.shared.PendingConfigurations.PendingConfiguration):
    """A configuration file that is pending

    :ivar str                                   content:    The configuration's content
    :ivar `vas.web_server.Instances.Instance`    instance:   The instance that owns the configuration
    :ivar str                                   path:       The configuration's path
    :ivar `vas.shared.Security.Security`        security:   The resource's security
    :ivar int                                   size:       The configuration's size
    """

    def __init__(self, client, location):
        super(PendingConfiguration, self).__init__(client, location, 'group-instance', Instance)


from vas.web_server.Instances import Instance