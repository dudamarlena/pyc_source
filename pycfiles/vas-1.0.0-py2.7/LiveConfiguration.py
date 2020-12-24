# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/shared/LiveConfiguration.py
# Compiled at: 2012-11-01 11:35:36
from vas.shared.Configuration import Configuration

class LiveConfiguration(Configuration):
    """A live configuration file in an instance

    :ivar str                               content:                The configuration's content
    :ivar `vas.shared.Instance.Instance`    instance:               The instance that owns the configuration
    :ivar str                               path:                   The configuration's path
    :ivar list                              node_configurations:    The configuration's node configurations
    :ivar `vas.shared.Security.Security`    security:               The resource's security
    :ivar int                               size:                   The configuration's size
    """

    @property
    def node_configurations(self):
        self.__node_live_configurations = self.__node_live_configurations or self._create_resources_from_links('node-live-configuration', self.__node_live_configuration_class)
        return self.__node_live_configurations

    def __init__(self, client, location, instance_type, instance_class, node_live_configuration_class):
        super(LiveConfiguration, self).__init__(client, location, instance_type, instance_class)
        self.__node_live_configuration_class = node_live_configuration_class

    def reload(self):
        """Reloads the live configuration's details from the server"""
        super(LiveConfiguration, self).reload()
        self.__node_live_configurations = None
        return