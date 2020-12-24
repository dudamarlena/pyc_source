# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/rabbitmq/RabbitMq.py
# Compiled at: 2012-11-01 11:37:44
from vas.util.LinkUtils import LinkUtils

class RabbitMq(object):
    """The entry point to the API for administering RabbitMQ

    :ivar `vas.rabbitmq.Groups.Groups`                          groups:                 The RabbitMQ groups
    :ivar `vas.rabbitmq.InstallationImages.InstallationImages`  installation_images:    The RabbitMQ installation images
    :ivar `vas.rabbitmq.Nodes.Nodes`                            nodes:                  The RabbitMQ nodes
    :ivar `vas.rabbitmq.PluginImages.PluginImages`              plugin_images:          The RabbitMQ plugin images
    """

    @property
    def groups(self):
        return self.__groups

    @property
    def installation_images(self):
        return self.__installation_images

    @property
    def nodes(self):
        return self.__nodes

    @property
    def plugin_images(self):
        return self.__plugin_images

    def __init__(self, client, location):
        self.__client = client
        self.__location = location
        json = client.get(location)
        self.__groups = Groups(client, LinkUtils.get_link_href(json, 'groups'))
        self.__installation_images = InstallationImages(client, LinkUtils.get_link_href(json, 'installation-images'))
        self.__nodes = Nodes(client, LinkUtils.get_link_href(json, 'nodes'))
        self.__plugin_images = PluginImages(client, LinkUtils.get_link_href(json, 'plugin-images'))

    def __repr__(self):
        return ('{}(client={}, location={})').format(self.__class__.__name__, self.__client, repr(self.__location))

    def __str__(self):
        return ('<{}>').format(self.__class__.__name__)


from vas.rabbitmq.Groups import Groups
from vas.rabbitmq.InstallationImages import InstallationImages
from vas.rabbitmq.Nodes import Nodes
from vas.rabbitmq.PluginImages import PluginImages