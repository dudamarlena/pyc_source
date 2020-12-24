# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/web_server/Instances.py
# Compiled at: 2012-11-01 11:36:39
import vas.shared.Instance
from vas.shared.MutableCollection import MutableCollection

class Instances(MutableCollection):
    """Used to enumerate, create, and delete Web Server instances

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(Instances, self).__init__(client, location, 'group-instances', Instance)

    def create(self, installation, name, properties=None):
        """Creates a new instance

        :param `vas.web_server.Installations.Installation`  installation:   The installation to be used by the instance
        :param str                                          name:           The name of the instance
        :param dict                                         properties:     Optional properties to use when creating the
                                                                            instance
        :rtype:     :class:`vas.web_server.Instances.Instance`
        :return:    The new instance
        """
        payload = {'installation': installation._location, 'name': name}
        if properties:
            payload['properties'] = properties
        return self._create(payload, 'group-instance')


class Instance(vas.shared.Instance.Instance):
    """A Web Server instance

    :ivar `vas.web_server.Groups.Group`                 group:          The group that contains this instance
    :ivar `vas.web_server.Installations.Installation`   installation:   The installation that this instance is using
    :ivar `vas.web_server.LiveConfigurations.LiveConfigurations`    live_configurations:    The instance's live
                                                                                            configurations
    :ivar str                                           name:           The instance's name
    :ivar list                                          node_instances: The instance's individual node instances
    :ivar `vas.web_server.PendingConfigurations.PendingConfigurations`  pending_configurations: The instance's pending
                                                                                                configurations
    :ivar `vas.shared.Security.Security`                security:       The resource's security
    :ivar str                                           state:          Retrieves the state of the resource from the
                                                                        server. Will be one of:

                                                                        * ``STARTING``
                                                                        * ``STARTED``
                                                                        * ``STOPPING``
                                                                        * ``STOPPED``
    """

    def __init__(self, client, location):
        super(Instance, self).__init__(client, location, Group, Installation, LiveConfigurations, PendingConfigurations, NodeInstance, 'node-instance')

    def update(self, installation):
        """Updates the installation used by the instance

        :param `vas.web_server.Installations.Installation`  installation:   The installation to be used by the instance
        """
        payload = {'installation': installation._location}
        self._client.post(self._location, payload)
        self.reload()


from vas.web_server.Groups import Group
from vas.web_server.Installations import Installation
from vas.web_server.LiveConfigurations import LiveConfigurations
from vas.web_server.NodeInstances import NodeInstance
from vas.web_server.PendingConfigurations import PendingConfigurations