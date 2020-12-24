# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/shared/Instance.py
# Compiled at: 2012-11-01 11:37:44
from vas.shared.Deletable import Deletable
from vas.shared.Resource import Resource
from vas.util.LinkUtils import LinkUtils

class Instance(Resource, Deletable):
    """An instance of a middleware component. Created from an installation that provides the binaries that the instance
    uses at runtime.

    :ivar `vas.shared.Groups.Group`                 group:          The group that contains this instance
    :ivar `vas.shared.Installations.Installation`   installation:   The installation that this instance is using
    :ivar `vas.shared.Collection.Collection`        live_configurations:    The instance's live configurations
    :ivar str                                       name:           The instance's name
    :ivar list                                      node_instances: The instance's individual node instances
    :ivar `vas.shared.PendingConfigurations.PendingConfigurations`  pending_configurations: The instance's pending
                                                                                            configurations
    :ivar `vas.shared.Security.Security`            security:       The resource's security
    :ivar str                                       state:          Retrieves the state of the resource from the server.
                                                                    Will be one of:

                                                                    * ``STARTING``
                                                                    * ``STARTED``
                                                                    * ``STOPPING``
                                                                    * ``STOPPED``
    """
    __group = None
    __live_configurations = None
    __pending_configurations = None

    @property
    def group(self):
        self.__group = self.__group or self.__group_class(self._client, self.__group_location)
        return self.__group

    @property
    def installation(self):
        self.__installation = self.__installation or self.__installation_class(self._client, self.__installation_location)
        return self.__installation

    @property
    def live_configurations(self):
        self.__live_configurations = self.__live_configurations or self.__live_configurations_class(self._client, self.__live_configurations_location)
        return self.__live_configurations

    @property
    def name(self):
        return self.__name

    @property
    def node_instances(self):
        self.__node_instances = self.__node_instances or self._create_resources_from_links(self.__node_instance_type, self.__node_instance_class)
        return self.__node_instances

    @property
    def pending_configurations(self):
        self.__pending_configurations = self.__pending_configurations or self.__pending_configurations_class(self._client, self.__pending_configurations_location)
        return self.__pending_configurations

    @property
    def state(self):
        return self._client.get(self.__state_location)['status']

    def __init__(self, client, location, group_class, installation_class, live_configurations_class, pending_configurations_class, node_instance_class, node_instance_type):
        super(Instance, self).__init__(client, location)
        self.__live_configurations_location = LinkUtils.get_link_href(self._details, 'live-configurations')
        self.__pending_configurations_location = LinkUtils.get_link_href(self._details, 'pending-configurations')
        self.__group_location = LinkUtils.get_link_href(self._details, 'group')
        self.__state_location = LinkUtils.get_link_href(self._details, 'state')
        self.__group_class = group_class
        self.__installation_class = installation_class
        self.__node_instance_class = node_instance_class
        self.__live_configurations_class = live_configurations_class
        self.__pending_configurations_class = pending_configurations_class
        self.__node_instance_type = node_instance_type
        self.__name = self._details['name']

    def reload(self):
        """Reloads the instance's details from the server"""
        super(Instance, self).reload()
        self.__installation_location = LinkUtils.get_link_href(self._details, 'installation')
        self.__installation = None
        self.__node_instances = None
        return

    def start(self, serial=False):
        """Starts the resource

        :param bool serial: Whether to start the node instance serially
        """
        self._client.post(self.__state_location, {'status': 'STARTED', 'serial': serial})

    def stop(self, serial=False):
        """Stops the resource

        :param bool serial: Whether to stop the node instance serially
        """
        self._client.post(self.__state_location, {'status': 'STOPPED', 'serial': serial})

    def __str__(self):
        return ('<{} name={}>').format(self.__class__.__name__, self.__name)