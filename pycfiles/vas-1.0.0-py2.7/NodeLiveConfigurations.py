# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/web_server/NodeLiveConfigurations.py
# Compiled at: 2012-11-01 11:36:39
from vas.shared.Collection import Collection
from vas.shared.NodeConfiguration import NodeConfiguration

class NodeLiveConfigurations(Collection):
    """Used to enumerate a node instance's live configuration

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(NodeLiveConfigurations, self).__init__(client, location, 'node-live-configurations', NodeLiveConfiguration)


class NodeLiveConfiguration(NodeConfiguration):
    """A live configuration file in a node instance

    :ivar str                                                   content:                The configuration's content
    :ivar `vas.web_server.LiveConfigurations.LiveConfiguration` group_configuration:    The node configuration's group
                                                                                        configuration
    :ivar `vas.web_server.NodeInstances.NodeInstance`           instance:               The instance the owns the
                                                                                        configuration
    :ivar str                                                   path:                   The configuration's path
    :ivar `vas.shared.Security.Security`                        security:               The resource's security
    :var int                                                    size:                   The configuration's size
    """

    def __init__(self, client, location):
        super(NodeLiveConfiguration, self).__init__(client, location, 'node-instance', NodeInstance, LiveConfiguration)


from vas.web_server.LiveConfigurations import LiveConfiguration
from vas.web_server.NodeInstances import NodeInstance