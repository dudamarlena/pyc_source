# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/rabbitmq/Plugins.py
# Compiled at: 2012-11-01 11:37:44
from vas.shared.Deletable import Deletable
from vas.shared.MutableCollection import MutableCollection
from vas.shared.Resource import Resource
from vas.util.LinkUtils import LinkUtils

class Plugins(MutableCollection):
    """Used to enumerate, create, and delete plugins

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(Plugins, self).__init__(client, location, 'plugins', Plugin)

    def create(self, plugin_image):
        """Creates a plugin from the ``plugin_image``

        :param `vas.rabbitmq.PluginImages.PluginImage`  plugin_image:   The plugin image to create the plugin from
        :rtype:     :class:`vas.rabbitmq.Plugins.Plugin`
        :return:    The new plugin
        """
        return self._create({'image': plugin_image._location}, 'plugin')


class Plugin(Resource, Deletable):
    """A plugin in a RabbitMQ instance

    :ivar `vas.rabbitmq.Instances.Instance`         instance:       The instance that contains the plugin
    :ivar str                                       name:           The plugin's name
    :ivar `vas.rabbitmq.PluginImages.PluginImage`   plugin_image:   The plugin image, if any, that was used to create
                                                                    the plugin
    :ivar `vas.shared.Security.Security`            security:       The resource's security
    :ivar str                                       state:          Retrieves the state of the plugin from the server.
                                                                    Will be one of:

                                                                    * ``ENABLED``
                                                                    * ``DISABLED``
    :ivar str                                       version:        The plugin's version
    """
    __instance = None
    __plugin_image = None

    @property
    def instance(self):
        self.__instance = self.__instance or Instance(self._client, self.__instance_location)
        return self.__instance

    @property
    def name(self):
        return self.__name

    @property
    def plugin_image(self):
        self.__plugin_image = self.__plugin_image or PluginImage(self._client, self.__plugin_image_location) if self.__plugin_image_location else None
        return self.__plugin_image

    @property
    def state(self):
        return self._client.get(self.__state_location)['status']

    @property
    def version(self):
        return self.__version

    def __init__(self, client, location):
        super(Plugin, self).__init__(client, location)
        self.__name = self._details['name']
        self.__version = self._details['version']
        self.__instance_location = LinkUtils.get_link_href(self._details, 'group-instance')
        self.__plugin_image_location = LinkUtils.get_link_href(self._details, 'plugin-image')
        self.__state_location = LinkUtils.get_link_href(self._details, 'state')

    def disable(self):
        """Disables the plugin"""
        self._client.post(self.__state_location, {'status': 'DISABLED'})

    def enable(self):
        """Enables the plugin"""
        self._client.post(self.__state_location, {'status': 'ENABLED'})

    def __str__(self):
        return ('<{} name={} version={}>').format(self.__class__.__name__, self.__name, self.__version)


from vas.rabbitmq.Instances import Instance
from vas.rabbitmq.PluginImages import PluginImage