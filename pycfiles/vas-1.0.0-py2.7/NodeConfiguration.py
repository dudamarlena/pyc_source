# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/shared/NodeConfiguration.py
# Compiled at: 2012-11-01 11:37:44
from vas.shared.Resource import Resource
from vas.util.LinkUtils import LinkUtils

class NodeConfiguration(Resource):
    """A configuration file in a node instance

    :ivar str                                       content:                The configuration's content
    :ivar `vas.shared.Configuration.Configuration`  group_configuration:    The node configuration's group configuration
    :ivar `vas.shared.NodeInstances.NodeInstance`   instance:               The instance the owns the configuration
    :ivar str                                       path:                   The configuration's path
    :ivar `vas.shared.Security.Security`            security:               The resource's security
    :var int                                        size:                   The configuration's size
    """
    __group_configuration = None
    __instance = None

    @property
    def content(self):
        return self._client.get(self.__content_location)

    @property
    def group_configuration(self):
        self.__group_configuration = self.__group_configuration or self.__group_configuration_class(self._client, self.__group_configuration_location)
        return self.__group_configuration

    @property
    def instance(self):
        self.__instance = self.__instance or self.__instance_class(self._client, self.__instance_location)
        return self.__instance

    @property
    def path(self):
        return self.__path

    @property
    def size(self):
        return self.__size

    def __init__(self, client, location, instance_type, instance_class, group_configuration_class):
        super(NodeConfiguration, self).__init__(client, location)
        self.__instance_class = instance_class
        self.__group_configuration_class = group_configuration_class
        self.__instance_location = LinkUtils.get_link_href(self._details, instance_type)
        self.__group_configuration_location = LinkUtils.get_link_href(self._details, 'group-live-configuration')
        self.__content_location = LinkUtils.get_link_href(self._details, 'content')
        self.__path = self._details['path']

    def reload(self):
        """Reloads the configuration's details from the server"""
        super(NodeConfiguration, self).reload()
        self.__size = self._details['size']

    def __str__(self):
        return ('<{} path={} size={}>').format(self.__class__.__name__, self.__path, self.__size)