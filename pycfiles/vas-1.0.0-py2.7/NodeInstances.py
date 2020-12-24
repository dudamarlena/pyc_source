# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/web_server/NodeInstances.py
# Compiled at: 2012-11-01 11:36:39
import vas.shared.NodeInstances

class NodeInstances(vas.shared.NodeInstances.NodeInstances):
    """Used to enumerate Web Server instances on an individual node

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(NodeInstances, self).__init__(client, location, 'node-instances', NodeInstance)


class NodeInstance(vas.shared.NodeInstances.NodeInstance):
    """A Web Server node instance

    :ivar `vas.web_server.Instances.Instance`   group_instance:         The node instance's group instance
    :ivar `vas.web_server.LiveConfigurations.LiveConfigurations`    live_configurations:    The node instance's live
                                                                                            configuration
    :ivar `vas.web_server.Logs.Logs`            logs:                   The instance's logs
    :ivar str                                   name:                   The instance's name
    :ivar `vas.web_server.Nodes.Node`           node:                   The node that contains this instance
    :ivar `vas.shared.Security.Security`        security:               The resource's security
    :ivar str                                   state:                  Retrieves the state of the resource from the
                                                                        server. Will be one of:

                                                                        * ``STARTING``
                                                                        * ``STARTED``
                                                                        * ``STOPPING``
                                                                        * ``STOPPED``
    """

    def __init__(self, client, location):
        super(NodeInstance, self).__init__(client, location, Node, Logs, Instance, 'group-instance', NodeLiveConfigurations)


from vas.web_server.Instances import Instance
from vas.web_server.Logs import Logs
from vas.web_server.NodeLiveConfigurations import NodeLiveConfigurations
from vas.web_server.Nodes import Node