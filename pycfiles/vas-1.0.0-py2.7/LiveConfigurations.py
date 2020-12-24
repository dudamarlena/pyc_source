# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/web_server/LiveConfigurations.py
# Compiled at: 2012-11-01 11:36:39
from vas.shared.Collection import Collection
import vas.shared.LiveConfiguration

class LiveConfigurations(Collection):
    """Used to enumerate an instance's live configuration

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(LiveConfigurations, self).__init__(client, location, 'live-configurations', LiveConfiguration)


class LiveConfiguration(vas.shared.LiveConfiguration.LiveConfiguration):
    """A live configuration file in a Web Server instance

    :ivar str                                   content:                The configuration's content
    :ivar `vas.web_server.Instances.Instance`   instance:               The instance that owns the configuration
    :ivar str                                   path:                   The configuration's path
    :ivar list                                  node_configurations:    The configuration's node configurations
    :ivar `vas.shared.Security.Security`        security:               The resource's security
    :ivar int                                   size:                   The configuration's size
    """

    def __init__(self, client, location):
        super(LiveConfiguration, self).__init__(client, location, 'group-instance', Instance, NodeLiveConfiguration)


from vas.web_server.Instances import Instance
from vas.web_server.NodeLiveConfigurations import NodeLiveConfiguration